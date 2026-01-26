# FEAT-001: Competitive Research & Analysis

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
-->

> **Type:** feature
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-25T00:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** EPIC-001
> **Owner:** Claude
> **Target Sprint:** Sprint 1

---

## Summary

Conduct comprehensive competitive research and analysis of meeting transcript/intelligence tools to derive requirements, understand industry best practices, and inform architectural decisions for the Transcript Skill.

**Value Proposition:**
- Evidence-based requirements from real product analysis
- Understanding of industry patterns and user expectations
- Informed architectural decisions avoiding common pitfalls

---

## Benefit Hypothesis

**We believe that** conducting deep competitive analysis of 5 leading products

**Will result in** well-informed requirements and architecture decisions

**We will know we have succeeded when:**
- Feature matrices exist for all 5 products
- 5W2H analysis is complete and reviewed
- FMEA identifies key failure modes
- Requirements specification passes critic review

---

## Acceptance Criteria

### Definition of Done

- [ ] 5 products analyzed (Pocket, Otter.ai, Fireflies, Grain, tl;dv)
- [ ] Feature comparison matrix created
- [ ] 5W2H framework analysis complete
- [ ] Ishikawa (fishbone) diagram created
- [ ] FMEA analysis with RPN scores
- [ ] ps-critic review passed
- [ ] Documentation at all 3 levels (ELI5, Engineer, Architect)

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Each product has dedicated research document | [ ] |
| AC-2 | Feature comparison matrix covers 10+ features | [ ] |
| AC-3 | All research has citations and sources | [ ] |
| AC-4 | Requirements derived from competitive analysis | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Research documents follow L0/L1/L2 format | [ ] |
| NFC-2 | All claims have evidence/citations | [ ] |

---

## MVP Definition

### In Scope (MVP)

- Competitive analysis of 5 products
- Feature comparison matrix
- 5W2H problem framing
- Basic FMEA analysis
- Requirements specification

### Out of Scope (Future)

- Pricing analysis
- User interview data
- A/B testing results
- Market size analysis

---

## Children (Enablers/Stories)

### Enabler/Story Inventory

| ID | Type | Title | Status | Priority | Effort |
|----|------|-------|--------|----------|--------|
| [EN-001](./EN-001-market-analysis/EN-001-market-analysis.md) | Enabler | Market Analysis Research | pending | high | 13 |
| [EN-002](./EN-002-technical-standards/EN-002-technical-standards.md) | Enabler | Technical Standards Research | pending | high | 8 |
| [EN-003](./EN-003-requirements-synthesis/EN-003-requirements-synthesis.md) | Enabler | Requirements Synthesis | pending | high | 8 |

### Work Item Links

- [EN-001: Market Analysis Research](./EN-001-market-analysis/EN-001-market-analysis.md)
- [EN-002: Technical Standards Research](./EN-002-technical-standards/EN-002-technical-standards.md)
- [EN-003: Requirements Synthesis](./EN-003-requirements-synthesis/EN-003-requirements-synthesis.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Enablers:  [....................] 0% (0/3 completed)             |
| Stories:   [....................] 0% (0/0 completed)             |
| Tasks:     [....................] 0% (0/5 completed)             |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Enablers** | 3 |
| **Completed Enablers** | 0 |
| **Total Stories** | 0 |
| **Completed Stories** | 0 |
| **Total Effort (points)** | 29 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Orchestration Pipeline

```
+------------------------------------------------------------------+
|              FEAT-001 RESEARCH PIPELINE                           |
+------------------------------------------------------------------+
|                                                                    |
|  PHASE 0A: PARALLEL COMPETITIVE RESEARCH                          |
|  ┌─────────────────────────────────────────────────────────┐      |
|  │                                                          │      |
|  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │      |
|  │  │ps-researcher│  │ps-researcher│  │ps-researcher│     │      |
|  │  │ (Pocket)    │  │ (Otter.ai)  │  │ (Fireflies) │     │      |
|  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │      |
|  │         │                │                │             │      |
|  │  ┌─────────────┐  ┌─────────────┐                      │      |
|  │  │ps-researcher│  │ps-researcher│                      │      |
|  │  │ (Grain)     │  │ (tl;dv)     │                      │      |
|  │  └──────┬──────┘  └──────┬──────┘                      │      |
|  │         │                │                              │      |
|  │  ┌──────┴────────────────┴──────────────────┐          │      |
|  │  │           SYNC BARRIER 1                  │          │      |
|  │  └───────────────────────────────────────────┘          │      |
|  └─────────────────────────────────────────────────────────┘      |
|                              │                                     |
|                              ▼                                     |
|  PHASE 0B: FRAMEWORK ANALYSIS                                     |
|  ┌─────────────────────────────────────────────────────────┐      |
|  │  ┌───────────┐  ┌───────────┐  ┌───────────┐           │      |
|  │  │ps-analyst │  │ps-analyst │  │nse-require│           │      |
|  │  │ (5W2H)    │  │ (FMEA)    │  │ (Reqs)    │           │      |
|  │  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘           │      |
|  │        └──────────────┼──────────────┘                  │      |
|  │                       │                                 │      |
|  │  ┌────────────────────┴────────────────────┐           │      |
|  │  │           SYNC BARRIER 2                 │           │      |
|  │  └──────────────────────────────────────────┘           │      |
|  └─────────────────────────────────────────────────────────┘      |
|                              │                                     |
|                              ▼                                     |
|  PHASE 0C: SYNTHESIS & REVIEW                                     |
|  ┌─────────────────────────────────────────────────────────┐      |
|  │  ┌───────────────┐      ┌───────────────┐              │      |
|  │  │ ps-synthesizer│ ───▶ │  ps-critic    │              │      |
|  │  │ (Combine)     │      │ (Adversarial) │              │      |
|  │  └───────────────┘      └───────┬───────┘              │      |
|  │                                 │                       │      |
|  │  ┌──────────────────────────────┴───────────────────┐  │      |
|  │  │           SYNC BARRIER 3 (Human Approval)         │  │      |
|  │  └───────────────────────────────────────────────────┘  │      |
|  └─────────────────────────────────────────────────────────┘      |
+------------------------------------------------------------------+
```

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001: Transcript Skill Foundation](../EPIC-001-transcript-skill.md)

### Related Features

- FEAT-002: VTT Parser (depends on this feature's outputs)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | None | First feature to execute |
| Blocks | FEAT-002 | Implementation requires research |
| Blocks | FEAT-003 | Mind map design needs requirements |
| Blocks | FEAT-004 | Integration needs architecture |

---

## Artifacts

### Bugs
- None identified

### Discoveries
- None documented yet

### Decisions
- See EPIC-001 decisions (DEC-001, DEC-002, DEC-003)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-25 | Claude | pending | Feature created |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Feature |
| **SAFe** | Feature (Program Backlog) |
| **JIRA** | Epic (or custom issue type) |
