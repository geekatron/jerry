"""Unit tests for EventSourcedWorkItemRepository.

Test Categories:
    - Happy Path: Normal CRUD operations
    - Edge Cases: Empty stores, multiple items
    - Event Reconstitution: History replay
    - Concurrency: Version handling
    - Protocol Compliance: IWorkItemRepository contract

References:
    - PAT-REPO-002: Event-Sourced Repository Pattern
    - TD-018: Event Sourcing for WorkItem Repository
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.work_tracking.domain.aggregates.work_item import WorkItem
from src.work_tracking.domain.ports.repository import AggregateNotFoundError
from src.work_tracking.domain.value_objects import Priority, WorkItemId, WorkItemStatus, WorkType
from src.work_tracking.infrastructure.adapters.event_sourced_work_item_repository import (
    EventSourcedWorkItemRepository,
)
from src.work_tracking.infrastructure.persistence.filesystem_event_store import (
    FileSystemEventStore,
)
from src.work_tracking.infrastructure.persistence.in_memory_event_store import (
    InMemoryEventStore,
)


def create_work_item_id(internal_id: int) -> WorkItemId:
    """Helper to create a WorkItemId."""
    return WorkItemId.create(internal_id, 1)


def create_work_item(
    internal_id: int = 1,
    title: str = "Test Work Item",
    work_type: WorkType = WorkType.TASK,
    priority: Priority = Priority.MEDIUM,
) -> WorkItem:
    """Helper to create a WorkItem for testing."""
    return WorkItem.create(
        id=create_work_item_id(internal_id),
        title=title,
        work_type=work_type,
        priority=priority,
    )


@pytest.fixture
def in_memory_store() -> InMemoryEventStore:
    """Create an InMemoryEventStore for testing."""
    return InMemoryEventStore()


@pytest.fixture
def repository(in_memory_store: InMemoryEventStore) -> EventSourcedWorkItemRepository:
    """Create a repository with in-memory event store."""
    return EventSourcedWorkItemRepository(in_memory_store)


@pytest.fixture
def temp_store_path(tmp_path: Path) -> Path:
    """Create a temporary directory for filesystem tests."""
    return tmp_path / "test_project"


@pytest.fixture
def filesystem_repository(temp_store_path: Path) -> EventSourcedWorkItemRepository:
    """Create a repository with filesystem event store."""
    store = FileSystemEventStore(temp_store_path)
    return EventSourcedWorkItemRepository(store)


class TestEventSourcedRepositorySaveAndGet:
    """Tests for save and get operations."""

    def test_save_and_get_work_item(self, repository: EventSourcedWorkItemRepository) -> None:
        """Can save and retrieve a work item."""
        work_item = create_work_item(internal_id=1, title="Test Task")

        repository.save(work_item)
        loaded = repository.get(work_item.id)

        assert loaded is not None
        assert loaded.id == work_item.id
        assert loaded.title == "Test Task"

    def test_get_nonexistent_returns_none(self, repository: EventSourcedWorkItemRepository) -> None:
        """get() returns None for non-existent item."""
        result = repository.get("nonexistent")
        assert result is None

    def test_get_or_raise_returns_item(self, repository: EventSourcedWorkItemRepository) -> None:
        """get_or_raise() returns existing item."""
        work_item = create_work_item(internal_id=2)
        repository.save(work_item)

        loaded = repository.get_or_raise(work_item.id)
        assert loaded.id == work_item.id

    def test_get_or_raise_raises_for_nonexistent(
        self, repository: EventSourcedWorkItemRepository
    ) -> None:
        """get_or_raise() raises AggregateNotFoundError for non-existent item."""
        with pytest.raises(AggregateNotFoundError) as exc_info:
            repository.get_or_raise("nonexistent")

        assert exc_info.value.aggregate_id == "nonexistent"

    def test_save_preserves_all_fields(self, repository: EventSourcedWorkItemRepository) -> None:
        """save() preserves all work item fields."""
        work_item = create_work_item(
            internal_id=3,
            title="Feature Implementation",
            work_type=WorkType.STORY,
            priority=Priority.HIGH,
        )

        repository.save(work_item)
        loaded = repository.get(work_item.id)

        assert loaded is not None
        assert loaded.title == "Feature Implementation"
        assert loaded.work_type == WorkType.STORY
        assert loaded.priority == Priority.HIGH
        assert loaded.status == WorkItemStatus.PENDING


class TestEventSourcedRepositoryReconstitution:
    """Tests for event history replay and reconstitution."""

    def test_reconstitutes_after_status_change(
        self, repository: EventSourcedWorkItemRepository
    ) -> None:
        """WorkItem state is correctly reconstituted after status changes."""
        work_item = create_work_item(internal_id=4)
        work_item.start_work()
        repository.save(work_item)

        loaded = repository.get(work_item.id)

        assert loaded is not None
        assert loaded.status == WorkItemStatus.IN_PROGRESS

    def test_reconstitutes_after_multiple_operations(
        self, repository: EventSourcedWorkItemRepository
    ) -> None:
        """WorkItem state is correctly reconstituted after multiple operations."""
        work_item = create_work_item(internal_id=5)
        repository.save(work_item)

        # Modify the work item
        work_item.start_work()
        work_item.change_priority(Priority.CRITICAL)
        repository.save(work_item)

        loaded = repository.get(work_item.id)

        assert loaded is not None
        assert loaded.status == WorkItemStatus.IN_PROGRESS
        assert loaded.priority == Priority.CRITICAL

    def test_version_increments_with_events(
        self, repository: EventSourcedWorkItemRepository
    ) -> None:
        """WorkItem version increments correctly with each event."""
        work_item = create_work_item(internal_id=6)
        repository.save(work_item)

        loaded = repository.get(work_item.id)
        assert loaded is not None
        # Version 1 from WorkItemCreated
        assert loaded.version == 1

        work_item.start_work()  # Version 2
        repository.save(work_item)

        loaded = repository.get(work_item.id)
        assert loaded is not None
        assert loaded.version == 2


class TestEventSourcedRepositoryDelete:
    """Tests for delete operation."""

    def test_delete_existing_item(self, repository: EventSourcedWorkItemRepository) -> None:
        """delete() removes item and returns True."""
        work_item = create_work_item(internal_id=7)
        repository.save(work_item)

        result = repository.delete(work_item.id)

        assert result is True
        assert repository.get(work_item.id) is None

    def test_delete_nonexistent_returns_false(
        self, repository: EventSourcedWorkItemRepository
    ) -> None:
        """delete() returns False for non-existent item."""
        result = repository.delete("nonexistent")
        assert result is False


class TestEventSourcedRepositoryExists:
    """Tests for exists operation."""

    def test_exists_returns_true_for_existing(
        self, repository: EventSourcedWorkItemRepository
    ) -> None:
        """exists() returns True for existing item."""
        work_item = create_work_item(internal_id=8)
        repository.save(work_item)

        assert repository.exists(work_item.id) is True

    def test_exists_returns_false_for_nonexistent(
        self, repository: EventSourcedWorkItemRepository
    ) -> None:
        """exists() returns False for non-existent item."""
        assert repository.exists("nonexistent") is False


class TestEventSourcedRepositoryListAll:
    """Tests for list_all operation."""

    def test_list_all_empty_repository(self, repository: EventSourcedWorkItemRepository) -> None:
        """list_all() returns empty list for empty repository."""
        result = repository.list_all()
        assert result == []

    def test_list_all_returns_all_items(self, repository: EventSourcedWorkItemRepository) -> None:
        """list_all() returns all saved items."""
        item1 = create_work_item(internal_id=10, title="Item 1")
        item2 = create_work_item(internal_id=11, title="Item 2")
        item3 = create_work_item(internal_id=12, title="Item 3")

        repository.save(item1)
        repository.save(item2)
        repository.save(item3)

        result = repository.list_all()

        assert len(result) == 3
        titles = {item.title for item in result}
        assert titles == {"Item 1", "Item 2", "Item 3"}

    def test_list_all_filters_by_status(self, repository: EventSourcedWorkItemRepository) -> None:
        """list_all() filters by status correctly."""
        pending_item = create_work_item(internal_id=13, title="Pending")
        in_progress_item = create_work_item(internal_id=14, title="In Progress")
        in_progress_item.start_work()

        repository.save(pending_item)
        repository.save(in_progress_item)

        pending_result = repository.list_all(status=WorkItemStatus.PENDING)
        in_progress_result = repository.list_all(status=WorkItemStatus.IN_PROGRESS)

        assert len(pending_result) == 1
        assert pending_result[0].title == "Pending"
        assert len(in_progress_result) == 1
        assert in_progress_result[0].title == "In Progress"

    def test_list_all_respects_limit(self, repository: EventSourcedWorkItemRepository) -> None:
        """list_all() respects limit parameter."""
        for i in range(5):
            item = create_work_item(internal_id=20 + i, title=f"Item {i}")
            repository.save(item)

        result = repository.list_all(limit=3)

        assert len(result) == 3


class TestEventSourcedRepositoryCount:
    """Tests for count operation."""

    def test_count_empty_repository(self, repository: EventSourcedWorkItemRepository) -> None:
        """count() returns 0 for empty repository."""
        assert repository.count() == 0

    def test_count_all_items(self, repository: EventSourcedWorkItemRepository) -> None:
        """count() returns total item count."""
        for i in range(3):
            item = create_work_item(internal_id=30 + i)
            repository.save(item)

        assert repository.count() == 3

    def test_count_filters_by_status(self, repository: EventSourcedWorkItemRepository) -> None:
        """count() filters by status correctly."""
        pending_item = create_work_item(internal_id=33)
        in_progress_item = create_work_item(internal_id=34)
        in_progress_item.start_work()

        repository.save(pending_item)
        repository.save(in_progress_item)

        assert repository.count(status=WorkItemStatus.PENDING) == 1
        assert repository.count(status=WorkItemStatus.IN_PROGRESS) == 1


class TestEventSourcedRepositoryClear:
    """Tests for clear operation."""

    def test_clear_removes_all_items(self, repository: EventSourcedWorkItemRepository) -> None:
        """clear() removes all items."""
        for i in range(3):
            item = create_work_item(internal_id=40 + i)
            repository.save(item)

        repository.clear()

        assert repository.count() == 0
        assert repository.list_all() == []


class TestEventSourcedRepositoryWithFileSystem:
    """Tests with FileSystemEventStore for persistence."""

    def test_items_persist_across_repository_instances(self, temp_store_path: Path) -> None:
        """Items persist when repository is recreated."""
        store1 = FileSystemEventStore(temp_store_path)
        repo1 = EventSourcedWorkItemRepository(store1)

        work_item = create_work_item(internal_id=50, title="Persistent Item")
        repo1.save(work_item)
        del repo1, store1

        # Create new instances
        store2 = FileSystemEventStore(temp_store_path)
        repo2 = EventSourcedWorkItemRepository(store2)

        loaded = repo2.get(work_item.id)

        assert loaded is not None
        assert loaded.title == "Persistent Item"

    def test_state_reconstitutes_after_persistence(self, temp_store_path: Path) -> None:
        """Full state reconstitutes correctly after persistence."""
        store1 = FileSystemEventStore(temp_store_path)
        repo1 = EventSourcedWorkItemRepository(store1)

        work_item = create_work_item(internal_id=51, title="Stateful Item")
        work_item.start_work()
        work_item.change_priority(Priority.HIGH)
        repo1.save(work_item)
        del repo1, store1

        # Create new instances
        store2 = FileSystemEventStore(temp_store_path)
        repo2 = EventSourcedWorkItemRepository(store2)

        loaded = repo2.get(work_item.id)

        assert loaded is not None
        assert loaded.status == WorkItemStatus.IN_PROGRESS
        assert loaded.priority == Priority.HIGH


class TestEventSourcedRepositoryProtocolCompliance:
    """Tests for IWorkItemRepository protocol compliance."""

    def test_has_get_method(self, repository: EventSourcedWorkItemRepository) -> None:
        """Repository has get method."""
        assert callable(repository.get)

    def test_has_get_or_raise_method(self, repository: EventSourcedWorkItemRepository) -> None:
        """Repository has get_or_raise method."""
        assert callable(repository.get_or_raise)

    def test_has_save_method(self, repository: EventSourcedWorkItemRepository) -> None:
        """Repository has save method."""
        assert callable(repository.save)

    def test_has_delete_method(self, repository: EventSourcedWorkItemRepository) -> None:
        """Repository has delete method."""
        assert callable(repository.delete)

    def test_has_exists_method(self, repository: EventSourcedWorkItemRepository) -> None:
        """Repository has exists method."""
        assert callable(repository.exists)

    def test_has_list_all_method(self, repository: EventSourcedWorkItemRepository) -> None:
        """Repository has list_all method."""
        assert callable(repository.list_all)

    def test_has_count_method(self, repository: EventSourcedWorkItemRepository) -> None:
        """Repository has count method."""
        assert callable(repository.count)
