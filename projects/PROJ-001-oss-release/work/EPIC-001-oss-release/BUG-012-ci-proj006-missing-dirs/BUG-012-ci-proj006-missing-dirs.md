# BUG-012: CI Failures — PROJ-006 Incomplete Project Directory Structure

> **Type:** bug
> **Status:** completed
> **Completed:** 2026-02-20
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-20
> **Parent:** EPIC-001-oss-release
> **Owner:** Claude
> **Found In:** 0.3.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Steps to Reproduce](#steps-to-reproduce) | Schema-required reproduction stub |
| [Reproduction Steps](#reproduction-steps) | Steps to reproduce the issue |
| [Environment](#environment) | Environment where bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Investigation and root cause details |
| [Fix Description](#fix-description) | Solution approach and changes made |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related work items |
| [History](#history) | Status changes and key events |

---

## Summary

Two project validation tests fail for PROJ-006-multi-instance because the project was bootstrapped with only a `decisions/` directory, but tests require at least 3 of the expected category directories.

---

## Steps to Reproduce

See [Reproduction Steps](#reproduction-steps) below for full details.

**Key Details:**
- **Symptom:** 2 test failures on PR #44 CI: `test_project_has_required_structure[PROJ-006-multi-instance]` and `test_directory_structure_complete[PROJ-006-multi-instance]`
- **Frequency:** Every CI run
- **Workaround:** None — blocks PR merge

---

## Reproduction Steps

### Prerequisites

- Branch `feat/proj-001-oss-documentation` checked out
- `uv sync` completed

### Steps to Reproduce

1. Run `uv run pytest tests/project_validation/architecture/test_path_conventions.py::test_project_has_required_structure -k PROJ-006`
2. Run `uv run pytest tests/project_validation/integration/test_file_resolution.py::test_directory_structure_complete -k PROJ-006`

### Expected Result

Both tests pass — PROJ-006 has at least 3 category directories.

### Actual Result

Both tests fail:
- `test_path_conventions.py`: "Project should have at least 3 category directories, found: ['decisions']"
- `test_file_resolution.py`: "Missing category directories. Found: ['decisions'], expected at least 3 of: ['research', 'synthesis', 'analysis', 'decisions', 'reports', 'design']"

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | macOS / GitHub Actions (ubuntu-latest) |
| **Runtime** | Python 3.12, uv |
| **Application Version** | 0.3.0 |
| **Configuration** | Default pytest configuration |

---

## Root Cause Analysis

### Root Cause

PROJ-006-multi-instance was bootstrapped (commit `5adece9`) with only a `decisions/` directory. The project structure validation tests (introduced earlier for all projects) require at least 3 of `[research, synthesis, analysis, decisions, reports, design]`. This is the same root cause as BUG-003 (EPIC-003) which fixed PROJ-002.

### Contributing Factors

- Empty directories are not tracked by git — need `.gitkeep` sentinel files
- PROJ-006 was bootstrapped minimally without full category directory scaffolding

---

## Fix Description

### Solution Approach

Add missing category directories with `.gitkeep` files to PROJ-006-multi-instance, following the same pattern used in BUG-003 (EPIC-003) for PROJ-002.

### Changes Made

- Add `research/.gitkeep` to PROJ-006-multi-instance
- Add `synthesis/.gitkeep` to PROJ-006-multi-instance
- Add `analysis/.gitkeep` to PROJ-006-multi-instance

---

## Acceptance Criteria

### Fix Verification

- [x] `test_project_has_required_structure[PROJ-006-multi-instance]` passes
- [x] `test_directory_structure_complete[PROJ-006-multi-instance]` passes
- [x] No new test failures introduced (3332 passed, 63 skipped)

---

## Related Items

### Hierarchy

- **Parent:** [EPIC-001-oss-release](../EPIC-001-oss-release.md)

### Related Items

- **Related Bug:** [BUG-003 (EPIC-003)](../../EPIC-003-quality-implementation/BUG-003-ci-pipeline-proj002-missing-dirs/BUG-003-ci-pipeline-proj002-missing-dirs.md) — Same root cause for PROJ-002
- **PR:** [PR #44](https://github.com/geekatron/jerry/pull/44) — FEAT-028 MCP Tool Integration

### Children

| ID | Title | Status |
|----|-------|--------|
| [TASK-001](./TASK-001-add-category-dirs.md) | Add missing category directories to PROJ-006 | in_progress |
| [TASK-002](./TASK-002-verify-ci.md) | Verify CI passes | pending |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Initial report. 2 test failures on PR #44 CI. |
| 2026-02-20 | Claude | in_progress | Root cause identified (same as BUG-003). Fix in progress. |
| 2026-02-20 | Claude | done | Added research/, synthesis/, analysis/ with .gitkeep + research/README.md. 3332 tests pass. |
