# Unified Architecture Canon: Jerry Framework

> **Document ID**: PROJ-001-e-006-unified-architecture-canon
> **PS ID**: PROJ-001
> **Date**: 2026-01-09
> **Synthesizer**: ps-synthesizer agent v2.0.0
> **Sources**:
> - e-001: `docs/research/PROJ-001-e-001-worktracker-proposal-extraction.md` (WORKTRACKER_PROPOSAL)
> - e-002: `docs/research/PROJ-001-e-002-plan-graph-model.md` (PLAN.md Graph Model)
> - e-003: `docs/research/PROJ-001-e-003-revised-architecture-foundation.md` (REVISED-ARCHITECTURE v3.0)
> - e-004: `docs/research/PROJ-001-e-004-strategic-plan-v3.md` (Strategic Plan v3.0)
> - e-005: `docs/research/PROJ-001-e-005-industry-best-practices.md` (Industry Best Practices)

---

## L0: Executive Summary

The Jerry Framework adopts a **Hexagonal Architecture** with **Event Sourcing** and **CQRS** as its foundational patterns. All domain state changes are captured as immutable **CloudEvents 1.0** compliant events, with aggregate state rebuilt by replaying events (snapshots provide performance optimization). The architecture enforces strict **dependency inversion**---the domain layer has zero external dependencies, and all infrastructure concerns are isolated behind port interfaces. The framework uses a **Property Graph Model** (Vertex/Edge primitives) enabling future migration to native graph databases, with **strongly typed identities** (VertexId hierarchy) providing type safety and self-documenting code. Four bounded contexts (Work Management, Knowledge Capture, Identity & Access, Reporting) define clear separation of concerns with eventual consistency across aggregate boundaries via domain events.

---

## L1: Unified Pattern Catalog

### 1. Identity Patterns

#### 1.1 VertexId (Base Identity Class)

| Attribute | Value |
|-----------|-------|
| **Definition** | Base class for all entity identifiers, providing graph-ready abstraction |
| **Source** | e-001 (L112-122), e-002 (L107-143) |
| **Validation** | VALIDATED (Industry: Value Object pattern - Vaughn Vernon) |

**Interface:**
```python
@dataclass(frozen=True)
class VertexId:
    """Graph-ready abstraction for all entity IDs."""
    value: str  # UUID format validation

    def __post_init__(self):
        # UUID format validation
        pass
```

**Key Properties:**
- Immutable (`@dataclass(frozen=True)`)
- Value equality (not identity equality)
- UUID format validation
- Graph primitive compatibility

#### 1.2 Domain-Specific IDs (VertexId Hierarchy)

| Attribute | Value |
|-----------|-------|
| **Definition** | Type-specific ID classes extending VertexId with deterministic formats |
| **Source** | e-001 (L124-136), e-002 (L109-136) |
| **Validation** | VALIDATED (Industry: Strongly Typed IDs prevent mixing) |

**ID Hierarchy:**
```python
VertexId (base, graph primitive)
├── TaskId      "TASK-{uuid8}"
├── PhaseId     "PHASE-{uuid8}"
├── PlanId      "PLAN-{uuid8}"
├── SubtaskId   "TASK-{parent}.{seq}"   # Composite: parent + sequence
├── KnowledgeId "KNOW-{uuid8}"
├── ActorId     "ACTOR-{type}-{id}"
└── EventId     "EVT-{uuid}"
```

**Format Specifications:**
| ID Type | Format | Example |
|---------|--------|---------|
| PlanId | `PLAN-{uuid8}` | `PLAN-a1b2c3d4` |
| PhaseId | `PHASE-{uuid8}` | `PHASE-e5f6g7h8` |
| TaskId | `TASK-{uuid8}` | `TASK-ABC12345` |
| SubtaskId | `TASK-{parent}.{seq}` | `TASK-ABC123.1` |
| KnowledgeId | `KNOW-{uuid8}` | `KNOW-xyz98765` |
| ActorId | `ACTOR-{type}-{id}` | `ACTOR-CLAUDE-main` |
| EventId | `EVT-{uuid}` | `EVT-a1b2c3d4` |

#### 1.3 JerryUri

| Attribute | Value |
|-----------|-------|
| **Definition** | URI-based entity reference format for cross-system identification |
| **Source** | e-001 (L137-148) |
| **Validation** | PROPOSED (Jerry-specific) |

**Format:**
```
jerry://entity_type/id[/sub_entity/sub_id]

Examples:
jerry://task/abc-123
jerry://plan/xyz/phase/001
jerry://knowledge/pattern/p-001
```

#### 1.4 EdgeId

| Attribute | Value |
|-----------|-------|
| **Definition** | Generated identifier for graph edges |
| **Source** | e-002 (L120-122) |
| **Validation** | VALIDATED (Industry: TinkerPop standard) |

**Format:**
```
"{outV}--{label}-->{inV}"

Example:
"PHASE-001--CONTAINS-->TASK-001"
```

---

### 2. Entity Patterns

#### 2.1 IAuditable Interface

| Attribute | Value |
|-----------|-------|
| **Definition** | Tracking metadata for entity creation and modification |
| **Source** | e-003 (L37-38, L347-349), e-004 (L88-89) |
| **Validation** | VALIDATED (Industry: Standard audit pattern) |

**Interface:**
```python
class IAuditable(Protocol):
    created_by: str      # User email, "Claude", or "System"
    created_at: datetime
    updated_by: str
    updated_at: datetime
```

#### 2.2 IVersioned Interface

| Attribute | Value |
|-----------|-------|
| **Definition** | Optimistic concurrency control via version tracking |
| **Source** | e-001 (L110-119), e-003 (L135, L197) |
| **Validation** | VALIDATED (Industry: Event Sourcing standard) |

**Interface:**
```python
class IVersioned(Protocol):
    version: int  # Incremented on each save

    def get_expected_version(self) -> int:
        """Return version for concurrency check."""
        pass
```

#### 2.3 AggregateRoot Base Class

| Attribute | Value |
|-----------|-------|
| **Definition** | Base class for all aggregate roots with event sourcing support |
| **Source** | e-001 (L36-39), e-003 (L375-399), e-005 (L36-55, L199-239) |
| **Validation** | VALIDATED (Industry: pyeventsourcing, Vaughn Vernon) |

**Interface:**
```python
class AggregateRoot(ABC):
    """Base class for event-sourced aggregates."""
    _id: VertexId
    _version: int = 0
    _uncommitted_events: List[DomainEvent] = field(default_factory=list)

    # IAuditable metadata
    _created_by: str
    _created_at: datetime
    _updated_by: str
    _updated_at: datetime

    def _raise_event(self, event: DomainEvent) -> None:
        """Add event to uncommitted list and apply to state."""
        self._uncommitted_events.append(event)
        self._apply(event)

    @abstractmethod
    def _apply(self, event: DomainEvent) -> None:
        """Apply event to aggregate state (called during replay and after raising)."""
        pass

    def get_uncommitted_events(self) -> List[DomainEvent]:
        """Return events not yet persisted."""
        return list(self._uncommitted_events)

    def mark_events_committed(self) -> None:
        """Clear uncommitted events after persistence."""
        self._uncommitted_events.clear()

    @classmethod
    def load_from_history(cls, events: List[DomainEvent]) -> 'AggregateRoot':
        """Rebuild aggregate state by replaying events."""
        pass
```

**Vaughn Vernon's 4 Rules (from e-005):**
1. Model true invariants in consistency boundaries
2. Design small aggregates
3. Reference other aggregates by ID only
4. Use eventual consistency outside boundaries

#### 2.4 Vertex Base Class

| Attribute | Value |
|-----------|-------|
| **Definition** | Base node class for property graph model |
| **Source** | e-002 (L24-30) |
| **Validation** | VALIDATED (Industry: TinkerPop property graph) |

**Interface:**
```python
@dataclass
class Vertex:
    """Base node class for graph model."""
    id: VertexId
    label: str
    properties: Dict[str, Any]
```

#### 2.5 Edge Base Class

| Attribute | Value |
|-----------|-------|
| **Definition** | Base relationship class for property graph model |
| **Source** | e-002 (L24-30) |
| **Validation** | VALIDATED (Industry: TinkerPop property graph) |

**Interface:**
```python
@dataclass
class Edge:
    """Base relationship class for graph model."""
    id: EdgeId
    label: str
    outV: VertexId  # Source vertex
    inV: VertexId   # Target vertex
    properties: Dict[str, Any]
```

---

### 3. Domain Model

#### 3.1 Task Aggregate Root

| Attribute | Value |
|-----------|-------|
| **Definition** | Primary aggregate root representing a unit of work |
| **Source** | e-001 (L191-266), e-002 (L50-52) |
| **Validation** | VALIDATED (Industry: Small aggregate pattern) |

**Core Properties:**
- Auto-generated TaskId
- Status: PENDING, IN_PROGRESS, BLOCKED, COMPLETED, CANCELLED
- Title (max 200 chars)
- Description
- Priority (LOW, MEDIUM, HIGH, CRITICAL)
- Version (optimistic concurrency)

**State Transitions:**
```
PENDING -> IN_PROGRESS (valid)
IN_PROGRESS -> COMPLETED (valid)
IN_PROGRESS -> BLOCKED (valid)
BLOCKED -> IN_PROGRESS (valid)
PENDING -> CANCELLED (valid)
COMPLETED -> IN_PROGRESS (INVALID)
CANCELLED -> any (INVALID)
```

**Invariants:**
- BLOCKED status must have blocker_reason
- Due date in past raises ValidationError on create
- Completed task has completed_at <= updated_at

#### 3.2 Phase Aggregate Root

| Attribute | Value |
|-----------|-------|
| **Definition** | Logical grouping of tasks within a plan |
| **Source** | e-001 (L278-327), e-002 (L50-52) |
| **Validation** | VALIDATED (Industry: Container aggregate pattern) |

**Core Properties:**
- Auto-generated PhaseId
- Status: NOT_STARTED, ACTIVE, COMPLETED
- Order index for sequencing
- Set of TaskIds (reference by ID only)

**Key Behaviors:**
- `add_task()` adds TaskId to set, emits TaskAddedToPhase
- `remove_task()` removes TaskId, emits TaskRemovedFromPhase
- Cannot add task to COMPLETED phase
- Completion requires ACTIVE status

#### 3.3 Plan Aggregate Root

| Attribute | Value |
|-----------|-------|
| **Definition** | Top-level container for phases and work items |
| **Source** | e-001 (L329-379), e-002 (L50-52), e-004 (L74-100) |
| **Validation** | VALIDATED (Industry: Aggregate root pattern) |

**Core Properties:**
- Auto-generated PlanId
- Status: DRAFT, ACTIVE, COMPLETED, ARCHIVED
- Ordered list of PhaseIds
- Set of Assumptions
- Name (max 100 chars)

**Key Behaviors:**
- `add_phase()` with order, emits PhaseAddedToPlan
- `reorder_phases()` updates order_index values
- Cannot add phase to COMPLETED plan
- Cannot remove last phase (PlanRequiresPhase)

#### 3.4 Knowledge Domain Aggregates

| Attribute | Value |
|-----------|-------|
| **Definition** | Knowledge management entities (Pattern, Lesson, Assumption) |
| **Source** | e-001 (L1309-1411), e-004 (L152-163) |
| **Validation** | PROPOSED (Jerry-specific extension) |

**KnowledgeItem Base:**
- KnowledgeId
- Title, description
- Knowledge type (PATTERN, LESSON, ASSUMPTION)
- Tags set
- Source URI
- Created/updated timestamps

**Pattern Entity:**
- Context, problem, solution, consequences
- Applicability conditions
- Application count
- `apply()` increments count, emits PatternApplied

**Lesson Entity:**
- Observation, reflection, action
- Source task ID (optional)
- `materialize()` converts to Pattern

**Assumption Entity:**
- Hypothesis, validation criteria
- Status: UNTESTED, VALIDATED, INVALIDATED
- `validate()` / `invalidate()` with evidence

---

### 4. Event Patterns

#### 4.1 CloudEvents 1.0 Envelope

| Attribute | Value |
|-----------|-------|
| **Definition** | CNCF standard event envelope for all domain events |
| **Source** | e-001 (L79-96), e-002 (L257-275), e-005 (L264) |
| **Validation** | VALIDATED (Industry: CNCF CloudEvents 1.0 specification) |

**Envelope Structure:**
```json
{
  "specversion": "1.0",
  "type": "com.jerry.task.completed.v1",
  "source": "/jerry/tasks/TASK-ABC123",
  "id": "EVT-a1b2c3d4",
  "time": "2026-01-07T14:30:00Z",
  "subject": "TASK-ABC123",
  "datacontenttype": "application/json",
  "data": {
    "task_id": "TASK-ABC123",
    "phase_id": "PHASE-001",
    "completed_by": {"type": "CLAUDE", "id": "main"},
    "subtasks_completed": 5
  }
}
```

#### 4.2 DomainEvent Base Class

| Attribute | Value |
|-----------|-------|
| **Definition** | Base class for all domain events with metadata |
| **Source** | e-003 (L337-358) |
| **Validation** | VALIDATED (Industry: Event Sourcing pattern) |

**Interface:**
```python
@dataclass(frozen=True)
class DomainEvent(ABC):
    """Base class for all domain events. Events are immutable, past-tense facts."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    caused_by: str = "Claude"  # IAuditable: User email, "Claude", or "System"
    ecw_version: str = "v2.2.0"
    fingerprint: str = ""

    @abstractmethod
    def event_type(self) -> str:
        """Event type name for serialization (CloudEvents type field)."""
        pass
```

#### 4.3 Work Tracker Domain Events

| Attribute | Value |
|-----------|-------|
| **Definition** | Events for Task, Phase, Plan aggregates |
| **Source** | e-001 (L399-409), e-002 (L278-289), e-003 (L361-371) |
| **Validation** | VALIDATED (Industry: Event Sourcing standard) |

**Event Catalog:**
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

#### 4.4 Knowledge Domain Events

| Attribute | Value |
|-----------|-------|
| **Definition** | Events for Knowledge Management entities |
| **Source** | e-001 (L1397-1411) |
| **Validation** | PROPOSED (Jerry-specific) |

**Event Catalog:**
```python
PatternCreated, PatternUpdated, PatternApplied
LessonCreated, LessonUpdated, LessonMaterialized
AssumptionCreated, AssumptionValidated, AssumptionInvalidated
EvidenceAdded, KnowledgeLinked
```

#### 4.5 IEventStore Interface

| Attribute | Value |
|-----------|-------|
| **Definition** | Append-only event log port |
| **Source** | e-001 (L88-96), e-003 (L189-227), e-005 (L60-68) |
| **Validation** | VALIDATED (Industry: pyeventsourcing, Martin Fowler) |

**Interface:**
```python
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
        """Append events atomically. Raises ConcurrencyError if version mismatch."""
        pass

    @abstractmethod
    def read(self, stream_id: str, from_version: int = 0) -> List[StreamEvent]:
        """Read events from stream starting at from_version."""
        pass

    @abstractmethod
    def get_version(self, stream_id: str) -> int:
        """Get current version of stream (last event number)."""
        pass
```

---

### 5. CQRS Patterns

#### 5.1 Command Pattern

| Attribute | Value |
|-----------|-------|
| **Definition** | Immutable write operation requests |
| **Source** | e-001 (L57-65), e-003 (L125-138), e-005 (L93-108) |
| **Validation** | VALIDATED (Industry: Axon Framework) |

**Structure:**
```python
# Commands are immutable frozen dataclasses
@dataclass(frozen=True)
class CreateTaskCommand:
    title: str
    description: str
    priority: Priority

@dataclass(frozen=True)
class TransitionTaskCommand:
    task_id: TaskId
    target_status: TaskStatus
```

**Handler Pattern:**
1. Handler receives command
2. Handler loads aggregate (via repository)
3. Aggregate validates and applies business logic
4. Aggregate raises domain events
5. Handler saves aggregate (events appended)
6. Handler returns result (e.g., created ID)

#### 5.2 Query Pattern

| Attribute | Value |
|-----------|-------|
| **Definition** | Read operations returning DTOs from projections |
| **Source** | e-001 (L53-56), e-003 (L103-111, L319-333), e-005 (L118-135) |
| **Validation** | VALIDATED (Industry: Axon Framework) |

**Key Principles:**
- Queries return DTOs, never domain entities
- Queries read from projections (not aggregates)
- Projections are eventually consistent

**Query Handler Pattern:**
```python
class ListTasksQueryHandler:
    def __init__(self, projection_store: IProjectionStore):
        self._projection_store = projection_store

    def handle(self, query: ListTasksQuery) -> TaskListResult:
        return self._projection_store.query(query.filters)
```

#### 5.3 Projection Pattern

| Attribute | Value |
|-----------|-------|
| **Definition** | Query-friendly read models built by consuming events |
| **Source** | e-003 (L136-137, L319-333, L402-414), e-005 (L118-135) |
| **Validation** | VALIDATED (Industry: Axon Framework) |

**Interface:**
```python
class IProjection(ABC):
    """Read model projection. Eventually consistent with write side."""

    @abstractmethod
    def project(self, event: DomainEvent) -> None:
        """Apply event to projection."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset projection (for rebuild)."""
        pass
```

**Projection Examples:**
- `TaskListProjection`: Fast list queries
- `TaskDetailProjection`: Single item retrieval
- `PhaseProgressProjection`: Aggregated progress stats

---

### 6. Repository Patterns

#### 6.1 IRepository<T, TId> (Generic Repository Port)

| Attribute | Value |
|-----------|-------|
| **Definition** | Domain abstraction for aggregate persistence |
| **Source** | e-001 (L100-119), e-003 (L130, L153-186), e-005 (L171-187) |
| **Validation** | VALIDATED (Industry: Standard DDD pattern) |

**Interface:**
```python
class IRepository(ABC, Generic[TAggregate, TId]):
    """
    Domain abstraction for accessing Aggregate Roots.
    Event-sourced: save() appends events, find_by_id() replays events.
    """

    @abstractmethod
    def save(self, aggregate: TAggregate) -> None:
        """Persist aggregate. Extracts uncommitted events, appends to stream."""
        pass

    @abstractmethod
    def find_by_id(self, id: TId) -> Optional[TAggregate]:
        """Retrieve aggregate by ID. Loads events, replays to rebuild state."""
        pass

    @abstractmethod
    def exists(self, id: TId) -> bool:
        """Check if aggregate exists."""
        pass
```

#### 6.2 Unit of Work Pattern

| Attribute | Value |
|-----------|-------|
| **Definition** | Atomic transaction boundary for coordinating changes |
| **Source** | e-001 (L115-119), e-003 (L134, L255-289) |
| **Validation** | VALIDATED (Industry: Standard enterprise pattern) |

**Interface:**
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
    def __exit__(self, exc_type, exc_val, exc_tb):
        """On success: commit. On failure: rollback."""
        pass

    @abstractmethod
    def register_aggregate(self, aggregate: Any) -> None:
        """Register aggregate for commit."""
        pass

    @abstractmethod
    def commit(self) -> None:
        """Commit all changes atomically."""
        pass

    @abstractmethod
    def rollback(self) -> None:
        """Rollback all changes."""
        pass
```

#### 6.3 Optimistic Concurrency Control

| Attribute | Value |
|-----------|-------|
| **Definition** | Version-based conflict detection |
| **Source** | e-001 (L110-113), e-003 (L135, L209-215), e-005 (L61-62, L301) |
| **Validation** | VALIDATED (Industry: Event Sourcing standard) |

**Implementation:**
- Save operation includes `expected_version` parameter
- Event store validates current version matches expected
- Stale version raises `ConcurrencyError(expected, actual)`

#### 6.4 Snapshot Pattern

| Attribute | Value |
|-----------|-------|
| **Definition** | Performance optimization for event-sourced aggregates |
| **Source** | e-001 (L95-96), e-003 (L229-253, L418-436), e-005 (L73-81, L324) |
| **Validation** | VALIDATED (Industry: pyeventsourcing, Martin Fowler) |

**Interface:**
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
        aggregate: AggregateRoot,
        at_version: int
    ) -> None:
        """Save aggregate snapshot at specific version."""
        pass

    @abstractmethod
    def get_snapshot(self, stream_id: str) -> Optional[Tuple[AggregateRoot, int]]:
        """Get latest snapshot. Returns (aggregate_state, version) or None."""
        pass
```

**Snapshot Strategy:**
- Snapshot every 10 events (tunable)
- Load: Get snapshot -> Load events after snapshot -> Replay
- Rebuild from events if snapshot corrupted

---

### 7. Graph Patterns

#### 7.1 IGraphStore Port

| Attribute | Value |
|-----------|-------|
| **Definition** | Secondary port for graph persistence operations |
| **Source** | e-001 (L354-367), e-002 (L148-179) |
| **Validation** | VALIDATED (Industry: TinkerPop pattern) |

**Interface:**
```python
class IGraphStore(Generic[T]):
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
        """Remove vertex and connected edges."""
        pass

    @abstractmethod
    def add_edge(self, edge: Edge) -> None:
        """Create relationship between vertices."""
        pass

    @abstractmethod
    def get_edges(self, vertex_id: VertexId, direction: str) -> List[Edge]:
        """Get edges (incoming/outgoing/both)."""
        pass

    @abstractmethod
    def traverse(self, start: VertexId, depth: int, direction: str) -> List[Vertex]:
        """Traverse graph and return subgraph."""
        pass
```

#### 7.2 Edge Labels (Relationship Types)

| Attribute | Value |
|-----------|-------|
| **Definition** | Semantic edge types for graph relationships |
| **Source** | e-002 (L57-66) |
| **Validation** | VALIDATED (Industry: Property graph standard) |

**Edge Label Catalog:**
| Edge Label | Semantics | Direction |
|------------|-----------|-----------|
| `CONTAINS` | Parent has child | parent -> child |
| `BELONGS_TO` | Child references parent | child -> parent |
| `DEPENDS_ON` | Task dependency | task -> task |
| `EMITTED` | Aggregate produced event | aggregate -> event |
| `PERFORMED_BY` | Event actor attribution | event -> actor |
| `REFERENCES` | Evidence linkage | task -> evidence |

#### 7.3 Gremlin Compatibility

| Attribute | Value |
|-----------|-------|
| **Definition** | TinkerPop Gremlin-compatible traversal patterns |
| **Source** | e-002 (L293-317) |
| **Validation** | VALIDATED (Industry: TinkerPop standard) |

**Supported Traversals:**
```gremlin
// Get all tasks in a phase
g.V('PHASE-001').out('CONTAINS').hasLabel('Task')

// Calculate phase progress
g.V('PHASE-001').out('CONTAINS').hasLabel('Task').group().by('status')

// Find task dependencies
g.V('TASK-001').out('DEPENDS_ON').hasLabel('Task')

// Find events emitted by aggregate
g.V('TASK-001').out('EMITTED').hasLabel('Event')

// Trace actor's actions
g.V('ACTOR-CLAUDE-main').in('PERFORMED_BY').hasLabel('Event')
```

---

### 8. Architecture Patterns

#### 8.1 Hexagonal Architecture (Ports & Adapters)

| Attribute | Value |
|-----------|-------|
| **Definition** | Architecture isolating domain from infrastructure |
| **Source** | e-001 (L25-47), e-002 (L146-243), e-003 (L46-119), e-005 (L142-194) |
| **Validation** | VALIDATED (Industry: Alistair Cockburn, sairyss/domain-driven-hexagon) |

**Layer Dependencies (HARD ENFORCEMENT):**
```
domain/       -> NO imports from application/, infrastructure/, interface/
domain/       -> ONLY stdlib imports allowed
application/  -> MAY import from domain/
application/  -> NO imports from infrastructure/, interface/
infrastructure/ -> MAY import from domain/, application/
infrastructure/ -> NO imports from interface/
interface/    -> MAY import from all inner layers
```

**Directory Structure:**
```
src/
├── domain/           # Pure business logic, NO external deps
│   ├── aggregates/
│   ├── value_objects/
│   ├── events/
│   ├── ports/        # Interfaces (contracts)
│   └── exceptions.py
├── application/      # Use cases, orchestration
│   ├── commands/
│   ├── queries/
│   ├── handlers/
│   ├── event_handlers/
│   └── dtos/
├── infrastructure/   # Adapters implementing ports
│   ├── persistence/
│   ├── event_store/
│   ├── graph/
│   └── messaging/
└── interface/        # Primary adapters (CLI, API)
    ├── cli/
    └── api/
```

#### 8.2 Primary vs Secondary Ports

| Attribute | Value |
|-----------|-------|
| **Definition** | Distinction between driving and driven ports |
| **Source** | e-002 (L196-243), e-003 (L64-116) |
| **Validation** | VALIDATED (Industry: Hexagonal Architecture) |

**Primary Ports (Driving/Left Side):**
- Define use case interfaces
- Called by external actors (CLI, API, sub-agents)
- Examples: `ICreateTaskUseCase`, `ICompleteTaskUseCase`

**Secondary Ports (Driven/Right Side):**
- Define infrastructure contracts
- Implemented by adapters
- Examples: `IRepository`, `IEventStore`, `IGraphStore`

#### 8.3 Bounded Contexts

| Attribute | Value |
|-----------|-------|
| **Definition** | Explicit boundaries around domain models |
| **Source** | e-004 (L69-179) |
| **Validation** | VALIDATED (Industry: Eric Evans DDD) |

**Jerry Bounded Contexts:**
1. **Work Management** - Task, Phase, Plan aggregates
2. **Knowledge Capture** - Pattern, Lesson, Assumption aggregates
3. **Identity & Access** - Consent, Permissions
4. **Reporting** - Projections, Analytics

**Context Relationships:**
- Work Management publishes events to Reporting (Customer-Supplier)
- Knowledge Capture references Work Management items
- Identity & Access guards completions across all contexts

---

## L2: Cross-Cutting Concerns

### How Event Sourcing + CQRS Work Together

**Write Path (Commands):**
1. Command arrives at primary port
2. Command handler loads aggregate from repository
3. Repository calls event store to get events
4. Events replayed to rebuild aggregate state
5. Aggregate validates command, raises domain events
6. Repository appends events to event store
7. Event bus publishes events to projections

**Read Path (Queries):**
1. Query arrives at query handler
2. Handler reads from projection store
3. Projection store returns pre-computed view
4. Handler returns DTO to caller

**Key Insight:** Writes mutate event stream, reads use projections. Projections are eventually consistent (target <100ms lag).

```
Command -> Handler -> Aggregate -> Events -> EventStore
                                      |
                                      v
                              [Event Bus]
                                      |
                                      v
                              Projection -> ProjectionStore <- Query
```

### How Graph + Event Sourcing Integrate

**Events as Graph Citizens:**
1. Aggregates (Task, Phase, Plan) are **Vertex** nodes
2. Domain events become **Event** vertices
3. `EMITTED` edge connects aggregate to event
4. `PERFORMED_BY` edge connects event to actor

**Dual Storage Model:**
- **Event Store**: Append-only log (source of truth)
- **Graph Store**: Relationship navigation (derived view)

**Synchronization:**
- Projection handlers update graph on event publication
- Graph is eventually consistent with event stream
- Graph can be rebuilt by replaying events

**Example Flow:**
```
1. Task.complete() raises TaskCompleted event
2. Event appended to event store
3. Event bus publishes TaskCompleted
4. GraphProjection.project(TaskCompleted):
   - Create Event vertex
   - Create EMITTED edge: Task -> Event
   - Create PERFORMED_BY edge: Event -> Actor
   - Update Task vertex status
```

### Hexagonal Boundaries and Dependencies

**Strict Rules:**

| Layer | Can Import From | Cannot Import From |
|-------|-----------------|-------------------|
| domain | stdlib ONLY | application, infrastructure, interface |
| application | domain | infrastructure, interface |
| infrastructure | domain, application | interface |
| interface | domain, application, infrastructure | - |

**Dependency Inversion:**
- Domain defines ports (interfaces)
- Infrastructure implements adapters
- Application uses ports (injected adapters)
- Interface configures and composes everything

**Composition Root:**
```python
# interface/cli/main.py (Composition Root)
def create_app():
    # Create infrastructure adapters
    event_store = SqliteEventStore(connection)
    snapshot_store = SqliteSnapshotStore(connection)
    graph_store = NetworkxGraphStore()

    # Create repositories (implementing domain ports)
    task_repo = EventSourcedTaskRepository(event_store, snapshot_store)

    # Create use case handlers
    create_task_handler = CreateTaskCommandHandler(task_repo, unit_of_work)

    # Wire up CLI
    return CLI(create_task_handler, ...)
```

### Eventual Consistency Model

**Consistency Boundaries:**
- **Within Aggregate**: Strong consistency (transactional)
- **Across Aggregates**: Eventual consistency (domain events)

**Example:**
```
Phase.add_task(task_id)    # Strong: Phase updated atomically
   -> emits TaskAddedToPhase event
   -> Event bus publishes
   -> ProgressProjection updated (eventual)
   -> Graph updated (eventual)
```

**Acceptable Lag:** <100ms for projections (imperceptible to users)

**Conflict Resolution:**
- Optimistic concurrency on write (expected_version)
- Last-write-wins for projections
- Idempotent event handlers (replay-safe)

---

## Appendix A: Conflict Resolution

### Identified Conflicts Between Source Documents

| Topic | e-001 | e-002 | e-003 | e-004 | Resolution |
|-------|-------|-------|-------|-------|------------|
| Primary AR | Task | Task | ProblemStatement | Plan | **Task** (Vernon's small aggregate rule; e-001/e-002 consensus) |
| Aggregate count | 3 (Task, Phase, Plan) | 6 (Plan, Phase, Task, Subtask, Actor, Event) | 1 (ProblemStatement) | 4+ (Initiative, Plan, Phase, Task, etc.) | **3 primary** (Task, Phase, Plan) + supporting entities |
| Subtask modeling | Entity within Task | Vertex (separate) | N/A | Entity within Task | **Entity within Task** (e-001/e-004 consensus; avoids aggregate explosion) |

### Resolution Rationale

1. **Task as Primary AR**: Vernon's Rule 2 (small aggregates) supports Task over Plan. Task operations are most frequent.

2. **Subtask as Entity**: Subtasks don't have independent identity lifecycle. They're checked/unchecked within Task's consistency boundary.

3. **Event as Vertex**: CloudEvents are promoted to graph vertices for audit trail queries, but they're not aggregates---they're immutable facts.

---

## Appendix B: Source Document Concordance

| Pattern | e-001 | e-002 | e-003 | e-004 | e-005 |
|---------|-------|-------|-------|-------|-------|
| **Identity Patterns** | | | | | |
| VertexId | L112-122 | L107-143 | - | - | - |
| TaskId/PhaseId/PlanId | L124-136 | L109-136 | L100-101 | L74-100 | L215-238 |
| JerryUri | L137-148 | - | - | - | - |
| EdgeId | - | L120-122 | - | - | - |
| **Entity Patterns** | | | | | |
| IAuditable | - | - | L37-38, L347-349 | L88-89 | - |
| IVersioned | L110-119 | - | L135, L197 | - | - |
| AggregateRoot | L36-39 | - | L375-399 | L74-100 | L36-55, L199-239 |
| Vertex/Edge | L364-367 | L24-30 | - | - | - |
| **Domain Model** | | | | | |
| Task | L191-266 | L50-52 | - | L79-81 | - |
| Phase | L278-327 | L50-52 | - | L79-81 | - |
| Plan | L329-379 | L50-52 | - | L74-100 | - |
| KnowledgeItem | L1309-1411 | - | - | L152-163 | - |
| **Event Patterns** | | | | | |
| CloudEvents 1.0 | L79-96 | L257-275 | - | - | L264 |
| DomainEvent base | L399-409 | - | L337-358 | - | - |
| IEventStore | L88-96 | L183-185 | L189-227 | - | L60-68 |
| **CQRS Patterns** | | | | | |
| Commands | L57-65 | - | L125-138 | - | L93-108 |
| Queries | L53-56 | - | L103-111, L319-333 | - | L118-135 |
| Projections | - | - | L136-137, L402-414 | - | L118-135 |
| **Repository Patterns** | | | | | |
| IRepository<T,TId> | L100-119 | - | L153-186 | - | L171-187 |
| Unit of Work | L115-119 | - | L134, L255-289 | - | - |
| Snapshots | L95-96 | - | L229-253, L418-436 | - | L73-81, L324 |
| **Graph Patterns** | | | | | |
| IGraphStore | L354-367 | L148-179 | - | - | - |
| Edge Labels | - | L57-66 | - | - | - |
| Gremlin Traversals | - | L293-317 | - | - | - |
| **Architecture** | | | | | |
| Hexagonal | L25-47 | L146-243 | L46-119 | - | L142-194 |
| Bounded Contexts | - | - | - | L69-179 | - |
| Layer Dependencies | L437-453 | - | L116 | - | L189-194 |

---

## Appendix C: Implementation Checklist

Based on unified canon, the following patterns MUST be implemented:

### Phase 1: Domain Foundation
- [ ] `VertexId` base class with UUID validation
- [ ] Type-specific IDs (TaskId, PhaseId, PlanId, etc.)
- [ ] `AggregateRoot` base with event sourcing support
- [ ] `DomainEvent` base with CloudEvents envelope
- [ ] Status enums with state machine validation
- [ ] Value objects (Priority, Tag, etc.)

### Phase 2: Event Infrastructure
- [ ] `IEventStore` port with optimistic concurrency
- [ ] `ISnapshotStore` port (snapshot every 10 events)
- [ ] SQLite adapters for event/snapshot stores
- [ ] Event serialization (CloudEvents JSON)

### Phase 3: Aggregates
- [ ] `Task` aggregate with event-sourced mutations
- [ ] `Phase` aggregate with TaskId references
- [ ] `Plan` aggregate with PhaseId references
- [ ] Domain exceptions (NotFound, InvalidState, etc.)

### Phase 4: CQRS
- [ ] Command classes (immutable dataclasses)
- [ ] Query classes
- [ ] Command handlers (returning events)
- [ ] Query handlers (reading projections)
- [ ] Projection interface and implementations

### Phase 5: Graph Layer
- [ ] `Vertex` and `Edge` base classes
- [ ] `IGraphStore` port
- [ ] NetworkX adapter
- [ ] Edge labels (CONTAINS, EMITTED, etc.)
- [ ] Graph projection handlers

### Phase 6: Hexagonal Wiring
- [ ] Repository implementations using event store
- [ ] Unit of Work implementation
- [ ] Composition root (dependency injection)
- [ ] CLI primary adapter

---

## References

### Source Documents
| ID | Title | Location |
|----|-------|----------|
| e-001 | WORKTRACKER_PROPOSAL Extraction | `docs/research/PROJ-001-e-001-worktracker-proposal-extraction.md` |
| e-002 | PLAN.md Graph Model | `docs/research/PROJ-001-e-002-plan-graph-model.md` |
| e-003 | REVISED-ARCHITECTURE v3.0 | `docs/research/PROJ-001-e-003-revised-architecture-foundation.md` |
| e-004 | Strategic Plan v3.0 | `docs/research/PROJ-001-e-004-strategic-plan-v3.md` |
| e-005 | Industry Best Practices | `docs/research/PROJ-001-e-005-industry-best-practices.md` |

### Industry References
- Alistair Cockburn - Hexagonal Architecture: https://alistair.cockburn.us/hexagonal-architecture/
- Martin Fowler - Event Sourcing: https://martinfowler.com/eaaDev/EventSourcing.html
- Vaughn Vernon - Implementing Domain-Driven Design (2013)
- Eric Evans - Domain-Driven Design (2003)
- CNCF CloudEvents 1.0: https://cloudevents.io/
- Apache TinkerPop (Gremlin): https://tinkerpop.apache.org/
- pyeventsourcing: https://github.com/pyeventsourcing/eventsourcing
- Axon Framework: https://docs.axoniq.io/
- sairyss/domain-driven-hexagon: https://github.com/sairyss/domain-driven-hexagon

---

*Document synthesized by ps-synthesizer agent v2.0.0*
*Canon established: 2026-01-09*
