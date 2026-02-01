# EN-006: Decomposition with Imports Research

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-01
PURPOSE: Research decomposition and import patterns for context optimization
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
> **Owner:** ps-researcher-decomposition
> **Effort:** 4

---

## Summary

Research decomposition patterns and import mechanisms for optimizing context loading. Focuses on the @ import syntax, always-loaded vs contextual loading, and tiered information architecture.

**Technical Scope:**
- @ import syntax (`@file.md`) patterns
- Always-loaded vs on-demand content strategies
- Tiered information architecture (Tier 1-4)
- Progressive disclosure patterns
- File reference vs inline content trade-offs

---

## Enabler Type Classification

**This Enabler Type:** EXPLORATION - Research into decomposition strategies for context optimization.

---

## Problem Statement

Jerry's CLAUDE.md contains 914 lines of content all loaded at session start. We need to understand decomposition patterns that enable:
- Selective loading based on need
- Progressive disclosure of information
- Reduced always-loaded token overhead

---

## Business Value

Decomposition research directly enables:
- 91-93% reduction in CLAUDE.md size
- 65% reduction in session start tokens
- Better user experience through progressive disclosure

### Features Unlocked

- FEAT-002: Full CLAUDE.md optimization implementation
- PLAN-CLAUDE-MD-OPTIMIZATION all phases

---

## Technical Approach

Used ps-researcher-decomposition agent to:
1. Research @ import syntax and behavior
2. Analyze Claude Code loading mechanisms
3. Document tiered loading strategy
4. Identify decomposition patterns from industry

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Effort | Owner |
|----|-------|--------|--------|-------|
| [TASK-001](./TASK-001-import-syntax-research.md) | @ Import Syntax Research | completed | 1 | ps-researcher-decomposition |
| [TASK-002](./TASK-002-loading-strategies.md) | Loading Strategies Research | completed | 2 | ps-researcher-decomposition |
| [TASK-003](./TASK-003-tiered-architecture.md) | Tiered Architecture Design | completed | 1 | ps-researcher-decomposition |

---

## Progress Summary

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

- [x] @ import syntax patterns documented
- [x] Always-loaded vs contextual trade-offs analyzed
- [x] Tiered loading strategy (Tier 1-4) designed
- [x] Progressive disclosure patterns documented
- [x] Multi-persona documentation (L0/L1/L2)

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | Import syntax behavior verified | [x] |
| TC-2 | Tier boundaries defined | [x] |
| TC-3 | Token savings quantified | [x] |

---

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| Decomposition Best Practices | Research | Decomposition patterns research | [decomposition-best-practices.md](../orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher-decomposition/decomposition-best-practices.md) |

---

## Key Findings

### @ Import Syntax

```markdown
See @docs/architecture.md for system design
Review @.claude/rules/coding-standards.md for style guide
```

- Content included when Claude processes the reference
- Supports up to 5 hops of nested includes
- Best for critical context needed immediately

### Tiered Loading Strategy

| Tier | Mechanism | Loading | Target Content |
|------|-----------|---------|----------------|
| Tier 1 | CLAUDE.md | Always | Identity, navigation (~75 lines) |
| Tier 2 | .claude/rules/ | Auto-loaded | Standards, rules (~500 lines) |
| Tier 3 | Skills | On-demand | Workflows, agents (~1500+ lines) |
| Tier 4 | docs/ | Explicit | Reference docs (unlimited) |

### Token Reduction Calculation

| Component | Current | After Decomposition |
|-----------|---------|---------------------|
| CLAUDE.md | 10,000 tokens | 3,500 tokens |
| Session start total | 15,000+ | ~5,000 |
| Reduction | - | 65-67% |

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001: Research and Preparation](../FEAT-001-research-and-preparation.md)

### Orchestration Artifacts

| Artifact | Path |
|----------|------|
| Research Output | [ps/phase-0/ps-researcher-decomposition/decomposition-best-practices.md](../orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher-decomposition/decomposition-best-practices.md) |

### Discovery

- Identified in: [DISC-001: Missed Research Scope](../FEAT-001--DISC-001-missed-research-scope.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-31T17:30:00Z | Claude | pending | Identified in DISC-001 |
| 2026-02-01T10:00:00Z | ps-researcher-decomposition | in_progress | Research started |
| 2026-02-01T14:00:00Z | ps-researcher-decomposition | completed | Research complete |
| 2026-02-01 | Claude | completed | Enabler file created |

---

*Enabler Version: 1.0.0*
