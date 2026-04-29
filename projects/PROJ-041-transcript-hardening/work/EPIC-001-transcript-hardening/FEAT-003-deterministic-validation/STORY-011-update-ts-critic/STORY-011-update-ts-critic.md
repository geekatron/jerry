# STORY-011: Update `ts-critic-extension.md` to consume validator output

> **Type:** story
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-003
> **Owner:** adam.nowak
> **Effort:** 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What needs to happen |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** `ps-critic` running adversarial review on a transcript packet,
**I want** to consume the deterministic validator output as pre-LLM signal,
**So that** my review focuses on substantive content quality rather than burning iterations on mechanically-checkable defects.

---

## Summary

`skills/transcript/ts-critic-extension.md` (or wherever the transcript-specific critic guidance lives) currently relies on LLM interpretation of ADR-007 §4 rules. This Story changes that contract: the critic invokes `jerry transcript verify --json <packet>` first, treats failures as reportable findings without re-judging, and reserves LLM critique cycles for content quality (clarity, completeness, ASR convention adherence in narrative fields, etc.).

This is the integration that closes the loop on the audit's diagnostic: ADR-007 §4 was always intended to be deterministic; we're connecting the critic to the deterministic implementation.

---

## Acceptance Criteria

- [ ] `ts-critic-extension.md` updated to invoke `jerry transcript verify --json <packet>` as Step 1 of review.
- [ ] Critic guidance updated: failures from `verify` become reportable findings without re-judging.
- [ ] Critic guidance updated: LLM judgment focuses on content quality (substantive review), not mechanical rules.
- [ ] Test against the audit packet: critic identifies the iter-9 drift via `verify` output (not via 30-min adversarial discovery).
- [ ] Critic output explicitly references rule_id from validator findings (traceability).
- [ ] `/adversary` C4 ≥0.95 phase gate.

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Locate canonical ts-critic-extension.md (or its successor) | pending |
| TASK-002 | Update Step 1 to invoke verify --json | pending |
| TASK-003 | Update finding format to reference rule_id | pending |
| TASK-004 | Test against audit packet | pending |
| TASK-005 | Run /adversary C4 review | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-003](../FEAT-003-deterministic-validation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | STORY-007 | verify CLI with --json flag |
| Cooperates | EN-008 | Final tournament uses updated critic |

### Source

- [#273 §C5](https://github.com/geekatron/jerry/issues/273) — "ts-critic-extension.md updated to consume the validator's structured output as deterministic pre-LLM signal"

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Story created. |
