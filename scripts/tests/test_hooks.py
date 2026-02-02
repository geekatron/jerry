#!/usr/bin/env python3
"""
BDD Tests for Guardrail Hooks

Work Item: WI-SAO-015
Acceptance Criteria Tested:
    - AC-015-001: Async validation via subprocess model
    - AC-015-003: mode: warn (log but don't block)
    - AC-015-004: Pattern library for common checks

Test Categories:
    - Happy Path (60%): Hook behavior works correctly
    - Negative Cases (30%): Error handling
    - Edge Cases (10%): Boundary conditions
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

# =============================================================================
# FIXTURES
# =============================================================================


HOOKS_DIR = Path(__file__).parent.parent


@pytest.fixture
def pre_tool_use_hook() -> Path:
    """Path to pre_tool_use.py hook."""
    return HOOKS_DIR / "pre_tool_use.py"


@pytest.fixture
def post_tool_use_hook() -> Path:
    """Path to post_tool_use.py hook."""
    return HOOKS_DIR / "post_tool_use.py"


def run_hook(hook_path: Path, input_data: dict) -> tuple[str, str, int]:
    """
    Run a hook script with given input.

    Returns:
        Tuple of (stdout, stderr, exit_code)
    """
    result = subprocess.run(
        [sys.executable, str(hook_path)],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout, result.stderr, result.returncode


# =============================================================================
# PRE-TOOL-USE HOOK TESTS
# =============================================================================


class TestPreToolUseHappyPath:
    """Happy path tests for pre_tool_use hook."""

    def test_safe_bash_command_approved(self, pre_tool_use_hook: Path) -> None:
        """Given safe bash command, when hook runs, then approved."""
        stdout, stderr, code = run_hook(
            pre_tool_use_hook, {"tool_name": "Bash", "tool_input": {"command": "ls -la"}}
        )
        result = json.loads(stdout)
        assert result["decision"] == "approve"
        assert code == 0

    def test_safe_write_approved(self, pre_tool_use_hook: Path) -> None:
        """Given safe file write, when hook runs, then approved."""
        stdout, stderr, code = run_hook(
            pre_tool_use_hook,
            {
                "tool_name": "Write",
                "tool_input": {"file_path": "/tmp/test.txt", "content": "hello"},
            },
        )
        result = json.loads(stdout)
        assert result["decision"] == "approve"
        assert code == 0

    def test_safe_edit_approved(self, pre_tool_use_hook: Path) -> None:
        """Given safe file edit, when hook runs, then approved."""
        stdout, stderr, code = run_hook(
            pre_tool_use_hook,
            {
                "tool_name": "Edit",
                "tool_input": {
                    "file_path": "/tmp/test.txt",
                    "old_string": "hello",
                    "new_string": "world",
                },
            },
        )
        result = json.loads(stdout)
        assert result["decision"] == "approve"
        assert code == 0


class TestPreToolUseSecurityBlocking:
    """Tests for security blocking in pre_tool_use hook."""

    def test_blocked_ssh_path(self, pre_tool_use_hook: Path) -> None:
        """Given write to ~/.ssh, when hook runs, then blocked."""
        stdout, stderr, code = run_hook(
            pre_tool_use_hook,
            {"tool_name": "Write", "tool_input": {"file_path": "~/.ssh/authorized_keys"}},
        )
        result = json.loads(stdout)
        assert result["decision"] == "block"
        assert "blocked" in result["reason"].lower()

    def test_blocked_etc_path(self, pre_tool_use_hook: Path) -> None:
        """Given write to /etc, when hook runs, then blocked."""
        stdout, stderr, code = run_hook(
            pre_tool_use_hook, {"tool_name": "Write", "tool_input": {"file_path": "/etc/passwd"}}
        )
        result = json.loads(stdout)
        assert result["decision"] == "block"

    def test_blocked_dangerous_command(self, pre_tool_use_hook: Path) -> None:
        """Given dangerous rm command, when hook runs, then blocked."""
        stdout, stderr, code = run_hook(
            pre_tool_use_hook, {"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}
        )
        result = json.loads(stdout)
        assert result["decision"] == "block"

    def test_blocked_force_push_main(self, pre_tool_use_hook: Path) -> None:
        """Given force push to main, when hook runs, then blocked."""
        stdout, stderr, code = run_hook(
            pre_tool_use_hook,
            {"tool_name": "Bash", "tool_input": {"command": "git push --force origin main"}},
        )
        result = json.loads(stdout)
        assert result["decision"] == "block"


class TestPreToolUseNegativeCases:
    """Negative test cases for pre_tool_use hook."""

    def test_invalid_json_input(self, pre_tool_use_hook: Path) -> None:
        """Given invalid JSON, when hook runs, then error handled."""
        result = subprocess.run(
            [sys.executable, str(pre_tool_use_hook)],
            input="not valid json",
            capture_output=True,
            text=True,
        )
        output = json.loads(result.stdout)
        assert output["decision"] == "block"
        assert "Invalid JSON" in output["reason"]
        assert result.returncode == 2

    def test_missing_tool_name(self, pre_tool_use_hook: Path) -> None:
        """Given missing tool_name, when hook runs, then approves."""
        stdout, stderr, code = run_hook(pre_tool_use_hook, {"tool_input": {"command": "ls"}})
        result = json.loads(stdout)
        # Should approve since no specific checks apply
        assert result["decision"] == "approve"


class TestPreToolUseEdgeCases:
    """Edge case tests for pre_tool_use hook."""

    def test_empty_input(self, pre_tool_use_hook: Path) -> None:
        """Given empty input dict, when hook runs, then approves."""
        stdout, stderr, code = run_hook(pre_tool_use_hook, {})
        result = json.loads(stdout)
        assert result["decision"] == "approve"

    def test_unknown_tool(self, pre_tool_use_hook: Path) -> None:
        """Given unknown tool, when hook runs, then approves."""
        stdout, stderr, code = run_hook(
            pre_tool_use_hook, {"tool_name": "UnknownTool", "tool_input": {"data": "test"}}
        )
        result = json.loads(stdout)
        assert result["decision"] == "approve"


# =============================================================================
# POST-TOOL-USE HOOK TESTS
# =============================================================================


class TestPostToolUseHappyPath:
    """Happy path tests for post_tool_use hook."""

    def test_safe_output_unchanged(self, post_tool_use_hook: Path) -> None:
        """Given safe output, when hook runs, then output unchanged."""
        stdout, stderr, code = run_hook(
            post_tool_use_hook, {"tool_name": "Bash", "tool_output": "Build completed successfully"}
        )
        result = json.loads(stdout)
        assert result["output"] == "Build completed successfully"
        assert code == 0

    def test_json_output_handled(self, post_tool_use_hook: Path) -> None:
        """Given JSON output, when hook runs, then handled correctly."""
        stdout, stderr, code = run_hook(
            post_tool_use_hook, {"tool_name": "Bash", "tool_output": {"status": "ok", "count": 5}}
        )
        result = json.loads(stdout)
        assert "output" in result
        assert code == 0


class TestPostToolUseRedaction:
    """Tests for output redaction in post_tool_use hook."""

    def test_bearer_token_redacted(self, post_tool_use_hook: Path) -> None:
        """Given Bearer token in output, when hook runs, then redacted."""
        stdout, stderr, code = run_hook(
            post_tool_use_hook,
            {"tool_name": "Bash", "tool_output": "Auth: Bearer eyJhbGciOiJIUzI1NiJ9.test.sig"},
        )
        result = json.loads(stdout)
        assert "Bearer" not in result["output"] or "REDACTED" in result["output"]

    def test_redaction_logged_to_stderr(self, post_tool_use_hook: Path) -> None:
        """Given redactable output, when hook runs, then logs to stderr."""
        stdout, stderr, code = run_hook(
            post_tool_use_hook, {"tool_name": "Bash", "tool_output": "Token: Bearer abc123xyz789"}
        )
        if "REDACTED" in json.loads(stdout)["output"]:
            assert "redact" in stderr.lower() or len(stderr) > 0


class TestPostToolUseNegativeCases:
    """Negative test cases for post_tool_use hook."""

    def test_invalid_json_input(self, post_tool_use_hook: Path) -> None:
        """Given invalid JSON, when hook runs, then error returned."""
        result = subprocess.run(
            [sys.executable, str(post_tool_use_hook)],
            input="not valid json",
            capture_output=True,
            text=True,
        )
        output = json.loads(result.stdout)
        assert "error" in output
        assert result.returncode == 2

    def test_missing_tool_output(self, post_tool_use_hook: Path) -> None:
        """Given missing tool_output, when hook runs, then handles gracefully."""
        stdout, stderr, code = run_hook(post_tool_use_hook, {"tool_name": "Bash"})
        result = json.loads(stdout)
        assert "output" in result
        assert code == 0


class TestPostToolUseEdgeCases:
    """Edge case tests for post_tool_use hook."""

    def test_empty_output(self, post_tool_use_hook: Path) -> None:
        """Given empty output, when hook runs, then returns empty."""
        stdout, stderr, code = run_hook(
            post_tool_use_hook, {"tool_name": "Bash", "tool_output": ""}
        )
        result = json.loads(stdout)
        assert result["output"] == ""

    def test_unicode_output(self, post_tool_use_hook: Path) -> None:
        """Given unicode output, when hook runs, then preserved."""
        stdout, stderr, code = run_hook(
            post_tool_use_hook, {"tool_name": "Bash", "tool_output": "日本語テスト 🎯"}
        )
        result = json.loads(stdout)
        assert "日本語" in result["output"]


# =============================================================================
# ACCEPTANCE CRITERIA TESTS
# =============================================================================


class TestAcceptanceCriteria:
    """Test acceptance criteria for WI-SAO-015."""

    def test_ac_015_001_subprocess_model(self, pre_tool_use_hook: Path) -> None:
        """AC-015-001: Verify hook runs as subprocess."""
        # Running the hook as subprocess proves AC-015-001
        stdout, stderr, code = run_hook(
            pre_tool_use_hook, {"tool_name": "Bash", "tool_input": {"command": "echo test"}}
        )
        assert code == 0
        # Output should be valid JSON
        result = json.loads(stdout)
        assert "decision" in result

    def test_ac_015_003_warn_mode_logs_warning(self, pre_tool_use_hook: Path) -> None:
        """AC-015-003: Verify warn mode logs but doesn't block."""
        # git reset --hard should warn but not block
        stdout, stderr, code = run_hook(
            pre_tool_use_hook,
            {"tool_name": "Bash", "tool_input": {"command": "git reset --hard HEAD~1"}},
        )
        result = json.loads(stdout)
        # Should warn (stderr) but approve
        assert result["decision"] == "approve"
        assert "warning" in stderr.lower() or "reset --hard" in stderr.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
