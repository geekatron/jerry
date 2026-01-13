# Research Artifact: WORKTRACKER_PROPOSAL.md Architecture Extraction

> **PS ID**: PROJ-001
> **Entry ID**: e-001
> **Date**: 2026-01-09
> **Source**: `projects/archive/plans/WORKTRACKER_PROPOSAL.md`
> **Researcher**: ps-researcher agent v2.0.0

---

## L0: Executive Summary

- **32-week phased implementation** spanning 4 phases: Work Tracker Foundation (Weeks 1-8), Shared Infrastructure (Weeks 9-16), KM Integration (Weeks 17-24), Advanced Features (Weeks 25-32)
- **Hexagonal Architecture** with CQRS and Event Sourcing as mandatory patterns, scoring 8.4/10 vs Layered Architecture at 7.0/10
- **Domain Model** comprises 3 Aggregate Roots (Task, Phase, Plan) plus Knowledge Management entities (Pattern, Lesson, Assumption) with CloudEvents 1.0 compliance
- **Technology stack**: Python 3.11+, NetworkX (graph), FAISS (semantic search), RDFLib (knowledge export), SQLite (persistence)
- **Test-first methodology**: BDD Red/Green/Refactor with ~845 estimated tests across 8 test types, targeting 95%+ coverage

---

## L1: Technical Pattern Descriptions

### 1. Architecture Patterns

#### 1.1 Hexagonal Architecture (Ports & Adapters)

**Source**: Lines 20-28, 454-591

The document mandates Hexagonal Architecture with **hard enforcement**:

| Pattern | Enforcement | Validation |
|---------|-------------|------------|
| DDD | Hard | Architecture tests verify bounded contexts |
| Hexagonal Architecture | Hard | No adapter imports in domain |
| Event Sourcing | Hard | Events immutable, append-only |
| CQRS | Hard | Commands return events, queries return DTOs |
| Repository Pattern | Hard | All data access via ports |
| Dispatcher Pattern | Hard | Events dispatched, not directly handled |
| Dependency Injection | Hard | No `new` in domain/application |

**Layer Dependencies** (Lines 437-453):
```
domain/ -> NO imports from application/, infrastructure/, interface/
domain/ -> ONLY stdlib imports allowed
Aggregates -> extend AggregateRoot base
Value Objects -> frozen dataclasses
```

#### 1.2 CQRS Implementation

**Source**: Lines 594-765

- **Commands**: Write operations returning domain events
- **Queries**: Read operations returning DTOs (never domain entities)
- **Separation**: Distinct command and query handlers

**Command Structure** (Lines 605-636):
```python
# Commands are immutable frozen dataclasses
CreateTaskCommand: title, description, priority
UpdateTaskCommand: task_id, optional fields
TransitionTaskCommand: task_id, target_status
CompleteTaskCommand: task_id, optional notes
AssignTaskToPhaseCommand: task_id, phase_id
```

**Handler Pattern** (Lines 638-690):
1. Handler creates entity via factory
2. Handler saves entity via repository
3. Handler dispatches domain event
4. Handler returns result (e.g., TaskId)
5. Rollback on dispatch failure

#### 1.3 Event Sourcing

**Source**: Lines 381-415, 927-1010

**CloudEvents 1.0 Envelope** (Lines 385-397):
```python
# CloudEventEnvelope structure
specversion: "1.0"
type: "jerry.task.created"
source: "jerry://worktracker"
id: UUID
time: ISO 8601
data: event payload
```

**Event Store Port** (Lines 939-951):
- `append(event)` - adds event to stream
- `get(event_id)` - returns single event
- `get_by_subject(subject_id)` - returns events for entity
- `get_by_type(event_type)` - returns events by type
- `replay(from_position)` - returns ordered events
- `get_snapshot(subject_id)` - returns latest snapshot
- `save_snapshot(snapshot)` - persists snapshot

**Immutability Guarantee**: Events table has NO UPDATE/DELETE triggers

#### 1.4 Repository Pattern

**Source**: Lines 456-591

**IWorkItemRepository Port** (Lines 469-479):
- `get_task(id)` -> Task | None
- `save_task(task)` -> None
- `delete_task(id)` -> bool
- `list_tasks(filters)` -> List[Task]

**Optimistic Concurrency** (Lines 554-563):
- Save increments version
- Stale version detection raises ConcurrencyError
- Error includes expected vs actual version

**Unit of Work Pattern** (Lines 480-490):
- `begin()` context manager
- `commit()` persists all changes
- `rollback()` reverts all changes
- Auto-commit on success, auto-rollback on exception

---

### 2. Domain Model

#### 2.1 Value Objects (Shared Kernel)

**Source**: Lines 108-190

**VertexId Base Class** (Lines 112-122):
- Graph-ready abstraction for all entity IDs
- UUID format validation
- Immutable (`@dataclass(frozen=True)`)
- Value equality (not identity)

**Domain-Specific IDs** (Lines 124-136):
```python
TaskId(VertexId)
PhaseId(VertexId)
PlanId(VertexId)
KnowledgeId(VertexId)
# Each ID type is distinct: TaskId != PhaseId
```

**JerryURI** (Lines 137-148):
```python
# Format: jerry://entity_type/id[/sub_entity/sub_id]
jerry://task/abc-123
jerry://plan/xyz/phase/001
```

**Priority Enum** (Lines 150-159):
- LOW, MEDIUM, HIGH, CRITICAL
- Ordering comparison: LOW < HIGH
- Case-insensitive parsing

**Status Enums** (Lines 161-171):
```python
TaskStatus: PENDING, IN_PROGRESS, BLOCKED, COMPLETED, CANCELLED
PhaseStatus: NOT_STARTED, ACTIVE, COMPLETED
PlanStatus: DRAFT, ACTIVE, COMPLETED, ARCHIVED
# Valid transitions defined, can_transition_to() method
```

**Tag Value Object** (Lines 173-183):
- Normalized to lowercase
- Whitespace trimmed
- Max length: 50 chars
- Validation regex for special characters

#### 2.2 Task Aggregate Root

**Source**: Lines 191-277

**Entity Core** (Lines 195-207):
- Auto-generated TaskId
- Starts in PENDING status
- Has created_at timestamp
- Has version=1 (optimistic concurrency)
- Title max: 200 chars

**State Transitions** (Lines 209-220):
```
PENDING -> IN_PROGRESS (valid)
IN_PROGRESS -> COMPLETED (valid)
IN_PROGRESS -> BLOCKED (valid)
BLOCKED -> IN_PROGRESS (valid)
PENDING -> CANCELLED (valid)
COMPLETED -> IN_PROGRESS (INVALID)
CANCELLED -> any (INVALID)
```

**Completion** (Lines 222-233):
- Sets status=COMPLETED
- Sets completed_at timestamp
- Emits TaskCompleted event
- Requires IN_PROGRESS status

**Invariants** (Lines 258-266):
- BLOCKED status must have blocker_reason
- Due_date in past raises ValidationError on create
- Completed task has completed_at <= updated_at

#### 2.3 Phase Aggregate Root

**Source**: Lines 278-327

**Entity Core** (Lines 282-294):
- Auto-generated PhaseId
- Starts in NOT_STARTED status
- Has order_index for sequencing
- Empty task_ids set initially

**Task Management** (Lines 296-306):
- `add_task()` adds TaskId to set, emits TaskAddedToPhase
- `remove_task()` removes TaskId, emits TaskRemovedFromPhase
- Cannot add task to COMPLETED phase

**Completion Logic** (Lines 308-318):
- Requires ACTIVE status
- Requires all tasks completed (or validates via callback)
- `complete(force=True)` completes regardless of tasks

#### 2.4 Plan Aggregate Root

**Source**: Lines 329-379

**Entity Core** (Lines 332-344):
- Auto-generated PlanId
- Starts in DRAFT status
- Empty phases list initially
- Empty assumptions set
- Name max: 100 chars

**Phase Management** (Lines 346-356):
- `add_phase()` with order, emits PhaseAddedToPlan
- `reorder_phases()` updates order_index values
- Cannot add phase to COMPLETED plan
- Cannot remove last phase (PlanRequiresPhase)

**Assumption Tracking** (Lines 358-368):
- `track_assumption()` adds assumption text
- `validate_assumption()` marks as validated/invalidated
- Duplicate assumption text is no-op

#### 2.5 Domain Events (Work Tracker)

**Source**: Lines 399-409

```python
# Task Events
TaskCreated(task_id, title, created_at)
TaskUpdated(task_id, fields_changed)
TaskTransitioned(task_id, from_status, to_status)
TaskCompleted(task_id, completed_at)
TaskAssignedToPhase(task_id, phase_id)
TaskRemovedFromPhase(task_id, phase_id)

# Phase Events
PhaseCreated(phase_id, name, plan_id)
PhaseActivated(phase_id)
PhaseCompleted(phase_id)

# Plan Events
PlanCreated(plan_id, name)
PlanActivated(plan_id)
PlanCompleted(plan_id)
PlanArchived(plan_id)
```

#### 2.6 Domain Exceptions

**Source**: Lines 417-433

```python
DomainError                    # Base class
NotFoundError                  # entity_type, entity_id
InvalidStateError              # current_state, attempted_action
InvalidStateTransition         # from_state, to_state
InvariantViolation            # invariant_name, details
ConcurrencyError              # expected_version, actual_version
ValidationError               # field_name, message
```

---

### 3. Knowledge Management Domain

#### 3.1 KM Value Objects

**Source**: Lines 1309-1341

**KnowledgeType Enum**: PATTERN, LESSON, ASSUMPTION

**Evidence Value Object**:
- Type: OBSERVATION, OUTCOME, REFERENCE, METRIC
- Fields: source, content, timestamp
- Immutable

**Confidence Value Object**:
- Score: 0.0-1.0
- Justification text
- Levels: HIGH, MEDIUM, LOW

#### 3.2 KnowledgeItem Aggregate

**Source**: Lines 1343-1411

**Base Entity**:
- id, title, description
- knowledge_type
- tags set
- source_uri (optional)
- created_at, updated_at
- `add_evidence()`, `link_to()`

**Pattern Entity** (Lines 1360-1371):
- Extends KnowledgeItem
- Fields: context, problem, solution, consequences
- applicability_conditions
- application_count
- `apply()` increments count, emits PatternApplied

**Lesson Entity** (Lines 1373-1384):
- Extends KnowledgeItem
- Fields: observation, reflection, action
- source_task_id (optional)
- `materialize()` converts to Pattern

**Assumption Entity** (Lines 1386-1396):
- Extends KnowledgeItem
- Fields: hypothesis, validation_criteria
- Status: UNTESTED, VALIDATED, INVALIDATED
- `validate()` / `invalidate()` with evidence

#### 3.3 KM Domain Events

**Source**: Lines 1397-1411

```python
PatternCreated, PatternUpdated, PatternApplied
LessonCreated, LessonUpdated, LessonMaterialized
AssumptionCreated, AssumptionValidated, AssumptionInvalidated
EvidenceAdded, KnowledgeLinked
```

---

### 4. Infrastructure Components

#### 4.1 Graph Store (NetworkX)

**Source**: Lines 1013-1105

**IGraphStore Port** (Lines 1025-1038):
- `add_vertex(vertex)` - adds node
- `get_vertex(id)` - returns vertex
- `update_vertex(vertex)` - updates properties
- `remove_vertex(id)` - removes node and edges
- `add_edge(source, target, relation)` - directed edge
- `get_edges(vertex_id, direction)` - incoming/outgoing/both
- `traverse(start, depth, direction)` - returns subgraph
- `shortest_path(start, end)` - returns path

**Graph Value Objects** (Lines 1041-1048):
- Vertex: id, type, properties
- Edge: source_id, target_id, relation, properties

**Persistence** (Lines 1086-1096):
- Save/load with gpickle
- File locking for concurrency

#### 4.2 Semantic Index (FAISS)

**Source**: Lines 1107-1203

**ISemanticIndex Port** (Lines 1120-1134):
- `add(id, embedding)` - adds vector
- `update(id, embedding)` - updates vector
- `remove(id)` - removes vector
- `search(query_embedding, k)` - k nearest neighbors
- `search_by_text(text, k)` - embeds and searches
- `save(path)` / `load(path)` - persistence
- `rebuild()` - rebuilds index

**SearchResult Value Object**: id, score, metadata

#### 4.3 RDF Serializer (RDFLib)

**Source**: Lines 1207-1280

**IRDFSerializer Port** (Lines 1220-1230):
- `add_triple(s, p, o)` - adds RDF triple
- `add_entity(entity)` - converts to triples
- `serialize(format)` - turtle, xml, json-ld, n3
- `save(path, format)` / `load(path)`
- `query(sparql)` - executes SPARQL query

**Jerry Ontology** (Lines 1273-1280):
- Jerry namespace
- Classes: Task, Phase, Plan, KnowledgeItem, Pattern, Lesson
- Relationships: hasTask, belongsToPhase, etc.

---

### 5. Implementation Structure

#### 5.1 Directory Structure

**Source**: Lines 110, 193, 456, etc.

```
src/
  domain/
    value_objects/
      vertex_id.py
      ids.py               # TaskId, PhaseId, PlanId, KnowledgeId
      jerry_uri.py
      priority.py
      status.py
      tag.py
      graph.py             # Vertex, Edge
      search_result.py
      knowledge/           # KnowledgeType, Evidence, Confidence
    aggregates/
      task.py
      phase.py
      plan.py
      knowledge/
        knowledge_item.py
        pattern.py
        lesson.py
        assumption.py
    events/
      base.py              # CloudEventEnvelope
      work_tracker.py
      knowledge.py
    ports/
      work_item_repository.py
      unit_of_work.py
      event_store.py
      event_dispatcher.py
      graph_store.py
      semantic_index.py
      rdf_serializer.py
      knowledge_repository.py
    exceptions.py

  application/
    commands/
      work_tracker/        # Task, Phase, Plan commands
      km/                  # Pattern, Lesson, Assumption commands
      export.py
      import.py
    queries/
      work_tracker/
      km/
      hybrid_search.py
    handlers/
      commands/
        work_tracker/
        km/
      queries/
        work_tracker/
        km/
    event_handlers/
      km/
        aar_prompt_handler.py
        materialize_lesson_handler.py
      cross_domain/
    services/
      knowledge_materializer.py
      pattern_discovery.py
      hybrid_rag.py
    dtos/
      work_tracker.py
      knowledge.py

  infrastructure/
    persistence/
      sqlite_unit_of_work.py
      sqlite_task_repo.py
      sqlite_phase_repo.py
      sqlite_plan_repo.py
      sqlite_knowledge_repo.py
    event_store/
      sqlite_event_store.py
    graph/
      networkx_graph_store.py
    search/
      faiss_semantic_index.py
      embedding_provider.py
    rdf/
      rdflib_serializer.py
      jerry_ontology.py
    messaging/
      in_memory_dispatcher.py

  interface/
    cli/
      work_tracker_cli.py
      km_cli.py
      export_cli.py
    api/
      sparql_endpoint.py

migrations/
  001_work_tracker_schema.sql
  002_event_store_schema.sql
  003_knowledge_schema.sql

tests/
  unit/
  integration/
  contract/
  system/
  e2e/
  bdd/
  architecture/
  performance/

skills/
  work-tracker/SKILL.md
  km/SKILL.md
```

#### 5.2 32-Week Phased Implementation

**Source**: Lines 62-92

| Work Item | Duration | Dependencies | Key Deliverables |
|-----------|----------|--------------|------------------|
| WORK-101 | Weeks 1-2 | None | Domain entities, VOs, events |
| WORK-102 | Weeks 3-4 | WORK-101 | Repository ports & adapters |
| WORK-103 | Weeks 5-6 | 101, 102 | CQRS commands & queries |
| WORK-104 | Weeks 7-8 | WORK-103 | CLI interface, BDD tests |
| WORK-201 | Weeks 9-10 | Phase 1 | Event store port & adapter |
| WORK-202 | Weeks 11-12 | WORK-201 | Graph store (NetworkX) |
| WORK-203 | Weeks 13-14 | WORK-202 | Semantic index (FAISS) |
| WORK-204 | Weeks 15-16 | 202, 203 | RDF serializer (RDFLib) |
| WORK-301 | Weeks 17-18 | Phase 2 | KM domain entities |
| WORK-302 | Weeks 19-20 | WORK-301 | KM repository layer |
| WORK-303 | Weeks 21-22 | 301, 302 | KM CQRS & AAR handlers |
| WORK-304 | Weeks 23-24 | WORK-303 | KM CLI & SKILL.md |
| WORK-401 | Weeks 25-26 | Phase 3 | Cross-domain handlers |
| WORK-402 | Weeks 27-28 | WORK-401 | HybridRAG & pattern discovery |
| WORK-403 | Weeks 29-30 | WORK-401 | SPARQL endpoint & export |
| WORK-404 | Weeks 31-32 | All | Documentation & final tests |

---

### 6. Testing Strategy

#### 6.1 Test Pyramid

**Source**: Lines 30-38

| Level | Count | Focus | Real Data |
|-------|-------|-------|-----------|
| Unit | Many | Single class/function | Mocked dependencies |
| Integration | Medium | Multiple components | Real SQLite |
| Contract | Few | Port compliance | Interface verification |
| System | Few | Multi-operation workflows | Full stack |
| E2E | Few | CLI to persistence | Real everything |
| Architecture | Always | Layer dependencies | Static analysis |

#### 6.2 BDD Red/Green/Refactor Protocol

**Source**: Lines 41-48

```
1. RED: Write failing test with REAL assertions (no placeholders)
2. GREEN: Implement MINIMUM code to pass
3. REFACTOR: Clean up while maintaining GREEN
4. REPEAT: Until acceptance criteria met
```

#### 6.3 Test Coverage Requirements

**Source**: Lines 50-57

| Scenario Type | Coverage |
|--------------|----------|
| Happy path | 100% of use cases |
| Edge cases | Boundary conditions, empty/max values |
| Failure scenarios | NotFound, InvalidState, Concurrent |
| Negative tests | Invalid input, malformed data |

#### 6.4 Test Estimation

**Source**: Lines 2101-2114

| Test Type | Est. Count | Purpose |
|-----------|------------|---------|
| Unit | ~500 | Isolated component testing |
| Integration | ~150 | Multi-component testing |
| Contract | ~30 | Port compliance |
| System | ~20 | Multi-operation workflows |
| E2E | ~50 | CLI to persistence |
| BDD | ~60 | Business scenarios |
| Architecture | ~20 | Layer dependencies |
| Performance | ~15 | Baseline validation |
| **Total** | **~845** | |

---

### 7. Technology Stack

**Source**: Lines 2062-2073

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Runtime | Python | 3.11+ | Zero-dependency core |
| Graph | NetworkX | 3.2.1 | Property graph |
| Vector Search | FAISS | 1.7.4 | Semantic similarity |
| RDF | RDFLib | 7.0.0 | Knowledge export |
| Persistence | SQLite | 3.x | Entity and event storage |
| Testing | pytest | 8.x | All test types |
| BDD | pytest-bdd | 7.x | BDD scenarios |

---

### 8. Key Design Decisions

**Source**: Lines 2076-2085

| Decision | Score | Choice | Alternative |
|----------|-------|--------|-------------|
| Architecture | 8.4/10 | Hexagonal | Layered (7.0) |
| Sequence | 8.65/10 | WT First | KM First (6.05) |
| Graph DB | 8.5/10 | NetworkX | Neo4j (7.05) |
| Vector Search | 8.1/10 | FAISS | Pinecone (7.25) |
| Database | 9.0/10 | SQLite | PostgreSQL (6.35) |

---

### 9. Risk Register

**Source**: Lines 2087-2098

| ID | Risk | Probability | Impact | Mitigation |
|----|------|-------------|--------|------------|
| R-001 | Performance at scale | Medium | High | Validate at WT scale first |
| R-002 | Supernode formation | Medium | High | Edge count validator |
| R-003 | Test suite too slow | Medium | Medium | Parallel execution, test isolation |
| R-004 | User AAR adoption | Medium | Medium | Track completion rate |
| R-005 | Schema evolution | Medium | High | Version envelope pattern |
| R-006 | Integration complexity | Medium | Medium | Feature flags, incremental rollout |

---

## L2: Strategic Trade-offs and Implications

### Architecture Trade-offs

1. **Hexagonal over Layered** (8.4 vs 7.0):
   - **Pro**: Maximum testability, clear dependency direction
   - **Con**: More boilerplate (ports, adapters)
   - **Implication**: Higher initial effort, better long-term maintainability

2. **SQLite over PostgreSQL** (9.0 vs 6.35):
   - **Pro**: Zero deployment complexity, embedded, file-portable
   - **Con**: No concurrent writes, limited scale
   - **Implication**: Perfect for single-user workstation; needs migration path for multi-user

3. **NetworkX over Neo4j** (8.5 vs 7.05):
   - **Pro**: In-process, no server, Python-native
   - **Con**: Memory-bound, no native persistence format
   - **Implication**: Suitable for <10K vertices; migration to Neo4j for enterprise

4. **FAISS over Pinecone** (8.1 vs 7.25):
   - **Pro**: Local, no API costs, no latency
   - **Con**: Index size limited by RAM
   - **Implication**: Good for thousands of embeddings; cloud alternative for millions

### Implementation Implications

1. **Work Tracker First Sequence**:
   - Proves architecture patterns before KM complexity
   - Enables iterative validation of persistence layers
   - Delays KM features by 8 weeks but reduces integration risk

2. **CloudEvents 1.0 Compliance**:
   - Enables external system integration
   - Supports future event streaming (Kafka, etc.)
   - Adds serialization overhead

3. **BDD Red/Green/Refactor**:
   - Enforces test-first discipline
   - Catches design issues early
   - Slows initial velocity but improves quality

### Risk Implications

1. **R-001 (Performance)**: Phase 1 validates before Phase 3 investment
2. **R-002 (Supernodes)**: Graph traversal may hit hot spots; edge count limits needed
3. **R-005 (Schema Evolution)**: Version envelope in CloudEvents enables backward compatibility

---

## Cross-References

| Reference | Type | Location |
|-----------|------|----------|
| ADR-034 | Architecture Decision | `docs/decisions/ADR-034-unified-wt-km-implementation.md` |
| Unified Design | Technical Spec | `docs/design/work-034-e-003-unified-design.md` |
| Trade-off Analysis | Decision Rationale | `docs/analysis/work-034-e-004-tradeoff-analysis.md` |
| Domain Synthesis | Domain Model | `docs/synthesis/work-034-e-002-domain-synthesis.md` |
| Domain Analysis | Research | `docs/research/work-034-e-001-domain-analysis.md` |
| Validation Report | Approval | `docs/validation/work-034-e-006-validation-report.md` |

---

## Extracted Patterns Summary

### Design Patterns Used

1. **Aggregate Root** - Task, Phase, Plan, KnowledgeItem
2. **Value Object** - All IDs, JerryURI, Priority, Status, Tag, Evidence, Confidence
3. **Domain Event** - CloudEvents 1.0 wrapped events
4. **Repository** - Port interface with SQLite adapter
5. **Unit of Work** - Transaction management
6. **CQRS** - Command/Query separation
7. **Event Sourcing** - Append-only event store with snapshots
8. **Dispatcher** - Event distribution to handlers
9. **Factory** - Entity creation via static methods
10. **State Machine** - Status transitions

### Infrastructure Patterns

1. **Adapter Pattern** - All infrastructure implementations
2. **Port Pattern** - All domain contracts
3. **Snapshot Pattern** - Event store optimization
4. **Hybrid Search** - Semantic + Graph retrieval fusion

---

*Document generated by ps-researcher agent for PROJ-001*
