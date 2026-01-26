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
- Formal Architecture Decision Records (ADRs)
- Three-tier documentation (ELI5, Engineer, Architect)
- Phased implementation: prompt-based agents first, Python later if needed
- Token-managed artifacts (<35K tokens each) with bidirectional deep linking

---

## Business Outcome Hypothesis

**We believe that** building a transcript skill with advanced entity extraction and mind mapping capabilities

**Will result in** users being able to transform meeting recordings into actionable insights and work items

**We will know we have succeeded when:**
- Entity extraction accuracy exceeds 90% for key entities
- Mind maps are generated that link to source transcripts
- Users can convert action items to worktracker tasks
- Documentation serves all three persona levels effectively
- All artifacts are Claude-friendly (<35K tokens)
- Bidirectional deep linking enables navigation

---

## Lean Business Case

| Aspect | Description |
|--------|-------------|
| **Problem** | Meeting transcripts contain valuable information but extracting structured insights requires manual effort |
| **Solution** | Automated entity extraction + mind map generation + worktracker integration |
| **Cost** | Development time across 2 features (estimated 4-6 weeks with semi-supervised workflow) |
| **Benefit** | Reduced time from meeting to action items; persistent knowledge capture |
| **Risk** | Entity extraction accuracy; handling diverse meeting formats |

---

## Children (Features)

### Feature Inventory

| ID | Title | Status | Priority | Progress | Gates |
|----|-------|--------|----------|----------|-------|
| [FEAT-001](./FEAT-001-analysis-design/FEAT-001-analysis-design.md) | Analysis & Design | pending | high | 0% | 1-4 |
| [FEAT-002](./FEAT-002-implementation/FEAT-002-implementation.md) | Implementation | pending | high | 0% | 5-6 |

### Feature Links

- [FEAT-001: Analysis & Design](./FEAT-001-analysis-design/FEAT-001-analysis-design.md)
  - Research, requirements, architecture decisions, design documentation
  - 6 enablers, 4 human approval gates
- [FEAT-002: Implementation](./FEAT-002-implementation/FEAT-002-implementation.md)
  - VTT parser, entity extraction, mind maps, artifact packaging, worktracker integration
  - 7 enablers, 2 human approval gates

---

## Human Approval Gates

| Gate | Feature | After | Approval For |
|------|---------|-------|--------------|
| GATE-1 | FEAT-001 | EN-001, EN-002 | Research completeness |
| GATE-2 | FEAT-001 | EN-003 | Requirements validity |
| GATE-3 | FEAT-001 | EN-004 | Architecture decisions |
| GATE-4 | FEAT-001 | EN-005, EN-006 | Design completeness |
| GATE-5 | FEAT-002 | EN-007, EN-008 | Core implementation |
| GATE-6 | FEAT-002 | EN-009..EN-013 | Final review |

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [....................] 0% (0/2 completed)             |
| Enablers:  [....................] 0% (0/13 completed)            |
| Tasks:     [....................] 0% (0/66 completed)            |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Features** | 2 |
| **Completed Features** | 0 |
| **In Progress Features** | 0 |
| **Pending Features** | 2 |
| **Total Enablers** | 13 |
| **Total Tasks** | ~66 |
| **Total Effort (points)** | 107 |
| **Completion %** | 0% |

### Milestone Tracking

| Milestone | Target Date | Status | Gate |
|-----------|-------------|--------|------|
| Research Complete | TBD | PENDING | GATE-1 |
| Requirements Complete | TBD | PENDING | GATE-2 |
| Architecture Complete | TBD | PENDING | GATE-3 |
| Design Complete | TBD | PENDING | GATE-4 |
| Core Implementation | TBD | PENDING | GATE-5 |
| Full Implementation | TBD | PENDING | GATE-6 |

---

## Orchestration Pipeline

```
+==============================================================================+
|                    EPIC-001 ORCHESTRATION PIPELINE                            |
+==============================================================================+
|                                                                               |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │                     FEAT-001: ANALYSIS & DESIGN                          │ |
|  │                                                                          │ |
|  │  PHASE 1: Research (EN-001, EN-002)                                     │ |
|  │  ───────────────────────────────────────                                │ |
|  │  Market analysis + Technical standards                                   │ |
|  │                              │                                           │ |
|  │                    ★ GATE 1: Research Review ★                          │ |
|  │                              │                                           │ |
|  │  PHASE 2: Requirements (EN-003)                                         │ |
|  │  ─────────────────────────────────                                      │ |
|  │  5W2H, Ishikawa, FMEA, Requirements Spec                                │ |
|  │                              │                                           │ |
|  │                    ★ GATE 2: Requirements Review ★                      │ |
|  │                              │                                           │ |
|  │  PHASE 3: Architecture (EN-004)                                         │ |
|  │  ──────────────────────────────────                                     │ |
|  │  ADRs: Agent Architecture, Artifact Structure, Deep Linking             │ |
|  │                              │                                           │ |
|  │                    ★ GATE 3: Architecture Review ★                      │ |
|  │                              │                                           │ |
|  │  PHASE 4: Design (EN-005, EN-006)                                       │ |
|  │  ───────────────────────────────────                                    │ |
|  │  L0/L1/L2 Design Docs + Context Injection Design                        │ |
|  │                              │                                           │ |
|  │                    ★ GATE 4: Design Review ★                            │ |
|  └──────────────────────────────┼──────────────────────────────────────────┘ |
|                                 │                                            |
|                                 ▼                                            |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │                     FEAT-002: IMPLEMENTATION                             │ |
|  │                                                                          │ |
|  │  PHASE 5: Core Implementation (EN-007, EN-008)                          │ |
|  │  ─────────────────────────────────────────────                          │ |
|  │  VTT Parser + Entity Extraction Pipeline                                 │ |
|  │                              │                                           │ |
|  │                    ★ GATE 5: Core Review ★                              │ |
|  │                              │                                           │ |
|  │  PHASE 6: Output Generation (EN-009..EN-013)                            │ |
|  │  ──────────────────────────────────────────────                         │ |
|  │  Mind Maps + Artifact Packaging + Worktracker + CLI + Context Injection │ |
|  │                              │                                           │ |
|  │                    ★ GATE 6: Final Review ★                             │ |
|  └──────────────────────────────┼──────────────────────────────────────────┘ |
|                                 │                                            |
|                                 ▼                                            |
|                    ┌────────────────────────┐                               |
|                    │  TRANSCRIPT SKILL       │                               |
|                    │  COMPLETE & RELEASED    │                               |
|                    └────────────────────────┘                               |
+==============================================================================+
```

---

## Related Items

### Hierarchy

- **Parent:** [PROJ-008-transcript-skill](../../WORKTRACKER.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | None | Epic is top-level for this project |
| Blocks | None | No downstream epics |

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
| DEC-004 | Bidirectional linking with backlinks | 2026-01-26 | DOCUMENTED |
| DEC-005 | Token limit: 35K per artifact | 2026-01-26 | DOCUMENTED |
| DEC-006 | Phased agents: Prompt-based first, Python later | 2026-01-26 | DOCUMENTED |
| DEC-007 | Two features: Analysis & Design + Implementation | 2026-01-26 | DOCUMENTED |
| DEC-008 | 6 human approval gates | 2026-01-26 | DOCUMENTED |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-25 | Claude | pending | Epic created |
| 2026-01-25 | Claude | in_progress | Starting Phase 0 research |
| 2026-01-26 | Claude | in_progress | Restructured to two features with 6 gates |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Epic |
| **SAFe** | Epic (Portfolio Backlog) |
| **JIRA** | Epic |
