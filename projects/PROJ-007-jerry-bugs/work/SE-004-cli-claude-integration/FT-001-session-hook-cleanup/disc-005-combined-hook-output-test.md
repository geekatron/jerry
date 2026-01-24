# DISC-005: Combined Hook Output Empirical Test

> **Type:** Discovery (Empirical Test)
> **Feature:** [FT-001](./FEATURE-WORKTRACKER.md) Session Hook Cleanup
> **Solution Epic:** [SE-004](../SOLUTION-WORKTRACKER.md) CLI and Claude Code Integration
> **Project:** PROJ-007-jerry-bugs
> **Status:** CONFIRMED
> **Created:** 2026-01-21
> **Last Updated:** 2026-01-21

---

## Hypothesis

Based on Claude Code documentation:

1. `systemMessage` is listed as a "common field for ALL hooks" ([source](https://code.claude.com/docs/en/hooks#common-json-fields))
2. `hookSpecificOutput.additionalContext` is the SessionStart-specific field ([source](https://code.claude.com/docs/en/hooks#sessionstart-decision-control))

**Hypothesis:** Both fields can be combined in a single SessionStart hook output.

---

## Test Setup

### Test Script

**File:** `scripts/test_combined_hook_output.py`

**Output format:**
```json
{
  "systemMessage": "TEST: systemMessage field is working!\n\nTimestamp: ...\nJERRY_PROJECT: ...\n\nIf you see this in your terminal, systemMessage works with SessionStart hooks.",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "TEST: additionalContext field is working!\n\n<test-context>\nTestTimestamp: ...\nTestProject: ...\n</test-context>\n\nIf Claude can see this, additionalContext works alongside systemMessage."
  }
}
```

### Configuration Change

**File:** `hooks/hooks.json`

**Before:**
```json
"command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session_start_hook.py"
```

**After:**
```json
"command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/test_combined_hook_output.py"
```

**Backup:** `hooks/hooks.json.backup`

---

## Test Procedure

1. **Ensure test configuration is active** (hooks.json points to test script)
2. **Start a new Claude Code session** in this project directory
3. **Observe terminal output** - does `systemMessage` appear?
4. **Ask Claude** "Can you see test-context tags in your context?"
5. **Document results** below

---

## Expected Results

| Field | Expected Behavior |
|-------|-------------------|
| `systemMessage` | Appears in terminal: "TEST: systemMessage field is working!" |
| `additionalContext` | Claude can see `<test-context>` tags in its context |

---

## Actual Results

**Test Date:** 2026-01-21T22:00:12Z
**Claude Code Version:** v2.1.15
**Tester:** Adam Nowak

### Terminal Output

```
❯ JERRY_PROJECT=PROJ-007-jerry-bugs CLAUDE_CONFIG_DIR=~/.claude-geek claude --verbose --plugin-dir=PROJ-007-jerry-bugs/bugs_20260114_performance

▗ ▗   ▖ ▖  Claude Code v2.1.15
           Opus 4.5 · Claude Max
  ▘▘ ▝▝    ~/workspace/GitHub/geekatron/jerry/PROJ-007-jerry-bugs/bugs_20260114_performance
  ⎿  SessionStart:startup hook succeeded: Success
  ⎿  SessionStart:startup says: TEST: systemMessage field is working!

     Timestamp: 2026-01-21T22:00:12.550087+00:00
     JERRY_PROJECT: PROJ-007-jerry-bugs

     If you see this in your terminal, systemMessage works with SessionStart hooks.
```

**Did `systemMessage` appear in terminal?** [x] Yes [ ] No

### Claude Context

**Ask Claude:** "Can you see any test-context tags in your context from the SessionStart hook?"

**Claude's Response:**
```
Yes, I can see the <test-context> tags from the SessionStart hook. Here's what I received:

<test-context>
TestTimestamp: 2026-01-21T22:00:12.550087+00:00
TestProject: PROJ-007-jerry-bugs
TestPurpose: Verify combined systemMessage + hookSpecificOutput.additionalContext
</test-context>

The hook output also included the message: "TEST: additionalContext field is working!"
and "If Claude can see this, additionalContext works alongside systemMessage."

So the combined systemMessage + hookSpecificOutput.additionalContext approach is
working correctly - both fields are being delivered to my context.
```

**Did Claude receive `additionalContext`?** [x] Yes [ ] No

---

## Conclusion

| Outcome | Description |
|---------|-------------|
| **CONFIRMED** | Both fields work together - use combined format |
| ~~PARTIAL~~ | ~~Only one field works - document which one~~ |
| ~~FAILED~~ | ~~Neither field works correctly - investigate~~ |

**Actual Outcome:** **CONFIRMED**

**Evidence:**
- Terminal showed `SessionStart:startup says:` followed by the `systemMessage` content
- Claude confirmed receiving `<test-context>` tags via `additionalContext`
- Both fields delivered successfully in a single JSON output

---

## Impact on EN-001

Based on results:

- [x] Update EN-001 AC-003 to specify combined format
- [x] Update target architecture diagram
- [x] Update hook output examples

### Verified Hook Output Format

```json
{
  "systemMessage": "Jerry Framework initialized.\n\nProject: PROJ-007-jerry-bugs\nPath: projects/PROJ-007-jerry-bugs/\nStatus: Valid and configured",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Jerry Framework initialized.\n<project-context>\nProjectActive: PROJ-007-jerry-bugs\nProjectPath: projects/PROJ-007-jerry-bugs/\nValidationMessage: Project is properly configured\n</project-context>"
  }
}
```

### Field Purposes (Verified)

| Field | Destination | Purpose |
|-------|-------------|---------|
| `systemMessage` | User terminal | User visibility into hook execution |
| `additionalContext` | Claude context | Project information for Claude to use |

---

## Rollback Procedure

To restore original hook after testing:

```bash
# From project root
cp hooks/hooks.json.backup hooks/hooks.json
```

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-21 | Test setup created, awaiting execution | Claude |
| 2026-01-21 | **TEST CONFIRMED**: Both systemMessage and additionalContext work together | Claude |
| 2026-01-21 | Documented results with terminal output and Claude confirmation | Claude |
