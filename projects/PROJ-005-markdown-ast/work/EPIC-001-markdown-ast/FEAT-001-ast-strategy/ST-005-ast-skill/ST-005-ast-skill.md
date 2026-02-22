# ST-005: Create `/ast` Claude Skill

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

**As a** Claude agent operating within Jerry

**I want** an `/ast` skill that provides AST operations as skill scripts

**So that** I can perform structured markdown manipulation (parse, query, modify, validate) during interactive sessions without shelling out to CLI commands

---

## Summary

Create the `/ast` skill -- the Claude-facing interface of Pattern D (Hybrid). Thin wrapper scripts that import the shared domain layer, providing Claude with direct access to AST operations.

**Scope:**
- `skills/ast/SKILL.md` -- skill definition with usage instructions
- `skills/ast/scripts/ast_ops.py` -- thin wrapper importing domain layer
- Operations: parse, query frontmatter, modify frontmatter, validate, render
- ~150 LOC in skill scripts

**Out of Scope:**
- Domain logic (in `src/domain/markdown_ast/`)
- CLI interface (ST-004)
- Agent definitions (future work if needed)

---

## Acceptance Criteria

### Acceptance Checklist

- [x] `/ast` skill is invocable by Claude Code
- [x] Skill scripts import from `src/domain/markdown_ast/` (shared domain layer)
- [x] Claude can parse a file and get structured frontmatter data
- [x] Claude can modify a frontmatter field and write back
- [x] Claude can validate a file against a schema
- [x] SKILL.md follows Jerry skill template format
- [x] Unit tests for skill scripts achieve 90% line coverage (H-21)

### Definition of Done

- [x] Code complete and peer reviewed
- [x] Unit tests written and passing
- [x] 90% line coverage (H-21)
- [x] SKILL.md reviewed for correctness

---

## Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Blocked By | [ST-001](../ST-001-jerry-document/ST-001-jerry-document.md) | Scripts import domain facade |
| Blocked By | [ST-002](../ST-002-frontmatter-ext/ST-002-frontmatter-ext.md) | Frontmatter ops needed for skill |
| Blocks | [ST-007](../ST-007-worktracker-migration/ST-007-worktracker-migration.md) | Worktracker agents use /ast skill |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: AST Strategy Evaluation & Library Selection](../FEAT-001-ast-strategy.md)

### Traceability

- **Architecture:** Go/No-Go Recommendation L1, Component: Skill Scripts (~150 LOC)
- **Pattern D:** Dual-audience interface (CLI for humans, skill for Claude)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Story created. Claude-facing /ast skill. 3 SP. Blocked by ST-001 + ST-002. |
| 2026-02-21 | Claude | completed | AC verified. SKILL.md (324 LOC) + ast_ops.py (428 LOC). 43 unit tests, 100% coverage. 7 operations: parse, query_frontmatter, modify_frontmatter, validate, render, extract_reinject, validate_nav_table. Registered in CLAUDE.md + AGENTS.md + mandatory-skill-usage.md (H-30). |
