# BUG-002: CLI `projects list` crashes with unhandled exception

> **Type:** bug
> **Status:** pending
> **Priority:** high
> **Impact:** high
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

The `jerry projects list` CLI command crashes with an unhandled exception (traceback on stderr), causing 3 CLI integration tests to fail. The JSON output variant also returns empty/invalid output instead of valid JSON.

**Key Details:**
- **Symptom:** Traceback on stderr, non-zero exit code, invalid JSON output
- **Frequency:** Every CI run (100%)
- **Workaround:** None — blocks CI
- **Affected Tests:**
  - `test_projects_list_returns_zero_exit_code`
  - `test_projects_list_json_contains_projects_key`
  - `test_json_output_is_parseable`

---

## Reproduction Steps

### Steps to Reproduce

1. Run `jerry projects list` in CI environment (no `projects/` directory)
2. Run `jerry --json projects list`

### Expected Result

- Exit code 0
- Valid JSON output with `projects` key

### Actual Result

- Exit code non-zero
- Traceback on stderr
- No JSON output (empty string)

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | Ubuntu 24.04 (GitHub Actions) |
| **Runtime** | Python 3.11-3.14 (all versions) |
| **CI Job** | CLI Integration Tests, Test pip/uv |

---

## Root Cause Analysis

### Investigation Summary

The CLI `projects list` command likely calls into the repository layer which throws a `RepositoryError` when `projects/` directory doesn't exist. This error is not caught by the CLI adapter, resulting in an unhandled exception.

### Root Cause

Likely related to BUG-003 — the `projects/` directory is not present in the CI checkout. The CLI adapter doesn't handle this gracefully.

---

## Acceptance Criteria

### Fix Verification

- [ ] `jerry projects list` returns exit code 0 even when no projects exist
- [ ] `jerry --json projects list` returns valid JSON with empty projects array
- [ ] All 3 CLI integration tests pass
- [ ] Works across Python 3.11-3.14

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001: Fix CI Build Failures](./FEAT-001-fix-ci-build-failures.md)

### Related Bugs

- **BUG-003:** Bootstrap test assumes `projects/` dir exists — likely same root cause

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-10 | Claude | pending | Bug triaged from PR #6 CI failure |
