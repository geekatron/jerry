# EN-003: CLAUDE.md Optimization Research

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-01
PURPOSE: Research CLAUDE.md optimization and context management best practices
-->

> **Type:** enabler
> **Status:** completed
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** exploration
> **Created:** 2026-01-31T17:30:00Z
> **Due:** 2026-02-01
> **Completed:** 2026-02-01T14:00:00Z
> **Parent:** FEAT-001
> **Owner:** ps-researcher-claude-md
> **Effort:** 5

---

## Summary

Research CLAUDE.md best practices including context loading strategies, decomposition patterns, and optimization techniques. This is a CRITICAL enabler as Jerry's CLAUDE.md is currently 914 lines (~10,000 tokens), causing context rot.

**Technical Scope:**
- CLAUDE.md structure and purpose
- Context loading mechanisms (auto-load vs on-demand)
- Decomposition strategies (tiered, progressive disclosure)
- @ import syntax and usage patterns
- Token budget optimization

---

## Enabler Type Classification

**This Enabler Type:** EXPLORATION - Research into CLAUDE.md optimization strategies.

---

## Problem Statement

Jerry's CLAUDE.md at 914 lines consumes ~10,000 tokens at every session start. Research from Chroma shows that context rot degrades LLM performance as context fills up. We need evidence-based strategies to reduce CLAUDE.md while maintaining functionality.

---

## Business Value

Optimized CLAUDE.md will:
- Reduce session start token overhead by 65%+
- Improve LLM response quality (less context rot)
- Better OSS onboarding experience
- Enable progressive disclosure of information

### Features Unlocked

- FEAT-002: CLAUDE.md optimization implementation
- PLAN-CLAUDE-MD-OPTIMIZATION execution

---

## Technical Approach

Used ps-researcher-claude-md agent to:
1. Research CLAUDE.md best practices from authoritative sources
2. Analyze context loading mechanisms
3. Document decomposition strategies
4. Identify tiered loading patterns

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Effort | Owner |
|----|-------|--------|--------|-------|
| [TASK-001](./TASK-001-context-loading-research.md) | Context Loading Mechanisms Research | completed | 2 | ps-researcher-claude-md |
| [TASK-002](./TASK-002-decomposition-strategies.md) | Decomposition Strategies Research | completed | 2 | ps-researcher-claude-md |
| [TASK-003](./TASK-003-token-optimization.md) | Token Budget Optimization Research | completed | 1 | ps-researcher-claude-md |

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [####################] 100% (3/3 completed)            |
+------------------------------------------------------------------+
| Overall:   [####################] 100%                            |
+------------------------------------------------------------------+
```

---

## Acceptance Criteria

### Definition of Done

- [x] Context loading mechanisms documented (CLAUDE.md, .claude/rules/, skills)
- [x] @ import syntax patterns documented
- [x] Tiered loading strategy researched and documented
- [x] Token optimization techniques identified
- [x] Multi-persona documentation (L0/L1/L2)

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | HumanLayer, Builder.io, Anthropic sources referenced | [x] |
| TC-2 | Tiered strategy (Tier 1-4) documented | [x] |
| TC-3 | Context rot research referenced | [x] |

---

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| CLAUDE.md Best Practices | Research | Comprehensive optimization research | [claude-md-best-practices.md](../orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher-claude-md/claude-md-best-practices.md) |
| CLAUDE.md Optimization Plan | Synthesis | Implementation plan based on research | [PLAN-CLAUDE-MD-OPTIMIZATION.md](../orchestration/oss-release-20260131-001/plans/PLAN-CLAUDE-MD-OPTIMIZATION.md) |

---

## Key Findings

### Tiered Hybrid Loading Strategy

| Tier | Location | Loading | Content |
|------|----------|---------|---------|
| Tier 1 | CLAUDE.md | Always | Identity, navigation, constraints (~75 lines) |
| Tier 2 | .claude/rules/ | Auto-loaded | Coding standards, architecture rules |
| Tier 3 | Skills | On-demand | Worktracker, problem-solving, etc. |
| Tier 4 | docs/ | Explicit access | Reference documentation |

### Target Metrics

| Metric | Current | Target |
|--------|---------|--------|
| CLAUDE.md lines | 914 | 60-80 |
| Token footprint | ~10,000 | ~3,500 |
| Worktracker in CLAUDE.md | 371 lines | 0 |

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001: Research and Preparation](../FEAT-001-research-and-preparation.md)

### Orchestration Artifacts

| Artifact | Path |
|----------|------|
| Research Output | [ps/phase-0/ps-researcher-claude-md/claude-md-best-practices.md](../orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher-claude-md/claude-md-best-practices.md) |
| Implementation Plan | [plans/PLAN-CLAUDE-MD-OPTIMIZATION.md](../orchestration/oss-release-20260131-001/plans/PLAN-CLAUDE-MD-OPTIMIZATION.md) |

### Discovery

- Identified in: [DISC-001: Missed Research Scope](../FEAT-001--DISC-001-missed-research-scope.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-31T17:30:00Z | Claude | pending | Identified in DISC-001 |
| 2026-02-01T10:00:00Z | ps-researcher-claude-md | in_progress | Research started |
| 2026-02-01T14:00:00Z | ps-researcher-claude-md | completed | Research complete, plan created |
| 2026-02-01 | Claude | completed | Enabler file created |

---

*Enabler Version: 1.0.0*
