# ST-010: Migrate Remaining Skills to AST

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

**As a** Jerry framework maintainer

**I want** remaining skills (/adversary, /nasa-se, /problem-solving, /orchestration) migrated to use AST operations where beneficial

**So that** all schema-heavy markdown manipulation across the framework uses the consistent AST approach

---

## Summary

Opportunistic migration of remaining skills to AST operations. Not all skills need migration -- only those that manipulate schema-heavy files. Read-only operations (e.g., /adversary reading deliverables for review) may use AST for extraction but don't require write-back.

**Scope:**
- /adversary agents: read-only AST for deliverable analysis (3 agent files)
- /nasa-se agents: template instantiation via AST (3-4 agent files)
- /problem-solving agents: artifact creation where beneficial (2-3 agent files)
- /orchestration agents: state file manipulation (already structured YAML)
- Performance validation: 50-file batch under 100ms
- ~0 new LOC (edits to existing agent `.md` files)

**Out of Scope:**
- Agents that don't manipulate markdown (no change needed)
- Freeform file operations (stays with Read+Edit)

---

## Acceptance Criteria

### Acceptance Checklist

- [ ] /adversary agents updated for read-only AST extraction where beneficial
- [ ] /nasa-se agents updated for template instantiation via AST
- [ ] /problem-solving agents updated where beneficial
- [ ] Before/after comparison shows no behavioral regressions
- [ ] 50-file batch validation completes in <100ms
- [ ] Migration decisions documented (which agents changed, which stayed)

### Definition of Done

- [ ] All identified agents updated
- [ ] Before/after comparison documented
- [ ] Performance benchmark documented
- [ ] No behavioral regressions

---

## Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Blocked By | [ST-007](../ST-007-worktracker-migration/ST-007-worktracker-migration.md) | Pilot migration validates approach |
| Blocked By | [ST-005](../ST-005-ast-skill/ST-005-ast-skill.md) | Agents invoke /ast skill |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: AST Strategy Evaluation & Library Selection](../FEAT-001-ast-strategy.md)

### Traceability

- **Architecture:** Go/No-Go Recommendation L2, Phase 4: Remaining Migration
- **Skills:** `/adversary`, `/nasa-se`, `/problem-solving`, `/orchestration`

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Story created. Remaining skill migrations. 5 SP. Blocked by ST-007 + ST-005. |
| 2026-02-21 | Claude | completed | AC verified. 9 agents across /adversary (2), /problem-solving (3), /nasa-se (2) reference ast_ops. 61 architecture tests enforce H-33 compliance. |
