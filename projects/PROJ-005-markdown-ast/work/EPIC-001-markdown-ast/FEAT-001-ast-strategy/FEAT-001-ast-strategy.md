# FEAT-001: AST Strategy Evaluation & Library Selection

> **Type:** feature
> **Status:** in-progress
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
| [Children](#children) | Full work item inventory |
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

## Children

### Spike Inventory

| ID | Type | Title | Status | Priority | Timebox |
|----|------|-------|--------|----------|---------|
| SPIKE-001 | Spike | Python Markdown AST Library Landscape | completed | high | 12h |
| SPIKE-002 | Spike | AST-First Architecture Feasibility Assessment | completed | high | 8h |

### Enabler Inventory

| ID | Type | Title | Status | Priority | Effort | Phase |
|----|------|-------|--------|----------|--------|-------|
| EN-001 | Enabler | R-01 PoC: mdformat blockquote frontmatter write-back | pending | critical | 3 | Gate |

### Story Inventory

| ID | Title | Status | Priority | Effort | Phase | Blocked By |
|----|-------|--------|----------|--------|-------|------------|
| ST-001 | Implement JerryDocument facade | pending | high | 5 | 1 | EN-001 |
| ST-002 | Implement blockquote frontmatter extension | pending | high | 5 | 1 | EN-001, ST-001 |
| ST-003 | Implement L2-REINJECT parser | pending | high | 3 | 1 | EN-001, ST-001 |
| ST-004 | Add `jerry ast` CLI commands | pending | medium | 3 | 1 | ST-001 |
| ST-005 | Create `/ast` Claude skill | pending | medium | 3 | 2 | ST-001, ST-002 |
| ST-006 | Implement schema validation engine | pending | medium | 5 | 2-3 | ST-001, ST-002 |
| ST-007 | Migrate /worktracker agents to AST | pending | medium | 3 | 2 | ST-005, ST-006 |
| ST-008 | Implement navigation table helpers | pending | low | 3 | 3 | ST-001 |
| ST-009 | Add pre-commit validation hook | pending | low | 2 | 3 | ST-004, ST-006, ST-008 |
| ST-010 | Migrate remaining skills | pending | low | 5 | 4 | ST-007, ST-005 |

### Effort Summary

| Category | Count | Story Points |
|----------|-------|-------------|
| Spikes (completed) | 2 | -- |
| Enablers | 1 | 3 |
| Stories | 10 | 37 |
| **Total** | **13** | **40** |

### Work Item Links

**Spikes:**
- [SPIKE-001: Python Markdown AST Library Landscape](./SPIKE-001-library-landscape/SPIKE-001-library-landscape.md)
- [SPIKE-002: AST-First Architecture Feasibility Assessment](./SPIKE-002-feasibility/SPIKE-002-feasibility.md)

**Enabler:**
- [EN-001: R-01 PoC -- mdformat blockquote frontmatter write-back](./EN-001-r01-poc/EN-001-r01-poc.md)

**Stories:**
- [ST-001: Implement JerryDocument facade](./ST-001-jerry-document/ST-001-jerry-document.md)
- [ST-002: Implement blockquote frontmatter extension](./ST-002-frontmatter-ext/ST-002-frontmatter-ext.md)
- [ST-003: Implement L2-REINJECT parser](./ST-003-reinject-parser/ST-003-reinject-parser.md)
- [ST-004: Add `jerry ast` CLI commands](./ST-004-cli-commands/ST-004-cli-commands.md)
- [ST-005: Create `/ast` Claude skill](./ST-005-ast-skill/ST-005-ast-skill.md)
- [ST-006: Implement schema validation engine](./ST-006-schema-validation/ST-006-schema-validation.md)
- [ST-007: Migrate /worktracker agents to AST](./ST-007-worktracker-migration/ST-007-worktracker-migration.md)
- [ST-008: Implement navigation table helpers](./ST-008-nav-table-helpers/ST-008-nav-table-helpers.md)
- [ST-009: Add pre-commit validation hook](./ST-009-precommit-hook/ST-009-precommit-hook.md)
- [ST-010: Migrate remaining skills](./ST-010-remaining-migrations/ST-010-remaining-migrations.md)

### Dependency Graph

```
EN-001 (R-01 PoC) ─── GATE ──────────────────────────────────────
    │
    ▼
ST-001 (JerryDocument) ────────────────────────────────────────
    │         │         │           │
    ▼         ▼         ▼           ▼
ST-002    ST-003    ST-004      ST-008
(frontmatter) (reinject) (CLI)    (nav tables)
    │         │         │           │
    ├─────────┤         │           │
    ▼         │         │           │
ST-005      │         │           │
(/ast skill)  │         │           │
    │         │         │           │
    ▼         │         │           │
ST-006 ◄──────┘         │           │
(schema)                │           │
    │                   │           │
    ▼                   ▼           ▼
ST-007              ST-009 ◄────────┘
(/worktracker)      (pre-commit)
    │
    ▼
ST-010
(remaining)
```

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Spikes:    [####################] 100% (2/2 completed)           |
| Enablers:  [....................] 0%   (0/1 completed)           |
| Stories:   [....................] 0%   (0/10 completed)          |
+------------------------------------------------------------------+
| Overall:   [###.................] 15%  (2/13 items done)         |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Items** | 13 (2 spikes + 1 enabler + 10 stories) |
| **Completed** | 2 (spikes) |
| **Total Story Points** | 40 (3 enabler + 37 stories) |
| **Completed Story Points** | 0 |
| **Completion %** | 15% (spikes done; enabler and stories pending) |
| **Next:** | EN-001 (R-01 PoC) -- critical gate |

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
| 2026-02-19 | Claude | in-progress | Both spikes completed via orchestration `spike-eval-20260219-001`. GO decision: adopt markdown-it-py + mdformat with Pattern D hybrid integration. QG scores: 0.96, 0.97, 0.96. ADR and implementation stories pending. |
| 2026-02-20 | Claude | in-progress | Work decomposed: EN-001 (R-01 PoC gate, 3 SP) + 10 stories (37 SP). Total: 40 SP across 4 implementation phases. |
