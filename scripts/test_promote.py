import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import promote
import check_parent


def digest(number):
    return f"sha256:{number:064x}"


class PromotionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        env = patch.dict(os.environ, GITHUB_RUN_ID="123", GITHUB_RUN_ATTEMPT="2")
        env.start()
        self.addCleanup(env.stop)
        self.records = []
        for index, (tag, arch) in enumerate(
            (tag, arch) for tag in sorted(promote.expected_tags()) for arch in promote.ARCHES
        ):
            self.records.append(dict(repository="kooldev/php", tag=tag, arch=arch,
                                     digest=digest(index + 1), image_id=digest(index + 100),
                                     run_id="123", run_attempt="2"))

    def write_records(self, records=None):
        for index, record in enumerate(self.records if records is None else records):
            (self.directory / f"{index}.json").write_text(json.dumps(record))

    def assert_rejected_before_write(self, records):
        self.write_records(records)
        with patch.object(promote, "run") as docker:
            with self.assertRaises((ValueError, KeyError)):
                promote.publish(self.directory)
            docker.assert_not_called()

    def test_complete_release_publishes_only_recorded_digests(self):
        self.assertEqual(len(promote.expected_tags()), 28)
        self.write_records()
        with patch.object(promote, "run", return_value="") as docker:
            promote.publish(self.directory)
        self.assertEqual(docker.call_count, 28)
        for call, tag in zip(docker.call_args_list, sorted(promote.expected_tags())):
            records = [r for r in self.records if r["tag"] == tag]
            self.assertEqual(call.args, ("buildx", "imagetools", "create", "--tag",
                                        f"kooldev/php:{tag}",
                                        *[f"kooldev/php@{r['digest']}" for r in records]))

    def test_missing_architecture(self):
        self.assert_rejected_before_write(self.records[:-1])

    def test_duplicate_architecture(self):
        self.assert_rejected_before_write(self.records + [self.records[0]])

    def test_wrong_repository_scope_tag_arch_and_digests(self):
        for field, value in (("repository", "attacker/php"), ("run_id", "122"),
                             ("run_attempt", "1"), ("tag", "latest"), ("arch", "s390x"),
                             ("digest", "sha256:bad"), ("image_id", "latest")):
            with self.subTest(field=field):
                records = copy.deepcopy(self.records)
                records[0][field] = value
                self.assert_rejected_before_write(records)

    def test_duplicate_digest(self):
        records = copy.deepcopy(self.records)
        records[1]["digest"] = records[0]["digest"]
        self.assert_rejected_before_write(records)

    def test_missing_digest(self):
        records = copy.deepcopy(self.records)
        del records[0]["digest"]
        self.assert_rejected_before_write(records)

    def test_stage_tags_exact_tested_id_and_records_push_digest(self):
        image_id = digest(999)
        image = dict(Id=image_id, Os="linux", Architecture="arm64")
        with patch.object(promote, "run", side_effect=[
            json.dumps([image]), "", f"staging: digest: {digest(1000)} size: 123\n"
        ]) as docker:
            promote.stage("8.5", "arm64", image_id, self.directory)
        staging = "kooldev/php:ci-php-123-2-8.5-arm64"
        self.assertEqual([c.args for c in docker.call_args_list],
                         [("image", "inspect", image_id), ("tag", image_id, staging),
                          ("push", staging)])
        record = json.loads((self.directory / "8.5-arm64.json").read_text())
        self.assertEqual(record["image_id"], image_id)
        self.assertEqual(record["digest"], digest(1000))

    def test_stage_rejects_wrong_id_or_platform_before_push(self):
        for image in (dict(Id=digest(998), Os="linux", Architecture="arm64"),
                      dict(Id=digest(999), Os="linux", Architecture="amd64")):
            with patch.object(promote, "run", return_value=json.dumps([image])) as docker:
                with self.assertRaises(ValueError):
                    promote.stage("8.5", "arm64", digest(999), self.directory)
                self.assertEqual(docker.call_count, 1)

    def test_stage_does_not_record_failed_or_ambiguous_push(self):
        image = dict(Id=digest(999), Os="linux", Architecture="amd64")
        for output in ("no digest", f"digest: {digest(1)}\ndigest: {digest(2)}"):
            with patch.object(promote, "run", side_effect=[json.dumps([image]), "", output]):
                with self.assertRaises(ValueError):
                    promote.stage("8.5", "amd64", digest(999), self.directory)
                self.assertEqual(list(self.directory.iterdir()), [])


class WorkflowContracts(unittest.TestCase):
    def setUp(self):
        self.workflow = (promote.ROOT / ".github/workflows/ci-cd.yml").read_text()
        self.build = self.workflow.split("  build-test:\n")[1].split("\n  publish:")[0]
        self.publish = self.workflow.split("  publish:\n")[1].split("\n  trigger-downstream:")[0]
        self.guard = ("github.event_name != 'pull_request' && github.ref == 'refs/heads/master'"
                      " && github.repository == 'kool-dev/docker-php'")

    def test_native_builds_and_same_job_base(self):
        self.assertIn("{arch: amd64, runner: ubuntu-24.04}", self.build)
        self.assertIn("{arch: arm64, runner: ubuntu-24.04-arm}", self.build)
        self.assertIn("runs-on: ${{ matrix.native.runner }}", self.build)
        self.assertIn("driver: docker\n", self.build)
        self.assertEqual(self.workflow.count("uses: docker/build-push-action@v7"), 3)
        self.assertEqual(self.build.count("platforms: linux/${{ env.ARCH }}"), 3)
        self.assertNotIn("qemu", self.workflow.lower())
        for variant in ("base", "nginx", "node"):
            self.assertEqual(self.build.count("${{ steps." + variant + ".outputs.imageid }}"),
                             4 if variant == "base" else 2)
            self.assertIn(f'bash scripts/test-image.sh "${variant.upper()}" "$IMAGE_ID"', self.build)
        self.assertLess(self.build.index("Test base image"), self.build.index("Build nginx image"))
        self.assertLess(self.build.index("Test node image"), self.build.index("docker/login-action"))
        base_build, derived_builds = self.build.split("      - name: Build nginx image", 1)
        self.assertEqual(base_build.count("pull: true"), 1)
        self.assertNotIn("pull:", derived_builds)
        self.assertEqual(derived_builds.count('python3 scripts/check_parent.py "$BASE" "$BASE_ID" "$IMAGE_ID"'), 2)

    def test_release_guards_and_current_attempt_artifacts(self):
        self.assertEqual(self.workflow.count("if: " + self.guard), 5)
        self.assertIn("needs: build-test", self.publish)
        self.assertIn("needs: publish", self.workflow)
        self.assertIn("actions/upload-artifact@v7.0.2", self.build)
        self.assertIn("php-${{ github.run_id }}-${{ github.run_attempt }}-${{ env.BASE }}-${{ env.ARCH }}", self.build)
        self.assertIn("actions/download-artifact@v8.0.2", self.publish)
        self.assertIn("pattern: php-${{ github.run_id }}-${{ github.run_attempt }}-*", self.publish)
        self.assertLess(self.publish.index("promote.py validate"), self.publish.index("docker/login-action"))
        self.assertNotIn("build-push", self.publish)
        self.assertIn("promote.py publish", self.publish)

    def test_schedule_generation_dispatch_and_concurrency_preserved(self):
        self.assertIn('cron: "0 0 * * 0"', self.workflow)
        self.assertIn("cancel-in-progress: ${{ github.event_name == 'pull_request' }}", self.workflow)
        self.assertIn("fireworkweb/fwd:v1.0 fwd template", self.workflow)
        self.assertIn("git diff --exit-code", self.workflow)
        self.assertIn("secrets.DISPATCH_TOKEN || secrets.WORKFLOW_TOKEN", self.workflow)
        downstream = self.workflow.split("  trigger-downstream:\n")[1]
        for repo in ("wordpress", "php-sqlsrv", "php-swoole"):
            self.assertIn(f"- kool-dev/docker-{repo}", downstream)
        for repo in ("phpqa", "oci8"):
            self.assertNotIn(repo, downstream)

    def test_probes_use_immutable_id(self):
        script = (promote.ROOT / "scripts/test-image.sh").read_text()
        self.assertIn('image=${2:-"kooldev/php:$tag"}', script)
        self.assertIn('test "$(docker image inspect "kooldev/php:$tag" --format \'{{.Id}}\')" = "$image"', script)
        self.assertNotIn('docker run --rm "kooldev/php:', script)


class ParentTests(unittest.TestCase):
    def test_local_base_id_and_layer_prefix(self):
        with patch.object(check_parent, "inspect", side_effect=[
            {"Id": digest(1), "RootFS": {"Layers": ["base", "fresh"]}},
            {"Id": digest(2), "RootFS": {"Layers": ["base", "fresh", "nginx"]}},
        ]):
            check_parent.check_parent("8.5", digest(1), digest(2))

    def test_rejects_replaced_base_even_with_identical_layers(self):
        with patch.object(check_parent, "inspect", return_value={
            "Id": digest(3), "RootFS": {"Layers": ["base", "fresh"]}
        }):
            with self.assertRaisesRegex(ValueError, "replaced"):
                check_parent.check_parent("8.5", digest(1), digest(2))

    def test_rejects_stale_parent_layers(self):
        with patch.object(check_parent, "inspect", side_effect=[
            {"Id": digest(1), "RootFS": {"Layers": ["base", "fresh"]}},
            {"Id": digest(2), "RootFS": {"Layers": ["base", "stale", "nginx"]}},
        ]):
            with self.assertRaisesRegex(ValueError, "inherit"):
                check_parent.check_parent("8.5", digest(1), digest(2))


if __name__ == "__main__":
    unittest.main()
