# Fix Creator TASK-001 Validation Report

**Agent:** fix-creator-task001
**Task:** Fix UserPromptSubmit hook -- add missing `hookEventName` field (RC-1)
**Date:** 2026-02-17
**File Modified:** `hooks/user-prompt-submit.py`

## Document Sections

| Section | Purpose |
|---------|---------|
| [What Was Changed](#what-was-changed) | Description of the single-line addition |
| [Before / After Code](#before--after-code) | Exact diff of the change |
| [Schema Compliance Verification](#schema-compliance-verification) | Alignment with the JSON schema |
| [Additional Issues Found](#additional-issues-found) | Observations beyond the targeted fix |

---

## What Was Changed

A single key-value pair was added as the first entry inside the `hookSpecificOutput` dictionary on line 59 of `hooks/user-prompt-submit.py`:

```
"hookEventName": "UserPromptSubmit",
```

This field is declared `required` in `schemas/hooks/user-prompt-submit-output.schema.json`. Without it, Claude Code cannot identify the event type of the `hookSpecificOutput` block, causing the `additionalContext` payload to be silently discarded. The result was that all L2 per-prompt quality reinforcement injections were non-functional.

No other code was modified. No refactoring was performed.

---

## Before / After Code

### Before (lines 56-63)

```python
        if result.preamble:
            output = {
                "hookSpecificOutput": {
                    "additionalContext": (
                        f"<quality-reinforcement>\n{result.preamble}\n</quality-reinforcement>"
                    ),
                },
            }
```

### After (lines 56-64)

```python
        if result.preamble:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        f"<quality-reinforcement>\n{result.preamble}\n</quality-reinforcement>"
                    ),
                },
            }
```

---

## Schema Compliance Verification

Schema file consulted: `schemas/hooks/user-prompt-submit-output.schema.json`

| Schema Requirement | Fixed Code | Status |
|--------------------|------------|--------|
| `hookSpecificOutput.required` includes `hookEventName` | `"hookEventName": "UserPromptSubmit"` present | PASS |
| `hookEventName` must be `const: "UserPromptSubmit"` | Value is exactly `"UserPromptSubmit"` | PASS |
| `additionalContext` is a string (optional) | f-string producing a string value | PASS |
| `additionalProperties: false` on `hookSpecificOutput` | Only `hookEventName` and `additionalContext` keys present | PASS |
| `additionalProperties: false` on root output object | Only `hookSpecificOutput` key present in the non-empty branch | PASS |

The fixed output is fully compliant with the schema.

---

## Additional Issues Found

No additional defects were identified in the targeted file. The following observations are informational only:

1. **Empty passthrough branch is correct.** When `result.preamble` is falsy, the code returns `{}` (an empty dict), which is valid per the schema (`required` properties on `hookSpecificOutput` only apply when that key is present).

2. **Fail-open error branch is correct.** The `except` block emits `{"warning": ...}` to stderr and `{}` to stdout. Neither the `warning` key on a stderr-only object nor the empty stdout object violates the output schema.

3. **No schema issues in the surrounding code.** The `json.dumps(output)` call correctly serialises the corrected dict to stdout as required by the Claude Code hook protocol.

The fix is minimal, targeted, and complete.
