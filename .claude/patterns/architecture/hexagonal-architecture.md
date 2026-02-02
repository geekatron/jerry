# PAT-ARCH-001: Hexagonal Architecture

> **Status**: MANDATORY
> **Category**: Architecture
> **Also Known As**: Ports and Adapters

---

## Intent

Allow an application to equally be driven by users, programs, automated test or batch scripts, and to be developed and tested in isolation from its eventual run-time devices and databases.

---

## Problem

Traditional layered architectures create tight coupling between business logic and infrastructure concerns (databases, UIs, external services), making it difficult to:
- Test business logic in isolation
- Switch infrastructure implementations
- Support multiple entry points (CLI, API, GUI)

---

## Solution

Organize code around a central hexagon (application core) with ports defining capabilities and adapters implementing them.

### Layer Structure

```
src/
├── domain/                    # Core business logic (innermost)
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
│   │   ├── primary/           # Inbound (ICommandHandler, IQueryHandler)
│   │   └── secondary/         # Outbound (IEventStore, INotifier)
│   └── projections/           # Read model projections
│
├── infrastructure/            # Technical adapters (driven side)
│   ├── adapters/              # Port implementations
│   │   ├── persistence/       # Repository adapters
│   │   ├── messaging/         # Event store adapters
│   │   └── external/          # External service adapters
│   ├── read_models/           # Materialized view storage
│   └── internal/              # Internal utilities
│
└── interface/                 # Primary adapters (driving side)
    ├── cli/                   # CLI adapter
    ├── api/                   # HTTP API adapter
    └── hooks/                 # Git/IDE hooks
```

### Visual Representation

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
                           │                   │
                           │   ┌───────────┐   │
                           │   │  DOMAIN   │   │
                           │   └───────────┘   │
                           └───────────────────┘
```

---

## The Dependency Rule

> "Source code dependencies can only point inwards. Nothing in an inner circle can know anything at all about something in an outer circle."
> — Robert C. Martin, Clean Architecture

### Dependency Matrix

| Layer | stdlib | domain | application | infrastructure | interface |
|-------|--------|--------|-------------|----------------|-----------|
| **domain** | YES | - | NO | NO | NO |
| **application** | YES | YES | - | NO | NO |
| **infrastructure** | YES | YES | YES | - | NO |
| **interface** | YES | YES | YES | YES | - |

### Key Principles

1. **Domain has no dependencies** - Pure Python only
2. **Application depends on domain** - Never on infrastructure
3. **Infrastructure implements domain ports** - Adapters fulfill contracts
4. **Interface orchestrates** - Composes all layers

---

## Jerry Implementation

### Layer Locations

| Layer | Location | Dependencies |
|-------|----------|--------------|
| Domain | `src/domain/` | stdlib only |
| Application | `src/application/` | domain |
| Infrastructure | `src/infrastructure/` | domain, application |
| Interface | `src/interface/` | all inner layers |
| Shared Kernel | `src/shared_kernel/` | stdlib only (exception: domain may import) |

### Composition Root

All dependency wiring happens in `src/bootstrap.py`:

```python
# bootstrap.py - The ONLY place infrastructure is instantiated
def create_query_dispatcher() -> QueryDispatcher:
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

---

## Industry Prior Art

### Primary Sources

| Source | Author | Year | Description |
|--------|--------|------|-------------|
| [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) | Alistair Cockburn | 2005 | Original pattern definition |
| [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) | Robert C. Martin | 2012 | Integration of hexagonal with other patterns |
| Clean Architecture (Book) | Robert C. Martin | 2017 | Comprehensive guide |

### Industry Implementations

| Source | Description |
|--------|-------------|
| [Netflix Engineering](https://netflixtechblog.com/ready-for-changes-with-hexagonal-architecture-b315ec967749) | Netflix's adoption of hexagonal architecture |
| [AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html) | AWS patterns for hexagonal |
| [Domain-Driven Hexagon](https://github.com/sairyss/domain-driven-hexagon) | Comprehensive TypeScript guide |

---

## Enforcement

Architecture tests validate layer boundaries:

```python
# tests/architecture/test_layer_boundaries.py
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

## Related Patterns

- [PAT-ARCH-002: Primary/Secondary Ports](./ports-adapters.md)
- [PAT-ARCH-003: Bounded Contexts](./bounded-contexts.md)
- [PAT-ARCH-005: Composition Root](./composition-root.md)
- [PAT-CQRS-004: Dispatcher Pattern](../cqrs/dispatcher-pattern.md)

---

## Jerry Design Canon Reference

Lines 1630-1750 in `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md`

---

*Pattern documented by Claude (Opus 4.5) as part of TD-017*
