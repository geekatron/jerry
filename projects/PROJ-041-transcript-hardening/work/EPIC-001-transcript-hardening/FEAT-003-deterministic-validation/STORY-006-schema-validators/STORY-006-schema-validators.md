# STORY-006: Implement SCHEMA-001..008 validators

> **Type:** story
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-003
> **Owner:** adam.nowak
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Rule Family](#rule-family) | Which ADR-007 §4 rules this Story implements |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Agent Assignment](#agent-assignment) | Specific skill+agent mappings |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## Summary

Implement the SCHEMA-001..008 validation rules per ADR-007 §4. Each rule loads its canonical schema via JsonSchemaAdapter (rules read schemas, do not hardcode shapes — so FEAT-004 schema additions extend rule coverage automatically). Uses post-FEAT-002 converged schemas (chunk_id, DOMAIN, seg-NNN regex).

---

## User Story

**As a** `ts-formatter` agent or CI pipeline,
**I want** mechanical JSON Schema conformance validation across the 8 packet schemas,
**So that** every packet sidecar JSON is structurally valid before the packet is reported as complete.

---

## Rule Family

ADR-007 §4 SCHEMA-001..008 rules. Each maps to a JSON Schema in the framework. Includes converged regex from FEAT-002 BUG-002 (`chunk_id`) and the canonical schema from BUG-003 (`domain`).

---

## Agent Assignment

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/eng-team` | `eng-backend` | Author `JsonSchemaAdapter` (infrastructure layer) |
| 2 | `/eng-team` | `eng-qa` | Author failing tests for SCHEMA-001..008 (TDD Red); include large-packet golden for forward-compat regex |
| 3 | `/eng-team` | `eng-backend` | Implement SCHEMA-001..008 (Green); rules read schemas, don't hardcode shapes (so FEAT-004 schema additions extend coverage automatically) |
| 4 | `/eng-team` | `eng-backend` | Refactor for DRY across SCHEMA family |
| 5 | `/problem-solving` | `ps-validator` | Verify rules use post-FEAT-002 schemas (converged chunk_id, canonical DOMAIN-SCHEMA, loosened seg-NNN) |
| 6 | `/adversary` | `adv-executor` + `adv-scorer` | C4 ≥0.95 review |
| 7 | `/worktracker` | `wt-verifier` | Validate AC; close |

---

## Acceptance Criteria

- [ ] All 8 SCHEMA-* rules implemented under `src/jerry/transcript/validation/domain/rules/schema/`.
- [ ] Each rule loads its canonical schema via `JsonSchemaAdapter` (infrastructure layer); no direct file reads from rule code.
- [ ] All 8 rules use the post-FEAT-002 schemas (converged `chunk_id` regex; canonical `DOMAIN-SCHEMA.json`; loosened `seg-NNN` regex).
- [ ] TDD Red-Green-Refactor; coverage ≥90%.
- [ ] All rules pass against clean-packet golden; fail against violation goldens.
- [ ] Validates against the large-packet golden (1000+ chunks/segments); confirms forward-compat regex.
- [ ] FEAT-004 schema additions (when they land) extend rule coverage automatically (rules read schemas, don't hardcode shapes).
- [ ] `/adversary` C4 ≥0.95 phase gate.

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Read canonical ADR-007 §4 SCHEMA-* rule bodies | pending |
| TASK-002 | Author JsonSchemaAdapter (infrastructure layer) | pending |
| TASK-003 | Author failing tests for SCHEMA-001..008 (TDD Red) | pending |
| TASK-004 | Implement SCHEMA-001..008 (Green) | pending |
| TASK-005 | Validate against large-packet golden (forward-compat) | pending |
| TASK-006 | Refactor for DRY across SCHEMA family | pending |
| TASK-007 | Run /adversary C4 review | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-003](../FEAT-003-deterministic-validation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | EN-001, EN-002 | Scaffolding + TDD harness |
| Blocked By | FEAT-001 STORY-001 | Canonical ADR-007 |
| Blocked By | FEAT-002 BUG-002, BUG-003, BUG-004 | Schemas must be converged before rules encode them |
| Cooperates | FEAT-004 | New schema fields extend rule coverage |

### Source

- [#273 §C5](https://github.com/geekatron/jerry/issues/273)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Story created. SCHEMA-* family. |
