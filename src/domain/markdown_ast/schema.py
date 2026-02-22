# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Schema validation engine for Jerry worktracker entity documents.

Provides a schema definition API and a validation engine that checks
JerryDocument instances against structural schemas.  Structural errors
(missing required frontmatter fields, invalid field values, missing required
sections, missing navigation tables) are reported as ValidationViolation
objects collected in a ValidationReport.

Built-in schemas cover the six WORKTRACKER entity types:
    - Epic, Feature, Story, Enabler, Task, Bug

Usage::

    from src.domain.markdown_ast.schema import (
        validate_document,
        get_entity_schema,
        EPIC_SCHEMA,
    )

    doc = JerryDocument.parse(source)
    report = validate_document(doc, EPIC_SCHEMA)
    if not report.is_valid:
        for v in report.violations:
            print(v.field_path, v.severity, v.message)

References:
    - ST-006: Schema Validation Engine
    - ST-002: BlockquoteFrontmatter Extension (dependency)
    - ST-008: Navigation Table Helpers (dependency)
    - H-07: Domain layer constraint -- no external infra/interface imports
    - H-23/H-24: Navigation table requirements

Exports:
    FieldRule: Rule for a single frontmatter field.
    SectionRule: Rule for a required ## heading section.
    EntitySchema: Schema definition for a Jerry worktracker entity type.
    ValidationViolation: A single schema violation found during validation.
    ValidationReport: Complete validation report for a document against a schema.
    validate_document: Validate a JerryDocument against an EntitySchema.
    get_entity_schema: Look up a built-in schema by entity type name.
    EPIC_SCHEMA: Built-in schema for Epic entities.
    FEATURE_SCHEMA: Built-in schema for Feature entities.
    STORY_SCHEMA: Built-in schema for Story entities.
    ENABLER_SCHEMA: Built-in schema for Enabler entities.
    TASK_SCHEMA: Built-in schema for Task entities.
    BUG_SCHEMA: Built-in schema for Bug entities.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from src.domain.markdown_ast.frontmatter import extract_frontmatter
from src.domain.markdown_ast.jerry_document import JerryDocument
from src.domain.markdown_ast.nav_table import validate_nav_table

# ---------------------------------------------------------------------------
# Schema definition dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FieldRule:
    """
    Rule for a single frontmatter field in a Jerry entity document.

    Defines whether the field is required and what values are acceptable.
    When ``allowed_values`` is set, the field value must be one of the listed
    strings.  When ``value_pattern`` is set, the field value must match the
    regex pattern.  Both constraints may be set simultaneously; both must pass.

    Attributes:
        key: The frontmatter field name (e.g., "Status", "Type").
        required: Whether the field must be present in the document.
        allowed_values: If set, the field value must be one of these strings.
        value_pattern: If set, the field value must match this regex pattern.

    Examples:
        >>> FieldRule(key="Status", required=True, allowed_values=("pending", "in_progress"))
        FieldRule(key='Status', required=True, allowed_values=('pending', 'in_progress'), value_pattern=None)
    """

    key: str
    required: bool = True
    allowed_values: tuple[str, ...] | None = None
    value_pattern: str | None = None


@dataclass(frozen=True)
class SectionRule:
    """
    Rule for a required ## heading section in a Jerry entity document.

    Attributes:
        heading: The expected heading text as it appears in the markdown source
            (e.g., "Summary", "Acceptance Criteria").
        required: Whether this section must be present in the document.

    Examples:
        >>> SectionRule(heading="Summary", required=True)
        SectionRule(heading='Summary', required=True)
    """

    heading: str
    required: bool = True


@dataclass(frozen=True)
class EntitySchema:
    """
    Schema definition for a Jerry worktracker entity type.

    Encapsulates all structural rules for a single entity type: which
    frontmatter fields are required and what values they accept, which
    ## sections must be present, and whether H-23 nav table compliance is
    enforced.

    Attributes:
        entity_type: The entity type identifier (e.g., "epic", "story").
        field_rules: Tuple of FieldRule instances to check against frontmatter.
        section_rules: Tuple of SectionRule instances for required ## sections.
        require_nav_table: When True, the document must have a valid H-23
            navigation table.  Defaults to True.

    Examples:
        >>> EntitySchema(
        ...     entity_type="story",
        ...     field_rules=(FieldRule(key="Type"),),
        ...     section_rules=(SectionRule(heading="Summary"),),
        ... )
    """

    entity_type: str
    field_rules: tuple[FieldRule, ...]
    section_rules: tuple[SectionRule, ...]
    require_nav_table: bool = True


@dataclass(frozen=True)
class ValidationViolation:
    """
    A single schema violation found during document validation.

    Attributes:
        field_path: Dotted path identifying what was checked, e.g.
            ``"frontmatter.Status"``, ``"sections.Summary"``, ``"nav_table"``.
        expected: Human-readable description of what was expected.
        actual: Human-readable description of what was actually found.
        severity: Either ``"error"`` (blocks validity) or ``"warning"``
            (informational).
        message: Full human-readable description of the violation.

    Examples:
        >>> ValidationViolation(
        ...     field_path="frontmatter.Status",
        ...     expected="one of: pending, in_progress, completed",
        ...     actual="invalid_value",
        ...     severity="error",
        ...     message="Field 'Status' value 'invalid_value' is not in allowed values.",
        ... )
    """

    field_path: str
    expected: str
    actual: str
    severity: str
    message: str
    line_number: int | None = None


@dataclass(frozen=True)
class ValidationReport:
    """
    Complete validation report produced by validating a document against a schema.

    Attributes:
        is_valid: True when all schema rules are satisfied (no error violations).
        violations: Tuple of ValidationViolation objects, one per detected issue.
        entity_type: The entity_type from the schema used for validation.
        field_count: Number of frontmatter fields found in the document.
        section_count: Number of ## headings found in the document.

    Examples:
        >>> report = validate_document(doc, EPIC_SCHEMA)
        >>> if not report.is_valid:
        ...     for v in report.violations:
        ...         print(v.field_path, v.message)
    """

    is_valid: bool
    violations: tuple[ValidationViolation, ...]
    entity_type: str
    field_count: int
    section_count: int


# ---------------------------------------------------------------------------
# Validation engine
# ---------------------------------------------------------------------------


def validate_document(doc: JerryDocument, schema: EntitySchema) -> ValidationReport:
    """
    Validate a JerryDocument against an EntitySchema.

    Checks the document for:
    1. **Frontmatter field rules**: required fields present, allowed values
       respected, value patterns matched.
    2. **Section rules**: required ## headings present.
    3. **Nav table compliance**: when ``schema.require_nav_table`` is True,
       the document must pass H-23/H-24 nav table validation.

    Args:
        doc: The JerryDocument to validate.
        schema: The EntitySchema defining the structural rules.

    Returns:
        A ValidationReport describing the outcome.  ``is_valid`` is True only
        when no ``"error"`` severity violations are present.

    Examples:
        >>> doc = JerryDocument.parse(source)
        >>> report = validate_document(doc, EPIC_SCHEMA)
        >>> report.is_valid
        True
    """
    violations: list[ValidationViolation] = []

    # ------------------------------------------------------------------
    # 1. Frontmatter field validation
    # ------------------------------------------------------------------
    frontmatter = extract_frontmatter(doc)
    field_count = len(frontmatter)

    for rule in schema.field_rules:
        present = rule.key in frontmatter

        if not present:
            if rule.required:
                violations.append(
                    ValidationViolation(
                        field_path=f"frontmatter.{rule.key}",
                        expected="field present (required)",
                        actual="field missing",
                        severity="error",
                        message=f"Required field '{rule.key}' is missing from frontmatter.",
                    )
                )
            # Optional field absent -> no violation; skip value checks
            continue

        fm_field = frontmatter.get_field(rule.key)
        value = fm_field.value if fm_field else ""
        field_line = fm_field.line_number if fm_field else None

        # Check allowed values
        if rule.allowed_values is not None and value not in rule.allowed_values:
            allowed_str = ", ".join(rule.allowed_values)
            violations.append(
                ValidationViolation(
                    field_path=f"frontmatter.{rule.key}",
                    expected=f"one of: {allowed_str}",
                    actual=value,
                    severity="error",
                    message=(
                        f"Field '{rule.key}' value '{value}' is not in allowed values: "
                        f"{allowed_str}."
                    ),
                    line_number=field_line,
                )
            )

        # Check value pattern (independent of allowed_values check)
        if rule.value_pattern is not None and not re.fullmatch(rule.value_pattern, value):
            violations.append(
                ValidationViolation(
                    field_path=f"frontmatter.{rule.key}",
                    expected=f"matches pattern: {rule.value_pattern}",
                    actual=value,
                    severity="error",
                    message=(
                        f"Field '{rule.key}' value '{value}' does not match "
                        f"required pattern '{rule.value_pattern}'."
                    ),
                    line_number=field_line,
                )
            )

    # ------------------------------------------------------------------
    # 2. Section validation -- collect ## heading texts from AST
    # ------------------------------------------------------------------
    h2_headings: set[str] = set()
    for node in doc.query("heading"):
        if node.tag != "h2":
            continue
        for child in node.children:
            if child.type == "inline":
                h2_headings.add(child.content)
                break

    section_count = len(h2_headings)

    for rule in schema.section_rules:
        if rule.required and rule.heading not in h2_headings:
            violations.append(
                ValidationViolation(
                    field_path=f"sections.{rule.heading}",
                    expected=f"## {rule.heading} section present",
                    actual="section missing",
                    severity="error",
                    message=f"Required section '## {rule.heading}' is missing from document.",
                )
            )

    # ------------------------------------------------------------------
    # 3. Nav table validation (H-23/H-24)
    # ------------------------------------------------------------------
    if schema.require_nav_table:
        nav_result = validate_nav_table(doc)
        if not nav_result.is_valid:
            if not nav_result.entries:
                # No nav table found at all
                violations.append(
                    ValidationViolation(
                        field_path="nav_table",
                        expected="navigation table present (H-23 required)",
                        actual="no nav table found",
                        severity="error",
                        message=("Document requires a navigation table (H-23) but none was found."),
                    )
                )
            else:
                # Nav table exists but has coverage issues
                if nav_result.missing_entries:
                    missing_str = ", ".join(nav_result.missing_entries)
                    violations.append(
                        ValidationViolation(
                            field_path="nav_table",
                            expected="all ## headings covered in nav table",
                            actual=f"missing entries: {missing_str}",
                            severity="error",
                            message=(
                                f"Navigation table is missing entries for headings: {missing_str}."
                            ),
                        )
                    )
                if nav_result.orphaned_entries:
                    orphaned_str = ", ".join(e.section_name for e in nav_result.orphaned_entries)
                    violations.append(
                        ValidationViolation(
                            field_path="nav_table",
                            expected="all nav table entries resolve to existing headings",
                            actual=f"orphaned entries: {orphaned_str}",
                            severity="error",
                            message=(
                                f"Navigation table has orphaned entries with no matching "
                                f"headings: {orphaned_str}."
                            ),
                        )
                    )

    # ------------------------------------------------------------------
    # Build report
    # ------------------------------------------------------------------
    is_valid = all(v.severity != "error" for v in violations)

    return ValidationReport(
        is_valid=is_valid,
        violations=tuple(violations),
        entity_type=schema.entity_type,
        field_count=field_count,
        section_count=section_count,
    )


# ---------------------------------------------------------------------------
# Built-in schema registry
# ---------------------------------------------------------------------------

_STATUS_VALUES = ("pending", "in_progress", "completed")
_PRIORITY_VALUES = ("critical", "high", "medium", "low")
_IMPACT_VALUES = ("critical", "high", "medium", "low")

EPIC_SCHEMA: EntitySchema = EntitySchema(
    entity_type="epic",
    field_rules=(
        FieldRule(key="Type", required=True, allowed_values=("epic",)),
        FieldRule(key="Status", required=True, allowed_values=_STATUS_VALUES),
        FieldRule(key="Priority", required=True, allowed_values=_PRIORITY_VALUES),
        FieldRule(key="Impact", required=True, allowed_values=_IMPACT_VALUES),
        FieldRule(key="Created", required=True),
        FieldRule(key="Due", required=False),
        FieldRule(key="Completed", required=False),
        FieldRule(key="Parent", required=False),
        FieldRule(key="Owner", required=False),
        FieldRule(key="Target Quarter", required=False),
    ),
    section_rules=(
        SectionRule(heading="Summary", required=True),
        SectionRule(heading="Children Features/Capabilities", required=True),
        SectionRule(heading="Progress Summary", required=True),
    ),
    require_nav_table=True,
)

FEATURE_SCHEMA: EntitySchema = EntitySchema(
    entity_type="feature",
    field_rules=(
        FieldRule(key="Type", required=True, allowed_values=("feature",)),
        FieldRule(key="Status", required=True, allowed_values=_STATUS_VALUES),
        FieldRule(key="Priority", required=True, allowed_values=_PRIORITY_VALUES),
        FieldRule(key="Impact", required=True, allowed_values=_IMPACT_VALUES),
        FieldRule(key="Created", required=True),
        FieldRule(key="Parent", required=True),
        FieldRule(key="Due", required=False),
        FieldRule(key="Completed", required=False),
        FieldRule(key="Owner", required=False),
        FieldRule(key="Target Sprint", required=False),
    ),
    section_rules=(
        SectionRule(heading="Summary", required=True),
        SectionRule(heading="Acceptance Criteria", required=True),
        SectionRule(heading="Children Stories/Enablers", required=True),
        SectionRule(heading="Progress Summary", required=True),
    ),
    require_nav_table=True,
)

STORY_SCHEMA: EntitySchema = EntitySchema(
    entity_type="story",
    field_rules=(
        FieldRule(key="Type", required=True, allowed_values=("story",)),
        FieldRule(key="Status", required=True, allowed_values=_STATUS_VALUES),
        FieldRule(key="Priority", required=True, allowed_values=_PRIORITY_VALUES),
        FieldRule(key="Impact", required=True, allowed_values=_IMPACT_VALUES),
        FieldRule(key="Created", required=True),
        FieldRule(key="Parent", required=True),
        FieldRule(key="Due", required=False),
        FieldRule(key="Completed", required=False),
        FieldRule(key="Owner", required=False),
        FieldRule(key="Effort", required=False),
    ),
    section_rules=(
        SectionRule(heading="Summary", required=True),
        SectionRule(heading="Acceptance Criteria", required=True),
    ),
    require_nav_table=True,
)

ENABLER_SCHEMA: EntitySchema = EntitySchema(
    entity_type="enabler",
    field_rules=(
        FieldRule(key="Type", required=True, allowed_values=("enabler",)),
        FieldRule(key="Status", required=True, allowed_values=_STATUS_VALUES),
        FieldRule(key="Priority", required=True, allowed_values=_PRIORITY_VALUES),
        FieldRule(key="Impact", required=True, allowed_values=_IMPACT_VALUES),
        FieldRule(
            key="Enabler Type",
            required=True,
            allowed_values=("infrastructure", "exploration", "architecture", "compliance"),
        ),
        FieldRule(key="Created", required=True),
        FieldRule(key="Parent", required=True),
        FieldRule(key="Due", required=False),
        FieldRule(key="Completed", required=False),
        FieldRule(key="Owner", required=False),
        FieldRule(key="Effort", required=False),
    ),
    section_rules=(
        SectionRule(heading="Summary", required=True),
        SectionRule(heading="Acceptance Criteria", required=True),
        SectionRule(heading="Technical Approach", required=True),
    ),
    require_nav_table=True,
)

TASK_SCHEMA: EntitySchema = EntitySchema(
    entity_type="task",
    field_rules=(
        FieldRule(key="Type", required=True, allowed_values=("task",)),
        FieldRule(key="Status", required=True, allowed_values=_STATUS_VALUES),
        FieldRule(key="Priority", required=True, allowed_values=_PRIORITY_VALUES),
        FieldRule(key="Created", required=True),
        FieldRule(key="Parent", required=True),
        FieldRule(key="Owner", required=False),
        FieldRule(key="Remaining", required=False),
    ),
    section_rules=(SectionRule(heading="Summary", required=True),),
    require_nav_table=False,
)

BUG_SCHEMA: EntitySchema = EntitySchema(
    entity_type="bug",
    field_rules=(
        FieldRule(key="Type", required=True, allowed_values=("bug",)),
        FieldRule(key="Status", required=True, allowed_values=_STATUS_VALUES),
        FieldRule(key="Priority", required=True, allowed_values=_PRIORITY_VALUES),
        FieldRule(key="Impact", required=True, allowed_values=_IMPACT_VALUES),
        FieldRule(
            key="Severity",
            required=True,
            allowed_values=("critical", "major", "minor", "trivial"),
        ),
        FieldRule(key="Created", required=True),
        FieldRule(key="Due", required=False),
        FieldRule(key="Completed", required=False),
        FieldRule(key="Parent", required=False),
        FieldRule(key="Owner", required=False),
        FieldRule(key="Found In", required=False),
        FieldRule(key="Fix Version", required=False),
    ),
    section_rules=(
        SectionRule(heading="Summary", required=True),
        SectionRule(heading="Steps to Reproduce", required=True),
        SectionRule(heading="Acceptance Criteria", required=True),
    ),
    require_nav_table=True,
)


# ---------------------------------------------------------------------------
# Schema registry lookup
# ---------------------------------------------------------------------------

_SCHEMA_REGISTRY: dict[str, EntitySchema] = {
    "epic": EPIC_SCHEMA,
    "feature": FEATURE_SCHEMA,
    "story": STORY_SCHEMA,
    "enabler": ENABLER_SCHEMA,
    "task": TASK_SCHEMA,
    "bug": BUG_SCHEMA,
}


def get_entity_schema(entity_type: str) -> EntitySchema:
    """
    Look up a built-in schema by entity type name.

    Returns the pre-defined EntitySchema for the given entity type identifier.
    The lookup is case-sensitive; ``"epic"`` is valid but ``"Epic"`` is not.

    Args:
        entity_type: The entity type string to look up (e.g., "epic", "story").

    Returns:
        The corresponding EntitySchema instance.

    Raises:
        ValueError: If ``entity_type`` is not a known built-in entity type.
            The error message lists the valid entity types.

    Examples:
        >>> schema = get_entity_schema("epic")
        >>> schema.entity_type
        'epic'
        >>> get_entity_schema("unknown")
        ValueError: Unknown entity type 'unknown'. Valid types: epic, feature, story, ...
    """
    schema = _SCHEMA_REGISTRY.get(entity_type)
    if schema is None:
        valid = ", ".join(sorted(_SCHEMA_REGISTRY.keys()))
        raise ValueError(f"Unknown entity type '{entity_type}'. Valid types: {valid}.")
    return schema
