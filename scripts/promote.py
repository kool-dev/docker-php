#!/usr/bin/env python3
"""Stage tested local IDs; validate a whole release; publish manifests only."""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess

REPOSITORY = "kooldev/php"
DIGEST = re.compile(r"sha256:[0-9a-f]{64}")
ARCHES = ("amd64", "arm64")
ROOT = Path(__file__).resolve().parents[1]


def expected_tags():
    return {build["name"] for build in json.loads((ROOT / "fwd-template.json").read_text())["builds"]}


def run(*args):
    return subprocess.check_output(["docker", *args], text=True)


def scope():
    run_id, attempt = os.environ["GITHUB_RUN_ID"], os.environ["GITHUB_RUN_ATTEMPT"]
    if not run_id.isdecimal() or not attempt.isdecimal():
        raise ValueError("Invalid workflow run scope")
    return run_id, attempt


def stage(tag, arch, image_id, directory):
    run_id, attempt = scope()
    if tag not in expected_tags() or arch not in ARCHES or not DIGEST.fullmatch(image_id):
        raise ValueError("Invalid tag, architecture or tested image ID")
    image = json.loads(run("image", "inspect", image_id))[0]
    if (image["Id"], image["Os"], image["Architecture"]) != (image_id, "linux", arch):
        raise ValueError("Tested image ID/platform mismatch")
    staging = f"{REPOSITORY}:ci-php-{run_id}-{attempt}-{tag}-{arch}"
    # Tag the ID, never a mutable local/stable tag.
    run("tag", image_id, staging)
    output = run("push", staging)
    print(output, end="")
    digests = re.findall(r"\bdigest: (sha256:[0-9a-f]{64})\b", output)
    if len(digests) != 1:
        raise ValueError("Push did not report exactly one registry digest")
    directory.mkdir(parents=True, exist_ok=True)
    record = dict(repository=REPOSITORY, tag=tag, arch=arch, image_id=image_id,
                  digest=digests[0], run_id=run_id, run_attempt=attempt)
    (directory / f"{tag}-{arch}.json").write_text(json.dumps(record) + "\n")


def validate(directory):
    run_id, attempt = scope()
    expected = {(tag, arch) for tag in expected_tags() for arch in ARCHES}
    records = {}
    for path in directory.rglob("*.json"):
        record = json.loads(path.read_text())
        key = record["tag"], record["arch"]
        if key not in expected or key in records:
            raise ValueError(f"Unexpected or duplicate tag/architecture: {key}")
        if (record["repository"], record["run_id"], record["run_attempt"]) != (REPOSITORY, run_id, attempt):
            raise ValueError(f"Wrong repository or workflow attempt: {path}")
        if not all(isinstance(record[field], str) and DIGEST.fullmatch(record[field])
                   for field in ("digest", "image_id")):
            raise ValueError(f"Invalid digest/image ID: {path}")
        records[key] = record
    if records.keys() != expected:
        raise ValueError(f"Missing metadata: {sorted(expected - records.keys())}")
    # A single image manifest cannot represent two different native platforms.
    if len({r["digest"] for r in records.values()}) != len(records):
        raise ValueError("Duplicate registry digests")
    return records


def publish(directory):
    # Validate everything before the FIRST stable-tag write, even if called directly.
    records = validate(directory)
    for tag in sorted(expected_tags()):
        sources = [f"{REPOSITORY}@{records[tag, arch]['digest']}" for arch in ARCHES]
        print(run("buildx", "imagetools", "create", "--tag", f"{REPOSITORY}:{tag}", *sources), end="")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("stage", "validate", "publish"))
    parser.add_argument("args", nargs="*")
    parser.add_argument("--directory", type=Path, default=Path("release-metadata"))
    args = parser.parse_args()
    if args.command == "stage" and len(args.args) == 3:
        stage(*args.args, args.directory)
    elif args.command == "validate" and not args.args:
        validate(args.directory)
    elif args.command == "publish" and not args.args:
        publish(args.directory)
    else:
        parser.error("stage requires TAG ARCH IMAGE_ID; validate/publish take no positional arguments")


if __name__ == "__main__":
    main()
