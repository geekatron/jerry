# Jerry Design Canon v1.0

> **Document ID**: PROJ-001-e-011-v1-jerry-design-canon
> **PS ID**: PROJ-001
> **Entry ID**: e-011-v1
> **Date**: 2026-01-10
> **Version**: 1.0.0
> **Synthesizer**: ps-synthesizer agent v2.0.0 (Opus 4.5)
> **Methodology**: Braun & Clarke Thematic Analysis

---

## Document Purpose

This document establishes the **Jerry Design Canon v1.0** - the authoritative reference for all Jerry framework development. It consolidates architectural decisions, design patterns, and implementation specifications from 6 research documents into a single, definitive source of truth.

**Normative Status**: All patterns marked "MANDATORY" must be implemented exactly as specified. Patterns marked "RECOMMENDED" should be followed unless there is documented justification for deviation.

---

## L0: Executive Summary

### What is Jerry?

Jerry is a **behavior and workflow guardrails framework** designed to solve the problem of **Context Rot** - the degradation of LLM performance as context windows fill up. Jerry addresses this through:

1. **Filesystem as Infinite Memory** - State offloaded to persistent files
2. **Event Sourcing** - All state changes captured as immutable events
3. **Hexagonal Architecture** - Clean separation of domain, application, and infrastructure
4. **Graph-Ready Data Model** - Property graph primitives enabling future graph database migration

### Architectural Foundation

Jerry adopts **three complementary patterns** validated by industry best practices:

| Pattern | Purpose | Enforcement |
|---------|---------|-------------|
| **Hexagonal Architecture** | Isolate domain from infrastructure | HARD |
| **Event Sourcing** | Capture all state changes as events | HARD |
| **CQRS** | Separate read and write models | HARD |

These patterns work together: Commands modify aggregates through domain events (Event Sourcing), events are stored immutably (Hexagonal via ports), and projections provide read-optimized views (CQRS).

### What Makes Jerry Unique?

1. **Graph-Ready Identities** - All entity IDs extend `VertexId`, enabling future migration to native graph databases without changing domain logic

2. **CloudEvents 1.0 Compliance** - Every domain event follows the CNCF standard, enabling interoperability with external event-driven systems

3. **Sub-Agent Permission Model** - First-class support for Claude sub-agents with restricted permissions (no COMPLETE, DELETE, or CONSENT operations)

4. **Dual Storage Model** - Event store as source of truth, graph store as derived navigation layer

### Key Architectural Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Primary Aggregate Root | Task | Small aggregate per Vernon's rules; most frequent operations |
| Persistence | SQLite | Zero deployment complexity; file-portable |
| Graph Library | NetworkX | In-process; Python-native |
| Event Envelope | CloudEvents 1.0 | CNCF standard; external system interop |
| Snapshot Frequency | Every 10 events | Balance of rebuild cost vs storage |

---

## L1: Technical Pattern Catalog

### 1. Identity Patterns

#### PAT-ID-001: VertexId (Base Identity Class)

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-ID-001 |
| **Name** | VertexId |
| **Category** | Identity Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L112-122), e-002 (L107-143) |

**Context**: All domain entities require unique identifiers that are type-safe and graph-compatible.

**Problem**: Raw strings or UUIDs lack type safety (TaskId could be mistakenly used as PhaseId) and don't carry semantic meaning.

**Solution**: Create a frozen dataclass base class that validates UUID format and provides value equality semantics.

```python
from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class VertexId:
    """
    Graph-ready abstraction for all entity IDs.
    Immutable value object with UUID format validation.
    """
    value: str

    def __post_init__(self) -> None:
        # Validate UUID format (raises ValueError if invalid)
        UUID(self.value.replace("-", "")[:32], version=4)

    def __str__(self) -> str:
        return self.value

    def __hash__(self) -> int:
        return hash(self.value)
```

**Consequences**:
- (+) Type safety prevents mixing ID types
- (+) Graph-compatible for future TinkerPop migration
- (+) Immutable guarantees consistency
- (-) Slightly more verbose than raw strings

---

#### PAT-ID-002: Domain-Specific IDs

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-ID-002 |
| **Name** | Domain-Specific IDs |
| **Category** | Identity Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L124-136), e-002 (L109-136) |

**Context**: Different entity types need distinguishable identifiers with human-readable prefixes.

**Problem**: Generic UUIDs are hard to identify and debug; mixing entity types causes subtle bugs.

**Solution**: Create type-specific subclasses with deterministic format prefixes.

**ID Hierarchy**:
```python
VertexId (base)
├── TaskId      # Format: "TASK-{uuid8}"     Example: TASK-a1b2c3d4
├── PhaseId     # Format: "PHASE-{uuid8}"    Example: PHASE-e5f6g7h8
├── PlanId      # Format: "PLAN-{uuid8}"     Example: PLAN-xyz98765
├── SubtaskId   # Format: "TASK-{parent}.{seq}"  Example: TASK-a1b2c3d4.1
├── KnowledgeId # Format: "KNOW-{uuid8}"     Example: KNOW-pat00001
├── ActorId     # Format: "ACTOR-{type}-{id}"    Example: ACTOR-CLAUDE-main
└── EventId     # Format: "EVT-{uuid}"       Example: EVT-a1b2c3d4
```

**Implementation**:
```python
@dataclass(frozen=True)
class TaskId(VertexId):
    """Strongly typed Task identifier."""

    @classmethod
    def generate(cls) -> 'TaskId':
        return cls(f"TASK-{uuid4().hex[:8]}")

    @classmethod
    def from_string(cls, value: str) -> 'TaskId':
        if not value.startswith("TASK-"):
            raise ValueError(f"Invalid TaskId format: {value}")
        return cls(value)
```

**Consequences**:
- (+) Self-documenting IDs in logs and debug output
- (+) Type system prevents ID mixing at compile time
- (+) Enables pattern matching in CLI parsing
- (-) Slightly longer identifiers

---

#### PAT-ID-003: JerryUri

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-ID-003 |
| **Name** | JerryUri |
| **Category** | Identity Pattern |
| **Status** | RECOMMENDED |
| **Sources** | e-001 (L137-148) |

**Context**: Cross-system entity references need a standardized URI format.

**Problem**: Different systems reference entities differently; no canonical format exists.

**Solution**: Define a URI scheme for Jerry entities.

**Format**:
```
jerry://entity_type/id[/sub_entity/sub_id]

Examples:
jerry://task/a1b2c3d4
jerry://plan/xyz98765/phase/001
jerry://knowledge/pattern/p-001
```

**Implementation**:
```python
@dataclass(frozen=True)
class JerryUri:
    """URI-based entity reference for cross-system identification."""
    entity_type: str
    entity_id: str
    sub_entity_type: str | None = None
    sub_entity_id: str | None = None

    def __str__(self) -> str:
        base = f"jerry://{self.entity_type}/{self.entity_id}"
        if self.sub_entity_type:
            base += f"/{self.sub_entity_type}/{self.sub_entity_id}"
        return base

    @classmethod
    def parse(cls, uri: str) -> 'JerryUri':
        # Parse jerry:// URI format
        ...
```

---

#### PAT-ID-004: EdgeId

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-ID-004 |
| **Name** | EdgeId |
| **Category** | Identity Pattern |
| **Status** | MANDATORY |
| **Sources** | e-002 (L120-122) |

**Context**: Graph edges need deterministic identifiers for retrieval and updates.

**Problem**: Edges are relationships, not entities; need a consistent naming scheme.

**Solution**: Generate edge IDs from source vertex, label, and target vertex.

**Format**:
```
{outV}--{label}-->{inV}

Example:
PHASE-001--CONTAINS-->TASK-001
TASK-ABC--DEPENDS_ON-->TASK-XYZ
```

**Implementation**:
```python
@dataclass(frozen=True)
class EdgeId:
    """Generated identifier for graph edges."""
    source_id: VertexId
    label: str
    target_id: VertexId

    def __str__(self) -> str:
        return f"{self.source_id}--{self.label}-->{self.target_id}"
```

---

### 2. Entity Patterns

#### PAT-ENT-001: IAuditable Interface

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-ENT-001 |
| **Name** | IAuditable |
| **Category** | Entity Pattern |
| **Status** | MANDATORY |
| **Sources** | e-003 (L37-38, L347-349), e-004 (L88-89) |

**Context**: All entities need creation and modification tracking for audit purposes.

**Problem**: Audit trails require consistent metadata across all entities.

**Solution**: Define a protocol for audit metadata.

```python
from typing import Protocol
from datetime import datetime

class IAuditable(Protocol):
    """Tracking metadata for entity creation and modification."""
    created_by: str      # User email, "Claude", or "System"
    created_at: datetime
    updated_by: str
    updated_at: datetime
```

---

#### PAT-ENT-002: IVersioned Interface

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-ENT-002 |
| **Name** | IVersioned |
| **Category** | Entity Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L110-119), e-003 (L135, L197) |

**Context**: Concurrent modifications to the same entity can cause lost updates.

**Problem**: Without version tracking, last-write-wins silently loses changes.

**Solution**: Optimistic concurrency control via version tracking.

```python
class IVersioned(Protocol):
    """Optimistic concurrency control via version tracking."""
    version: int  # Incremented on each save

    def get_expected_version(self) -> int:
        """Return version for concurrency check."""
        return self.version
```

---

#### PAT-ENT-003: AggregateRoot Base Class

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-ENT-003 |
| **Name** | AggregateRoot |
| **Category** | Entity Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L36-39), e-003 (L375-399), e-005 (L36-55, L199-239) |

**Context**: Domain aggregates need event sourcing support with consistent behavior.

**Problem**: Each aggregate implementing event sourcing independently leads to inconsistency.

**Solution**: Abstract base class with event raising, application, and history loading.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class AggregateRoot(ABC):
    """
    Base class for event-sourced aggregates.

    Implements Vaughn Vernon's 4 Rules:
    1. Model true invariants in consistency boundaries
    2. Design small aggregates
    3. Reference other aggregates by ID only
    4. Use eventual consistency outside boundaries
    """
    _id: VertexId
    _version: int = 0
    _uncommitted_events: List['DomainEvent'] = field(default_factory=list)

    # IAuditable metadata
    _created_by: str = "System"
    _created_at: datetime = field(default_factory=datetime.utcnow)
    _updated_by: str = "System"
    _updated_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def id(self) -> VertexId:
        return self._id

    @property
    def version(self) -> int:
        return self._version

    def _raise_event(self, event: 'DomainEvent') -> None:
        """Add event to uncommitted list and apply to state."""
        self._uncommitted_events.append(event)
        self._apply(event)
        self._version += 1
        self._updated_at = datetime.utcnow()

    @abstractmethod
    def _apply(self, event: 'DomainEvent') -> None:
        """Apply event to aggregate state."""
        pass

    def get_uncommitted_events(self) -> List['DomainEvent']:
        """Return events not yet persisted."""
        return list(self._uncommitted_events)

    def mark_events_committed(self) -> None:
        """Clear uncommitted events after persistence."""
        self._uncommitted_events.clear()

    @classmethod
    def load_from_history(cls, events: List['DomainEvent']) -> 'AggregateRoot':
        """Rebuild aggregate state by replaying events."""
        if not events:
            raise ValueError("Cannot load from empty event history")

        # Create instance from first event
        aggregate = cls._create_from_event(events[0])

        # Replay remaining events
        for event in events[1:]:
            aggregate._apply(event)
            aggregate._version += 1

        return aggregate

    @classmethod
    @abstractmethod
    def _create_from_event(cls, event: 'DomainEvent') -> 'AggregateRoot':
        """Factory method for creating instance from creation event."""
        pass
```

---

#### PAT-ENT-004: Vertex Base Class

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-ENT-004 |
| **Name** | Vertex |
| **Category** | Entity Pattern |
| **Status** | MANDATORY |
| **Sources** | e-002 (L24-30) |

**Context**: Property graph model requires base node class.

**Problem**: Graph nodes need consistent structure for traversal and storage.

**Solution**: Base dataclass with id, label, and properties.

```python
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class Vertex:
    """Base node class for property graph model."""
    id: VertexId
    label: str
    properties: Dict[str, Any] = field(default_factory=dict)
```

---

#### PAT-ENT-005: Edge Base Class

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-ENT-005 |
| **Name** | Edge |
| **Category** | Entity Pattern |
| **Status** | MANDATORY |
| **Sources** | e-002 (L24-30) |

**Context**: Property graph model requires base relationship class.

**Problem**: Graph relationships need consistent structure.

**Solution**: Base dataclass with id, label, source, target, and properties.

```python
@dataclass
class Edge:
    """Base relationship class for property graph model."""
    id: EdgeId
    label: str
    outV: VertexId  # Source vertex
    inV: VertexId   # Target vertex
    properties: Dict[str, Any] = field(default_factory=dict)
```

---

### 3. Aggregate Patterns

#### PAT-AGG-001: Task Aggregate Root

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-AGG-001 |
| **Name** | Task Aggregate |
| **Category** | Aggregate Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L191-266), e-002 (L50-52) |

**Context**: Tasks are the primary unit of work in Jerry.

**Problem**: Work items need rich state management with transitions and invariants.

**Solution**: Event-sourced aggregate with status state machine.

**State Transitions**:
```
PENDING -> IN_PROGRESS       (start())
IN_PROGRESS -> COMPLETED     (complete())
IN_PROGRESS -> BLOCKED       (block(reason))
BLOCKED -> IN_PROGRESS       (unblock())
PENDING -> CANCELLED         (cancel())
COMPLETED -> any             (INVALID)
CANCELLED -> any             (INVALID)
```

**Invariants**:
- BLOCKED status MUST have blocker_reason
- Due date in past raises ValidationError on create
- Title max length: 200 characters
- Completed task has completed_at <= updated_at

**Domain Events**:
```python
TaskCreated(task_id, title, description, priority, created_at)
TaskStarted(task_id)
TaskCompleted(task_id, completed_at)
TaskBlocked(task_id, reason)
TaskUnblocked(task_id)
TaskCancelled(task_id)
TaskAssignedToPhase(task_id, phase_id)
```

---

#### PAT-AGG-002: Phase Aggregate Root

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-AGG-002 |
| **Name** | Phase Aggregate |
| **Category** | Aggregate Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L278-327), e-002 (L50-52) |

**Context**: Phases group tasks within a plan.

**Problem**: Need logical grouping with ordering and completion tracking.

**Solution**: Aggregate that references tasks by ID only (Vernon Rule 3).

**State Transitions**:
```
NOT_STARTED -> ACTIVE        (activate())
ACTIVE -> COMPLETED          (complete())
```

**Key Behaviors**:
- `add_task(task_id)` - Adds TaskId reference, emits TaskAddedToPhase
- `remove_task(task_id)` - Removes TaskId reference, emits TaskRemovedFromPhase
- Cannot add task to COMPLETED phase
- `complete(force=False)` - Validates all tasks complete (unless force=True)

**Critical Design Decision**: Phase stores `Set[TaskId]`, NOT `List[Task]`. This follows Vernon's Rule 3: reference other aggregates by ID only.

---

#### PAT-AGG-003: Plan Aggregate Root

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-AGG-003 |
| **Name** | Plan Aggregate |
| **Category** | Aggregate Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L329-379), e-002 (L50-52), e-004 (L74-100) |

**Context**: Plans are top-level containers for phases.

**Problem**: Need hierarchical organization with ordering and lifecycle.

**Solution**: Aggregate with ordered phase references and assumption tracking.

**State Transitions**:
```
DRAFT -> ACTIVE              (activate())
ACTIVE -> COMPLETED          (complete())
COMPLETED -> ARCHIVED        (archive())
ACTIVE -> DRAFT              (pause())
```

**Key Behaviors**:
- `add_phase(phase_id, order)` - Adds PhaseId with order index
- `reorder_phases(ordering)` - Updates order_index values
- `track_assumption(text)` - Adds assumption to set
- `validate_assumption(text, evidence)` - Marks assumption validated
- Cannot add phase to COMPLETED plan
- Cannot remove last phase (invariant: PlanRequiresPhase)

---

#### PAT-AGG-004: Knowledge Aggregates

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-AGG-004 |
| **Name** | Knowledge Aggregates |
| **Category** | Aggregate Pattern |
| **Status** | RECOMMENDED |
| **Sources** | e-001 (L1309-1411), e-004 (L152-163) |

**Context**: Knowledge management domain with patterns, lessons, and assumptions.

**Problem**: Organizational learning needs structured capture and retrieval.

**Solution**: Three knowledge aggregate types extending KnowledgeItem base.

**Knowledge Types**:

| Type | Fields | Key Behaviors |
|------|--------|---------------|
| **Pattern** | context, problem, solution, consequences | `apply()` increments count, emits PatternApplied |
| **Lesson** | observation, reflection, action, source_task_id | `materialize()` converts to Pattern |
| **Assumption** | hypothesis, validation_criteria, status | `validate(evidence)`, `invalidate(evidence)` |

**Assumption Status**:
```
UNTESTED -> VALIDATED       (validate(evidence))
UNTESTED -> INVALIDATED     (invalidate(evidence))
```

---

### 4. Event Patterns

#### PAT-EVT-001: CloudEvents 1.0 Envelope

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-EVT-001 |
| **Name** | CloudEvents Envelope |
| **Category** | Event Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L79-96), e-002 (L257-275), e-005 (L264) |

**Context**: Domain events need standardized format for interoperability.

**Problem**: Custom event formats prevent integration with external systems.

**Solution**: CNCF CloudEvents 1.0 specification.

**Envelope Structure**:
```json
{
  "specversion": "1.0",
  "type": "com.jerry.task.completed.v1",
  "source": "/jerry/tasks/TASK-ABC123",
  "id": "EVT-a1b2c3d4",
  "time": "2026-01-10T14:30:00Z",
  "subject": "TASK-ABC123",
  "datacontenttype": "application/json",
  "data": {
    "task_id": "TASK-ABC123",
    "completed_at": "2026-01-10T14:30:00Z",
    "completed_by": {"type": "CLAUDE", "id": "main"}
  }
}
```

**Type Naming Convention**:
```
com.jerry.{aggregate}.{action}.v{version}

Examples:
com.jerry.task.created.v1
com.jerry.task.completed.v1
com.jerry.phase.activated.v1
com.jerry.plan.archived.v1
```

---

#### PAT-EVT-002: DomainEvent Base Class

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-EVT-002 |
| **Name** | DomainEvent Base |
| **Category** | Event Pattern |
| **Status** | MANDATORY |
| **Sources** | e-003 (L337-358) |

**Context**: All domain events share common metadata.

**Problem**: Inconsistent event structures complicate serialization and handling.

**Solution**: Abstract base class with CloudEvents-compatible fields.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass(frozen=True)
class DomainEvent(ABC):
    """
    Base class for all domain events.
    Events are immutable, past-tense facts.
    """
    event_id: str = field(default_factory=lambda: f"EVT-{uuid.uuid4().hex[:8]}")
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    caused_by: str = "Claude"  # User email, "Claude", or "System"

    @property
    @abstractmethod
    def event_type(self) -> str:
        """CloudEvents type field (e.g., 'com.jerry.task.created.v1')."""
        pass

    @property
    @abstractmethod
    def subject(self) -> str:
        """CloudEvents subject field (aggregate ID)."""
        pass

    def to_cloud_event(self) -> dict:
        """Convert to CloudEvents 1.0 envelope."""
        return {
            "specversion": "1.0",
            "type": self.event_type,
            "source": f"/jerry/{self.__class__.__name__.lower()}",
            "id": self.event_id,
            "time": self.occurred_at.isoformat() + "Z",
            "subject": self.subject,
            "datacontenttype": "application/json",
            "data": self._get_data()
        }

    @abstractmethod
    def _get_data(self) -> dict:
        """Return event-specific data payload."""
        pass
```

---

#### PAT-EVT-003: Work Tracker Events

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-EVT-003 |
| **Name** | Work Tracker Events |
| **Category** | Event Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L399-409), e-002 (L278-289), e-003 (L361-371) |

**Event Catalog**:

| Event | Fields | Aggregate |
|-------|--------|-----------|
| `TaskCreated` | task_id, title, description, priority | Task |
| `TaskStarted` | task_id | Task |
| `TaskCompleted` | task_id, completed_at | Task |
| `TaskBlocked` | task_id, reason | Task |
| `TaskUnblocked` | task_id | Task |
| `TaskCancelled` | task_id | Task |
| `TaskAssignedToPhase` | task_id, phase_id | Task |
| `TaskRemovedFromPhase` | task_id, phase_id | Task |
| `PhaseCreated` | phase_id, name, plan_id | Phase |
| `PhaseActivated` | phase_id | Phase |
| `PhaseCompleted` | phase_id | Phase |
| `TaskAddedToPhase` | phase_id, task_id | Phase |
| `TaskRemovedFromPhase` | phase_id, task_id | Phase |
| `PlanCreated` | plan_id, name | Plan |
| `PlanActivated` | plan_id | Plan |
| `PlanCompleted` | plan_id | Plan |
| `PlanArchived` | plan_id | Plan |

---

#### PAT-EVT-004: IEventStore Port

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-EVT-004 |
| **Name** | IEventStore |
| **Category** | Event Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L88-96), e-003 (L189-227), e-005 (L60-68) |

**Context**: Event sourcing requires append-only event storage.

**Problem**: Events must be immutable and support optimistic concurrency.

**Solution**: Port interface for event store operations.

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

@dataclass(frozen=True)
class StreamEvent:
    """Event with stream metadata."""
    event: DomainEvent
    stream_id: str
    version: int
    timestamp: datetime
    metadata: Dict[str, Any]

class IEventStore(ABC):
    """
    Append-only event log. Core of Event Sourcing architecture.
    Events table has NO UPDATE/DELETE operations.
    """

    @abstractmethod
    def append(
        self,
        stream_id: str,
        events: List[DomainEvent],
        expected_version: int,
        metadata: Dict[str, Any] = None
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
        """Get current version of stream (last event number)."""
        pass

    @abstractmethod
    def get_all_streams(self) -> List[str]:
        """Get all stream IDs (for projections rebuild)."""
        pass
```

---

### 5. CQRS Patterns

#### PAT-CQRS-001: Command Pattern

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-CQRS-001 |
| **Name** | Command Pattern |
| **Category** | CQRS Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L57-65), e-003 (L125-138), e-005 (L93-108) |

**Context**: Write operations need explicit intent capture.

**Problem**: Method calls don't capture the full context of the operation.

**Solution**: Immutable command objects with all required data.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class CreateTaskCommand:
    """Command to create a new task."""
    title: str
    description: str
    priority: Priority
    phase_id: PhaseId | None = None

@dataclass(frozen=True)
class CompleteTaskCommand:
    """Command to complete a task."""
    task_id: TaskId
    notes: str | None = None

@dataclass(frozen=True)
class TransitionTaskCommand:
    """Command to transition task status."""
    task_id: TaskId
    target_status: TaskStatus
    reason: str | None = None  # Required for BLOCKED
```

**Command Handler Pattern**:
```python
class CreateTaskCommandHandler:
    def __init__(self, repository: ITaskRepository, uow: IUnitOfWork):
        self._repository = repository
        self._uow = uow

    def handle(self, command: CreateTaskCommand) -> TaskId:
        with self._uow:
            # 1. Create aggregate via factory
            task = Task.create(
                title=command.title,
                description=command.description,
                priority=command.priority
            )

            # 2. Save aggregate (appends events)
            self._repository.save(task)

            # 3. Commit transaction
            self._uow.commit()

            # 4. Return result
            return task.id
```

---

#### PAT-CQRS-002: Query Pattern

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-CQRS-002 |
| **Name** | Query Pattern |
| **Category** | CQRS Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L53-56), e-003 (L103-111, L319-333), e-005 (L118-135) |

**Context**: Read operations need optimization separate from writes.

**Problem**: Reading from aggregates is expensive and couples reads to write model.

**Solution**: Query objects with DTOs from projections.

```python
@dataclass(frozen=True)
class GetTaskQuery:
    """Query to retrieve a single task."""
    task_id: TaskId

@dataclass(frozen=True)
class ListTasksQuery:
    """Query to list tasks with filters."""
    phase_id: PhaseId | None = None
    status: TaskStatus | None = None
    limit: int = 50
    offset: int = 0

# Query Handler reads from projection, not aggregate
class ListTasksQueryHandler:
    def __init__(self, projection_store: IProjectionStore):
        self._projection_store = projection_store

    def handle(self, query: ListTasksQuery) -> TaskListResult:
        # Read from pre-computed projection
        return self._projection_store.list_tasks(
            phase_id=query.phase_id,
            status=query.status,
            limit=query.limit,
            offset=query.offset
        )
```

**Critical Rule**: Query handlers NEVER return domain entities. They return DTOs from projections.

---

#### PAT-CQRS-003: Projection Pattern

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-CQRS-003 |
| **Name** | Projection Pattern |
| **Category** | CQRS Pattern |
| **Status** | MANDATORY |
| **Sources** | e-003 (L136-137, L402-414), e-005 (L118-135) |

**Context**: Read models need to be optimized for specific query patterns.

**Problem**: Single data model can't optimize for both writes and reads.

**Solution**: Event-driven projections that update on domain events.

```python
class IProjection(ABC):
    """Read model projection. Eventually consistent with write side."""

    @abstractmethod
    def project(self, event: DomainEvent) -> None:
        """Apply event to projection."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset projection (for rebuild from events)."""
        pass

    @property
    @abstractmethod
    def last_event_position(self) -> int:
        """Track last processed event for resumption."""
        pass

class TaskListProjection(IProjection):
    """Projection for fast task list queries."""

    def project(self, event: DomainEvent) -> None:
        match event:
            case TaskCreated():
                self._add_task(event.task_id, event.title, event.priority)
            case TaskCompleted():
                self._update_status(event.task_id, "COMPLETED")
            case TaskAssignedToPhase():
                self._update_phase(event.task_id, event.phase_id)
```

**Projection Types**:
- `TaskListProjection` - Fast list queries
- `TaskDetailProjection` - Single item retrieval
- `PhaseProgressProjection` - Aggregated progress stats
- `PlanOverviewProjection` - Plan summary with phase counts

---

### 6. Repository Patterns

#### PAT-REPO-001: Generic Repository Port

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-REPO-001 |
| **Name** | IRepository<T, TId> |
| **Category** | Repository Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L100-119), e-003 (L153-186), e-005 (L171-187) |

**Context**: Domain needs abstraction for aggregate persistence.

**Problem**: Direct infrastructure access couples domain to technology choices.

**Solution**: Generic port interface for repositories.

```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional

TAggregate = TypeVar('TAggregate', bound=AggregateRoot)
TId = TypeVar('TId', bound=VertexId)

class IRepository(ABC, Generic[TAggregate, TId]):
    """
    Domain abstraction for accessing Aggregate Roots.

    Event-sourced implementation:
    - save() extracts uncommitted events, appends to event stream
    - find_by_id() loads events, replays to rebuild state
    """

    @abstractmethod
    def save(self, aggregate: TAggregate) -> None:
        """Persist aggregate by appending uncommitted events."""
        pass

    @abstractmethod
    def find_by_id(self, id: TId) -> Optional[TAggregate]:
        """Retrieve aggregate by ID, rebuilding from events."""
        pass

    @abstractmethod
    def exists(self, id: TId) -> bool:
        """Check if aggregate exists."""
        pass

# Type-specific repositories
class ITaskRepository(IRepository[Task, TaskId]):
    """Repository for Task aggregates."""
    pass

class IPhaseRepository(IRepository[Phase, PhaseId]):
    """Repository for Phase aggregates."""
    pass

class IPlanRepository(IRepository[Plan, PlanId]):
    """Repository for Plan aggregates."""
    pass
```

---

#### PAT-REPO-002: Unit of Work Pattern

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-REPO-002 |
| **Name** | Unit of Work |
| **Category** | Repository Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L115-119), e-003 (L255-289) |

**Context**: Multiple operations need atomic transaction boundary.

**Problem**: Partial commits leave system in inconsistent state.

**Solution**: Transaction boundary that coordinates commits.

```python
class IUnitOfWork(ABC):
    """
    Atomic commit boundary.
    Coordinates repository changes and event publishing.
    One UoW per application command.
    """

    @abstractmethod
    def __enter__(self) -> 'IUnitOfWork':
        """Start unit of work."""
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """On success: commit. On failure: rollback."""
        pass

    @abstractmethod
    def register_aggregate(self, aggregate: AggregateRoot) -> None:
        """Register aggregate for commit tracking."""
        pass

    @abstractmethod
    def commit(self) -> None:
        """
        Commit all changes atomically.
        1. Append events to event store
        2. Update snapshots if needed
        3. Publish events to event bus
        """
        pass

    @abstractmethod
    def rollback(self) -> None:
        """Rollback all pending changes."""
        pass
```

---

#### PAT-REPO-003: Snapshot Pattern

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-REPO-003 |
| **Name** | Snapshot Pattern |
| **Category** | Repository Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L95-96), e-003 (L229-253), e-005 (L73-81) |

**Context**: Aggregates with many events are slow to rebuild.

**Problem**: Replaying 1000 events on every load is expensive.

**Solution**: Periodic snapshots with incremental event replay.

```python
class ISnapshotStore(ABC):
    """
    Snapshot storage for performance optimization.

    CRITICAL: Snapshots are CACHE - events are source of truth.
    If snapshot is corrupted, rebuild from events.
    """

    @abstractmethod
    def save_snapshot(
        self,
        stream_id: str,
        aggregate: AggregateRoot,
        at_version: int
    ) -> None:
        """Save aggregate snapshot at specific version."""
        pass

    @abstractmethod
    def get_snapshot(self, stream_id: str) -> Optional[Tuple[AggregateRoot, int]]:
        """
        Get latest snapshot.
        Returns (aggregate_state, version) or None if no snapshot.
        """
        pass

# Snapshot Strategy
SNAPSHOT_FREQUENCY = 10  # Snapshot every 10 events

def load_aggregate(stream_id: str) -> AggregateRoot:
    # 1. Try to load snapshot
    snapshot_result = snapshot_store.get_snapshot(stream_id)

    if snapshot_result:
        aggregate, snapshot_version = snapshot_result
        # 2. Load events after snapshot
        events = event_store.read(stream_id, from_version=snapshot_version + 1)
    else:
        # 3. Load all events
        events = event_store.read(stream_id)
        aggregate = None

    # 4. Replay events to rebuild/update state
    if aggregate is None:
        aggregate = AggregateRoot.load_from_history(events)
    else:
        for event in events:
            aggregate._apply(event.event)

    return aggregate
```

---

### 7. Graph Patterns

#### PAT-GRAPH-001: IGraphStore Port

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-GRAPH-001 |
| **Name** | IGraphStore |
| **Category** | Graph Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L354-367), e-002 (L148-179) |

**Context**: Graph operations need abstraction for portability.

**Problem**: Direct NetworkX usage couples domain to specific library.

**Solution**: Port interface for graph storage operations.

```python
class IGraphStore(ABC):
    """Secondary port for graph persistence operations."""

    @abstractmethod
    def add_vertex(self, vertex: Vertex) -> None:
        """Add node to graph."""
        pass

    @abstractmethod
    def get_vertex(self, id: VertexId) -> Optional[Vertex]:
        """Retrieve vertex by ID."""
        pass

    @abstractmethod
    def update_vertex(self, vertex: Vertex) -> None:
        """Update vertex properties."""
        pass

    @abstractmethod
    def remove_vertex(self, id: VertexId) -> bool:
        """Remove vertex and all connected edges."""
        pass

    @abstractmethod
    def add_edge(self, edge: Edge) -> None:
        """Create directed relationship between vertices."""
        pass

    @abstractmethod
    def remove_edge(self, id: EdgeId) -> bool:
        """Remove edge by ID."""
        pass

    @abstractmethod
    def get_edges(
        self,
        vertex_id: VertexId,
        direction: str = "both",  # "in", "out", "both"
        label: str | None = None
    ) -> List[Edge]:
        """Get edges connected to vertex."""
        pass

    @abstractmethod
    def traverse(
        self,
        start: VertexId,
        edge_label: str,
        direction: str = "out",
        depth: int = 1
    ) -> List[Vertex]:
        """Traverse graph following edges."""
        pass
```

---

#### PAT-GRAPH-002: Edge Labels

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-GRAPH-002 |
| **Name** | Edge Labels |
| **Category** | Graph Pattern |
| **Status** | MANDATORY |
| **Sources** | e-002 (L57-66) |

**Context**: Graph relationships need semantic meaning.

**Problem**: Generic edges don't capture relationship semantics.

**Solution**: Defined edge label vocabulary.

**Edge Label Catalog**:

| Label | Semantics | Direction | Example |
|-------|-----------|-----------|---------|
| `CONTAINS` | Parent has child | parent -> child | Phase CONTAINS Task |
| `BELONGS_TO` | Child references parent | child -> parent | Task BELONGS_TO Phase |
| `DEPENDS_ON` | Dependency relationship | source -> target | Task DEPENDS_ON Task |
| `EMITTED` | Aggregate produced event | aggregate -> event | Task EMITTED TaskCompleted |
| `PERFORMED_BY` | Actor attribution | event -> actor | Event PERFORMED_BY Actor |
| `REFERENCES` | Evidence linkage | item -> evidence | Task REFERENCES Evidence |
| `APPLIES` | Pattern application | item -> pattern | Task APPLIES Pattern |

```python
class EdgeLabels:
    """Constants for graph edge labels."""
    CONTAINS = "CONTAINS"
    BELONGS_TO = "BELONGS_TO"
    DEPENDS_ON = "DEPENDS_ON"
    EMITTED = "EMITTED"
    PERFORMED_BY = "PERFORMED_BY"
    REFERENCES = "REFERENCES"
    APPLIES = "APPLIES"
```

---

#### PAT-GRAPH-003: Gremlin Compatibility

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-GRAPH-003 |
| **Name** | Gremlin Compatibility |
| **Category** | Graph Pattern |
| **Status** | RECOMMENDED |
| **Sources** | e-002 (L293-317) |

**Context**: Future migration to native graph databases.

**Problem**: Custom traversal API prevents TinkerPop migration.

**Solution**: Design traversals compatible with Gremlin patterns.

**Supported Traversal Patterns**:
```gremlin
// Get all tasks in a phase
g.V('PHASE-001').out('CONTAINS').hasLabel('Task')

// Calculate phase progress by status
g.V('PHASE-001').out('CONTAINS').hasLabel('Task').group().by('status')

// Find task dependencies
g.V('TASK-001').out('DEPENDS_ON').hasLabel('Task')

// Find events emitted by aggregate
g.V('TASK-001').out('EMITTED').hasLabel('Event')

// Trace actor's actions
g.V('ACTOR-CLAUDE-main').in('PERFORMED_BY').hasLabel('Event')

// Shortest path between tasks
g.V('TASK-001').shortestPath().with(to, 'TASK-999')
```

---

### 8. Architecture Patterns

#### PAT-ARCH-001: Hexagonal Architecture

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-ARCH-001 |
| **Name** | Hexagonal Architecture |
| **Category** | Architecture Pattern |
| **Status** | MANDATORY (HARD ENFORCEMENT) |
| **Sources** | e-001 (L25-47), e-002 (L146-243), e-003 (L46-119), e-005 (L142-194) |

**Context**: Domain logic must be isolated from infrastructure.

**Problem**: Direct coupling to databases, frameworks, and external systems makes testing and evolution difficult.

**Solution**: Ports & Adapters architecture with strict layer dependencies.

**Layer Dependency Rules (HARD ENFORCEMENT)**:
```
domain/         -> ONLY stdlib imports
domain/         -> NO imports from application/, infrastructure/, interface/

application/    -> MAY import from domain/
application/    -> NO imports from infrastructure/, interface/

infrastructure/ -> MAY import from domain/, application/
infrastructure/ -> NO imports from interface/

interface/      -> MAY import from all inner layers
```

**Canonical Directory Structure**:
```
src/
├── shared_kernel/        # Cross-cutting value objects and interfaces
│   ├── identity/         # VertexId, EdgeId, etc.
│   ├── interfaces/       # IAuditable, IVersioned, etc.
│   └── events/           # DomainEvent base, CloudEvents
│
├── domain/               # Pure business logic
│   ├── aggregates/       # Task, Phase, Plan
│   │   ├── task.py
│   │   ├── phase.py
│   │   └── plan.py
│   ├── value_objects/    # Priority, Status, Tag
│   ├── events/           # Domain-specific events
│   ├── ports/            # Repository interfaces
│   └── exceptions.py
│
├── application/          # Use cases, orchestration
│   ├── commands/         # Command objects
│   ├── queries/          # Query objects
│   ├── handlers/         # Command and query handlers
│   │   ├── commands/
│   │   └── queries/
│   ├── event_handlers/   # Projection builders
│   └── dtos/             # Data transfer objects
│
├── infrastructure/       # Adapters implementing ports
│   ├── persistence/      # SQLite repositories
│   │   ├── sqlite_task_repo.py
│   │   ├── sqlite_phase_repo.py
│   │   └── sqlite_plan_repo.py
│   ├── event_store/      # SQLite event store
│   ├── graph/            # NetworkX graph store
│   └── messaging/        # In-memory event bus
│
└── interface/            # Primary adapters
    ├── cli/              # Command-line interface
    └── api/              # REST/GraphQL API (future)
```

---

#### PAT-ARCH-002: Primary vs Secondary Ports

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-ARCH-002 |
| **Name** | Primary/Secondary Ports |
| **Category** | Architecture Pattern |
| **Status** | MANDATORY |
| **Sources** | e-002 (L196-243), e-003 (L64-116) |

**Context**: Ports serve different purposes depending on direction.

**Problem**: Conflating driving and driven ports causes confusion.

**Solution**: Explicit distinction between primary and secondary ports.

**Primary Ports (Driving/Left Side)**:
- Define use case interfaces
- Called by external actors (CLI, API, sub-agents)
- Implemented by application layer handlers

```python
# Primary Port (Use Case Interface)
class ICreateTaskUseCase(ABC):
    @abstractmethod
    def execute(self, command: CreateTaskCommand) -> TaskId:
        pass
```

**Secondary Ports (Driven/Right Side)**:
- Define infrastructure contracts
- Called by application/domain layers
- Implemented by infrastructure adapters

```python
# Secondary Port (Infrastructure Contract)
class ITaskRepository(ABC):
    @abstractmethod
    def save(self, task: Task) -> None:
        pass

    @abstractmethod
    def find_by_id(self, id: TaskId) -> Optional[Task]:
        pass
```

---

#### PAT-ARCH-003: Bounded Contexts

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-ARCH-003 |
| **Name** | Bounded Contexts |
| **Category** | Architecture Pattern |
| **Status** | MANDATORY |
| **Sources** | e-004 (L69-179) |

**Context**: Large domains need explicit boundaries.

**Problem**: Monolithic models become unwieldy and tangled.

**Solution**: Four bounded contexts with defined relationships.

**Jerry Bounded Contexts**:

| Context | Aggregates | Purpose |
|---------|------------|---------|
| **Work Management** | Task, Phase, Plan | Track multi-phase work items |
| **Knowledge Capture** | Pattern, Lesson, Assumption | Capture organizational learning |
| **Identity & Access** | ConsentState | Guard completions, manage permissions |
| **Reporting** | Projections | Provide read-optimized views |

**Context Relationships**:
```
Work Management <-----> Knowledge Capture
      |                       |
      | publishes events      | references work items
      v                       v
  Reporting              Evidence
      ^                       ^
      |                       |
      | queries               | attaches to
      |                       |
Identity & Access ------------+
  (guards completions)
```

**Relationship Types**:
- Work Management -> Reporting: **Customer-Supplier** (WM publishes, Reporting consumes)
- Knowledge Capture <-> Work Management: **Shared Kernel** (common events)
- Identity & Access: **Conformist** to Work Management events

---

### 9. Testing Patterns

#### PAT-TEST-001: BDD Red/Green/Refactor

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-TEST-001 |
| **Name** | BDD Red/Green/Refactor |
| **Category** | Testing Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L41-48, L566-575) |

**Context**: Test-first development ensures quality.

**Problem**: Writing tests after implementation leads to gaps and weak assertions.

**Solution**: Strict BDD protocol with real assertions.

**Protocol**:
```
1. RED: Write failing test with REAL assertions (no placeholders)
2. GREEN: Implement MINIMUM code to pass
3. REFACTOR: Clean up while maintaining GREEN
4. REPEAT: Until acceptance criteria met
```

**Critical Rules**:
- Never write placeholder assertions (e.g., `assert True`)
- Each test must fail for the RIGHT reason before making it pass
- Refactoring must not change behavior (tests stay green)

---

#### PAT-TEST-002: Test Pyramid

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-TEST-002 |
| **Name** | Test Pyramid |
| **Category** | Testing Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L30-38, L557-564) |

**Test Type Distribution**:

| Level | Estimated Count | Focus | Dependencies |
|-------|----------------|-------|--------------|
| Unit | ~500 (many) | Single class/function | Mocked |
| Integration | ~150 (medium) | Multiple components | Real SQLite |
| Contract | ~30 (few) | Port compliance | Interface verification |
| System | ~20 (few) | Multi-operation workflows | Full stack |
| E2E | ~50 (few) | CLI to persistence | Real everything |
| Architecture | ~20 (always) | Layer dependencies | Static analysis |
| BDD | ~60 | Business scenarios | Gherkin features |
| Performance | ~15 | Baseline validation | Benchmarks |

**Total Estimated**: ~845 tests

---

#### PAT-TEST-003: Architecture Tests

| Attribute | Value |
|-----------|-------|
| **Pattern ID** | PAT-TEST-003 |
| **Name** | Architecture Tests |
| **Category** | Testing Pattern |
| **Status** | MANDATORY |
| **Sources** | e-001 (L437-453) |

**Context**: Layer dependencies must be enforced automatically.

**Problem**: Manual code review misses violations.

**Solution**: Static analysis tests for import violations.

```python
# tests/architecture/test_layer_dependencies.py

def test_domain_has_no_infrastructure_imports():
    """Domain layer must not import from infrastructure."""
    domain_files = list(Path("src/domain").rglob("*.py"))
    for file in domain_files:
        content = file.read_text()
        assert "from infrastructure" not in content
        assert "from interface" not in content
        assert "from application" not in content

def test_domain_only_stdlib_imports():
    """Domain layer may only use stdlib imports."""
    allowed_packages = {"dataclasses", "datetime", "enum", "typing", "abc", "uuid"}
    # ... validate imports
```

---

## L2: Strategic Implications

### Bounded Context Map

```
+------------------------------------------------------------------+
|                     JERRY FRAMEWORK                               |
+------------------------------------------------------------------+
|                                                                  |
|  +------------------------+      +------------------------+      |
|  |   WORK MANAGEMENT      |      |   KNOWLEDGE CAPTURE    |      |
|  |   ==================   |      |   ==================   |      |
|  |                        |      |                        |      |
|  |   Aggregates:          |<---->|   Aggregates:          |      |
|  |   - Task (Primary AR)  |shared|   - Pattern            |      |
|  |   - Phase              |kernel|   - Lesson             |      |
|  |   - Plan               |      |   - Assumption         |      |
|  |                        |      |                        |      |
|  |   Events:              |      |   Events:              |      |
|  |   - TaskCreated        |      |   - PatternApplied     |      |
|  |   - TaskCompleted      |      |   - LessonMaterialized |      |
|  |                        |      |   - AssumptionValidated|      |
|  +----------+-------------+      +-----------+------------+      |
|             |                                |                   |
|             | publishes                      | references        |
|             v                                v                   |
|  +------------------------+      +------------------------+      |
|  |   REPORTING            |      |   EVIDENCE             |      |
|  |   ==================   |      |   ==================   |      |
|  |                        |      |                        |      |
|  |   Projections:         |      |   Types:               |      |
|  |   - TaskList           |      |   - COMMAND_OUTPUT     |      |
|  |   - PhaseProgress      |      |   - FILE_REFERENCE     |      |
|  |   - PlanOverview       |      |   - TEST_RESULT        |      |
|  |                        |      |   - MANUAL_NOTE        |      |
|  +----------+-------------+      +-----------+------------+      |
|             ^                                ^                   |
|             |                                |                   |
|             | queries                        | attaches to       |
|             |                                |                   |
|  +------------------------+------------------+---------------+   |
|  |              IDENTITY & ACCESS                            |   |
|  |              ======================================       |   |
|  |                                                           |   |
|  |   ConsentState: PER_ITEM | BLANKET | SESSION_BLANKET      |   |
|  |                                                           |   |
|  |   Permissions:                                            |   |
|  |   +------------+--------------+-----------+               |   |
|  |   | Operation  | Main Agent   | Sub-agent |               |   |
|  |   +------------+--------------+-----------+               |   |
|  |   | CREATE     | YES          | YES       |               |   |
|  |   | READ       | YES          | YES       |               |   |
|  |   | WRITE      | YES          | YES       |               |   |
|  |   | COMPLETE   | YES          | NO        |               |   |
|  |   | DELETE     | YES          | NO        |               |   |
|  |   | CONSENT    | NO (Human)   | NO        |               |   |
|  |   | DELEGATE   | YES          | NO        |               |   |
|  |   +------------+--------------+-----------+               |   |
|  +-----------------------------------------------------------+   |
|                                                                  |
+------------------------------------------------------------------+
```

### Evolution Strategy

**What Can Change (Soft)**:
- Infrastructure adapters (SQLite -> PostgreSQL, NetworkX -> Neo4j)
- Projection schemas (add new fields, new projections)
- CLI commands and output formats
- Snapshot frequency tuning
- Event metadata (additional context)

**What Cannot Change (Hard)**:
- Domain model invariants
- Event types once published (versioning only)
- Layer dependency rules
- Aggregate boundary definitions
- CloudEvents 1.0 envelope structure

**Migration Path**:

| Phase | From | To | Breaking Changes |
|-------|------|-----|------------------|
| 1 | FileGraph | SQLite | None |
| 2 | SQLite | SQLite + Graph | None |
| 3 | NetworkX | Neo4j | Minor (configuration) |
| 4 | Local | Distributed | Major (event streaming) |

### Non-Negotiable Constraints

| ID | Constraint | Enforcement | Validation |
|----|------------|-------------|------------|
| NC-001 | Domain has no external imports | HARD | Architecture tests |
| NC-002 | Events are immutable | HARD | No UPDATE/DELETE on events table |
| NC-003 | Aggregates reference by ID only | HARD | Code review + tests |
| NC-004 | CloudEvents 1.0 envelope | HARD | Schema validation |
| NC-005 | Sub-agents cannot COMPLETE | HARD | Permission middleware |
| NC-006 | User consent required for CONSENT ops | HARD | Identity context check |
| NC-007 | Commands return events | HARD | Handler tests |
| NC-008 | Queries read from projections | HARD | No aggregate access in query handlers |

### Integration Points

**External System Integration**:

| System | Pattern | Purpose |
|--------|---------|---------|
| Azure DevOps | Anti-Corruption Layer | Work item sync |
| FAISS | Secondary Adapter | Semantic search |
| RDFLib | Secondary Adapter | Knowledge export |
| MCP Server | Primary Adapter | Agent communication |

**ADO Integration (ACL Architecture)**:
```
DOMAIN LAYER (Protected)
         |
         v
SECONDARY PORTS (Interfaces)
         |
         v
+-----------------------------------+
|     ANTI-CORRUPTION LAYER         |
|                                   |
|  FACADE: AdoIntegrationFacade     |
|    - Simplified API               |
|    - Orchestrates sync            |
|    - Circuit breaker              |
|                                   |
|  TRANSLATORS:                     |
|    - EntityTranslator             |
|    - StatusTranslator             |
|    - IdentityTranslator           |
+-----------------------------------+
         |
         v
AZURE DEVOPS (External System)
```

---

## Shared Kernel Specification

The Shared Kernel contains cross-cutting components that are used across all bounded contexts. These MUST exist in `src/shared_kernel/`.

### Directory Structure

```
src/shared_kernel/
├── __init__.py
├── identity/
│   ├── __init__.py
│   ├── vertex_id.py        # VertexId base class
│   ├── edge_id.py          # EdgeId generation
│   ├── domain_ids.py       # TaskId, PhaseId, PlanId, etc.
│   └── jerry_uri.py        # JerryUri value object
├── interfaces/
│   ├── __init__.py
│   ├── auditable.py        # IAuditable protocol
│   ├── versioned.py        # IVersioned protocol
│   └── specification.py    # ISpecification protocol
├── entities/
│   ├── __init__.py
│   ├── aggregate_root.py   # AggregateRoot base class
│   ├── vertex.py           # Vertex base class
│   └── edge.py             # Edge base class
├── events/
│   ├── __init__.py
│   ├── domain_event.py     # DomainEvent base class
│   ├── cloud_events.py     # CloudEvents envelope
│   └── stream_event.py     # StreamEvent wrapper
├── exceptions/
│   ├── __init__.py
│   └── domain_errors.py    # DomainError, NotFoundError, etc.
└── value_objects/
    ├── __init__.py
    ├── priority.py         # Priority enum
    ├── status.py           # Status enums (Task, Phase, Plan)
    └── tag.py              # Tag value object
```

### Component Specifications

#### 1. Identity Components (`shared_kernel/identity/`)

| Component | File | Dependencies |
|-----------|------|--------------|
| `VertexId` | `vertex_id.py` | stdlib only |
| `EdgeId` | `edge_id.py` | `VertexId` |
| `TaskId`, `PhaseId`, `PlanId`, `KnowledgeId`, `ActorId`, `EventId` | `domain_ids.py` | `VertexId` |
| `JerryUri` | `jerry_uri.py` | stdlib only |

#### 2. Interface Components (`shared_kernel/interfaces/`)

| Component | File | Dependencies |
|-----------|------|--------------|
| `IAuditable` | `auditable.py` | `typing.Protocol` |
| `IVersioned` | `versioned.py` | `typing.Protocol` |
| `ISpecification[T]` | `specification.py` | `typing.Protocol`, `Generic` |

#### 3. Entity Components (`shared_kernel/entities/`)

| Component | File | Dependencies |
|-----------|------|--------------|
| `AggregateRoot` | `aggregate_root.py` | `VertexId`, `DomainEvent`, `IAuditable`, `IVersioned` |
| `Vertex` | `vertex.py` | `VertexId` |
| `Edge` | `edge.py` | `EdgeId`, `VertexId` |

#### 4. Event Components (`shared_kernel/events/`)

| Component | File | Dependencies |
|-----------|------|--------------|
| `DomainEvent` | `domain_event.py` | stdlib only |
| `CloudEventEnvelope` | `cloud_events.py` | `DomainEvent` |
| `StreamEvent` | `stream_event.py` | `DomainEvent` |

#### 5. Exception Components (`shared_kernel/exceptions/`)

```python
# domain_errors.py
class DomainError(Exception):
    """Base class for domain errors."""
    pass

class NotFoundError(DomainError):
    """Entity not found."""
    def __init__(self, entity_type: str, entity_id: str):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} '{entity_id}' not found")

class InvalidStateError(DomainError):
    """Operation invalid for current state."""
    def __init__(self, current_state: str, attempted_action: str):
        self.current_state = current_state
        self.attempted_action = attempted_action
        super().__init__(f"Cannot {attempted_action} from state {current_state}")

class InvalidStateTransition(InvalidStateError):
    """State transition not allowed."""
    def __init__(self, from_state: str, to_state: str):
        super().__init__(from_state, f"transition to {to_state}")
        self.from_state = from_state
        self.to_state = to_state

class InvariantViolation(DomainError):
    """Domain invariant violated."""
    def __init__(self, invariant_name: str, details: str):
        self.invariant_name = invariant_name
        super().__init__(f"Invariant '{invariant_name}' violated: {details}")

class ConcurrencyError(DomainError):
    """Optimistic concurrency conflict."""
    def __init__(self, expected_version: int, actual_version: int):
        self.expected_version = expected_version
        self.actual_version = actual_version
        super().__init__(
            f"Concurrency conflict: expected version {expected_version}, "
            f"actual version {actual_version}"
        )

class ValidationError(DomainError):
    """Validation failed."""
    def __init__(self, field_name: str, message: str):
        self.field_name = field_name
        super().__init__(f"Validation failed for '{field_name}': {message}")
```

#### 6. Value Object Components (`shared_kernel/value_objects/`)

```python
# priority.py
from enum import Enum

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

    def __lt__(self, other: 'Priority') -> bool:
        return self.value < other.value

    @classmethod
    def from_string(cls, value: str) -> 'Priority':
        return cls[value.upper()]

# status.py
from enum import Enum
from typing import Set

class TaskStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

    def can_transition_to(self, target: 'TaskStatus') -> bool:
        return target in _TASK_TRANSITIONS.get(self, set())

_TASK_TRANSITIONS: dict[TaskStatus, Set[TaskStatus]] = {
    TaskStatus.PENDING: {TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED},
    TaskStatus.IN_PROGRESS: {TaskStatus.COMPLETED, TaskStatus.BLOCKED},
    TaskStatus.BLOCKED: {TaskStatus.IN_PROGRESS},
    TaskStatus.COMPLETED: set(),
    TaskStatus.CANCELLED: set(),
}

class PhaseStatus(Enum):
    NOT_STARTED = "NOT_STARTED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"

class PlanStatus(Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"
```

---

## Traceability Matrix

### Pattern to Source Document Matrix

| Pattern ID | Pattern Name | e-001 | e-002 | e-003 | e-004 | e-005 | e-006 | Validation |
|------------|--------------|-------|-------|-------|-------|-------|-------|------------|
| **Identity Patterns** |||||||
| PAT-ID-001 | VertexId | L112-122 | L107-143 | - | - | - | L26-50 | VALIDATED |
| PAT-ID-002 | Domain-Specific IDs | L124-136 | L109-136 | L100-101 | L74-100 | L215-238 | L52-82 | VALIDATED |
| PAT-ID-003 | JerryUri | L137-148 | - | - | - | - | L83-99 | RECOMMENDED |
| PAT-ID-004 | EdgeId | - | L120-122 | - | - | - | L101-115 | VALIDATED |
| **Entity Patterns** |||||||
| PAT-ENT-001 | IAuditable | - | - | L37-38, L347-349 | L88-89 | - | L121-136 | VALIDATED |
| PAT-ENT-002 | IVersioned | L110-119 | - | L135, L197 | - | - | L138-154 | VALIDATED |
| PAT-ENT-003 | AggregateRoot | L36-39 | - | L375-399 | L74-100 | L36-55, L199-239 | L156-207 | VALIDATED |
| PAT-ENT-004 | Vertex | L364-367 | L24-30 | - | - | - | L209-224 | VALIDATED |
| PAT-ENT-005 | Edge | L364-367 | L24-30 | - | - | - | L226-244 | VALIDATED |
| **Aggregate Patterns** |||||||
| PAT-AGG-001 | Task Aggregate | L191-266 | L50-52 | - | L79-81 | - | L250-280 | VALIDATED |
| PAT-AGG-002 | Phase Aggregate | L278-327 | L50-52 | - | L79-81 | - | L282-301 | VALIDATED |
| PAT-AGG-003 | Plan Aggregate | L329-379 | L50-52 | - | L74-100 | - | L303-322 | VALIDATED |
| PAT-AGG-004 | Knowledge Aggregates | L1309-1411 | - | - | L152-163 | - | L324-354 | RECOMMENDED |
| **Event Patterns** |||||||
| PAT-EVT-001 | CloudEvents Envelope | L79-96 | L257-275 | - | - | L264 | L359-384 | VALIDATED |
| PAT-EVT-002 | DomainEvent Base | L399-409 | - | L337-358 | - | - | L386-409 | VALIDATED |
| PAT-EVT-003 | Work Tracker Events | L399-409 | L278-289 | L361-371 | - | - | L411-439 | VALIDATED |
| PAT-EVT-004 | IEventStore | L88-96 | L183-185 | L189-227 | - | L60-68 | L457-490 | VALIDATED |
| **CQRS Patterns** |||||||
| PAT-CQRS-001 | Command Pattern | L57-65 | - | L125-138 | - | L93-108 | L500-526 | VALIDATED |
| PAT-CQRS-002 | Query Pattern | L53-56 | - | L103-111, L319-333 | - | L118-135 | L528-548 | VALIDATED |
| PAT-CQRS-003 | Projection Pattern | - | - | L136-137, L402-414 | - | L118-135 | L550-578 | VALIDATED |
| **Repository Patterns** |||||||
| PAT-REPO-001 | Generic Repository | L100-119 | - | L153-186 | - | L171-187 | L583-614 | VALIDATED |
| PAT-REPO-002 | Unit of Work | L115-119 | - | L255-289 | - | - | L616-656 | VALIDATED |
| PAT-REPO-003 | Snapshot Pattern | L95-96 | - | L229-253, L418-436 | - | L73-81, L324 | L672-708 | VALIDATED |
| **Graph Patterns** |||||||
| PAT-GRAPH-001 | IGraphStore | L354-367 | L148-179 | - | - | - | L715-760 | VALIDATED |
| PAT-GRAPH-002 | Edge Labels | - | L57-66 | - | - | - | L762-779 | VALIDATED |
| PAT-GRAPH-003 | Gremlin Compatibility | - | L293-317 | - | - | - | L781-804 | RECOMMENDED |
| **Architecture Patterns** |||||||
| PAT-ARCH-001 | Hexagonal Architecture | L25-47 | L146-243 | L46-119 | - | L142-194 | L808-852 | VALIDATED |
| PAT-ARCH-002 | Primary/Secondary Ports | - | L196-243 | L64-116 | - | - | L854-871 | VALIDATED |
| PAT-ARCH-003 | Bounded Contexts | - | - | - | L69-179 | - | L872-891 | VALIDATED |
| **Testing Patterns** |||||||
| PAT-TEST-001 | BDD Red/Green/Refactor | L41-48, L566-575 | - | - | - | - | - | VALIDATED |
| PAT-TEST-002 | Test Pyramid | L30-38, L557-564 | - | - | - | - | - | VALIDATED |
| PAT-TEST-003 | Architecture Tests | L437-453 | - | - | - | - | - | VALIDATED |

### Validation Status Legend

| Status | Meaning |
|--------|---------|
| VALIDATED | Pattern confirmed by multiple sources and/or industry best practices |
| RECOMMENDED | Pattern suggested by sources but not universally required |
| PROPOSED | Jerry-specific extension without external validation |

---

## Source Summary Table

| ID | Document | Focus Area | Key Contributions |
|----|----------|------------|-------------------|
| e-001 | WORKTRACKER_PROPOSAL Extraction | Domain model, CQRS, Testing | Task/Phase/Plan aggregates, Event sourcing, Test pyramid |
| e-002 | PLAN.md Graph Model | Graph architecture | VertexId hierarchy, Edge labels, Gremlin compatibility |
| e-003 | REVISED-ARCHITECTURE v3.0 | Event sourcing, Hexagonal | IEventStore, ISnapshotStore, Layer dependencies |
| e-004 | Strategic Plan v3.0 | Bounded contexts, ADO integration | 4 bounded contexts, Permission model, ACL pattern |
| e-005 | Industry Best Practices | External validation | pyeventsourcing, Axon, Vernon's rules, Martin Fowler |
| e-006 | Unified Architecture Canon | Initial synthesis | Pattern consolidation, conflict resolution |

---

## Knowledge Items Generated

### PAT: Patterns

| ID | Name | Summary |
|----|------|---------|
| PAT-ID-001 | VertexId | Graph-ready base identity class with UUID validation |
| PAT-ID-002 | Domain-Specific IDs | Type-safe ID hierarchy with deterministic formats |
| PAT-ID-003 | JerryUri | URI-based entity reference for cross-system identification |
| PAT-ID-004 | EdgeId | Generated edge identifiers from source-label-target |
| PAT-ENT-001 | IAuditable | Creation and modification tracking protocol |
| PAT-ENT-002 | IVersioned | Optimistic concurrency via version tracking |
| PAT-ENT-003 | AggregateRoot | Event-sourced aggregate base class |
| PAT-ENT-004 | Vertex | Property graph node base class |
| PAT-ENT-005 | Edge | Property graph relationship base class |
| PAT-AGG-001 | Task Aggregate | Primary work unit with status state machine |
| PAT-AGG-002 | Phase Aggregate | Task grouping with ID references only |
| PAT-AGG-003 | Plan Aggregate | Top-level container for phases |
| PAT-AGG-004 | Knowledge Aggregates | Pattern, Lesson, Assumption entities |
| PAT-EVT-001 | CloudEvents Envelope | CNCF standard event format |
| PAT-EVT-002 | DomainEvent Base | Immutable event base class |
| PAT-EVT-003 | Work Tracker Events | Task, Phase, Plan domain events |
| PAT-EVT-004 | IEventStore | Append-only event log port |
| PAT-CQRS-001 | Command Pattern | Immutable command objects |
| PAT-CQRS-002 | Query Pattern | DTOs from projections |
| PAT-CQRS-003 | Projection Pattern | Event-driven read models |
| PAT-REPO-001 | Generic Repository | Domain abstraction for persistence |
| PAT-REPO-002 | Unit of Work | Atomic transaction boundary |
| PAT-REPO-003 | Snapshot Pattern | Performance optimization for event replay |
| PAT-GRAPH-001 | IGraphStore | Graph operations port |
| PAT-GRAPH-002 | Edge Labels | Semantic relationship vocabulary |
| PAT-GRAPH-003 | Gremlin Compatibility | TinkerPop traversal patterns |
| PAT-ARCH-001 | Hexagonal Architecture | Ports & Adapters with strict dependencies |
| PAT-ARCH-002 | Primary/Secondary Ports | Driving vs driven port distinction |
| PAT-ARCH-003 | Bounded Contexts | Domain boundary definitions |
| PAT-TEST-001 | BDD Red/Green/Refactor | Test-first development protocol |
| PAT-TEST-002 | Test Pyramid | Test type distribution |
| PAT-TEST-003 | Architecture Tests | Automated layer dependency validation |

### LES: Lessons Learned

| ID | Lesson | Source |
|----|--------|--------|
| LES-001 | Small aggregates per Vernon's Rule 2 prevent contention | e-005 |
| LES-002 | Reference by ID only (Rule 3) enables eventual consistency | e-005 |
| LES-003 | CloudEvents 1.0 enables external system integration | e-001, e-002 |
| LES-004 | Snapshots every 10 events balances rebuild cost vs storage | e-003 |
| LES-005 | Sub-agent permission restrictions ensure safety | e-004 |
| LES-006 | JSON SSOT with derived markdown prevents data loss | e-004 |

### ASM: Assumptions

| ID | Assumption | Status | Validation Criteria |
|----|------------|--------|---------------------|
| ASM-001 | SQLite sufficient for single-user workstation | UNTESTED | <10K aggregates performance acceptable |
| ASM-002 | NetworkX handles <10K vertices in memory | UNTESTED | Memory <500MB, query <100ms |
| ASM-003 | Projection lag <100ms acceptable to users | UNTESTED | User testing feedback |
| ASM-004 | 32-week implementation timeline realistic | UNTESTED | Milestone completion tracking |

---

## References

### Source Documents

| ID | Title | Location |
|----|-------|----------|
| e-001 | WORKTRACKER_PROPOSAL Extraction | `projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-001-worktracker-proposal-extraction.md` |
| e-002 | PLAN.md Graph Model | `projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-002-plan-graph-model.md` |
| e-003 | REVISED-ARCHITECTURE v3.0 | `projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-003-revised-architecture-foundation.md` |
| e-004 | Strategic Plan v3.0 | `projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-004-strategic-plan-v3.md` |
| e-005 | Industry Best Practices | `projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-005-industry-best-practices.md` |
| e-006 | Unified Architecture Canon | `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-006-unified-architecture-canon.md` |

### Industry References

| Reference | URL |
|-----------|-----|
| Alistair Cockburn - Hexagonal Architecture | https://alistair.cockburn.us/hexagonal-architecture/ |
| Martin Fowler - Event Sourcing | https://martinfowler.com/eaaDev/EventSourcing.html |
| Vaughn Vernon - Implementing Domain-Driven Design | Book (2013) |
| Eric Evans - Domain-Driven Design | Book (2003) |
| CNCF CloudEvents 1.0 | https://cloudevents.io/ |
| Apache TinkerPop (Gremlin) | https://tinkerpop.apache.org/ |
| pyeventsourcing | https://github.com/pyeventsourcing/eventsourcing |
| Axon Framework | https://docs.axoniq.io/ |
| sairyss/domain-driven-hexagon | https://github.com/sairyss/domain-driven-hexagon |
| Chroma Context Rot Research | https://research.trychroma.com/context-rot |

---

*Document synthesized by ps-synthesizer agent v2.0.0 (Opus 4.5)*
*Methodology: Braun & Clarke Thematic Analysis*
*Canon established: 2026-01-10*
*Version: 1.0.0*
