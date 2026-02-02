# PAT-REPO-002: Event-Sourced Repository Pattern

> **Status**: MANDATORY
> **Category**: Repository Pattern
> **Location**: `src/work_tracking/infrastructure/persistence/`

---

## Overview

Event-Sourced Repositories persist aggregates by storing their domain events rather than current state. Aggregates are reconstituted by replaying the event history.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Greg Young** | "Event sourcing means storing facts, not state" |
| **Vaughn Vernon** | "Event-sourced repositories append events, never update" |
| **Martin Fowler** | "Event Sourcing ensures every change is captured in an event" |

---

## Jerry Implementation

### Repository Implementation

```python
# File: src/work_tracking/infrastructure/persistence/event_sourced_work_item_repository.py
from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

from src.shared_kernel.exceptions import AggregateNotFoundError, ConcurrencyError
from src.work_tracking.domain.aggregates.work_item import WorkItem
from src.work_tracking.domain.events.event_registry import EventRegistry
from src.work_tracking.domain.ports.event_store import (
    ConcurrencyError as EventStoreConcurrencyError,
    IEventStore,
    StoredEvent,
)
from src.work_tracking.domain.value_objects.work_item_id import WorkItemId
from src.work_tracking.domain.value_objects.work_item_status import WorkItemStatus

if TYPE_CHECKING:
    from src.shared_kernel.domain_event import DomainEvent


class EventSourcedWorkItemRepository:
    """Event-sourced repository for WorkItem aggregate.

    Persists aggregates by appending domain events to event streams.
    Reconstitutes aggregates by replaying event history.

    References:
        - PAT-REPO-001: Generic Repository interface
        - PAT-EVT-004: Event Store pattern
        - PAT-AGG-003: History Replay pattern
    """

    STREAM_PREFIX = "WorkItem"

    def __init__(self, event_store: IEventStore) -> None:
        """Initialize with event store dependency.

        Args:
            event_store: Event persistence adapter
        """
        self._event_store = event_store

    def get(self, id: WorkItemId) -> WorkItem | None:
        """Load aggregate from event history.

        Reads all events from the stream and replays them
        to reconstruct current aggregate state.

        Args:
            id: Work item identifier

        Returns:
            Reconstituted aggregate or None if not found
        """
        stream_id = self._stream_id(id)
        stored_events = self._event_store.read(stream_id)

        if not stored_events:
            return None

        domain_events = [
            self._to_domain_event(stored)
            for stored in stored_events
        ]

        return WorkItem.load_from_history(domain_events)

    def get_or_raise(self, id: WorkItemId) -> WorkItem:
        """Load aggregate or raise if not found.

        Args:
            id: Work item identifier

        Returns:
            Reconstituted aggregate

        Raises:
            AggregateNotFoundError: If aggregate doesn't exist
        """
        work_item = self.get(id)
        if work_item is None:
            raise AggregateNotFoundError(
                entity_type="WorkItem",
                entity_id=id.value,
            )
        return work_item

    def save(self, aggregate: WorkItem) -> None:
        """Persist aggregate by appending new events.

        Only new events (collected since last save) are appended.
        Uses optimistic concurrency via expected version.

        Args:
            aggregate: Work item to persist

        Raises:
            ConcurrencyError: If version conflict detected
        """
        stream_id = self._stream_id(WorkItemId(aggregate.id))
        domain_events = aggregate.collect_events()

        if not domain_events:
            return  # No changes to persist

        # Convert to stored events
        stored_events = [
            self._to_stored_event(event, stream_id)
            for event in domain_events
        ]

        # Calculate expected version (version before these events)
        expected_version = aggregate.version - len(domain_events)

        try:
            self._event_store.append(stream_id, stored_events, expected_version)
        except EventStoreConcurrencyError as e:
            raise ConcurrencyError(
                entity_type="WorkItem",
                entity_id=aggregate.id,
                expected_version=expected_version,
                actual_version=e.actual_version,
            ) from e

    def delete(self, id: WorkItemId) -> bool:
        """Delete aggregate by removing its event stream.

        In production, this should be a soft delete (tombstone event).

        Args:
            id: Work item identifier

        Returns:
            True if deleted, False if not found
        """
        stream_id = self._stream_id(id)
        return self._event_store.delete_stream(stream_id)

    def exists(self, id: WorkItemId) -> bool:
        """Check if aggregate exists.

        Args:
            id: Work item identifier

        Returns:
            True if stream exists
        """
        stream_id = self._stream_id(id)
        return self._event_store.stream_exists(stream_id)

    # Domain-specific queries

    def find_by_status(self, status: WorkItemStatus) -> Sequence[WorkItem]:
        """Find all work items with given status.

        Note: This is inefficient for event-sourced repos.
        Consider using a read model/projection for this query.

        Args:
            status: Status to filter by

        Returns:
            List of matching work items
        """
        # Implementation would scan all streams
        # In practice, use a projection for this
        raise NotImplementedError(
            "Use WorkItemListProjection for status-based queries"
        )

    def find_by_parent(self, parent_id: WorkItemId) -> Sequence[WorkItem]:
        """Find all children of a work item.

        Args:
            parent_id: Parent work item ID

        Returns:
            List of child work items
        """
        # Implementation would scan all streams
        # In practice, use a projection for this
        raise NotImplementedError(
            "Use WorkItemHierarchyProjection for parent-based queries"
        )

    # Internal helpers

    def _stream_id(self, id: WorkItemId) -> str:
        """Generate stream ID from work item ID.

        Format: {StreamPrefix}-{AggregateId}
        Example: WorkItem-WORK-001
        """
        return f"{self.STREAM_PREFIX}-{id.value}"

    def _to_stored_event(
        self,
        event: DomainEvent,
        stream_id: str,
    ) -> StoredEvent:
        """Convert domain event to stored event format."""
        return StoredEvent(
            stream_id=stream_id,
            version=0,  # Event store assigns actual version
            event_type=type(event).__name__,
            data=event.to_dict(),
            timestamp=event.timestamp,
        )

    def _to_domain_event(self, stored: StoredEvent) -> DomainEvent:
        """Convert stored event to domain event."""
        return EventRegistry.deserialize(stored.data)
```

---

## Save Flow

```
    WorkItem                    Repository                     Event Store
        │                           │                              │
        │ collect_events()          │                              │
        │──────────►                │                              │
        │ [Event1, Event2]          │                              │
        │                           │                              │
        │ save(work_item)           │                              │
        │────────────────────────►  │                              │
        │                           │ to_stored_event()            │
        │                           │─────────►                    │
        │                           │                              │
        │                           │ append(stream_id, events,    │
        │                           │        expected_version)     │
        │                           │─────────────────────────────►│
        │                           │                              │
        │                           │              OK / ConcurrencyError
        │                           │◄─────────────────────────────│
        │                           │                              │
        │ success/error             │                              │
        │◄────────────────────────  │                              │
```

---

## Load Flow

```
    Client                      Repository                     Event Store
        │                           │                              │
        │ get(work_item_id)         │                              │
        │────────────────────────►  │                              │
        │                           │ _stream_id(id)               │
        │                           │─────────►                    │
        │                           │                              │
        │                           │ read(stream_id)              │
        │                           │─────────────────────────────►│
        │                           │                              │
        │                           │ [StoredEvent1, StoredEvent2, │
        │                           │  StoredEvent3]               │
        │                           │◄─────────────────────────────│
        │                           │                              │
        │                           │ _to_domain_event() × 3       │
        │                           │─────────►                    │
        │                           │                              │
        │                           │ WorkItem.load_from_history() │
        │                           │─────────►                    │
        │                           │                              │
        │ WorkItem                  │                              │
        │◄────────────────────────  │                              │
```

---

## Optimistic Concurrency

```python
# Example: Concurrent modification detection

def handle_concurrent_updates():
    """Demonstrate optimistic concurrency."""
    repo = EventSourcedWorkItemRepository(event_store)

    # User A loads work item
    item_a = repo.get(WorkItemId("WORK-001"))

    # User B loads same work item (different instance)
    item_b = repo.get(WorkItemId("WORK-001"))

    # Both at version 5

    # User A makes change and saves
    item_a.update_priority("high")
    repo.save(item_a)  # Succeeds, now version 6

    # User B makes different change
    item_b.start()

    try:
        repo.save(item_b)  # Fails!
    except ConcurrencyError as e:
        # e.expected_version == 5
        # e.actual_version == 6
        # User B must reload and retry
        pass
```

---

## Testing Pattern

```python
def test_repository_saves_events_to_store():
    """Repository appends events to event store."""
    event_store = InMemoryEventStore()
    repo = EventSourcedWorkItemRepository(event_store)

    work_item = WorkItem.create(
        id="WORK-001",
        title="Test Task",
        work_type="task",
        priority="medium",
    )

    repo.save(work_item)

    # Verify events in store
    stored = event_store.read("WorkItem-WORK-001")
    assert len(stored) == 1
    assert stored[0].event_type == "WorkItemCreated"


def test_repository_reconstitutes_from_history():
    """Repository rebuilds aggregate from event history."""
    event_store = InMemoryEventStore()
    repo = EventSourcedWorkItemRepository(event_store)

    # Create and modify
    work_item = WorkItem.create(
        id="WORK-001",
        title="Test",
        work_type="task",
        priority="low",
    )
    work_item.start()
    work_item.update_priority("high")
    repo.save(work_item)

    # Load fresh instance
    loaded = repo.get(WorkItemId("WORK-001"))

    assert loaded is not None
    assert loaded.status == WorkItemStatus.IN_PROGRESS
    assert loaded.priority == Priority.HIGH
    assert loaded.version == 3


def test_repository_detects_concurrent_modification():
    """Repository raises ConcurrencyError on version conflict."""
    event_store = InMemoryEventStore()
    repo = EventSourcedWorkItemRepository(event_store)

    # Create initial
    item = WorkItem.create(id="WORK-001", title="Test")
    repo.save(item)

    # Load two instances
    item1 = repo.get(WorkItemId("WORK-001"))
    item2 = repo.get(WorkItemId("WORK-001"))

    # Both modify
    item1.start()
    item2.start()

    # First save succeeds
    repo.save(item1)

    # Second save fails
    with pytest.raises(ConcurrencyError) as exc_info:
        repo.save(item2)

    assert exc_info.value.expected_version == 1
    assert exc_info.value.actual_version == 2
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Stream ID format is `{AggregateType}-{AggregateId}` for clear identification.

> **Jerry Decision**: Domain-specific queries (find_by_status, find_by_parent) should use projections, not full stream scans.

> **Jerry Decision**: Delete is soft-delete via stream deletion. Event store may implement as tombstone for audit trail.

---

## Anti-Patterns

### 1. Updating Instead of Appending

```python
# WRONG: Updating event in place
def save(self, aggregate):
    events = aggregate.collect_events()
    for event in events:
        self._event_store.update(event)  # NO!

# CORRECT: Always append
def save(self, aggregate):
    events = aggregate.collect_events()
    self._event_store.append(stream_id, events, expected_version)
```

### 2. Bypassing Aggregate for Persistence

```python
# WRONG: Saving events directly
def save_event(self, event: DomainEvent):
    self._event_store.append(stream_id, [event], version)

# CORRECT: Always go through aggregate
def save(self, aggregate: WorkItem):
    events = aggregate.collect_events()  # Aggregate controls events
    self._event_store.append(stream_id, events, version)
```

---

## References

- **Greg Young**: [Event Sourcing](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)
- **Vaughn Vernon**: Implementing DDD (2013), Chapter 12
- **Design Canon**: Section 5.6 - Event-Sourced Repository
- **Related Patterns**: PAT-REPO-001 (Generic Repository), PAT-EVT-004 (Event Store), PAT-AGG-003 (History Replay)
