# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for ISnapshotStore port and InMemorySnapshotStore.

Test Categories:
    - StoredSnapshot: Creation, validation, serialization
    - Protocol Compliance: Interface adherence
    - Save Operations: Storing snapshots
    - Load Operations: Retrieving snapshots
    - Delete Operations: Removing snapshots
    - Edge Cases: Boundary conditions

References:
    - IMPL-ES-002: ISnapshotStore Port
    - PAT-001: Event Store Interface Pattern
"""

from __future__ import annotations

from datetime import datetime

import pytest

from src.work_tracking.domain.ports.snapshot_store import (
    InMemorySnapshotStore,
    ISnapshotStore,
    SnapshotNotFoundError,
    StoredSnapshot,
)

# =============================================================================
# StoredSnapshot Tests
# =============================================================================


class TestStoredSnapshotCreation:
    """Tests for StoredSnapshot creation and validation."""

    def test_create_with_required_fields(self) -> None:
        """Create snapshot with required fields."""
        snapshot = StoredSnapshot(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            version=5,
            state={"title": "Test", "status": "pending"},
        )
        assert snapshot.aggregate_id == "WORK-001"
        assert snapshot.aggregate_type == "WorkItem"
        assert snapshot.version == 5
        assert snapshot.state["title"] == "Test"

    def test_snapshot_has_timestamp(self) -> None:
        """Snapshot has auto-generated timestamp."""
        snapshot = StoredSnapshot(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            version=1,
            state={},
        )
        assert snapshot.timestamp is not None
        assert isinstance(snapshot.timestamp, datetime)

    def test_snapshot_has_snapshot_id(self) -> None:
        """Snapshot has auto-generated ID."""
        snapshot = StoredSnapshot(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            version=1,
            state={},
        )
        assert snapshot.snapshot_id is not None

    def test_empty_aggregate_id_raises(self) -> None:
        """Empty aggregate_id raises ValueError."""
        with pytest.raises(ValueError, match="aggregate_id"):
            StoredSnapshot(
                aggregate_id="",
                aggregate_type="WorkItem",
                version=1,
                state={},
            )

    def test_empty_aggregate_type_raises(self) -> None:
        """Empty aggregate_type raises ValueError."""
        with pytest.raises(ValueError, match="aggregate_type"):
            StoredSnapshot(
                aggregate_id="WORK-001",
                aggregate_type="",
                version=1,
                state={},
            )

    def test_zero_version_raises(self) -> None:
        """Version 0 raises ValueError."""
        with pytest.raises(ValueError, match="version"):
            StoredSnapshot(
                aggregate_id="WORK-001",
                aggregate_type="WorkItem",
                version=0,
                state={},
            )

    def test_negative_version_raises(self) -> None:
        """Negative version raises ValueError."""
        with pytest.raises(ValueError, match="version"):
            StoredSnapshot(
                aggregate_id="WORK-001",
                aggregate_type="WorkItem",
                version=-1,
                state={},
            )

    def test_non_dict_state_raises(self) -> None:
        """Non-dict state raises TypeError."""
        with pytest.raises(TypeError, match="dict"):
            StoredSnapshot(
                aggregate_id="WORK-001",
                aggregate_type="WorkItem",
                version=1,
                state="not a dict",  # type: ignore
            )


class TestStoredSnapshotSerialization:
    """Tests for StoredSnapshot serialization."""

    def test_to_dict(self) -> None:
        """to_dict produces correct structure."""
        snapshot = StoredSnapshot(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            version=5,
            state={"title": "Test"},
        )
        data = snapshot.to_dict()

        assert data["aggregate_id"] == "WORK-001"
        assert data["aggregate_type"] == "WorkItem"
        assert data["version"] == 5
        assert data["state"]["title"] == "Test"
        assert "timestamp" in data
        assert "snapshot_id" in data

    def test_from_dict_roundtrip(self) -> None:
        """from_dict reverses to_dict."""
        original = StoredSnapshot(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            version=5,
            state={"title": "Test", "count": 42},
        )
        data = original.to_dict()
        restored = StoredSnapshot.from_dict(data)

        assert restored.aggregate_id == original.aggregate_id
        assert restored.aggregate_type == original.aggregate_type
        assert restored.version == original.version
        assert restored.state == original.state


class TestStoredSnapshotImmutability:
    """Tests for StoredSnapshot immutability."""

    def test_snapshot_is_frozen(self) -> None:
        """StoredSnapshot is immutable."""
        snapshot = StoredSnapshot(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            version=1,
            state={},
        )
        with pytest.raises(Exception):  # FrozenInstanceError
            snapshot.version = 2  # type: ignore


# =============================================================================
# InMemorySnapshotStore Protocol Tests
# =============================================================================


class TestSnapshotStoreProtocol:
    """Tests for ISnapshotStore protocol compliance."""

    def test_in_memory_implements_protocol(self) -> None:
        """InMemorySnapshotStore implements ISnapshotStore."""
        store = InMemorySnapshotStore()
        assert isinstance(store, ISnapshotStore)

    def test_protocol_has_save_method(self) -> None:
        """Protocol requires save() method."""
        assert hasattr(ISnapshotStore, "save")

    def test_protocol_has_load_method(self) -> None:
        """Protocol requires load() method."""
        assert hasattr(ISnapshotStore, "load")

    def test_protocol_has_delete_method(self) -> None:
        """Protocol requires delete() method."""
        assert hasattr(ISnapshotStore, "delete")

    def test_protocol_has_exists_method(self) -> None:
        """Protocol requires exists() method."""
        assert hasattr(ISnapshotStore, "exists")


# =============================================================================
# InMemorySnapshotStore Save Tests
# =============================================================================


class TestSnapshotStoreSave:
    """Tests for saving snapshots."""

    def test_save_new_snapshot(self) -> None:
        """Can save a new snapshot."""
        store = InMemorySnapshotStore()
        snapshot = StoredSnapshot(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            version=5,
            state={"title": "Test"},
        )
        store.save(snapshot)
        assert store.exists("WORK-001")

    def test_save_replaces_existing(self) -> None:
        """Saving snapshot replaces existing one for same aggregate."""
        store = InMemorySnapshotStore()

        snapshot1 = StoredSnapshot(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            version=5,
            state={"title": "Version 5"},
        )
        store.save(snapshot1)

        snapshot2 = StoredSnapshot(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            version=10,
            state={"title": "Version 10"},
        )
        store.save(snapshot2)

        loaded = store.load("WORK-001")
        assert loaded.version == 10
        assert loaded.state["title"] == "Version 10"

    def test_save_multiple_aggregates(self) -> None:
        """Can save snapshots for different aggregates."""
        store = InMemorySnapshotStore()

        store.save(
            StoredSnapshot(
                aggregate_id="WORK-001",
                aggregate_type="WorkItem",
                version=5,
                state={"id": 1},
            )
        )
        store.save(
            StoredSnapshot(
                aggregate_id="WORK-002",
                aggregate_type="WorkItem",
                version=3,
                state={"id": 2},
            )
        )

        assert store.exists("WORK-001")
        assert store.exists("WORK-002")


# =============================================================================
# InMemorySnapshotStore Load Tests
# =============================================================================


class TestSnapshotStoreLoad:
    """Tests for loading snapshots."""

    def test_load_existing_snapshot(self) -> None:
        """Can load an existing snapshot."""
        store = InMemorySnapshotStore()
        snapshot = StoredSnapshot(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            version=5,
            state={"title": "Test", "status": "done"},
        )
        store.save(snapshot)

        loaded = store.load("WORK-001")
        assert loaded.aggregate_id == "WORK-001"
        assert loaded.version == 5
        assert loaded.state["title"] == "Test"

    def test_load_non_existent_raises(self) -> None:
        """Loading non-existent snapshot raises SnapshotNotFoundError."""
        store = InMemorySnapshotStore()
        with pytest.raises(SnapshotNotFoundError) as exc_info:
            store.load("WORK-999")
        assert "WORK-999" in str(exc_info.value)

    def test_load_returns_copy(self) -> None:
        """Loaded snapshot is independent copy."""
        store = InMemorySnapshotStore()
        snapshot = StoredSnapshot(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            version=5,
            state={"items": [1, 2, 3]},
        )
        store.save(snapshot)

        loaded1 = store.load("WORK-001")
        loaded2 = store.load("WORK-001")

        # Both should have same data
        assert loaded1.version == loaded2.version
        assert loaded1.state == loaded2.state


# =============================================================================
# InMemorySnapshotStore Delete Tests
# =============================================================================


class TestSnapshotStoreDelete:
    """Tests for deleting snapshots."""

    def test_delete_existing_returns_true(self) -> None:
        """Deleting existing snapshot returns True."""
        store = InMemorySnapshotStore()
        store.save(
            StoredSnapshot(
                aggregate_id="WORK-001",
                aggregate_type="WorkItem",
                version=5,
                state={},
            )
        )

        result = store.delete("WORK-001")
        assert result is True
        assert not store.exists("WORK-001")

    def test_delete_non_existent_returns_false(self) -> None:
        """Deleting non-existent snapshot returns False."""
        store = InMemorySnapshotStore()
        result = store.delete("WORK-999")
        assert result is False

    def test_delete_then_load_raises(self) -> None:
        """Loading after delete raises SnapshotNotFoundError."""
        store = InMemorySnapshotStore()
        store.save(
            StoredSnapshot(
                aggregate_id="WORK-001",
                aggregate_type="WorkItem",
                version=5,
                state={},
            )
        )
        store.delete("WORK-001")

        with pytest.raises(SnapshotNotFoundError):
            store.load("WORK-001")


# =============================================================================
# InMemorySnapshotStore Exists Tests
# =============================================================================


class TestSnapshotStoreExists:
    """Tests for checking snapshot existence."""

    def test_exists_returns_true_for_saved(self) -> None:
        """exists() returns True for saved snapshots."""
        store = InMemorySnapshotStore()
        store.save(
            StoredSnapshot(
                aggregate_id="WORK-001",
                aggregate_type="WorkItem",
                version=1,
                state={},
            )
        )
        assert store.exists("WORK-001") is True

    def test_exists_returns_false_for_new(self) -> None:
        """exists() returns False for non-existent."""
        store = InMemorySnapshotStore()
        assert store.exists("WORK-999") is False


# =============================================================================
# InMemorySnapshotStore Get Version Tests
# =============================================================================


class TestSnapshotStoreGetVersion:
    """Tests for getting snapshot version."""

    def test_get_version_returns_snapshot_version(self) -> None:
        """get_version() returns the snapshot's version."""
        store = InMemorySnapshotStore()
        store.save(
            StoredSnapshot(
                aggregate_id="WORK-001",
                aggregate_type="WorkItem",
                version=42,
                state={},
            )
        )
        assert store.get_version("WORK-001") == 42

    def test_get_version_returns_none_for_missing(self) -> None:
        """get_version() returns None for non-existent aggregate."""
        store = InMemorySnapshotStore()
        assert store.get_version("WORK-999") is None


# =============================================================================
# Edge Cases
# =============================================================================


class TestSnapshotStoreEdgeCases:
    """Edge case tests for snapshot store."""

    def test_empty_state_allowed(self) -> None:
        """Empty state dictionary is allowed."""
        store = InMemorySnapshotStore()
        snapshot = StoredSnapshot(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            version=1,
            state={},
        )
        store.save(snapshot)
        loaded = store.load("WORK-001")
        assert loaded.state == {}

    def test_complex_state(self) -> None:
        """Complex nested state is preserved."""
        store = InMemorySnapshotStore()
        complex_state = {
            "title": "Test",
            "nested": {"a": 1, "b": [1, 2, 3]},
            "list": [{"x": 1}, {"x": 2}],
        }
        store.save(
            StoredSnapshot(
                aggregate_id="WORK-001",
                aggregate_type="WorkItem",
                version=1,
                state=complex_state,
            )
        )
        loaded = store.load("WORK-001")
        assert loaded.state == complex_state

    def test_unicode_in_state(self) -> None:
        """Unicode in state is preserved."""
        store = InMemorySnapshotStore()
        store.save(
            StoredSnapshot(
                aggregate_id="WORK-001",
                aggregate_type="WorkItem",
                version=1,
                state={"title": "日本語テスト", "emoji": "🎉"},
            )
        )
        loaded = store.load("WORK-001")
        assert loaded.state["title"] == "日本語テスト"
        assert loaded.state["emoji"] == "🎉"

    def test_large_state(self) -> None:
        """Large state is handled correctly."""
        store = InMemorySnapshotStore()
        large_state = {"data": list(range(10000))}
        store.save(
            StoredSnapshot(
                aggregate_id="WORK-001",
                aggregate_type="WorkItem",
                version=1,
                state=large_state,
            )
        )
        loaded = store.load("WORK-001")
        assert len(loaded.state["data"]) == 10000

    def test_version_at_boundary(self) -> None:
        """Version at int boundary works."""
        store = InMemorySnapshotStore()
        store.save(
            StoredSnapshot(
                aggregate_id="WORK-001",
                aggregate_type="WorkItem",
                version=2**31 - 1,  # Max 32-bit signed int
                state={},
            )
        )
        loaded = store.load("WORK-001")
        assert loaded.version == 2**31 - 1
