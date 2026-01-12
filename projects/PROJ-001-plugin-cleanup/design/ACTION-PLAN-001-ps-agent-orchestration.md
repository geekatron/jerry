# Action Plan: PS-* Agent Orchestration for Document Ingestion

> **Document ID**: ACTION-PLAN-001
> **Date**: 2026-01-09
> **Author**: Claude (Session cc/task-subtask)
> **Purpose**: Systematic ingestion of 82 design documents using ps-* agents
> **Status**: PROPOSED

---

## Executive Summary

This plan defines a systematic approach to ingest all design artifacts from the Jerry repository using the problem-solving (ps-*) agent framework. The goal is to build a comprehensive, persistent knowledge foundation that survives context compaction.

**Critical Correction**: The initial Document Index (DOCUMENT-INDEX-001) incorrectly weighted `WORKTRACKER_PROPOSAL.md` as P3 (Historical). Based on user input, this is the **primary synthesis document** and should be **P0 Critical Foundation**.

---

## Document Evolution Chain (User-Defined)

The user spent several days developing these documents in this evolutionary order:

```
1. REVISED-ARCHITECTURE-v3.0.md
   └── Foundation: Event Sourcing + CQRS + Hexagonal Architecture
       │
       ▼
2. glimmering-brewing-lake-v3.md
   └── Claude's analysis of v2.0 with recommendations for v3.0
       │
       ▼
3. projects/archive/PLAN.md
   └── Graph Database direction emerged here
   └── Property Graph Model (Vertex/Edge abstractions)
       │
       ▼
4. WORKTRACKER_PROPOSAL.md ← PRIMARY SYNTHESIS (Most Comprehensive)
   └── Marriage of all research into executable 32-week design
   └── Full BDD test specifications
   └── Detailed task breakdowns with RED/GREEN/REFACTOR
```

### Corrected Weighting

| Document | Original Weight | Corrected Weight | Rationale |
|----------|-----------------|------------------|-----------|
| WORKTRACKER_PROPOSAL.md | P3 (Historical) | **P0 (Critical)** | Primary synthesis, executable design |
| projects/archive/PLAN.md | P2 | **P0 (Critical)** | Graph architecture direction |
| REVISED-ARCHITECTURE-v3.0.md | P1 | P1 | Foundation patterns |
| glimmering-brewing-lake-v3.md | P0 | P0 | Strategic plan |

---

## PS-* Agent Orchestration Strategy

### Available Agents

| Agent | Role | Output Location |
|-------|------|-----------------|
| `ps-researcher` | Gather information with citations | `docs/research/` |
| `ps-analyst` | Deep analysis (5 Whys, trade-offs, gaps) | `docs/analysis/` |
| `ps-synthesizer` | Pattern extraction across documents | `docs/synthesis/` |
| `ps-architect` | Create ADRs with Nygard format | `docs/decisions/` |
| `ps-validator` | Verify constraints with evidence | `docs/analysis/` |
| `ps-reporter` | Status and progress reports | `docs/reports/` |

### Orchestration Constraints

Per Jerry Constitution (P-003: No Recursive Subagents):
- Maximum ONE level of nesting (orchestrator → agent)
- Agents CANNOT spawn other agents
- State passed via file artifacts

---

## Recommended Approach: Tiered Synthesis

### Tier 1: Primary Synthesis Extraction (Parallel)

**Goal**: Extract the authoritative patterns from the evolutionary documents.

| Agent | Target Document | Output | Purpose |
|-------|-----------------|--------|---------|
| ps-researcher | `WORKTRACKER_PROPOSAL.md` | `docs/research/wt-proposal-extraction.md` | Extract architecture patterns, domain model, testing strategy |
| ps-researcher | `projects/archive/PLAN.md` | `docs/research/plan-graph-model.md` | Extract graph primitives, Gremlin patterns |

**Execution**: Launch in parallel (no dependencies)

### Tier 2: Evolutionary Context (Sequential after Tier 1)

**Goal**: Understand how decisions evolved and why.

| Agent | Target Documents | Output | Purpose |
|-------|------------------|--------|---------|
| ps-researcher | `REVISED-ARCHITECTURE-v3.0.md` | `docs/research/arch-v3-foundation.md` | Extract Event Sourcing, CQRS, Hexagonal patterns |
| ps-researcher | `glimmering-brewing-lake-v3.md` | `docs/research/strategic-plan-v3.md` | Extract 5W1H, bounded contexts, wisdom |

**Execution**: Can run in parallel

### Tier 3: Cross-Document Synthesis (After Tier 1 & 2)

**Goal**: Create unified understanding from all research artifacts.

| Agent | Input Artifacts | Output | Purpose |
|-------|-----------------|--------|---------|
| ps-synthesizer | All Tier 1 & 2 outputs | `docs/synthesis/unified-architecture-canon.md` | Create authoritative pattern reference |

**Execution**: Sequential (requires all research complete)

### Tier 4: Gap Analysis & Alignment (After Tier 3)

**Goal**: Identify gaps between design and current implementation.

| Agent | Input | Output | Purpose |
|-------|-------|--------|---------|
| ps-analyst | Synthesis + current code | `docs/analysis/implementation-gap-analysis.md` | Identify what exists vs. what's designed |

### Tier 5: Implementation ADR (After Tier 4)

**Goal**: Create authoritative Architecture Decision Record for implementation alignment.

| Agent | Input | Output | Purpose |
|-------|-------|--------|---------|
| ps-architect | Gap analysis + synthesis | `docs/decisions/ADR-IMPL-001-unified-alignment.md` | Establish implementation roadmap |

### Tier 6: Validation & Status (After Tier 5)

| Agent | Input | Output | Purpose |
|-------|-------|--------|---------|
| ps-validator | ADR + current code | `docs/analysis/alignment-validation.md` | Verify path forward is sound |
| ps-reporter | All artifacts | `docs/reports/proj-001-status-report.md` | Executive summary of foundation |

---

## Execution Timeline

```
Phase 1: Research (Parallel)
├── T1.1: ps-researcher → WORKTRACKER_PROPOSAL.md
├── T1.2: ps-researcher → projects/archive/PLAN.md
├── T1.3: ps-researcher → REVISED-ARCHITECTURE-v3.0.md
└── T1.4: ps-researcher → glimmering-brewing-lake-v3.md

Phase 2: Synthesis (Sequential)
└── T2.1: ps-synthesizer → unified-architecture-canon.md

Phase 3: Analysis (Sequential)
└── T3.1: ps-analyst → implementation-gap-analysis.md

Phase 4: Architecture Decision (Sequential)
└── T4.1: ps-architect → ADR-IMPL-001-unified-alignment.md

Phase 5: Validation & Reporting (Parallel)
├── T5.1: ps-validator → alignment-validation.md
└── T5.2: ps-reporter → proj-001-status-report.md
```

**Estimated Agent Invocations**: 8 total
**Estimated Artifacts**: 8 persistent documents

---

## Alternative Approaches Considered

### Option A: Manual Sequential Read
- **Pros**: Full context in single session
- **Cons**: Context rot risk, no persistent artifacts

### Option B: Single ps-synthesizer Pass
- **Pros**: Fast, single artifact
- **Cons**: May miss nuances, no research trail

### Option C: Fan-Out All Documents at Once
- **Pros**: Maximum parallelism
- **Cons**: Overwhelming, hard to synthesize 82 documents

### Option D (Selected): Tiered Approach
- **Pros**:
  - Respects document evolution chain
  - Creates persistent research trail
  - Builds toward authoritative synthesis
  - Enables gap analysis against current state
- **Cons**:
  - More agent invocations
  - Longer total time

---

## Key Patterns to Extract

From the evolutionary documents, these patterns must be captured:

### From WORKTRACKER_PROPOSAL.md (Primary Synthesis)
- [ ] 32-week implementation phases
- [ ] BDD test specifications with RED/GREEN/REFACTOR
- [ ] Domain entities (Task, Phase, Plan aggregates)
- [ ] CQRS commands and queries
- [ ] Repository port definitions
- [ ] CloudEvents 1.0 event schema
- [ ] Architecture test patterns

### From projects/archive/PLAN.md (Graph Direction)
- [ ] Vertex/Edge base classes
- [ ] VertexId inheritance hierarchy
- [ ] EdgeLabels constants
- [ ] Graph traversal patterns (Gremlin-compatible)
- [ ] IGraphRepository port

### From REVISED-ARCHITECTURE-v3.0.md (Foundation)
- [ ] Event Sourcing with Snapshots
- [ ] CQRS pattern implementation
- [ ] Generic IRepository<T, TId>
- [ ] Unit of Work pattern
- [ ] Optimistic concurrency
- [ ] Projection builders

### From glimmering-brewing-lake-v3.md (Strategic)
- [ ] 5W1H analysis framework
- [ ] Bounded context definitions
- [ ] Wisdom capture approach
- [ ] ADO integration strategy

---

## Success Criteria

| Criterion | Measure |
|-----------|---------|
| All 4 evolutionary documents processed | 4/4 research artifacts exist |
| Unified synthesis created | `unified-architecture-canon.md` exists |
| Gap analysis complete | Implementation gaps documented |
| ADR created | `ADR-IMPL-001` approved |
| Validation passed | No blocking gaps identified |
| Status report delivered | Executive summary available |

---

## Next Steps

1. **User Approval**: Review this action plan
2. **Execute Tier 1**: Launch 4 parallel ps-researcher agents
3. **Execute Tiers 2-6**: Sequential synthesis and analysis
4. **Review Artifacts**: User validates extracted patterns
5. **Proceed to Implementation**: Use artifacts as implementation guide

---

## Appendix: PS Context Convention

For all agent invocations, use:

```
PS ID: PROJ-001
Entry ID: e-{sequence}
Topic: {specific topic}
```

Example:
```
PS ID: PROJ-001
Entry ID: e-001
Topic: WORKTRACKER_PROPOSAL Architecture Extraction
```

---

*Action Plan Version: 1.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Last Updated: 2026-01-09*
