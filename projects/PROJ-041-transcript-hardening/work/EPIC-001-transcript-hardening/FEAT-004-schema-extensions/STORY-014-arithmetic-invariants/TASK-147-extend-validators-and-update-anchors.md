# TASK-147: Extend FEAT-003 SCHEMA-* validators + update-anchors to recompute and refresh `computed`

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-014
> **Owner:** eng-backend

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

FEAT-003 STORY-008 update-anchors gets a hook to refresh `arithmetic_invariants.computed` field at write time.

---

## Acceptance Criteria

- [ ] SCHEMA-* validator catches arithmetic_invariants mismatch
- [ ] update-anchors refreshes `computed` field automatically
- [ ] match boolean automatically maintained
