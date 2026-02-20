# EPIC-001: Context Resilience

> **Type:** epic
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** --
> **Parent:** PROJ-004-context-resilience
> **Owner:** --
> **Target Quarter:** FY26-Q1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key objectives |
| [Business Outcome Hypothesis](#business-outcome-hypothesis) | Expected outcomes |
| [Lean Business Case](#lean-business-case) | Problem/solution/cost/benefit |
| [Children (Features)](#children-features) | Feature inventory |
| [Progress Summary](#progress-summary) | Overall epic progress |
| [Related Items](#related-items) | Dependencies and related work |
| [History](#history) | Status changes and key events |

---

## Summary

Multi-orchestration workflows (C3/C4 criticality) routinely exhaust the ~200K token context window, causing performance degradation and forced session termination. Currently, resumption is manual and error-prone. This epic delivers automated context exhaustion detection, graceful checkpoint-and-handoff, and a structured resumption protocol that reads ORCHESTRATION.yaml + WORKTRACKER.md to reconstruct execution context.

**Key Objectives:**
- Implement context fill detection with configurable warning/critical thresholds
- Build graceful session handoff that checkpoints state before termination
- Create a resumption protocol that enables Claude to self-orient from persistent state (ORCHESTRATION.yaml, WORKTRACKER.md)
- Minimize operator intervention during context exhaustion events

---

## Business Outcome Hypothesis

**We believe that** implementing automated context exhaustion detection and structured resumption protocols

**Will result in** reduced manual intervention during multi-orchestration workflows, fewer lost-state incidents, and maintained quality gate compliance across session boundaries

**We will know we have succeeded when** operators can clear a context-exhausted session and resume orchestration with a single command, with no quality regression and no state loss

---

## Lean Business Case

| Aspect | Description |
|--------|-------------|
| **Problem** | Multi-orchestration runs (10+ agents, 5+ phases) exhaust context, causing forced session clears. Resumption requires manual reading of ORCHESTRATION.yaml and mental reconstruction of execution state. This is slow, error-prone, and blocks autonomous operation. |
| **Solution** | Three-pronged approach: (1) detect context fill proactively, (2) checkpoint state gracefully before exhaustion, (3) provide structured resumption prompt that reads persistent state and reconstructs context. |
| **Cost** | Research spike + feature implementation. Estimated 1-2 orchestration cycles. |
| **Benefit** | Autonomous multi-session orchestration. Reduced operator burden. No state loss at session boundaries. Quality gate compliance maintained. |
| **Risk** | Context measurement APIs may be limited or unreliable. Resumption fidelity depends on ORCHESTRATION.yaml completeness. |

---

## Children (Features)

### Feature Inventory

| ID | Title | Status | Priority | Progress |
|----|-------|--------|----------|----------|
| FEAT-001 | Context Exhaustion Detection & Graceful Session Handoff | pending | high | 0% |

### Spike Inventory

| ID | Title | Status | Priority | Timebox |
|----|-------|--------|----------|---------|
| SPIKE-001 | Research Context Measurement, Detection Thresholds & Resumption Protocols | pending | high | 8 hours |

### Feature Links

- [FEAT-001: Context Exhaustion Detection & Graceful Session Handoff](./FEAT-001-context-detection/FEAT-001-context-detection.md)

### Spike Links

- [SPIKE-001: Research Context Measurement, Detection Thresholds & Resumption Protocols](./FEAT-001-context-detection/SPIKE-001-context-research.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [....................] 0% (0/1 completed)              |
| Spikes:    [....................] 0% (0/1 completed)              |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Features** | 1 |
| **Completed Features** | 0 |
| **In Progress Features** | 0 |
| **Pending Features** | 1 |
| **Total Spikes** | 1 |
| **Completed Spikes** | 0 |
| **Feature Completion %** | 0% |

---

## Related Items

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | SPIKE-001 | Feature design depends on research findings (thresholds, APIs, protocols) |
| Informs | PROJ-001 /orchestration skill | Resumption protocol will integrate with existing orchestration skill |
| Informs | PROJ-002 roadmap-next | Context resilience is a capability on the roadmap |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Epic created. Captures context exhaustion detection and graceful session handoff requirements. |
