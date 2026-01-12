# Architecture Standards

> Hexagonal Architecture, CQRS, and Event Sourcing standards for Jerry.
> These rules are enforced via architecture tests.

**Authoritative Pattern Source**: `.claude/patterns/PATTERN-CATALOG.md`

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

---

## Bounded Contexts

### Context Structure

```
src/
├── session_management/        # Project and session handling
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── interface/
│
├── work_tracking/             # Task and work item management
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── interface/
│
└── shared_kernel/             # Cross-context shared code
    ├── identity/
    ├── events/
    └── domain/
```

### Context Communication

Contexts communicate via:
1. **Domain Events** - Async, decoupled
2. **Shared Kernel** - Common types only
3. **Anti-Corruption Layer** - For external systems

**Rule**: Never import directly across context boundaries except shared_kernel.

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

## References

- **Pattern Catalog**: `.claude/patterns/PATTERN-CATALOG.md`
- **Design Canon**: `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md`
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Alistair Cockburn
- [CQRS](https://martinfowler.com/bliki/CQRS.html) - Martin Fowler
- [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) - Martin Fowler
