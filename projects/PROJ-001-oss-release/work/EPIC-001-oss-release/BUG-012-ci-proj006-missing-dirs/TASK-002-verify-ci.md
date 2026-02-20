# TASK-002: Verify CI Passes

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

Run the two failing tests locally to verify the fix, then push and confirm CI passes on PR #44.

### Acceptance Criteria

- [x] `test_project_has_required_structure[PROJ-006-multi-instance]` passes locally
- [x] `test_directory_structure_complete[PROJ-006-multi-instance]` passes locally
- [ ] CI on PR #44 passes (pending push)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-20 | pending | Created. Blocked by TASK-001. |
| 2026-02-20 | done | 3332 passed, 63 skipped locally. Pending CI confirmation after push. |
