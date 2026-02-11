# BUG-003: Bootstrap test assumes `projects/` directory exists

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

The bootstrap integration test `test_dispatcher_can_dispatch_query_e2e` fails with `RepositoryError: Projects directory does not exist: /home/runner/work/jerry/jerry/projects`. The test assumes a `projects/` directory exists in the repository, but this directory is not committed to git (it's a local workspace artifact).

**Key Details:**
- **Symptom:** `RepositoryError: Projects directory does not exist`
- **Frequency:** Every CI run (100%)
- **Workaround:** None — blocks CI

---

## Reproduction Steps

### Steps to Reproduce

1. Clone repository fresh (no local `projects/` directory)
2. Run `uv run pytest tests/integration/test_bootstrap.py::TestBootstrapEdgeCases::test_dispatcher_can_dispatch_query_e2e`

### Expected Result

Test passes or gracefully handles missing directory.

### Actual Result

```
RepositoryError: Projects directory does not exist: /home/runner/work/jerry/jerry/projects
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

The `projects/` directory is not committed to git. It is created locally when users set up projects. The bootstrap test and repository adapter do not handle the case where this directory is absent.

### Fix Options

1. **Create `projects/` in CI** — Add `mkdir -p projects` step in CI workflow
2. **Commit `projects/.gitkeep`** — Ensure directory always exists in repo
3. **Fix adapter** — Handle missing directory gracefully (create or return empty)
4. **Fix test** — Mock or set up the directory in test fixtures

---

## Acceptance Criteria

### Fix Verification

- [ ] `test_dispatcher_can_dispatch_query_e2e` passes in CI
- [ ] Repository adapter handles missing `projects/` directory gracefully
- [ ] Fix works across Python 3.11-3.14

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001: Fix CI Build Failures](./FEAT-001-fix-ci-build-failures.md)

### Related Bugs

- **BUG-002:** CLI `projects list` crashes — likely same root cause (missing `projects/` dir)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-10 | Claude | pending | Bug triaged from PR #6 CI failure |
