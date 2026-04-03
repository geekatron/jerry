# BUG-006: Fix file_repository.py Hardcoded Forward Slash (GH #117)

> **Type:** bug
> **Status:** completed
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-03-30T00:00:00Z
> **Due:**
> **Completed:** 2026-03-30T09:00:00Z
> **Severity:** minor
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 1
> **GitHub Issue:** [#117](https://github.com/geekatron/jerry/issues/117)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What's broken |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the bug |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Dependencies](#dependencies) | Relationship to other work |
| [History](#history) | Change log |

---

## Steps to Reproduce

1. Run file_repository.py on Windows
2. Path construction uses "/" instead of `pathlib.Path` / `os.path.join`
3. File operations fail on Windows due to path separator mismatch

---

## Summary

file_repository.py uses hardcoded "/" instead of pathlib for path construction. Breaks on Windows. Same portability theme as GH #113 (statusline fix).

---

## Acceptance Criteria

- [x] All hardcoded "/" path separators in file_repository.py replaced with pathlib
- [x] Existing tests pass
- [x] Path construction works on both Unix and Windows

---

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Independent | -- | No blockers |
| Related | GH #113 | Same portability theme, already closed |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-30 | adam.nowak | pending | Created from PROJ-024 session. Linked to GH #117. |
| 2026-03-30 | adam.nowak | completed | Commit `85a168e0`. Replaced hardcoded separators with pathlib. GH #117 closed. |
