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
    """Create environment with PYTHONPATH set to project root.

    Also disables path containment checks (WI-018) since integration tests
    use temp files outside the repository root.
    """
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{project_root}:{existing}" if existing else str(project_root)
    env["JERRY_DISABLE_PATH_CONTAINMENT"] = "1"
    return env


@pytest.fixture
def env_with_containment_enabled(project_root: Path) -> dict[str, str]:
    """Like env_with_pythonpath but leaves path containment ENABLED
    (BUG-010 Option C, Section 4.E).

    Unlike ``env_with_pythonpath``, this fixture does NOT set
    ``JERRY_DISABLE_PATH_CONTAINMENT`` -- and explicitly pops it (and any
    ``JERRY_AST__TRUSTED_ROOTS``/``JERRY_PROJECT`` residue) from the
    inherited environment, so containment enforcement and config
    precedence are deterministic for these black-box subprocess tests.
    """
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{project_root}:{existing}" if existing else str(project_root)
    env.pop("JERRY_DISABLE_PATH_CONTAINMENT", None)
    env.pop("JERRY_AST__TRUSTED_ROOTS", None)
    env.pop("JERRY_PROJECT", None)
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


# =============================================================================
# BUG-010 Option C: black-box containment regression via real subprocess
# invocation with path containment ENABLED (not the module-wide
# env_with_pythonpath fixture, which disables containment).
# =============================================================================


class TestOptionCContainmentSubprocess:
    """End-to-end containment behavior via ``uv run jerry ast`` subprocess."""

    def test_ast_parse_subprocess_when_file_in_tempdir_and_no_trusted_roots_then_rejected(
        self,
        project_root: Path,
        env_with_containment_enabled: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """Black-box negative regression: a file outside the project root,
        with no configured ast.trusted_roots, is rejected (exit code 2)."""
        target = tmp_path / "outside.md"
        target.write_text("# Outside\n", encoding="utf-8")

        result = run_jerry_ast(["parse", str(target)], project_root, env_with_containment_enabled)

        assert result.returncode == 2

    def test_ast_parse_subprocess_when_file_in_configured_trusted_root_via_env_then_allowed(
        self,
        project_root: Path,
        env_with_containment_enabled: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """A file inside a JERRY_AST__TRUSTED_ROOTS-declared directory is
        allowed, even though it is outside the project root."""
        trusted_dir = tmp_path / "trusted"
        trusted_dir.mkdir()
        target = trusted_dir / "scratchpad.md"
        target.write_text("# Scratch\n", encoding="utf-8")

        env = dict(env_with_containment_enabled)
        env["JERRY_AST__TRUSTED_ROOTS"] = json.dumps([str(trusted_dir)])

        result = run_jerry_ast(["parse", str(target)], project_root, env)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["file"] == str(target)

    def test_ast_parse_subprocess_when_quiet_flag_given_then_stderr_empty_despite_configured_root_match(
        self,
        project_root: Path,
        env_with_containment_enabled: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """--quiet suppresses the R-4 configured-root transparency note."""
        trusted_dir = tmp_path / "trusted"
        trusted_dir.mkdir()
        target = trusted_dir / "scratchpad.md"
        target.write_text("# Scratch\n", encoding="utf-8")

        env = dict(env_with_containment_enabled)
        env["JERRY_AST__TRUSTED_ROOTS"] = json.dumps([str(trusted_dir)])

        result = run_jerry_ast(["parse", str(target), "--quiet"], project_root, env)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert result.stderr == ""

    def test_ast_parse_subprocess_when_no_quiet_and_configured_root_match_then_stderr_has_note(
        self,
        project_root: Path,
        env_with_containment_enabled: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """Without --quiet, a configured-root match prints the R-4
        transparency note on stderr."""
        trusted_dir = tmp_path / "trusted"
        trusted_dir.mkdir()
        target = trusted_dir / "scratchpad.md"
        target.write_text("# Scratch\n", encoding="utf-8")

        env = dict(env_with_containment_enabled)
        env["JERRY_AST__TRUSTED_ROOTS"] = json.dumps([str(trusted_dir)])

        result = run_jerry_ast(["parse", str(target)], project_root, env)

        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "configured trusted root" in result.stderr.lower()

    def test_ast_modify_subprocess_when_symlink_swapped_before_write_then_rejected_and_file_unchanged(
        self,
        project_root: Path,
        env_with_containment_enabled: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """End-to-end C2 regression: a symlink that initially resolves
        inside a configured trusted root (so an earlier ``ast parse``
        succeeds) is then repointed outside all allowed roots. A
        subsequent ``ast modify`` on the same symlink is rejected -- the
        write-time recheck uses the identical containment function as the
        read-time check, re-resolving the symlink fresh, so it cannot
        disagree with (or lag behind) the live filesystem state."""
        trusted_dir = tmp_path / "trusted"
        trusted_dir.mkdir()
        inside_target = trusted_dir / "inside.md"
        inside_target.write_text(
            "# Entity\n\n> **Status:** pending\n\n## Details\n", encoding="utf-8"
        )
        outside_dir = tmp_path / "outside"
        outside_dir.mkdir()
        outside_target = outside_dir / "outside.md"
        outside_target.write_text(
            "# Entity\n\n> **Status:** pending\n\n## Details\n", encoding="utf-8"
        )

        link = trusted_dir / "entity.md"
        link.symlink_to(inside_target)

        env = dict(env_with_containment_enabled)
        env["JERRY_AST__TRUSTED_ROOTS"] = json.dumps([str(trusted_dir)])

        # Baseline: the symlink currently resolves inside the trusted
        # root, so a read-only command succeeds.
        baseline = run_jerry_ast(["parse", str(link)], project_root, env)
        assert baseline.returncode == 0, f"stderr: {baseline.stderr}"

        # Swap the symlink to point outside all allowed roots.
        link.unlink()
        link.symlink_to(outside_target)

        # Act: ast modify on the now-escaping symlink must be rejected.
        result = run_jerry_ast(
            ["modify", str(link), "--key", "Status", "--value", "done"], project_root, env
        )

        # Assert
        assert result.returncode == 2
        assert outside_target.read_text(encoding="utf-8") == (
            "# Entity\n\n> **Status:** pending\n\n## Details\n"
        )

    def test_ast_parse_subprocess_when_root_flag_and_broad_root_then_warns_on_stderr_and_succeeds(
        self,
        project_root: Path,
        env_with_containment_enabled: dict[str, str],
        tmp_path: Path,
    ) -> None:
        """--root '/' triggers the R-3 broad-root stderr warning but the
        invocation still succeeds (user discretion), propagated end-to-end
        through a real subprocess invocation."""
        target = tmp_path / "file.md"
        target.write_text("# File\n", encoding="utf-8")

        result = run_jerry_ast(
            ["parse", str(target), "--root", "/"], project_root, env_with_containment_enabled
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "Warning" in result.stderr
