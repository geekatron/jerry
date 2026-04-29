# TASK-111: Probe for race condition / partial-write window via concurrent write simulation

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-008
> **Owner:** red-exploit

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Two parallel update-anchors invocations against the same packet — one must succeed cleanly, the other should fail or queue.

---

## Acceptance Criteria

- [ ] Race-condition probe report persisted in STORY-008 directory
- [ ] No partial-write state observed across 100+ concurrent invocations
