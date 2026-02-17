# Codebase Analysis: Hook Implementation Current State

> **Agent:** fix-researcher-task006 (Explore stream)
> **Date:** 2026-02-17
> **Source:** Direct codebase exploration

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Overview of findings |
| [Correct Reference Implementation](#1-correct-reference-implementation) | session_start_hook.py pattern |
| [Broken Hook 1: UserPromptSubmit](#2-broken-hook-1-userpromptsubmit) | Missing hookEventName |
| [Broken Hook 2: PreToolUse](#3-broken-hook-2-pretooluse) | Deprecated API + exit codes |
| [Broken Hook 3: SubagentStop](#4-broken-hook-3-subagentstop) | Wrong event + non-standard output |
| [Hook Configuration](#5-hook-configuration-file) | hooks.json issues |
| [Existing Schemas](#6-existing-schema-files) | What schemas exist today |
| [Existing Tests](#7-existing-tests) | Test coverage gaps |
| [Summary Table](#8-summary-table) | All findings at a glance |

---

## Executive Summary

- **1 correct implementation:** `session_start_hook.py` (lines 34-44)
- **3 broken implementations:** Missing or non-standard fields in JSON output
- **Multiple schema violations:** Deprecated API usage, missing fields, non-standard exit codes

---

## 1. CORRECT REFERENCE IMPLEMENTATION

### File: `scripts/session_start_hook.py` (Lines 25-44)

**Status:** CORRECT

**JSON Output Structure:**
```json
{
  "systemMessage": "string",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "string"
  }
}
```

**Key Details:**
- **Exit Code:** Always 0 (fail-open)
- **systemMessage:** Shown to user in terminal (AC-002/AC-003)
- **hookEventName:** Explicitly set to `"SessionStart"`
- **additionalContext:** Added to Claude's context window
- **Error Handling:** Errors still produce valid JSON with both fields

**Lines 25-44:**
```python
def output_json(system_message: str, additional_context: str) -> None:
    print(
        json.dumps(
            {
                "systemMessage": system_message,
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": additional_context,
                },
            }
        )
    )
```

---

## 2. BROKEN HOOK 1: UserPromptSubmit

### File: `hooks/user-prompt-submit.py`

**Status:** BROKEN -- Missing `hookEventName`

**Current JSON Output (Lines 57-63):**
```python
output = {
    "hookSpecificOutput": {
        "additionalContext": (
            f"<quality-reinforcement>\n{result.preamble}\n</quality-reinforcement>"
        ),
    },
}
```

**What It Currently Outputs:**
```json
{
  "hookSpecificOutput": {
    "additionalContext": "<quality-reinforcement>\n...\n</quality-reinforcement>"
  }
}
```

**What It SHOULD Output:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "<quality-reinforcement>\n...\n</quality-reinforcement>"
  }
}
```

**Problems:**
1. **Missing `hookEventName: "UserPromptSubmit"`** -- schema validation requires this field
2. **No systemMessage** -- user sees no feedback at prompt submission time
3. **Line 71:** Fallback on error outputs empty object `{}` instead of valid error structure

**Error Path (Lines 76-83):**
```python
except Exception as e:
    print(json.dumps({"warning": f"L2 reinforcement error: {e}"}), file=sys.stderr)
    print(json.dumps({}))  # Empty object is invalid
    return 0
```

**Impact:** L2 per-prompt quality reinforcement completely non-functional since EN-705 implementation.

---

## 3. BROKEN HOOK 2: PreToolUse

### File: `scripts/pre_tool_use.py`

**Status:** BROKEN -- Deprecated API + Wrong Exit Codes

**Lines where JSON is output:**
- **Line 275:** `{"decision": "block", "reason": ...}`
- **Line 286-289:** `{"decision": "block", "reason": ..., "matches": ...}`
- **Line 301-306:** `{"decision": "ask", "reason": ..., "matches": ...}`
- **Line 336:** `{"decision": "block", "reason": ...}`
- **Line 365:** `{"decision": "approve"}`

**What It Currently Outputs:**
```json
{
  "decision": "approve|block|ask",
  "reason": "optional string",
  "matches": "optional array"
}
```

**What It SHOULD Output:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "optional string"
  }
}
```

**Problems:**

1. **Deprecated Top-Level `decision` Field** (Lines 275, 286, 301, 336, 365)
   - Schema now requires `hookSpecificOutput.permissionDecision`
   - Top-level `decision` field is deprecated

2. **Wrong Decision Values** (Lines 275, 286)
   - Uses `"approve"`/`"block"` (deprecated)
   - Should use `"allow"`/`"deny"` (current API)

3. **Wrong Exit Codes** (Lines 369, 372)
   - Returns exit code `2` on errors
   - **Should always return 0** (fail-open)
   - Current behavior: Errors block tool calls instead of allowing them

4. **Missing `hookEventName`**
   - PreToolUse hooks should identify themselves with `"PreToolUse"`

---

## 4. BROKEN HOOK 3: SubagentStop

### File: `scripts/subagent_stop.py`

**Status:** BROKEN -- Wrong Event Type + Non-Standard Output

**Current JSON Output (Lines 173-186, 190):**
```python
print(json.dumps({
    "action": "handoff",
    "to_agent": to_agent,
    "context": context,
    "work_items": signals.get("work_items", []),
    "summary": signals.get("summary", ""),
    "status_transition": STATUS_TRANSITIONS.get(...),
}))

# Line 190
print(json.dumps({"action": "none", "reason": "No handoff condition matched"}))
```

**What It SHOULD Output:**
```json
{
  "decision": "block|approve",
  "reason": "string"
}
```

**Problems:**
1. **Wrong Event Registration** (hooks.json Lines 40-51) -- under `Stop` instead of `SubagentStop`
2. **Non-Standard Output Fields** (Lines 173-186) -- custom fields not in schema
3. **Missing `hookEventName`** -- should identify as SubagentStop
4. **Stop event doesn't support matchers** -- `"matcher": "subagent:*"` is silently ignored

---

## 5. HOOK CONFIGURATION FILE

### File: `hooks/hooks.json`

**Status:** PARTIALLY BROKEN

**Problems:**
1. **Line 18:** UserPromptSubmit has unnecessary `matcher: "*"` (event doesn't support matchers)
2. **Lines 40-51:** SubagentStop registered under `Stop` event (should be `"SubagentStop"`)

---

## 6. EXISTING SCHEMA FILES

### `schemas/hooks.schema.json` -- Configuration Schema (CORRECT)

Validates `hooks.json` configuration structure. Key: allows `"Stop"` but NOT `"SubagentStop"` in properties -- this may need updating too.

**Missing:** No schemas exist for hook OUTPUT validation. Only configuration registration is validated.

### `schemas/plugin.schema.json` -- Plugin Manifest Schema (CORRECT, unrelated)

---

## 7. EXISTING TESTS

### Contract Tests: `tests/contract/test_hook_output_contract.py`
- Tests ONLY SessionStart hook output
- No tests for UserPromptSubmit, PreToolUse, SubagentStop output

### Hook Unit Tests: `tests/hooks/test_pre_tool_use.py`
- Tests exist but validate the **WRONG** (deprecated) output format
- Example: `assert output["decision"] == "approve"` -- tests the broken format
- These tests will fail once the fix is applied

### Integration Tests: `tests/integration/test_session_start_hook_integration.py`
- Good pattern but only covers SessionStart
- No integration tests for other hooks

---

## 8. SUMMARY TABLE

| Component | File | Status | Issues | Lines |
|-----------|------|--------|--------|-------|
| SessionStart Hook | `scripts/session_start_hook.py` | CORRECT | None | 34-44 |
| UserPromptSubmit Hook | `hooks/user-prompt-submit.py` | BROKEN | Missing hookEventName | 57-63 |
| PreToolUse Hook | `scripts/pre_tool_use.py` | BROKEN | Deprecated API, exit codes | 275,286,301,336,365,369,372 |
| SubagentStop Hook | `scripts/subagent_stop.py` | BROKEN | Wrong event, non-standard | 173-190 |
| hooks.json Config | `hooks/hooks.json` | PARTIAL | Wrong event registration | 18, 40-51 |
| Config Schema | `schemas/hooks.schema.json` | CORRECT | Config only, not output | N/A |
| Contract Tests | `tests/contract/test_hook_output_contract.py` | INCOMPLETE | SessionStart only | all |
| Hook Unit Tests | `tests/hooks/test_pre_tool_use.py` | WRONG FORMAT | Tests deprecated output | 63-349 |
| Integration Tests | `tests/integration/test_session_start_hook_integration.py` | INCOMPLETE | SessionStart only | 59-103 |

---

## 9. KEY FINDINGS FOR SCHEMA CREATION

### Required Schema Files (Don't Exist Yet)
- Hook output schema for SessionStart events (document known-good pattern)
- Hook output schema for UserPromptSubmit events
- Hook output schema for PreToolUse decisions
- Hook output schema for SubagentStop events
- Base/common hook output fields

### Existing Tests That Will Break After Fix
- `tests/hooks/test_pre_tool_use.py` -- validates deprecated `decision` field format
- These tests must be updated alongside the hook fixes in Phase 2

### Configuration Schema Gap
- `schemas/hooks.schema.json` allows `"Stop"` but not `"SubagentStop"` in hook event types
- May need to add `"SubagentStop"` to the allowed events
