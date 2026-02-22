# ST-008: Implement Navigation Table Helpers

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

> **Type:** story
> **Status:** completed
> **Priority:** low
> **Impact:** medium
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** 2026-02-20
> **Parent:** FEAT-001
> **Owner:** Claude
> **Effort:** 3

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

**As a** Jerry framework maintainer

**I want** AST-based helpers for querying and validating navigation tables

**So that** H-23 (navigation table required) and H-24 (anchor links required) can be enforced programmatically

---

## Summary

Implement navigation table helpers that enable programmatic validation of H-23/H-24 compliance. Currently these rules rely on manual review; AST-based validation can automate enforcement.

**Scope:**
- Walk AST to find navigation tables (first table after frontmatter)
- Extract section-link pairs from navigation table
- Validate: all `##` headings have corresponding navigation entries
- Validate: all navigation links resolve to valid anchors
- ~120 LOC in `src/domain/markdown_ast/nav_table.py`

**Out of Scope:**
- Auto-generating navigation tables (future enhancement)
- Table manipulation beyond navigation tables

---

## Acceptance Criteria

### Acceptance Checklist

- [x] Find navigation table in a Jerry document (first table after frontmatter)
- [x] Extract section names and anchor links from navigation table
- [x] Validate: every `##` heading has a navigation entry
- [x] Validate: every navigation link resolves to a valid heading anchor
- [x] Report missing/orphaned entries with line numbers
- [x] `jerry ast validate <file> --nav` checks navigation table compliance
- [x] Unit tests achieve 90% line coverage (H-21)

### Definition of Done

- [x] Code complete and peer reviewed
- [x] Unit tests written and passing
- [x] 90% line coverage (H-21)
- [x] Type hints on all public functions (H-11)
- [x] Docstrings on all public functions (H-12)

---

## Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Blocked By | [ST-001](../ST-001-jerry-document/ST-001-jerry-document.md) | Builds on JerryDocument facade |
| Blocks | [ST-009](../ST-009-precommit-hook/ST-009-precommit-hook.md) | Pre-commit hook includes nav validation |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: AST Strategy Evaluation & Library Selection](../FEAT-001-ast-strategy.md)

### Traceability

- **Rules Enforced:** H-23 (NAV-001), H-24 (NAV-006) from `markdown-navigation-standards.md`
- **Architecture:** Go/No-Go Recommendation L1, Component: NavTableHelpers (~120 LOC)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Story created. Navigation table validation helpers. 3 SP. Blocked by ST-001. |
| 2026-02-21 | Claude | completed | AC verified. nav_table.py with NavEntry, NavValidationResult, extract_nav_table, validate_nav_table, heading_to_anchor. 100% coverage. H-23/H-24 enforcement. |
