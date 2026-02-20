# FEAT-001: Context Exhaustion Detection & Graceful Session Handoff

> **Type:** feature
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** --
> **Parent:** EPIC-001
> **Owner:** --
> **Target Sprint:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and value proposition |
| [Benefit Hypothesis](#benefit-hypothesis) | Expected benefits |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [MVP Definition](#mvp-definition) | Minimum viable scope |
| [Children (Stories/Enablers)](#children-storiesenablers) | Work item inventory |
| [Progress Summary](#progress-summary) | Overall feature progress |
| [Related Items](#related-items) | Dependencies |
| [History](#history) | Status changes |

---

## Summary

Implement a context exhaustion detection mechanism that monitors session fill level during multi-orchestration runs, triggers graceful checkpoint-and-handoff when configurable thresholds are breached, and provides a structured resumption protocol that reads ORCHESTRATION.yaml + WORKTRACKER.md to reconstruct execution context in a new session.

**Value Proposition:**
- Eliminates manual state reconstruction after context exhaustion
- Preserves orchestration continuity across session boundaries
- Reduces operator burden from "figure it out" to "resume from checkpoint"

---

## Benefit Hypothesis

**We believe that** detecting context fill proactively and providing structured resumption prompts

**Will result in** seamless multi-session orchestration with no state loss and minimal operator intervention

**We will know we have succeeded when** a context-exhausted orchestration run can be resumed in a new session within 2 minutes with no quality regression

---

## Acceptance Criteria

### Definition of Done

- [ ] Context fill level is measurable during orchestration runs
- [ ] Configurable warning threshold triggers pre-emptive checkpoint
- [ ] Configurable critical threshold triggers graceful session handoff
- [ ] Checkpoint captures: current phase, agent status, quality gate state, next actions
- [ ] Resumption prompt reads ORCHESTRATION.yaml + WORKTRACKER.md and reconstructs context
- [ ] Resumption prompt identifies exactly where to resume (phase, agent, iteration)
- [ ] End-to-end test: exhaust context -> clear -> resume -> complete orchestration
- [ ] No quality gate regression across session boundary (>= 0.92 maintained)
- [ ] SPIKE-001 research complete and findings integrated

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Detection mechanism reports context fill as percentage (0-100%) | [ ] |
| AC-2 | Warning threshold (configurable, default ~70%) logs advisory | [ ] |
| AC-3 | Critical threshold (configurable, default ~85%) triggers checkpoint + handoff prompt | [ ] |
| AC-4 | Checkpoint writes to ORCHESTRATION.yaml `resumption` section | [ ] |
| AC-5 | Handoff prompt includes: (a) files to read, (b) current state summary, (c) next action | [ ] |
| AC-6 | Resumption in new session reads state and continues from checkpoint | [ ] |
| AC-7 | Works with all orchestration patterns: sequential, cross-pollinated, fan-out/fan-in | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Detection overhead < 500 tokens per check | [ ] |
| NFC-2 | Checkpoint operation completes in < 30 seconds | [ ] |
| NFC-3 | Resumption protocol is self-contained (no external dependencies beyond project files) | [ ] |
| NFC-4 | Compatible with Claude Code context compaction (system-initiated compression) | [ ] |

---

## MVP Definition

### In Scope (MVP)

- Context fill detection (hook-based or heuristic)
- Single configurable threshold (critical only)
- Checkpoint to ORCHESTRATION.yaml `resumption` section
- Resumption prompt template that reads ORCHESTRATION.yaml + WORKTRACKER.md
- Manual session clear + resume workflow

### Out of Scope (Future)

- Automatic session rotation (clear + restart without operator)
- Multi-level thresholds with graduated responses
- Integration with Claude Code's internal context compaction API
- Cross-machine session migration
- Context optimization / compression strategies

---

## Children (Stories/Enablers)

### Work Item Inventory

| ID | Type | Title | Status | Priority | Effort |
|----|------|-------|--------|----------|--------|
| SPIKE-001 | Spike | Research Context Measurement, Detection Thresholds & Resumption Protocols | done | high | 8h |
| SPIKE-002 | Spike | Jerry CLI Integration Architecture for Context Resilience | done | high | 4h |
| DISC-001 | Discovery | Hook-CLI Architecture Violations and Enforcement Tech Debt | documented | critical | -- |
| DEC-001 | Decision | CLI-First Hook Architecture & Context Monitoring Bounded Context | pending | critical | -- |

> DISC-001 identified that hooks bypass the CLI and that the enforcement folder is tech debt. DEC-001 captures 4 architectural decisions: CLI-first hooks, proper bounded context, `jerry hooks` commands, and separate enforcement tech debt tracking. Work items to be revised once DEC-001 is accepted.

### Work Item Links

- [SPIKE-001: Research Context Measurement, Detection Thresholds & Resumption Protocols](./SPIKE-001-context-research.md)
- [SPIKE-002: Jerry CLI Integration Architecture for Context Resilience](./SPIKE-002-cli-integration.md)
- [DISC-001: Hook-CLI Architecture Violations and Enforcement Tech Debt](./DISC-001-architecture-violations.md)
- [DEC-001: CLI-First Hook Architecture & Context Monitoring Bounded Context](./DEC-001-cli-first-architecture.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Spikes:    [....................] 0% (0/1 completed)              |
| Stories:   Pending SPIKE-001 findings                             |
| Enablers:  Pending SPIKE-001 findings                             |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Spikes** | 1 |
| **Completed Spikes** | 0 |
| **Total Stories** | TBD (after SPIKE-001) |
| **Total Enablers** | TBD (after SPIKE-001) |
| **Completion %** | 0% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001: Context Resilience](../EPIC-001-context-resilience.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | SPIKE-001 | Design depends on research findings |
| Informs | /orchestration skill | Resumption protocol extends orchestration skill |
| Informs | quality-enforcement.md (AE-006) | Aligns with existing token exhaustion escalation rule |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Feature created. Captures detection, checkpoint, and resumption requirements. Blocked on SPIKE-001 research. |
| 2026-02-19 | Claude | pending | DISC-001 created: Hook-CLI architecture violations found during SPIKE-002 ADR review. 3 of 4 hooks bypass CLI. Enforcement folder is tech debt. |
| 2026-02-19 | Claude | pending | DEC-001 created: 4 architectural decisions -- CLI-first hooks, proper bounded context, jerry hooks commands, enforcement debt tracked separately. Supersedes ADR-SPIKE002-001 approach. Pending user acceptance. |
