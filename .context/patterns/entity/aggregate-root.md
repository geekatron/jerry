# PAT-ENT-003: Aggregate Root Pattern

> **Status**: MANDATORY
> **Category**: Entity Pattern
> **Location**: `src/work_tracking/domain/aggregates/base.py`

---

## Overview

The Aggregate Root pattern defines a cluster of domain objects that are treated as a single unit for data changes. The aggregate root is the only member of the aggregate that outside objects can reference.

In Jerry, aggregates are event-sourced, meaning their state is derived from a sequence of domain events.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Eric Evans** (DDD, 2003) | "Cluster the entities and value objects into aggregates and define boundaries around each" |
| **Vaughn Vernon** (Implementing DDD, 2013) | "Aggregates should be designed small - prefer referencing by ID over object reference" |
| **Greg Young** (Event Sourcing) | "An aggregate is a consistency boundary where events are applied atomically" |
| **Robert C. Martin** (Clean Architecture) | "Entities encapsulate enterprise-wide business rules" |

---

## Jerry Implementation

### Base Class

```python
# File: src/work_tracking/domain/aggregates/base.py
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from src.shared_kernel.domain_event import DomainEvent

@dataclass
class AggregateRoot(ABC):
    """Event-sourced aggregate base class.

    Lifecycle:
        1. Create via factory method (e.g., Task.create())
        2. Mutate via behavior methods (e.g., task.complete())
        3. Collect events via collect_events()
        4. Persist via repository.save(aggregate)
        5. Reconstitute via AggregateRoot.load_from_history(events)

    References:
        - PAT-EVT-002: DomainEvent base class
        - PAT-REPO-001: Generic Repository pattern
        - Design Canon: 5.4 Aggregate Root Pattern
    """

    def _initialize(self, id: str, version: int = 0) -> None:
        """Initialize aggregate state."""
        self._id = id
        self._version = version
        self._pending_events: list[DomainEvent] = []
        self._created_on: datetime | None = None
        self._modified_on: datetime | None = None

    @property
    def id(self) -> str:
        """Aggregate identity."""
        return self._id

    @property
    def version(self) -> int:
        """Current version for optimistic concurrency."""
        return self._version

    def _raise_event(self, event: DomainEvent) -> None:
        """Record a new domain event.

        This method:
        1. Increments version
        2. Applies event to update state
        3. Appends to pending events list
        4. Updates modification timestamp
        """
        self._version += 1
        self._apply(event)
        self._pending_events.append(event)
        self._modified_on = event.timestamp

    @abstractmethod
    def _apply(self, event: DomainEvent) -> None:
        """Apply event to update aggregate state.

        MUST be deterministic and side-effect free.
        This method is called during:
        - Event recording (_raise_event)
        - History replay (load_from_history)
        """
        ...

    def collect_events(self) -> Sequence[DomainEvent]:
        """Return and clear pending events.

        Call after repository.save() to get events for publication.
        """
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    @classmethod
    def load_from_history(cls, events: Sequence[DomainEvent]) -> AggregateRoot:
        """Reconstruct aggregate from event stream.

        Used by repository to rehydrate aggregate from event store.
        """
        if not events:
            raise ValueError("Cannot load from empty event stream")

        # Create instance without triggering factory
        instance = cls.__new__(cls)
        instance._initialize(
            id=events[0].aggregate_id,
            version=0,
        )

        # Replay all events
        for event in events:
            instance._version += 1
            instance._apply(event)
            if instance._created_on is None:
                instance._created_on = event.timestamp
            instance._modified_on = event.timestamp

        return instance
```

---

## Usage Example

```python
# File: src/work_tracking/domain/aggregates/work_item.py
from src.work_tracking.domain.aggregates.base import AggregateRoot
from src.work_tracking.domain.events.work_item_events import (
    WorkItemCreated,
    StatusChanged,
)
from src.work_tracking.domain.value_objects.work_item_status import WorkItemStatus

class WorkItem(AggregateRoot):
    """Work item aggregate root.

    Invariants:
    - Title cannot be empty
    - Status transitions must follow state machine
    - Completed items cannot be modified
    """

    @classmethod
    def create(
        cls,
        id: str,
        title: str,
        work_type: str = "task",
        priority: str = "medium",
    ) -> WorkItem:
        """Factory method to create new work item."""
        if not title.strip():
            raise ValueError("Title cannot be empty")

        item = cls.__new__(cls)
        item._initialize(id=id)

        # Raise creation event
        event = WorkItemCreated(
            aggregate_id=id,
            aggregate_type="WorkItem",
            title=title,
            work_type=work_type,
            priority=priority,
        )
        item._raise_event(event)

        return item

    def start(self) -> None:
        """Transition to in_progress status."""
        self._status.validate_transition(WorkItemStatus.IN_PROGRESS)

        event = StatusChanged(
            aggregate_id=self._id,
            aggregate_type="WorkItem",
            old_status=self._status.value,
            new_status=WorkItemStatus.IN_PROGRESS.value,
        )
        self._raise_event(event)

    def _apply(self, event: DomainEvent) -> None:
        """Apply event to update state."""
        match event:
            case WorkItemCreated():
                self._title = event.title
                self._work_type = event.work_type
                self._priority = event.priority
                self._status = WorkItemStatus.PENDING
            case StatusChanged():
                self._status = WorkItemStatus(event.new_status)
```

---

## Key Principles

### 1. Consistency Boundary

Aggregates define transaction boundaries. All changes within an aggregate are atomic.

```python
# CORRECT: Single aggregate, single transaction
work_item.start()
work_item.add_subtask("Research")
events = work_item.collect_events()  # All events committed together
repository.save(work_item)
```

### 2. Reference by ID

Aggregates should reference other aggregates by ID, not by object reference.

```python
# CORRECT: Reference by ID
class WorkItem:
    _parent_id: str | None  # ID reference

# WRONG: Object reference
class WorkItem:
    _parent: WorkItem  # Direct object reference
```

### 3. Small Aggregates

Design aggregates to be as small as possible while maintaining invariants.

> **Jerry Decision**: WorkItem is the primary aggregate. Phase and Plan are separate aggregates referenced by ID, not nested within WorkItem.

### 4. Invariant Enforcement

Aggregates enforce their own invariants. External code cannot put an aggregate into an invalid state.

```python
def complete(self) -> None:
    """Complete the work item."""
    # Enforce invariant: must be in_progress
    if self._status != WorkItemStatus.IN_PROGRESS:
        raise InvalidStateError(
            f"Cannot complete work item in {self._status} state"
        )

    # Raise event (invariant is satisfied)
    event = WorkItemCompleted(...)
    self._raise_event(event)
```

---

## Event Sourcing Integration

### Event Replay

Aggregates can be reconstituted from their event history:

```python
# In repository adapter
def get(self, id: WorkItemId) -> WorkItem | None:
    events = self._event_store.read(stream_id=str(id))
    if not events:
        return None

    # Reconstitute from history
    return WorkItem.load_from_history(events)
```

### Snapshot Optimization

For aggregates with many events, snapshots improve load time:

```python
# Every 10 events, take a snapshot (per Design Canon)
SNAPSHOT_FREQUENCY = 10

def save(self, aggregate: WorkItem) -> None:
    events = aggregate.collect_events()
    self._event_store.append(
        stream_id=str(aggregate.id),
        events=events,
        expected_version=aggregate.version - len(events),
    )

    # Take snapshot if needed
    if aggregate.version % SNAPSHOT_FREQUENCY == 0:
        self._snapshot_store.save(aggregate)
```

> **Jerry Decision**: Snapshot every 10 events. This balances storage cost with replay performance.

---

## Testing Pattern

```python
def test_work_item_transitions_when_started_then_status_is_in_progress():
    """Aggregate enforces valid state transitions."""
    # Arrange
    item = WorkItem.create(id="WORK-001", title="Test Task")

    # Act
    item.start()

    # Assert
    assert item._status == WorkItemStatus.IN_PROGRESS
    events = item.collect_events()
    assert len(events) == 2  # Created + StatusChanged
    assert isinstance(events[1], StatusChanged)


def test_work_item_rejects_invalid_transition():
    """Aggregate rejects invalid state transitions."""
    item = WorkItem.create(id="WORK-001", title="Test Task")
    # Item is PENDING, cannot complete directly

    with pytest.raises(InvalidStateError):
        item.complete()
```

---

## Anti-Patterns

### 1. Anemic Aggregate

```python
# WRONG: No business logic in aggregate
class WorkItem:
    def set_status(self, status: str) -> None:
        self._status = status  # No validation!

# CORRECT: Business logic encapsulated
class WorkItem:
    def complete(self) -> None:
        self._status.validate_transition(WorkItemStatus.DONE)
        self._raise_event(WorkItemCompleted(...))
```

### 2. God Aggregate

```python
# WRONG: Aggregate too large
class Project:
    tasks: list[Task]
    phases: list[Phase]
    team_members: list[User]
    documents: list[Document]
    comments: list[Comment]
    # Too many things!

# CORRECT: Separate aggregates
class Project:
    _id: ProjectId
    _phase_ids: list[PhaseId]  # Reference by ID
```

### 3. Leaky Invariants

```python
# WRONG: Invariant checked outside aggregate
if work_item._status == "pending":
    work_item.start()  # Caller checks invariant

# CORRECT: Aggregate enforces internally
work_item.start()  # Aggregate validates internally
```

---

## References

- **Eric Evans**: Domain-Driven Design (2003), Chapter 6
- **Vaughn Vernon**: Implementing Domain-Driven Design (2013), Chapter 10
- **Greg Young**: [CQRS and Event Sourcing](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)
- **Design Canon**: Section 5.4 - Aggregate Root Pattern
- **Related Patterns**: PAT-EVT-002 (DomainEvent), PAT-REPO-001 (Repository)
