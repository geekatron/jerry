# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for shared_kernel.domain_event module.

These tests verify the DomainEvent base class and event infrastructure
per ADR-009 (Event Storage Mechanism).
"""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

# Imports will fail until implemented - RED phase
from src.shared_kernel.domain_event import (
    DomainEvent,
    EventRegistry,
)


class TestDomainEventCreation:
    """Tests for DomainEvent initialization."""

    def test_create_with_required_fields(self) -> None:
        """Event can be created with required fields."""
        event = DomainEvent(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        assert event.aggregate_id == "WORK-001"
        assert event.aggregate_type == "WorkItem"

    def test_event_has_auto_generated_id(self) -> None:
        """Event gets auto-generated event_id."""
        event = DomainEvent(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        assert event.event_id is not None
        assert event.event_id.startswith("EVT-")

    def test_event_has_auto_generated_timestamp(self) -> None:
        """Event gets auto-generated UTC timestamp."""
        before = datetime.now(UTC)
        event = DomainEvent(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        after = datetime.now(UTC)

        assert event.timestamp is not None
        assert before <= event.timestamp <= after
        assert event.timestamp.tzinfo == UTC

    def test_event_default_version_is_one(self) -> None:
        """Event defaults to version 1."""
        event = DomainEvent(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        assert event.version == 1

    def test_event_accepts_explicit_version(self) -> None:
        """Event accepts explicit version number."""
        event = DomainEvent(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            version=5,
        )
        assert event.version == 5

    def test_event_accepts_explicit_event_id(self) -> None:
        """Event accepts explicit event_id."""
        event = DomainEvent(
            event_id="EVT-custom-123",
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        assert event.event_id == "EVT-custom-123"

    def test_event_accepts_explicit_timestamp(self) -> None:
        """Event accepts explicit timestamp."""
        custom_time = datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)
        event = DomainEvent(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            timestamp=custom_time,
        )
        assert event.timestamp == custom_time


class TestDomainEventValidation:
    """Tests for DomainEvent validation."""

    def test_empty_aggregate_id_rejected(self) -> None:
        """Empty aggregate_id is rejected."""
        with pytest.raises(ValueError, match="aggregate_id"):
            DomainEvent(
                aggregate_id="",
                aggregate_type="WorkItem",
            )

    def test_none_aggregate_id_rejected(self) -> None:
        """None aggregate_id is rejected."""
        with pytest.raises((ValueError, TypeError)):
            DomainEvent(
                aggregate_id=None,  # type: ignore
                aggregate_type="WorkItem",
            )

    def test_empty_aggregate_type_rejected(self) -> None:
        """Empty aggregate_type is rejected."""
        with pytest.raises(ValueError, match="aggregate_type"):
            DomainEvent(
                aggregate_id="WORK-001",
                aggregate_type="",
            )

    def test_negative_version_rejected(self) -> None:
        """Negative version is rejected."""
        with pytest.raises(ValueError, match="version"):
            DomainEvent(
                aggregate_id="WORK-001",
                aggregate_type="WorkItem",
                version=-1,
            )

    def test_zero_version_rejected(self) -> None:
        """Zero version is rejected."""
        with pytest.raises(ValueError, match="version"):
            DomainEvent(
                aggregate_id="WORK-001",
                aggregate_type="WorkItem",
                version=0,
            )


class TestDomainEventImmutability:
    """Tests for DomainEvent immutability."""

    def test_event_is_frozen(self) -> None:
        """Event is a frozen dataclass."""
        event = DomainEvent(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        with pytest.raises(FrozenInstanceError):
            event.aggregate_id = "WORK-002"  # type: ignore

    def test_event_timestamp_immutable(self) -> None:
        """Event timestamp cannot be modified."""
        event = DomainEvent(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        with pytest.raises(FrozenInstanceError):
            event.timestamp = datetime.now(UTC)  # type: ignore


class TestDomainEventSerialization:
    """Tests for DomainEvent serialization."""

    def test_to_dict_contains_event_type(self) -> None:
        """to_dict includes event_type."""
        event = DomainEvent(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        data = event.to_dict()
        assert data["event_type"] == "DomainEvent"

    def test_to_dict_contains_event_id(self) -> None:
        """to_dict includes event_id."""
        event = DomainEvent(
            event_id="EVT-test-123",
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        data = event.to_dict()
        assert data["event_id"] == "EVT-test-123"

    def test_to_dict_contains_timestamp_as_iso(self) -> None:
        """to_dict includes timestamp as ISO string."""
        event = DomainEvent(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        data = event.to_dict()
        assert "timestamp" in data
        # Should be parseable as ISO format
        datetime.fromisoformat(data["timestamp"])

    def test_to_dict_contains_aggregate_id(self) -> None:
        """to_dict includes aggregate_id."""
        event = DomainEvent(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        data = event.to_dict()
        assert data["aggregate_id"] == "WORK-001"

    def test_to_dict_contains_aggregate_type(self) -> None:
        """to_dict includes aggregate_type."""
        event = DomainEvent(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        data = event.to_dict()
        assert data["aggregate_type"] == "WorkItem"

    def test_to_dict_contains_version(self) -> None:
        """to_dict includes version."""
        event = DomainEvent(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            version=3,
        )
        data = event.to_dict()
        assert data["version"] == 3

    def test_to_dict_json_serializable(self) -> None:
        """to_dict result is JSON serializable."""
        event = DomainEvent(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        data = event.to_dict()
        # Should not raise
        json_str = json.dumps(data)
        assert json_str is not None


class TestDomainEventDeserialization:
    """Tests for DomainEvent deserialization."""

    def test_from_dict_reconstructs_event(self) -> None:
        """from_dict reconstructs event from dictionary."""
        original = DomainEvent(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            version=3,
        )
        data = original.to_dict()
        reconstructed = DomainEvent.from_dict(data)

        assert reconstructed.event_id == original.event_id
        assert reconstructed.aggregate_id == original.aggregate_id
        assert reconstructed.aggregate_type == original.aggregate_type
        assert reconstructed.version == original.version

    def test_from_dict_preserves_timestamp(self) -> None:
        """from_dict preserves timestamp correctly."""
        custom_time = datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)
        original = DomainEvent(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            timestamp=custom_time,
        )
        data = original.to_dict()
        reconstructed = DomainEvent.from_dict(data)

        assert reconstructed.timestamp == custom_time

    def test_roundtrip_serialization(self) -> None:
        """Event survives roundtrip serialization."""
        original = DomainEvent(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            version=5,
        )

        json_str = json.dumps(original.to_dict())
        data = json.loads(json_str)
        reconstructed = DomainEvent.from_dict(data)

        assert reconstructed.event_id == original.event_id
        assert reconstructed.aggregate_id == original.aggregate_id


class TestDomainEventEquality:
    """Tests for DomainEvent equality."""

    def test_equality_by_event_id(self) -> None:
        """Events with same event_id are equal."""
        event1 = DomainEvent(
            event_id="EVT-same-123",
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        event2 = DomainEvent(
            event_id="EVT-same-123",
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        assert event1 == event2

    def test_same_hash_for_equal_events(self) -> None:
        """Events with same event_id have same hash."""
        event1 = DomainEvent(
            event_id="EVT-same-123",
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        event2 = DomainEvent(
            event_id="EVT-same-123",
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        assert hash(event1) == hash(event2)

    def test_inequality_by_different_event_id(self) -> None:
        """Events with different event_id are not equal."""
        event1 = DomainEvent(
            event_id="EVT-aaa",
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        event2 = DomainEvent(
            event_id="EVT-bbb",
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        assert event1 != event2

    def test_events_usable_in_set(self) -> None:
        """Events can be used in sets."""
        event1 = DomainEvent(
            event_id="EVT-a",
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        event2 = DomainEvent(
            event_id="EVT-b",
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
        )
        events = {event1, event2}
        assert len(events) == 2


class TestDomainEventNegative:
    """Negative tests for DomainEvent deserialization.

    These tests verify proper error handling for malformed input.
    Per battle-tested ratios: 20-30% of tests should be negative.
    """

    def test_from_dict_missing_aggregate_id(self) -> None:
        """from_dict raises on missing aggregate_id.

        aggregate_id is a required field - deserialization must fail
        clearly if it's missing rather than producing invalid events.
        """
        data = {
            "event_type": "DomainEvent",
            "aggregate_type": "WorkItem",
            "version": 1,
        }
        with pytest.raises(KeyError):
            DomainEvent.from_dict(data)

    def test_from_dict_missing_aggregate_type(self) -> None:
        """from_dict raises on missing aggregate_type.

        aggregate_type is a required field - deserialization must fail
        clearly if it's missing.
        """
        data = {
            "event_type": "DomainEvent",
            "aggregate_id": "WORK-001",
            "version": 1,
        }
        with pytest.raises(KeyError):
            DomainEvent.from_dict(data)

    def test_from_dict_invalid_timestamp_format(self) -> None:
        """from_dict raises on invalid timestamp format.

        Invalid timestamp strings must be rejected rather than
        silently ignored or causing cryptic errors downstream.
        """
        data = {
            "event_type": "DomainEvent",
            "aggregate_id": "WORK-001",
            "aggregate_type": "WorkItem",
            "timestamp": "not-a-valid-timestamp",
            "version": 1,
        }
        with pytest.raises(ValueError):
            DomainEvent.from_dict(data)

    def test_deserialize_missing_event_type(self) -> None:
        """Registry raises on missing event_type field.

        The event_type field is required for polymorphic deserialization.
        Its absence must be caught and reported clearly.
        """
        registry = EventRegistry()
        registry.register(DomainEvent)
        data = {"aggregate_id": "WORK-001", "aggregate_type": "WorkItem"}
        with pytest.raises(ValueError, match="Missing event_type"):
            registry.deserialize(data)

    def test_deserialize_empty_event_type(self) -> None:
        """Registry raises on empty event_type.

        Empty string event_type should be treated as missing.
        """
        registry = EventRegistry()
        registry.register(DomainEvent)
        data = {
            "event_type": "",
            "aggregate_id": "WORK-001",
            "aggregate_type": "WorkItem",
        }
        with pytest.raises(ValueError, match="Missing event_type|Unknown event"):
            registry.deserialize(data)


class TestEventRegistry:
    """Tests for EventRegistry."""

    def test_register_event_class(self) -> None:
        """EventRegistry can register event classes."""
        registry = EventRegistry()
        registry.register(DomainEvent)

        assert "DomainEvent" in registry.event_types

    def test_get_registered_class(self) -> None:
        """EventRegistry returns registered class by name."""
        registry = EventRegistry()
        registry.register(DomainEvent)

        cls = registry.get("DomainEvent")
        assert cls is DomainEvent

    def test_get_unregistered_returns_none(self) -> None:
        """EventRegistry returns None for unregistered types."""
        registry = EventRegistry()

        cls = registry.get("NonExistent")
        assert cls is None

    def test_deserialize_using_registry(self) -> None:
        """EventRegistry can deserialize events by type."""
        registry = EventRegistry()
        registry.register(DomainEvent)

        data = {
            "event_type": "DomainEvent",
            "event_id": "EVT-test",
            "aggregate_id": "WORK-001",
            "aggregate_type": "WorkItem",
            "version": 1,
            "timestamp": "2026-01-01T12:00:00+00:00",
        }

        event = registry.deserialize(data)
        assert isinstance(event, DomainEvent)
        assert event.event_id == "EVT-test"

    def test_deserialize_unknown_type_raises(self) -> None:
        """EventRegistry raises for unknown event types."""
        registry = EventRegistry()

        data = {"event_type": "UnknownEvent"}

        with pytest.raises(ValueError, match="Unknown event type"):
            registry.deserialize(data)

    def test_decorator_registration(self) -> None:
        """EventRegistry supports decorator-based registration."""
        registry = EventRegistry()

        @registry.register
        class TestEvent(DomainEvent):
            pass

        assert "TestEvent" in registry.event_types
        assert registry.get("TestEvent") is TestEvent
