# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for PreToolUse hook enforcement via CLI pipeline.

These tests validate the security guardrail hook returns correct decision values
and properly blocks dangerous operations, using the consolidated CLI enforcement
path (``uv run jerry hooks pre-tool-use``).

References:
    - TD-003: Add hook decision value tests
    - #150: pre_tool_use.py consolidation into CLI pipeline
    - STORY-023: Deprecated script removal
    - Claude Code Hooks: https://docs.anthropic.com/en/docs/claude-code/hooks
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

# Repo root for --directory flag
_REPO_ROOT = str(Path(__file__).resolve().parents[2])


def run_hook(tool_name: str, tool_input: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    """Run the pre-tool-use hook via CLI.

    Args:
        tool_name: The name of the tool being used.
        tool_input: The input parameters for the tool.

    Returns:
        Tuple of (exit_code, parsed_output_json).
    """
    input_json = json.dumps(
        {
            "tool_name": tool_name,
            "tool_input": tool_input,
        }
    )

    result = subprocess.run(
        ["uv", "run", "--directory", _REPO_ROOT, "jerry", "--json", "hooks", "pre-tool-use"],
        input=input_json,
        capture_output=True,
        text=True,
        timeout=15,
    )

    output: dict[str, Any] = {}
    if result.stdout.strip():
        output = json.loads(result.stdout.strip())

    return result.returncode, output


def is_blocked(output: dict[str, Any]) -> bool:
    """Return True if the hook blocked the tool use."""
    return output.get("decision") == "block"


def is_approved(output: dict[str, Any]) -> bool:
    """Return True if the hook approved the tool use.

    The CLI handler returns ``{}`` for approve (no ``decision`` key)
    or any value other than ``"block"``.
    """
    return "decision" not in output or output["decision"] != "block"


def get_reason(output: dict[str, Any]) -> str:
    """Extract the block reason from hook output."""
    return output.get("reason", "")


# =============================================================================
# Test: Approve Decision for Allowed Tools
# =============================================================================


class TestApproveDecision:
    """Tests verifying allowed tools are approved by CLI enforcement."""

    def test_read_tool_returns_approve(self) -> None:
        """Read tool should always be approved."""
        exit_code, output = run_hook("Read", {"file_path": "/some/file.txt"})

        assert exit_code == 0
        assert is_approved(output)

    def test_glob_tool_returns_approve(self) -> None:
        """Glob tool should always be approved."""
        exit_code, output = run_hook("Glob", {"pattern": "**/*.py"})

        assert exit_code == 0
        assert is_approved(output)

    def test_grep_tool_returns_approve(self) -> None:
        """Grep tool should always be approved."""
        exit_code, output = run_hook("Grep", {"pattern": "test", "path": "."})

        assert exit_code == 0
        assert is_approved(output)

    def test_write_to_safe_path_returns_approve(self) -> None:
        """Write to non-sensitive path should be approved."""
        exit_code, output = run_hook(
            "Write",
            {
                "file_path": "/tmp/test_output.txt",
                "content": "test content",
            },
        )

        assert exit_code == 0
        assert is_approved(output)

    def test_bash_safe_command_returns_approve(self) -> None:
        """Safe bash command should be approved."""
        exit_code, output = run_hook(
            "Bash",
            {
                "command": "ls -la /tmp",
            },
        )

        assert exit_code == 0
        assert is_approved(output)

    def test_bash_git_status_returns_approve(self) -> None:
        """git status command should be approved."""
        exit_code, output = run_hook(
            "Bash",
            {
                "command": "git status",
            },
        )

        assert exit_code == 0
        assert is_approved(output)


# =============================================================================
# Test: Block Decision for Denied Tools
# =============================================================================


class TestBlockDecision:
    """Tests verifying dangerous operations are blocked by CLI enforcement."""

    def test_write_to_ssh_blocked(self) -> None:
        """Writing to ~/.ssh should be blocked."""
        exit_code, output = run_hook(
            "Write",
            {
                "file_path": "~/.ssh/authorized_keys",
                "content": "malicious key",
            },
        )

        assert exit_code == 0  # Hook exits 0, decision in output
        assert is_blocked(output)
        reason = get_reason(output)
        assert reason
        assert "ssh" in reason.lower() or "blocked" in reason.lower()

    def test_write_to_env_file_blocked(self) -> None:
        """Writing to .env files should be blocked."""
        exit_code, output = run_hook(
            "Write",
            {
                "file_path": "/project/.env",
                "content": "SECRET=value",
            },
        )

        assert exit_code == 0
        assert is_blocked(output)
        assert "sensitive" in get_reason(output).lower()

    def test_write_to_credentials_blocked(self) -> None:
        """Writing to credentials.json should be blocked."""
        exit_code, output = run_hook(
            "Write",
            {
                "file_path": "/path/credentials.json",
                "content": "{}",
            },
        )

        assert exit_code == 0
        assert is_blocked(output)

    def test_bash_rm_rf_root_blocked(self) -> None:
        """rm -rf / command should be blocked."""
        exit_code, output = run_hook(
            "Bash",
            {
                "command": "rm -rf /",
            },
        )

        assert exit_code == 0
        assert is_blocked(output)
        reason = get_reason(output)
        assert (
            "dangerous" in reason.lower()
            or "rm" in reason.lower()
            or "destructive" in reason.lower()
        )

    def test_bash_rm_split_flags_blocked(self) -> None:
        """rm -r -f / with split flags should be blocked (RT-004)."""
        exit_code, output = run_hook(
            "Bash",
            {
                "command": "rm -r -f /",
            },
        )

        assert exit_code == 0
        assert is_blocked(output)

    def test_bash_rm_long_flags_blocked(self) -> None:
        """rm --recursive --force / with long flags should be blocked (RT-004)."""
        exit_code, output = run_hook(
            "Bash",
            {
                "command": "rm --recursive --force /",
            },
        )

        assert exit_code == 0
        assert is_blocked(output)

    def test_bash_rm_fr_root_blocked(self) -> None:
        """rm -fr / with reversed flags should be blocked (RT-004)."""
        exit_code, output = run_hook(
            "Bash",
            {
                "command": "rm -fr /",
            },
        )

        assert exit_code == 0
        assert is_blocked(output)

    def test_bash_rm_rf_home_blocked(self) -> None:
        """rm -rf ~ targeting home should be blocked (RT-004)."""
        exit_code, output = run_hook(
            "Bash",
            {
                "command": "rm -rf ~",
            },
        )

        assert exit_code == 0
        assert is_blocked(output)

    def test_bash_cd_command_blocked(self) -> None:
        """cd command should be blocked (use absolute paths instead)."""
        exit_code, output = run_hook(
            "Bash",
            {
                "command": "cd /tmp && ls",
            },
        )

        assert exit_code == 0
        assert is_blocked(output)
        assert "cd" in get_reason(output).lower()

    def test_git_force_push_main_blocked(self) -> None:
        """git push --force to main should be blocked."""
        exit_code, output = run_hook(
            "Bash",
            {
                "command": "git push --force origin main",
            },
        )

        assert exit_code == 0
        assert is_blocked(output)
        assert "force push" in get_reason(output).lower() or "force" in get_reason(output).lower()

    def test_eval_command_blocked(self) -> None:
        """eval command should be blocked."""
        exit_code, output = run_hook(
            "Bash",
            {
                "command": "eval $(cat script.sh)",
            },
        )

        assert exit_code == 0
        assert is_blocked(output)


# =============================================================================
# Test: Decision Format Matches CLI Spec
# =============================================================================


class TestDecisionFormat:
    """Tests verifying output format matches CLI hook specification."""

    def test_output_is_valid_json(self) -> None:
        """Hook output must be valid JSON."""
        _exit_code, output = run_hook("Read", {"file_path": "test.txt"})

        assert _exit_code == 0
        assert isinstance(output, dict)

    def test_approve_returns_empty_or_no_block(self) -> None:
        """Approved tools should return empty JSON or non-block decision."""
        _exit_code, output = run_hook("Read", {"file_path": "test.txt"})

        assert is_approved(output)

    def test_block_decision_includes_reason(self) -> None:
        """Block decision must include a reason string."""
        _exit_code, output = run_hook(
            "Write",
            {
                "file_path": "~/.ssh/test",
                "content": "x",
            },
        )

        assert is_blocked(output)
        reason = get_reason(output)
        assert isinstance(reason, str)
        assert len(reason) > 0

    def test_hook_always_exits_zero(self) -> None:
        """Hook should always exit 0 (fail-open design)."""
        exit_code, _output = run_hook("Read", {"file_path": "test.txt"})
        assert exit_code == 0

        exit_code, _output = run_hook("Write", {"file_path": "~/.ssh/test", "content": "x"})
        assert exit_code == 0


# =============================================================================
# Test: Edge Cases
# =============================================================================


class TestEdgeCases:
    """Tests for edge case handling."""

    def test_empty_tool_input(self) -> None:
        """Empty tool input should be handled gracefully."""
        _exit_code, output = run_hook("Read", {})

        assert is_approved(output)

    def test_unknown_tool_returns_approve(self) -> None:
        """Unknown tool names should default to approve."""
        _exit_code, output = run_hook("UnknownTool", {"param": "value"})

        assert is_approved(output)

    def test_edit_to_sensitive_path_blocked(self) -> None:
        """Edit tool should also check file paths."""
        exit_code, output = run_hook(
            "Edit",
            {
                "file_path": "~/.aws/credentials",
                "old_string": "old",
                "new_string": "new",
            },
        )

        assert exit_code == 0
        assert is_blocked(output)

    def test_multiedit_to_sensitive_path_blocked(self) -> None:
        """MultiEdit tool should also check file paths."""
        exit_code, output = run_hook(
            "MultiEdit",
            {
                "file_path": "/etc/passwd",
                "edits": [],
            },
        )

        assert exit_code == 0
        assert is_blocked(output)
