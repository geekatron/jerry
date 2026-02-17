# Context7 Research Report: Claude Code Hook Output Schemas

> **Researcher:** fix-researcher-task006 (Context7 stream)
> **Date:** 2026-02-17
> **Sources:** Context7 libraries -- `/anthropics/claude-code`, `/mizunashi-mana/claude-code-hook-sdk`, `/websites/code_claude`, `/websites/code_claude_en_plugins-reference`

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Key findings overview |
| [Universal Output Fields](#universal-output-fields) | Fields available to ALL hook events |
| [Hook Output Architecture](#hook-output-architecture) | Two-tier decision control model |
| [Event-Specific Output Schemas](#event-specific-output-schemas) | Per-event field definitions |
| [Hook Input Schemas](#hook-input-schemas) | Input fields per event (for context) |
| [TypeScript Type Definitions](#typescript-type-definitions) | SDK interface definitions |
| [Complete Hook Event List](#complete-hook-event-list) | All known event types |
| [Confidence Assessment](#confidence-assessment) | Per-finding confidence levels |
| [Sources and References](#sources-and-references) | Traceability to Context7 documents |

---

## Executive Summary

Claude Code hooks use a **two-tier output model**:

1. **Universal fields** (`continue`, `stopReason`, `suppressOutput`, `systemMessage`) -- work across ALL events.
2. **Event-specific decision control** -- either via top-level `decision`/`reason` fields OR via a nested `hookSpecificOutput` object containing `hookEventName` plus event-specific fields.

**Critical finding:** `PreToolUse` and `PermissionRequest` use `hookSpecificOutput` for decision control, while `UserPromptSubmit`, `PostToolUse`, `PostToolUseFailure`, `Stop`, and `SubagentStop` use **top-level** `decision`/`reason` fields. This is a fundamental architectural split in how decisions are communicated.

---

## Universal Output Fields

These fields are available on ALL hook event outputs regardless of event type.

| Field | Type | Default | Required | Description | Confidence |
|-------|------|---------|----------|-------------|------------|
| `continue` | `boolean` | `true` | Optional | If `false`, Claude stops processing entirely. Takes precedence over event-specific decision fields. | HIGH |
| `stopReason` | `string` | none | Optional | Message shown to the user when `continue` is `false`. NOT shown to Claude. | HIGH |
| `suppressOutput` | `boolean` | `false` | Optional | If `true`, hides stdout from verbose mode output. | HIGH |
| `systemMessage` | `string` | none | Optional | Warning message shown to the user. | HIGH |

**Source:** Official Claude Code docs at `code.claude.com/docs/en/hooks` -- "Universal Fields" table.

---

## Hook Output Architecture

### Decision Control Model

There are TWO distinct patterns for decision control:

#### Pattern 1: Top-Level Decision (5 events)

Used by: `UserPromptSubmit`, `PostToolUse`, `PostToolUseFailure`, `Stop`, `SubagentStop`

```json
{
  "decision": "block",
  "reason": "Explanation for decision"
}
```

- To **allow**: omit the `decision` field entirely, or exit with code 0 without JSON output.
- To **block**: set `decision` to `"block"` and provide a `reason`.

#### Pattern 2: hookSpecificOutput (2 events)

Used by: `PreToolUse`, `PermissionRequest`

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "Reason text"
  }
}
```

#### Pattern 3: hookSpecificOutput for Context Injection (multiple events)

Used by: `SessionStart`, `UserPromptSubmit`, `PostToolUse` (and possibly others)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "EventName",
    "additionalContext": "Context string for Claude"
  }
}
```

**Important:** The `hookSpecificOutput` object ALWAYS requires a `hookEventName` field set to the event name.

### Exit Code Model (Alternative to JSON)

| Exit Code | Meaning |
|-----------|---------|
| 0 | Allow / success. If JSON on stdout, it is parsed. |
| 2 | Block / deny. JSON on stdout is IGNORED. |

You must choose ONE approach per hook: exit codes alone, OR exit 0 with JSON. Cannot combine.

---

## Event-Specific Output Schemas

### SessionStart

**Decision control:** `hookSpecificOutput` pattern (context injection only; no decision/block capability found).

| Field Path | Type | Required | Values | Description | Confidence |
|------------|------|----------|--------|-------------|------------|
| `hookSpecificOutput.hookEventName` | `string` | Required (when using hookSpecificOutput) | `"SessionStart"` | Event identifier | HIGH |
| `hookSpecificOutput.additionalContext` | `string` | Optional | free text | Context string concatenated with values from other hooks. Added to Claude's context. | HIGH |

**Full output example:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "My additional context here"
  }
}
```

**Note:** No `decision` or `permissionDecision` field documented for SessionStart. This hook is primarily for injecting startup context.

**Source:** Official docs at `code.claude.com/docs/en/hooks` -- "SessionStart Hook Decision Control Output"

---

### PreToolUse

**Decision control:** `hookSpecificOutput` pattern with `permissionDecision`.

| Field Path | Type | Required | Values | Description | Confidence |
|------------|------|----------|--------|-------------|------------|
| `hookSpecificOutput.hookEventName` | `string` | Required | `"PreToolUse"` | Event identifier | HIGH |
| `hookSpecificOutput.permissionDecision` | `string` | Required (for decision) | `"allow"` \| `"deny"` \| `"ask"` | `allow` bypasses permission system, `deny` prevents tool call, `ask` prompts user | HIGH |
| `hookSpecificOutput.permissionDecisionReason` | `string` | Optional | free text | Context for user or Claude depending on decision | HIGH |
| `hookSpecificOutput.updatedInput` | `object` | Optional | `Record<string, unknown>` | Modifies tool input parameters before execution | HIGH |
| `hookSpecificOutput.additionalContext` | `string` | Optional | free text | String added to Claude's context before tool executes | HIGH |

**Alternative simple output (also supported):**

| Field | Type | Required | Values | Description | Confidence |
|-------|------|----------|--------|-------------|------------|
| `decision` | `string` | Optional | `"allow"` \| `"deny"` \| `"ask"` | Simple top-level decision (alternative to hookSpecificOutput) | MEDIUM |
| `reason` | `string` | Optional | free text | Reason for decision | MEDIUM |

**Full output example (hookSpecificOutput pattern):**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "My reason here",
    "updatedInput": {
      "field_to_modify": "new value"
    },
    "additionalContext": "Current environment: production. Proceed with caution."
  }
}
```

**Note on dual interface:** The official docs mention BOTH top-level `decision` and `hookSpecificOutput.permissionDecision`. The hookSpecificOutput pattern provides richer control (3 outcomes + input modification + context injection) vs. the simple top-level pattern. The official docs explicitly state: "Unlike other hooks that use a top-level `decision` field, PreToolUse returns its decision inside a `hookSpecificOutput` object."

**Source:** Official docs at `code.claude.com/docs/en/hooks` -- "PreToolUse decision control"; Plugin dev SKILL.md from `github.com/anthropics/claude-code`

---

### PostToolUse

**Decision control:** Top-level `decision` pattern + optional `hookSpecificOutput` for context.

| Field | Type | Required | Values | Description | Confidence |
|-------|------|----------|--------|-------------|------------|
| `decision` | `string` | Optional | `"block"` | To block further processing after tool use. Omit to allow. | HIGH |
| `reason` | `string` | Optional | free text | Explanation for decision | HIGH |
| `hookSpecificOutput.hookEventName` | `string` | Required (when using hookSpecificOutput) | `"PostToolUse"` | Event identifier | HIGH |
| `hookSpecificOutput.additionalContext` | `string` | Optional | free text | Additional information for Claude | HIGH |

**Full output example:**
```json
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude"
  }
}
```

**Source:** Official docs at `code.claude.com/docs/en/hooks` -- "PostToolUse Decision Control Output"

---

### PostToolUseFailure

**Decision control:** Top-level `decision` pattern (same as PostToolUse).

| Field | Type | Required | Values | Description | Confidence |
|-------|------|----------|--------|-------------|------------|
| `decision` | `string` | Optional | `"block"` | To block further processing. Omit to allow. | HIGH |
| `reason` | `string` | Optional | free text | Explanation for decision | HIGH |

**Source:** Official docs list PostToolUseFailure in the same decision-control group as PostToolUse, Stop, SubagentStop.

---

### UserPromptSubmit

**Decision control:** Top-level `decision` pattern + optional `hookSpecificOutput` for context.

| Field | Type | Required | Values | Description | Confidence |
|-------|------|----------|--------|-------------|------------|
| `decision` | `string` | Optional | `"block"` | Prevents prompt from being processed; erases it from context. Omit to allow. | HIGH |
| `reason` | `string` | Optional | free text | Shown to user when blocking. NOT added to context. | HIGH |
| `additionalContext` | `string` | Optional | free text | Top-level field: string added to Claude's context. | HIGH |
| `hookSpecificOutput.hookEventName` | `string` | Required (when using hookSpecificOutput) | `"UserPromptSubmit"` | Event identifier | HIGH |
| `hookSpecificOutput.additionalContext` | `string` | Optional | free text | Additional context specific to the hook | HIGH |

**Plain text alternative:** Any non-JSON text written to stdout is added as context directly.

**Full output example:**
```json
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here"
  }
}
```

**Source:** Official docs at `code.claude.com/docs/en/hooks` -- "UserPromptSubmit Hook" APIDOC section

---

### Stop

**Decision control:** Top-level `decision` pattern.

| Field | Type | Required | Values | Description | Confidence |
|-------|------|----------|--------|-------------|------------|
| `decision` | `string` | Optional | `"approve"` \| `"block"` | `approve` allows stopping, `block` prevents stopping and continues agent work. Omit to allow. | HIGH |
| `reason` | `string` | Optional (Required when blocking) | free text | Explanation for decision. MUST be provided when `decision` is `"block"`. | HIGH |

**Full output example:**
```json
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping",
  "systemMessage": "Additional context"
}
```

**Note:** The Stop event uses `"approve"` | `"block"` rather than just `"block"`, per the plugin dev SKILL.md. However, the official hooks docs say to simply omit `decision` to allow. Both approaches appear supported.

**Source:** Plugin dev SKILL.md from `github.com/anthropics/claude-code`; Official docs at `code.claude.com/docs/en/hooks`

---

### SubagentStop

**Decision control:** Top-level `decision` pattern (same as Stop).

| Field | Type | Required | Values | Description | Confidence |
|-------|------|----------|--------|-------------|------------|
| `decision` | `string` | Optional | `"block"` | Prevents subagent from stopping. Omit to allow. | HIGH |
| `reason` | `string` | Optional (Required when blocking) | free text | Explanation for decision | HIGH |

**Source:** Official docs list SubagentStop in the same decision-control group as Stop.

---

### PermissionRequest

**Decision control:** `hookSpecificOutput` pattern with nested `decision` object.

| Field Path | Type | Required | Values | Description | Confidence |
|------------|------|----------|--------|-------------|------------|
| `hookSpecificOutput.hookEventName` | `string` | Required | `"PermissionRequest"` | Event identifier | HIGH |
| `hookSpecificOutput.decision.behavior` | `string` | Required (for decision) | `"allow"` \| `"deny"` | Determines outcome | HIGH |
| `hookSpecificOutput.decision.updatedInput` | `object` | Optional (allow only) | `Record<string, unknown>` | Modifies tool input before execution | HIGH |
| `hookSpecificOutput.decision.updatedPermissions` | `array/object` | Optional (allow only) | permission rules | Applies permission rule updates (equivalent to "always allow" option) | HIGH |
| `hookSpecificOutput.decision.message` | `string` | Optional (deny only) | free text | Tells Claude why permission was denied | HIGH |
| `hookSpecificOutput.decision.interrupt` | `boolean` | Optional (deny only) | `true`/`false` | If `true`, stops Claude entirely | HIGH |

**Full output example (allow):**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm run lint"
      }
    }
  }
}
```

**Full output example (deny):**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "deny",
      "message": "This operation is not permitted in production",
      "interrupt": false
    }
  }
}
```

**Source:** Official docs at `code.claude.com/docs/en/hooks` -- "PermissionRequest decision control"

---

### Notification

**Decision control:** None. Notification hooks are informational only and cannot block or modify notifications.

| Field | Type | Required | Values | Description | Confidence |
|-------|------|----------|--------|-------------|------------|
| (universal fields only) | -- | -- | -- | Only `continue`, `stopReason`, `suppressOutput`, `systemMessage` apply | HIGH |

**Source:** SDK type definitions (NotificationHookOutput extends BaseHookOutput with no additional fields); Official docs confirm Notification hooks "cannot block or modify notifications."

---

### PreCompact

**Decision control:** None documented. Informational hook.

| Field | Type | Required | Values | Description | Confidence |
|-------|------|----------|--------|-------------|------------|
| (universal fields only) | -- | -- | -- | Only `continue`, `stopReason`, `suppressOutput`, `systemMessage` apply | MEDIUM |

**Source:** SDK type definitions (PreCompactHookOutput extends BaseHookOutput with no additional fields).

---

## Hook Input Schemas

For completeness and cross-reference, here are the INPUT schemas per event (what hooks receive via stdin).

### Common Input Fields (ALL events)

| Field | Type | Description | Confidence |
|-------|------|-------------|------------|
| `session_id` | `string` | Unique session identifier | HIGH |
| `transcript_path` | `string` | Path to conversation transcript (.jsonl) | HIGH |
| `cwd` | `string` | Current working directory | HIGH |
| `permission_mode` | `string` | Permission mode (e.g., `"default"`, `"ask"`, `"allow"`) | HIGH |
| `hook_event_name` | `string` | Event type identifier | HIGH |

### Event-Specific Input Fields

| Event | Additional Fields | Confidence |
|-------|-------------------|------------|
| `SessionStart` | `source` (string, e.g., `"startup"`), `model` (string, e.g., `"claude-sonnet-4-5-20250929"`) | HIGH |
| `PreToolUse` | `tool_name` (string), `tool_input` (object), `tool_use_id` (string) | HIGH |
| `PostToolUse` | `tool_name` (string), `tool_input` (object), `tool_response` (object), `tool_use_id` (string) | HIGH |
| `PostToolUseFailure` | `tool_name` (string), `tool_input` (object), `tool_use_id` (string), `error` (string), `is_interrupt` (boolean) | HIGH |
| `UserPromptSubmit` | `prompt` (string) | HIGH |
| `Stop` | `stop_hook_active` (boolean) | HIGH |
| `SubagentStop` | `stop_hook_active` (boolean), `agent_id` (string), `agent_type` (string), `agent_transcript_path` (string) | HIGH |
| `PermissionRequest` | `tool_name` (string), `tool_input` (object), `permission_suggestions` (array of objects with `type` and `tool` fields) | HIGH |
| `Notification` | `message` (string), `title` (string), `notification_type` (string) | HIGH |
| `PreCompact` | `trigger` (string), `custom_instructions` (string) | HIGH |

---

## TypeScript Type Definitions

### From `@mizunashi-mana/claude-code-hook-sdk`

These are the TypeScript interfaces from the community SDK that provides Zod-validated type safety for hook development.

#### Output Interfaces

```typescript
interface BaseHookOutput {
  continue?: boolean;        // false to stop processing
  stopReason?: string;       // Reason for stopping (shown to user, not Claude)
  suppressOutput?: boolean;  // Suppress hook output from verbose mode
}

interface PreToolUseHookOutput extends BaseHookOutput {
  decision?: 'approve' | 'block';
  reason?: string;  // Shown to user when blocking
}

interface PostToolUseHookOutput extends BaseHookOutput {
  decision?: 'block';
  reason?: string;
}

interface StopHookOutput extends BaseHookOutput {
  decision?: 'block';
  reason?: string;
}

interface SubagentStopHookOutput extends BaseHookOutput {
  decision?: 'block';
  reason?: string;
}

interface UserPromptSubmitHookOutput extends BaseHookOutput {
  decision?: 'block';
  reason?: string;
  hookSpecificOutput?: {
    hookEventName: string;
    additionalContext: string;
  };
}

interface NotificationHookOutput extends BaseHookOutput {}

interface PreCompactHookOutput extends BaseHookOutput {}
```

#### Input Interfaces

```typescript
interface BaseHookInput {
  session_id: string;
  transcript_path: string;
  hook_event_name: string;
}

interface PreToolUseHookInput extends BaseHookInput {
  hook_event_name: 'PreToolUse';
  tool_name: string;
  tool_input: Record<string, unknown>;
}

interface PostToolUseHookInput extends BaseHookInput {
  hook_event_name: 'PostToolUse';
  tool_name: string;
  tool_input: Record<string, unknown>;
  tool_response: Record<string, unknown>;
}

interface NotificationHookInput extends BaseHookInput {
  hook_event_name: 'Notification';
  message: string;
}

interface StopHookInput extends BaseHookInput {
  hook_event_name: 'Stop';
  stop_hook_active: boolean;
}

interface SubagentStopHookInput extends BaseHookInput {
  hook_event_name: 'SubagentStop';
  stop_hook_active: boolean;
}

interface UserPromptSubmitHookInput extends BaseHookInput {
  hook_event_name: 'UserPromptSubmit';
  prompt: string;
}

interface PreCompactHookInput extends BaseHookInput {
  hook_event_name: 'PreCompact';
  trigger: string;
  custom_instructions: string;
}
```

**SDK Confidence Note:** These types are from the community SDK (`@mizunashi-mana/claude-code-hook-sdk`), not the official Anthropic codebase. However, they are Zod-validated against actual Claude Code behavior and have a Context7 Benchmark Score of 85.4 with High source reputation. The SDK types are **simpler** than the official docs -- notably, the SDK's `PreToolUseHookOutput` uses `decision?: 'approve' | 'block'` while the official docs show the richer `hookSpecificOutput.permissionDecision: 'allow' | 'deny' | 'ask'` pattern. **The official docs should be considered authoritative where they diverge from the SDK types.**

---

## Complete Hook Event List

All known hook event types from the official Claude Code plugins reference:

| Event | Category | Has Decision Control | Decision Pattern |
|-------|----------|---------------------|-----------------|
| `SessionStart` | Session | No (context injection only) | hookSpecificOutput (additionalContext) |
| `SessionEnd` | Session | Not documented | -- |
| `PreToolUse` | Tool | Yes | hookSpecificOutput (permissionDecision) |
| `PostToolUse` | Tool | Yes | Top-level decision (block) |
| `PostToolUseFailure` | Tool | Yes | Top-level decision (block) |
| `PermissionRequest` | Permission | Yes | hookSpecificOutput (decision.behavior) |
| `UserPromptSubmit` | User | Yes | Top-level decision (block) |
| `Notification` | Info | No | None |
| `Stop` | Agent | Yes | Top-level decision (approve/block) |
| `SubagentStop` | Agent | Yes | Top-level decision (block) |
| `SubagentStart` | Agent | Not documented | -- |
| `TeammateIdle` | Agent | Not documented | -- |
| `TaskCompleted` | Agent | Not documented | -- |
| `PreCompact` | Context | No | None |

---

## Confidence Assessment

| Finding | Confidence | Rationale |
|---------|------------|-----------|
| Universal fields (continue, stopReason, suppressOutput, systemMessage) | **HIGH** | Directly from official Claude Code docs table at code.claude.com/docs/en/hooks |
| PreToolUse hookSpecificOutput fields (permissionDecision, permissionDecisionReason, updatedInput, additionalContext) | **HIGH** | Multiple official sources confirm: code.claude.com/docs/en/hooks + github.com/anthropics/claude-code SKILL.md |
| PostToolUse top-level decision pattern | **HIGH** | Directly from official docs |
| PostToolUse hookSpecificOutput.additionalContext | **HIGH** | Directly from official docs with example JSON |
| UserPromptSubmit decision + additionalContext (both top-level and hookSpecificOutput) | **HIGH** | Detailed APIDOC section in official docs |
| Stop/SubagentStop decision pattern | **HIGH** | Multiple official sources |
| PermissionRequest hookSpecificOutput.decision (behavior, updatedInput, updatedPermissions, message, interrupt) | **HIGH** | Directly from official docs |
| SessionStart hookSpecificOutput.additionalContext | **HIGH** | Directly from official docs with example JSON |
| Notification output (no decision) | **HIGH** | Official docs state "cannot block or modify" |
| PreCompact output (no decision) | **MEDIUM** | Only from SDK types; no detailed official docs found for output |
| SDK TypeScript interfaces (BaseHookOutput etc.) | **MEDIUM** | Community SDK, not official Anthropic types. Validated against real behavior. |
| hookSpecificOutput always requires hookEventName | **HIGH** | Stated in official docs: "It requires a `hookEventName` field set to the event name" |
| Exit code 2 blocks; exit code 0 allows JSON parsing | **HIGH** | Directly from official docs |
| PreToolUse simple top-level decision (alternative) | **MEDIUM** | Shown in official docs APIDOC but described as less capable than hookSpecificOutput |
| SessionEnd, SubagentStart, TeammateIdle, TaskCompleted output schemas | **LOW** | Events listed in plugins reference but no output schema documentation found |

---

## Key Discrepancies Found

### 1. SDK vs Official Docs: PreToolUse Decision Values

| Source | Field | Values |
|--------|-------|--------|
| SDK (`claude-code-hook-sdk`) | `decision` | `'approve'` \| `'block'` |
| Official docs (hookSpecificOutput) | `permissionDecision` | `'allow'` \| `'deny'` \| `'ask'` |
| Official docs (simple top-level) | `decision` | `'allow'` \| `'deny'` \| `'ask'` |

**Resolution:** The official docs are authoritative. The SDK uses a simplified model. For PreToolUse, use `hookSpecificOutput.permissionDecision` with values `allow`/`deny`/`ask`.

### 2. Stop Hook: approve vs omit

| Source | Allow Pattern |
|--------|--------------|
| Plugin dev SKILL.md | `decision: "approve"` |
| Official hooks docs | Omit `decision` field entirely |

**Resolution:** Both appear to work. Omitting is the documented default behavior.

### 3. `systemMessage` field name discrepancy

The plugin dev SKILL.md uses `systemMessage` as a top-level field. The SDK does not include this field. The official docs list it as a universal field. It appears to be a universal field that is valid but may not be in the SDK types.

---

## Sources and References

| # | Source | URL / Path | Content |
|---|--------|-----------|---------|
| 1 | Official Claude Code Hooks Docs | `code.claude.com/docs/en/hooks` | Authoritative hook event documentation with input/output schemas |
| 2 | Official Hooks Guide | `code.claude.com/docs/en/hooks-guide` | Troubleshooting and usage examples |
| 3 | Claude Code Plugins Reference | `code.claude.com/docs/en/plugins-reference` | Plugin manifest, hook configuration, event list |
| 4 | Claude Code Plugin Dev SKILL.md | `github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/hook-development/SKILL.md` | Hook development guide with APIDOC-style schemas |
| 5 | Claude Code Hook SDK | `github.com/mizunashi-mana/claude-code-hook-sdk` (Context7: `/mizunashi-mana/claude-code-hook-sdk`) | TypeScript SDK with Zod schemas, interfaces |
| 6 | Claude Code Main Repo | Context7: `/anthropics/claude-code` | Source code reference |

All findings were retrieved via Context7 library queries on 2026-02-17.
