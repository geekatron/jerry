# TASK-027: Evaluate Replacing MishaKav Coverage Comment Action

> **Type:** task
> **Status:** completed
> **Priority:** medium
> **Created:** 2026-04-15
> **Parent:** EN-006
> **GitHub Issue:** [#252](https://github.com/geekatron/jerry/issues/252)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

`MishaKav/pytest-coverage-comment` is a single-maintainer action processing attacker-generated coverage XML with `pull-requests: write` permission. SHA-pinned (frozen) but represents the weakest third-party trust link. Evaluate replacing with `actions/github-script` to post coverage comments directly, eliminating the third-party dependency.

**Finding:** eng-devsecops Finding 4 (MEDIUM) + red-recon FINDING-001, `ci.yml:371`

---

## Acceptance Criteria

- [x] Alternatives evaluated: github-script (replace), keep with review, remove entirely
- [x] Decision: **REMOVE** — Codecov already receives identical coverage data; PR comments are cosmetic redundancy
- [x] Coverage visibility preserved via Codecov dashboard and PR check status
- [x] `pull-requests: write` eliminated entirely from ci.yml (was only needed for this action)

## Evidence

| Verification | Agent | Result |
|-------------|-------|--------|
| Decision | eng-devsecops | REMOVE — eliminates third-party trust boundary, one fewer job, pull-requests:write dropped |
| Codecov integration intact | ci.yml lines 334-341 | Codecov upload step unchanged in test-uv job |
