"""Unit tests for FileRepository infrastructure adapter.

Test Categories:
    - Protocol Compliance: IRepository implementation
    - Get Operations: Retrieve aggregates
    - Save Operations: Persist aggregates
    - Delete Operations: Remove aggregates
    - Concurrency: Version checking
    - Edge Cases: Boundary conditions

References:
    - IMPL-REPO-003: FileRepository<T>
    - PAT-009: Generic Repository Port
    - PAT-010: Composed Infrastructure Adapters
"""
from __future__ import annotations

from typing import Any

import pytest

from src.infrastructure.adapters.file_repository import FileRepository
from src.infrastructure.internal.file_store import InMemoryFileStore
from src.infrastructure.internal.serializer import JsonSerializer
from src.work_tracking.domain.aggregates.base import AggregateRoot
from src.work_tracking.domain.ports.repository import (
    AggregateNotFoundError,
    ConcurrencyError,
)


# =============================================================================
# Test Fixtures - Simple Aggregate for Testing
# =============================================================================


class SampleAggregate(AggregateRoot):
    """Simple aggregate for testing repository operations."""

    _aggregate_type = "SampleAggregate"

    def __init__(self, id: str, title: str = "", status: str = "pending") -> None:
        """Initialize test aggregate."""
        super().__init__(id)
        self._title = title
        self._status = status
        self._items: list[str] = []

    @property
    def title(self) -> str:
        """Get title."""
        return self._title

    @property
    def status(self) -> str:
        """Get status."""
        return self._status

    @property
    def items(self) -> list[str]:
        """Get items."""
        return self._items.copy()

    @classmethod
    def create(cls, id: str, title: str) -> SampleAggregate:
        """Factory method to create a new aggregate."""
        aggregate = cls(id=id, title=title)
        aggregate._version = 1
        return aggregate

    def _apply(self, event: Any) -> None:
        """Apply event (no-op for test aggregate)."""
        pass

    def update_title(self, new_title: str) -> None:
        """Update the title."""
        self._title = new_title
        self._version += 1

    def complete(self) -> None:
        """Mark as complete."""
        self._status = "completed"
        self._version += 1

    def add_item(self, item: str) -> None:
        """Add an item to the list."""
        self._items.append(item)
        self._version += 1

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "title": self._title,
            "status": self._status,
            "items": self._items,
            "version": self._version,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SampleAggregate:
        """Deserialize from dictionary."""
        aggregate = cls(
            id=data["id"],
            title=data.get("title", ""),
            status=data.get("status", "pending"),
        )
        aggregate._items = data.get("items", [])
        aggregate._version = data.get("version", 1)
        return aggregate


@pytest.fixture
def file_store() -> InMemoryFileStore:
    """Provide a fresh in-memory file store."""
    return InMemoryFileStore()


@pytest.fixture
def serializer() -> JsonSerializer[SampleAggregate]:
    """Provide a JSON serializer for SampleAggregate."""
    return JsonSerializer[SampleAggregate]()


@pytest.fixture
def repository(
    file_store: InMemoryFileStore, serializer: JsonSerializer[SampleAggregate]
) -> FileRepository[SampleAggregate, str]:
    """Provide a file repository with in-memory backing."""
    return FileRepository(
        file_store=file_store,
        serializer=serializer,
        aggregate_type=SampleAggregate,
        base_path="test_aggregates",
        id_extractor=lambda agg: agg.id,
    )


# =============================================================================
# Protocol Compliance Tests
# =============================================================================


class TestFileRepositoryProtocol:
    """Tests for IRepository protocol compliance."""

    def test_implements_protocol(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """FileRepository implements IRepository."""
        assert hasattr(repository, "get")
        assert hasattr(repository, "get_or_raise")
        assert hasattr(repository, "save")
        assert hasattr(repository, "delete")
        assert hasattr(repository, "exists")

    def test_protocol_methods_callable(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """All protocol methods are callable."""
        assert callable(repository.get)
        assert callable(repository.get_or_raise)
        assert callable(repository.save)
        assert callable(repository.delete)
        assert callable(repository.exists)


# =============================================================================
# Get Operations Tests
# =============================================================================


class TestFileRepositoryGet:
    """Tests for get operations."""

    def test_get_returns_none_when_not_found(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """get() returns None for non-existent aggregate."""
        result = repository.get("nonexistent-id")
        assert result is None

    def test_get_returns_saved_aggregate(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """get() returns previously saved aggregate."""
        aggregate = SampleAggregate.create("TEST-001", "Test Title")
        repository.save(aggregate)

        result = repository.get("TEST-001")
        assert result is not None
        assert result.id == "TEST-001"
        assert result.title == "Test Title"

    def test_get_returns_latest_version(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """get() returns the latest version after updates."""
        aggregate = SampleAggregate.create("TEST-001", "Original")
        repository.save(aggregate)

        aggregate.update_title("Updated")
        repository.save(aggregate)

        result = repository.get("TEST-001")
        assert result is not None
        assert result.title == "Updated"


class TestFileRepositoryGetOrRaise:
    """Tests for get_or_raise operations."""

    def test_get_or_raise_returns_aggregate_when_found(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """get_or_raise() returns aggregate when it exists."""
        aggregate = SampleAggregate.create("TEST-001", "Test Title")
        repository.save(aggregate)

        result = repository.get_or_raise("TEST-001")
        assert result.id == "TEST-001"
        assert result.title == "Test Title"

    def test_get_or_raise_raises_when_not_found(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """get_or_raise() raises AggregateNotFoundError when missing."""
        with pytest.raises(AggregateNotFoundError) as exc_info:
            repository.get_or_raise("nonexistent-id")

        assert "nonexistent-id" in str(exc_info.value)


# =============================================================================
# Save Operations Tests
# =============================================================================


class TestFileRepositorySave:
    """Tests for save operations."""

    def test_save_new_aggregate(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """Can save a new aggregate."""
        aggregate = SampleAggregate.create("TEST-001", "New Task")
        repository.save(aggregate)

        assert repository.exists("TEST-001")

    def test_save_updates_existing_aggregate(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """Can update an existing aggregate."""
        aggregate = SampleAggregate.create("TEST-001", "Original")
        repository.save(aggregate)

        aggregate.update_title("Updated")
        repository.save(aggregate)

        result = repository.get("TEST-001")
        assert result is not None
        assert result.title == "Updated"

    def test_save_preserves_complex_state(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """Save preserves complex nested state."""
        aggregate = SampleAggregate.create("TEST-001", "Task")
        aggregate.add_item("item1")
        aggregate.add_item("item2")
        aggregate.complete()
        repository.save(aggregate)

        result = repository.get("TEST-001")
        assert result is not None
        assert result.items == ["item1", "item2"]
        assert result.status == "completed"

    def test_save_multiple_aggregates(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """Can save multiple different aggregates."""
        agg1 = SampleAggregate.create("TEST-001", "First")
        agg2 = SampleAggregate.create("TEST-002", "Second")
        agg3 = SampleAggregate.create("TEST-003", "Third")

        repository.save(agg1)
        repository.save(agg2)
        repository.save(agg3)

        assert repository.exists("TEST-001")
        assert repository.exists("TEST-002")
        assert repository.exists("TEST-003")


# =============================================================================
# Delete Operations Tests
# =============================================================================


class TestFileRepositoryDelete:
    """Tests for delete operations."""

    def test_delete_existing_returns_true(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """delete() returns True for existing aggregate."""
        aggregate = SampleAggregate.create("TEST-001", "Task")
        repository.save(aggregate)

        result = repository.delete("TEST-001")
        assert result is True
        assert not repository.exists("TEST-001")

    def test_delete_nonexistent_returns_false(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """delete() returns False for non-existent aggregate."""
        result = repository.delete("nonexistent-id")
        assert result is False

    def test_delete_then_get_returns_none(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """get() returns None after delete."""
        aggregate = SampleAggregate.create("TEST-001", "Task")
        repository.save(aggregate)
        repository.delete("TEST-001")

        result = repository.get("TEST-001")
        assert result is None


# =============================================================================
# Exists Operations Tests
# =============================================================================


class TestFileRepositoryExists:
    """Tests for exists operations."""

    def test_exists_returns_true_for_saved(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """exists() returns True for saved aggregates."""
        aggregate = SampleAggregate.create("TEST-001", "Task")
        repository.save(aggregate)

        assert repository.exists("TEST-001") is True

    def test_exists_returns_false_for_new(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """exists() returns False for non-existent."""
        assert repository.exists("nonexistent-id") is False


# =============================================================================
# Concurrency Tests
# =============================================================================


class TestFileRepositoryConcurrency:
    """Tests for concurrency handling."""

    def test_save_detects_version_behind_storage(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """save() detects when aggregate version is behind storage version."""
        # Save initial version
        aggregate = SampleAggregate.create("TEST-001", "Original")
        repository.save(aggregate)

        # Load the aggregate
        loaded = repository.get("TEST-001")
        assert loaded is not None

        # Meanwhile, someone else updates and saves (simulated by direct modification)
        other_session = repository.get("TEST-001")
        assert other_session is not None
        other_session.update_title("Updated by other")
        other_session.update_title("Updated again")  # Now at v3
        repository.save(other_session)

        # Our loaded aggregate is still at v1, doesn't know about v3
        # Trying to save our old version should fail
        with pytest.raises(ConcurrencyError) as exc_info:
            repository.save(loaded)

        assert "TEST-001" in str(exc_info.value)


class TestFileRepositoryVersionTracking:
    """Tests for version tracking."""

    def test_version_increments_on_save(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """Version increments are preserved through save/load cycle."""
        aggregate = SampleAggregate.create("TEST-001", "Task")
        assert aggregate.version == 1

        repository.save(aggregate)

        loaded = repository.get("TEST-001")
        assert loaded is not None
        assert loaded.version == 1

        loaded.update_title("Updated")
        assert loaded.version == 2
        repository.save(loaded)

        reloaded = repository.get("TEST-001")
        assert reloaded is not None
        assert reloaded.version == 2


# =============================================================================
# Edge Cases Tests
# =============================================================================


class TestFileRepositoryEdgeCases:
    """Edge case tests for file repository."""

    def test_short_aggregate_id(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """Handles short ID string."""
        aggregate = SampleAggregate.create("X", "Short ID")
        repository.save(aggregate)
        result = repository.get("X")
        assert result is not None
        assert result.title == "Short ID"

    def test_special_characters_in_id(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """Handles special characters in ID."""
        aggregate = SampleAggregate.create("TEST/001:special", "Special ID")
        repository.save(aggregate)
        result = repository.get("TEST/001:special")
        assert result is not None
        assert result.id == "TEST/001:special"

    def test_unicode_in_title(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """Handles unicode content."""
        aggregate = SampleAggregate.create("TEST-001", "日本語テスト 🎉")
        repository.save(aggregate)
        result = repository.get("TEST-001")
        assert result is not None
        assert result.title == "日本語テスト 🎉"

    def test_large_aggregate(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """Handles large aggregate with many items."""
        aggregate = SampleAggregate.create("TEST-001", "Large")
        for i in range(1000):
            aggregate.add_item(f"item-{i}")
        repository.save(aggregate)

        result = repository.get("TEST-001")
        assert result is not None
        assert len(result.items) == 1000

    def test_save_same_aggregate_twice(
        self, repository: FileRepository[SampleAggregate, str]
    ) -> None:
        """Can save same aggregate instance twice if no changes."""
        aggregate = SampleAggregate.create("TEST-001", "Task")
        repository.save(aggregate)

        # Save again without modification should work
        # (version check passes as version matches)
        repository.save(aggregate)

        result = repository.get("TEST-001")
        assert result is not None
        assert result.title == "Task"
