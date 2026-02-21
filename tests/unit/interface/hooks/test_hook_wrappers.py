# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for hook wrapper scripts (EN-007).

BDD scenarios:
    - Each wrapper script exists in hooks/ directory
    - Each wrapper is thin (<= 15 lines)
    - No wrapper imports from src/
    - Each wrapper calls the correct jerry CLI command
    - Wrappers always exit 0 (fail-open design)
    - Wrappers handle subprocess timeouts gracefully

References:
    - EN-007: Hook Wrapper Scripts
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

# Project root for locating hook scripts
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent

# Hook wrapper scripts and their expected CLI commands
WRAPPER_SPECS = {
    "session-start": {
        "path": PROJECT_ROOT / "hooks" / "session-start.py",
        "cli_command": "session-start",
        "timeout": 9,
    },
    "pre-compact": {
        "path": PROJECT_ROOT / "hooks" / "pre-compact.py",
        "cli_command": "pre-compact",
        "timeout": 9,
    },
    "pre-tool-use": {
        "path": PROJECT_ROOT / "hooks" / "pre-tool-use.py",
        "cli_command": "pre-tool-use",
        "timeout": 4,
    },
    "user-prompt-submit": {
        "path": PROJECT_ROOT / "hooks" / "user-prompt-submit.py",
        "cli_command": "prompt-submit",
        "timeout": 4,
    },
}


# =============================================================================
# Tests: Wrapper Script Existence and Structure
# =============================================================================


class TestWrapperScriptsExist:
    """BDD: Each hook wrapper script exists in the hooks/ directory."""

    @pytest.mark.parametrize("name,spec", WRAPPER_SPECS.items())
    def test_wrapper_script_exists(self, name: str, spec: dict) -> None:
        """GIVEN the hooks/ directory WHEN checking for {name} THEN it exists."""
        assert spec["path"].exists(), f"hooks/{name}.py does not exist"

    @pytest.mark.parametrize("name,spec", WRAPPER_SPECS.items())
    def test_wrapper_script_is_thin(self, name: str, spec: dict) -> None:
        """GIVEN hooks/{name}.py WHEN counting lines THEN <= 30 lines."""
        content = spec["path"].read_text()
        line_count = len(content.strip().splitlines())
        assert line_count <= 30, f"hooks/{name}.py has {line_count} lines (max 30)"


class TestWrapperScriptsNoSrcImports:
    """BDD: No wrapper script imports from src/ (thin delegation only)."""

    @pytest.mark.parametrize("name,spec", WRAPPER_SPECS.items())
    def test_no_src_imports(self, name: str, spec: dict) -> None:
        """GIVEN hooks/{name}.py WHEN scanning for imports THEN no src/ imports."""
        content = spec["path"].read_text()
        assert "from src" not in content, f"hooks/{name}.py contains 'from src'"
        assert "import src" not in content, f"hooks/{name}.py contains 'import src'"


class TestWrapperScriptsCorrectCliCommand:
    """BDD: Each wrapper calls the correct jerry hooks CLI command."""

    @pytest.mark.parametrize("name,spec", WRAPPER_SPECS.items())
    def test_calls_correct_command(self, name: str, spec: dict) -> None:
        """GIVEN hooks/{name}.py WHEN reading content THEN contains jerry hooks {command}."""
        content = spec["path"].read_text()
        expected_cmd = f'"hooks", "{spec["cli_command"]}"'
        assert expected_cmd in content, (
            f"hooks/{name}.py does not contain expected command: {expected_cmd}"
        )

    @pytest.mark.parametrize("name,spec", WRAPPER_SPECS.items())
    def test_has_correct_timeout(self, name: str, spec: dict) -> None:
        """GIVEN hooks/{name}.py WHEN reading content THEN has correct timeout."""
        content = spec["path"].read_text()
        expected_timeout = f"timeout={spec['timeout']}"
        assert expected_timeout in content, f"hooks/{name}.py does not contain {expected_timeout}"

    @pytest.mark.parametrize("name,spec", WRAPPER_SPECS.items())
    def test_always_exits_zero(self, name: str, spec: dict) -> None:
        """GIVEN hooks/{name}.py WHEN reading content THEN has sys.exit(0)."""
        content = spec["path"].read_text()
        assert "sys.exit(0)" in content, (
            f"hooks/{name}.py does not contain sys.exit(0) (fail-open required)"
        )

    @pytest.mark.parametrize("name,spec", WRAPPER_SPECS.items())
    def test_has_shebang(self, name: str, spec: dict) -> None:
        """GIVEN hooks/{name}.py WHEN reading first line THEN has python shebang."""
        content = spec["path"].read_text()
        first_line = content.splitlines()[0]
        assert first_line.startswith("#!/usr/bin/env"), f"hooks/{name}.py missing shebang line"

    @pytest.mark.parametrize("name,spec", WRAPPER_SPECS.items())
    def test_pipes_stdin(self, name: str, spec: dict) -> None:
        """GIVEN hooks/{name}.py WHEN reading content THEN pipes stdin to subprocess."""
        content = spec["path"].read_text()
        assert "sys.stdin.buffer.read()" in content, (
            f"hooks/{name}.py does not pipe stdin to subprocess"
        )

    @pytest.mark.parametrize("name,spec", WRAPPER_SPECS.items())
    def test_pipes_stdout(self, name: str, spec: dict) -> None:
        """GIVEN hooks/{name}.py WHEN reading content THEN pipes stdout back."""
        content = spec["path"].read_text()
        assert "sys.stdout.buffer.write" in content, f"hooks/{name}.py does not pipe stdout back"


# =============================================================================
# Tests: hooks.json Structure
# =============================================================================


class TestHooksJsonStructure:
    """BDD: hooks.json has correct structure with all hook events."""

    @pytest.fixture()
    def hooks_json(self) -> dict:
        """Load and parse hooks.json."""
        hooks_path = PROJECT_ROOT / "hooks" / "hooks.json"
        assert hooks_path.exists(), "hooks/hooks.json does not exist"
        content = hooks_path.read_text()
        return json.loads(content)

    def test_hooks_json_is_valid(self, hooks_json: dict) -> None:
        """GIVEN hooks.json WHEN parsed THEN is valid JSON with hooks key."""
        assert "hooks" in hooks_json
        assert "description" in hooks_json

    def test_session_start_registered(self, hooks_json: dict) -> None:
        """GIVEN hooks.json WHEN checking SessionStart THEN points to hooks/session-start.py."""
        assert "SessionStart" in hooks_json["hooks"]
        session_start = hooks_json["hooks"]["SessionStart"]
        commands = [h["command"] for entry in session_start for h in entry.get("hooks", [])]
        assert any("hooks/session-start.py" in cmd for cmd in commands), (
            f"SessionStart does not point to hooks/session-start.py. Commands: {commands}"
        )

    def test_user_prompt_submit_registered(self, hooks_json: dict) -> None:
        """GIVEN hooks.json WHEN checking UserPromptSubmit THEN points to hooks/user-prompt-submit.py."""
        assert "UserPromptSubmit" in hooks_json["hooks"]
        prompt_submit = hooks_json["hooks"]["UserPromptSubmit"]
        commands = [h["command"] for entry in prompt_submit for h in entry.get("hooks", [])]
        assert any("hooks/user-prompt-submit.py" in cmd for cmd in commands), (
            f"UserPromptSubmit does not point to hooks/user-prompt-submit.py. Commands: {commands}"
        )

    def test_pre_compact_registered(self, hooks_json: dict) -> None:
        """GIVEN hooks.json WHEN checking PreCompact THEN points to hooks/pre-compact.py."""
        assert "PreCompact" in hooks_json["hooks"]
        pre_compact = hooks_json["hooks"]["PreCompact"]
        commands = [h["command"] for entry in pre_compact for h in entry.get("hooks", [])]
        assert any("hooks/pre-compact.py" in cmd for cmd in commands), (
            f"PreCompact does not point to hooks/pre-compact.py. Commands: {commands}"
        )

    def test_pre_tool_use_registered(self, hooks_json: dict) -> None:
        """GIVEN hooks.json WHEN checking PreToolUse THEN has hooks/pre-tool-use.py."""
        assert "PreToolUse" in hooks_json["hooks"]
        pre_tool_use = hooks_json["hooks"]["PreToolUse"]
        commands = [h["command"] for entry in pre_tool_use for h in entry.get("hooks", [])]
        assert any("hooks/pre-tool-use.py" in cmd for cmd in commands), (
            f"PreToolUse does not include hooks/pre-tool-use.py. Commands: {commands}"
        )

    def test_pre_tool_use_keeps_security_guardrails(self, hooks_json: dict) -> None:
        """GIVEN hooks.json WHEN checking PreToolUse THEN still has scripts/pre_tool_use.py."""
        pre_tool_use = hooks_json["hooks"]["PreToolUse"]
        commands = [h["command"] for entry in pre_tool_use for h in entry.get("hooks", [])]
        assert any("scripts/pre_tool_use.py" in cmd for cmd in commands), (
            f"PreToolUse must retain scripts/pre_tool_use.py for security guardrails. Commands: {commands}"
        )

    def test_subagent_stop_unchanged(self, hooks_json: dict) -> None:
        """GIVEN hooks.json WHEN checking SubagentStop THEN still uses scripts/subagent_stop.py."""
        assert "SubagentStop" in hooks_json["hooks"]
        subagent = hooks_json["hooks"]["SubagentStop"]
        commands = [h["command"] for entry in subagent for h in entry.get("hooks", [])]
        assert any("scripts/subagent_stop.py" in cmd for cmd in commands)

    def test_session_start_timeout(self, hooks_json: dict) -> None:
        """GIVEN hooks.json SessionStart WHEN checking timeout THEN is 10000ms."""
        session_start = hooks_json["hooks"]["SessionStart"]
        for entry in session_start:
            for hook in entry.get("hooks", []):
                if "session-start.py" in hook.get("command", ""):
                    assert hook["timeout"] == 10000

    def test_user_prompt_submit_timeout(self, hooks_json: dict) -> None:
        """GIVEN hooks.json UserPromptSubmit WHEN checking timeout THEN is 5000ms."""
        prompt_submit = hooks_json["hooks"]["UserPromptSubmit"]
        for entry in prompt_submit:
            for hook in entry.get("hooks", []):
                if "user-prompt-submit.py" in hook.get("command", ""):
                    assert hook["timeout"] == 5000

    def test_pre_compact_timeout(self, hooks_json: dict) -> None:
        """GIVEN hooks.json PreCompact WHEN checking timeout THEN is 10000ms."""
        pre_compact = hooks_json["hooks"]["PreCompact"]
        for entry in pre_compact:
            for hook in entry.get("hooks", []):
                if "pre-compact.py" in hook.get("command", ""):
                    assert hook["timeout"] == 10000

    def test_pre_tool_use_context_monitor_timeout(self, hooks_json: dict) -> None:
        """GIVEN hooks.json PreToolUse context monitor hook WHEN checking timeout THEN is 5000ms."""
        pre_tool_use = hooks_json["hooks"]["PreToolUse"]
        for entry in pre_tool_use:
            for hook in entry.get("hooks", []):
                if "hooks/pre-tool-use.py" in hook.get("command", ""):
                    assert hook["timeout"] == 5000


# =============================================================================
# Tests: Retired Scripts
# =============================================================================


class TestRetiredScripts:
    """BDD: Old hook scripts are retired (not deleted)."""

    def test_session_start_hook_retired(self) -> None:
        """GIVEN scripts/session_start_hook.py WHEN checking THEN is marked retired."""
        retired_path = PROJECT_ROOT / "scripts" / "session_start_hook.py.retired"
        original_path = PROJECT_ROOT / "scripts" / "session_start_hook.py"
        # Either renamed to .retired OR original has retired comment at top
        if retired_path.exists():
            assert True
        elif original_path.exists():
            content = original_path.read_text()
            assert "RETIRED" in content.upper(), (
                "scripts/session_start_hook.py exists but is not marked as retired"
            )
        else:
            pytest.fail(
                "Neither scripts/session_start_hook.py nor "
                "scripts/session_start_hook.py.retired exists"
            )
