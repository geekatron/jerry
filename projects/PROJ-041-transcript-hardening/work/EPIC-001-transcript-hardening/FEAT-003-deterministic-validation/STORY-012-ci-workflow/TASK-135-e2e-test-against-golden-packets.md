# TASK-135: End-to-end test: workflow runs against test_data/golden/ on PR; blocks merge on validator failure

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-012
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Live PR test confirms gate behavior.

---

## Acceptance Criteria

- [ ] Test PR with passing validators succeeds CI
- [ ] Test PR with failing validators blocks merge
- [ ] Test PR with insufficient coverage blocks merge
