# fix-creator-task003 Validation Report

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Tasks completed and root causes addressed |
| [RC-5 Fix: Output Format](#rc-5-fix-output-format) | Replacing custom JSON with SubagentStop schema |
| [RC-6 Fix: Exit Code](#rc-6-fix-exit-code) | Correcting exit code for no-handoff path |
| [RC-4 Fix: hooks.json](#rc-4-fix-hooksjson) | Correcting event registration and matchers |
| [Preserved Logic](#preserved-logic) | What was intentionally left unchanged |
| [File Diff Summary](#file-diff-summary) | Line-by-line change summary |
| [Validation Checklist](#validation-checklist) | Change-by-change verification |
| [Known Limitation](#known-limitation) | GitHub Issue #20221 |

---

## Summary

Agent: fix-creator-task003
Task: TASK-003 (subagent_stop.py) + TASK-004 (hooks.json)
Date: 2026-02-17
Status: COMPLETE

Three root causes were addressed across two files:

| RC | File | Bug | Fix Applied |
|----|------|-----|-------------|
| RC-5 | subagent_stop.py | Custom JSON format not understood by Claude Code | Replaced with SubagentStop schema: `{"decision": "block", "reason": "..."}` |
| RC-6 | subagent_stop.py | Exit code 1 for "no handoff" treated as error | Changed to exit 0 with empty JSON `{}` |
| RC-4 | hooks.json | Hook registered under wrong event (`Stop` with `subagent:*` matcher) | Moved to `SubagentStop` event; removed unsupported matchers |

---

## RC-5 Fix: Output Format

**File**: `/Users/adam.nowak/workspace/GitHub/geekatron/jerry-gitwt/PROJ-001-oss-release-cont/scripts/subagent_stop.py`

**Before** (lines 173-186 in original):
```python
print(
    json.dumps(
        {
            "action": "handoff",
            "to_agent": to_agent,
            "context": context,
            "work_items": signals.get("work_items", []),
            "summary": signals.get("summary", ""),
            "status_transition": STATUS_TRANSITIONS.get(
                signals.get("handoff_condition", ""), None
            ),
        }
    )
)
return 0
```

**After**:
```python
print(
    json.dumps(
        {
            "decision": "block",
            "reason": f"Handoff required: route to {to_agent}. Context: {context}",
            "systemMessage": f"Agent handoff: {agent_name} -> {to_agent}. {context}",
        }
    )
)
return 0
```

**Why**: The SubagentStop schema only accepts `decision`, `reason`, and `systemMessage` (plus base fields). The old `action`/`to_agent`/`context`/`work_items`/`summary`/`status_transition` fields are not part of the schema and are silently ignored by Claude Code. The `additionalProperties: false` schema constraint confirms these fields are invalid. Setting `decision: "block"` with a `reason` is the correct way to prevent the subagent from stopping.

---

## RC-6 Fix: Exit Code

**File**: `/Users/adam.nowak/workspace/GitHub/geekatron/jerry-gitwt/PROJ-001-oss-release-cont/scripts/subagent_stop.py`

**Before** (lines 190-191 in original):
```python
print(json.dumps({"action": "none", "reason": "No handoff condition matched"}))
return 1
```

**After**:
```python
# No handoff needed — allow the subagent to stop normally
print(json.dumps({}))
return 0
```

**Why**: In Claude Code hooks, any non-zero exit code signals an error condition. Exit code 1 on the "no handoff" path was incorrectly treated as a hook failure, not a normal no-op. The correct behavior is exit 0 with empty JSON `{}`, which tells Claude Code: hook ran successfully, no intervention needed, allow the subagent to stop.

---

## RC-4 Fix: hooks.json

**File**: `/Users/adam.nowak/workspace/GitHub/geekatron/jerry-gitwt/PROJ-001-oss-release-cont/hooks/hooks.json`

### Change 1: Wrong event name (`Stop` -> `SubagentStop`)

**Before**:
```json
"Stop": [
  {
    "matcher": "subagent:*",
    "hooks": [...]
  }
]
```

**After**:
```json
"SubagentStop": [
  {
    "hooks": [...]
  }
]
```

**Why**: `Stop` is the main agent stop event. `SubagentStop` is the distinct event that fires when a subagent (spawned via Task tool) completes. The `subagent:*` matcher on `Stop` was not a valid way to target subagent stops — it would never match. The correct event key is `SubagentStop`, which does not support matchers (it fires per-subagent, not per-tool).

### Change 2: Remove unsupported matcher from `UserPromptSubmit`

**Before**:
```json
"UserPromptSubmit": [
  {
    "matcher": "*",
    "hooks": [...]
  }
]
```

**After**:
```json
"UserPromptSubmit": [
  {
    "hooks": [...]
  }
]
```

**Why**: `UserPromptSubmit` does not support the `matcher` field. Including `"matcher": "*"` has no effect at best and may cause registration issues at worst. Removed to match the correct schema.

### Change 3: Extend `PreToolUse` matcher

**Before**:
```json
"matcher": "Write|Edit"
```

**After**:
```json
"matcher": "Write|Edit|MultiEdit|Bash"
```

**Why**: The pre_tool_use.py hook handles Bash commands and MultiEdit operations in addition to Write and Edit. The matcher was not covering the full set of tools the hook is designed to intercept.

---

## Preserved Logic

The following internal logic was intentionally left unchanged:

- `HANDOFF_RULES` dictionary — all agent routing rules intact
- `STATUS_TRANSITIONS` dictionary — all status transition mappings intact
- `parse_agent_output()` function — signal parsing (##HANDOFF:##, ##WORKITEM:##, ##STATUS:##) unchanged
- `determine_handoff()` function — rule lookup logic unchanged
- `log_handoff()` function — audit trail logging unchanged
- `main()` control flow — read stdin, parse, determine, log, output — structure unchanged
- Error handler exit codes (2) for genuine errors — unchanged

The `STATUS_TRANSITIONS` dict remains in place even though the transition value is no longer included in the stdout output. This is intentional: the data may be used by future logging enhancements or the `systemMessage` field can be extended to include it if needed. No logic was removed that was not part of the output format fix.

---

## File Diff Summary

### subagent_stop.py

| Location | Change Type | Description |
|----------|-------------|-------------|
| Lines 2-13 (docstring) | Updated | Corrected event name to `SubagentStop`; documented output schema; updated exit code semantics; added known bug reference |
| Lines 181-190 | Replaced | Handoff output: custom JSON -> `{"decision": "block", "reason": ..., "systemMessage": ...}` |
| Lines 193-195 | Replaced | No-handoff output: `{"action": "none", ...}` + exit 1 -> `{}` + exit 0 |
| Lines 197-202 | Replaced | Error handlers: stdout -> stderr (exit 2 ignores stdout) |

### hooks.json

| Location | Change Type | Description |
|----------|-------------|-------------|
| `UserPromptSubmit` entry | Removed field | Removed unsupported `"matcher": "*"` |
| `PreToolUse` matcher | Updated | `"Write|Edit"` -> `"Write|Edit|MultiEdit|Bash"` |
| `Stop` entry (lines 40-51) | Removed | Entire `Stop` event block with `subagent:*` matcher removed |
| `SubagentStop` entry | Added | New event block with correct event name, no matcher, same command and timeout |

---

## Validation Checklist

| Check | Result |
|-------|--------|
| RC-5: Handoff output uses `decision`/`reason`/`systemMessage` only | PASS |
| RC-5: No `hookSpecificOutput` or `hookEventName` in output | PASS |
| RC-5: No custom fields (`action`, `to_agent`, `work_items`, etc.) in output | PASS |
| RC-6: No-handoff path exits with code 0 | PASS |
| RC-6: No-handoff path prints `{}` | PASS |
| RC-4: Hook registered under `SubagentStop` event | PASS |
| RC-4: No `subagent:*` matcher (SubagentStop has no matcher support) | PASS |
| RC-4: `UserPromptSubmit` has no `matcher` field | PASS |
| RC-4: `PreToolUse` matcher includes `MultiEdit` and `Bash` | PASS |
| Error handlers write JSON to stderr (stdout ignored on exit 2) | PASS |
| `HANDOFF_RULES` unchanged | PASS |
| `STATUS_TRANSITIONS` unchanged | PASS |
| `parse_agent_output()` unchanged | PASS |
| `determine_handoff()` unchanged | PASS |
| `log_handoff()` unchanged | PASS |
| Schema compliance: empty `{}` for allow-stop | PASS |
| Schema compliance: `decision`+`reason` both present when blocking | PASS |

---

## Known Limitation

GitHub Issue #20221 (OPEN): Prompt-based SubagentStop hooks may not actually prevent subagent termination even when `decision: "block"` is returned. This is a Claude Code platform bug, not a defect in this hook implementation. The fix implemented here is schema-correct; enforcement reliability depends on platform resolution of #20221.

This limitation is documented in:
- The module docstring of `subagent_stop.py`
- The schema file at `schemas/hooks/subagent-stop-output.schema.json`
