# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Contract tests for ICommitLogReader implementations.

Verifies that all adapters implementing ICommitLogReader satisfy
the protocol contract.

References:
    - BUG-002: Version bump regex rejects uppercase scopes
"""

from __future__ import annotations

import io

import pytest

from src.version.application.ports.commit_log_reader import CommitLogEntry, ICommitLogReader
from src.version.infrastructure.adapters.stdin_commit_reader import StdinCommitReader


class TestStdinCommitReaderContract:
    """Contract tests for StdinCommitReader."""

    @pytest.mark.happy_path
    def test_implements_protocol(self) -> None:
        reader = StdinCommitReader(input_stream=io.StringIO(""))
        assert isinstance(reader, ICommitLogReader)

    @pytest.mark.happy_path
    def test_read_commits_returns_list(self) -> None:
        reader = StdinCommitReader(input_stream=io.StringIO("feat: add\n"))
        result = reader.read_commits()
        assert isinstance(result, list)

    @pytest.mark.happy_path
    def test_entries_are_commit_log_entry(self) -> None:
        reader = StdinCommitReader(input_stream=io.StringIO("feat: add\n"))
        result = reader.read_commits()
        assert len(result) == 1
        assert isinstance(result[0], CommitLogEntry)
        assert result[0].subject == "feat: add"
        assert result[0].body == ""

    @pytest.mark.happy_path
    def test_multiple_lines(self) -> None:
        reader = StdinCommitReader(input_stream=io.StringIO("feat: add\nfix: fix\n"))
        result = reader.read_commits()
        assert len(result) == 2

    @pytest.mark.negative
    def test_empty_input(self) -> None:
        reader = StdinCommitReader(input_stream=io.StringIO(""))
        result = reader.read_commits()
        assert result == []

    @pytest.mark.negative
    def test_ignores_since_tag_param(self) -> None:
        reader = StdinCommitReader(input_stream=io.StringIO("feat: add\n"))
        result = reader.read_commits(since_tag="v1.0.0")
        assert len(result) == 1

    @pytest.mark.negative
    def test_ignores_range_spec_param(self) -> None:
        reader = StdinCommitReader(input_stream=io.StringIO("feat: add\n"))
        result = reader.read_commits(range_spec="v1.0.0..HEAD")
        assert len(result) == 1

    @pytest.mark.edge_case
    def test_blank_lines_skipped(self) -> None:
        reader = StdinCommitReader(input_stream=io.StringIO("feat: add\n\n\nfix: fix\n"))
        result = reader.read_commits()
        assert len(result) == 2
