# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Integration tests for AST CLI commands via subprocess execution.

These tests validate the actual invocation patterns by shelling out to
``uv run jerry ast <command>`` for all CLI commands. This ensures the full
import chain and execution path works end-to-end.

Test Categories:
- TestJerryAstCli: jerry ast parse/render/validate/query via subprocess
- TestJerryAstFrontmatter: jerry ast frontmatter via subprocess
- TestJerryAstModify: jerry ast modify via subprocess
- TestJerryAstReinject: jerry ast reinject via subprocess
- TestJerryAstValidateEnhanced: jerry ast validate (JSON output, --nav) via subprocess
- TestErrorCases: Error handling for missing files and bad schemas
- TestImportChain: Domain layer import validation

References:
    - ST-004: Add jerry ast CLI Commands
    - BUG-002: Route /ast Skill Through CLI
    - FEAT-001: AST-Based Markdown Operations
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

# Mark entire module as integration + subprocess tests
pytestmark = [
    pytest.mark.integration,
    pytest.mark.subprocess,
]


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent.parent


@pytest.fixture
def env_with_pythonpath(project_root: Path) -> dict[str, str]:
    """Create environment with PYTHONPATH set to project root."""
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{project_root}:{existing}" if existing else str(project_root)
    return env


@pytest.fixture
def story_file(project_root: Path) -> Path:
    """Path to a real story entity file in the repo."""
    return (
        project_root
        / "projects"
        / "PROJ-005-markdown-ast"
        / "work"
        / "EPIC-001-markdown-ast"
        / "FEAT-001-ast-strategy"
        / "ST-001-jerry-document"
        / "ST-001-jerry-document.md"
    )


@pytest.fixture
def rules_file(project_root: Path) -> Path:
    """Path to a rules file with L2-REINJECT directives and nav table."""
    return project_root / ".context" / "rules" / "quality-enforcement.md"


@pytest.fixture
def scratch_story(story_file: Path, tmp_path: Path) -> Path:
    """Copy a story file to tmp_path for write tests."""
    dest = tmp_path / "scratch-story.md"
    shutil.copy2(story_file, dest)
    return dest


# =============================================================================
# Helpers
# =============================================================================


def run_jerry_ast(
    args: list[str],
    project_root: Path,
    env: dict[str, str],
    timeout: int = 30,
) -> subprocess.CompletedProcess[str]:
    """Execute ``uv run jerry ast <args>``.

    Args:
        args: Arguments after ``jerry ast`` (e.g., ["parse", "file.md"]).
        project_root: Project root path for cwd.
        env: Environment variables.
        timeout: Max seconds before killing the process.

    Returns:
        CompletedProcess with stdout, stderr, and returncode.
    """
    return subprocess.run(
        ["uv", "run", "jerry", "ast", *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(project_root),
        timeout=timeout,
    )


# =============================================================================
# jerry ast CLI commands
# =============================================================================


class TestJerryAstCli:
    """Integration tests for jerry ast CLI commands via subprocess."""

    def test_ast_parse_outputs_valid_json(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        story_file: Path,
    ) -> None:
        """jerry ast parse outputs valid JSON with tokens and tree."""
        result = run_jerry_ast(["parse", str(story_file)], project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert "file" in data
        assert "tokens" in data
        assert "tree" in data
        assert isinstance(data["tokens"], list)
        assert isinstance(data["tree"], dict)

    def test_ast_render_outputs_markdown(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        story_file: Path,
    ) -> None:
        """jerry ast render outputs normalized markdown."""
        result = run_jerry_ast(["render", str(story_file)], project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "# ST-001" in result.stdout

    def test_ast_validate_without_schema(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        story_file: Path,
    ) -> None:
        """jerry ast validate without --schema outputs JSON with nav table results."""
        result = run_jerry_ast(["validate", str(story_file)], project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert "is_valid" in data
        assert "nav_table_valid" in data
        assert "schema_valid" in data
        assert data["schema_valid"] is True

    def test_ast_validate_with_schema(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        story_file: Path,
    ) -> None:
        """jerry ast validate --schema story outputs JSON report."""
        result = run_jerry_ast(
            ["validate", "--schema", "story", str(story_file)],
            project_root,
            env_with_pythonpath,
        )

        # Exit code: 0 if valid, 1 if violations
        assert result.returncode in [0, 1], f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert "schema" in data
        assert data["schema"] == "story"
        assert "is_valid" in data
        assert "violations" in data

    def test_ast_query_heading(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        story_file: Path,
    ) -> None:
        """jerry ast query heading returns matching nodes."""
        result = run_jerry_ast(
            ["query", str(story_file), "heading"],
            project_root,
            env_with_pythonpath,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["selector"] == "heading"
        assert data["count"] > 0
        assert isinstance(data["nodes"], list)

    def test_ast_query_nonexistent_type(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        story_file: Path,
    ) -> None:
        """jerry ast query with non-matching type returns count=0."""
        result = run_jerry_ast(
            ["query", str(story_file), "nonexistent_type"],
            project_root,
            env_with_pythonpath,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["count"] == 0
        assert data["nodes"] == []


# =============================================================================
# Error Cases
# =============================================================================


class TestErrorCases:
    """Error handling tests for CLI via subprocess."""

    def test_cli_parse_file_not_found(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """jerry ast parse with missing file returns exit code 2."""
        result = run_jerry_ast(["parse", "/nonexistent/file.md"], project_root, env_with_pythonpath)

        assert result.returncode == 2

    def test_cli_validate_unknown_schema(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        story_file: Path,
    ) -> None:
        """jerry ast validate --schema unknown returns exit code 2."""
        result = run_jerry_ast(
            ["validate", "--schema", "unknown_type", str(story_file)],
            project_root,
            env_with_pythonpath,
        )

        assert result.returncode == 2

    def test_cli_frontmatter_file_not_found(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """jerry ast frontmatter with missing file returns exit code 2."""
        result = run_jerry_ast(
            ["frontmatter", "/nonexistent/file.md"], project_root, env_with_pythonpath
        )

        assert result.returncode == 2

    def test_cli_modify_nonexistent_key(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        scratch_story: Path,
    ) -> None:
        """jerry ast modify with nonexistent key returns exit code 1."""
        result = run_jerry_ast(
            ["modify", str(scratch_story), "--key", "NonExistent", "--value", "v"],
            project_root,
            env_with_pythonpath,
        )

        assert result.returncode == 1


# =============================================================================
# jerry ast frontmatter
# =============================================================================


class TestJerryAstFrontmatter:
    """Integration tests for jerry ast frontmatter via subprocess."""

    def test_frontmatter_extracts_fields(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        story_file: Path,
    ) -> None:
        """jerry ast frontmatter extracts Type, Status, etc. from entity files."""
        result = run_jerry_ast(["frontmatter", str(story_file)], project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert isinstance(data, dict)
        assert data.get("Type") == "story"
        assert "Status" in data
        assert "Parent" in data

    def test_frontmatter_returns_empty_for_plain_markdown(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """jerry ast frontmatter returns {} for files without frontmatter."""
        plain_file = tmp_path / "plain.md"
        plain_file.write_text("# Just a heading\n\nSome text.\n")

        result = run_jerry_ast(["frontmatter", str(plain_file)], project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data == {}


# =============================================================================
# jerry ast modify
# =============================================================================


class TestJerryAstModify:
    """Integration tests for jerry ast modify via subprocess."""

    def test_modify_updates_field(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        scratch_story: Path,
    ) -> None:
        """jerry ast modify writes new value and returns JSON status."""
        result = run_jerry_ast(
            ["modify", str(scratch_story), "--key", "Status", "--value", "done"],
            project_root,
            env_with_pythonpath,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["status"] == "modified"
        assert data["key"] == "Status"
        assert data["value"] == "done"

        # Verify file was modified on disk
        content = scratch_story.read_text(encoding="utf-8")
        assert "done" in content

    def test_modify_is_idempotent(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        scratch_story: Path,
    ) -> None:
        """jerry ast modify applied twice produces same result."""
        run_jerry_ast(
            ["modify", str(scratch_story), "--key", "Status", "--value", "done"],
            project_root,
            env_with_pythonpath,
        )
        result = run_jerry_ast(
            ["modify", str(scratch_story), "--key", "Status", "--value", "done"],
            project_root,
            env_with_pythonpath,
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"
        content = scratch_story.read_text(encoding="utf-8")
        assert content.count("done") >= 1


# =============================================================================
# jerry ast reinject
# =============================================================================


class TestJerryAstReinject:
    """Integration tests for jerry ast reinject via subprocess."""

    def test_reinject_from_rules_file(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        rules_file: Path,
    ) -> None:
        """jerry ast reinject finds L2-REINJECT directives in rules files."""
        result = run_jerry_ast(["reinject", str(rules_file)], project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert isinstance(data, list)
        assert len(data) > 0
        first = data[0]
        assert "rank" in first
        assert "tokens" in first
        assert "content" in first
        assert "line_number" in first

    def test_reinject_returns_empty_for_plain_file(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """jerry ast reinject returns [] for files without directives."""
        plain_file = tmp_path / "no-reinject.md"
        plain_file.write_text("# No directives\n\nJust text.\n")

        result = run_jerry_ast(["reinject", str(plain_file)], project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data == []


# =============================================================================
# jerry ast validate (enhanced)
# =============================================================================


class TestJerryAstValidateEnhanced:
    """Integration tests for enhanced jerry ast validate via subprocess."""

    def test_validate_no_schema_outputs_json(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        story_file: Path,
    ) -> None:
        """jerry ast validate without --schema outputs JSON with nav table results."""
        result = run_jerry_ast(["validate", str(story_file)], project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert "is_valid" in data
        assert "nav_table_valid" in data
        assert "missing_nav_entries" in data
        assert "schema_valid" in data
        assert data["schema_valid"] is True

    def test_validate_nav_flag_includes_entries(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        rules_file: Path,
    ) -> None:
        """jerry ast validate --nav includes detailed nav table entries."""
        result = run_jerry_ast(
            ["validate", "--nav", str(rules_file)], project_root, env_with_pythonpath
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert "nav_entries" in data
        assert isinstance(data["nav_entries"], list)
        assert len(data["nav_entries"]) > 0
        entry = data["nav_entries"][0]
        assert "section_name" in entry
        assert "anchor" in entry
