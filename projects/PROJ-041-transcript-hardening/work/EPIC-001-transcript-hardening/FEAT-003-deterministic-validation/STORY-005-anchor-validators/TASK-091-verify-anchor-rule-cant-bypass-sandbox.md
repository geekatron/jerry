# TASK-091: Verify ANCHOR rule cannot bypass SubprocessSandbox boundary

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-005
> **Owner:** red-exploit

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Re-uses EN-004 Phase 4 work; targeted check on this rule's surface.

---

## Acceptance Criteria

- [ ] red-exploit attempts ≥3 bypass classes against the rule
- [ ] All blocked by SubprocessSandbox
- [ ] Engagement findings persisted in STORY-005 directory
