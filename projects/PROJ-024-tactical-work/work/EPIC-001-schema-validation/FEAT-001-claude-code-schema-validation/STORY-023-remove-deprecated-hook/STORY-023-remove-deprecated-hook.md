# STORY-023: Remove Deprecated scripts/pre_tool_use.py (GH #177)

> **Type:** story
> **Status:** completed
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-03-30T00:00:00Z
> **Due:**
> **Completed:** 2026-03-30T12:00:00Z
> **Parent:** FEAT-001
> **Owner:**
> **Effort:** 1
> **GitHub Issue:** [#177](https://github.com/geekatron/jerry/issues/177)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What and why |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Dependencies](#dependencies) | Relationship to other work |
| [History](#history) | Change log |

---

## Summary

`scripts/pre_tool_use.py` is deprecated since #150 migration to plugin hooks. Dead code that bypasses the Jerry CLI. Any security guardrail logic it contains MUST be ported into the CLI enforcement pipeline (Clean Architecture) before deletion -- not replaced with another standalone script.

---

## Architectural Constraints

| Constraint | Rationale |
|------------|-----------|
| **MUST NOT introduce new scripts** | Standalone scripts increase surface area, bypass CLI testing infrastructure, and create parallel code paths that drift from the CLI implementation. |
| **All hook logic MUST route through Jerry CLI** | Hooks invoke `uv run jerry ...` commands. The CLI is the single entry point; enforcement logic lives in `src/` under Clean Architecture layers. |
| **MUST follow Clean Architecture** | Any security guardrail logic migrated from this script goes into the appropriate hexagonal layer: domain (rules), application (handlers), infrastructure (adapters). |
| **MUST NOT leave orphaned test dependencies** | `scripts/tests/test_hooks.py` tests this script. Those tests must be updated or removed as part of this work. |
| **MUST follow TDD Red/Green/Refactor (H-20)** | Write failing tests for CLI-based enforcement BEFORE porting logic. Red: test fails because CLI doesn't have the check. Green: port logic, test passes. Refactor: clean up. |

---

## Acceptance Criteria

- [x] `scripts/pre_tool_use.py` deleted
- [x] Any security guardrail logic not already in the CLI enforcement pipeline is ported to `src/` (Clean Architecture)
- [x] No remaining imports or references to the old hook in active code/config
- [x] Documentation references updated (CHANGELOG, playbooks) to point to CLI enforcement
- [x] `scripts/tests/test_hooks.py` updated to test CLI-based enforcement (not deleted script)
- [x] Pre-commit hooks still pass
- [x] CI pipeline still passes
- [x] Zero new files in `scripts/` (no script replacement)

---

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocks | STORY-024 | Consolidate hooks after deprecated one is removed |
| Blocks | BUG-005 | Hook infrastructure must be clean before fixing hook tests |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-30 | adam.nowak | pending | Created from PROJ-024 session. Linked to GH #177. |
| 2026-03-30 | adam.nowak | completed | Commit `1597e224`. Deleted script, rewrote 5 test files for CLI pipeline. 16,352 tests green. GH #177 closed. |
