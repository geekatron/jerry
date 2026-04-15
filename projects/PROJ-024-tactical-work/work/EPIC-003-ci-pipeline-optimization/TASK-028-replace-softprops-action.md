# TASK-028: Evaluate Replacing softprops Release Action with gh CLI

> **Type:** task
> **Status:** pending
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

`softprops/action-gh-release` is from a personal GitHub account with `contents: write` and `GITHUB_TOKEN` access. Consider migrating to `gh release create` in a shell step, reducing third-party action surface to only `actions/*`, `astral-sh/*`, and `codecov/*`.

**Finding:** eng-devsecops Finding 5 (MEDIUM), `release.yml:264`

---

## Acceptance Criteria

- [ ] Alternatives evaluated (gh CLI, GitHub API via github-script)
- [ ] Decision documented: replace or keep with rationale
- [ ] If replaced: release artifacts, notes, and prerelease detection work identically
- [ ] If kept: added to quarterly third-party action review checklist
