# Architecture Standards

> Hexagonal Architecture, CQRS, and Event Sourcing standards for Jerry.
> These rules are enforced via architecture tests.

**Authoritative Pattern Source**: `.claude/patterns/PATTERN-CATALOG.md`

**Related Pattern Files**:
- [Hexagonal Architecture](../patterns/architecture/hexagonal-architecture.md) (PAT-ARCH-001)
- [Ports and Adapters](../patterns/architecture/ports-adapters.md) (PAT-ARCH-002)
- [Bounded Contexts](../patterns/architecture/bounded-contexts.md) (PAT-ARCH-003)
- [Composition Root](../patterns/architecture/composition-root.md) (PAT-ARCH-005)

---

## Hexagonal Architecture

### Layer Structure

```
src/
├── domain/                    # Core business logic
│   ├── aggregates/            # Aggregate roots
│   ├── entities/              # Domain entities
│   ├── value_objects/         # Immutable value objects
│   ├── events/                # Domain events
│   ├── services/              # Domain services
│   └── ports/                 # DOMAIN ports (IRepository, etc.)
│
├── application/               # Use cases
│   ├── commands/              # Command definitions
│   ├── queries/               # Query definitions
│   ├── handlers/              # Command/Query handlers
│   │   ├── commands/          # Command handlers
│   │   └── queries/           # Query handlers
│   ├── ports/                 # APPLICATION ports
│   │   ├── primary/           # Inbound ports (ICommandHandler, IQueryHandler)
│   │   └── secondary/         # Outbound ports (IEventStore, INotifier)
│   └── projections/           # Read model projections
│
├── infrastructure/            # Technical adapters
│   ├── adapters/              # Port implementations
│   │   ├── persistence/       # Repository adapters
│   │   ├── messaging/         # Event store adapters
│   │   └── external/          # External service adapters
│   ├── read_models/           # Materialized view storage
│   └── internal/              # Internal utilities (IFileStore, ISerializer)
│
└── interface/                 # Primary adapters
    ├── cli/                   # CLI adapter
    ├── api/                   # HTTP API adapter
    └── hooks/                 # Git/IDE hooks
```

### Dependency Rules

| Layer | Can Import From | Cannot Import From |
|-------|-----------------|-------------------|
| `domain/` | stdlib only | application, infrastructure, interface |
| `application/` | domain | infrastructure, interface |
| `infrastructure/` | domain, application | interface |
| `interface/` | domain, application, infrastructure | - |

### Shared Kernel

`shared_kernel/` is cross-cutting code shared across bounded contexts:
- Identity types (VertexId, SnowflakeIdGenerator)
- Base classes (DomainEvent, AggregateRoot)
- Common protocols (IAuditable, IVersioned)

**Rule**: Domain layer may import from shared_kernel.

---

## Ports and Adapters

### Port Naming Convention

| Type | Location | Naming | Example |
|------|----------|--------|---------|
| Primary Port | `application/ports/primary/` | `I{Verb}Handler` | `IQueryHandler` |
| Secondary Port | `application/ports/secondary/` | `I{Noun}` | `IEventStore`, `IRepository` |
| Domain Port | `domain/ports/` | `I{Noun}` | `IRepository` |

### Adapter Naming Convention

| Type | Location | Naming | Example |
|------|----------|--------|---------|
| Persistence | `infrastructure/adapters/persistence/` | `{Tech}{Entity}Adapter` | `FilesystemProjectAdapter` |
| Messaging | `infrastructure/adapters/messaging/` | `{Tech}EventStore` | `InMemoryEventStore` |
| External | `infrastructure/adapters/external/` | `{Service}Adapter` | `GitHubApiAdapter` |

### Composition Root

All dependency wiring happens in `src/bootstrap.py`:

```python
# bootstrap.py - The ONLY place infrastructure is instantiated
def create_query_dispatcher() -> QueryDispatcher:
    # Create infrastructure adapters
    repository = FilesystemProjectAdapter()
    environment = OsEnvironmentAdapter()

    # Create handlers with injected dependencies
    handler = GetProjectContextHandler(repository=repository, environment=environment)

    # Configure dispatcher
    dispatcher = QueryDispatcher()
    dispatcher.register(GetProjectContextQuery, handler.handle)

    return dispatcher
```

**Rule**: Adapters NEVER instantiate their own dependencies.

---

## CQRS Pattern

### Command Structure

```python
# File: src/application/commands/create_task_command.py
@dataclass(frozen=True)
class CreateTaskCommand:
    """Command to create a new task."""
    title: str
    description: str | None = None
    parent_id: TaskId | None = None

# File: src/application/handlers/commands/create_task_command_handler.py
class CreateTaskCommandHandler:
    """Handler for CreateTaskCommand."""

    def __init__(self, repository: ITaskRepository) -> None:
        self._repository = repository

    def handle(self, command: CreateTaskCommand) -> list[DomainEvent]:
        task = Task.create(title=command.title, description=command.description)
        self._repository.save(task)
        return task.collect_events()
```

### Query Structure

```python
# File: src/application/queries/retrieve_project_context_query.py
@dataclass(frozen=True)
class RetrieveProjectContextQuery:
    """Query to retrieve project context."""
    base_path: str

# File: src/application/handlers/queries/retrieve_project_context_query_handler.py
class RetrieveProjectContextQueryHandler:
    """Handler for RetrieveProjectContextQuery."""

    def __init__(self, repository: IProjectRepository) -> None:
        self._repository = repository

    def handle(self, query: RetrieveProjectContextQuery) -> ProjectContextDTO:
        # Return DTO, never domain entity
        ...
```

### File Naming Rules

| Type | Pattern | Example |
|------|---------|---------|
| Command | `{verb}_{noun}_command.py` | `create_task_command.py` |
| Query | `retrieve_{noun}_query.py` | `retrieve_project_context_query.py` |
| Command Handler | `{verb}_{noun}_command_handler.py` | `create_task_command_handler.py` |
| Query Handler | `{verb}_{noun}_query_handler.py` | `retrieve_project_context_query_handler.py` |

### Dispatcher Pattern

```python
# File: src/application/ports/primary/iquerydispatcher.py
class IQueryDispatcher(Protocol):
    def dispatch(self, query: Query) -> Any: ...

# File: src/application/ports/primary/icommanddispatcher.py
class ICommandDispatcher(Protocol):
    def dispatch(self, command: Command) -> list[DomainEvent]: ...
```

**Rule**: Separate files for each dispatcher protocol.

---

## Event Sourcing

### Domain Events

```python
# File: src/domain/events/task_events.py
@dataclass(frozen=True)
class TaskCreated(DomainEvent):
    task_id: TaskId
    title: str
    created_at: datetime

@dataclass(frozen=True)
class TaskCompleted(DomainEvent):
    task_id: TaskId
    completed_at: datetime
```

**Naming**: Past tense verb (e.g., `Created`, `Completed`, `Updated`)

### Event Store Port

```python
# File: src/application/ports/secondary/ieventstore.py
class IEventStore(Protocol):
    def append(self, stream_id: str, events: list[DomainEvent], expected_version: int) -> None: ...
    def read(self, stream_id: str, from_version: int = 0) -> list[DomainEvent]: ...
```

### Aggregate Root Pattern

```python
class AggregateRoot(ABC):
    _events: list[DomainEvent]
    _version: int

    def apply_event(self, event: DomainEvent) -> None:
        self._apply(event)
        self._events.append(event)

    def collect_events(self) -> list[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events

    @abstractmethod
    def _apply(self, event: DomainEvent) -> None:
        """Apply event to aggregate state."""
```

**See Also**: [Aggregate Root Pattern](../patterns/entity/aggregate-root.md) (PAT-ENT-003)

### Snapshot Optimization

For aggregates with many events, use snapshots every N events:

```python
class ISnapshotStore(Protocol):
    def save(self, aggregate_id: str, snapshot: Snapshot, version: int) -> None: ...
    def load(self, aggregate_id: str) -> tuple[Snapshot, int] | None: ...
```

**Jerry Decision**: Snapshot every 10 events.

**See Also**: [Snapshot Store Pattern](../patterns/repository/snapshot-store.md) (PAT-REPO-003)

---

## Value Objects

### Immutable Value Objects

All value objects MUST be immutable:

```python
@dataclass(frozen=True, slots=True)
class Priority:
    """Value object representing task priority."""
    value: str

    def __post_init__(self) -> None:
        if self.value not in {"low", "medium", "high", "critical"}:
            raise ValidationError(field="priority", message=f"Invalid: {self.value}")
```

### Value Object Rules

| Rule | Description |
|------|-------------|
| Immutability | Use `@dataclass(frozen=True, slots=True)` |
| Equality by Value | Two VOs with same data are equal |
| Self-Validating | Validation in `__post_init__` |
| No Identity | VOs have no lifecycle, only values |

### Value Object Types

| Type | Use Case | Example |
|------|----------|---------|
| Simple | Single value with validation | `Priority`, `Title`, `Percentage` |
| Enum | Fixed set of values | `WorkItemStatus`, `WorkType` |
| Composite | Multiple related values | `DateRange`, `Address`, `Money` |

**See Also**:
- [Immutable Value Object](../patterns/value-object/immutable-value-object.md) (PAT-VO-001)
- [Enum Value Object](../patterns/value-object/enum-value-object.md) (PAT-VO-002)
- [Composite Value Object](../patterns/value-object/composite-value-object.md) (PAT-VO-003)

---

## Domain Services

### Service Classification

| Type | Layer | Characteristics |
|------|-------|-----------------|
| Domain Service | `domain/services/` | Pure domain logic, no I/O, stateless |
| Application Service | `application/handlers/` | Orchestrates use cases, uses ports |
| Infrastructure Service | `infrastructure/internal/` | Technical concerns, external I/O |

### Domain Service Pattern

```python
# src/domain/services/quality_validator.py
class QualityValidator:
    """Domain service for quality gate validation."""

    def validate_completion(self, work_item: WorkItem) -> QualityResult:
        """Validate work item meets quality criteria."""
        violations = []

        if not work_item.has_description:
            violations.append("Missing description")

        if work_item.subtask_count > 0 and not work_item.all_subtasks_done:
            violations.append("Incomplete subtasks")

        return QualityResult(
            passed=len(violations) == 0,
            violations=violations,
        )
```

### Application Service (Handler)

```python
# src/application/handlers/commands/complete_work_item_handler.py
class CompleteWorkItemCommandHandler:
    """Application service orchestrating work item completion."""

    def __init__(
        self,
        repository: IWorkItemRepository,
        quality_validator: QualityValidator,
    ) -> None:
        self._repository = repository
        self._validator = quality_validator

    def handle(self, command: CompleteWorkItemCommand) -> list[DomainEvent]:
        work_item = self._repository.get_or_raise(command.work_item_id)

        result = self._validator.validate_completion(work_item)
        if not result.passed:
            raise QualityGateFailedError(violations=result.violations)

        work_item.complete(quality_passed=True)
        self._repository.save(work_item)
        return work_item.collect_events()
```

**See Also**:
- [Domain Service Pattern](../patterns/domain-service/domain-service.md) (PAT-SVC-001)
- [Application Service Pattern](../patterns/domain-service/application-service.md) (PAT-SVC-002)

---

## Repository Pattern

### Repository Hierarchy

```
IRepository<TAggregate, TId>          # Domain port (abstract)
    │
    ├── InMemoryRepository            # Testing adapter
    ├── EventSourcedRepository        # Event sourcing adapter
    │       └── uses IEventStore
    └── SnapshottingRepository        # With snapshot optimization
            └── uses ISnapshotStore
```

### Generic Repository Port

```python
# src/domain/ports/repository.py
class IRepository(Protocol[TAggregate, TId]):
    def get(self, id: TId) -> TAggregate | None: ...
    def get_or_raise(self, id: TId) -> TAggregate: ...
    def save(self, aggregate: TAggregate) -> None: ...
    def delete(self, id: TId) -> bool: ...
    def exists(self, id: TId) -> bool: ...
```

### Event-Sourced Repository

```python
# src/infrastructure/adapters/persistence/event_sourced_repository.py
class EventSourcedWorkItemRepository:
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

**See Also**:
- [Generic Repository](../patterns/repository/generic-repository.md) (PAT-REPO-001)
- [Event-Sourced Repository](../patterns/repository/event-sourced-repository.md) (PAT-REPO-002)

---

## Bounded Contexts

### Context Structure

```
src/
├── session_management/        # BC: Project and session handling
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── interface/
│
├── work_tracking/             # BC: Task and work item management
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── interface/
│
├── problem_solving/           # BC: (Future) ps-* agent orchestration
│   └── (planned)
│
└── shared_kernel/             # Cross-context shared code
    ├── identity/
    ├── events/
    └── domain/
```

### Context Map

```
┌─────────────────────────────────────────────────────────────────┐
│                        Jerry Framework                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────────┐         ┌───────────────────┐           │
│  │ session_management│◄───────►│   work_tracking   │           │
│  │                   │   SK    │                   │           │
│  └─────────┬─────────┘         └─────────┬─────────┘           │
│            │                             │                      │
│            │ SK                          │ SK                   │
│            ▼                             ▼                      │
│  ┌─────────────────────────────────────────────────┐           │
│  │               shared_kernel                      │           │
│  │  - VertexId hierarchy    - DomainEvent          │           │
│  │  - IAuditable           - AggregateRoot         │           │
│  └─────────────────────────────────────────────────┘           │
│                                                                 │
│  Legend: SK = Shared Kernel, ◄──► = Partnership                │
└─────────────────────────────────────────────────────────────────┘
```

### Context Communication

Contexts communicate via:
1. **Domain Events** - Internal, within BC boundaries
2. **Integration Events** - CloudEvents format for external/cross-BC
3. **Shared Kernel** - Identity types and base classes only
4. **Anti-Corruption Layer** - For external systems (ADO, GitHub, etc.)

**Rule**: Never import directly across context boundaries except shared_kernel.

**See Also**: PAT-ARCH-003 in Pattern Catalog

---

## Validation Enforcement

These standards are enforced by:

1. **Architecture Tests**: `tests/architecture/test_composition_root.py`
2. **Import Validation**: AST-based import analysis
3. **CI Pipeline**: Automated boundary checks

### Test Examples

```python
def test_domain_has_no_infrastructure_imports():
    """Domain layer must not import infrastructure."""
    domain_files = Path("src/domain").rglob("*.py")
    for file in domain_files:
        imports = get_imports_from_file(file)
        assert not has_infrastructure_import(imports)

def test_application_has_no_interface_imports():
    """Application layer must not import interface."""
    app_files = Path("src/application").rglob("*.py")
    for file in app_files:
        imports = get_imports_from_file(file)
        assert not has_interface_import(imports)
```

---

## Primary and Secondary Adapters

### Primary Adapters (Driving)

Primary adapters drive the application from the outside:

| Adapter | Location | Purpose |
|---------|----------|---------|
| CLI Adapter | `interface/cli/` | Command-line interface |
| API Adapter | `interface/api/` | HTTP REST endpoints |
| Hook Adapter | `interface/hooks/` | Git/IDE integration |

**See Also**: [CLI Adapter Pattern](../patterns/adapter/cli-adapter.md) (PAT-ADP-001)

### Secondary Adapters (Driven)

Secondary adapters are driven by the application:

| Adapter | Location | Purpose |
|---------|----------|---------|
| Persistence | `infrastructure/adapters/persistence/` | Data storage |
| Messaging | `infrastructure/adapters/messaging/` | Event handling |
| External | `infrastructure/adapters/external/` | Third-party services |

**See Also**: [Persistence Adapter Pattern](../patterns/adapter/persistence-adapter.md) (PAT-ADP-002)

---

## References

### Pattern Files

| Pattern | File |
|---------|------|
| Hexagonal Architecture | [architecture/hexagonal-architecture.md](../patterns/architecture/hexagonal-architecture.md) |
| Ports and Adapters | [architecture/ports-adapters.md](../patterns/architecture/ports-adapters.md) |
| Bounded Contexts | [architecture/bounded-contexts.md](../patterns/architecture/bounded-contexts.md) |
| Composition Root | [architecture/composition-root.md](../patterns/architecture/composition-root.md) |
| Command Pattern | [cqrs/command-pattern.md](../patterns/cqrs/command-pattern.md) |
| Query Pattern | [cqrs/query-pattern.md](../patterns/cqrs/query-pattern.md) |
| Dispatcher Pattern | [cqrs/dispatcher-pattern.md](../patterns/cqrs/dispatcher-pattern.md) |
| Generic Repository | [repository/generic-repository.md](../patterns/repository/generic-repository.md) |
| Event Store | [event/event-store.md](../patterns/event/event-store.md) |

### Jerry Sources

- **Pattern Catalog**: `.claude/patterns/PATTERN-CATALOG.md`
- **Design Canon**: `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md`

### Industry References

- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Alistair Cockburn
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) - Robert C. Martin
- [CQRS](https://martinfowler.com/bliki/CQRS.html) - Martin Fowler
- [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) - Martin Fowler
- [Domain-Driven Design](https://www.domainlanguage.com/ddd/) - Eric Evans
