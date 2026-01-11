"""
IEventStore - Event store port for domain event persistence.

Defines the contract for append-only event storage with optimistic
concurrency control. Implementations provide the actual persistence
mechanism (file-based, in-memory, etc.).

References:
    - PAT-001: Event Store Interface Pattern
    - PAT-003: Optimistic Concurrency with File Locking
    - pyeventsourcing EventStore API
    - Microsoft Azure Event Sourcing Pattern
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Protocol
from uuid import UUID, uuid4

# =============================================================================
# Exceptions
# =============================================================================


class EventStoreError(Exception):
    """Base exception for event store errors."""


class ConcurrencyError(EventStoreError):
    """
    Raised when optimistic concurrency check fails.

    This occurs when attempting to append events with an expected_version
    that doesn't match the stream's current version.

    Attributes:
        stream_id: The stream where the conflict occurred
        expected_version: The version the caller expected
        actual_version: The actual current version of the stream

    Example:
        >>> raise ConcurrencyError("WORK-001", expected=5, actual=7)
        ConcurrencyError: Stream 'WORK-001' version mismatch: expected 5, actual 7
    """

    def __init__(self, stream_id: str, expected: int, actual: int) -> None:
        self.stream_id = stream_id
        self.expected_version = expected
        self.actual_version = actual
        super().__init__(
            f"Stream '{stream_id}' version mismatch: expected {expected}, actual {actual}"
        )


class StreamNotFoundError(EventStoreError):
    """
    Raised when attempting to read a non-existent stream.

    Attributes:
        stream_id: The stream that was not found

    Example:
        >>> raise StreamNotFoundError("WORK-999")
        StreamNotFoundError: Stream 'WORK-999' not found
    """

    def __init__(self, stream_id: str) -> None:
        self.stream_id = stream_id
        super().__init__(f"Stream '{stream_id}' not found")


# =============================================================================
# Value Objects
# =============================================================================


def _current_utc() -> datetime:
    """Get current UTC timestamp."""
    return datetime.now(UTC)


@dataclass(frozen=True, slots=True)
class StoredEvent:
    """
    Immutable wrapper for a persisted domain event.

    StoredEvent adds stream metadata (stream_id, version) to domain events
    for persistence and retrieval. It serves as the unit of storage in
    the event store.

    Attributes:
        stream_id: Unique identifier for the event stream (aggregate ID)
        version: Sequential version number within the stream (1-based)
        event_type: Fully qualified type name for deserialization
        data: Serialized event payload as dictionary
        timestamp: When the event was stored (UTC)
        event_id: Globally unique identifier for this event

    Invariants:
        - stream_id must not be empty
        - version must be >= 1
        - event_type must not be empty
        - data must be a dictionary

    Example:
        >>> event = StoredEvent(
        ...     stream_id="WORK-001",
        ...     version=1,
        ...     event_type="WorkItemCreated",
        ...     data={"title": "Implement feature"},
        ... )
        >>> event.stream_id
        'WORK-001'
    """

    stream_id: str
    version: int
    event_type: str
    data: dict
    timestamp: datetime = field(default_factory=_current_utc)
    event_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        """Validate stored event after initialization."""
        if not self.stream_id:
            raise ValueError("stream_id cannot be empty")
        if self.version < 1:
            raise ValueError(f"version must be >= 1, got {self.version}")
        if not self.event_type:
            raise ValueError("event_type cannot be empty")
        if not isinstance(self.data, dict):
            raise TypeError(f"data must be a dict, got {type(self.data).__name__}")

    def to_dict(self) -> dict:
        """
        Serialize to dictionary for persistence.

        Returns:
            Dictionary representation suitable for JSON serialization.
        """
        return {
            "stream_id": self.stream_id,
            "version": self.version,
            "event_type": self.event_type,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "event_id": str(self.event_id),
        }

    @classmethod
    def from_dict(cls, data: dict) -> StoredEvent:
        """
        Deserialize from dictionary.

        Args:
            data: Dictionary from persistence layer

        Returns:
            Reconstructed StoredEvent instance
        """
        timestamp = data.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        elif timestamp is None:
            timestamp = _current_utc()

        event_id = data.get("event_id")
        if isinstance(event_id, str):
            event_id = UUID(event_id)
        elif event_id is None:
            event_id = uuid4()

        return cls(
            stream_id=data["stream_id"],
            version=data["version"],
            event_type=data["event_type"],
            data=data["data"],
            timestamp=timestamp,
            event_id=event_id,
        )


# =============================================================================
# Port Interface
# =============================================================================


class IEventStore(Protocol):
    """
    Port: Event Store for persisting domain events.

    Implements append-only storage with optimistic concurrency control.
    This is the primary persistence mechanism for event-sourced aggregates.

    Thread Safety:
        Implementations MUST ensure thread-safe operations, typically via
        file locking or database transactions.

    Concurrency Model:
        Uses optimistic concurrency - callers provide expected_version,
        and the operation fails if it doesn't match actual version.

    References:
        - PAT-001: Event Store Interface Pattern
        - PAT-003: Optimistic Concurrency with File Locking
        - pyeventsourcing EventStore API
        - Microsoft Azure Event Sourcing Pattern

    Example Usage:
        >>> store = InMemoryEventStore()
        >>> events = [StoredEvent(stream_id="WORK-001", version=1, ...)]
        >>> store.append("WORK-001", events, expected_version=0)
        >>> loaded = store.read("WORK-001")
        >>> len(loaded)
        1
    """

    def append(
        self,
        stream_id: str,
        events: Sequence[StoredEvent],
        expected_version: int,
    ) -> None:
        """
        Append events to a stream with optimistic concurrency.

        This is an atomic operation - either all events are appended,
        or none are (on concurrency conflict).

        Args:
            stream_id: Unique identifier for the event stream (aggregate ID)
            events: Sequence of events to append (must have correct versions)
            expected_version: Expected current version for concurrency check.
                Use -1 for new streams, or current version for existing.

        Raises:
            ConcurrencyError: If current version != expected_version
            ValueError: If events is empty or has invalid versions

        Note:
            Events MUST have sequential versions starting from
            expected_version + 1.

        Example:
            >>> store.append("WORK-001", [event1, event2], expected_version=0)
            # event1.version should be 1, event2.version should be 2
        """
        ...

    def read(
        self,
        stream_id: str,
        from_version: int = 1,
        to_version: int | None = None,
    ) -> Sequence[StoredEvent]:
        """
        Read events from a stream.

        Args:
            stream_id: Stream to read from
            from_version: Starting version (inclusive), defaults to 1
            to_version: Ending version (inclusive), None for all remaining

        Returns:
            Events in version order (ascending)

        Raises:
            StreamNotFoundError: If the stream doesn't exist

        Example:
            >>> events = store.read("WORK-001")  # All events
            >>> events = store.read("WORK-001", from_version=5)  # From v5 onwards
            >>> events = store.read("WORK-001", from_version=1, to_version=10)
        """
        ...

    def get_version(self, stream_id: str) -> int:
        """
        Get current version of a stream.

        The version is the highest event version in the stream.
        For empty/new streams, returns -1.

        Args:
            stream_id: Stream to check

        Returns:
            Current version number, or -1 if stream doesn't exist

        Example:
            >>> store.get_version("WORK-001")
            5
            >>> store.get_version("non-existent")
            -1
        """
        ...

    def stream_exists(self, stream_id: str) -> bool:
        """
        Check if a stream exists.

        Args:
            stream_id: Stream to check

        Returns:
            True if stream has at least one event

        Example:
            >>> store.stream_exists("WORK-001")
            True
            >>> store.stream_exists("non-existent")
            False
        """
        ...

    def delete_stream(self, stream_id: str) -> bool:
        """
        Delete all events in a stream.

        This is a destructive operation and should be used with caution.
        In production event stores, deletion is often disallowed or
        replaced with soft-delete via tombstone events.

        Args:
            stream_id: Stream to delete

        Returns:
            True if stream was deleted, False if it didn't exist

        Example:
            >>> store.delete_stream("WORK-001")
            True
            >>> store.delete_stream("non-existent")
            False
        """
        ...
