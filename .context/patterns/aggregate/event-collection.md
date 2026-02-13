# PAT-AGG-002: Event Collection Pattern

> **Status**: MANDATORY
> **Category**: Aggregate Pattern
> **Location**: `src/work_tracking/domain/aggregates/base.py`

---

## Overview

The Event Collection pattern manages how aggregates accumulate and publish domain events. Events are collected during aggregate operations and published after successful persistence.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Greg Young** | "Domain events should be raised by aggregates, not by services or handlers" |
| **Vaughn Vernon** | "Collect events during operations, publish after transaction commits" |
| **Udi Dahan** | "Domain events represent something that happened in the past" |

---

## Jerry Implementation

### Core Mechanism

```python
# In AggregateRoot base class
class AggregateRoot(ABC):
    def _initialize(self, id: str, version: int = 0) -> None:
        self._id = id
        self._version = version
        self._pending_events: list[DomainEvent] = []  # Event collection

    def _raise_event(self, event: DomainEvent) -> None:
        """Record a domain event.

        Called by aggregate behavior methods when state changes.
        Events are NOT published here - just collected.
        """
        self._version += 1
        self._apply(event)
        self._pending_events.append(event)

    def collect_events(self) -> Sequence[DomainEvent]:
        """Return and clear pending events.

        Called after successful persistence to get events for publication.
        Clears the internal list to prevent duplicate publication.
        """
        events = list(self._pending_events)
        self._pending_events.clear()
        return events
```

---

## Collection Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                         Aggregate                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    _pending_events                        │   │
│  │                                                           │   │
│  │   1. aggregate.create()     → [Created]                  │   │
│  │   2. aggregate.start()      → [Created, StatusChanged]   │   │
│  │   3. aggregate.complete()   → [Created, StatusChanged,   │   │
│  │                                 Completed]                │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  4. events = aggregate.collect_events()                          │
│     → Returns [Created, StatusChanged, Completed]                │
│     → _pending_events cleared to []                              │
│                                                                   │
│  5. repository.save(aggregate)                                   │
│  6. event_publisher.publish(events)                              │
└──────────────────────────────────────────────────────────────────┘
```

---

## Usage Pattern

### In Application Handler

```python
class CompleteWorkItemCommandHandler:
    """Handler that collects and publishes events."""

    def __init__(
        self,
        repository: IWorkItemRepository,
        event_publisher: IEventPublisher,
    ) -> None:
        self._repository = repository
        self._event_publisher = event_publisher

    def handle(self, command: CompleteWorkItemCommand) -> list[DomainEvent]:
        # 1. Load aggregate
        work_item = self._repository.get_or_raise(command.work_item_id)

        # 2. Execute behavior (events collected internally)
        work_item.complete(quality_passed=command.quality_passed)

        # 3. Collect events BEFORE save
        events = work_item.collect_events()

        # 4. Save aggregate
        self._repository.save(work_item)

        # 5. Publish events AFTER successful save
        self._event_publisher.publish(events)

        # 6. Return events for handler response
        return events
```

### Alternative: Outbox Pattern

```python
class CompleteWorkItemCommandHandler:
    """Handler using outbox for reliable event publishing."""

    def handle(self, command: CompleteWorkItemCommand) -> list[DomainEvent]:
        work_item = self._repository.get_or_raise(command.work_item_id)
        work_item.complete()

        events = work_item.collect_events()

        # Save aggregate AND events atomically
        with self._unit_of_work.begin():
            self._repository.save(work_item)
            self._outbox.store(events)  # Same transaction

        # Outbox processor publishes later
        return events
```

---

## Key Principles

### 1. Events Raised by Aggregate

Events are created inside the aggregate, not by external code:

```python
# CORRECT: Aggregate raises event
class WorkItem(AggregateRoot):
    def start(self) -> None:
        self._status.validate_transition(WorkItemStatus.IN_PROGRESS)
        event = StatusChanged(...)
        self._raise_event(event)

# WRONG: External code creates event
def start_work_item(item: WorkItem) -> None:
    item._status = WorkItemStatus.IN_PROGRESS  # Direct mutation
    event = StatusChanged(...)  # Event created externally
    event_store.append(event)
```

### 2. Collect Before Publish

Events are collected before publishing to ensure consistency:

```python
# CORRECT: Collect, save, then publish
events = aggregate.collect_events()
repository.save(aggregate)
publisher.publish(events)

# WRONG: Publish before save (could fail after publish)
aggregate.complete()
publisher.publish(aggregate.collect_events())  # Published!
repository.save(aggregate)  # Could fail!
```

### 3. Clear After Collection

`collect_events()` clears the list to prevent duplicate publication:

```python
events1 = aggregate.collect_events()  # Returns [A, B, C]
events2 = aggregate.collect_events()  # Returns [] (already collected)
```

---

## Testing Pattern

```python
def test_collect_events_returns_all_pending_events():
    """Collecting returns all events raised during operations."""
    item = WorkItem.create(id="WORK-001", title="Test")
    item.start()
    item.complete()

    events = item.collect_events()

    assert len(events) == 3
    assert isinstance(events[0], WorkItemCreated)
    assert isinstance(events[1], StatusChanged)
    assert isinstance(events[2], WorkItemCompleted)


def test_collect_events_clears_pending_list():
    """After collection, pending list is empty."""
    item = WorkItem.create(id="WORK-001", title="Test")
    item.start()

    first_collection = item.collect_events()
    second_collection = item.collect_events()

    assert len(first_collection) == 2
    assert len(second_collection) == 0


def test_events_accumulate_across_operations():
    """Multiple operations accumulate events."""
    item = WorkItem.create(id="WORK-001", title="Test")

    # First operation
    item.start()
    # Don't collect yet

    # Second operation
    item.set_priority(Priority.HIGH)
    # Still accumulating

    events = item.collect_events()

    assert len(events) == 3  # Created + Started + PriorityChanged
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Events are collected, not immediately published. This allows the handler to control the publish timing and handle failures gracefully.

> **Jerry Decision**: `collect_events()` is called once per save operation. The handler is responsible for event publication.

> **Jerry Decision**: For critical flows, use the outbox pattern to ensure events are eventually published even if the publisher fails.

---

## Anti-Patterns

### 1. Publishing Before Persistence

```python
# WRONG: Events published before save
work_item.complete()
publisher.publish(work_item.collect_events())  # Published!
repository.save(work_item)  # Could fail, events already published!
```

### 2. Multiple Collections

```python
# WRONG: Collecting multiple times loses events
events1 = work_item.collect_events()  # Gets events
events2 = work_item.collect_events()  # Empty!
all_events = events1 + events2  # Missing events from events2
```

### 3. External Event Creation

```python
# WRONG: Events created outside aggregate
work_item._status = WorkItemStatus.DONE
event = WorkItemCompleted(...)  # Created externally
event_store.append(event)  # Bypasses aggregate
```

---

## References

- **Vaughn Vernon**: Implementing DDD (2013), Domain Events
- **Greg Young**: [Domain Events](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)
- **Udi Dahan**: [Domain Events – Salvation](https://udidahan.com/2009/06/14/domain-events-salvation/)
- **Design Canon**: Section 5.5 - Event Collection
- **Related Patterns**: PAT-EVT-002 (DomainEvent), PAT-ENT-003 (AggregateRoot)
