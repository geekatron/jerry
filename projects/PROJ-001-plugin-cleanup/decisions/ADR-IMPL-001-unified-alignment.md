# ADR-IMPL-001: Unified Implementation Alignment

> **Status**: PROPOSED
> **Date**: 2026-01-09
> **Deciders**: [To be filled by user]
> **Technical Story**: PROJ-001, Phase 7

---

## Context

The Jerry Framework has reached an inflection point. The [Unified Architecture Canon](../synthesis/PROJ-001-e-006-unified-architecture-canon.md) establishes authoritative patterns synthesized from five source documents, validated against industry best practices (Vernon, Evans, Fowler, Cockburn, CNCF CloudEvents). The [Implementation Gap Analysis](../analysis/PROJ-001-e-007-implementation-gap-analysis.md) reveals that only **15-20% of the canonical architecture** is currently implemented.

### Current State Summary

| Aspect | Status |
|--------|--------|
| Bounded Contexts Implemented | 1 of 4 (`session_management` only) |
| Shared Kernel | Non-existent |
| Event Sourcing Infrastructure | Non-existent |
| VertexId Hierarchy | Non-existent (`ProjectId` exists but misaligned) |
| AggregateRoot Base | Non-existent |
| Domain Model (Task, Phase, Plan) | Non-existent |
| Test Coverage | 0% |
| Hexagonal Compliance | Mostly compliant with minor issues |

### Critical Gaps (BLOCKING)

1. **GAP-001**: Shared Kernel Non-Existent - No foundation for cross-context types
2. **GAP-004**: Event Sourcing Infrastructure Missing - Core architecture pattern absent
3. **GAP-008**: Domain Model Missing - Primary value proposition unrealized

### Architectural Tension

The existing `session_management` bounded context was implemented with good hexagonal principles but without the foundational shared kernel. This creates a migration decision:

- **ProjectId** uses format `PROJ-{nnn}-{slug}` (hierarchical, human-readable)
- **Canon specifies** format `PLAN-{uuid8}` (graph-ready, consistent with VertexId hierarchy)

This tension exemplifies the broader decision: evolve existing code or build fresh on canon.

---

## Decision Drivers

* **DD-1**: Shared Kernel is prerequisite for ALL bounded contexts (GAP-001 blocks everything)
* **DD-2**: Event Sourcing is foundational, not optional - audit trail, CQRS, and replay depend on it
* **DD-3**: Current implementation is small (~15-20%), minimizing migration cost
* **DD-4**: Jerry Constitution P-002 requires file persistence for state (aligns with Event Sourcing)
* **DD-5**: Jerry Constitution P-003 prohibits recursive subagents (architecture must be simple)
* **DD-6**: Domain layer must remain stdlib-only (Python 3.11+)
* **DD-7**: Test-first approach is industry standard for Event Sourcing correctness

---

## Considered Options

### Option A: Greenfield Implementation

Build canon from scratch, deprecate existing `session_management` code.

**Pros:**
- Clean architecture from day one
- No migration complexity
- Canon patterns implemented consistently

**Cons:**
- Existing working code discarded
- Lose learnings embedded in current implementation
- Higher initial effort

### Option B: Incremental Migration

Evolve existing `session_management` to canon while building new bounded contexts on shared kernel.

**Pros:**
- Preserves working code
- Lower risk (gradual transition)
- Can deliver value incrementally

**Cons:**
- Two parallel implementation styles during transition
- `ProjectId` vs `PlanId` format mismatch requires careful handling
- Migration adds complexity to each phase

### Option C: Parallel Development (Recommended)

Build Shared Kernel and new bounded contexts (Work Management) on canon. Existing `session_management` code remains operational but isolated. Migrate it as final phase when core is stable.

**Pros:**
- Unblocks core domain implementation immediately
- Existing code continues to function
- Migration risk deferred until patterns proven
- Clear separation between "legacy" and "canon"

**Cons:**
- Two implementations coexist (acceptable short-term)
- Session management migration still required eventually

---

## Decision Outcome

**Chosen option: Option C (Parallel Development)**, because:

1. **Minimal disruption**: The existing `session_management` context (project scanning) works and is isolated. Breaking it gains nothing.

2. **Foundation first**: The Shared Kernel and Event Sourcing infrastructure are prerequisites for Work Management. Building them fresh avoids contamination from non-canonical patterns.

3. **Risk mitigation**: If canon patterns prove problematic during Work Management implementation, we can adjust before touching existing code.

4. **Clear migration path**: Once Task/Phase/Plan aggregates are working with Event Sourcing, we have a proven template for migrating `session_management`.

5. **15-20% is small**: The gap analysis confirms existing implementation is minimal. The migration cost is low enough that preserving it doesn't constrain future decisions.

### Migration Strategy for `session_management`

The existing bounded context will be migrated in Phase 9 (final phase) after the core architecture is proven. Migration involves:

1. **ProjectId -> PlanId**: Create adapter that maps `PROJ-{nnn}-{slug}` to `PLAN-{uuid8}` internally
2. **FilesystemProjectAdapter -> Event-Sourced Repository**: Convert read-only filesystem adapter to emit events for project discovery
3. **Queries -> Projections**: Convert existing queries to read from projections built from events

This migration is a **good validation** of the architecture's extensibility.

---

## Consequences

### Good

* **Clean foundation**: Shared Kernel provides consistent identity, auditing, and versioning across all future bounded contexts
* **Event Sourcing benefits**: Audit trail, time-travel debugging, CQRS optimization come "free"
* **Graph-ready**: VertexId hierarchy enables future migration to graph databases
* **Test coverage**: Building fresh allows TDD from the start
* **Canon compliance**: New code matches authoritative patterns 100%

### Bad

* **Coexistence complexity**: Two implementation styles exist until session_management is migrated
* **Initial velocity impact**: Building foundation delays domain feature delivery by ~5-7 days
* **Learning curve**: Team must internalize Event Sourcing patterns

### Neutral

* **ProjectId format preserved**: Existing project identifiers remain human-readable; PlanId uses UUID format internally
* **SQLite dependency**: Event Store and Snapshot Store use SQLite (stdlib), acceptable for single-agent deployment

---

## Implementation Roadmap

### Phase 1: Shared Kernel Foundation
**Priority**: P0 (Blocking)
**Estimated Duration**: 2-3 days
**Dependencies**: None
**Gap Addressed**: GAP-001, GAP-002, GAP-003

#### Deliverables
- [ ] Create `src/shared_kernel/` directory structure
- [ ] Implement `VertexId` base class with UUID validation (frozen dataclass)
- [ ] Implement type-specific IDs: `TaskId`, `PhaseId`, `PlanId`, `SubtaskId`, `KnowledgeId`, `ActorId`, `EventId`
- [ ] Implement `JerryUri` for cross-system identification
- [ ] Implement `EdgeId` for graph edges
- [ ] Implement `IAuditable` protocol
- [ ] Implement `IVersioned` protocol
- [ ] Implement `Vertex` and `Edge` base classes

#### Success Criteria
- [ ] All identity types pass format validation tests
- [ ] `VertexId` hierarchy enforces type safety (cannot mix TaskId with PhaseId)
- [ ] Zero external imports in shared kernel (stdlib only)
- [ ] 100% test coverage on identity value objects

#### Directory Structure
```
src/shared_kernel/
├── __init__.py
├── identity/
│   ├── __init__.py
│   ├── vertex_id.py      # Base class
│   ├── task_id.py
│   ├── phase_id.py
│   ├── plan_id.py
│   ├── subtask_id.py
│   ├── knowledge_id.py
│   ├── actor_id.py
│   ├── event_id.py
│   ├── edge_id.py
│   └── jerry_uri.py
├── entity/
│   ├── __init__.py
│   ├── auditable.py      # IAuditable protocol
│   ├── versioned.py      # IVersioned protocol
│   ├── vertex.py         # Vertex base class
│   └── edge.py           # Edge base class
└── exceptions.py         # SharedKernelError base
```

---

### Phase 2: Event Sourcing Infrastructure
**Priority**: P0 (Blocking)
**Estimated Duration**: 3-4 days
**Dependencies**: Phase 1
**Gap Addressed**: GAP-004

#### Deliverables
- [ ] Implement `DomainEvent` base class with CloudEvents 1.0 fields
- [ ] Implement `IEventStore` port with `append()`, `read()`, `get_version()`
- [ ] Implement `ISnapshotStore` port with configurable snapshot frequency
- [ ] Implement in-memory event store adapter (for testing)
- [ ] Implement SQLite event store adapter (for persistence)
- [ ] Implement SQLite snapshot store adapter
- [ ] Implement event serialization (JSON with CloudEvents envelope)
- [ ] Define event catalog types for Work Management context

#### Success Criteria
- [ ] Events are immutable (frozen dataclasses)
- [ ] Optimistic concurrency prevents lost updates (version mismatch raises `ConcurrencyError`)
- [ ] Event replay reconstructs aggregate state correctly
- [ ] Snapshots reduce replay time by >50% for streams with >10 events
- [ ] CloudEvents envelope validates against spec 1.0

#### Event Store Technology Decision

**Phase 2a (Immediate)**: In-memory adapter for unit testing
**Phase 2b (Persistence)**: SQLite adapter using Python stdlib `sqlite3`

SQLite is chosen because:
1. Zero external dependencies (stdlib)
2. Single-file database fits Jerry's single-agent deployment model
3. ACID compliance for event append
4. Sufficient performance for expected load (<1000 events/minute)

#### Directory Structure
```
src/shared_kernel/
├── events/
│   ├── __init__.py
│   ├── domain_event.py      # DomainEvent base class
│   ├── cloud_events.py      # CloudEvents 1.0 envelope utilities
│   └── serialization.py     # JSON serialization
├── ports/
│   ├── __init__.py
│   ├── event_store.py       # IEventStore port
│   └── snapshot_store.py    # ISnapshotStore port

src/infrastructure/
├── event_store/
│   ├── __init__.py
│   ├── in_memory.py         # InMemoryEventStore adapter
│   └── sqlite.py            # SqliteEventStore adapter
├── snapshot_store/
│   ├── __init__.py
│   └── sqlite.py            # SqliteSnapshotStore adapter
```

---

### Phase 3: Aggregate Foundation
**Priority**: P1
**Estimated Duration**: 2-3 days
**Dependencies**: Phase 1, Phase 2
**Gap Addressed**: GAP-003 (completion), GAP-006 (partial)

#### Deliverables
- [ ] Implement `AggregateRoot` base class with event sourcing support
- [ ] Implement `_raise_event(event)` method (adds to uncommitted, applies to state)
- [ ] Implement `_apply(event)` abstract method (state mutation)
- [ ] Implement `load_from_history(events)` class method (replay)
- [ ] Implement `get_uncommitted_events()` and `mark_events_committed()`
- [ ] Create generic `IRepository[TAggregate, TId]` interface
- [ ] Implement event-sourced repository base class

#### Success Criteria
- [ ] Aggregate state is ONLY mutated via events
- [ ] `load_from_history()` produces identical state as step-by-step mutations
- [ ] Repository `save()` appends uncommitted events to event store
- [ ] Repository `find_by_id()` replays events (with snapshot optimization)
- [ ] No direct property assignment on aggregates (enforced by design)

#### Directory Structure
```
src/shared_kernel/
├── entity/
│   └── aggregate_root.py    # AggregateRoot base class
├── ports/
│   └── repository.py        # IRepository[T, TId] generic interface

src/infrastructure/
├── persistence/
│   └── event_sourced_repository.py  # EventSourcedRepository base
```

---

### Phase 4: Work Management Bounded Context
**Priority**: P1
**Estimated Duration**: 5-7 days
**Dependencies**: Phase 3
**Gap Addressed**: GAP-008

#### Deliverables
- [ ] Create `src/work_management/` bounded context structure
- [ ] Implement `TaskStatus` enum with state machine validation
- [ ] Implement `Priority` enum (LOW, MEDIUM, HIGH, CRITICAL)
- [ ] Implement `Task` aggregate with all canonical invariants
- [ ] Implement `Phase` aggregate with TaskId references (by ID only)
- [ ] Implement `Plan` aggregate with PhaseId references (by ID only)
- [ ] Implement domain events: `TaskCreated`, `TaskTransitioned`, `TaskCompleted`, etc.
- [ ] Implement domain exceptions: `TaskNotFoundError`, `InvalidStateError`, `PlanRequiresPhaseError`
- [ ] Implement CQRS commands: `CreateTaskCommand`, `TransitionTaskCommand`, `AddTaskToPhaseCommand`
- [ ] Implement command handlers

#### Success Criteria
- [ ] Task state machine rejects invalid transitions (e.g., COMPLETED -> IN_PROGRESS)
- [ ] BLOCKED status requires `blocker_reason`
- [ ] Phase cannot add task when COMPLETED
- [ ] Plan cannot remove last phase (`PlanRequiresPhaseError`)
- [ ] All mutations emit domain events
- [ ] Command handlers validate and delegate to aggregates

#### State Machine Specification (Canon Reference)

**Task Status Transitions:**
```
PENDING -> IN_PROGRESS (StartTask)
IN_PROGRESS -> COMPLETED (CompleteTask)
IN_PROGRESS -> BLOCKED (BlockTask - requires reason)
BLOCKED -> IN_PROGRESS (UnblockTask)
PENDING -> CANCELLED (CancelTask)
COMPLETED -> any: INVALID
CANCELLED -> any: INVALID
```

#### Directory Structure
```
src/work_management/
├── __init__.py
├── domain/
│   ├── __init__.py
│   ├── aggregates/
│   │   ├── __init__.py
│   │   ├── task.py
│   │   ├── phase.py
│   │   └── plan.py
│   ├── value_objects/
│   │   ├── __init__.py
│   │   ├── task_status.py
│   │   └── priority.py
│   ├── events/
│   │   ├── __init__.py
│   │   ├── task_events.py
│   │   ├── phase_events.py
│   │   └── plan_events.py
│   └── exceptions.py
├── application/
│   ├── __init__.py
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── create_task.py
│   │   ├── transition_task.py
│   │   └── add_task_to_phase.py
│   ├── queries/
│   │   ├── __init__.py
│   │   └── get_task.py
│   └── handlers/
│       ├── __init__.py
│       ├── command_handlers.py
│       └── query_handlers.py
└── infrastructure/
    ├── __init__.py
    └── repositories/
        ├── __init__.py
        ├── task_repository.py
        ├── phase_repository.py
        └── plan_repository.py
```

---

### Phase 5: CQRS Completion
**Priority**: P2
**Estimated Duration**: 2-3 days
**Dependencies**: Phase 4
**Gap Addressed**: GAP-005

#### Deliverables
- [ ] Separate query handlers from query definitions (refactor existing pattern)
- [ ] Implement `IProjection` interface with `project(event)` and `reset()` methods
- [ ] Implement `TaskListProjection` (fast list queries)
- [ ] Implement `TaskDetailProjection` (single item retrieval)
- [ ] Implement `PhaseProgressProjection` (aggregated progress stats)
- [ ] Wire projections to event bus (subscribe to domain events)
- [ ] Implement projection rebuild from event store

#### Success Criteria
- [ ] Queries read ONLY from projections (not from event store/aggregates)
- [ ] Projections update within <100ms of event publication
- [ ] Projection rebuild produces identical state as incremental updates
- [ ] Query handlers return DTOs (never domain entities)

---

### Phase 6: Unit of Work & Transactions
**Priority**: P2
**Estimated Duration**: 2 days
**Dependencies**: Phase 3
**Gap Addressed**: GAP-006 (completion)

#### Deliverables
- [ ] Implement `IUnitOfWork` interface with context manager protocol
- [ ] Implement SQLite Unit of Work with transaction support
- [ ] Integrate UoW with command handlers
- [ ] Add rollback support for failed commands
- [ ] Implement event publishing within commit phase

#### Success Criteria
- [ ] Changes across multiple aggregates commit atomically
- [ ] Failed command rolls back all changes
- [ ] Events are published ONLY after successful commit
- [ ] Context manager `with uow:` syntax works correctly

---

### Phase 7: Graph Layer
**Priority**: P3
**Estimated Duration**: 3-4 days
**Dependencies**: Phase 1
**Gap Addressed**: GAP-007

#### Deliverables
- [ ] Implement `IGraphStore` port with standard operations (`add_vertex`, `get_vertex`, `add_edge`, `traverse`)
- [ ] Define edge label constants: `CONTAINS`, `BELONGS_TO`, `DEPENDS_ON`, `EMITTED`, `PERFORMED_BY`, `REFERENCES`
- [ ] Implement NetworkX graph store adapter
- [ ] Implement graph projection handlers (sync graph from domain events)
- [ ] Validate Gremlin-compatible traversal patterns

#### Success Criteria
- [ ] Plan -> Phase -> Task containment relationships navigable
- [ ] Event -> Aggregate -> Actor attribution queryable
- [ ] Graph can be rebuilt by replaying all events
- [ ] Traversal patterns match canon examples

#### Graph Technology Decision

**Initial**: NetworkX (pure Python, stdlib-compatible via pip install)

NetworkX is chosen because:
1. Pure Python implementation
2. Supports property graph model (vertices, edges, properties)
3. Sufficient for expected graph size (<10,000 nodes)
4. Migration path to Neptune/TinkerPop preserved by IGraphStore abstraction

---

### Phase 8: Test Infrastructure (Parallel Track)
**Priority**: P1 (runs in parallel with Phases 1-7)
**Estimated Duration**: 4-5 days (spread across other phases)
**Dependencies**: None (starts immediately)
**Gap Addressed**: GAP-010

#### Deliverables
- [ ] Create `tests/` directory structure (unit, integration, e2e)
- [ ] Add pytest configuration (`pyproject.toml` or `pytest.ini`)
- [ ] Write unit tests for shared kernel value objects (Phase 1)
- [ ] Write unit tests for event store (Phase 2)
- [ ] Write unit tests for aggregate root (Phase 3)
- [ ] Write unit tests for domain aggregates (Phase 4)
- [ ] Write integration tests for SQLite adapters (Phase 2)
- [ ] Write integration tests for repositories (Phase 4)
- [ ] Add property-based tests for value objects (hypothesis library optional)

#### Success Criteria
- [ ] 80%+ coverage on domain layer
- [ ] 70%+ coverage on application layer
- [ ] All aggregates have state machine transition tests
- [ ] Event replay correctness validated by tests
- [ ] CI pipeline runs tests on every commit

#### Test Naming Convention

Follow `test_{scenario}_when_{condition}_then_{expected}`:

```python
def test_task_transition_when_pending_to_in_progress_then_succeeds():
    ...

def test_task_transition_when_completed_to_in_progress_then_raises_invalid_state():
    ...
```

#### Directory Structure
```
tests/
├── __init__.py
├── conftest.py                 # Shared fixtures
├── unit/
│   ├── __init__.py
│   ├── shared_kernel/
│   │   ├── test_vertex_id.py
│   │   ├── test_task_id.py
│   │   ├── test_domain_event.py
│   │   └── test_aggregate_root.py
│   └── work_management/
│       ├── test_task.py
│       ├── test_phase.py
│       └── test_plan.py
├── integration/
│   ├── __init__.py
│   ├── test_sqlite_event_store.py
│   ├── test_sqlite_snapshot_store.py
│   └── test_task_repository.py
└── e2e/
    ├── __init__.py
    └── test_task_lifecycle.py
```

---

### Phase 9: Session Management Migration & Hexagonal Cleanup
**Priority**: P4
**Estimated Duration**: 3-4 days
**Dependencies**: Phases 1-7 complete
**Gap Addressed**: GAP-009, session_management alignment

#### Deliverables
- [ ] Create `ProjectId` -> `PlanId` adapter/bridge
- [ ] Migrate `FilesystemProjectAdapter` to emit events for project discovery
- [ ] Convert existing queries to read from projections
- [ ] Move `RepositoryError` to infrastructure layer
- [ ] Implement composition root / dependency injection
- [ ] Validate import graph compliance (no hexagonal boundary violations)
- [ ] Archive or remove deprecated code

#### Success Criteria
- [ ] Session management uses canonical patterns (Event Sourcing, projections)
- [ ] Zero hexagonal boundary violations (verified by import analysis)
- [ ] Composition root wires all dependencies
- [ ] Legacy `ProjectId` format remains externally compatible (human-readable)

---

## Validation Approach

### Architecture Tests (Automated)

Architecture compliance will be enforced via automated tests using import analysis.

```python
# tests/architecture/test_hexagonal_boundaries.py

def test_domain_layer_has_zero_external_imports():
    """Domain layer may only import from stdlib."""
    domain_files = glob.glob("src/**/domain/**/*.py", recursive=True)
    for file in domain_files:
        imports = extract_imports(file)
        for imp in imports:
            assert is_stdlib(imp) or imp.startswith("src."), \
                f"{file} imports non-stdlib module: {imp}"

def test_adapters_implement_port_interfaces():
    """All adapters must implement their corresponding port interfaces."""
    # Use ABC/Protocol inheritance checking
    pass

def test_no_cyclic_dependencies():
    """Detect cyclic imports between modules."""
    # Use import graph analysis
    pass
```

### Pattern Compliance Tests

```python
# tests/architecture/test_pattern_compliance.py

def test_vertex_id_inheritance():
    """All domain IDs must inherit from VertexId."""
    from src.shared_kernel.identity import TaskId, PhaseId, PlanId, VertexId
    assert issubclass(TaskId, VertexId)
    assert issubclass(PhaseId, VertexId)
    assert issubclass(PlanId, VertexId)

def test_cloud_events_envelope_validation():
    """Domain events must serialize to valid CloudEvents 1.0."""
    from src.shared_kernel.events import DomainEvent
    event = SampleEvent(...)
    envelope = event.to_cloud_event()
    assert envelope["specversion"] == "1.0"
    assert "id" in envelope
    assert "type" in envelope
    assert "source" in envelope
    assert "time" in envelope

def test_event_sourcing_replay_correctness():
    """Aggregate state from replay must match step-by-step mutations."""
    # Create aggregate, perform mutations
    task = Task.create(title="Test")
    task.start()
    task.complete()
    events = task.get_uncommitted_events()

    # Rebuild from history
    replayed = Task.load_from_history(events)

    # Compare states
    assert replayed.status == task.status
    assert replayed.version == task.version
```

### Manual Validation Checklist

Before each phase is marked complete:

- [ ] All deliverables implemented
- [ ] All success criteria met
- [ ] Unit tests passing
- [ ] Integration tests passing (if applicable)
- [ ] Code review completed
- [ ] Documentation updated

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Event Sourcing complexity delays delivery | Medium | High | Start with in-memory store; SQLite can follow |
| NetworkX requires pip install (not stdlib) | Low | Low | Acceptable for graph layer; abstract behind port |
| Team unfamiliar with Event Sourcing | Medium | Medium | Document patterns; pair programming on Phase 2 |
| Scope creep adds features before foundation | High | High | Strict phase gating; no new features until Phase 4 complete |
| SQLite performance insufficient | Low | Medium | Snapshots mitigate; can switch to PostgreSQL later |

---

## Open Questions

1. **NetworkX Dependency**: The canon specifies NetworkX for graph storage. This requires `pip install networkx`. Is this acceptable, or should we implement a simpler in-memory graph first?

   **Recommendation**: Accept NetworkX dependency for infrastructure layer (not domain). It's behind IGraphStore port, so replaceable.

2. **Snapshot Frequency**: The canon suggests "every 10 events." Should this be configurable per aggregate type?

   **Recommendation**: Make configurable with sensible default (10). Task may need higher frequency than Plan.

3. **Event Bus Technology**: In-process pub/sub or external message broker?

   **Recommendation**: In-process for Phase 2-6. External broker is future enhancement if multi-agent deployment needed.

---

## Links

* [Unified Architecture Canon](../synthesis/PROJ-001-e-006-unified-architecture-canon.md) - Authoritative pattern specification
* [Implementation Gap Analysis](../analysis/PROJ-001-e-007-implementation-gap-analysis.md) - Gap inventory and prioritization
* [Jerry Constitution](../governance/JERRY_CONSTITUTION.md) - Agent governance principles
* [WORKTRACKER_PROPOSAL Extraction](../research/PROJ-001-e-001-worktracker-proposal-extraction.md) - Original proposal analysis
* [Industry Best Practices](../research/PROJ-001-e-005-industry-best-practices.md) - External validation sources

### Industry References

* [Alistair Cockburn - Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
* [Martin Fowler - Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
* [Vaughn Vernon - Implementing Domain-Driven Design](https://www.amazon.com/Implementing-Domain-Driven-Design-Vaughn-Vernon/dp/0321834577)
* [CNCF CloudEvents 1.0](https://cloudevents.io/)
* [Michael Nygard - Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
* [MADR - Markdown Architectural Decision Records](https://adr.github.io/madr/)

---

*ADR created by ps-architect agent*
*Decision date: 2026-01-09*
