# ST-007: Migrate /worktracker Agents to AST

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
> **Completed:** 2026-02-21
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

**As a** Jerry /worktracker skill user

**I want** worktracker agents to use AST operations instead of raw text manipulation

**So that** entity creation and updates are structurally correct, validated against schemas, and preserve formatting

---

## Summary

Pilot migration: update /worktracker agent definitions to use `/ast` skill operations for entity manipulation. This is the highest-value, lowest-risk migration target (SPIKE-002, Phase 5).

**Scope:**
- Update wt-verifier, wt-visualizer, wt-auditor agent definitions
- Replace Read+Edit patterns with /ast parse+modify+validate+render
- Before/after comparison on 10 real entity files
- ~0 new LOC (edits to existing agent `.md` files)

**Out of Scope:**
- Other skill migrations (ST-010)
- Schema expansion beyond WORKTRACKER entities (Phase 3 work)

---

## Acceptance Criteria

### Acceptance Checklist

- [ ] wt-verifier agent uses AST-based frontmatter extraction for status checks
- [ ] wt-auditor agent uses AST-based validation for integrity checks
- [ ] wt-visualizer agent uses AST-based hierarchy extraction for diagrams
- [ ] Before/after comparison on 10 real entity files shows no regressions
- [ ] Agent outputs remain identical (behavior-preserving migration)
- [ ] Schema validation errors are surfaced in agent reports

### Definition of Done

- [ ] All 3 worktracker agents updated
- [ ] Before/after comparison documented
- [ ] No behavioral regressions

---

## Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Blocked By | [ST-005](../ST-005-ast-skill/ST-005-ast-skill.md) | Agents invoke /ast skill |
| Blocked By | [ST-006](../ST-006-schema-validation/ST-006-schema-validation.md) | Agents use schema validation |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: AST Strategy Evaluation & Library Selection](../FEAT-001-ast-strategy.md)

### Traceability

- **Pilot Target:** SPIKE-002 Phase 5, Migration Effort: "/worktracker as pilot (highest value, lowest risk)"
- **Agents:** `skills/worktracker/agents/wt-verifier.md`, `wt-visualizer.md`, `wt-auditor.md`

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Story created. Pilot migration of /worktracker agents to AST. 3 SP. Blocked by ST-005 + ST-006. |
| 2026-02-21 | Claude | completed | AC verified. 3 agents (wt-verifier, wt-auditor, wt-visualizer) updated with ast_ops references. H-33 enforcement via 61 architecture tests. |
