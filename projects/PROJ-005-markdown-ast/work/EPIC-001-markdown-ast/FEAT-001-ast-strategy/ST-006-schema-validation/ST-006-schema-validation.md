# ST-006: Implement Schema Validation Engine

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

> **Type:** story
> **Status:** completed
> **Priority:** medium
> **Impact:** high
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** 2026-02-20
> **Parent:** FEAT-001
> **Owner:** Claude
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | Scope and context |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Dependencies](#dependencies) | Blocked by / Blocks |
| [Related Items](#related-items) | Hierarchy |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry developer or CI pipeline

**I want** a schema validation engine that can check Jerry markdown files against structural schemas

**So that** structural errors (missing required fields, invalid navigation tables, malformed frontmatter) are caught at parse time rather than propagating silently

---

## Summary

Implement the schema validation engine and initial schema definitions for WORKTRACKER entities. This addresses the primary benefit identified in SPIKE-002: 4 of 6 Jerry structural patterns currently have zero automated error detection.

**Scope:**
- Schema definition format (Python dataclasses or similar)
- Validation engine: check AST against schema, report violations
- Initial schemas: WORKTRACKER entity (Epic, Feature, Story, Enabler, Spike, Task, Bug)
- ~250 LOC in `src/domain/markdown_ast/schema.py`

**Out of Scope:**
- Skill file schemas (ST-008 nav table helpers support this)
- Rule file schemas (Phase 3)
- Pre-commit integration (ST-009)

---

## Acceptance Criteria

### Acceptance Checklist

- [x] Schema definition API: define required frontmatter fields, types, allowed values
- [x] Schema definition API: define required sections (## headings)
- [x] Schema definition API: define navigation table requirements (H-23/H-24)
- [x] Validate a WORKTRACKER Epic entity against its schema -- catches missing fields
- [x] Validate a WORKTRACKER Story entity -- catches invalid status values
- [x] `jerry ast validate <file> --schema entity` returns structured validation report
- [x] Validation report includes: field path, expected, actual, severity
- [x] Unit tests achieve 90% line coverage (H-21)

### Definition of Done

- [x] Code complete and peer reviewed
- [x] Unit tests written and passing
- [x] 90% line coverage (H-21)
- [x] Type hints on all public functions (H-11)
- [x] Docstrings on all public functions (H-12)
- [x] Schema definitions match `.context/templates/worktracker/` templates

---

## Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Blocked By | [ST-001](../ST-001-jerry-document/ST-001-jerry-document.md) | Validation operates on JerryDocument AST |
| Blocked By | [ST-002](../ST-002-frontmatter-ext/ST-002-frontmatter-ext.md) | Validates frontmatter field presence/values |
| Blocks | [ST-007](../ST-007-worktracker-migration/ST-007-worktracker-migration.md) | Worktracker migration uses validation |
| Blocks | [ST-009](../ST-009-precommit-hook/ST-009-precommit-hook.md) | Pre-commit hook calls validation |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: AST Strategy Evaluation & Library Selection](../FEAT-001-ast-strategy.md)

### Traceability

- **Architecture:** Go/No-Go Recommendation L1, Component: SchemaValidator (~250 LOC)
- **SPIKE-002 Finding:** 4/6 patterns have zero automated detection (Phase 5, Schema Validation Capability)
- **Templates:** `.context/templates/worktracker/` -- source schemas for entity validation

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Story created. Schema validation engine + WORKTRACKER schemas. 5 SP. Blocked by ST-001 + ST-002. |
| 2026-02-21 | Claude | completed | AC verified. 574 LOC in schema.py. 6 built-in schemas (Epic, Feature, Story, Enabler, Task, Bug). FieldRule, SectionRule, EntitySchema, ValidationViolation, ValidationReport. 100% coverage. |
