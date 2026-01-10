"""Unit tests for work_tracking.domain.ports.event_store module.

Test Categories:
    - Happy Path: Normal StoredEvent creation and serialization
    - Edge Cases: Boundary conditions
    - Negative Cases: Validation errors
    - Exception Tests: ConcurrencyError, StreamNotFoundError

References:
    - PAT-001: Event Store Interface Pattern
    - IMPL-ES-001: IEventStore Port implementation
"""
from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest

from src.work_tracking.domain.ports.event_store import (
    ConcurrencyError,
    EventStoreError,
    StoredEvent,
    StreamNotFoundError,
)


class TestStoredEventCreation:
    """Tests for StoredEvent initialization."""

    def test_create_with_required_fields(self) -> None:
        """StoredEvent can be created with required fields."""
        event = StoredEvent(
            stream_id="WORK-001",
            version=1,
            event_type="WorkItemCreated",
            data={"title": "Test"},
        )
        assert event.stream_id == "WORK-001"
        assert event.version == 1
        assert event.event_type == "WorkItemCreated"
        assert event.data == {"title": "Test"}

    def test_create_with_all_fields(self) -> None:
        """StoredEvent can be created with all fields."""
        timestamp = datetime(2025, 1, 15, 10, 30, 0, tzinfo=timezone.utc)
        event_id = uuid4()

        event = StoredEvent(
            stream_id="WORK-002",
            version=5,
            event_type="WorkItemCompleted",
            data={"status": "done"},
            timestamp=timestamp,
            event_id=event_id,
        )
        assert event.timestamp == timestamp
        assert event.event_id == event_id

    def test_auto_generates_timestamp(self) -> None:
        """StoredEvent auto-generates timestamp if not provided."""
        before = datetime.now(timezone.utc)
        event = StoredEvent(
            stream_id="WORK-001",
            version=1,
            event_type="Test",
            data={},
        )
        after = datetime.now(timezone.utc)

        assert before <= event.timestamp <= after

    def test_auto_generates_event_id(self) -> None:
        """StoredEvent auto-generates event_id if not provided."""
        event = StoredEvent(
            stream_id="WORK-001",
            version=1,
            event_type="Test",
            data={},
        )
        assert isinstance(event.event_id, UUID)

    def test_event_ids_are_unique(self) -> None:
        """Each StoredEvent gets a unique event_id."""
        events = [
            StoredEvent(stream_id="WORK-001", version=i, event_type="Test", data={})
            for i in range(1, 11)
        ]
        event_ids = [e.event_id for e in events]
        assert len(set(event_ids)) == 10


class TestStoredEventValidation:
    """Negative tests for StoredEvent validation."""

    def test_empty_stream_id_rejected(self) -> None:
        """Empty stream_id is rejected."""
        with pytest.raises(ValueError, match="stream_id cannot be empty"):
            StoredEvent(
                stream_id="",
                version=1,
                event_type="Test",
                data={},
            )

    def test_zero_version_rejected(self) -> None:
        """Version 0 is rejected (must be >= 1)."""
        with pytest.raises(ValueError, match="version must be >= 1"):
            StoredEvent(
                stream_id="WORK-001",
                version=0,
                event_type="Test",
                data={},
            )

    def test_negative_version_rejected(self) -> None:
        """Negative version is rejected."""
        with pytest.raises(ValueError, match="version must be >= 1"):
            StoredEvent(
                stream_id="WORK-001",
                version=-1,
                event_type="Test",
                data={},
            )

    def test_empty_event_type_rejected(self) -> None:
        """Empty event_type is rejected."""
        with pytest.raises(ValueError, match="event_type cannot be empty"):
            StoredEvent(
                stream_id="WORK-001",
                version=1,
                event_type="",
                data={},
            )

    def test_non_dict_data_rejected(self) -> None:
        """Non-dict data is rejected."""
        with pytest.raises(TypeError, match="data must be a dict"):
            StoredEvent(
                stream_id="WORK-001",
                version=1,
                event_type="Test",
                data="not a dict",  # type: ignore
            )

    def test_list_data_rejected(self) -> None:
        """List data is rejected (must be dict)."""
        with pytest.raises(TypeError, match="data must be a dict"):
            StoredEvent(
                stream_id="WORK-001",
                version=1,
                event_type="Test",
                data=[1, 2, 3],  # type: ignore
            )


class TestStoredEventImmutability:
    """Tests for StoredEvent immutability."""

    def test_is_frozen(self) -> None:
        """StoredEvent is immutable."""
        event = StoredEvent(
            stream_id="WORK-001",
            version=1,
            event_type="Test",
            data={},
        )
        with pytest.raises(FrozenInstanceError):
            event.stream_id = "WORK-002"  # type: ignore

    def test_is_not_hashable_due_to_dict_data(self) -> None:
        """StoredEvent cannot be hashed due to mutable dict field.

        Note: This is intentional - events contain payload data as dict
        which is mutable and thus unhashable. For lookup, use event_id.
        """
        event = StoredEvent(
            stream_id="WORK-001",
            version=1,
            event_type="Test",
            data={"key": "value"},
        )
        with pytest.raises(TypeError, match="unhashable"):
            hash(event)


class TestStoredEventSerialization:
    """Tests for StoredEvent serialization."""

    def test_to_dict(self) -> None:
        """to_dict returns JSON-serializable dictionary."""
        timestamp = datetime(2025, 1, 15, 10, 30, 0, tzinfo=timezone.utc)
        event_id = UUID("12345678-1234-5678-1234-567812345678")

        event = StoredEvent(
            stream_id="WORK-001",
            version=1,
            event_type="WorkItemCreated",
            data={"title": "Test"},
            timestamp=timestamp,
            event_id=event_id,
        )
        result = event.to_dict()

        assert result["stream_id"] == "WORK-001"
        assert result["version"] == 1
        assert result["event_type"] == "WorkItemCreated"
        assert result["data"] == {"title": "Test"}
        assert result["timestamp"] == "2025-01-15T10:30:00+00:00"
        assert result["event_id"] == "12345678-1234-5678-1234-567812345678"

    def test_from_dict(self) -> None:
        """from_dict reconstructs StoredEvent from dictionary."""
        data = {
            "stream_id": "WORK-001",
            "version": 2,
            "event_type": "WorkItemUpdated",
            "data": {"status": "in_progress"},
            "timestamp": "2025-06-20T14:45:30+00:00",
            "event_id": "abcd1234-abcd-1234-abcd-1234abcd1234",
        }

        event = StoredEvent.from_dict(data)

        assert event.stream_id == "WORK-001"
        assert event.version == 2
        assert event.event_type == "WorkItemUpdated"
        assert event.data == {"status": "in_progress"}
        assert event.timestamp == datetime(2025, 6, 20, 14, 45, 30, tzinfo=timezone.utc)
        assert event.event_id == UUID("abcd1234-abcd-1234-abcd-1234abcd1234")

    def test_roundtrip(self) -> None:
        """to_dict/from_dict roundtrip preserves data."""
        original = StoredEvent(
            stream_id="WORK-003",
            version=10,
            event_type="ComplexEvent",
            data={"nested": {"value": 42}, "list": [1, 2, 3]},
        )

        serialized = original.to_dict()
        restored = StoredEvent.from_dict(serialized)

        assert restored.stream_id == original.stream_id
        assert restored.version == original.version
        assert restored.event_type == original.event_type
        assert restored.data == original.data
        # Note: timestamp and event_id are regenerated if not in dict

    def test_from_dict_with_missing_optional_fields(self) -> None:
        """from_dict handles missing timestamp and event_id."""
        data = {
            "stream_id": "WORK-001",
            "version": 1,
            "event_type": "Test",
            "data": {},
        }

        event = StoredEvent.from_dict(data)

        assert isinstance(event.timestamp, datetime)
        assert isinstance(event.event_id, UUID)


class TestConcurrencyError:
    """Tests for ConcurrencyError exception."""

    def test_has_stream_id(self) -> None:
        """ConcurrencyError stores stream_id."""
        error = ConcurrencyError("WORK-001", expected=5, actual=7)
        assert error.stream_id == "WORK-001"

    def test_has_expected_version(self) -> None:
        """ConcurrencyError stores expected_version."""
        error = ConcurrencyError("WORK-001", expected=5, actual=7)
        assert error.expected_version == 5

    def test_has_actual_version(self) -> None:
        """ConcurrencyError stores actual_version."""
        error = ConcurrencyError("WORK-001", expected=5, actual=7)
        assert error.actual_version == 7

    def test_message_format(self) -> None:
        """ConcurrencyError has descriptive message."""
        error = ConcurrencyError("WORK-001", expected=5, actual=7)
        assert "WORK-001" in str(error)
        assert "expected 5" in str(error)
        assert "actual 7" in str(error)

    def test_is_event_store_error(self) -> None:
        """ConcurrencyError is EventStoreError subclass."""
        error = ConcurrencyError("WORK-001", expected=5, actual=7)
        assert isinstance(error, EventStoreError)

    def test_can_be_raised_and_caught(self) -> None:
        """ConcurrencyError can be raised and caught."""
        with pytest.raises(ConcurrencyError) as exc_info:
            raise ConcurrencyError("WORK-001", expected=0, actual=5)

        assert exc_info.value.stream_id == "WORK-001"


class TestStreamNotFoundError:
    """Tests for StreamNotFoundError exception."""

    def test_has_stream_id(self) -> None:
        """StreamNotFoundError stores stream_id."""
        error = StreamNotFoundError("WORK-999")
        assert error.stream_id == "WORK-999"

    def test_message_format(self) -> None:
        """StreamNotFoundError has descriptive message."""
        error = StreamNotFoundError("WORK-999")
        assert "WORK-999" in str(error)
        assert "not found" in str(error)

    def test_is_event_store_error(self) -> None:
        """StreamNotFoundError is EventStoreError subclass."""
        error = StreamNotFoundError("WORK-999")
        assert isinstance(error, EventStoreError)


class TestEventStoreError:
    """Tests for base EventStoreError."""

    def test_is_exception(self) -> None:
        """EventStoreError is Exception subclass."""
        error = EventStoreError("test error")
        assert isinstance(error, Exception)

    def test_message(self) -> None:
        """EventStoreError preserves message."""
        error = EventStoreError("custom message")
        assert str(error) == "custom message"
