# TD-003: Hooks Execution Inconsistency

> **Technical Debt ID:** TD-003
> **Feature:** FT-002-plugin-loading-fix
> **Project:** PROJ-007-jerry-bugs
> **Status:** DOCUMENTED
> **Priority:** Low
> **Created:** 2026-01-14
> **Target Version:** v0.3.0+ (Evaluate)

---

## Summary

Plugin hooks use inconsistent execution methods: SessionStart uses `uv run` while PreToolUse and Stop use `python3`. This works by accident but violates the principle of consistent user journey.

---

## Evidence

| Hook | Command | Works? | Reason |
|------|---------|--------|--------|
| SessionStart | `uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py` | ❌ NO* | PEP 723 creates isolated env |
| PreToolUse | `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/pre_tool_use.py` | ✅ YES | Only uses stdlib |
| Stop | `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/subagent_stop.py` | ✅ YES | Only uses stdlib |

*Will be fixed by UoW-001 (remove PEP 723)

---

## Root Cause Analysis

**Why PreToolUse and Stop work with `python3`:**
```python
# scripts/pre_tool_use.py - ONLY stdlib imports
import json
import os
import sys
from pathlib import Path
```

**Why SessionStart fails with `uv run`:**
```python
# src/interface/cli/session_start.py - Imports from src.*
from src.infrastructure.adapters.persistence.filesystem_project_adapter import (
    FilesystemProjectAdapter,
)
```

The scripts in `scripts/` are self-contained stdlib-only scripts. The scripts in `src/` import from the project structure.

---

## Current State (Acceptable?)

After UoW-001 fix:
- SessionStart: `uv run` with project's pyproject.toml (works)
- PreToolUse: `python3` with system Python (works)
- Stop: `python3` with system Python (works)

**Question:** Is this inconsistency acceptable, or should all hooks use `uv run` for consistency?

---

## Risk Assessment

| Option | Risk | Benefit |
|--------|------|---------|
| Keep as-is | Low | Scripts work, minimal change |
| Standardize to uv | Medium | Consistency, but may break working scripts |
| Standardize to python3 | High | SessionStart needs src.* imports |

---

## Recommendation

**Evaluate in v0.3.0+**: After UoW-001 fix is validated, assess whether standardizing hooks to `uv run` provides meaningful benefit vs. risk of breaking working scripts.

---

## Work Items

| Type | ID | Description | Version |
|------|-----|-------------|---------|
| UoW | UoW-003 | Standardize hooks execution (if decided) | v0.3.0+ |

---

## Related Artifacts

| Type | Reference |
|------|-----------|
| Discovery | disc-003 (Hooks Inconsistency) |
| Hook Config | `hooks/hooks.json` |
| Script | `scripts/pre_tool_use.py` |
| Script | `scripts/subagent_stop.py` |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | TD-003 created from disc-003 findings | Claude |
