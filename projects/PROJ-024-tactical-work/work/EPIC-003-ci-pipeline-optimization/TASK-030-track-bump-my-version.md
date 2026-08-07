# TASK-030: Track bump-my-version in Dependabot or Scheduled Check

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

`uv tool install 'bump-my-version==1.2.7'` in version-bump.yml is not tracked by Dependabot and has no hash verification. The tool runs with `VERSION_BUMP_PAT` access (contents:write + branch protection bypass). A PyPI compromise of this version would execute in a privileged context with no detection mechanism.

**Finding:** eng-devsecops Finding 7 (MEDIUM) + red-recon FINDING-005, `version-bump.yml:231`

---

## Acceptance Criteria

- [x] bump-my-version added to `[dependency-groups] dev` in pyproject.toml — Dependabot now tracks it
- [x] Decision: **MOVE TO PYPROJECT.TOML** — hash-verified via uv.lock, Dependabot coverage, H-05 consistent
- [x] uv.lock regenerated (103 packages resolved), version-bump.yml uses `uv run bump-my-version`

## Evidence

| Verification | Agent | Result |
|-------------|-------|--------|
| Decision | eng-devsecops | MOVE — supply chain integrity is dominant criterion given VERSION_BUMP_PAT access |
| pyproject.toml | `bump-my-version>=1.2.7` in `[dependency-groups] dev` | Added |
| uv.lock | `uv lock` resolved 103 packages | Regenerated |
| version-bump.yml | `uv tool install` removed, `uv run bump-my-version` used | Updated |
