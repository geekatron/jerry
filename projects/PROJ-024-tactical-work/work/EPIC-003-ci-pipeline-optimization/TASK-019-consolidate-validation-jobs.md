# TASK-019: Consolidate 6 Validation Jobs into 1

> **Type:** task
> **Status:** completed
> **Priority:** medium
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

Merge lockfile-check, template-validation, frontmatter-validation, license-headers, version-sync, and hard-rule-ceiling into a single `validations` job with sequential steps. Each of these 6 jobs currently spends ~50s on setup for ~5-10s of actual work.

---

## Acceptance Criteria

- [x] Single `validation` job with 6 named steps
- [x] Each step failure clearly identifies which validation failed
- [x] `ci-success` gate references `validation` instead of 6 individual jobs
- [x] Same pass/fail behavior per check
