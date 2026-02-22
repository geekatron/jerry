# TASK-001: Fix ruff lint errors in r01_poc.py

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-02-21
> **Parent:** BUG-001-ci-cd-lint-test-failures
> **Owner:** Claude
> **Effort:** 1

---

## Summary

Fix or exclude the 32 ruff lint errors in `r01_poc.py` that cause the CI "Lint & Format" job to fail.

## Acceptance Criteria

- [ ] `ruff check .` returns 0 errors
- [ ] CI "Lint & Format" job passes
- [ ] Approach chosen: exclude PoC path from ruff, fix inline, or delete file
