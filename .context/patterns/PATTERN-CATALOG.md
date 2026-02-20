# Jerry Pattern Catalog

> Comprehensive index of architecture and design patterns used in Jerry.
> Each pattern links to a detailed pattern file for in-depth documentation.

**Last Updated**: 2026-01-12
**Total Patterns**: 49 patterns across 13 categories

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
| [Skill Development](#skill-development-patterns) | 6 | Jerry Skill Structure, Workflow Patterns |
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



---






---

## Event Patterns





---

## CQRS Patterns






---

## Repository Patterns



```
IRepository<TAggregate, TId>          # Domain port (abstract)
    │
    ├── InMemoryRepository            # Testing adapter
    ├── EventSourcedRepository        # Event sourcing adapter
    │       └── uses IEventStore
    └── SnapshottingRepository        # With snapshot optimization
            └── uses ISnapshotStore
```


---






---

## Graph Patterns


---

## Architecture Patterns



```
```



---






---

## Testing Patterns



```
                    ┌─────────────┐
                   ┌┴─────────────┴┐
                  ┌┴───────────────┴┐
                 ┌┴─────────────────┴┐
                ┌┴───────────────────┴┐
                └─────────────────────┘
```

---

## Skill Development Patterns

| ID | Pattern | Status | Detail File |
|----|---------|--------|-------------|
| PAT-SKILL-001 | **Jerry Skill Structure** | MANDATORY | [skill-development/skill-structure.md](skill-development/skill-structure.md) |
| PAT-SKILL-WF-001 | Sequential Orchestration | RECOMMENDED | [skill-development/skill-structure.md](skill-development/skill-structure.md#workflow-patterns) |
| PAT-SKILL-WF-002 | Multi-Source Coordination | RECOMMENDED | [skill-development/skill-structure.md](skill-development/skill-structure.md#workflow-patterns) |
| PAT-SKILL-WF-003 | Iterative Refinement | RECOMMENDED | [skill-development/skill-structure.md](skill-development/skill-structure.md#workflow-patterns) |
| PAT-SKILL-WF-004 | Context-Aware Selection | RECOMMENDED | [skill-development/skill-structure.md](skill-development/skill-structure.md#workflow-patterns) |
| PAT-SKILL-WF-005 | Domain-Specific Intelligence | RECOMMENDED | [skill-development/skill-structure.md](skill-development/skill-structure.md#workflow-patterns) |

**Source:** Anthropic's "Complete Guide to Building Skills for Claude" (January 2026) + Jerry Framework conventions.

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




---

## References


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
├── skill-development/             # Skill development patterns
│   └── skill-structure.md        # PAT-SKILL-001
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
