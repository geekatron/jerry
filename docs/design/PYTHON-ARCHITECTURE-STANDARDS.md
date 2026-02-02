# Python Architecture Standards for Jerry Framework

> **Version**: 1.0.0
> **Date**: 2026-01-12
> **Status**: APPROVED
> **Related**: BUG-006, DISC-011, ADR-003

---

## Executive Summary

This document establishes Python-specific coding standards for Domain-Driven Design (DDD), Hexagonal Architecture, and CQRS patterns within the Jerry Framework. These standards ensure consistency, maintainability, and architectural integrity across all bounded contexts.

---

## Table of Contents

1. [Core Principles](#core-principles)
2. [Hexagonal Architecture](#hexagonal-architecture)
3. [CQRS Pattern](#cqrs-pattern)
4. [Domain-Driven Design](#domain-driven-design)
5. [Port Design](#port-design)
6. [Adapter Boundaries](#adapter-boundaries)
7. [CLI Standards](#cli-standards)
8. [Token Efficiency](#token-efficiency)
9. [Enforcement Levels](#enforcement-levels)
10. [Anti-Patterns](#anti-patterns)

---

## Core Principles

### Principle 1: Dependency Direction

```
Interface Layer → Application Layer → Domain Layer
    (outer)           (middle)           (inner)

Dependencies ONLY point inward. Inner layers NEVER depend on outer layers.
```

### Principle 2: Zero-Dependency Domain

The Domain layer has NO external dependencies:
- Only Python stdlib allowed
- No framework imports
- No infrastructure imports
- Pure business logic only

### Principle 3: Port-Based Boundaries

All external communication goes through ports (interfaces):
- **Primary Ports**: Drive the application (CLI, API, hooks)
- **Secondary Ports**: Driven by the application (repositories, external services)

---

## Hexagonal Architecture

### Layer Responsibilities

| Layer | Location | Responsibility | MAY Import |
|-------|----------|----------------|------------|
| **Domain** | `src/{context}/domain/` | Business logic, entities, value objects | stdlib only |
| **Application** | `src/{context}/application/` | Use cases, orchestration, ports | domain |
| **Infrastructure** | `src/{context}/infrastructure/` | Adapters implementing ports | domain, application |
| **Interface** | `src/interface/` | Primary adapters (CLI, API) | all inner layers |

### Directory Structure per Bounded Context

```
src/{bounded_context}/
├── domain/
│   ├── entities/           # Mutable domain objects with identity
│   ├── value_objects/      # Immutable objects defined by attributes
│   ├── aggregates/         # Aggregate roots (transaction boundaries)
│   ├── events/             # Domain events (past tense)
│   └── exceptions.py       # Domain-specific exceptions
├── application/
│   ├── ports/              # Secondary port interfaces (Protocol classes)
│   ├── queries/            # Query objects with execute() method
│   ├── commands/           # Command objects with execute() method
│   └── dtos/               # Data Transfer Objects for boundaries
└── infrastructure/
    └── adapters/           # Port implementations
```

---

## CQRS Pattern

### Dispatcher Pattern (REQUIRED)

Jerry uses the **Dispatcher Pattern** with proper handler separation. Direct `.execute()` calls from adapters are **NOT PERMITTED**.

```
REQUIRED Architecture:
┌─────────────┐     ┌────────────┐     ┌─────────────┐     ┌───────────────┐
│   Adapter   │ ──▶ │ Dispatcher │ ──▶ │   Handler   │ ──▶ │ Query/Command │
│             │     │            │     │             │     │               │
│ - Parse     │     │ - Route    │     │ - Validate  │     │ - Execute     │
│ - Map DTO   │     │ - Resolve  │     │ - Authorize │     │ - Domain      │
│ - Format    │     │ - Dispatch │     │ - Orchestrate│    │   Logic       │
└─────────────┘     └────────────┘     └─────────────┘     └───────────────┘
```

### Dispatcher Implementation

```python
# src/application/dispatcher.py
from typing import Protocol, TypeVar, Generic

TQuery = TypeVar("TQuery")
TResult = TypeVar("TResult")

class IQueryDispatcher(Protocol):
    """Dispatcher for routing queries to handlers."""

    def dispatch(self, query: TQuery) -> TResult: ...


class QueryDispatcher:
    """Concrete dispatcher with handler registration."""

    def __init__(self) -> None:
        self._handlers: dict[type, type] = {}

    def register(self, query_type: type, handler_type: type) -> None:
        """Register a handler for a query type."""
        self._handlers[query_type] = handler_type

    def dispatch(self, query: TQuery, container: IContainer) -> TResult:
        """Dispatch query to registered handler."""
        handler_type = self._handlers.get(type(query))
        if not handler_type:
            raise UnregisteredQueryError(f"No handler for {type(query).__name__}")

        handler = container.resolve(handler_type)
        return handler.handle(query)
```

### Query and Handler Separation

```python
# Query (DTO - no logic)
@dataclass(frozen=True)
class ScanProjectsQuery:
    """Query to scan for all available projects."""
    base_path: str


# Handler (contains orchestration logic)
class ScanProjectsHandler:
    """Handles ScanProjectsQuery execution."""

    def __init__(self, repository: IProjectRepository) -> None:
        self._repository = repository

    def handle(self, query: ScanProjectsQuery) -> list[ProjectInfo]:
        """Execute the query and return results."""
        return self._repository.scan_projects(query.base_path)
```

### Key Rules (HARD ENFORCEMENT)

1. **Adapters NEVER call `.execute()` directly** - must go through dispatcher
2. **Queries are frozen DTOs** - no logic, no methods except `__init__`
3. **Handlers contain orchestration** - validation, authorization, domain calls
4. **One query + one handler per file pair**
5. **Dispatcher is injected into adapters** - not instantiated in adapter

### Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Query | `{Verb}{Noun}Query` | `ScanProjectsQuery`, `GetProjectContextQuery` |
| Command | `{Verb}{Noun}Command` | `CreateProjectCommand`, `UpdateStatusCommand` |
| Handler | `{Query/Command}Handler` | `ScanProjectsQueryHandler` (if using handlers) |

### Return Types

```python
# Queries return domain objects or DTOs
def execute(self) -> list[ProjectInfo]: ...
def execute(self) -> tuple[ProjectId | None, ValidationResult]: ...

# Commands return None or domain events
def execute(self) -> None: ...
def execute(self) -> list[DomainEvent]: ...
```

---

## Domain-Driven Design

### Entities

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar

@dataclass
class ProjectInfo:
    """Project entity with identity and audit metadata."""

    id: ProjectId                          # Identity
    status: ProjectStatus
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None
    version: int = 1

    # Class-level invariant documentation
    INVARIANTS: ClassVar[list[str]] = [
        "id must be valid ProjectId format",
        "status transitions follow state machine",
    ]

    def touch(self) -> None:
        """Update the modification timestamp."""
        self.updated_at = datetime.utcnow()
```

### Value Objects

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)  # MUST be frozen
class ProjectId:
    """Immutable project identifier."""

    number: int
    slug: str

    def __post_init__(self) -> None:
        if not (1 <= self.number <= 999):
            raise InvalidProjectIdError("Number must be 1-999")
        if not self.slug:
            raise InvalidProjectIdError("Slug required")

    def __str__(self) -> str:
        return f"PROJ-{self.number:03d}-{self.slug}"
```

### Domain Events

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class ProjectCreated:  # Past tense
    """Raised when a new project is created."""

    project_id: ProjectId
    occurred_at: datetime
    created_by: str
```

---

## Port Design

### One Port per Bounded Context

Each bounded context exposes ONE primary port interface:

```python
# src/session_management/application/ports/session_port.py
class ISessionManagementPort(Protocol):
    """Primary port for Session Management bounded context."""

    def get_project_context(self, project_id: str) -> ProjectContext: ...
    def scan_projects(self, base_path: str) -> list[ProjectInfo]: ...
    def validate_project(self, project_id: str) -> ValidationResult: ...


# src/work_tracking/application/ports/worktracker_port.py
class IWorkTrackerPort(Protocol):
    """Primary port for Work Tracking bounded context."""

    def create_task(self, task: TaskDTO) -> TaskId: ...
    def list_tasks(self, filters: TaskFilters) -> list[TaskDTO]: ...
    def update_status(self, task_id: TaskId, status: TaskStatus) -> None: ...
```

### Secondary Ports (Infrastructure Interfaces)

```python
# Repository port (secondary)
class IProjectRepository(Protocol):
    """Secondary port for project persistence."""

    def scan_projects(self, base_path: str) -> list[ProjectInfo]: ...
    def get_project(self, base_path: str, project_id: ProjectId) -> ProjectInfo | None: ...
    def validate_project(self, base_path: str, project_id: ProjectId) -> ValidationResult: ...
    def project_exists(self, base_path: str, project_id: ProjectId) -> bool: ...


# Environment port (secondary)
class IEnvironmentProvider(Protocol):
    """Secondary port for environment variable access."""

    def get_env(self, name: str) -> str | None: ...
    def get_env_or_default(self, name: str, default: str) -> str: ...
```

---

## Adapter Boundaries

### What Adapters MAY Do

| Allowed Action | Example |
|----------------|---------|
| Parse input | `argparse`, JSON/TOON parsing |
| Validate syntax | Check argument formats |
| Wire dependencies | Instantiate adapters, inject into queries |
| Call use cases | `query.execute()` |
| Format output | JSON, table, TOON serialization |
| Catch/translate exceptions | Convert domain errors to exit codes |

### What Adapters MAY NOT Do

| Forbidden Action | Why |
|------------------|-----|
| Contain business rules | Business logic belongs in domain |
| Call repositories directly | Must go through use cases |
| Decide which aggregate to load | Domain decision |
| Modify domain state | Only commands modify state |
| Import from other adapters | Coupling violation |

### Composition Root Pattern (EXTERNAL TO ADAPTER)

The Composition Root is **NOT** inside adapters. Dependency wiring happens at application startup, OUTSIDE the adapter:

```python
# WRONG - "Poor Man's DI" in adapter (VIOLATION)
def cmd_init(args: argparse.Namespace) -> int:
    repository = FilesystemProjectAdapter()  # WRONG: Adapter wires dependencies
    query = GetProjectContextQuery(repository=repository)
    context = query.execute()  # WRONG: Direct execution
```

```python
# CORRECT - Adapter receives pre-wired dispatcher
class CLIAdapter:
    """Primary adapter for CLI interface."""

    def __init__(self, dispatcher: IQueryDispatcher) -> None:
        """Dispatcher injected from composition root."""
        self._dispatcher = dispatcher

    def cmd_init(self, args: argparse.Namespace) -> int:
        """Execute init command via dispatcher."""
        query = GetProjectContextQuery(base_path=get_projects_directory())
        try:
            context = self._dispatcher.dispatch(query)
        except DomainError as e:
            return format_error(args, e)
        return format_output(args, context)
```

```python
# Composition Root (src/bootstrap.py) - SEPARATE FROM ADAPTER
def create_application() -> CLIAdapter:
    """Wire all dependencies at application startup."""

    # Create infrastructure adapters
    repository = FilesystemProjectAdapter()
    environment = OsEnvironmentAdapter()

    # Create handlers with dependencies
    handlers = {
        GetProjectContextQuery: GetProjectContextHandler(repository, environment),
        ScanProjectsQuery: ScanProjectsHandler(repository),
        ValidateProjectQuery: ValidateProjectHandler(repository),
    }

    # Create dispatcher with registered handlers
    dispatcher = QueryDispatcher(handlers)

    # Return adapter with injected dispatcher
    return CLIAdapter(dispatcher)
```

---

## CLI Standards

### Namespace per Bounded Context (HARD REQUIREMENT)

Each bounded context gets its own CLI subcommand namespace:

```bash
jerry session <command>          # Session Management bounded context
jerry worktracker <command>      # Work Tracker bounded context
jerry projects <command>         # Project Management bounded context
```

**This mirrors:**
- **Bounded Contexts**: Each namespace maps to a distinct domain
- **Authorization Scopes**: Security boundaries align with namespaces
- **Threat Models**: Attack surface isolation per bounded context
- **Use Case Ports**: Each namespace routes to a distinct application service

**Architecture:**
```
CLI Command → Use Case (Application Service) → Domain
     │
     ├── jerry session → ISessionManagementPort
     ├── jerry worktracker → IWorkTrackerPort
     └── jerry projects → IProjectManagementPort
```

### CLI Adapter Rules (HARD ENFORCEMENT)

| Rule | Description |
|------|-------------|
| **Rule 1** | CLI is a Primary Adapter - translates user intent to use case invocation |
| **Rule 2** | CLI NEVER contains business logic |
| **Rule 3** | CLI NEVER knows infrastructure details |
| **Rule 4** | Routing is pure orchestration, not logic |
| **Rule 5** | CLI structure reflects actor intent, not domain structure |
| **Rule 6** | Ports represent use cases, NOT interfaces - do NOT mirror CLI structure |

### Multi-Format Output Support

The CLI MUST support three output formats:

| Format | Flag | Purpose | Priority |
|--------|------|---------|----------|
| **TOON** | `--toon` (default) | Token-efficient for LLM consumption | PRIMARY |
| **JSON** | `--json` | Machine-readable structured data | SECONDARY |
| **Human** | `--human` | Human-readable tables/text | TERTIARY |

### TOON (Token-Object Oriented Notation)

TOON is a token-efficient format optimized for LLM context windows:

```toon
# TOON Format Example
P:PROJ-001-plugin-cleanup|S:active|V:true
P:PROJ-002-api-redesign|S:draft|V:true
#T:2
```

**TOON Rules:**
- Single-character field prefixes (`P:` = project, `S:` = status, `V:` = valid)
- Pipe-delimited fields
- Hash-prefixed metadata (`#T:` = total count)
- No whitespace except in values
- Newline-separated records

### CLI Argument Structure

```bash
jerry [--format toon|json|human] <command> [subcommand] [args]

# Examples:
jerry --toon projects list          # TOON output (default)
jerry --json projects list          # JSON output
jerry projects list                 # Human-readable output
jerry projects validate PROJ-001
```

### Input Format Support

```python
def parse_input(args: argparse.Namespace) -> dict:
    """Parse input from various formats."""

    if args.stdin:
        raw = sys.stdin.read()
        if raw.startswith('{'):
            return json.loads(raw)
        elif '|' in raw:
            return parse_toon(raw)
        else:
            return parse_args(raw)

    return vars(args)
```

---

## Token Efficiency

### Principle: Minimize Token Usage

Token efficiency is PARAMOUNT for LLM-consumed output:

| Approach | Tokens | Preference |
|----------|--------|------------|
| TOON | ~50 | ✅ PREFERRED |
| JSON | ~150 | Acceptable |
| Human table | ~300 | Last resort |

### TOON Serialization Implementation

```python
def to_toon(projects: list[ProjectInfo]) -> str:
    """Serialize projects to TOON format."""
    lines = []
    for p in projects:
        lines.append(f"P:{p.id}|S:{p.status.name.lower()}|V:{p.is_valid}")
    lines.append(f"#T:{len(projects)}")
    return "\n".join(lines)


def from_toon(toon: str) -> list[dict]:
    """Parse TOON format to structured data."""
    result = []
    for line in toon.strip().split("\n"):
        if line.startswith("#"):
            continue  # Metadata
        fields = {}
        for pair in line.split("|"):
            key, value = pair.split(":", 1)
            fields[TOON_KEYS[key]] = value
        result.append(fields)
    return result


TOON_KEYS = {
    "P": "project_id",
    "S": "status",
    "V": "is_valid",
    "T": "total",
    "E": "error",
}
```

---

## Enforcement Levels

| Level | Meaning | Violation Consequence |
|-------|---------|----------------------|
| **HARD** | Cannot override | Blocked at CI/review |
| **MEDIUM** | Override with justification | Documented exception |
| **SOFT** | Guideline | Best effort |

### Hard Rules (Non-Negotiable)

- Domain layer has zero external dependencies
- Adapters never contain business logic
- Dependency direction is inward only
- Value objects are frozen dataclasses
- One query/command per file

### Medium Rules (Override with ADR)

- Query Object vs Handler pattern
- TOON vs JSON default output
- Port granularity per bounded context

### Soft Rules (Guidelines)

- Naming conventions
- File organization within layers
- Comment style

---

## Anti-Patterns

### Anti-Pattern 1: Adapter with Business Logic

```python
# WRONG - Business logic in adapter
def cmd_validate(args):
    if args.project_id.startswith("PROJ-"):  # Business rule!
        # ...
```

```python
# CORRECT - Delegate to domain
def cmd_validate(args):
    query = ValidateProjectQuery(...)
    result = query.execute()  # Domain validates
```

### Anti-Pattern 2: Direct Repository Access

```python
# WRONG - Adapter calls repository directly
def cmd_list(args):
    repo = FilesystemProjectAdapter()
    projects = repo.scan_projects(base_path)  # Bypasses use case!
```

```python
# CORRECT - Use query object
def cmd_list(args):
    query = ScanProjectsQuery(repository=repo, base_path=base_path)
    projects = query.execute()
```

### Anti-Pattern 3: Mutable Value Objects

```python
# WRONG - Value object is mutable
@dataclass
class ProjectId:
    number: int  # Can be changed!
```

```python
# CORRECT - Frozen dataclass
@dataclass(frozen=True, slots=True)
class ProjectId:
    number: int  # Immutable
```

### Anti-Pattern 4: Cross-Adapter Imports

```python
# WRONG - Adapter imports another adapter
from src.interface.api.serializers import ProjectSerializer
```

```python
# CORRECT - Shared serialization in application/dtos/
from src.session_management.application.dtos import ProjectDTO
```

---

## References

- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Alistair Cockburn
- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html) - Martin Fowler
- [Domain-Driven Design](https://www.domainlanguage.com/ddd/) - Eric Evans
- [Query Object Pattern](https://martinfowler.com/eaaCatalog/queryObject.html) - Fowler PoEAA
- [Context Rot Research](https://research.trychroma.com/context-rot) - Chroma

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-12 | Claude | Initial creation from DISC-011 research |
