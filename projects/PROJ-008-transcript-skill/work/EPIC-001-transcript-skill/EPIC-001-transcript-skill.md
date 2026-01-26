# EPIC-001: Transcript Skill Foundation

<!--
TEMPLATE: Epic
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.2
-->

> **Type:** epic
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-25T00:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** PROJ-008-transcript-skill
> **Owner:** Claude
> **Target Quarter:** FY26-Q1

---

## Summary

Build a comprehensive Transcript Skill for the Jerry framework that processes meeting transcripts (VTT files), extracts structured entities (speakers, topics, questions, ideas, action items), and generates mind maps linking concepts back to source transcripts.

**Key Objectives:**
- Deep competitive research on 5 meeting intelligence products
- Multi-framework problem analysis (5W2H, Ishikawa, FMEA, 8D, NASA SE)
- Phased implementation from VTT MVP to full entity extraction
- Three-tier documentation (ELI5, Engineer, Architect)

---

## Business Outcome Hypothesis

**We believe that** building a transcript skill with advanced entity extraction and mind mapping capabilities

**Will result in** users being able to transform meeting recordings into actionable insights and work items

**We will know we have succeeded when:**
- Entity extraction accuracy exceeds 90% for key entities
- Mind maps are generated that link to source transcripts
- Users can convert action items to worktracker tasks
- Documentation serves all three persona levels effectively

---

## Lean Business Case

| Aspect | Description |
|--------|-------------|
| **Problem** | Meeting transcripts contain valuable information but extracting structured insights requires manual effort |
| **Solution** | Automated entity extraction + mind map generation + worktracker integration |
| **Cost** | Development time across 4 phases (estimated 8-12 weeks) |
| **Benefit** | Reduced time from meeting to action items; persistent knowledge capture |
| **Risk** | Entity extraction accuracy; handling diverse meeting formats |

---

## Children (Features)

### Feature Inventory

| ID | Title | Status | Priority | Progress |
|----|-------|--------|----------|----------|
| [FEAT-001](./FEAT-001-competitive-research/FEAT-001-competitive-research.md) | Competitive Research & Analysis | pending | high | 0% |
| FEAT-002 | VTT Parser & Entity Extraction | pending | high | 0% |
| FEAT-003 | Mind Map Generation | pending | medium | 0% |
| FEAT-004 | Worktracker Integration | pending | medium | 0% |

### Feature Links

- [FEAT-001: Competitive Research & Analysis](./FEAT-001-competitive-research/FEAT-001-competitive-research.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [....................] 0% (0/4 completed)             |
| Enablers:  [....................] 0% (0/4 completed)             |
| Stories:   [....................] 0% (0/0 completed)             |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Features** | 4 |
| **Completed Features** | 0 |
| **In Progress Features** | 0 |
| **Pending Features** | 4 |
| **Feature Completion %** | 0% |

### Milestone Tracking

| Milestone | Target Date | Status | Notes |
|-----------|-------------|--------|-------|
| Research Complete | TBD | PENDING | Phase 0 |
| MVP VTT Parser | TBD | PENDING | Phase 1 |
| Entity Extraction | TBD | PENDING | Phase 2 |
| Full Integration | TBD | PENDING | Phase 3-4 |

---

## Orchestration Plan

### Current Phase: 0 - Research & Discovery

```
+------------------------------------------------------------------+
|              EPIC-001 ORCHESTRATION PIPELINE                      |
+------------------------------------------------------------------+
|                                                                    |
|  PHASE 0: RESEARCH                                                |
|  ┌─────────────────────────────────────────────────────────┐      |
|  │  Status: STARTING                                        │      |
|  │                                                          │      |
|  │  Agents:                                                 │      |
|  │  - ps-researcher (x5): Competitive analysis             │      |
|  │  - ps-analyst: Framework analysis                        │      |
|  │  - ps-synthesizer: Combine findings                      │      |
|  │  - ps-critic: Adversarial review                         │      |
|  │                                                          │      |
|  │  Deliverables:                                           │      |
|  │  - Competitive analysis report                           │      |
|  │  - 5W2H analysis                                         │      |
|  │  - FMEA analysis                                         │      |
|  │  - Requirements specification                            │      |
|  └─────────────────────────────────────────────────────────┘      |
|                              │                                     |
|                              ▼                                     |
|  PHASE 1: MVP FOUNDATION (Blocked by Phase 0)                     |
|  ┌─────────────────────────────────────────────────────────┐      |
|  │  Status: BLOCKED                                         │      |
|  └─────────────────────────────────────────────────────────┘      |
|                              │                                     |
|                              ▼                                     |
|  PHASE 2-4: (Sequential)                                          |
|  ┌─────────────────────────────────────────────────────────┐      |
|  │  Status: BLOCKED                                         │      |
|  └─────────────────────────────────────────────────────────┘      |
+------------------------------------------------------------------+
```

---

## Related Items

### Hierarchy

- **Parent:** [PROJ-008-transcript-skill](../../WORKTRACKER.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | None | Epic is top-level for this project |
| Blocks | FEAT-002 | Research must complete before implementation |

---

## Artifacts at Epic Level

### Bugs
- None identified yet

### Discoveries
- None documented yet

### Impediments
- None identified yet

### Decisions
| ID | Decision | Date | Status |
|----|----------|------|--------|
| DEC-001 | MVP format: VTT only | 2026-01-25 | DOCUMENTED |
| DEC-002 | Mind map output: Mermaid + ASCII | 2026-01-25 | DOCUMENTED |
| DEC-003 | Task creation: Suggest first | 2026-01-25 | DOCUMENTED |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-25 | Claude | pending | Epic created |
| 2026-01-25 | Claude | in_progress | Starting Phase 0 research |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Epic |
| **SAFe** | Epic (Portfolio Backlog) |
| **JIRA** | Epic |
