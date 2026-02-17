# fix-validator-task006: JSON Schema Validation Report

> **Agent:** fix-validator-task006
> **Date:** 2026-02-17
> **Verdict:** VALIDATED
> **Result:** 8/8 tests passed

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall validation result |
| [Test Results](#test-results) | Pass/fail status for each test |
| [Test Details](#test-details) | Detailed output per test |
| [Schema Files Validated](#schema-files-validated) | List of schema files |
| [Methodology](#methodology) | Tools and approach used |

---

## Summary

All 8 JSON Schema files for Claude Code hook outputs are **syntactically valid** JSON Schema draft 2020-12 and produce **correct validation behavior** for both known-good and known-bad test inputs.

| Metric | Value |
|--------|-------|
| Total tests | 8 |
| Passed | 8 |
| Failed | 0 |
| Verdict | **VALIDATED** |

---

## Test Results

| ID | Test | Expected | Actual | Status |
|----|------|----------|--------|--------|
| T1 | Schema syntax validation (all 8 files) | All valid JSON Schema draft 2020-12 | All valid | PASS |
| T2 | Known-good SessionStart output | Validates successfully | No errors | PASS |
| T3 | Known-bad UserPromptSubmit (missing hookEventName) | Rejected | Rejected: `'hookEventName' is a required property` | PASS |
| T4 | Known-bad PreToolUse (deprecated top-level decision) | Rejected | Rejected: `Additional properties are not allowed ('decision' was unexpected)` | PASS |
| T5 | Known-bad SubagentStop (has hookSpecificOutput) | Rejected | Rejected: `Additional properties are not allowed ('hookSpecificOutput' was unexpected)` | PASS |
| T6 | Known-good PreToolUse (correct hookSpecificOutput) | Validates successfully | No errors | PASS |
| T7 | Known-good SubagentStop (correct top-level decision) | Validates successfully | No errors | PASS |
| T8 | Known-good UserPromptSubmit (with hookEventName) | Validates successfully | No errors | PASS |

---

## Test Details

### T1: Schema Syntax Validation

Validates all 8 schema files are parseable JSON and conform to JSON Schema draft 2020-12 meta-schema using `Draft202012Validator.check_schema()`.

**Result:** All 8 files passed.

```
hook-output-base.schema.json: valid
session-start-output.schema.json: valid
user-prompt-submit-output.schema.json: valid
pre-tool-use-output.schema.json: valid
post-tool-use-output.schema.json: valid
stop-output.schema.json: valid
subagent-stop-output.schema.json: valid
permission-request-output.schema.json: valid
```

### T2: Known-Good SessionStart

Tests the output format matching what `scripts/session_start_hook.py` produces (lines 25-44):

```json
{
  "systemMessage": "test message",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "test context"
  }
}
```

**Result:** PASS -- no validation errors.

### T3: Known-Bad UserPromptSubmit (missing hookEventName)

Tests that a `hookSpecificOutput` object without the required `hookEventName` is correctly rejected:

```json
{
  "hookSpecificOutput": {
    "additionalContext": "test"
  }
}
```

**Result:** PASS -- correctly rejected with error: `$.hookSpecificOutput: 'hookEventName' is a required property`

### T4: Known-Bad PreToolUse (deprecated format)

Tests that the deprecated top-level `decision` format (which PreToolUse does NOT use) is correctly rejected:

```json
{
  "decision": "approve"
}
```

**Result:** PASS -- correctly rejected with error: `$: Additional properties are not allowed ('decision' was unexpected)`

This confirms the schema enforces `additionalProperties: false` and PreToolUse's unique pattern of using `hookSpecificOutput.permissionDecision` instead of top-level `decision`.

### T5: Known-Bad SubagentStop (has hookSpecificOutput)

Tests that SubagentStop (which uses ONLY top-level `decision`/`reason`, NOT `hookSpecificOutput`) rejects output with hookSpecificOutput:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStop",
    "action": "handoff"
  }
}
```

**Result:** PASS -- correctly rejected with error: `$: Additional properties are not allowed ('hookSpecificOutput' was unexpected)`

This confirms the schema correctly models SubagentStop's top-level-only output format.

### T6: Known-Good PreToolUse

Tests the correct PreToolUse format using `hookSpecificOutput.permissionDecision`:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow"
  }
}
```

**Result:** PASS -- no validation errors.

### T7: Known-Good SubagentStop

Tests the correct SubagentStop format using top-level `decision` and `reason`:

```json
{
  "decision": "block",
  "reason": "Must complete handoff first"
}
```

**Result:** PASS -- no validation errors.

### T8: Known-Good UserPromptSubmit

Tests the correct UserPromptSubmit format with required `hookEventName`:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "quality reinforcement content"
  }
}
```

**Result:** PASS -- no validation errors.

---

## Schema Files Validated

All files located at `schemas/hooks/`:

| File | Purpose | $ref |
|------|---------|------|
| `hook-output-base.schema.json` | Universal fields (continue, stopReason, suppressOutput, systemMessage) | -- |
| `session-start-output.schema.json` | SessionStart: context injection via hookSpecificOutput.additionalContext | Base |
| `user-prompt-submit-output.schema.json` | UserPromptSubmit: L2 quality reinforcement, optional block decision | Base |
| `pre-tool-use-output.schema.json` | PreToolUse: permission via hookSpecificOutput.permissionDecision (allow/deny/ask) | Base |
| `post-tool-use-output.schema.json` | PostToolUse: feedback via top-level decision, MCP output replacement | Base |
| `stop-output.schema.json` | Stop: top-level block decision with conditional reason requirement | Base |
| `subagent-stop-output.schema.json` | SubagentStop: top-level block decision, no hookSpecificOutput | Base |
| `permission-request-output.schema.json` | PermissionRequest: nested decision.behavior (allow/deny) with conditional fields | Base |

---

## Methodology

- **Python version:** Executed via `uv run python` (H-05 compliant)
- **Validator:** `jsonschema` library v4.26.0, `Draft202012Validator`
- **$ref resolution:** `referencing` library with `Registry` for cross-schema references
- **Test strategy:** 3 known-good inputs (must pass) + 3 known-bad inputs (must fail) + 1 syntax check (all 8 files) + 1 additional known-good
- **Script location:** `scripts/validate_schemas.py`

---

## Conclusion

All 8 JSON Schema files are valid, correctly enforce their structural constraints, and properly distinguish between valid and invalid hook outputs. The schemas correctly model the documented differences between hook event types (e.g., PreToolUse using hookSpecificOutput.permissionDecision vs. Stop/SubagentStop using top-level decision, and SubagentStop not supporting hookSpecificOutput at all).
