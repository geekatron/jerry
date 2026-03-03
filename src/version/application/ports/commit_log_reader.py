# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ICommitLogReader port for reading commit history.

References:
    - BUG-002: Version bump regex rejects uppercase scopes
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class CommitLogEntry:
    """A single commit log entry.

    Attributes:
        subject: The commit subject line (first line).
        body: The full commit body (may be empty).
    """

    subject: str
    body: str


@runtime_checkable
class ICommitLogReader(Protocol):
    """Port for reading commit log entries.

    Implementations may read from git, stdin, or other sources.
    """

    def read_commits(
        self,
        since_tag: str | None = None,
        range_spec: str | None = None,
    ) -> list[CommitLogEntry]:
        """Read commit log entries.

        Args:
            since_tag: Read commits since this tag (e.g., 'v0.22.1').
                If None and range_spec is None, reads all commits.
            range_spec: Git range spec (e.g., 'v0.22.1..HEAD').
                Takes precedence over since_tag.

        Returns:
            List of commit log entries.
        """
        ...
