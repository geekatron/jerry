"""Unit tests for Work Item Query Handlers.

Test Categories:
    - ListWorkItemsQueryHandler: List work items with filtering
    - GetWorkItemQueryHandler: Get single work item by ID

References:
    - ENFORCE-009: Application Layer Tests
    - CQRS Pattern: Queries return DTOs

Test Matrix:
    Happy Path:
        - list_all returns WorkItemListDTO
        - list with status filter returns filtered items
        - list with limit returns limited items
        - get returns WorkItemDetailDTO
    Negative:
        - get non-existent ID raises error
        - list with invalid status returns empty
    Edge:
        - list empty repository returns empty result
        - list with pagination info
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from src.work_tracking.application.handlers.queries import (
    GetWorkItemQueryHandler,
    ListWorkItemsQueryHandler,
    WorkItemDetailDTO,
    WorkItemDTO,
    WorkItemListDTO,
)
from src.work_tracking.application.handlers.queries.get_work_item_query_handler import (
    WorkItemNotFoundError,
)
from src.work_tracking.application.queries import (
    GetWorkItemQuery,
    ListWorkItemsQuery,
)
from src.work_tracking.domain.aggregates.work_item import WorkItem
from src.work_tracking.domain.value_objects import (
    Priority,
    WorkItemId,
    WorkItemStatus,
    WorkType,
)

# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def mock_repository() -> Mock:
    """Create a mock IWorkItemRepository."""
    return Mock()


@pytest.fixture
def sample_work_item() -> WorkItem:
    """Create a sample work item for testing."""
    item = WorkItem.create(
        id=WorkItemId.create(12345, 1),
        title="Sample task",
        description="A sample task description",
        work_type=WorkType.TASK,
        priority=Priority.HIGH,
    )
    # Clear creation events
    item.collect_events()
    return item


@pytest.fixture
def in_progress_work_item() -> WorkItem:
    """Create a work item in progress."""
    item = WorkItem.create(
        id=WorkItemId.create(12346, 2),
        title="In progress task",
        work_type=WorkType.TASK,
        priority=Priority.MEDIUM,
    )
    item.start_work()
    item.collect_events()
    return item


# =============================================================================
# ListWorkItemsQueryHandler Tests
# =============================================================================


class TestListWorkItemsQueryHandlerHappyPath:
    """Happy path tests for ListWorkItemsQueryHandler."""

    def test_list_returns_work_item_list_dto(
        self, mock_repository: Mock, sample_work_item: WorkItem
    ) -> None:
        """list should return WorkItemListDTO."""
        mock_repository.list_all.return_value = [sample_work_item]
        mock_repository.count.return_value = 1

        handler = ListWorkItemsQueryHandler(repository=mock_repository)
        query = ListWorkItemsQuery()
        result = handler.handle(query)

        assert isinstance(result, WorkItemListDTO)
        assert len(result.items) == 1
        assert result.total_count == 1

    def test_list_converts_items_to_dtos(
        self, mock_repository: Mock, sample_work_item: WorkItem
    ) -> None:
        """list should convert WorkItem to WorkItemDTO."""
        mock_repository.list_all.return_value = [sample_work_item]
        mock_repository.count.return_value = 1

        handler = ListWorkItemsQueryHandler(repository=mock_repository)
        query = ListWorkItemsQuery()
        result = handler.handle(query)

        item_dto = result.items[0]
        assert isinstance(item_dto, WorkItemDTO)
        assert item_dto.id == sample_work_item.id
        assert item_dto.title == "Sample task"
        assert item_dto.status == "pending"
        assert item_dto.priority == "high"
        assert item_dto.work_type == "task"

    def test_list_with_status_filter(
        self, mock_repository: Mock, in_progress_work_item: WorkItem
    ) -> None:
        """list should filter by status."""
        mock_repository.list_all.return_value = [in_progress_work_item]
        mock_repository.count.return_value = 1

        handler = ListWorkItemsQueryHandler(repository=mock_repository)
        query = ListWorkItemsQuery(status="in_progress")
        result = handler.handle(query)

        mock_repository.list_all.assert_called_once_with(
            status=WorkItemStatus.IN_PROGRESS,
            limit=None,
        )
        assert len(result.items) == 1

    def test_list_with_limit(self, mock_repository: Mock, sample_work_item: WorkItem) -> None:
        """list should respect limit parameter."""
        mock_repository.list_all.return_value = [sample_work_item]
        mock_repository.count.return_value = 5  # More items exist

        handler = ListWorkItemsQueryHandler(repository=mock_repository)
        query = ListWorkItemsQuery(limit=1)
        result = handler.handle(query)

        mock_repository.list_all.assert_called_once_with(
            status=None,
            limit=1,
        )
        assert result.has_more is True
        assert result.total_count == 5


class TestListWorkItemsQueryHandlerNegative:
    """Negative tests for ListWorkItemsQueryHandler."""

    def test_list_with_invalid_status_returns_empty(self, mock_repository: Mock) -> None:
        """list with invalid status should return empty result."""
        handler = ListWorkItemsQueryHandler(repository=mock_repository)
        query = ListWorkItemsQuery(status="invalid_status")
        result = handler.handle(query)

        assert len(result.items) == 0
        assert result.total_count == 0
        # Repository should not be called for invalid status
        mock_repository.list_all.assert_not_called()


class TestListWorkItemsQueryHandlerEdge:
    """Edge case tests for ListWorkItemsQueryHandler."""

    def test_list_empty_repository_returns_empty_result(self, mock_repository: Mock) -> None:
        """list on empty repository should return empty result."""
        mock_repository.list_all.return_value = []
        mock_repository.count.return_value = 0

        handler = ListWorkItemsQueryHandler(repository=mock_repository)
        query = ListWorkItemsQuery()
        result = handler.handle(query)

        assert len(result.items) == 0
        assert result.total_count == 0
        assert result.has_more is False

    def test_list_pagination_shows_has_more(
        self, mock_repository: Mock, sample_work_item: WorkItem
    ) -> None:
        """list should show has_more when more items exist."""
        mock_repository.list_all.return_value = [sample_work_item]
        mock_repository.count.return_value = 10  # 10 total, showing 1

        handler = ListWorkItemsQueryHandler(repository=mock_repository)
        query = ListWorkItemsQuery(limit=1)
        result = handler.handle(query)

        assert result.has_more is True
        assert len(result.items) == 1
        assert result.total_count == 10


# =============================================================================
# GetWorkItemQueryHandler Tests
# =============================================================================


class TestGetWorkItemQueryHandlerHappyPath:
    """Happy path tests for GetWorkItemQueryHandler."""

    def test_get_returns_work_item_detail_dto(
        self, mock_repository: Mock, sample_work_item: WorkItem
    ) -> None:
        """get should return WorkItemDetailDTO."""
        mock_repository.get.return_value = sample_work_item

        handler = GetWorkItemQueryHandler(repository=mock_repository)
        query = GetWorkItemQuery(work_item_id=sample_work_item.id)
        result = handler.handle(query)

        assert isinstance(result, WorkItemDetailDTO)
        assert result.id == sample_work_item.id

    def test_get_includes_all_fields(
        self, mock_repository: Mock, sample_work_item: WorkItem
    ) -> None:
        """get should include all work item fields."""
        mock_repository.get.return_value = sample_work_item

        handler = GetWorkItemQueryHandler(repository=mock_repository)
        query = GetWorkItemQuery(work_item_id=sample_work_item.id)
        result = handler.handle(query)

        assert result.title == "Sample task"
        assert result.description == "A sample task description"
        assert result.status == "pending"
        assert result.priority == "high"
        assert result.work_type == "task"

    def test_get_includes_optional_fields(
        self, mock_repository: Mock, sample_work_item: WorkItem
    ) -> None:
        """get should include optional fields when present."""
        # Assign and add dependency
        sample_work_item.assign("test-agent")
        sample_work_item.collect_events()
        mock_repository.get.return_value = sample_work_item

        handler = GetWorkItemQueryHandler(repository=mock_repository)
        query = GetWorkItemQuery(work_item_id=sample_work_item.id)
        result = handler.handle(query)

        assert result.assignee == "test-agent"


class TestGetWorkItemQueryHandlerNegative:
    """Negative tests for GetWorkItemQueryHandler."""

    def test_get_nonexistent_raises_error(self, mock_repository: Mock) -> None:
        """get non-existent ID should raise WorkItemNotFoundError."""
        mock_repository.get.return_value = None

        handler = GetWorkItemQueryHandler(repository=mock_repository)
        query = GetWorkItemQuery(work_item_id="nonexistent")

        with pytest.raises(WorkItemNotFoundError) as exc_info:
            handler.handle(query)

        assert "nonexistent" in str(exc_info.value)


class TestGetWorkItemQueryHandlerEdge:
    """Edge case tests for GetWorkItemQueryHandler."""

    def test_get_completed_item_includes_completion_time(self, mock_repository: Mock) -> None:
        """get should include completed_at for completed items."""
        item = WorkItem.create(
            id=WorkItemId.create(99999, 1),
            title="Completed task",
            work_type=WorkType.SPIKE,  # SPIKE doesn't require quality gates
        )
        item.start_work()
        item.complete()
        item.collect_events()
        mock_repository.get.return_value = item

        handler = GetWorkItemQueryHandler(repository=mock_repository)
        query = GetWorkItemQuery(work_item_id=item.id)
        result = handler.handle(query)

        assert result.status == "done"
        assert result.completed_at is not None
