# TASK-092: Reproduce audit's iter-9 drift detection on original audit packet

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-005
> **Owner:** ps-validator

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Validate the substrate-coupling rule actually catches the drift class identified in #273 comment 1.

---

## Acceptance Criteria

- [ ] Run substrate-coupling rule against iter-9 audit packet state
- [ ] Rule detects declared 33 vs walked 32 drift
- [ ] Verification report persisted
