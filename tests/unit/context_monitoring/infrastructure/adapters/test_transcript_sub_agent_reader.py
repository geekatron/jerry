# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for TranscriptSubAgentReader.

BDD scenarios:
    - Reads agent metadata from lifecycle file
    - Parses transcript JSONL for last usage entry
    - Computes fill percentage from context_window_size
    - Handles missing/empty lifecycle file gracefully
    - Handles missing/empty/corrupt transcript files gracefully
    - Returns empty list when no agents recorded

References:
    - EN-018: Sub-Agent Transcript Parser
    - EN-017: Sub-Agent Lifecycle Hooks
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.context_monitoring.infrastructure.adapters.transcript_sub_agent_reader import (
    TranscriptSubAgentReader,
)

# =============================================================================
# Helpers
# =============================================================================


def _write_lifecycle(path: Path, agents: dict) -> None:
    """Write a lifecycle JSON file with the given agents dict."""
    data = {"agents": agents, "updated_at": "2026-02-21T12:00:00+00:00"}
    path.write_text(json.dumps(data), encoding="utf-8")


def _write_transcript(path: Path, entries: list[dict]) -> None:
    """Write a JSONL transcript file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(entry) for entry in entries]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _make_assistant_entry(
    input_tokens: int = 5000,
    cache_creation: int = 1000,
    cache_read: int = 2000,
    output_tokens: int = 500,
) -> dict:
    """Create a Claude Code assistant JSONL entry with usage data."""
    return {
        "type": "assistant",
        "message": {
            "usage": {
                "input_tokens": input_tokens,
                "cache_creation_input_tokens": cache_creation,
                "cache_read_input_tokens": cache_read,
                "output_tokens": output_tokens,
            }
        },
    }


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def lifecycle_path(tmp_path: Path) -> Path:
    """Path for the lifecycle JSON file."""
    return tmp_path / ".jerry" / "local" / "subagent-lifecycle.json"


@pytest.fixture()
def reader(lifecycle_path: Path) -> TranscriptSubAgentReader:
    """Create reader with temporary lifecycle path."""
    return TranscriptSubAgentReader(lifecycle_path=lifecycle_path)


# =============================================================================
# Tests: Reads agent metadata
# =============================================================================


class TestReadsAgentMetadata:
    """BDD: Reads agent metadata from lifecycle file."""

    def test_reads_single_agent(
        self,
        reader: TranscriptSubAgentReader,
        lifecycle_path: Path,
        tmp_path: Path,
    ) -> None:
        """Single agent with transcript is read correctly."""
        transcript = tmp_path / "agent-abc.jsonl"
        _write_transcript(transcript, [_make_assistant_entry()])

        lifecycle_path.parent.mkdir(parents=True, exist_ok=True)
        _write_lifecycle(
            lifecycle_path,
            {
                "abc": {
                    "session_id": "sess-1",
                    "agent_type": "Explore",
                    "model": "claude-opus-4-6",
                    "status": "completed",
                    "transcript_path": str(transcript),
                }
            },
        )

        agents = reader.read_sub_agents(context_window_size=200_000)

        assert len(agents) == 1
        assert agents[0].agent_id == "abc"
        assert agents[0].agent_type == "Explore"
        assert agents[0].model == "claude-opus-4-6"
        assert agents[0].status == "completed"

    def test_reads_multiple_agents(
        self,
        reader: TranscriptSubAgentReader,
        lifecycle_path: Path,
        tmp_path: Path,
    ) -> None:
        """Multiple agents are all returned."""
        lifecycle_path.parent.mkdir(parents=True, exist_ok=True)
        agents_data = {}
        for i in range(3):
            transcript = tmp_path / f"agent-{i}.jsonl"
            _write_transcript(transcript, [_make_assistant_entry()])
            agents_data[f"agent-{i}"] = {
                "session_id": "sess-1",
                "agent_type": "Explore",
                "status": "completed",
                "transcript_path": str(transcript),
            }

        _write_lifecycle(lifecycle_path, agents_data)

        agents = reader.read_sub_agents(context_window_size=200_000)

        assert len(agents) == 3
        agent_ids = {a.agent_id for a in agents}
        assert agent_ids == {"agent-0", "agent-1", "agent-2"}

    def test_agent_without_model_defaults_empty(
        self,
        reader: TranscriptSubAgentReader,
        lifecycle_path: Path,
    ) -> None:
        """Agent without model field gets empty string."""
        lifecycle_path.parent.mkdir(parents=True, exist_ok=True)
        _write_lifecycle(
            lifecycle_path,
            {
                "abc": {
                    "session_id": "sess-1",
                    "agent_type": "Bash",
                    "status": "completed",
                }
            },
        )

        agents = reader.read_sub_agents(context_window_size=200_000)

        assert len(agents) == 1
        assert agents[0].model == ""


# =============================================================================
# Tests: Parses transcript for usage
# =============================================================================


class TestParsesTranscriptUsage:
    """BDD: Parses JSONL transcript for last usage entry."""

    def test_extracts_context_tokens(
        self,
        reader: TranscriptSubAgentReader,
        lifecycle_path: Path,
        tmp_path: Path,
    ) -> None:
        """Context tokens = input + cache_creation + cache_read."""
        transcript = tmp_path / "agent.jsonl"
        _write_transcript(
            transcript,
            [
                _make_assistant_entry(
                    input_tokens=5000,
                    cache_creation=1000,
                    cache_read=2000,
                    output_tokens=800,
                ),
            ],
        )

        lifecycle_path.parent.mkdir(parents=True, exist_ok=True)
        _write_lifecycle(
            lifecycle_path,
            {
                "abc": {
                    "session_id": "sess-1",
                    "agent_type": "Explore",
                    "status": "completed",
                    "transcript_path": str(transcript),
                }
            },
        )

        agents = reader.read_sub_agents(context_window_size=200_000)

        assert agents[0].context_tokens == 8000  # 5000 + 1000 + 2000
        assert agents[0].output_tokens == 800

    def test_uses_last_usage_entry(
        self,
        reader: TranscriptSubAgentReader,
        lifecycle_path: Path,
        tmp_path: Path,
    ) -> None:
        """Last usage entry is cumulative — use it directly."""
        transcript = tmp_path / "agent.jsonl"
        _write_transcript(
            transcript,
            [
                _make_assistant_entry(input_tokens=1000, cache_creation=0, cache_read=0),
                {"type": "user", "message": {"content": "hello"}},
                _make_assistant_entry(
                    input_tokens=10000,
                    cache_creation=3000,
                    cache_read=5000,
                    output_tokens=2000,
                ),
            ],
        )

        lifecycle_path.parent.mkdir(parents=True, exist_ok=True)
        _write_lifecycle(
            lifecycle_path,
            {
                "abc": {
                    "session_id": "sess-1",
                    "agent_type": "Explore",
                    "status": "completed",
                    "transcript_path": str(transcript),
                }
            },
        )

        agents = reader.read_sub_agents(context_window_size=200_000)

        # Last entry: 10000 + 3000 + 5000 = 18000
        assert agents[0].context_tokens == 18000
        assert agents[0].output_tokens == 2000

    def test_skips_non_assistant_entries(
        self,
        reader: TranscriptSubAgentReader,
        lifecycle_path: Path,
        tmp_path: Path,
    ) -> None:
        """Non-assistant entries (user, progress) are skipped."""
        transcript = tmp_path / "agent.jsonl"
        entries = [
            _make_assistant_entry(input_tokens=5000, cache_creation=0, cache_read=0),
            {"type": "user", "message": {"content": "hello"}},
            {"type": "progress", "data": {"percent": 50}},
        ]
        _write_transcript(transcript, entries)

        lifecycle_path.parent.mkdir(parents=True, exist_ok=True)
        _write_lifecycle(
            lifecycle_path,
            {
                "abc": {
                    "session_id": "sess-1",
                    "agent_type": "Explore",
                    "status": "completed",
                    "transcript_path": str(transcript),
                }
            },
        )

        agents = reader.read_sub_agents(context_window_size=200_000)

        # Only assistant entry has usage: 5000
        assert agents[0].context_tokens == 5000


# =============================================================================
# Tests: Fill percentage computation
# =============================================================================


class TestFillPercentage:
    """BDD: Computes fill percentage from context_window_size."""

    def test_computes_fill_percentage(
        self,
        reader: TranscriptSubAgentReader,
        lifecycle_path: Path,
        tmp_path: Path,
    ) -> None:
        """Fill pct = context_tokens / window_size * 100."""
        transcript = tmp_path / "agent.jsonl"
        # 50000 tokens total
        _write_transcript(
            transcript,
            [
                _make_assistant_entry(
                    input_tokens=40000,
                    cache_creation=5000,
                    cache_read=5000,
                    output_tokens=1000,
                ),
            ],
        )

        lifecycle_path.parent.mkdir(parents=True, exist_ok=True)
        _write_lifecycle(
            lifecycle_path,
            {
                "abc": {
                    "session_id": "sess-1",
                    "agent_type": "Explore",
                    "status": "completed",
                    "transcript_path": str(transcript),
                }
            },
        )

        agents = reader.read_sub_agents(context_window_size=200_000)

        assert agents[0].context_fill_pct == 25.0  # 50000 / 200000 * 100

    def test_zero_window_size_gives_zero_fill(
        self,
        reader: TranscriptSubAgentReader,
        lifecycle_path: Path,
        tmp_path: Path,
    ) -> None:
        """Zero context_window_size produces 0% fill (no divide by zero)."""
        transcript = tmp_path / "agent.jsonl"
        _write_transcript(transcript, [_make_assistant_entry()])

        lifecycle_path.parent.mkdir(parents=True, exist_ok=True)
        _write_lifecycle(
            lifecycle_path,
            {
                "abc": {
                    "session_id": "sess-1",
                    "agent_type": "Explore",
                    "status": "completed",
                    "transcript_path": str(transcript),
                }
            },
        )

        agents = reader.read_sub_agents(context_window_size=0)

        assert agents[0].context_fill_pct == 0.0


# =============================================================================
# Tests: Graceful handling of missing/empty data
# =============================================================================


class TestGracefulHandling:
    """BDD: Handles missing/empty/corrupt data gracefully."""

    def test_missing_lifecycle_file_returns_empty(
        self,
        reader: TranscriptSubAgentReader,
    ) -> None:
        """No lifecycle file returns empty list."""
        agents = reader.read_sub_agents(context_window_size=200_000)

        assert agents == []

    def test_empty_lifecycle_file_returns_empty(
        self,
        reader: TranscriptSubAgentReader,
        lifecycle_path: Path,
    ) -> None:
        """Empty lifecycle file returns empty list."""
        lifecycle_path.parent.mkdir(parents=True, exist_ok=True)
        lifecycle_path.write_text("", encoding="utf-8")

        agents = reader.read_sub_agents(context_window_size=200_000)

        assert agents == []

    def test_lifecycle_with_no_agents_key_returns_empty(
        self,
        reader: TranscriptSubAgentReader,
        lifecycle_path: Path,
    ) -> None:
        """Lifecycle file without agents key returns empty list."""
        lifecycle_path.parent.mkdir(parents=True, exist_ok=True)
        lifecycle_path.write_text(json.dumps({"updated_at": "now"}), encoding="utf-8")

        agents = reader.read_sub_agents(context_window_size=200_000)

        assert agents == []

    def test_missing_transcript_returns_zero_tokens(
        self,
        reader: TranscriptSubAgentReader,
        lifecycle_path: Path,
    ) -> None:
        """Agent with missing transcript gets zero tokens."""
        lifecycle_path.parent.mkdir(parents=True, exist_ok=True)
        _write_lifecycle(
            lifecycle_path,
            {
                "abc": {
                    "session_id": "sess-1",
                    "agent_type": "Explore",
                    "status": "completed",
                    "transcript_path": "/nonexistent/transcript.jsonl",
                }
            },
        )

        agents = reader.read_sub_agents(context_window_size=200_000)

        assert len(agents) == 1
        assert agents[0].context_tokens == 0
        assert agents[0].output_tokens == 0
        assert agents[0].context_fill_pct == 0.0

    def test_empty_transcript_returns_zero_tokens(
        self,
        reader: TranscriptSubAgentReader,
        lifecycle_path: Path,
        tmp_path: Path,
    ) -> None:
        """Agent with empty transcript gets zero tokens."""
        transcript = tmp_path / "empty.jsonl"
        transcript.write_text("", encoding="utf-8")

        lifecycle_path.parent.mkdir(parents=True, exist_ok=True)
        _write_lifecycle(
            lifecycle_path,
            {
                "abc": {
                    "session_id": "sess-1",
                    "agent_type": "Explore",
                    "status": "completed",
                    "transcript_path": str(transcript),
                }
            },
        )

        agents = reader.read_sub_agents(context_window_size=200_000)

        assert agents[0].context_tokens == 0

    def test_transcript_with_no_usage_returns_zero_tokens(
        self,
        reader: TranscriptSubAgentReader,
        lifecycle_path: Path,
        tmp_path: Path,
    ) -> None:
        """Transcript with no usage entries gets zero tokens."""
        transcript = tmp_path / "no-usage.jsonl"
        _write_transcript(
            transcript,
            [
                {"type": "user", "message": {"content": "hello"}},
                {"type": "progress", "data": {"percent": 100}},
            ],
        )

        lifecycle_path.parent.mkdir(parents=True, exist_ok=True)
        _write_lifecycle(
            lifecycle_path,
            {
                "abc": {
                    "session_id": "sess-1",
                    "agent_type": "Explore",
                    "status": "completed",
                    "transcript_path": str(transcript),
                }
            },
        )

        agents = reader.read_sub_agents(context_window_size=200_000)

        assert agents[0].context_tokens == 0

    def test_no_transcript_path_returns_zero_tokens(
        self,
        reader: TranscriptSubAgentReader,
        lifecycle_path: Path,
    ) -> None:
        """Agent without transcript_path gets zero tokens."""
        lifecycle_path.parent.mkdir(parents=True, exist_ok=True)
        _write_lifecycle(
            lifecycle_path,
            {
                "abc": {
                    "session_id": "sess-1",
                    "agent_type": "Explore",
                    "status": "completed",
                }
            },
        )

        agents = reader.read_sub_agents(context_window_size=200_000)

        assert agents[0].context_tokens == 0
        assert agents[0].output_tokens == 0

    def test_corrupt_lifecycle_json_returns_empty(
        self,
        reader: TranscriptSubAgentReader,
        lifecycle_path: Path,
    ) -> None:
        """Corrupt lifecycle JSON returns empty list."""
        lifecycle_path.parent.mkdir(parents=True, exist_ok=True)
        lifecycle_path.write_text("{invalid json", encoding="utf-8")

        agents = reader.read_sub_agents(context_window_size=200_000)

        assert agents == []

    def test_corrupt_transcript_returns_zero_tokens(
        self,
        reader: TranscriptSubAgentReader,
        lifecycle_path: Path,
        tmp_path: Path,
    ) -> None:
        """Corrupt transcript JSONL returns zero tokens."""
        transcript = tmp_path / "corrupt.jsonl"
        transcript.write_text("not valid json at all\n", encoding="utf-8")

        lifecycle_path.parent.mkdir(parents=True, exist_ok=True)
        _write_lifecycle(
            lifecycle_path,
            {
                "abc": {
                    "session_id": "sess-1",
                    "agent_type": "Explore",
                    "status": "completed",
                    "transcript_path": str(transcript),
                }
            },
        )

        agents = reader.read_sub_agents(context_window_size=200_000)

        assert agents[0].context_tokens == 0
