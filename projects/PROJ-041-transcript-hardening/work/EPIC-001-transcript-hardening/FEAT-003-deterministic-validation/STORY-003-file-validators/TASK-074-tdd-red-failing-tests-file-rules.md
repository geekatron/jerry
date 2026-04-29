# TASK-074: Author failing tests for FILE-001..003 (TDD Red)

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-003
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Per ADR-007 §4 FILE rule definitions, write parameterized tests against the clean-packet golden that fail until implementations land.

---

## Acceptance Criteria

- [ ] Test cases for FILE-001, FILE-002, FILE-003 exist in tests/transcript/validation/golden/
- [ ] Initial run confirms all 3 tests FAIL with `NotImplementedError`
