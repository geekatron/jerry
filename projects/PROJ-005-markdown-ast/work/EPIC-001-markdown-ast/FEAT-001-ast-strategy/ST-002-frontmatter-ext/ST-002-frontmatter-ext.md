# ST-002: Implement Blockquote Frontmatter Extension

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

> **Type:** story
> **Status:** completed
> **Priority:** high
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

**As a** Jerry skill or CLI user

**I want** to extract, modify, and write back blockquote frontmatter fields (`> **Key:** Value`)

**So that** I can programmatically update entity status, priority, owner, and other metadata without full-file text replacement

---

## Summary

Implement the blockquote frontmatter extraction and write-back extension for markdown-it-py. This is the most complex custom extension and the one validated by EN-001's R-01 PoC.

**Scope:**
- Parse `> **Key:** Value` patterns from blockquote nodes
- Return structured dict of key-value pairs with source positions
- Write-back: modify individual fields and re-render without disturbing other content
- Handle multiline values, inline markdown in values, colon-inclusive key text
- ~220 LOC in `src/domain/markdown_ast/frontmatter.py`

**Out of Scope:**
- YAML frontmatter (standard `---` delimited) -- handled natively by mdit-py-plugins
- Schema validation of frontmatter fields (ST-006)

---

## Acceptance Criteria

### Acceptance Checklist

- [x] Extract all key-value pairs from a Jerry entity blockquote frontmatter
- [x] Handle multiline values (e.g., wrapped descriptions)
- [x] Handle inline markdown in values (e.g., `**Status:** pending`)
- [x] Write-back: modify a single field, render, verify unmodified fields preserved
- [x] Write-back: add a new field to existing frontmatter
- [x] Works on WORKTRACKER entities, skill definitions, spike entities, enabler entities
- [x] Unit tests achieve 90% line coverage (H-21)
- [x] BDD test-first approach followed (H-20)

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
| Blocked By | [EN-001](../EN-001-r01-poc/EN-001-r01-poc.md) | R-01 PoC validates write-back feasibility |
| Blocked By | [ST-001](../ST-001-jerry-document/ST-001-jerry-document.md) | Builds on JerryDocument facade |
| Blocks | [ST-006](../ST-006-schema-validation/ST-006-schema-validation.md) | Schema validation validates frontmatter fields |
| Blocks | [ST-007](../ST-007-worktracker-migration/ST-007-worktracker-migration.md) | Worktracker migration uses frontmatter ops |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: AST Strategy Evaluation & Library Selection](../FEAT-001-ast-strategy.md)

### Traceability

- **Architecture:** Go/No-Go Recommendation L1, Component: BlockquoteFrontmatter (~220 LOC)
- **SPIKE-001:** Extension effort estimate ~220 LOC (library-feature-matrix.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Story created. Core frontmatter extension. 5 SP. Blocked by EN-001 + ST-001. |
| 2026-02-21 | Claude | completed | AC verified. 491 LOC in frontmatter.py. BlockquoteFrontmatter with extract/get/set/add. 100% line coverage. R-01 validated write-back. |
