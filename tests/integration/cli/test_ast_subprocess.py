# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Integration tests for AST operations via subprocess execution.

These tests validate the actual Claude Code invocation pattern by shelling
out to ``uv run python -c`` for ast_ops functions and ``uv run jerry ast``
for CLI commands. This ensures the full import chain and execution path
works end-to-end -- not just the Python API in isolation.

Test Categories:
- TestAstOpsParseFile: parse_file() via subprocess
- TestAstOpsQueryFrontmatter: query_frontmatter() via subprocess
- TestAstOpsModifyFrontmatter: modify_frontmatter() via subprocess
- TestAstOpsValidateFile: validate_file() via subprocess
- TestAstOpsRenderFile: render_file() via subprocess
- TestAstOpsExtractReinject: extract_reinject() via subprocess
- TestAstOpsValidateNavTable: validate_nav_table_file() via subprocess
- TestJerryAstCli: jerry ast parse/render/validate/query via subprocess
- TestErrorCases: Error handling for missing files and bad schemas

References:
    - ST-005: /ast Claude Skill
    - ST-004: Add jerry ast CLI Commands
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


def run_ast_op(
    code: str,
    project_root: Path,
    env: dict[str, str],
    timeout: int = 30,
) -> subprocess.CompletedProcess[str]:
    """Execute a Python one-liner via ``uv run python -c``.

    This mirrors the exact invocation pattern Claude Code uses when calling
    /ast skill operations.

    Args:
        code: Python code string to execute.
        project_root: Project root path for cwd.
        env: Environment variables.
        timeout: Max seconds before killing the process.

    Returns:
        CompletedProcess with stdout, stderr, and returncode.
    """
    return subprocess.run(
        ["uv", "run", "python", "-c", code],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(project_root),
        timeout=timeout,
    )


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
# ast_ops: parse_file
# =============================================================================


class TestAstOpsParseFile:
    """Integration tests for parse_file() via subprocess."""

    def test_parse_file_returns_valid_json(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        story_file: Path,
    ) -> None:
        """parse_file() returns parseable JSON with expected keys."""
        code = (
            "import json; "
            "from skills.ast.scripts.ast_ops import parse_file; "
            f"print(json.dumps(parse_file('{story_file}')))"
        )
        result = run_ast_op(code, project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert isinstance(data, dict)
        assert "source_length" in data
        assert "node_types" in data
        assert "heading_count" in data
        assert "has_frontmatter" in data

    def test_parse_file_detects_frontmatter(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        story_file: Path,
    ) -> None:
        """parse_file() detects blockquote frontmatter in entity files."""
        code = (
            "import json; "
            "from skills.ast.scripts.ast_ops import parse_file; "
            f"print(json.dumps(parse_file('{story_file}')))"
        )
        result = run_ast_op(code, project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["has_frontmatter"] is True
        assert data["heading_count"] > 0
        assert isinstance(data["node_types"], list)
        assert len(data["node_types"]) > 0


# =============================================================================
# ast_ops: query_frontmatter
# =============================================================================


class TestAstOpsQueryFrontmatter:
    """Integration tests for query_frontmatter() via subprocess."""

    def test_query_frontmatter_extracts_fields(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        story_file: Path,
    ) -> None:
        """query_frontmatter() extracts Type, Status, etc. from entity files."""
        code = (
            "import json; "
            "from skills.ast.scripts.ast_ops import query_frontmatter; "
            f"print(json.dumps(query_frontmatter('{story_file}')))"
        )
        result = run_ast_op(code, project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert isinstance(data, dict)
        assert data.get("Type") == "story"
        assert "Status" in data
        assert "Parent" in data

    def test_query_frontmatter_returns_empty_dict_for_plain_markdown(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """query_frontmatter() returns {} for files without frontmatter."""
        plain_file = tmp_path / "plain.md"
        plain_file.write_text("# Just a heading\n\nSome text.\n")

        code = (
            "import json; "
            "from skills.ast.scripts.ast_ops import query_frontmatter; "
            f"print(json.dumps(query_frontmatter('{plain_file}')))"
        )
        result = run_ast_op(code, project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data == {}


# =============================================================================
# ast_ops: modify_frontmatter
# =============================================================================


class TestAstOpsModifyFrontmatter:
    """Integration tests for modify_frontmatter() via subprocess."""

    def test_modify_frontmatter_updates_field(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        scratch_story: Path,
    ) -> None:
        """modify_frontmatter() writes new value and returns updated content."""
        code = (
            "from skills.ast.scripts.ast_ops import modify_frontmatter; "
            f"result = modify_frontmatter('{scratch_story}', 'Status', 'done'); "
            "print(result)"
        )
        result = run_ast_op(code, project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "done" in result.stdout

        # Verify the file was actually modified on disk
        content = scratch_story.read_text(encoding="utf-8")
        assert "done" in content

    def test_modify_frontmatter_is_idempotent(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        scratch_story: Path,
    ) -> None:
        """modify_frontmatter() applied twice produces same result."""
        code = (
            "from skills.ast.scripts.ast_ops import modify_frontmatter; "
            f"modify_frontmatter('{scratch_story}', 'Status', 'done'); "
            f"result = modify_frontmatter('{scratch_story}', 'Status', 'done'); "
            "print(result)"
        )
        result = run_ast_op(code, project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        content = scratch_story.read_text(encoding="utf-8")
        assert content.count("done") >= 1


# =============================================================================
# ast_ops: validate_file
# =============================================================================


class TestAstOpsValidateFile:
    """Integration tests for validate_file() via subprocess."""

    def test_validate_file_without_schema(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        story_file: Path,
    ) -> None:
        """validate_file() without schema checks nav table only."""
        code = (
            "import json; "
            "from skills.ast.scripts.ast_ops import validate_file; "
            f"print(json.dumps(validate_file('{story_file}')))"
        )
        result = run_ast_op(code, project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert isinstance(data, dict)
        assert "is_valid" in data
        assert "nav_table_valid" in data
        assert "schema_valid" in data
        assert data["schema"] is None

    def test_validate_file_with_story_schema(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        story_file: Path,
    ) -> None:
        """validate_file() with schema='story' performs schema validation."""
        code = (
            "import json; "
            "from skills.ast.scripts.ast_ops import validate_file; "
            f"print(json.dumps(validate_file('{story_file}', schema='story')))"
        )
        result = run_ast_op(code, project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["schema"] == "story"
        assert isinstance(data["schema_violations"], list)


# =============================================================================
# ast_ops: render_file
# =============================================================================


class TestAstOpsRenderFile:
    """Integration tests for render_file() via subprocess."""

    def test_render_file_returns_normalized_markdown(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        story_file: Path,
    ) -> None:
        """render_file() returns non-empty normalized markdown."""
        code = (
            "from skills.ast.scripts.ast_ops import render_file; "
            f"print(render_file('{story_file}'), end='')"
        )
        result = run_ast_op(code, project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert len(result.stdout) > 0
        assert "# ST-001" in result.stdout

    def test_render_file_is_idempotent(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """Rendering the rendered output produces identical output."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Hello\n\nSome text.\n")

        # First render
        code1 = (
            "from skills.ast.scripts.ast_ops import render_file; "
            f"print(render_file('{md_file}'), end='')"
        )
        r1 = run_ast_op(code1, project_root, env_with_pythonpath)
        assert r1.returncode == 0, f"stderr: {r1.stderr}"

        # Write rendered output and render again
        md_file.write_text(r1.stdout)
        code2 = (
            "from skills.ast.scripts.ast_ops import render_file; "
            f"print(render_file('{md_file}'), end='')"
        )
        r2 = run_ast_op(code2, project_root, env_with_pythonpath)
        assert r2.returncode == 0, f"stderr: {r2.stderr}"
        assert r1.stdout == r2.stdout


# =============================================================================
# ast_ops: extract_reinject
# =============================================================================


class TestAstOpsExtractReinject:
    """Integration tests for extract_reinject() via subprocess."""

    def test_extract_reinject_from_rules_file(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        rules_file: Path,
    ) -> None:
        """extract_reinject() finds L2-REINJECT directives in rules files."""
        code = (
            "import json; "
            "from skills.ast.scripts.ast_ops import extract_reinject; "
            f"print(json.dumps(extract_reinject('{rules_file}')))"
        )
        result = run_ast_op(code, project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert isinstance(data, list)
        assert len(data) > 0
        # Each directive should have rank, tokens, content, line_number
        first = data[0]
        assert "rank" in first
        assert "tokens" in first
        assert "content" in first
        assert "line_number" in first

    def test_extract_reinject_returns_empty_for_plain_file(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """extract_reinject() returns [] for files without directives."""
        plain_file = tmp_path / "no-reinject.md"
        plain_file.write_text("# No directives\n\nJust text.\n")

        code = (
            "import json; "
            "from skills.ast.scripts.ast_ops import extract_reinject; "
            f"print(json.dumps(extract_reinject('{plain_file}')))"
        )
        result = run_ast_op(code, project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data == []


# =============================================================================
# ast_ops: validate_nav_table_file
# =============================================================================


class TestAstOpsValidateNavTable:
    """Integration tests for validate_nav_table_file() via subprocess."""

    def test_validate_nav_table_on_rules_file(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        rules_file: Path,
    ) -> None:
        """validate_nav_table_file() validates a file with nav table."""
        code = (
            "import json; "
            "from skills.ast.scripts.ast_ops import validate_nav_table_file; "
            f"print(json.dumps(validate_nav_table_file('{rules_file}')))"
        )
        result = run_ast_op(code, project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert isinstance(data, dict)
        assert "is_valid" in data
        assert "entries" in data
        assert isinstance(data["entries"], list)
        if data["entries"]:
            entry = data["entries"][0]
            assert "section_name" in entry
            assert "anchor" in entry

    def test_validate_nav_table_on_entity_file(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        story_file: Path,
    ) -> None:
        """validate_nav_table_file() works on entity files with nav tables."""
        code = (
            "import json; "
            "from skills.ast.scripts.ast_ops import validate_nav_table_file; "
            f"print(json.dumps(validate_nav_table_file('{story_file}')))"
        )
        result = run_ast_op(code, project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert isinstance(data["is_valid"], bool)
        assert isinstance(data["missing_entries"], list)


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
        """jerry ast validate without --schema prints OK message."""
        result = run_jerry_ast(["validate", str(story_file)], project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "Validation OK" in result.stdout

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
    """Error handling tests for ast_ops and CLI via subprocess."""

    def test_ast_ops_file_not_found(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """ast_ops raises FileNotFoundError for missing files."""
        code = (
            "from skills.ast.scripts.ast_ops import parse_file; parse_file('/nonexistent/file.md')"
        )
        result = run_ast_op(code, project_root, env_with_pythonpath)

        assert result.returncode != 0
        assert "FileNotFoundError" in result.stderr

    def test_ast_ops_invalid_schema_name(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        story_file: Path,
    ) -> None:
        """validate_file() raises ValueError for unknown schema."""
        code = (
            "from skills.ast.scripts.ast_ops import validate_file; "
            f"validate_file('{story_file}', schema='nonexistent')"
        )
        result = run_ast_op(code, project_root, env_with_pythonpath)

        assert result.returncode != 0
        assert "ValueError" in result.stderr

    def test_ast_ops_modify_nonexistent_key(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
        scratch_story: Path,
    ) -> None:
        """modify_frontmatter() raises KeyError for missing field."""
        code = (
            "from skills.ast.scripts.ast_ops import modify_frontmatter; "
            f"modify_frontmatter('{scratch_story}', 'NonExistentKey', 'value')"
        )
        result = run_ast_op(code, project_root, env_with_pythonpath)

        assert result.returncode != 0
        assert "KeyError" in result.stderr

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


# =============================================================================
# Import Validation
# =============================================================================


class TestImportChain:
    """Validate that the full import chain works via subprocess."""

    def test_ast_ops_importable(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """skills.ast.scripts.ast_ops is importable via uv run."""
        code = (
            "from skills.ast.scripts.ast_ops import ("
            "parse_file, query_frontmatter, modify_frontmatter, "
            "validate_file, render_file, extract_reinject, "
            "validate_nav_table_file); "
            "print('OK')"
        )
        result = run_ast_op(code, project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "OK" in result.stdout
        assert "ModuleNotFoundError" not in result.stderr
        assert "ImportError" not in result.stderr

    def test_domain_layer_importable(
        self,
        project_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """src.domain.markdown_ast package is importable via uv run."""
        code = (
            "from src.domain.markdown_ast import ("
            "JerryDocument, BlockquoteFrontmatter, extract_frontmatter, "
            "extract_reinject_directives, validate_nav_table, "
            "get_entity_schema, validate_document); "
            "print('OK')"
        )
        result = run_ast_op(code, project_root, env_with_pythonpath)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "OK" in result.stdout
