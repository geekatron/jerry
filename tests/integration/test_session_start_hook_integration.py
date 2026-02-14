"""
Integration tests for session_start_hook.py quality context injection.

Verifies that the SessionStart hook correctly integrates the quality
framework preamble into its output without breaking existing
project context functionality.

Test naming follows BDD convention:
    test_{scenario}_when_{condition}_then_{expected}

References:
    - EN-706: SessionStart Quality Context Injection
    - scripts/session_start_hook.py: Hook under test
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

# Project root for running the hook
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
HOOK_SCRIPT = PROJECT_ROOT / "scripts" / "session_start_hook.py"


def run_hook(env_overrides: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    """Run the session_start_hook.py and capture output.

    Args:
        env_overrides: Optional environment variable overrides.

    Returns:
        CompletedProcess with captured stdout/stderr.
    """
    import os

    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)

    return subprocess.run(
        [sys.executable, str(HOOK_SCRIPT)],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=str(PROJECT_ROOT),
        env=env,
    )


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
        assert "systemMessage" in data
        assert "hookSpecificOutput" in data
        assert "additionalContext" in data["hookSpecificOutput"]

    def test_hook_output_when_executed_then_contains_quality_context(self) -> None:
        """Hook output includes quality-context XML wrapper with preamble."""
        result = run_hook()

        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        additional = data["hookSpecificOutput"]["additionalContext"]

        # Quality context should be present
        assert "<quality-context>" in additional
        assert "</quality-context>" in additional
        assert "<quality-framework" in additional

    def test_hook_output_when_executed_then_preserves_project_context(self) -> None:
        """Hook still produces project context alongside quality context."""
        result = run_hook()

        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        additional = data["hookSpecificOutput"]["additionalContext"]

        # Must contain EITHER project-context, project-required, project-error, or hook-error
        has_project_info = any(
            tag in additional
            for tag in [
                "<project-context>",
                "<project-required>",
                "<project-error>",
                "<hook-error>",
            ]
        )
        assert has_project_info, (
            f"Hook output missing project context tags. additionalContext: {additional[:200]}..."
        )

    def test_hook_output_when_executed_then_quality_appears_after_project(self) -> None:
        """Quality context appears after the project context in output."""
        result = run_hook()

        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        additional = data["hookSpecificOutput"]["additionalContext"]

        # If both are present, quality should come after project
        if "<quality-context>" in additional and (
            "<project-context>" in additional or "<project-required>" in additional
        ):
            # Find positions
            quality_pos = additional.index("<quality-context>")
            project_pos = max(
                additional.find("<project-context>"),
                additional.find("<project-required>"),
                additional.find("<project-error>"),
            )
            assert quality_pos > project_pos, "Quality context should appear after project context"
