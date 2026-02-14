# EN-704: Pre-commit Quality Gates

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Set up pre-commit quality gates for L5 Post-Hoc Verification
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-14
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-008
> **Owner:** —
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Proof of completion |
| [Dependencies](#dependencies) | What this depends on |
| [History](#history) | Change log |

---

## Summary

Set up pre-commit quality gates (L5 Post-Hoc Verification). Implements vector V-044 (pre-commit hook validation) to catch violations that escaped runtime enforcement. Pre-commit hooks serve as the last line of defense before code enters version control, providing deterministic, context-rot-immune validation at the git boundary. This complements L3 (PreToolUse) enforcement by catching violations in files that were not routed through the PreToolUse hook.

## Problem Statement

While L3 Pre-Action Gating (EN-703) can block violations at write-time, not all file modifications pass through the PreToolUse hook. Manual edits, external tooling, and edge cases in hook routing can allow non-compliant code to reach the staging area. Without pre-commit gates, these violations enter version control undetected. V-044 scored 4.80 WCS in the EN-402 priority analysis, making it the third highest priority enforcement vector. Pre-commit gates are deterministic, external to the LLM, and immune to context rot.

## Technical Approach

1. **Update pre-commit configuration** -- Configure `.pre-commit-config.yaml` with quality gate hooks that enforce Jerry's coding standards.

2. **Integrate ruff check** -- Add ruff linting as a pre-commit step to enforce code style, import ordering, and common Python issues. Configure to match Jerry's `pyproject.toml` ruff settings.

3. **Add architecture boundary check** -- Create a pre-commit hook that validates layer dependency rules (domain must not import infrastructure, etc.). Reuse AST analysis from EN-703's enforcement engine where possible.

4. **Add type hint validation** -- Configure mypy or a lightweight type hint checker as a pre-commit step to catch missing type annotations on public APIs.

5. **Validate on current codebase** -- Ensure all pre-commit hooks pass on the existing codebase before merging. Fix any pre-existing violations or configure appropriate baselines.

6. **Testing** -- Verify `uv run pytest` passes after all changes.

**Design Source:** EPIC-002 EN-402 (V-044 scored 4.80 WCS), EN-404 (rule enforcement)

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| 1 | Pre-commit configuration updated with quality gates | [ ] |
| 2 | Ruff check integrated as pre-commit step | [ ] |
| 3 | Architecture boundary check as pre-commit step | [ ] |
| 4 | Type hint validation as pre-commit step | [ ] |
| 5 | All pre-commit hooks pass on current codebase | [ ] |
| 6 | `uv run pytest` passes | [ ] |

## Evidence

_No evidence yet. Will be populated during implementation._

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-402 | Enforcement priority analysis (V-044 scored 4.80 WCS) |
| depends_on | EN-404 | Rule-based enforcement design |
| related_to | EN-703 | PreToolUse enforcement engine (L3) -- pre-commit (L5) catches what L3 misses |
| parent | FEAT-008 | Quality Framework Implementation |

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created. Implements L5 Post-Hoc Verification with vector V-044 (pre-commit hook validation). Design sourced from EPIC-002 EN-402 priority analysis and EN-404 rule enforcement. |
