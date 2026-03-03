# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""End-to-end tests for the version bump detection pipeline.

Creates a real git repository, adds commits, and verifies the full
detection pipeline produces correct bump types.

References:
    - BUG-002: Version bump regex rejects uppercase scopes
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from src.version.application.handlers.queries.detect_bump_type_query_handler import (
    DetectBumpTypeQueryHandler,
)
from src.version.domain.services.bump_type_detector import BumpTypeDetector
from src.version.domain.value_objects.bump_type import BumpType
from src.version.infrastructure.adapters.git_commit_log_reader import GitCommitLogReader

pytestmark = [
    pytest.mark.e2e,
]


@pytest.fixture()
def versioned_repo(tmp_path: Path) -> Path:
    """Create a repository simulating the BUG-002 scenario.

    Reproduces: v0.22.1 tag, then feat(GH-122) and fix commits that
    should have triggered a minor bump but were missed.
    """
    repo = tmp_path / "versioned-repo"
    repo.mkdir()

    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(
        {
            "GIT_AUTHOR_NAME": "Test",
            "GIT_AUTHOR_EMAIL": "test@test.com",
            "GIT_COMMITTER_NAME": "Test",
            "GIT_COMMITTER_EMAIL": "test@test.com",
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_NOSYSTEM": "1",
            "HOME": str(tmp_path),
        }
    )

    subprocess.run(
        ["git", "init", "--initial-branch=main"],
        cwd=repo,
        check=True,
        capture_output=True,
        env=env,
    )
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=repo,
        check=True,
        capture_output=True,
        env=env,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=repo,
        check=True,
        capture_output=True,
        env=env,
    )
    subprocess.run(
        ["git", "config", "commit.gpgsign", "false"],
        cwd=repo,
        check=True,
        capture_output=True,
        env=env,
    )

    # Initial release
    (repo / "README.md").write_text("# Project v0.22.1\n")
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, env=env)
    subprocess.run(
        ["git", "commit", "--no-verify", "-m", "chore: release v0.22.1"],
        cwd=repo,
        check=True,
        capture_output=True,
        env=env,
    )
    subprocess.run(
        ["git", "tag", "-a", "v0.22.1", "-m", "v0.22.1"],
        cwd=repo,
        check=True,
        capture_output=True,
        env=env,
    )

    # PR #125 merge (fix) - should have bumped to v0.22.2
    (repo / "fix1.py").write_text("# fix\n")
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, env=env)
    subprocess.run(
        [
            "git",
            "commit",
            "--no-verify",
            "-m",
            "fix(ci): version bump regex rejects uppercase scopes",
        ],
        cwd=repo,
        check=True,
        capture_output=True,
        env=env,
    )

    # PR #128 merge (feat with uppercase scope) - should have bumped to v0.23.0
    (repo / "feat1.py").write_text("# feat\n")
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, env=env)
    subprocess.run(
        [
            "git",
            "commit",
            "--no-verify",
            "-m",
            "feat(GH-122): complete EPIC-007 MKDocs site publication",
        ],
        cwd=repo,
        check=True,
        capture_output=True,
        env=env,
    )

    return repo


class TestVersionBumpE2E:
    """End-to-end pipeline tests reproducing BUG-002."""

    @pytest.mark.happy_path
    def test_full_pipeline_detects_minor_bump(self, versioned_repo: Path) -> None:
        """Full pipeline: repo with feat(GH-122) -> MINOR bump detected.

        This is THE BUG-002 regression test: the old inline regex would
        have returned NONE because 'GH-122' has uppercase characters.
        """
        reader = GitCommitLogReader(repo_path=versioned_repo)
        detector = BumpTypeDetector()
        handler = DetectBumpTypeQueryHandler(
            commit_reader=reader,
            detector=detector,
        )

        result = handler.handle(since_tag="v0.22.1")

        assert result == BumpType.MINOR, (
            f"Expected MINOR for feat(GH-122) commit, got {result.label}"
        )

    @pytest.mark.happy_path
    def test_full_pipeline_latest_tag_sentinel(self, versioned_repo: Path) -> None:
        """Full pipeline: __latest__ sentinel finds v0.22.1 and detects MINOR."""
        reader = GitCommitLogReader(repo_path=versioned_repo)
        detector = BumpTypeDetector()
        handler = DetectBumpTypeQueryHandler(
            commit_reader=reader,
            detector=detector,
        )

        result = handler.handle(since_tag="__latest__")

        assert result == BumpType.MINOR

    @pytest.mark.edge_case
    def test_full_pipeline_all_commits_returns_minor(self, versioned_repo: Path) -> None:
        """Reading all commits (no since_tag) also returns MINOR because feat is present."""
        reader = GitCommitLogReader(repo_path=versioned_repo)
        detector = BumpTypeDetector()
        handler = DetectBumpTypeQueryHandler(
            commit_reader=reader,
            detector=detector,
        )

        result = handler.handle()

        # All commits include: chore (none), fix (patch), feat (minor)
        # Highest severity wins: MINOR
        assert result == BumpType.MINOR
