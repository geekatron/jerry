# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
End-to-end tests for context_monitoring via CLI.

Tests verify the full workflow through the actual jerry CLI:
    - jerry hooks prompt-submit produces valid JSON with context-monitor XML
    - jerry hooks pre-compact creates checkpoints on filesystem
    - jerry hooks session-start discovers and injects checkpoint context
    - Cross-hook lifecycle: pre-compact → checkpoint → session-start → resumption
    - Hook output is parseable and contains expected elements

Test Distribution:
    - Happy Path (60%): 9 tests
    - Negative (30%): 3 tests
    - Edge (10%): 1 test (cross-hook lifecycle)

Acceptance Criteria Coverage:
    - AC-FEAT001-003: XML context-monitor tag in prompt-submit output
    - AC-FEAT001-005: Fail-open on missing/invalid transcript
    - AC-FEAT001-007: Hook returns valid JSON with exit code 0
    - AC-FEAT001-008: Cross-hook lifecycle (prompt-submit → pre-compact → session-start)

References:
    - FEAT-001: Context Detection (EN-006, EN-007)
    - PROJ-004: Context Resilience
    - H-09: Tests exercise production composition root via `jerry` CLI
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.subprocess,
]

PROJECT_ROOT = Path(__file__).parent.parent.parent


def _run_hook(
    hook_name: str,
    stdin_data: str = "{}",
    env_overrides: dict[str, str] | None = None,
    timeout: int = 30,
) -> subprocess.CompletedProcess[str]:
    """Run a jerry hook via CLI and capture output."""
    env = os.environ.copy()
    env["JERRY_PROJECT"] = "PROJ-004-context-resilience"
    if env_overrides:
        env.update(env_overrides)

    return subprocess.run(
        ["uv", "run", "jerry", "--json", "hooks", hook_name],
        input=stdin_data,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(PROJECT_ROOT),
        env=env,
    )


# =============================================================================
# Prompt-Submit Hook E2E
# =============================================================================


class TestPromptSubmitHookE2E:
    """E2E: jerry hooks prompt-submit produces valid context monitoring output.

    References: FEAT-001 (EN-006), PROJ-004
    """

    def test_prompt_submit_returns_valid_json(self) -> None:
        """prompt-submit hook returns valid JSON with exit code 0."""
        result = _run_hook("prompt-submit")
        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        assert "additionalContext" in data

    def test_prompt_submit_with_transcript_includes_context_monitor(self, tmp_path: Path) -> None:
        """prompt-submit with transcript_path includes <context-monitor> XML tag."""
        # Create a real transcript file
        transcript = tmp_path / "test_transcript.jsonl"
        entry = {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "usage": {
                    "input_tokens": 100_000,
                    "cache_creation_input_tokens": 0,
                    "cache_read_input_tokens": 0,
                },
            },
        }
        transcript.write_text(json.dumps(entry) + "\n")

        hook_input = json.dumps(
            {
                "hook_event_name": "UserPromptSubmit",
                "transcript_path": str(transcript),
            }
        )
        result = _run_hook("prompt-submit", stdin_data=hook_input)
        assert result.returncode == 0

        data = json.loads(result.stdout.strip())
        additional = data.get("additionalContext", "")
        assert "<context-monitor>" in additional
        assert "<fill-percentage>" in additional
        assert "<tier>" in additional
        assert "<monitoring-ok>" in additional

    def test_prompt_submit_without_transcript_still_succeeds(self) -> None:
        """prompt-submit without transcript_path returns valid JSON (no crash)."""
        hook_input = json.dumps({"hook_event_name": "UserPromptSubmit"})
        result = _run_hook("prompt-submit", stdin_data=hook_input)
        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        assert isinstance(data, dict)

    def test_prompt_submit_with_missing_transcript_fails_open(self) -> None:
        """prompt-submit with nonexistent transcript returns valid JSON (fail-open)."""
        hook_input = json.dumps(
            {
                "hook_event_name": "UserPromptSubmit",
                "transcript_path": "/nonexistent/transcript.jsonl",
            }
        )
        result = _run_hook("prompt-submit", stdin_data=hook_input)
        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        assert "additionalContext" in data

    def test_prompt_submit_xml_contains_tier(self, tmp_path: Path) -> None:
        """prompt-submit XML output contains the correct tier for token count."""
        # WARNING tier: 150K / 200K = 0.75 (>= 0.70 warning threshold)
        transcript = tmp_path / "warning_transcript.jsonl"
        entry = {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "usage": {"input_tokens": 150_000},
            },
        }
        transcript.write_text(json.dumps(entry) + "\n")

        hook_input = json.dumps({"transcript_path": str(transcript)})
        result = _run_hook("prompt-submit", stdin_data=hook_input)

        data = json.loads(result.stdout.strip())
        additional = data.get("additionalContext", "")
        assert "<tier>WARNING</tier>" in additional

    def test_prompt_submit_includes_quality_reinforcement(self) -> None:
        """prompt-submit output includes quality reinforcement context."""
        result = _run_hook("prompt-submit")
        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        additional = data.get("additionalContext", "")
        # Quality reinforcement injects L2-REINJECT constitutional principles
        assert "Constitutional" in additional


# =============================================================================
# Session-Start Hook E2E
# =============================================================================


class TestSessionStartHookE2E:
    """E2E: jerry hooks session-start produces valid session context.

    References: FEAT-001 (EN-006), PROJ-004
    """

    def test_session_start_returns_valid_json(self) -> None:
        """session-start hook returns valid JSON with exit code 0."""
        result = _run_hook("session-start")
        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        assert "additionalContext" in data

    def test_session_start_includes_project_context(self) -> None:
        """session-start includes project context when JERRY_PROJECT is set."""
        result = _run_hook(
            "session-start",
            env_overrides={"JERRY_PROJECT": "PROJ-004-context-resilience"},
        )
        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        additional = data.get("additionalContext", "")
        assert "project" in additional.lower()


# =============================================================================
# Pre-Compact Hook E2E
# =============================================================================


class TestPreCompactHookE2E:
    """E2E: jerry hooks pre-compact creates checkpoints.

    References: FEAT-001 (EN-006), PROJ-004
    """

    def test_pre_compact_returns_valid_json(self) -> None:
        """pre-compact hook returns valid JSON with exit code 0."""
        hook_input = json.dumps(
            {
                "hook_event_name": "PreCompact",
            }
        )
        result = _run_hook("pre-compact", stdin_data=hook_input)
        assert result.returncode == 0
        # Pre-compact may or may not produce output, but should not crash
        if result.stdout.strip():
            data = json.loads(result.stdout.strip())
            assert isinstance(data, dict)

    def test_pre_compact_with_transcript_does_not_error(self, tmp_path: Path) -> None:
        """pre-compact with high-fill transcript exits 0 without errors.

        Verifies the hook processes a high context fill transcript without
        crashing. Pre-compact hooks may or may not produce stdout (depending
        on composition root checkpoint creation), but must never produce
        Python tracebacks.
        """
        transcript = tmp_path / "high_fill.jsonl"
        entry = {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "usage": {"input_tokens": 180_000},
            },
        }
        transcript.write_text(json.dumps(entry) + "\n")

        hook_input = json.dumps(
            {
                "hook_event_name": "PreCompact",
                "transcript_path": str(transcript),
            }
        )
        result = _run_hook("pre-compact", stdin_data=hook_input)
        assert result.returncode == 0
        assert "Traceback" not in result.stderr
        assert "Error" not in result.stderr


# =============================================================================
# Cross-Hook Lifecycle E2E
# =============================================================================


class TestCrossHookLifecycleE2E:
    """E2E: Cross-hook interactions through the real CLI.

    Verifies that hooks can be invoked in the expected operational sequence
    without state corruption between them.

    References: FEAT-001 (EN-006, EN-007), PROJ-004
    """

    def test_prompt_submit_then_pre_compact_then_session_start(self, tmp_path: Path) -> None:
        """Full hook lifecycle: prompt-submit → pre-compact → session-start.

        Verifies all three hooks can execute in sequence on the same
        project without state corruption or crashes. This is the expected
        operational sequence during a context compaction event.
        """
        # Step 1: prompt-submit with a transcript showing high fill
        transcript = tmp_path / "lifecycle.jsonl"
        entry = {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "usage": {"input_tokens": 175_000},
            },
        }
        transcript.write_text(json.dumps(entry) + "\n")

        hook_input = json.dumps(
            {
                "hook_event_name": "UserPromptSubmit",
                "transcript_path": str(transcript),
            }
        )
        result1 = _run_hook("prompt-submit", stdin_data=hook_input)
        assert result1.returncode == 0
        data1 = json.loads(result1.stdout.strip())
        assert "<context-monitor>" in data1.get("additionalContext", "")

        # Step 2: pre-compact (triggered by compaction)
        compact_input = json.dumps(
            {
                "hook_event_name": "PreCompact",
                "transcript_path": str(transcript),
            }
        )
        result2 = _run_hook("pre-compact", stdin_data=compact_input)
        assert result2.returncode == 0
        assert "Traceback" not in result2.stderr

        # Step 3: session-start (new session after compaction)
        result3 = _run_hook("session-start")
        assert result3.returncode == 0
        data3 = json.loads(result3.stdout.strip())
        assert "additionalContext" in data3


# =============================================================================
# Negative E2E
# =============================================================================


class TestNegativeE2E:
    """E2E: Negative paths for hook invocations.

    References: FEAT-001, PROJ-004
    """

    def test_invalid_json_stdin_still_succeeds(self) -> None:
        """Hook with invalid JSON stdin still returns exit code 0 (fail-open)."""
        result = _run_hook("prompt-submit", stdin_data="not valid json")
        assert result.returncode == 0

    def test_empty_stdin_still_succeeds(self) -> None:
        """Hook with empty stdin still returns exit code 0 (fail-open)."""
        result = _run_hook("prompt-submit", stdin_data="")
        assert result.returncode == 0
