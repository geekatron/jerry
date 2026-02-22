# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BDD tests for ST-007: Migrate /worktracker Agents to AST.

Validates that the AST domain layer correctly handles real-format entity files,
which is the foundation for migrating wt-verifier, wt-auditor, and wt-visualizer
agents from raw text manipulation to AST-based operations.

Test categories:
    - query_frontmatter: Extracts fields from real-format entity files
    - validate_file with schema: Validates entity files against built-in schemas
    - Entity type detection: Infers entity type from file path/name
    - Schema validation errors: Surfaces violations in structured reports

References:
    - ST-007: Migrate /worktracker Agents to AST
    - H-20: BDD test-first (RED phase written before implementation)
    - H-21: 90% line coverage required
"""

from __future__ import annotations

import os
import tempfile

import pytest

from skills.ast.scripts.ast_ops import (
    parse_file,
    query_frontmatter,
    validate_file,
)
from src.domain.markdown_ast.jerry_document import JerryDocument
from src.domain.markdown_ast.schema import (
    get_entity_schema,
    validate_document,
)

# ---------------------------------------------------------------------------
# Fixtures: temp file helpers
# ---------------------------------------------------------------------------


def _write_temp(content: str, suffix: str = ".md") -> str:
    """Write content to a temporary file and return its absolute path."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)
    return path


# ---------------------------------------------------------------------------
# Fixtures: realistic entity file content strings
# ---------------------------------------------------------------------------

EPIC_MD = """\
# EPIC-001: OSS Release Preparation

> **Type:** epic
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-10
> **Due:** ---
> **Completed:** ---
> **Parent:** ---
> **Owner:** Adam Nowak
> **Target Quarter:** FY26-Q1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description |
| [Children Features/Capabilities](#children-featurescapabilities) | Feature inventory |
| [Progress Summary](#progress-summary) | Overall progress |

---

## Summary

Prepare the Jerry framework for public open-source release.

---

## Children Features/Capabilities

| Feature | Status |
|---------|--------|
| FEAT-001 | done |

---

## Progress Summary

In progress.
"""

FEATURE_MD = """\
# FEAT-001: Fix CI Build Failures

> **Type:** feature
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-10
> **Due:** ---
> **Completed:** 2026-02-11
> **Parent:** EPIC-001
> **Owner:** Adam Nowak
> **Target Sprint:** ---

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Children Stories/Enablers](#children-storiesenablers) | Child work items |
| [Progress Summary](#progress-summary) | Feature progress |

---

## Summary

Fix all CI build failures.

---

## Acceptance Criteria

- [x] All CI checks pass

---

## Children Stories/Enablers

| Child | Status |
|-------|--------|
| EN-001 | done |

---

## Progress Summary

Complete.
"""

ENABLER_MD = """\
# EN-001: Fix Plugin Validation

> **Type:** enabler
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-10
> **Due:** ---
> **Completed:** 2026-02-11
> **Parent:** FEAT-001
> **Owner:** ---
> **Effort:** ---

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Technical Approach](#technical-approach) | How to fix |

---

## Summary

Fix the Plugin Validation CI check.

---

## Acceptance Criteria

- [x] Plugin validation passes

---

## Technical Approach

Add missing keywords property to schema.
"""

TASK_MD = """\
# TASK-001: Add keywords to marketplace schema

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Created:** 2026-02-10
> **Parent:** EN-001
> **Owner:** ---
> **Remaining:** 0

---

## Summary

Add the `keywords` property to the marketplace plugin item schema.
"""

STORY_MD = """\
# ST-007: Migrate /worktracker Agents to AST

> **Type:** story
> **Status:** pending
> **Priority:** medium
> **Impact:** high
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** --
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Scope and context |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |

---

## Summary

Pilot migration: update /worktracker agent definitions to use /ast skill operations.

---

## Acceptance Criteria

- [ ] wt-verifier agent uses AST-based frontmatter extraction
- [ ] wt-auditor agent uses AST-based validation
"""

BUG_MD = """\
# BUG-004: Plugin Uninstall Fails

> **Type:** bug
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-18
> **Due:** ---
> **Completed:** 2026-02-18
> **Parent:** EPIC-001
> **Owner:** Adam Nowak
> **Found In:** 0.2.0
> **Fix Version:** 0.2.1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description |
| [Steps to Reproduce](#steps-to-reproduce) | How to trigger the bug |
| [Acceptance Criteria](#acceptance-criteria) | Fix verification |

---

## Summary

Jerry plugin cannot be uninstalled via Claude Code UI.

---

## Steps to Reproduce

1. Install Jerry plugin
2. Try to uninstall
3. Error occurs

---

## Acceptance Criteria

- [x] Plugin can be uninstalled cleanly
"""

# A malformed entity file: missing required frontmatter fields
MALFORMED_ENABLER_MD = """\
# EN-999: Broken Enabler

> **Type:** enabler
> **Status:** in_progress

---

## Summary

Missing most required fields -- no Priority, Impact, Enabler Type, Created, Parent.
"""

# A file with invalid status value
INVALID_STATUS_MD = """\
# TASK-099: Bad Status

> **Type:** task
> **Status:** done
> **Priority:** high
> **Created:** 2026-02-20
> **Parent:** EN-001

---

## Summary

This task has invalid status "done" instead of "completed".
"""


# ---------------------------------------------------------------------------
# Entity type detection helper (used by migration comparison script)
# ---------------------------------------------------------------------------

_ENTITY_PREFIX_MAP = {
    "EPIC": "epic",
    "FEAT": "feature",
    "ST": "story",
    "EN": "enabler",
    "TASK": "task",
    "BUG": "bug",
}


def detect_entity_type(file_path: str) -> str | None:
    """
    Detect entity type from a file path based on filename prefix.

    Inspects the basename of the file path for known entity prefixes
    (EPIC-, FEAT-, ST-, EN-, TASK-, BUG-) and returns the corresponding
    entity type string suitable for get_entity_schema().

    Args:
        file_path: Path to a worktracker entity file.

    Returns:
        Entity type string (e.g., "epic", "task") or None if unrecognized.
    """
    basename = os.path.basename(file_path)
    for prefix, entity_type in _ENTITY_PREFIX_MAP.items():
        if basename.startswith(f"{prefix}-"):
            return entity_type
    return None


# ---------------------------------------------------------------------------
# Tests: query_frontmatter on real-format entity files
# ---------------------------------------------------------------------------


class TestQueryFrontmatterEntityFiles:
    """Tests that query_frontmatter correctly extracts fields from real-format entity files."""

    @pytest.mark.happy_path
    def test_epic_frontmatter_extraction(self) -> None:
        """query_frontmatter extracts all expected fields from an epic entity file."""
        path = _write_temp(EPIC_MD)
        try:
            fm = query_frontmatter(path)
            assert fm["Type"] == "epic"
            assert fm["Status"] == "in_progress"
            assert fm["Priority"] == "high"
            assert fm["Impact"] == "high"
            assert fm["Created"] == "2026-02-10"
            assert fm["Owner"] == "Adam Nowak"
            assert fm["Target Quarter"] == "FY26-Q1"
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_feature_frontmatter_extraction(self) -> None:
        """query_frontmatter extracts all expected fields from a feature entity file."""
        path = _write_temp(FEATURE_MD)
        try:
            fm = query_frontmatter(path)
            assert fm["Type"] == "feature"
            assert fm["Status"] == "completed"
            assert fm["Parent"] == "EPIC-001"
            assert fm["Owner"] == "Adam Nowak"
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_enabler_frontmatter_extraction(self) -> None:
        """query_frontmatter extracts Enabler Type from enabler entity files."""
        path = _write_temp(ENABLER_MD)
        try:
            fm = query_frontmatter(path)
            assert fm["Type"] == "enabler"
            assert fm["Enabler Type"] == "infrastructure"
            assert fm["Parent"] == "FEAT-001"
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_task_frontmatter_extraction(self) -> None:
        """query_frontmatter extracts task-specific fields."""
        path = _write_temp(TASK_MD)
        try:
            fm = query_frontmatter(path)
            assert fm["Type"] == "task"
            assert fm["Status"] == "completed"
            assert fm["Parent"] == "EN-001"
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_story_frontmatter_extraction(self) -> None:
        """query_frontmatter extracts story-specific fields."""
        path = _write_temp(STORY_MD)
        try:
            fm = query_frontmatter(path)
            assert fm["Type"] == "story"
            assert fm["Status"] == "pending"
            assert fm["Effort"] == "3"
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_bug_frontmatter_extraction(self) -> None:
        """query_frontmatter extracts bug-specific fields (Severity, Found In, Fix Version)."""
        path = _write_temp(BUG_MD)
        try:
            fm = query_frontmatter(path)
            assert fm["Type"] == "bug"
            assert fm["Severity"] == "major"
            assert fm["Found In"] == "0.2.0"
            assert fm["Fix Version"] == "0.2.1"
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_frontmatter_status_usable_for_verification(self) -> None:
        """query_frontmatter status value can be used for wt-verifier status checks."""
        path = _write_temp(ENABLER_MD)
        try:
            fm = query_frontmatter(path)
            status = fm.get("Status", "")
            # wt-verifier checks if status is a valid value
            valid_statuses = {"pending", "in_progress", "completed", "blocked", "cancelled"}
            assert status in valid_statuses
        finally:
            os.unlink(path)


# ---------------------------------------------------------------------------
# Tests: validate_file with schema validation (via domain layer)
# ---------------------------------------------------------------------------


class TestValidateFileWithSchema:
    """Tests that validate_file with appropriate schema validates entity files correctly."""

    @pytest.mark.happy_path
    def test_valid_epic_passes_schema(self) -> None:
        """A well-formed epic passes schema validation."""
        path = _write_temp(EPIC_MD)
        try:
            result = validate_file(path, schema="epic")
            assert result["schema_valid"] is True
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_valid_feature_passes_schema(self) -> None:
        """A well-formed feature passes schema validation."""
        path = _write_temp(FEATURE_MD)
        try:
            result = validate_file(path, schema="feature")
            assert result["schema_valid"] is True
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_valid_enabler_passes_schema(self) -> None:
        """A well-formed enabler passes schema validation."""
        path = _write_temp(ENABLER_MD)
        try:
            result = validate_file(path, schema="enabler")
            assert result["schema_valid"] is True
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_valid_task_passes_schema(self) -> None:
        """A well-formed task passes schema validation."""
        path = _write_temp(TASK_MD)
        try:
            result = validate_file(path, schema="task")
            assert result["schema_valid"] is True
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_valid_story_passes_schema(self) -> None:
        """A well-formed story passes schema validation."""
        path = _write_temp(STORY_MD)
        try:
            result = validate_file(path, schema="story")
            assert result["schema_valid"] is True
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_valid_bug_passes_schema(self) -> None:
        """A well-formed bug passes schema validation."""
        path = _write_temp(BUG_MD)
        try:
            result = validate_file(path, schema="bug")
            assert result["schema_valid"] is True
        finally:
            os.unlink(path)

    @pytest.mark.negative
    def test_malformed_enabler_fails_schema(self) -> None:
        """An enabler missing required fields fails schema validation."""
        path = _write_temp(MALFORMED_ENABLER_MD)
        try:
            result = validate_file(path, schema="enabler")
            assert result["schema_valid"] is False
            # Should have violations for missing fields
            assert len(result.get("schema_violations", [])) > 0
        finally:
            os.unlink(path)

    @pytest.mark.negative
    def test_invalid_status_value_fails_schema(self) -> None:
        """A task with invalid status 'done' (not 'completed') fails schema validation."""
        path = _write_temp(INVALID_STATUS_MD)
        try:
            result = validate_file(path, schema="task")
            assert result["schema_valid"] is False
            # Should report status value violation
            violations = result.get("schema_violations", [])
            status_violations = [v for v in violations if "Status" in v.get("field_path", "")]
            assert len(status_violations) > 0
        finally:
            os.unlink(path)

    @pytest.mark.negative
    def test_unknown_schema_raises_value_error(self) -> None:
        """Passing an unknown schema name raises ValueError."""
        path = _write_temp(TASK_MD)
        try:
            with pytest.raises(ValueError, match="Unknown entity type"):
                validate_file(path, schema="nonexistent_type")
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_no_schema_still_works(self) -> None:
        """validate_file without schema still returns schema_valid True (backward compat)."""
        path = _write_temp(TASK_MD)
        try:
            result = validate_file(path)
            assert result["schema_valid"] is True
            assert result["schema"] is None
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_validate_result_includes_violation_details(self) -> None:
        """Schema validation errors include field_path, expected, actual, and message."""
        path = _write_temp(MALFORMED_ENABLER_MD)
        try:
            result = validate_file(path, schema="enabler")
            violations = result.get("schema_violations", [])
            assert len(violations) > 0
            first_violation = violations[0]
            assert "field_path" in first_violation
            assert "expected" in first_violation
            assert "actual" in first_violation
            assert "message" in first_violation
        finally:
            os.unlink(path)


# ---------------------------------------------------------------------------
# Tests: Entity type detection from file path
# ---------------------------------------------------------------------------


class TestEntityTypeDetection:
    """Tests that entity type can be detected from file path prefixes."""

    @pytest.mark.happy_path
    @pytest.mark.parametrize(
        "filename, expected_type",
        [
            ("EPIC-001-oss-release.md", "epic"),
            ("FEAT-001-fix-ci.md", "feature"),
            ("ST-007-worktracker-migration.md", "story"),
            ("EN-001-fix-plugin-validation.md", "enabler"),
            ("TASK-001-add-keywords.md", "task"),
            ("BUG-004-plugin-uninstall.md", "bug"),
        ],
    )
    def test_detect_entity_type_from_filename(self, filename: str, expected_type: str) -> None:
        """detect_entity_type correctly maps filename prefix to entity type."""
        assert detect_entity_type(filename) == expected_type

    @pytest.mark.happy_path
    def test_detect_entity_type_from_full_path(self) -> None:
        """detect_entity_type works with full file paths, not just basenames."""
        path = "projects/PROJ-001/work/EPIC-001/EN-001-fix/EN-001-fix.md"
        assert detect_entity_type(path) == "enabler"

    @pytest.mark.negative
    def test_detect_entity_type_unknown_prefix(self) -> None:
        """detect_entity_type returns None for unknown prefixes."""
        assert detect_entity_type("README.md") is None
        assert detect_entity_type("WORKTRACKER.md") is None
        assert detect_entity_type("DEC-001-decision.md") is None

    @pytest.mark.happy_path
    def test_detected_type_resolves_to_schema(self) -> None:
        """Detected entity type can be used with get_entity_schema."""
        for filename, expected_type in [
            ("EPIC-001.md", "epic"),
            ("FEAT-001.md", "feature"),
            ("EN-001.md", "enabler"),
            ("TASK-001.md", "task"),
            ("BUG-001.md", "bug"),
            ("ST-001.md", "story"),
        ]:
            entity_type = detect_entity_type(filename)
            assert entity_type is not None
            schema = get_entity_schema(entity_type)
            assert schema.entity_type == expected_type


# ---------------------------------------------------------------------------
# Tests: Domain layer schema validation directly (validate_document)
# ---------------------------------------------------------------------------


class TestDomainSchemaValidation:
    """Tests that validate_document from the domain layer correctly validates entity docs."""

    @pytest.mark.happy_path
    def test_validate_document_valid_epic(self) -> None:
        """validate_document returns is_valid=True for a conforming epic."""
        doc = JerryDocument.parse(EPIC_MD)
        schema = get_entity_schema("epic")
        report = validate_document(doc, schema)
        assert report.is_valid is True
        assert report.entity_type == "epic"

    @pytest.mark.happy_path
    def test_validate_document_valid_task(self) -> None:
        """validate_document returns is_valid=True for a conforming task."""
        doc = JerryDocument.parse(TASK_MD)
        schema = get_entity_schema("task")
        report = validate_document(doc, schema)
        assert report.is_valid is True
        assert report.entity_type == "task"

    @pytest.mark.negative
    def test_validate_document_missing_fields(self) -> None:
        """validate_document detects missing required frontmatter fields."""
        doc = JerryDocument.parse(MALFORMED_ENABLER_MD)
        schema = get_entity_schema("enabler")
        report = validate_document(doc, schema)
        assert report.is_valid is False
        # Should detect missing Priority, Impact, Enabler Type, Created, Parent
        missing_fields = {v.field_path for v in report.violations if "missing" in v.actual}
        assert "frontmatter.Priority" in missing_fields
        assert "frontmatter.Impact" in missing_fields
        assert "frontmatter.Enabler Type" in missing_fields
        assert "frontmatter.Created" in missing_fields
        assert "frontmatter.Parent" in missing_fields

    @pytest.mark.negative
    def test_validate_document_invalid_status(self) -> None:
        """validate_document detects invalid status value."""
        doc = JerryDocument.parse(INVALID_STATUS_MD)
        schema = get_entity_schema("task")
        report = validate_document(doc, schema)
        assert report.is_valid is False
        status_violations = [v for v in report.violations if v.field_path == "frontmatter.Status"]
        assert len(status_violations) > 0
        assert "done" in status_violations[0].actual

    @pytest.mark.happy_path
    def test_validate_document_field_count(self) -> None:
        """validate_document reports correct field_count."""
        doc = JerryDocument.parse(ENABLER_MD)
        schema = get_entity_schema("enabler")
        report = validate_document(doc, schema)
        # ENABLER_MD has: Type, Status, Priority, Impact, Enabler Type,
        #                 Created, Due, Completed, Parent, Owner, Effort = 11
        assert report.field_count >= 10

    @pytest.mark.happy_path
    def test_validate_document_section_count(self) -> None:
        """validate_document reports section count from the document."""
        doc = JerryDocument.parse(ENABLER_MD)
        schema = get_entity_schema("enabler")
        report = validate_document(doc, schema)
        # ENABLER_MD has: Document Sections, Summary, Acceptance Criteria,
        #                 Technical Approach = 4
        assert report.section_count >= 3


# ---------------------------------------------------------------------------
# Tests: parse_file for entity structure analysis (wt-visualizer use case)
# ---------------------------------------------------------------------------


class TestParseFileEntityStructure:
    """Tests that parse_file returns useful structural info for entity files."""

    @pytest.mark.happy_path
    def test_parse_entity_detects_frontmatter(self) -> None:
        """parse_file correctly detects frontmatter in entity files."""
        path = _write_temp(EPIC_MD)
        try:
            info = parse_file(path)
            assert info["has_frontmatter"] is True
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_parse_entity_counts_headings(self) -> None:
        """parse_file counts headings in entity files for hierarchy analysis."""
        path = _write_temp(FEATURE_MD)
        try:
            info = parse_file(path)
            # FEATURE_MD has: h1 + Document Sections + Summary + AC +
            #                 Children Stories/Enablers + Progress Summary = 6
            assert info["heading_count"] >= 5
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_parse_entity_returns_node_types(self) -> None:
        """parse_file returns AST node types useful for structural analysis."""
        path = _write_temp(ENABLER_MD)
        try:
            info = parse_file(path)
            assert "heading" in info["node_types"]
        finally:
            os.unlink(path)
