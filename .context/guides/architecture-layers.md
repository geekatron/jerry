# Architecture Layers Guide

> Educational companion to [architecture-standards.md](../rules/architecture-standards.md).
> Explains hexagonal architecture layer concepts, import rules rationale, and decision trees.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Hexagonal Architecture Overview](#hexagonal-architecture-overview) | Core concepts and philosophy |
| [Layer Responsibilities](#layer-responsibilities) | What belongs in each layer |
| [Import Rules Rationale](#import-rules-rationale) | Why dependency direction matters |
| [Decision Trees](#decision-trees) | How to choose the right layer |
| [Common Mistakes](#common-mistakes) | Anti-patterns and how to fix them |
| [Shared Kernel](#shared-kernel) | Cross-cutting concerns |
| [Enforcement Mechanisms](#enforcement-mechanisms) | How rules are checked |

---

## Hexagonal Architecture Overview

### Philosophy

Hexagonal Architecture (also called Ports and Adapters) is a pattern that **protects your domain logic from external concerns**. The key insight: your business rules shouldn't care whether data comes from a database, a file, or an HTTP API. They shouldn't care whether the UI is a CLI, web app, or API.

### The Hexagon Metaphor

```
                    ┌──────────────────────┐
                    │    Interface Layer   │  ← Primary Adapters (CLI, API, Hooks)
                    │   (Driving Side)     │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  Application Layer   │  ← Use Cases, Handlers
                    │   (Orchestration)    │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │    Domain Layer      │  ← Business Logic (Pure)
                    │   (Business Rules)   │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │ Infrastructure Layer │  ← Secondary Adapters (Persistence, External)
                    │   (Driven Side)      │
                    └──────────────────────┘
```

**Key Principle**: Dependencies point **inward**. Outer layers depend on inner layers, never the reverse.

### Why This Matters

1. **Testability**: Test business logic without databases or external APIs.
2. **Flexibility**: Swap infrastructure without touching domain code.
3. **Clarity**: Each layer has a clear, single responsibility.
4. **Longevity**: Business logic outlives technical choices.

---

## Layer Responsibilities

### Domain Layer (`src/domain/`)

**Purpose**: Pure business logic. No technical concerns.

**What belongs here**:
- **Aggregates**: Consistency boundaries (e.g., `WorkItem`, `Project`)
- **Entities**: Objects with identity and lifecycle
- **Value Objects**: Immutable values (e.g., `Priority`, `TaskId`)
- **Domain Events**: Things that happened (e.g., `WorkItemCompleted`)
- **Domain Services**: Logic that doesn't belong to a single entity
- **Domain Ports**: Interfaces the domain needs (e.g., `IRepository`)

**What NEVER belongs here**:
- HTTP requests, file I/O, database queries
- Framework-specific code (FastAPI, Click, SQLAlchemy)
- Infrastructure concerns (logging, metrics, caching)

**Example** (Valid):
```python
# src/domain/aggregates/work_item.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class WorkItem:
    """Aggregate root representing a unit of work."""
    id: str
    title: str
    status: Status

    def complete(self) -> None:
        """Complete the work item."""
        if self.status != Status.IN_PROGRESS:
            raise InvalidStateError(...)
        self.status = Status.COMPLETED
```

**Example** (Invalid):
```python
# WRONG: Domain importing infrastructure
from src.infrastructure.adapters.persistence.filesystem_adapter import FilesystemAdapter

class WorkItem:
    def save(self) -> None:
        adapter = FilesystemAdapter()  # ❌ Domain shouldn't know about persistence
        adapter.save(self)
```

---

### Application Layer (`src/application/`)

**Purpose**: Orchestrate use cases. Coordinate domain logic and infrastructure.

**What belongs here**:
- **Commands**: Intent to change state (e.g., `CreateWorkItemCommand`)
- **Queries**: Intent to read data (e.g., `ListWorkItemsQuery`)
- **Handlers**: Execute commands/queries
- **DTOs**: Data transfer objects for external communication
- **Application Ports**: Interfaces for infrastructure (e.g., `IEventStore`, `INotifier`)
- **Projections**: Read model definitions

**What NEVER belongs here**:
- Domain logic (that belongs in domain/)
- Concrete infrastructure implementations (adapters)
- UI/API details (routes, click decorators)

**Example** (Valid):
```python
# src/application/handlers/commands/create_work_item_command_handler.py
from src.domain.aggregates.work_item import WorkItem
from src.domain.ports.repository import IRepository

class CreateWorkItemCommandHandler:
    def __init__(self, repository: IRepository) -> None:
        self._repository = repository  # Port, not concrete adapter

    def handle(self, command: CreateWorkItemCommand) -> list[DomainEvent]:
        work_item = WorkItem.create(title=command.title)
        self._repository.save(work_item)
        return work_item.collect_events()
```

**Example** (Invalid):
```python
# WRONG: Application importing infrastructure
from src.infrastructure.adapters.persistence.filesystem_adapter import FilesystemAdapter

class CreateWorkItemCommandHandler:
    def __init__(self) -> None:
        self._repository = FilesystemAdapter()  # ❌ Should inject via port
```

---

### Infrastructure Layer (`src/infrastructure/`)

**Purpose**: Implement technical details. Adapt external systems to domain ports.

**What belongs here**:
- **Persistence Adapters**: Database, filesystem, in-memory implementations
- **Messaging Adapters**: Event stores, message queues
- **External Service Adapters**: GitHub API, ADO API, etc.
- **Read Models**: Optimized query data structures
- **Internal Utilities**: Serialization, file handling

**What NEVER belongs here**:
- Business rules (domain concern)
- Use case orchestration (application concern)
- UI/CLI code (interface concern)

**Example** (Valid):
```python
# src/infrastructure/adapters/persistence/filesystem_work_item_adapter.py
from pathlib import Path
from src.domain.aggregates.work_item import WorkItem
from src.domain.ports.repository import IRepository

class FilesystemWorkItemAdapter(IRepository[WorkItem, str]):
    """Filesystem implementation of work item repository."""

    def __init__(self, base_path: Path) -> None:
        self._base_path = base_path

    def save(self, aggregate: WorkItem) -> None:
        # Technical details isolated here
        path = self._base_path / f"{aggregate.id}.json"
        path.write_text(self._serialize(aggregate))
```

---

### Interface Layer (`src/interface/`)

**Purpose**: Adapt external inputs (CLI, API, hooks) to application use cases.

**What belongs here**:
- **CLI Adapters**: Click commands, argument parsing
- **API Adapters**: FastAPI routes, request/response handling
- **Hook Adapters**: Git hooks, IDE integrations
- **Presenters**: Format output for humans or machines

**What NEVER belongs here**:
- Business logic (delegate to application/domain)
- Persistence details (use application ports)

**Example** (Valid):
```python
# src/interface/cli/commands/work_item.py
import click
from src.application.commands.create_work_item_command import CreateWorkItemCommand
from src.application.ports.primary.icommanddispatcher import ICommandDispatcher

@click.command()
@click.argument("title")
def create_item(title: str, dispatcher: ICommandDispatcher) -> None:
    """Create a new work item."""
    command = CreateWorkItemCommand(title=title)
    dispatcher.dispatch(command)
    click.echo(f"Created: {title}")
```

---

## Import Rules Rationale

### Why Domain Can't Import Application/Infrastructure

**Reason**: Domain is the **stable core**. It contains business rules that change only when the business changes. If domain depends on infrastructure, then:

1. **Database changes force domain rewrites** → Violates Single Responsibility Principle
2. **Testing becomes hard** → Can't test domain without infrastructure
3. **Business logic gets polluted** → Technical concerns leak into domain

**Example of the problem**:
```python
# ❌ BAD: Domain importing infrastructure
from src.infrastructure.adapters.persistence.sqlalchemy_adapter import SessionFactory

class WorkItem:
    def save(self) -> None:
        session = SessionFactory.create()  # Now domain depends on SQLAlchemy!
        session.add(self)
        session.commit()
```

**Correct solution**:
```python
# ✅ GOOD: Domain defines a port
class IRepository(Protocol):
    def save(self, work_item: WorkItem) -> None: ...

# Infrastructure implements the port
class SqlAlchemyAdapter(IRepository):
    def save(self, work_item: WorkItem) -> None:
        # SQLAlchemy details isolated
```

### Why Application Can't Import Infrastructure

**Reason**: Application layer orchestrates **use cases**, not technical details. If application imports concrete adapters:

1. **Testing requires real infrastructure** → Slow, brittle tests
2. **Swapping implementations is hard** → Tight coupling
3. **Violates Dependency Inversion** → High-level depends on low-level

**Solution**: Application depends on **ports** (interfaces), infrastructure **implements** ports.

### Why Only Bootstrap Instantiates Infrastructure (H-09)

**Reason**: Centralized wiring. All dependency injection happens in **one place** (`src/bootstrap.py`).

**Benefits**:
1. **Easy to see the full dependency graph**
2. **Easy to swap implementations** (e.g., in-memory for tests)
3. **Prevents scattered `new` calls** throughout codebase

**Example**:
```python
# src/bootstrap.py
def create_command_dispatcher() -> CommandDispatcher:
    # Infrastructure adapters created here
    repository = FilesystemWorkItemAdapter(base_path=Path(".jerry"))
    event_store = InMemoryEventStore()

    # Handlers injected with adapters
    handler = CreateWorkItemCommandHandler(
        repository=repository,
        event_store=event_store,
    )

    # Dispatcher configured
    dispatcher = CommandDispatcher()
    dispatcher.register(CreateWorkItemCommand, handler.handle)
    return dispatcher
```

---

## Decision Trees

### "Where does this code go?"

```
START: What is the code's primary concern?

├─ Pure business logic (rules, invariants)?
│  └─ Domain Layer
│     ├─ Has identity and lifecycle? → Entity/Aggregate
│     ├─ Immutable value? → Value Object
│     ├─ Something that happened? → Domain Event
│     └─ Cross-entity logic? → Domain Service
│
├─ Orchestrating a use case (creating, updating, querying)?
│  └─ Application Layer
│     ├─ Change state? → Command + Handler
│     ├─ Read data? → Query + Handler
│     └─ Data for external use? → DTO
│
├─ Technical implementation (database, API, filesystem)?
│  └─ Infrastructure Layer
│     ├─ Stores/retrieves data? → Persistence Adapter
│     ├─ Calls external API? → External Service Adapter
│     └─ Handles events? → Event Store Adapter
│
└─ User interaction (CLI, API, hooks)?
   └─ Interface Layer
      ├─ Command-line? → CLI Adapter
      ├─ HTTP? → API Adapter
      └─ Git hook? → Hook Adapter
```

### "Can I import this?"

```
From: <YOUR_LAYER>
To: <TARGET_LAYER>

1. Same layer? → ✅ YES (prefer minimal coupling)
2. Inner layer? → ✅ YES (dependency points inward)
3. shared_kernel? → ✅ YES (cross-cutting)
4. Outer layer? → ❌ NO (violates dependency rule)

Examples:
- Application importing Domain? ✅ YES
- Domain importing Application? ❌ NO
- Infrastructure importing Domain? ✅ YES
- Domain importing Infrastructure? ❌ NO
- Interface importing Application? ✅ YES
- Application importing Interface? ❌ NO
```

### "Should this be a Domain Service or Application Service?"

```
Does the logic involve:

├─ Only domain concepts (entities, value objects)?
│  ├─ Coordinates multiple aggregates?
│  │  └─ Domain Service (pure, no I/O)
│  └─ Single aggregate?
│     └─ Method on the aggregate itself
│
└─ Infrastructure (repositories, external APIs)?
   └─ Application Service (handler)
```

**Example**:
- **Domain Service**: `QualityValidator.validate_completion(work_item)` → Pure logic, no I/O
- **Application Service**: `CompleteWorkItemHandler.handle(command)` → Loads from repo, calls domain service, saves

---

## Common Mistakes

### Mistake 1: Domain importing infrastructure

**Problem**:
```python
# src/domain/aggregates/work_item.py
from src.infrastructure.adapters.persistence.filesystem_adapter import FilesystemAdapter

class WorkItem:
    def save(self) -> None:
        adapter = FilesystemAdapter()
        adapter.save(self)
```

**Why it's wrong**: Domain now depends on filesystem implementation. Can't test without filesystem. Can't swap to database.

**Fix**: Move persistence to application layer.
```python
# src/application/handlers/commands/create_work_item_command_handler.py
class CreateWorkItemCommandHandler:
    def __init__(self, repository: IRepository) -> None:
        self._repository = repository

    def handle(self, command: CreateWorkItemCommand) -> None:
        work_item = WorkItem.create(title=command.title)
        self._repository.save(work_item)  # Handler saves, not domain
```

---

### Mistake 2: Application instantiating infrastructure

**Problem**:
```python
# src/application/handlers/commands/handler.py
from src.infrastructure.adapters.persistence.filesystem_adapter import FilesystemAdapter

class CreateWorkItemCommandHandler:
    def __init__(self) -> None:
        self._repository = FilesystemAdapter()  # Instantiating concrete adapter
```

**Why it's wrong**: Handler is coupled to filesystem. Can't inject mock for testing.

**Fix**: Inject via constructor (Dependency Injection).
```python
class CreateWorkItemCommandHandler:
    def __init__(self, repository: IRepository) -> None:  # Port, not adapter
        self._repository = repository
```

---

### Mistake 3: Multiple classes per file

**Problem**:
```python
# src/domain/aggregates/work_item.py
class WorkItem:
    ...

class Task:  # ❌ Violates H-10
    ...
```

**Why it's wrong**: Harder to navigate codebase. Harder to reuse. Violates H-10.

**Fix**: One public class per file.
```python
# src/domain/aggregates/work_item.py
class WorkItem:
    ...

# src/domain/aggregates/task.py
class Task:
    ...
```

---

### Mistake 4: Business logic in CLI/API adapter

**Problem**:
```python
# src/interface/cli/commands/work_item.py
@click.command()
def complete_item(item_id: str) -> None:
    item = load_from_file(item_id)
    if item.status != Status.IN_PROGRESS:  # ❌ Business logic in interface layer
        raise ValueError("Can't complete")
    item.status = Status.COMPLETED
    save_to_file(item)
```

**Why it's wrong**: Business rules duplicated in UI layer. Can't reuse via API.

**Fix**: Delegate to application layer.
```python
@click.command()
def complete_item(item_id: str, dispatcher: ICommandDispatcher) -> None:
    command = CompleteWorkItemCommand(work_item_id=item_id)
    dispatcher.dispatch(command)  # Business logic in handler
```

---

### Mistake 5: Query returning domain entities

**Problem**:
```python
class ListWorkItemsQuery:
    ...

class ListWorkItemsQueryHandler:
    def handle(self, query: ListWorkItemsQuery) -> list[WorkItem]:  # ❌ Returning entities
        return self._repository.list()
```

**Why it's wrong**: Exposes domain entities to external world. Couples UI to domain structure.

**Fix**: Return DTOs.
```python
@dataclass(frozen=True)
class WorkItemDTO:
    id: str
    title: str
    status: str

class ListWorkItemsQueryHandler:
    def handle(self, query: ListWorkItemsQuery) -> list[WorkItemDTO]:
        items = self._repository.list()
        return [WorkItemDTO(id=i.id, title=i.title, status=i.status.value) for i in items]
```

---

## Shared Kernel

### What is Shared Kernel?

**Purpose**: Code shared across **bounded contexts** that would otherwise be duplicated.

**What belongs in `shared_kernel/`**:
- **Identity types**: `VertexId`, `SnowflakeIdGenerator`
- **Base classes**: `DomainEvent`, `AggregateRoot`, `Entity`
- **Common protocols**: `IAuditable`, `IVersioned`
- **Exception base classes**: `DomainError`

**What does NOT belong in shared kernel**:
- Infrastructure adapters (those go in `infrastructure/`)
- Application-specific logic (those go in bounded contexts)
- Cross-context communication (use domain events)

### Import Rules for Shared Kernel

- **Domain MAY import shared_kernel** (exception to the "stdlib only" rule)
- **Application MAY import shared_kernel**
- **Infrastructure MAY import shared_kernel**

**Example**:
```python
# src/shared_kernel/identity/vertex_id.py
@dataclass(frozen=True)
class VertexId:
    """Base class for all identity types."""
    value: str

# src/domain/aggregates/work_item.py
from src.shared_kernel.identity.vertex_id import VertexId  # ✅ Allowed

@dataclass(frozen=True)
class WorkItemId(VertexId):
    """Work item identifier."""
```

---

## Enforcement Mechanisms

### 1. Architecture Tests

**Purpose**: Automated checks for layer boundary violations.

**Location**: `tests/architecture/test_*.py`

**Example**:
```python
def test_domain_has_no_infrastructure_imports():
    """Verify domain layer doesn't import infrastructure."""
    domain_files = Path("src/domain").rglob("*.py")
    for file in domain_files:
        imports = extract_imports(file)
        assert not any("infrastructure" in imp for imp in imports), \
            f"{file} violates H-07"
```

**Run**: `uv run pytest tests/architecture/`

---

### 2. CI Pipeline

**Where**: `.github/workflows/ci.yml`

**What it does**:
1. Runs architecture tests
2. Fails the build if violations detected
3. Blocks merge to main

---

### 3. AST Analysis (H-10)

**Purpose**: Enforce one-class-per-file rule.

**How**: Parse Python AST, count public class definitions.

**Location**: `tests/architecture/test_composition_root.py`

---

### 4. Manual Code Review

- Reviewers check for layer violations
- Look for imports that violate dependency rules
- Verify H-09 (only bootstrap instantiates infrastructure)

---

## References

### Related Documents

- [Architecture Standards](../rules/architecture-standards.md) - Enforcement rules (H-07 through H-10)
- [Architecture Patterns Guide](architecture-patterns.md) - Port/adapter pattern details
- [Coding Practices Guide](coding-practices.md) - Type hints, imports

### External References

- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Alistair Cockburn
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) - Robert C. Martin
- [Dependency Inversion Principle](https://en.wikipedia.org/wiki/Dependency_inversion_principle) - Wikipedia
