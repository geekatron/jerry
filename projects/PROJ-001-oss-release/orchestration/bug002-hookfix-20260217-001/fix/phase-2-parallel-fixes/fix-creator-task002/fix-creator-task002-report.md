# fix-creator-task002 Validation Report

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overview of changes applied |
| [Root Causes Addressed](#root-causes-addressed) | RC-2 and RC-3 from Phase 1 |
| [Helper Function Added](#helper-function-added) | make_decision() |
| [Change Log](#change-log) | All changes with before/after and line numbers |
| [Schema Compliance](#schema-compliance) | Verification against pre-tool-use-output.schema.json |
| [Invariants Preserved](#invariants-preserved) | Security logic left untouched |

---

## Summary

File modified: `scripts/pre_tool_use.py`

All 7 output points were updated to use the correct PreToolUse hook API:
- Deprecated top-level `decision` field removed from all stdout JSON
- Correct `hookSpecificOutput.permissionDecision` wrapping applied
- Vocabulary changed: `"approve"` -> `"allow"`, `"block"` -> `"deny"`, `"ask"` unchanged
- Both error handlers now write diagnostic JSON to stderr (not stdout); exit code 2 retained
- `matches` data (not part of the schema) moved to stderr for "block" and "ask" decisions
- New `make_decision()` helper added before `def main()` to centralize output construction

---

## Root Causes Addressed

| Root Cause | Description | Fix Applied |
|------------|-------------|-------------|
| RC-2 | Deprecated top-level `decision` field used instead of `hookSpecificOutput.permissionDecision` | All 5 decision outputs replaced with `make_decision()` producing correct schema structure |
| RC-3 | Error handlers returned exit code 2 with JSON on stdout; exit code 2 causes Claude Code to ignore stdout JSON | JSON moved to stderr; exit code 2 retained (correct blocking behavior on hook crash) |

---

## Helper Function Added

Added `make_decision()` at lines 250-271 (before `def main()`):

```python
def make_decision(decision: str, reason: str = "", **extra) -> str:
    """Build a PreToolUse hook output JSON string.

    Args:
        decision: One of "allow", "deny", or "ask".
        reason: Optional human-readable reason for the decision.
        **extra: Additional fields to merge into hookSpecificOutput.

    Returns:
        JSON string conforming to the PreToolUse hook output schema.
    """
    output: dict[str, Any] = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
        }
    }
    if reason:
        output["hookSpecificOutput"]["permissionDecisionReason"] = reason
    if extra:
        output["hookSpecificOutput"].update(extra)
    return json.dumps(output)
```

---

## Change Log

### Change 1: Rule-based security block (Phase 1 exit)

**Original line 275:**
```python
print(json.dumps({"decision": "block", "reason": reason}))
```

**New line 299:**
```python
print(make_decision("deny", reason))
```

**Produces:**
```json
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "<reason>"}}
```

---

### Change 2: Pattern-based block decision (Phase 2 exit)

**Original lines 285-290:**
```python
if pattern_decision == "block":
    print(
        json.dumps(
            {"decision": "block", "reason": pattern_reason, "matches": pattern_matches}
        )
    )
    return 0
```

**New lines 308-312:**
```python
if pattern_decision == "block":
    if pattern_matches:
        print(json.dumps({"matches": pattern_matches}), file=sys.stderr)
    print(make_decision("deny", pattern_reason))
    return 0
```

**Notes:** `matches` moved to stderr because `hookSpecificOutput` has `additionalProperties: false` in the schema; the field cannot be included in the stdout JSON.

---

### Change 3: Pattern-based ask decision (Phase 2 exit)

**Original lines 299-306:**
```python
if pattern_decision == "ask":
    # Ask user for confirmation
    print(
        json.dumps(
            {"decision": "ask", "reason": pattern_reason, "matches": pattern_matches}
        )
    )
    return 0
```

**New lines 321-326:**
```python
if pattern_decision == "ask":
    # Ask user for confirmation
    if pattern_matches:
        print(json.dumps({"matches": pattern_matches}), file=sys.stderr)
    print(make_decision("ask", pattern_reason))
    return 0
```

**Notes:** Same `matches` handling as Change 2. Vocabulary "ask" is valid in the new schema.

---

### Change 4: AST enforcement block (Phase 3 exit)

**Original line 336:**
```python
print(json.dumps({"decision": "block", "reason": decision.reason}))
```

**New line 356:**
```python
print(make_decision("deny", decision.reason))
```

---

### Change 5: Final approve (Phase 4 exit)

**Original line 365:**
```python
print(json.dumps({"decision": "approve"}))
```

**New line 385:**
```python
print(make_decision("allow"))
```

**Produces:**
```json
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}
```

---

### Change 6: JSONDecodeError handler

**Original lines 368-370:**
```python
except json.JSONDecodeError as e:
    print(json.dumps({"decision": "block", "reason": f"Hook error: Invalid JSON input - {e}"}))
    return 2
```

**New lines 388-393:**
```python
except json.JSONDecodeError as e:
    print(
        json.dumps({"error": f"Hook error: Invalid JSON input - {e}"}),
        file=sys.stderr,
    )
    return 2
```

**Rationale:** Exit code 2 signals "blocking error" to Claude Code, which causes stdout JSON to be IGNORED. Diagnostic information moved to stderr where it is always visible regardless of exit code. The blocking behavior is preserved by the exit code itself, not by any JSON payload.

---

### Change 7: General Exception handler

**Original lines 371-373:**
```python
except Exception as e:
    print(json.dumps({"decision": "block", "reason": f"Hook error: {e}"}))
    return 2
```

**New lines 394-399:**
```python
except Exception as e:
    print(
        json.dumps({"error": f"Hook error: {e}"}),
        file=sys.stderr,
    )
    return 2
```

**Rationale:** Same as Change 6.

---

## Schema Compliance

Schema file: `schemas/hooks/pre-tool-use-output.schema.json`

| Schema Requirement | Compliance |
|--------------------|------------|
| `hookSpecificOutput.hookEventName` must be `"PreToolUse"` | All outputs set `"hookEventName": "PreToolUse"` |
| `hookSpecificOutput.permissionDecision` must be one of `"allow"`, `"deny"`, `"ask"` | "deny" used for blocks, "allow" for approvals, "ask" for user confirmation |
| `hookSpecificOutput` has `additionalProperties: false` | `matches` field removed from stdout JSON and moved to stderr |
| Top-level `decision` field is NOT part of the schema | Removed from all 5 output points |

---

## Invariants Preserved

The following functions were NOT modified (security logic preserved):

- `check_file_write()` — blocked paths and sensitive file pattern logic unchanged
- `check_bash_command()` — cd-blocking, dangerous command detection unchanged
- `check_git_operation()` — force-push and hard-reset logic unchanged
- `check_patterns()` — pattern library integration unchanged
- `get_patterns()` — caching logic unchanged

Phase 3 (AST enforcement) warn path is also unchanged — it already correctly writes to stderr.

---

## Status

COMPLETE. All 7 output points updated. No security logic was modified. File passes schema compliance check.
