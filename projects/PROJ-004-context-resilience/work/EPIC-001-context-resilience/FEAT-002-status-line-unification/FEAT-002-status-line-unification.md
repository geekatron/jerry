# FEAT-002: Status Line / Context Monitoring Unification & Automatic Session Rotation

> **Type:** feature
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-21
> **Due:** --
> **Completed:** 2026-02-21
> **Parent:** EPIC-001
> **Owner:** Claude
> **Target Sprint:** --
> **GitHub Issue:** [#63](https://github.com/geekatron/jerry/issues/63)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and value proposition |
| [Benefit Hypothesis](#benefit-hypothesis) | Expected benefits |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [MVP Definition](#mvp-definition) | Minimum viable scope |
| [Children Stories/Enablers](#children-storiesenablers) | Work item inventory |
| [Progress Summary](#progress-summary) | Overall feature progress |
| [Related Items](#related-items) | Dependencies |
| [History](#history) | Status changes |

---

## Summary

Jerry's `context_monitoring` bounded context owns all context domain logic. The `jerry context estimate` CLI command reads exact `current_usage` data from Claude Code stdin and returns structured JSON. Automatic session rotation is orchestrated across multiple hooks (prompt-submit escalation, stop gate, pre-compact checkpoint, session-start resumption). Sub-agent context tracking via transcript parsing. A 5-tier threshold SSOT (NOMINAL/LOW/WARNING/CRITICAL/EMERGENCY) is consumed by jerry-statusline.

**Value Proposition:**
- jerry-statusline reads real context fill from Jerry's domain layer — no duplicate heuristic logic
- Automatic graduated escalation from WARNING through EMERGENCY without operator intervention
- Sub-agent context usage visible in status line alongside parent session
- Single threshold definition propagates to all consumers

---

## Benefit Hypothesis

**We believe that** unifying context monitoring under Jerry's bounded context and providing structured JSON output to consumers

**Will result in** accurate context fill display in jerry-statusline, automatic session rotation at configurable thresholds, and consistent tier definitions across all system components

**We will know we have succeeded when** jerry-statusline calls `jerry context estimate` and displays accurate context fill, and sessions rotate automatically at EMERGENCY tier without operator intervention beyond confirming /compact

---

## Acceptance Criteria

### Definition of Done

- [x] `jerry context estimate` reads exact `current_usage` from Claude Code JSON stdin
- [x] Command returns structured JSON with fill, tier, thresholds, compaction status, sub-agent info
- [x] 5-tier threshold SSOT (NOMINAL/LOW/WARNING/CRITICAL/EMERGENCY) in Jerry config
- [x] Prompt-submit hook reads state file and escalates at WARNING+
- [x] Stop hook blocks at EMERGENCY tier, approves otherwise
- [x] Pre-compact hook checkpoints state before compaction fires
- [x] Session-start hook detects compaction vs /clear, injects appropriate resumption context
- [x] SubagentStop hook records agent lifecycle to `.jerry/local/subagent-lifecycle.json`
- [x] TranscriptSubAgentReader parses per-agent JSONL for cumulative context fill
- [x] jerry-statusline v3.0 calls `jerry context estimate` and renders context/compaction/sub-agent segments
- [x] SPIKE-004 benchmarked latency (p50=96ms, p95=112ms) within 2s status line budget
- [x] Fail-open: all handlers exit 0 on error

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | `jerry context estimate` reads `current_usage` from stdin, computes fill from exact token counts | [x] |
| AC-2 | JSON response includes: fill, tier, thresholds block, compaction detected flag, sub_agents list | [x] |
| AC-3 | 5-tier classification: NOMINAL (<0.60), LOW (<0.70), WARNING (<0.80), CRITICAL (<0.88), EMERGENCY (>=0.88) | [x] |
| AC-4 | Stop hook returns `decision: block` at EMERGENCY, `decision: approve` otherwise | [x] |
| AC-5 | Session-start injects `<compaction-notice>` or `<session-reset>` XML in additionalContext | [x] |
| AC-6 | Sub-agent fill computed from cumulative JSONL usage, displayed in jerry-statusline | [x] |
| AC-7 | jerry-statusline falls back to standalone mode if `jerry context estimate` unavailable | [x] |

---

## MVP Definition

### In Scope (MVP)

- `jerry context estimate` CLI command consuming Claude Code stdin JSON
- FilesystemContextStateStore for cross-invocation state persistence
- Stop hook gate at EMERGENCY tier
- Pre-compact state checkpoint
- Session-start compaction/clear detection and resumption context injection
- SubagentStop lifecycle hook
- TranscriptSubAgentReader for per-agent fill computation
- jerry-statusline Phase 1 integration (call Jerry CLI, render segments)
- 5-tier threshold SSOT consumed by statusline

### Out of Scope (Future)

- Automatic /compact invocation without user confirmation
- Cross-machine context state migration
- Sub-agent start hook (not available in Claude Code API)
- Configurable per-agent context windows

---

## Children Stories/Enablers

### Work Item Inventory

| ID | Type | Title | Status | Priority | Effort |
|----|------|-------|--------|----------|--------|
| SPIKE-004 | Spike | `uv run jerry context estimate` Latency Benchmark | completed | high | 1h |
| DEC-002 | Decision | Jerry Returns JSON, Not Rendered Output | accepted | high | -- |
| DEC-003 | Decision | Multi-Hook Rotation Architecture | accepted | high | -- |
| DEC-004 | Decision | Sub-Agent Tracking via Transcript Parsing + Lifecycle Hooks | accepted | high | -- |
| EN-009 | Enabler | Domain VOs + ContextEstimateComputer Service | completed | critical | 2-3h |
| EN-010 | Enabler | Application Port (IContextStateStore) + ContextEstimateService | completed | critical | 2-3h |
| EN-011 | Enabler | FilesystemContextStateStore Infrastructure Adapter | completed | high | 1-2h |
| EN-012 | Enabler | `jerry context estimate` CLI Command | completed | high | 1-2h |
| EN-013 | Enabler | Bootstrap Wiring + Config Integration | completed | high | 1-2h |
| EN-014 | Enabler | Stop Hook Gate (`context-stop-gate.py`) | completed | high | 1h |
| EN-015 | Enabler | PreCompact Hook State Persistence | completed | high | 1h |
| EN-016 | Enabler | SessionStart compact\|clear Resumption Context | completed | high | 1h |
| EN-017 | Enabler | Sub-Agent Lifecycle Hooks (SubagentStop) | completed | high | 1h |
| EN-018 | Enabler | Sub-Agent Transcript Parser (ISubAgentReader + TranscriptSubAgentReader) | completed | high | 2h |
| ST-004 | Story | Threshold Unification (5-tier SSOT) | completed | high | 1h |
| ST-005 | Story | jerry-statusline Phase 1 Integration | completed | high | 2h |
| ST-006 | Story | Automatic Session Rotation | completed | critical | 2h |

### Work Item Links

- [SPIKE-004: Latency Benchmark](./SPIKE-004-latency-benchmark.md)
- [DEC-002: Jerry Returns JSON, Not Rendered Output](./DEC-002-json-not-rendering.md)
- [DEC-003: Multi-Hook Rotation Architecture](./DEC-003-multi-hook-rotation.md)
- [DEC-004: Sub-Agent Tracking via Transcript Parsing + Lifecycle Hooks](./DEC-004-sub-agent-tracking.md)
- [EN-009: Domain VOs + ContextEstimateComputer Service](./EN-009-domain-vos-estimate-computer.md)
- [EN-010: Application Port (IContextStateStore) + ContextEstimateService](./EN-010-application-layer.md)
- [EN-011: FilesystemContextStateStore Infrastructure Adapter](./EN-011-filesystem-state-store.md)
- [EN-012: `jerry context estimate` CLI Command](./EN-012-context-estimate-cli.md)
- [EN-013: Bootstrap Wiring + Config Integration](./EN-013-bootstrap-wiring.md)
- [EN-014: Stop Hook Gate](./EN-014-stop-hook-gate.md)
- [EN-015: PreCompact Hook State Persistence](./EN-015-pre-compact-checkpoint.md)
- [EN-016: SessionStart compact|clear Resumption Context](./EN-016-session-start-resumption.md)
- [EN-017: Sub-Agent Lifecycle Hooks (SubagentStop)](./EN-017-subagent-lifecycle-hooks.md)
- [EN-018: Sub-Agent Transcript Parser](./EN-018-sub-agent-transcript-parser.md)
- [ST-004: Threshold Unification](./ST-004-threshold-unification.md)
- [ST-005: jerry-statusline Phase 1 Integration](./ST-005-statusline-phase1.md)
- [ST-006: Automatic Session Rotation](./ST-006-automatic-session-rotation.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Spikes:    [####################] 100% (1/1 completed)           |
| Decisions: [####################] 100% (3/3 accepted)            |
| Enablers:  [####################] 100% (10/10 completed)         |
| Stories:   [####################] 100% (3/3 completed)           |
+------------------------------------------------------------------+
| Overall:   [####################] 100% (COMPLETE)                |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Completed Spikes** | 1/1 (SPIKE-004) |
| **Decisions** | 3/3 accepted (DEC-002, DEC-003, DEC-004) |
| **Enablers** | 10/10 done (EN-009 through EN-018) |
| **Stories** | 3/3 done (ST-004, ST-005, ST-006) |
| **Latency p50** | 96ms (well within 2s budget) |
| **Completion %** | 100% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001: Context Resilience](../EPIC-001-context-resilience.md)
- **Resolves Discoveries:** DISC-002 (status line unification gap), DISC-003 (latency benchmark)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | FEAT-001 | context_monitoring BC foundation, hooks CLI infrastructure |
| Resolves | DISC-002 | Status line unification gap resolved via `jerry context estimate` |
| Resolves | DISC-003 | Latency claims resolved via SPIKE-004 benchmark (p50=96ms) |
| Extends | jerry-statusline | External repo — statusline.py updated to call Jerry CLI |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-21 | Claude | pending | Feature created retroactively. DISC-002 and DISC-003 drove this work. Architecture decisions DEC-002/003/004 accepted. |
| 2026-02-21 | Claude | completed | All implementation items done. SPIKE-004 benchmark complete (p50=96ms). jerry-statusline v3.0 integrated. Automatic session rotation operational. |
