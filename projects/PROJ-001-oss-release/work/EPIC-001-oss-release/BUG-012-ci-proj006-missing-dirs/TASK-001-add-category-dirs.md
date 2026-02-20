# TASK-001: Add Missing Category Directories to PROJ-006

> **Type:** task
> **Status:** done
> **Priority:** high
> **Created:** 2026-02-20
> **Parent:** BUG-012-ci-proj006-missing-dirs
> **Owner:** Claude
> **Effort:** 1

---

## Content

### Description

Add `research/`, `synthesis/`, and `analysis/` directories with `.gitkeep` sentinel files to `PROJ-006-multi-instance project root.`. Git does not track empty directories, so `.gitkeep` files are required.

### Acceptance Criteria

- [x] `PROJ-006-multi-instance project root.research/.gitkeep` exists
- [x] `PROJ-006-multi-instance project root.synthesis/.gitkeep` exists
- [x] `PROJ-006-multi-instance project root.analysis/.gitkeep` exists
- [x] PROJ-006 has at least 3 category directories

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-20 | in_progress | Created. Adding .gitkeep files. |
| 2026-02-20 | done | .gitkeep files added + research/README.md placeholder. |
