import copy
import os
from pathlib import Path
import unittest
from unittest.mock import patch

import recover


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.source = dict(id=123, workflow_id=7, event="push",
                           head_branch=recover.BRANCH, head_sha="abc",
                           head_repository=dict(full_name=recover.REPOSITORY),
                           run_attempt=2, status="completed", run_started_at="2026-11-15T11:00:00Z")
        self.recent = [copy.deepcopy(self.source)]
        self.jobs = [dict(name=f"{recover.BUILD_PREFIX}{i})", conclusion="success")
                     for i in range(recover.BUILD_COUNT)]
        self.jobs.append(dict(name=recover.CHECK_JOB, conclusion="success"))
        env = dict(GITHUB_REPOSITORY=recover.REPOSITORY,
                   GITHUB_REF=f"refs/heads/{recover.BRANCH}",
                   GITHUB_EVENT_NAME="workflow_dispatch", GITHUB_SHA="abc")
        self.env = patch.dict(os.environ, env, clear=True)
        self.env.start()
        self.addCleanup(self.env.stop)

    def api(self, path):
        if path.endswith("/actions/workflows/ci-cd.yml"):
            return dict(id=7)
        if "/branches/" in path:
            return dict(commit=dict(sha="abc"))
        if "/runs?" in path:
            return dict(workflow_runs=self.recent)
        if "/jobs?" in path:
            return dict(jobs=self.jobs)
        return self.source

    def test_latest_complete_source_accepted_even_if_publication_failed(self):
        self.source["conclusion"] = "failure"
        with patch.object(recover, "api", side_effect=self.api):
            self.assertEqual(recover.validate("123", "2"), ("123", "2"))

    def test_untrusted_or_malformed_request_never_calls_api(self):
        for env, run, attempt in [
            (dict(GITHUB_EVENT_NAME="pull_request"), "123", "2"),
            (dict(GITHUB_REF="refs/heads/feature"), "123", "2"),
            (dict(GITHUB_REPOSITORY="fork/repo"), "123", "2"),
            ({}, "123\nOTHER=bad", "2"), ({}, "123", "0"),
        ]:
            with patch.dict(os.environ, env), patch.object(recover, "api") as api:
                with self.assertRaises(ValueError):
                    recover.validate(run, attempt)
                api.assert_not_called()

    def test_rejects_wrong_workflow_fork_branch_commit_event_attempt_and_active_run(self):
        for field, value in [
            ("workflow_id", 8), ("head_branch", "feature"), ("head_sha", "old"),
            ("head_repository", dict(full_name="fork/repo")),
            ("event", "pull_request"), ("run_attempt", 3), ("status", "in_progress"),
        ]:
            with patch.dict(self.source, {field: value}), patch.object(recover, "api", side_effect=self.api):
                with self.assertRaises(ValueError):
                    recover.validate("123", "2")

    def test_rejects_newer_release_even_at_same_commit(self):
        self.recent.append(dict(self.source, id=124))
        with patch.object(recover, "api", side_effect=self.api):
            with self.assertRaises(ValueError):
                recover.validate("123", "2")

    def test_old_run_id_with_newer_attempt_is_newer_than_source(self):
        self.recent.append(dict(self.source, id=122, run_started_at="2026-11-15T12:00:00Z"))
        with patch.object(recover, "api", side_effect=self.api):
            with self.assertRaises(ValueError):
                recover.validate("123", "2")

    def test_rejects_incomplete_failed_or_duplicate_builds_and_missing_checks(self):
        original = copy.deepcopy(self.jobs)
        for jobs in [
            original[:-1], original[1:], original + [original[0]],
            [dict(j, conclusion="failure") if i == 0 else j for i, j in enumerate(original)],
            [dict(j, name=original[0]["name"]) if i == 1 else j for i, j in enumerate(original)],
        ]:
            self.jobs = jobs
            with patch.object(recover, "api", side_effect=self.api):
                with self.assertRaises(ValueError):
                    recover.validate("123", "2")

    def test_recovery_workflow_is_read_only_until_validation_and_shares_release_lock(self):
        text = (Path(__file__).resolve().parents[1] /
                ".github/workflows/resume-publication.yml").read_text()
        self.assertIn("group: CI/CD-${{ github.ref }}", text)
        self.assertIn(f"github.ref == 'refs/heads/{recover.BRANCH}'", text)
        self.assertIn(f"github.repository == '{recover.REPOSITORY}'", text)
        self.assertIn("actions: read", text)
        self.assertIn("run-id: ${{ env.SOURCE_RUN_ID }}", text)
        self.assertLess(text.index("recover.py"), text.index("download-artifact@"))
        self.assertLess(text.index("download-artifact@"), text.index("docker/login-action@"))
        self.assertNotIn("build-push-action@", text)
        self.assertNotIn("always()", text)
        self.assertIn("needs: publish", text)


if __name__ == "__main__":
    unittest.main()
