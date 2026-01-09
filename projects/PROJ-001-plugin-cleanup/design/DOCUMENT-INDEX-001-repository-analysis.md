# Document Index: Jerry Framework Repository Analysis

> **Document ID**: DOCUMENT-INDEX-001
> **Date**: 2026-01-09
> **Author**: Claude (Session cc/task-subtask)
> **Purpose**: Systematic catalog of all design artifacts with importance weighting
> **Method**: Parallel agent analysis of 82 documents across 6 categories

---

## Executive Summary

This index catalogs 82 design documents discovered in the Jerry Framework repository.
Analysis reveals a mature, well-documented architecture with clear patterns and decisions.

**Key Finding**: The repository contains a sophisticated, cohesive design system with:
- Unified identity patterns (JerryId, JerryUri, VertexId)
- Hexagonal Architecture with CQRS + Event Sourcing
- Three-layer knowledge architecture (Filesystem → Graph → Semantic)
- 32-week phased implementation plan
- ~1,250 planned tests across all phases

---

## Document Importance Weighting

### Weight Criteria

| Weight | Meaning | Criteria |
|--------|---------|----------|
| **P0** | Critical Foundation | Must read to understand system identity, architecture |
| **P1** | Core Architecture | Defines bounded contexts, domain models, patterns |
| **P2** | Implementation Detail | Phase-specific plans, technical specifications |
| **P3** | Supporting Material | Templates, examples, historical context |

---

## P0: Critical Foundation Documents (Must Read First)

These documents establish the identity and architectural foundation. Read in order.

| # | Document | Location | Purpose | Key Content |
|---|----------|----------|---------|-------------|
| 1 | **JERRY_URI_SPECIFICATION.md** | `docs/specifications/` | Identity standard | Jerry URI scheme (`jer:partition:tenant:domain:resource`), JerryUri value object, CloudEvents integration |
| 2 | **PS_EXPORT_DOMAIN_ALIGNMENT.md** | `projects/archive/proposals/` | Entity patterns | IAuditable, IVersioned, EntityBase, JerryId, Edge types |
| 3 | **work-034-e-003-unified-design.md** | `projects/archive/design/` | Architecture integration | Shared Kernel (VertexId, JerryUri, CloudEvents), Work Tracker + KM integration, 32-week roadmap |
| 4 | **glimmering-brewing-lake-v3.md** | `docs/knowledge/dragonsbelurkin/` | Complete strategic plan | 5W1H analysis, bounded contexts, ADO integration, gap analysis, wisdom capture |
| 5 | **DISCOVERIES_EXPANDED.md** | `docs/knowledge/` | Research synthesis | 53 discoveries (L0/L1/L2), context rot research, architectural decisions |

### P0 Document Dependency Chain

```
JERRY_URI_SPECIFICATION.md (Identity Layer)
    ↓ (referenced by)
PS_EXPORT_DOMAIN_ALIGNMENT.md (Entity Patterns)
    ↓ (unified by)
work-034-e-003-unified-design.md (Architecture Integration)
    ↓ (implemented in)
glimmering-brewing-lake-v3.md (Strategic Plan)
    ↓ (validated by)
DISCOVERIES_EXPANDED.md (Research Validation)
```

---

## P1: Core Architecture Documents

### Domain Model & Patterns

| Document | Location | Purpose | Weight |
|----------|----------|---------|--------|
| **work_tracker_architecture_hexagonal_ddd_cqrs_layered_teaching_edition.md** | `docs/knowledge/exemplars/architecture/` | Hexagonal + DDD + CQRS reference | P1 |
| **REVISED-ARCHITECTURE-v3.0.md** | `docs/knowledge/dragonsbelurkin/history/` | Event Sourcing + CQRS foundation | P1 |
| **work-033-e-002-unified-design.md** | `projects/archive/design/` | Knowledge Management architecture | P1 |
| **canonical-structure.md** | `docs/knowledge/exemplars/patterns/` | Directory structure, naming conventions | P1 |

### Behavioral Rules & SOPs

| Document | Location | Purpose | Weight |
|----------|----------|---------|--------|
| **hard-rules.md** | `docs/knowledge/exemplars/rules/` | Non-negotiable gates (3-tier enforcement) | P1 |
| **sop.md** | `docs/knowledge/exemplars/rules/` | Standard Operating Procedures | P1 |
| **problem_solving_meta_framework.md** | `docs/knowledge/exemplars/frameworks/problemsolving/` | Universal problem-solving loop | P1 |
| **domain_specific_playbooks.md** | `docs/knowledge/exemplars/architecture/` | Domain-specific approaches (NASA, Google SRE, NIST) | P1 |

### Specifications & Templates

| Document | Location | Purpose | Weight |
|----------|----------|---------|--------|
| **PS-EXPORT-SPECIFICATION.md** | `docs/knowledge/exemplars/templates/` | Problem Statement export format v2.1 | P1 |

---

## P2: Implementation Detail Documents

### Work Tracker Implementation Plans

| Document | Location | Purpose | Phase |
|----------|----------|---------|-------|
| **WORK_TRACKER_PLAN.md** | `projects/archive/plans/` | Main hexagonal core plan | All |
| **00-wt-index.md** | `projects/archive/plans/worktracker/` | 32-week implementation index | All |
| **01-wt-foundation.md** | `projects/archive/plans/worktracker/` | Phase 1: Task + SubTask vertical slice | Weeks 1-8 |
| **02-wt-infrastructure.md** | `projects/archive/plans/worktracker/` | Phase 2: Event Store, Graph, FAISS, RDF | Weeks 9-16 |
| **03-wt-km-integration.md** | `projects/archive/plans/worktracker/` | Phase 3: Knowledge Management | Weeks 17-24 |
| **04-wt-advanced-features.md** | `projects/archive/plans/worktracker/` | Phase 4: HybridRAG, Patterns, API | Weeks 25-32 |

### Research Series (WORK-031 to WORK-034)

| Series | Topic | Key Documents | Recommendation |
|--------|-------|---------------|----------------|
| **WORK-031** | Semantic Architecture | e-001 to e-005 | JSON-LD, HybridRAG, pyoxigraph |
| **WORK-032** | Knowledge Management | e-001 to e-005 | NetworkX + RDFLib + FAISS |
| **WORK-033** | Integration Analysis | e-001 to e-003 | Unified 4-phase roadmap |
| **WORK-034** | Domain Analysis | e-001 to e-004 | Work Tracker as proving ground |

### Trade-off Analyses

| Document | Location | Purpose |
|----------|----------|---------|
| **work-031-e-007-trade-off-analysis.md** | `projects/archive/analysis/` | Semantic architecture trade-offs |
| **work-032-e-007-trade-off-analysis.md** | `projects/archive/analysis/` | KM implementation trade-offs |
| **work-033-e-003-design-trade-offs.md** | `projects/archive/analysis/` | Integration trade-offs |
| **work-034-e-004-tradeoff-analysis.md** | `projects/archive/analysis/` | Domain model trade-offs |

---

## P3: Supporting Material

### Templates

| Document | Location | Purpose |
|----------|----------|---------|
| **adr.md** | `docs/knowledge/exemplars/templates/` | ADR template |
| **analysis.md** | `docs/knowledge/exemplars/templates/` | Analysis template |
| **research.md** | `docs/knowledge/exemplars/templates/` | Research template |
| **synthesis.md** | `docs/knowledge/exemplars/templates/` | Synthesis template |
| **investigation.md** | `docs/knowledge/exemplars/templates/` | Investigation template |
| **review.md** | `docs/knowledge/exemplars/templates/` | Review template |
| **deep-analysis.md** | `docs/knowledge/exemplars/templates/` | Deep analysis template |
| **use-case-template.md** | `docs/knowledge/exemplars/templates/` | Use case template |
| **jrn.md** | `docs/knowledge/exemplars/templates/` | Journal template |

### Historical / Superseded

| Document | Location | Status |
|----------|----------|--------|
| **glimmering-brewing-lake.md** (v1) | `docs/knowledge/dragonsbelurkin/` | Superseded by v3 |
| **glimmering-brewing-lake-v2.md** | `docs/knowledge/dragonsbelurkin/` | Superseded by v3 |
| **WORKTRACKER_PROPOSAL.md** | `projects/archive/plans/` | Evolved into WORK_TRACKER_PLAN |
| **AGENT_REORGANIZATION_PLAN.md** | `projects/archive/plans/` | Historical context |

### Aspirations (Future Work)

| Document | Location | Purpose |
|----------|----------|---------|
| **blackboard-agent-orchestration-design.md** | `docs/knowledge/dragonsbelurkin/aspirations/blackboard/` | Future agent orchestration |
| **self-healing-architecture.md** | `docs/knowledge/dragonsbelurkin/aspirations/self-healing/` | Future self-healing hooks |
| **phase-38.17-*.md** (series) | `docs/knowledge/dragonsbelurkin/aspirations/blackboard/` | Blackboard architecture exploration |

---

## Key Architectural Patterns Extracted

### Identity Patterns

| Pattern | Source | Description |
|---------|--------|-------------|
| **JerryUri** | SPEC-001 | `jer:partition:tenant:domain:resource[+version]` |
| **JerryId** | PROP-001 | Strongly-typed with prefix/sequence/uuid |
| **VertexId** | work-034 | Abstract base for graph-ready IDs |
| **Type-Specific IDs** | PROP-001 | TaskId, PhaseId, PlanId, KnowledgeId |

### Entity Patterns

| Pattern | Source | Properties |
|---------|--------|------------|
| **IAuditable** | PROP-001 | created_on, updated_on, created_by, updated_by |
| **IVersioned** | PROP-001 | content_hash, hash_algorithm, version |
| **EntityBase** | PROP-001 | id, uri, slug, name, descriptions, audit, version, graph, extensibility |
| **Edge Types** | PROP-001 | CONTAINS, HAS_SUBTASK, BLOCKS, DEPENDS_ON, etc. |

### Architectural Patterns

| Pattern | Source | Description |
|---------|--------|-------------|
| **Hexagonal** | work_tracker_architecture | Ports & Adapters, domain isolation |
| **CQRS** | REVISED-ARCHITECTURE-v3.0 | Command/Query separation |
| **Event Sourcing** | REVISED-ARCHITECTURE-v3.0 | Append-only events, projections |
| **Shared Kernel** | work-034 | VertexId, JerryUri, CloudEvents |

### Technology Stack

| Layer | Technology | Source |
|-------|------------|--------|
| **Graph** | NetworkX 3.2.1 | WORK-031, WORK-032 |
| **Vector Search** | FAISS 1.7.4 | WORK-031 |
| **RDF** | RDFLib 7.0.0 | WORK-031 |
| **Persistence** | SQLite + JSON/TOON | work_tracker_architecture |
| **Testing** | pytest + pytest-bdd | WORK_TRACKER_PLAN |

---

## Recommended Reading Order

### For Full Context (Comprehensive)

```
Day 1: Identity & Entity Foundation
  1. JERRY_URI_SPECIFICATION.md (30 min)
  2. PS_EXPORT_DOMAIN_ALIGNMENT.md (45 min)

Day 2: Architecture Integration
  3. work-034-e-003-unified-design.md (60 min)
  4. REVISED-ARCHITECTURE-v3.0.md (45 min)

Day 3: Strategic Plan & Discoveries
  5. glimmering-brewing-lake-v3.md (90 min)
  6. DISCOVERIES_EXPANDED.md (30 min)

Day 4: Rules & Patterns
  7. hard-rules.md (20 min)
  8. sop.md (30 min)
  9. work_tracker_architecture_hexagonal_ddd_cqrs_layered_teaching_edition.md (45 min)

Day 5: Implementation Plans
  10. 00-wt-index.md through 04-wt-advanced-features.md (90 min)
```

### For Quick Alignment (Minimal)

```
1. JERRY_URI_SPECIFICATION.md - Identity patterns
2. PS_EXPORT_DOMAIN_ALIGNMENT.md - Entity patterns
3. work-034-e-003-unified-design.md - Architecture
4. DISCOVERIES_EXPANDED.md - Research synthesis
5. hard-rules.md - Behavioral gates
```

---

## Document Statistics

| Category | Count | Status |
|----------|-------|--------|
| **Specifications** | 1 | Active |
| **Proposals** | 1 | Approved |
| **Unified Designs** | 2 | Complete |
| **Strategic Plans** | 3 (v1, v2, v3) | v3 Active |
| **Implementation Plans** | 7 | Proposed |
| **Research Documents** | 21 | Archived |
| **Analysis Documents** | 4 | Archived |
| **Templates** | 11 | Active |
| **Rules/SOPs** | 4 | Active |
| **Aspirations** | 14 | Future |
| **Current Project ADRs** | 4 | Active |

**Total: 82 documents**

---

## Cross-Document Dependency Map

```
                    ┌─────────────────────────────────────────┐
                    │         JERRY_URI_SPECIFICATION         │
                    │              (SPEC-001)                 │
                    │         Identity Foundation             │
                    └──────────────────┬──────────────────────┘
                                       │
                    ┌──────────────────▼──────────────────────┐
                    │      PS_EXPORT_DOMAIN_ALIGNMENT         │
                    │              (PROP-001)                 │
                    │   IAuditable, IVersioned, EntityBase    │
                    └──────────────────┬──────────────────────┘
                                       │
           ┌───────────────────────────┼───────────────────────────┐
           │                           │                           │
           ▼                           ▼                           ▼
┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│  work-033-e-002     │   │  work-034-e-003     │   │  REVISED-ARCH-v3.0  │
│ (KM Unified Design) │   │ (Integration Design)│   │ (Event Sourcing)    │
└─────────┬───────────┘   └─────────┬───────────┘   └─────────┬───────────┘
          │                         │                         │
          └─────────────────────────┼─────────────────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │   glimmering-brewing-lake-v3  │
                    │     (Strategic Plan - FINAL)  │
                    └───────────────┬───────────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼                         ▼                         ▼
┌─────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│ WORK_TRACKER_   │   │ 00-wt-index.md      │   │ DISCOVERIES_        │
│ PLAN.md         │   │ (Implementation)    │   │ EXPANDED.md         │
└─────────────────┘   └─────────────────────┘   └─────────────────────┘
```

---

## Gaps & Observations

### Implemented vs. Planned

| Component | Status | Gap |
|-----------|--------|-----|
| **JerryUri** | Specified | Not yet implemented in code |
| **EntityBase** | Specified | Not yet implemented in code |
| **IAuditable** | Specified | Not yet implemented in code |
| **Shared Kernel** | Designed | `src/shared_kernel/` does not exist |
| **Work Tracker Domain** | Partial | `session_management` exists but not aligned |

### Observations

1. **Documentation is Ahead of Implementation**: Sophisticated design exists but code lags
2. **Clear Evolution Path**: v1 → v2 → v3 progression shows iterative refinement
3. **Research is Thorough**: 21 research documents with citations and trade-offs
4. **Patterns are Consistent**: Same patterns (Hexagonal, CQRS, Event Sourcing) across all designs
5. **Integration Points Defined**: Clear Shared Kernel specification

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-09 | Initial document index from parallel agent analysis |
