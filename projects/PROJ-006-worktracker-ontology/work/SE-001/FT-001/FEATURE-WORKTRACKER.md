# FEATURE-WORKTRACKER: FT-001 Domain Discovery

> **Feature ID:** FT-001
> **Name:** Domain Discovery
> **Status:** IN PROGRESS (SYNC BARRIER 3 - CL-003 APPROVED, Awaiting Human Approval)
> **Parent:** [SE-001](../SOLUTION-WORKTRACKER.md)
> **Created:** 2026-01-13
> **Last Updated:** 2026-01-14
> **Phase 1 Completed:** 2026-01-13
> **Phase 2 Completed:** 2026-01-13
> **Phase 3 Completed:** 2026-01-13
> **Current Barrier:** SYNC-3 (CL-003 APPROVED - Awaiting Human Approval)

---

## Overview

This feature encompasses the research, analysis, and synthesis required to understand the work tracker domain across ADO Scrum, SAFe, and JIRA systems.

### Problem Statement

Work tracking systems have overlapping but inconsistent domain models. To build a universal Claude Code skill for work tracking, we need to:
1. Understand each system's domain entities, properties, and behaviors
2. Map relationships and state transitions
3. Synthesize a canonical ontology

### Success Criteria

- [x] Complete domain research for ADO Scrum, SAFe, and JIRA
- [x] Extracted domain models with entities, properties, behaviors, relationships, state machines
- [x] Cross-domain synthesis identifying common patterns
- [ ] Parent ontology designed with mapping rules
- [ ] Markdown templates generated for skill integration
- [ ] All artifacts reviewed and validated

---

## Enablers

| ID | Name | Status | Tasks | Critic | Description |
|----|------|--------|-------|--------|-------------|
| [EN-001](./en-001.md) | ADO Scrum Domain Analysis | COMPLETED | 6/6 | Skipped | Research and analyze ADO Scrum domain |
| [EN-002](./en-002.md) | SAFe Domain Analysis | COMPLETED | 6/6 | Skipped | Research and analyze SAFe domain |
| [EN-003](./en-003.md) | JIRA Domain Analysis | COMPLETED | 6/6 | Skipped | Research and analyze JIRA domain |
| [EN-004](./en-004.md) | Cross-Domain Synthesis | COMPLETED | 4/4 | [CL-003](../../../reviews/CL-003-synthesis-review.md) APPROVED | Synthesize patterns across domains |

---

## Units of Work

| ID | Name | Status | Tasks | Critic | Description |
|----|------|--------|-------|--------|-------------|
| [WI-001](./wi-001.md) | Parent Ontology Design | BLOCKED | 0/5 | [CL-004](../../../reviews/CL-004-ontology-review.md) BLOCKED | Design canonical ontology |
| [WI-002](./wi-002.md) | Markdown Template Generation | BLOCKED | 0/7 | [CL-005](../../../reviews/CL-005-templates-review.md) BLOCKED | Generate skill templates |
| [WI-003](./wi-003.md) | Design Review & Validation | BLOCKED | 0/4 | Final Gate | Final review and quality gate |

---

## Orchestration Pipeline

```
PHASE 1: Parallel Research (COMPLETED)
┌─────────────┬─────────────┬─────────────┐
│   EN-001    │   EN-002    │   EN-003    │
│  ADO Scrum  │    SAFe     │    JIRA     │
│ ps-research │ ps-research │ ps-research │
└──────┬──────┴──────┬──────┴──────┬──────┘
       │             │             │
       └─────────────┼─────────────┘
                     ▼
          ═══ SYNC BARRIER 1 ═══ [PASSED]

PHASE 2: Parallel Analysis (COMPLETED)
┌─────────────┬─────────────┬─────────────┐
│   EN-001    │   EN-002    │   EN-003    │
│  ADO Model  │ SAFe Model  │ JIRA Model  │
│ ps-analyst  │ ps-analyst  │ ps-analyst  │
└──────┬──────┴──────┬──────┴──────┬──────┘
       │             │             │
       └─────────────┼─────────────┘
                     ▼
          ═══ SYNC BARRIER 2 ═══ [PASSED]

PHASE 3: Cross-Domain Synthesis (COMPLETED)
              ┌─────────────┐
              │   EN-004    │
              │ ps-synthesi │
              └──────┬──────┘
                     ▼
          ═══ SYNC BARRIER 3 ═══ [CURRENT]
                     │
              ┌──────┴──────┐
              │   CL-003    │ ◄── APPROVED
              │  ps-review  │
              └──────┬──────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   [APPROVE]    [REVISE]    [DOC+PROCEED]
        │            │            │
        ▼            ▼            │
                ▲    │            │
                └────┘            │
                                  ▼
PHASE 4: Ontology Design (BLOCKED)
              ┌─────────────┐
              │   WI-001    │
              │nse-architect│
              └──────┬──────┘
                     ▼
          ═══ SYNC BARRIER 4 ═══ [BLOCKED]
                     │
              ┌──────┴──────┐
              │   CL-004    │
              │  ps-archit  │
              └──────┬──────┘
                     ▼
PHASE 5: Template Generation (BLOCKED)
              ┌─────────────┐
              │   WI-002    │
              │ ps-synthesi │
              └──────┬──────┘
                     ▼
          ═══ SYNC BARRIER 5 ═══ [BLOCKED]
                     │
              ┌──────┴──────┐
              │   CL-005    │
              │  ps-review  │
              └──────┬──────┘
                     ▼
PHASE 6: Final Review (BLOCKED)
              ┌─────────────┐
              │   WI-003    │
              │ nse-reviews │
              └─────────────┘
```

---

## Progress Tracking

| Phase | Status | Completion | Critic |
|-------|--------|------------|--------|
| Phase 1: Research | COMPLETED | 100% | Skipped |
| Phase 2: Analysis | COMPLETED | 100% | Skipped |
| Phase 3: Synthesis | COMPLETED (CL-003 APPROVED) | 100% | CL-003 APPROVED |
| Phase 4: Design | BLOCKED | 0% | CL-004 BLOCKED |
| Phase 5: Templates | BLOCKED | 0% | CL-005 BLOCKED |
| Phase 6: Review | BLOCKED | 0% | Final Gate |

**Overall Completion:** 57% (4/4 enablers complete + 0/3 work items)

---

## Critic Loops

Quality feedback loops ensure artifact integrity before proceeding to next phase.

| ID | Name | Reviews | Status | Iteration | Max | Artifact |
|----|------|---------|--------|-----------|-----|----------|
| CL-003 | Synthesis Review | EN-004 | APPROVED | 1 | 2 | `reviews/CL-003-synthesis-review.md` |
| CL-004 | Ontology Review | WI-001 | BLOCKED | 0 | 2 | `reviews/CL-004-ontology-review.md` |
| CL-005 | Templates Review | WI-002 | BLOCKED | 0 | 2 | `reviews/CL-005-templates-review.md` |

### Critic Loop Pattern

```
Producer ──► Artifact ──► Critic ──► Decision
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼
          APPROVE          REVISE       DOCUMENT+PROCEED
             │                │                │
             │         ┌──────┘                │
             │         ▼                       │
             │    Return to                    │
             │    Producer                     │
             │         │                       │
             │    ┌────┴────┐                  │
             │    │ max_iter│                  │
             │    │ reached?│                  │
             │    └────┬────┘                  │
             │         │                       │
             │    Yes  │  No                   │
             │    ▼    │  ▼                    │
             │  Human  │  Loop                 │
             │  Review │                       │
             │    │    │                       │
             │    ▼    │                       │
             └────┼────┴───────────────────────┘
                  ▼
           Next Phase
```

---

## Artifacts

| Type | Location | Status |
|------|----------|--------|
| Research: ADO | `research/ADO-SCRUM-RAW.md` | COMPLETED |
| Research: SAFe | `research/SAFE-RAW.md` | COMPLETED |
| Research: JIRA | `research/JIRA-RAW.md` | COMPLETED |
| Analysis: ADO | `analysis/ADO-SCRUM-MODEL.md` | COMPLETED |
| Analysis: SAFe | `analysis/SAFE-MODEL.md` | COMPLETED |
| Analysis: JIRA | `analysis/JIRA-MODEL.md` | COMPLETED |
| Synthesis | `synthesis/CROSS-DOMAIN-SYNTHESIS.md` | COMPLETED |
| Ontology | `synthesis/ONTOLOGY-v1.md` | Not started |
| ADR | `decisions/ADR-001-ontology-design.md` | Not started |
| Templates | `templates/*.md` | Not started |
| Review: CL-003 | `reviews/CL-003-synthesis-review.md` | COMPLETED (APPROVED) |
| Review: CL-004 | `reviews/CL-004-ontology-review.md` | Not started |
| Review: CL-005 | `reviews/CL-005-templates-review.md` | Not started |
| Discovery: DISC-004 | `discoveries/disc-004-critic-loops.md` | COMPLETED |
| Bug: BUG-001 | `bugs/BUG-001-incorrect-artifact-paths.md` | RESOLVED |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-13 | Created FT-001 for domain discovery | Claude |
| 2026-01-13 | Added EN-001, EN-002, EN-003, EN-004 | Claude |
| 2026-01-13 | Added WI-001, WI-002, WI-003 | Claude |
| 2026-01-13 | Phase 1 (Research) completed - 3 raw research docs | Claude |
| 2026-01-13 | Phase 2 (Analysis) completed - 3 domain models | Claude |
| 2026-01-13 | EN-001, EN-002, EN-003 marked COMPLETED | Claude |
| 2026-01-13 | Reached SYNC BARRIER 1 - awaiting approval | Claude |
| 2026-01-13 | Phase 3 (Synthesis) completed - EN-004 cross-domain synthesis | Claude (ps-synthesizer) |
| 2026-01-13 | EN-004 marked COMPLETED; awaiting SYNC BARRIER 3 approval | Claude |
| 2026-01-14 | Added Critic Loop infrastructure: CL-003, CL-004, CL-005 | Claude |
| 2026-01-14 | Updated tables with Critic columns; added Critic Loops section | Claude |
| 2026-01-14 | Updated pipeline diagram with critic nodes at sync barriers | Claude |
| 2026-01-14 | CL-003 critic review executed; APPROVED with 5 LOW/INFO issues | Claude (ps-reviewer) |
| 2026-01-14 | BUG-001: Fixed artifact paths (reviews/, discoveries/ moved to project root) | Claude |
| 2026-01-14 | Added artifact_paths section to ORCHESTRATION.yaml v2.1 for prevention | Claude |
