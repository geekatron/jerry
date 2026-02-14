# Architecture Standards

> Hexagonal Architecture, CQRS, Event Sourcing, and file organization rules.

<!-- L2-REINJECT: rank=4, tokens=60, content="domain/ MUST NOT import application/, infrastructure/, interface/. Only bootstrap.py instantiates infrastructure. One public class per file." -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rules](#hard-rules) | Architectural constraints H-07 to H-10 |
| [Layer Dependencies](#layer-dependencies) | Import boundary rules |
| [Directory Structure](#directory-structure) | Hexagonal layer layout |
| [Standards (MEDIUM)](#standards-medium) | Naming conventions, patterns |
| [Guidance (SOFT)](#guidance-soft) | Optional best practices |

---

## HARD Rules

> These rules CANNOT be overridden. Violations will be blocked.

| ID | Rule | Consequence |
|----|------|-------------|
| H-07 | `src/domain/` MUST NOT import from `application/`, `infrastructure/`, or `interface/`. Stdlib and `shared_kernel/` only. | Architecture test fails. CI blocks merge. |
| H-08 | `src/application/` MUST NOT import from `infrastructure/` or `interface/`. | Architecture test fails. CI blocks merge. |
| H-09 | Only `src/bootstrap.py` SHALL instantiate infrastructure adapters. | Architecture test fails. |
| H-10 | Each Python file SHALL contain exactly ONE public class or protocol. | AST check fails. |

---

## Layer Dependencies

| Layer | Can Import | MUST NOT Import |
|-------|-----------|-----------------|
| `domain/` | stdlib, `shared_kernel/` | application, infrastructure, interface |
| `application/` | domain | infrastructure, interface |
| `infrastructure/` | domain, application | interface |
| `interface/` | all inner layers | -- |

---

## Directory Structure

```
src/
  domain/           # Aggregates, entities, value objects, events, ports, services
  application/      # Commands, queries, handlers, ports (primary/secondary), DTOs
  infrastructure/   # Adapters (persistence, messaging, external), read models
  interface/        # CLI, API, hooks
  shared_kernel/    # Identity types, base classes, common protocols
  bootstrap.py      # Composition root (H-09)
```

**Project workspace:** `projects/PROJ-{NNN}-{slug}/` with `PLAN.md`, `WORKTRACKER.md`, `.jerry/data/items/`, `work/`, `research/`, `synthesis/`, `decisions/`.

---

## Standards (MEDIUM)

Override requires documented justification.

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Port (primary) | `I{Verb}Handler` | `IQueryHandler` |
| Port (secondary/domain) | `I{Noun}` | `IEventStore`, `IRepository` |
| Adapter (persistence) | `{Tech}{Entity}Adapter` | `FilesystemProjectAdapter` |
| Adapter (messaging) | `{Tech}EventStore` | `InMemoryEventStore` |
| Command class | `{Verb}{Noun}Command` | `CreateWorkItemCommand` |
| Query class | `{Verb}{Noun}Query` | `RetrieveProjectContextQuery` |
| Handler class | `{CommandOrQuery}Handler` | `CreateWorkItemCommandHandler` |
| Event class | `{Noun}{PastVerb}` | `WorkItemCreated` |

### CQRS File Naming

| Type | Pattern | Example |
|------|---------|---------|
| Command | `{verb}_{noun}_command.py` | `create_work_item_command.py` |
| Query | `{verb}_{noun}_query.py` | `retrieve_project_context_query.py` |
| Handler | `{type}_handler.py` | `create_work_item_command_handler.py` |
| Event | `{noun}_events.py` | `work_item_events.py` |

### Query Verb Selection

| Scenario | Verb |
|----------|------|
| Single by ID | `Get` or `Retrieve` |
| Collection | `List` |
| Discovery | `Scan` |
| Validation | `Validate` |

### Pattern Guidance

- Commands SHOULD return `None` or domain events. Queries SHOULD return DTOs, never domain entities.
- Value objects SHOULD use `@dataclass(frozen=True, slots=True)` with validation in `__post_init__`.
- Domain events SHOULD use past tense naming and include `EVENT_TYPE` class variable.
- Aggregates SHOULD implement `apply_event()` and `collect_events()`.
- Repositories SHOULD implement `IRepository` protocol. See `.context/patterns/` for reference.
- Bounded contexts SHOULD communicate via domain events or shared kernel only.
- `__init__.py` SHOULD explicitly export public API via `__all__`.

---

## Guidance (SOFT)

*Optional best practices.*

- *Snapshot optimization MAY be used for aggregates with many events (every 10 events).*
- *Anti-corruption layer MAY be used for external system integration.*
- *Read model projections MAY be stored in `infrastructure/read_models/`.*
