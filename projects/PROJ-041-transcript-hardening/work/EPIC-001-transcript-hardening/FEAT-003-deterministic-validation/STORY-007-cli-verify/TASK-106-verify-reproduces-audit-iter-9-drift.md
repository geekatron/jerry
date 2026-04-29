# TASK-106: Verify reproduces audit's iter-9 drift detection

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-007
> **Owner:** ps-validator

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Run `jerry transcript verify <iter-9-state-packet>`; confirm drift detected in ~300ms.

---

## Acceptance Criteria

- [ ] CLI detects iter-9 drift on audit packet
- [ ] Total runtime under 1s
- [ ] Verification report persisted
