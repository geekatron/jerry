# TASK-001: Add .gitkeep Files to PROJ-002 Category Directories

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Parent:** BUG-003
> **Owner:** Claude
> **Created:** 2026-02-17
> **Effort:** 1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Description and acceptance criteria |
| [History](#history) | Status changes |

---

## Content

### Description

Add `.gitkeep` files to PROJ-002-roadmap-next empty category directories so they are tracked by git. This ensures CI clean checkouts have the required directory structure.

### Acceptance Criteria

- [ ] PROJ-002-roadmap-next `synthesis/.gitkeep` exists
- [ ] PROJ-002-roadmap-next `analysis/.gitkeep` exists
- [ ] Both directories are git-tracked (appear in `git ls-files`)

### Implementation Notes

Pattern follows PROJ-001-oss-release which has `.gitkeep` in `analysis/`, `decisions/`, and `synthesis/`.

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-17 | Created | Initial creation |
