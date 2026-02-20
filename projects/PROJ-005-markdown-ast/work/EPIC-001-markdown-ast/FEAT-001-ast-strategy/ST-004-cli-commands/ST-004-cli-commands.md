# ST-004: Add `jerry ast` CLI Commands

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

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
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | Scope and context |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Dependencies](#dependencies) | Blocked by / Blocks |
| [Related Items](#related-items) | Hierarchy |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry developer or CI pipeline

**I want** CLI commands for AST operations (`jerry ast parse|render|validate|query`)

**So that** I can perform markdown AST operations from the terminal for batch processing, debugging, and CI integration

---

## Summary

Add the CLI adapter that exposes the domain layer as `jerry ast` subcommands. This is the human-facing interface of Pattern D (Hybrid).

**Scope:**
- `jerry ast parse <file>` -- output AST as JSON
- `jerry ast render <file>` -- roundtrip parse-render
- `jerry ast validate <file> [--schema <type>]` -- validate against schema
- `jerry ast query <file> <selector>` -- query AST nodes
- ~250 LOC in `src/interface/cli/ast_commands.py`

**Out of Scope:**
- Skill interface (ST-005)
- Schema definitions (ST-006)
- Pre-commit hook integration (ST-009)

---

## Acceptance Criteria

### Acceptance Checklist

- [ ] `jerry ast parse WORKTRACKER.md` outputs valid JSON AST
- [ ] `jerry ast render WORKTRACKER.md` produces roundtripped markdown
- [ ] `jerry ast validate WORKTRACKER.md --schema entity` reports validation results
- [ ] `jerry ast query WORKTRACKER.md "blockquote.frontmatter"` returns structured data
- [ ] Exit codes: 0 (success), 1 (validation failure), 2 (parse error)
- [ ] `--help` documentation for all subcommands
- [ ] Unit tests achieve 90% line coverage (H-21)

### Definition of Done

- [ ] Code complete and peer reviewed
- [ ] Unit tests written and passing
- [ ] 90% line coverage (H-21)
- [ ] Type hints on all public functions (H-11)
- [ ] Docstrings on all public functions (H-12)

---

## Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Blocked By | [ST-001](../ST-001-jerry-document/ST-001-jerry-document.md) | CLI wraps the JerryDocument facade |
| Blocks | [ST-009](../ST-009-precommit-hook/ST-009-precommit-hook.md) | Pre-commit hook calls CLI commands |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: AST Strategy Evaluation & Library Selection](../FEAT-001-ast-strategy.md)

### Traceability

- **Architecture:** Go/No-Go Recommendation L1, Component: CLI Adapter (~250 LOC)
- **Pattern D:** Phase 4 integration-patterns-research.md, Pattern D specification

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Story created. CLI adapter for AST operations. 3 SP. Blocked by ST-001. |
