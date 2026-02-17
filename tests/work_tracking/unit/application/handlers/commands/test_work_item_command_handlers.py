# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for Work Item Command Handlers.

Test Categories:
    - CreateWorkItemCommandHandler: Create new work items
    - StartWorkItemCommandHandler: Start work on items
    - CompleteWorkItemCommandHandler: Complete work items
    - BlockWorkItemCommandHandler: Block work items
    - CancelWorkItemCommandHandler: Cancel work items

References:
    - PHASE-45-ITEMS-COMMANDS.md: Implementation tracker
    - PAT-CQRS-001: Command Pattern

Test Matrix:
    Happy Path:
        - Handlers create/modify work items correctly
        - Handlers return domain events
        - Handlers persist via repository
    Negative:
        - Handlers raise AggregateNotFoundError for missing items
        - Handlers raise InvalidStateTransitionError for invalid transitions
    Edge:
        - Empty optional fields
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from src.work_tracking.application.commands import (
    BlockWorkItemCommand,
    CancelWorkItemCommand,
    CompleteWorkItemCommand,
    CreateWorkItemCommand,
    StartWorkItemCommand,
)
from src.work_tracking.application.handlers.commands import (
    BlockWorkItemCommandHandler,
    CancelWorkItemCommandHandler,
    CompleteWorkItemCommandHandler,
    CreateWorkItemCommandHandler,
    StartWorkItemCommandHandler,
)
from src.work_tracking.domain.aggregates.work_item import WorkItem
from src.work_tracking.domain.events import StatusChanged, WorkItemCreated
from src.work_tracking.domain.ports.repository import AggregateNotFoundError
from src.work_tracking.domain.value_objects import (
    Priority,
    WorkItemId,
    WorkType,
)
from src.work_tracking.domain.value_objects.work_item_status import (
    InvalidStateTransitionError,
)

# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def mock_repository() -> Mock:
    """Create a mock IWorkItemRepository.

    The save() method is configured to return events from the work item,
    matching the real repository behavior where save() calls collect_events()
    and returns the persisted events.
    """
    repo = Mock()

    def save_side_effect(work_item: WorkItem) -> list:
        """Extract and return events from the work item."""
        return list(work_item.collect_events())

    repo.save.side_effect = save_side_effect
    return repo


@pytest.fixture
def mock_id_generator() -> Mock:
    """Create a mock IWorkItemIdGenerator."""
    generator = Mock()
    generator.create.return_value = WorkItemId.create(12345, 1)
    return generator


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
    """Create a work item in IN_PROGRESS status."""
    item = WorkItem.create(
        id=WorkItemId.create(12345, 2),
        title="In progress task",
        work_type=WorkType.TASK,
        priority=Priority.MEDIUM,
    )
    item.collect_events()  # Clear creation events
    item.start_work()
    item.collect_events()  # Clear start events
    return item


@pytest.fixture
def completable_work_item() -> WorkItem:
    """Create a work item in IN_PROGRESS status with quality metrics."""
    from src.work_tracking.domain.value_objects import Coverage, TypeRatio

    item = WorkItem.create(
        id=WorkItemId.create(12345, 3),
        title="Completable task",
        work_type=WorkType.TASK,
        priority=Priority.MEDIUM,
    )
    item.collect_events()
    item.start_work()
    item.collect_events()
    # Add quality metrics so it can be completed
    item.update_quality_metrics(
        coverage=Coverage(percent=80.0),
        ratio=TypeRatio(positive=5, negative=2, edge_case=1),
    )
    item.collect_events()
    return item


@pytest.fixture
def done_work_item() -> WorkItem:
    """Create a work item in DONE status."""
    from src.work_tracking.domain.value_objects import Coverage, TypeRatio

    item = WorkItem.create(
        id=WorkItemId.create(12345, 4),
        title="Completed task",
        work_type=WorkType.TASK,
        priority=Priority.MEDIUM,
    )
    item.collect_events()
    item.start_work()
    item.collect_events()
    item.update_quality_metrics(
        coverage=Coverage(percent=80.0),
        ratio=TypeRatio(positive=5, negative=2, edge_case=1),
    )
    item.collect_events()
    item.complete()
    item.collect_events()
    return item


# =============================================================================
# CreateWorkItemCommandHandler Tests
# =============================================================================


class TestCreateWorkItemCommandHandler:
    """Tests for CreateWorkItemCommandHandler."""

    def test_create_work_item_success(
        self,
        mock_repository: Mock,
        mock_id_generator: Mock,
    ) -> None:
        """Handler creates work item and returns WorkItemCreated event."""
        handler = CreateWorkItemCommandHandler(
            repository=mock_repository,
            id_generator=mock_id_generator,
        )
        command = CreateWorkItemCommand(
            title="New task",
            work_type="task",
            priority="high",
            description="Task description",
        )

        events = handler.handle(command)

        # Verify event returned
        assert len(events) == 1
        assert isinstance(events[0], WorkItemCreated)
        assert events[0].title == "New task"
        assert events[0].work_type == "task"
        assert events[0].priority == "high"

        # Verify repository.save was called
        mock_repository.save.assert_called_once()

    def test_create_work_item_with_defaults(
        self,
        mock_repository: Mock,
        mock_id_generator: Mock,
    ) -> None:
        """Handler uses default values for optional fields."""
        handler = CreateWorkItemCommandHandler(
            repository=mock_repository,
            id_generator=mock_id_generator,
        )
        command = CreateWorkItemCommand(title="Minimal task")

        events = handler.handle(command)

        assert len(events) == 1
        event = events[0]
        assert event.title == "Minimal task"
        assert event.work_type == "task"
        assert event.priority == "medium"

    def test_create_work_item_with_parent(
        self,
        mock_repository: Mock,
        mock_id_generator: Mock,
    ) -> None:
        """Handler creates work item with parent ID.

        Note: Current implementation expects parent_id to be convertible to int.
        This is a known limitation (see DISC-016 in PHASE-DISCOVERY.md).
        Using a numeric string as parent_id for this test.
        """
        # Create parent work item mock
        parent_item = WorkItem.create(
            id=WorkItemId.create(54321, 1),
            title="Parent task",
            work_type=WorkType.STORY,
            priority=Priority.HIGH,
        )
        mock_repository.get.return_value = parent_item

        handler = CreateWorkItemCommandHandler(
            repository=mock_repository,
            id_generator=mock_id_generator,
        )
        # Use numeric string for parent_id (current limitation)
        command = CreateWorkItemCommand(
            title="Child task",
            parent_id="54321",  # Numeric string to match handler expectation
        )

        events = handler.handle(command)

        assert len(events) == 1
        # parent_id is set (actual value is WorkItemId)
        assert events[0].parent_id is not None


# =============================================================================
# StartWorkItemCommandHandler Tests
# =============================================================================


class TestStartWorkItemCommandHandler:
    """Tests for StartWorkItemCommandHandler."""

    def test_start_work_item_success(
        self,
        mock_repository: Mock,
        sample_work_item: WorkItem,
    ) -> None:
        """Handler starts work item and returns StatusChanged event."""
        mock_repository.get_or_raise.return_value = sample_work_item

        handler = StartWorkItemCommandHandler(repository=mock_repository)
        command = StartWorkItemCommand(
            work_item_id="WORK-12345-1",
            reason="Starting implementation",
        )

        events = handler.handle(command)

        # Verify event returned
        assert len(events) == 1
        assert isinstance(events[0], StatusChanged)
        assert events[0].old_status == "pending"
        assert events[0].new_status == "in_progress"

        # Verify repository interactions
        mock_repository.get_or_raise.assert_called_once_with("WORK-12345-1")
        mock_repository.save.assert_called_once()

    def test_start_work_item_not_found(
        self,
        mock_repository: Mock,
    ) -> None:
        """Handler raises error when work item not found."""
        mock_repository.get_or_raise.side_effect = AggregateNotFoundError(
            "WORK-999",
            "WorkItem",
        )

        handler = StartWorkItemCommandHandler(repository=mock_repository)
        command = StartWorkItemCommand(work_item_id="WORK-999")

        with pytest.raises(AggregateNotFoundError):
            handler.handle(command)

    def test_start_work_item_invalid_state(
        self,
        mock_repository: Mock,
        in_progress_work_item: WorkItem,
    ) -> None:
        """Handler raises error when starting already started item."""
        mock_repository.get_or_raise.return_value = in_progress_work_item

        handler = StartWorkItemCommandHandler(repository=mock_repository)
        command = StartWorkItemCommand(work_item_id="WORK-12345-2")

        with pytest.raises(InvalidStateTransitionError):
            handler.handle(command)


# =============================================================================
# CompleteWorkItemCommandHandler Tests
# =============================================================================


class TestCompleteWorkItemCommandHandler:
    """Tests for CompleteWorkItemCommandHandler."""

    def test_complete_work_item_success(
        self,
        mock_repository: Mock,
        completable_work_item: WorkItem,
    ) -> None:
        """Handler completes work item and returns events."""
        mock_repository.get_or_raise.return_value = completable_work_item

        handler = CompleteWorkItemCommandHandler(repository=mock_repository)
        command = CompleteWorkItemCommand(
            work_item_id="WORK-12345-3",
            reason="Implementation complete",
        )

        events = handler.handle(command)

        # Verify events returned (StatusChanged + WorkItemCompleted)
        assert len(events) >= 1
        status_events = [e for e in events if isinstance(e, StatusChanged)]
        assert len(status_events) == 1
        assert status_events[0].new_status == "done"

        # Verify repository interactions
        mock_repository.get_or_raise.assert_called_once_with("WORK-12345-3")
        mock_repository.save.assert_called_once()

    def test_complete_work_item_not_found(
        self,
        mock_repository: Mock,
    ) -> None:
        """Handler raises error when work item not found."""
        mock_repository.get_or_raise.side_effect = AggregateNotFoundError(
            "WORK-999",
            "WorkItem",
        )

        handler = CompleteWorkItemCommandHandler(repository=mock_repository)
        command = CompleteWorkItemCommand(work_item_id="WORK-999")

        with pytest.raises(AggregateNotFoundError):
            handler.handle(command)

    def test_complete_work_item_invalid_state(
        self,
        mock_repository: Mock,
        sample_work_item: WorkItem,
    ) -> None:
        """Handler raises error when completing pending item."""
        mock_repository.get_or_raise.return_value = sample_work_item

        handler = CompleteWorkItemCommandHandler(repository=mock_repository)
        command = CompleteWorkItemCommand(work_item_id="WORK-12345-1")

        with pytest.raises(InvalidStateTransitionError):
            handler.handle(command)


# =============================================================================
# BlockWorkItemCommandHandler Tests
# =============================================================================


class TestBlockWorkItemCommandHandler:
    """Tests for BlockWorkItemCommandHandler."""

    def test_block_work_item_success(
        self,
        mock_repository: Mock,
        in_progress_work_item: WorkItem,
    ) -> None:
        """Handler blocks work item and returns StatusChanged event."""
        mock_repository.get_or_raise.return_value = in_progress_work_item

        handler = BlockWorkItemCommandHandler(repository=mock_repository)
        command = BlockWorkItemCommand(
            work_item_id="WORK-12345-2",
            reason="Waiting for API",
        )

        events = handler.handle(command)

        # Verify event returned
        assert len(events) == 1
        assert isinstance(events[0], StatusChanged)
        assert events[0].new_status == "blocked"

        # Verify repository interactions
        mock_repository.get_or_raise.assert_called_once_with("WORK-12345-2")
        mock_repository.save.assert_called_once()

    def test_block_work_item_not_found(
        self,
        mock_repository: Mock,
    ) -> None:
        """Handler raises error when work item not found."""
        mock_repository.get_or_raise.side_effect = AggregateNotFoundError(
            "WORK-999",
            "WorkItem",
        )

        handler = BlockWorkItemCommandHandler(repository=mock_repository)
        command = BlockWorkItemCommand(
            work_item_id="WORK-999",
            reason="Reason",
        )

        with pytest.raises(AggregateNotFoundError):
            handler.handle(command)

    def test_block_work_item_invalid_state_from_pending(
        self,
        mock_repository: Mock,
        sample_work_item: WorkItem,
    ) -> None:
        """Handler raises error when blocking pending item (not in_progress)."""
        mock_repository.get_or_raise.return_value = sample_work_item

        handler = BlockWorkItemCommandHandler(repository=mock_repository)
        command = BlockWorkItemCommand(
            work_item_id="WORK-12345-1",
            reason="Blocked",
        )

        with pytest.raises(InvalidStateTransitionError):
            handler.handle(command)


# =============================================================================
# CancelWorkItemCommandHandler Tests
# =============================================================================


class TestCancelWorkItemCommandHandler:
    """Tests for CancelWorkItemCommandHandler."""

    def test_cancel_work_item_from_pending_success(
        self,
        mock_repository: Mock,
        sample_work_item: WorkItem,
    ) -> None:
        """Handler cancels pending work item and returns events."""
        mock_repository.get_or_raise.return_value = sample_work_item

        handler = CancelWorkItemCommandHandler(repository=mock_repository)
        command = CancelWorkItemCommand(
            work_item_id="WORK-12345-1",
            reason="No longer needed",
        )

        events = handler.handle(command)

        # Verify events returned
        status_events = [e for e in events if isinstance(e, StatusChanged)]
        assert len(status_events) == 1
        assert status_events[0].new_status == "cancelled"

        # Verify repository interactions
        mock_repository.get_or_raise.assert_called_once_with("WORK-12345-1")
        mock_repository.save.assert_called_once()

    def test_cancel_work_item_from_blocked_success(
        self,
        mock_repository: Mock,
    ) -> None:
        """Handler cancels blocked work item."""
        blocked_item = WorkItem.create(
            id=WorkItemId.create(12345, 3),
            title="Blocked task",
            work_type=WorkType.TASK,
            priority=Priority.MEDIUM,
        )
        blocked_item.collect_events()
        blocked_item.start_work()
        blocked_item.collect_events()
        blocked_item.block(reason="Waiting")
        blocked_item.collect_events()

        mock_repository.get_or_raise.return_value = blocked_item

        handler = CancelWorkItemCommandHandler(repository=mock_repository)
        command = CancelWorkItemCommand(
            work_item_id="WORK-12345-3",
            reason="Cancelled due to delay",
        )

        events = handler.handle(command)

        status_events = [e for e in events if isinstance(e, StatusChanged)]
        assert len(status_events) == 1
        assert status_events[0].new_status == "cancelled"

    def test_cancel_work_item_not_found(
        self,
        mock_repository: Mock,
    ) -> None:
        """Handler raises error when work item not found."""
        mock_repository.get_or_raise.side_effect = AggregateNotFoundError(
            "WORK-999",
            "WorkItem",
        )

        handler = CancelWorkItemCommandHandler(repository=mock_repository)
        command = CancelWorkItemCommand(work_item_id="WORK-999")

        with pytest.raises(AggregateNotFoundError):
            handler.handle(command)

    def test_cancel_work_item_invalid_state_from_done(
        self,
        mock_repository: Mock,
        done_work_item: WorkItem,
    ) -> None:
        """Handler raises error when cancelling completed item (done can only reopen)."""
        mock_repository.get_or_raise.return_value = done_work_item

        handler = CancelWorkItemCommandHandler(repository=mock_repository)
        command = CancelWorkItemCommand(work_item_id="WORK-12345-4")

        with pytest.raises(InvalidStateTransitionError):
            handler.handle(command)
