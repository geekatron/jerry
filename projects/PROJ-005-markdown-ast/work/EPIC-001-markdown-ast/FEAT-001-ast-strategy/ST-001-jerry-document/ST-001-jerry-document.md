# ST-001: Implement JerryDocument Facade

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

> **Type:** story
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** --
> **Parent:** FEAT-001
> **Owner:** --
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

**As a** Jerry developer (human or Claude agent)

**I want** a unified `JerryDocument` facade that wraps markdown-it-py + mdformat

**So that** I can parse, query, transform, and render Jerry markdown files through a single typed API without interacting with library internals directly

---

## Summary

Implement the core domain facade (`JerryDocument`) that provides the unified API for all AST operations. This is the foundational component that all other stories build upon.

**Scope:**
- `JerryDocument` class with `parse()`, `render()`, `query()`, `transform()` methods
- Integration with markdown-it-py for parsing and mdformat for rendering
- SyntaxTreeNode wrapper for typed AST traversal
- Value object semantics (immutable parse result, new document on transform)
- ~130 LOC in `src/domain/markdown_ast/jerry_document.py`

**Out of Scope:**
- Custom extensions (ST-002, ST-003, ST-008)
- CLI adapter (ST-004)
- Schema validation (ST-006)

---

## Acceptance Criteria

### Acceptance Checklist

- [ ] `JerryDocument.parse(source: str)` returns a typed AST representation
- [ ] `JerryDocument.render()` produces markdown output via mdformat
- [ ] `JerryDocument.query(selector)` enables node lookup by type/attribute
- [ ] `JerryDocument.transform(visitor)` enables node modification with new document return
- [ ] Parse-render roundtrip preserves unmodified content (mdformat normalization accepted)
- [ ] All public methods have type hints (H-11) and docstrings (H-12)
- [ ] Unit tests achieve 90% line coverage (H-21)
- [ ] BDD test-first approach followed (H-20)

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
| Blocked By | [EN-001](../EN-001-r01-poc/EN-001-r01-poc.md) | R-01 PoC must pass before implementation |
| Blocks | [ST-002](../ST-002-frontmatter-ext/ST-002-frontmatter-ext.md) | Frontmatter extension builds on facade |
| Blocks | [ST-003](../ST-003-reinject-parser/ST-003-reinject-parser.md) | L2-REINJECT parser builds on facade |
| Blocks | [ST-004](../ST-004-cli-commands/ST-004-cli-commands.md) | CLI commands wrap facade |
| Blocks | [ST-006](../ST-006-schema-validation/ST-006-schema-validation.md) | Schema validation uses facade |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: AST Strategy Evaluation & Library Selection](../FEAT-001-ast-strategy.md)

### Traceability

- **Architecture:** Go/No-Go Recommendation L1 (`orchestration/spike-eval-20260219-001/ps/phase-6-decision/ps-synthesizer-002/go-nogo-recommendation.md`, Component Breakdown)
- **LOC Budget:** ~130 LOC domain layer

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Story created. Core facade for AST operations. 5 SP. Blocked by EN-001. |
