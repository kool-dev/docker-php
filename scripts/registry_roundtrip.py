#!/usr/bin/env python3
"""Exercise promotion against an ephemeral loopback registry, never Docker Hub.

Uses tiny synthetic scratch images (no PHP runtime tests, no QEMU). Registry
configuration and the reduced tag set are overridden only in this test process.
"""

import json
import hashlib
import io
import os
from pathlib import Path
import subprocess
import tempfile
import tarfile
import time
from unittest.mock import patch
import uuid

import promote


def docker(*args):
    return subprocess.check_output(["docker", *args], text=True).strip()


def main():
    name = f"php-promotion-test-{uuid.uuid4().hex[:12]}"
    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary)
        # Attached child process; no shell backgrounding or detached container.
        with (directory / "registry.log").open("w+") as log:
            registry = subprocess.Popen(
                ["docker", "run", "--rm", "--name", name, "-p", "127.0.0.1::5000", "registry:2"],
                stdout=log, stderr=subprocess.STDOUT,
            )
            try:
                for _ in range(600):
                    if registry.poll() is not None:
                        log.seek(0)
                        raise RuntimeError(log.read())
                    result = subprocess.run(["docker", "port", name, "5000/tcp"],
                                            capture_output=True, text=True)
                    if result.returncode == 0 and result.stdout.strip():
                        address = result.stdout.strip()
                        break
                    time.sleep(0.1)
                else:
                    raise RuntimeError("Registry did not start")
                repository = f"{address}/php"
                assert repository.startswith("127.0.0.1:")
                tags = {"8.5", "8.5-node"}
                metadata = directory / "metadata"
                (directory / "Dockerfile").write_text("FROM scratch\nCOPY payload /payload\n")
                config_ids = {}
                with patch.object(promote, "REPOSITORY", repository), \
                     patch.object(promote, "expected_tags", return_value=tags), \
                     patch.dict(os.environ, GITHUB_RUN_ID="123", GITHUB_RUN_ATTEMPT="2"):
                    for tag in sorted(tags):
                        for arch in promote.ARCHES:
                            (directory / "payload").write_text(f"{tag}-{arch}\n")
                            iidfile = directory / "image-id"
                            docker("buildx", "build", "--platform", f"linux/{arch}", "--load",
                                   "--provenance=false", "--iidfile", str(iidfile), str(directory))
                            image_id = iidfile.read_text().strip()
                            # Docker's classic store identifies images by config,
                            # while its containerd store may use the manifest ID.
                            saved = subprocess.check_output(["docker", "image", "save", image_id])
                            with tarfile.open(fileobj=io.BytesIO(saved)) as archive:
                                config = json.load(archive.extractfile("manifest.json"))[0]["Config"]
                                config_ids[tag, arch] = "sha256:" + hashlib.sha256(
                                    archive.extractfile(config).read()).hexdigest()
                            promote.stage(tag, arch, image_id, metadata)
                    records = promote.validate(metadata)
                    # Exercise the production publish function without mocking Docker.
                    promote.publish(metadata)
                    for tag in sorted(tags):
                        manifest = json.loads(docker("buildx", "imagetools", "inspect",
                                                     "--raw", f"{repository}:{tag}"))
                        actual = {m["platform"]["architecture"]: m["digest"]
                                  for m in manifest["manifests"]}
                        assert actual == {arch: records[tag, arch]["digest"] for arch in promote.ARCHES}
                        for arch in promote.ARCHES:
                            image_manifest = json.loads(docker(
                                "buildx", "imagetools", "inspect", "--raw",
                                f"{repository}@{actual[arch]}"))
                            assert image_manifest["config"]["digest"] == config_ids[tag, arch]
                    print("PASS: real local-registry staging and manifest publication preserve tested config IDs")
            finally:
                subprocess.run(["docker", "rm", "-f", name], capture_output=True)
                registry.wait(timeout=30)


if __name__ == "__main__":
    main()
