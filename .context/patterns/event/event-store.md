# PAT-EVT-004: Event Store Pattern

> **Status**: MANDATORY
> **Category**: Event Pattern
> **Location**: `src/work_tracking/domain/ports/event_store.py`

---

## Overview

The Event Store is a secondary port that defines the contract for event persistence. It enables append-only storage of domain events with optimistic concurrency control.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Greg Young** | "EventStore is an append-only log with optimistic concurrency" |
| **Martin Fowler** | "Event Sourcing stores every change as an event" |
| **Event Store DB** | "Streams are the fundamental storage unit" |

---

## Jerry Implementation

### Port Definition

```python
# File: src/work_tracking/domain/ports/event_store.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Protocol, Sequence
from uuid import UUID, uuid4


def _current_utc() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class StoredEvent:
    """Immutable wrapper for persisted domain event.

    Represents an event as stored in the event store,
    with stream position and storage metadata.
    """

    stream_id: str
    version: int
    event_type: str
    data: dict
    timestamp: datetime = field(default_factory=_current_utc)
    event_id: UUID = field(default_factory=uuid4)


class IEventStore(Protocol):
    """Port for event persistence.

    Defines the contract for append-only event storage
    with optimistic concurrency control.

    References:
        - PAT-EVT-001: DomainEvent base class
        - PAT-AGG-003: History Replay pattern
    """

    def append(
        self,
        stream_id: str,
        events: Sequence[StoredEvent],
        expected_version: int,
    ) -> None:
        """Append events to stream with optimistic concurrency.

        Args:
            stream_id: Unique stream identifier (e.g., "WorkItem-WORK-001")
            events: Events to append
            expected_version: Expected current stream version

        Raises:
            ConcurrencyError: If current version != expected_version
            StreamNotFoundError: If expected_version > 0 and stream doesn't exist
        """
        ...

    def read(
        self,
        stream_id: str,
        from_version: int = 1,
        to_version: int | None = None,
    ) -> Sequence[StoredEvent]:
        """Read events from stream.

        Args:
            stream_id: Stream to read from
            from_version: Start reading from this version (inclusive)
            to_version: Stop at this version (inclusive), None for all

        Returns:
            Ordered sequence of events
        """
        ...

    def get_version(self, stream_id: str) -> int:
        """Get current stream version.

        Returns 0 if stream doesn't exist.
        """
        ...

    def stream_exists(self, stream_id: str) -> bool:
        """Check if stream exists."""
        ...

    def delete_stream(self, stream_id: str) -> bool:
        """Delete stream (soft delete/tombstone in production).

        Returns True if stream was deleted, False if not found.
        """
        ...


class EventStoreError(Exception):
    """Base error for event store operations."""
    pass


class ConcurrencyError(EventStoreError):
    """Raised when optimistic concurrency check fails."""

    def __init__(
        self,
        stream_id: str,
        expected_version: int,
        actual_version: int,
    ) -> None:
        self.stream_id = stream_id
        self.expected_version = expected_version
        self.actual_version = actual_version
        super().__init__(
            f"Concurrency error on stream {stream_id}: "
            f"expected version {expected_version}, actual {actual_version}"
        )


class StreamNotFoundError(EventStoreError):
    """Raised when stream doesn't exist."""

    def __init__(self, stream_id: str) -> None:
        self.stream_id = stream_id
        super().__init__(f"Stream not found: {stream_id}")
```

---

## In-Memory Adapter (Testing)

```python
# File: src/work_tracking/infrastructure/persistence/in_memory_event_store.py
from collections import defaultdict
from threading import Lock
from typing import Sequence

from src.work_tracking.domain.ports.event_store import (
    ConcurrencyError,
    IEventStore,
    StoredEvent,
    StreamNotFoundError,
)


class InMemoryEventStore:
    """In-memory event store for testing.

    Thread-safe implementation suitable for unit tests
    and development environments.
    """

    def __init__(self) -> None:
        self._streams: dict[str, list[StoredEvent]] = defaultdict(list)
        self._lock = Lock()

    def append(
        self,
        stream_id: str,
        events: Sequence[StoredEvent],
        expected_version: int,
    ) -> None:
        with self._lock:
            current_version = self.get_version(stream_id)

            if current_version != expected_version:
                raise ConcurrencyError(
                    stream_id=stream_id,
                    expected_version=expected_version,
                    actual_version=current_version,
                )

            for i, event in enumerate(events):
                # Ensure correct versioning
                versioned_event = StoredEvent(
                    stream_id=event.stream_id,
                    version=expected_version + i + 1,
                    event_type=event.event_type,
                    data=event.data,
                    timestamp=event.timestamp,
                    event_id=event.event_id,
                )
                self._streams[stream_id].append(versioned_event)

    def read(
        self,
        stream_id: str,
        from_version: int = 1,
        to_version: int | None = None,
    ) -> Sequence[StoredEvent]:
        with self._lock:
            events = self._streams.get(stream_id, [])

            # Filter by version range
            filtered = [
                e for e in events
                if e.version >= from_version
                and (to_version is None or e.version <= to_version)
            ]

            return filtered

    def get_version(self, stream_id: str) -> int:
        with self._lock:
            events = self._streams.get(stream_id, [])
            return len(events)

    def stream_exists(self, stream_id: str) -> bool:
        with self._lock:
            return stream_id in self._streams and len(self._streams[stream_id]) > 0

    def delete_stream(self, stream_id: str) -> bool:
        with self._lock:
            if stream_id in self._streams:
                del self._streams[stream_id]
                return True
            return False
```

---

## Usage in Repository

```python
class EventSourcedWorkItemRepository:
    """Repository using event store for persistence."""

    def __init__(self, event_store: IEventStore) -> None:
        self._event_store = event_store

    def get(self, id: WorkItemId) -> WorkItem | None:
        stream_id = f"WorkItem-{id.value}"
        stored_events = self._event_store.read(stream_id)

        if not stored_events:
            return None

        # Convert StoredEvent to DomainEvent
        domain_events = [
            EventRegistry.deserialize(e.data)
            for e in stored_events
        ]

        return WorkItem.load_from_history(domain_events)

    def save(self, aggregate: WorkItem) -> None:
        stream_id = f"WorkItem-{aggregate.id}"
        domain_events = aggregate.collect_events()

        if not domain_events:
            return

        # Convert DomainEvent to StoredEvent
        stored_events = [
            StoredEvent(
                stream_id=stream_id,
                version=0,  # Will be set by event store
                event_type=type(e).__name__,
                data=e.to_dict(),
                timestamp=e.timestamp,
            )
            for e in domain_events
        ]

        expected_version = aggregate.version - len(domain_events)
        self._event_store.append(stream_id, stored_events, expected_version)
```

---

## Concurrency Control

```
Writer A                    Event Store                    Writer B
    │                           │                              │
    │  append(expected=2)       │                              │
    │ ─────────────────────────►│                              │
    │                           │  append(expected=2)          │
    │                           │◄─────────────────────────────│
    │                           │                              │
    │  ✓ version 3              │                              │
    │◄─────────────────────────│                              │
    │                           │  ✗ ConcurrencyError          │
    │                           │  expected=2, actual=3        │
    │                           │─────────────────────────────►│
```

---

## Testing Pattern

```python
def test_event_store_appends_events():
    """Events are stored in stream."""
    store = InMemoryEventStore()

    events = [
        StoredEvent(
            stream_id="test-1",
            version=1,
            event_type="TestEvent",
            data={"value": "data"},
        )
    ]

    store.append("test-1", events, expected_version=0)

    stored = store.read("test-1")
    assert len(stored) == 1
    assert stored[0].event_type == "TestEvent"


def test_event_store_detects_concurrency_conflict():
    """Concurrent writes are detected."""
    store = InMemoryEventStore()

    # First writer succeeds
    store.append("test-1", [make_event()], expected_version=0)

    # Second writer with stale version fails
    with pytest.raises(ConcurrencyError) as exc_info:
        store.append("test-1", [make_event()], expected_version=0)

    assert exc_info.value.expected_version == 0
    assert exc_info.value.actual_version == 1
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Stream IDs follow format `{AggregateType}-{AggregateId}` (e.g., `WorkItem-WORK-001`).

> **Jerry Decision**: In-memory event store for testing; file-based JSON for development; real event store for production (future).

> **Jerry Decision**: Soft delete (tombstone) for streams rather than hard delete to maintain audit trail.

---

## References

- **Greg Young**: [Event Sourcing](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)
- **Event Store DB**: [Streams and Events](https://developers.eventstore.com/)
- **Design Canon**: Section 5.5 - Event Store
- **Related Patterns**: PAT-EVT-001 (DomainEvent), PAT-AGG-003 (History Replay)
