# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for JsonlTranscriptReader.

Tests cover BDD scenarios from EN-004 and SPIKE-003 findings:
    - Read cumulative context usage from real Claude Code JSONL format
    - Sum input_tokens + cache_creation_input_tokens + cache_read_input_tokens
    - Skip non-assistant entries (user, progress, etc.)
    - FileNotFoundError raised on missing file
    - ValueError raised on empty file or no usage entries
    - Handles large entries (> 4096 bytes)

References:
    - EN-004: ContextFillEstimator and ResumptionContextGenerator
    - SPIKE-003: Validation findings — wrong field path and semantics
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.context_monitoring.infrastructure.adapters.jsonl_transcript_reader import (
    JsonlTranscriptReader,
)

# =============================================================================
# Helper: Build realistic Claude Code JSONL entries
# =============================================================================


def _assistant_entry(
    input_tokens: int = 1,
    cache_creation_input_tokens: int = 0,
    cache_read_input_tokens: int = 0,
    output_tokens: int = 100,
) -> str:
    """Build a realistic Claude Code assistant entry as a JSONL line."""
    entry = {
        "type": "assistant",
        "message": {
            "model": "claude-sonnet-4-6",
            "id": "msg_test",
            "type": "message",
            "role": "assistant",
            "content": [{"type": "text", "text": "Hello"}],
            "usage": {
                "input_tokens": input_tokens,
                "cache_creation_input_tokens": cache_creation_input_tokens,
                "cache_read_input_tokens": cache_read_input_tokens,
                "output_tokens": output_tokens,
            },
        },
    }
    return json.dumps(entry)


def _user_entry() -> str:
    """Build a realistic Claude Code user entry (no usage data)."""
    entry = {
        "type": "user",
        "message": {
            "role": "user",
            "content": [{"type": "text", "text": "Hello"}],
        },
    }
    return json.dumps(entry)


def _progress_entry() -> str:
    """Build a realistic Claude Code progress entry (no usage data)."""
    entry = {
        "type": "progress",
        "data": {"type": "hook_progress", "hookEvent": "PreToolUse"},
    }
    return json.dumps(entry)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def reader() -> JsonlTranscriptReader:
    """Return a JsonlTranscriptReader instance."""
    return JsonlTranscriptReader()


# =============================================================================
# BDD Scenario: Read cumulative context usage from real Claude Code format
# =============================================================================


class TestReadFromRealClaudeCodeFormat:
    """Scenario: Reader extracts cumulative context window usage.

    Given a Claude Code JSONL transcript with nested message.usage structure,
    read_latest_tokens() should return the SUM of input_tokens +
    cache_creation_input_tokens + cache_read_input_tokens from the last
    assistant entry.
    """

    def test_sums_all_three_token_fields(
        self, reader: JsonlTranscriptReader, tmp_path: Path
    ) -> None:
        """Returns sum of input_tokens + cache_creation + cache_read."""
        transcript = tmp_path / "transcript.jsonl"
        line = _assistant_entry(
            input_tokens=1,
            cache_creation_input_tokens=989,
            cache_read_input_tokens=106_468,
        )
        transcript.write_text(line + "\n", encoding="utf-8")

        result = reader.read_latest_tokens(str(transcript))
        assert result == 1 + 989 + 106_468  # 107_458

    def test_handles_zero_cache_fields(self, reader: JsonlTranscriptReader, tmp_path: Path) -> None:
        """When cache fields are zero, returns just input_tokens."""
        transcript = tmp_path / "transcript.jsonl"
        line = _assistant_entry(
            input_tokens=50_000,
            cache_creation_input_tokens=0,
            cache_read_input_tokens=0,
        )
        transcript.write_text(line + "\n", encoding="utf-8")

        result = reader.read_latest_tokens(str(transcript))
        assert result == 50_000

    def test_returns_integer(self, reader: JsonlTranscriptReader, tmp_path: Path) -> None:
        """read_latest_tokens() returns an int."""
        transcript = tmp_path / "transcript.jsonl"
        line = _assistant_entry(input_tokens=100, cache_read_input_tokens=900)
        transcript.write_text(line + "\n", encoding="utf-8")

        result = reader.read_latest_tokens(str(transcript))
        assert isinstance(result, int)


# =============================================================================
# BDD Scenario: Skips non-assistant entries
# =============================================================================


class TestSkipsNonAssistantEntries:
    """Scenario: Reader finds the last assistant entry with usage data.

    Given a JSONL transcript with user, progress, and assistant entries,
    the reader should skip entries without message.usage and return
    the token sum from the last assistant entry.
    """

    def test_skips_trailing_user_entry(self, reader: JsonlTranscriptReader, tmp_path: Path) -> None:
        """Skips user entries after the last assistant entry."""
        transcript = tmp_path / "transcript.jsonl"
        lines = [
            _assistant_entry(input_tokens=1, cache_read_input_tokens=150_000),
            _user_entry(),
        ]
        transcript.write_text("\n".join(lines) + "\n", encoding="utf-8")

        result = reader.read_latest_tokens(str(transcript))
        assert result == 1 + 150_000  # 150_001

    def test_skips_trailing_progress_entries(
        self, reader: JsonlTranscriptReader, tmp_path: Path
    ) -> None:
        """Skips progress entries after the last assistant entry."""
        transcript = tmp_path / "transcript.jsonl"
        lines = [
            _assistant_entry(input_tokens=5, cache_read_input_tokens=100_000),
            _progress_entry(),
            _progress_entry(),
            _user_entry(),
        ]
        transcript.write_text("\n".join(lines) + "\n", encoding="utf-8")

        result = reader.read_latest_tokens(str(transcript))
        assert result == 5 + 100_000  # 100_005

    def test_reads_last_assistant_not_first(
        self, reader: JsonlTranscriptReader, tmp_path: Path
    ) -> None:
        """With multiple assistant entries, returns data from the last one."""
        transcript = tmp_path / "transcript.jsonl"
        lines = [
            _assistant_entry(input_tokens=1, cache_read_input_tokens=50_000),
            _user_entry(),
            _assistant_entry(input_tokens=1, cache_read_input_tokens=120_000),
            _user_entry(),
            _assistant_entry(
                input_tokens=1,
                cache_creation_input_tokens=500,
                cache_read_input_tokens=158_000,
            ),
        ]
        transcript.write_text("\n".join(lines) + "\n", encoding="utf-8")

        result = reader.read_latest_tokens(str(transcript))
        assert result == 1 + 500 + 158_000  # 158_501


# =============================================================================
# BDD Scenario: FileNotFoundError on missing file
# =============================================================================


class TestFileNotFoundError:
    """Scenario: JsonlTranscriptReader raises FileNotFoundError for missing file."""

    def test_raises_file_not_found_for_missing_file(
        self, reader: JsonlTranscriptReader, tmp_path: Path
    ) -> None:
        """FileNotFoundError raised when file does not exist."""
        missing_path = str(tmp_path / "nonexistent.jsonl")
        with pytest.raises(FileNotFoundError):
            reader.read_latest_tokens(missing_path)


# =============================================================================
# BDD Scenario: ValueError on empty file or no usage entries
# =============================================================================


class TestValueErrorOnInvalidContent:
    """Scenario: ValueError raised for files with no usable usage data."""

    def test_raises_value_error_for_empty_file(
        self, reader: JsonlTranscriptReader, tmp_path: Path
    ) -> None:
        """ValueError raised when JSONL file is empty."""
        empty_file = tmp_path / "empty.jsonl"
        empty_file.write_text("", encoding="utf-8")
        with pytest.raises(ValueError):
            reader.read_latest_tokens(str(empty_file))

    def test_raises_value_error_for_blank_lines_only(
        self, reader: JsonlTranscriptReader, tmp_path: Path
    ) -> None:
        """ValueError raised when JSONL file contains only whitespace."""
        blank_file = tmp_path / "blank.jsonl"
        blank_file.write_text("\n\n\n", encoding="utf-8")
        with pytest.raises(ValueError):
            reader.read_latest_tokens(str(blank_file))

    def test_raises_value_error_for_no_usage_entries(
        self, reader: JsonlTranscriptReader, tmp_path: Path
    ) -> None:
        """ValueError raised when file has no entries with message.usage."""
        transcript = tmp_path / "no_usage.jsonl"
        lines = [_user_entry(), _progress_entry(), _user_entry()]
        transcript.write_text("\n".join(lines) + "\n", encoding="utf-8")
        with pytest.raises(ValueError):
            reader.read_latest_tokens(str(transcript))


# =============================================================================
# BDD Scenario: Missing cache fields treated as zero
# =============================================================================


class TestMissingCacheFieldsDefault:
    """Scenario: Entries with missing cache fields default to zero.

    Claude Code's usage object may not always include cache fields.
    Missing cache_creation_input_tokens or cache_read_input_tokens
    should default to 0 rather than raising an error.
    """

    def test_missing_cache_creation_defaults_to_zero(
        self, reader: JsonlTranscriptReader, tmp_path: Path
    ) -> None:
        """Missing cache_creation_input_tokens treated as 0."""
        transcript = tmp_path / "transcript.jsonl"
        entry = {
            "type": "assistant",
            "message": {
                "usage": {
                    "input_tokens": 50_000,
                    "cache_read_input_tokens": 100_000,
                    "output_tokens": 500,
                },
            },
        }
        transcript.write_text(json.dumps(entry) + "\n", encoding="utf-8")

        result = reader.read_latest_tokens(str(transcript))
        assert result == 50_000 + 100_000  # 150_000

    def test_missing_both_cache_fields_returns_input_tokens(
        self, reader: JsonlTranscriptReader, tmp_path: Path
    ) -> None:
        """Missing both cache fields returns just input_tokens."""
        transcript = tmp_path / "transcript.jsonl"
        entry = {
            "type": "assistant",
            "message": {
                "usage": {
                    "input_tokens": 75_000,
                    "output_tokens": 200,
                },
            },
        }
        transcript.write_text(json.dumps(entry) + "\n", encoding="utf-8")

        result = reader.read_latest_tokens(str(transcript))
        assert result == 75_000


# =============================================================================
# BDD Scenario: Large JSONL entries (> 4096 bytes) read correctly
# =============================================================================


class TestLargeJsonlEntries:
    """Scenario: Reader handles entries larger than _READ_BLOCK_SIZE (4096)."""

    def test_last_entry_exceeds_block_size(
        self, reader: JsonlTranscriptReader, tmp_path: Path
    ) -> None:
        """Last entry > 4096 bytes returns correct token sum."""
        transcript = tmp_path / "large_entry.jsonl"
        small_line = _assistant_entry(input_tokens=1, cache_read_input_tokens=10_000)
        # Build a large assistant entry
        large_entry = {
            "type": "assistant",
            "message": {
                "content": [{"type": "text", "text": "x" * 8000}],
                "usage": {
                    "input_tokens": 5,
                    "cache_creation_input_tokens": 1_000,
                    "cache_read_input_tokens": 180_000,
                    "output_tokens": 500,
                },
            },
        }
        large_line = json.dumps(large_entry)
        assert len(large_line.encode("utf-8")) > 4096
        transcript.write_text(small_line + "\n" + large_line + "\n", encoding="utf-8")

        result = reader.read_latest_tokens(str(transcript))
        assert result == 5 + 1_000 + 180_000  # 181_005

    def test_single_large_entry(self, reader: JsonlTranscriptReader, tmp_path: Path) -> None:
        """Single entry > 4096 bytes."""
        transcript = tmp_path / "single_large.jsonl"
        entry = {
            "type": "assistant",
            "message": {
                "content": [{"type": "text", "text": "y" * 10_000}],
                "usage": {
                    "input_tokens": 10,
                    "cache_read_input_tokens": 200_000,
                    "output_tokens": 100,
                },
            },
        }
        line = json.dumps(entry)
        assert len(line.encode("utf-8")) > 4096
        transcript.write_text(line + "\n", encoding="utf-8")

        result = reader.read_latest_tokens(str(transcript))
        assert result == 10 + 200_000  # 200_010
