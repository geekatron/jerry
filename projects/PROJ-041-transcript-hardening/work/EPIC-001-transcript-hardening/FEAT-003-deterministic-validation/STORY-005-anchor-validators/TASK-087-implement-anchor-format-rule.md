# TASK-087: Implement anchor format rule (ANCHOR-001)

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-005
> **Owner:** eng-backend

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Per ADR-007 §3.1 (post-BUG-004): regex `^seg-\d{3,}$`. Supports disc-NNN once FEAT-004 STORY-015 lands.

---

## Acceptance Criteria

- [ ] ANCHOR format rule passes tests
- [ ] Regex enforces `\d{3,}` (per BUG-004 resolution)
