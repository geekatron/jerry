# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
GitCommitLogReader adapter for reading commit history from git.

Security: Uses subprocess.run with shell=False to prevent injection.

References:
    - BUG-002: Version bump regex rejects uppercase scopes
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from src.version.application.ports.commit_log_reader import CommitLogEntry

# Separator between subject and body in git log output.
# Uses a unique string unlikely to appear in commit messages.
_RECORD_SEP = "---JERRY-COMMIT-SEP---"
_FIELD_SEP = "---JERRY-FIELD-SEP---"


class GitCommitLogReader:
    """Reads commit log entries from git using subprocess.

    Security considerations:
    - Always uses shell=False (no shell injection)
    - Tag/range arguments are passed as list elements (no interpolation)
    - Timeout prevents hanging on large repos
    """

    def __init__(
        self,
        repo_path: Path | str | None = None,
        timeout: int = 30,
    ) -> None:
        """Initialize with optional repo path and timeout.

        Args:
            repo_path: Path to the git repository. If None, uses cwd.
            timeout: Maximum seconds for git commands (default: 30).
        """
        self._repo_path = str(repo_path) if repo_path else None
        self._timeout = timeout

    def read_commits(
        self,
        since_tag: str | None = None,
        range_spec: str | None = None,
    ) -> list[CommitLogEntry]:
        """Read commit entries from git log.

        Args:
            since_tag: Read commits since this tag. If the tag doesn't
                exist, reads all commits.
            range_spec: Git range spec (e.g., 'v0.22.1..HEAD').
                Takes precedence over since_tag.

        Returns:
            List of CommitLogEntry with subject and body.
        """
        if range_spec:
            git_range = range_spec
        elif since_tag:
            # "__latest__" sentinel means "find the latest version tag"
            tag = self._find_latest_tag() if since_tag == "__latest__" else since_tag
            if tag:
                git_range = f"{tag}..HEAD"
            else:
                git_range = "HEAD"
        else:
            git_range = "HEAD"

        # Format: subject<FIELD_SEP>body<RECORD_SEP>
        format_str = f"%s{_FIELD_SEP}%b{_RECORD_SEP}"

        cmd = [
            "git",
            "log",
            git_range,
            f"--pretty=format:{format_str}",
        ]

        result = self._run_git(cmd)
        if not result.strip():
            return []

        return self._parse_output(result)

    def find_latest_tag(self) -> str | None:
        """Find the latest version tag.

        Returns:
            The latest version tag (e.g., 'v0.22.1'), or None if no tags exist.
        """
        return self._find_latest_tag()

    def _find_latest_tag(self) -> str | None:
        """Find the latest version tag matching v* pattern.

        Returns:
            Tag string or None.
        """
        cmd = [
            "git",
            "describe",
            "--tags",
            "--abbrev=0",
            "--match",
            "v*",
        ]

        try:
            result = self._run_git(cmd)
            tag = result.strip()
            return tag if tag else None
        except subprocess.CalledProcessError:
            return None

    def _run_git(self, cmd: list[str]) -> str:
        """Execute a git command safely.

        Args:
            cmd: Command and arguments as a list (never a string).

        Returns:
            stdout as a string.

        Raises:
            subprocess.CalledProcessError: If git returns non-zero.
        """
        # Strip GIT_DIR/GIT_WORK_TREE from environment when repo_path is set.
        # These vars override cwd, breaking the repo_path contract.
        # Common when running under pre-commit or other git hooks.
        env = None
        if self._repo_path:
            env = {
                k: v
                for k, v in os.environ.items()
                if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")
            }

        result = subprocess.run(  # noqa: S603
            cmd,
            capture_output=True,
            text=True,
            timeout=self._timeout,
            check=True,
            cwd=self._repo_path,
            env=env,
        )
        return result.stdout

    def _parse_output(self, output: str) -> list[CommitLogEntry]:
        """Parse git log output into CommitLogEntry objects.

        Args:
            output: Raw git log output with custom separators.

        Returns:
            List of parsed entries.
        """
        entries: list[CommitLogEntry] = []

        records = output.split(_RECORD_SEP)
        for record in records:
            record = record.strip()
            if not record:
                continue

            parts = record.split(_FIELD_SEP, maxsplit=1)
            subject = parts[0].strip()
            body = parts[1].strip() if len(parts) > 1 else ""

            if subject:
                entries.append(CommitLogEntry(subject=subject, body=body))

        return entries
