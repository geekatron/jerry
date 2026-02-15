# EN-705: UserPromptSubmit Quality Hook

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Implement L2 Per-Prompt Reinforcement hook to counteract context rot
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** infrastructure
> **Created:** 2026-02-14
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-008
> **Owner:** —
> **Effort:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Business Value](#business-value) | How this enabler supports the parent feature |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Progress Summary](#progress-summary) | Completion status and metrics |
| [Evidence](#evidence) | Proof of completion |
| [Dependencies](#dependencies) | What this depends on |
| [History](#history) | Change log |

---

## Summary

Implement the L2 Per-Prompt Reinforcement hook. Creates `hooks/user-prompt-submit.py` (Claude Code hook adapter) and `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py` (enforcement logic). Counteracts context rot by re-injecting critical rules on every user prompt. Budget: 600 tokens per session (V-024). The hook is immune to context rot by design -- reinforcement content is re-injected every prompt regardless of LLM context state. This is the primary mechanism for compensating L1 (Static Context) degradation beyond ~20K context tokens.

## Problem Statement

Jerry's L1 static context (~12,476 tokens in `.claude/rules/`) degrades as the context window fills. Research on context rot (Chroma Research) shows that LLM compliance with instructions degrades significantly as context grows. Without a per-prompt reinforcement mechanism, there is no way to counteract this degradation during a session. The UserPromptSubmit hook (V-005) delivering V-024 (Context Reinforcement via Repetition) is the designated L2 layer in the 5-layer hybrid enforcement architecture (ADR-EPIC002-002). Without L2, the entire L1 static context layer has no compensation for degradation. V-024 scored 4.11 WCS in the EN-402 priority analysis, placing it in Tier 1.

## Business Value

Delivers the primary mechanism for counteracting L1 context rot by re-injecting critical rules on every user prompt. This is the only enforcement layer that actively compensates for degradation of static context as the context window fills.

### Features Unlocked

- Per-prompt reinforcement of constitutional principles, quality thresholds, and enforcement calibration
- Context-rot-immune rule delivery within a 600-token budget (V-024)

## Technical Approach

1. **Create `hooks/user-prompt-submit.py`** -- Claude Code hook adapter that intercepts the UserPromptSubmit event. This file follows Claude Code's hook protocol: reads JSON from stdin, writes JSON to stdout. Delegates all enforcement logic to the engine class. Implements fail-open behavior: on any error, returns an empty block and logs the error.

2. **Create `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py`** -- `PromptReinforcementEngine` class containing the reinforcement logic, separated from hook infrastructure per hexagonal architecture. Responsible for:
   - Extracting L2-REINJECT content from rules files
   - Assembling the reinforcement preamble
   - Enforcing the 600-token budget constraint
   - Returning structured reinforcement content

3. **Design reinforcement content** -- The preamble must include within the 600-token budget:
   - Quality gate threshold (0.92)
   - Constitutional principles reminder (P-003, P-020, P-022)
   - Self-review reminder (S-010)
   - Leniency bias calibration for S-014 (LLM-as-Judge)
   - UV-only Python environment reminder

4. **Update hooks configuration** -- Update `hooks.json` (or equivalent Claude Code hooks configuration) with the UserPromptSubmit event registration.

5. **Implement fail-open error handling** -- Hook errors must never block user work. On error: return empty/passthrough block, log the error for diagnostics.

6. **Testing** -- Unit tests for `PromptReinforcementEngine` (token budget validation, content assembly, error handling). Integration test for the hook end-to-end. Verify `uv run pytest` passes.

**Design Source:** EPIC-002 EN-403/TASK-002 (UserPromptSubmit design), EN-405/TASK-006 (preamble content)

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [████████████████████] 100% (4/4 completed)           |
| Effort:    [████████████████████] 100% (8/8 points completed)    |
+------------------------------------------------------------------+
| Overall:   [████████████████████] 100%                            |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 4 |
| **Completed Tasks** | 4 |
| **Completion %** | 100% |

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| 1 | `hooks/user-prompt-submit.py` created (Claude Code hook adapter) | [ ] |
| 2 | `PromptReinforcementEngine` class created in `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py` | [ ] |
| 3 | Engine extracts L2-REINJECT content from rules | [ ] |
| 4 | Engine applies 600-token budget constraint | [ ] |
| 5 | Hooks configuration updated with UserPromptSubmit event | [ ] |
| 6 | Fail-open on error (empty block returned, error logged) | [ ] |
| 7 | Unit tests for engine (content assembly, budget, error handling) | [ ] |
| 8 | Integration test for hook end-to-end | [ ] |
| 9 | `uv run pytest` passes | [ ] |

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| user-prompt-submit.py | Hook Script | Claude Code hook adapter for UserPromptSubmit event | `hooks/user-prompt-submit.py` |
| PromptReinforcementEngine | Source Code | L2 per-prompt reinforcement engine | `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py` |
| Unit + Integration Tests | Test Suite | Engine and hook tests | `tests/` |

### Verification Checklist

- [x] All acceptance criteria verified
- [x] All tasks completed
- [x] Quality gate passed (>= 0.92)

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-402 | Enforcement priority analysis (V-024 scored 4.11 WCS, Tier 1) |
| depends_on | EN-403 | Hook-based enforcement design (TASK-002: UserPromptSubmit design) |
| depends_on | EN-405 | Session context enforcement (TASK-006: preamble content design) |
| related_to | EN-703 | PreToolUse enforcement (L3) compensates when L2 is ignored by LLM |
| related_to | EN-706 | SessionStart quality context (L1) -- L2 compensates for L1 context rot |
| parent | FEAT-008 | Quality Framework Implementation |

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created. Implements L2 Per-Prompt Reinforcement with V-024 context reinforcement. 600-token budget. Design sourced from EPIC-002 EN-403/TASK-002 and EN-405/TASK-006. |
