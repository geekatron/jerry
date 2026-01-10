"""
InMemoryEventStore - Thread-safe in-memory event store implementation.

A lightweight event store adapter suitable for testing and development.
Uses threading locks for thread safety and provides full IEventStore
protocol compliance.

References:
    - PAT-001: Event Store Interface Pattern
    - PAT-003: Optimistic Concurrency with File Locking
"""
from __future__ import annotations

import threading
from collections import defaultdict
from typing import Sequence

from src.work_tracking.domain.ports.event_store import (
    ConcurrencyError,
    IEventStore,
    StoredEvent,
    StreamNotFoundError,
)


class InMemoryEventStore:
    """
    Thread-safe in-memory event store implementation.

    This adapter stores events in memory using dictionaries and lists.
    Thread safety is ensured via a reentrant lock (RLock).

    Use Cases:
        - Unit testing aggregates and repositories
        - Integration testing without file I/O
        - Development and prototyping

    Thread Safety:
        All public methods are protected by a threading.RLock,
        making this safe for concurrent access.

    Memory Characteristics:
        - Events are stored in a dict[str, list[StoredEvent]]
        - No size limits are enforced
        - All data is lost when the store is garbage collected

    Example:
        >>> store = InMemoryEventStore()
        >>> event = StoredEvent(
        ...     stream_id="WORK-001",
        ...     version=1,
        ...     event_type="WorkItemCreated",
        ...     data={"title": "Test"},
        ... )
        >>> store.append("WORK-001", [event], expected_version=0)
        >>> store.get_version("WORK-001")
        1
    """

    def __init__(self) -> None:
        """Initialize empty event store."""
        self._streams: dict[str, list[StoredEvent]] = defaultdict(list)
        self._lock = threading.RLock()

    def append(
        self,
        stream_id: str,
        events: Sequence[StoredEvent],
        expected_version: int,
    ) -> None:
        """
        Append events to a stream with optimistic concurrency.

        Args:
            stream_id: Unique identifier for the event stream
            events: Sequence of events to append
            expected_version: Expected current version (-1 for new stream)

        Raises:
            ConcurrencyError: If current version != expected_version
            ValueError: If events is empty or has invalid versions

        Note:
            For new streams, use expected_version=-1 or expected_version=0.
            Both are accepted to accommodate different calling conventions.
        """
        if not events:
            raise ValueError("Cannot append empty event sequence")

        with self._lock:
            current_version = self._get_version_unlocked(stream_id)

            # Allow -1 or 0 for new streams
            if current_version == -1 and expected_version == 0:
                expected_version = -1

            if current_version != expected_version:
                raise ConcurrencyError(stream_id, expected_version, current_version)

            # Validate event versions are sequential
            # For new streams (version -1), first event should be version 1
            expected_next = max(current_version, 0) + 1
            for i, event in enumerate(events):
                expected_event_version = expected_next + i
                if event.version != expected_event_version:
                    raise ValueError(
                        f"Event version mismatch: expected {expected_event_version}, "
                        f"got {event.version} for event at index {i}"
                    )
                if event.stream_id != stream_id:
                    raise ValueError(
                        f"Event stream_id mismatch: expected '{stream_id}', "
                        f"got '{event.stream_id}'"
                    )

            # Append all events
            self._streams[stream_id].extend(events)

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
            from_version: Starting version (inclusive, 1-based)
            to_version: Ending version (inclusive), None for all

        Returns:
            Events in version order

        Raises:
            StreamNotFoundError: If the stream doesn't exist
        """
        with self._lock:
            if stream_id not in self._streams or not self._streams[stream_id]:
                raise StreamNotFoundError(stream_id)

            events = self._streams[stream_id]

            # Filter by version range
            result = [
                e for e in events
                if e.version >= from_version
                and (to_version is None or e.version <= to_version)
            ]

            return result

    def get_version(self, stream_id: str) -> int:
        """
        Get current version of a stream.

        Args:
            stream_id: Stream to check

        Returns:
            Current version number, or -1 if stream doesn't exist
        """
        with self._lock:
            return self._get_version_unlocked(stream_id)

    def _get_version_unlocked(self, stream_id: str) -> int:
        """Get version without acquiring lock (internal use)."""
        if stream_id not in self._streams or not self._streams[stream_id]:
            return -1
        return self._streams[stream_id][-1].version

    def stream_exists(self, stream_id: str) -> bool:
        """
        Check if a stream exists.

        Args:
            stream_id: Stream to check

        Returns:
            True if stream has at least one event
        """
        with self._lock:
            return (
                stream_id in self._streams
                and len(self._streams[stream_id]) > 0
            )

    def delete_stream(self, stream_id: str) -> bool:
        """
        Delete all events in a stream.

        Args:
            stream_id: Stream to delete

        Returns:
            True if stream was deleted, False if it didn't exist
        """
        with self._lock:
            if stream_id in self._streams and self._streams[stream_id]:
                del self._streams[stream_id]
                return True
            return False

    def clear(self) -> None:
        """
        Clear all streams (for testing).

        Removes all events from all streams.
        """
        with self._lock:
            self._streams.clear()

    def get_all_stream_ids(self) -> list[str]:
        """
        Get all stream IDs in the store.

        Returns:
            List of stream IDs that have at least one event
        """
        with self._lock:
            return [
                stream_id
                for stream_id, events in self._streams.items()
                if events
            ]

    def count_events(self, stream_id: str | None = None) -> int:
        """
        Count events in a stream or all streams.

        Args:
            stream_id: Specific stream, or None for total count

        Returns:
            Number of events
        """
        with self._lock:
            if stream_id is not None:
                return len(self._streams.get(stream_id, []))
            return sum(len(events) for events in self._streams.values())


# Type assertion for protocol compliance
def _assert_protocol_compliance() -> None:
    """Static assertion that InMemoryEventStore implements IEventStore."""
    store: IEventStore = InMemoryEventStore()
    _ = store  # Suppress unused variable warning
