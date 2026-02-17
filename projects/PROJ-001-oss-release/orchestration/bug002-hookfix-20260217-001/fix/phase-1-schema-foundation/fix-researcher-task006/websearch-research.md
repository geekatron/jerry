# Claude Code Hook Output JSON Schema -- Web Search Research Report

> Authoritative documentation extraction for hook output JSON schemas.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Sources Consulted](#sources-consulted) | All URLs with access dates |
| [Exit Code Semantics](#exit-code-semantics) | What exit codes 0, 1, 2 mean |
| [Universal JSON Output Fields](#universal-json-output-fields) | Fields common to all hook events |
| [Decision Control Patterns](#decision-control-patterns) | Summary of which events use which pattern |
| [Per-Event Output Schemas](#per-event-output-schemas) | Exact JSON structures per hook event type |
| [Matcher Support Matrix](#matcher-support-matrix) | Which events support matchers |
| [Common Input Fields](#common-input-fields) | Shared input envelope across all events |
| [Known Issues and Discrepancies](#known-issues-and-discrepancies) | Bugs, gaps between docs and behavior |
| [Prompt/Agent Hook Response Schema](#promptagent-hook-response-schema) | Output format for prompt-based and agent-based hooks |

---

## Sources Consulted

| # | Source | URL | Date Accessed | Reliability |
|---|--------|-----|---------------|-------------|
| 1 | Official Hooks Reference (primary) | https://code.claude.com/docs/en/hooks | 2026-02-17 | Authoritative (Anthropic) |
| 2 | Official Hooks Guide | https://code.claude.com/docs/en/hooks-guide | 2026-02-17 | Authoritative (Anthropic) |
| 3 | GitHub Issue #15485 -- Stop/SubagentStop schema clarification | https://github.com/anthropics/claude-code/issues/15485 | 2026-02-17 | Primary (closed as COMPLETED 2026-01-23) |
| 4 | GitHub Issue #20221 -- SubagentStop prompt hooks don't prevent termination | https://github.com/anthropics/claude-code/issues/20221 | 2026-02-17 | Primary (OPEN bug) |
| 5 | GitHub Issue #4809 -- PostToolUse hook exit code 1 blocks execution | https://github.com/anthropics/claude-code/issues/4809 | 2026-02-17 | Primary (referenced) |
| 6 | Community Gist: claude-code-hooks-schemas.md | https://gist.github.com/FrancisBourre/50dca37124ecc43eaf08328cdcccdb34 | 2026-02-17 | Secondary (community) |
| 7 | claude-code plugin-dev hook-development SKILL.md | https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/hook-development/SKILL.md | 2026-02-17 | Primary (Anthropic repo) |
| 8 | GitHub Issue #19298 -- PermissionRequest hook cannot deny | https://github.com/anthropics/claude-code/issues/19298 | 2026-02-17 | Primary (referenced) |

---

## Exit Code Semantics

Exit codes are the simplest way to control hook behavior. JSON output is only processed on exit code 0.

| Exit Code | Meaning | Behavior |
|-----------|---------|----------|
| **0** | Success | Action proceeds. Claude Code parses stdout for JSON output fields. For `UserPromptSubmit` and `SessionStart`, stdout is added as context visible to Claude. For all other events, stdout is only shown in verbose mode (`Ctrl+O`). |
| **2** | Blocking error | Action is blocked (for events that support blocking). stderr text is fed back to Claude as an error message. **JSON in stdout is IGNORED.** |
| **Any other** (e.g., 1) | Non-blocking error | Action continues. stderr is shown in verbose mode (`Ctrl+O`) but NOT fed to Claude. Execution is not interrupted. |

### Exit Code 2 Behavior Per Event

| Hook Event | Can Block? | Effect of Exit 2 |
|------------|-----------|-------------------|
| `PreToolUse` | Yes | Blocks the tool call |
| `PermissionRequest` | Yes | Denies the permission |
| `UserPromptSubmit` | Yes | Blocks prompt processing, erases the prompt |
| `Stop` | Yes | Prevents Claude from stopping, continues conversation |
| `SubagentStop` | Yes | Prevents the subagent from stopping |
| `TeammateIdle` | Yes | Prevents teammate from going idle |
| `TaskCompleted` | Yes | Prevents task from being marked completed |
| `PostToolUse` | No | Shows stderr to Claude (tool already ran) |
| `PostToolUseFailure` | No | Shows stderr to Claude (tool already failed) |
| `Notification` | No | Shows stderr to user only |
| `SubagentStart` | No | Shows stderr to user only |
| `SessionStart` | No | Shows stderr to user only |
| `SessionEnd` | No | Shows stderr to user only |
| `PreCompact` | No | Shows stderr to user only |

**Critical rule:** You must choose ONE approach per hook -- either exit codes alone, or exit 0 + JSON. Never mix exit 2 with JSON output.

---

## Universal JSON Output Fields

These fields are recognized across ALL hook event types when output as JSON on stdout (exit code 0):

| Field | Type | Default | Required | Description |
|-------|------|---------|----------|-------------|
| `continue` | boolean | `true` | No | If `false`, Claude stops ALL processing after hook runs. **Takes precedence over any event-specific decision fields.** This is the ultimate override. |
| `stopReason` | string | none | No | Message shown to user when `continue` is `false`. Not shown to Claude. |
| `suppressOutput` | boolean | `false` | No | If `true`, hides stdout from verbose mode output. |
| `systemMessage` | string | none | No | Warning message shown to the user. For async hooks, delivered on next conversation turn. |

### Priority Order

1. `continue: false` -- overrides everything; Claude stops entirely
2. JSON `decision: "block"` -- blocks the specific action
3. Exit code 2 -- blocks the specific action (but JSON is ignored)

---

## Decision Control Patterns

Not every event supports blocking or controlling behavior through JSON. The official documentation defines three distinct patterns:

| Pattern | Events Using It | Key Fields |
|---------|----------------|------------|
| **Top-level `decision`** | `UserPromptSubmit`, `PostToolUse`, `PostToolUseFailure`, `Stop`, `SubagentStop` | `decision: "block"`, `reason` |
| **`hookSpecificOutput` with `permissionDecision`** | `PreToolUse` | `permissionDecision` (allow/deny/ask), `permissionDecisionReason`, `updatedInput`, `additionalContext` |
| **`hookSpecificOutput` with `decision.behavior`** | `PermissionRequest` | `decision.behavior` (allow/deny), `updatedInput`, `updatedPermissions`, `message`, `interrupt` |
| **Exit code only** | `TeammateIdle`, `TaskCompleted` | Exit code 2 blocks; stderr is feedback |
| **No decision control** | `SessionStart`, `SessionEnd`, `Notification`, `SubagentStart`, `PreCompact` | Cannot block; can add context or run side effects |

---

## Per-Event Output Schemas

### SessionStart

**Decision control:** Cannot block session start. Can add context.

**Output JSON:**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "string -- added to Claude's context"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `hookSpecificOutput.hookEventName` | string (literal `"SessionStart"`) | Yes (if using hookSpecificOutput) | Must match the event name |
| `hookSpecificOutput.additionalContext` | string | No | Added to Claude's context. Multiple hooks' values are concatenated. |

**Additional behavior:** Plain text stdout is also added as context visible to Claude (unlike most other events where stdout is only shown in verbose mode).

**Special feature:** Has access to `CLAUDE_ENV_FILE` environment variable for persisting env vars.

---

### UserPromptSubmit

**Decision control:** Top-level `decision` field.

**Output JSON (blocking):**

```json
{
  "decision": "block",
  "reason": "Explanation shown to user when blocked",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "string -- added to Claude's context"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `decision` | string, enum: `"block"` | No | `"block"` prevents prompt processing and erases it. Omit to allow. |
| `reason` | string | No (recommended when blocking) | Shown to user when `decision` is `"block"`. NOT added to context. |
| `hookSpecificOutput.hookEventName` | string (literal `"UserPromptSubmit"`) | Yes (if using hookSpecificOutput) | Must match event name |
| `hookSpecificOutput.additionalContext` | string | No | Added to Claude's context |

**Additional behavior:** Plain non-JSON text on stdout is also added as context. The `additionalContext` field is added "more discretely" than plain stdout.

---

### PreToolUse

**Decision control:** Uses `hookSpecificOutput` with `permissionDecision` (NOT top-level `decision`).

**Output JSON:**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow | deny | ask",
    "permissionDecisionReason": "string",
    "updatedInput": {
      "field_to_modify": "new value"
    },
    "additionalContext": "string -- added to Claude's context before tool executes"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `hookSpecificOutput.hookEventName` | string (literal `"PreToolUse"`) | Yes | Must match event name |
| `hookSpecificOutput.permissionDecision` | string, enum: `"allow"`, `"deny"`, `"ask"` | No | `"allow"` bypasses permission system. `"deny"` prevents tool call. `"ask"` prompts user to confirm. |
| `hookSpecificOutput.permissionDecisionReason` | string | No | For `"allow"` and `"ask"`: shown to user but NOT to Claude. For `"deny"`: shown TO Claude. |
| `hookSpecificOutput.updatedInput` | object | No | Modifies tool input parameters before execution. Combine with `"allow"` for auto-approve, or `"ask"` to show modified input to user. |
| `hookSpecificOutput.additionalContext` | string | No | Added to Claude's context before tool executes |

**Deprecated fields:** PreToolUse previously used top-level `decision` and `reason` fields. The deprecated values `"approve"` and `"block"` map to `"allow"` and `"deny"` respectively. Use `hookSpecificOutput.permissionDecision` instead.

---

### PermissionRequest

**Decision control:** Uses `hookSpecificOutput` with nested `decision` object containing `behavior` field.

**Output JSON (allow):**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "modified command"
      },
      "updatedPermissions": [
        { "type": "toolAlwaysAllow", "tool": "Bash" }
      ]
    }
  }
}
```

**Output JSON (deny):**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "deny",
      "message": "Tells Claude why permission was denied",
      "interrupt": true
    }
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `hookSpecificOutput.hookEventName` | string (literal `"PermissionRequest"`) | Yes | Must match event name |
| `hookSpecificOutput.decision.behavior` | string, enum: `"allow"`, `"deny"` | Yes (if returning decision) | `"allow"` grants permission. `"deny"` denies it. |
| `hookSpecificOutput.decision.updatedInput` | object | No (allow only) | Modifies tool input before execution |
| `hookSpecificOutput.decision.updatedPermissions` | array | No (allow only) | Applies permission rule updates, equivalent to user selecting "always allow" |
| `hookSpecificOutput.decision.message` | string | No (deny only) | Tells Claude why permission was denied |
| `hookSpecificOutput.decision.interrupt` | boolean | No (deny only) | If `true`, stops Claude |

**Important limitation:** PermissionRequest hooks do NOT fire in non-interactive mode (`-p`). Use PreToolUse hooks for automated permission decisions.

---

### PostToolUse

**Decision control:** Top-level `decision` field.

**Output JSON:**

```json
{
  "decision": "block",
  "reason": "Explanation shown to Claude",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude",
    "updatedMCPToolOutput": "replacement output value"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `decision` | string, enum: `"block"` | No | `"block"` prompts Claude with the `reason`. Omit to allow. |
| `reason` | string | No (recommended when blocking) | Explanation shown to Claude when `decision` is `"block"` |
| `hookSpecificOutput.hookEventName` | string (literal `"PostToolUse"`) | Yes (if using hookSpecificOutput) | Must match event name |
| `hookSpecificOutput.additionalContext` | string | No | Additional context for Claude |
| `hookSpecificOutput.updatedMCPToolOutput` | any | No | **MCP tools only.** Replaces the tool's output with the provided value. |

**Note:** PostToolUse cannot undo actions (tool already ran). `decision: "block"` provides feedback to Claude but does not reverse the action.

---

### PostToolUseFailure

**Decision control:** Top-level `decision` field (same as PostToolUse).

**Output JSON:**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "Additional information about the failure for Claude"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `hookSpecificOutput.hookEventName` | string (literal `"PostToolUseFailure"`) | Yes (if using hookSpecificOutput) | Must match event name |
| `hookSpecificOutput.additionalContext` | string | No | Additional context for Claude alongside the error |

**Note:** The decision control table lists PostToolUseFailure under top-level `decision` pattern, but the dedicated section only shows `additionalContext`. Treat it as: top-level `decision: "block"` + `reason` are available, plus `hookSpecificOutput.additionalContext`.

---

### Notification

**Decision control:** Cannot block or modify notifications.

**Output JSON:**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "Notification",
    "additionalContext": "string -- added to Claude's context"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `hookSpecificOutput.additionalContext` | string | No | Added to Claude's context |

---

### SubagentStart

**Decision control:** Cannot block subagent creation. Can inject context.

**Output JSON:**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Follow security guidelines for this task"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `hookSpecificOutput.hookEventName` | string (literal `"SubagentStart"`) | Yes (if using hookSpecificOutput) | Must match event name |
| `hookSpecificOutput.additionalContext` | string | No | Added to the subagent's context |

---

### SubagentStop

**Decision control:** Top-level `decision` field. Same format as Stop.

**Output JSON:**

```json
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `decision` | string, enum: `"block"` | No | `"block"` prevents subagent from stopping. Omit to allow. |
| `reason` | string | **Required when `decision` is `"block"`** | Tells Claude why it should continue. |

**CRITICAL FINDING (Source #3, Issue #15485):** Stop and SubagentStop do **NOT** use `hookSpecificOutput`. They use ONLY top-level `decision` and `reason` fields. The `hookEventName` field is NOT used for these events. This was confirmed by Anthropic (issue closed as COMPLETED 2026-01-23) and is enforced at the TypeScript SDK type system level via the `SyncHookJSONOutput` union type.

**Known Bug (Source #4, Issue #20221):** Prompt-based SubagentStop hooks correctly evaluate and send feedback, but do NOT actually prevent subagent termination. The subagent receives the feedback as a user message but never gets another turn to respond. This issue is OPEN as of 2026-02-17.

---

### Stop

**Decision control:** Top-level `decision` field. Identical format to SubagentStop.

**Output JSON:**

```json
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `decision` | string, enum: `"block"` | No | `"block"` prevents Claude from stopping. Omit to allow. |
| `reason` | string | **Required when `decision` is `"block"`** | Tells Claude why it should continue. |

**CRITICAL:** Does NOT use `hookSpecificOutput` or `hookEventName`. Top-level fields only.

**Infinite loop prevention:** Check `stop_hook_active` in the input JSON. If `true`, the hook has already triggered a continuation. Exit 0 to allow Claude to stop, or risk infinite loops.

---

### TeammateIdle

**Decision control:** Exit code only. Does NOT support JSON decision control.

Exit code 2 prevents teammate from going idle; stderr is fed back as feedback.

---

### TaskCompleted

**Decision control:** Exit code only. Does NOT support JSON decision control.

Exit code 2 prevents task from being marked completed; stderr is fed back as feedback.

---

### PreCompact

**Decision control:** None. Cannot block compaction.

Only universal JSON output fields apply.

---

### SessionEnd

**Decision control:** None. Cannot block session termination.

Only universal JSON output fields apply. Can perform cleanup tasks.

---

## Matcher Support Matrix

| Event | Matcher Supported | What Matcher Filters | Example Values |
|-------|-------------------|---------------------|----------------|
| `PreToolUse` | Yes | tool name | `Bash`, `Edit\|Write`, `mcp__.*` |
| `PostToolUse` | Yes | tool name | Same as PreToolUse |
| `PostToolUseFailure` | Yes | tool name | Same as PreToolUse |
| `PermissionRequest` | Yes | tool name | Same as PreToolUse |
| `SessionStart` | Yes | how session started | `startup`, `resume`, `clear`, `compact` |
| `SessionEnd` | Yes | why session ended | `clear`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other` |
| `Notification` | Yes | notification type | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog` |
| `SubagentStart` | Yes | agent type | `Bash`, `Explore`, `Plan`, custom agent names |
| `SubagentStop` | Yes | agent type | Same as SubagentStart |
| `PreCompact` | Yes | what triggered compaction | `manual`, `auto` |
| `UserPromptSubmit` | **No** | N/A | Always fires on every occurrence |
| `Stop` | **No** | N/A | Always fires on every occurrence |
| `TeammateIdle` | **No** | N/A | Always fires on every occurrence |
| `TaskCompleted` | **No** | N/A | Always fires on every occurrence |

**Important:** If you add a `matcher` field to events that don't support matchers, it is silently ignored.

---

## Common Input Fields

All hook events receive these fields via stdin as JSON:

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | string | Current session identifier |
| `transcript_path` | string | Path to conversation JSON |
| `cwd` | string | Current working directory when hook is invoked |
| `permission_mode` | string, enum: `"default"`, `"plan"`, `"acceptEdits"`, `"dontAsk"`, `"bypassPermissions"` | Current permission mode |
| `hook_event_name` | string | Name of the event that fired |

### Event-Specific Input Additions

| Event | Additional Fields |
|-------|------------------|
| `SessionStart` | `source` (startup/resume/clear/compact), `model`, optional `agent_type` |
| `UserPromptSubmit` | `prompt` |
| `PreToolUse` | `tool_name`, `tool_input` (varies by tool), `tool_use_id` |
| `PermissionRequest` | `tool_name`, `tool_input`, optional `permission_suggestions` array |
| `PostToolUse` | `tool_name`, `tool_input`, `tool_response`, `tool_use_id` |
| `PostToolUseFailure` | `tool_name`, `tool_input`, `tool_use_id`, `error`, optional `is_interrupt` |
| `Notification` | `message`, optional `title`, `notification_type` |
| `SubagentStart` | `agent_id`, `agent_type` |
| `SubagentStop` | `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path` |
| `Stop` | `stop_hook_active` |
| `TeammateIdle` | `teammate_name`, `team_name` |
| `TaskCompleted` | `task_id`, `task_subject`, optional `task_description`, optional `teammate_name`, optional `team_name` |
| `PreCompact` | `trigger` (manual/auto), `custom_instructions` |
| `SessionEnd` | `reason` |

---

## Known Issues and Discrepancies

### 1. Stop/SubagentStop hookSpecificOutput Ambiguity (RESOLVED)

**Source:** GitHub Issue #15485 (closed 2026-01-23)

**Issue:** Documentation was ambiguous about whether Stop/SubagentStop should use `hookSpecificOutput` wrapper like other hooks.

**Resolution:** Stop and SubagentStop use ONLY top-level `decision` and `reason` fields. They do NOT use `hookSpecificOutput` or `hookEventName`. This is enforced at the TypeScript type system level.

### 2. SubagentStop Prompt Hooks Don't Prevent Termination (OPEN BUG)

**Source:** GitHub Issue #20221

**Issue:** Prompt-based SubagentStop hooks send feedback but do not actually prevent subagent termination. The subagent receives feedback as a user message with `isMeta: true` but never gets another turn.

**Status:** OPEN as of 2026-02-17. No fix implemented.

**Workaround:** Use command-based hooks (type: "command") instead of prompt-based hooks for SubagentStop.

### 3. PreToolUse Deprecated Fields

**Source:** Official docs (Source #1)

**Discrepancy:** PreToolUse previously used top-level `decision` (with values `"approve"` and `"block"`) and `reason`. These are deprecated. Current format uses `hookSpecificOutput.permissionDecision` with values `"allow"`, `"deny"`, `"ask"`. The deprecated `"approve"` maps to `"allow"` and `"block"` maps to `"deny"`.

**Impact for validation:** A permissive schema should accept both old and new formats for backward compatibility.

### 4. PostToolUseFailure Decision Fields

**Discrepancy:** The decision control summary table groups PostToolUseFailure with events using top-level `decision`, but the dedicated PostToolUseFailure section only documents `additionalContext` in `hookSpecificOutput`. It is unclear whether `decision: "block"` + `reason` is actually supported for PostToolUseFailure. The exit code 2 behavior table says PostToolUseFailure "Shows stderr to Claude" (cannot block), suggesting `decision: "block"` may not have practical effect.

### 5. JSON Validation Failures from Shell Profile

**Source:** Official guide (Source #2), multiple GitHub issues

**Issue:** Shell profiles (~/.zshrc, ~/.bashrc) with unconditional `echo` statements contaminate hook stdout, causing JSON parsing failures.

**Fix:** Wrap profile echo statements in `if [[ $- == *i* ]]; then ... fi` guards.

### 6. Discrepancy Between plugin-dev SKILL.md and Official Docs

**Source:** Source #7 vs Source #1

The plugin-dev SKILL.md describes Stop/SubagentStop output as having `decision` values of `"approve"` or `"block"`. The official docs only document `"block"` (omit `decision` to allow). The SKILL.md may be outdated.

### 7. PermissionRequest Hook Bugs

**Source:** GitHub Issue #19298 (deny not working), Issue #12176 (race condition with allow)

There are reported bugs where PermissionRequest hooks returning deny do not always take effect, and hooks returning allow may still briefly show the permission dialog.

---

## Prompt/Agent Hook Response Schema

For hooks with `type: "prompt"` or `type: "agent"`, the LLM/agent returns a different schema:

```json
{
  "ok": true | false,
  "reason": "Explanation for the decision"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ok` | boolean | Yes | `true` allows the action, `false` prevents it |
| `reason` | string | Required when `ok` is `false` | Explanation shown to Claude |

**Supported events for prompt/agent hooks:** `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `TaskCompleted`.

**NOT supported:** `TeammateIdle` does not support prompt-based or agent-based hooks.

---

## Complete Hook Event List (14 events)

1. `SessionStart` -- session begins/resumes
2. `UserPromptSubmit` -- user submits prompt
3. `PreToolUse` -- before tool call
4. `PermissionRequest` -- permission dialog shown
5. `PostToolUse` -- after successful tool call
6. `PostToolUseFailure` -- after failed tool call
7. `Notification` -- notification sent
8. `SubagentStart` -- subagent spawned
9. `SubagentStop` -- subagent finished
10. `Stop` -- main agent finished responding
11. `TeammateIdle` -- teammate about to go idle
12. `TaskCompleted` -- task being marked complete
13. `PreCompact` -- before context compaction
14. `SessionEnd` -- session terminates

---

## Summary of hookSpecificOutput Usage

| Event | Uses hookSpecificOutput? | hookEventName Required? | Key hookSpecificOutput Fields |
|-------|-------------------------|------------------------|-------------------------------|
| `SessionStart` | Yes | Yes | `additionalContext` |
| `UserPromptSubmit` | Yes | Yes | `additionalContext` |
| `PreToolUse` | **Yes (primary)** | Yes | `permissionDecision`, `permissionDecisionReason`, `updatedInput`, `additionalContext` |
| `PermissionRequest` | **Yes (primary)** | Yes | `decision.behavior`, `decision.updatedInput`, `decision.updatedPermissions`, `decision.message`, `decision.interrupt` |
| `PostToolUse` | Yes | Yes | `additionalContext`, `updatedMCPToolOutput` |
| `PostToolUseFailure` | Yes | Yes | `additionalContext` |
| `Notification` | Yes | Yes | `additionalContext` |
| `SubagentStart` | Yes | Yes | `additionalContext` |
| `SubagentStop` | **No** | **No** | N/A -- uses top-level `decision`, `reason` only |
| `Stop` | **No** | **No** | N/A -- uses top-level `decision`, `reason` only |
| `TeammateIdle` | **No** | **No** | N/A -- exit code only |
| `TaskCompleted` | **No** | **No** | N/A -- exit code only |
| `PreCompact` | No documented fields | No | Universal fields only |
| `SessionEnd` | No documented fields | No | Universal fields only |
