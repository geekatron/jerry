# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Integration tests for UserPromptSubmit hook with L2 reinforcement.

Tests the full hook pipeline by running hooks/user-prompt-submit.py
as a subprocess, simulating the Claude Code hook protocol.

References:
    - EN-705: L2 Per-Prompt Reinforcement Hook
    - ADR-EPIC002-002: 5-layer enforcement architecture
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HOOKS_DIR = Path(__file__).resolve().parents[2] / "hooks"
HOOK_SCRIPT = HOOKS_DIR / "user-prompt-submit.py"
PROJECT_ROOT = HOOKS_DIR.parent


def run_hook(input_data: str | None = None) -> tuple[int, dict | None, str]:
    """Run the user-prompt-submit.py hook with the given input.

    Args:
        input_data: JSON string to pass via stdin. If None, sends empty JSON.

    Returns:
        Tuple of (exit_code, stdout_json_or_none, stderr_text).
    """
    if input_data is None:
        input_data = json.dumps({"prompt": "test prompt"})

    result = subprocess.run(
        [sys.executable, str(HOOK_SCRIPT)],
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
        # Should have hookSpecificOutput with additionalContext
        hook_output = stdout_json.get("hookSpecificOutput", {})
        additional_context = hook_output.get("additionalContext", "")
        assert "quality-reinforcement" in additional_context

    def test_hook_output_contains_quality_reinforcement_xml_tag(self) -> None:
        """Hook output should wrap content in quality-reinforcement XML tags."""
        exit_code, stdout_json, stderr = run_hook()

        assert exit_code == 0
        assert stdout_json is not None
        additional_context = stdout_json.get("hookSpecificOutput", {}).get("additionalContext", "")
        assert additional_context.startswith("<quality-reinforcement>")
        assert additional_context.endswith("</quality-reinforcement>")

    def test_hook_fails_open_on_missing_rules_file(self) -> None:
        """Hook should return valid JSON even with nonexistent rules file.

        When run from a directory without quality-enforcement.md reachable,
        the hook should still exit 0 and return valid JSON.
        """
        # Run from temp dir which has no CLAUDE.md or rules
        result = subprocess.run(
            [sys.executable, str(HOOK_SCRIPT)],
            input=json.dumps({"prompt": "test"}),
            capture_output=True,
            text=True,
            timeout=15,
            cwd=tempfile.gettempdir(),
        )

        assert result.returncode == 0
        # Output should be valid JSON (either empty {} or with content)
        stdout = result.stdout.strip()
        assert stdout != ""
        parsed = json.loads(stdout)
        assert isinstance(parsed, dict)

    def test_hook_always_exits_zero(self) -> None:
        """Hook should always exit with code 0 (fail-open)."""
        # Even with completely invalid input
        result = subprocess.run(
            [sys.executable, str(HOOK_SCRIPT)],
            input="not json at all",
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(PROJECT_ROOT),
        )

        assert result.returncode == 0
