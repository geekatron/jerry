# BUG-005: Project validation tests reference non-existent PROJ-001-plugin-cleanup

> **Type:** bug
> **Status:** done
> **Priority:** medium
> **Impact:** medium
> **Severity:** major
> **Created:** 2026-02-10
> **Due:** —
> **Completed:** 2026-02-11
> **Parent:** EN-002
> **Owner:** —
> **Found In:** PR #6
> **Fix Version:** —

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Reproduction Steps](#reproduction-steps) | Steps to reproduce the issue |
| [Environment](#environment) | Environment where bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Investigation and root cause |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related items |
| [History](#history) | Status changes |

---

## Summary

Four project validation tests fail because they reference `PROJ-001-plugin-cleanup`, which does not exist in the repository. The tests expect project artifacts (PLAN.md, WORKTRACKER.md, category directories) that were never committed.

**Key Details:**
- **Symptom:** Missing PLAN.md, WORKTRACKER.md, and category directories for PROJ-001-plugin-cleanup
- **Frequency:** Every CI run (100%)
- **Workaround:** None — blocks CI
- **Affected Tests:**
  - `test_project_has_required_structure[PROJ-001-plugin-cleanup]`
  - `test_worktracker_exists[PROJ-001-plugin-cleanup]`
  - `test_plan_exists[PROJ-001-plugin-cleanup]`
  - `test_directory_structure_complete[PROJ-001-plugin-cleanup]`

---

## Reproduction Steps

### Steps to Reproduce

1. Clone repository fresh
2. Run `uv run pytest tests/project_validation/`

### Expected Result

Tests pass or are parameterized against actually existing projects.

### Actual Result

```
AssertionError: Missing required file: PLAN.md
AssertionError: Missing WORKTRACKER.md
AssertionError: Missing category directories. Found: [], expected at least 3 of: ['research', 'synthesis', 'analysis', 'decisions', 'reports', 'design']
```

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | Ubuntu 24.04 (GitHub Actions) |
| **Runtime** | Python 3.11-3.14 (all versions) |
| **CI Job** | Test pip/uv (all variants) |

---

## Root Cause Analysis

### Investigation Summary

The test file `tests/project_validation/conftest.py` contains:

```python
# Line 114-117
@pytest.fixture(params=["PROJ-001-plugin-cleanup"])
def project_id(request):
    return request.param
```

The `project_id` fixture is hardcoded to `["PROJ-001-plugin-cleanup"]`. The conftest also has a `discover_projects()` function (lines 29-41) that can dynamically find projects in the `projects/` directory, but **it is not used** for the `project_id` fixture parameterization.

The actual project in the repository is `PROJ-001-oss-release` (our new project), not `PROJ-001-plugin-cleanup` (which was a previous development-era project that was never committed to git).

### Root Cause

**Hardcoded stale project ID.** The `project_id` fixture in `tests/project_validation/conftest.py` is hardcoded to `PROJ-001-plugin-cleanup`, which does not exist in the repository. The dynamic `discover_projects()` function exists but is not wired into the fixture. Tests validate structure against ADR-003 (category directories: research, synthesis, analysis, decisions, reports, design, etc.).

### Fix Options

1. **Use dynamic discovery** — Wire `discover_projects()` into the `project_id` fixture parameterization
2. **Update hardcoded ID** — Change to `PROJ-001-oss-release` (the existing project)
3. **Combine both** — Use dynamic discovery with fallback, and ensure PROJ-001-oss-release has required structure

**Recommended:** Option 1 (dynamic discovery) — most robust and prevents future breakage.

### Files Involved

| File | Role | Change Needed |
|------|------|---------------|
| `tests/project_validation/conftest.py` | Test fixture | Change `project_id` fixture to use `discover_projects()` |
| `projects/PROJ-001-oss-release/` | Project directory | May need category directories (research, analysis, etc.) |

---

## Children (Tasks)

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| [TASK-001](./BUG-005--TASK-001-wire-dynamic-project-discovery.md) | Wire dynamic project discovery into project_id fixture | done | medium |
| [TASK-002](./BUG-005--TASK-002-create-category-directories.md) | Create required category directories in PROJ-001-oss-release | done | medium |

**Dependency:** Both TASK-001 and TASK-002 are required for tests to pass. TASK-001 makes the fixture discover `PROJ-001-oss-release`. TASK-002 ensures it has the required structure. They can be implemented in parallel but both must be committed together.

---

## Acceptance Criteria

### Fix Verification

- [x] All 4 project validation tests pass (68 passed, 1 skipped locally)
- [x] Tests don't depend on uncommitted project artifacts (dynamic discovery)
- [ ] Fix works across Python 3.11-3.14 (pending CI verification)

---

## Related Items

### Hierarchy

- **Parent:** [EN-002: Fix Test Infrastructure](./EN-002-fix-test-infrastructure.md)
- **Feature:** [FEAT-001: Fix CI Build Failures](../FEAT-001-fix-ci-build-failures.md)

### Children

- [TASK-001: Wire dynamic project discovery into project_id fixture](./BUG-005--TASK-001-wire-dynamic-project-discovery.md)
- [TASK-002: Create required category directories in PROJ-001-oss-release](./BUG-005--TASK-002-create-category-directories.md)

### Related Bugs

- **BUG-003:** Bootstrap test assumes `projects/` dir exists — related missing directory issue

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-10 | Claude | pending | Bug triaged from PR #6 CI failure |
| 2026-02-10 | Claude | pending | Root cause confirmed: `project_id` fixture in conftest.py hardcoded to `PROJ-001-plugin-cleanup` (doesn't exist). Dynamic `discover_projects()` exists but isn't used. |
| 2026-02-11 | Claude | pending | TASK-001 (dynamic discovery) and TASK-002 (category directories) created. Both required for tests to pass. |
| 2026-02-11 | Claude | done | Both tasks completed. TASK-001: Module-level dynamic discovery with sentinel pattern, adversarial critic feedback incorporated. TASK-002: synthesis/, analysis/, decisions/ dirs + orchestration in valid_categories. All 68 project validation tests pass. Committed in `4789625`. |
