# TASK-080: Author failing tests for CONTENT-001..003 (TDD Red)

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-004
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Includes backlinks-format rule per BUG-005 (`<backlinks>` tag canonical, `## Backlinks` H2 rejected).

---

## Acceptance Criteria

- [ ] Test cases for CONTENT-001..003 exist
- [ ] Initial run confirms all FAIL with NotImplementedError
- [ ] Backlinks-format test rejects `## Backlinks` H2 form
