# FEATURE-WORKTRACKER: FT-002 Plugin Loading Fix

> **Feature ID:** FT-002
> **Solution Epic:** SE-001
> **Project:** PROJ-007-jerry-bugs
> **Status:** DISCOVERY (Validating Solution)
> **Target Version:** v0.2.0
> **Created:** 2026-01-14
> **Last Updated:** 2026-01-14

---

## Overview

Fix Jerry plugin not loading when started via `claude --plugin-dir`. The plugin should print a message or interact with the user on session start.

**Root Cause:** PEP 723 inline metadata (`dependencies = []`) causes `uv run` to create an isolated environment that ignores PYTHONPATH, breaking `from src.infrastructure.*` imports.

**Proposed Solution:** Remove PEP 723 metadata so `uv run` uses project's `pyproject.toml`.

---

## Enablers

| ID | Name | Status | Tasks |
|----|------|--------|-------|
| EN-002 | Investigate plugin loading failure | COMPLETE | Done via orchestration |
| [EN-003](./en-003-validate-solution.md) | Validate Solution Hypothesis | COMPLETE ✅ | 4/4 tasks done |

---

## Technical Debt

| ID | Title | Status | Creates |
|----|-------|--------|---------|
| [TD-002](./td-002-ci-test-coverage-gap.md) | CI Test Coverage Gap | DOCUMENTED | UoW-002 (v0.3.0+) |
| [TD-003](./td-003-hooks-execution-inconsistency.md) | Hooks Execution Inconsistency | DOCUMENTED | UoW-003 (v0.3.0+) |

---

## Discoveries

| ID | Title | Status | Blocks |
|----|-------|--------|--------|
| [disc-001](./disc-001-uv-portability-requirement.md) | uv Portability Requirement | RESOLVED ✅ | ~~UoW-001~~ (unblocked) |
| disc-002 | CI vs Hook Environment Discrepancy | OPEN | → TD-002 |
| disc-003 | Hooks Inconsistency (uv vs python3) | DOCUMENTED | → TD-003 |

### disc-001: uv Portability Requirement [RESOLVED ✅]
**Solution validated via EN-003:** Remove PEP 723 inline metadata from session_start.py. This allows `uv run` to use the project's pyproject.toml instead of creating an isolated environment.

### disc-002: CI vs Hook Environment Discrepancy [CRITICAL → TD-002]
**Root Cause for CI Passing but Hook Failing:**
- CI uses: `PYTHONPATH="." uv run src/interface/cli/session_start.py`
- Hook uses: `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" uv run ${CLAUDE_PLUGIN_ROOT}/src/.../session_start.py`
- PEP 723 `dependencies = []` creates isolated env that ignores PYTHONPATH

### disc-003: Hooks Inconsistency [DOCUMENTED → TD-003]
- SessionStart: uses `uv run` (FAILS due to PEP 723)
- PreToolUse: uses `python3` (WORKS - stdlib only)
- Stop: uses `python3` (WORKS - stdlib only)

---

## Units of Work

| ID | Title | Status | Tasks | Blocked By |
|----|-------|--------|-------|------------|
| [UoW-001](./uow-001-implement-plugin-loading-fix.md) | Implement Plugin Loading Fix | READY ✅ | 12 tasks (TDD/BDD) | ~~EN-003~~ (unblocked) |

### UoW-001: TDD/BDD Task Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| RED (Failing Tests) | T-001, T-002, T-003 | PENDING |
| GREEN (Implement) | T-004, T-005 | PENDING |
| REFACTOR | T-006, T-007 | PENDING |
| Quality Gates | T-008 - T-012 | PENDING |

**Acceptance Criteria:**
- AC-001: Hook executes from any working directory
- AC-002: Output matches contract format
- AC-003: Full test suite passes (≥80% coverage)
- AC-004: CI pipeline passes
- AC-005: User verification via `claude --plugin-dir`

---

## Bugs

| ID | Description | Status | Resolved By |
|----|-------------|--------|-------------|
| [BUG-002](./bug-002-plugin-not-loading.md) | Plugin not loading/interacting via --plugin-dir | INVESTIGATING | UoW-001 |

---

## Related Work

| Project | Reference | Description |
|---------|-----------|-------------|
| PROJ-005-plugin-bugs | [WORKTRACKER.md](../../../../PROJ-005-plugin-bugs/WORKTRACKER.md) | Previous plugin fixes |
| PROJ-005 SE-001 | FT-001, FT-002 | Manifest fixes, session_start.py fix |
| PROJ-005 ADR | PROJ-005-e-010 | uv + PEP 723 decision (prior art) |

---

## Evidence

| ID | Type | Source | Relevance |
|----|------|--------|-----------|
| E-001 | Config | `hooks/hooks.json:4-14` | SessionStart hook configuration |
| E-002 | Code | `session_start.py:36-39` | PEP 723 metadata (empty dependencies) |
| E-003 | Code | `session_start.py:50-57` | Imports from src.infrastructure |
| E-004 | CI | `.github/workflows/ci.yml:126` | CI uses `PYTHONPATH="."` (differs from hook) |
| E-005 | Config | `hooks/hooks.json:16-27` | PreToolUse uses `python3` (not uv) |
| E-006 | Config | `hooks/hooks.json:28-38` | Stop uses `python3` (not uv) |
| E-007 | Code | `scripts/pre_tool_use.py` | Only stdlib imports (no src.*) |
| E-008 | Code | `scripts/subagent_stop.py` | Only stdlib imports (no src.*) |

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Solution Tracker | [../SOLUTION-WORKTRACKER.md](../SOLUTION-WORKTRACKER.md) | Parent SE-001 |
| Investigation | [../../../investigations/](../../../investigations/) | ps-investigator report |
| Hook Config | `hooks/hooks.json` | Hook configuration |
| Plugin Manifest | `.claude-plugin/plugin.json` | Plugin definition |
| ADR (needs correction) | `decisions/ADR-PROJ007-002-*.md` | Plugin loading fix decision |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | FT-002 created | Claude |
| 2026-01-14 | disc-001 created for uv portability requirement | Claude |
| 2026-01-14 | disc-002 identified: CI vs Hook environment discrepancy | Claude |
| 2026-01-14 | disc-003 documented: Hooks inconsistency (uv vs python3) | Claude |
| 2026-01-14 | Added evidence E-004 through E-008 | Claude |
| 2026-01-14 | EN-002 marked COMPLETE (investigation done via orchestration) | Claude |
| 2026-01-14 | EN-003 created for solution validation | Claude |
| 2026-01-14 | TD-002 created from disc-002 | Claude |
| 2026-01-14 | TD-003 created from disc-003 | Claude |
| 2026-01-14 | UoW-001 detailed with TDD/BDD tasks (12 tasks) | Claude |
| 2026-01-14 | EN-003 COMPLETE: Solution validated (all 4 tests passed) | Claude |
| 2026-01-14 | disc-001 RESOLVED: PEP 723 removal confirmed as solution | Claude |
| 2026-01-14 | UoW-001 UNBLOCKED: Ready for TDD/BDD implementation | Claude |
