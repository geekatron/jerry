# EN-001: Market Analysis Research

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-25T00:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** FEAT-001
> **Owner:** Claude
> **Target Sprint:** Sprint 1
> **Effort Points:** 13

---

## Summary

Conduct comprehensive competitive analysis of 5 leading meeting transcript/intelligence products to understand industry capabilities, feature sets, and user expectations. This research forms the foundation for evidence-based requirements derivation.

**Technical Justification:**
- Industry best practices inform architecture decisions
- Feature matrices reveal market expectations
- Competitive gaps identify differentiation opportunities
- User patterns guide entity extraction priorities

---

## Benefit Hypothesis

**We believe that** analyzing 5 leading products (Pocket, Otter.ai, Fireflies, Grain, tl;dv)

**Will result in** comprehensive understanding of industry capabilities and user expectations

**We will know we have succeeded when:**
- Each product has a detailed research document with citations
- Feature comparison matrix covers 10+ features
- Entity extraction approaches are documented
- Integration patterns are catalogued

---

## Acceptance Criteria

### Definition of Done

- [ ] 5 products researched (Pocket, Otter.ai, Fireflies, Grain, tl;dv)
- [ ] Each product has dedicated research document
- [ ] Feature comparison matrix created
- [ ] All research has citations and sources
- [ ] L0/L1/L2 documentation for findings
- [ ] ps-critic review passed

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | Research documents follow standard template | [ ] |
| TC-2 | All claims have evidence/citations | [ ] |
| TC-3 | Feature matrix is machine-parseable (YAML/JSON) | [ ] |
| TC-4 | Entity types documented per product | [ ] |

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner | Effort | Blocked By |
|----|-------|--------|-------|--------|------------|
| [TASK-001](./TASK-001-research-pocket.md) | Research Pocket (heypocket.com) | pending | ps-researcher | 3 | None |
| [TASK-002](./TASK-002-research-otter.md) | Research Otter.ai | pending | ps-researcher | 2 | None |
| [TASK-003](./TASK-003-research-fireflies.md) | Research Fireflies.ai | pending | ps-researcher | 2 | None |
| [TASK-004](./TASK-004-research-grain.md) | Research Grain | pending | ps-researcher | 2 | None |
| [TASK-005](./TASK-005-research-tldv.md) | Research tl;dv | pending | ps-researcher | 2 | None |
| TASK-006 | Synthesize Feature Matrix | pending | ps-synthesizer | 2 | TASK-001..005 |

### Task Links

- [TASK-001: Research Pocket](./TASK-001-research-pocket.md)
- [TASK-002: Research Otter.ai](./TASK-002-research-otter.md)
- [TASK-003: Research Fireflies.ai](./TASK-003-research-fireflies.md)
- [TASK-004: Research Grain](./TASK-004-research-grain.md)
- [TASK-005: Research tl;dv](./TASK-005-research-tldv.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/6 completed)             |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 6 |
| **Completed Tasks** | 0 |
| **In Progress Tasks** | 0 |
| **Total Effort (points)** | 13 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Research Template

Each product research task should produce a document with the following structure:

```markdown
# {Product Name} Competitive Analysis

## L0: ELI5 Summary
{What does this product do in simple terms?}

## L1: Engineer Summary
{Technical capabilities, APIs, integrations}

## L2: Architect Summary
{Architecture patterns, scalability, trade-offs}

## Feature Analysis

### Core Features
| Feature | Description | Evidence |
|---------|-------------|----------|

### Entity Extraction
| Entity Type | Supported | Accuracy (if known) | Evidence |
|-------------|-----------|---------------------|----------|

### Integrations
| Platform | Integration Type | Evidence |
|----------|------------------|----------|

### Transcript Formats
| Format | Supported | Evidence |
|--------|-----------|----------|

## Strengths
- {Citation required}

## Weaknesses
- {Citation required}

## Pricing (if available)
| Tier | Price | Features |
|------|-------|----------|

## References
1. {URL with access date}
2. {Documentation link}
```

---

## Orchestration Pipeline

```
+------------------------------------------------------------------+
|              EN-001 RESEARCH PIPELINE                             |
+------------------------------------------------------------------+
|                                                                    |
|  PARALLEL RESEARCH PHASE (Fan-Out)                                |
|  ┌─────────────────────────────────────────────────────────┐      |
|  │                                                          │      |
|  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │      |
|  │  │ps-researcher│  │ps-researcher│  │ps-researcher│     │      |
|  │  │ TASK-001    │  │ TASK-002    │  │ TASK-003    │     │      |
|  │  │ (Pocket)    │  │ (Otter.ai)  │  │ (Fireflies) │     │      |
|  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │      |
|  │         │                │                │             │      |
|  │  ┌─────────────┐  ┌─────────────┐                      │      |
|  │  │ps-researcher│  │ps-researcher│                      │      |
|  │  │ TASK-004    │  │ TASK-005    │                      │      |
|  │  │ (Grain)     │  │ (tl;dv)     │                      │      |
|  │  └──────┬──────┘  └──────┬──────┘                      │      |
|  │         │                │                              │      |
|  │  ┌──────┴────────────────┴──────────────────┐          │      |
|  │  │           SYNC BARRIER 1                  │          │      |
|  │  │   (All 5 research tasks complete)         │          │      |
|  │  └───────────────────────────────────────────┘          │      |
|  └─────────────────────────────────────────────────────────┘      |
|                              │                                     |
|                              ▼                                     |
|  SYNTHESIS PHASE (Fan-In)                                         |
|  ┌─────────────────────────────────────────────────────────┐      |
|  │  ┌───────────────┐                                      │      |
|  │  │ ps-synthesizer│ ──▶ Feature Matrix                   │      |
|  │  │ TASK-006      │                                      │      |
|  │  └───────────────┘                                      │      |
|  └─────────────────────────────────────────────────────────┘      |
+------------------------------------------------------------------+
```

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Competitive Research & Analysis](../FEAT-001-competitive-research.md)
- **Grandparent Epic:** [EPIC-001: Transcript Skill Foundation](../../EPIC-001-transcript-skill.md)

### Related Enablers

- EN-002: Technical Standards Research (parallel, no dependency)
- EN-003: Requirements Synthesis (depends on this enabler)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | None | First enabler to execute |
| Blocks | EN-003 | Requirements need research findings |
| Blocks | FEAT-002 | Implementation needs requirements |

---

## Artifacts

### Research Documents (To Be Created)

| Product | Document Path | Status |
|---------|---------------|--------|
| Pocket | `research/POCKET-analysis.md` | PENDING |
| Otter.ai | `research/OTTER-analysis.md` | PENDING |
| Fireflies.ai | `research/FIREFLIES-analysis.md` | PENDING |
| Grain | `research/GRAIN-analysis.md` | PENDING |
| tl;dv | `research/TLDV-analysis.md` | PENDING |

### Synthesized Outputs (To Be Created)

| Artifact | Path | Status |
|----------|------|--------|
| Feature Comparison Matrix | `research/FEATURE-MATRIX.md` | PENDING |
| Feature Matrix (YAML) | `research/feature-matrix.yaml` | PENDING |

### Discoveries

- None documented yet

### Decisions

- See EPIC-001 decisions (DEC-001, DEC-002, DEC-003)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-25 | Claude | pending | Enabler created |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (tagged Architecture) |
| **SAFe** | Enabler Story |
| **JIRA** | Task |
