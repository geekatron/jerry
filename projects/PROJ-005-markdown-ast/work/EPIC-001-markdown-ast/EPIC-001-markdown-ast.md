# EPIC-001: Markdown AST Infrastructure

> **Type:** epic
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** 2026-02-21
> **Parent:** PROJ-005-markdown-ast
> **Owner:** --
> **Target Quarter:** FY26-Q1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key objectives |
| [Business Outcome Hypothesis](#business-outcome-hypothesis) | Expected outcomes |
| [Lean Business Case](#lean-business-case) | Problem/solution/cost/benefit |
| [Children Features/Capabilities](#children-featurescapabilities) | Feature and spike inventory |
| [Progress Summary](#progress-summary) | Overall epic progress |
| [Related Items](#related-items) | Dependencies and related work |
| [History](#history) | Status changes and key events |

---

## Summary

Replace raw text manipulation of markdown files with an AST (Abstract Syntax Tree) intermediary. Today, every markdown operation across Jerry's full surface — worktracker entities, skill definitions, rules, templates, orchestration plans, ADRs — is performed through string find-and-replace on `.md` files. An AST approach would enable structured parsing, typed manipulation, schema validation, and clean rendering.

**Key Objectives:**
- Evaluate 5+ Python markdown AST libraries against Jerry's requirements (blockquote frontmatter, navigation tables, template placeholders, Mermaid code blocks)
- Assess build-from-scratch vs adopt-existing trade-off with evidence
- Determine go/no-go on AST strategy with adversarial review
- If go: define integration architecture (Jerry CLI extension vs hidden Claude skills)
- If no-go: document alternative strategy with rationale

---

## Business Outcome Hypothesis

**We believe that** replacing raw text markdown manipulation with AST-based structured operations

**Will result in** reduced token consumption, fewer structural errors, faster template instantiation, and reliable schema enforcement across Jerry's documentation surface

**We will know we have succeeded when** markdown operations use typed APIs (parse/query/transform/render) instead of string replacement, and structural validation catches errors at parse time rather than at human review

---

## Lean Business Case

| Aspect | Description |
|--------|-------------|
| **Problem** | All Jerry markdown is manipulated via raw text operations. This is brittle (exact string matching), schema-unaware (no validation), token-expensive (full file reads for targeted changes), and inconsistent (ad-hoc parsing per file type). |
| **Solution** | Parse markdown into AST, manipulate via typed API, validate against schemas, render back to clean markdown. Integrate into Jerry CLI or Claude-accessible tooling. |
| **Cost** | Research spikes + library integration + skill migration. Estimated 2-3 orchestration cycles. |
| **Benefit** | Reduced token consumption per markdown operation. Schema enforcement at parse time. Consistent cross-file operations. Foundation for advanced features (auto-migration, bulk transforms, validation CI). |
| **Risk** | Python AST libraries may not handle Jerry's markdown dialect (blockquote frontmatter, custom patterns). Build-from-scratch may be prohibitively expensive. Migration of existing skills may introduce regressions. |

---

## Children Features/Capabilities

### Feature Inventory

| ID | Title | Status | Priority | Progress |
|----|-------|--------|----------|----------|
| FEAT-001 | AST Strategy Evaluation & Library Selection | completed | high | 100% (13/13 items) |

### Spike Inventory

| ID | Title | Status | Priority | Timebox | Parent |
|----|-------|--------|----------|---------|--------|
| SPIKE-001 | Python Markdown AST Library Landscape | completed | high | 12 hours | FEAT-001 |
| SPIKE-002 | AST-First Architecture Feasibility Assessment | completed | high | 8 hours | FEAT-001 |

### Feature Links

- [FEAT-001: AST Strategy Evaluation & Library Selection](./FEAT-001-ast-strategy/FEAT-001-ast-strategy.md)

### Spike Links

- [SPIKE-001: Python Markdown AST Library Landscape](./FEAT-001-ast-strategy/SPIKE-001-library-landscape/SPIKE-001-library-landscape.md)
- [SPIKE-002: AST-First Architecture Feasibility Assessment](./FEAT-001-ast-strategy/SPIKE-002-feasibility/SPIKE-002-feasibility.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [####################] 100% (1/1 completed)            |
| Spikes:    [####################] 100% (2/2 completed)           |
+------------------------------------------------------------------+
| Overall:   [####################] 100% (FEAT-001 complete)        |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Features** | 1 |
| **Completed Features** | 1 |
| **Total Spikes** | 2 |
| **Completed Spikes** | 2 |
| **Feature Completion %** | 100% (13/13 FEAT-001 items done) |

---

## Related Items

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Informs | All Jerry skills | AST tooling would change how skills manipulate markdown |
| Informs | /worktracker skill | Worktracker entities are the most schema-rigid markdown files |
| Informs | PROJ-004 context resilience | AST could reduce token consumption, extending context lifetime |
| Relates To | .context/templates/ | Templates are the source schemas for markdown files |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Epic created. Full-surface AST infrastructure initiative. Python-only, 5+ library evaluation required. |
| 2026-02-19 | Claude | in-progress | Both spikes completed. GO decision: adopt markdown-it-py + mdformat with Pattern D hybrid integration. Orchestration `spike-eval-20260219-001` complete (QG scores: 0.96, 0.97, 0.96). |
| 2026-02-20 | Claude | in-progress | FEAT-001 decomposed: EN-001 (R-01 PoC gate) + 10 stories = 40 SP across 4 phases. Next: EN-001 (critical gate). |
| 2026-02-21 | Claude | in-progress | Worktracker sync: 12/13 FEAT-001 items completed (38/40 SP). 1,925 LOC, 404 tests, 100% domain coverage. ST-009 (pre-commit hook, 2 SP) remaining. |
| 2026-02-21 | Claude | completed | ST-009 completed. All 13/13 FEAT-001 items done (40/40 SP). Total: ~2,200 LOC, 439 tests (35 for ST-009), 98%+ coverage across all modules. EPIC-001 complete. |
