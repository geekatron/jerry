# STORY-003: Implement FILE-001..003 validators

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

## Summary

Implement the FILE-001..003 validation rules (file existence, size, format) per ADR-007 §4. TDD Red-Green-Refactor against golden packets. Part of the FEAT-003 deterministic-validation work that replaces LLM-judged compliance with mechanical checks.

---

## User Story

**As a** `ts-formatter` agent or CI pipeline,
**I want** mechanical validation that every required packet file exists at the right path with the right shape,
**So that** packet structure violations are caught at write time, not at adversary review.

---

## Rule Family

ADR-007 §4 FILE-001..003 rules. Exact rule definitions live in the vendored ADR-007; this Story implements them per its specification. Any deviation requires an ADR amendment.

(Audit identified the rule IDs but did not transcribe rule bodies into #273. STORY-003 implementer reads the canonical ADR-007 in `docs/adrs/` after FEAT-001 STORY-001 completes.)

---

## Agent Assignment

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/eng-team` | `eng-qa` | Author failing tests for FILE-001..003 against golden packets (TDD Red phase) |
| 2 | `/eng-team` | `eng-backend` | Implement FILE-001..003 as ValidationRule entities under `src/jerry/transcript/validation/domain/rules/file/` (Green) |
| 3 | `/eng-team` | `eng-backend` | Refactor for DRY across the 3 rules (Refactor) |
| 4 | `/problem-solving` | `ps-validator` | Confirm all 3 rules pass against clean-packet golden; fail against violation goldens |
| 5 | `/adversary` | `adv-executor` + `adv-scorer` | C4 ≥0.95 review on rule implementations + tests |
| 6 | `/worktracker` | `wt-verifier` | Validate AC; close |

---

## Acceptance Criteria

- [ ] All 3 FILE-* rules implemented as ValidationRule entities under `src/jerry/transcript/validation/domain/rules/file/`.
- [ ] Each rule returns `(rule_id, severity, pass|fail, evidence)` tuple per the canonical contract.
- [ ] TDD Red-Green-Refactor: golden packet tests for each rule precede implementation; coverage ≥90%.
- [ ] No direct filesystem access from rule code — uses `FilesystemPacketLoader` adapter via injected port.
- [ ] All 3 rules pass against the clean-packet golden in EN-002.
- [ ] All 3 rules fail against the matching violation golden(s) in EN-002.
- [ ] Property-based test: rule behavior is deterministic (same input always produces same output).
- [ ] `/adversary` C4 ≥0.95 phase gate before merge.

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Read canonical ADR-007 §4 FILE-* rule bodies in docs/adrs/ | pending |
| TASK-002 | Author failing tests for FILE-001 (TDD Red) | pending |
| TASK-003 | Implement FILE-001 (Green) | pending |
| TASK-004 | Repeat Red-Green for FILE-002, FILE-003 | pending |
| TASK-005 | Refactor for DRY across the 3 rules | pending |
| TASK-006 | Run /adversary C4 review | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-003](../FEAT-003-deterministic-validation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | EN-001 | Module skeleton |
| Blocked By | EN-002 | TDD harness with failing tests |
| Blocked By | FEAT-001 STORY-001 | Canonical ADR-007 readable in docs/adrs/ |
| Blocked By | FEAT-002 (all 5 bugs) | Rules must not encode contradictions |
| Blocks | STORY-007 (verify CLI), STORY-009 (post-render hook), STORY-012 (CI) | Validators must exist before integration |

### Source

- [#273 §C5](https://github.com/geekatron/jerry/issues/273) (ADR-007 §4 rule catalog)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Story created. FILE-* family. |
