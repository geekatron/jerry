# TASK-028: Evaluate Replacing softprops Release Action with gh CLI

> **Type:** task
> **Status:** completed
> **Priority:** medium
> **Created:** 2026-04-15
> **Completed:** 2026-04-16
> **Parent:** EN-006
> **GitHub Issue:** [#252](https://github.com/geekatron/jerry/issues/252)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |
| [Evidence](#evidence) | Verification record |

---

## Summary

`softprops/action-gh-release` is from a personal GitHub account with `contents: write` and `GITHUB_TOKEN` access. Consider migrating to `gh release create` in a shell step, reducing third-party action surface to only `actions/*`, `astral-sh/*`, and `codecov/*`.

**Finding:** eng-devsecops Finding 5 (MEDIUM), `release.yml:264`

---

## Acceptance Criteria

- [x] Alternatives evaluated: gh CLI (replace) vs keep with quarterly review
- [x] Decision: **REPLACE** with `gh release create` — first-party CLI, pre-installed on runners
- [x] Release artifacts, notes, and prerelease detection work identically (conditional `--prerelease` flag)
- [x] `softprops/action-gh-release` removed from pipeline — one fewer third-party action with contents:write

## Evidence

| Verification | Agent | Result |
|-------------|-------|--------|
| Decision | eng-devsecops | REPLACE — gh CLI handles all features; eliminates personal-account action trust |
| Exact YAML provided | eng-devsecops | `gh release create` with conditional --prerelease, --notes-file, glob artifact upload |
