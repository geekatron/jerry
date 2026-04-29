# STORY-004: Implement CONTENT-001..003 validators

> **Type:** story
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-003
> **Owner:** adam.nowak
> **Effort:** 3

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

## User Story

**As a** `ts-formatter` agent or CI pipeline,
**I want** mechanical validation of packet content shape (markdown structure, sections, naming),
**So that** content drift is caught at write time, not at adversary review.

---

## Rule Family

ADR-007 §4 CONTENT-001..003 rules. Includes the backlinks-format rule resolved by FEAT-002 BUG-005 (`<backlinks>` tag, not `## Backlinks` H2). Exact rule definitions in the vendored ADR-007.

---

## Agent Assignment

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/eng-team` | `eng-qa` | Author failing tests for CONTENT-001..003 (TDD Red); include backlinks-format rule per BUG-005 (`<backlinks>` tag canonical) |
| 2 | `/eng-team` | `eng-backend` | Implement CONTENT-001..003 (Green) under `src/jerry/transcript/validation/domain/rules/content/` |
| 3 | `/eng-team` | `eng-backend` | Refactor for DRY |
| 4 | `/problem-solving` | `ps-validator` | Confirm rules reject `## Backlinks` H2 form; accept `<backlinks>` tag form |
| 5 | `/adversary` | `adv-executor` + `adv-scorer` | C4 ≥0.95 review |
| 6 | `/worktracker` | `wt-verifier` | Validate AC; close |

---

## Acceptance Criteria

- [ ] All 3 CONTENT-* rules implemented as ValidationRule entities under `src/jerry/transcript/validation/domain/rules/content/`.
- [ ] CONTENT rule encoding the backlinks format **uses `<backlinks>` tag** per BUG-005 resolution.
- [ ] TDD Red-Green-Refactor; coverage ≥90%.
- [ ] All 3 rules pass against clean-packet golden; fail against matching violation goldens.
- [ ] Property-based test for deterministic behavior.
- [ ] `/adversary` C4 ≥0.95 phase gate.

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Read canonical ADR-007 §4 CONTENT-* rule bodies | pending |
| TASK-002 | Author failing tests (TDD Red) | pending |
| TASK-003 | Implement CONTENT-001..003 (Green) | pending |
| TASK-004 | Refactor for DRY | pending |
| TASK-005 | Run /adversary C4 review | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-003](../FEAT-003-deterministic-validation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | EN-001, EN-002 | Scaffolding + TDD harness |
| Blocked By | FEAT-001 STORY-001 | Canonical ADR-007 |
| Blocked By | FEAT-002 BUG-005 | Backlinks format must be resolved |

### Source

- [#273 §C5](https://github.com/geekatron/jerry/issues/273)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Story created. CONTENT-* family. |
