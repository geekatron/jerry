# FEAT-001: Multi-Instance Strategy Assessment

> **Type:** feature
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-20
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
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Children (Spikes)](#children-spikes) | Spike inventory |
| [Progress Summary](#progress-summary) | Overall feature progress |
| [Related Items](#related-items) | Dependencies |
| [History](#history) | Status changes |

---

## Summary

Assess the two primary approaches for automated multi-instance Claude management — Python Claude SDK (Anthropic Agent SDK) and Claude Code CLI subprocess spawning — and determine the optimal strategy. Includes automated worktree lifecycle management as a companion concern.

**Value Proposition:**
- Evidence-based decision on SDK vs CLI vs hybrid approach
- Automated worktree lifecycle feasibility confirmed
- Clear integration path with Jerry CLI and /orchestration skill

---

## Acceptance Criteria

### Definition of Done

- [ ] SPIKE-001 complete: SDK vs CLI compared with evidence, prototypes, and trade-off matrix
- [ ] SPIKE-002 complete: worktree lifecycle automation feasibility confirmed
- [ ] Go/no-go recommendation on approach
- [ ] Adversarial review completed (S-003 Steelman, S-002 Devil's Advocate)
- [ ] ADR published documenting the decision
- [ ] If go: integration architecture defined, MVP scope outlined

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Claude SDK API surface documented: instance creation, tool use, context control, session persistence | [ ] |
| AC-2 | CLI spawning approach prototyped: subprocess management, I/O handling, lifecycle control | [ ] |
| AC-3 | Side-by-side comparison on 8+ dimensions (see SPIKE-001 framework) | [ ] |
| AC-4 | Worktree automation prototype: create, bind session, merge, cleanup | [ ] |
| AC-5 | Cost analysis: API token costs (SDK) vs CLI instance overhead | [ ] |
| AC-6 | Integration path with /orchestration skill defined | [ ] |

---

## Children (Spikes)

| ID | Type | Title | Status | Priority | Timebox |
|----|------|-------|--------|----------|---------|
| SPIKE-001 | Spike | Claude SDK vs CLI Instance Comparison | pending | high | 12h |
| SPIKE-002 | Spike | Automated Worktree & Session Lifecycle Management | pending | high | 8h |

### Work Item Links

- [SPIKE-001: Claude SDK vs CLI Instance Comparison](./SPIKE-001-sdk-vs-cli.md)
- [SPIKE-002: Automated Worktree & Session Lifecycle Management](./SPIKE-002-worktree-lifecycle.md)

---

## Progress Summary

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Spikes:    [....................] 0% (0/2 completed)              |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001: Automated Multi-Instance Orchestration](../EPIC-001-multi-instance.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| SPIKE-001 parallel with | SPIKE-002 | Cross-pollinated pipeline with sync barriers; research runs concurrently, analysis cross-informs |
| Both spikes inform | Go/no-go ADR | Convergent Phase 3: ps-architect synthesizes both spikes into decision |
| Orchestrated by | ORCHESTRATION_PLAN.md | Cross-pollinated pipeline pattern with quality gates at barriers |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Feature created. Two spikes: SDK vs CLI comparison (SPIKE-001) and worktree lifecycle (SPIKE-002). |
