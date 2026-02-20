# EPIC-001: Automated Multi-Instance Orchestration

> **Type:** epic
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** --
> **Parent:** PROJ-006-multi-instance
> **Owner:** --
> **Target Quarter:** FY26-Q1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key objectives |
| [Business Outcome Hypothesis](#business-outcome-hypothesis) | Expected outcomes |
| [Lean Business Case](#lean-business-case) | Problem/solution/cost/benefit |
| [Children (Features)](#children-features) | Feature and spike inventory |
| [Progress Summary](#progress-summary) | Overall epic progress |
| [Related Items](#related-items) | Dependencies and related work |
| [History](#history) | Status changes and key events |

---

## Summary

Replace manual multi-project orchestration (create worktree, open terminal, launch `claude`, context-switch, manually merge) with automated multi-instance management. Investigate two approaches: (1) Python Claude SDK / Anthropic Agent SDK for full programmatic control, (2) spawning and managing Claude Code CLI processes. Determine the optimal strategy and build a control plane that dispatches work to parallel instances.

**Key Objectives:**
- Compare Claude SDK vs CLI spawning: API surface, session persistence, tool use, context control, cost
- Assess automated worktree lifecycle: create, provision, session bind, merge, cleanup
- Design a single control plane for multi-project parallel orchestration
- Determine integration path with existing /orchestration skill
- Build MVP that can dispatch work to N parallel Claude instances from one command

---

## Business Outcome Hypothesis

**We believe that** automating multi-instance Claude management via SDK or CLI spawning

**Will result in** elimination of manual worktree/session overhead, enabling true parallel multi-project execution without operator context-switching

**We will know we have succeeded when** a single command can spin up N Claude instances on separate worktrees, dispatch project work, monitor progress, and merge results — with no manual terminal management

---

## Lean Business Case

| Aspect | Description |
|--------|-------------|
| **Problem** | Multi-project work requires manual worktree creation, terminal management, and session lifecycle. Operator must context-switch between projects, manually merge main into branches, and coordinate cross-project state. This is slow, error-prone, and doesn't scale. |
| **Solution** | Programmatic instance management via Claude SDK or CLI spawning. Automated worktree lifecycle. Single control plane for dispatch, monitoring, and coordination. |
| **Cost** | Research spikes + SDK/CLI integration + control plane implementation. Estimated 2-3 orchestration cycles. |
| **Benefit** | True parallel execution. No operator context-switching. Automated merge coordination. Scales to N projects. Foundation for autonomous multi-project workflows. |
| **Risk** | SDK may lack session persistence or tool-use parity with CLI. CLI spawning may be brittle. Cross-instance state coordination adds complexity. Cost implications of running multiple Claude instances. |

---

## Children (Features)

### Feature Inventory

| ID | Title | Status | Priority | Progress |
|----|-------|--------|----------|----------|
| FEAT-001 | Multi-Instance Strategy Assessment | pending | high | 0% |

### Spike Inventory

| ID | Title | Status | Priority | Timebox | Parent |
|----|-------|--------|----------|---------|--------|
| SPIKE-001 | Claude SDK vs CLI Instance Comparison | pending | high | 12 hours | FEAT-001 |
| SPIKE-002 | Automated Worktree & Session Lifecycle Management | pending | high | 8 hours | FEAT-001 |

### Feature Links

- [FEAT-001: Multi-Instance Strategy Assessment](./FEAT-001-instance-strategy/FEAT-001-instance-strategy.md)

---

## Progress Summary

```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [....................] 0% (0/1 completed)              |
| Spikes:    [....................] 0% (0/2 completed)              |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

---

## Related Items

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Informs | /orchestration skill | Multi-instance control plane extends orchestration capabilities |
| Relates To | PROJ-004 context resilience | Session lifecycle management overlaps with context exhaustion handling |
| Relates To | PROJ-005 markdown AST | AST tooling could be exposed to instances via shared CLI |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Epic created. SDK vs CLI comparison and automated worktree lifecycle as initial research spikes. |
