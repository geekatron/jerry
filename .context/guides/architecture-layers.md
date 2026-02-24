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
| [Evidence](#evidence) | Verified codebase file paths and code quotes |

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
# (Hypothetical -- illustrative pattern)
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

**Real codebase example**: See `src/session_management/domain/aggregates/session.py` for the actual `Session` aggregate with `complete()` and `abandon()` methods.

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

### Why Only Bootstrap Instantiates Infrastructure (H-07)

**Reason**: Centralized wiring. All dependency injection happens in **one place** (`src/bootstrap.py`).

**Benefits**:
1. **Easy to see the full dependency graph**
2. **Easy to swap implementations** (e.g., in-memory for tests)
3. **Prevents scattered `new` calls** throughout codebase

**Example** (simplified from the real `src/bootstrap.py`):
```python
# (From: src/bootstrap.py, lines 436-500 -- simplified)
def create_command_dispatcher() -> CommandDispatcher:
    # Infrastructure singletons created here
    session_repository = get_session_repository()
    work_item_repository = get_work_item_repository()
    id_generator = get_id_generator()

    # Handlers injected with adapters
    create_work_item_handler = CreateWorkItemCommandHandler(
        repository=work_item_repository,
        id_generator=id_generator,
    )

    # Dispatcher configured
    dispatcher = CommandDispatcher()
    dispatcher.register(CreateWorkItemCommand, create_work_item_handler.handle)
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

### Ambiguous Cases: "Where does this code go?"

| Question | Guidance |
|----------|----------|
| **Validation logic** -- domain or application? | If it checks a business invariant (e.g., "percentages must sum to 100%"), it belongs in the **domain**. If it validates input format (e.g., "title must be non-empty string"), it can live in the **command/query dataclass** (application layer). |
| **Logging** -- which layer? | Logging is a cross-cutting concern. Infrastructure adapters MAY log I/O operations. Application handlers MAY log use case entry/exit. Domain MUST NOT log (pure logic). |
| **Configuration reading** -- domain or infrastructure? | Reading config files/env vars is **infrastructure**. The config values themselves may be domain value objects. Use a port to abstract config access. |
| **ID generation** -- domain or infrastructure? | ID format/validation is **domain** (e.g., `ProjectId.parse()`). ID generation mechanics (UUID, Snowflake) are **shared_kernel** or **infrastructure**. Jerry uses `shared_kernel/snowflake_id.py`. |
| **Serialization** -- application or infrastructure? | Serialization to/from external formats (JSON, TOML, TOON) is **infrastructure**. DTOs that define the shape of data are **application**. |
| **Cross-context communication?** | Use **domain events** via shared_kernel, not direct imports. If you need to reference another context's entity, use its ID (a value object) from shared_kernel, not the entity itself. |

**Escalation**: If the decision tree and ambiguous cases table don't resolve your question, invoke `/architecture` skill for a design decision review.

---

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
- Verify H-07 (only bootstrap instantiates infrastructure)

---

## Evidence

> Verified references to actual Jerry codebase files demonstrating the layer architecture.

### Layer Structure -- Real Directory Layout

```
src/
  bootstrap.py                                           # Composition root (H-07)
  shared_kernel/                                         # Cross-cutting: VertexId, DomainEvent, exceptions
  application/
    dispatchers/query_dispatcher.py                      # QueryDispatcher (routes queries)
    dispatchers/command_dispatcher.py                    # CommandDispatcher (routes commands)
    handlers/queries/retrieve_project_context_query_handler.py
    handlers/queries/scan_projects_query_handler.py
    ports/primary/iquerydispatcher.py                    # Primary port (Protocol)
    ports/primary/icommanddispatcher.py                  # Primary port (Protocol)
    ports/secondary/iread_model_store.py                 # Secondary port (Protocol)
    queries/retrieve_project_context_query.py            # Query dataclass
  infrastructure/
    adapters/persistence/filesystem_local_context_adapter.py  # Secondary adapter
    adapters/persistence/atomic_file_adapter.py
    adapters/serialization/toon_serializer.py
    read_models/in_memory_read_model_store.py
  interface/
    cli/adapter.py                                       # CLI adapter
    cli/main.py                                          # CLI entry point
  session_management/                                    # Bounded context
    domain/aggregates/session.py                         # Session aggregate
    domain/value_objects/project_id.py                   # ProjectId value object
    domain/events/session_events.py                      # Domain events
    application/commands/create_session_command.py        # Command
    application/handlers/commands/create_session_command_handler.py
    infrastructure/adapters/filesystem_project_adapter.py # Adapter
```

### Composition Root (H-07) -- Real Implementation

**`src/bootstrap.py`** is the sole composition root. It:
- Imports ALL infrastructure adapters (lines 47-106)
- Creates singleton instances via factory functions
- Wires handlers with their dependencies
- Exposes `create_query_dispatcher()` and `create_command_dispatcher()`

```python
# (From: src/bootstrap.py, lines 1-8)
"""
Composition Root - Application Bootstrap.

This module is the sole owner of dependency wiring.
It creates infrastructure adapters and wires them to handlers.

The key principle: NO adapter should instantiate its own dependencies.
All dependencies are created HERE and injected.
"""
```

### Architecture Tests -- Real Files

| Test File | What It Verifies |
|-----------|-----------------|
| `tests/architecture/test_composition_root.py` | Bootstrap imports infrastructure; dispatchers/ports do not (H-07) |
| `tests/architecture/test_config_boundaries.py` | Domain has no infra/app imports; adapters implement ports |
| `tests/session_management/architecture/test_architecture.py` | Per-context: domain layer stdlib-only, dependency direction inward |

**`tests/architecture/test_composition_root.py`** -- AST-based import checking:
```python
# (From: tests/architecture/test_composition_root.py, lines 84-92)
def test_bootstrap_imports_infrastructure(self) -> None:
    """Bootstrap legitimately imports from infrastructure."""
    bootstrap_path = Path("src/bootstrap.py")
    assert bootstrap_path.exists(), "bootstrap.py must exist"

    imports = get_imports_from_file(bootstrap_path)

    # Bootstrap SHOULD import infrastructure
    assert has_infrastructure_import(imports), "Bootstrap must import infrastructure adapters"
```

### Bounded Contexts -- Real Structure

Jerry currently has these bounded contexts under `src/`:

| Context | Path | Domain Entities |
|---------|------|-----------------|
| Session Management | `src/session_management/` | `Session`, `ProjectId`, `SessionId`, `ProjectInfo` |
| Work Tracking | `src/work_tracking/` | Work items, event-sourced repository |
| Transcript | `src/transcript/` | VTT parsing, chunking |
| Configuration | `src/configuration/` | Config aggregates, value objects |

### CI Pipeline Enforcement

**`.github/workflows/ci.yml`** runs architecture tests as part of the `test-pip` and `test-uv` jobs (lines 239-251 and 325-336). Architecture test failures block merge to main.

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
