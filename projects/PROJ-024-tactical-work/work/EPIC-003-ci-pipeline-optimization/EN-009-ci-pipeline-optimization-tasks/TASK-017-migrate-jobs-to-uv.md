# TASK-017: Migrate Lint, Type-Check, Security to UV

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Created:** 2026-04-13
> **Completed:** 2026-04-13
> **Parent:** EN-009
> **GitHub Issue:** [#252](https://github.com/geekatron/jerry/issues/252)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Replace `pip install` with `uv sync --frozen` in 3 CI jobs (lint, type-check, security). The `type-check` job currently resolves deps against live PyPI with no lockfile protection -- this is a supply chain risk. This task eliminates 4 H-05 violations and closes 1 supply chain gap.

This task is a prerequisite for TASK-016 (remove pip matrix) and TASK-020 (merge static-analysis).

---

## Acceptance Criteria

- [x] lint job uses `uv run ruff` instead of `pip install ruff`
- [x] type-check job uses `uv sync --frozen --extra dev` + `uv run pyright`
- [x] security job uses `uv export` + `pip-audit` against full lockfile
- [x] Zero `pip install` commands remain in ci.yml (except test-pip if kept as smoke test)
