# EN-925: Agent Registry Completion

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-17 (Claude)
PURPOSE: Complete AGENTS.md with all agents across all skills
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** infrastructure
> **Created:** 2026-02-17
> **Due:** --
> **Completed:** --
> **Parent:** FEAT-014
> **Owner:** --
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Business Value](#business-value) | How this enabler supports parent feature delivery |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Progress Summary](#progress-summary) | Current completion status |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Dependencies](#dependencies) | Dependencies and task ordering |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Complete AGENTS.md with all agents across all skills. Currently only 8 problem-solving agents are documented; missing ps-critic, all NASA-SE (10), Orchestration (3), Adversary (3), Transcript (4), and Worktracker (3) agents. Total ~24 agents need to be in the registry.

**Technical Scope:**
- Audit all skill directories for agent files
- Add per-skill sections to AGENTS.md following existing problem-solving format
- Update summary table and total counts

---

## Problem Statement

AGENTS.md is the canonical agent registry referenced by H-22 mandatory-skill-usage. It documents only 8 of 24+ agents, making the majority of agents undiscoverable. This undermines the registry's purpose as the authoritative source for agent capabilities and invocation patterns.

---

## Business Value

A complete agent registry ensures all agents are discoverable and their roles are understood. This directly supports H-22 (proactive skill invocation) by making it possible to identify the correct agent for any given task. Incomplete registry leads to underutilization of available agents and potential misrouting of work.

### Features Unlocked

- Enables accurate agent selection across all skills via a single registry
- Supports future orchestration improvements by providing a complete capability inventory

---

## Technical Approach

1. Read every agent file across all skill directories (`skills/*/agents/`)
2. Extract role, cognitive mode, and file path for each agent
3. Add per-skill sections to AGENTS.md following the existing problem-solving format
4. Update summary table and total counts
5. Remove/update "Future Skills" placeholder section

---

## Children (Tasks)

| ID | Title | Status | Activity | Owner |
|----|-------|--------|----------|-------|
| TASK-001 | Add ps-critic to problem-solving agents section | pending | DEVELOPMENT | ps-architect |
| TASK-002 | Add NASA-SE agents section (10 agents) | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Add Orchestration agents section (3 agents) | pending | DEVELOPMENT | ps-architect |
| TASK-004 | Add Adversary agents section (3 agents) | pending | DEVELOPMENT | ps-architect |
| TASK-005 | Add Transcript and Worktracker agents sections (7 agents) | pending | DEVELOPMENT | ps-architect |
| TASK-006 | Update agent summary table and counts | pending | DEVELOPMENT | ps-architect |
| TASK-007 | Remove/update "Future Skills" placeholder section | pending | DEVELOPMENT | ps-architect |

---

## Progress Summary

### Status Overview

```
[                    ] 0% (0/7 tasks)
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| Total Tasks | 7 |
| Completed | 0 |
| In Progress | 0 |
| Pending | 7 |
| Blocked | 0 |
| Completion | 0% |

---

## Acceptance Criteria

### Definition of Done

- [ ] AGENTS.md lists all agents from all skills with role, file path, cognitive mode
- [ ] Agent count matches actual agent files in skills/*/agents/
- [ ] Each skill has its own section following problem-solving format
- [ ] Summary table reflects accurate totals

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| 1 | All agent files across all skills inventoried | [ ] |
| 2 | Per-skill sections follow consistent format | [ ] |
| 3 | Summary table counts match actual agent files | [ ] |
| 4 | No placeholder or "Future Skills" sections remain | [ ] |

---

## Evidence

### Deliverables

| # | Deliverable | Path | Status |
|---|-------------|------|--------|
| 1 | -- | -- | Pending |

### Verification Checklist

- [ ] All acceptance criteria verified
- [ ] All technical criteria verified
- [ ] Quality gate score >= 0.92
- [ ] Creator-critic-revision cycle completed (minimum 3 iterations)
- [ ] No regressions introduced

---

## Dependencies

### Task Dependencies

TASK-001 through TASK-005 can run in parallel (independent skill sections). TASK-006 depends on TASK-001 through TASK-005 completion (needs all sections to compute totals). TASK-007 can run in parallel with any task.

### Depends On

- None

### Enables

- Accurate H-22 skill invocation across all skills

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-014: Framework Synchronization](../FEAT-014-framework-synchronization.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-17 | Claude | pending | Enabler created for FEAT-014 framework synchronization. |
