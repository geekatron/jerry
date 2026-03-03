# Phase 4: Advanced Features (Weeks 25-32)

> **Goal**: Implement HybridRAG, pattern discovery, external API, and final documentation.
> **Reference**: [Index](00-wt-index.md) | [Unified Design](../../design/work-034-e-003-unified-design.md)

**Status**: PENDING
**Duration**: Weeks 25-32
**WORK Items**: WORK-401 to WORK-404
**Dependencies**: Phase 3 complete

---

## Phase 4 Overview

| WORK Item | Name | Duration | Dependencies |
|-----------|------|----------|--------------|
| WORK-401 | Cross-Domain Integration | Weeks 25-26 | Phase 3 |
| WORK-402 | HybridRAG & Pattern Discovery | Weeks 27-28 | WORK-401 |
| WORK-403 | External API & Export | Weeks 29-30 | WORK-401 |
| WORK-404 | Documentation & Final Testing | Weeks 31-32 | All |

---

## WORK-401: Cross-Domain Integration

**Status**: PENDING
**Duration**: Weeks 25-26
**Artifacts**: Unified graph service, enriched queries, sagas
**Dependencies**: Phase 3

### Sub-task 401.1: Unified Graph Service

**Files**: `src/application/services/unified_graph_service.py`
**Tests**: `tests/integration/application/test_unified_graph.py`

- [ ] `UnifiedGraphService`
  - [ ] `get_task_with_knowledge(task_id)` → Task + related patterns/lessons
  - [ ] `get_pattern_with_tasks(pattern_id)` → Pattern + source tasks
  - [ ] `traverse_cross_domain(start_id, depth)` → Mixed WT + KM results
  - [ ] `path_between_domains(wt_id, km_id)` → Connection path

- [ ] Graph materialization
  - [ ] `materialize_task_knowledge_links()`
  - [ ] Incremental updates on event
  - [ ] Full rebuild option

### Sub-task 401.2: Enriched Query Handlers

**Files**: `src/application/handlers/queries/enriched/`
**Tests**: `tests/unit/application/handlers/queries/test_enriched_queries.py`

- [ ] `GetTaskWithKnowledgeQuery` → TaskDTO + patterns/lessons
- [ ] `GetKnowledgeWithContextQuery` → KnowledgeDTO + source tasks + usage
- [ ] `GetDashboardQuery` → Summary view

### Sub-task 401.3: Event Saga Implementation

**Files**: `src/application/sagas/`
**Tests**: `tests/integration/application/test_sagas.py`

- [ ] `SagaCoordinator`
  - [ ] Execute multi-step operations
  - [ ] Compensation on failure
  - [ ] Idempotent steps
  - [ ] Timeout handling

- [ ] `TaskCompletionSaga`
  - [ ] Complete task → Update graph → Trigger AAR → Create knowledge

- [ ] `PatternDiscoverySaga`
  - [ ] Detect pattern → Validate → Create item → Link sources

### Sub-task 401.4: Cross-Domain Performance

**Files**: `tests/integration/cross_domain/`

- [ ] Cross-domain query < 150ms p95
- [ ] Saga completion < 500ms
- [ ] Graph traversal 3 hops < 100ms
- [ ] Stress tests (100 concurrent queries)

---

## WORK-402: HybridRAG & Pattern Discovery

**Status**: PENDING
**Duration**: Weeks 27-28
**Artifacts**: HybridRAG service, pattern discovery, CLI
**Dependencies**: WORK-401

### Sub-task 402.1: HybridRAG Service

**Files**: `src/application/services/hybrid_rag.py`
**Tests**: `tests/integration/application/test_hybrid_rag.py`

- [ ] `HybridRAGService`
  - [ ] `retrieve(query, k)` → Combined semantic + graph results
  - [ ] Configurable weights (semantic vs graph)
  - [ ] Duplicate removal
  - [ ] Score combination

- [ ] Re-ranking
  - [ ] Relevance scoring
  - [ ] Diversity promotion
  - [ ] Recency boost

- [ ] Context assembly
  - [ ] Token budget management
  - [ ] Chunk selection
  - [ ] Priority ordering

- [ ] Query expansion
  - [ ] Synonym addition
  - [ ] Related term discovery

### Sub-task 402.2: Pattern Discovery Service

**Files**: `src/application/services/pattern_discovery.py`
**Tests**: `tests/integration/application/test_pattern_discovery.py`

- [ ] Similarity detection
  - [ ] `detect_similar_items(threshold)`
  - [ ] Cluster formation
  - [ ] Minimum cluster size

- [ ] Pattern candidate generation
  - [ ] Template extraction
  - [ ] Confidence scoring
  - [ ] Source tracking

- [ ] Pattern validation
  - [ ] Minimum evidence requirement
  - [ ] User confirmation flow
  - [ ] Rejection tracking

- [ ] Pattern evolution
  - [ ] Merge similar patterns
  - [ ] Split divergent patterns
  - [ ] Deprecation

### Sub-task 402.3: HybridRAG CLI

**Files**: `src/interface/cli/rag_cli.py`
**Tests**: `tests/e2e/cli/test_rag_cli.py`

- [ ] `rag search "query"`
- [ ] `rag context "query" --budget 2000`
- [ ] `--semantic-only` / `--graph-only` flags
- [ ] `pattern discover`
- [ ] `pattern candidates`
- [ ] `pattern approve <id>` / `pattern reject <id>`

### Sub-task 402.4: Quality Benchmarks

**Files**: `tests/integration/application/test_rag_benchmarks.py`

- [ ] Precision@k, Recall@k, MRR metrics
- [ ] Golden dataset
- [ ] Quality regression detection
- [ ] Performance: retrieval < 200ms, reranking < 50ms, assembly < 100ms

---

## WORK-403: External API & Export

**Status**: PENDING
**Duration**: Weeks 29-30
**Artifacts**: SPARQL endpoint, bulk export/import
**Dependencies**: WORK-401

### Sub-task 403.1: SPARQL Endpoint

**Files**: `src/interface/api/sparql_endpoint.py`
**Tests**: `tests/integration/api/test_sparql_endpoint.py`

- [ ] HTTP endpoint
  - [ ] POST /sparql with query body
  - [ ] GET /sparql with query param
  - [ ] Content negotiation
  - [ ] Rate limiting

- [ ] Query execution
  - [ ] SELECT → JSON/XML results
  - [ ] ASK → boolean
  - [ ] CONSTRUCT → RDF graph

- [ ] Security
  - [ ] Query whitelist
  - [ ] Depth limit
  - [ ] Result size limit
  - [ ] Audit logging

### Sub-task 403.2: Bulk Export/Import

**Files**: `src/application/commands/export/`, `src/application/commands/import/`
**Tests**: `tests/integration/application/test_bulk_export_import.py`

- [ ] Bulk export
  - [ ] Streaming output for large datasets
  - [ ] Format options (Turtle, JSON-LD, N-Triples)
  - [ ] Progress callback
  - [ ] Resume on failure

- [ ] Bulk import
  - [ ] Validation pass
  - [ ] Conflict resolution strategies
  - [ ] Transaction batching
  - [ ] Error reporting
  - [ ] Dry-run mode

- [ ] CLI integration
  - [ ] `export --format turtle --output data.ttl --all`
  - [ ] `import data.ttl --validate-only`
  - [ ] Progress bar

### Sub-task 403.3: API Contract Tests

**Files**: `tests/contract/api/`

- [ ] SPARQL endpoint response format
- [ ] Error codes
- [ ] Export format validation
- [ ] Round-trip preservation

---

## WORK-404: Documentation & Final Testing

**Status**: PENDING
**Duration**: Weeks 31-32
**Artifacts**: User docs, final tests, release
**Dependencies**: All previous WORK items

### Sub-task 404.1: User Documentation

**Files**: `docs/user-guide/`

- [ ] `getting-started.md`
  - [ ] Installation
  - [ ] First task
  - [ ] First knowledge item
  - [ ] AAR walkthrough

- [ ] `work-tracker.md`
  - [ ] Task lifecycle
  - [ ] Sub-task management
  - [ ] CLI reference
  - [ ] Best practices

- [ ] `knowledge-management.md`
  - [ ] Patterns, lessons, assumptions
  - [ ] Evidence and confidence
  - [ ] Linking knowledge
  - [ ] AAR workflow

- [ ] `advanced.md`
  - [ ] HybridRAG queries
  - [ ] SPARQL endpoint
  - [ ] Export/import
  - [ ] Pattern discovery

- [ ] `api/` reference
  - [ ] CLI commands
  - [ ] SPARQL reference
  - [ ] Export formats

### Sub-task 404.2: Final Integration Testing

**Files**: `tests/system/final/`

- [ ] Full workflow tests
  - [ ] Create plan → phases → tasks → complete → AAR → lessons → patterns → export

- [ ] Regression test suite
  - [ ] All Phase 1-4 gates re-verified
  - [ ] No performance degradation

- [ ] Load testing
  - [ ] 1000 concurrent users
  - [ ] 10,000 tasks
  - [ ] 5,000 knowledge items
  - [ ] Sustained load 1hr

- [ ] Security testing
  - [ ] Injection tests
  - [ ] Authorization tests
  - [ ] OWASP top 10 checks

### Sub-task 404.3: Release Preparation

- [ ] Final gate checklist
  - [ ] All 1200+ tests pass
  - [ ] Coverage > 90%
  - [ ] Performance targets met
  - [ ] Security review approved
  - [ ] Documentation reviewed

- [ ] Release artifacts
  - [ ] CHANGELOG.md
  - [ ] Version bump
  - [ ] Migration guide
  - [ ] Release notes

- [ ] Deployment preparation
  - [ ] CI/CD pipeline verified
  - [ ] Rollback procedure
  - [ ] Monitoring configured

---

## Estimated Test Counts

| Category | Count |
|----------|-------|
| Unit tests | ~100 |
| Integration tests | ~80 |
| Contract tests | ~20 |
| System tests | ~40 |
| Load tests | ~10 |
| Security tests | ~20 |
| **Total** | **~270** |

---

## Grand Total Test Counts (All Phases)

| Phase | Tests |
|-------|-------|
| Phase 1 | ~430 |
| Phase 2 | ~250 |
| Phase 3 | ~300 |
| Phase 4 | ~270 |
| **Total** | **~1,250** |

---

*Phase 4 plan created 2026-01-09*
