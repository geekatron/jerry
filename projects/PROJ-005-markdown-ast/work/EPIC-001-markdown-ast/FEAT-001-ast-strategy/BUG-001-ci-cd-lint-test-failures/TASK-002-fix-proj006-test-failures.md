# TASK-002: Fix PROJ-006 test failures

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-02-21
> **Parent:** BUG-001-ci-cd-lint-test-failures
> **Owner:** Claude
> **Effort:** 1

---

## Summary

Fix the 2 pre-existing PROJ-006-multi-instance test failures that block CI on all branches. The project only has a `decisions/` directory but the validation tests require >= 3 category directories.

## Failing Tests

- `tests/project_validation/architecture/test_path_conventions.py::TestProjectIsolation::test_project_has_required_structure[PROJ-006-multi-instance]`
- `tests/project_validation/integration/test_file_resolution.py::TestCoreFilesExist::test_directory_structure_complete[PROJ-006-multi-instance]`

## Acceptance Criteria

- [ ] Both PROJ-006 test assertions pass (or are properly marked xfail/skip)
- [ ] CI test jobs report 0 failures
- [ ] Solution does not mask real validation issues in other projects
