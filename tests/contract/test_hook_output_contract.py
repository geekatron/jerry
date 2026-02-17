# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Contract tests for SessionStart hook output compliance.

These tests verify that the hook output conforms to the Claude Code
Advanced JSON format specification for SessionStart hooks.

Contract Reference:
    - https://code.claude.com/docs/en/hooks#advanced:-json-output
    - DISC-004: Hook format correction
    - DISC-005: Combined output empirical test (verified)

Expected Format:
    {
        "systemMessage": "...",  // Optional: shown to user in terminal
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "..."  // Added to Claude's context
        }
    }

Test Distribution per testing-standards.md:
    - Contract tests: 5% of total coverage
    - Focus: External interface compliance

References:
    - EN-001: Session Start Hook TDD Cleanup
    - Phase 3: Contract Tests (T-020 to T-026)
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    pass


# Mark as contract tests
pytestmark = [
    pytest.mark.contract,
]


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def project_root() -> Path:
    """Get the project root directory."""
    # Navigate from tests/contract to project root
    return Path(__file__).parent.parent.parent


@pytest.fixture
def hook_script_path(project_root: Path) -> Path:
    """Get the path to the session start hook script."""
    return project_root / "scripts" / "session_start_hook.py"


@pytest.fixture
def temp_project_with_context(tmp_path: Path) -> Path:
    """Create a temporary project directory with valid context.

    Returns:
        Path to the temporary project root (containing projects/).
    """
    # Create projects structure
    projects_dir = tmp_path / "projects"
    projects_dir.mkdir()
    project_dir = projects_dir / "PROJ-001-test"
    project_dir.mkdir()
    (project_dir / "PLAN.md").write_text("# Test Plan")

    # Create local context
    local_dir = tmp_path / ".jerry" / "local"
    local_dir.mkdir(parents=True)
    context_file = local_dir / "context.toml"
    context_file.write_text('[context]\nactive_project = "PROJ-001-test"\n')

    return tmp_path


def run_hook_script(
    hook_script_path: Path,
    project_root: Path,
    project_dir: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run the hook script and capture output.

    Args:
        hook_script_path: Path to session_start_hook.py
        project_root: Jerry plugin root directory
        project_dir: Optional project directory to set as CLAUDE_PROJECT_DIR

    Returns:
        CompletedProcess with stdout, stderr, and returncode
    """
    env = os.environ.copy()
    if project_dir:
        env["CLAUDE_PROJECT_DIR"] = str(project_dir)

    # Remove JERRY_PROJECT to test local context behavior
    env.pop("JERRY_PROJECT", None)

    return subprocess.run(
        ["python3", str(hook_script_path)],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(project_root),
        timeout=30,
    )


def parse_hook_output(stdout: str) -> dict[str, Any]:
    """Parse hook output as JSON.

    Raises:
        json.JSONDecodeError: If output is not valid JSON
    """
    return json.loads(stdout.strip())


# =============================================================================
# T-020: Hook Output is Valid JSON
# =============================================================================


class TestHookOutputValidJson:
    """Contract: Hook output MUST be valid JSON."""

    def test_hook_output_is_valid_json(
        self,
        hook_script_path: Path,
        project_root: Path,
        temp_project_with_context: Path,
    ) -> None:
        """T-020: Hook output is valid JSON.

        Contract: The hook MUST output valid JSON that can be parsed
        without errors.
        """
        # Act
        result = run_hook_script(
            hook_script_path,
            project_root,
            project_dir=temp_project_with_context,
        )

        # Assert - output must be valid JSON
        assert result.returncode == 0, f"Hook failed with stderr: {result.stderr}"

        try:
            data = parse_hook_output(result.stdout)
        except json.JSONDecodeError as e:
            pytest.fail(
                f"Hook output is not valid JSON: {e}\n"
                f"stdout: {result.stdout}\n"
                f"stderr: {result.stderr}"
            )

        assert isinstance(data, dict), "Hook output must be a JSON object"

    def test_hook_output_not_empty(
        self,
        hook_script_path: Path,
        project_root: Path,
        temp_project_with_context: Path,
    ) -> None:
        """Hook output must not be empty."""
        # Act
        result = run_hook_script(
            hook_script_path,
            project_root,
            project_dir=temp_project_with_context,
        )

        # Assert
        assert result.stdout.strip(), "Hook output must not be empty"


# =============================================================================
# T-021: Hook Output Has hookSpecificOutput Object
# =============================================================================


class TestHookSpecificOutput:
    """Contract: Hook output MUST have hookSpecificOutput object."""

    def test_hook_output_has_hook_specific_output(
        self,
        hook_script_path: Path,
        project_root: Path,
        temp_project_with_context: Path,
    ) -> None:
        """T-021: Hook output has hookSpecificOutput object.

        Contract: Per Claude Code Advanced JSON format, SessionStart hooks
        MUST include a hookSpecificOutput object.
        """
        # Act
        result = run_hook_script(
            hook_script_path,
            project_root,
            project_dir=temp_project_with_context,
        )

        # Assert
        data = parse_hook_output(result.stdout)

        assert "hookSpecificOutput" in data, (
            "Hook output must contain 'hookSpecificOutput' field.\n"
            f"Actual keys: {list(data.keys())}"
        )

        assert isinstance(data["hookSpecificOutput"], dict), (
            "hookSpecificOutput must be an object.\n"
            f"Actual type: {type(data['hookSpecificOutput'])}"
        )


# =============================================================================
# T-022: hookEventName is "SessionStart"
# =============================================================================


class TestHookEventName:
    """Contract: hookEventName MUST be 'SessionStart'."""

    def test_hook_event_name_is_session_start(
        self,
        hook_script_path: Path,
        project_root: Path,
        temp_project_with_context: Path,
    ) -> None:
        """T-022: hookEventName is 'SessionStart'.

        Contract: The hookSpecificOutput.hookEventName MUST be 'SessionStart'
        for session initialization hooks.
        """
        # Act
        result = run_hook_script(
            hook_script_path,
            project_root,
            project_dir=temp_project_with_context,
        )

        # Assert
        data = parse_hook_output(result.stdout)
        hook_output = data.get("hookSpecificOutput", {})

        assert "hookEventName" in hook_output, (
            "hookSpecificOutput must contain 'hookEventName' field."
        )

        assert hook_output["hookEventName"] == "SessionStart", (
            f"hookEventName must be 'SessionStart', got: {hook_output['hookEventName']}"
        )


# =============================================================================
# T-023: additionalContext is a String
# =============================================================================


class TestAdditionalContext:
    """Contract: additionalContext MUST be a string."""

    def test_additional_context_is_string(
        self,
        hook_script_path: Path,
        project_root: Path,
        temp_project_with_context: Path,
    ) -> None:
        """T-023: additionalContext is a string.

        Contract: The hookSpecificOutput.additionalContext MUST be a string
        that will be added to Claude's context window.
        """
        # Act
        result = run_hook_script(
            hook_script_path,
            project_root,
            project_dir=temp_project_with_context,
        )

        # Assert
        data = parse_hook_output(result.stdout)
        hook_output = data.get("hookSpecificOutput", {})

        assert "additionalContext" in hook_output, (
            "hookSpecificOutput must contain 'additionalContext' field."
        )

        assert isinstance(hook_output["additionalContext"], str), (
            f"additionalContext must be a string, got: {type(hook_output['additionalContext'])}"
        )

    def test_additional_context_not_empty(
        self,
        hook_script_path: Path,
        project_root: Path,
        temp_project_with_context: Path,
    ) -> None:
        """additionalContext must not be empty."""
        # Act
        result = run_hook_script(
            hook_script_path,
            project_root,
            project_dir=temp_project_with_context,
        )

        # Assert
        data = parse_hook_output(result.stdout)
        hook_output = data.get("hookSpecificOutput", {})
        additional_context = hook_output.get("additionalContext", "")

        assert additional_context.strip(), "additionalContext must not be empty"


# =============================================================================
# T-024: additionalContext Contains Project XML Tags
# =============================================================================


class TestXmlTagsInAdditionalContext:
    """Contract: additionalContext SHOULD contain XML tags for Claude."""

    def test_additional_context_contains_project_context_tags(
        self,
        hook_script_path: Path,
        project_root: Path,
        temp_project_with_context: Path,
    ) -> None:
        """T-024: additionalContext contains project XML tags.

        Contract: Per Anthropic prompt engineering best practices, the
        additionalContext SHOULD use XML tags to structure data for Claude.

        Expected tags:
        - <project-context> when a project is active
        - <project-required> when no project is set
        - <project-error> when project validation fails
        """
        # Act
        result = run_hook_script(
            hook_script_path,
            project_root,
            project_dir=temp_project_with_context,
        )

        # Assert
        data = parse_hook_output(result.stdout)
        hook_output = data.get("hookSpecificOutput", {})
        additional_context = hook_output.get("additionalContext", "")

        # At least one of the expected tags should be present
        has_project_context = "<project-context>" in additional_context
        has_project_required = "<project-required>" in additional_context
        has_project_error = "<project-error>" in additional_context
        has_hook_error = "<hook-error>" in additional_context

        assert has_project_context or has_project_required or has_project_error or has_hook_error, (
            "additionalContext should contain project XML tags.\n"
            f"Expected one of: <project-context>, <project-required>, <project-error>\n"
            f"Actual content: {additional_context[:500]}..."
        )

    def test_project_context_tag_has_required_fields(
        self,
        hook_script_path: Path,
        project_root: Path,
        temp_project_with_context: Path,
    ) -> None:
        """<project-context> tag contains required fields.

        When a project is active, the <project-context> tag should include:
        - ProjectActive: the project ID
        - ProjectPath: the project path
        - ValidationMessage: validation status
        """
        # Act
        result = run_hook_script(
            hook_script_path,
            project_root,
            project_dir=temp_project_with_context,
        )

        # Assert
        data = parse_hook_output(result.stdout)
        hook_output = data.get("hookSpecificOutput", {})
        additional_context = hook_output.get("additionalContext", "")

        # If project-context is present, verify required fields
        if "<project-context>" in additional_context:
            assert "ProjectActive:" in additional_context, (
                "<project-context> should contain ProjectActive field"
            )
            assert "ProjectPath:" in additional_context, (
                "<project-context> should contain ProjectPath field"
            )
            # ValidationMessage is optional but preferred


# =============================================================================
# T-025: systemMessage Field for User Terminal Output (AC-002, AC-003)
# =============================================================================


class TestSystemMessage:
    """Contract: Hook output MUST have systemMessage for user visibility.

    Per DISC-005 and AC-002/AC-003, the hook output MUST include BOTH:
    - systemMessage: Shown to user in terminal
    - hookSpecificOutput.additionalContext: Added to Claude's context

    This ensures users see project context at session start, not just
    the generic "SessionStart:startup hook succeeded: Success" message.
    """

    def test_hook_output_has_system_message(
        self,
        hook_script_path: Path,
        project_root: Path,
        temp_project_with_context: Path,
    ) -> None:
        """T-025a: Hook output has systemMessage field.

        Contract: Per AC-003, the hook MUST include systemMessage field
        so users see project context in their terminal.
        """
        # Act
        result = run_hook_script(
            hook_script_path,
            project_root,
            project_dir=temp_project_with_context,
        )

        # Assert
        data = parse_hook_output(result.stdout)

        assert "systemMessage" in data, (
            "Hook output must contain 'systemMessage' field (AC-003).\n"
            f"Actual keys: {list(data.keys())}\n"
            "Without systemMessage, users only see:\n"
            "  'SessionStart:startup hook succeeded: Success'\n"
            "instead of useful project context."
        )

    def test_system_message_is_string(
        self,
        hook_script_path: Path,
        project_root: Path,
        temp_project_with_context: Path,
    ) -> None:
        """T-025b: systemMessage is a string.

        Contract: systemMessage must be a string that will be displayed
        to the user in their terminal at session start.
        """
        # Act
        result = run_hook_script(
            hook_script_path,
            project_root,
            project_dir=temp_project_with_context,
        )

        # Assert
        data = parse_hook_output(result.stdout)

        assert "systemMessage" in data, "Missing systemMessage field"
        assert isinstance(data["systemMessage"], str), (
            f"systemMessage must be a string, got: {type(data['systemMessage'])}"
        )

    def test_system_message_contains_jerry_context(
        self,
        hook_script_path: Path,
        project_root: Path,
        temp_project_with_context: Path,
    ) -> None:
        """T-025c: systemMessage contains meaningful Jerry context.

        Contract: systemMessage should indicate Jerry Framework status
        to help users understand the session context.
        """
        # Act
        result = run_hook_script(
            hook_script_path,
            project_root,
            project_dir=temp_project_with_context,
        )

        # Assert
        data = parse_hook_output(result.stdout)

        assert "systemMessage" in data, "Missing systemMessage field"
        system_message = data["systemMessage"]

        # Should contain Jerry-related content
        assert "Jerry" in system_message or "jerry" in system_message.lower(), (
            f"systemMessage should mention Jerry Framework.\nActual message: {system_message}"
        )

    def test_system_message_not_empty(
        self,
        hook_script_path: Path,
        project_root: Path,
        temp_project_with_context: Path,
    ) -> None:
        """T-025d: systemMessage must not be empty."""
        # Act
        result = run_hook_script(
            hook_script_path,
            project_root,
            project_dir=temp_project_with_context,
        )

        # Assert
        data = parse_hook_output(result.stdout)

        assert "systemMessage" in data, "Missing systemMessage field"
        assert data["systemMessage"].strip(), "systemMessage must not be empty"


# =============================================================================
# T-026: Combined Output Format (AC-002, AC-003)
# =============================================================================


class TestCombinedOutputFormat:
    """Contract: Hook MUST output BOTH systemMessage AND additionalContext.

    Per DISC-005 empirical testing and AC-002/AC-003:
    - systemMessage: What user sees in terminal
    - hookSpecificOutput.additionalContext: What Claude sees in context

    Both fields serve different purposes and MUST both be present.
    """

    def test_hook_has_both_system_message_and_additional_context(
        self,
        hook_script_path: Path,
        project_root: Path,
        temp_project_with_context: Path,
    ) -> None:
        """T-026a: Hook has BOTH systemMessage AND additionalContext.

        Contract: Per AC-003, hook must include BOTH fields for proper
        user and Claude visibility.
        """
        # Act
        result = run_hook_script(
            hook_script_path,
            project_root,
            project_dir=temp_project_with_context,
        )

        # Assert
        data = parse_hook_output(result.stdout)

        # Verify both fields exist
        assert "systemMessage" in data, "Missing systemMessage - user won't see project context"
        assert "hookSpecificOutput" in data, "Missing hookSpecificOutput"
        assert "additionalContext" in data.get("hookSpecificOutput", {}), (
            "Missing additionalContext - Claude won't see project context"
        )

        # Verify neither is empty
        assert data["systemMessage"].strip(), "systemMessage is empty"
        assert data["hookSpecificOutput"]["additionalContext"].strip(), "additionalContext is empty"


# =============================================================================
# Error Handling Contract Tests
# =============================================================================


class TestHookErrorHandling:
    """Contract: Hook errors MUST still output valid JSON."""

    def test_hook_error_outputs_valid_json(
        self,
        hook_script_path: Path,
        project_root: Path,
        tmp_path: Path,
    ) -> None:
        """Hook errors should still output valid JSON.

        Contract: Even when errors occur, the hook MUST output valid JSON
        to prevent breaking Claude's hook system.
        """
        # Arrange - point to non-existent project dir
        env = os.environ.copy()
        env["CLAUDE_PROJECT_DIR"] = str(tmp_path)
        env.pop("JERRY_PROJECT", None)

        # Act
        result = subprocess.run(
            ["python3", str(hook_script_path)],
            capture_output=True,
            text=True,
            env=env,
            cwd=str(project_root),
            timeout=30,
        )

        # Assert - even with potential errors, output should be valid JSON
        assert result.returncode == 0, "Hook should exit 0 even on errors"

        try:
            data = parse_hook_output(result.stdout)
            assert "hookSpecificOutput" in data
        except json.JSONDecodeError:
            pytest.fail(
                f"Hook output is not valid JSON even during error.\n"
                f"stdout: {result.stdout}\n"
                f"stderr: {result.stderr}"
            )
