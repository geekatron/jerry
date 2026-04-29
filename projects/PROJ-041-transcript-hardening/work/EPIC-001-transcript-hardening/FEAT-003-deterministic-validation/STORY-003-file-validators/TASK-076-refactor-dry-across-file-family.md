# TASK-076: Refactor for DRY across the 3 FILE rules

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-003
> **Owner:** eng-backend

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Extract common patterns; ensure no duplicated logic.

---

## Acceptance Criteria

- [ ] Common helpers extracted; rule-specific logic remains in each rule
- [ ] Coverage ≥90% on file/ subpackage
