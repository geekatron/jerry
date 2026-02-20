# ST-003: Implement L2-REINJECT Parser

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

> **Type:** story
> **Status:** pending
> **Priority:** high
> **Impact:** medium
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

**As a** Jerry framework maintainer

**I want** to parse and modify `<!-- L2-REINJECT: ... -->` HTML comments as structured data

**So that** I can programmatically manage context re-injection directives (rank, tokens, content) without regex-based string manipulation

---

## Summary

Implement the L2-REINJECT comment parser extension. These HTML comments carry structured metadata for Jerry's L2 enforcement layer and need to be accessible as typed data through the AST.

**Scope:**
- Parse `<!-- L2-REINJECT: rank=N, tokens=N, content="..." -->` from HTML comment nodes
- Return structured data: rank (int), tokens (int), content (str)
- Write-back: modify rank/tokens/content and re-render
- ~120 LOC in `src/domain/markdown_ast/reinject.py`

**Out of Scope:**
- Modifying L2 enforcement behavior (that's in `.context/rules/`)
- Other HTML comment patterns (only L2-REINJECT)

---

## Acceptance Criteria

### Acceptance Checklist

- [ ] Extract all L2-REINJECT comments from a Jerry rule file
- [ ] Parse structured fields: rank, tokens, content
- [ ] Write-back: modify rank value, verify roundtrip
- [ ] Write-back: modify content string, verify roundtrip
- [ ] Works on `quality-enforcement.md` (6+ L2-REINJECT comments)
- [ ] Non-L2-REINJECT HTML comments are preserved unchanged
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
| Blocked By | [EN-001](../EN-001-r01-poc/EN-001-r01-poc.md) | R-01 PoC must pass |
| Blocked By | [ST-001](../ST-001-jerry-document/ST-001-jerry-document.md) | Builds on JerryDocument facade |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: AST Strategy Evaluation & Library Selection](../FEAT-001-ast-strategy.md)

### Traceability

- **Architecture:** Go/No-Go Recommendation L1, Component: L2ReinjectParser (~120 LOC)
- **L2 Enforcement:** `.context/rules/quality-enforcement.md` (Enforcement Architecture, Layer L2)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Story created. L2-REINJECT comment parser. 3 SP. Blocked by EN-001 + ST-001. |
