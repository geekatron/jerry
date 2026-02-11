# BUG-005: Project validation tests reference non-existent PROJ-001-plugin-cleanup

> **Type:** bug
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Severity:** major
> **Created:** 2026-02-10
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-001
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

### Root Cause

The project validation tests are parameterized with `PROJ-001-plugin-cleanup`, but:
1. The project directory and artifacts were never committed to git, OR
2. They were removed/gitignored during cleanup, OR
3. The tests need to discover projects dynamically rather than hardcoding

### Fix Options

1. **Remove hardcoded project reference** — Make tests discover available projects
2. **Commit minimal project artifacts** — Add PROJ-001-plugin-cleanup skeleton to git
3. **Skip when no projects** — Skip validation tests when no projects directory exists
4. **Use test fixtures** — Create temporary project structure in test setup

---

## Acceptance Criteria

### Fix Verification

- [ ] All 4 project validation tests pass in CI
- [ ] Tests don't depend on uncommitted project artifacts
- [ ] Fix works across Python 3.11-3.14

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001: Fix CI Build Failures](./FEAT-001-fix-ci-build-failures.md)

### Related Bugs

- **BUG-003:** Bootstrap test assumes `projects/` dir exists — related missing directory issue

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-10 | Claude | pending | Bug triaged from PR #6 CI failure |
