# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Integration tests for GitCommitLogReader.

Creates temporary git repositories to test real git log parsing.

References:
    - BUG-002: Version bump regex rejects uppercase scopes
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from src.version.application.ports.commit_log_reader import CommitLogEntry, ICommitLogReader
from src.version.infrastructure.adapters.git_commit_log_reader import GitCommitLogReader

pytestmark = [
    pytest.mark.integration,
]


@pytest.fixture()
def git_repo(tmp_path: Path) -> Path:
    """Create a temporary git repository with some commits."""
    repo = tmp_path / "test-repo"
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

    # Initial commit
    (repo / "README.md").write_text("# Test\n")
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, env=env)
    subprocess.run(
        ["git", "commit", "--no-verify", "-m", "docs: initial commit"],
        cwd=repo,
        check=True,
        capture_output=True,
        env=env,
    )

    # Tag v0.1.0
    subprocess.run(
        ["git", "tag", "-a", "v0.1.0", "-m", "v0.1.0"],
        cwd=repo,
        check=True,
        capture_output=True,
        env=env,
    )

    # Add a feature commit
    (repo / "feature.py").write_text("# feature\n")
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, env=env)
    subprocess.run(
        ["git", "commit", "--no-verify", "-m", "feat(GH-122): add version detection"],
        cwd=repo,
        check=True,
        capture_output=True,
        env=env,
    )

    # Add a fix commit
    (repo / "fix.py").write_text("# fix\n")
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, env=env)
    subprocess.run(
        ["git", "commit", "--no-verify", "-m", "fix: correct edge case"],
        cwd=repo,
        check=True,
        capture_output=True,
        env=env,
    )

    return repo


class TestGitCommitLogReaderHappy:
    """Happy path tests for GitCommitLogReader."""

    @pytest.mark.happy_path
    def test_implements_protocol(self, git_repo: Path) -> None:
        """GitCommitLogReader implements ICommitLogReader."""
        reader = GitCommitLogReader(repo_path=git_repo)
        assert isinstance(reader, ICommitLogReader)

    @pytest.mark.happy_path
    def test_read_all_commits(self, git_repo: Path) -> None:
        """Read all commits from the repository."""
        reader = GitCommitLogReader(repo_path=git_repo)
        commits = reader.read_commits()
        assert len(commits) == 3
        assert all(isinstance(c, CommitLogEntry) for c in commits)

    @pytest.mark.happy_path
    def test_read_commits_since_tag(self, git_repo: Path) -> None:
        """Read commits since a specific tag."""
        reader = GitCommitLogReader(repo_path=git_repo)
        commits = reader.read_commits(since_tag="v0.1.0")
        assert len(commits) == 2
        subjects = [c.subject for c in commits]
        assert "feat(GH-122): add version detection" in subjects
        assert "fix: correct edge case" in subjects

    @pytest.mark.happy_path
    def test_read_commits_since_latest_tag(self, git_repo: Path) -> None:
        """Read commits since __latest__ sentinel."""
        reader = GitCommitLogReader(repo_path=git_repo)
        commits = reader.read_commits(since_tag="__latest__")
        assert len(commits) == 2

    @pytest.mark.happy_path
    def test_commit_subjects_preserved(self, git_repo: Path) -> None:
        """Commit subjects are read accurately."""
        reader = GitCommitLogReader(repo_path=git_repo)
        commits = reader.read_commits(since_tag="v0.1.0")
        subjects = {c.subject for c in commits}
        assert "feat(GH-122): add version detection" in subjects
        assert "fix: correct edge case" in subjects


class TestGitCommitLogReaderNegative:
    """Negative tests for GitCommitLogReader."""

    @pytest.mark.negative
    def test_nonexistent_repo_path(self, tmp_path: Path) -> None:
        """Non-existent repo path raises an error."""
        reader = GitCommitLogReader(repo_path=tmp_path / "nonexistent")
        with pytest.raises((subprocess.CalledProcessError, FileNotFoundError, OSError)):
            reader.read_commits()

    @pytest.mark.negative
    def test_nonexistent_tag(self, git_repo: Path) -> None:
        """Non-existent tag raises an error on git log."""
        reader = GitCommitLogReader(repo_path=git_repo)
        with pytest.raises(subprocess.CalledProcessError):
            reader.read_commits(since_tag="v99.99.99")


class TestGitCommitLogReaderEdgeCases:
    """Edge case tests for GitCommitLogReader."""

    @pytest.mark.edge_case
    def test_empty_repo_no_commits(self, tmp_path: Path) -> None:
        """Empty repo with no commits returns empty list or raises."""
        repo = tmp_path / "empty-repo"
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
        reader = GitCommitLogReader(repo_path=repo)
        # Empty repo with no commits: HEAD doesn't exist, git log fails
        # Accept either CalledProcessError or empty list depending on git version
        try:
            commits = reader.read_commits()
            assert commits == []
        except subprocess.CalledProcessError:
            pass  # Expected: HEAD doesn't exist in empty repo
