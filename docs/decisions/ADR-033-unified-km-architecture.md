# ADR-033: Unified Knowledge Management Architecture

## Status
PROPOSED

## Date
2026-01-09

## Context
Jerry requires a unified Knowledge Management architecture that merges:
- WORK-031: Hybrid Property + RDF Architecture (semantic web standards)
- WORK-032: Lightweight KM Stack (NetworkX + FAISS + RDFLib)

The integration analysis (WORK-033 Step 1) found 95% compatibility between these approaches.

## Decision
We will adopt **Phased Implementation** of the Unified KM Architecture.

This approach scored 4.6/5 (92%) in the trade-off analysis, winning across all sensitivity scenarios:
- Beats Minimal (3.2/5, 64%) by 44%
- Beats Full (2.6/5, 52%) by 77%

### Core Components
1. **KnowledgeItem** - Aggregate root for PAT/LES/ASM
2. **Three Ports** - IKnowledgeRepository, ISemanticIndex, IGraphStore
3. **Six Use Cases** - 3 commands, 3 queries (CQRS)
4. **Four Events** - CloudEvents 1.0 compliant

### Technology Stack
- NetworkX 3.2.1 (graph operations)
- FAISS 1.7.4 (vector search)
- RDFLib 7.0.0 (semantic web)

## Consequences

### Positive
- 186% ROI over 5 years
- Minimal regret - can accelerate or decelerate
- 2-year runway before migration needed
- Hexagonal architecture preserved

### Negative
- Learning curve for KM concepts
- Additional dependencies (3 libraries)
- Ongoing maintenance (~40 hrs/year)

### Neutral
- Phase gates require governance overhead
- Success metrics need quarterly review

## Implementation

### Phase 2: Foundation (8 weeks, 70-90 hours)
- Week 1-2: Ports + JSON-LD serialization
- Week 3-4: AAR templates + file adapter
- Week 5-6: NetworkX graph store
- Week 7-8: Basic FAISS integration
- **Gate**: 3+ knowledge items captured, query latency <100ms

### Phase 3: Advanced (12 weeks, conditional)
- Triggered by: >100 knowledge items OR user request
- GraphRAG integration
- SPARQL query support
- Monitoring dashboard

### Phase 4: Scale (triggered by metrics)
- Triggered by: >10M entities OR multi-tenant OR >500ms latency
- Graph database migration
- Distributed vector store

## Compliance

### Jerry Constitution
- P-030: Knowledge items stored as files (filesystem as truth)
- P-031: All KM operations auditable
- P-032: Graceful degradation if adapters unavailable

### Hexagonal Architecture
- Domain layer: Pure Python, no external deps
- Ports: Interfaces in domain layer
- Adapters: Infrastructure layer implementations

## References
- work-033-e-001-integration-analysis.md (95% compatibility)
- work-033-e-002-unified-design.md (domain model)
- work-033-e-003-design-trade-offs.md (Phased wins 92%)
- ADR-031 (Hybrid Property + RDF)
- ADR-032 (Lightweight KM Stack)
