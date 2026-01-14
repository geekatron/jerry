# BUG-002: Plugin Not Loading

> **Bug ID:** BUG-002
> **Feature:** FT-002 Plugin Loading Fix
> **Enabler:** EN-002
> **Status:** PENDING
> **Severity:** HIGH
> **Created:** 2026-01-14
> **Last Updated:** 2026-01-14

---

## Summary

Jerry plugin does not print a message or interact with the user when started via `claude --plugin-dir`. The SessionStart hook appears to not execute or fails silently.

---

## Symptoms

1. Starting Claude Code with Jerry plugin via `--plugin-dir` shows no Jerry initialization message
2. No `<project-context>` or `<project-required>` output appears
3. Plugin appears to not be active

---

## Reproduction Steps

1. Run: `JERRY_PROJECT=PROJ-007-jerry-bugs CLAUDE_CONFIG_DIR=~/.claude-geek claude --plugin-dir=/path/to/jerry`
2. Expected: Jerry framework initialization message
3. Actual: No message or interaction

---

## Technical Details

### Hook Configuration

**File:** `hooks/hooks.json`

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "PYTHONPATH=\"${CLAUDE_PLUGIN_ROOT}\" uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py",
        "timeout": 10000
      }]
    }]
  }
}
```

### session_start.py Issues

1. **PEP 723 metadata (lines 36-39):**
   ```python
   # /// script
   # requires-python = ">=3.11"
   # dependencies = []
   # ///
   ```
   Empty dependencies, but script imports from `src.infrastructure`.

2. **Module imports (lines 50-57):** Require PYTHONPATH to include plugin root.

### Related PROJ-005 Fixes

PROJ-005 fixed:
- plugin.json and marketplace.json validation errors
- Changed hooks.json to use uv run with PYTHONPATH
- Added PEP 723 metadata to session_start.py

---

## Evidence Chain

| ID | Type | Source | Finding |
|----|------|--------|---------|
| E-001 | Config | `hooks/hooks.json:10` | Command uses PYTHONPATH and uv run |
| E-002 | Code | `session_start.py:38` | `dependencies = []` (empty) |
| E-003 | Code | `session_start.py:50-57` | Imports from src.* modules |
| E-004 | Doc | PROJ-005 PLAN.md | Previous fixes applied |

---

## Proposed Investigation

1. Manually test hook command execution
2. Verify `${CLAUDE_PLUGIN_ROOT}` expansion
3. Check uv run behavior with PYTHONPATH
4. Test session_start.py directly

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Enabler | [en-002.md](./en-002.md) | Investigation enabler |
| Feature | [FEATURE-WORKTRACKER.md](./FEATURE-WORKTRACKER.md) | Parent feature |
| PROJ-005 | [../../PROJ-005-plugin-bugs/](../../PROJ-005-plugin-bugs/) | Previous fixes |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | BUG-002 documented | Claude |
