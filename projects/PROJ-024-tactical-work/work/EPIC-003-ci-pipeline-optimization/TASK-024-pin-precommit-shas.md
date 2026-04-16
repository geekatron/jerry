# TASK-024: Pin Pre-Commit Hooks to SHAs

> **Type:** task
> **Status:** completed
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

- [x] All external pre-commit repos pinned to full 40-character commit SHAs
- [x] Version comments preserved alongside SHA pins (e.g., `# v5.0.0`)
- [x] SHAs resolved via GitHub API (`git/ref/tags/{tag}`) — not guessed
- [x] Pre-commit hooks still pass on all files

## Evidence

| Verification | Agent | Result |
|-------------|-------|--------|
| SHA resolution | eng-devsecops | 3 SHAs resolved via GitHub API (all lightweight tags) |
| Attack vector closed | red-recon | CLOSED — tag-mutable supply chain substitution eliminated |
| Reference doc updated | diataxis-reference | Pre-Commit Hook Pinning section added to ci-cd-pipeline-security.md |

| Repo | Tag | SHA |
|------|-----|-----|
| pre-commit/pre-commit-hooks | v5.0.0 | `cef0300fd0fc4d2a87a85fa2093c6b283ea36f4b` |
| astral-sh/ruff-pre-commit | v0.9.2 | `73413df07b4ab0bf103ca1ae73c7cec5c0ace593` |
| commitizen-tools/commitizen | v4.4.1 | `b494c556437473519f8ab69020c7256ba84714c1` |
