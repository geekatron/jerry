# TASK-021: Scope pull-requests:write to Coverage-Report Only

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Created:** 2026-04-13
> **Parent:** EPIC-003
> **GitHub Issue:** [#252](https://github.com/geekatron/jerry/issues/252)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

`pull-requests: write` is declared at the workflow level, giving all 29 jobs PR write access. Only `coverage-report` needs it (to post coverage comments). This is an unnecessary attack surface identified by the red-team assessment.

---

## Acceptance Criteria

- [x] Top-level permissions: `contents: read` only
- [x] `coverage-report` job declares its own `permissions: pull-requests: write`
- [x] All other jobs have read-only access
