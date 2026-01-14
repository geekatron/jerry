# FEATURE-WORKTRACKER: FT-002 Plugin Loading Fix

> **Feature ID:** FT-002
> **Solution Epic:** SE-001
> **Project:** PROJ-007-jerry-bugs
> **Status:** DISCOVERY (Iterating)
> **Created:** 2026-01-14
> **Last Updated:** 2026-01-14

---

## Overview

Fix Jerry plugin not loading when started via `claude --plugin-dir`. The plugin should print a message or interact with the user on session start.

---

## Enablers

| ID | Name | Status | Tasks |
|----|------|--------|-------|
| [EN-002](./en-002.md) | Investigate plugin loading failure | PENDING | See en-002.md |

---

## Discoveries

| ID | Title | Status | Blocks |
|----|-------|--------|--------|
| [disc-001](./disc-001-uv-portability-requirement.md) | uv Portability Requirement | OPEN | UoW-001 |
| disc-002 | CI vs Hook Environment Discrepancy | OPEN | UoW-001 |
| disc-003 | Hooks Inconsistency (uv vs python3) | DOCUMENTED | - |

### disc-001: uv Portability Requirement [OPEN]
ADR-PROJ007-002 proposed `python -m` but this violates portability requirement (must use `uv`). Iterating on correct solution with user.

### disc-002: CI vs Hook Environment Discrepancy [CRITICAL]
**Root Cause for CI Passing but Hook Failing:**
- CI uses: `PYTHONPATH="." uv run src/interface/cli/session_start.py`
- Hook uses: `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" uv run ${CLAUDE_PLUGIN_ROOT}/src/.../session_start.py`
- CI runs from repo root with relative paths
- Hook runs from arbitrary directory with absolute paths
- PEP 723 `dependencies = []` creates isolated env that ignores PYTHONPATH

### disc-003: Hooks Inconsistency [DOCUMENTED]
- SessionStart: uses `uv run` (FAILS due to PEP 723)
- PreToolUse: uses `python3` (WORKS - stdlib only)
- Stop: uses `python3` (WORKS - stdlib only)

---

## Units of Work

| ID | Title | Status | Tasks | Notes |
|----|-------|--------|-------|-------|
| UoW-001 | Implement Plugin Loading Fix | DISCOVERY | TBD | Blocked by disc-001 |

**UoW-001 Blocked Reason:** Cannot implement until uv-compatible solution is validated. See disc-001.

---

## Bugs

| ID | Description | Status | Enabler |
|----|-------------|--------|---------|
| [BUG-002](./bug-002-plugin-not-loading.md) | Plugin not loading/interacting via --plugin-dir | PENDING | EN-002 |

---

## Related Work

| Project | Reference | Description |
|---------|-----------|-------------|
| PROJ-005-plugin-bugs | [WORKTRACKER.md](../../../../PROJ-005-plugin-bugs/WORKTRACKER.md) | Previous plugin fixes |
| PROJ-005 SE-001 | FT-001, FT-002 | Manifest fixes, session_start.py fix |

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

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | FT-002 created | Claude |
| 2026-01-14 | disc-001 created for uv portability requirement | Claude |
| 2026-01-14 | disc-002 identified: CI vs Hook environment discrepancy | Claude |
| 2026-01-14 | disc-003 documented: Hooks inconsistency (uv vs python3) | Claude |
| 2026-01-14 | Added evidence E-004 through E-008 | Claude |
