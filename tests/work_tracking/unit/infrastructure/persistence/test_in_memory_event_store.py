# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for work_tracking.infrastructure.persistence.in_memory_event_store.

Test Categories:
    - Happy Path: Normal append/read operations
    - Edge Cases: Empty streams, version boundaries
    - Negative Cases: Concurrency errors, validation failures
    - Thread Safety: Concurrent access patterns
    - Protocol Compliance: IEventStore contract verification

References:
    - PAT-001: Event Store Interface Pattern
    - PAT-003: Optimistic Concurrency with File Locking
    - IMPL-ES-001: IEventStore Port implementation
"""

from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest

from src.work_tracking.domain.ports.event_store import (
    ConcurrencyError,
    StoredEvent,
    StreamNotFoundError,
)
from src.work_tracking.infrastructure.persistence.in_memory_event_store import (
    InMemoryEventStore,
)


def create_event(stream_id: str, version: int, event_type: str = "Test") -> StoredEvent:
    """Helper to create a StoredEvent for testing."""
    return StoredEvent(
        stream_id=stream_id,
        version=version,
        event_type=event_type,
        data={"version": version},
    )


class TestInMemoryEventStoreAppend:
    """Tests for InMemoryEventStore.append()."""

    def test_append_to_new_stream(self) -> None:
        """Can append events to a new stream."""
        store = InMemoryEventStore()
        event = create_event("WORK-001", version=1)

        store.append("WORK-001", [event], expected_version=-1)

        assert store.get_version("WORK-001") == 1

    def test_append_with_zero_expected_for_new_stream(self) -> None:
        """Can use expected_version=0 for new streams."""
        store = InMemoryEventStore()
        event = create_event("WORK-001", version=1)

        store.append("WORK-001", [event], expected_version=0)

        assert store.get_version("WORK-001") == 1

    def test_append_multiple_events(self) -> None:
        """Can append multiple events at once."""
        store = InMemoryEventStore()
        events = [
            create_event("WORK-001", version=1),
            create_event("WORK-001", version=2),
            create_event("WORK-001", version=3),
        ]

        store.append("WORK-001", events, expected_version=-1)

        assert store.get_version("WORK-001") == 3
        assert store.count_events("WORK-001") == 3

    def test_append_to_existing_stream(self) -> None:
        """Can append to an existing stream with correct expected_version."""
        store = InMemoryEventStore()
        event1 = create_event("WORK-001", version=1)
        store.append("WORK-001", [event1], expected_version=-1)

        event2 = create_event("WORK-001", version=2)
        store.append("WORK-001", [event2], expected_version=1)

        assert store.get_version("WORK-001") == 2

    def test_append_raises_on_wrong_expected_version(self) -> None:
        """append raises ConcurrencyError on version mismatch."""
        store = InMemoryEventStore()
        event1 = create_event("WORK-001", version=1)
        store.append("WORK-001", [event1], expected_version=-1)

        event2 = create_event("WORK-001", version=2)
        with pytest.raises(ConcurrencyError) as exc_info:
            store.append("WORK-001", [event2], expected_version=0)  # Wrong!

        assert exc_info.value.stream_id == "WORK-001"
        assert exc_info.value.expected_version == 0
        assert exc_info.value.actual_version == 1

    def test_append_empty_sequence_raises(self) -> None:
        """append raises ValueError for empty event sequence."""
        store = InMemoryEventStore()

        with pytest.raises(ValueError, match="empty"):
            store.append("WORK-001", [], expected_version=-1)

    def test_append_wrong_event_version_raises(self) -> None:
        """append raises ValueError if event versions are not sequential."""
        store = InMemoryEventStore()
        events = [
            create_event("WORK-001", version=1),
            create_event("WORK-001", version=3),  # Skipped 2!
        ]

        with pytest.raises(ValueError, match="version mismatch"):
            store.append("WORK-001", events, expected_version=-1)

    def test_append_wrong_stream_id_in_event_raises(self) -> None:
        """append raises ValueError if event stream_id doesn't match."""
        store = InMemoryEventStore()
        event = create_event("WORK-002", version=1)  # Wrong stream_id

        with pytest.raises(ValueError, match="stream_id mismatch"):
            store.append("WORK-001", [event], expected_version=-1)


class TestInMemoryEventStoreRead:
    """Tests for InMemoryEventStore.read()."""

    def test_read_all_events(self) -> None:
        """read returns all events in order."""
        store = InMemoryEventStore()
        events = [create_event("WORK-001", version=i) for i in range(1, 6)]
        store.append("WORK-001", events, expected_version=-1)

        result = store.read("WORK-001")

        assert len(result) == 5
        assert [e.version for e in result] == [1, 2, 3, 4, 5]

    def test_read_from_version(self) -> None:
        """read with from_version filters correctly."""
        store = InMemoryEventStore()
        events = [create_event("WORK-001", version=i) for i in range(1, 11)]
        store.append("WORK-001", events, expected_version=-1)

        result = store.read("WORK-001", from_version=5)

        assert len(result) == 6
        assert [e.version for e in result] == [5, 6, 7, 8, 9, 10]

    def test_read_version_range(self) -> None:
        """read with from_version and to_version filters correctly."""
        store = InMemoryEventStore()
        events = [create_event("WORK-001", version=i) for i in range(1, 11)]
        store.append("WORK-001", events, expected_version=-1)

        result = store.read("WORK-001", from_version=3, to_version=7)

        assert len(result) == 5
        assert [e.version for e in result] == [3, 4, 5, 6, 7]

    def test_read_nonexistent_stream_raises(self) -> None:
        """read raises StreamNotFoundError for non-existent stream."""
        store = InMemoryEventStore()

        with pytest.raises(StreamNotFoundError) as exc_info:
            store.read("NONEXISTENT")

        assert exc_info.value.stream_id == "NONEXISTENT"

    def test_read_preserves_event_data(self) -> None:
        """read returns events with all original data intact."""
        store = InMemoryEventStore()
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


class TestInMemoryEventStoreGetVersion:
    """Tests for InMemoryEventStore.get_version()."""

    def test_returns_minus_one_for_nonexistent_stream(self) -> None:
        """get_version returns -1 for non-existent stream."""
        store = InMemoryEventStore()

        assert store.get_version("NONEXISTENT") == -1

    def test_returns_correct_version(self) -> None:
        """get_version returns highest event version."""
        store = InMemoryEventStore()
        events = [create_event("WORK-001", version=i) for i in range(1, 8)]
        store.append("WORK-001", events, expected_version=-1)

        assert store.get_version("WORK-001") == 7

    def test_updates_after_append(self) -> None:
        """get_version updates after each append."""
        store = InMemoryEventStore()

        assert store.get_version("WORK-001") == -1

        store.append("WORK-001", [create_event("WORK-001", 1)], expected_version=-1)
        assert store.get_version("WORK-001") == 1

        store.append("WORK-001", [create_event("WORK-001", 2)], expected_version=1)
        assert store.get_version("WORK-001") == 2


class TestInMemoryEventStoreStreamExists:
    """Tests for InMemoryEventStore.stream_exists()."""

    def test_returns_false_for_nonexistent(self) -> None:
        """stream_exists returns False for non-existent stream."""
        store = InMemoryEventStore()

        assert store.stream_exists("NONEXISTENT") is False

    def test_returns_true_for_existing(self) -> None:
        """stream_exists returns True after events are appended."""
        store = InMemoryEventStore()
        store.append("WORK-001", [create_event("WORK-001", 1)], expected_version=-1)

        assert store.stream_exists("WORK-001") is True


class TestInMemoryEventStoreDeleteStream:
    """Tests for InMemoryEventStore.delete_stream()."""

    def test_delete_existing_stream(self) -> None:
        """delete_stream removes all events and returns True."""
        store = InMemoryEventStore()
        store.append("WORK-001", [create_event("WORK-001", 1)], expected_version=-1)

        result = store.delete_stream("WORK-001")

        assert result is True
        assert store.stream_exists("WORK-001") is False
        assert store.get_version("WORK-001") == -1

    def test_delete_nonexistent_stream(self) -> None:
        """delete_stream returns False for non-existent stream."""
        store = InMemoryEventStore()

        result = store.delete_stream("NONEXISTENT")

        assert result is False


class TestInMemoryEventStoreUtilityMethods:
    """Tests for utility methods."""

    def test_clear(self) -> None:
        """clear removes all streams."""
        store = InMemoryEventStore()
        store.append("WORK-001", [create_event("WORK-001", 1)], expected_version=-1)
        store.append("WORK-002", [create_event("WORK-002", 1)], expected_version=-1)

        store.clear()

        assert store.count_events() == 0
        assert store.get_all_stream_ids() == []

    def test_get_all_stream_ids(self) -> None:
        """get_all_stream_ids returns all streams with events."""
        store = InMemoryEventStore()
        store.append("WORK-001", [create_event("WORK-001", 1)], expected_version=-1)
        store.append("WORK-002", [create_event("WORK-002", 1)], expected_version=-1)
        store.append("WORK-003", [create_event("WORK-003", 1)], expected_version=-1)

        stream_ids = store.get_all_stream_ids()

        assert set(stream_ids) == {"WORK-001", "WORK-002", "WORK-003"}

    def test_count_events_specific_stream(self) -> None:
        """count_events returns count for specific stream."""
        store = InMemoryEventStore()
        events = [create_event("WORK-001", i) for i in range(1, 6)]
        store.append("WORK-001", events, expected_version=-1)

        assert store.count_events("WORK-001") == 5

    def test_count_events_all_streams(self) -> None:
        """count_events without argument returns total count."""
        store = InMemoryEventStore()
        store.append(
            "WORK-001", [create_event("WORK-001", i) for i in range(1, 4)], expected_version=-1
        )
        store.append(
            "WORK-002", [create_event("WORK-002", i) for i in range(1, 3)], expected_version=-1
        )

        assert store.count_events() == 5  # 3 + 2


class TestInMemoryEventStoreThreadSafety:
    """Tests for thread safety."""

    def test_concurrent_reads_are_safe(self) -> None:
        """Multiple threads can read simultaneously."""
        store = InMemoryEventStore()
        events = [create_event("WORK-001", i) for i in range(1, 101)]
        store.append("WORK-001", events, expected_version=-1)

        results = []
        errors = []

        def read_events():
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

    def test_concurrent_writes_to_different_streams(self) -> None:
        """Concurrent writes to different streams succeed."""
        store = InMemoryEventStore()
        errors = []

        def write_to_stream(stream_id: str):
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

    def test_concurrent_writes_to_same_stream_some_fail(self) -> None:
        """Concurrent writes to same stream: one wins, others fail."""
        store = InMemoryEventStore()
        successes = []
        failures = []

        def try_append():
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


class TestInMemoryEventStoreEdgeCases:
    """Edge case tests."""

    def test_empty_data_dict(self) -> None:
        """Events with empty data dict are accepted."""
        store = InMemoryEventStore()
        event = StoredEvent(
            stream_id="WORK-001",
            version=1,
            event_type="EmptyEvent",
            data={},
        )

        store.append("WORK-001", [event], expected_version=-1)

        result = store.read("WORK-001")
        assert result[0].data == {}

    def test_large_event_data(self) -> None:
        """Large event data is handled correctly."""
        store = InMemoryEventStore()
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

    def test_special_characters_in_stream_id(self) -> None:
        """Stream IDs with special characters work."""
        store = InMemoryEventStore()
        stream_id = "namespace/project:entity-123"
        event = create_event(stream_id, 1)

        store.append(stream_id, [event], expected_version=-1)

        assert store.stream_exists(stream_id)
        assert store.get_version(stream_id) == 1

    def test_many_streams(self) -> None:
        """Store handles many streams correctly."""
        store = InMemoryEventStore()

        for i in range(100):
            stream_id = f"WORK-{i:03d}"
            event = create_event(stream_id, 1)
            store.append(stream_id, [event], expected_version=-1)

        assert len(store.get_all_stream_ids()) == 100
        assert store.count_events() == 100

    def test_many_events_in_stream(self) -> None:
        """Store handles many events in one stream."""
        store = InMemoryEventStore()
        events = [create_event("WORK-001", i) for i in range(1, 1001)]

        store.append("WORK-001", events, expected_version=-1)

        assert store.get_version("WORK-001") == 1000
        assert store.count_events("WORK-001") == 1000


class TestInMemoryEventStoreProtocolCompliance:
    """Tests that InMemoryEventStore complies with IEventStore protocol."""

    def test_has_append_method(self) -> None:
        """InMemoryEventStore has append method."""
        store = InMemoryEventStore()
        assert callable(store.append)

    def test_has_read_method(self) -> None:
        """InMemoryEventStore has read method."""
        store = InMemoryEventStore()
        assert callable(store.read)

    def test_has_get_version_method(self) -> None:
        """InMemoryEventStore has get_version method."""
        store = InMemoryEventStore()
        assert callable(store.get_version)

    def test_has_stream_exists_method(self) -> None:
        """InMemoryEventStore has stream_exists method."""
        store = InMemoryEventStore()
        assert callable(store.stream_exists)

    def test_has_delete_stream_method(self) -> None:
        """InMemoryEventStore has delete_stream method."""
        store = InMemoryEventStore()
        assert callable(store.delete_stream)
