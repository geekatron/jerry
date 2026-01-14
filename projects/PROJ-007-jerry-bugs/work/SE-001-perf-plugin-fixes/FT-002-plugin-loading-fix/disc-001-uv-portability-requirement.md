# disc-001: uv Portability Requirement Discovery

> **Discovery ID:** disc-001
> **Date:** 2026-01-14
> **Feature:** FT-002-plugin-loading-fix
> **Status:** OPEN (Iterating)
> **Author:** Adam Nowak, Claude

---

## Summary

During review of ADR-PROJ007-002, a critical requirement gap was identified: **the project MUST use `uv` for portability**, but the proposed solution (`python -m` instead of `uv run`) abandons `uv` entirely.

---

## Context

### PROJ-005 Prior Art

PROJ-005 evaluated and decided on `uv run` with PEP 723 inline metadata (ADR PROJ-005-e-010). Key decisions:

| Decision | Rationale |
|----------|-----------|
| Use `uv run` | Automatic dependency resolution, no manual env activation |
| PEP 723 metadata | Inline script dependencies, self-contained |
| Requirement: `uv` on user system | Acceptable trade-off for portability |

**Reference Documents:**
- `projects/PROJ-005-plugin-bugs/decisions/PROJ-005-e-010-adr-uv-session-start.md`
- `projects/PROJ-005-plugin-bugs/research/PROJ-005-e-008-uv-dependency-management.md`

### The Problem

PROJ-007 investigation (BUG-002) correctly identified the root cause:
- PEP 723 `dependencies = []` tells uv "I have no dependencies"
- uv creates an isolated environment with only declared dependencies
- Isolated environment ignores PYTHONPATH
- `from src.infrastructure...` imports fail

**But the proposed solution in ADR-PROJ007-002 was wrong:**
```json
// Proposed (INCORRECT - abandons uv)
"command": "cd ${CLAUDE_PLUGIN_ROOT} && python -m src.interface.cli.session_start"
```

This violates the portability requirement established in PROJ-005.

---

## Critical Questions

### Q1: Why is uv required for portability?

**Answer:** The project must work across different environments without requiring manual `pip install` or virtual environment activation. `uv` provides:
- Automatic environment management
- Reproducible environments via lockfiles
- No activation required
- Cross-platform support

### Q2: What else needs to work with uv besides session_start.py?

**Identified scope:**
1. **CLI** - `jerry` command (`src/interface/cli/main.py`)
2. **Session hook** - `jerry-session-start` (`src/interface/cli/session_start.py`)
3. **Test suite** - pytest runs (`tests/`)
4. **Other hooks** - PreToolUse, Stop hooks

### Q3: How do tests currently run?

**Current configuration (pyproject.toml):**
```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

Tests require `src/` to be on Python path. If we use `uv run pytest`, we need to ensure the project context is available.

### Q4: What are the entry points?

**From pyproject.toml:**
```toml
[project.scripts]
jerry = "src.interface.cli.main:main"
jerry-session-start = "src.interface.cli.session_start:main"
```

These entry points only work after `pip install -e .` but we want to avoid that for plugin portability.

---

## Hypothesis: Correct Solution

### Option A: `uv run python -m` (Hybrid)

Use `uv` for environment management but invoke as a Python module:

```json
"command": "cd ${CLAUDE_PLUGIN_ROOT} && uv run python -m src.interface.cli.session_start"
```

**How it works:**
1. `cd ${CLAUDE_PLUGIN_ROOT}` - Set working directory to project root
2. `uv run python` - Use uv's Python with project dependencies
3. `-m src.interface.cli.session_start` - Run as module (not script)

**Key difference from direct script execution:**
- Does NOT trigger PEP 723 inline metadata parsing
- uv manages environment based on `pyproject.toml`
- `src/` is discoverable via module path

### Option B: Remove PEP 723 metadata

Remove the conflicting metadata from `session_start.py`:

```python
# REMOVE these lines:
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
```

Then `uv run script.py` would not create an isolated environment.

### Option C: Use uv with --no-project flag

```bash
uv run --no-project python session_start.py
```

This tells uv to not treat the directory as a project.

---

## Interactive Q&A Session (2026-01-14)

### Q1: Why is uv required for portability? [ANSWERED]

**User Question:** Why can't we just use `python -m`?

**Answer:** The project must work across different environments without requiring manual `pip install` or virtual environment activation. `uv` provides:
- Automatic environment management
- Reproducible environments via lockfiles
- No activation required
- Cross-platform support

The PROJ-005 prior art (ADR PROJ-005-e-010) explicitly chose `uv run` for these reasons.

---

### Q2: What is the full scope beyond session_start.py? [IDENTIFIED]

**User Concern:** "It's not just the `src.interface.cli.session_start` module alone but we're supposed to have a CLI that we can use."

**Identified Scope:**
1. **CLI** - `jerry` command (`src/interface/cli/main.py`)
2. **Session hook** - `jerry-session-start` (`src/interface/cli/session_start.py`)
3. **Test suite** - pytest runs (`tests/`)
4. **Other hooks** - PreToolUse, Stop hooks

---

### Q3: Why aren't tests catching regressions? [CRITICAL FINDING]

**User Question:** "The *.toml may have it setup correctly but if that's the case why aren't we catching whenever we regress in the project with this functionality?"

**Investigation Result: CI vs Hook Discrepancy**

The CI tests differently than the actual hook executes:

| Environment | PYTHONPATH | Command |
|------------|------------|---------|
| **CI (line 126)** | `PYTHONPATH="."` | `uv run src/interface/cli/session_start.py` |
| **Actual Hook** | `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}"` | `uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py` |

**Key Differences:**
1. CI uses relative path `"."` vs hook uses absolute path `"${CLAUDE_PLUGIN_ROOT}"`
2. CI runs from repo root; hook runs from wherever Claude is launched
3. CI sets working directory implicitly; hook doesn't `cd` first

**This explains why CI passes but the actual hook fails.**

---

### Q4: Do other hooks (PreToolUse, Stop) work? [CONFIRMED WORKING]

**User Intuition:** "I bet you will be able to get them working because you are launching the scripts directly."

**Investigation Result: Hooks Inconsistency Discovered**

From `hooks/hooks.json`:
```json
{
  "SessionStart": [{
    "command": "PYTHONPATH=\"${CLAUDE_PLUGIN_ROOT}\" uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py"
  }],
  "PreToolUse": [{
    "command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/pre_tool_use.py"
  }],
  "Stop": [{
    "command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/subagent_stop.py"
  }]
}
```

| Hook | Uses | Works? | Why |
|------|------|--------|-----|
| SessionStart | `uv run` | ❌ NO | PEP 723 isolated env ignores PYTHONPATH |
| PreToolUse | `python3` | ✅ YES | Only uses stdlib (no `src.` imports) |
| Stop | `python3` | ✅ YES | Only uses stdlib (no `src.` imports) |

**Why PreToolUse/Stop work:** These scripts (`scripts/pre_tool_use.py`, `scripts/subagent_stop.py`) only import from Python stdlib:
```python
import json
import os
import sys
from pathlib import Path
```

They do NOT import from `src.infrastructure.*` so they don't need PYTHONPATH or uv's environment.

---

### Q5: Why are we trying to go hybrid with uv and pip? [USER REJECTION]

**User Feedback:** "Why wouldn't we be able to achieve this consistency? Why are we trying to go hybrid with `uv` and `pip`?"

**Clarification:** User requires **SAME user journey** for:
- Plugin User (via `claude --plugin-dir`)
- Developer User (local development)

**Constraint:** No hybrid approach. Use `uv` consistently everywhere.

---

## Critical Discoveries Summary

### Discovery 1: CI Tests Differently Than Production

```
┌─────────────────────────────────────────────────────────────┐
│ CI ENVIRONMENT                                              │
│ PYTHONPATH="."                                              │
│ Working dir: /repo/                                         │
│ Command: uv run src/interface/cli/session_start.py          │
│ Result: ✅ PASSES                                            │
└─────────────────────────────────────────────────────────────┘
         ≠ (NOT EQUAL)
┌─────────────────────────────────────────────────────────────┐
│ PLUGIN ENVIRONMENT                                          │
│ PYTHONPATH="${CLAUDE_PLUGIN_ROOT}"                          │
│ Working dir: (wherever claude is launched)                  │
│ Command: uv run ${CLAUDE_PLUGIN_ROOT}/src/.../session_start │
│ Result: ❌ FAILS                                             │
└─────────────────────────────────────────────────────────────┘
```

**Root Cause:** PEP 723 `dependencies = []` causes uv to create an isolated environment that ignores PYTHONPATH entirely.

### Discovery 2: Hooks Are Inconsistent

SessionStart uses `uv run` while other hooks use `python3`. This works by accident because:
- Scripts in `scripts/` only use stdlib
- Scripts in `src/interface/cli/` import from `src.infrastructure.*`

### Discovery 3: Entry Points Only Work After pip install

```toml
[project.scripts]
jerry = "src.interface.cli.main:main"
jerry-session-start = "src.interface.cli.session_start:main"
```

These require `pip install -e .` which violates portability for plugin mode.

---

## Corrected Solution Path

### Requirement: Consistent uv-only Approach

All hooks and CLI invocations must:
1. Use `uv run` (not `python3` or `python -m`)
2. Work without `pip install -e .`
3. Work regardless of working directory

### Proposed Fix: Remove PEP 723 Isolated Environment

**Option B (Recommended):** Remove PEP 723 inline metadata from `session_start.py`:

```python
# REMOVE these lines that cause isolated environment:
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
```

**Why this works:**
- Without PEP 723 metadata, `uv run script.py` uses project's `pyproject.toml`
- Project dependencies and PYTHONPATH are respected
- Consistent behavior between CI and production

### Alternative: Change Hook to Use python -m

```json
"command": "cd ${CLAUDE_PLUGIN_ROOT} && uv run python -m src.interface.cli.session_start"
```

**Why this might work:**
- `uv run python` uses project's Python
- `-m` treats `src.interface.cli.session_start` as a module
- Does NOT trigger PEP 723 parsing

**Needs validation.**

---

## Open Questions for Iteration

1. **Option B validation:** Does removing PEP 723 metadata fix the issue without side effects?

2. **`cd` approach:** Should hooks `cd` to plugin root first?
   ```json
   "command": "cd ${CLAUDE_PLUGIN_ROOT} && PYTHONPATH=. uv run ..."
   ```

3. **Test coverage gap:** Should CI be updated to test with same paths as hooks?
   - Add test that uses `${CLAUDE_PLUGIN_ROOT}` pattern
   - Or: test from different working directory

4. **Consistency audit:** Should PreToolUse and Stop also use `uv run` for consistency?
   - Even though they work now, future scripts might need `src.` imports

---

## Next Steps

1. **Validate Option B** - Test removing PEP 723 metadata
2. **Update CI** - Add test that mimics actual hook environment
3. **Update ADR-PROJ007-002** - After validation, correct the solution
4. **Consistency pass** - Consider updating all hooks to use `uv run`

---

## Related Artifacts

| Artifact | Path |
|----------|------|
| PROJ-005 uv ADR | `projects/PROJ-005-plugin-bugs/decisions/PROJ-005-e-010-adr-uv-session-start.md` |
| PROJ-005 uv Research | `projects/PROJ-005-plugin-bugs/research/PROJ-005-e-008-uv-dependency-management.md` |
| PROJ-007 ADR (needs correction) | `projects/PROJ-007-jerry-bugs/decisions/ADR-PROJ007-002-plugin-loading-fix.md` |
| PROJ-007 Investigation | `orchestration/.../investigations/bug-002-e-001-investigation.md` |
| pyproject.toml | `pyproject.toml` |

---

## Relationships

| Type | ID | Description |
|------|-----|-------------|
| BLOCKS | UoW-002 | Cannot implement until solution validated |
| RELATED_TO | BUG-002 | Root cause for plugin not loading |
| REFERENCES | PROJ-005-e-010 | Prior art on uv decision |
| MAY_CREATE | EN-XXX | Enabler for test suite uv integration |

---

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | Discovery created | Claude |
| 2026-01-14 | Added Q&A session findings | Claude |
| 2026-01-14 | Documented CI vs Hook discrepancy | Claude |
| 2026-01-14 | Identified hooks inconsistency (uv vs python3) | Claude |
| 2026-01-14 | User rejected hybrid approach - uv-only required | Adam Nowak |

---

*Discovery created: 2026-01-14*
*Last Updated: 2026-01-14*
*Status: OPEN - Iterating on solution validation*
