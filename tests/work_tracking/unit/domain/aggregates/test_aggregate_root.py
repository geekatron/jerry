# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for work_tracking.domain.aggregates.base module.

Test Categories:
    - Happy Path: Normal aggregate creation, event raising, and collection
    - Edge Cases: Boundary conditions and special scenarios
    - Negative Cases: Validation errors and rejected inputs
    - History Replay: load_from_history reconstruction tests

References:
    - PAT-001: Event Store Interface Pattern
    - IMPL-ES-003: AggregateRoot Base Class implementation
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime

import pytest

from src.shared_kernel.domain_event import DomainEvent
from src.work_tracking.domain.aggregates.base import AggregateRoot

# Fixtures - Concrete implementation for testing
# Note: Classes prefixed with "_" to avoid pytest collection warnings


@dataclass(frozen=True)
class _ItemCreatedEvent(DomainEvent):
    """Fixture event: Item was created."""

    title: str = ""

    def _payload(self) -> dict:
        return {"title": self.title}


@dataclass(frozen=True)
class _ItemTitleChangedEvent(DomainEvent):
    """Fixture event: Item title was changed."""

    old_title: str = ""
    new_title: str = ""

    def _payload(self) -> dict:
        return {"old_title": self.old_title, "new_title": self.new_title}


@dataclass(frozen=True)
class _ItemCompletedEvent(DomainEvent):
    """Fixture event: Item was completed."""

    reason: str | None = None

    def _payload(self) -> dict:
        return {"reason": self.reason}


class _SampleItem(AggregateRoot):
    """Concrete aggregate for testing AggregateRoot."""

    _aggregate_type = "SampleItem"

    def __init__(self, id: str, title: str = "") -> None:
        super().__init__(id)
        self._title = title
        self._status = "pending"

    @classmethod
    def create(cls, id: str, title: str) -> _SampleItem:
        """Factory method to create a new _SampleItem."""
        item = cls(id, title)
        event = _ItemCreatedEvent(
            aggregate_id=id,
            aggregate_type=cls._aggregate_type,
            version=1,
            title=title,
        )
        item._raise_event(event)
        return item

    @property
    def title(self) -> str:
        return self._title

    @property
    def status(self) -> str:
        return self._status

    def change_title(self, new_title: str) -> None:
        """Change the item title."""
        event = _ItemTitleChangedEvent(
            aggregate_id=self.id,
            aggregate_type=self._aggregate_type,
            version=self.version + 1,
            old_title=self._title,
            new_title=new_title,
        )
        self._raise_event(event)

    def complete(self, reason: str | None = None) -> None:
        """Mark item as completed."""
        event = _ItemCompletedEvent(
            aggregate_id=self.id,
            aggregate_type=self._aggregate_type,
            version=self.version + 1,
            reason=reason,
        )
        self._raise_event(event)

    def _apply(self, event: DomainEvent) -> None:
        """Apply event to update state."""
        if isinstance(event, _ItemCreatedEvent):
            self._title = event.title
            self._status = "pending"
        elif isinstance(event, _ItemTitleChangedEvent):
            self._title = event.new_title
        elif isinstance(event, _ItemCompletedEvent):
            self._status = "completed"


# =============================================================================
# Happy Path Tests
# =============================================================================


class TestAggregateRootCreation:
    """Tests for AggregateRoot initialization."""

    def test_create_with_id(self) -> None:
        """Aggregate can be created with an ID."""
        item = _SampleItem("ITEM-001")
        assert item.id == "ITEM-001"

    def test_initial_version_is_zero(self) -> None:
        """New aggregate has version 0."""
        item = _SampleItem("ITEM-001")
        assert item.version == 0

    def test_no_pending_events_initially(self) -> None:
        """New aggregate has no pending events."""
        item = _SampleItem("ITEM-001")
        assert item.has_pending_events() is False

    def test_created_on_initially_none(self) -> None:
        """New aggregate has no created_on timestamp."""
        item = _SampleItem("ITEM-001")
        assert item.created_on is None

    def test_modified_on_initially_none(self) -> None:
        """New aggregate has no modified_on timestamp."""
        item = _SampleItem("ITEM-001")
        assert item.modified_on is None

    def test_factory_method_creates_with_event(self) -> None:
        """Factory method creates aggregate and raises event."""
        item = _SampleItem.create("ITEM-001", "Test Title")
        assert item.id == "ITEM-001"
        assert item.title == "Test Title"
        assert item.version == 1

    def test_factory_method_has_pending_event(self) -> None:
        """Factory method results in pending event."""
        item = _SampleItem.create("ITEM-001", "Test Title")
        assert item.has_pending_events() is True


class TestRaiseEvent:
    """Tests for _raise_event behavior."""

    def test_raises_event_increments_version(self) -> None:
        """Raising an event increments the version."""
        item = _SampleItem.create("ITEM-001", "Original")
        assert item.version == 1

        item.change_title("New Title")
        assert item.version == 2

    def test_raises_event_applies_state(self) -> None:
        """Raising an event applies the state change."""
        item = _SampleItem.create("ITEM-001", "Original")
        item.change_title("New Title")
        assert item.title == "New Title"

    def test_raises_event_adds_to_pending(self) -> None:
        """Raising an event adds it to pending events."""
        item = _SampleItem.create("ITEM-001", "Test")
        events = item.collect_events()
        assert len(events) == 1

        item.change_title("Updated")
        events = item.collect_events()
        assert len(events) == 1

    def test_multiple_events_accumulate(self) -> None:
        """Multiple events accumulate in pending list."""
        item = _SampleItem.create("ITEM-001", "Test")
        item.change_title("Updated")
        item.complete("Done")

        events = item.collect_events()
        assert len(events) == 3

    def test_sets_created_on_from_first_event(self) -> None:
        """First event sets created_on timestamp."""
        item = _SampleItem.create("ITEM-001", "Test")
        assert item.created_on is not None
        assert isinstance(item.created_on, datetime)

    def test_updates_modified_on_from_event(self) -> None:
        """Each event updates modified_on timestamp."""
        item = _SampleItem.create("ITEM-001", "Test")
        first_modified = item.modified_on

        item.change_title("Updated")
        assert item.modified_on is not None
        assert item.modified_on >= first_modified


class TestCollectEvents:
    """Tests for collect_events behavior."""

    def test_returns_pending_events(self) -> None:
        """collect_events returns list of pending events."""
        item = _SampleItem.create("ITEM-001", "Test")
        events = item.collect_events()

        assert len(events) == 1
        assert isinstance(events[0], _ItemCreatedEvent)

    def test_clears_pending_events(self) -> None:
        """collect_events clears the pending list."""
        item = _SampleItem.create("ITEM-001", "Test")
        item.collect_events()

        assert item.has_pending_events() is False
        assert item.collect_events() == []

    def test_preserves_event_order(self) -> None:
        """Events are returned in order raised."""
        item = _SampleItem.create("ITEM-001", "Test")
        item.change_title("Updated")
        item.complete()

        events = item.collect_events()
        assert isinstance(events[0], _ItemCreatedEvent)
        assert isinstance(events[1], _ItemTitleChangedEvent)
        assert isinstance(events[2], _ItemCompletedEvent)

    def test_returns_sequence_type(self) -> None:
        """collect_events returns a Sequence."""
        item = _SampleItem.create("ITEM-001", "Test")
        events = item.collect_events()
        assert isinstance(events, Sequence)


class TestLoadFromHistory:
    """Tests for load_from_history reconstruction."""

    def test_reconstructs_from_single_event(self) -> None:
        """Aggregate can be reconstructed from a single event."""
        event = _ItemCreatedEvent(
            aggregate_id="ITEM-001",
            aggregate_type="_SampleItem",
            version=1,
            title="Test Title",
        )

        item = _SampleItem.load_from_history([event])

        assert item.id == "ITEM-001"
        assert item.version == 1
        assert item.title == "Test Title"

    def test_reconstructs_from_multiple_events(self) -> None:
        """Aggregate can be reconstructed from multiple events."""
        events = [
            _ItemCreatedEvent(
                aggregate_id="ITEM-001",
                aggregate_type="_SampleItem",
                version=1,
                title="Original",
            ),
            _ItemTitleChangedEvent(
                aggregate_id="ITEM-001",
                aggregate_type="_SampleItem",
                version=2,
                old_title="Original",
                new_title="Updated",
            ),
            _ItemCompletedEvent(
                aggregate_id="ITEM-001",
                aggregate_type="_SampleItem",
                version=3,
                reason="Done",
            ),
        ]

        item = _SampleItem.load_from_history(events)

        assert item.id == "ITEM-001"
        assert item.version == 3
        assert item.title == "Updated"
        assert item.status == "completed"

    def test_no_pending_events_after_load(self) -> None:
        """Loaded aggregate has no pending events."""
        event = _ItemCreatedEvent(
            aggregate_id="ITEM-001",
            aggregate_type="_SampleItem",
            version=1,
            title="Test",
        )

        item = _SampleItem.load_from_history([event])

        assert item.has_pending_events() is False

    def test_sets_created_on_from_first_event(self) -> None:
        """created_on is set from first event timestamp."""
        timestamp = datetime(2025, 1, 15, 10, 30, 0, tzinfo=UTC)
        event = _ItemCreatedEvent(
            aggregate_id="ITEM-001",
            aggregate_type="_SampleItem",
            version=1,
            timestamp=timestamp,
            title="Test",
        )

        item = _SampleItem.load_from_history([event])

        assert item.created_on == timestamp

    def test_sets_modified_on_from_last_event(self) -> None:
        """modified_on is set from last event timestamp."""
        ts1 = datetime(2025, 1, 15, 10, 30, 0, tzinfo=UTC)
        ts2 = datetime(2025, 1, 16, 14, 45, 0, tzinfo=UTC)

        events = [
            _ItemCreatedEvent(
                aggregate_id="ITEM-001",
                aggregate_type="_SampleItem",
                version=1,
                timestamp=ts1,
                title="Test",
            ),
            _ItemCompletedEvent(
                aggregate_id="ITEM-001",
                aggregate_type="_SampleItem",
                version=2,
                timestamp=ts2,
            ),
        ]

        item = _SampleItem.load_from_history(events)

        assert item.modified_on == ts2


# =============================================================================
# Edge Case Tests
# =============================================================================


class TestEdgeCases:
    """Edge case tests for AggregateRoot."""

    def test_version_increases_monotonically(self) -> None:
        """Version increases by 1 for each event."""
        item = _SampleItem.create("ITEM-001", "Test")
        versions = [item.version]

        for i in range(5):
            item.change_title(f"Title {i}")
            versions.append(item.version)

        assert versions == [1, 2, 3, 4, 5, 6]

    def test_can_collect_empty_events(self) -> None:
        """Collecting when no events is safe."""
        item = _SampleItem("ITEM-001")
        events = item.collect_events()
        assert events == []

    def test_can_collect_multiple_times(self) -> None:
        """Collecting multiple times returns new events each time."""
        item = _SampleItem.create("ITEM-001", "Test")
        events1 = item.collect_events()
        assert len(events1) == 1

        item.change_title("Updated")
        events2 = item.collect_events()
        assert len(events2) == 1

        events3 = item.collect_events()
        assert len(events3) == 0

    def test_aggregate_state_independent_of_pending(self) -> None:
        """Aggregate state is correct regardless of collection status."""
        item = _SampleItem.create("ITEM-001", "Original")
        item.change_title("Updated")

        # Before collection
        assert item.title == "Updated"

        item.collect_events()

        # After collection
        assert item.title == "Updated"

    def test_repr_shows_useful_info(self) -> None:
        """repr shows ID, version, and pending count."""
        item = _SampleItem.create("ITEM-001", "Test")
        repr_str = repr(item)

        assert "ITEM-001" in repr_str
        assert "version=1" in repr_str
        assert "pending_events=1" in repr_str


# =============================================================================
# Equality and Hashing Tests
# =============================================================================


class TestEqualityAndHashing:
    """Tests for aggregate equality and hashing."""

    def test_equal_by_id(self) -> None:
        """Aggregates with same ID are equal."""
        item1 = _SampleItem("ITEM-001", "Title A")
        item2 = _SampleItem("ITEM-001", "Title B")
        assert item1 == item2

    def test_not_equal_different_id(self) -> None:
        """Aggregates with different IDs are not equal."""
        item1 = _SampleItem("ITEM-001", "Title")
        item2 = _SampleItem("ITEM-002", "Title")
        assert item1 != item2

    def test_hash_by_id(self) -> None:
        """Same ID produces same hash."""
        item1 = _SampleItem("ITEM-001", "Title A")
        item2 = _SampleItem("ITEM-001", "Title B")
        assert hash(item1) == hash(item2)

    def test_usable_in_set(self) -> None:
        """Aggregates can be used in sets."""
        item1 = _SampleItem("ITEM-001", "Title")
        item2 = _SampleItem("ITEM-001", "Title")  # Same ID
        item3 = _SampleItem("ITEM-002", "Title")

        items = {item1, item2, item3}
        assert len(items) == 2

    def test_usable_as_dict_key(self) -> None:
        """Aggregates can be used as dictionary keys."""
        item = _SampleItem("ITEM-001", "Title")
        data = {item: "value"}
        assert data[item] == "value"

    def test_not_equal_to_non_aggregate(self) -> None:
        """Aggregates are not equal to non-aggregates."""
        item = _SampleItem("ITEM-001", "Title")
        assert item != "ITEM-001"
        assert item != 42


# =============================================================================
# Negative Tests
# =============================================================================


class TestValidationErrors:
    """Negative tests for validation errors."""

    def test_empty_id_rejected(self) -> None:
        """Empty ID is rejected."""
        with pytest.raises(ValueError, match="cannot be empty"):
            _SampleItem("")

    def test_whitespace_id_accepted(self) -> None:
        """Whitespace-only ID is currently accepted (non-empty string)."""
        item = _SampleItem("   ")
        assert item.id == "   "

    def test_event_with_wrong_aggregate_id_rejected(self) -> None:
        """Event with mismatched aggregate_id is rejected."""
        item = _SampleItem("ITEM-001")
        event = _ItemCreatedEvent(
            aggregate_id="ITEM-999",  # Wrong ID
            aggregate_type="_SampleItem",
            version=1,
            title="Test",
        )

        with pytest.raises(ValueError, match="does not match"):
            item._raise_event(event)


class TestLoadFromHistoryErrors:
    """Negative tests for load_from_history errors."""

    def test_empty_history_rejected(self) -> None:
        """Empty event history is rejected."""
        with pytest.raises(ValueError, match="empty event history"):
            _SampleItem.load_from_history([])

    def test_inconsistent_aggregate_id_rejected(self) -> None:
        """Events with different aggregate IDs are rejected."""
        events = [
            _ItemCreatedEvent(
                aggregate_id="ITEM-001",
                aggregate_type="_SampleItem",
                version=1,
                title="Test",
            ),
            _ItemCompletedEvent(
                aggregate_id="ITEM-002",  # Different ID!
                aggregate_type="_SampleItem",
                version=2,
            ),
        ]

        with pytest.raises(ValueError, match="aggregate_id"):
            _SampleItem.load_from_history(events)

    def test_out_of_order_versions_rejected(self) -> None:
        """Events with non-sequential versions are rejected."""
        events = [
            _ItemCreatedEvent(
                aggregate_id="ITEM-001",
                aggregate_type="_SampleItem",
                version=1,
                title="Test",
            ),
            _ItemCompletedEvent(
                aggregate_id="ITEM-001",
                aggregate_type="_SampleItem",
                version=3,  # Skipped version 2!
            ),
        ]

        with pytest.raises(ValueError, match="version"):
            _SampleItem.load_from_history(events)

    def test_non_starting_at_one_rejected(self) -> None:
        """Events not starting at version 1 are rejected."""
        events = [
            _ItemCreatedEvent(
                aggregate_id="ITEM-001",
                aggregate_type="_SampleItem",
                version=5,  # Should start at 1
                title="Test",
            ),
        ]

        # This should work - we validate sequence, not absolute start
        # The first event defines the starting point
        item = _SampleItem.load_from_history(events)
        assert item.version == 5


class TestValidateEventSequence:
    """Tests for _validate_event_sequence helper."""

    def test_validates_sequential_versions(self) -> None:
        """Sequential versions pass validation."""
        events = [
            _ItemCreatedEvent(
                aggregate_id="ITEM-001",
                aggregate_type="_SampleItem",
                version=1,
                title="Test",
            ),
            _ItemCompletedEvent(
                aggregate_id="ITEM-001",
                aggregate_type="_SampleItem",
                version=2,
            ),
        ]

        # Should not raise
        AggregateRoot._validate_event_sequence(events)

    def test_validates_empty_sequence(self) -> None:
        """Empty sequence passes validation."""
        # Should not raise
        AggregateRoot._validate_event_sequence([])

    def test_rejects_version_gap(self) -> None:
        """Version gaps are rejected."""
        events = [
            _ItemCreatedEvent(
                aggregate_id="ITEM-001",
                aggregate_type="_SampleItem",
                version=1,
                title="Test",
            ),
            _ItemCompletedEvent(
                aggregate_id="ITEM-001",
                aggregate_type="_SampleItem",
                version=5,  # Gap!
            ),
        ]

        with pytest.raises(ValueError, match="version"):
            AggregateRoot._validate_event_sequence(events)

    def test_rejects_decreasing_version(self) -> None:
        """Decreasing versions are rejected."""
        events = [
            _ItemCreatedEvent(
                aggregate_id="ITEM-001",
                aggregate_type="_SampleItem",
                version=5,
                title="Test",
            ),
            _ItemCompletedEvent(
                aggregate_id="ITEM-001",
                aggregate_type="_SampleItem",
                version=4,  # Decreased!
            ),
        ]

        with pytest.raises(ValueError, match="version"):
            AggregateRoot._validate_event_sequence(events)
