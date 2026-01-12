# Research Artifact: REVISED-ARCHITECTURE-v3.0 Foundation

> **Document ID:** PROJ-001-e-003-revised-architecture-foundation
> **PS ID:** PROJ-001
> **Entry ID:** e-003
> **Date:** 2026-01-09
> **Researcher:** ps-researcher agent v2.0.0
> **Sources:**
> - `docs/knowledge/dragonsbelurkin/history/REVISED-ARCHITECTURE-v3.0.md`

---

## L0: Executive Summary

**v3.0 represents a fundamental architectural shift from State-Stored to Event-Sourced persistence.**

The architecture document establishes three foundational patterns that work together:

1. **Event Sourcing** - All state changes captured as immutable events; aggregate state rebuilt by replaying events
2. **CQRS (Command Query Responsibility Segregation)** - Separate write model (events) from read models (projections)
3. **Hexagonal Architecture** - Ports define contracts, adapters implement them; all dependencies point inward

**Key Decision:** Hybrid Event Sourcing with Snapshots - events are the source of truth, snapshots provide performance optimization (rebuild from events if corrupted).

**Status:** Proposed for Review (as of 2025-12-21)

---

## L1: Technical Specifications

### 1. What Changed (v2.0 to v3.0)

| Aspect | v2.0 (State-Stored) | v3.0 (Event-Sourced) |
|--------|---------------------|----------------------|
| Persistence | Repository saves current state | Repository appends events to event store |
| Audit Trail | Via metadata (IAuditable, IECWTracked) | By design (immutable event log) |
| Data Model | Single model for reads and writes | Separate write model (events) and read models (projections) |
| Performance | Direct state access | Snapshots + projections |

**Architecture Decision (ADR-001):**
- Event Sourcing with Snapshots (hybrid approach)
- CQRS (separate write/read models)
- Generic IRepository<T, TId> pattern
- Complementary patterns: Unit of Work, Domain Events, Specification, Projections

---

### 2. Hexagonal Architecture Diagram

```
+----------------------------------+              +----------------------------------+
|   LEFT SIDE (Primary/Driving)    |              |   RIGHT SIDE (Secondary/Driven) |
|   ==============================  |              |   ==============================  |
|                                  |              |                                  |
|   ACTORS (External)              |              |   INFRASTRUCTURE                 |
|   +------------------+           |              |   +------------------+           |
|   | User/Developer   |           |              |   | Event Store      |           |
|   | Claude AI        |           |              |   | (SQLite/MCP)     |           |
|   | SessionStart Hook|           |              |   |                  |           |
|   +--------+---------+           |              |   | Snapshot Store   |           |
|            | calls               |              |   | (SQLite/MCP)     |           |
|            v                     |              |   |                  |           |
|                                  |              |   | Projection Store |           |
|   PRIMARY PORTS                  |              |   | (SQLite/MCP)     |           |
|   +------------------+           |              |   +--------^---------+           |
|   | Use Case Ifaces  |           |              |            | adapts              |
|   | (Commands)       |           |              |            |                     |
|   +------------------+           |              |   SECONDARY PORTS                |
|   | ICreatePS...     |           |              |   +------------------+           |
|   | IAddConstraint...|           |              |   | IRepository<T,Id>|           |
|   | IAnswerQ...      |           |              |   | IEventStore      |           |
|   | ILoadPS...       |           |              |   | ISnapshotStore   |           |
|   +--------+---------+           |              |   | IUnitOfWork      |           |
|            | implemented by      |              |   | IProjectionStore |           |
|            v                     |              |   | ISpecification<T>|           |
|                                  |              |   +--------^---------+           |
|   APPLICATION LAYER              |              |            |                     |
|   +------------------+           |              |            | implemented by      |
|   | Command Handlers |           |              |                                  |
|   | (Use Cases)      |           |              |   ADAPTERS                       |
|   +------------------+           |              |   +------------------+           |
|   | CreatePS         |---uses----+--------->----+-->| EventStoreAdapter|           |
|   | AddConstraint    |           |              |   | (SQLite/MCP)     |           |
|   | AnswerQuestion   |           |              |   |                  |           |
|   |                  |           |              |   | SnapshotAdapter  |           |
|   | Unit of Work     |           |              |   | (SQLite/MCP)     |           |
|   +--------+---------+           |              |   |                  |           |
|            | uses & raises       |              |   | ProjectionAdapter|           |
|            v                     |              |   | (SQLite/MCP)     |           |
|                                  |              |   +------------------+           |
|   DOMAIN LAYER                   |              |                                  |
|   +------------------+           |              |   EVENT HANDLERS                 |
|   | Aggregates       |           |              |   +------------------+           |
|   +------------------+           |              |   | Projection       |           |
|   | ProblemStatement |<-rehydr---+-------<------+---| Builders         |           |
|   |   - apply(event) |   ated    |              |   | (Event->View)    |           |
|   |   - raise(event) |   from    |              |   |                  |           |
|   |                  |  events   |              |   | PSListProjection |           |
|   | Value Objects    |           |              |   | PSDetailProj     |           |
|   |   - PhaseId      |           |              |   | ConstraintSearch |           |
|   |   - Constraint   |           |              |   +------------------+           |
|   |   - Question     |           |              |                                  |
|   |                  |           |              |   QUERY SIDE (CQRS)              |
|   | Domain Events    |------->---+--------->----+-->+------------------+           |
|   |   - PS Created   | published |              |   | IQueryHandler    |           |
|   |   - Cons Added   |           |              |   |   - ListPS       |           |
|   |   - Q Answered   |           |              |   |   - GetPS        |           |
|   |                  |           |              |   |   - SearchCons   |           |
|   | Specifications   |           |              |   +------------------+           |
|   |   - ByPhaseId    |           |              |                                  |
|   |   - WithStatus   |           |              |                                  |
|   +------------------+           |              |                                  |
|                                  |              |                                  |
+----------------------------------+              +----------------------------------+

                         ALL DEPENDENCIES POINT INWARD -->
```

**Key Insight:** Domain layer has NO external dependencies. Infrastructure adapters implement port interfaces. Application layer orchestrates domain logic and infrastructure.

---

### 3. Pattern Inventory

#### Mandatory Patterns (Event Sourcing + CQRS)

| Pattern | Purpose | Status |
|---------|---------|--------|
| **Aggregate Root** | Consistency boundary | Existing: ProblemStatement |
| **IRepository<T, TId>** | Domain abstraction for aggregates | Update to generic |
| **Event Store** | Append-only event log | NEW |
| **Snapshot Store** | Performance optimization | NEW |
| **Domain Events** | Capture business changes | NEW |
| **Unit of Work** | Atomic event batches | NEW |
| **Optimistic Concurrency** | Prevent lost updates | NEW |
| **Projection** | Query-friendly read models | NEW |
| **CQRS** | Separate write/read models | NEW |
| **Specification** | Business predicates | NEW |
| **Event Versioning** | Schema evolution | NEW |

#### Optional Patterns (If Needed)

| Pattern | Purpose | When Needed |
|---------|---------|-------------|
| **Outbox/Inbox** | Reliable event publishing | If integrating externally |
| **Saga/Process Manager** | Multi-aggregate workflows | If complex workflows |
| **Anti-Corruption Layer** | Protect from external models | If integrating MCP deeply |

---

### 4. Core Interface Specifications

#### 4.1 Generic Repository (Domain Abstraction)

```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional

TAggregate = TypeVar('TAggregate')
TId = TypeVar('TId')

class IRepository(ABC, Generic[TAggregate, TId]):
    """
    Domain abstraction for accessing Aggregate Roots.
    NOT a persistence mechanism - that's the adapter's job.

    Event-sourced implementation:
    - save() appends events to event store
    - find_by_id() reads events, replays to rebuild state
    """

    @abstractmethod
    def save(self, aggregate: TAggregate) -> None:
        """Persist aggregate. Event-sourced: Extracts uncommitted events, appends to stream."""
        pass

    @abstractmethod
    def find_by_id(self, id: TId) -> Optional[TAggregate]:
        """Retrieve aggregate by ID. Event-sourced: Loads events, replays to rebuild state."""
        pass

    @abstractmethod
    def exists(self, id: TId) -> bool:
        """Check if aggregate exists"""
        pass
```

#### 4.2 Event Store Interface

```python
@dataclass(frozen=True)
class StreamEvent:
    """Event with metadata"""
    event: DomainEvent
    event_id: str
    stream_id: str
    version: int  # Event version in stream
    timestamp: datetime
    metadata: Dict[str, Any]  # ECWVersion, Fingerprint, CreatedBy, etc.

class IEventStore(ABC):
    """Append-only event log. Core of Event Sourcing architecture."""

    @abstractmethod
    def append(
        self,
        stream_id: str,
        events: List[DomainEvent],
        expected_version: int,
        metadata: Dict[str, Any]
    ) -> None:
        """
        Append events to stream atomically.
        Raises ConcurrencyError if expected_version doesn't match actual.
        """
        pass

    @abstractmethod
    def read(self, stream_id: str, from_version: int = 0) -> List[StreamEvent]:
        """Read events from stream starting at from_version."""
        pass

    @abstractmethod
    def get_version(self, stream_id: str) -> int:
        """Get current version of stream (last event number)"""
        pass
```

#### 4.3 Snapshot Store Interface

```python
class ISnapshotStore(ABC):
    """
    Snapshot storage for performance.
    Snapshots are CACHE - events are source of truth.
    If snapshot corrupt, rebuild from events.
    """

    @abstractmethod
    def save_snapshot(
        self,
        stream_id: str,
        aggregate: ProblemStatement,
        at_version: int
    ) -> None:
        """Save aggregate snapshot at specific version."""
        pass

    @abstractmethod
    def get_snapshot(self, stream_id: str) -> Optional[Tuple[ProblemStatement, int]]:
        """Get latest snapshot. Returns (aggregate_state, version) or None."""
        pass
```

#### 4.4 Unit of Work Interface

```python
class IUnitOfWork(ABC):
    """
    Atomic commit boundary.
    Coordinates repository changes and event publishing.
    One UoW per application command.
    """

    @abstractmethod
    def __enter__(self) -> 'IUnitOfWork':
        """Start unit of work"""
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """On success: Append events, update snapshots, publish domain events. On failure: Rollback."""
        pass

    @abstractmethod
    def register_aggregate(self, aggregate: Any) -> None:
        """Register aggregate for commit"""
        pass

    @abstractmethod
    def commit(self) -> None:
        """Commit all changes atomically"""
        pass

    @abstractmethod
    def rollback(self) -> None:
        """Rollback all changes"""
        pass
```

#### 4.5 Specification Interface

```python
class ISpecification(ABC, Generic[T]):
    """Business predicate for querying. Encapsulates business logic, prevents repository method explosion."""

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if candidate satisfies specification"""
        pass

    @abstractmethod
    def and_(self, other: 'ISpecification[T]') -> 'ISpecification[T]':
        """Combine with AND"""
        pass

    @abstractmethod
    def or_(self, other: 'ISpecification[T]') -> 'ISpecification[T]':
        """Combine with OR"""
        pass

    @abstractmethod
    def not_(self) -> 'ISpecification[T]':
        """Negate"""
        pass
```

#### 4.6 Projection Interface

```python
class IProjection(ABC):
    """Read model projection. Built by consuming events from event store. Eventually consistent with write side."""

    @abstractmethod
    def project(self, event: DomainEvent) -> None:
        """Apply event to projection"""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset projection (for rebuild)"""
        pass
```

---

### 5. Domain Events

#### Event Base Class

```python
@dataclass(frozen=True)
class DomainEvent(ABC):
    """Base class for all domain events. Events are immutable, past-tense facts."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    occurred_at: datetime = field(default_factory=datetime.utcnow)

    # IAuditable metadata
    caused_by: str = "Claude"  # User email or "Claude" or "System"

    # IECWTracked metadata
    ecw_version: str = "v2.2.0"
    fingerprint: str = ""

    @abstractmethod
    def event_type(self) -> str:
        """Event type name for serialization"""
        pass
```

#### Problem Statement Events

| Event | Purpose | Key Fields |
|-------|---------|------------|
| `ProblemStatementCreated` | PS was created | phase_id, title, what, why, who |
| `ConstraintAdded` | Constraint was added | phase_id, constraint_id, description, impact, status |
| `ConstraintStatusUpdated` | Constraint status changed | phase_id, constraint_id, old_status, new_status |
| `QuestionAdded` | Question was added | phase_id, question_id, question, hypothesis |
| `QuestionAnswered` | Question was answered | phase_id, question_id, answer |
| `ExplorationEntryAdded` | Exploration entry logged | phase_id, date, event_name, description, impact |
| `ProblemStatementStatusUpdated` | PS status changed | phase_id, old_status, new_status |

---

### 6. Aggregate Root Pattern (Event-Sourced)

The `ProblemStatement` aggregate follows this pattern:

**Structure:**
- Business fields (phase_id, title, constraints, questions, etc.)
- Event sourcing metadata (_version, _uncommitted_events)
- IAuditable metadata (created_by, updated_by, etc.)
- IECWTracked metadata (ecw_version, fingerprint)

**Command Methods (raise events):**
- `create()` - Factory method, raises `ProblemStatementCreated`
- `add_constraint()` - Raises `ConstraintAdded`
- `answer_question()` - Raises `QuestionAnswered`
- `update_status()` - Raises `ProblemStatementStatusUpdated`

**Event Application:**
- `_apply(event)` - Applies event to state (called during replay and after raising)
- `_raise_event(event)` - Adds to uncommitted events + applies to state

**Infrastructure Methods:**
- `get_uncommitted_events()` - Returns events not yet persisted
- `mark_events_committed()` - Clears uncommitted events
- `load_from_history(events)` - Rebuilds state by replaying events

---

### 7. CQRS Projections

**List View Projection:** `ProblemStatementListProjection`
- Fields: phase_id, title, status, constraint_count, question_count, unanswered_questions, updated_on, updated_by
- Purpose: Fast list queries

**Detail View Projection:** `ProblemStatementDetailProjection`
- Fields: Complete PS data for display
- Purpose: Single item retrieval

**Search Projection:** `ConstraintSearchProjection`
- Fields: phase_id, constraint_id, description, status, impact
- Purpose: Cross-PS constraint search

---

### 8. Performance Strategy

**Snapshot Strategy:**
- Snapshot after every 10 events (tunable)
- Snapshots stored separately from events
- Load process: Get snapshot -> Load events after snapshot version -> Replay

**Expected Performance:**

| Operation | Baseline | Target | Strategy |
|-----------|----------|--------|----------|
| create_problem_statement | 0.58ms | 0.64ms | Snapshot after creation |
| add_constraint | 2.35ms | 2.59ms | Snapshot every 10 events |
| full_workflow | 5.47ms | 6.02ms | Snapshots + CQRS projections |

**CQRS Performance Benefits:**
- Reads from projections (pre-computed) = Fast
- Writes append events (no complex queries) = Fast
- Eventual consistency (projection lag <100ms acceptable)

---

### 9. Migration Path (v2.0 to v3.0)

| Phase | Description | Breaking Changes |
|-------|-------------|------------------|
| Phase 1 | Add Event Infrastructure | None |
| Phase 2 | Dual Write (Events + State) | None |
| Phase 3 | Switch to Event-Sourced Repository | Minor |
| Phase 4 | Add CQRS Projections | None |
| Phase 5 | Cleanup (remove state-stored) | Breaking |

---

## L2: Strategic Analysis

### Why Event Sourcing?

1. **Audit Trail by Design** - Every state change is captured as an immutable event. No need for separate audit tables or metadata.

2. **Temporal Queries** - Can reconstruct state at any point in time by replaying events up to that moment.

3. **Event-Driven Architecture** - Events can be published to other systems, enabling loose coupling and eventual consistency patterns.

4. **Debugging and Troubleshooting** - Complete history of what happened and why (including who caused each change).

5. **Schema Evolution** - Event versioning allows gradual schema changes without losing historical data.

### Why CQRS?

1. **Scalability** - Read and write models can scale independently. Projections can be denormalized for query performance.

2. **Separation of Concerns** - Write model optimized for consistency and invariant enforcement. Read models optimized for specific query patterns.

3. **Multiple Views** - Same events can power multiple projections (list view, detail view, search index, analytics).

4. **Eventual Consistency Trade-off** - Acceptable for this domain; projection lag <100ms is unnoticeable to users.

### Why Hexagonal Architecture?

1. **Testability** - Domain logic can be tested without infrastructure. Ports can be mocked.

2. **Flexibility** - Adapters can be swapped (SQLite -> PostgreSQL, MCP -> REST) without changing domain or application logic.

3. **Dependency Inversion** - Infrastructure depends on domain, not vice versa. Protects core business logic from technical concerns.

4. **Clean Boundaries** - Clear separation between what the system does (domain) and how it does it (infrastructure).

### Long-Term Implications

**Benefits:**
- System becomes more maintainable as complexity grows
- Complete audit history without additional effort
- Easier to add new query patterns (just add projections)
- Supports future distributed/microservices architecture if needed

**Costs:**
- Higher initial implementation complexity
- Learning curve for team members unfamiliar with patterns
- Eventual consistency requires careful UI/UX design
- More infrastructure components to manage

**Risk Mitigation:**
- Hybrid approach (snapshots) addresses performance concerns
- Migration path allows gradual adoption
- Events as source of truth means snapshots/projections can be rebuilt

---

## Files to Create/Update (Implementation Roadmap)

### New Files

| File | Purpose |
|------|---------|
| `domain/events/*.py` | Domain event classes |
| `ports/i_event_store.py` | Event store interface |
| `ports/i_snapshot_store.py` | Snapshot store interface |
| `ports/i_unit_of_work.py` | Unit of Work interface |
| `ports/i_specification.py` | Specification interface |
| `ports/i_projection.py` | Projection interface |
| `adapters/event_store_sqlite.py` | SQLite event store adapter |
| `adapters/snapshot_store_sqlite.py` | SQLite snapshot store adapter |
| `adapters/projection_store_sqlite.py` | SQLite projection store adapter |
| `projections/*.py` | Projection builders |
| `contracts/ADR-001-event-sourcing-cqrs.md` | Architecture decision record |

### Updated Files

| File | Changes |
|------|---------|
| `ports/i_repository.py` | Migrate to Generic IRepository<T, TId> |
| `domain/entities/problem_statement.py` | Make event-sourced |
| `application/use_cases/*.py` | Use Unit of Work |

---

## References

- Source Document: `docs/knowledge/dragonsbelurkin/history/REVISED-ARCHITECTURE-v3.0.md`
- Related ADR: `ADR-001-event-sourcing-cqrs.md`
- Version: 3.0.0 (Architectural Revision)
- Original Date: 2025-12-21
