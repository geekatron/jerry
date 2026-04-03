# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Integration tests for PreToolUse hook with AST enforcement.

Tests the full hook pipeline by invoking the CLI-based enforcement
(``uv run jerry hooks pre-tool-use``) which runs SecurityEnforcementEngine
(security checks) + PreToolEnforcementEngine (architecture).

References:
    - EN-703: PreToolUse Enforcement Engine
    - AC-015: Hook validation framework
    - STORY-023: Deprecated scripts/pre_tool_use.py removal
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

_REPO_ROOT = str(Path(__file__).resolve().parents[2])


def run_hook(tool_name: str, tool_input: dict) -> tuple[int, dict | None, str]:
    """Run the pre-tool-use hook via CLI.

    Args:
        tool_name: Name of the tool (e.g., "Write", "Edit", "Bash").
        tool_input: Tool input parameters.

    Returns:
        Tuple of (exit_code, stdout_json_or_none, stderr_text).
    """
    input_data = json.dumps({"tool_name": tool_name, "tool_input": tool_input})

    result = subprocess.run(
        ["uv", "run", "--directory", _REPO_ROOT, "jerry", "--json", "hooks", "pre-tool-use"],
        input=input_data,
        capture_output=True,
        text=True,
        timeout=15,
        cwd=_REPO_ROOT,
    )

    stdout_json = None
    if result.stdout.strip():
        try:
            stdout_json = json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            pass

    return result.returncode, stdout_json, result.stderr


def is_blocked(output: dict | None) -> bool:
    """Return True if the hook blocked the tool use."""
    return output is not None and output.get("decision") == "block"


def is_approved(output: dict | None) -> bool:
    """Return True if the hook approved the tool use."""
    if output is None:
        return True
    return output.get("decision") != "block"


def get_reason(output: dict | None) -> str:
    """Extract the block reason from hook output."""
    if output is None:
        return ""
    return output.get("reason", "")


class TestHookArchitectureEnforcement:
    """Integration tests for AST enforcement in the hook pipeline."""

    def test_hook_blocks_architecture_violation_on_write(self) -> None:
        """Hook should block a Write that violates import boundaries."""
        content = '''"""Bad domain module."""

from src.infrastructure.adapters.persistence import FileAdapter


class BadEntity:
    """Entity with forbidden import."""
    pass
'''
        file_path = str(Path(_REPO_ROOT) / "src" / "domain" / "bad_entity.py")

        exit_code, stdout_json, stderr = run_hook(
            "Write",
            {"file_path": file_path, "content": content},
        )

        assert exit_code == 0
        assert is_blocked(stdout_json)
        assert "infrastructure" in get_reason(stdout_json).lower()

    def test_hook_approves_clean_write(self) -> None:
        """Hook should approve a Write with no violations."""
        content = '''"""Clean domain module."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CleanEntity:
    """A compliant domain entity."""

    name: str
'''
        file_path = str(Path(_REPO_ROOT) / "src" / "domain" / "clean_entity.py")

        exit_code, stdout_json, stderr = run_hook(
            "Write",
            {"file_path": file_path, "content": content},
        )

        assert exit_code == 0
        assert is_approved(stdout_json)

    def test_hook_preserves_existing_security_checks(self) -> None:
        """Hook should still block writes to sensitive paths."""
        exit_code, stdout_json, stderr = run_hook(
            "Write",
            {"file_path": "~/.ssh/id_rsa", "content": "private key"},
        )

        assert exit_code == 0
        assert is_blocked(stdout_json)
        reason = get_reason(stdout_json)
        assert (
            "security" in reason.lower() or "blocked" in reason.lower() or "ssh" in reason.lower()
        )

    def test_hook_preserves_bash_security_checks(self) -> None:
        """Hook should still block dangerous bash commands."""
        exit_code, stdout_json, stderr = run_hook(
            "Bash",
            {"command": "rm -rf /"},
        )

        assert exit_code == 0
        assert is_blocked(stdout_json)

    def test_hook_approves_non_python_write(self) -> None:
        """Hook should approve writing non-Python files without AST checks."""
        file_path = str(Path(_REPO_ROOT) / "docs" / "README.md")

        exit_code, stdout_json, stderr = run_hook(
            "Write",
            {"file_path": file_path, "content": "# README"},
        )

        assert exit_code == 0
        assert is_approved(stdout_json)

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
        file_path = str(Path(_REPO_ROOT) / "src" / "domain" / "multi_class.py")

        exit_code, stdout_json, stderr = run_hook(
            "Write",
            {"file_path": file_path, "content": content},
        )

        assert exit_code == 0
        assert is_blocked(stdout_json)
        assert "one-class-per-file" in get_reason(stdout_json).lower()
