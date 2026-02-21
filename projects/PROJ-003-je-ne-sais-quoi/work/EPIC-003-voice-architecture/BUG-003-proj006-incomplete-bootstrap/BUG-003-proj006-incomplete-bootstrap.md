# BUG-003: Project Validation Tests Enforce Undocumented Category Directory Requirement

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
CREATED: 2026-02-20 (Claude)
PURPOSE: Document CI/CD failure caused by tests enforcing non-existent directory requirement
-->

> **Type:** bug
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** 2026-02-20
> **Parent:** EPIC-003
> **Owner:** Claude
> **Found In:** 0.5.0
> **Fix Version:** 0.5.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What the bug is |
| [Reproduction Steps](#reproduction-steps) | How to reproduce |
| [Environment](#environment) | Where it occurs |
| [Root Cause Analysis](#root-cause-analysis) | Why it happens |
| [Fix Description](#fix-description) | What was changed |
| [Acceptance Criteria](#acceptance-criteria) | When it's fixed |
| [Related Items](#related-items) | Hierarchy and links |
| [History](#history) | Change log |

---

## Summary

Two project validation tests enforce an undocumented requirement that each project must have at least 3 "category directories" (research, synthesis, analysis, decisions, reports). This requirement does not exist in the authoritative worktracker directory structure specification (`worktracker-directory-structure.md`), which only requires `PLAN.md`, `WORKTRACKER.md`, and `work/`. When PROJ-006 was bootstrapped with the correct minimal structure, these tests failed, blocking all CI test matrix jobs across all branches.

**Key Details:**
- **Symptom:** All test matrix CI jobs fail with `AssertionError: Project should have at least 3 category directories, found: ['decisions']`
- **Frequency:** Every CI run on every branch since PROJ-006 was merged to main
- **Workaround:** None for CI. Local tests can `--deselect` the 2 failing tests.

---

## Reproduction Steps

### Prerequisites

- Jerry Framework repository with PROJ-006-multi-instance present

### Steps to Reproduce

1. Push any branch that includes PROJ-006 (present on main since `5adece9`)
2. CI triggers test matrix across all Python versions and OS combinations
3. All test-pip and test-uv jobs fail

### Expected Result

All project validation tests pass. Projects with the minimum required structure (PLAN.md, WORKTRACKER.md, work/) should be valid.

### Actual Result

2 tests fail across every matrix combination:

```
FAILED tests/project_validation/architecture/test_path_conventions.py::TestProjectIsolation::test_project_has_required_structure[PROJ-006-multi-instance]
FAILED tests/project_validation/integration/test_file_resolution.py::TestCoreFilesExist::test_directory_structure_complete[PROJ-006-multi-instance]
```

---

## Environment

| Attribute | Value |
|-----------|-------|
| **CI Platform** | GitHub Actions |
| **Test Matrix** | pip + uv, Python 3.11-3.14, ubuntu/macos/windows |
| **Introducing Commit** | `5adece9` (feat(proj-006): bootstrap automated multi-instance orchestration project) |
| **Affected Runs** | All runs since merge to main (PR #41 runs 22221122436, 22221133679) |

---

## Root Cause Analysis

### Investigation Summary

The tests were originally written in commit `5fa1848` (BUG-001 path validation) for PROJ-001 specifically. They were hardcoded to match PROJ-001's directory structure, which happened to have research, synthesis, analysis, decisions, and reports directories. When migrated in `b34f591` (TD-005) from PROJ-001-scoped to framework-level parameterized tests, the `proj_001_root` fixture was generalized to `proj_root` (parameterized over all projects), but the "at least 3 category directories" assertion was carried forward without verifying it against the authoritative directory structure specification.

### Root Cause

**The tests enforce a requirement that doesn't exist.** The authoritative source for project directory structure (`skills/worktracker/rules/worktracker-directory-structure.md`) requires only `PLAN.md`, `WORKTRACKER.md`, and `work/`. Category directories (research, synthesis, analysis, decisions, reports) are optional — they emerge as projects produce artifacts, not as a bootstrap requirement.

The "at least 3 category dirs" check was an artifact of PROJ-001's mature directory structure being treated as a universal requirement during test migration.

### Contributing Factors

- Test migration (TD-005) generalized fixtures but not assertions — the PROJ-001-specific structure check became a universal check
- No review caught the mismatch between the test assertion and the worktracker directory structure spec
- PROJ-006 was the first project bootstrapped after the tests were generalized, exposing the discrepancy

---

## Fix Description

### Solution Approach

Align the tests with the authoritative directory structure specification. Replace the "at least 3 category directories" assertion with the actual requirement: `work/` directory must exist. `PLAN.md` and `WORKTRACKER.md` are already checked by separate test methods.

### Changes Made

- Removed category directory count assertion from `test_project_has_required_structure`
- Replaced with `work/` directory existence check
- Removed category directory count assertion from `test_directory_structure_complete`
- Replaced with `work/` directory existence check

### Code References

| File | Change Description |
|------|-------------------|
| `tests/project_validation/architecture/test_path_conventions.py:84-98` | Replaced category dirs assertion with `work/` check |
| `tests/project_validation/integration/test_file_resolution.py:69-77` | Replaced category dirs assertion with `work/` check |

---

## Acceptance Criteria

### Fix Verification

- [x] `test_project_has_required_structure[PROJ-006-multi-instance]` passes
- [x] `test_directory_structure_complete[PROJ-006-multi-instance]` passes
- [x] All project validation tests pass (151 passed, 24 skipped)
- [x] Full test suite passes (3329 passed, 66 skipped)

### Quality Checklist

- [x] Existing tests still passing
- [x] No new issues introduced

---

## Related Items

### Hierarchy

- **Parent:** [EPIC-003: Voice Architecture](../EPIC-003-voice-architecture.md)

### Related Items

- **Related Bug:** [BUG-001: CI/CD Pipeline Failures on PR #37](../../EPIC-001-je-ne-sais-quoi/BUG-001-cicd-pipeline-failures/BUG-001-cicd-pipeline-failures.md) (prior CI/CD fix, original source of tests)
- **Causing Change:** Commit `5fa1848` (test migration TD-005) — generalized PROJ-001 tests to all projects without updating assertions
- **Exposing Change:** Commit `5adece9` (PROJ-006 bootstrap) — first minimal-structure project
- **Fix Commit:** `tests/project_validation/architecture/test_path_conventions.py`, `tests/project_validation/integration/test_file_resolution.py`
- **Authoritative Spec:** `skills/worktracker/rules/worktracker-directory-structure.md`

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Bug filed. Initially attributed to PROJ-006 incomplete bootstrap. |
| 2026-02-20 | Claude | completed | RCA corrected: tests enforce undocumented requirement, not PROJ-006. Fixed tests to align with worktracker-directory-structure.md spec. 3329 tests passing. |

---
