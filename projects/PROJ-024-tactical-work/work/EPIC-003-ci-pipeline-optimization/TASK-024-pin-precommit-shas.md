# TASK-024: Pin Pre-Commit Hooks to SHAs

> **Type:** task
> **Status:** pending
> **Priority:** high
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

Three external pre-commit repos use floating version tags instead of SHAs: `pre-commit/pre-commit-hooks` (v5.0.0), `astral-sh/ruff-pre-commit` (v0.9.2), `commitizen-tools/commitizen` (v4.4.1). A force-pushed tag silently replaces code that runs with full developer machine access. The `ruff` hook has `--fix` enabled, meaning it writes to the working tree.

**Finding:** eng-devsecops Finding 1 (HIGH), `.pre-commit-config.yaml:24,42,205`

---

## Acceptance Criteria

- [ ] All external pre-commit repos pinned to full 40-character commit SHAs
- [ ] Version comments preserved alongside SHA pins (e.g., `# v5.0.0`)
- [ ] `pre-commit autoupdate --freeze` run or equivalent manual SHA resolution
- [ ] Pre-commit hooks still pass on all files
