# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for SubagentStop hook via CLI pipeline.

Tests the consolidated SubagentStop hook (``uv run jerry hooks subagent-stop``)
which records sub-agent lifecycle data and always approves.

References:
    - EN-017: Sub-Agent Lifecycle Hooks
    - STORY-024: Consolidated dual SubagentStop hooks into CLI
    - FEAT-002: Status Line / Context Monitoring Unification
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

# Repo root for --directory flag
_REPO_ROOT = str(Path(__file__).resolve().parents[2])


# ---------------------------------------------------------------------------
# Subprocess helper
# ---------------------------------------------------------------------------


def run_hook(
    agent_name: str = "unknown",
    agent_output: str = "",
    extra_fields: dict[str, Any] | None = None,
) -> tuple[int, dict[str, Any] | None, str]:
    """Run the SubagentStop hook via CLI.

    Args:
        agent_name: Name of the agent that is stopping.
        agent_output: The agent's output text.
        extra_fields: Additional fields to include in the input JSON.

    Returns:
        Tuple of (exit_code, parsed_stdout_json_or_None, stderr_text).
    """
    input_data: dict[str, Any] = {
        "agent_name": agent_name,
        "output": agent_output,
    }
    if extra_fields:
        input_data.update(extra_fields)

    result = subprocess.run(
        ["uv", "run", "--directory", _REPO_ROOT, "jerry", "--json", "hooks", "subagent-stop"],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
        timeout=15,
    )

    stdout_json = None
    if result.stdout.strip():
        try:
            stdout_json = json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            pass

    return result.returncode, stdout_json, result.stderr


# =============================================================================
# Test: Approve Decision (CLI always approves)
# =============================================================================


class TestAlwaysApprove:
    """CLI SubagentStop handler always approves (never blocks)."""

    def test_normal_agent_stop_approved(self) -> None:
        """Agent with normal output should be approved."""
        exit_code, output, stderr = run_hook(
            agent_name="some-agent",
            agent_output="Just finished my work.",
        )

        assert exit_code == 0
        assert output is not None
        assert output.get("decision") != "block"

    def test_unknown_agent_approved(self) -> None:
        """Unknown agent name should be approved."""
        exit_code, output, stderr = run_hook(
            agent_name="brand-new-agent",
            agent_output="Work done.",
        )

        assert exit_code == 0
        assert output is not None
        assert output.get("decision") != "block"

    def test_empty_output_approved(self) -> None:
        """Agent with empty output should be approved."""
        exit_code, output, stderr = run_hook(
            agent_name="orchestrator",
            agent_output="",
        )

        assert exit_code == 0
        assert output is not None
        assert output.get("decision") != "block"

    def test_agent_with_session_id_approved(self) -> None:
        """Agent with session_id extra field should be approved."""
        exit_code, output, stderr = run_hook(
            agent_name="ps-researcher",
            agent_output="Research complete.",
            extra_fields={"session_id": "test-session-123"},
        )

        assert exit_code == 0
        assert output is not None
        assert output.get("decision") != "block"


# =============================================================================
# Test: Output Format
# =============================================================================


class TestOutputFormat:
    """Tests for hook output format compliance."""

    def test_output_is_valid_json(self) -> None:
        """Hook output must be valid JSON."""
        exit_code, output, stderr = run_hook(agent_name="test-agent")

        assert exit_code == 0
        assert output is not None
        assert isinstance(output, dict)

    def test_output_has_decision_field(self) -> None:
        """Hook output should include a decision field."""
        exit_code, output, stderr = run_hook(agent_name="test-agent")

        assert exit_code == 0
        assert output is not None
        assert "decision" in output

    def test_output_does_not_use_hookspecificoutput(self) -> None:
        """SubagentStop MUST NOT use hookSpecificOutput format."""
        exit_code, output, stderr = run_hook(agent_name="test-agent")

        assert exit_code == 0
        assert output is not None
        assert "hookSpecificOutput" not in output


# =============================================================================
# Test: Exit Code Semantics
# =============================================================================


class TestExitCodes:
    """Tests for hook exit code behavior."""

    def test_normal_input_exits_zero(self) -> None:
        """Normal input should always exit 0."""
        exit_code, _, _ = run_hook(agent_name="test-agent", agent_output="Done.")

        assert exit_code == 0

    def test_empty_json_exits_zero(self) -> None:
        """Empty JSON object should exit 0 (fail-open)."""
        result = subprocess.run(
            ["uv", "run", "--directory", _REPO_ROOT, "jerry", "--json", "hooks", "subagent-stop"],
            input="{}",
            capture_output=True,
            text=True,
            timeout=15,
        )

        assert result.returncode == 0

    def test_missing_agent_name_exits_zero(self) -> None:
        """Missing agent_name should exit 0 (fail-open)."""
        result = subprocess.run(
            ["uv", "run", "--directory", _REPO_ROOT, "jerry", "--json", "hooks", "subagent-stop"],
            input=json.dumps({"output": "test"}),
            capture_output=True,
            text=True,
            timeout=15,
        )

        assert result.returncode == 0

    def test_missing_output_field_exits_zero(self) -> None:
        """Missing output field should exit 0 (fail-open)."""
        result = subprocess.run(
            ["uv", "run", "--directory", _REPO_ROOT, "jerry", "--json", "hooks", "subagent-stop"],
            input=json.dumps({"agent_name": "test"}),
            capture_output=True,
            text=True,
            timeout=15,
        )

        assert result.returncode == 0


# =============================================================================
# Test: Various Agent Types
# =============================================================================


class TestAgentTypes:
    """Tests verifying different agent types are handled correctly."""

    def test_explore_agent_approved(self) -> None:
        """Explore agent type should be approved."""
        exit_code, output, _ = run_hook(
            agent_name="ps-researcher",
            agent_output="Research complete.",
            extra_fields={"agent_type": "Explore"},
        )
        assert exit_code == 0
        assert output is not None
        assert output.get("decision") != "block"

    def test_general_purpose_agent_approved(self) -> None:
        """General-purpose agent type should be approved."""
        exit_code, output, _ = run_hook(
            agent_name="general",
            agent_output="Task finished.",
            extra_fields={"agent_type": "general-purpose"},
        )
        assert exit_code == 0
        assert output is not None
        assert output.get("decision") != "block"

    def test_orchestrator_agent_approved(self) -> None:
        """Orchestrator agent should be approved (no more handoff blocking)."""
        exit_code, output, _ = run_hook(
            agent_name="orchestrator",
            agent_output="Orchestration complete.",
        )
        assert exit_code == 0
        assert output is not None
        assert output.get("decision") != "block"

    def test_agent_with_long_output_approved(self) -> None:
        """Agent with lengthy output should be approved."""
        long_output = "Line of output.\n" * 100
        exit_code, output, _ = run_hook(
            agent_name="verbose-agent",
            agent_output=long_output,
        )
        assert exit_code == 0
        assert output is not None
        assert output.get("decision") != "block"

    def test_agent_with_unicode_output_approved(self) -> None:
        """Agent with unicode output should be approved."""
        exit_code, output, _ = run_hook(
            agent_name="i18n-agent",
            agent_output="Results: 日本語テスト 🎯 données françaises",
        )
        assert exit_code == 0
        assert output is not None
        assert output.get("decision") != "block"

    def test_agent_with_json_in_output_approved(self) -> None:
        """Agent with JSON content in output should be approved."""
        exit_code, output, _ = run_hook(
            agent_name="json-agent",
            agent_output='{"result": "success", "count": 42}',
        )
        assert exit_code == 0
        assert output is not None
        assert output.get("decision") != "block"


# =============================================================================
# Test: Input Robustness
# =============================================================================


class TestInputRobustness:
    """Tests for graceful handling of various input shapes."""

    def test_extra_fields_ignored(self) -> None:
        """Extra fields in input should be ignored gracefully."""
        exit_code, output, _ = run_hook(
            agent_name="test-agent",
            agent_output="Done.",
            extra_fields={"unknown_field": "value", "another": 123},
        )
        assert exit_code == 0
        assert output is not None
        assert output.get("decision") != "block"

    def test_null_agent_name_handled(self) -> None:
        """Null agent_name should be handled gracefully."""
        result = subprocess.run(
            ["uv", "run", "--directory", _REPO_ROOT, "jerry", "--json", "hooks", "subagent-stop"],
            input=json.dumps({"agent_name": None, "output": "done"}),
            capture_output=True,
            text=True,
            timeout=15,
        )
        assert result.returncode == 0

    def test_numeric_agent_name_handled(self) -> None:
        """Numeric agent_name should be handled gracefully."""
        result = subprocess.run(
            ["uv", "run", "--directory", _REPO_ROOT, "jerry", "--json", "hooks", "subagent-stop"],
            input=json.dumps({"agent_name": 12345, "output": "done"}),
            capture_output=True,
            text=True,
            timeout=15,
        )
        assert result.returncode == 0

    def test_empty_string_agent_name_handled(self) -> None:
        """Empty string agent_name should be handled gracefully."""
        exit_code, output, _ = run_hook(agent_name="", agent_output="done")
        assert exit_code == 0
        assert output is not None

    def test_agent_id_field_handled(self) -> None:
        """agent_id field (alternative to agent_name) should be handled."""
        result = subprocess.run(
            ["uv", "run", "--directory", _REPO_ROOT, "jerry", "--json", "hooks", "subagent-stop"],
            input=json.dumps({"agent_id": "abc123", "session_id": "sess-1"}),
            capture_output=True,
            text=True,
            timeout=15,
        )
        assert result.returncode == 0

    def test_transcript_path_recorded(self) -> None:
        """agent_transcript_path should be processed without error."""
        exit_code, output, _ = run_hook(
            agent_name="agent-with-transcript",
            agent_output="done",
            extra_fields={"agent_transcript_path": "/tmp/transcript.jsonl"},
        )
        assert exit_code == 0
        assert output is not None

    def test_session_id_processed(self) -> None:
        """session_id should be processed without error."""
        exit_code, output, _ = run_hook(
            agent_name="session-agent",
            agent_output="done",
            extra_fields={"session_id": "session-xyz-789"},
        )
        assert exit_code == 0
        assert output is not None

    def test_all_fields_combined(self) -> None:
        """All known fields provided together should work."""
        exit_code, output, _ = run_hook(
            agent_name="full-agent",
            agent_output="Complete with all fields.",
            extra_fields={
                "session_id": "session-full",
                "agent_id": "agent-full-id",
                "agent_type": "Explore",
                "agent_transcript_path": "/path/to/transcript.jsonl",
            },
        )
        assert exit_code == 0
        assert output is not None
        assert output.get("decision") != "block"

    def test_invalid_json_exits_zero(self) -> None:
        """Invalid JSON input should still exit 0 (fail-open)."""
        result = subprocess.run(
            ["uv", "run", "--directory", _REPO_ROOT, "jerry", "--json", "hooks", "subagent-stop"],
            input="not valid json at all",
            capture_output=True,
            text=True,
            timeout=15,
        )
        assert result.returncode == 0
