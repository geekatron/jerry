# Research Artifact: Industry Best Practices for Event Sourcing, CQRS, and Hexagonal Architecture

> **PS ID:** PROJ-001
> **Entry ID:** e-005
> **Date:** 2026-01-09
> **Researcher:** Orchestrator (Context7 + Web Research)
> **Sources:**
> - pyeventsourcing/eventsourcing (Context7)
> - axoniq/reference-guide (Context7)
> - sairyss/domain-driven-hexagon (Context7)
> - Martin Fowler - Event Sourcing (Web)
> - Vaughn Vernon - DDD Aggregate Design (Cached Knowledge)

---

## L0: Executive Summary

Industry research validates the Jerry Framework's architectural choices while providing specific implementation guidance:

1. **Event Sourcing**: Aggregate state derived from replaying events, with `@event` decorator pattern (pyeventsourcing)
2. **CQRS**: Complete command/query separation with Axon Framework's handler model as reference
3. **Hexagonal Architecture**: Ports & Adapters with explicit primary/secondary port distinction
4. **DDD Aggregates**: Small aggregates, reference by ID, eventual consistency (Vaughn Vernon's 4 rules)

**Key Finding**: All three patterns (ES, CQRS, Hexagonal) are complementary and widely adopted together.

---

## L1: Pattern Implementations from Industry

### 1. Event Sourcing (pyeventsourcing)

**Source**: Context7 query of `pyeventsourcing/eventsourcing`

#### Core Pattern: `@event` Decorator

```python
from eventsourcing.domain import Aggregate, event

class Dog(Aggregate):
    @event('Registered')
    def __init__(self, name: str):
        self.name = name
        self.tricks = []

    @event('TrickAdded')
    def add_trick(self, trick: str):
        self.tricks.append(trick)
```

**Key Principles:**
- Aggregate state is ONLY modified within `@event` decorated methods
- Events are immutable facts about what happened
- State rebuilt by replaying events in order
- Aggregate root enforces invariants

#### Event Store Interface

```python
class EventStore:
    def append(self, aggregate_id: UUID, events: List[Event], expected_version: int) -> None:
        """Append events with optimistic concurrency check."""
        pass

    def get(self, aggregate_id: UUID) -> List[Event]:
        """Retrieve all events for aggregate."""
        pass
```

#### Snapshots for Performance

```python
# Snapshot every N events
if aggregate.version % 10 == 0:
    snapshot_store.save(aggregate.id, aggregate.state, aggregate.version)

# Load with snapshot
snapshot = snapshot_store.get(aggregate_id)
events = event_store.get(aggregate_id, from_version=snapshot.version)
aggregate = rebuild(snapshot.state, events)
```

**Implication for Jerry**: Use `@event` pattern for domain aggregates (Task, Phase, Plan). Snapshot every 10 events.

---

### 2. CQRS (Axon Framework Reference Guide)

**Source**: Context7 query of `axoniq/reference-guide`

#### Command Model

```java
@Aggregate
public class GiftCard {
    @AggregateIdentifier
    private String id;

    @CommandHandler
    public GiftCard(IssueCardCommand cmd) {
        apply(new CardIssuedEvent(cmd.getId(), cmd.getAmount()));
    }

    @EventSourcingHandler
    private void on(CardIssuedEvent event) {
        this.id = event.getId();
        this.remainingValue = event.getAmount();
    }
}
```

**Key Principles:**
- `@CommandHandler` - Processes write operations
- `@EventSourcingHandler` - Applies events to aggregate state
- `@QueryHandler` - Handles read operations
- Clear separation: Commands mutate, Queries read

#### Query Model (Projections)

```java
@Component
public class CardSummaryProjection {
    @EventHandler
    public void on(CardIssuedEvent event) {
        // Update read model
        cardSummaryRepository.save(
            new CardSummary(event.getId(), event.getAmount())
        );
    }

    @QueryHandler
    public List<CardSummary> handle(FindAllQuery query) {
        return cardSummaryRepository.findAll();
    }
}
```

**Implication for Jerry**: Implement command handlers that raise events, query handlers that read from projections. Projections are eventually consistent.

---

### 3. Hexagonal Architecture (Domain-Driven Hexagon)

**Source**: Context7 query of `sairyss/domain-driven-hexagon`

#### Layer Structure

```
src/
├── domain/           # Pure business logic, NO external deps
│   ├── aggregates/
│   ├── value-objects/
│   ├── events/
│   └── ports/        # Interfaces (contracts)
├── application/      # Use cases, orchestration
│   ├── commands/
│   ├── queries/
│   └── handlers/
├── infrastructure/   # Adapters implementing ports
│   ├── persistence/
│   ├── messaging/
│   └── external/
└── interface/        # Primary adapters (CLI, API)
    ├── cli/
    └── api/
```

#### Ports & Adapters

```python
# Primary Port (Domain interface for use cases)
class ITaskRepository(ABC):
    @abstractmethod
    def save(self, task: Task) -> None: pass

    @abstractmethod
    def get(self, task_id: TaskId) -> Optional[Task]: pass

# Secondary Adapter (Infrastructure implementation)
class SqliteTaskRepository(ITaskRepository):
    def __init__(self, connection: Connection):
        self._conn = connection

    def save(self, task: Task) -> None:
        # SQLite implementation
        pass
```

**Key Principles:**
- Domain has ZERO external imports (stdlib only)
- Ports define WHAT, Adapters define HOW
- All dependencies point inward
- Infrastructure depends on domain, never vice versa

**Implication for Jerry**: Strict layering. Domain modules cannot import from application, infrastructure, or interface.

---

### 4. DDD Aggregate Design (Vaughn Vernon)

**Source**: Cached knowledge - Implementing Domain-Driven Design

#### The 4 Rules of Aggregate Design

| Rule | Description | Implication |
|------|-------------|-------------|
| **Rule 1** | Model true invariants in consistency boundaries | Aggregates should be small, focused on single consistency concern |
| **Rule 2** | Design small aggregates | Avoid large aggregates; prefer multiple small ones |
| **Rule 3** | Reference other aggregates by ID only | Never hold object references across aggregate boundaries |
| **Rule 4** | Use eventual consistency outside boundaries | Cross-aggregate operations use domain events |

#### Applying to Jerry Domain Model

```python
# GOOD: Small aggregate, ID reference
class Task(AggregateRoot):
    def __init__(self, task_id: TaskId, phase_id: PhaseId):  # ID reference
        self._id = task_id
        self._phase_id = phase_id  # Reference by ID, not object
        self._status = TaskStatus.PENDING

# BAD: Large aggregate holding references
class Phase(AggregateRoot):
    def __init__(self):
        self._tasks: List[Task] = []  # DON'T hold Task objects
```

**Correct Pattern:**
```python
class Phase(AggregateRoot):
    def __init__(self, phase_id: PhaseId, plan_id: PlanId):
        self._id = phase_id
        self._plan_id = plan_id  # Reference parent by ID
        self._task_ids: Set[TaskId] = set()  # Store IDs only

    def add_task(self, task_id: TaskId) -> None:
        self._task_ids.add(task_id)
        self._raise_event(TaskAddedToPhase(self._id, task_id))
```

---

### 5. Martin Fowler on Event Sourcing

**Source**: Web Search - martinfowler.com/eaaDev/EventSourcing.html

#### Core Concept

> "Event Sourcing ensures that all changes to application state are stored as a sequence of events. Not just can we query these events, we can also use the event log to reconstruct past states."

#### Benefits Validated

1. **Complete Audit Log**: Every state change is recorded
2. **Temporal Queries**: Reconstruct state at any point in time
3. **Event Replay**: Rebuild read models by replaying events
4. **Debugging**: "What happened" is explicit, not inferred

#### Challenges to Address

1. **Event Schema Evolution**: Version events, support upcasting
2. **Performance**: Use snapshots for long event streams
3. **Eventual Consistency**: UI must handle projection lag

**Implication for Jerry**: CloudEvents 1.0 envelope provides schema versioning. Snapshot every 10 events. Accept <100ms projection lag.

---

## L2: Strategic Synthesis for Jerry Framework

### Pattern Alignment Matrix

| Jerry Component | Industry Pattern | Implementation |
|-----------------|------------------|----------------|
| Task, Phase, Plan | Aggregate Root | Event-sourced with `@event` pattern |
| TaskId, PhaseId, PlanId | VertexId (Value Object) | Immutable, graph-ready |
| IWorkItemRepository | Port | Domain abstraction, no infrastructure |
| SqliteTaskRepository | Secondary Adapter | Implements port |
| CreateTaskCommand | Command | Returns domain events |
| ListTasksQuery | Query | Reads from projection |
| TaskCreated, TaskCompleted | Domain Event | CloudEvents 1.0 envelope |

### Validated Design Decisions

| Decision | Industry Evidence | Status |
|----------|-------------------|--------|
| Hexagonal Architecture | sairyss/domain-driven-hexagon | Validated |
| Event Sourcing with Snapshots | pyeventsourcing, Martin Fowler | Validated |
| CQRS Separation | Axon Framework | Validated |
| Small Aggregates | Vaughn Vernon | Validated |
| Reference by ID | Vaughn Vernon Rule 3 | Validated |
| CloudEvents 1.0 | CNCF Standard | Validated |
| SQLite for Single-User | Local-first patterns | Validated |
| NetworkX for Graph | In-process graph | Validated |

### Gaps to Address

| Gap | Industry Guidance | Resolution |
|-----|-------------------|------------|
| Event Versioning | Use envelope with version field | CloudEvents type field includes version |
| Projection Rebuild | Store projection version | Track `last_event_position` per projection |
| Concurrency Control | Optimistic with version check | `expected_version` parameter |
| Cross-Aggregate Coordination | Domain events + eventual consistency | Event handlers update related aggregates |

---

## Cross-References

| Reference | Purpose |
|-----------|---------|
| PROJ-001-e-001 | WORKTRACKER_PROPOSAL extraction (primary synthesis) |
| PROJ-001-e-002 | PLAN.md graph model extraction |
| PROJ-001-e-003 | REVISED-ARCHITECTURE foundation |
| PROJ-001-e-004 | Strategic plan v3 extraction |
| ADR-034 | Unified WT-KM implementation decision |

---

## Implementation Checklist

Based on industry research, the following patterns MUST be implemented:

- [ ] `@event` decorator pattern for aggregate mutations
- [ ] `IEventStore` with optimistic concurrency (`expected_version`)
- [ ] `ISnapshotStore` for performance (every 10 events)
- [ ] `IProjection` interface with `last_event_position` tracking
- [ ] Small aggregates with ID references only
- [ ] Domain layer with ZERO external imports
- [ ] CloudEvents 1.0 envelope for all domain events
- [ ] Command handlers returning events (not void)
- [ ] Query handlers reading from projections (not aggregates)

---

*Document generated for PROJ-001 Design Document Synthesis*
*Industry research conducted via Context7 and Web Search*
