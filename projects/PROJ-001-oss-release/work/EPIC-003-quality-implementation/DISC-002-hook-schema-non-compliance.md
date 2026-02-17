# EPIC-003:DISC-002: Hook Schema Non-Compliance

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-17 (Claude)
PURPOSE: Document systematic hook schema violations across Jerry Framework hooks
-->

> **Type:** discovery
> **Status:** validated
> **Priority:** critical
> **Impact:** critical
> **Created:** 2026-02-17
> **Completed:** 2026-02-17
> **Parent:** EPIC-003
> **Owner:** Claude
> **Source:** Debug log analysis + Claude Code official documentation

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Core finding and key observations |
| [Context](#context) | How this was discovered |
| [Finding](#finding) | Detailed technical findings per hook script |
| [Evidence](#evidence) | Sources and verification |
| [Implications](#implications) | Impact on quality framework |
| [Relationships](#relationships) | Created work items |
| [Document History](#document-history) | Change log |

---

## Summary

All Jerry Framework hook scripts except `session_start_hook.py` produce JSON output that violates Claude Code's documented hook schema. The L2 per-prompt quality reinforcement layer is **completely non-functional** because the `UserPromptSubmit` hook output fails validation.

**Key Findings:**
- `user-prompt-submit.py`: Missing required `hookEventName` field in `hookSpecificOutput` — L2 enforcement layer broken
- `pre_tool_use.py`: Uses deprecated top-level `decision`/`reason` fields instead of `hookSpecificOutput.permissionDecision`; uses deprecated `"approve"`/`"block"` values; incorrect exit code semantics
- `subagent_stop.py`: Registered under wrong event (`Stop` instead of `SubagentStop`); `Stop` doesn't support matchers; non-standard output fields
- `hooks.json`: Unnecessary matchers on events that don't support them; wrong event registration

**Validation:** Confirmed against official Claude Code documentation (code.claude.com/docs/en/hooks, Context7 /anthropics/claude-code)

---

## Context

### Background

The L2 enforcement layer (EN-705) was implemented to inject quality reinforcement rules on every user prompt. Debug logging revealed that `UserPromptSubmit` hook JSON was being rejected by Claude Code's schema validator, meaning zero quality reinforcement has been reaching Claude's context since implementation.

### Research Question

Are all Jerry hook scripts compliant with the current Claude Code hook JSON schema?

### Investigation Approach

1. Extracted error from `/tmp/claude-debug-jerry-wt-1.log` showing schema validation failure
2. Retrieved authoritative schema from Claude Code official docs (code.claude.com/docs/en/hooks) and Context7
3. Audited all 4 hook scripts against the documented schema
4. Cross-referenced with the correctly-implemented `session_start_hook.py` as a known-good example

---

## Finding

### F1: UserPromptSubmit Hook — Missing hookEventName (Critical)

**File:** `hooks/user-prompt-submit.py:57-63`

**Issue:** Output contains `hookSpecificOutput.additionalContext` but is missing the required `hookEventName: "UserPromptSubmit"` field.

**Schema Requirement (from docs):**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "string"
  }
}
```

**Actual Output:**
```json
{
  "hookSpecificOutput": {
    "additionalContext": "<quality-reinforcement>...</quality-reinforcement>"
  }
}
```

**Impact:** L2 quality reinforcement completely non-functional. Every prompt submission generates a validation error. Zero reinforcement tokens reaching Claude's context.

### F2: PreToolUse Hook — Deprecated API Usage (High)

**File:** `scripts/pre_tool_use.py:275, 286, 301, 336, 365`

**Issues:**
1. Uses deprecated top-level `{"decision": "block", "reason": ...}` format. Per docs: "PreToolUse previously used top-level decision and reason fields, but these are deprecated. Use `hookSpecificOutput.permissionDecision` and `hookSpecificOutput.permissionDecisionReason` instead."
2. Uses deprecated values `"approve"` and `"block"` instead of canonical `"allow"` and `"deny"`
3. Exit code 2 on errors (lines 370, 373) blocks tool calls instead of failing open — exit 2 means "blocking error" per docs

**Correct Format:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "reason string"
  }
}
```

### F3: SubagentStop Hook — Wrong Event Registration (High)

**File:** `scripts/subagent_stop.py` + `hooks/hooks.json:40-51`

**Issues:**
1. Registered under `Stop` event (hooks.json line 40) but should be `SubagentStop`
2. `Stop` event does not support matchers — `"matcher": "subagent:*"` is silently ignored
3. Output uses non-standard fields (`action`, `to_agent`, `work_items`, `summary`) not recognized by schema
4. Exit code 1 for "no handoff needed" — exit 1 is a non-blocking error in hook protocol

**Result:** This hook never fires for subagent completions. It may fire when the main agent stops, but the matcher is ignored so it runs on every Stop, outputting non-standard JSON.

### F4: hooks.json Configuration Issues (Medium)

**File:** `hooks/hooks.json`

1. Line 17: `"matcher": "*"` on `UserPromptSubmit` — silently ignored per docs ("UserPromptSubmit and Stop don't support matchers")
2. Lines 40-51: `Stop` event with `"matcher": "subagent:*"` — Stop doesn't support matchers; should be `SubagentStop`

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Debug Log | UserPromptSubmit hook validation error | `/tmp/claude-debug-jerry-wt-1.log` | 2026-02-17 |
| E-002 | Official Docs | Claude Code Hooks Reference | [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks) | 2026-02-17 |
| E-003 | Context7 | Claude Code library docs (/anthropics/claude-code) | Context7 query | 2026-02-17 |
| E-004 | Source Code | Known-good pattern in `session_start_hook.py:38-39` | Repository | 2026-02-17 |

---

## Implications

### Impact on Project

The L2 enforcement layer (per-prompt quality reinforcement) has been non-functional since implementation. This means:
- Constitutional rules are NOT being re-injected per prompt as designed (ADR-EPIC002-002)
- Quality gate thresholds are NOT being reinforced during context rot
- The entire 5-layer enforcement architecture has a broken layer

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Quality degradation during long sessions due to missing L2 reinforcement | Critical | Fix UserPromptSubmit hook immediately |
| PreToolUse security guardrails may break in future Claude Code versions | High | Migrate to current API |
| SubagentStop hook provides zero orchestration value | Medium | Fix event registration |

---

## Relationships

### Creates

- [BUG-002](./BUG-002-hook-schema-validation-failures/BUG-002-hook-schema-validation-failures.md) - Fix all hook schema validation failures

### Informs

- EN-705 (L2 Per-Prompt Reinforcement Hook) — original implementation has the bug
- ADR-EPIC002-002 (5-layer enforcement architecture) — L2 layer non-functional

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-17 | Claude | Created discovery. Validated against official Claude Code docs. |
