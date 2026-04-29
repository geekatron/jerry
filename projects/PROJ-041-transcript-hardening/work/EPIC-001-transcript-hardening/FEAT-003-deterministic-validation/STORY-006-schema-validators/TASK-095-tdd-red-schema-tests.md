# TASK-095: Author failing tests for SCHEMA-001..008 (TDD Red); include large-packet golden

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-006
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Tests parameterize over the 8 SCHEMA rule_ids.

---

## Acceptance Criteria

- [ ] Test cases for SCHEMA-001..008 exist
- [ ] Includes large-packet test (forward-compat regex)
- [ ] Initial run all FAIL with NotImplementedError
