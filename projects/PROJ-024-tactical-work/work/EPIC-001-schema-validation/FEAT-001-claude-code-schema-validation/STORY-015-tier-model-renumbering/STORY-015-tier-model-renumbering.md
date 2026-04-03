# STORY-015: Evaluate and Renumber Tool Security Tier Model

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: ADR-level evaluation of tier model renumbering to close the T3+T4 gap
-->

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-27T11:00:00Z
> **Due:**
> **Completed:** 2026-03-28T18:00:00Z
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What needs to happen |
| [Problem Statement](#problem-statement) | The structural gap in the current tier model |
| [Current Tier Model](#current-tier-model) | Existing T1-T5 |
| [Evaluation Criteria](#evaluation-criteria) | How to judge proposals |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry framework architect

**I want** the tool security tier model renumbered so that every valid tool combination has a home in the hierarchy

**So that** agents like nse-requirements (T3 + Memory-Keeper) and ps-architect (Context7 + Memory-Keeper) have a proper tier instead of undocumented exceptions

---

## Summary

The STORY-012 audit and STORY-013 mismatch analysis revealed a structural gap: the current T1-T5 tier model treats External (web/Context7) and Persistent (Memory-Keeper) as parallel branches that only merge at T5 (Full = T3 + T4 + Agent tool). An agent needing web research AND cross-session persistence has no valid tier without also getting the Agent tool (which H-35 forbids for workers).

This story evaluates renumbering options via ADR process with C4 quality at >= 0.95 threshold.

**Quality gate: C4 adversarial at >= 0.95** (higher than standard 0.92 because this changes governance infrastructure affecting all 89 agents).

---

## Problem Statement

### Current Gap

```
T3 (External) = T2 + WebSearch + WebFetch + Context7
T4 (Persistent) = T2 + Memory-Keeper
T5 (Full) = T3 + T4 + Agent

Gap: T3 + Memory-Keeper (without Agent) = ???
```

### Real-World Impact

| Agent | Needs | Current Tier | Problem |
|-------|-------|-------------|---------|
| ps-architect | Context7 + Memory-Keeper | T4 (declared) | Actually has T3 tools too -- no valid tier |
| nse-requirements | WebSearch + WebFetch + Memory-Keeper | T4 (declared) | Actually has T3+T4 tools = undeclared T5 |
| ps-researcher | Should persist findings (MCP-M-001) | T3 | Can't have Memory-Keeper without T5 |
| orch-planner | Memory-Keeper only | T4 | Doesn't need web tools |

### Root Cause

The original model conflated "external + persistent" with "orchestrating." T5 was designed for orchestrator agents that delegate work (Agent tool), but it's the only tier combining web access with persistence.

---

## Current Tier Model

| Tier | Name | Tools | Agent Count |
|------|------|-------|-------------|
| T1 | Read-Only | Read, Glob, Grep | ~3 |
| T2 | Read-Write | T1 + Write, Edit, Bash | ~15 |
| T3 | External | T2 + WebSearch, WebFetch, Context7 | ~40 |
| T4 | Persistent | T2 + Memory-Keeper | ~7 |
| T5 | Full | T3 + T4 + Agent | ~5 |

---

## Evaluation Criteria

Each proposal must be evaluated against:

1. **Simplicity** -- Is the model easy to understand and remember?
2. **Completeness** -- Does every valid tool combination have a tier?
3. **Monotonicity** -- Does each tier strictly add capability over the previous?
4. **Migration cost** -- How many governance YAMLs need updating?
5. **Principle of least privilege** -- Does the model encourage minimal tool access?
6. **Forward compatibility** -- Can new tools/MCP servers be added without restructuring?
7. **H-35 compliance** -- Does the Agent tool remain restricted to the highest tier?

---

## Acceptance Criteria

- [x] ADR produced in Nygard format evaluating at minimum 3 renumbering options
- [x] Each option scored against the 7 evaluation criteria
- [x] Recommended option selected with full trade-off analysis
- [x] Migration plan: every agent's tier change documented
- [x] Schema update plan: `agent-governance-v1.schema.json` tool_tier enum
- [x] Rule file update plan: `agent-development-standards.md` tier table
- [x] Impact on all governance YAMLs quantified
- [x] C4 adversarial review at >= 0.95
- [x] /user-experience developer ergonomics review of the new model
- [x] No existing agent becomes invalid under the new model

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner |
|----|-------|--------|-------|
| TASK-001 | Research: enumerate all renumbering options (ps-researcher) | done | adam.nowak |
| TASK-002 | Analysis: score options against 7 criteria (ps-analyst) | done | adam.nowak |
| TASK-003 | ADR: produce architecture decision record (ps-architect) | done | adam.nowak |
| TASK-004 | DX review: developer ergonomics of new tier model (ux-heuristic-eval) | done | adam.nowak |
| TASK-005 | Migration plan: per-agent tier changes | done | adam.nowak |
| TASK-006 | C4 adversarial review at >= 0.95 (adv-scorer) | done | adam.nowak |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Claude Code Schema Validation](../FEAT-001-claude-code-schema-validation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Informed By | STORY-012 | Audit revealed the T3+T4 gap |
| Informed By | STORY-013 M-004 | nse-requirements tier mismatch is the triggering case |
| Informed By | Memory-Keeper analysis | ps-analyst recommended T3a; user rejected, wants clean renumbering |
| Blocks | STORY-013 M-004 | nse-requirements fix depends on new tier model |
| Blocks | STORY-014 D-001 | Tier example fixes depend on final tier definitions |

### Auto-Escalation

Per AE-002: modifying `.context/rules/agent-development-standards.md` (Tool Security Tiers) = **auto-C3 minimum**. User has set C4 with >= 0.95 threshold.

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-27 | adam.nowak | pending | Story created -- T3a rejected, clean renumbering required |
| 2026-03-28 | adam.nowak | done | ADR-STORY015-001 produced. Recommends Option A (Persistent-First Linear). C4 adversarial review: 0.953 PASS after 5 iterations. DX review completed. |
