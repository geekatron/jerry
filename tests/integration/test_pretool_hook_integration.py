# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Integration tests for PreToolUse hook with AST enforcement.

Tests the full hook pipeline by simulating stdin JSON input and
running scripts/pre_tool_use.py as a subprocess.

References:
    - EN-703: PreToolUse Enforcement Engine
    - AC-015: Hook validation framework
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "scripts"
HOOK_SCRIPT = SCRIPTS_DIR / "pre_tool_use.py"


def run_hook(tool_name: str, tool_input: dict) -> tuple[int, dict | None, str]:
    """Run the pre_tool_use.py hook with the given input.

    Args:
        tool_name: Name of the tool (e.g., "Write", "Edit", "Bash").
        tool_input: Tool input parameters.

    Returns:
        Tuple of (exit_code, stdout_json_or_none, stderr_text).
    """
    input_data = json.dumps({"tool_name": tool_name, "tool_input": tool_input})

    result = subprocess.run(
        [sys.executable, str(HOOK_SCRIPT)],
        input=input_data,
        capture_output=True,
        text=True,
        timeout=10,
        cwd=str(SCRIPTS_DIR.parent),
    )

    stdout_json = None
    if result.stdout.strip():
        try:
            stdout_json = json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            pass

    return result.returncode, stdout_json, result.stderr


def get_permission_decision(stdout_json: dict) -> str:
    """Extract the permission decision from the new hookSpecificOutput format."""
    hso = stdout_json.get("hookSpecificOutput", {})
    return hso.get("permissionDecision", "")


def get_permission_reason(stdout_json: dict) -> str:
    """Extract the permission decision reason from hookSpecificOutput."""
    hso = stdout_json.get("hookSpecificOutput", {})
    return hso.get("permissionDecisionReason", "")


class TestHookArchitectureEnforcement:
    """Integration tests for AST enforcement in the hook pipeline."""

    def test_hook_blocks_architecture_violation_on_write(self) -> None:
        """Hook should block a Write that violates import boundaries."""
        # Domain file importing from infrastructure
        content = '''"""Bad domain module."""

from src.infrastructure.adapters.persistence import FileAdapter


class BadEntity:
    """Entity with forbidden import."""
    pass
'''
        # Use the actual project root (where CLAUDE.md is)
        project_root = SCRIPTS_DIR.parent
        file_path = str(project_root / "src" / "domain" / "bad_entity.py")

        exit_code, stdout_json, stderr = run_hook(
            "Write",
            {"file_path": file_path, "content": content},
        )

        assert exit_code == 0
        assert stdout_json is not None
        assert get_permission_decision(stdout_json) == "deny"
        assert "infrastructure" in get_permission_reason(stdout_json).lower()

    def test_hook_approves_clean_write(self) -> None:
        """Hook should approve a Write with no violations."""
        content = '''"""Clean domain module."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CleanEntity:
    """A compliant domain entity."""

    name: str
'''
        project_root = SCRIPTS_DIR.parent
        file_path = str(project_root / "src" / "domain" / "clean_entity.py")

        exit_code, stdout_json, stderr = run_hook(
            "Write",
            {"file_path": file_path, "content": content},
        )

        assert exit_code == 0
        assert stdout_json is not None
        assert get_permission_decision(stdout_json) == "allow"

    def test_hook_preserves_existing_security_checks(self) -> None:
        """Hook should still block writes to sensitive paths."""
        exit_code, stdout_json, stderr = run_hook(
            "Write",
            {"file_path": "~/.ssh/id_rsa", "content": "private key"},
        )

        assert exit_code == 0
        assert stdout_json is not None
        assert get_permission_decision(stdout_json) == "deny"
        assert "security" in get_permission_reason(stdout_json).lower()

    def test_hook_preserves_bash_security_checks(self) -> None:
        """Hook should still block dangerous bash commands."""
        exit_code, stdout_json, stderr = run_hook(
            "Bash",
            {"command": "rm -rf /"},
        )

        assert exit_code == 0
        assert stdout_json is not None
        assert get_permission_decision(stdout_json) == "deny"

    def test_hook_approves_non_python_write(self) -> None:
        """Hook should approve writing non-Python files without AST checks."""
        project_root = SCRIPTS_DIR.parent
        file_path = str(project_root / "docs" / "README.md")

        exit_code, stdout_json, stderr = run_hook(
            "Write",
            {"file_path": file_path, "content": "# README"},
        )

        assert exit_code == 0
        assert stdout_json is not None
        assert get_permission_decision(stdout_json) == "allow"

    def test_hook_blocks_multi_class_file(self) -> None:
        """Hook should block a Write with multiple public classes."""
        content = '''"""Module with two classes."""


class FirstPublic:
    """First class."""
    pass


class SecondPublic:
    """Second class."""
    pass
'''
        project_root = SCRIPTS_DIR.parent
        file_path = str(project_root / "src" / "domain" / "multi_class.py")

        exit_code, stdout_json, stderr = run_hook(
            "Write",
            {"file_path": file_path, "content": content},
        )

        assert exit_code == 0
        assert stdout_json is not None
        assert get_permission_decision(stdout_json) == "deny"
        assert "one-class-per-file" in get_permission_reason(stdout_json).lower()
