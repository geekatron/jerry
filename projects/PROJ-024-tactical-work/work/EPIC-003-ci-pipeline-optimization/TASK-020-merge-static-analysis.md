# TASK-020: Merge Lint + Type-Check into Static-Analysis

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

Both lint and type-check are single-OS, single-Python static analysis jobs. Combine into one `static-analysis` job with shared setup to eliminate redundant environment setup time.

**Dependency:** TASK-017 (migrate to uv) must complete first -- the merged job will use `uv sync --frozen --extra dev`.

---

## Acceptance Criteria

- [x] Single `static-analysis` job runs ruff check, ruff format, and pyright
- [x] Uses `uv sync --frozen --extra dev` (from TASK-017)
- [x] `ci-success` gate references `static-analysis`
