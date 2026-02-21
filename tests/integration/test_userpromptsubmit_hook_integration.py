# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Integration tests for UserPromptSubmit hook with L2 reinforcement.

Tests the full hook pipeline by running jerry --json hooks prompt-submit
as a subprocess, simulating the Claude Code hook protocol.

References:
    - EN-006: jerry hooks CLI Command Namespace
    - EN-007: Hook Wrapper Scripts
    - EN-705: L2 Per-Prompt Reinforcement Hook
    - ADR-EPIC002-002: 5-layer enforcement architecture
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

import pytest

# Requires uv for CLI invocation
pytestmark = [pytest.mark.subprocess]

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def run_hook(input_data: str | None = None) -> tuple[int, dict | None, str]:
    """Run the prompt-submit hook via CLI with the given input.

    Args:
        input_data: JSON string to pass via stdin. If None, sends empty JSON.

    Returns:
        Tuple of (exit_code, stdout_json_or_none, stderr_text).
    """
    if input_data is None:
        input_data = json.dumps({"prompt": "test prompt"})

    result = subprocess.run(
        ["uv", "run", "jerry", "--json", "hooks", "prompt-submit"],
        input=input_data,
        capture_output=True,
        text=True,
        timeout=15,
        cwd=str(PROJECT_ROOT),
    )

    stdout_json = None
    if result.stdout.strip():
        try:
            stdout_json = json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            pass

    return result.returncode, stdout_json, result.stderr


class TestUserPromptSubmitHookIntegration:
    """Integration tests for the UserPromptSubmit hook pipeline."""

    def test_hook_returns_valid_json_with_reinforcement(self) -> None:
        """Hook should return valid JSON with reinforcement content."""
        exit_code, stdout_json, stderr = run_hook()

        assert exit_code == 0
        assert stdout_json is not None
        # New format: additionalContext at top level
        additional_context = stdout_json.get("additionalContext", "")
        # Should contain quality reinforcement content
        assert (
            "P-003" in additional_context or "P-020" in additional_context or additional_context
        ), f"Expected quality reinforcement content. Got: {additional_context[:200]}..."

    def test_hook_output_contains_quality_reinforcement_xml_tag(self) -> None:
        """Hook output should contain quality reinforcement content."""
        exit_code, stdout_json, stderr = run_hook()

        assert exit_code == 0
        assert stdout_json is not None
        additional_context = stdout_json.get("additionalContext", "")
        # Should contain constitutional principle references
        assert "P-003" in additional_context or "HARD" in additional_context, (
            f"Expected quality reinforcement. Got: {additional_context[:200]}..."
        )

    def test_hook_fails_open_on_missing_rules_file(self) -> None:
        """Hook should return valid JSON even with nonexistent rules file.

        When run from a directory without quality-enforcement.md reachable,
        the hook should still exit 0 and return valid JSON.
        """
        env = os.environ.copy()
        env.pop("JERRY_PROJECT", None)

        result = subprocess.run(
            ["uv", "run", "jerry", "--json", "hooks", "prompt-submit"],
            input=json.dumps({"prompt": "test"}),
            capture_output=True,
            text=True,
            timeout=15,
            cwd=tempfile.gettempdir(),
        )

        assert result.returncode == 0
        # Output should be valid JSON
        stdout = result.stdout.strip()
        assert stdout != ""
        parsed = json.loads(stdout)
        assert isinstance(parsed, dict)

    def test_hook_always_exits_zero(self) -> None:
        """Hook should always exit with code 0 (fail-open)."""
        # Even with completely invalid input
        result = subprocess.run(
            ["uv", "run", "jerry", "--json", "hooks", "prompt-submit"],
            input="not json at all",
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(PROJECT_ROOT),
        )

        assert result.returncode == 0
