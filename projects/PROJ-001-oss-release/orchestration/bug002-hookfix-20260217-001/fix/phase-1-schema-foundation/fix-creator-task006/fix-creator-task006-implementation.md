# Phase 1 Schema Foundation -- Implementation Report

> **Agent:** fix-creator-task006
> **Date:** 2026-02-17
> **Deliverable:** JSON Schema (draft 2020-12) files for all Claude Code hook output types

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What was created and why |
| [Schema Files Created](#schema-files-created) | Catalog of all 8 schema files |
| [Architecture](#architecture) | Base/extension pattern, decision control models |
| [Validation Results](#validation-results) | Meta-validation and functional test outcomes |
| [Usage Guide](#usage-guide) | How to validate hook output against these schemas |
| [Design Decisions](#design-decisions) | Key choices with rationale |
| [Traceability](#traceability) | Mapping to research findings |

---

## Summary

Created 8 JSON Schema files under `schemas/hooks/` that formally define the output contract for every Claude Code hook event type used (or planned for use) by the Jerry Framework. These schemas serve as:

1. **Validation contracts** -- Hook implementations can be validated against their respective schema at test time and in CI.
2. **Documentation** -- Each schema is self-documenting with descriptions, source references, and known issues.
3. **Fix targets** -- Phase 2 (hook implementation fixes) can use these schemas as the target specification.

All schemas use JSON Schema draft 2020-12 and have been validated both at the meta level (valid schema) and functionally (correct accept/reject behavior against example payloads).

---

## Schema Files Created

All files are located at: `schemas/hooks/`

### 1. hook-output-base.schema.json

| Attribute | Value |
|-----------|-------|
| **Purpose** | Universal fields shared by ALL hook event outputs |
| **Properties** | `continue` (boolean), `stopReason` (string), `suppressOutput` (boolean), `systemMessage` (string) |
| **Required fields** | None (all optional) |
| **additionalProperties** | `true` (allows event-specific fields in compositions) |

This is the base schema. All event-specific schemas reference it via `allOf: [{ "$ref": "hook-output-base.schema.json" }]`.

### 2. session-start-output.schema.json

| Attribute | Value |
|-----------|-------|
| **Purpose** | SessionStart hook event output |
| **Decision control** | None (cannot block session start) |
| **Key fields** | `hookSpecificOutput.hookEventName` (const "SessionStart"), `hookSpecificOutput.additionalContext` |
| **Jerry usage** | `scripts/session_start_hook.py` -- project context injection, quality framework preamble |
| **Reference impl** | CORRECT -- matches this schema exactly |

### 3. user-prompt-submit-output.schema.json

| Attribute | Value |
|-----------|-------|
| **Purpose** | UserPromptSubmit hook event output |
| **Decision control** | Top-level `decision: "block"` + `reason` |
| **Key fields** | `decision`, `reason`, `hookSpecificOutput.hookEventName` (const "UserPromptSubmit"), `hookSpecificOutput.additionalContext` |
| **Jerry usage** | `hooks/user-prompt-submit.py` -- L2 per-prompt quality reinforcement injection |
| **Current impl status** | BROKEN -- missing `hookEventName` field |

### 4. pre-tool-use-output.schema.json

| Attribute | Value |
|-----------|-------|
| **Purpose** | PreToolUse hook event output |
| **Decision control** | `hookSpecificOutput.permissionDecision` (allow/deny/ask) |
| **Key fields** | `hookSpecificOutput.hookEventName` (const "PreToolUse"), `permissionDecision`, `permissionDecisionReason`, `updatedInput`, `additionalContext` |
| **Jerry usage** | `scripts/pre_tool_use.py` -- L3 deterministic tool gating |
| **Current impl status** | BROKEN -- uses deprecated top-level `decision` with wrong values (`approve`/`block` instead of `allow`/`deny`) |

### 5. post-tool-use-output.schema.json

| Attribute | Value |
|-----------|-------|
| **Purpose** | PostToolUse hook event output |
| **Decision control** | Top-level `decision: "block"` + `reason` |
| **Key fields** | `decision`, `reason`, `hookSpecificOutput.hookEventName` (const "PostToolUse"), `additionalContext`, `updatedMCPToolOutput` |
| **Jerry usage** | Not currently implemented; schema provided for future L4 output inspection hooks |

### 6. stop-output.schema.json

| Attribute | Value |
|-----------|-------|
| **Purpose** | Stop hook event output |
| **Decision control** | Top-level `decision: "block"` + `reason` ONLY |
| **Key fields** | `decision`, `reason` |
| **Critical constraint** | Does NOT use `hookSpecificOutput` or `hookEventName` (confirmed by GitHub Issue #15485) |
| **Conditional validation** | When `decision` is "block", `reason` is REQUIRED |
| **Jerry usage** | Not currently implemented; schema provided for future use |

### 7. subagent-stop-output.schema.json

| Attribute | Value |
|-----------|-------|
| **Purpose** | SubagentStop hook event output |
| **Decision control** | Top-level `decision: "block"` + `reason` ONLY |
| **Key fields** | `decision`, `reason` |
| **Critical constraint** | Does NOT use `hookSpecificOutput` or `hookEventName` (confirmed by GitHub Issue #15485) |
| **Conditional validation** | When `decision` is "block", `reason` is REQUIRED |
| **Known bug** | Issue #20221 -- prompt-based SubagentStop hooks may not actually prevent termination |
| **Jerry usage** | `scripts/subagent_stop.py` -- BROKEN (registered under wrong event, uses non-standard output fields) |

### 8. permission-request-output.schema.json

| Attribute | Value |
|-----------|-------|
| **Purpose** | PermissionRequest hook event output |
| **Decision control** | `hookSpecificOutput.decision.behavior` (allow/deny) |
| **Key fields** | `hookSpecificOutput.hookEventName` (const "PermissionRequest"), `decision.behavior`, `decision.updatedInput`, `decision.updatedPermissions`, `decision.message`, `decision.interrupt` |
| **Conditional validation** | Allow-only fields: `updatedInput`, `updatedPermissions`. Deny-only fields: `message`, `interrupt`. |
| **Jerry usage** | Not currently implemented; schema provided for future use |

---

## Architecture

### Base/Extension Pattern

```
hook-output-base.schema.json          (universal fields, additionalProperties: true)
  |
  +-- session-start-output.schema.json      (allOf $ref to base)
  +-- user-prompt-submit-output.schema.json  (allOf $ref to base)
  +-- pre-tool-use-output.schema.json        (allOf $ref to base)
  +-- post-tool-use-output.schema.json       (allOf $ref to base)
  +-- stop-output.schema.json                (allOf $ref to base)
  +-- subagent-stop-output.schema.json       (allOf $ref to base)
  +-- permission-request-output.schema.json  (allOf $ref to base)
```

Each event-specific schema uses `allOf` to compose with the base schema while setting `additionalProperties: false` to ensure strict validation of event-specific fields.

### Three Decision Control Models

| Model | Events | Key Field |
|-------|--------|-----------|
| Top-level `decision: "block"` | UserPromptSubmit, PostToolUse, Stop, SubagentStop | `decision` + `reason` |
| `hookSpecificOutput.permissionDecision` | PreToolUse | `permissionDecision` (allow/deny/ask) |
| `hookSpecificOutput.decision.behavior` | PermissionRequest | `decision.behavior` (allow/deny) |

### hookSpecificOutput Presence

| Event | Uses hookSpecificOutput | hookEventName Required |
|-------|-------------------------|------------------------|
| SessionStart | Yes | Yes |
| UserPromptSubmit | Yes | Yes |
| PreToolUse | Yes (primary decision mechanism) | Yes |
| PostToolUse | Yes | Yes |
| PermissionRequest | Yes (primary decision mechanism) | Yes |
| Stop | **No** | **No** |
| SubagentStop | **No** | **No** |

---

## Validation Results

### Meta-Validation (Schema Validity)

All 8 schemas pass `Draft202012Validator.check_schema()`:

| Schema | Meta-Valid |
|--------|-----------|
| hook-output-base.schema.json | PASS |
| session-start-output.schema.json | PASS |
| user-prompt-submit-output.schema.json | PASS |
| pre-tool-use-output.schema.json | PASS |
| post-tool-use-output.schema.json | PASS |
| stop-output.schema.json | PASS |
| subagent-stop-output.schema.json | PASS |
| permission-request-output.schema.json | PASS |

### Functional Validation Tests

| Test Case | Schema | Input | Expected | Result |
|-----------|--------|-------|----------|--------|
| SessionStart good output | session-start | `{systemMessage, hookSpecificOutput: {hookEventName: "SessionStart", additionalContext}}` | PASS | PASS |
| SessionStart missing hookEventName | session-start | `{hookSpecificOutput: {additionalContext}}` | REJECT | CORRECTLY REJECTED |
| SessionStart wrong hookEventName | session-start | `{hookSpecificOutput: {hookEventName: "PreToolUse"}}` | REJECT | CORRECTLY REJECTED |
| Stop block with reason | stop | `{decision: "block", reason: "..."}` | PASS | PASS |
| Stop empty (allow by omission) | stop | `{}` | PASS | PASS |
| Stop block without reason | stop | `{decision: "block"}` | REJECT | CORRECTLY REJECTED |
| Stop with hookSpecificOutput | stop | `{hookSpecificOutput: {...}}` | REJECT | CORRECTLY REJECTED |

---

## Usage Guide

### Validating Hook Output in Python

```python
import json
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

# Load schemas
schemas_dir = Path("schemas/hooks")
base_schema = json.loads((schemas_dir / "hook-output-base.schema.json").read_text())

# Create a resolver for $ref resolution
store = {}
for schema_file in schemas_dir.glob("*.schema.json"):
    schema = json.loads(schema_file.read_text())
    store[schema_file.name] = schema

resolver = RefResolver.from_schema(base_schema, store=store)

# Load event-specific schema
session_schema = json.loads(
    (schemas_dir / "session-start-output.schema.json").read_text()
)
validator = Draft202012Validator(session_schema, resolver=resolver)

# Validate hook output
hook_output = {
    "systemMessage": "Jerry Framework: Project active",
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "Project context here"
    }
}

errors = list(validator.iter_errors(hook_output))
if errors:
    for error in errors:
        print(f"Validation error: {error.message}")
else:
    print("Hook output is valid")
```

### Validating in Contract Tests

```python
import pytest
from jsonschema import Draft202012Validator

def test_session_start_output_conforms_to_schema(
    session_start_schema, hook_output
):
    """Contract test: SessionStart output must match schema."""
    validator = Draft202012Validator(session_start_schema)
    errors = list(validator.iter_errors(hook_output))
    assert not errors, f"Schema violations: {[e.message for e in errors]}"
```

### Schema Selection by Event Type

```python
SCHEMA_MAP = {
    "SessionStart": "session-start-output.schema.json",
    "UserPromptSubmit": "user-prompt-submit-output.schema.json",
    "PreToolUse": "pre-tool-use-output.schema.json",
    "PostToolUse": "post-tool-use-output.schema.json",
    "Stop": "stop-output.schema.json",
    "SubagentStop": "subagent-stop-output.schema.json",
    "PermissionRequest": "permission-request-output.schema.json",
}
```

---

## Design Decisions

### DD-001: Separate Files Per Event Type

**Decision:** One schema file per hook event type rather than a monolithic schema.

**Rationale:** Each event has fundamentally different decision control patterns (three distinct models). A monolithic schema with `oneOf` branches would be harder to maintain and produce less clear validation errors. Separate files allow each hook implementation to reference only its own contract.

### DD-002: Base Schema with additionalProperties: true

**Decision:** Base schema allows additional properties; event-specific schemas set `additionalProperties: false`.

**Rationale:** The base schema must be composable via `allOf`. If the base set `additionalProperties: false`, it would reject event-specific fields like `decision` or `hookSpecificOutput`. Event schemas override to `false` for strict validation.

### DD-003: Conditional Validation for Stop/SubagentStop

**Decision:** Use `if/then` to require `reason` when `decision` is "block".

**Rationale:** The official docs state reason is "REQUIRED when decision is block." The `if/then` pattern in JSON Schema draft 2020-12 expresses this conditional constraint directly.

### DD-004: PermissionRequest Allow/Deny Field Restrictions

**Decision:** Use `if/then` with `"properties": { "fieldName": false }` to restrict allow-only and deny-only fields.

**Rationale:** `updatedInput` and `updatedPermissions` only make sense for allow decisions. `message` and `interrupt` only make sense for deny decisions. The schema enforces this mutual exclusivity using conditional validation.

### DD-005: No Top-Level Decision on PreToolUse

**Decision:** PreToolUse schema does NOT include a top-level `decision` property.

**Rationale:** The official docs explicitly state "Unlike other hooks that use a top-level decision field, PreToolUse returns its decision inside a hookSpecificOutput object." The deprecated top-level `decision` field with `approve`/`block` values is intentionally not supported. Hook implementations must migrate to `hookSpecificOutput.permissionDecision`.

### DD-006: hookEventName as const

**Decision:** Each event schema uses `const` for `hookEventName` (e.g., `"const": "SessionStart"`).

**Rationale:** The official docs require hookEventName to match the event name exactly. Using `const` ensures the schema rejects mismatched event names (e.g., a PreToolUse output cannot claim to be SessionStart).

---

## Traceability

| Schema Element | Research Source | Confidence |
|----------------|----------------|------------|
| Universal fields (continue, stopReason, suppressOutput, systemMessage) | Context7 report: Official docs "Universal Fields" table | HIGH |
| SessionStart hookSpecificOutput.additionalContext | Context7 + WebSearch: Both confirm | HIGH |
| UserPromptSubmit top-level decision + hookSpecificOutput | WebSearch: Official docs APIDOC section | HIGH |
| PreToolUse hookSpecificOutput.permissionDecision (allow/deny/ask) | Context7 + WebSearch: Both confirm. Deprecated top-level decision intentionally excluded | HIGH |
| PostToolUse decision + hookSpecificOutput.updatedMCPToolOutput | WebSearch: Official docs "PostToolUse Decision Control Output" | HIGH |
| Stop/SubagentStop top-level only, no hookSpecificOutput | WebSearch: GitHub Issue #15485 (closed, COMPLETED) | HIGH |
| PermissionRequest hookSpecificOutput.decision.behavior | Context7 + WebSearch: Both confirm | HIGH |
| Stop/SubagentStop reason REQUIRED when blocking | Context7 + WebSearch: "Must be provided when Claude is blocked from stopping" | HIGH |
| PermissionRequest allow/deny conditional fields | WebSearch: Official docs with separate allow/deny examples | HIGH |

---

## Files Created

| # | File Path | Size |
|---|-----------|------|
| 1 | `schemas/hooks/hook-output-base.schema.json` | Base schema |
| 2 | `schemas/hooks/session-start-output.schema.json` | SessionStart output |
| 3 | `schemas/hooks/user-prompt-submit-output.schema.json` | UserPromptSubmit output |
| 4 | `schemas/hooks/pre-tool-use-output.schema.json` | PreToolUse output |
| 5 | `schemas/hooks/post-tool-use-output.schema.json` | PostToolUse output |
| 6 | `schemas/hooks/stop-output.schema.json` | Stop output |
| 7 | `schemas/hooks/subagent-stop-output.schema.json` | SubagentStop output |
| 8 | `schemas/hooks/permission-request-output.schema.json` | PermissionRequest output |
| 9 | This report | Implementation documentation |
