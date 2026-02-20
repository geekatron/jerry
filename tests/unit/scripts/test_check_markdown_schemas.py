# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for the pre-commit markdown schema validation hook (ST-009).

Tests cover:
    - Schema detection from file paths (entity prefix -> schema type mapping)
    - Validation logic with valid and invalid entity files
    - Output formatting (violation messages, summary line)
    - Exit codes (0 for pass, 1 for violations)
    - Skipping non-entity markdown files

Test Categories:
    - detect_schema_from_path: Maps file paths to entity schema types
    - validate_file: Validates individual files against detected schemas
    - format_violation: Formats violations for IDE-friendly output
    - main integration: End-to-end with mocked git output

References:
    - ST-009: Add Pre-Commit Validation Hook
    - H-20: BDD test-first approach
    - H-21: 90% line coverage
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add project root to sys.path so we can import the script
_project_root = Path(__file__).parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# ---------------------------------------------------------------------------
# Import the module under test
# ---------------------------------------------------------------------------

from scripts.check_markdown_schemas import (  # noqa: E402
    detect_schema_from_path,
    format_summary,
    format_violation,
    main,
    validate_file,
)


# ---------------------------------------------------------------------------
# Fixtures: valid entity markdown sources
# ---------------------------------------------------------------------------

VALID_STORY_SOURCE = """\
# ST-001: My Story

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this covers |
| [Acceptance Criteria](#acceptance-criteria) | Done conditions |

---

> **Type:** story
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-01-01
> **Parent:** FEAT-001

---

## Summary

Story summary.

---

## Acceptance Criteria

- [ ] Done when X
"""

INVALID_STORY_SOURCE = """\
# ST-001: Missing Fields

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this covers |
| [Acceptance Criteria](#acceptance-criteria) | Done conditions |

---

> **Status:** pending
> **Priority:** medium

---

## Summary

Story summary.

---

## Acceptance Criteria

- [ ] Done when X
"""

PLAIN_MARKDOWN = """\
# Some Readme

Just a plain markdown file with no entity structure.
"""


# ===========================================================================
# Test: detect_schema_from_path
# ===========================================================================


class TestDetectSchemaFromPath:
    """Tests for schema detection from file paths."""

    def test_enabler_path(self) -> None:
        """EN-xxx path in projects work directory returns 'enabler'."""
        path = "projects/PROJ-001/work/EPIC-001/FEAT-001/EN-001-infra/EN-001-infra.md"
        assert detect_schema_from_path(path) == "enabler"

    def test_story_path(self) -> None:
        """ST-xxx path in projects work directory returns 'story'."""
        path = "projects/PROJ-005/work/EPIC-001/FEAT-001/ST-009-precommit/ST-009-precommit.md"
        assert detect_schema_from_path(path) == "story"

    def test_task_path(self) -> None:
        """TASK-xxx path in projects work directory returns 'task'."""
        path = "projects/PROJ-001/work/EPIC-001/FEAT-001/TASK-001-setup/TASK-001-setup.md"
        assert detect_schema_from_path(path) == "task"

    def test_bug_path(self) -> None:
        """BUG-xxx path in projects work directory returns 'bug'."""
        path = "projects/PROJ-003/work/BUG-011-fix/BUG-011-fix.md"
        assert detect_schema_from_path(path) == "bug"

    def test_feature_path_in_directory(self) -> None:
        """FEAT-xxx path inside a directory returns 'feature'."""
        path = "projects/PROJ-005/work/EPIC-001/FEAT-001-ast/FEAT-001-ast.md"
        assert detect_schema_from_path(path) == "feature"

    def test_feature_path_direct(self) -> None:
        """FEAT-xxx.md directly under work returns 'feature'."""
        path = "projects/PROJ-001/work/EPIC-001/FEAT-001-ast.md"
        assert detect_schema_from_path(path) == "feature"

    def test_epic_path_in_directory(self) -> None:
        """EPIC-xxx path inside a directory returns 'epic'."""
        path = "projects/PROJ-005/work/EPIC-001-markdown-ast/EPIC-001-markdown-ast.md"
        assert detect_schema_from_path(path) == "epic"

    def test_epic_path_direct(self) -> None:
        """EPIC-xxx.md directly under work returns 'epic'."""
        path = "projects/PROJ-001/work/EPIC-001-markdown-ast.md"
        assert detect_schema_from_path(path) == "epic"

    def test_random_md_returns_none(self) -> None:
        """Random .md file outside projects/work returns None (skip)."""
        path = "README.md"
        assert detect_schema_from_path(path) is None

    def test_context_rules_returns_none(self) -> None:
        """.context/rules/ markdown file returns None (skip)."""
        path = ".context/rules/coding-standards.md"
        assert detect_schema_from_path(path) is None

    def test_docs_markdown_returns_none(self) -> None:
        """docs/ markdown file returns None (skip)."""
        path = "docs/knowledge/some-doc.md"
        assert detect_schema_from_path(path) is None

    def test_plan_md_returns_none(self) -> None:
        """PLAN.md in project directory returns None (skip)."""
        path = "projects/PROJ-005-markdown-ast/PLAN.md"
        assert detect_schema_from_path(path) is None

    def test_worktracker_md_returns_none(self) -> None:
        """WORKTRACKER.md in project directory returns None (skip)."""
        path = "projects/PROJ-005-markdown-ast/WORKTRACKER.md"
        assert detect_schema_from_path(path) is None


# ===========================================================================
# Test: validate_file
# ===========================================================================


class TestValidateFile:
    """Tests for file validation logic using tmp_path."""

    def test_valid_story_file_no_violations(self, tmp_path: Path) -> None:
        """Valid entity file produces no violations."""
        file_path = tmp_path / "ST-001.md"
        file_path.write_text(VALID_STORY_SOURCE, encoding="utf-8")

        violations = validate_file(str(file_path), "story")
        assert violations == []

    def test_invalid_story_file_has_violations(self, tmp_path: Path) -> None:
        """Invalid entity file (missing required fields) produces violations."""
        file_path = tmp_path / "ST-001.md"
        file_path.write_text(INVALID_STORY_SOURCE, encoding="utf-8")

        violations = validate_file(str(file_path), "story")
        assert len(violations) > 0
        # Should detect missing Type field at minimum
        field_paths = [v.field_path for v in violations]
        assert "frontmatter.Type" in field_paths

    def test_nonexistent_file_returns_empty(self, tmp_path: Path) -> None:
        """Non-existent file returns empty violations list (skip gracefully)."""
        file_path = tmp_path / "does-not-exist.md"

        violations = validate_file(str(file_path), "story")
        assert violations == []

    def test_valid_task_file_no_violations(self, tmp_path: Path) -> None:
        """Valid task file (no nav table required) produces no violations."""
        task_source = """\
# TASK-001: My Task

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-01-01
> **Parent:** ST-001

---

## Summary

Task summary.
"""
        file_path = tmp_path / "TASK-001.md"
        file_path.write_text(task_source, encoding="utf-8")

        violations = validate_file(str(file_path), "task")
        assert violations == []


# ===========================================================================
# Test: format_violation
# ===========================================================================


class TestFormatViolation:
    """Tests for violation output formatting."""

    def test_format_includes_filepath_and_message(self) -> None:
        """Formatted violation includes file path and message."""
        from src.domain.markdown_ast.schema import ValidationViolation

        v = ValidationViolation(
            field_path="frontmatter.Type",
            expected="field present (required)",
            actual="field missing",
            severity="error",
            message="Required field 'Type' is missing from frontmatter.",
        )

        result = format_violation("path/to/file.md", v)
        assert "path/to/file.md" in result
        assert "Required field 'Type' is missing from frontmatter." in result

    def test_format_uses_colon_separator(self) -> None:
        """Formatted violation uses colon separator for IDE integration."""
        from src.domain.markdown_ast.schema import ValidationViolation

        v = ValidationViolation(
            field_path="sections.Summary",
            expected="## Summary section present",
            actual="section missing",
            severity="error",
            message="Required section '## Summary' is missing from document.",
        )

        result = format_violation("file.md", v)
        # Format should be "file:message"
        assert result.startswith("file.md:")


# ===========================================================================
# Test: format_summary
# ===========================================================================


class TestFormatSummary:
    """Tests for summary line formatting."""

    def test_summary_format_no_violations(self) -> None:
        """Summary with zero violations."""
        result = format_summary(5, 0)
        assert "5 files checked" in result
        assert "0 violations found" in result

    def test_summary_format_with_violations(self) -> None:
        """Summary with violations."""
        result = format_summary(3, 7)
        assert "3 files checked" in result
        assert "7 violations found" in result


# ===========================================================================
# Test: main (exit codes)
# ===========================================================================


class TestMain:
    """Tests for main() exit codes with mocked git interaction."""

    @patch("scripts.check_markdown_schemas.get_staged_markdown_files")
    def test_no_staged_files_exits_zero(self, mock_git: MagicMock) -> None:
        """No staged markdown files -> exit 0."""
        mock_git.return_value = []
        assert main() == 0

    @patch("scripts.check_markdown_schemas.get_staged_markdown_files")
    def test_staged_non_entity_files_exits_zero(self, mock_git: MagicMock) -> None:
        """Staged files that are not entity files -> exit 0 (all skipped)."""
        mock_git.return_value = ["README.md", "docs/architecture.md"]
        assert main() == 0

    @patch("scripts.check_markdown_schemas.get_staged_markdown_files")
    @patch("scripts.check_markdown_schemas.validate_file")
    def test_all_valid_exits_zero(
        self, mock_validate: MagicMock, mock_git: MagicMock
    ) -> None:
        """All valid entity files -> exit 0."""
        mock_git.return_value = [
            "projects/PROJ-005/work/EPIC-001/FEAT-001/ST-001-x/ST-001-x.md"
        ]
        mock_validate.return_value = []
        assert main() == 0

    @patch("scripts.check_markdown_schemas.get_staged_markdown_files")
    @patch("scripts.check_markdown_schemas.validate_file")
    def test_violations_found_exits_one(
        self, mock_validate: MagicMock, mock_git: MagicMock
    ) -> None:
        """Entity files with violations -> exit 1."""
        from src.domain.markdown_ast.schema import ValidationViolation

        mock_git.return_value = [
            "projects/PROJ-005/work/EPIC-001/FEAT-001/ST-001-x/ST-001-x.md"
        ]
        mock_validate.return_value = [
            ValidationViolation(
                field_path="frontmatter.Type",
                expected="field present (required)",
                actual="field missing",
                severity="error",
                message="Required field 'Type' is missing from frontmatter.",
            )
        ]
        assert main() == 1
