# TASK-086: Author failing tests for ANCHOR-001..003 (TDD Red); cover declared-vs-walked drift

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-005
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Test cases include the substrate-coupling rule that walks declared patterns through SubprocessSandbox.

---

## Acceptance Criteria

- [ ] Test cases for ANCHOR-001..003 exist
- [ ] Drift-detection test loads drift-detected golden and expects substrate-coupling rule FAIL
- [ ] Initial run all FAIL with NotImplementedError
