"""Tests for pre_tool_use.py hook.

These tests validate the security guardrail hook returns correct decision values
and properly blocks dangerous operations.

References:
    - TD-003: Add hook decision value tests
    - Claude Code Hooks: https://docs.anthropic.com/en/docs/claude-code/hooks
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

# Path to the hook script
HOOK_SCRIPT = Path(__file__).parent.parent.parent / ".claude" / "hooks" / "pre_tool_use.py"


def run_hook(tool_name: str, tool_input: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    """Run the pre_tool_use hook with given input.

    Args:
        tool_name: The name of the tool being used
        tool_input: The input parameters for the tool

    Returns:
        Tuple of (exit_code, parsed_output_json)
    """
    input_json = json.dumps({
        "tool_name": tool_name,
        "tool_input": tool_input,
    })

    result = subprocess.run(
        [sys.executable, str(HOOK_SCRIPT)],
        input=input_json,
        capture_output=True,
        text=True,
    )

    # Parse the JSON output from stdout
    output = {}
    if result.stdout.strip():
        output = json.loads(result.stdout.strip())

    return result.returncode, output


# =============================================================================
# Test: Approve Decision for Allowed Tools
# =============================================================================


class TestApproveDecision:
    """Tests verifying allowed tools return 'approve' decision."""

    def test_read_tool_returns_approve(self) -> None:
        """Read tool should always be approved."""
        exit_code, output = run_hook("Read", {"file_path": "/some/file.txt"})

        assert exit_code == 0
        assert output["decision"] == "approve"

    def test_glob_tool_returns_approve(self) -> None:
        """Glob tool should always be approved."""
        exit_code, output = run_hook("Glob", {"pattern": "**/*.py"})

        assert exit_code == 0
        assert output["decision"] == "approve"

    def test_grep_tool_returns_approve(self) -> None:
        """Grep tool should always be approved."""
        exit_code, output = run_hook("Grep", {"pattern": "test", "path": "."})

        assert exit_code == 0
        assert output["decision"] == "approve"

    def test_write_to_safe_path_returns_approve(self) -> None:
        """Write to non-sensitive path should be approved."""
        exit_code, output = run_hook("Write", {
            "file_path": "/tmp/test_output.txt",
            "content": "test content",
        })

        assert exit_code == 0
        assert output["decision"] == "approve"

    def test_bash_safe_command_returns_approve(self) -> None:
        """Safe bash command should be approved."""
        exit_code, output = run_hook("Bash", {
            "command": "ls -la /tmp",
        })

        assert exit_code == 0
        assert output["decision"] == "approve"

    def test_bash_git_status_returns_approve(self) -> None:
        """git status command should be approved."""
        exit_code, output = run_hook("Bash", {
            "command": "git status",
        })

        assert exit_code == 0
        assert output["decision"] == "approve"


# =============================================================================
# Test: Block Decision for Denied Tools
# =============================================================================


class TestBlockDecision:
    """Tests verifying dangerous operations return 'block' decision."""

    def test_write_to_ssh_blocked(self) -> None:
        """Writing to ~/.ssh should be blocked."""
        exit_code, output = run_hook("Write", {
            "file_path": "~/.ssh/authorized_keys",
            "content": "malicious key",
        })

        assert exit_code == 0  # Hook exits 0, decision in output
        assert output["decision"] == "block"
        assert "reason" in output
        assert "ssh" in output["reason"].lower()

    def test_write_to_env_file_blocked(self) -> None:
        """Writing to .env files should be blocked."""
        exit_code, output = run_hook("Write", {
            "file_path": "/project/.env",
            "content": "SECRET=value",
        })

        assert exit_code == 0
        assert output["decision"] == "block"
        assert "sensitive" in output["reason"].lower()

    def test_write_to_credentials_blocked(self) -> None:
        """Writing to credentials.json should be blocked."""
        exit_code, output = run_hook("Write", {
            "file_path": "/path/credentials.json",
            "content": "{}",
        })

        assert exit_code == 0
        assert output["decision"] == "block"

    def test_bash_rm_rf_root_blocked(self) -> None:
        """rm -rf / command should be blocked."""
        exit_code, output = run_hook("Bash", {
            "command": "rm -rf /",
        })

        assert exit_code == 0
        assert output["decision"] == "block"
        assert "dangerous" in output["reason"].lower()

    def test_bash_cd_command_blocked(self) -> None:
        """cd command should be blocked (use absolute paths instead)."""
        exit_code, output = run_hook("Bash", {
            "command": "cd /tmp && ls",
        })

        assert exit_code == 0
        assert output["decision"] == "block"
        assert "cd" in output["reason"].lower()

    def test_git_force_push_main_blocked(self) -> None:
        """git push --force to main should be blocked."""
        exit_code, output = run_hook("Bash", {
            "command": "git push --force origin main",
        })

        assert exit_code == 0
        assert output["decision"] == "block"
        assert "force push" in output["reason"].lower()

    def test_pipe_to_bash_warned(self) -> None:
        """Piping to bash triggers warning but is approved (trusted sources)."""
        # Note: The hook warns but approves "| bash" patterns
        # Only exact "curl | bash" or "wget | bash" substring is blocked
        exit_code, output = run_hook("Bash", {
            "command": "echo 'test' | bash",
        })

        # This triggers a warning but is approved
        assert exit_code == 0
        assert output["decision"] == "approve"

    def test_eval_command_blocked(self) -> None:
        """eval command should be blocked."""
        exit_code, output = run_hook("Bash", {
            "command": "eval $(cat script.sh)",
        })

        assert exit_code == 0
        assert output["decision"] == "block"
        assert "dangerous" in output["reason"].lower()


# =============================================================================
# Test: Decision Format Matches Spec
# =============================================================================


class TestDecisionFormat:
    """Tests verifying output format matches Claude Code hook specification."""

    def test_output_is_valid_json(self) -> None:
        """Hook output must be valid JSON."""
        _exit_code, output = run_hook("Read", {"file_path": "test.txt"})

        assert _exit_code == 0
        assert isinstance(output, dict)

    def test_output_contains_decision_field(self) -> None:
        """Hook output must contain 'decision' field."""
        _exit_code, output = run_hook("Read", {"file_path": "test.txt"})
        _ = _exit_code  # Used for type checking

        assert "decision" in output

    def test_approve_decision_has_correct_value(self) -> None:
        """Approve decision must be exactly 'approve' string."""
        _exit_code, output = run_hook("Glob", {"pattern": "*.txt"})
        _ = _exit_code  # Used for type checking

        assert output["decision"] == "approve"
        assert isinstance(output["decision"], str)

    def test_block_decision_includes_reason(self) -> None:
        """Block decision must include 'reason' field."""
        _exit_code, output = run_hook("Write", {
            "file_path": "~/.ssh/test",
            "content": "x",
        })
        _ = _exit_code  # Check exit code

        assert output["decision"] == "block"
        assert "reason" in output
        assert isinstance(output["reason"], str)
        assert len(output["reason"]) > 0

    def test_invalid_json_input_returns_block(self) -> None:
        """Invalid JSON input should return block with error reason."""
        result = subprocess.run(
            [sys.executable, str(HOOK_SCRIPT)],
            input="not valid json",
            capture_output=True,
            text=True,
        )

        assert result.returncode == 2  # Error exit code
        output = json.loads(result.stdout.strip())
        assert output["decision"] == "block"
        assert "error" in output["reason"].lower()


# =============================================================================
# Test: Edge Cases
# =============================================================================


class TestEdgeCases:
    """Tests for edge case handling."""

    def test_empty_tool_input(self) -> None:
        """Empty tool input should be handled gracefully."""
        _exit_code, output = run_hook("Read", {})
        _ = _exit_code  # Check exit code

        assert output["decision"] == "approve"

    def test_unknown_tool_returns_approve(self) -> None:
        """Unknown tool names should default to approve."""
        _exit_code, output = run_hook("UnknownTool", {"param": "value"})
        _ = _exit_code  # Check exit code

        assert output["decision"] == "approve"

    def test_edit_to_sensitive_path_blocked(self) -> None:
        """Edit tool should also check file paths."""
        exit_code, output = run_hook("Edit", {
            "file_path": "~/.aws/credentials",
            "old_string": "old",
            "new_string": "new",
        })

        assert exit_code == 0
        assert output["decision"] == "block"

    def test_multiedit_to_sensitive_path_blocked(self) -> None:
        """MultiEdit tool should also check file paths."""
        exit_code, output = run_hook("MultiEdit", {
            "file_path": "/etc/passwd",
            "edits": [],
        })

        assert exit_code == 0
        assert output["decision"] == "block"
