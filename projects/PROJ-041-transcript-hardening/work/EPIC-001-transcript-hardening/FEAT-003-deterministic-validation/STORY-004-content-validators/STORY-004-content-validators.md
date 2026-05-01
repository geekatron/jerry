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
| [Summary](#summary) | What this story delivers |
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

## Summary

Implement the CONTENT-001..003 validation rules (markdown content shape) per ADR-007 §4. Includes the backlinks-format rule per BUG-005 (canonical `<backlinks>` tag, deprecated `## Backlinks` H2). TDD Red-Green-Refactor.

---

## Rule Family

ADR-007 §4 CONTENT-001..003 rules. Includes the backlinks-format rule resolved by FEAT-002 BUG-005 (`<backlinks>` tag, not `## Backlinks` H2). Exact rule definitions in the vendored ADR-007.

---

## Acceptance Criteria

- [ ] All 3 CONTENT-* rules implemented as ValidationRule entities under `src/jerry/transcript/validation/domain/rules/content/`.
- [ ] CONTENT rule encoding the backlinks format **uses `<backlinks>` tag** per BUG-005 resolution.
- [ ] TDD Red-Green-Refactor; coverage ≥90%.
- [ ] All 3 rules pass against clean-packet golden; fail against matching violation goldens.
- [ ] Property-based test for deterministic behavior.
- [ ] `/adversary` C4 ≥0.95 phase gate.

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

## Children Tasks

| ID | Title | Owner | Status |
|----|-------|-------|--------|
| [TASK-080](./TASK-080-tdd-red-failing-tests-content-rules.md) | Author failing tests for CONTENT-001..003 (TDD Red) | `eng-qa` | pending |
| [TASK-081](./TASK-081-implement-content-rules-green.md) | Implement CONTENT-001..003 (Green) | `eng-backend` | pending |
| [TASK-082](./TASK-082-refactor-dry-content-family.md) | Refactor for DRY across CONTENT rules | `eng-backend` | pending |
| [TASK-083](./TASK-083-verify-content-rules-reject-h2-backlinks.md) | Verify rules reject `## Backlinks` H2 form; accept `<backlinks>` tag form | `ps-validator` | pending |
| [TASK-084](./TASK-084-run-adversary-c4-review.md) | Run /adversary C4 review | `adv-executor` | pending |
| [TASK-085](./TASK-085-validate-ac-and-close-story-004.md) | Validate STORY-004 AC and close | `wt-verifier` | pending |

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
