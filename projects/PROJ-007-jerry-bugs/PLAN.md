# PROJ-007: Jerry Performance and Plugin Bugs

> **Project ID:** PROJ-007-jerry-bugs
> **Status:** IN PROGRESS
> **Branch:** bugs/bugs-20260114-performance
> **Created:** 2026-01-14
> **Last Updated:** 2026-01-14

---

## Overview

This project addresses two critical bugs in the Jerry Framework:

1. **Performance Degradation**: Lock files accumulating in `.jerry/local/locks/` without cleanup, causing session slowdowns
2. **Plugin Not Loading**: Jerry plugin not initializing when started via `claude --plugin-dir`

---

## Problem Statement

### BUG-001: Lock File Accumulation (Performance)

**Symptom:** As sessions with Claude using Jerry grow, Claude Code slows down.

**Root Cause (Preliminary):** `AtomicFileAdapter` creates lock files in `.jerry/local/locks/` for every file operation but never cleans them up. Currently 97 empty lock files accumulated.

**Impact:**
- Directory scan overhead on every lock acquisition
- Storage bloat
- Potential file descriptor exhaustion over time

**Evidence:**
- `.jerry/local/locks/` contains 97 `.lock` files (all 0 bytes)
- `AtomicFileAdapter._get_lock_path()` creates but never removes lock files
- ADR-006 acknowledges: "Lock file cleanup needed for crashed processes" but cleanup was never implemented

### BUG-002: Plugin Not Loading

**Symptom:** When running `JERRY_PROJECT=PROJ-007-jerry-bugs CLAUDE_CONFIG_DIR=~/.claude-geek claude --plugin-dir=...`, the Jerry plugin doesn't print a message or interact.

**Related Work:** PROJ-005-plugin-bugs fixed manifest validation and session_start.py to use uv run.

**Current Hook Configuration:**
```json
"SessionStart": [{
  "command": "PYTHONPATH=\"${CLAUDE_PLUGIN_ROOT}\" uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py"
}]
```

**Potential Issues:**
1. uv run not finding the src/ modules
2. PYTHONPATH expansion not working correctly
3. Hook execution silently failing

---

## Solution Strategy

### Phase 1: Investigation

Use ps-investigator methodology:
- 5 Whys root cause analysis
- Evidence chain documentation
- Corrective action planning

### Phase 2: Implementation

1. **Lock File Cleanup:**
   - Option A: Cleanup old lock files at session start
   - Option B: Add TTL-based cleanup to AtomicFileAdapter
   - Option C: Use lock file adjacent to data file (per ADR-006 original design)

2. **Plugin Loading:**
   - Verify hook execution
   - Debug PYTHONPATH handling
   - Test uv run in plugin context

### Phase 3: Verification

- Performance metrics before/after
- End-to-end plugin installation test
- Regression test suite

---

## Work Hierarchy

```
WORKTRACKER.md (Global Manifest)
└── SE-001: Performance and Plugin Bug Fixes
    ├── FT-001: Lock File Cleanup [PENDING]
    │   └── EN-001: Investigate lock file accumulation [IN PROGRESS]
    └── FT-002: Plugin Loading Fix [PENDING]
        └── EN-002: Investigate plugin loading failure [PENDING]
```

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Investigation | [investigations/](./investigations/) | ps-investigator reports |
| PROJ-005 Reference | [../PROJ-005-plugin-bugs/](../PROJ-005-plugin-bugs/) | Previous plugin bug fixes |
| ADR-006 | [PROJ-001 design/](../PROJ-001-plugin-cleanup/design/ADR-006-file-locking-strategy.md) | File locking strategy |

---

## Files Under Investigation

| File | Relevance |
|------|-----------|
| `src/infrastructure/adapters/persistence/atomic_file_adapter.py` | Lock file creation (BUG-001) |
| `src/interface/cli/session_start.py` | Session hook that uses AtomicFileAdapter |
| `hooks/hooks.json` | Hook configuration |
| `.claude-plugin/plugin.json` | Plugin manifest |
| `.jerry/local/locks/` | Accumulated lock files |

---

*Last Updated: 2026-01-14*
