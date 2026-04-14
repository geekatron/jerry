# TASK-016: Remove Pip Test Matrix (8 Jobs)

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

Remove the `test-pip` job (8 matrix cells) from the CI pipeline. Jerry mandates uv-only (H-05). The pip matrix tests an installation path that users are forbidden from taking. Saves ~8 jobs and ~20-30 min compute per run.

**Dependency:** TASK-017 (migrate to uv) must complete first -- pip matrix removal should follow uv migration to ensure all jobs use the correct toolchain.

---

## Acceptance Criteria

- [x] `test-pip` job removed from ci.yml
- [x] `ci-success` gate updated to remove `test-pip` from `needs:`
- [x] `coverage-report` updated if it references `test-pip`
- [x] uv test matrix (8 cells) unchanged
