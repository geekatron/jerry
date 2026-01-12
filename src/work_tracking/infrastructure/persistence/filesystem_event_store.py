"""
FileSystemEventStore - Persistent file-based event store implementation.

A durable event store adapter that persists events to JSON Lines files on disk.
Each stream is stored in a separate file, enabling efficient append operations
and human-readable event logs.

Storage Format:
    - Each stream stored in: {base_path}/.jerry/data/events/{stream_id}.jsonl
    - JSON Lines format (one JSON object per line)
    - Append-only writes for durability

Thread Safety:
    Uses threading.RLock for in-process thread safety and fcntl.flock
    for cross-process file locking on POSIX systems.

References:
    - PAT-001: Event Store Interface Pattern
    - PAT-003: Optimistic Concurrency with File Locking
    - DISC-019: InMemoryEventStore Not Persistent
    - TD-018: Event Sourcing for Work Item Repository
"""

from __future__ import annotations

import fcntl
import json
import os
import threading
from collections.abc import Sequence
from pathlib import Path

from src.work_tracking.domain.ports.event_store import (
    ConcurrencyError,
    IEventStore,
    StoredEvent,
    StreamNotFoundError,
)


class FileSystemEventStore:
    """
    Persistent file-based event store implementation.

    This adapter stores events in JSON Lines files on the filesystem.
    Each stream gets its own file, enabling efficient append operations
    and human-readable event logs that are git-friendly.

    Storage Structure:
        {base_path}/.jerry/data/events/
        ├── work_item-WORK-001.jsonl
        ├── work_item-WORK-002.jsonl
        └── ...

    Use Cases:
        - Production event storage for single-process applications
        - Development with persistent state
        - Audit trail with human-readable format
        - Git-friendly event logs (text diffs)

    Thread Safety:
        All public methods are protected by a threading.RLock for
        in-process thread safety. File operations use fcntl.flock
        for cross-process safety on POSIX systems.

    Concurrency Model:
        Uses optimistic concurrency - callers provide expected_version,
        and the operation fails if it doesn't match actual version.

    Example:
        >>> store = FileSystemEventStore(Path("/path/to/project"))
        >>> event = StoredEvent(
        ...     stream_id="work_item-WORK-001",
        ...     version=1,
        ...     event_type="WorkItemCreated",
        ...     data={"title": "Test"},
        ... )
        >>> store.append("work_item-WORK-001", [event], expected_version=0)
        >>> store.get_version("work_item-WORK-001")
        1
    """

    def __init__(self, base_path: Path | str) -> None:
        """
        Initialize file system event store.

        Args:
            base_path: Base project path (Path or str). Events stored in
                {base_path}/.jerry/data/events/

        Raises:
            ValueError: If base_path is not a valid path
        """
        if isinstance(base_path, str):
            base_path = Path(base_path)

        self._base_path = base_path
        self._events_dir = base_path / ".jerry" / "data" / "events"
        self._lock = threading.RLock()

        # Create events directory if it doesn't exist
        self._events_dir.mkdir(parents=True, exist_ok=True)

    def _stream_file_path(self, stream_id: str) -> Path:
        """Get the file path for a stream."""
        # Sanitize stream_id to be filesystem-safe
        safe_stream_id = stream_id.replace("/", "_").replace("\\", "_")
        return self._events_dir / f"{safe_stream_id}.jsonl"

    def _read_stream_from_file(self, stream_path: Path) -> list[StoredEvent]:
        """Read all events from a stream file."""
        if not stream_path.exists():
            return []

        events = []
        with open(stream_path, encoding="utf-8") as f:
            # Acquire shared lock for reading
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            try:
                for line in f:
                    line = line.strip()
                    if line:
                        data = json.loads(line)
                        events.append(StoredEvent.from_dict(data))
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

        return events

    def _get_version_from_file(self, stream_path: Path) -> int:
        """Get the current version from a stream file."""
        if not stream_path.exists():
            return -1

        events = self._read_stream_from_file(stream_path)
        if not events:
            return -1

        return events[-1].version

    def append(
        self,
        stream_id: str,
        events: Sequence[StoredEvent],
        expected_version: int,
    ) -> None:
        """
        Append events to a stream with optimistic concurrency.

        Events are atomically appended to the stream file. The operation
        uses file locking to ensure thread and process safety.

        Args:
            stream_id: Unique identifier for the event stream
            events: Sequence of events to append
            expected_version: Expected current version (-1 or 0 for new stream)

        Raises:
            ConcurrencyError: If current version != expected_version
            ValueError: If events is empty or has invalid versions
        """
        if not events:
            raise ValueError("Cannot append empty event sequence")

        with self._lock:
            stream_path = self._stream_file_path(stream_id)
            current_version = self._get_version_from_file(stream_path)

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
                        f"Event stream_id mismatch: expected '{stream_id}', got '{event.stream_id}'"
                    )

            # Append all events to file
            with open(stream_path, "a", encoding="utf-8") as f:
                # Acquire exclusive lock for writing
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                try:
                    for event in events:
                        json_line = json.dumps(event.to_dict(), separators=(",", ":"))
                        f.write(json_line + "\n")
                    # Ensure data is flushed to disk
                    f.flush()
                    os.fsync(f.fileno())
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)

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
            stream_path = self._stream_file_path(stream_id)

            if not stream_path.exists():
                raise StreamNotFoundError(stream_id)

            events = self._read_stream_from_file(stream_path)

            if not events:
                raise StreamNotFoundError(stream_id)

            # Filter by version range
            result = [
                e
                for e in events
                if e.version >= from_version and (to_version is None or e.version <= to_version)
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
            stream_path = self._stream_file_path(stream_id)
            return self._get_version_from_file(stream_path)

    def stream_exists(self, stream_id: str) -> bool:
        """
        Check if a stream exists.

        Args:
            stream_id: Stream to check

        Returns:
            True if stream has at least one event
        """
        with self._lock:
            stream_path = self._stream_file_path(stream_id)
            if not stream_path.exists():
                return False
            events = self._read_stream_from_file(stream_path)
            return len(events) > 0

    def delete_stream(self, stream_id: str) -> bool:
        """
        Delete all events in a stream.

        This removes the stream file from disk.

        Args:
            stream_id: Stream to delete

        Returns:
            True if stream was deleted, False if it didn't exist
        """
        with self._lock:
            stream_path = self._stream_file_path(stream_id)

            if not stream_path.exists():
                return False

            # Check if file has events before deleting
            events = self._read_stream_from_file(stream_path)
            if not events:
                # Empty file, remove it
                stream_path.unlink(missing_ok=True)
                return False

            # Delete the file
            stream_path.unlink()
            return True

    def clear(self) -> None:
        """
        Clear all streams (for testing).

        Removes all event files from the events directory.
        """
        with self._lock:
            for stream_file in self._events_dir.glob("*.jsonl"):
                stream_file.unlink()

    def get_all_stream_ids(self) -> list[str]:
        """
        Get all stream IDs in the store.

        Returns:
            List of stream IDs that have at least one event
        """
        with self._lock:
            stream_ids = []
            for stream_file in self._events_dir.glob("*.jsonl"):
                # Convert filename back to stream_id
                stream_id = stream_file.stem  # Remove .jsonl extension
                events = self._read_stream_from_file(stream_file)
                if events:
                    stream_ids.append(stream_id)
            return stream_ids

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
                stream_path = self._stream_file_path(stream_id)
                events = self._read_stream_from_file(stream_path)
                return len(events)

            total = 0
            for stream_file in self._events_dir.glob("*.jsonl"):
                events = self._read_stream_from_file(stream_file)
                total += len(events)
            return total

    @property
    def events_directory(self) -> Path:
        """Get the events directory path (for testing/debugging)."""
        return self._events_dir


# Type assertion for protocol compliance
def _assert_protocol_compliance() -> None:
    """Static assertion that FileSystemEventStore implements IEventStore."""
    store: IEventStore = FileSystemEventStore(Path("/tmp"))
    _ = store  # Suppress unused variable warning
