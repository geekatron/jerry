# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
StdinCommitReader adapter for reading commit subjects from stdin.

Reads one commit subject per line from stdin pipe. Does not support
commit bodies (subjects only).

References:
    - BUG-002: Version bump regex rejects uppercase scopes
"""

from __future__ import annotations

import sys
from typing import IO

from src.version.application.ports.commit_log_reader import CommitLogEntry


class StdinCommitReader:
    """Reads commit subjects from stdin, one per line.

    This adapter is used when commit subjects are piped via stdin:
        echo "feat(GH-122): add feature" | jerry ci detect-bump-type --commits-from-stdin
    """

    def __init__(self, input_stream: IO[str] | None = None) -> None:
        """Initialize with optional input stream for testing.

        Args:
            input_stream: File-like object to read from.
                Defaults to sys.stdin.
        """
        self._input: IO[str] = input_stream if input_stream is not None else sys.stdin

    def read_commits(
        self,
        since_tag: str | None = None,
        range_spec: str | None = None,
    ) -> list[CommitLogEntry]:
        """Read commit subjects from stdin.

        Args:
            since_tag: Ignored (stdin has no git context).
            range_spec: Ignored (stdin has no git context).

        Returns:
            List of CommitLogEntry with subjects from stdin.
            Bodies are always empty.
        """
        entries: list[CommitLogEntry] = []

        for line in self._input:
            subject = line.strip()
            if subject:
                entries.append(CommitLogEntry(subject=subject, body=""))

        return entries
