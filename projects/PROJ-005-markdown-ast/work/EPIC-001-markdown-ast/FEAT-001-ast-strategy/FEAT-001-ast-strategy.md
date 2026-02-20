# FEAT-001: AST Strategy Evaluation & Library Selection

> **Type:** feature
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** --
> **Parent:** EPIC-001
> **Owner:** --
> **Target Sprint:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and value proposition |
| [Benefit Hypothesis](#benefit-hypothesis) | Expected benefits |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [MVP Definition](#mvp-definition) | Minimum viable scope |
| [Children (Spikes)](#children-spikes) | Spike inventory |
| [Progress Summary](#progress-summary) | Overall feature progress |
| [Related Items](#related-items) | Dependencies |
| [History](#history) | Status changes |

---

## Summary

Evaluate the AST-first strategy for Jerry's markdown manipulation, select the best Python library (or decide to build from scratch), and produce a go/no-go recommendation with adversarial review. This feature is research-first: two spikes investigate the library landscape and architectural feasibility before any implementation decisions are made.

**Value Proposition:**
- Evidence-based decision on markdown tooling strategy
- 5+ libraries evaluated with feature matrices, benchmarks, and Jerry-specific compatibility testing
- Build-vs-buy trade-off formally assessed
- Adversarial review (S-002 Devil's Advocate, S-003 Steelman, S-013 Inversion) on the go/no-go decision

---

## Benefit Hypothesis

**We believe that** a rigorous evaluation of Python AST libraries against Jerry's specific markdown patterns

**Will result in** a high-confidence decision on whether to adopt, adapt, or build markdown AST tooling

**We will know we have succeeded when** the decision is backed by evidence (library feature matrices, compatibility test results, architecture analysis) and has survived adversarial review

---

## Acceptance Criteria

### Definition of Done

- [ ] SPIKE-001 complete: 5+ Python libraries evaluated with evidence
- [ ] SPIKE-002 complete: AST architecture feasibility assessed
- [ ] Build-from-scratch option formally evaluated against adoption options
- [ ] Feature matrix comparing all options across Jerry-specific requirements
- [ ] Go/no-go recommendation with rationale
- [ ] Adversarial review completed (S-003 Steelman, S-002 Devil's Advocate, S-013 Inversion)
- [ ] ADR published documenting the decision
- [ ] If go: integration architecture defined (CLI extension vs hidden skills vs both)
- [ ] If no-go: alternative strategy documented

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | 5+ Python markdown AST libraries identified and evaluated | [ ] |
| AC-2 | Each library tested against Jerry markdown samples (blockquote frontmatter, nav tables, Mermaid, template placeholders) | [ ] |
| AC-3 | Build-from-scratch effort estimated with architecture sketch | [ ] |
| AC-4 | Feature matrix with weighted scoring published | [ ] |
| AC-5 | Token efficiency analysis: AST operations vs raw text operations | [ ] |
| AC-6 | Integration options assessed: Jerry CLI command, hidden skill, or hybrid | [ ] |
| AC-7 | Adversarial review artifacts persisted to decisions/ | [ ] |

---

## MVP Definition

### In Scope (MVP)

- Library landscape research (5+ Python libraries)
- Jerry-specific compatibility testing (sample files)
- Build-vs-buy analysis
- Go/no-go recommendation with adversarial review
- ADR documenting the decision

### Out of Scope (Future)

- Actual library integration (separate feature, after go decision)
- Full skill migration (separate feature)
- Performance benchmarking at scale (future spike if needed)
- Schema definition language design (future feature)

---

## Children (Spikes)

### Spike Inventory

| ID | Type | Title | Status | Priority | Timebox |
|----|------|-------|--------|----------|---------|
| SPIKE-001 | Spike | Python Markdown AST Library Landscape | pending | high | 12h |
| SPIKE-002 | Spike | AST-First Architecture Feasibility Assessment | pending | high | 8h |

### Work Item Links

- [SPIKE-001: Python Markdown AST Library Landscape](./SPIKE-001-library-landscape/SPIKE-001-library-landscape.md)
- [SPIKE-002: AST-First Architecture Feasibility Assessment](./SPIKE-002-feasibility/SPIKE-002-feasibility.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Spikes:    [....................] 0% (0/2 completed)              |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Spikes** | 2 |
| **Completed Spikes** | 0 |
| **Completion %** | 0% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001: Markdown AST Infrastructure](../EPIC-001-markdown-ast.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| SPIKE-001 informs | SPIKE-002 | Library capabilities inform feasibility assessment |
| SPIKE-002 informs | Go/no-go ADR | Feasibility determines whether to proceed |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Feature created. Two spikes: library landscape (SPIKE-001) and feasibility (SPIKE-002). |
