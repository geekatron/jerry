# TASK-034: Add Dependabot Pre-Commit Ecosystem Entry

> **Type:** task
> **Status:** completed
> **Priority:** low
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

Dependabot has no `pre-commit` ecosystem entry. External pre-commit repos will not receive automated update PRs. Combined with floating tags (TASK-024), this means known-vulnerable hook versions persist without alerting.

**Finding:** eng-devsecops Finding 11 (LOW), `.github/dependabot.yml` (missing entry)
**Dependency:** TASK-024 must complete first (SHA pins must be in place before Dependabot can track them)

---

## Acceptance Criteria

- [x] Dependabot `pre-commit` ecosystem evaluated — supported (GA 2026-03-10)
- [x] Entry added to dependabot.yml: `package-ecosystem: "pre-commit"`, weekly Monday, `chore` prefix, limit 5
- [x] Dependabot will open PRs for SHA-pinned hooks in `.pre-commit-config.yaml`

## Evidence

| Verification | Agent | Result |
|-------------|-------|--------|
| Ecosystem supported | eng-devsecops | GA 2026-03-10 per GitHub Changelog |
| Entry added | dependabot.yml lines 240-272 | `package-ecosystem: "pre-commit"` with weekly schedule |
| D5 comment updated | eng-devsecops | `chore` prefix documented, Filter B interaction noted |
