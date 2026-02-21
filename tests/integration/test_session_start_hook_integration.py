# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

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
from unittest.mock import MagicMock, patch

import pytest

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


# ---------------------------------------------------------------------------
# Import check_precommit_hooks for unit-level tests (no subprocess needed)
# ---------------------------------------------------------------------------
# Add project root so we can import directly from scripts/
_project_root = str(PROJECT_ROOT)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from scripts.session_start_hook import check_precommit_hooks  # noqa: E402


class TestPrecommitAutoInstall:
    """Unit tests for pre-commit hook auto-install behaviour (D-003).

    These tests mock subprocess and Path operations — they do NOT
    execute real subprocesses.
    """

    def _make_plugin_root(self, tmp_path: Path) -> Path:
        """Create a minimal plugin_root with .git/hooks directory."""
        git_dir = tmp_path / ".git" / "hooks"
        git_dir.mkdir(parents=True)
        return tmp_path

    # -- auto-install success --------------------------------------------------

    @patch("scripts.session_start_hook.subprocess.run")
    def test_auto_install_when_hooks_missing_and_uv_available_then_runs_precommit_install(
        self, mock_run: MagicMock, tmp_path: Path
    ) -> None:
        """When hooks are missing and uv_path is provided, runs pre-commit install."""
        plugin_root = self._make_plugin_root(tmp_path)
        mock_run.return_value = MagicMock(returncode=0, stderr=b"")

        check_precommit_hooks(plugin_root, uv_path="/usr/bin/uv")

        mock_run.assert_called_once_with(
            ["/usr/bin/uv", "run", "pre-commit", "install"],
            capture_output=True,
            cwd=str(plugin_root),
            timeout=8,
        )

    @patch("scripts.session_start_hook.subprocess.run")
    def test_auto_install_when_install_succeeds_then_returns_success_message(
        self, mock_run: MagicMock, tmp_path: Path
    ) -> None:
        """Successful install returns a success info message."""
        plugin_root = self._make_plugin_root(tmp_path)
        mock_run.return_value = MagicMock(returncode=0, stderr=b"")

        result = check_precommit_hooks(plugin_root, uv_path="/usr/bin/uv")

        assert result is not None
        assert "auto-installed" in result.lower()

    # -- auto-install failure --------------------------------------------------

    @patch("scripts.session_start_hook.subprocess.run")
    def test_auto_install_when_install_fails_then_returns_warning_with_fallback(
        self, mock_run: MagicMock, tmp_path: Path
    ) -> None:
        """Failed install returns warning with manual fallback instructions."""
        plugin_root = self._make_plugin_root(tmp_path)
        mock_run.return_value = MagicMock(returncode=1, stderr=b"some error")

        result = check_precommit_hooks(plugin_root, uv_path="/usr/bin/uv")

        assert result is not None
        assert "make setup" in result.lower()

    @patch("scripts.session_start_hook.subprocess.run")
    def test_auto_install_when_install_times_out_then_returns_warning(
        self, mock_run: MagicMock, tmp_path: Path
    ) -> None:
        """Timeout during install returns warning with fallback."""
        plugin_root = self._make_plugin_root(tmp_path)
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="pre-commit", timeout=8)

        result = check_precommit_hooks(plugin_root, uv_path="/usr/bin/uv")

        assert result is not None
        assert "timed out" in result.lower()
        assert "make setup" in result.lower()

    # -- no auto-install conditions --------------------------------------------

    def test_no_auto_install_when_hooks_already_exist_then_returns_none(
        self, tmp_path: Path
    ) -> None:
        """When hooks are already installed, returns None with no subprocess call."""
        plugin_root = self._make_plugin_root(tmp_path)
        # Create the pre-commit hook file
        hook_file = tmp_path / ".git" / "hooks" / "pre-commit"
        hook_file.write_text("#!/bin/sh\n# pre-commit hook")

        result = check_precommit_hooks(plugin_root, uv_path="/usr/bin/uv")

        assert result is None

    def test_no_auto_install_when_uv_path_is_none_then_returns_warning(
        self, tmp_path: Path
    ) -> None:
        """Without uv_path, returns old-style warning (no auto-install attempt)."""
        plugin_root = self._make_plugin_root(tmp_path)

        result = check_precommit_hooks(plugin_root, uv_path=None)

        assert result is not None
        assert "NOT installed" in result
        assert "make setup" in result.lower()
