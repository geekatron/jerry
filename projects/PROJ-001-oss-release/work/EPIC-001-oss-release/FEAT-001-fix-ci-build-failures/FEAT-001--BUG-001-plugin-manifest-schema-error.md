# BUG-001: Plugin manifest schema error — `keywords` not allowed

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

The Plugin Validation CI check fails with schema validation error: `Additional properties are not allowed ('keywords' was unexpected)`. The plugin manifest contains a `keywords` field that is not permitted by the schema validator.

**Key Details:**
- **Symptom:** Plugin Validation CI check fails with schema error
- **Frequency:** Every CI run (100%)
- **Workaround:** None — blocks CI

---

## Reproduction Steps

### Steps to Reproduce

1. Push any commit to PR #6
2. CI triggers Plugin Validation job
3. Plugin validation runs schema check on manifest

### Expected Result

Plugin validation passes.

### Actual Result

```
Error: Schema validation failed: Additional properties are not allowed ('keywords' was unexpected)
Some validations failed.
```

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | Ubuntu 24.04 (GitHub Actions) |
| **Runtime** | Python 3.14 / uv 0.10.2 |
| **CI Job** | Plugin Validation |

---

## Root Cause Analysis

### Investigation Summary

The `.claude-plugin/manifest.json` (or equivalent) likely contains a `keywords` field that is not defined in the Claude Code plugin schema.

### Root Cause

To be determined — need to inspect the manifest file and schema.

---

## Acceptance Criteria

### Fix Verification

- [ ] Remove or relocate the `keywords` field from the plugin manifest
- [ ] Plugin Validation CI check passes
- [ ] No regression in plugin functionality

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001: Fix CI Build Failures](./FEAT-001-fix-ci-build-failures.md)

### CI Reference

- **CI Run:** [GitHub Actions #21845050753](https://github.com/geekatron/jerry/actions/runs/21845050753/job/63161832093)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-10 | Claude | pending | Bug triaged from PR #6 CI failure |
