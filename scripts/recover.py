"""Authorize reusing one complete, latest trusted CI attempt without rebuilding."""

import json
import os
import re
import subprocess
import sys

REPOSITORY = "kool-dev/docker-php"
BRANCH = "master"
BUILD_PREFIX = "build-test ("
BUILD_COUNT = 24
CHECK_JOB = "checks"
EVENTS = {"push", "schedule", "workflow_dispatch", "repository_dispatch"}


def api(path):
    return json.loads(subprocess.check_output(["gh", "api", path], text=True))


def validate(run_id, attempt):
    if (os.environ.get("GITHUB_REPOSITORY") != REPOSITORY
            or os.environ.get("GITHUB_REF") != f"refs/heads/{BRANCH}"
            or os.environ.get("GITHUB_EVENT_NAME") != "workflow_dispatch"
            or not all(re.fullmatch(r"[1-9][0-9]*", s) for s in (run_id, attempt))):
        raise ValueError("Recovery requires a trusted default-branch manual run and numeric scope")
    root = f"repos/{REPOSITORY}"
    workflow = api(f"{root}/actions/workflows/ci-cd.yml")
    source = api(f"{root}/actions/runs/{run_id}")
    head = api(f"{root}/branches/{BRANCH}")["commit"]["sha"]
    if (source["workflow_id"] != workflow["id"]
            or source["event"] not in EVENTS
            or source["head_branch"] != BRANCH
            or source["head_repository"]["full_name"] != REPOSITORY
            or source["head_sha"] != head or head != os.environ["GITHUB_SHA"]
            or source["run_attempt"] != int(attempt)
            or source["status"] != "completed"):
        raise ValueError("Source must be the completed latest attempt at the current default-branch HEAD")
    # A rerun keeps its ID/creation time. Compare attempt start times, not IDs.
    trusted = []
    page = 1
    while True:
        batch = api(f"{root}/actions/workflows/ci-cd.yml/runs?branch={BRANCH}&per_page=100&page={page}")["workflow_runs"]
        trusted.extend(r for r in batch if r["event"] in EVENTS and r["head_branch"] == BRANCH)
        if len(batch) < 100:
            break
        page += 1
    latest = max(trusted, key=lambda r: (r["run_started_at"], r["id"]), default=None)
    if (not latest or latest["id"] != int(run_id)
            or latest["run_attempt"] != int(attempt) or latest["status"] != "completed"):
        raise ValueError("A newer CI release exists; do not resume this source")
    jobs = []
    page = 1
    while True:
        batch = api(f"{root}/actions/runs/{run_id}/attempts/{attempt}/jobs?per_page=100&page={page}")["jobs"]
        jobs.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    builds = [j for j in jobs if j["name"].startswith(BUILD_PREFIX)]
    checks = [j for j in jobs if j["name"] == CHECK_JOB]
    if (len(builds) != BUILD_COUNT or len({j["name"] for j in builds}) != BUILD_COUNT
            or len(checks) != 1
            or any(j["conclusion"] != "success" for j in builds + checks)):
        raise ValueError("Every native build/test/staging job and the checks must have succeeded")
    # Metadata completeness/schema is validated again by the publisher after download.
    return run_id, attempt


def main():
    run_id, attempt = validate(*sys.argv[1:])
    with open(os.environ["GITHUB_ENV"], "a") as env:
        env.write(f"SOURCE_RUN_ID={run_id}\nSOURCE_RUN_ATTEMPT={attempt}\n")


if __name__ == "__main__":
    main()
