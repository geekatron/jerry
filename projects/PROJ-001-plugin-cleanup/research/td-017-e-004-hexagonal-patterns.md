# TD-017 Research: Hexagonal Architecture Patterns

> **Entry ID**: td-017-e-004
> **Date**: 2026-01-11
> **Topic**: Clean Architecture / Hexagonal Architecture Patterns
> **Author**: Claude Code (PS-Researcher Role)
> **Status**: COMPLETE

---

## Executive Summary

This research document establishes authoritative definitions and patterns for hexagonal (ports and adapters) architecture as implemented in Jerry. It consolidates industry best practices from Alistair Cockburn's original work, Robert C. Martin's Clean Architecture, and modern Python implementations.

**Key Findings**:
1. Jerry's current implementation aligns with authoritative sources
2. The composition root pattern in `bootstrap.py` follows Clean Architecture best practices
3. Port classification (primary/secondary) matches Cockburn's original definitions
4. Layer dependency rules enforce proper isolation

---

## Table of Contents

1. [Authoritative Definitions](#1-authoritative-definitions)
2. [Layer Dependency Rules](#2-layer-dependency-rules)
3. [Port and Adapter Classification](#3-port-and-adapter-classification)
4. [Composition Root Pattern](#4-composition-root-pattern)
5. [Jerry-Specific Implementations](#5-jerry-specific-implementations)
6. [Sources and References](#6-sources-and-references)

---

## 1. Authoritative Definitions

### 1.1 Hexagonal Architecture (Alistair Cockburn, 2005)

The canonical definition from the pattern author:

> "Allow an application to equally be driven by users, programs, automated test or batch scripts, and to be developed and tested in isolation from its eventual run-time devices and databases."
> -- [Alistair Cockburn, Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)

**Core Motivation**: Prevent business logic infiltration into UI code, enabling automated testing, batch processing, and inter-application communication.

**Historical Context**:
- 1994: Cockburn begins teaching the concept
- 2005: Formal naming as "Ports and Adapters" by Kevin Rutherford
- 2012: Adoption by Domain-Driven Design community
- 2024: Definitive book "Hexagonal Architecture Explained" published

### 1.2 Clean Architecture (Robert C. Martin, 2012)

Uncle Bob's integration of multiple architectural patterns:

> "The overriding rule that makes this architecture work is The Dependency Rule. This rule says that source code dependencies can only point inwards. Nothing in an inner circle can know anything at all about something in an outer circle."
> -- [Robert C. Martin, The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

**Layer Definitions**:

| Layer | Responsibility | Dependencies |
|-------|---------------|--------------|
| **Entities** | Enterprise-wide business rules | None (innermost) |
| **Use Cases** | Application-specific business logic | Entities only |
| **Interface Adapters** | Data format conversion | Use Cases, Entities |
| **Frameworks & Drivers** | External tools (DB, Web) | All inner layers |

### 1.3 Relationship Between Architectures

Clean Architecture integrates multiple approaches:
- Hexagonal Architecture (Ports and Adapters) - Cockburn
- Onion Architecture - Jeffrey Palermo
- DCI (Data, Context, and Interaction)

All share the objective: **separation of concerns through layered design**.

---

## 2. Layer Dependency Rules

### 2.1 The Dependency Rule

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRAMEWORKS & DRIVERS                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              INTERFACE ADAPTERS                          │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │            APPLICATION / USE CASES               │    │    │
│  │  │  ┌─────────────────────────────────────────┐    │    │    │
│  │  │  │              DOMAIN / ENTITIES           │    │    │    │
│  │  │  │                                          │    │    │    │
│  │  │  │    (innermost - NO dependencies)         │    │    │    │
│  │  │  └─────────────────────────────────────────┘    │    │    │
│  │  │                    ↑                             │    │    │
│  │  │       Dependencies point INWARD only            │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  │                        ↑                                  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            ↑                                      │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Jerry Layer Mapping

| Clean Architecture | Jerry Layer | Location | Can Import From |
|--------------------|-------------|----------|-----------------|
| Entities | Domain | `src/domain/` | stdlib only |
| Use Cases | Application | `src/application/` | domain |
| Interface Adapters | Infrastructure | `src/infrastructure/` | domain, application |
| Frameworks & Drivers | Interface | `src/interface/` | all inner layers |

### 2.3 Boundary Crossing Pattern

When control flow moves outward but dependencies must point inward:

```python
# Inner layer defines interface (port)
class IRepository(Protocol):
    def save(self, entity: Entity) -> None: ...

# Outer layer implements interface (adapter)
class FilesystemRepository:
    def save(self, entity: Entity) -> None:
        # Implementation details
        pass

# Use case depends on abstraction, not implementation
class CreateTaskCommandHandler:
    def __init__(self, repository: IRepository) -> None:
        self._repository = repository  # Injected at runtime
```

**Key Principle**: Inner layers call outer-layer implementations through interfaces defined in inner circles.

---

## 3. Port and Adapter Classification

### 3.1 Ports Definition

> "Ports represent purposeful conversations between the application and external entities, analogous to operating system ports where compatible devices can be plugged in."
> -- [Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture/)

### 3.2 Primary vs Secondary Ports

| Aspect | Primary (Driving) | Secondary (Driven) |
|--------|-------------------|-------------------|
| **Direction** | External actor drives application | Application drives external system |
| **Who Initiates** | User, test harness, API client | Application logic |
| **Examples** | CLI, REST API, GUI | Database, Message Queue, Email |
| **Use Case Terminology** | Primary actors | Secondary actors |
| **Jerry Location** | `application/ports/primary/` | `application/ports/secondary/` |

**Visual Representation**:
```
           DRIVING SIDE                    DRIVEN SIDE
           (Primary)                       (Secondary)
              │                                 │
    ┌─────────▼─────────┐           ┌─────────▼─────────┐
    │  Primary Adapters │           │ Secondary Adapters│
    │  (CLI, REST API)  │           │  (DB, MQ, Email)  │
    └─────────┬─────────┘           └─────────┬─────────┘
              │                                 │
    ┌─────────▼─────────┐           ┌─────────▼─────────┐
    │  Primary Ports    │           │ Secondary Ports   │
    │  (IQueryHandler)  │           │  (IRepository)    │
    └─────────┬─────────┘           └─────────┬─────────┘
              │                                 │
              └─────────────┬───────────────────┘
                            │
                  ┌─────────▼─────────┐
                  │  APPLICATION CORE │
                  │  (Business Logic) │
                  └───────────────────┘
```

### 3.3 Adapter Classification

| Type | Direction | Implements | Jerry Location |
|------|-----------|------------|----------------|
| **Driving Adapter** | Inbound | Calls primary ports | `interface/cli/`, `interface/api/` |
| **Driven Adapter** | Outbound | Implements secondary ports | `infrastructure/adapters/` |

### 3.4 Naming Conventions

**Ports (Interfaces)**:
| Type | Pattern | Example |
|------|---------|---------|
| Primary | `I{Verb}Handler` or `I{Verb}Dispatcher` | `IQueryDispatcher`, `ICommandHandler` |
| Secondary | `I{Noun}` or `I{Noun}Port` | `IRepository`, `IEventStore` |

**Adapters (Implementations)**:
| Type | Pattern | Example |
|------|---------|---------|
| Infrastructure | `{Tech}{Entity}Adapter` | `FilesystemProjectAdapter` |
| Interface | `{Type}Adapter` | `CLIAdapter`, `RestApiAdapter` |

---

## 4. Composition Root Pattern

### 4.1 Definition

The **Composition Root** is the single location where all dependency wiring occurs. This is the ONLY place in the application that knows about concrete implementations.

> "Use Dependency Injection container to wire adapters to ports. Configuration should happen at application startup in a composition root."
> -- [Szymon Miks, Hexagonal Architecture in Python](https://blog.szymonmiks.pl/p/hexagonal-architecture-in-python/)

### 4.2 Key Principles

1. **Single Point of Wiring**: All adapter instantiation happens HERE
2. **No Self-Instantiation**: Adapters NEVER create their own dependencies
3. **Constructor Injection**: Dependencies passed via constructors
4. **Runtime Selection**: Implementation selection at startup

### 4.3 Python Pattern

```python
# bootstrap.py - Composition Root

def create_query_dispatcher() -> QueryDispatcher:
    """Factory function that wires all dependencies."""

    # 1. Create infrastructure adapters (driven/secondary)
    repository = FilesystemProjectAdapter()
    environment = OsEnvironmentAdapter()

    # 2. Create handlers with injected dependencies
    handler = RetrieveProjectContextQueryHandler(
        repository=repository,
        environment=environment,
    )

    # 3. Configure dispatcher with handlers
    dispatcher = QueryDispatcher()
    dispatcher.register(RetrieveProjectContextQuery, handler.handle)

    return dispatcher
```

### 4.4 Factory vs Container Approaches

| Approach | Pros | Cons | When to Use |
|----------|------|------|-------------|
| **Factory Functions** | Simple, explicit, no dependencies | Manual wiring | Small to medium apps |
| **DI Container** | Automatic resolution, less boilerplate | Added complexity | Large apps with many dependencies |

Jerry uses **factory functions** for simplicity and explicitness.

---

## 5. Jerry-Specific Implementations

### 5.1 Layer Structure

```
src/
├── domain/                    # Core business logic
│   ├── aggregates/            # Aggregate roots (WorkItem, Task)
│   ├── entities/              # Domain entities
│   ├── value_objects/         # Immutable value objects
│   ├── events/                # Domain events
│   ├── services/              # Domain services
│   └── ports/                 # DOMAIN ports (IRepository)
│
├── application/               # Use cases
│   ├── commands/              # Command definitions
│   ├── queries/               # Query definitions
│   ├── handlers/              # Command/Query handlers
│   │   ├── commands/          # Command handlers
│   │   └── queries/           # Query handlers
│   ├── ports/                 # APPLICATION ports
│   │   ├── primary/           # IQueryDispatcher, ICommandDispatcher
│   │   └── secondary/         # IEventStore, ISnapshotStore
│   ├── dispatchers/           # Dispatcher implementations
│   └── dtos/                  # Data Transfer Objects
│
├── infrastructure/            # Technical adapters
│   ├── adapters/              # Port implementations
│   │   ├── persistence/       # FilesystemProjectAdapter
│   │   ├── messaging/         # InMemoryEventStore
│   │   └── external/          # OsEnvironmentAdapter
│   └── internal/              # Internal utilities
│
├── interface/                 # Primary adapters
│   ├── cli/                   # CLIAdapter
│   │   ├── adapter.py         # Clean Architecture CLI adapter
│   │   └── main.py            # Entry point
│   └── hooks/                 # Git/IDE hooks
│
├── session_management/        # Bounded Context
│   └── infrastructure/        # Context-specific adapters
│
├── shared_kernel/             # Cross-cutting concerns
│   ├── identity/              # VertexId, SnowflakeIdGenerator
│   ├── events/                # DomainEvent base
│   └── domain/                # AggregateRoot base
│
└── bootstrap.py               # COMPOSITION ROOT
```

### 5.2 Key Components

#### Primary Port: IQueryDispatcher

**Location**: `src/application/ports/primary/iquerydispatcher.py`

```python
@runtime_checkable
class IQueryDispatcher(Protocol):
    """Inbound/primary port - query routing contract."""

    def dispatch(self, query: Any) -> Any:
        """Dispatch a query to its registered handler."""
        ...
```

#### Dispatcher Implementation: QueryDispatcher

**Location**: `src/application/dispatchers/query_dispatcher.py`

```python
class QueryDispatcher:
    """Concrete dispatcher that routes queries to handlers."""

    def register(self, query_type: type, handler: Callable) -> None: ...
    def dispatch(self, query: Any) -> Any: ...
```

#### Driving Adapter: CLIAdapter

**Location**: `src/interface/cli/adapter.py`

```python
class CLIAdapter:
    """Clean Architecture CLI Adapter.

    Receives a dispatcher via constructor injection and routes
    all commands through it.

    NO infrastructure imports allowed.
    """

    def __init__(self, dispatcher: IQueryDispatcher) -> None:
        self._dispatcher = dispatcher

    def cmd_init(self, json_output: bool = False) -> int:
        query = RetrieveProjectContextQuery(base_path=self._projects_dir)
        context = self._dispatcher.dispatch(query)
        # Format and display results
```

#### Composition Root: bootstrap.py

**Location**: `src/bootstrap.py`

```python
def create_query_dispatcher() -> QueryDispatcher:
    """Factory function that wires all dependencies.

    This is the ONLY place infrastructure adapters are instantiated.
    """
    # Create infrastructure adapters
    repository = FilesystemProjectAdapter()
    environment = OsEnvironmentAdapter()

    # Create handlers with injected dependencies
    handler = RetrieveProjectContextQueryHandler(
        repository=repository,
        environment=environment,
    )

    # Configure dispatcher
    dispatcher = QueryDispatcher()
    dispatcher.register(RetrieveProjectContextQuery, handler.handle)

    return dispatcher
```

### 5.3 Dependency Rules Enforcement

Jerry enforces layer boundaries via architecture tests:

**Location**: `tests/architecture/test_composition_root.py`

```python
def test_cli_adapter_has_no_infrastructure_imports() -> None:
    """CLIAdapter must not import infrastructure directly."""
    adapter_path = Path("src/interface/cli/adapter.py")
    imports = get_imports_from_file(adapter_path)
    assert not has_infrastructure_import(imports)

def test_bootstrap_imports_infrastructure() -> None:
    """Bootstrap SHOULD import infrastructure adapters."""
    bootstrap_path = Path("src/bootstrap.py")
    imports = get_imports_from_file(bootstrap_path)
    assert has_infrastructure_import(imports)
```

### 5.4 Bounded Contexts

Jerry organizes domain logic into bounded contexts:

| Context | Responsibility | Location |
|---------|---------------|----------|
| `session_management` | Project and session handling | `src/session_management/` |
| `work_tracking` | Task and work item management | `src/work_tracking/` |
| `shared_kernel` | Cross-context shared code | `src/shared_kernel/` |

**Rule**: Never import directly across context boundaries except `shared_kernel`.

---

## 6. Sources and References

### Primary Sources

1. **Alistair Cockburn** (Pattern Author)
   - [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Original article (2005)
   - [Hexagonal Architecture Explained](https://www.amazon.com/Hexagonal-Architecture-Explained-Alistair-Cockburn/dp/173751978X) - Book (2024)

2. **Robert C. Martin** (Clean Architecture)
   - [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) - Blog post (2012)
   - Clean Architecture: A Craftsman's Guide to Software Structure and Design - Book (2017)

### Industry Implementations

3. **Netflix Technology Blog**
   - [Ready for changes with Hexagonal Architecture](https://netflixtechblog.com/ready-for-changes-with-hexagonal-architecture-b315ec967749)
   - Key insight: "Having core logic isolated means you can easily change data source details without a significant impact or major code rewrites."

4. **AWS Prescriptive Guidance**
   - [Hexagonal Architecture Pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html)

5. **Domain-Driven Hexagon** (Comprehensive Guide)
   - [GitHub Repository](https://github.com/sairyss/domain-driven-hexagon)
   - Covers DDD, Hexagonal, Clean, and Onion Architecture with code examples

### Python-Specific Resources

6. **Szymon Miks**
   - [Hexagonal Architecture in Python](https://blog.szymonmiks.pl/p/hexagonal-architecture-in-python/)

7. **Zaur Nasibov**
   - [Hexagonal Architecture and Python Series](https://www.zaurnasibov.com/posts/2021/10/30/hexarch_di_python_part_1.html)

8. **Rost Glukhov**
   - [Python Design Patterns for Clean Architecture](https://www.glukhov.org/post/2025/11/python-design-patterns-for-clean-architecture/)

### Context7 Documentation

9. **Modular Architecture Hexagonal Demo Project**
   - Context7 ID: `/alicanakkus/modular-architecture-hexagonal-demo-project`
   - Java implementation demonstrating port/adapter patterns

10. **Ardalis Clean Architecture Template**
    - Context7 ID: `/ardalis/cleanarchitecture`
    - .NET implementation with Core, UseCases, Infrastructure, Web layers

### Jerry-Specific Documents

11. **Pattern Catalog**
    - `.claude/patterns/PATTERN-CATALOG.md`
    - 31 patterns across 9 categories

12. **Architecture Standards**
    - `.claude/rules/architecture-standards.md`
    - Layer dependencies, port/adapter naming

13. **Design Canon**
    - `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md`
    - Authoritative Jerry design document

---

## Appendix A: Quick Reference Card

### Dependency Matrix

| Layer | stdlib | domain | application | infrastructure | interface |
|-------|--------|--------|-------------|----------------|-----------|
| domain | YES | - | NO | NO | NO |
| application | YES | YES | - | NO | NO |
| infrastructure | YES | YES | YES | - | NO |
| interface | YES | YES | YES | YES | - |

### File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Command | `{verb}_{noun}_command.py` | `create_task_command.py` |
| Query | `retrieve_{noun}_query.py` | `retrieve_project_context_query.py` |
| Command Handler | `{verb}_{noun}_command_handler.py` | `create_task_command_handler.py` |
| Query Handler | `{verb}_{noun}_query_handler.py` | `retrieve_project_context_query_handler.py` |
| Port | `i{noun}.py` | `iquerydispatcher.py` |
| Adapter | `{tech}_{entity}_adapter.py` | `filesystem_project_adapter.py` |

### Port Classification Checklist

- [ ] Primary ports are in `application/ports/primary/`
- [ ] Secondary ports are in `application/ports/secondary/`
- [ ] Driving adapters (CLI, API) are in `interface/`
- [ ] Driven adapters (DB, MQ) are in `infrastructure/adapters/`
- [ ] Composition root is in `bootstrap.py`
- [ ] Architecture tests validate boundaries

---

## Appendix B: Validation Criteria

This research document should be validated against:

1. **Consistency with Jerry Implementation**
   - [ ] Layer structure matches `src/` directory
   - [ ] Port locations match documented patterns
   - [ ] Architecture tests pass

2. **Authority of Sources**
   - [ ] Primary sources cited (Cockburn, Martin)
   - [ ] Industry implementations referenced (Netflix, AWS)
   - [ ] Python-specific patterns included

3. **Completeness**
   - [ ] All four architectural layers covered
   - [ ] Both port types defined
   - [ ] Composition root pattern documented
   - [ ] Jerry-specific implementations detailed

---

**Document Status**: COMPLETE
**Review Required**: Architecture Team
**Next Steps**: Integrate findings into TD-017 implementation tasks
