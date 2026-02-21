# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Contract tests for SessionStart hook output compliance.

These tests verify that the hook output conforms to the Claude Code
hook response format. The hook is invoked via the Jerry CLI:
    jerry --json hooks session-start

Expected Format (EN-006 architecture):
    {
        "additionalContext": "..."  // Added to Claude's context
    }

Test Distribution per testing-standards.md:
    - Contract tests: 5% of total coverage
    - Focus: External interface compliance

References:
    - EN-006: jerry hooks CLI Command Namespace
    - EN-007: Hook Wrapper Scripts
    - Phase 3: Contract Tests (T-020 to T-026)
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

import pytest


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


def run_hook_cli(
    project_root: Path,
    project_dir: Path | None = None,
    stdin_data: str = "{}",
) -> subprocess.CompletedProcess[str]:
    """Run the hooks session-start CLI command and capture output.

    Args:
        project_root: Jerry plugin root directory
        project_dir: Optional project directory to set as CLAUDE_PROJECT_DIR
        stdin_data: JSON to pass as stdin (default: empty object)

    Returns:
        CompletedProcess with stdout, stderr, and returncode
    """
    env = os.environ.copy()
    if project_dir:
        env["CLAUDE_PROJECT_DIR"] = str(project_dir)

    # Remove JERRY_PROJECT to test local context behavior
    env.pop("JERRY_PROJECT", None)

    return subprocess.run(
        ["uv", "run", "jerry", "--json", "hooks", "session-start"],
        input=stdin_data,
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
        project_root: Path,
    ) -> None:
        """T-020: Hook output is valid JSON.

        Contract: The hook MUST output valid JSON that can be parsed
        without errors.
        """
        # Act
        result = run_hook_cli(project_root)

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
        project_root: Path,
    ) -> None:
        """Hook output must not be empty."""
        # Act
        result = run_hook_cli(project_root)

        # Assert
        assert result.stdout.strip(), "Hook output must not be empty"


# =============================================================================
# T-023: additionalContext is a String
# =============================================================================


class TestAdditionalContext:
    """Contract: additionalContext MUST be a string."""

    def test_additional_context_is_string(
        self,
        project_root: Path,
    ) -> None:
        """T-023: additionalContext is a string.

        Contract: The additionalContext MUST be a string
        that will be added to Claude's context window.
        """
        # Act
        result = run_hook_cli(project_root)

        # Assert
        data = parse_hook_output(result.stdout)

        assert "additionalContext" in data, (
            "Hook output must contain 'additionalContext' field.\n"
            f"Actual keys: {list(data.keys())}"
        )

        assert isinstance(data["additionalContext"], str), (
            f"additionalContext must be a string, got: {type(data['additionalContext'])}"
        )

    def test_additional_context_not_empty(
        self,
        project_root: Path,
    ) -> None:
        """additionalContext must not be empty."""
        # Act
        result = run_hook_cli(project_root)

        # Assert
        data = parse_hook_output(result.stdout)
        additional_context = data.get("additionalContext", "")

        assert additional_context.strip(), "additionalContext must not be empty"


# =============================================================================
# T-024: additionalContext Contains Project XML Tags
# =============================================================================


class TestXmlTagsInAdditionalContext:
    """Contract: additionalContext SHOULD contain XML tags for Claude."""

    def test_additional_context_contains_project_context_tags_when_project_active(
        self,
        project_root: Path,
    ) -> None:
        """T-024: additionalContext contains project XML tags when project is active.

        Contract: Per Anthropic prompt engineering best practices, the
        additionalContext SHOULD use XML tags to structure data for Claude.

        Expected tags:
        - <project-context> when a project is active
        """
        # Act - run with JERRY_PROJECT set to an active project
        env = os.environ.copy()
        env["JERRY_PROJECT"] = "PROJ-004-context-resilience"

        result = subprocess.run(
            ["uv", "run", "jerry", "--json", "hooks", "session-start"],
            input="{}",
            capture_output=True,
            text=True,
            env=env,
            cwd=str(project_root),
            timeout=30,
        )

        # Assert
        data = parse_hook_output(result.stdout)
        additional_context = data.get("additionalContext", "")

        # At least one project-related tag should be present
        has_project_context = "<project-context>" in additional_context
        has_jerry_project = "<jerry-project>" in additional_context

        assert has_project_context or has_jerry_project, (
            "additionalContext should contain project XML tags.\n"
            f"Expected: <project-context> or <jerry-project>\n"
            f"Actual content: {additional_context[:500]}..."
        )

    def test_project_context_tag_has_required_fields(
        self,
        project_root: Path,
    ) -> None:
        """<project-context> tag contains required fields.

        When a project is active, the <project-context> tag should include
        <jerry-project> and <project-id>.
        """
        # Act
        result = run_hook_cli(project_root)

        # Assert
        data = parse_hook_output(result.stdout)
        additional_context = data.get("additionalContext", "")

        # If project-context is present, verify required fields
        if "<project-context>" in additional_context:
            assert "<jerry-project>" in additional_context, (
                "<project-context> should contain <jerry-project> element"
            )
            assert "<project-id>" in additional_context, (
                "<project-context> should contain <project-id> element"
            )


# =============================================================================
# T-025: Quality Reinforcement Content
# =============================================================================


class TestQualityReinforcement:
    """Contract: additionalContext SHOULD contain quality reinforcement."""

    def test_additional_context_contains_quality_content(
        self,
        project_root: Path,
    ) -> None:
        """T-025: additionalContext contains quality reinforcement.

        Contract: The hook should inject L2 quality reinforcement content
        into Claude's context per EN-705 architecture.
        """
        # Act
        result = run_hook_cli(project_root)

        # Assert
        data = parse_hook_output(result.stdout)
        additional_context = data.get("additionalContext", "")

        # Quality reinforcement should contain constitutional principles
        assert "P-003" in additional_context or "P-020" in additional_context, (
            "additionalContext should contain quality reinforcement content.\n"
            f"Actual content (first 300 chars): {additional_context[:300]}..."
        )


# =============================================================================
# Error Handling Contract Tests
# =============================================================================


class TestHookErrorHandling:
    """Contract: Hook errors MUST still output valid JSON."""

    def test_hook_error_outputs_valid_json(
        self,
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
            ["uv", "run", "jerry", "--json", "hooks", "session-start"],
            input="{}",
            capture_output=True,
            text=True,
            env=env,
            cwd=str(project_root),
            timeout=30,
        )

        # Assert - even with potential errors, output should be valid JSON
        assert result.returncode == 0, (
            f"Hook should exit 0 even on errors\n"
            f"stderr: {result.stderr}"
        )

        try:
            data = parse_hook_output(result.stdout)
            assert "additionalContext" in data
        except json.JSONDecodeError:
            pytest.fail(
                f"Hook output is not valid JSON even during error.\n"
                f"stdout: {result.stdout}\n"
                f"stderr: {result.stderr}"
            )
