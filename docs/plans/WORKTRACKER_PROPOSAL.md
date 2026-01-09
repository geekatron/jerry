# Jerry Framework - Implementation Work Tracker (Proposed)

> Granular implementation plan derived from ADR-034 unified design.
> **Source**: [ADR-034](../decisions/ADR-034-unified-wt-km-implementation.md) | [Unified Design](../design/work-034-e-003-unified-design.md)

**Created**: 2026-01-09
**Status**: PROPOSED (awaiting approval)
**Total Duration**: 32 weeks (4 phases)
**Branch**: TBD (implementation branch)

---

## Quick Status

| Phase | Status | Progress |
|-------|--------|----------|
| Phase 1: Work Tracker Foundation | ⏳ PENDING | 0% |
| Phase 2: Shared Infrastructure | ⏳ PENDING | 0% |
| Phase 3: KM Integration | ⏳ PENDING | 0% |
| Phase 4: Advanced Features | ⏳ PENDING | 0% |

---

## Implementation Work Items

| Work Item | Status | Artifacts | Duration | Dependencies |
|-----------|--------|-----------|----------|--------------|
| WORK-101 | ⏳ PENDING | Domain entities, VOs, events | Weeks 1-2 | None |
| WORK-102 | ⏳ PENDING | Repository ports & adapters | Weeks 3-4 | WORK-101 |
| WORK-103 | ⏳ PENDING | CQRS commands & queries | Weeks 5-6 | WORK-101, WORK-102 |
| WORK-104 | ⏳ PENDING | CLI interface, BDD tests | Weeks 7-8 | WORK-103 |
| WORK-201 | ⏳ PENDING | Event store port & adapter | Weeks 9-10 | Phase 1 |
| WORK-202 | ⏳ PENDING | Graph store (NetworkX) | Weeks 11-12 | WORK-201 |
| WORK-203 | ⏳ PENDING | Semantic index (FAISS) | Weeks 13-14 | WORK-202 |
| WORK-204 | ⏳ PENDING | RDF serializer (RDFLib) | Weeks 15-16 | WORK-202, WORK-203 |
| WORK-301 | ⏳ PENDING | KM domain entities | Weeks 17-18 | Phase 2 |
| WORK-302 | ⏳ PENDING | KM repository layer | Weeks 19-20 | WORK-301 |
| WORK-303 | ⏳ PENDING | KM CQRS & AAR handlers | Weeks 21-22 | WORK-301, WORK-302 |
| WORK-304 | ⏳ PENDING | KM CLI & SKILL.md | Weeks 23-24 | WORK-303 |
| WORK-401 | ⏳ PENDING | Cross-domain handlers | Weeks 25-26 | Phase 3 |
| WORK-402 | ⏳ PENDING | HybridRAG & pattern discovery | Weeks 27-28 | WORK-401 |
| WORK-403 | ⏳ PENDING | SPARQL endpoint & export | Weeks 29-30 | WORK-401 |
| WORK-404 | ⏳ PENDING | Documentation & final tests | Weeks 31-32 | All |

---

## Phase 1: Work Tracker Foundation (Weeks 1-8)

> **Goal**: Establish Work Tracker domain with full CQRS, proving hexagonal architecture patterns.
> **Reference**: [Unified Design §11 Phase 1](../design/work-034-e-003-unified-design.md#phase-1-work-tracker-foundation-weeks-1-8)

### WORK-101: Domain Layer - Shared Kernel & Work Tracker Entities ⏳
- **Status**: PENDING
- **Duration**: Weeks 1-2
- **Dependencies**: None
- **Acceptance**: All BDD scenarios in [§10.1](../design/work-034-e-003-unified-design.md#101-task-aggregate) pass
- **Sub-tasks**:
  - [ ] 101.1: Shared Kernel Value Objects
    - [ ] `src/domain/value_objects/vertex_id.py` - Base VertexId class
    - [ ] `src/domain/value_objects/ids.py` - TaskId, PhaseId, PlanId, KnowledgeId
    - [ ] `src/domain/value_objects/jerry_uri.py` - Jerry URI parser
    - [ ] `src/domain/value_objects/priority.py` - Priority enum
    - [ ] `src/domain/value_objects/status.py` - TaskStatus, PhaseStatus, PlanStatus
    - [ ] `src/domain/value_objects/tag.py` - Tag value object
    - [ ] Unit tests for all value objects
  - [ ] 101.2: Task Aggregate Root
    - [ ] RED: Write failing tests for Task creation
    - [ ] GREEN: Implement `src/domain/aggregates/task.py`
    - [ ] Implement create(), transition_to(), complete(), assign_to_phase()
    - [ ] BDD scenarios for task lifecycle
  - [ ] 101.3: Phase Aggregate Root
    - [ ] RED: Write failing tests for Phase
    - [ ] GREEN: Implement `src/domain/aggregates/phase.py`
    - [ ] Implement add_task(), remove_task(), complete()
    - [ ] BDD scenarios for phase lifecycle
  - [ ] 101.4: Plan Aggregate Root
    - [ ] RED: Write failing tests for Plan
    - [ ] GREEN: Implement `src/domain/aggregates/plan.py`
    - [ ] Implement add_phase(), reorder_phases(), track_assumption()
  - [ ] 101.5: Domain Events
    - [ ] `src/domain/events/base.py` - CloudEventEnvelope
    - [ ] `src/domain/events/work_tracker.py` - TaskCreated, TaskCompleted, PhaseCompleted, etc.
    - [ ] CloudEvents 1.0 compliance tests

### WORK-102: Repository Layer - Ports & SQLite Adapters ⏳
- **Status**: PENDING
- **Duration**: Weeks 3-4
- **Dependencies**: WORK-101
- **Acceptance**: CRUD operations work for all aggregates
- **Sub-tasks**:
  - [ ] 102.1: Repository Port Definition
    - [ ] `src/domain/ports/work_item_repository.py` - IWorkItemRepository interface
    - [ ] Task CRUD: get_task, save_task, delete_task, list_tasks
    - [ ] Phase CRUD: get_phase, save_phase, delete_phase, list_phases
    - [ ] Plan CRUD: get_plan, save_plan, delete_plan, list_plans
    - [ ] `src/domain/exceptions.py` - DomainError, NotFoundError, ConcurrencyError
  - [ ] 102.2: SQLite Repository Adapter
    - [ ] `src/infrastructure/persistence/sqlite_work_item_repo.py`
    - [ ] Task table schema & CRUD
    - [ ] Phase table schema & CRUD
    - [ ] Plan table schema & CRUD
    - [ ] Optimistic concurrency (version column)
    - [ ] `migrations/001_work_tracker_schema.sql`
    - [ ] Integration tests
  - [ ] 102.3: Unit of Work Pattern
    - [ ] `src/domain/ports/unit_of_work.py` - IUnitOfWork interface
    - [ ] `src/infrastructure/persistence/sqlite_unit_of_work.py`
    - [ ] Transaction rollback tests

### WORK-103: CQRS Implementation - Commands & Queries ⏳
- **Status**: PENDING
- **Duration**: Weeks 5-6
- **Dependencies**: WORK-101, WORK-102
- **Acceptance**: Commands emit events, queries return DTOs
- **Reference**: [Unified Design §6.1-6.2](../design/work-034-e-003-unified-design.md#61-work-tracker-commands)
- **Sub-tasks**:
  - [ ] 103.1: Command Definitions
    - [ ] CreateTaskCommand, UpdateTaskCommand, TransitionTaskCommand
    - [ ] CompleteTaskCommand, AssignTaskToPhaseCommand
    - [ ] CreatePhaseCommand, CompletePhaseCommand
    - [ ] CreatePlanCommand, ActivatePlanCommand, CompletePlanCommand
  - [ ] 103.2: Command Handlers
    - [ ] `src/application/handlers/commands/work_tracker/`
    - [ ] Handler for each command type
    - [ ] Unit tests for handlers
  - [ ] 103.3: Query Definitions & Handlers
    - [ ] GetTaskQuery, ListTasksQuery, GetPhaseQuery, ListPhasesQuery
    - [ ] GetPlanQuery, ListPlansQuery, GetTaskHistoryQuery
    - [ ] `src/application/dtos/work_tracker.py` - TaskDTO, PhaseDTO, PlanDTO
    - [ ] Query handlers
  - [ ] 103.4: Event Dispatcher
    - [ ] `src/domain/ports/event_dispatcher.py` - IEventDispatcher
    - [ ] `src/infrastructure/messaging/in_memory_dispatcher.py`
    - [ ] Dispatcher tests

### WORK-104: CLI Interface & BDD Tests ⏳
- **Status**: PENDING
- **Duration**: Weeks 7-8
- **Dependencies**: WORK-103
- **Acceptance**: Full CRUD via CLI, 100% BDD scenario coverage
- **Sub-tasks**:
  - [ ] 104.1: CLI Adapter
    - [ ] `src/interface/cli/work_tracker_cli.py` - Main entry point
    - [ ] `task` subcommand (create, list, show, update, complete, delete)
    - [ ] `phase` subcommand (create, list, show, complete)
    - [ ] `plan` subcommand (create, list, show, activate, complete)
    - [ ] `scripts/wt.py` - CLI shim
  - [ ] 104.2: Work Tracker SKILL.md
    - [ ] `skills/work-tracker/SKILL.md` - Natural language interface
    - [ ] Command examples and patterns
  - [ ] 104.3: BDD Test Suite
    - [ ] `tests/bdd/work_tracker/features/task.feature`
    - [ ] `tests/bdd/work_tracker/features/phase.feature`
    - [ ] `tests/bdd/work_tracker/features/plan.feature`
    - [ ] Step definitions
  - [ ] 104.4: **Phase 1 Go/No-Go Gate**
    - [ ] All unit tests pass (target: 95%+ coverage)
    - [ ] All BDD scenarios pass
    - [ ] CLI operations < 100ms p95
    - [ ] Code review approved

---

## Phase 2: Shared Infrastructure (Weeks 9-16)

> **Goal**: Build shared infrastructure components (Event Store, Graph, Search, RDF).
> **Reference**: [Unified Design §11 Phase 2](../design/work-034-e-003-unified-design.md#phase-2-shared-infrastructure-weeks-9-16)

### WORK-201: Event Store Implementation ⏳
- **Status**: PENDING
- **Duration**: Weeks 9-10
- **Dependencies**: Phase 1 complete
- **Acceptance**: CloudEvents 1.0 compliant, append-only semantics
- **Reference**: [Unified Design §5.5](../design/work-034-e-003-unified-design.md#55-ieventstore)
- **Sub-tasks**:
  - [ ] 201.1: Event Store Port
    - [ ] `src/domain/ports/event_store.py` - IEventStore interface
    - [ ] append(), get(), get_by_subject(), get_by_type(), replay()
    - [ ] Snapshot support (get_snapshot, save_snapshot)
  - [ ] 201.2: SQLite Event Store Adapter
    - [ ] `src/infrastructure/event_store/sqlite_event_store.py`
    - [ ] Events table (append-only)
    - [ ] Snapshots table
    - [ ] Indexes for subject, type, time queries
    - [ ] `migrations/002_event_store_schema.sql`
    - [ ] Integration tests, replay scenario tests

### WORK-202: Graph Store Implementation ⏳
- **Status**: PENDING
- **Duration**: Weeks 11-12
- **Dependencies**: WORK-201
- **Acceptance**: Traversal operations, persistence to disk
- **Reference**: [Unified Design §5.3](../design/work-034-e-003-unified-design.md#53-igraphstore)
- **Sub-tasks**:
  - [ ] 202.1: Graph Store Port
    - [ ] `src/domain/ports/graph_store.py` - IGraphStore interface
    - [ ] Vertex operations: add_vertex, get_vertex, update_vertex, remove_vertex
    - [ ] Edge operations: add_edge, get_edges, remove_edge
    - [ ] Traversal: traverse, traverse_incoming, shortest_path
    - [ ] `src/domain/value_objects/graph.py` - Vertex, Edge VOs
  - [ ] 202.2: NetworkX Graph Adapter
    - [ ] `src/infrastructure/graph/networkx_graph_store.py`
    - [ ] DiGraph initialization
    - [ ] Vertex & Edge CRUD
    - [ ] BFS traversal, shortest_path
    - [ ] gpickle persistence
    - [ ] Unit & integration tests
  - [ ] 202.3: Performance Baseline
    - [ ] Benchmark: Add 500 vertices, 2-hop traversal, save/load
    - [ ] Document baseline metrics

### WORK-203: Semantic Index Implementation ⏳
- **Status**: PENDING
- **Duration**: Weeks 13-14
- **Dependencies**: WORK-202
- **Acceptance**: kNN search functional, persistence to disk
- **Reference**: [Unified Design §5.4](../design/work-034-e-003-unified-design.md#54-isemanticindex)
- **Sub-tasks**:
  - [ ] 203.1: Semantic Index Port
    - [ ] `src/domain/ports/semantic_index.py` - ISemanticIndex interface
    - [ ] add, update, remove operations
    - [ ] search, search_by_text operations
    - [ ] save, load, rebuild operations
    - [ ] `src/domain/value_objects/search_result.py` - SearchResult VO
  - [ ] 203.2: FAISS Semantic Index Adapter
    - [ ] `src/infrastructure/search/faiss_semantic_index.py`
    - [ ] IndexFlatL2 initialization
    - [ ] ID-to-index mapping
    - [ ] kNN search implementation
    - [ ] Index persistence (faiss.write_index)
    - [ ] `src/infrastructure/search/embedding_provider.py`
    - [ ] Unit & integration tests
  - [ ] 203.3: Performance Baseline
    - [ ] Benchmark: Add 1000 embeddings, kNN search (k=10), save/load
    - [ ] Document baseline metrics

### WORK-204: RDF Serialization Implementation ⏳
- **Status**: PENDING
- **Duration**: Weeks 15-16
- **Dependencies**: WORK-202, WORK-203
- **Acceptance**: Export to Turtle/JSON-LD, SPARQL queries
- **Reference**: [Unified Design §5.6](../design/work-034-e-003-unified-design.md#56-irdfserializer)
- **Sub-tasks**:
  - [ ] 204.1: RDF Serializer Port
    - [ ] `src/domain/ports/rdf_serializer.py` - IRDFSerializer interface
    - [ ] add_triple, add_entity
    - [ ] serialize (turtle, xml, json-ld, n3)
    - [ ] save, load, query (SPARQL)
  - [ ] 204.2: RDFLib Serializer Adapter
    - [ ] `src/infrastructure/rdf/rdflib_serializer.py`
    - [ ] Graph initialization with namespaces
    - [ ] Multi-format serialization
    - [ ] SPARQL query execution
    - [ ] `src/infrastructure/rdf/jerry_ontology.py`
    - [ ] Unit & integration tests
  - [ ] 204.3: **Phase 2 Go/No-Go Gate**
    - [ ] All infrastructure adapters implement ports
    - [ ] Performance baselines documented
    - [ ] Integration tests pass
    - [ ] Work Tracker entities stored in graph
    - [ ] Code review approved

---

## Phase 3: Knowledge Management Integration (Weeks 17-24)

> **Goal**: Implement KM domain entities and integrate with Work Tracker.
> **Reference**: [Unified Design §11 Phase 3](../design/work-034-e-003-unified-design.md#phase-3-knowledge-management-integration-weeks-17-24)

### WORK-301: KM Domain Layer ⏳
- **Status**: PENDING
- **Duration**: Weeks 17-18
- **Dependencies**: Phase 2 complete
- **Acceptance**: Pattern, Lesson, Assumption entities with BDD scenarios
- **Reference**: [Unified Design §4.3](../design/work-034-e-003-unified-design.md#43-knowledge-management-domain)
- **Sub-tasks**:
  - [ ] 301.1: KM Value Objects
    - [ ] `src/domain/value_objects/knowledge/knowledge_type.py` - KnowledgeType enum
    - [ ] `src/domain/value_objects/knowledge/evidence.py` - Evidence VO
    - [ ] `src/domain/value_objects/knowledge/evidence_type.py` - EvidenceType enum
    - [ ] Unit tests
  - [ ] 301.2: KnowledgeItem Aggregate
    - [ ] `src/domain/aggregates/knowledge_item.py` - Base aggregate
    - [ ] `src/domain/aggregates/pattern.py` - Pattern subtype
    - [ ] `src/domain/aggregates/lesson.py` - Lesson subtype
    - [ ] `src/domain/aggregates/assumption.py` - Assumption subtype
    - [ ] BDD scenarios for KM lifecycle
  - [ ] 301.3: KM Domain Events
    - [ ] PatternCreated, PatternUpdated, LessonCreated, LessonMaterialized
    - [ ] AssumptionCreated, AssumptionValidated, EvidenceAdded, KnowledgeLinked

### WORK-302: KM Repository Layer ⏳
- **Status**: PENDING
- **Duration**: Weeks 19-20
- **Dependencies**: WORK-301
- **Acceptance**: Full CRUD for knowledge items
- **Reference**: [Unified Design §5.2](../design/work-034-e-003-unified-design.md#52-iknowledgerepository)
- **Sub-tasks**:
  - [ ] 302.1: Knowledge Repository Port
    - [ ] `src/domain/ports/knowledge_repository.py` - IKnowledgeRepository
    - [ ] get, save, delete, list_by_type, list_by_tags, get_by_source
  - [ ] 302.2: SQLite Knowledge Repository
    - [ ] `src/infrastructure/persistence/sqlite_knowledge_repo.py`
    - [ ] Knowledge items table, Evidence table (1:N), Tags table (M:N)
    - [ ] `migrations/003_knowledge_schema.sql`
    - [ ] Integration tests

### WORK-303: KM CQRS Implementation ⏳
- **Status**: PENDING
- **Duration**: Weeks 21-22
- **Dependencies**: WORK-301, WORK-302
- **Acceptance**: All commands/queries functional, AAR handler working
- **Reference**: [Unified Design §6.3-6.4](../design/work-034-e-003-unified-design.md#63-knowledge-management-commands)
- **Sub-tasks**:
  - [ ] 303.1: KM Commands
    - [ ] CreatePatternCommand, CreateLessonCommand, CreateAssumptionCommand
    - [ ] ValidateAssumptionCommand, AddEvidenceCommand, LinkKnowledgeCommand, ApplyPatternCommand
  - [ ] 303.2: KM Command Handlers
    - [ ] `src/application/handlers/commands/km/` - All handlers
    - [ ] Unit tests
  - [ ] 303.3: KM Queries
    - [ ] GetKnowledgeQuery, ListPatternsQuery, ListLessonsQuery, ListAssumptionsQuery
    - [ ] SearchKnowledgeQuery (semantic), GetRelatedKnowledgeQuery (graph)
    - [ ] `src/application/dtos/knowledge.py` - KM DTOs
  - [ ] 303.4: AAR Event Handler
    - [ ] `src/application/event_handlers/km/aar_prompt_handler.py`
    - [ ] `src/application/event_handlers/km/materialize_lesson_handler.py`
    - [ ] `src/domain/value_objects/aar_response.py` - AARResponse VO
    - [ ] AAR flow integration tests

### WORK-304: KM Interface Layer ⏳
- **Status**: PENDING
- **Duration**: Weeks 23-24
- **Dependencies**: WORK-303
- **Acceptance**: Full KM operations via CLI and SKILL
- **Sub-tasks**:
  - [ ] 304.1: KM CLI Adapter
    - [ ] `src/interface/cli/km_cli.py` - KM CLI entry point
    - [ ] `pattern` subcommand, `lesson` subcommand, `assumption` subcommand
    - [ ] `search` command (semantic), `related` command (graph)
    - [ ] `scripts/km.py` - CLI shim
  - [ ] 304.2: KM SKILL.md
    - [ ] `skills/km/SKILL.md` - Natural language interface
    - [ ] Pattern, Lesson, Assumption operations
  - [ ] 304.3: Cross-Domain BDD Tests
    - [ ] `tests/bdd/cross_domain/features/task_to_lesson.feature`
    - [ ] `tests/bdd/cross_domain/features/pattern_application.feature`
    - [ ] `tests/bdd/cross_domain/features/assumption_validation.feature`
  - [ ] 304.4: **Phase 3 Go/No-Go Gate**
    - [ ] KM entity CRUD working
    - [ ] AAR prompt flow functional
    - [ ] Semantic search returning results
    - [ ] Graph traversal working
    - [ ] Cross-domain BDD scenarios pass
    - [ ] Code review approved

---

## Phase 4: Advanced Features (Weeks 25-32)

> **Goal**: Complete cross-domain integration, HybridRAG, and external APIs.
> **Reference**: [Unified Design §11 Phase 4](../design/work-034-e-003-unified-design.md#phase-4-advanced-features-weeks-25-32)

### WORK-401: Cross-Domain Integration ⏳
- **Status**: PENDING
- **Duration**: Weeks 25-26
- **Dependencies**: Phase 3 complete
- **Acceptance**: Task→Lesson, Phase→Pattern flows automated
- **Reference**: [Unified Design §4.4](../design/work-034-e-003-unified-design.md#44-cross-domain-integration)
- **Sub-tasks**:
  - [ ] 401.1: Cross-Domain Event Handlers
    - [ ] `src/application/event_handlers/cross_domain/task_completed_handler.py`
    - [ ] `src/application/event_handlers/cross_domain/phase_completed_handler.py`
    - [ ] `src/application/event_handlers/cross_domain/pattern_applied_handler.py`
    - [ ] `src/application/event_handlers/cross_domain/assumption_validation_handler.py`
    - [ ] Integration tests
  - [ ] 401.2: Knowledge Materializer Service
    - [ ] `src/application/services/knowledge_materializer.py`
    - [ ] materialize_lesson, materialize_pattern
    - [ ] Graph edge creation
  - [ ] 401.3: Graph Enrichment
    - [ ] Add WT entities to graph on create
    - [ ] Update graph on status changes
    - [ ] Enriched queries with graph context

### WORK-402: HybridRAG & Pattern Discovery ⏳
- **Status**: PENDING
- **Duration**: Weeks 27-28
- **Dependencies**: WORK-401
- **Acceptance**: Semantic + graph retrieval, pattern candidates surfaced
- **Sub-tasks**:
  - [ ] 402.1: HybridRAG Service
    - [ ] `src/application/services/hybrid_rag.py`
    - [ ] Semantic search + graph context enrichment
    - [ ] Result fusion and ranking
    - [ ] `src/application/queries/hybrid_search.py`
    - [ ] Integration tests
  - [ ] 402.2: Pattern Discovery Service
    - [ ] `src/application/services/pattern_discovery.py`
    - [ ] Lesson clustering, candidate identification
    - [ ] Confidence scoring
    - [ ] `src/domain/value_objects/pattern_candidate.py`
    - [ ] Unit tests

### WORK-403: External API & Export ⏳
- **Status**: PENDING
- **Duration**: Weeks 29-30
- **Dependencies**: WORK-401
- **Acceptance**: SPARQL endpoint functional, RDF export working
- **Sub-tasks**:
  - [ ] 403.1: SPARQL Endpoint
    - [ ] `src/interface/api/sparql_endpoint.py`
    - [ ] Query validation, result formatting
    - [ ] Endpoint tests
  - [ ] 403.2: Export/Import Commands
    - [ ] `src/application/commands/export.py`, `import.py`
    - [ ] RDF export/import handlers
    - [ ] `src/interface/cli/export_cli.py`

### WORK-404: Documentation & Final Testing ⏳
- **Status**: PENDING
- **Duration**: Weeks 31-32
- **Dependencies**: All
- **Acceptance**: Full documentation, all tests pass, system validated
- **Sub-tasks**:
  - [ ] 404.1: Integration Test Suite
    - [ ] `tests/integration/test_full_workflow.py`
    - [ ] `tests/integration/test_performance.py`
    - [ ] `tests/integration/test_data_integrity.py`
  - [ ] 404.2: User Documentation
    - [ ] `docs/user-guide/getting-started.md`
    - [ ] `docs/user-guide/work-tracker.md`
    - [ ] `docs/user-guide/knowledge-management.md`
    - [ ] `docs/user-guide/cli-reference.md`
  - [ ] 404.3: Developer Documentation
    - [ ] `docs/dev-guide/architecture.md`
    - [ ] `docs/dev-guide/extending.md`
    - [ ] `docs/dev-guide/testing.md`
  - [ ] 404.4: **Final Go/No-Go Gate**
    - [ ] All unit tests pass (target: 95%+ coverage)
    - [ ] All BDD scenarios pass
    - [ ] All integration tests pass
    - [ ] Performance targets met (<100ms p95)
    - [ ] Documentation complete
    - [ ] Security review passed
    - [ ] Final code review approved

---

## Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Runtime | Python | 3.11+ | Zero-dependency core |
| Graph | NetworkX | 3.2.1 | Property graph |
| Vector Search | FAISS | 1.7.4 | Semantic similarity |
| RDF | RDFLib | 7.0.0 | Knowledge export |
| Persistence | SQLite | 3.x | Entity and event storage |
| Testing | pytest | 8.x | BDD scenarios |

---

## Key Decisions (From ADR-034)

| Decision | Score | Choice | Alternative |
|----------|-------|--------|-------------|
| Architecture | 8.4/10 | Hexagonal | Layered (7.0) |
| Sequence | 8.65/10 | WT First | KM First (6.05) |
| Graph DB | 8.5/10 | NetworkX | Neo4j (7.05) |
| Vector Search | 8.1/10 | FAISS | Pinecone (7.25) |
| Database | 9.0/10 | SQLite | PostgreSQL (6.35) |

---

## Risk Register Summary

| ID | Risk | Probability | Impact | Mitigation |
|----|------|-------------|--------|------------|
| R-001 | Performance at scale | Medium | High | Validate at WT scale first |
| R-002 | Supernode formation | Medium | High | Edge count validator |
| R-004 | User AAR adoption | Medium | Medium | Track completion rate |
| R-005 | Schema evolution | Medium | High | Version envelope pattern |

---

## References

| Document | Size | Purpose |
|----------|------|---------|
| [ADR-034](../decisions/ADR-034-unified-wt-km-implementation.md) | 59KB | Architecture decision |
| [Unified Design](../design/work-034-e-003-unified-design.md) | 87KB | Technical specifications |
| [Trade-off Analysis](../analysis/work-034-e-004-tradeoff-analysis.md) | 39KB | Decision rationale |
| [Domain Synthesis](../synthesis/work-034-e-002-domain-synthesis.md) | 54KB | Domain model |
| [Domain Analysis](../research/work-034-e-001-domain-analysis.md) | 93KB | Research foundation |
| [Validation Report](../validation/work-034-e-006-validation-report.md) | 17KB | Approval status |

---

*Generated from WORK-034 artifacts on 2026-01-09*
