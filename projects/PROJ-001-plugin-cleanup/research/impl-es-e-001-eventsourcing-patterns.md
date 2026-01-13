# Event Sourcing Patterns for Python Implementation

| Field | Value |
|-------|-------|
| **PS ID** | impl-es |
| **Entry ID** | e-001 |
| **Date** | 2026-01-09 |
| **Author** | ps-researcher (v2.0.0) |
| **Status** | Complete |

---

## L0: Executive Summary

**Event Sourcing (ES)** is an architectural pattern where all changes to application state are stored as an immutable sequence of events, rather than storing only the current state. This approach provides a complete audit trail, enables temporal queries, and supports rebuilding system state at any point in time.

### Why Event Sourcing for Jerry's Domain Model?

1. **Audit Trail**: Every change to work items, initiatives, and tasks is preserved with full history
2. **Temporal Queries**: Ability to reconstruct state at any point in time ("What was the status last Tuesday?")
3. **Debug & Recovery**: Replay events to diagnose issues or recover from corruption
4. **Multi-Agent Coordination**: Events provide natural boundaries for concurrent access

### Key Infrastructure Components

| Component | Purpose | Interface Pattern |
|-----------|---------|-------------------|
| **IEventStore** | Append and read events with optimistic concurrency | `append(stream_id, events, expected_version)` |
| **ISnapshotStore** | Store aggregate state for fast reconstruction | `save(stream_id, snapshot, version)` |
| **AggregateRoot** | Base class for event-sourced domain entities | `_raise_event()`, `collect_events()` |

### Recommendation

Implement ES infrastructure in `src/infrastructure/persistence/` with ports defined in `src/domain/ports/`. Use the pyeventsourcing library patterns as reference but implement custom lightweight versions aligned with Jerry's zero-dependency-core principle.

---

## L1: Technical Implementation Patterns

### 1. IEventStore Interface Pattern

The event store is the heart of event sourcing, responsible for persisting and retrieving domain events.

#### Interface Definition (Port)

```python
# src/domain/ports/event_store.py
from abc import ABC, abstractmethod
from typing import Protocol, TypeVar, Sequence
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class StoredEvent:
    """Immutable event as persisted in the store."""
    stream_id: str
    version: int
    event_type: str
    data: dict
    timestamp: datetime
    event_id: UUID


class IEventStore(Protocol):
    """Port: Event Store for persisting domain events.

    Implements append-only storage with optimistic concurrency control.

    References:
        - pyeventsourcing EventStore API
        - Azure Event Sourcing Pattern
    """

    def append(
        self,
        stream_id: str,
        events: Sequence[StoredEvent],
        expected_version: int
    ) -> None:
        """Append events to a stream with optimistic concurrency.

        Args:
            stream_id: Unique identifier for the event stream (aggregate ID)
            events: Sequence of events to append
            expected_version: Expected current version for concurrency check

        Raises:
            ConcurrencyError: If current version != expected_version

        Note:
            If a conflict occurs, none of the new events are stored.
            This follows pyeventsourcing's EventStore.put() semantics.
        """
        ...

    def read(
        self,
        stream_id: str,
        from_version: int = 0,
        to_version: int | None = None
    ) -> Sequence[StoredEvent]:
        """Read events from a stream.

        Args:
            stream_id: Stream to read from
            from_version: Starting version (inclusive)
            to_version: Ending version (inclusive), None for all

        Returns:
            Events in version order
        """
        ...

    def get_version(self, stream_id: str) -> int:
        """Get current version of a stream.

        Returns:
            Current version number, or -1 if stream doesn't exist
        """
        ...
```

#### Optimistic Concurrency Control

From [Microsoft Azure Event Sourcing Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing):

> Event sourcing can help prevent concurrent updates from causing conflicts because it avoids the requirement to directly update objects in the data store.

Implementation pattern from [Streamstone (Azure Table Storage)](https://github.com/yevhen/Streamstone):

```python
# Optimistic concurrency implementation
class ConcurrencyError(Exception):
    """Raised when optimistic concurrency check fails."""
    def __init__(self, stream_id: str, expected: int, actual: int):
        self.stream_id = stream_id
        self.expected_version = expected
        self.actual_version = actual
        super().__init__(
            f"Stream '{stream_id}' version mismatch: "
            f"expected {expected}, actual {actual}"
        )
```

#### JSON File Adapter Implementation

```python
# src/infrastructure/persistence/json_event_store.py
from pathlib import Path
import json
import fcntl  # File locking for concurrency
from typing import Sequence
from datetime import datetime

class JsonEventStore:
    """Adapter: File-based event store using JSON.

    Each stream is stored in a separate file:
    {base_path}/{stream_id}.events.json

    File locking ensures atomic operations.
    """

    def __init__(self, base_path: Path):
        self._base_path = base_path
        self._base_path.mkdir(parents=True, exist_ok=True)

    def _stream_path(self, stream_id: str) -> Path:
        # Sanitize stream_id for filesystem
        safe_id = stream_id.replace("/", "_")
        return self._base_path / f"{safe_id}.events.json"

    def append(
        self,
        stream_id: str,
        events: Sequence[StoredEvent],
        expected_version: int
    ) -> None:
        path = self._stream_path(stream_id)

        with open(path, "a+") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # Exclusive lock
            try:
                f.seek(0)
                existing = json.load(f) if f.read(1) else {"events": [], "version": -1}
                f.seek(0)

                current_version = existing.get("version", -1)
                if current_version != expected_version:
                    raise ConcurrencyError(stream_id, expected_version, current_version)

                # Append events
                for i, event in enumerate(events):
                    event_dict = {
                        "stream_id": event.stream_id,
                        "version": expected_version + i + 1,
                        "event_type": event.event_type,
                        "data": event.data,
                        "timestamp": event.timestamp.isoformat(),
                        "event_id": str(event.event_id)
                    }
                    existing["events"].append(event_dict)

                existing["version"] = expected_version + len(events)

                f.seek(0)
                f.truncate()
                json.dump(existing, f, indent=2)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
```

### 2. ISnapshotStore Interface Pattern

Snapshots optimize aggregate reconstruction by storing periodic state captures.

#### When to Snapshot

From [Kurrent.io Snapshots Guide](https://www.kurrent.io/blog/snapshots-in-event-sourcing):

> **Event Count-Based**: Take a snapshot after a certain number of events (e.g., every 100 events)
> **Time-Based**: Take a snapshot at regular intervals (e.g., every hour)
> **State Change-Based**: Take a snapshot when significant changes occur

From [EventStore Blog on Snapshotting Strategies](https://www.eventstore.com/blog/snapshotting-strategies):

> Before you go down this road, make sure you absolutely need snapshots. They might not be required.

#### Interface Definition

```python
# src/domain/ports/snapshot_store.py
from typing import Protocol
from dataclasses import dataclass

@dataclass(frozen=True)
class Snapshot:
    """Point-in-time state of an aggregate."""
    stream_id: str
    version: int
    state: dict
    timestamp: datetime


class ISnapshotStore(Protocol):
    """Port: Snapshot Store for optimized aggregate loading.

    References:
        - pyeventsourcing Snapshot.take() pattern
        - CodeOpinion Snapshots Guide
    """

    def save(self, stream_id: str, snapshot: Snapshot) -> None:
        """Save a snapshot of aggregate state.

        Args:
            stream_id: Aggregate stream identifier
            snapshot: State capture at specific version
        """
        ...

    def get_latest(self, stream_id: str) -> Snapshot | None:
        """Get the most recent snapshot for a stream.

        Args:
            stream_id: Aggregate stream identifier

        Returns:
            Latest snapshot or None if no snapshots exist
        """
        ...
```

#### Snapshot Strategy Implementation

```python
# src/infrastructure/persistence/snapshot_strategy.py
from abc import ABC, abstractmethod

class SnapshotStrategy(ABC):
    """Determines when to create a new snapshot."""

    @abstractmethod
    def should_snapshot(
        self,
        events_since_snapshot: int,
        time_since_snapshot: timedelta
    ) -> bool:
        ...


class EventCountStrategy(SnapshotStrategy):
    """Snapshot every N events."""

    def __init__(self, threshold: int = 50):
        self._threshold = threshold

    def should_snapshot(self, events_since: int, time_since: timedelta) -> bool:
        return events_since >= self._threshold


class CompositeStrategy(SnapshotStrategy):
    """Snapshot when ANY strategy triggers."""

    def __init__(self, *strategies: SnapshotStrategy):
        self._strategies = strategies

    def should_snapshot(self, events_since: int, time_since: timedelta) -> bool:
        return any(s.should_snapshot(events_since, time_since) for s in self._strategies)
```

### 3. AggregateRoot Base Class

The AggregateRoot is the foundation for event-sourced domain entities.

#### Pattern from pyeventsourcing

From [pyeventsourcing Domain Documentation](https://eventsourcing.readthedocs.io/en/stable/topics/introduction.html):

```python
# Key methods from pyeventsourcing Aggregate base class:
# - _create(event_class, id=None, **kwargs): Create new aggregate
# - trigger_event(event_class, **kwargs): Trigger subsequent events
# - collect_events(): Return pending events for persistence
```

#### Jerry Implementation

```python
# src/domain/aggregates/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar, Generic, Sequence
from uuid import UUID, uuid4

T = TypeVar("T", bound="DomainEvent")


@dataclass(frozen=True)
class DomainEvent:
    """Base class for all domain events.

    Immutable, capturing what happened at a specific point in time.

    References:
        - Martin Fowler Event Sourcing: events capture state changes
        - pyeventsourcing DomainEvent base class
    """
    originator_id: str
    originator_version: int
    timestamp: datetime = field(default_factory=datetime.utcnow)
    event_id: UUID = field(default_factory=uuid4)


class AggregateRoot(ABC):
    """Base class for event-sourced aggregates.

    Lifecycle:
        1. Create: _create() class method constructs via Created event
        2. Mutate: Commands call _raise_event() to record changes
        3. Apply: Events mutate state via _apply() dispatcher
        4. Persist: collect_events() returns pending events for storage
        5. Load: load_from_history() or load_from_snapshot() reconstructs

    References:
        - pyeventsourcing Aggregate base class API
        - DDD Aggregate pattern (Evans, 2004)
    """

    def __init__(self, id: str, version: int = 0):
        self._id = id
        self._version = version
        self._pending_events: list[DomainEvent] = []
        self._created_on: datetime | None = None
        self._modified_on: datetime | None = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def version(self) -> int:
        return self._version

    @property
    def created_on(self) -> datetime | None:
        return self._created_on

    @property
    def modified_on(self) -> datetime | None:
        return self._modified_on

    def _raise_event(self, event: DomainEvent) -> None:
        """Record a new domain event.

        1. Increments version
        2. Applies event to update state
        3. Adds event to pending list for persistence

        Based on pyeventsourcing trigger_event() pattern.
        """
        self._version += 1
        self._apply(event)
        self._pending_events.append(event)
        self._modified_on = event.timestamp

    @abstractmethod
    def _apply(self, event: DomainEvent) -> None:
        """Apply an event to update aggregate state.

        Implement event-specific state mutations.
        Must be deterministic (same events = same state).
        """
        ...

    def collect_events(self) -> Sequence[DomainEvent]:
        """Return and clear pending events.

        Call after successful persistence.

        Returns:
            List of events raised since last collection
        """
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    @classmethod
    def load_from_history(cls, events: Sequence[DomainEvent]) -> "AggregateRoot":
        """Reconstruct aggregate by replaying events.

        Args:
            events: Historical events in version order

        Returns:
            Aggregate with state rebuilt from events

        Note:
            Used when no snapshot available.
        """
        if not events:
            raise ValueError("Cannot load from empty event history")

        first_event = events[0]
        aggregate = cls.__new__(cls)
        aggregate._id = first_event.originator_id
        aggregate._version = 0
        aggregate._pending_events = []
        aggregate._created_on = first_event.timestamp
        aggregate._modified_on = None

        for event in events:
            aggregate._version = event.originator_version
            aggregate._apply(event)
            aggregate._modified_on = event.timestamp

        return aggregate

    @classmethod
    def load_from_snapshot(
        cls,
        snapshot: "Snapshot",
        events: Sequence[DomainEvent]
    ) -> "AggregateRoot":
        """Reconstruct aggregate from snapshot plus subsequent events.

        Args:
            snapshot: Point-in-time state capture
            events: Events occurring after the snapshot

        Returns:
            Aggregate with state rebuilt efficiently

        Note:
            More efficient than full replay for long-lived aggregates.
        """
        aggregate = cls.__new__(cls)
        aggregate._id = snapshot.stream_id
        aggregate._version = snapshot.version
        aggregate._pending_events = []
        aggregate._apply_snapshot(snapshot.state)

        for event in events:
            aggregate._version = event.originator_version
            aggregate._apply(event)
            aggregate._modified_on = event.timestamp

        return aggregate

    def _apply_snapshot(self, state: dict) -> None:
        """Restore aggregate state from snapshot data.

        Override in subclasses to handle specific state restoration.
        """
        for key, value in state.items():
            if hasattr(self, key):
                setattr(self, f"_{key}" if key.startswith("_") else key, value)

    def to_snapshot_state(self) -> dict:
        """Export current state for snapshotting.

        Override in subclasses for custom serialization.
        """
        return {
            k.lstrip("_"): v
            for k, v in self.__dict__.items()
            if not k.startswith("_pending")
        }
```

### 4. Complete Usage Example

```python
# Example: WorkItem aggregate with events

@dataclass(frozen=True)
class WorkItemCreated(DomainEvent):
    """Work item was created."""
    title: str
    description: str
    item_type: str


@dataclass(frozen=True)
class WorkItemStatusChanged(DomainEvent):
    """Work item status was changed."""
    old_status: str
    new_status: str
    reason: str | None = None


class WorkItem(AggregateRoot):
    """Event-sourced Work Item aggregate."""

    def __init__(self, id: str, title: str, description: str, item_type: str):
        super().__init__(id)
        self._title = title
        self._description = description
        self._item_type = item_type
        self._status = "backlog"

    @classmethod
    def create(cls, id: str, title: str, description: str, item_type: str = "task") -> "WorkItem":
        """Factory method to create a new work item."""
        item = cls(id, title, description, item_type)
        item._raise_event(WorkItemCreated(
            originator_id=id,
            originator_version=1,
            title=title,
            description=description,
            item_type=item_type
        ))
        item._created_on = item._pending_events[-1].timestamp
        return item

    def change_status(self, new_status: str, reason: str | None = None) -> None:
        """Change work item status."""
        if new_status == self._status:
            return

        self._raise_event(WorkItemStatusChanged(
            originator_id=self._id,
            originator_version=self._version + 1,
            old_status=self._status,
            new_status=new_status,
            reason=reason
        ))

    def _apply(self, event: DomainEvent) -> None:
        """Apply event to update state."""
        match event:
            case WorkItemCreated():
                self._title = event.title
                self._description = event.description
                self._item_type = event.item_type
                self._status = "backlog"
            case WorkItemStatusChanged():
                self._status = event.new_status
```

---

## L2: Architectural Implications and Trade-offs

### Event Sourcing vs CRUD: Decision Matrix

| Factor | Event Sourcing | CRUD | Jerry Fit |
|--------|----------------|------|-----------|
| **Audit Requirements** | Built-in, complete | Requires separate log | ES wins - Work items need full history |
| **Complexity** | Higher upfront | Lower | CRUD simpler, but ES ROI good |
| **Temporal Queries** | Native | Manual implementation | ES wins - "What was status yesterday?" |
| **Storage Growth** | Events accumulate | Overwrites | ES needs snapshots for long-lived items |
| **Debugging** | Replay events | Limited to logs | ES wins - Reproduce any state |
| **Multi-Agent Sync** | Event streams natural | Lock contention | ES wins - Events as sync points |

### When to Use Each (From Industry Sources)

From [Confluent Event Sourcing Course](https://developer.confluent.io/courses/event-sourcing/storing-data-as-events/):

> With CRUD, you can create and read values, but unlike CRUD, in event sourcing you never update a value and you never delete a value.

From [Baytech Consulting](https://www.baytechconsulting.com/blog/event-sourcing-explained-2025):

> Using event sourcing over CRUD is an investment of more code and effort up front, but will yield a simpler, more resilient and easier to maintain system in the future.

### Recommended Architecture for Jerry

```
src/
├── domain/
│   ├── aggregates/
│   │   ├── base.py          # AggregateRoot base class
│   │   ├── work_item.py     # WorkItem aggregate
│   │   └── initiative.py    # Initiative aggregate
│   ├── events/
│   │   ├── base.py          # DomainEvent base
│   │   ├── work_item_events.py
│   │   └── initiative_events.py
│   └── ports/
│       ├── event_store.py   # IEventStore protocol
│       └── snapshot_store.py # ISnapshotStore protocol
├── infrastructure/
│   └── persistence/
│       ├── json_event_store.py      # File-based adapter
│       ├── json_snapshot_store.py   # File-based adapter
│       └── snapshot_strategy.py     # When to snapshot
└── application/
    └── services/
        └── aggregate_repository.py   # Load/Save aggregates
```

### Key Architectural Decisions

#### ADR-001: File-Based Event Store

**Context**: Jerry uses filesystem as persistence layer.

**Decision**: Implement JSON file-based event store with file locking.

**Consequences**:
- (+) Zero external dependencies
- (+) Human-readable event logs
- (-) Not suitable for high-throughput (acceptable for Jerry's use case)
- (-) File locking limits concurrency

#### ADR-002: Snapshot Strategy

**Context**: Work items may accumulate many events over time.

**Decision**: Use event-count-based snapshotting (every 50 events).

**Consequences**:
- (+) Bounded reconstruction time
- (+) Predictable storage growth
- (-) Additional storage for snapshots
- (-) Snapshot versioning complexity

#### ADR-003: Event Schema Evolution

**Context**: Event schemas will evolve as Jerry matures.

**Decision**: Include event version in event type, use upcasters.

**Consequences**:
- (+) Backward compatibility
- (+) Clean separation of old/new schemas
- (-) Additional complexity for migrations

---

## Sources

### Primary Sources

- [pyeventsourcing Documentation](https://eventsourcing.readthedocs.io/) - Python event sourcing library
- [pyeventsourcing GitHub](https://github.com/pyeventsourcing/eventsourcing) - Source code and examples
- [Martin Fowler - Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) - Original pattern definition

### Cloud Provider Guidance

- [Microsoft Azure Event Sourcing Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing) - Enterprise patterns
- [AWS Event Sourcing Pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/event-sourcing.html) - AWS implementation guidance
- [AWS DynamoDB CQRS Event Store](https://aws.amazon.com/blogs/database/build-a-cqrs-event-store-with-amazon-dynamodb/) - DynamoDB patterns

### Snapshot Strategies

- [Kurrent.io - Snapshots in Event Sourcing](https://www.kurrent.io/blog/snapshots-in-event-sourcing) - When and why to snapshot
- [EventStore Blog - Snapshotting Strategies](https://www.eventstore.com/blog/snapshotting-strategies) - Strategy comparison
- [CodeOpinion - Snapshots for Rehydrating Aggregates](https://codeopinion.com/snapshots-in-event-sourcing-for-rehydrating-aggregates/) - Implementation patterns

### ES vs CRUD Analysis

- [Confluent - Event Sourcing vs CRUD](https://developer.confluent.io/courses/event-sourcing/storing-data-as-events/) - Comparison
- [Baytech Consulting - Event Sourcing Explained](https://www.baytechconsulting.com/blog/event-sourcing-explained-2025) - Trade-offs analysis
- [RisingStack - Event Sourcing vs CRUD](https://blog.risingstack.com/event-sourcing-vs-crud/) - Implementation comparison

### Implementation References

- [Eveneum - Cosmos DB Event Store](https://github.com/Eveneum/Eveneum) - Azure Cosmos DB adapter
- [Streamstone - Azure Table Storage](https://github.com/yevhen/Streamstone) - Azure Tables adapter
- [Microservices.io - Event Sourcing Pattern](https://microservices.io/patterns/data/event-sourcing.html) - Pattern catalog

---

*Document ID: impl-es-e-001*
*Compliance: P-001 (cited sources), P-002 (file persisted), P-004 (reasoning documented)*
