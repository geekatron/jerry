# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for work_tracking.infrastructure.persistence.filesystem_event_store.

Test Categories:
    - Happy Path: Normal append/read operations
    - Edge Cases: Empty streams, version boundaries
    - Negative Cases: Concurrency errors, validation failures
    - Thread Safety: Concurrent access patterns
    - Persistence: Events survive store recreation (key difference from InMemory)
    - Protocol Compliance: IEventStore contract verification

References:
    - PAT-001: Event Store Interface Pattern
    - PAT-003: Optimistic Concurrency with File Locking
    - DISC-019: InMemoryEventStore Not Persistent - Events Lost on Restart
    - TD-018: Event Sourcing for Work Item Repository
"""

from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pytest

from src.work_tracking.domain.ports.event_store import (
    ConcurrencyError,
    StoredEvent,
    StreamNotFoundError,
)
from src.work_tracking.infrastructure.persistence.filesystem_event_store import (
    FileSystemEventStore,
)


def create_event(stream_id: str, version: int, event_type: str = "Test") -> StoredEvent:
    """Helper to create a StoredEvent for testing."""
    return StoredEvent(
        stream_id=stream_id,
        version=version,
        event_type=event_type,
        data={"version": version},
    )


@pytest.fixture
def temp_store_path(tmp_path: Path) -> Path:
    """Create a temporary directory for the event store."""
    return tmp_path / "test_project"


@pytest.fixture
def store(temp_store_path: Path) -> FileSystemEventStore:
    """Create a FileSystemEventStore for testing."""
    return FileSystemEventStore(temp_store_path)


class TestFileSystemEventStoreAppend:
    """Tests for FileSystemEventStore.append()."""

    def test_append_to_new_stream(self, store: FileSystemEventStore) -> None:
        """Can append events to a new stream."""
        event = create_event("WORK-001", version=1)

        store.append("WORK-001", [event], expected_version=-1)

        assert store.get_version("WORK-001") == 1

    def test_append_with_zero_expected_for_new_stream(self, store: FileSystemEventStore) -> None:
        """Can use expected_version=0 for new streams."""
        event = create_event("WORK-001", version=1)

        store.append("WORK-001", [event], expected_version=0)

        assert store.get_version("WORK-001") == 1

    def test_append_multiple_events(self, store: FileSystemEventStore) -> None:
        """Can append multiple events at once."""
        events = [
            create_event("WORK-001", version=1),
            create_event("WORK-001", version=2),
            create_event("WORK-001", version=3),
        ]

        store.append("WORK-001", events, expected_version=-1)

        assert store.get_version("WORK-001") == 3
        assert store.count_events("WORK-001") == 3

    def test_append_to_existing_stream(self, store: FileSystemEventStore) -> None:
        """Can append to an existing stream with correct expected_version."""
        event1 = create_event("WORK-001", version=1)
        store.append("WORK-001", [event1], expected_version=-1)

        event2 = create_event("WORK-001", version=2)
        store.append("WORK-001", [event2], expected_version=1)

        assert store.get_version("WORK-001") == 2

    def test_append_raises_on_wrong_expected_version(self, store: FileSystemEventStore) -> None:
        """append raises ConcurrencyError on version mismatch."""
        event1 = create_event("WORK-001", version=1)
        store.append("WORK-001", [event1], expected_version=-1)

        event2 = create_event("WORK-001", version=2)
        with pytest.raises(ConcurrencyError) as exc_info:
            store.append("WORK-001", [event2], expected_version=0)  # Wrong!

        assert exc_info.value.stream_id == "WORK-001"
        assert exc_info.value.expected_version == 0
        assert exc_info.value.actual_version == 1

    def test_append_empty_sequence_raises(self, store: FileSystemEventStore) -> None:
        """append raises ValueError for empty event sequence."""
        with pytest.raises(ValueError, match="empty"):
            store.append("WORK-001", [], expected_version=-1)

    def test_append_wrong_event_version_raises(self, store: FileSystemEventStore) -> None:
        """append raises ValueError if event versions are not sequential."""
        events = [
            create_event("WORK-001", version=1),
            create_event("WORK-001", version=3),  # Skipped 2!
        ]

        with pytest.raises(ValueError, match="version mismatch"):
            store.append("WORK-001", events, expected_version=-1)

    def test_append_wrong_stream_id_in_event_raises(self, store: FileSystemEventStore) -> None:
        """append raises ValueError if event stream_id doesn't match."""
        event = create_event("WORK-002", version=1)  # Wrong stream_id

        with pytest.raises(ValueError, match="stream_id mismatch"):
            store.append("WORK-001", [event], expected_version=-1)


class TestFileSystemEventStoreRead:
    """Tests for FileSystemEventStore.read()."""

    def test_read_all_events(self, store: FileSystemEventStore) -> None:
        """read returns all events in order."""
        events = [create_event("WORK-001", version=i) for i in range(1, 6)]
        store.append("WORK-001", events, expected_version=-1)

        result = store.read("WORK-001")

        assert len(result) == 5
        assert [e.version for e in result] == [1, 2, 3, 4, 5]

    def test_read_from_version(self, store: FileSystemEventStore) -> None:
        """read with from_version filters correctly."""
        events = [create_event("WORK-001", version=i) for i in range(1, 11)]
        store.append("WORK-001", events, expected_version=-1)

        result = store.read("WORK-001", from_version=5)

        assert len(result) == 6
        assert [e.version for e in result] == [5, 6, 7, 8, 9, 10]

    def test_read_version_range(self, store: FileSystemEventStore) -> None:
        """read with from_version and to_version filters correctly."""
        events = [create_event("WORK-001", version=i) for i in range(1, 11)]
        store.append("WORK-001", events, expected_version=-1)

        result = store.read("WORK-001", from_version=3, to_version=7)

        assert len(result) == 5
        assert [e.version for e in result] == [3, 4, 5, 6, 7]

    def test_read_nonexistent_stream_raises(self, store: FileSystemEventStore) -> None:
        """read raises StreamNotFoundError for non-existent stream."""
        with pytest.raises(StreamNotFoundError) as exc_info:
            store.read("NONEXISTENT")

        assert exc_info.value.stream_id == "NONEXISTENT"

    def test_read_preserves_event_data(self, store: FileSystemEventStore) -> None:
        """read returns events with all original data intact."""
        event = StoredEvent(
            stream_id="WORK-001",
            version=1,
            event_type="ComplexEvent",
            data={"nested": {"key": "value"}, "list": [1, 2, 3]},
        )
        store.append("WORK-001", [event], expected_version=-1)

        result = store.read("WORK-001")

        assert result[0].data == {"nested": {"key": "value"}, "list": [1, 2, 3]}
        assert result[0].event_type == "ComplexEvent"


class TestFileSystemEventStoreGetVersion:
    """Tests for FileSystemEventStore.get_version()."""

    def test_returns_minus_one_for_nonexistent_stream(self, store: FileSystemEventStore) -> None:
        """get_version returns -1 for non-existent stream."""
        assert store.get_version("NONEXISTENT") == -1

    def test_returns_correct_version(self, store: FileSystemEventStore) -> None:
        """get_version returns highest event version."""
        events = [create_event("WORK-001", version=i) for i in range(1, 8)]
        store.append("WORK-001", events, expected_version=-1)

        assert store.get_version("WORK-001") == 7

    def test_updates_after_append(self, store: FileSystemEventStore) -> None:
        """get_version updates after each append."""
        assert store.get_version("WORK-001") == -1

        store.append("WORK-001", [create_event("WORK-001", 1)], expected_version=-1)
        assert store.get_version("WORK-001") == 1

        store.append("WORK-001", [create_event("WORK-001", 2)], expected_version=1)
        assert store.get_version("WORK-001") == 2


class TestFileSystemEventStoreStreamExists:
    """Tests for FileSystemEventStore.stream_exists()."""

    def test_returns_false_for_nonexistent(self, store: FileSystemEventStore) -> None:
        """stream_exists returns False for non-existent stream."""
        assert store.stream_exists("NONEXISTENT") is False

    def test_returns_true_for_existing(self, store: FileSystemEventStore) -> None:
        """stream_exists returns True after events are appended."""
        store.append("WORK-001", [create_event("WORK-001", 1)], expected_version=-1)

        assert store.stream_exists("WORK-001") is True


class TestFileSystemEventStoreDeleteStream:
    """Tests for FileSystemEventStore.delete_stream()."""

    def test_delete_existing_stream(self, store: FileSystemEventStore) -> None:
        """delete_stream removes all events and returns True."""
        store.append("WORK-001", [create_event("WORK-001", 1)], expected_version=-1)

        result = store.delete_stream("WORK-001")

        assert result is True
        assert store.stream_exists("WORK-001") is False
        assert store.get_version("WORK-001") == -1

    def test_delete_nonexistent_stream(self, store: FileSystemEventStore) -> None:
        """delete_stream returns False for non-existent stream."""
        result = store.delete_stream("NONEXISTENT")

        assert result is False


class TestFileSystemEventStoreUtilityMethods:
    """Tests for utility methods."""

    def test_clear(self, store: FileSystemEventStore) -> None:
        """clear removes all streams."""
        store.append("WORK-001", [create_event("WORK-001", 1)], expected_version=-1)
        store.append("WORK-002", [create_event("WORK-002", 1)], expected_version=-1)

        store.clear()

        assert store.count_events() == 0
        assert store.get_all_stream_ids() == []

    def test_get_all_stream_ids(self, store: FileSystemEventStore) -> None:
        """get_all_stream_ids returns all streams with events."""
        store.append("WORK-001", [create_event("WORK-001", 1)], expected_version=-1)
        store.append("WORK-002", [create_event("WORK-002", 1)], expected_version=-1)
        store.append("WORK-003", [create_event("WORK-003", 1)], expected_version=-1)

        stream_ids = store.get_all_stream_ids()

        assert set(stream_ids) == {"WORK-001", "WORK-002", "WORK-003"}

    def test_count_events_specific_stream(self, store: FileSystemEventStore) -> None:
        """count_events returns count for specific stream."""
        events = [create_event("WORK-001", i) for i in range(1, 6)]
        store.append("WORK-001", events, expected_version=-1)

        assert store.count_events("WORK-001") == 5

    def test_count_events_all_streams(self, store: FileSystemEventStore) -> None:
        """count_events without argument returns total count."""
        store.append(
            "WORK-001", [create_event("WORK-001", i) for i in range(1, 4)], expected_version=-1
        )
        store.append(
            "WORK-002", [create_event("WORK-002", i) for i in range(1, 3)], expected_version=-1
        )

        assert store.count_events() == 5  # 3 + 2

    def test_events_directory_property(self, temp_store_path: Path) -> None:
        """events_directory returns correct path."""
        store = FileSystemEventStore(temp_store_path)

        expected = temp_store_path / ".jerry" / "data" / "events"
        assert store.events_directory == expected


class TestFileSystemEventStorePersistence:
    """Tests for persistence across store recreations (simulating restarts).

    This is the KEY difference from InMemoryEventStore - events survive
    when the store is destroyed and recreated.
    """

    def test_events_persist_after_store_recreation(self, temp_store_path: Path) -> None:
        """Events survive store destruction and recreation (Task 1.2.4)."""
        # First store instance - write events
        store1 = FileSystemEventStore(temp_store_path)
        events = [create_event("WORK-001", version=i) for i in range(1, 4)]
        store1.append("WORK-001", events, expected_version=-1)

        # Verify events exist in first store
        assert store1.get_version("WORK-001") == 3
        del store1  # Destroy first store

        # Second store instance - events should still exist (simulates restart)
        store2 = FileSystemEventStore(temp_store_path)
        assert store2.get_version("WORK-001") == 3
        assert store2.stream_exists("WORK-001") is True

        result = store2.read("WORK-001")
        assert len(result) == 3
        assert [e.version for e in result] == [1, 2, 3]

    def test_can_append_after_store_recreation(self, temp_store_path: Path) -> None:
        """Can append more events after store recreation."""
        # First store - write initial events
        store1 = FileSystemEventStore(temp_store_path)
        store1.append("WORK-001", [create_event("WORK-001", 1)], expected_version=-1)
        del store1

        # Second store - append more events
        store2 = FileSystemEventStore(temp_store_path)
        store2.append("WORK-001", [create_event("WORK-001", 2)], expected_version=1)

        assert store2.get_version("WORK-001") == 2

    def test_multiple_streams_persist(self, temp_store_path: Path) -> None:
        """Multiple streams all persist correctly."""
        # Create and populate multiple streams
        store1 = FileSystemEventStore(temp_store_path)
        store1.append("WORK-001", [create_event("WORK-001", 1)], expected_version=-1)
        store1.append("WORK-002", [create_event("WORK-002", 1)], expected_version=-1)
        store1.append("WORK-003", [create_event("WORK-003", 1)], expected_version=-1)
        del store1

        # Verify all streams exist in new store
        store2 = FileSystemEventStore(temp_store_path)
        assert set(store2.get_all_stream_ids()) == {"WORK-001", "WORK-002", "WORK-003"}

    def test_concurrency_error_after_recreation(self, temp_store_path: Path) -> None:
        """ConcurrencyError still works correctly after recreation."""
        # First store - create stream with version 1
        store1 = FileSystemEventStore(temp_store_path)
        store1.append("WORK-001", [create_event("WORK-001", 1)], expected_version=-1)
        del store1

        # Second store - wrong expected version should fail
        store2 = FileSystemEventStore(temp_store_path)
        with pytest.raises(ConcurrencyError) as exc_info:
            store2.append("WORK-001", [create_event("WORK-001", 2)], expected_version=0)

        assert exc_info.value.expected_version == 0
        assert exc_info.value.actual_version == 1

    def test_jsonl_format_human_readable(self, temp_store_path: Path) -> None:
        """Verify stored files are human-readable JSON Lines."""
        store = FileSystemEventStore(temp_store_path)
        event = StoredEvent(
            stream_id="WORK-001",
            version=1,
            event_type="TestEvent",
            data={"key": "value"},
        )
        store.append("WORK-001", [event], expected_version=-1)

        # Read raw file content
        jsonl_file = store.events_directory / "WORK-001.jsonl"
        assert jsonl_file.exists()

        content = jsonl_file.read_text()
        assert "TestEvent" in content
        assert '"key":"value"' in content or '"key": "value"' in content


class TestFileSystemEventStoreThreadSafety:
    """Tests for thread safety."""

    def test_concurrent_reads_are_safe(self, store: FileSystemEventStore) -> None:
        """Multiple threads can read simultaneously."""
        events = [create_event("WORK-001", i) for i in range(1, 101)]
        store.append("WORK-001", events, expected_version=-1)

        results: list[int] = []
        errors: list[Exception] = []

        def read_events() -> None:
            try:
                result = store.read("WORK-001")
                results.append(len(result))
            except Exception as e:
                errors.append(e)

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(read_events) for _ in range(50)]
            for future in as_completed(futures):
                future.result()

        assert len(errors) == 0
        assert all(r == 100 for r in results)

    def test_concurrent_writes_to_different_streams(self, store: FileSystemEventStore) -> None:
        """Concurrent writes to different streams succeed."""
        errors: list[Exception] = []

        def write_to_stream(stream_id: str) -> None:
            try:
                events = [create_event(stream_id, i) for i in range(1, 11)]
                store.append(stream_id, events, expected_version=-1)
            except Exception as e:
                errors.append(e)

        with ThreadPoolExecutor(max_workers=10) as executor:
            stream_ids = [f"WORK-{i:03d}" for i in range(20)]
            futures = [executor.submit(write_to_stream, sid) for sid in stream_ids]
            for future in as_completed(futures):
                future.result()

        assert len(errors) == 0
        assert len(store.get_all_stream_ids()) == 20

    def test_concurrent_writes_to_same_stream_some_fail(self, store: FileSystemEventStore) -> None:
        """Concurrent writes to same stream: one wins, others fail."""
        successes: list[bool] = []
        failures: list[bool] = []

        def try_append() -> None:
            try:
                event = create_event("WORK-001", 1)
                store.append("WORK-001", [event], expected_version=-1)
                successes.append(True)
            except ConcurrencyError:
                failures.append(True)

        threads = [threading.Thread(target=try_append) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Exactly one should succeed
        assert len(successes) == 1
        assert len(failures) == 9
        assert store.get_version("WORK-001") == 1


class TestFileSystemEventStoreEdgeCases:
    """Edge case tests."""

    def test_empty_data_dict(self, store: FileSystemEventStore) -> None:
        """Events with empty data dict are accepted."""
        event = StoredEvent(
            stream_id="WORK-001",
            version=1,
            event_type="EmptyEvent",
            data={},
        )

        store.append("WORK-001", [event], expected_version=-1)

        result = store.read("WORK-001")
        assert result[0].data == {}

    def test_large_event_data(self, store: FileSystemEventStore) -> None:
        """Large event data is handled correctly."""
        large_data = {"items": list(range(10000))}
        event = StoredEvent(
            stream_id="WORK-001",
            version=1,
            event_type="LargeEvent",
            data=large_data,
        )

        store.append("WORK-001", [event], expected_version=-1)

        result = store.read("WORK-001")
        assert result[0].data == large_data

    def test_special_characters_in_stream_id_sanitized(self, store: FileSystemEventStore) -> None:
        """Stream IDs with slashes are sanitized to underscores for filesystem."""
        stream_id = "namespace/project:entity-123"
        event = create_event(stream_id, 1)

        store.append(stream_id, [event], expected_version=-1)

        assert store.stream_exists(stream_id)
        assert store.get_version(stream_id) == 1

        # Verify file uses sanitized name
        expected_file = store.events_directory / "namespace_project:entity-123.jsonl"
        assert expected_file.exists()

    def test_many_streams(self, store: FileSystemEventStore) -> None:
        """Store handles many streams correctly."""
        for i in range(100):
            stream_id = f"WORK-{i:03d}"
            event = create_event(stream_id, 1)
            store.append(stream_id, [event], expected_version=-1)

        assert len(store.get_all_stream_ids()) == 100
        assert store.count_events() == 100

    def test_many_events_in_stream(self, store: FileSystemEventStore) -> None:
        """Store handles many events in one stream."""
        events = [create_event("WORK-001", i) for i in range(1, 1001)]

        store.append("WORK-001", events, expected_version=-1)

        assert store.get_version("WORK-001") == 1000
        assert store.count_events("WORK-001") == 1000

    def test_string_path_accepted(self, temp_store_path: Path) -> None:
        """Store accepts string path as well as Path object."""
        store = FileSystemEventStore(str(temp_store_path))
        event = create_event("WORK-001", 1)

        store.append("WORK-001", [event], expected_version=-1)

        assert store.get_version("WORK-001") == 1


class TestFileSystemEventStoreProtocolCompliance:
    """Tests that FileSystemEventStore complies with IEventStore protocol."""

    def test_has_append_method(self, store: FileSystemEventStore) -> None:
        """FileSystemEventStore has append method."""
        assert callable(store.append)

    def test_has_read_method(self, store: FileSystemEventStore) -> None:
        """FileSystemEventStore has read method."""
        assert callable(store.read)

    def test_has_get_version_method(self, store: FileSystemEventStore) -> None:
        """FileSystemEventStore has get_version method."""
        assert callable(store.get_version)

    def test_has_stream_exists_method(self, store: FileSystemEventStore) -> None:
        """FileSystemEventStore has stream_exists method."""
        assert callable(store.stream_exists)

    def test_has_delete_stream_method(self, store: FileSystemEventStore) -> None:
        """FileSystemEventStore has delete_stream method."""
        assert callable(store.delete_stream)


class TestFileSystemEventStoreIsolation:
    """Tests for stream isolation (Task 1.2.3)."""

    def test_streams_are_isolated(self, store: FileSystemEventStore) -> None:
        """Operations on one stream don't affect others."""
        # Create two streams
        store.append("WORK-001", [create_event("WORK-001", 1)], expected_version=-1)
        store.append("WORK-002", [create_event("WORK-002", 1)], expected_version=-1)

        # Modify first stream
        store.append("WORK-001", [create_event("WORK-001", 2)], expected_version=1)

        # Second stream should be unchanged
        assert store.get_version("WORK-002") == 1
        assert len(store.read("WORK-002")) == 1

    def test_delete_stream_doesnt_affect_others(self, store: FileSystemEventStore) -> None:
        """Deleting one stream doesn't affect others."""
        store.append("WORK-001", [create_event("WORK-001", 1)], expected_version=-1)
        store.append("WORK-002", [create_event("WORK-002", 1)], expected_version=-1)

        store.delete_stream("WORK-001")

        assert store.stream_exists("WORK-002") is True
        assert store.get_version("WORK-002") == 1

    def test_stream_files_are_separate(
        self, store: FileSystemEventStore, temp_store_path: Path
    ) -> None:
        """Each stream has its own file."""
        store.append("WORK-001", [create_event("WORK-001", 1)], expected_version=-1)
        store.append("WORK-002", [create_event("WORK-002", 1)], expected_version=-1)

        events_dir = temp_store_path / ".jerry" / "data" / "events"
        files = list(events_dir.glob("*.jsonl"))

        assert len(files) == 2
        assert {f.name for f in files} == {"WORK-001.jsonl", "WORK-002.jsonl"}
