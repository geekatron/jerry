# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Integration tests for session-start hook quality context injection.

Verifies that the SessionStart hook (via jerry hooks session-start CLI)
correctly integrates the quality framework preamble into its output
without breaking existing project context functionality.

Test naming follows BDD convention:
    test_{scenario}_when_{condition}_then_{expected}

References:
    - EN-006: jerry hooks CLI Command Namespace
    - EN-007: Hook Wrapper Scripts
    - EN-706: SessionStart Quality Context Injection
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

# Project root for running the hook
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def run_hook(env_overrides: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    """Run the session-start hook via CLI and capture output.

    Args:
        env_overrides: Optional environment variable overrides.

    Returns:
        CompletedProcess with captured stdout/stderr.
    """
    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)

    return subprocess.run(
        ["uv", "run", "jerry", "--json", "hooks", "session-start"],
        input="{}",
        capture_output=True,
        text=True,
        timeout=60,
        cwd=str(PROJECT_ROOT),
        env=env,
    )


@pytest.mark.subprocess
class TestHookOutputFormat:
    """Tests for hook JSON output structure and quality context."""

    def test_hook_output_when_executed_then_produces_valid_json(self) -> None:
        """Hook always produces valid JSON output regardless of project state."""
        result = run_hook()

        # Hook should exit 0 (fail-open)
        assert result.returncode == 0, f"Hook exited with {result.returncode}: {result.stderr}"

        # Output must be valid JSON
        output = result.stdout.strip()
        assert output, "Hook produced no output"

        data = json.loads(output)
        assert "additionalContext" in data

    def test_hook_output_when_executed_then_contains_quality_context(self) -> None:
        """Hook output includes quality reinforcement content."""
        result = run_hook()

        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        additional = data["additionalContext"]

        # Quality reinforcement should contain constitutional principles
        assert "P-003" in additional or "P-020" in additional, (
            f"additionalContext should contain quality reinforcement. Got: {additional[:200]}..."
        )

    def test_hook_output_when_executed_then_preserves_project_context(self) -> None:
        """Hook still produces project context alongside quality context."""
        result = run_hook()

        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        additional = data["additionalContext"]

        # Must contain project context tags
        has_project_info = "<project-context>" in additional or "<jerry-project>" in additional
        assert has_project_info, (
            f"Hook output missing project context tags. additionalContext: {additional[:200]}..."
        )

    def test_hook_output_when_executed_then_quality_appears_after_project(self) -> None:
        """Quality context appears after the project context in output."""
        result = run_hook()

        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        additional = data["additionalContext"]

        # If both are present, quality reinforcement should come after project
        if "P-003" in additional and "<project-context>" in additional:
            project_pos = additional.index("<project-context>")
            quality_pos = additional.index("P-003")
            assert quality_pos > project_pos, "Quality context should appear after project context"
