# STORY-005: Implement ANCHOR-001..003 validators

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
| [Summary](#summary) | What this story delivers |
| [Rule Family](#rule-family) | Which ADR-007 §4 rules this Story implements |
| [Substrate Coupling](#substrate-coupling) | Why this Story is the heart of the audit's diagnostic |
| [Agent Assignment](#agent-assignment) | Specific skill+agent mappings |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## Summary

Implement the ANCHOR-001..003 validation rules per ADR-007 §4 — the heart of the substrate-coupling fix. ANCHOR-003 is the substrate-coupling rule that walks declared grep patterns through SubprocessSandbox and asserts walked == declared per bucket; this is the rule that catches the iter-9 audit drift class. Security-adjacent (uses subprocess), so reviewed by eng-security and red-exploit.

---

## User Story

**As a** `ts-formatter` agent, CI pipeline, or downstream consumer,
**I want** mechanical validation that anchor format, anchor uniqueness, and anchor resolution match the declared substrate,
**So that** the declared-derived coupling defect class (audit comment 1) cannot recur.

---

## Rule Family

ADR-007 §4 ANCHOR-001..003 rules. Includes seg-NNN format from FEAT-002 BUG-004 (`^seg-\d{3,}$`).

---

## Substrate Coupling

This Story implements the rule family that catches the declared-derived coupling defect described in [#273 comment 1](https://github.com/geekatron/jerry/issues/273#issuecomment-4339264545):

> "Each transcript packet has an `audit_breakdown.per_bucket_derivation` block in `_anchors.json` that publishes both declared counts AND derivation patterns (bash one-liners that should reproduce the declared counts when run against the rendered .md files). Declared counts are static, but they are derived from grepping rendered files. Any later edit silently invalidates the declared counts."

Rule (sketched): for each bucket, walk the documented `derivation_grep_pattern` (via `SubprocessSandbox` from EN-003) and assert `walked_count == declared_count`. Drift = fail.

This is the rule that catches the iter-9-class regression in the audit. Without this Story, the substrate cannot be machine-verified.

---

## Agent Assignment

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/eng-team` | `eng-qa` | Author failing tests for ANCHOR-001..003 (TDD Red); use `\d{3,}` regex per BUG-004; cover declared-vs-walked drift case |
| 2 | `/eng-team` | `eng-backend` | Implement anchor format + uniqueness + substrate-coupling rules; substrate-coupling rule routes through SubprocessSandbox port (EN-003) |
| 3 | `/eng-team` | `eng-security` | Code review on substrate-coupling rule (uses subprocess via sandbox; security-adjacent) |
| 4 | `/red-team` | `red-exploit` | Verify ANCHOR rule cannot bypass SubprocessSandbox boundary (re-uses EN-004 Phase 4 work) |
| 5 | `/problem-solving` | `ps-validator` | Reproduce audit's iter-9 drift detection on the original audit packet (declared 33 vs walked 32) |
| 6 | `/adversary` | `adv-executor` + `adv-scorer` | C4 ≥0.95 review |
| 7 | `/worktracker` | `wt-verifier` | Validate AC; close |

---

## Acceptance Criteria

- [ ] All 3 ANCHOR-* rules implemented under `src/jerry/transcript/validation/domain/rules/anchor/`.
- [ ] Anchor format rule encodes `^seg-\d{3,}$` (post-BUG-004 resolution); supports `disc-\d{3,}` once FEAT-004 STORY-015 lands.
- [ ] Anchor uniqueness rule walks all rendered .md files and asserts no duplicate anchor IDs.
- [ ] Substrate-coupling rule walks `_anchors.json.audit_breakdown.per_bucket_derivation` patterns through SubprocessSandbox; asserts walked == declared per bucket.
- [ ] All grep execution routes through `SubprocessSandbox` (EN-003); no direct `subprocess.run` calls.
- [ ] TDD Red-Green-Refactor; coverage ≥95% (security-adjacent code).
- [ ] All rules pass against clean-packet golden; fail against drift-detected golden (EN-002).
- [ ] Validates against the iter-9 audit packet state and reproduces the audit's drift detection (1 walked, 1 declared difference).
- [ ] `/red-team` validates ANCHOR rule does not bypass SubprocessSandbox boundary.
- [ ] `/adversary` C4 ≥0.95 phase gate.

---

## Children Tasks

| ID | Title | Owner | Status |
|----|-------|-------|--------|
| [TASK-086](./TASK-086-tdd-red-anchor-tests-with-drift-case.md) | Author failing tests for ANCHOR-001..003 (TDD Red); cover declared-vs-walked drift | `eng-qa` | pending |
| [TASK-087](./TASK-087-implement-anchor-format-rule.md) | Implement anchor format rule (ANCHOR-001) | `eng-backend` | pending |
| [TASK-088](./TASK-088-implement-anchor-uniqueness-rule.md) | Implement anchor uniqueness rule (ANCHOR-002) | `eng-backend` | pending |
| [TASK-089](./TASK-089-implement-substrate-coupling-rule.md) | Implement substrate-coupling rule (ANCHOR-003) using SubprocessSandbox | `eng-backend` | pending |
| [TASK-090](./TASK-090-code-review-substrate-coupling.md) | Code review on substrate-coupling rule (subprocess-using rule) | `eng-security` | pending |
| [TASK-091](./TASK-091-verify-anchor-rule-cant-bypass-sandbox.md) | Verify ANCHOR rule cannot bypass SubprocessSandbox boundary | `red-exploit` | pending |
| [TASK-092](./TASK-092-reproduce-iter-9-audit-drift.md) | Reproduce audit's iter-9 drift detection on original audit packet | `ps-validator` | pending |
| [TASK-093](./TASK-093-run-adversary-c4-review.md) | Run /adversary C4 review | `adv-executor` | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-003](../FEAT-003-deterministic-validation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | EN-001, EN-002, EN-003 | Scaffolding + TDD harness + SubprocessSandbox |
| Blocked By | FEAT-001 STORY-001 | Canonical ADR-007 |
| Blocked By | FEAT-002 BUG-004 | seg-NNN regex must be resolved |
| Blocks | STORY-009, STORY-010 | Hook + write pipeline integration |

### Source

- [#273 §C5](https://github.com/geekatron/jerry/issues/273) + [comment 1](https://github.com/geekatron/jerry/issues/273#issuecomment-4339264545)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Story created. ANCHOR-* family — heart of substrate coupling fix. |
