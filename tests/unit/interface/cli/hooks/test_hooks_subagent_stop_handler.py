# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for HooksSubagentStopHandler.

BDD scenarios:
    - Handler records agent completion to lifecycle file
    - Handler always returns approve decision
    - Handler is fail-open: errors log to stderr and exit 0
    - Handler handles missing/empty lifecycle file gracefully

References:
    - EN-017: Sub-Agent Lifecycle Hooks
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from src.interface.cli.hooks.hooks_subagent_stop_handler import (
    HooksSubagentStopHandler,
)

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def lifecycle_dir(tmp_path: Path) -> Path:
    """Create a temporary lifecycle directory."""
    d = tmp_path / ".jerry" / "local"
    d.mkdir(parents=True)
    return d


@pytest.fixture()
def handler(lifecycle_dir: Path) -> HooksSubagentStopHandler:
    """Create a handler with temporary lifecycle directory."""
    return HooksSubagentStopHandler(lifecycle_dir=lifecycle_dir)


# =============================================================================
# Tests: Always approves
# =============================================================================


class TestAlwaysApproves:
    """BDD: Handler always returns approve decision."""

    def test_returns_approve_decision(
        self,
        handler: HooksSubagentStopHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Handler always outputs approve decision."""
        hook_input = json.dumps(
            {
                "session_id": "session-abc",
                "hook_event_name": "SubagentStop",
            }
        )

        exit_code = handler.handle(hook_input)

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result["decision"] == "approve"

    def test_always_returns_zero(
        self,
        handler: HooksSubagentStopHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Handler always returns exit code 0."""
        exit_code = handler.handle("invalid-json")

        assert exit_code == 0


# =============================================================================
# Tests: Records agent completion
# =============================================================================


class TestRecordsCompletion:
    """BDD: Handler records agent completion to lifecycle file."""

    def test_records_agent_with_agent_id(
        self,
        handler: HooksSubagentStopHandler,
        lifecycle_dir: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Agent completion with agent_id is recorded."""
        hook_input = json.dumps(
            {
                "session_id": "session-abc",
                "agent_id": "a01ef61",
                "agent_type": "Explore",
                "agent_transcript_path": "/path/to/transcript.jsonl",
            }
        )

        handler.handle(hook_input)

        lifecycle_file = lifecycle_dir / "subagent-lifecycle.json"
        assert lifecycle_file.exists()
        data = json.loads(lifecycle_file.read_text())
        assert "a01ef61" in data["agents"]
        agent = data["agents"]["a01ef61"]
        assert agent["session_id"] == "session-abc"
        assert agent["agent_type"] == "Explore"
        assert agent["status"] == "completed"
        assert agent["transcript_path"] == "/path/to/transcript.jsonl"
        assert "completed_at" in agent

    def test_records_agent_with_agent_name_fallback(
        self,
        handler: HooksSubagentStopHandler,
        lifecycle_dir: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Falls back to agent_name when agent_id not present."""
        hook_input = json.dumps(
            {
                "session_id": "session-def",
                "agent_name": "my-explorer",
            }
        )

        handler.handle(hook_input)

        lifecycle_file = lifecycle_dir / "subagent-lifecycle.json"
        data = json.loads(lifecycle_file.read_text())
        assert "my-explorer" in data["agents"]

    def test_records_multiple_agents(
        self,
        handler: HooksSubagentStopHandler,
        lifecycle_dir: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Multiple agent completions are accumulated."""
        for i in range(3):
            hook_input = json.dumps(
                {
                    "session_id": "session-abc",
                    "agent_id": f"agent-{i}",
                    "agent_type": "Explore",
                }
            )
            handler.handle(hook_input)

        lifecycle_file = lifecycle_dir / "subagent-lifecycle.json"
        data = json.loads(lifecycle_file.read_text())
        assert len(data["agents"]) == 3
        for i in range(3):
            assert f"agent-{i}" in data["agents"]

    def test_uses_transcript_path_fallback(
        self,
        handler: HooksSubagentStopHandler,
        lifecycle_dir: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Falls back to transcript_path when agent_transcript_path not present."""
        hook_input = json.dumps(
            {
                "session_id": "session-abc",
                "agent_id": "agent-1",
                "transcript_path": "/fallback/path.jsonl",
            }
        )

        handler.handle(hook_input)

        lifecycle_file = lifecycle_dir / "subagent-lifecycle.json"
        data = json.loads(lifecycle_file.read_text())
        assert data["agents"]["agent-1"]["transcript_path"] == "/fallback/path.jsonl"


# =============================================================================
# Tests: Fail-open behavior
# =============================================================================


class TestFailOpen:
    """BDD: Handler is fail-open on all errors."""

    def test_invalid_json_still_approves(
        self,
        handler: HooksSubagentStopHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Invalid JSON input still produces approve decision."""
        exit_code = handler.handle("not-json")

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result["decision"] == "approve"

    def test_none_stdin_still_approves(
        self,
        handler: HooksSubagentStopHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """FOS-001: None stdin (TypeError) still produces approve decision."""
        exit_code = handler.handle(None)  # type: ignore[arg-type]

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result["decision"] == "approve"

    @pytest.mark.skipif(
        sys.platform == "win32",
        reason="chmod(0o444) does not enforce read-only directories on Windows",
    )
    def test_readonly_dir_still_approves(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When lifecycle dir is read-only, handler still approves."""
        readonly_dir = tmp_path / "readonly"
        readonly_dir.mkdir()
        readonly_dir.chmod(0o444)

        handler = HooksSubagentStopHandler(lifecycle_dir=readonly_dir)
        hook_input = json.dumps(
            {
                "session_id": "session-abc",
                "agent_id": "agent-1",
            }
        )

        exit_code = handler.handle(hook_input)

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result["decision"] == "approve"
        assert "Lifecycle record failed" in captured.err

        # Cleanup: restore permissions for tmp_path cleanup
        readonly_dir.chmod(0o755)

    def test_no_session_id_no_agent_id_skips_recording(
        self,
        handler: HooksSubagentStopHandler,
        lifecycle_dir: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When both session_id and agent_id are empty, skips recording."""
        hook_input = json.dumps({"hook_event_name": "SubagentStop"})

        handler.handle(hook_input)

        lifecycle_file = lifecycle_dir / "subagent-lifecycle.json"
        assert not lifecycle_file.exists()

    def test_lifecycle_file_created_on_first_write(
        self,
        handler: HooksSubagentStopHandler,
        lifecycle_dir: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Lifecycle file is created if it doesn't exist."""
        lifecycle_file = lifecycle_dir / "subagent-lifecycle.json"
        assert not lifecycle_file.exists()

        hook_input = json.dumps({"session_id": "session-abc", "agent_id": "agent-1"})
        handler.handle(hook_input)

        assert lifecycle_file.exists()
