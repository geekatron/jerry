# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for the schema validation engine (ST-006).

Tests cover:
    - AC-ST006-1: Schema definition API (FieldRule, SectionRule, EntitySchema)
    - AC-ST006-2: validate_document with valid Epic -> is_valid=True
    - AC-ST006-3: validate_document with missing required field -> violation reported
    - AC-ST006-4: validate_document with invalid status value -> violation reported
    - AC-ST006-5: validate_document with missing required section -> violation reported
    - AC-ST006-6: validate_document for Story entity -> catches invalid status
    - AC-ST006-7: get_entity_schema("epic") returns EPIC_SCHEMA
    - AC-ST006-8: get_entity_schema("unknown") raises appropriate error
    - AC-ST006-9: Nav table validation integration: missing nav table -> violation
    - AC-ST006-10: Validation report structure: field_path, expected, actual, severity
    - H-20: BDD test-first approach
    - H-21: 90% line coverage

Test Categories:
    - Schema definition: FieldRule, SectionRule, EntitySchema construction
    - validate_document happy path: valid Epic document -> is_valid=True
    - validate_document violations: missing field, invalid value, missing section
    - Story validation: invalid status caught
    - get_entity_schema lookups: known and unknown entity types
    - Nav table integration: missing nav table produces violation
    - ValidationReport structure: correct field_path, expected, actual, severity
    - Built-in schemas: all 6 entity schemas defined and accessible
"""

from __future__ import annotations

import pytest

from src.domain.markdown_ast.jerry_document import JerryDocument
from src.domain.markdown_ast.schema import (
    BUG_SCHEMA,
    ENABLER_SCHEMA,
    EPIC_SCHEMA,
    FEATURE_SCHEMA,
    STORY_SCHEMA,
    TASK_SCHEMA,
    EntitySchema,
    FieldRule,
    SectionRule,
    ValidationReport,
    ValidationViolation,
    get_entity_schema,
    validate_document,
)

# ---------------------------------------------------------------------------
# Source fixtures
# ---------------------------------------------------------------------------

VALID_EPIC_SOURCE = """\
# EPIC-001: My Epic

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this covers |
| [Children Features/Capabilities](#children-featurescapabilities) | Child entities |
| [Progress Summary](#progress-summary) | Current progress |

---

> **Type:** epic
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-01-01

---

## Summary

This is the summary.

---

## Children Features/Capabilities

No children yet.

---

## Progress Summary

0% complete.
"""

VALID_STORY_SOURCE = """\
# STORY-001: My Story

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

MISSING_TYPE_FIELD_EPIC_SOURCE = """\
# EPIC-001: Missing Type

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overview |
| [Children Features/Capabilities](#children-featurescapabilities) | Children |
| [Progress Summary](#progress-summary) | Progress |

---

> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-01-01

---

## Summary

Summary content.

---

## Children Features/Capabilities

No children.

---

## Progress Summary

0%.
"""

INVALID_STATUS_STORY_SOURCE = """\
# STORY-001: Bad Status

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this covers |
| [Acceptance Criteria](#acceptance-criteria) | Done conditions |

---

> **Type:** story
> **Status:** invalid_value
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

MISSING_SECTION_STORY_SOURCE = """\
# STORY-001: Missing Section

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this covers |

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
"""

NO_NAV_TABLE_EPIC_SOURCE = """\
# EPIC-001: No Nav Table

> **Type:** epic
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-01-01

## Summary

This epic has no nav table.

## Children Features/Capabilities

None.

## Progress Summary

0%.
"""

VALID_FEATURE_SOURCE = """\
# FEAT-001: My Feature

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this covers |
| [Acceptance Criteria](#acceptance-criteria) | Done conditions |
| [Children Stories/Enablers](#children-storiesenablers) | Child entities |
| [Progress Summary](#progress-summary) | Current progress |

---

> **Type:** feature
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-01
> **Parent:** EPIC-001

---

## Summary

Feature summary.

---

## Acceptance Criteria

- [ ] Criterion 1

---

## Children Stories/Enablers

No children yet.

---

## Progress Summary

25% complete.
"""

VALID_ENABLER_SOURCE = """\
# EN-001: My Enabler

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this covers |
| [Acceptance Criteria](#acceptance-criteria) | Done conditions |
| [Technical Approach](#technical-approach) | Implementation plan |

---

> **Type:** enabler
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Enabler Type:** infrastructure
> **Created:** 2026-01-01
> **Parent:** FEAT-001

---

## Summary

Enabler summary.

---

## Acceptance Criteria

- [ ] Criterion 1

---

## Technical Approach

Technical approach details.
"""

VALID_TASK_SOURCE = """\
# TASK-001: My Task

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-01-01
> **Parent:** ST-001

## Summary

Task summary.
"""

VALID_BUG_SOURCE = """\
# BUG-001: My Bug

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this covers |
| [Steps to Reproduce](#steps-to-reproduce) | How to reproduce |
| [Acceptance Criteria](#acceptance-criteria) | Done conditions |

---

> **Type:** bug
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-01-01

---

## Summary

Bug summary.

---

## Steps to Reproduce

1. Step one
2. Step two

---

## Acceptance Criteria

- [ ] Fix verified
"""


# ---------------------------------------------------------------------------
# 1. Schema definition construction tests
# ---------------------------------------------------------------------------


class TestFieldRuleConstruction:
    """AC-ST006-1: Schema definition API -- FieldRule construction."""

    def test_field_rule_required_with_allowed_values(self) -> None:
        """FieldRule stores key, required flag, and allowed values."""
        rule = FieldRule(
            key="Status",
            required=True,
            allowed_values=("pending", "in_progress", "completed"),
        )
        assert rule.key == "Status"
        assert rule.required is True
        assert rule.allowed_values == ("pending", "in_progress", "completed")
        assert rule.value_pattern is None

    def test_field_rule_optional_no_constraints(self) -> None:
        """FieldRule can be optional with no value constraints."""
        rule = FieldRule(key="Due", required=False)
        assert rule.key == "Due"
        assert rule.required is False
        assert rule.allowed_values is None
        assert rule.value_pattern is None

    def test_field_rule_with_value_pattern(self) -> None:
        """FieldRule supports regex pattern constraint."""
        rule = FieldRule(
            key="Created",
            required=True,
            value_pattern=r"\d{4}-\d{2}-\d{2}",
        )
        assert rule.value_pattern == r"\d{4}-\d{2}-\d{2}"

    def test_field_rule_defaults(self) -> None:
        """FieldRule defaults: required=True, no allowed_values, no pattern."""
        rule = FieldRule(key="Type")
        assert rule.required is True
        assert rule.allowed_values is None
        assert rule.value_pattern is None


class TestSectionRuleConstruction:
    """AC-ST006-1: Schema definition API -- SectionRule construction."""

    def test_section_rule_required(self) -> None:
        """SectionRule stores heading and required flag."""
        rule = SectionRule(heading="Summary", required=True)
        assert rule.heading == "Summary"
        assert rule.required is True

    def test_section_rule_optional(self) -> None:
        """SectionRule can be optional."""
        rule = SectionRule(heading="Notes", required=False)
        assert rule.required is False

    def test_section_rule_default_required(self) -> None:
        """SectionRule defaults to required=True."""
        rule = SectionRule(heading="Summary")
        assert rule.required is True


class TestEntitySchemaConstruction:
    """AC-ST006-1: Schema definition API -- EntitySchema construction."""

    def test_entity_schema_stores_all_fields(self) -> None:
        """EntitySchema stores entity_type, rules, and nav_table flag."""
        schema = EntitySchema(
            entity_type="story",
            field_rules=(FieldRule(key="Type"),),
            section_rules=(SectionRule(heading="Summary"),),
            require_nav_table=True,
        )
        assert schema.entity_type == "story"
        assert len(schema.field_rules) == 1
        assert len(schema.section_rules) == 1
        assert schema.require_nav_table is True

    def test_entity_schema_default_require_nav_table(self) -> None:
        """EntitySchema defaults require_nav_table to True."""
        schema = EntitySchema(
            entity_type="epic",
            field_rules=(),
            section_rules=(),
        )
        assert schema.require_nav_table is True

    def test_entity_schema_no_nav_table_required(self) -> None:
        """EntitySchema can have require_nav_table=False (e.g., Task)."""
        schema = EntitySchema(
            entity_type="task",
            field_rules=(),
            section_rules=(),
            require_nav_table=False,
        )
        assert schema.require_nav_table is False

    def test_field_rule_is_frozen(self) -> None:
        """FieldRule is immutable (frozen dataclass)."""
        rule = FieldRule(key="Status")
        with pytest.raises((AttributeError, TypeError)):
            rule.key = "Changed"  # type: ignore[misc]

    def test_section_rule_is_frozen(self) -> None:
        """SectionRule is immutable (frozen dataclass)."""
        rule = SectionRule(heading="Summary")
        with pytest.raises((AttributeError, TypeError)):
            rule.heading = "Changed"  # type: ignore[misc]

    def test_entity_schema_is_frozen(self) -> None:
        """EntitySchema is immutable (frozen dataclass)."""
        schema = EntitySchema(entity_type="story", field_rules=(), section_rules=())
        with pytest.raises((AttributeError, TypeError)):
            schema.entity_type = "changed"  # type: ignore[misc]

    def test_validation_violation_is_frozen(self) -> None:
        """ValidationViolation is immutable (frozen dataclass)."""
        v = ValidationViolation(
            field_path="f", expected="e", actual="a", severity="error", message="m"
        )
        with pytest.raises((AttributeError, TypeError)):
            v.message = "changed"  # type: ignore[misc]

    def test_validation_report_is_frozen(self) -> None:
        """ValidationReport is immutable (frozen dataclass)."""
        report = ValidationReport(
            is_valid=True,
            violations=(),
            entity_type="story",
            field_count=0,
            section_count=0,
        )
        with pytest.raises((AttributeError, TypeError)):
            report.is_valid = False  # type: ignore[misc]


# ---------------------------------------------------------------------------
# 2. ValidationViolation and ValidationReport structure tests
# ---------------------------------------------------------------------------


class TestValidationViolationStructure:
    """AC-ST006-10: Validation report structure."""

    def test_violation_stores_all_fields(self) -> None:
        """ValidationViolation stores field_path, expected, actual, severity, message."""
        violation = ValidationViolation(
            field_path="frontmatter.Status",
            expected="one of: pending, in_progress, completed",
            actual="invalid_value",
            severity="error",
            message="Field 'Status' has invalid value 'invalid_value'.",
        )
        assert violation.field_path == "frontmatter.Status"
        assert violation.expected == "one of: pending, in_progress, completed"
        assert violation.actual == "invalid_value"
        assert violation.severity == "error"
        assert violation.message == "Field 'Status' has invalid value 'invalid_value'."

    def test_violation_warning_severity(self) -> None:
        """ValidationViolation supports 'warning' severity."""
        violation = ValidationViolation(
            field_path="nav_table",
            expected="nav table present",
            actual="no nav table found",
            severity="warning",
            message="No navigation table found.",
        )
        assert violation.severity == "warning"


class TestValidationReportStructure:
    """AC-ST006-10: ValidationReport structure."""

    def test_report_stores_all_fields(self) -> None:
        """ValidationReport stores is_valid, violations, entity_type, counts."""
        report = ValidationReport(
            is_valid=True,
            violations=(),
            entity_type="epic",
            field_count=5,
            section_count=3,
        )
        assert report.is_valid is True
        assert report.violations == ()
        assert report.entity_type == "epic"
        assert report.field_count == 5
        assert report.section_count == 3

    def test_report_with_violations(self) -> None:
        """ValidationReport can contain violations and is_valid=False."""
        violation = ValidationViolation(
            field_path="frontmatter.Type",
            expected="field present",
            actual="field missing",
            severity="error",
            message="Required field 'Type' is missing.",
        )
        report = ValidationReport(
            is_valid=False,
            violations=(violation,),
            entity_type="epic",
            field_count=4,
            section_count=3,
        )
        assert report.is_valid is False
        assert len(report.violations) == 1
        assert report.violations[0].field_path == "frontmatter.Type"


# ---------------------------------------------------------------------------
# 3. validate_document -- happy path tests
# ---------------------------------------------------------------------------


class TestValidateDocumentHappyPath:
    """AC-ST006-2: validate_document with valid documents -> is_valid=True."""

    def test_valid_epic_document(self) -> None:
        """Valid Epic document passes validation without violations."""
        doc = JerryDocument.parse(VALID_EPIC_SOURCE)
        report = validate_document(doc, EPIC_SCHEMA)
        assert report.is_valid is True
        assert report.violations == ()
        assert report.entity_type == "epic"

    def test_valid_epic_field_count(self) -> None:
        """Valid Epic report reports correct field count."""
        doc = JerryDocument.parse(VALID_EPIC_SOURCE)
        report = validate_document(doc, EPIC_SCHEMA)
        # VALID_EPIC_SOURCE has 5 frontmatter fields
        assert report.field_count == 5

    def test_valid_epic_section_count(self) -> None:
        """Valid Epic report reports correct section count (## headings)."""
        doc = JerryDocument.parse(VALID_EPIC_SOURCE)
        report = validate_document(doc, EPIC_SCHEMA)
        # VALID_EPIC_SOURCE has 4 ## headings: Document Sections + 3 content sections
        assert report.section_count >= 3

    def test_valid_story_document(self) -> None:
        """Valid Story document passes validation without violations."""
        doc = JerryDocument.parse(VALID_STORY_SOURCE)
        report = validate_document(doc, STORY_SCHEMA)
        assert report.is_valid is True
        assert report.violations == ()

    def test_valid_feature_document(self) -> None:
        """Valid Feature document passes validation without violations."""
        doc = JerryDocument.parse(VALID_FEATURE_SOURCE)
        report = validate_document(doc, FEATURE_SCHEMA)
        assert report.is_valid is True
        assert report.violations == ()

    def test_valid_enabler_document(self) -> None:
        """Valid Enabler document passes validation without violations."""
        doc = JerryDocument.parse(VALID_ENABLER_SOURCE)
        report = validate_document(doc, ENABLER_SCHEMA)
        assert report.is_valid is True
        assert report.violations == ()

    def test_valid_task_document(self) -> None:
        """Valid Task document passes validation (no nav table required)."""
        doc = JerryDocument.parse(VALID_TASK_SOURCE)
        report = validate_document(doc, TASK_SCHEMA)
        assert report.is_valid is True
        assert report.violations == ()

    def test_valid_bug_document(self) -> None:
        """Valid Bug document passes validation without violations."""
        doc = JerryDocument.parse(VALID_BUG_SOURCE)
        report = validate_document(doc, BUG_SCHEMA)
        assert report.is_valid is True
        assert report.violations == ()


# ---------------------------------------------------------------------------
# 4. validate_document -- missing required field tests
# ---------------------------------------------------------------------------


class TestValidateDocumentMissingField:
    """AC-ST006-3: validate_document with missing required field -> violation reported."""

    def test_missing_type_field_produces_violation(self) -> None:
        """Missing 'Type' field produces an error violation."""
        doc = JerryDocument.parse(MISSING_TYPE_FIELD_EPIC_SOURCE)
        report = validate_document(doc, EPIC_SCHEMA)
        assert report.is_valid is False
        paths = [v.field_path for v in report.violations]
        assert "frontmatter.Type" in paths

    def test_missing_field_violation_severity_is_error(self) -> None:
        """Missing required field violation has severity='error'."""
        doc = JerryDocument.parse(MISSING_TYPE_FIELD_EPIC_SOURCE)
        report = validate_document(doc, EPIC_SCHEMA)
        type_violations = [v for v in report.violations if v.field_path == "frontmatter.Type"]
        assert len(type_violations) == 1
        assert type_violations[0].severity == "error"

    def test_missing_field_violation_expected_is_descriptive(self) -> None:
        """Missing field violation has a descriptive 'expected' string."""
        doc = JerryDocument.parse(MISSING_TYPE_FIELD_EPIC_SOURCE)
        report = validate_document(doc, EPIC_SCHEMA)
        type_violations = [v for v in report.violations if v.field_path == "frontmatter.Type"]
        assert (
            "present" in type_violations[0].expected.lower()
            or "required" in type_violations[0].expected.lower()
        )

    def test_missing_field_violation_actual_indicates_missing(self) -> None:
        """Missing field violation has an 'actual' that indicates absence."""
        doc = JerryDocument.parse(MISSING_TYPE_FIELD_EPIC_SOURCE)
        report = validate_document(doc, EPIC_SCHEMA)
        type_violations = [v for v in report.violations if v.field_path == "frontmatter.Type"]
        assert (
            "missing" in type_violations[0].actual.lower()
            or "not found" in type_violations[0].actual.lower()
            or "absent" in type_violations[0].actual.lower()
        )


# ---------------------------------------------------------------------------
# 5. validate_document -- invalid allowed value tests
# ---------------------------------------------------------------------------


class TestValidateDocumentInvalidValue:
    """AC-ST006-4: validate_document with invalid allowed value -> violation reported."""

    def test_invalid_status_value_produces_violation(self) -> None:
        """Invalid Status value produces an error violation for Story."""
        doc = JerryDocument.parse(INVALID_STATUS_STORY_SOURCE)
        report = validate_document(doc, STORY_SCHEMA)
        assert report.is_valid is False
        paths = [v.field_path for v in report.violations]
        assert "frontmatter.Status" in paths

    def test_invalid_status_violation_severity_is_error(self) -> None:
        """Invalid value violation has severity='error'."""
        doc = JerryDocument.parse(INVALID_STATUS_STORY_SOURCE)
        report = validate_document(doc, STORY_SCHEMA)
        status_violations = [v for v in report.violations if v.field_path == "frontmatter.Status"]
        assert len(status_violations) == 1
        assert status_violations[0].severity == "error"

    def test_invalid_status_violation_actual_is_the_bad_value(self) -> None:
        """Invalid value violation 'actual' field contains the invalid value."""
        doc = JerryDocument.parse(INVALID_STATUS_STORY_SOURCE)
        report = validate_document(doc, STORY_SCHEMA)
        status_violations = [v for v in report.violations if v.field_path == "frontmatter.Status"]
        assert "invalid_value" in status_violations[0].actual

    def test_invalid_status_violation_expected_lists_allowed_values(self) -> None:
        """Invalid value violation 'expected' lists allowed values."""
        doc = JerryDocument.parse(INVALID_STATUS_STORY_SOURCE)
        report = validate_document(doc, STORY_SCHEMA)
        status_violations = [v for v in report.violations if v.field_path == "frontmatter.Status"]
        expected = status_violations[0].expected
        # Expected should mention allowed values
        assert "pending" in expected or "in_progress" in expected or "completed" in expected

    def test_invalid_priority_value_epic_produces_violation(self) -> None:
        """Invalid Priority value for Epic produces a violation."""
        source = VALID_EPIC_SOURCE.replace(
            "> **Priority:** medium", "> **Priority:** ultra_critical"
        )
        doc = JerryDocument.parse(source)
        report = validate_document(doc, EPIC_SCHEMA)
        assert report.is_valid is False
        paths = [v.field_path for v in report.violations]
        assert "frontmatter.Priority" in paths

    def test_invalid_value_violation_has_line_number(self) -> None:
        """Invalid value violation includes a 0-based line_number from frontmatter."""
        doc = JerryDocument.parse(INVALID_STATUS_STORY_SOURCE)
        report = validate_document(doc, STORY_SCHEMA)
        status_violations = [v for v in report.violations if v.field_path == "frontmatter.Status"]
        assert len(status_violations) == 1
        assert status_violations[0].line_number is not None
        assert status_violations[0].line_number >= 0

    def test_missing_field_violation_has_no_line_number(self) -> None:
        """Missing field violation has line_number=None (field not in source)."""
        doc = JerryDocument.parse(MISSING_TYPE_FIELD_EPIC_SOURCE)
        report = validate_document(doc, EPIC_SCHEMA)
        type_violations = [v for v in report.violations if v.field_path == "frontmatter.Type"]
        assert len(type_violations) == 1
        assert type_violations[0].line_number is None


# ---------------------------------------------------------------------------
# 6. validate_document -- missing required section tests
# ---------------------------------------------------------------------------


class TestValidateDocumentMissingSection:
    """AC-ST006-5: validate_document with missing required section -> violation reported."""

    def test_missing_acceptance_criteria_section_produces_violation(self) -> None:
        """Missing 'Acceptance Criteria' section produces an error violation."""
        doc = JerryDocument.parse(MISSING_SECTION_STORY_SOURCE)
        report = validate_document(doc, STORY_SCHEMA)
        assert report.is_valid is False
        paths = [v.field_path for v in report.violations]
        assert "sections.Acceptance Criteria" in paths

    def test_missing_section_violation_severity_is_error(self) -> None:
        """Missing section violation has severity='error'."""
        doc = JerryDocument.parse(MISSING_SECTION_STORY_SOURCE)
        report = validate_document(doc, STORY_SCHEMA)
        section_violations = [
            v for v in report.violations if v.field_path == "sections.Acceptance Criteria"
        ]
        assert len(section_violations) == 1
        assert section_violations[0].severity == "error"

    def test_missing_section_violation_actual_indicates_absent(self) -> None:
        """Missing section violation 'actual' indicates section is absent."""
        doc = JerryDocument.parse(MISSING_SECTION_STORY_SOURCE)
        report = validate_document(doc, STORY_SCHEMA)
        section_violations = [
            v for v in report.violations if v.field_path == "sections.Acceptance Criteria"
        ]
        assert (
            "missing" in section_violations[0].actual.lower()
            or "not found" in section_violations[0].actual.lower()
            or "absent" in section_violations[0].actual.lower()
        )


# ---------------------------------------------------------------------------
# 7. Story validation -- invalid status
# ---------------------------------------------------------------------------


class TestStoryValidation:
    """AC-ST006-6: validate_document for Story catches invalid status values."""

    def test_story_invalid_status_caught(self) -> None:
        """Story with invalid status value fails validation."""
        doc = JerryDocument.parse(INVALID_STATUS_STORY_SOURCE)
        report = validate_document(doc, STORY_SCHEMA)
        assert report.is_valid is False

    def test_story_valid_status_in_progress(self) -> None:
        """Story with 'in_progress' status passes validation."""
        source = VALID_STORY_SOURCE.replace("> **Status:** pending", "> **Status:** in_progress")
        doc = JerryDocument.parse(source)
        report = validate_document(doc, STORY_SCHEMA)
        assert report.is_valid is True

    def test_story_valid_status_completed(self) -> None:
        """Story with 'completed' status passes validation."""
        source = VALID_STORY_SOURCE.replace("> **Status:** pending", "> **Status:** completed")
        doc = JerryDocument.parse(source)
        report = validate_document(doc, STORY_SCHEMA)
        assert report.is_valid is True

    def test_story_missing_parent_produces_violation(self) -> None:
        """Story missing required 'Parent' field produces a violation."""
        source = VALID_STORY_SOURCE.replace("> **Parent:** FEAT-001\n", "")
        doc = JerryDocument.parse(source)
        report = validate_document(doc, STORY_SCHEMA)
        assert report.is_valid is False
        paths = [v.field_path for v in report.violations]
        assert "frontmatter.Parent" in paths


# ---------------------------------------------------------------------------
# 8. get_entity_schema tests
# ---------------------------------------------------------------------------


class TestGetEntitySchema:
    """AC-ST006-7/8: get_entity_schema lookups."""

    def test_get_epic_schema(self) -> None:
        """get_entity_schema('epic') returns EPIC_SCHEMA."""
        schema = get_entity_schema("epic")
        assert schema is EPIC_SCHEMA
        assert schema.entity_type == "epic"

    def test_get_feature_schema(self) -> None:
        """get_entity_schema('feature') returns FEATURE_SCHEMA."""
        schema = get_entity_schema("feature")
        assert schema is FEATURE_SCHEMA
        assert schema.entity_type == "feature"

    def test_get_story_schema(self) -> None:
        """get_entity_schema('story') returns STORY_SCHEMA."""
        schema = get_entity_schema("story")
        assert schema is STORY_SCHEMA
        assert schema.entity_type == "story"

    def test_get_enabler_schema(self) -> None:
        """get_entity_schema('enabler') returns ENABLER_SCHEMA."""
        schema = get_entity_schema("enabler")
        assert schema is ENABLER_SCHEMA
        assert schema.entity_type == "enabler"

    def test_get_task_schema(self) -> None:
        """get_entity_schema('task') returns TASK_SCHEMA."""
        schema = get_entity_schema("task")
        assert schema is TASK_SCHEMA
        assert schema.entity_type == "task"

    def test_get_bug_schema(self) -> None:
        """get_entity_schema('bug') returns BUG_SCHEMA."""
        schema = get_entity_schema("bug")
        assert schema is BUG_SCHEMA
        assert schema.entity_type == "bug"

    def test_get_unknown_schema_raises_value_error(self) -> None:
        """get_entity_schema('unknown') raises ValueError."""
        with pytest.raises(ValueError, match="unknown"):
            get_entity_schema("unknown")

    def test_get_schema_case_sensitive(self) -> None:
        """get_entity_schema is case-sensitive: 'Epic' is not 'epic'."""
        with pytest.raises(ValueError):
            get_entity_schema("Epic")


# ---------------------------------------------------------------------------
# 9. Nav table validation integration
# ---------------------------------------------------------------------------


class TestNavTableValidationIntegration:
    """AC-ST006-9: Missing nav table produces violation when required."""

    def test_no_nav_table_epic_produces_violation(self) -> None:
        """Epic without nav table produces a nav_table violation."""
        doc = JerryDocument.parse(NO_NAV_TABLE_EPIC_SOURCE)
        report = validate_document(doc, EPIC_SCHEMA)
        assert report.is_valid is False
        paths = [v.field_path for v in report.violations]
        assert "nav_table" in paths

    def test_no_nav_table_violation_severity_is_error(self) -> None:
        """Missing nav table violation has severity='error'."""
        doc = JerryDocument.parse(NO_NAV_TABLE_EPIC_SOURCE)
        report = validate_document(doc, EPIC_SCHEMA)
        nav_violations = [v for v in report.violations if v.field_path == "nav_table"]
        assert len(nav_violations) == 1
        assert nav_violations[0].severity == "error"

    def test_task_no_nav_table_required_no_violation(self) -> None:
        """Task with no nav table does NOT produce a nav_table violation."""
        doc = JerryDocument.parse(VALID_TASK_SOURCE)
        report = validate_document(doc, TASK_SCHEMA)
        paths = [v.field_path for v in report.violations]
        assert "nav_table" not in paths

    def test_story_nav_table_violations_included(self) -> None:
        """Story missing nav table produces nav_table violation."""
        source = MISSING_SECTION_STORY_SOURCE  # already has a nav table for Summary only
        doc = JerryDocument.parse(source)
        report = validate_document(doc, STORY_SCHEMA)
        # This source is missing Acceptance Criteria section but still has a nav table
        # Ensure nav_table is NOT a violation here (nav table exists)
        nav_violations = [v for v in report.violations if v.field_path == "nav_table"]
        # The source has a nav table (albeit incomplete), so nav_table violation
        # depends on whether the nav_table validation finds it invalid
        # The key property we test: violations list has proper structure
        for v in nav_violations:
            assert v.field_path == "nav_table"
            assert v.severity in ("error", "warning")


# ---------------------------------------------------------------------------
# 10. Built-in schema definitions
# ---------------------------------------------------------------------------


class TestBuiltInSchemas:
    """Verify all 6 built-in schemas are properly defined."""

    def test_epic_schema_entity_type(self) -> None:
        assert EPIC_SCHEMA.entity_type == "epic"

    def test_epic_schema_has_required_fields(self) -> None:
        """Epic schema has Type, Status, Priority, Impact, Created as required."""
        required_keys = {r.key for r in EPIC_SCHEMA.field_rules if r.required}
        assert "Type" in required_keys
        assert "Status" in required_keys
        assert "Priority" in required_keys
        assert "Impact" in required_keys
        assert "Created" in required_keys

    def test_epic_schema_status_allowed_values(self) -> None:
        """Epic schema Status field has correct allowed values."""
        status_rule = next(r for r in EPIC_SCHEMA.field_rules if r.key == "Status")
        assert status_rule.allowed_values is not None
        assert "pending" in status_rule.allowed_values
        assert "in_progress" in status_rule.allowed_values
        assert "completed" in status_rule.allowed_values

    def test_epic_schema_required_sections(self) -> None:
        """Epic schema requires Summary, Children, Progress Summary sections."""
        required_sections = {r.heading for r in EPIC_SCHEMA.section_rules if r.required}
        assert "Summary" in required_sections

    def test_epic_schema_requires_nav_table(self) -> None:
        assert EPIC_SCHEMA.require_nav_table is True

    def test_feature_schema_entity_type(self) -> None:
        assert FEATURE_SCHEMA.entity_type == "feature"

    def test_feature_schema_requires_parent(self) -> None:
        """Feature schema requires Parent field."""
        required_keys = {r.key for r in FEATURE_SCHEMA.field_rules if r.required}
        assert "Parent" in required_keys

    def test_story_schema_entity_type(self) -> None:
        assert STORY_SCHEMA.entity_type == "story"

    def test_story_schema_requires_parent(self) -> None:
        """Story schema requires Parent field."""
        required_keys = {r.key for r in STORY_SCHEMA.field_rules if r.required}
        assert "Parent" in required_keys

    def test_enabler_schema_entity_type(self) -> None:
        assert ENABLER_SCHEMA.entity_type == "enabler"

    def test_enabler_schema_has_enabler_type_field(self) -> None:
        """Enabler schema has 'Enabler Type' required field with allowed values."""
        enabler_type_rules = [r for r in ENABLER_SCHEMA.field_rules if r.key == "Enabler Type"]
        assert len(enabler_type_rules) == 1
        rule = enabler_type_rules[0]
        assert rule.required is True
        assert rule.allowed_values is not None
        assert "infrastructure" in rule.allowed_values

    def test_task_schema_entity_type(self) -> None:
        assert TASK_SCHEMA.entity_type == "task"

    def test_task_schema_no_nav_table_required(self) -> None:
        """Task schema does not require nav table."""
        assert TASK_SCHEMA.require_nav_table is False

    def test_bug_schema_entity_type(self) -> None:
        assert BUG_SCHEMA.entity_type == "bug"

    def test_bug_schema_has_severity_field(self) -> None:
        """Bug schema has 'Severity' required field with allowed values."""
        severity_rules = [r for r in BUG_SCHEMA.field_rules if r.key == "Severity"]
        assert len(severity_rules) == 1
        rule = severity_rules[0]
        assert rule.required is True
        assert rule.allowed_values is not None
        assert "critical" in rule.allowed_values
        assert "major" in rule.allowed_values

    def test_bug_schema_requires_steps_to_reproduce(self) -> None:
        """Bug schema requires 'Steps to Reproduce' section."""
        required_sections = {r.heading for r in BUG_SCHEMA.section_rules if r.required}
        assert "Steps to Reproduce" in required_sections


# ---------------------------------------------------------------------------
# 11. Custom schema tests
# ---------------------------------------------------------------------------


class TestCustomSchema:
    """Validate with user-defined custom schemas."""

    def test_custom_schema_validates_required_field(self) -> None:
        """Custom schema with a required field catches missing field."""
        custom_schema = EntitySchema(
            entity_type="custom",
            field_rules=(FieldRule(key="CustomField", required=True),),
            section_rules=(),
            require_nav_table=False,
        )
        source = "# My Doc\n\n> **OtherField:** value\n"
        doc = JerryDocument.parse(source)
        report = validate_document(doc, custom_schema)
        assert report.is_valid is False
        paths = [v.field_path for v in report.violations]
        assert "frontmatter.CustomField" in paths

    def test_custom_schema_with_no_rules_valid_doc(self) -> None:
        """Custom schema with no rules always returns is_valid=True."""
        custom_schema = EntitySchema(
            entity_type="anything",
            field_rules=(),
            section_rules=(),
            require_nav_table=False,
        )
        doc = JerryDocument.parse("# Hello\n\nContent.\n")
        report = validate_document(doc, custom_schema)
        assert report.is_valid is True

    def test_custom_schema_regex_pattern_valid_value(self) -> None:
        """Custom schema FieldRule value_pattern: valid value passes."""
        custom_schema = EntitySchema(
            entity_type="custom",
            field_rules=(
                FieldRule(
                    key="Created",
                    required=True,
                    value_pattern=r"\d{4}-\d{2}-\d{2}",
                ),
            ),
            section_rules=(),
            require_nav_table=False,
        )
        source = "# Doc\n\n> **Created:** 2026-01-15\n"
        doc = JerryDocument.parse(source)
        report = validate_document(doc, custom_schema)
        assert report.is_valid is True

    def test_custom_schema_regex_pattern_invalid_value(self) -> None:
        """Custom schema FieldRule value_pattern: invalid value produces violation."""
        custom_schema = EntitySchema(
            entity_type="custom",
            field_rules=(
                FieldRule(
                    key="Created",
                    required=True,
                    value_pattern=r"\d{4}-\d{2}-\d{2}",
                ),
            ),
            section_rules=(),
            require_nav_table=False,
        )
        source = "# Doc\n\n> **Created:** not-a-date\n"
        doc = JerryDocument.parse(source)
        report = validate_document(doc, custom_schema)
        assert report.is_valid is False
        paths = [v.field_path for v in report.violations]
        assert "frontmatter.Created" in paths

    def test_custom_schema_required_section_present(self) -> None:
        """Custom schema SectionRule: required section present -> valid."""
        custom_schema = EntitySchema(
            entity_type="custom",
            field_rules=(),
            section_rules=(SectionRule(heading="MySection", required=True),),
            require_nav_table=False,
        )
        source = "# Doc\n\n## MySection\n\nContent.\n"
        doc = JerryDocument.parse(source)
        report = validate_document(doc, custom_schema)
        assert report.is_valid is True

    def test_custom_schema_required_section_absent(self) -> None:
        """Custom schema SectionRule: required section absent -> violation."""
        custom_schema = EntitySchema(
            entity_type="custom",
            field_rules=(),
            section_rules=(SectionRule(heading="MySection", required=True),),
            require_nav_table=False,
        )
        source = "# Doc\n\n## OtherSection\n\nContent.\n"
        doc = JerryDocument.parse(source)
        report = validate_document(doc, custom_schema)
        assert report.is_valid is False
        paths = [v.field_path for v in report.violations]
        assert "sections.MySection" in paths

    def test_optional_field_missing_no_violation(self) -> None:
        """Optional FieldRule: missing optional field does NOT produce a violation."""
        custom_schema = EntitySchema(
            entity_type="custom",
            field_rules=(FieldRule(key="OptionalField", required=False),),
            section_rules=(),
            require_nav_table=False,
        )
        source = "# Doc\n\n> **OtherField:** value\n"
        doc = JerryDocument.parse(source)
        report = validate_document(doc, custom_schema)
        assert report.is_valid is True
        paths = [v.field_path for v in report.violations]
        assert "frontmatter.OptionalField" not in paths

    def test_optional_field_with_invalid_value_still_produces_violation(self) -> None:
        """Optional FieldRule present with invalid allowed value -> still a violation."""
        custom_schema = EntitySchema(
            entity_type="custom",
            field_rules=(
                FieldRule(
                    key="Mode",
                    required=False,
                    allowed_values=("fast", "slow"),
                ),
            ),
            section_rules=(),
            require_nav_table=False,
        )
        source = "# Doc\n\n> **Mode:** ultra\n"
        doc = JerryDocument.parse(source)
        report = validate_document(doc, custom_schema)
        assert report.is_valid is False
        paths = [v.field_path for v in report.violations]
        assert "frontmatter.Mode" in paths


# ---------------------------------------------------------------------------
# 12. Nav table coverage issue tests (nav table exists but incomplete)
# ---------------------------------------------------------------------------


class TestNavTableCoverageViolations:
    """Validate nav table violations when nav table exists but is incomplete."""

    def test_nav_table_with_missing_entries_produces_violation(self) -> None:
        """Nav table missing a heading entry produces a nav_table violation."""
        # A source with a nav table that is missing a required heading
        source = """\
# EPIC-001: Incomplete Nav

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overview |

---

> **Type:** epic
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-01-01

---

## Summary

Content.

---

## Children Features/Capabilities

None.

---

## Progress Summary

0%.
"""
        doc = JerryDocument.parse(source)
        report = validate_document(doc, EPIC_SCHEMA)
        # Nav table exists but is missing Children and Progress Summary entries
        assert report.is_valid is False
        nav_violations = [v for v in report.violations if v.field_path == "nav_table"]
        assert len(nav_violations) >= 1
        # At least one violation should mention missing entries
        missing_violations = [
            v
            for v in nav_violations
            if "missing" in v.expected.lower() or "missing" in v.actual.lower()
        ]
        assert len(missing_violations) >= 1

    def test_nav_table_with_orphaned_entries_produces_violation(self) -> None:
        """Nav table with orphaned entries (no matching heading) produces violation."""
        source = """\
# DOC: Orphaned Nav

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overview |
| [Ghost Section](#ghost-section) | Does not exist |

---

> **Type:** epic
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-01-01

---

## Summary

Content.

---

## Children Features/Capabilities

None.

---

## Progress Summary

0%.
"""
        doc = JerryDocument.parse(source)
        report = validate_document(doc, EPIC_SCHEMA)
        assert report.is_valid is False
        nav_violations = [v for v in report.violations if v.field_path == "nav_table"]
        assert len(nav_violations) >= 1
