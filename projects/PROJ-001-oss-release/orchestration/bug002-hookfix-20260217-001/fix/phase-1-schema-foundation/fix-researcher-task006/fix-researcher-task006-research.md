# fix-researcher-task006: Unified Research Synthesis

> **Agent:** fix-researcher-task006 (synthesis)
> **Date:** 2026-02-17
> **Version:** 1.0
> **Purpose:** Cross-referenced synthesis of all three research streams for BUG-002 hook schema foundation
> **Feeds Into:** fix-creator-task006 (JSON Schema creation)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Key conclusions from all three streams |
| [Source Inventory](#source-inventory) | All sources with dates and reliability ratings |
| [Cross-Reference Matrix](#cross-reference-matrix) | Stream agreement/disagreement on key findings |
| [Authoritative Hook Output Schemas](#authoritative-hook-output-schemas) | Definitive schema for each event type Jerry uses |
| [SubagentStop Revised Understanding](#subagentstop-revised-understanding) | Critical correction to prior assumptions |
| [Root Cause to Fix Mapping](#root-cause-to-fix-mapping) | RC-1 through RC-7 with research-backed fixes |
| [Impact on BUG-002 Task Definitions](#impact-on-bug-002-task-definitions) | TASK-003 and other affected tasks |
| [Discrepancies Between Sources](#discrepancies-between-sources) | Conflicts found and resolutions |
| [Confidence Assessment](#confidence-assessment) | Per-finding confidence with rationale |
| [Open Issues and Known Bugs](#open-issues-and-known-bugs) | Upstream issues affecting Jerry |
| [Recommendations for Schema Creation](#recommendations-for-schema-creation) | Guidance for fix-creator-task006 |

---

## Executive Summary

Three independent research streams -- Context7 library queries, web search with GitHub issue analysis, and direct codebase exploration -- converge on a consistent picture of the Claude Code hook output architecture. The key findings are:

1. **Two-tier output model confirmed.** All three streams agree: Claude Code uses universal fields (`continue`, `stopReason`, `suppressOutput`, `systemMessage`) plus event-specific decision control that follows one of three patterns.

2. **SubagentStop does NOT use hookSpecificOutput.** This is the most critical correction. All three streams confirm that SubagentStop uses ONLY top-level `decision` and `reason` fields. GitHub Issue #15485 (closed 2026-01-23, confirmed by Anthropic) explicitly resolved this ambiguity. TASK-003 in its current form correctly reflects this, but the broader BUG-002 description's assumption that SubagentStop might use `hookSpecificOutput` is corrected.

3. **PreToolUse deprecated API confirmed.** The top-level `decision` field with values `"approve"`/`"block"` is deprecated. The current API uses `hookSpecificOutput.permissionDecision` with values `"allow"`/`"deny"`/`"ask"`.

4. **All Jerry hooks except session_start_hook.py are broken.** The codebase analysis confirms 3 broken hooks with 7 distinct root causes, each traceable to a specific fix based on the authoritative documentation.

5. **No upstream JSON Schema files exist.** Neither the official Claude Code repository nor community resources provide reusable JSON Schema definitions for hook outputs. Schemas must be created from the documentation.

---

## Source Inventory

### Primary Sources (Anthropic-Authoritative)

| # | Source | Access Date | Reliability | Used By Stream(s) |
|---|--------|-------------|-------------|-------------------|
| S-01 | Official Claude Code Hooks Reference (`code.claude.com/docs/en/hooks`) | 2026-02-17 | Authoritative | Context7, WebSearch |
| S-02 | Official Claude Code Hooks Guide (`code.claude.com/docs/en/hooks-guide`) | 2026-02-17 | Authoritative | Context7, WebSearch |
| S-03 | Claude Code Plugins Reference (`code.claude.com/docs/en/plugins-reference`) | 2026-02-17 | Authoritative | Context7 |
| S-04 | Claude Code Plugin Dev SKILL.md (`github.com/anthropics/claude-code`) | 2026-02-17 | Primary (Anthropic repo) | Context7, WebSearch |

### Primary Sources (GitHub Issues)

| # | Source | Access Date | Reliability | Used By Stream(s) |
|---|--------|-------------|-------------|-------------------|
| S-05 | GitHub Issue #15485 -- Stop/SubagentStop schema clarification | 2026-02-17 | Primary (closed COMPLETED 2026-01-23) | WebSearch |
| S-06 | GitHub Issue #20221 -- SubagentStop prompt hooks don't prevent termination | 2026-02-17 | Primary (OPEN bug) | WebSearch |
| S-07 | GitHub Issue #4809 -- PostToolUse hook exit code 1 blocks execution | 2026-02-17 | Primary (referenced) | WebSearch |
| S-08 | GitHub Issue #19298 -- PermissionRequest hook cannot deny | 2026-02-17 | Primary (referenced) | WebSearch |

### Secondary Sources

| # | Source | Access Date | Reliability | Used By Stream(s) |
|---|--------|-------------|-------------|-------------------|
| S-09 | `@mizunashi-mana/claude-code-hook-sdk` (Context7) | 2026-02-17 | Secondary (community, Zod-validated) | Context7 |
| S-10 | Community Gist: `claude-code-hooks-schemas.md` | 2026-02-17 | Secondary (community) | WebSearch |

### Codebase Sources

| # | Source | Access Date | Reliability | Used By Stream(s) |
|---|--------|-------------|-------------|-------------------|
| S-11 | `scripts/session_start_hook.py` (lines 25-44) | 2026-02-17 | Primary (known-good reference) | Codebase |
| S-12 | `hooks/user-prompt-submit.py` (lines 57-63, 76-83) | 2026-02-17 | Primary (known-bad) | Codebase |
| S-13 | `scripts/pre_tool_use.py` (lines 275-372) | 2026-02-17 | Primary (known-bad) | Codebase |
| S-14 | `scripts/subagent_stop.py` (lines 173-190) | 2026-02-17 | Primary (known-bad) | Codebase |
| S-15 | `hooks/hooks.json` (lines 17, 40-51) | 2026-02-17 | Primary (partially broken config) | Codebase |
| S-16 | `schemas/hooks.schema.json` | 2026-02-17 | Primary (config schema only, no output schema) | Codebase |
| S-17 | `tests/contract/test_hook_output_contract.py` | 2026-02-17 | Primary (SessionStart only) | Codebase |
| S-18 | `tests/hooks/test_pre_tool_use.py` | 2026-02-17 | Primary (validates deprecated format) | Codebase |

---

## Cross-Reference Matrix

This matrix shows where all three research streams agree, partially agree, or conflict.

### Universal Output Fields

| Field | Context7 | WebSearch | Codebase | Agreement | Confidence |
|-------|----------|-----------|----------|-----------|------------|
| `continue` (boolean, default `true`) | Confirmed | Confirmed | Used in session_start_hook.py | **FULL** | **HIGH** |
| `stopReason` (string) | Confirmed | Confirmed | Not used in codebase | **FULL** | **HIGH** |
| `suppressOutput` (boolean, default `false`) | Confirmed | Confirmed | Not used in codebase | **FULL** | **HIGH** |
| `systemMessage` (string) | Confirmed | Confirmed | Used in session_start_hook.py | **FULL** | **HIGH** |

### Decision Control Patterns

| Finding | Context7 | WebSearch | Codebase | Agreement | Confidence |
|---------|----------|-----------|----------|-----------|------------|
| SessionStart: hookSpecificOutput with additionalContext only | Confirmed | Confirmed | Correctly implemented | **FULL** | **HIGH** |
| UserPromptSubmit: top-level decision + hookSpecificOutput for context | Confirmed | Confirmed | Missing hookEventName | **FULL** | **HIGH** |
| PreToolUse: hookSpecificOutput.permissionDecision (allow/deny/ask) | Confirmed | Confirmed | Uses deprecated top-level decision | **FULL** | **HIGH** |
| Stop: top-level decision only, NO hookSpecificOutput | Confirmed | Confirmed (Issue #15485) | N/A (not used) | **FULL** | **HIGH** |
| SubagentStop: top-level decision only, NO hookSpecificOutput | Confirmed | Confirmed (Issue #15485) | Wrong format entirely | **FULL** | **HIGH** |
| PermissionRequest: hookSpecificOutput.decision.behavior | Confirmed | Confirmed | N/A (not used by Jerry) | **FULL** | **HIGH** |

### Exit Code Semantics

| Exit Code | Context7 | WebSearch | Codebase | Agreement | Confidence |
|-----------|----------|-----------|----------|-----------|------------|
| 0 = success, parse JSON | Confirmed | Confirmed | session_start_hook.py correct | **FULL** | **HIGH** |
| 2 = block, JSON IGNORED | Confirmed | Confirmed | pre_tool_use.py misuses on errors | **FULL** | **HIGH** |
| 1 = non-blocking error | Not explicit | Confirmed | pre_tool_use.py uses for errors | **PARTIAL** | **HIGH** |

### Matcher Support

| Event | Context7 | WebSearch | Codebase | Agreement | Confidence |
|-------|----------|-----------|----------|-----------|------------|
| UserPromptSubmit: NO matchers | Not explicit | Confirmed | Has `matcher: "*"` (RC-7) | **FULL** | **HIGH** |
| Stop: NO matchers | Not explicit | Confirmed | Uses `matcher: "subagent:*"` (RC-5) | **FULL** | **HIGH** |
| SubagentStop: YES matchers (agent type) | Not explicit | Confirmed | Not registered under SubagentStop | **FULL** | **HIGH** |

---

## Authoritative Hook Output Schemas

The following schemas represent the definitive output format for each hook event type used by Jerry. These are derived from the convergence of all three research streams, with the official Claude Code documentation (S-01, S-02) as the primary authority.

### Common: Universal Fields (All Events)

```json
{
  "continue": true,
  "stopReason": "string (optional, shown to user when continue=false)",
  "suppressOutput": false,
  "systemMessage": "string (optional, shown to user as warning)"
}
```

All fields are optional. Default values: `continue=true`, `suppressOutput=false`.

**Confidence: HIGH** -- All three streams agree. Sources: S-01, S-09.

---

### SessionStart Output Schema

**Decision control:** Cannot block. Context injection only via `hookSpecificOutput`.

```json
{
  "systemMessage": "string (optional)",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "string -- injected into Claude's context"
  }
}
```

| Field Path | Type | Required | Description | Confidence |
|------------|------|----------|-------------|------------|
| `systemMessage` | string | Optional | Warning shown to user | HIGH |
| `hookSpecificOutput` | object | Optional | Hook-specific output wrapper | HIGH |
| `hookSpecificOutput.hookEventName` | string (literal `"SessionStart"`) | Required when using hookSpecificOutput | Event identifier | HIGH |
| `hookSpecificOutput.additionalContext` | string | Optional | Added to Claude's context. Multiple hooks' values concatenated. | HIGH |

**Plain text fallback:** Non-JSON stdout is also added as context (unique to SessionStart and UserPromptSubmit).

**Validation reference:** `scripts/session_start_hook.py` lines 25-44 (S-11) implements this correctly. This is the known-good reference implementation.

**Confidence: HIGH** -- All streams confirm. Codebase reference implementation validates.

---

### UserPromptSubmit Output Schema

**Decision control:** Top-level `decision` field. Can also inject context via top-level `additionalContext` or `hookSpecificOutput.additionalContext`.

```json
{
  "decision": "block",
  "reason": "string -- shown to user, NOT added to context",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "string -- injected into Claude's context"
  }
}
```

| Field Path | Type | Required | Values | Description | Confidence |
|------------|------|----------|--------|-------------|------------|
| `decision` | string | Optional | `"block"` | Prevents prompt processing. Omit to allow. | HIGH |
| `reason` | string | Optional | free text | Shown to user when blocking. NOT added to context. | HIGH |
| `hookSpecificOutput` | object | Optional | -- | Hook-specific output wrapper | HIGH |
| `hookSpecificOutput.hookEventName` | string | Required when using hookSpecificOutput | `"UserPromptSubmit"` | Event identifier | HIGH |
| `hookSpecificOutput.additionalContext` | string | Optional | free text | Added to Claude's context | HIGH |

**Plain text fallback:** Non-JSON stdout is also added as context.

**Matcher support:** NO. UserPromptSubmit does not support matchers. Any `matcher` field is silently ignored (S-02 WebSearch confirmed).

**Confidence: HIGH** -- Context7 and WebSearch confirm identical schema. S-01 APIDOC section provides detailed specification.

---

### PreToolUse Output Schema

**Decision control:** `hookSpecificOutput` with `permissionDecision` (PRIMARY). Top-level `decision` is DEPRECATED.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow | deny | ask",
    "permissionDecisionReason": "string",
    "updatedInput": { "field": "modified_value" },
    "additionalContext": "string -- added to Claude's context"
  }
}
```

| Field Path | Type | Required | Values | Description | Confidence |
|------------|------|----------|--------|-------------|------------|
| `hookSpecificOutput` | object | Required for decisions | -- | Hook-specific output wrapper | HIGH |
| `hookSpecificOutput.hookEventName` | string | Required | `"PreToolUse"` | Event identifier | HIGH |
| `hookSpecificOutput.permissionDecision` | string | Required for decision | `"allow"`, `"deny"`, `"ask"` | `allow` bypasses permissions, `deny` blocks, `ask` prompts user | HIGH |
| `hookSpecificOutput.permissionDecisionReason` | string | Optional | free text | For allow/ask: shown to user. For deny: shown to Claude. | HIGH |
| `hookSpecificOutput.updatedInput` | object | Optional | `Record<string, unknown>` | Modifies tool input before execution | HIGH |
| `hookSpecificOutput.additionalContext` | string | Optional | free text | Added to Claude's context before tool executes | HIGH |

**Deprecated fields (backward compatibility):**

| Deprecated Field | Deprecated Value | Maps To |
|------------------|------------------|---------|
| `decision` (top-level) | `"approve"` | `hookSpecificOutput.permissionDecision: "allow"` |
| `decision` (top-level) | `"block"` | `hookSpecificOutput.permissionDecision: "deny"` |
| `reason` (top-level) | -- | `hookSpecificOutput.permissionDecisionReason` |

**Important:** The official docs (S-01) explicitly state: "Unlike other hooks that use a top-level `decision` field, PreToolUse returns its decision inside a `hookSpecificOutput` object." The deprecated top-level format may still work via backward-compatibility mapping, but relying on it is risky.

**Matcher support:** YES. Filters by tool name (e.g., `"Bash"`, `"Edit|Write"`, `"mcp__.*"`).

**Confidence: HIGH** -- All three streams confirm. Context7 found both patterns; WebSearch confirms deprecated status of top-level fields; codebase confirms current code uses the deprecated format.

---

### SubagentStop Output Schema

**Decision control:** Top-level `decision` and `reason` ONLY. Does NOT use `hookSpecificOutput`.

```json
{
  "decision": "block",
  "reason": "string -- tells Claude why subagent should continue"
}
```

| Field | Type | Required | Values | Description | Confidence |
|-------|------|----------|--------|-------------|------------|
| `decision` | string | Optional | `"block"` | Prevents subagent from stopping. Omit to allow. | HIGH |
| `reason` | string | Required when `decision` is `"block"` | free text | Tells Claude why it should continue | HIGH |

**CRITICAL: No hookSpecificOutput, No hookEventName.** This is confirmed by:
- Context7 (S-01, S-04): Lists SubagentStop in top-level decision group
- WebSearch (S-05 -- GitHub Issue #15485): Anthropic explicitly confirmed (closed COMPLETED 2026-01-23) that Stop and SubagentStop use ONLY top-level fields. This is enforced at the TypeScript type system level via the `SyncHookJSONOutput` union type.
- SDK types (S-09): `SubagentStopHookOutput extends BaseHookOutput { decision?: 'block'; reason?: string; }` -- no hookSpecificOutput.

**Matcher support:** YES. Filters by agent type (e.g., `"Bash"`, `"Explore"`, `"Plan"`, custom agent names).

**Infinite loop prevention:** Check `stop_hook_active` in input. If `true`, the hook has already triggered continuation -- exit 0 to allow stopping, or risk infinite loops.

**Known upstream bug (S-06 -- Issue #20221):** Prompt-based SubagentStop hooks correctly evaluate and send feedback, but do NOT actually prevent subagent termination. The subagent receives feedback but never gets another turn. Workaround: use command-based hooks (`type: "command"`). This bug is OPEN as of 2026-02-17. **Jerry's SubagentStop hook is command-based, so this bug does not directly affect it, but it is worth noting for future reference.**

**Confidence: HIGH** -- All streams agree. GitHub Issue #15485 provides authoritative Anthropic confirmation.

---

### Additional Event Schemas (For Reference, Not Used by Jerry)

The following events are documented but not currently used by Jerry. Included for completeness of the schema set.

#### PostToolUse

Top-level `decision` + optional `hookSpecificOutput` for context injection:

```json
{
  "decision": "block",
  "reason": "string",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "string",
    "updatedMCPToolOutput": "replacement value (MCP tools only)"
  }
}
```

**Confidence: HIGH** -- All streams agree. S-01 provides example JSON.

#### Stop

Top-level `decision` only (same as SubagentStop):

```json
{
  "decision": "block",
  "reason": "string -- MUST be provided when blocking"
}
```

**Confidence: HIGH** -- All streams agree. Issue #15485 confirms no hookSpecificOutput.

#### Notification, PreCompact, SessionEnd

No decision control. Universal fields only.

**Confidence: HIGH (Notification), MEDIUM (PreCompact/SessionEnd)** -- Limited documentation for output specifics.

---

## SubagentStop Revised Understanding

This section documents the critical correction to the prior understanding of SubagentStop, which has material impact on TASK-003.

### Prior Assumption (INCORRECT)

The initial BUG-002 analysis and early task definitions may have assumed SubagentStop follows a pattern similar to PreToolUse or SessionStart with `hookSpecificOutput` containing `hookEventName` and additional fields.

### Corrected Understanding (AUTHORITATIVE)

SubagentStop is architecturally distinct from events that use `hookSpecificOutput`. It belongs to a group of events (Stop, SubagentStop) that use ONLY top-level `decision` and `reason` fields. This is not a documentation gap -- it is a deliberate architectural choice, confirmed by Anthropic in GitHub Issue #15485 (S-05, closed COMPLETED 2026-01-23).

### Evidence Chain

| Evidence | Source | Date | Status |
|----------|--------|------|--------|
| Official docs group SubagentStop with top-level decision events | S-01 | 2026-02-17 | Current |
| GitHub Issue #15485 explicitly resolves ambiguity | S-05 | 2026-01-23 | Closed COMPLETED |
| SDK TypeScript types: `SubagentStopHookOutput { decision?: 'block'; reason?: string; }` | S-09 | 2026-02-17 | Current |
| Context7 research confirms top-level pattern | Context7 stream | 2026-02-17 | Current |
| WebSearch research confirms top-level pattern | WebSearch stream | 2026-02-17 | Current |

### What This Means for subagent_stop.py

The current `subagent_stop.py` output is wrong in two ways:
1. **Wrong event registration** (under `Stop` instead of `SubagentStop`) -- already identified as RC-5
2. **Wrong output format** (custom fields like `action`, `to_agent`, `work_items`) -- already identified as RC-6

The fix is simpler than expected: the output should be ONLY `{"decision": "block", "reason": "..."}` or an empty/no-JSON response to allow. There is no `hookSpecificOutput` wrapper, no `hookEventName`, and no room for custom fields like handoff metadata.

### Impact on Jerry's Orchestration

The SubagentStop hook cannot pass structured handoff data (agent names, work items, summaries) through the hook output mechanism. If this orchestration data is needed, it must be communicated through a different channel (e.g., filesystem, transcript, or context injection via a different hook event). The SubagentStop hook can only make a binary decision: allow the subagent to stop, or block it with a reason.

**Confidence: HIGH** -- Confirmed by Anthropic, all three research streams, and TypeScript type system enforcement.

---

## Root Cause to Fix Mapping

Each root cause (RC-1 through RC-7) is mapped to the authoritative fix based on the research findings.

### RC-1: UserPromptSubmit Missing hookEventName

| Attribute | Value |
|-----------|-------|
| **Root Cause** | `hooks/user-prompt-submit.py:57-63` outputs `hookSpecificOutput` without `hookEventName: "UserPromptSubmit"` |
| **Impact** | L2 per-prompt quality reinforcement completely non-functional |
| **Fix** | Add `"hookEventName": "UserPromptSubmit"` to the `hookSpecificOutput` object |
| **Authority** | S-01 (Official docs), S-11 (reference implementation pattern) |
| **Fix Complexity** | Trivial -- single field addition |
| **Task** | TASK-001 |
| **Confidence** | **HIGH** -- All streams agree. Reference implementation (session_start_hook.py) demonstrates correct pattern. |

**Correct output after fix:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "<quality-reinforcement>\n...\n</quality-reinforcement>"
  }
}
```

**Additional fix needed (error path):** Lines 76-83 currently output empty `{}` on error. This should output a valid minimal JSON (either `{}` with no hookSpecificOutput, or a structure with empty additionalContext). An empty object `{}` is technically valid -- it means "allow, no additional context" -- but a `systemMessage` warning would be more informative.

---

### RC-2: PreToolUse Uses Deprecated Top-Level decision Field

| Attribute | Value |
|-----------|-------|
| **Root Cause** | `scripts/pre_tool_use.py:275,286,301,336,365` uses top-level `decision` and `reason` instead of `hookSpecificOutput.permissionDecision` |
| **Impact** | Security guardrails on deprecated API; may stop working in future Claude Code updates |
| **Fix** | Migrate all output paths to `hookSpecificOutput` pattern with `permissionDecision` |
| **Authority** | S-01 (Official docs explicitly state hookSpecificOutput is the current API for PreToolUse) |
| **Fix Complexity** | Medium -- 5+ output paths to modify |
| **Task** | TASK-002 |
| **Confidence** | **HIGH** -- All streams confirm deprecation. Official docs are explicit. |

---

### RC-3: PreToolUse Uses Deprecated Decision Values

| Attribute | Value |
|-----------|-------|
| **Root Cause** | `scripts/pre_tool_use.py:365` uses `"approve"` instead of `"allow"`, and lines 275,286 use `"block"` instead of `"deny"` |
| **Impact** | Deprecated values may work via backward-compat mapping but are not guaranteed |
| **Fix** | Replace `"approve"` with `"allow"`, `"block"` with `"deny"` in `permissionDecision` field |
| **Authority** | S-01 (Official docs: deprecated values map approve->allow, block->deny) |
| **Fix Complexity** | Trivial -- string value replacements within the RC-2 fix |
| **Task** | TASK-002 (combined with RC-2) |
| **Confidence** | **HIGH** -- All streams confirm. WebSearch found explicit deprecation note. |

---

### RC-4: PreToolUse Exit Code 2 on Errors

| Attribute | Value |
|-----------|-------|
| **Root Cause** | `scripts/pre_tool_use.py:370,373` returns exit code 2 on errors, which blocks tool calls |
| **Impact** | Script errors block legitimate tool usage instead of failing open |
| **Fix** | Change error exit codes from 2 to 0 (fail-open). Exit code 2 means "block" -- it should only be used for intentional blocking. Errors should exit 0 (or exit 1 for non-blocking error logging). |
| **Authority** | S-01, S-02 (Exit code semantics table) |
| **Fix Complexity** | Simple -- change exit code values |
| **Task** | TASK-002 (combined with RC-2, RC-3) |
| **Confidence** | **HIGH** -- All streams agree on exit code semantics. WebSearch provides explicit per-event table. |

**Exit code reference (from WebSearch S-02):**
- Exit 0: Success. JSON parsed from stdout.
- Exit 1: Non-blocking error. stderr shown in verbose mode. Action continues.
- Exit 2: Blocking error. Action blocked. JSON IGNORED.

---

### RC-5: SubagentStop Registered Under Wrong Event

| Attribute | Value |
|-----------|-------|
| **Root Cause** | `hooks/hooks.json:40-51` registers `subagent_stop.py` under the `Stop` event with `matcher: "subagent:*"`. The `Stop` event does NOT support matchers -- they are silently ignored. This means the hook fires for ALL stop events (main agent stops), not just subagent stops. |
| **Impact** | Hook fires at wrong time (main agent stops) and not at the intended time (subagent stops). The `"subagent:*"` matcher is silently ignored because Stop does not support matchers. |
| **Fix** | Change event registration from `"Stop"` to `"SubagentStop"` in hooks.json. SubagentStop DOES support matchers on agent type. Replace `"subagent:*"` with a valid agent type matcher (e.g., `"*"` for all agent types, or specific agent types like `"Bash"`, `"Explore"`, `"Plan"`). |
| **Authority** | S-01, S-02 (Matcher support matrix), S-05 (Issue #15485) |
| **Fix Complexity** | Simple -- config change in hooks.json |
| **Task** | TASK-003 and TASK-004 (combined) |
| **Confidence** | **HIGH** -- WebSearch provides complete matcher support matrix. Context7 confirms SubagentStop supports matchers. |

---

### RC-6: SubagentStop Non-Standard Output Fields

| Attribute | Value |
|-----------|-------|
| **Root Cause** | `scripts/subagent_stop.py:173-186,190` outputs non-standard fields (`action`, `to_agent`, `context`, `work_items`, `summary`, `status_transition`) not recognized by Claude Code |
| **Impact** | Entire output is ignored by Claude Code; no decision is communicated |
| **Fix** | Replace entire output structure with top-level `decision`/`reason` format. Remove all custom fields. SubagentStop only supports: `decision: "block"` + `reason` (to prevent stopping) or no output / empty JSON (to allow stopping). |
| **Authority** | S-01, S-05 (Issue #15485 -- Anthropic confirmed top-level fields only), S-09 (SDK types) |
| **Fix Complexity** | Medium -- requires redesigning the output logic. Handoff metadata cannot be passed through SubagentStop output. |
| **Task** | TASK-003 |
| **Confidence** | **HIGH** -- All streams confirm. Anthropic confirmation in Issue #15485 is definitive. |

**Architecture implication:** The current subagent_stop.py attempts to use the hook output as a structured handoff mechanism (passing agent names, work items, summaries). This is fundamentally incompatible with the SubagentStop output schema, which only allows a binary block/allow decision. The orchestration metadata must be communicated through alternative channels if it is still needed.

---

### RC-7: UserPromptSubmit Unnecessary Matcher

| Attribute | Value |
|-----------|-------|
| **Root Cause** | `hooks/hooks.json:17` has `matcher: "*"` on UserPromptSubmit, which does not support matchers |
| **Impact** | Cosmetic -- silently ignored. Does not cause functional failure. |
| **Fix** | Remove the `matcher` field from the UserPromptSubmit hook entry in hooks.json |
| **Authority** | S-02 (WebSearch: matcher support matrix shows UserPromptSubmit does not support matchers) |
| **Fix Complexity** | Trivial -- remove one field from config |
| **Task** | TASK-004 |
| **Confidence** | **HIGH** -- WebSearch provides explicit matcher support matrix. |

---

## Impact on BUG-002 Task Definitions

### TASK-003: Fix SubagentStop Hook (REQUIRES REVISION)

**Current definition states:**
> "Output format: SubagentStop uses the same decision control as Stop hooks"
> ```json
> { "decision": "block", "reason": "reason why subagent should continue" }
> ```

**Assessment:** TASK-003 is CORRECT in its output format description. It already specifies top-level `decision`/`reason` without `hookSpecificOutput`. No revision needed for the output format.

**However, TASK-003 should be updated to note:**
1. The known upstream bug (Issue #20221) where prompt-based SubagentStop hooks do not actually prevent termination. Jerry's command-based hook is not affected, but this should be documented.
2. The `stop_hook_active` infinite loop prevention check should be included in the acceptance criteria.
3. The current custom output fields (`action`, `to_agent`, `work_items`, etc.) represent orchestration logic that needs to be either removed or moved to an alternative communication channel.

### TASK-001: Fix UserPromptSubmit Hook (CORRECT AS-IS)

TASK-001 correctly identifies the missing `hookEventName` field. No revision needed.

### TASK-002: Fix PreToolUse Hook (CORRECT AS-IS)

TASK-002 correctly identifies the migration to `hookSpecificOutput.permissionDecision`. No revision needed.

### TASK-004: Fix hooks.json Config (CORRECT AS-IS)

TASK-004 correctly identifies the event registration and matcher issues. No revision needed.

### TASK-005: Add Hook Schema Tests (DEPENDENT ON THIS SYNTHESIS)

TASK-005 depends on TASK-006 (schema creation). This synthesis provides the authoritative schema definitions that fix-creator-task006 will use to generate JSON Schema files.

### TASK-006: Create Hook Output JSON Schema (THIS TASK)

This synthesis is the key deliverable of TASK-006 research phase. It provides the authoritative field-level specifications needed by fix-creator-task006 to create JSON Schema 2020-12 files.

---

## Discrepancies Between Sources

### Resolved Discrepancies

| # | Discrepancy | Context7 | WebSearch | Codebase | Resolution | Confidence |
|---|-------------|----------|-----------|----------|------------|------------|
| D-1 | PreToolUse decision values: SDK uses `approve`/`block` vs docs use `allow`/`deny`/`ask` | Found both | Confirmed deprecated | Uses deprecated | **Official docs authoritative.** Use `allow`/`deny`/`ask`. SDK uses simplified deprecated model. | HIGH |
| D-2 | Stop hook: `decision: "approve"` vs omit to allow | SKILL.md says `approve` | Official docs say omit | N/A | **Both work.** Omitting is documented default. `"approve"` appears to be accepted but undocumented in official hooks reference. | MEDIUM |
| D-3 | `systemMessage` field: in SDK types? | Found in official docs as universal | Confirmed universal | Used in session_start_hook.py | **Universal field.** SDK types may be incomplete. | HIGH |
| D-4 | PostToolUseFailure: does it support `decision: "block"`? | Lists in top-level decision group | Summary table includes it, but dedicated section only shows additionalContext. Exit code table says "Shows stderr to Claude" (cannot block). | N/A | **Ambiguous.** The dedicated PostToolUseFailure section does not show decision:block, and the exit-code table says it cannot block. Schema should accept the field but note it may have no practical effect. | MEDIUM |

### Unresolved Discrepancies

| # | Discrepancy | Notes | Impact on Jerry | Resolution Approach |
|---|-------------|-------|-----------------|---------------------|
| D-5 | Stop hook `decision` values: `"approve"` | SKILL.md lists `"approve" | "block"` but official docs only document `"block"` (omit to allow). Jerry does not use Stop hooks, so this is informational only. | None | Accept both in schema for robustness. |
| D-6 | PostToolUse `updatedMCPToolOutput` field | Only documented in WebSearch stream (S-01). Context7 stream did not find this field. May be newer addition. | None (Jerry doesn't use PostToolUse hooks) | Include in PostToolUse schema as optional. |

---

## Confidence Assessment

### Per-Finding Confidence Summary

| Finding | Confidence | Source Count | Rationale |
|---------|------------|-------------|-----------|
| Universal fields (continue, stopReason, suppressOutput, systemMessage) | **HIGH** | 3/3 streams | All streams agree. Official docs table. Reference impl validates. |
| SessionStart schema (hookSpecificOutput + additionalContext) | **HIGH** | 3/3 streams | All streams agree. Known-good reference implementation confirms. |
| UserPromptSubmit schema (top-level decision + hookSpecificOutput context) | **HIGH** | 3/3 streams | All streams agree. Official APIDOC section. |
| PreToolUse current API (hookSpecificOutput.permissionDecision) | **HIGH** | 3/3 streams | All streams agree. Official docs explicit about deprecation. |
| PreToolUse deprecated API still works (backward compat) | **MEDIUM** | 2/3 streams | Context7 and WebSearch mention backward compat. No explicit removal date. |
| SubagentStop: NO hookSpecificOutput | **HIGH** | 3/3 streams + Anthropic confirmation | Issue #15485 is definitive. TypeScript types enforce it. |
| SubagentStop: top-level decision/reason only | **HIGH** | 3/3 streams + Anthropic confirmation | Same as above. |
| Exit code 2 = block, JSON ignored | **HIGH** | 3/3 streams | All streams agree. Official docs table. |
| Exit code 1 = non-blocking error | **HIGH** | 2/3 streams | WebSearch explicit. Context7 implicit. Consistent semantics. |
| Matcher support matrix | **HIGH** | 2/3 streams | WebSearch provides complete matrix. Context7 partially confirms. |
| hookEventName required in hookSpecificOutput | **HIGH** | 3/3 streams | Official docs: "It requires a `hookEventName` field set to the event name." |
| No upstream JSON Schema files exist | **HIGH** | 3/3 streams | None found in any source. Must create from documentation. |
| SubagentStop prompt hook bug (Issue #20221) | **HIGH** | 1/3 streams (WebSearch) | Direct GitHub issue. OPEN status. Not relevant to command-based hooks. |
| SubagentStop input fields (agent_id, agent_type, agent_transcript_path, stop_hook_active) | **HIGH** | 2/3 streams | Context7 and WebSearch both confirm. |

### Overall Research Confidence

**OVERALL: HIGH.** All three research streams converge on the same conclusions for every finding relevant to BUG-002. No unresolved conflicts exist for any finding that affects the fix implementation. The SubagentStop clarification (no hookSpecificOutput) is the strongest finding, backed by an Anthropic-closed GitHub issue.

---

## Open Issues and Known Bugs

### Upstream Bugs Affecting Jerry

| Issue | Status | Impact on Jerry | Workaround |
|-------|--------|-----------------|------------|
| #20221: SubagentStop prompt hooks don't prevent termination | OPEN | None -- Jerry uses command-based hooks | Use `type: "command"` (Jerry already does this) |
| #19298: PermissionRequest hook cannot deny | Referenced | None -- Jerry doesn't use PermissionRequest hooks | N/A |
| #4809: PostToolUse exit code 1 blocks execution | Referenced | None -- Jerry doesn't use PostToolUse hooks | N/A |

### Schema Gaps

| Gap | Impact | Recommendation |
|-----|--------|----------------|
| No official JSON Schema files exist upstream | Must create our own | Create from authoritative documentation (this synthesis) |
| `schemas/hooks.schema.json` only validates config, not output | No output validation exists | TASK-006 creates output schemas; TASK-005 creates tests |
| `schemas/hooks.schema.json` does not include `SubagentStop` in allowed events | Config validation may reject correct SubagentStop registration | Update config schema as part of TASK-004 |

---

## Recommendations for Schema Creation

These recommendations are for fix-creator-task006, which will create JSON Schema 2020-12 files.

### Schema File Structure

Create the following files in `schemas/hooks/`:

| File | Content | Priority |
|------|---------|----------|
| `hook-output-base.schema.json` | Universal fields shared by all events | Required |
| `session-start-output.schema.json` | SessionStart-specific output | Required (validation reference) |
| `user-prompt-submit-output.schema.json` | UserPromptSubmit-specific output | Required (RC-1 fix target) |
| `pre-tool-use-output.schema.json` | PreToolUse-specific output | Required (RC-2/3 fix target) |
| `subagent-stop-output.schema.json` | SubagentStop-specific output | Required (RC-5/6 fix target) |

### Schema Design Principles

1. **Use `$ref` for base fields.** All schemas should reference `hook-output-base.schema.json` for universal fields using `allOf` composition.

2. **Use JSON Schema draft 2020-12.** Set `$schema: "https://json-schema.org/draft/2020-12/schema"`.

3. **Be permissive on additional properties.** Claude Code may add new fields in future versions. Use `"additionalProperties": true` at the top level to avoid breaking on unknown fields.

4. **Be strict on required fields.** When `hookSpecificOutput` is present, `hookEventName` MUST be required. When `decision` is `"block"`, `reason` SHOULD be required.

5. **Document deprecated alternatives.** For PreToolUse, include comments or `deprecated` annotations for the top-level `decision` field pattern. The schema should validate the CURRENT API, not the deprecated one.

6. **Validate against known outputs.**
   - Known-good: `session_start_hook.py` output MUST pass SessionStart schema.
   - Known-bad: Current `user-prompt-submit.py` output MUST fail UserPromptSubmit schema (missing `hookEventName`).
   - Known-bad: Current `pre_tool_use.py` output SHOULD fail PreToolUse schema (uses deprecated top-level decision).
   - Known-bad: Current `subagent_stop.py` output MUST fail SubagentStop schema (non-standard fields).

### SubagentStop Schema: Keep It Simple

The SubagentStop schema is the simplest of all four:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "SubagentStop Hook Output",
  "description": "Output schema for SubagentStop hook events. Uses ONLY top-level decision/reason fields. Does NOT use hookSpecificOutput.",
  "type": "object",
  "properties": {
    "decision": { "type": "string", "enum": ["block"] },
    "reason": { "type": "string" },
    "continue": { "type": "boolean" },
    "stopReason": { "type": "string" },
    "suppressOutput": { "type": "boolean" },
    "systemMessage": { "type": "string" }
  },
  "if": {
    "properties": { "decision": { "const": "block" } },
    "required": ["decision"]
  },
  "then": {
    "required": ["reason"]
  },
  "additionalProperties": true
}
```

Note: No `hookSpecificOutput` field. No `hookEventName`. This is intentional and correct.

---

*Document ID: fix-researcher-task006-research*
*Workflow ID: bug002-hookfix-20260217-001*
*Phase: 1 (Schema Foundation)*
*Version: 1.0*
*All paths are repository-relative*
