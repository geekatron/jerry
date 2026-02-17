# Architecture Patterns Guide

> Educational companion to [architecture-standards.md](../rules/architecture-standards.md).
> Explains port/adapter pattern, CQRS rationale, event sourcing concepts, and naming convention rationale.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Ports and Adapters Pattern](#ports-and-adapters-pattern) | Interface segregation and dependency inversion |
| [CQRS Pattern](#cqrs-pattern) | Command-Query Responsibility Segregation rationale |
| [Event Sourcing](#event-sourcing) | Event-based persistence concepts |
| [Naming Convention Rationale](#naming-convention-rationale) | Why we name things this way |
| [Composition Root Pattern](#composition-root-pattern) | Centralized dependency injection |
| [Bounded Contexts](#bounded-contexts) | Context boundaries and communication |
| [Repository Pattern](#repository-pattern) | Aggregate persistence abstraction |

---

## Ports and Adapters Pattern

### The Problem

How do you keep business logic independent of technical details (databases, APIs, frameworks)?

**Bad approach**: Let domain code directly call infrastructure:
```python
class WorkItem:
    def save(self) -> None:
        # ❌ Domain tightly coupled to PostgreSQL
        conn = psycopg2.connect("postgresql://...")
        conn.execute("INSERT INTO work_items ...")
```

**Problems**:
1. Can't test domain logic without a database
2. Changing database requires changing domain code
3. Business logic polluted with SQL

---

### The Solution: Ports and Adapters

**Port**: An interface (protocol) that defines what the application needs.
**Adapter**: A concrete implementation that provides what the application needs.

```python
# PORT (defined by domain/application)
class IRepository(Protocol):
    def save(self, work_item: WorkItem) -> None: ...
    def get(self, id: str) -> WorkItem | None: ...

# ADAPTER 1: PostgreSQL implementation
class PostgresWorkItemAdapter(IRepository):
    def save(self, work_item: WorkItem) -> None:
        # PostgreSQL-specific code here
        ...

# ADAPTER 2: Filesystem implementation
class FilesystemWorkItemAdapter(IRepository):
    def save(self, work_item: WorkItem) -> None:
        # Filesystem-specific code here
        ...

# ADAPTER 3: In-memory implementation (for tests)
class InMemoryWorkItemAdapter(IRepository):
    def save(self, work_item: WorkItem) -> None:
        self._items[work_item.id] = work_item
```

**Key insight**: Application depends on **IRepository** (port), not the concrete adapters. Infrastructure provides adapters.

---

### Primary vs Secondary Ports

#### Primary Ports (Driving Side)

**Purpose**: Define what the application **can do** (use cases).

**Location**: `src/application/ports/primary/`

**Examples**:
- `ICommandHandler` - Handles commands (write operations)
- `IQueryHandler` - Handles queries (read operations)

**Naming**: `I{Verb}Handler`

**Why this matters**: The application **offers** these interfaces. The UI/CLI/API **uses** them.

```python
# Primary port
class ICommandHandler(Protocol[TCommand, TResult]):
    def handle(self, command: TCommand) -> TResult: ...

# Primary adapter (in interface layer)
@click.command()
def create_item(title: str, handler: ICommandHandler) -> None:
    command = CreateWorkItemCommand(title=title)
    handler.handle(command)  # CLI drives the application
```

---

#### Secondary Ports (Driven Side)

**Purpose**: Define what the application **needs** from infrastructure.

**Location**:
- `src/application/ports/secondary/` - Application-level ports
- `src/domain/ports/` - Domain-level ports

**Examples**:
- `IRepository` - Persistence abstraction
- `IEventStore` - Event persistence
- `INotifier` - External notifications

**Naming**: `I{Noun}`

**Why this matters**: The application **defines** what it needs. Infrastructure **implements** it.

```python
# Secondary port (defined by application)
class IEventStore(Protocol):
    def append(self, stream_id: str, events: list[DomainEvent]) -> None: ...
    def read(self, stream_id: str) -> list[DomainEvent]: ...

# Secondary adapter (in infrastructure)
class InMemoryEventStore(IEventStore):
    def append(self, stream_id: str, events: list[DomainEvent]) -> None:
        # In-memory implementation
        ...
```

---

### Port Naming Conventions

| Port Type | Location | Pattern | Example |
|-----------|----------|---------|---------|
| Primary (use case) | `application/ports/primary/` | `I{Verb}Handler` | `IQueryHandler`, `ICommandHandler` |
| Secondary (infra need) | `application/ports/secondary/` | `I{Noun}` | `IEventStore`, `INotifier` |
| Domain (persistence) | `domain/ports/` | `I{Noun}` | `IRepository` |

**Rationale**:
- **Primary ports are verbs** because they represent **actions** the system can perform
- **Secondary ports are nouns** because they represent **capabilities** the system needs

---

### Adapter Naming Conventions

| Adapter Type | Location | Pattern | Example |
|--------------|----------|---------|---------|
| Persistence | `infrastructure/adapters/persistence/` | `{Tech}{Entity}Adapter` | `FilesystemProjectAdapter`, `PostgresWorkItemAdapter` |
| Messaging | `infrastructure/adapters/messaging/` | `{Tech}EventStore` | `InMemoryEventStore`, `KafkaEventStore` |
| External | `infrastructure/adapters/external/` | `{Service}Adapter` | `GitHubApiAdapter`, `AdoApiAdapter` |

**Rationale**:
- **Tech prefix** makes it clear what technology is used (easier to swap)
- **Entity suffix** indicates what domain concept it handles
- **Adapter suffix** clearly marks it as an adapter implementation

---

## CQRS Pattern

### What is CQRS?

**Command-Query Responsibility Segregation**: Separate the write model (commands) from the read model (queries).

**Core principle**: Methods should either **change state** (command) or **return data** (query), never both.

---

### Why CQRS?

#### Problem 1: Complex query methods on domain entities

```python
# ❌ BAD: Domain entity with complex query logic
class WorkItem:
    def get_all_incomplete_subtasks_with_high_priority(self) -> list[Task]:
        # Complex query logic in domain entity
        return [t for t in self.tasks if not t.is_complete and t.priority == "high"]
```

**Problems**:
- Domain entity polluted with query concerns
- Can't optimize queries independently
- Forces domain model to support all query needs

---

#### Problem 2: One model for reads and writes

```python
# ❌ BAD: Same model for reading and writing
class WorkItemRepository:
    def get_work_items_with_stats(self) -> list[WorkItem]:
        # Must load entire aggregate just to show a list
        items = self._load_all_items()
        for item in items:
            item.stats = self._calculate_stats(item)  # Expensive
        return items
```

**Problems**:
- Reading a list requires loading full aggregates (slow)
- Write model optimized for consistency, not query performance
- Can't cache or pre-compute query results

---

### The CQRS Solution

**Commands** (Write Model):
- Represent **intent to change state**
- Return `None` or domain events
- Validated against business rules
- Change aggregate state

**Queries** (Read Model):
- Represent **intent to read data**
- Return DTOs (never domain entities)
- Optimized for performance
- No business logic

```python
# COMMAND (Write Side)
@dataclass(frozen=True)
class CreateWorkItemCommand:
    title: str
    description: str | None = None

class CreateWorkItemCommandHandler:
    def __init__(self, repository: IRepository) -> None:
        self._repository = repository

    def handle(self, command: CreateWorkItemCommand) -> list[DomainEvent]:
        work_item = WorkItem.create(title=command.title, description=command.description)
        self._repository.save(work_item)
        return work_item.collect_events()  # Returns events, not data

# QUERY (Read Side)
@dataclass(frozen=True)
class ListWorkItemsQuery:
    status: str | None = None

@dataclass(frozen=True)
class WorkItemDTO:
    id: str
    title: str
    status: str
    subtask_count: int  # Optimized projection

class ListWorkItemsQueryHandler:
    def __init__(self, read_model: IWorkItemReadModel) -> None:
        self._read_model = read_model

    def handle(self, query: ListWorkItemsQuery) -> list[WorkItemDTO]:
        return self._read_model.list_with_stats(status=query.status)  # Optimized query
```

---

### CQRS Benefits

1. **Performance**: Optimize reads separately from writes
2. **Simplicity**: Each side has one job
3. **Scalability**: Scale reads and writes independently
4. **Flexibility**: Use different storage for reads (e.g., pre-computed views)

---

### CQRS File Naming Rationale

| Type | Pattern | Rationale | Example |
|------|---------|-----------|---------|
| Command | `{verb}_{noun}_command.py` | Action intent clearly stated | `create_work_item_command.py` |
| Query | `{verb}_{noun}_query.py` | Read intent clearly stated | `list_work_items_query.py` |
| Handler | `{command/query}_handler.py` | Clear mapping to command/query | `create_work_item_command_handler.py` |

**Why verb-first naming?**
- Groups related operations together in file listings
- `create_work_item_command.py`, `create_task_command.py` appear together
- Easy to find all "create" operations

**Why separate handler files?**
- One class per file (H-10)
- Handler can be complex, deserves its own file
- Easy to locate handler implementation

---

### Query Verb Selection Guide

| Scenario | Recommended Verb | Rationale | Example |
|----------|------------------|-----------|---------|
| Single by ID | `Retrieve` or `Get` | Implies specific item | `RetrieveProjectContextQuery` |
| Collection | `List` | Implies multiple items | `ListWorkItemsQuery` |
| Discovery | `Scan` | Implies exploration | `ScanProjectsQuery` |
| Validation | `Validate` | Implies check | `ValidateProjectQuery` |
| Search | `Find` or `Search` | Implies filtering | `FindTasksByStatusQuery` |

**Why standardize verbs?**
- **Consistency**: Developers know what to expect
- **Searchability**: Easy to find all "List" queries
- **Intent clarity**: `List` vs `Get` conveys cardinality

---

## Event Sourcing

### What is Event Sourcing?

**Event Sourcing**: Store **changes to state** (events) instead of **current state**.

**Traditional approach**:
```
Database: [WorkItem(id=1, status="completed", title="Fix bug")]
```

**Event sourcing approach**:
```
Event Stream: [
  WorkItemCreated(id=1, title="Fix bug"),
  WorkItemStarted(id=1),
  WorkItemCompleted(id=1)
]
```

To get current state: **replay all events**.

---

### Why Event Sourcing?

#### Benefit 1: Complete Audit Trail

**Traditional**: Lost history. Only know current state.
```
Before: status = "in_progress"
After:  status = "completed"
Lost:   When? Who? Why?
```

**Event sourcing**: Full history preserved.
```
Events:
  2024-01-15 10:00 - WorkItemCreated by alice
  2024-01-15 14:00 - WorkItemStarted by alice
  2024-01-16 09:30 - WorkItemCompleted by alice
```

---

#### Benefit 2: Temporal Queries

**Question**: "What was the state of this work item on January 15th?"

**Traditional**: Impossible (unless you kept versioned snapshots).

**Event sourcing**: Replay events up to that date.
```python
def get_state_at(item_id: str, timestamp: datetime) -> WorkItem:
    events = event_store.read(stream_id=item_id)
    events_before = [e for e in events if e.timestamp <= timestamp]
    return WorkItem.reconstitute(events_before)
```

---

#### Benefit 3: Event-Driven Architecture

Events are **first-class citizens**. Other systems can subscribe.

```python
# Event emitted
event = WorkItemCompleted(work_item_id="WORK-123")

# Subscribers react
NotificationService.on(WorkItemCompleted, send_email)
MetricsService.on(WorkItemCompleted, update_dashboard)
SearchIndex.on(WorkItemCompleted, reindex_item)
```

---

### Domain Event Pattern

#### Event Structure

```python
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import ClassVar

@dataclass(frozen=True)
class WorkItemCompleted(DomainEvent):
    """Event raised when a work item is completed."""

    EVENT_TYPE: ClassVar[str] = "work_item.completed"  # Unique identifier

    work_item_id: str
    completed_at: datetime
    quality_passed: bool

    @classmethod
    def create(cls, work_item_id: str, quality_passed: bool = True) -> "WorkItemCompleted":
        """Factory method with automatic timestamp."""
        return cls(
            work_item_id=work_item_id,
            completed_at=datetime.now(timezone.utc),
            quality_passed=quality_passed,
        )
```

---

#### Event Naming Conventions

| Rule | Example | Rationale |
|------|---------|-----------|
| Use **past tense** | `WorkItemCompleted`, `TaskStarted` | Event already happened |
| Include **aggregate type** | `WorkItem` + `Completed` | Clear which aggregate changed |
| Event type string | `work_item.completed` | Lowercase, dotted, for serialization |

**Why past tense?**
- Events are **facts**. They happened.
- Present tense (`WorkItemComplete`) sounds like a command

**Why include aggregate type?**
- `Completed` alone is ambiguous (what was completed?)
- `WorkItemCompleted` is unambiguous

---

#### Event Store Pattern

```python
class IEventStore(Protocol):
    """Port for event persistence."""

    def append(
        self,
        stream_id: str,
        events: list[DomainEvent],
        expected_version: int,
    ) -> None:
        """Append events to stream. Raises ConcurrencyError if version mismatch."""
        ...

    def read(self, stream_id: str, from_version: int = 0) -> list[DomainEvent]:
        """Read events from stream starting at version."""
        ...
```

**Stream ID**: Unique identifier for event stream (e.g., `"work_item-123"`)
**Expected version**: Optimistic locking (detects concurrent modifications)

---

### Aggregate Root with Event Sourcing

```python
class WorkItem(AggregateRoot):
    """Aggregate root reconstructed from events."""

    def __init__(self, id: str) -> None:
        super().__init__()
        self.id = id
        self.title = ""
        self.status = Status.PENDING

    @classmethod
    def create(cls, title: str) -> "WorkItem":
        """Factory method that emits creation event."""
        item = cls(id=generate_id())
        event = WorkItemCreated(work_item_id=item.id, title=title)
        item.apply_event(event)
        return item

    def complete(self) -> None:
        """Complete the work item."""
        if self.status != Status.IN_PROGRESS:
            raise InvalidStateError(...)
        event = WorkItemCompleted(work_item_id=self.id)
        self.apply_event(event)

    def _apply(self, event: DomainEvent) -> None:
        """Apply event to aggregate state."""
        if isinstance(event, WorkItemCreated):
            self.title = event.title
            self.status = Status.PENDING
        elif isinstance(event, WorkItemCompleted):
            self.status = Status.COMPLETED

    @classmethod
    def reconstitute(cls, events: list[DomainEvent]) -> "WorkItem":
        """Rebuild aggregate from event history."""
        item = cls(id=events[0].work_item_id)
        for event in events:
            item._apply(event)
        return item
```

**Pattern**:
1. **Public methods emit events** (`complete()` emits `WorkItemCompleted`)
2. **`_apply()` updates state** based on event
3. **`reconstitute()` rebuilds** aggregate from history

---

### Snapshot Optimization

**Problem**: Replaying 10,000 events is slow.

**Solution**: Periodic snapshots.

```python
class ISnapshotStore(Protocol):
    def save(self, aggregate_id: str, snapshot: Snapshot, version: int) -> None: ...
    def load(self, aggregate_id: str) -> tuple[Snapshot, int] | None: ...

# Every 10 events, save a snapshot
if len(events) % 10 == 0:
    snapshot = Snapshot(state=work_item.__dict__, version=work_item.version)
    snapshot_store.save(work_item.id, snapshot, work_item.version)

# To reconstitute: load snapshot + replay events since snapshot
snapshot, version = snapshot_store.load(work_item_id)
events_since = event_store.read(work_item_id, from_version=version)
work_item = WorkItem.from_snapshot(snapshot)
for event in events_since:
    work_item._apply(event)
```

**Jerry decision**: Snapshot every **10 events**.

---

## Naming Convention Rationale

### Command Naming

**Pattern**: `{Verb}{Noun}Command`

**Examples**:
- `CreateWorkItemCommand`
- `CompleteTaskCommand`
- `UpdateProjectCommand`

**Rationale**:
- **Verb-first**: Emphasizes **action intent**
- **Imperative mood**: Commands are orders ("Create this", "Complete that")
- **Command suffix**: Clear distinction from queries

---

### Query Naming

**Pattern**: `{Verb}{Noun}Query`

**Examples**:
- `ListWorkItemsQuery`
- `RetrieveProjectContextQuery`
- `FindTasksByStatusQuery`

**Rationale**:
- **Verb-first**: Matches command pattern for consistency
- **Query suffix**: Clear distinction from commands
- **Specific verbs**: `List` vs `Retrieve` vs `Find` conveys intent

---

### Handler Naming

**Pattern**: `{CommandOrQuery}Handler`

**Examples**:
- `CreateWorkItemCommandHandler`
- `ListWorkItemsQueryHandler`

**Rationale**:
- **One-to-one mapping**: Clear which command/query it handles
- **Handler suffix**: Follows application service pattern
- **No abbreviation**: `Handler` not `Hdlr` (clarity over brevity)

---

### Event Naming

**Pattern**: `{Noun}{PastVerb}`

**Examples**:
- `WorkItemCreated`
- `TaskStarted`
- `ProjectCompleted`

**Rationale**:
- **Past tense**: Event already happened (fact, not intent)
- **Noun-first**: Groups events by aggregate (`WorkItemCreated`, `WorkItemCompleted`)
- **No "Event" suffix**: Context makes it clear (in `events/` directory)

---

## Composition Root Pattern

### What is a Composition Root?

**Composition Root**: The **one place** where all dependency wiring happens.

**In Jerry**: `src/bootstrap.py`

---

### Why Centralize Dependency Injection?

#### Problem: Scattered `new` calls

```python
# ❌ BAD: Dependencies created everywhere
class CreateWorkItemCommandHandler:
    def __init__(self) -> None:
        self._repository = FilesystemAdapter()  # Created here
        self._event_store = InMemoryEventStore()  # Created here

class CLI:
    def __init__(self) -> None:
        self._handler = CreateWorkItemCommandHandler()  # Created here
```

**Problems**:
1. **Hard to test**: Can't inject mocks
2. **Hard to swap**: Changing database requires editing many files
3. **Hidden dependencies**: Can't see full dependency graph

---

#### Solution: Composition Root

```python
# ✅ GOOD: All wiring in bootstrap.py
def create_command_dispatcher() -> CommandDispatcher:
    # Infrastructure adapters
    repository = FilesystemWorkItemAdapter(base_path=Path(".jerry"))
    event_store = InMemoryEventStore()

    # Handlers with injected dependencies
    create_handler = CreateWorkItemCommandHandler(
        repository=repository,
        event_store=event_store,
    )

    # Dispatcher
    dispatcher = CommandDispatcher()
    dispatcher.register(CreateWorkItemCommand, create_handler.handle)
    return dispatcher

# CLI just receives the dispatcher
class CLI:
    def __init__(self, dispatcher: CommandDispatcher) -> None:
        self._dispatcher = dispatcher
```

**Benefits**:
1. **Single source of truth**: All wiring visible in one file
2. **Easy to swap**: Change adapter in one place
3. **Testable**: Inject test doubles easily

---

### H-09: Only Bootstrap Instantiates Infrastructure

**Rule**: Only `src/bootstrap.py` may `import` and `new` infrastructure adapters.

**Rationale**:
- **Prevents coupling**: Application/domain can't accidentally instantiate concrete adapters
- **Enforces dependency inversion**: Application depends on ports, infrastructure on implementation
- **Single point of change**: Swapping implementations requires editing one file

**Example**:
```python
# src/bootstrap.py ✅ ALLOWED
from src.infrastructure.adapters.persistence.filesystem_adapter import FilesystemAdapter
repository = FilesystemAdapter()

# src/application/handlers/handler.py ❌ FORBIDDEN
from src.infrastructure.adapters.persistence.filesystem_adapter import FilesystemAdapter
repository = FilesystemAdapter()  # Violates H-09
```

---

## Bounded Contexts

### What is a Bounded Context?

**Bounded Context**: A boundary within which a domain model is defined and applicable.

**Example**: `WorkItem` means different things in different contexts:
- **Work Tracking context**: A task with status, priority, subtasks
- **Billing context**: A billable unit of work with hours and rate
- **Reporting context**: A data point for metrics

**Key insight**: Don't try to make one `WorkItem` class serve all contexts. Each context has its own model.

---

### Jerry's Bounded Contexts

```
src/
├── session_management/      # BC: Projects, sessions, environment
├── work_tracking/           # BC: Work items, tasks, workflows
├── problem_solving/         # BC: (Future) ps-* agents
└── shared_kernel/           # Cross-context shared code
```

---

### Context Communication Rules

**Rule**: Contexts NEVER import directly from each other (except `shared_kernel/`).

**Communication mechanisms**:
1. **Domain Events**: Publish events, other contexts subscribe
2. **Shared Kernel**: Identity types, base classes
3. **Anti-Corruption Layer**: Translate external systems

**Example**:
```python
# ✅ GOOD: Context publishes event
class WorkItemCompleted(DomainEvent):
    work_item_id: str

# Other context subscribes
class BillingContext:
    def on_work_item_completed(self, event: WorkItemCompleted) -> None:
        # Create invoice
        ...

# ❌ BAD: Direct import across contexts
from src.work_tracking.domain.aggregates.work_item import WorkItem
class BillingContext:
    def create_invoice(self, work_item: WorkItem) -> None:  # Coupling!
        ...
```

---

## Repository Pattern

### Why Repository?

**Problem**: How to persist and retrieve aggregates without coupling domain to database?

**Solution**: Repository pattern abstracts persistence behind an interface.

---

### Generic Repository Port

```python
from typing import Protocol, TypeVar

TAggregate = TypeVar("TAggregate")
TId = TypeVar("TId")

class IRepository(Protocol[TAggregate, TId]):
    """Port interface for aggregate persistence."""

    def get(self, id: TId) -> TAggregate | None:
        """Retrieve aggregate by ID. Returns None if not found."""
        ...

    def get_or_raise(self, id: TId) -> TAggregate:
        """Retrieve aggregate by ID. Raises NotFoundError if not found."""
        ...

    def save(self, aggregate: TAggregate) -> None:
        """Persist aggregate."""
        ...

    def delete(self, id: TId) -> bool:
        """Delete aggregate. Returns True if deleted, False if not found."""
        ...

    def exists(self, id: TId) -> bool:
        """Check if aggregate exists."""
        ...
```

**Why generic?**
- **Reusable**: Same interface for `WorkItemRepository`, `ProjectRepository`, etc.
- **Type-safe**: `IRepository[WorkItem, WorkItemId]` enforces types

---

### Repository Implementations

#### Event-Sourced Repository

```python
class EventSourcedWorkItemRepository(IRepository[WorkItem, WorkItemId]):
    def __init__(self, event_store: IEventStore) -> None:
        self._event_store = event_store

    def get(self, id: WorkItemId) -> WorkItem | None:
        stream_id = f"work_item-{id.value}"
        events = self._event_store.read(stream_id)
        if not events:
            return None
        return WorkItem.reconstitute(events)

    def save(self, work_item: WorkItem) -> None:
        stream_id = f"work_item-{work_item.id.value}"
        events = work_item.collect_events()
        self._event_store.append(stream_id, events, work_item.version)
```

---

#### In-Memory Repository (for tests)

```python
class InMemoryWorkItemRepository(IRepository[WorkItem, WorkItemId]):
    def __init__(self) -> None:
        self._items: dict[WorkItemId, WorkItem] = {}

    def get(self, id: WorkItemId) -> WorkItem | None:
        return self._items.get(id)

    def save(self, work_item: WorkItem) -> None:
        self._items[work_item.id] = work_item
```

**Why in-memory?**
- **Fast tests**: No I/O overhead
- **Simple**: No database setup required
- **Implements same port**: Tests use same interface as production

---

## References

### Related Documents

- [Architecture Standards](../rules/architecture-standards.md) - Enforcement rules
- [Architecture Layers Guide](architecture-layers.md) - Layer responsibilities
- [Coding Practices Guide](coding-practices.md) - Implementation details

### External References

- [CQRS](https://martinfowler.com/bliki/CQRS.html) - Martin Fowler
- [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) - Martin Fowler
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html) - Martin Fowler
- [Domain-Driven Design](https://www.domainlanguage.com/ddd/) - Eric Evans
