# PAT-REPO-003: Snapshot Store Pattern

> **Status**: OPTIONAL
> **Category**: Repository Pattern
> **Location**: `src/application/ports/secondary/`

---

## Overview

Snapshots optimize event-sourced aggregate loading by persisting periodic state captures. Instead of replaying hundreds of events, the repository loads the latest snapshot and replays only subsequent events.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Greg Young** | "Snapshots are an optimization, not a fundamental change to event sourcing" |
| **Event Store** | "Snapshotting reduces read latency for long-lived aggregates" |
| **Vaughn Vernon** | "Snapshot every N events or at time intervals" |

---

## Jerry Implementation

### Snapshot Port

```python
# File: src/application/ports/secondary/isnapshot_store.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Protocol


def _current_utc() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class Snapshot:
    """Aggregate state snapshot.

    Captures aggregate state at a specific version,
    enabling faster reconstitution.
    """

    aggregate_id: str
    aggregate_type: str
    version: int
    state: dict[str, Any]
    created_at: datetime = field(default_factory=_current_utc)


class ISnapshotStore(Protocol):
    """Port for aggregate snapshot persistence.

    Stores periodic state snapshots to optimize
    aggregate reconstitution from events.
    """

    def save(self, snapshot: Snapshot) -> None:
        """Save an aggregate snapshot.

        Args:
            snapshot: Snapshot to persist
        """
        ...

    def get_latest(
        self,
        aggregate_type: str,
        aggregate_id: str,
    ) -> Snapshot | None:
        """Get the most recent snapshot for an aggregate.

        Args:
            aggregate_type: Type of aggregate (e.g., "WorkItem")
            aggregate_id: Unique aggregate identifier

        Returns:
            Latest snapshot or None if no snapshots exist
        """
        ...

    def delete(self, aggregate_type: str, aggregate_id: str) -> bool:
        """Delete all snapshots for an aggregate.

        Args:
            aggregate_type: Type of aggregate
            aggregate_id: Aggregate identifier

        Returns:
            True if snapshots deleted, False if none found
        """
        ...
```

---

## Repository with Snapshot Support

```python
# File: src/work_tracking/infrastructure/persistence/snapshotting_work_item_repository.py
from __future__ import annotations

from typing import TYPE_CHECKING

from src.application.ports.secondary.isnapshot_store import ISnapshotStore, Snapshot
from src.shared_kernel.exceptions import AggregateNotFoundError, ConcurrencyError
from src.work_tracking.domain.aggregates.work_item import WorkItem
from src.work_tracking.domain.events.event_registry import EventRegistry
from src.work_tracking.domain.ports.event_store import IEventStore
from src.work_tracking.domain.value_objects.work_item_id import WorkItemId

if TYPE_CHECKING:
    from src.shared_kernel.domain_event import DomainEvent


class SnapshottingWorkItemRepository:
    """Event-sourced repository with snapshot optimization.

    Combines event sourcing with periodic snapshots:
    1. Load latest snapshot (if exists)
    2. Replay only events after snapshot version
    3. Optionally create new snapshot after save

    References:
        - PAT-REPO-002: Event-Sourced Repository
        - PAT-AGG-003: History Replay pattern
    """

    STREAM_PREFIX = "WorkItem"
    SNAPSHOT_INTERVAL = 10  # Snapshot every 10 events

    def __init__(
        self,
        event_store: IEventStore,
        snapshot_store: ISnapshotStore,
    ) -> None:
        """Initialize with event and snapshot stores.

        Args:
            event_store: Event persistence adapter
            snapshot_store: Snapshot persistence adapter
        """
        self._event_store = event_store
        self._snapshot_store = snapshot_store

    def get(self, id: WorkItemId) -> WorkItem | None:
        """Load aggregate using snapshot optimization.

        Strategy:
        1. Try to load latest snapshot
        2. If snapshot exists, replay events from snapshot version
        3. If no snapshot, replay all events

        Args:
            id: Work item identifier

        Returns:
            Reconstituted aggregate or None if not found
        """
        stream_id = self._stream_id(id)

        # Try snapshot first
        snapshot = self._snapshot_store.get_latest(
            aggregate_type=self.STREAM_PREFIX,
            aggregate_id=id.value,
        )

        if snapshot:
            # Load from snapshot + subsequent events
            return self._load_from_snapshot(snapshot, stream_id)
        else:
            # Full event replay
            return self._load_from_events(stream_id)

    def get_or_raise(self, id: WorkItemId) -> WorkItem:
        """Load aggregate or raise if not found."""
        work_item = self.get(id)
        if work_item is None:
            raise AggregateNotFoundError(
                entity_type="WorkItem",
                entity_id=id.value,
            )
        return work_item

    def save(self, aggregate: WorkItem) -> None:
        """Persist aggregate and optionally create snapshot.

        Creates snapshot if version is multiple of SNAPSHOT_INTERVAL.

        Args:
            aggregate: Work item to persist

        Raises:
            ConcurrencyError: If version conflict detected
        """
        stream_id = self._stream_id(WorkItemId(aggregate.id))
        domain_events = aggregate.collect_events()

        if not domain_events:
            return

        # Append events
        stored_events = [
            self._to_stored_event(event, stream_id)
            for event in domain_events
        ]
        expected_version = aggregate.version - len(domain_events)

        try:
            self._event_store.append(stream_id, stored_events, expected_version)
        except Exception as e:
            if "concurrency" in str(e).lower():
                raise ConcurrencyError(
                    entity_type="WorkItem",
                    entity_id=aggregate.id,
                    expected_version=expected_version,
                    actual_version=aggregate.version,
                ) from e
            raise

        # Create snapshot if at interval
        if aggregate.version % self.SNAPSHOT_INTERVAL == 0:
            self._create_snapshot(aggregate)

    def delete(self, id: WorkItemId) -> bool:
        """Delete aggregate and its snapshots."""
        stream_id = self._stream_id(id)
        stream_deleted = self._event_store.delete_stream(stream_id)
        self._snapshot_store.delete(self.STREAM_PREFIX, id.value)
        return stream_deleted

    def exists(self, id: WorkItemId) -> bool:
        """Check if aggregate exists."""
        stream_id = self._stream_id(id)
        return self._event_store.stream_exists(stream_id)

    # Internal methods

    def _load_from_snapshot(
        self,
        snapshot: Snapshot,
        stream_id: str,
    ) -> WorkItem:
        """Reconstitute from snapshot plus subsequent events."""
        # Restore from snapshot state
        work_item = WorkItem.from_snapshot(snapshot.state, snapshot.version)

        # Load events after snapshot
        stored_events = self._event_store.read(
            stream_id,
            from_version=snapshot.version + 1,
        )

        if stored_events:
            domain_events = [
                self._to_domain_event(stored)
                for stored in stored_events
            ]
            work_item.apply_events(domain_events)

        return work_item

    def _load_from_events(self, stream_id: str) -> WorkItem | None:
        """Reconstitute from full event history."""
        stored_events = self._event_store.read(stream_id)

        if not stored_events:
            return None

        domain_events = [
            self._to_domain_event(stored)
            for stored in stored_events
        ]

        return WorkItem.load_from_history(domain_events)

    def _create_snapshot(self, aggregate: WorkItem) -> None:
        """Create snapshot of current aggregate state."""
        snapshot = Snapshot(
            aggregate_id=aggregate.id,
            aggregate_type=self.STREAM_PREFIX,
            version=aggregate.version,
            state=aggregate.to_snapshot(),
        )
        self._snapshot_store.save(snapshot)

    def _stream_id(self, id: WorkItemId) -> str:
        """Generate stream ID from work item ID."""
        return f"{self.STREAM_PREFIX}-{id.value}"

    def _to_stored_event(self, event, stream_id: str):
        """Convert domain event to stored event format."""
        from src.work_tracking.domain.ports.event_store import StoredEvent
        return StoredEvent(
            stream_id=stream_id,
            version=0,
            event_type=type(event).__name__,
            data=event.to_dict(),
            timestamp=event.timestamp,
        )

    def _to_domain_event(self, stored) -> DomainEvent:
        """Convert stored event to domain event."""
        return EventRegistry.deserialize(stored.data)
```

---

## Aggregate Snapshot Support

```python
# In WorkItem aggregate
class WorkItem(AggregateRoot):
    """Work item aggregate with snapshot support."""

    def to_snapshot(self) -> dict[str, Any]:
        """Serialize current state to snapshot format.

        Returns dictionary that can be used to restore state.
        """
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "work_type": self._work_type.value,
            "priority": self._priority.value,
            "status": self._status.value,
            "parent_id": self._parent_id,
            "subtask_ids": list(self._subtask_ids),
            "dependency_ids": list(self._dependency_ids),
            "created_at": self._created_at.isoformat(),
            "started_at": self._started_at.isoformat() if self._started_at else None,
            "completed_at": self._completed_at.isoformat() if self._completed_at else None,
        }

    @classmethod
    def from_snapshot(cls, state: dict[str, Any], version: int) -> WorkItem:
        """Restore aggregate from snapshot state.

        Args:
            state: Snapshot state dictionary
            version: Version at snapshot time

        Returns:
            Partially reconstituted aggregate
        """
        instance = cls.__new__(cls)

        # Restore state from snapshot
        instance._id = state["id"]
        instance._title = state["title"]
        instance._description = state["description"]
        instance._work_type = WorkType(state["work_type"])
        instance._priority = Priority(state["priority"])
        instance._status = WorkItemStatus(state["status"])
        instance._parent_id = state["parent_id"]
        instance._subtask_ids = list(state["subtask_ids"])
        instance._dependency_ids = list(state["dependency_ids"])
        instance._created_at = datetime.fromisoformat(state["created_at"])
        instance._started_at = (
            datetime.fromisoformat(state["started_at"])
            if state["started_at"] else None
        )
        instance._completed_at = (
            datetime.fromisoformat(state["completed_at"])
            if state["completed_at"] else None
        )

        # Set version and initialize events list
        instance._version = version
        instance._events = []

        return instance

    def apply_events(self, events: Sequence[DomainEvent]) -> None:
        """Apply additional events after snapshot restore."""
        for event in events:
            self._apply(event)
            self._version += 1
```

---

## Snapshot Strategies

### Interval-Based (Jerry Default)

```python
# Snapshot every N events
SNAPSHOT_INTERVAL = 10

def save(self, aggregate):
    # ... save events ...
    if aggregate.version % self.SNAPSHOT_INTERVAL == 0:
        self._create_snapshot(aggregate)
```

### Time-Based

```python
# Snapshot if last snapshot is older than threshold
SNAPSHOT_AGE_THRESHOLD = timedelta(hours=1)

def save(self, aggregate):
    # ... save events ...
    last_snapshot = self._snapshot_store.get_latest(...)
    if last_snapshot is None or self._is_stale(last_snapshot):
        self._create_snapshot(aggregate)
```

### Event-Count-Since-Snapshot

```python
# Snapshot if many events since last snapshot
MAX_EVENTS_SINCE_SNAPSHOT = 20

def get(self, id):
    snapshot = self._get_snapshot(id)
    events_since = self._get_events_since(snapshot.version)

    work_item = self._restore(snapshot, events_since)

    # Opportunistic snapshot
    if len(events_since) > self.MAX_EVENTS_SINCE_SNAPSHOT:
        self._create_snapshot(work_item)

    return work_item
```

---

## In-Memory Snapshot Store

```python
# File: src/infrastructure/adapters/persistence/in_memory_snapshot_store.py
from src.application.ports.secondary.isnapshot_store import ISnapshotStore, Snapshot


class InMemorySnapshotStore:
    """In-memory snapshot store for testing."""

    def __init__(self) -> None:
        # Key: (aggregate_type, aggregate_id)
        self._snapshots: dict[tuple[str, str], Snapshot] = {}

    def save(self, snapshot: Snapshot) -> None:
        """Save snapshot, replacing any existing."""
        key = (snapshot.aggregate_type, snapshot.aggregate_id)
        self._snapshots[key] = snapshot

    def get_latest(
        self,
        aggregate_type: str,
        aggregate_id: str,
    ) -> Snapshot | None:
        """Get latest snapshot for aggregate."""
        key = (aggregate_type, aggregate_id)
        return self._snapshots.get(key)

    def delete(self, aggregate_type: str, aggregate_id: str) -> bool:
        """Delete snapshots for aggregate."""
        key = (aggregate_type, aggregate_id)
        if key in self._snapshots:
            del self._snapshots[key]
            return True
        return False
```

---

## Testing Pattern

```python
def test_repository_loads_from_snapshot():
    """Repository uses snapshot for faster loading."""
    event_store = InMemoryEventStore()
    snapshot_store = InMemorySnapshotStore()
    repo = SnapshottingWorkItemRepository(event_store, snapshot_store)

    # Create work item with many events
    work_item = WorkItem.create(id="WORK-001", title="Test", ...)
    for i in range(15):
        work_item.add_note(f"Note {i}")
    repo.save(work_item)

    # Verify snapshot was created (at version 10)
    snapshot = snapshot_store.get_latest("WorkItem", "WORK-001")
    assert snapshot is not None
    assert snapshot.version == 10

    # Load uses snapshot + 5 subsequent events
    loaded = repo.get(WorkItemId("WORK-001"))
    assert loaded.version == 15


def test_repository_falls_back_to_events_without_snapshot():
    """Repository works without snapshots."""
    event_store = InMemoryEventStore()
    snapshot_store = InMemorySnapshotStore()
    repo = SnapshottingWorkItemRepository(event_store, snapshot_store)

    work_item = WorkItem.create(id="WORK-001", title="Test", ...)
    work_item.start()
    repo.save(work_item)  # Only 2 events, below snapshot threshold

    # No snapshot should exist
    assert snapshot_store.get_latest("WorkItem", "WORK-001") is None

    # But loading still works (from events only)
    loaded = repo.get(WorkItemId("WORK-001"))
    assert loaded.status == WorkItemStatus.IN_PROGRESS


def test_aggregate_snapshot_roundtrip():
    """Aggregate serializes and restores from snapshot."""
    original = WorkItem.create(id="WORK-001", title="Test Task", ...)
    original.start()
    original.update_priority("high")

    # Snapshot and restore
    state = original.to_snapshot()
    restored = WorkItem.from_snapshot(state, original.version)

    assert restored.id == original.id
    assert restored.title == original.title
    assert restored.status == original.status
    assert restored.priority == original.priority
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Snapshot interval is 10 events. This balances storage overhead against load time optimization.

> **Jerry Decision**: Snapshots are optional optimization. Repositories MUST work without snapshots (pure event replay).

> **Jerry Decision**: Aggregates implement `to_snapshot()` and `from_snapshot()` for snapshot support.

---

## References

- **Greg Young**: [Snapshotting](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)
- **Event Store**: [Snapshotting Aggregates](https://developers.eventstore.com/)
- **Design Canon**: Section 5.7 - Snapshot Optimization
- **Related Patterns**: PAT-REPO-002 (Event-Sourced Repository), PAT-AGG-003 (History Replay)
