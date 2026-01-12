# Jerry Pattern Catalog

> Comprehensive index of architecture and design patterns used in Jerry.
> Each pattern links to a detailed pattern file for in-depth documentation.

**Last Updated**: 2026-01-12
**Total Patterns**: 43 patterns across 12 categories

---

## Quick Navigation

| Category | Count | Key Patterns |
|----------|-------|--------------|
| [Identity](#identity-patterns) | 4 | VertexId, Domain-Specific IDs |
| [Entity](#entity-patterns) | 5 | IAuditable, IVersioned, AggregateRoot |
| [Aggregate](#aggregate-patterns) | 4 | Task, Phase, Plan, Knowledge |
| [Value Object](#value-object-patterns) | 3 | Immutable, Enum, Composite |
| [Event](#event-patterns) | 4 | DomainEvent, CloudEvents, IEventStore |
| [CQRS](#cqrs-patterns) | 4 | Command, Query, Projection, Dispatcher |
| [Repository](#repository-patterns) | 3 | Generic, Event-Sourced, Snapshot |
| [Domain Service](#domain-service-patterns) | 2 | Domain Service, Application Service |
| [Architecture](#architecture-patterns) | 5 | Hexagonal, Ports, BCs, One-Class, Composition |
| [Adapter](#adapter-patterns) | 2 | CLI Adapter, Persistence Adapter |
| [Testing](#testing-patterns) | 3 | Test Pyramid, BDD Cycle, Architecture Tests |
| [Graph](#graph-patterns) | 3 | IGraphStore, Edge Labels |

---

## Identity Patterns

| ID | Pattern | Status | Detail File |
|----|---------|--------|-------------|
| PAT-ID-001 | **VertexId** | MANDATORY | [identity/vertex-id.md](identity/vertex-id.md) |
| PAT-ID-002 | **Domain-Specific IDs** | MANDATORY | [identity/domain-specific-ids.md](identity/domain-specific-ids.md) |
| PAT-ID-003 | **JerryUri** | RECOMMENDED | [identity/jerry-uri.md](identity/jerry-uri.md) |
| PAT-ID-004 | **EdgeId** | RECOMMENDED | [identity/edge-id.md](identity/edge-id.md) |

**Location**: `src/shared_kernel/identity/`

---

## Entity Patterns

| ID | Pattern | Status | Detail File |
|----|---------|--------|-------------|
| PAT-ENT-001 | **IAuditable** | MANDATORY | [entity/auditable-protocol.md](entity/auditable-protocol.md) |
| PAT-ENT-002 | **IVersioned** | MANDATORY | [entity/versioned-protocol.md](entity/versioned-protocol.md) |
| PAT-ENT-003 | **AggregateRoot** | MANDATORY | [entity/aggregate-root.md](entity/aggregate-root.md) |
| PAT-ENT-004 | Vertex | RECOMMENDED | Base for entities in graph relationships |
| PAT-ENT-005 | Edge | RECOMMENDED | Graph relationship between vertices |

**Location**: `src/shared_kernel/domain/`

---

## Aggregate Patterns

| ID | Pattern | Status | Detail File |
|----|---------|--------|-------------|
| PAT-AGG-001 | **Task Aggregate** | MANDATORY | [aggregate/task-aggregate.md](aggregate/task-aggregate.md) |
| PAT-AGG-002 | **Phase Aggregate** | RECOMMENDED | [aggregate/phase-aggregate.md](aggregate/phase-aggregate.md) |
| PAT-AGG-003 | **Plan Aggregate** | RECOMMENDED | [aggregate/plan-aggregate.md](aggregate/plan-aggregate.md) |
| PAT-AGG-004 | **Knowledge Aggregate** | RECOMMENDED | [aggregate/knowledge-aggregate.md](aggregate/knowledge-aggregate.md) |

**Location**: `src/domain/aggregates/`

---

## Value Object Patterns

| ID | Pattern | Status | Detail File |
|----|---------|--------|-------------|
| PAT-VO-001 | **Immutable Value Object** | MANDATORY | [value-object/immutable-value-object.md](value-object/immutable-value-object.md) |
| PAT-VO-002 | **Enum Value Object** | MANDATORY | [value-object/enum-value-object.md](value-object/enum-value-object.md) |
| PAT-VO-003 | **Composite Value Object** | RECOMMENDED | [value-object/composite-value-object.md](value-object/composite-value-object.md) |

### Value Object Principles

- **Immutability**: All VOs use `@dataclass(frozen=True, slots=True)`
- **Equality by Value**: Two VOs with same data are equal
- **Self-Validating**: Validation in `__post_init__`
- **No Identity**: VOs have no lifecycle, only values

**Location**: `src/domain/value_objects/`, `src/{bc}/domain/value_objects/`

---

## Event Patterns

| ID | Pattern | Status | Detail File |
|----|---------|--------|-------------|
| PAT-EVT-001 | **DomainEvent** | MANDATORY | [event/domain-event.md](event/domain-event.md) |
| PAT-EVT-002 | **CloudEvents** | MANDATORY | [event/cloud-events.md](event/cloud-events.md) |
| PAT-EVT-003 | **WorkItem Events** | MANDATORY | [event/work-item-events.md](event/work-item-events.md) |
| PAT-EVT-004 | **IEventStore** | MANDATORY | [event/event-store.md](event/event-store.md) |

### Event Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| Domain Event | `{Noun}{PastVerb}` | `TaskCreated`, `WorkItemCompleted` |
| Integration Event | `jerry.{bc}.{aggregate}.{verb}` | `jerry.work_tracking.work_item.completed` |

**Location**: `src/shared_kernel/events/`, `src/application/ports/secondary/`

---

## CQRS Patterns

| ID | Pattern | Status | Detail File |
|----|---------|--------|-------------|
| PAT-CQRS-001 | **Command Pattern** | MANDATORY | [cqrs/command-pattern.md](cqrs/command-pattern.md) |
| PAT-CQRS-002 | **Query Pattern** | MANDATORY | [cqrs/query-pattern.md](cqrs/query-pattern.md) |
| PAT-CQRS-003 | **Projection Pattern** | RECOMMENDED | [cqrs/projection-pattern.md](cqrs/projection-pattern.md) |
| PAT-CQRS-004 | **Dispatcher Pattern** | MANDATORY | [cqrs/dispatcher-pattern.md](cqrs/dispatcher-pattern.md) |

### CQRS Naming Conventions

| Element | Pattern | File Pattern | Example |
|---------|---------|--------------|---------|
| Command | `{Verb}{Noun}Command` | `{verb}_{noun}_command.py` | `CreateTaskCommand` |
| Query | `{Verb}{Noun}Query` | `{verb}_{noun}_query.py` | `RetrieveProjectQuery` |
| Event | `{Noun}{PastVerb}` | `{noun}_events.py` | `TaskCreated` |
| Handler | `{Name}Handler` | `{name}_handler.py` | `CreateTaskCommandHandler` |

### Query Verb Guidelines

| Scenario | Verb | Example |
|----------|------|---------|
| Single by ID | `Get` or `Retrieve` | `RetrieveProjectContextQuery` |
| Collection | `List` | `ListTasksQuery` |
| Discovery | `Scan` | `ScanProjectsQuery` |
| Validation | `Validate` | `ValidateProjectQuery` |
| Search | `Find` or `Search` | `FindTasksByStatusQuery` |

---

## Repository Patterns

| ID | Pattern | Status | Detail File |
|----|---------|--------|-------------|
| PAT-REPO-001 | **Generic Repository** | MANDATORY | [repository/generic-repository.md](repository/generic-repository.md) |
| PAT-REPO-002 | **Event-Sourced Repository** | MANDATORY | [repository/event-sourced-repository.md](repository/event-sourced-repository.md) |
| PAT-REPO-003 | **Snapshot Store** | RECOMMENDED | [repository/snapshot-store.md](repository/snapshot-store.md) |

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

**Location**: `src/domain/ports/`, `src/application/ports/secondary/`

---

## Domain Service Patterns

| ID | Pattern | Status | Detail File |
|----|---------|--------|-------------|
| PAT-SVC-001 | **Domain Service** | MANDATORY | [domain-service/domain-service.md](domain-service/domain-service.md) |
| PAT-SVC-002 | **Application Service** | MANDATORY | [domain-service/application-service.md](domain-service/application-service.md) |

### Service Classification

| Type | Layer | Characteristics |
|------|-------|-----------------|
| Domain Service | `domain/services/` | Pure domain logic, no I/O, stateless |
| Application Service | `application/handlers/` | Orchestrates use cases, uses ports |
| Infrastructure Service | `infrastructure/internal/` | Technical concerns, external I/O |

**Location**: `src/domain/services/`, `src/application/handlers/`

---

## Graph Patterns

| ID | Pattern | Status | Description |
|----|---------|--------|-------------|
| PAT-GRAPH-001 | IGraphStore | RECOMMENDED | Port for graph persistence |
| PAT-GRAPH-002 | Edge Labels | RECOMMENDED | Standardized relationship types |
| PAT-GRAPH-003 | Gremlin Compatibility | RECOMMENDED | Traversal query compatibility |

---

## Architecture Patterns

| ID | Pattern | Status | Detail File |
|----|---------|--------|-------------|
| PAT-ARCH-001 | **Hexagonal Architecture** | MANDATORY | [architecture/hexagonal-architecture.md](architecture/hexagonal-architecture.md) |
| PAT-ARCH-002 | **Ports and Adapters** | MANDATORY | [architecture/ports-adapters.md](architecture/ports-adapters.md) |
| PAT-ARCH-003 | **Bounded Contexts** | MANDATORY | [architecture/bounded-contexts.md](architecture/bounded-contexts.md) |
| PAT-ARCH-004 | **One-Class-Per-File** | MANDATORY | [architecture/one-class-per-file.md](architecture/one-class-per-file.md) |
| PAT-ARCH-005 | **Composition Root** | MANDATORY | [architecture/composition-root.md](architecture/composition-root.md) |

### Layer Dependency Rules

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRAMEWORKS & DRIVERS                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              INTERFACE ADAPTERS                          │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │            APPLICATION / USE CASES               │    │    │
│  │  │  ┌─────────────────────────────────────────┐    │    │    │
│  │  │  │              DOMAIN / ENTITIES           │    │    │    │
│  │  │  │        (innermost - NO dependencies)     │    │    │    │
│  │  │  └─────────────────────────────────────────┘    │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
           Dependencies point INWARD only
```

### Bounded Contexts in Jerry

| Context | Package | Description |
|---------|---------|-------------|
| Session Management | `session_management/` | Project and session handling |
| Work Tracking | `work_tracking/` | Task and work item management |
| Shared Kernel | `shared_kernel/` | Cross-context shared code |
| Problem Solving | `problem_solving/` | (Future) ps-* agent orchestration |

---

## Adapter Patterns

| ID | Pattern | Status | Detail File |
|----|---------|--------|-------------|
| PAT-ADP-001 | **CLI Adapter** | MANDATORY | [adapter/cli-adapter.md](adapter/cli-adapter.md) |
| PAT-ADP-002 | **Persistence Adapter** | MANDATORY | [adapter/persistence-adapter.md](adapter/persistence-adapter.md) |

### Adapter Classification

| Type | Layer | Port Direction | Example |
|------|-------|----------------|---------|
| Primary (Driving) | `interface/` | Inbound | CLI, API, Hooks |
| Secondary (Driven) | `infrastructure/adapters/` | Outbound | Repository, EventStore |

**Location**: `src/interface/`, `src/infrastructure/adapters/`

---

## Testing Patterns

| ID | Pattern | Status | Detail File |
|----|---------|--------|-------------|
| PAT-TEST-001 | **Test Pyramid** | MANDATORY | [testing/test-pyramid.md](testing/test-pyramid.md) |
| PAT-TEST-002 | **BDD Cycle** | MANDATORY | [testing/bdd-cycle.md](testing/bdd-cycle.md) |
| PAT-TEST-003 | **Architecture Tests** | MANDATORY | [testing/architecture-tests.md](testing/architecture-tests.md) |

### Test Pyramid Distribution

```
                    ┌─────────────┐
                    │    E2E      │ ← 5%
                   ┌┴─────────────┴┐
                   │    System     │ ← 10%
                  ┌┴───────────────┴┐
                  │   Integration   │ ← 15%
                 ┌┴─────────────────┴┐
                 │       Unit        │ ← 60%
                ┌┴───────────────────┴┐
                │ Contract+Architecture│ ← 10%
                └─────────────────────┘
```

---

## Lessons Learned

| ID | Lesson | Priority |
|----|--------|----------|
| LES-001 | Event Schemas Are Forever | HIGH |
| LES-002 | Layer Violations Compound | HIGH |
| LES-003 | Retry is Not Optional | HIGH |
| LES-004 | Test at Boundaries First | MEDIUM |
| LES-005 | Document Decisions Immediately | MEDIUM |

---

## Jerry Opinions

These are Jerry-specific architectural decisions that may differ from generic patterns:

| Opinion | Description | Rationale |
|---------|-------------|-----------|
| **One-Class-Per-File** | Deviate from Python's "one idea per file" | LLM navigation optimization |
| **Factory over DI Container** | Use factory functions, not DI frameworks | Simplicity for framework size |
| **DomainEvent over CloudEvents** | Internal events stay as DomainEvent | CloudEvents only for external |
| **BC Names** | `session_management` not "Identity & Access" | Better describes implementation scope |

---

## References

### Jerry Sources

| Document | Location |
|----------|----------|
| Design Canon | `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md` |
| TD-017 Synthesis | `projects/PROJ-001-plugin-cleanup/synthesis/td-017-s-001-design-canon-synthesis.md` |
| Architecture Teaching Edition | `docs/knowledge/exemplars/architecture/work_tracker_architecture_hexagonal_ddd_cqrs_layered_teaching_edition.md` |

### Industry References

| Source | URL |
|--------|-----|
| Hexagonal Architecture | [Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture/) |
| Clean Architecture | [Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) |
| CQRS | [Martin Fowler](https://martinfowler.com/bliki/CQRS.html) |
| Event Sourcing | [Martin Fowler](https://martinfowler.com/eaaDev/EventSourcing.html) |
| MediatR | [Jimmy Bogard](https://github.com/jbogard/mediatr) |
| Domain-Driven Hexagon | [Sairyss](https://github.com/sairyss/domain-driven-hexagon) |

### Enforcement Tools

| Tool | Purpose |
|------|---------|
| [pytest-archon](https://github.com/jwbargsten/pytest-archon) | Architecture boundary testing |
| [PyTestArch](https://pypi.org/project/PyTestArch/) | ArchUnit-inspired Python testing |

---

## Pattern File Structure

```
.claude/patterns/
├── PATTERN-CATALOG.md              # This index file
│
├── adapter/                        # Adapter patterns
│   ├── cli-adapter.md             # PAT-ADP-001
│   └── persistence-adapter.md     # PAT-ADP-002
│
├── aggregate/                      # Aggregate patterns
│   ├── task-aggregate.md          # PAT-AGG-001
│   ├── phase-aggregate.md         # PAT-AGG-002
│   ├── plan-aggregate.md          # PAT-AGG-003
│   └── knowledge-aggregate.md     # PAT-AGG-004
│
├── architecture/                   # Architecture patterns
│   ├── hexagonal-architecture.md  # PAT-ARCH-001
│   ├── ports-adapters.md          # PAT-ARCH-002
│   ├── bounded-contexts.md        # PAT-ARCH-003
│   ├── one-class-per-file.md      # PAT-ARCH-004
│   └── composition-root.md        # PAT-ARCH-005
│
├── cqrs/                           # CQRS patterns
│   ├── command-pattern.md         # PAT-CQRS-001
│   ├── query-pattern.md           # PAT-CQRS-002
│   ├── projection-pattern.md      # PAT-CQRS-003
│   └── dispatcher-pattern.md      # PAT-CQRS-004
│
├── domain-service/                 # Service patterns
│   ├── domain-service.md          # PAT-SVC-001
│   └── application-service.md     # PAT-SVC-002
│
├── entity/                         # Entity patterns
│   ├── auditable-protocol.md      # PAT-ENT-001
│   ├── versioned-protocol.md      # PAT-ENT-002
│   └── aggregate-root.md          # PAT-ENT-003
│
├── event/                          # Event patterns
│   ├── domain-event.md            # PAT-EVT-001
│   ├── cloud-events.md            # PAT-EVT-002
│   ├── work-item-events.md        # PAT-EVT-003
│   └── event-store.md             # PAT-EVT-004
│
├── identity/                       # Identity patterns
│   ├── vertex-id.md               # PAT-ID-001
│   ├── domain-specific-ids.md     # PAT-ID-002
│   ├── jerry-uri.md               # PAT-ID-003
│   └── edge-id.md                 # PAT-ID-004
│
├── repository/                     # Repository patterns
│   ├── generic-repository.md      # PAT-REPO-001
│   ├── event-sourced-repository.md # PAT-REPO-002
│   └── snapshot-store.md          # PAT-REPO-003
│
├── testing/                        # Testing patterns
│   ├── test-pyramid.md            # PAT-TEST-001
│   ├── bdd-cycle.md               # PAT-TEST-002
│   └── architecture-tests.md      # PAT-TEST-003
│
└── value-object/                   # Value object patterns
    ├── immutable-value-object.md  # PAT-VO-001
    ├── enum-value-object.md       # PAT-VO-002
    └── composite-value-object.md  # PAT-VO-003
```

---

*Catalog maintained by Claude (Opus 4.5) as part of TD-017*
