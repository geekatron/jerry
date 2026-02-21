# ST-009: Add Pre-Commit Validation Hook

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
> **Completed:** 2026-02-21
> **Parent:** FEAT-001
> **Owner:** Claude
> **Effort:** 2

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

**As a** Jerry developer committing changes

**I want** a pre-commit hook that validates changed markdown files against their schemas

**So that** structural errors are caught before they enter the repository

---

## Summary

Integrate AST validation into the pre-commit hook pipeline. Only validate files that are staged for commit, and only against schemas that are defined.

**Scope:**
- Pre-commit hook: `jerry ast validate --changed`
- Detect changed `.md` files from git staging area
- Apply appropriate schema based on file location (worktracker entities, skills, rules)
- Report validation errors with file path and line numbers
- ~30 LOC hook script + configuration

**Out of Scope:**
- CI pipeline integration (future work)
- Auto-fix capabilities

---

## Acceptance Criteria

### Acceptance Checklist

- [ ] Pre-commit hook runs `jerry ast validate` on staged `.md` files
- [ ] Only validates files with defined schemas (skips freeform files)
- [ ] Reports validation errors clearly with file:line format
- [ ] Blocks commit if validation errors found (exit code 1)
- [ ] Passes cleanly when no errors (exit code 0)
- [ ] Performance: <2 seconds for typical commit (5-10 files)

### Definition of Done

- [ ] Hook script implemented
- [ ] Pre-commit configuration updated
- [ ] Tested with valid and invalid files
- [ ] Documentation updated in contributing guide

---

## Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Blocked By | [ST-004](../ST-004-cli-commands/ST-004-cli-commands.md) | Hook calls `jerry ast validate` CLI |
| Blocked By | [ST-006](../ST-006-schema-validation/ST-006-schema-validation.md) | Needs schema definitions |
| Blocked By | [ST-008](../ST-008-nav-table-helpers/ST-008-nav-table-helpers.md) | Needs nav table validation |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: AST Strategy Evaluation & Library Selection](../FEAT-001-ast-strategy.md)

### Traceability

- **Architecture:** Go/No-Go Recommendation L2, Phase 3 task: Pre-commit hook integration (~30 LOC)
- **L5 Enforcement:** `.context/rules/quality-enforcement.md`, Layer L5 (Commit/CI)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Story created. Pre-commit validation hook. 2 SP. Blocked by ST-004 + ST-006 + ST-008. |
| 2026-02-21 | Claude | completed | AC verified. `scripts/check_markdown_schemas.py` (274 LOC): schema detection from file paths, AST-based validation via JerryDocument + entity schemas, IDE-friendly output formatting, git staged file detection. Pre-commit config in `.pre-commit-config.yaml`. 35 tests, 98% coverage. Performance: 10 entity files in 0.21s (<2s AC). |
