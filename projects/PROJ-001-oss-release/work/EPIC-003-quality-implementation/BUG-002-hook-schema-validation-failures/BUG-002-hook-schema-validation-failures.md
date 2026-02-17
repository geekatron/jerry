# BUG-002: Hook JSON Schema Validation Failures

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
CREATED: 2026-02-17 (Claude)
PURPOSE: Fix all hook scripts producing invalid JSON that fails Claude Code schema validation
-->

> **Type:** bug
> **Status:** completed
> **Priority:** critical
> **Impact:** critical
> **Severity:** critical
> **Created:** 2026-02-17
> **Due:** ---
> **Completed:** 2026-02-17
> **Parent:** EPIC-003
> **Owner:** Claude
> **Found In:** EPIC-003 (EN-705 L2 implementation)
> **Fix Version:** ---

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Bug overview and key details |
| [Reproduction Steps](#reproduction-steps) | How to reproduce |
| [Environment](#environment) | Where the bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Why it's broken |
| [Fix Description](#fix-description) | Solution for each hook |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Related Items](#related-items) | Linked work items |
| [History](#history) | Status changes |

---

## Summary

All Jerry Framework hook scripts except `session_start_hook.py` produce JSON output that fails Claude Code's schema validation. The `UserPromptSubmit` hook is the most critical — L2 per-prompt quality reinforcement has been completely non-functional since EN-705 implementation.

**Key Details:**
- **Symptom:** Hook JSON validation errors in debug logs; L2 reinforcement not reaching Claude context
- **Frequency:** Every prompt submission (UserPromptSubmit), every tool call (PreToolUse), every agent stop (SubagentStop)
- **Workaround:** None — hooks silently fail

---

## Reproduction Steps

### Prerequisites

- Claude Code with `--debug` flag or debug logging enabled
- Jerry Framework hooks configured via `hooks/hooks.json`

### Steps to Reproduce

1. Start a Claude Code session with Jerry hooks enabled
2. Submit any prompt
3. Check debug log at `/tmp/claude-debug-jerry-wt-1.log`

### Expected Result

`UserPromptSubmit` hook outputs valid JSON with `hookEventName` field; `additionalContext` is injected into Claude's context.

### Actual Result

```
Hook JSON output validation failed: Invalid input
```

The `hookSpecificOutput` is missing `hookEventName: "UserPromptSubmit"`, causing full JSON rejection. No quality reinforcement reaches Claude.

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | macOS Darwin 25.3.0 |
| **Runtime** | Claude Code (Opus 4.6) |
| **Application Version** | Jerry Framework (EPIC-003 quality implementation) |
| **Configuration** | hooks/hooks.json plugin hooks |

---

## Root Cause Analysis

### Investigation Summary

Cross-referenced all 4 hook scripts against the authoritative Claude Code hooks schema (code.claude.com/docs/en/hooks, fetched 2026-02-17).

### Root Causes

| # | Hook Script | Root Cause | Impact |
|---|-------------|-----------|--------|
| RC-1 | `hooks/user-prompt-submit.py:57-63` | Missing `hookEventName: "UserPromptSubmit"` in `hookSpecificOutput` | L2 reinforcement broken |
| RC-2 | `scripts/pre_tool_use.py:275,286,301,336,365` | Uses deprecated top-level `decision`/`reason` instead of `hookSpecificOutput.permissionDecision` | Security guardrails on deprecated API |
| RC-3 | `scripts/pre_tool_use.py:365` | Uses deprecated `"approve"`/`"block"` values instead of `"allow"`/`"deny"` | Backwards-compat mapping may break |
| RC-4 | `scripts/pre_tool_use.py:370,373` | Exit code 2 on errors blocks tool calls instead of failing open | Errors block legitimate tool usage |
| RC-5 | `scripts/subagent_stop.py` + `hooks/hooks.json:40-51` | Registered under `Stop` event instead of `SubagentStop`; Stop doesn't support matchers | Hook never fires for subagents |
| RC-6 | `scripts/subagent_stop.py:173-186,190` | Non-standard JSON output fields not in schema | Output ignored by Claude Code |
| RC-7 | `hooks/hooks.json:17` | Unnecessary `matcher: "*"` on UserPromptSubmit | Silently ignored; cosmetic |

### Contributing Factors

- No automated schema validation tests for hook output
- `session_start_hook.py` was implemented correctly but the pattern was not replicated to other hooks
- Hook schema documentation was not consulted during EN-705 implementation

---

## Fix Description

### Solution Approach

Fix each hook script to conform to the authoritative Claude Code hook JSON schema per official docs. Each fix is a separate task.

### Changes Required

| Task | File | Change |
|------|------|--------|
| TASK-001 | `hooks/user-prompt-submit.py` | Add `hookEventName: "UserPromptSubmit"` to `hookSpecificOutput` |
| TASK-002 | `scripts/pre_tool_use.py` | Migrate to `hookSpecificOutput` format with `permissionDecision`; fix exit codes |
| TASK-003 | `scripts/subagent_stop.py` + `hooks/hooks.json` | Move to `SubagentStop` event; fix output format; fix exit codes |
| TASK-004 | `hooks/hooks.json` | Remove unnecessary matchers; fix event registrations |
| TASK-005 | `tests/` | Add schema validation tests for all hook outputs |
| TASK-006 | `schemas/hooks/` | Find or generate JSON Schema definitions for hook outputs (TASK-005 depends on this) |

---

## Children (Tasks)

| ID | Title | Status | Effort | Owner |
|----|-------|--------|--------|-------|
| [TASK-001](./tasks/TASK-001-fix-user-prompt-submit-hook.md) | Fix UserPromptSubmit hook — add hookEventName | done | 1 | Claude |
| [TASK-002](./tasks/TASK-002-fix-pre-tool-use-hook.md) | Fix PreToolUse hook — migrate to hookSpecificOutput API | done | 3 | Claude |
| [TASK-003](./tasks/TASK-003-fix-subagent-stop-hook.md) | Fix SubagentStop hook — correct event and output | done | 2 | Claude |
| [TASK-004](./tasks/TASK-004-fix-hooks-json-config.md) | Fix hooks.json configuration | done | 1 | Claude |
| [TASK-005](./tasks/TASK-005-add-hook-schema-tests.md) | Add hook output schema validation tests | done | 3 | Claude |
| [TASK-006](./tasks/TASK-006-create-hook-output-schema.md) | Create or extract hook output JSON Schema definition | done | 3 | Claude |

---

## Acceptance Criteria

### Fix Verification

- [x] `user-prompt-submit.py` outputs valid JSON with `hookEventName: "UserPromptSubmit"`
- [x] `pre_tool_use.py` uses `hookSpecificOutput.permissionDecision` (not deprecated top-level `decision`)
- [x] `pre_tool_use.py` uses `"allow"`/`"deny"` (not deprecated `"approve"`/`"block"`)
- [x] `pre_tool_use.py` exits 0 on errors (fail-open), not exit 2
- [x] `subagent_stop.py` registered under `SubagentStop` event in hooks.json
- [x] `subagent_stop.py` outputs schema-compliant JSON
- [x] `hooks.json` has no matchers on events that don't support them
- [x] All hooks pass schema validation tests
- [x] JSON Schema files exist for all hook event types used by Jerry
- [x] L2 quality reinforcement confirmed working via live session test (2026-02-17)

### Quality Checklist

- [x] Regression tests added for all hook output schemas
- [x] Existing tests still passing (3195/3195 PASS)
- [x] No new issues introduced
- [x] `session_start_hook.py` pattern confirmed as reference implementation

---

## Related Items

### Hierarchy

- **Parent:** [EPIC-003: Quality Framework Implementation](../EPIC-003-quality-implementation.md)

### Related Items

- **Discovery:** [DISC-002](../DISC-002-hook-schema-non-compliance.md) — Root cause analysis
- **Related Enabler:** EN-705 (L2 Per-Prompt Reinforcement Hook) — original implementation
- **Related ADR:** ADR-EPIC002-002 (5-layer enforcement architecture)
- **Reference Implementation:** `scripts/session_start_hook.py:34-44` — correct pattern

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-17 | Claude | pending | Bug filed. 4 hook scripts with schema violations. 5 tasks created. DISC-002 documents findings. |
| 2026-02-17 | Claude | pending | TASK-006 added: Create or extract JSON Schema definitions for hook outputs. TASK-005 depends on TASK-006. Total: 6 tasks, 13 effort points. |
| 2026-02-17 | Claude | done | BUG-002 RESOLVED via 5-phase orchestration workflow (bug002-hookfix-20260217-001). Phase 1: Schema foundation (C3 score 0.927). Phase 2: Parallel hook fixes (3 streams). Phase 3: Schema validation tests (31 tests). Phase 4: C4 tournament (0.9125 REVISE). Phase 5: P1-P5 remediation + re-score (0.9355 PASS). 3195 tests pass, 8/8 schema validations pass. All 7 root causes fixed. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Bug |
| **SAFe** | Defect |
| **JIRA** | Bug |
