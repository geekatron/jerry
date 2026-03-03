# Phase 38 Revised Architecture v3.0
## Event Sourcing + CQRS + Hexagonal Architecture

> **Version:** 3.0.0 (Architectural Revision)
> **Previous:** 2.0.0 (State-Stored with Metadata)
> **Date:** 2025-12-21
> **Status:** Proposed for Review
> **ADR:** [ADR-001-event-sourcing-cqrs.md](ADR-001-event-sourcing-cqrs.md)

---

## What Changed (v2.0 → v3.0)

### Fundamental Shift

**v2.0 (State-Stored):**
- Repository saves current state
- Audit trail via metadata (IAuditable, IECWTracked)
- Single model for reads and writes

**v3.0 (Event-Sourced + CQRS):**
- Repository appends events to event store
- Audit trail by design (immutable event log)
- Separate write model (events) and read models (projections)
- State snapshots for performance

### Architecture Decision

Per [ADR-001](ADR-001-event-sourcing-cqrs.md), chosen:
- ✅ **Event Sourcing with Snapshots** (hybrid approach)
- ✅ **CQRS** (separate write/read models)
- ✅ **Generic IRepository<T, TId>** pattern
- ✅ **Complementary patterns:** Unit of Work, Domain Events, Specification, Projections

---

## Complete Hexagonal Architecture (Both Sides + All Patterns)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                         HEXAGONAL ARCHITECTURE v3.0                              │
│                  Event Sourcing + CQRS + Complete Pattern Suite                  │
└──────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────┐              ┌─────────────────────────────────┐
│   LEFT SIDE (Primary/Driving)   │              │   RIGHT SIDE (Secondary/Driven) │
│   ═══════════════════════════   │              │   ════════════════════════════  │
│                                 │              │                                 │
│   ACTORS (External)             │              │   INFRASTRUCTURE                │
│   ┌──────────────────┐          │              │   ┌──────────────────┐          │
│   │ User/Developer   │          │              │   │ Event Store      │          │
│   │ Claude AI        │          │              │   │ (SQLite/MCP)     │          │
│   │ SessionStart Hook│          │              │   │                  │          │
│   └────────┬─────────┘          │              │   │ Snapshot Store   │          │
│            │                    │              │   │ (SQLite/MCP)     │          │
│            │ calls              │              │   │                  │          │
│            ▼                    │              │   │ Projection Store │          │
│                                 │              │   │ (SQLite/MCP)     │          │
│   PRIMARY PORTS                 │              │   └────────▲─────────┘          │
│   ┌──────────────────┐          │              │            │                    │
│   │ Use Case Ifaces  │          │              │            │ adapts             │
│   │ (Commands)       │          │              │            │                    │
│   ├──────────────────┤          │              │   SECONDARY PORTS               │
│   │ ICreatePS...     │          │              │   ┌──────────────────┐          │
│   │ IAddConstraint...│          │              │   │ IRepository<T,Id>│          │
│   │ IAnswerQ...      │          │              │   │ IEventStore      │          │
│   │ ILoadPS...       │          │              │   │ ISnapshotStore   │          │
│   └────────┬─────────┘          │              │   │ IUnitOfWork      │          │
│            │                    │              │   │ IProjectionStore │          │
│            │ implemented by     │              │   │ ISpecification<T>│          │
│            ▼                    │              │   └────────▲─────────┘          │
│                                 │              │            │                    │
│   APPLICATION LAYER             │              │            │ implemented by     │
│   ┌──────────────────┐          │              │                                 │
│   │ Command Handlers │          │              │   ADAPTERS                      │
│   │ (Use Cases)      │          │              │   ┌──────────────────┐          │
│   ├──────────────────┤          │              │   │ EventStoreAdapter│          │
│   │ CreatePS         │───uses───┼──────────────┼──→│ (SQLite/MCP)     │          │
│   │ AddConstraint    │          │              │   │                  │          │
│   │ AnswerQuestion   │          │              │   │ SnapshotAdapter  │          │
│   │                  │          │              │   │ (SQLite/MCP)     │          │
│   │ Unit of Work     │          │              │   │                  │          │
│   └────────┬─────────┘          │              │   │ ProjectionAdapter│          │
│            │                    │              │   │ (SQLite/MCP)     │          │
│            │ uses & raises      │              │   └──────────────────┘          │
│            ▼                    │              │                                 │
│                                 │              │                                 │
│   DOMAIN LAYER                  │              │   EVENT HANDLERS                │
│   ┌──────────────────┐          │              │   ┌──────────────────┐          │
│   │ Aggregates       │          │              │   │ Projection       │          │
│   ├──────────────────┤          │              │   │ Builders         │          │
│   │ ProblemStatement │◄─rehydr──┼──────────────┼───│ (Event→View)     │          │
│   │   - apply(event) │   ated   │              │   │                  │          │
│   │   - raise(event) │   from   │              │   │ PSListProjection │          │
│   │                  │  events  │              │   │ PSDetailProj     │          │
│   │ Value Objects    │          │              │   │ ConstraintSearch │          │
│   │   - PhaseId      │          │              │   └──────────────────┘          │
│   │   - Constraint   │          │              │                                 │
│   │   - Question     │          │              │                                 │
│   │                  │          │              │   QUERY SIDE (CQRS)             │
│   │ Domain Events    │──────────┼──────────────┼──→┌──────────────────┐          │
│   │   - PS Created   │ published│              │   │ IQueryHandler    │          │
│   │   - Cons Added   │          │              │   │   - ListPS       │          │
│   │   - Q Answered   │          │              │   │   - GetPS        │          │
│   │                  │          │              │   │   - SearchCons   │          │
│   │ Specifications   │          │              │   └──────────────────┘          │
│   │   - ByPhaseId    │          │              │                                 │
│   │   - WithStatus   │          │              │                                 │
│   └──────────────────┘          │              │                                 │
│                                 │              │                                 │
└─────────────────────────────────┘              └─────────────────────────────────┘

                              ALL DEPENDENCIES POINT INWARD →
```

---

## Pattern Inventory

### Mandatory (Event Sourcing + CQRS)

| Pattern | Purpose | Status |
|---------|---------|--------|
| **Aggregate Root** | Consistency boundary | ✅ ProblemStatement |
| **IRepository<T, TId>** | Domain abstraction for aggregates | 🔄 Update to generic |
| **Event Store** | Append-only event log | ⭐ NEW |
| **Snapshot Store** | Performance optimization | ⭐ NEW |
| **Domain Events** | Capture business changes | ⭐ NEW |
| **Unit of Work** | Atomic event batches | ⭐ NEW |
| **Optimistic Concurrency** | Prevent lost updates | ⭐ NEW |
| **Projection** | Query-friendly read models | ⭐ NEW |
| **CQRS** | Separate write/read models | ⭐ NEW |
| **Specification** | Business predicates | ⭐ NEW |
| **Event Versioning** | Schema evolution | ⭐ NEW |

### Optional (If Needed)

| Pattern | Purpose | When Needed |
|---------|---------|-------------|
| **Outbox/Inbox** | Reliable event publishing | If integrating externally |
| **Saga/Process Manager** | Multi-aggregate workflows | If complex workflows |
| **Anti-Corruption Layer** | Protect from external models | If integrating MCP deeply |

---

## Core Interfaces (Updated)

### 1. Generic Repository (Domain Abstraction)

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
        """
        Persist aggregate.

        Event-sourced: Extracts uncommitted events, appends to stream.
        State-stored: Saves current state.
        """
        pass

    @abstractmethod
    def find_by_id(self, id: TId) -> Optional[TAggregate]:
        """
        Retrieve aggregate by ID.

        Event-sourced: Loads events, replays to rebuild state (with snapshot optimization).
        State-stored: Loads state from database.
        """
        pass

    @abstractmethod
    def exists(self, id: TId) -> bool:
        """Check if aggregate exists"""
        pass
```

### 2. Problem Statement Repository (Specific)

```python
class IProblemStatementRepository(IRepository[ProblemStatement, PhaseId]):
    """
    Repository for ProblemStatement aggregate root.

    Inherits from generic IRepository<TAggregate, TId>.
    No additional methods - aggregate-specific logic is in the aggregate itself.
    """
    pass
```

### 3. Event Store (Infrastructure Port)

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
    """
    Append-only event log.

    Core of Event Sourcing architecture.
    """

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

        Args:
            stream_id: Aggregate ID (e.g., "problem-statement:phase-42")
            events: Domain events to append
            expected_version: For optimistic concurrency
            metadata: IAuditable + IECWTracked fields

        Raises:
            ConcurrencyError: If expected_version doesn't match actual
        """
        pass

    @abstractmethod
    def read(
        self,
        stream_id: str,
        from_version: int = 0
    ) -> List[StreamEvent]:
        """
        Read events from stream.

        Args:
            stream_id: Aggregate ID
            from_version: Start reading from this version (for snapshots)

        Returns:
            List of events in order
        """
        pass

    @abstractmethod
    def get_version(self, stream_id: str) -> int:
        """Get current version of stream (last event number)"""
        pass
```

### 4. Snapshot Store (Performance Optimization)

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
        """
        Save aggregate snapshot at specific version.

        Args:
            stream_id: Aggregate ID
            aggregate: Current aggregate state
            at_version: Event version this snapshot represents
        """
        pass

    @abstractmethod
    def get_snapshot(
        self,
        stream_id: str
    ) -> Optional[Tuple[ProblemStatement, int]]:
        """
        Get latest snapshot.

        Returns:
            (aggregate_state, version) or None if no snapshot
        """
        pass
```

### 5. Unit of Work (Atomic Commit Boundary)

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
        """
        Commit or rollback.

        On success: Append events, update snapshots, publish domain events
        On failure: Rollback all changes
        """
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

### 6. Specification (Business Predicates)

```python
class ISpecification(ABC, Generic[T]):
    """
    Business predicate for querying.

    Encapsulates business logic, prevents repository method explosion.
    """

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

# Example Specifications
class ByPhaseIdSpec(ISpecification[ProblemStatement]):
    def __init__(self, phase_id: PhaseId):
        self.phase_id = phase_id

    def is_satisfied_by(self, ps: ProblemStatement) -> bool:
        return ps.phase_id == self.phase_id

class WithStatusSpec(ISpecification[ProblemStatement]):
    def __init__(self, status: str):
        self.status = status

    def is_satisfied_by(self, ps: ProblemStatement) -> bool:
        return ps.status == self.status
```

---

## Domain Events (NEW)

### Event Base Class

```python
@dataclass(frozen=True)
class DomainEvent(ABC):
    """
    Base class for all domain events.

    Events are immutable, past-tense facts.
    """
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    occurred_at: datetime = field(default_factory=datetime.utcnow)

    # IAuditable metadata (who caused this event)
    caused_by: str = "Claude"  # User email or "Claude" or "System"

    # IECWTracked metadata (which ECW version)
    ecw_version: str = "v2.2.0"
    fingerprint: str = ""

    @abstractmethod
    def event_type(self) -> str:
        """Event type name for serialization"""
        pass
```

### Problem Statement Events

```python
@dataclass(frozen=True)
class ProblemStatementCreated(DomainEvent):
    """Problem statement was created"""
    phase_id: PhaseId
    title: str
    what: str
    why: str
    who: List[str]

    def event_type(self) -> str:
        return "ProblemStatementCreated"

@dataclass(frozen=True)
class ConstraintAdded(DomainEvent):
    """Constraint was added to problem statement"""
    phase_id: PhaseId
    constraint_id: str
    description: str
    impact: str
    discovered: str
    status: str  # "HYPOTHESIS" | "VALIDATED"
    mitigation: Optional[str] = None

    def event_type(self) -> str:
        return "ConstraintAdded"

@dataclass(frozen=True)
class ConstraintStatusUpdated(DomainEvent):
    """Constraint status changed"""
    phase_id: PhaseId
    constraint_id: str
    old_status: str
    new_status: str

    def event_type(self) -> str:
        return "ConstraintStatusUpdated"

@dataclass(frozen=True)
class QuestionAdded(DomainEvent):
    """Question was added"""
    phase_id: PhaseId
    question_id: str
    question: str
    hypothesis: Optional[str] = None
    blocked_by: Optional[str] = None

    def event_type(self) -> str:
        return "QuestionAdded"

@dataclass(frozen=True)
class QuestionAnswered(DomainEvent):
    """Question was answered"""
    phase_id: PhaseId
    question_id: str
    answer: str

    def event_type(self) -> str:
        return "QuestionAnswered"

@dataclass(frozen=True)
class ExplorationEntryAdded(DomainEvent):
    """Exploration entry was logged"""
    phase_id: PhaseId
    date: str
    event_name: str
    description: str
    impact: str

    def event_type(self) -> str:
        return "ExplorationEntryAdded"

@dataclass(frozen=True)
class ProblemStatementStatusUpdated(DomainEvent):
    """Problem statement status changed"""
    phase_id: PhaseId
    old_status: str
    new_status: str

    def event_type(self) -> str:
        return "ProblemStatementStatusUpdated"
```

---

## Aggregate Root (Event-Sourced)

### ProblemStatement Aggregate

```python
from dataclasses import dataclass, field
from typing import List
from datetime import datetime

@dataclass
class ProblemStatement:
    """
    Aggregate Root - Event-Sourced.

    State is rebuilt by replaying events.
    Changes produce new events (not saved immediately).
    """

    # Business fields
    phase_id: PhaseId
    title: str = ""
    what: str = ""
    why: str = ""
    who: List[str] = field(default_factory=list)
    status: str = "EXPLORING"
    constraints: List[Constraint] = field(default_factory=list)
    questions: List[Question] = field(default_factory=list)
    exploration_log: List[ExplorationEntry] = field(default_factory=list)

    # Event sourcing metadata
    _version: int = 0  # Stream version
    _uncommitted_events: List[DomainEvent] = field(default_factory=list)

    # IAuditable metadata (from events)
    created_by: str = "Claude"
    created_on: datetime = field(default_factory=datetime.utcnow)
    updated_by: str = "Claude"
    updated_on: datetime = field(default_factory=datetime.utcnow)

    # IECWTracked metadata (from events)
    ecw_version: str = "v2.2.0"
    fingerprint: str = ""

    # ============================================================================
    # COMMAND METHODS (Business logic - raises events)
    # ============================================================================

    @staticmethod
    def create(
        phase_id: PhaseId,
        title: str,
        what: str,
        why: str,
        who: List[str],
        created_by: str,
        ecw_version: str,
        fingerprint: str
    ) -> 'ProblemStatement':
        """
        Create new problem statement (factory method).

        Raises: ProblemStatementCreated event
        """
        ps = ProblemStatement(phase_id=phase_id)
        event = ProblemStatementCreated(
            phase_id=phase_id,
            title=title,
            what=what,
            why=why,
            who=who,
            caused_by=created_by,
            ecw_version=ecw_version,
            fingerprint=fingerprint
        )
        ps._raise_event(event)
        return ps

    def add_constraint(
        self,
        constraint: Constraint,
        added_by: str,
        ecw_version: str,
        fingerprint: str
    ) -> None:
        """
        Add constraint to problem statement.

        Business rule: Unique constraint IDs
        Raises: ConstraintAdded event
        """
        if any(c.id == constraint.id for c in self.constraints):
            raise DuplicateConstraintError(constraint.id)

        event = ConstraintAdded(
            phase_id=self.phase_id,
            constraint_id=constraint.id,
            description=constraint.description,
            impact=constraint.impact,
            discovered=constraint.discovered,
            status=constraint.status,
            mitigation=constraint.mitigation,
            caused_by=added_by,
            ecw_version=ecw_version,
            fingerprint=fingerprint
        )
        self._raise_event(event)

    def answer_question(
        self,
        question_id: str,
        answer: str,
        answered_by: str,
        ecw_version: str,
        fingerprint: str
    ) -> None:
        """
        Answer a question.

        Business rule: Question must exist and be open
        Raises: QuestionAnswered event
        """
        question = self._find_question(question_id)
        if not question:
            raise QuestionNotFoundError(question_id)

        if question.status == "ANSWERED":
            raise ValueError(f"Question {question_id} already answered")

        event = QuestionAnswered(
            phase_id=self.phase_id,
            question_id=question_id,
            answer=answer,
            caused_by=answered_by,
            ecw_version=ecw_version,
            fingerprint=fingerprint
        )
        self._raise_event(event)

        # If all questions answered, suggest status update
        if self._all_questions_answered():
            self.update_status("UNDERSTOOD", answered_by, ecw_version, fingerprint)

    def update_status(
        self,
        new_status: str,
        updated_by: str,
        ecw_version: str,
        fingerprint: str
    ) -> None:
        """
        Update problem statement status.

        Raises: ProblemStatementStatusUpdated event
        """
        if new_status not in ["EXPLORING", "UNDERSTOOD", "BLOCKED"]:
            raise ValueError(f"Invalid status: {new_status}")

        if self.status == new_status:
            return  # No change

        event = ProblemStatementStatusUpdated(
            phase_id=self.phase_id,
            old_status=self.status,
            new_status=new_status,
            caused_by=updated_by,
            ecw_version=ecw_version,
            fingerprint=fingerprint
        )
        self._raise_event(event)

    # ============================================================================
    # EVENT APPLICATION (State changes - replays events)
    # ============================================================================

    def _apply(self, event: DomainEvent) -> None:
        """
        Apply event to aggregate state.

        Called during:
        1. Event replay (loading from event store)
        2. After raising new event (optimistic update)
        """
        if isinstance(event, ProblemStatementCreated):
            self.title = event.title
            self.what = event.what
            self.why = event.why
            self.who = event.who
            self.created_by = event.caused_by
            self.created_on = event.occurred_at
            self.updated_by = event.caused_by
            self.updated_on = event.occurred_at
            self.ecw_version = event.ecw_version
            self.fingerprint = event.fingerprint

        elif isinstance(event, ConstraintAdded):
            constraint = Constraint(
                id=event.constraint_id,
                description=event.description,
                impact=event.impact,
                discovered=event.discovered,
                status=event.status,
                mitigation=event.mitigation
            )
            self.constraints.append(constraint)
            self.updated_by = event.caused_by
            self.updated_on = event.occurred_at

        elif isinstance(event, QuestionAnswered):
            question = self._find_question(event.question_id)
            if question:
                # Create new question with answer (immutable)
                answered_question = question.answer_with(event.answer)
                self.questions = [
                    answered_question if q.id == event.question_id else q
                    for q in self.questions
                ]
            self.updated_by = event.caused_by
            self.updated_on = event.occurred_at

        elif isinstance(event, ProblemStatementStatusUpdated):
            self.status = event.new_status
            self.updated_by = event.caused_by
            self.updated_on = event.occurred_at

        # ... handle other events ...

        self._version += 1

    def _raise_event(self, event: DomainEvent) -> None:
        """
        Raise new event.

        1. Add to uncommitted events (for persistence)
        2. Apply to current state (optimistic update)
        """
        self._uncommitted_events.append(event)
        self._apply(event)

    # ============================================================================
    # EVENT SOURCING INFRASTRUCTURE
    # ============================================================================

    def get_uncommitted_events(self) -> List[DomainEvent]:
        """Get events raised but not yet persisted"""
        return self._uncommitted_events.copy()

    def mark_events_committed(self) -> None:
        """Clear uncommitted events after successful persistence"""
        self._uncommitted_events.clear()

    def load_from_history(self, events: List[DomainEvent]) -> None:
        """Rebuild state by replaying events"""
        for event in events:
            self._apply(event)

    @property
    def version(self) -> int:
        """Current version (event count)"""
        return self._version

    # ============================================================================
    # HELPER METHODS
    # ============================================================================

    def _find_question(self, question_id: str) -> Optional[Question]:
        return next((q for q in self.questions if q.id == question_id), None)

    def _all_questions_answered(self) -> bool:
        return all(q.status == "ANSWERED" for q in self.questions)
```

---

## CQRS Read Models (Projections)

### Projection Interface

```python
class IProjection(ABC):
    """
    Read model projection.

    Built by consuming events from event store.
    Eventually consistent with write side.
    """

    @abstractmethod
    def project(self, event: DomainEvent) -> None:
        """Apply event to projection"""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset projection (for rebuild)"""
        pass
```

### Example Projections

```python
# 1. Problem Statement List View (for "list all")
@dataclass
class ProblemStatementListItem:
    phase_id: str
    title: str
    status: str
    constraint_count: int
    question_count: int
    unanswered_questions: int
    updated_on: datetime
    updated_by: str

class ProblemStatementListProjection(IProjection):
    def __init__(self, store: IProjectionStore):
        self.store = store

    def project(self, event: DomainEvent) -> None:
        if isinstance(event, ProblemStatementCreated):
            item = ProblemStatementListItem(
                phase_id=str(event.phase_id),
                title=event.title,
                status="EXPLORING",
                constraint_count=0,
                question_count=0,
                unanswered_questions=0,
                updated_on=event.occurred_at,
                updated_by=event.caused_by
            )
            self.store.save("ps_list", str(event.phase_id), item)

        elif isinstance(event, ConstraintAdded):
            item = self.store.get("ps_list", str(event.phase_id))
            if item:
                item.constraint_count += 1
                item.updated_on = event.occurred_at
                self.store.save("ps_list", str(event.phase_id), item)

        # ... handle other events ...

    def reset(self) -> None:
        self.store.clear("ps_list")

# 2. Problem Statement Detail View (for "get by id")
@dataclass
class ProblemStatementDetailView:
    """Complete problem statement for display"""
    phase_id: str
    title: str
    what: str
    why: str
    who: List[str]
    status: str
    constraints: List[dict]
    questions: List[dict]
    exploration_log: List[dict]
    created_by: str
    created_on: datetime
    updated_by: str
    updated_on: datetime
    ecw_version: str
    fingerprint: str

class ProblemStatementDetailProjection(IProjection):
    # Similar to list projection but builds complete view
    pass

# 3. Constraint Search View (for filtering)
@dataclass
class ConstraintSearchItem:
    phase_id: str
    constraint_id: str
    description: str
    status: str
    impact: str

class ConstraintSearchProjection(IProjection):
    # Builds searchable index of constraints across all problem statements
    pass
```

---

## Revised Workflow

### Write Side (Commands)

```python
# Example: Add Constraint Use Case

class AddConstraintUseCase(IAddConstraintUseCase):
    def __init__(
        self,
        repository: IProblemStatementRepository,
        unit_of_work: IUnitOfWork
    ):
        self.repository = repository
        self.uow = unit_of_work

    def execute(self, request: AddConstraintRequest) -> AddConstraintResponse:
        with self.uow:
            # 1. Load aggregate (from events + snapshot)
            ps = self.repository.find_by_id(request.phase_id)
            if not ps:
                raise ProblemStatementNotFoundError(request.phase_id)

            # 2. Execute command (raises events)
            constraint = Constraint(
                id=request.constraint_id,
                description=request.description,
                impact=request.impact,
                discovered=request.discovered,
                status="HYPOTHESIS"
            )
            ps.add_constraint(
                constraint,
                added_by=request.updated_by,
                ecw_version=request.ecw_version,
                fingerprint=request.fingerprint
            )

            # 3. Register for commit
            self.uow.register_aggregate(ps)

            # 4. Commit (appends events, updates snapshot, publishes domain events)
            self.uow.commit()

        return AddConstraintResponse(
            success=True,
            constraint_id=request.constraint_id
        )
```

### Read Side (Queries)

```python
# Example: List Problem Statements Query

class ListProblemStatementsQueryHandler:
    def __init__(self, projection_store: IProjectionStore):
        self.store = projection_store

    def handle(self, query: ListProblemStatementsQuery) -> List[ProblemStatementListItem]:
        # Query projection (not events!)
        items = self.store.query("ps_list", query.filter_spec)
        return items
```

---

## Performance Strategy

### Snapshot Strategy

- **Snapshot after every 10 events** (tunable)
- Snapshots stored separately from events
- On load:
  1. Try to get snapshot
  2. If found, load events AFTER snapshot version
  3. If not, load all events
  4. Replay events to rebuild state

### Expected Performance

| Operation | Baseline | Target | Strategy |
|-----------|----------|--------|----------|
| create_problem_statement | 0.58ms | 0.64ms | Snapshot after creation |
| add_constraint | 2.35ms | 2.59ms | Snapshot every 10 events |
| full_workflow | 5.47ms | 6.02ms | Snapshots + CQRS projections |

### CQRS Performance

- **Reads from projections** (pre-computed views) → Fast
- **Writes append events** (no complex queries) → Fast
- **Eventual consistency** (projection lag <100ms acceptable)

---

## Migration Path (v2.0 → v3.0)

### Phase 1: Add Event Infrastructure (No Breaking Changes)

1. Create Event Store adapter (SQLite)
2. Create Snapshot Store adapter (SQLite)
3. Create Domain Events
4. Keep existing state-stored repository working

### Phase 2: Dual Write (Events + State)

1. Repository appends events AND saves state
2. Both event store and state store active
3. Verify events are correct

### Phase 3: Switch to Event-Sourced Repository

1. Repository reads from events (with snapshots)
2. Stop writing to state store
3. Run performance tests

### Phase 4: Add CQRS Projections

1. Create projection builders
2. Build projections from events
3. Switch queries to projections

### Phase 5: Cleanup

1. Remove state-stored repository
2. Remove redundant code
3. Final performance validation

---

## Files Requiring Updates

### New Files (v3.0)

1. **domain/events/*.py** - Domain event classes
2. **ports/i_event_store.py** - Event store interface
3. **ports/i_snapshot_store.py** - Snapshot store interface
4. **ports/i_unit_of_work.py** - Unit of Work interface
5. **ports/i_specification.py** - Specification interface
6. **ports/i_projection.py** - Projection interface
7. **adapters/event_store_sqlite.py** - SQLite event store
8. **adapters/snapshot_store_sqlite.py** - SQLite snapshot store
9. **adapters/projection_store_sqlite.py** - SQLite projection store
10. **projections/*.py** - Projection builders
11. **contracts/ADR-001-event-sourcing-cqrs.md** - This decision ✅

### Updated Files (v2.0 → v3.0)

1. **ports/i_repository.py** - Generic IRepository<T, TId>
2. **domain/entities/problem_statement.py** - Event-sourced aggregate
3. **application/use_cases/*.py** - Use Unit of Work
4. **contracts/diagrams/ports-interfaces.md** - Add new interfaces
5. **contracts/diagrams/domain-model.md** - Add events
6. **contracts/README.md** - Update to v3.0
7. **contracts/primary-ports.md** - Fix hexagon diagram ⭐
8. **contracts/schemas/events.schema.json** - NEW: Event schemas
9. **contracts/database/event-store-schema.sql** - NEW: Event store schema

---

## Next Steps

1. **Review This Architecture** - User approval required
2. **Fix Hexagon Diagram** - Add ALL relationships (primary-ports.md)
3. **Create Event Schemas** - JSON Schema for events
4. **Create Event Store Schema** - SQLite schema
5. **Update All Contracts** - Reflect v3.0 architecture
6. **Implement Event Store Adapter** - SQLite first
7. **Implement Event-Sourced Repository** - With snapshots
8. **Create Projections** - CQRS read models
9. **Performance Testing** - Validate meets baseline
10. **E2E BDD Tests** - Real MCP, no mocks

---

**Status:** Awaiting User Review
**Decision:** [ADR-001](ADR-001-event-sourcing-cqrs.md)
**Version:** 3.0.0 (Architectural Revision)
