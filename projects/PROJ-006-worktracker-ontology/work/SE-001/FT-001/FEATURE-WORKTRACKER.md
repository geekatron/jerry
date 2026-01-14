# FEATURE-WORKTRACKER: FT-001 Domain Discovery

> **Feature ID:** FT-001
> **Name:** Domain Discovery
> **Status:** PENDING APPROVAL
> **Parent:** [SE-001](../SOLUTION-WORKTRACKER.md)
> **Created:** 2026-01-13
> **Last Updated:** 2026-01-13

---

## Overview

This feature encompasses the research, analysis, and synthesis required to understand the work tracker domain across ADO Scrum, SAFe, and JIRA systems.

### Problem Statement

Work tracking systems have overlapping but inconsistent domain models. To build a universal Claude Code skill for work tracking, we need to:
1. Understand each system's domain entities, properties, and behaviors
2. Map relationships and state transitions
3. Synthesize a canonical ontology

### Success Criteria

- [ ] Complete domain research for ADO Scrum, SAFe, and JIRA
- [ ] Extracted domain models with entities, properties, behaviors, relationships, state machines
- [ ] Cross-domain synthesis identifying common patterns
- [ ] Parent ontology designed with mapping rules
- [ ] Markdown templates generated for skill integration
- [ ] All artifacts reviewed and validated

---

## Enablers

| ID | Name | Status | Tasks | Description |
|----|------|--------|-------|-------------|
| [EN-001](./en-001.md) | ADO Scrum Domain Analysis | PENDING | 0/6 | Research and analyze ADO Scrum domain |
| [EN-002](./en-002.md) | SAFe Domain Analysis | PENDING | 0/6 | Research and analyze SAFe domain |
| [EN-003](./en-003.md) | JIRA Domain Analysis | PENDING | 0/6 | Research and analyze JIRA domain |
| [EN-004](./en-004.md) | Cross-Domain Synthesis | BLOCKED | 0/4 | Synthesize patterns across domains |

---

## Units of Work

| ID | Name | Status | Tasks | Description |
|----|------|--------|-------|-------------|
| [WI-001](./wi-001.md) | Parent Ontology Design | BLOCKED | 0/5 | Design canonical ontology |
| [WI-002](./wi-002.md) | Markdown Template Generation | BLOCKED | 0/7 | Generate skill templates |
| [WI-003](./wi-003.md) | Design Review & Validation | BLOCKED | 0/4 | Final review and quality gate |

---

## Orchestration Pipeline

```
PHASE 1: Parallel Research
┌─────────────┬─────────────┬─────────────┐
│   EN-001    │   EN-002    │   EN-003    │
│  ADO Scrum  │    SAFe     │    JIRA     │
│ ps-research │ ps-research │ ps-research │
└──────┬──────┴──────┬──────┴──────┬──────┘
       │             │             │
       └─────────────┼─────────────┘
                     │
          ═══ SYNC BARRIER 1 ═══

PHASE 2: Parallel Analysis
┌─────────────┬─────────────┬─────────────┐
│   EN-001    │   EN-002    │   EN-003    │
│  ADO Model  │ SAFe Model  │ JIRA Model  │
│ ps-analyst  │ ps-analyst  │ ps-analyst  │
└──────┬──────┴──────┬──────┴──────┬──────┘
       │             │             │
       └─────────────┼─────────────┘
                     │
          ═══ SYNC BARRIER 2 ═══

PHASE 3: Cross-Domain Synthesis
              ┌─────────────┐
              │   EN-004    │
              │ ps-synthesi │
              └──────┬──────┘
                     │
          ═══ SYNC BARRIER 3 ═══

PHASE 4: Ontology Design
              ┌─────────────┐
              │   WI-001    │
              │nse-architect│
              └──────┬──────┘
                     │
PHASE 5: Template Generation
              ┌─────────────┐
              │   WI-002    │
              │ ps-synthesi │
              └──────┬──────┘
                     │
PHASE 6: Review
              ┌─────────────┐
              │   WI-003    │
              │ nse-reviews │
              └─────────────┘
```

---

## Progress Tracking

| Phase | Status | Completion |
|-------|--------|------------|
| Phase 1: Research | PENDING | 0% |
| Phase 2: Analysis | PENDING | 0% |
| Phase 3: Synthesis | BLOCKED | 0% |
| Phase 4: Design | BLOCKED | 0% |
| Phase 5: Templates | BLOCKED | 0% |
| Phase 6: Review | BLOCKED | 0% |

**Overall Completion:** 0%

---

## Artifacts

| Type | Location | Status |
|------|----------|--------|
| Research: ADO | `research/ADO-SCRUM-RAW.md` | Not started |
| Research: SAFe | `research/SAFE-RAW.md` | Not started |
| Research: JIRA | `research/JIRA-RAW.md` | Not started |
| Analysis: ADO | `analysis/ADO-SCRUM-MODEL.md` | Not started |
| Analysis: SAFe | `analysis/SAFE-MODEL.md` | Not started |
| Analysis: JIRA | `analysis/JIRA-MODEL.md` | Not started |
| Synthesis | `synthesis/CROSS-DOMAIN-SYNTHESIS.md` | Not started |
| Ontology | `synthesis/ONTOLOGY-v1.md` | Not started |
| ADR | `decisions/ADR-001-ontology-design.md` | Not started |
| Templates | `templates/*.md` | Not started |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-13 | Created FT-001 for domain discovery | Claude |
| 2026-01-13 | Added EN-001, EN-002, EN-003, EN-004 | Claude |
| 2026-01-13 | Added WI-001, WI-002, WI-003 | Claude |
