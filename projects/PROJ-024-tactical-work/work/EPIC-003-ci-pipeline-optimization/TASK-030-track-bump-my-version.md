# TASK-030: Track bump-my-version in Dependabot or Scheduled Check

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

`uv tool install 'bump-my-version==1.2.7'` in version-bump.yml is not tracked by Dependabot and has no hash verification. The tool runs with `VERSION_BUMP_PAT` access (contents:write + branch protection bypass). A PyPI compromise of this version would execute in a privileged context with no detection mechanism.

**Finding:** eng-devsecops Finding 7 (MEDIUM) + red-recon FINDING-005, `version-bump.yml:231`

---

## Acceptance Criteria

- [ ] bump-my-version either added to pyproject.toml dev deps (Dependabot tracked) or monitored by a scheduled version check
- [ ] Decision documented with rationale
- [ ] If moved to pyproject.toml: uv.lock updated, version-bump.yml uses `uv run bump-my-version`
