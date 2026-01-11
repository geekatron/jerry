"""Unit tests for WorkItem aggregate.

Test Categories:
    - Creation: Factory method and initial state
    - Status Transitions: State machine enforcement
    - Priority Changes: Priority modification
    - Quality Metrics: Test coverage and ratio recording
    - Dependencies: Adding/removing dependencies
    - Assignee: Assignment changes
    - Event Sourcing: Event replay and collection

References:
    - IMPL-005: WorkItem Aggregate
    - impl-es-e-006-workitem-schema: WorkItem design specification
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from src.work_tracking.domain.aggregates.work_item import (
    QualityGateNotMetError,
    WorkItem,
)
from src.work_tracking.domain.events.work_item_events import (
    AssigneeChanged,
    DependencyAdded,
    DependencyRemoved,
    PriorityChanged,
    QualityMetricsUpdated,
    StatusChanged,
    WorkItemCompleted,
    WorkItemCreated,
)
from src.work_tracking.domain.value_objects import (
    InvalidStateTransitionError,
    Priority,
    TestCoverage,
    TestRatio,
    WorkItemId,
    WorkItemStatus,
    WorkType,
)

# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def work_item_id() -> WorkItemId:
    """Create a standard work item ID for testing."""
    return WorkItemId.create(internal_id=12345, display_number=1)


@pytest.fixture
def second_work_item_id() -> WorkItemId:
    """Create a second work item ID for dependency testing."""
    return WorkItemId.create(internal_id=67890, display_number=2)


@pytest.fixture
def pending_item(work_item_id: WorkItemId) -> WorkItem:
    """Create a work item in PENDING status."""
    return WorkItem.create(
        id=work_item_id,
        title="Test Task",
        work_type=WorkType.TASK,
        priority=Priority.MEDIUM,
    )


@pytest.fixture
def in_progress_item(work_item_id: WorkItemId) -> WorkItem:
    """Create a work item in IN_PROGRESS status."""
    item = WorkItem.create(
        id=work_item_id,
        title="Test Task",
        work_type=WorkType.TASK,
        priority=Priority.MEDIUM,
    )
    item.start_work()
    return item


# =============================================================================
# Creation Tests
# =============================================================================


class TestWorkItemCreation:
    """Tests for WorkItem.create() factory method."""

    def test_create_with_minimal_args(self, work_item_id: WorkItemId) -> None:
        """Create work item with only required arguments."""
        item = WorkItem.create(id=work_item_id, title="Test Task")

        assert item.id == str(work_item_id.internal_id)
        assert item.title == "Test Task"
        assert item.work_type == WorkType.TASK
        assert item.priority == Priority.MEDIUM
        assert item.status == WorkItemStatus.PENDING

    def test_create_with_all_args(self, work_item_id: WorkItemId) -> None:
        """Create work item with all arguments."""
        parent_id = WorkItemId.create(99999, 99)
        item = WorkItem.create(
            id=work_item_id,
            title="Feature Implementation",
            work_type=WorkType.STORY,
            priority=Priority.HIGH,
            description="Detailed description here",
            parent_id=parent_id,
        )

        assert item.title == "Feature Implementation"
        assert item.work_type == WorkType.STORY
        assert item.priority == Priority.HIGH
        assert item.description == "Detailed description here"
        assert item.parent_id == str(parent_id.internal_id)

    def test_create_emits_work_item_created_event(self, work_item_id: WorkItemId) -> None:
        """Creation emits WorkItemCreated event."""
        item = WorkItem.create(id=work_item_id, title="Test Task")
        events = item.collect_events()

        assert len(events) == 1
        assert isinstance(events[0], WorkItemCreated)
        assert events[0].title == "Test Task"
        assert events[0].work_type == "task"
        assert events[0].priority == "medium"

    def test_create_with_empty_title_raises(self, work_item_id: WorkItemId) -> None:
        """Empty title raises ValueError."""
        with pytest.raises(ValueError, match="title cannot be empty"):
            WorkItem.create(id=work_item_id, title="")

    def test_create_with_whitespace_title_raises(self, work_item_id: WorkItemId) -> None:
        """Whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="title cannot be empty"):
            WorkItem.create(id=work_item_id, title="   ")

    def test_create_strips_title_whitespace(self, work_item_id: WorkItemId) -> None:
        """Title is stripped of leading/trailing whitespace."""
        item = WorkItem.create(id=work_item_id, title="  Test Task  ")
        assert item.title == "Test Task"

    def test_initial_state_is_pending(self, work_item_id: WorkItemId) -> None:
        """New work item starts in PENDING status."""
        item = WorkItem.create(id=work_item_id, title="Test")
        assert item.status == WorkItemStatus.PENDING
        assert item.status.is_waiting

    def test_initial_quality_metrics_are_none(self, work_item_id: WorkItemId) -> None:
        """New work item has no quality metrics."""
        item = WorkItem.create(id=work_item_id, title="Test")
        assert item.test_coverage is None
        assert item.test_ratio is None

    def test_initial_assignee_is_none(self, work_item_id: WorkItemId) -> None:
        """New work item has no assignee."""
        item = WorkItem.create(id=work_item_id, title="Test")
        assert item.assignee is None

    def test_initial_dependencies_is_empty(self, work_item_id: WorkItemId) -> None:
        """New work item has no dependencies."""
        item = WorkItem.create(id=work_item_id, title="Test")
        assert item.dependencies == ()

    def test_version_after_creation(self, work_item_id: WorkItemId) -> None:
        """Version is 1 after creation event."""
        item = WorkItem.create(id=work_item_id, title="Test")
        assert item.version == 1


# =============================================================================
# Status Transition Tests - Happy Path
# =============================================================================


class TestStatusTransitionsHappyPath:
    """Tests for valid status transitions."""

    def test_start_work_from_pending(self, pending_item: WorkItem) -> None:
        """Can start work from PENDING."""
        pending_item.start_work()
        assert pending_item.status == WorkItemStatus.IN_PROGRESS

    def test_block_from_in_progress(self, in_progress_item: WorkItem) -> None:
        """Can block from IN_PROGRESS."""
        in_progress_item.block(reason="Waiting for API")
        assert in_progress_item.status == WorkItemStatus.BLOCKED

    def test_unblock_to_in_progress(self, in_progress_item: WorkItem) -> None:
        """Can unblock from BLOCKED to IN_PROGRESS."""
        in_progress_item.block()
        in_progress_item.start_work(reason="Blocker resolved")
        assert in_progress_item.status == WorkItemStatus.IN_PROGRESS

    def test_complete_from_in_progress_with_metrics(self, in_progress_item: WorkItem) -> None:
        """Can complete from IN_PROGRESS with quality metrics."""
        in_progress_item.update_quality_metrics(
            coverage=TestCoverage.from_percent(80),
            ratio=TestRatio(positive=5, negative=3, edge_case=2),
        )
        in_progress_item.complete()
        assert in_progress_item.status == WorkItemStatus.DONE
        assert in_progress_item.completed_at is not None

    def test_cancel_from_pending(self, pending_item: WorkItem) -> None:
        """Can cancel from PENDING."""
        pending_item.cancel(reason="Out of scope")
        assert pending_item.status == WorkItemStatus.CANCELLED

    def test_cancel_from_in_progress(self, in_progress_item: WorkItem) -> None:
        """Can cancel from IN_PROGRESS."""
        in_progress_item.cancel()
        assert in_progress_item.status == WorkItemStatus.CANCELLED

    def test_cancel_from_blocked(self, in_progress_item: WorkItem) -> None:
        """Can cancel from BLOCKED."""
        in_progress_item.block()
        in_progress_item.cancel()
        assert in_progress_item.status == WorkItemStatus.CANCELLED

    def test_reopen_from_done(self, in_progress_item: WorkItem) -> None:
        """Can reopen from DONE."""
        in_progress_item.update_quality_metrics(
            ratio=TestRatio(positive=5, negative=3, edge_case=2),
        )
        in_progress_item.complete()
        in_progress_item.reopen(reason="Need to fix bug")
        assert in_progress_item.status == WorkItemStatus.IN_PROGRESS
        assert in_progress_item.completed_at is None


# =============================================================================
# Status Transition Tests - Invalid Transitions
# =============================================================================


class TestStatusTransitionsInvalid:
    """Tests for invalid status transitions."""

    def test_cannot_complete_from_pending(self, pending_item: WorkItem) -> None:
        """Cannot complete directly from PENDING."""
        with pytest.raises(InvalidStateTransitionError):
            pending_item.complete()

    def test_cannot_block_from_pending(self, pending_item: WorkItem) -> None:
        """Cannot block from PENDING."""
        with pytest.raises(InvalidStateTransitionError):
            pending_item.block()

    def test_cannot_transition_from_cancelled(self, pending_item: WorkItem) -> None:
        """Cannot transition from CANCELLED (terminal state)."""
        pending_item.cancel()
        with pytest.raises(InvalidStateTransitionError):
            pending_item.start_work()

    def test_cannot_cancel_from_done(self, in_progress_item: WorkItem) -> None:
        """Cannot cancel from DONE."""
        in_progress_item.update_quality_metrics(
            ratio=TestRatio(positive=5, negative=3, edge_case=2),
        )
        in_progress_item.complete()
        with pytest.raises(InvalidStateTransitionError):
            in_progress_item.cancel()


# =============================================================================
# Quality Gate Tests
# =============================================================================


class TestQualityGates:
    """Tests for quality gate validation."""

    def test_cannot_complete_without_quality_metrics(self, in_progress_item: WorkItem) -> None:
        """Cannot complete without any quality metrics."""
        with pytest.raises(QualityGateNotMetError) as exc_info:
            in_progress_item.complete()
        assert "No quality metrics recorded" in exc_info.value.failures

    def test_can_complete_spike_without_quality_metrics(self, work_item_id: WorkItemId) -> None:
        """SPIKEs don't require quality metrics."""
        item = WorkItem.create(
            id=work_item_id,
            title="Research Task",
            work_type=WorkType.SPIKE,
        )
        item.start_work()
        item.complete()  # Should not raise
        assert item.status == WorkItemStatus.DONE

    def test_update_quality_metrics_records_coverage(self, pending_item: WorkItem) -> None:
        """Quality metrics update records coverage."""
        coverage = TestCoverage.from_percent(85.5)
        pending_item.update_quality_metrics(coverage=coverage)
        assert pending_item.test_coverage is not None
        assert pending_item.test_coverage.percent == 85.5

    def test_update_quality_metrics_records_ratio(self, pending_item: WorkItem) -> None:
        """Quality metrics update records test ratio."""
        ratio = TestRatio(positive=10, negative=5, edge_case=3)
        pending_item.update_quality_metrics(ratio=ratio)
        assert pending_item.test_ratio is not None
        assert pending_item.test_ratio.positive == 10

    def test_quality_metrics_emits_event(self, pending_item: WorkItem) -> None:
        """Quality metrics update emits event."""
        pending_item.collect_events()  # Clear creation event
        pending_item.update_quality_metrics(
            coverage=TestCoverage.from_percent(80),
            ratio=TestRatio(positive=5, negative=3, edge_case=2),
        )
        events = pending_item.collect_events()

        assert len(events) == 1
        assert isinstance(events[0], QualityMetricsUpdated)
        assert events[0].coverage_percent == 80.0
        assert events[0].positive_tests == 5
        assert events[0].gate_passed


# =============================================================================
# Priority Change Tests
# =============================================================================


class TestPriorityChanges:
    """Tests for priority modification."""

    def test_change_priority(self, pending_item: WorkItem) -> None:
        """Can change priority."""
        pending_item.change_priority(Priority.CRITICAL)
        assert pending_item.priority == Priority.CRITICAL

    def test_change_priority_emits_event(self, pending_item: WorkItem) -> None:
        """Priority change emits event."""
        pending_item.collect_events()  # Clear creation event
        pending_item.change_priority(Priority.HIGH, reason="Urgent")
        events = pending_item.collect_events()

        assert len(events) == 1
        assert isinstance(events[0], PriorityChanged)
        assert events[0].old_priority == "medium"
        assert events[0].new_priority == "high"
        assert events[0].reason == "Urgent"

    def test_change_priority_same_is_noop(self, pending_item: WorkItem) -> None:
        """Changing to same priority is a no-op."""
        pending_item.collect_events()  # Clear creation event
        pending_item.change_priority(Priority.MEDIUM)  # Same as current
        events = pending_item.collect_events()

        assert len(events) == 0


# =============================================================================
# Dependency Tests
# =============================================================================


class TestDependencies:
    """Tests for dependency management."""

    def test_add_dependency(self, pending_item: WorkItem, second_work_item_id: WorkItemId) -> None:
        """Can add a dependency."""
        pending_item.add_dependency(second_work_item_id)
        assert str(second_work_item_id.internal_id) in pending_item.dependencies

    def test_add_dependency_emits_event(
        self, pending_item: WorkItem, second_work_item_id: WorkItemId
    ) -> None:
        """Adding dependency emits event."""
        pending_item.collect_events()
        pending_item.add_dependency(second_work_item_id, dependency_type="blocks")
        events = pending_item.collect_events()

        assert len(events) == 1
        assert isinstance(events[0], DependencyAdded)
        assert events[0].dependency_id == str(second_work_item_id.internal_id)
        assert events[0].dependency_type == "blocks"

    def test_cannot_add_self_dependency(
        self, pending_item: WorkItem, work_item_id: WorkItemId
    ) -> None:
        """Cannot depend on self."""
        with pytest.raises(ValueError, match="cannot depend on itself"):
            pending_item.add_dependency(work_item_id)

    def test_cannot_add_duplicate_dependency(
        self, pending_item: WorkItem, second_work_item_id: WorkItemId
    ) -> None:
        """Cannot add same dependency twice."""
        pending_item.add_dependency(second_work_item_id)
        with pytest.raises(ValueError, match="already exists"):
            pending_item.add_dependency(second_work_item_id)

    def test_remove_dependency(
        self, pending_item: WorkItem, second_work_item_id: WorkItemId
    ) -> None:
        """Can remove a dependency."""
        pending_item.add_dependency(second_work_item_id)
        pending_item.remove_dependency(second_work_item_id)
        assert str(second_work_item_id.internal_id) not in pending_item.dependencies

    def test_remove_dependency_emits_event(
        self, pending_item: WorkItem, second_work_item_id: WorkItemId
    ) -> None:
        """Removing dependency emits event."""
        pending_item.add_dependency(second_work_item_id)
        pending_item.collect_events()
        pending_item.remove_dependency(second_work_item_id)
        events = pending_item.collect_events()

        assert len(events) == 1
        assert isinstance(events[0], DependencyRemoved)
        assert events[0].dependency_id == str(second_work_item_id.internal_id)

    def test_cannot_remove_nonexistent_dependency(
        self, pending_item: WorkItem, second_work_item_id: WorkItemId
    ) -> None:
        """Cannot remove dependency that doesn't exist."""
        with pytest.raises(ValueError, match="does not exist"):
            pending_item.remove_dependency(second_work_item_id)


# =============================================================================
# Assignee Tests
# =============================================================================


class TestAssignee:
    """Tests for assignment changes."""

    def test_assign_work_item(self, pending_item: WorkItem) -> None:
        """Can assign work item."""
        pending_item.assign("agent:qa-engineer")
        assert pending_item.assignee == "agent:qa-engineer"

    def test_unassign_work_item(self, pending_item: WorkItem) -> None:
        """Can unassign work item."""
        pending_item.assign("user:john")
        pending_item.assign(None)
        assert pending_item.assignee is None

    def test_assign_emits_event(self, pending_item: WorkItem) -> None:
        """Assignment emits event."""
        pending_item.collect_events()
        pending_item.assign("agent:developer")
        events = pending_item.collect_events()

        assert len(events) == 1
        assert isinstance(events[0], AssigneeChanged)
        assert events[0].old_assignee is None
        assert events[0].new_assignee == "agent:developer"

    def test_reassign_to_same_is_noop(self, pending_item: WorkItem) -> None:
        """Reassigning to same value is a no-op."""
        pending_item.assign("user:john")
        pending_item.collect_events()
        pending_item.assign("user:john")  # Same as current
        events = pending_item.collect_events()

        assert len(events) == 0


# =============================================================================
# Event Sourcing Tests
# =============================================================================


class TestEventSourcing:
    """Tests for event sourcing behavior."""

    def test_collect_events_returns_pending(self, pending_item: WorkItem) -> None:
        """collect_events returns pending events."""
        events = pending_item.collect_events()
        assert len(events) == 1
        assert isinstance(events[0], WorkItemCreated)

    def test_collect_events_clears_pending(self, pending_item: WorkItem) -> None:
        """collect_events clears pending events."""
        pending_item.collect_events()
        events = pending_item.collect_events()
        assert len(events) == 0

    def test_has_pending_events(self, work_item_id: WorkItemId) -> None:
        """has_pending_events returns correct state."""
        item = WorkItem.create(id=work_item_id, title="Test")
        assert item.has_pending_events()
        item.collect_events()
        assert not item.has_pending_events()

    def test_load_from_history(self, work_item_id: WorkItemId) -> None:
        """Can reconstruct from event history."""
        # Create and modify an item
        original = WorkItem.create(
            id=work_item_id,
            title="Test Task",
            work_type=WorkType.TASK,
            priority=Priority.MEDIUM,
        )
        original.start_work()
        original.change_priority(Priority.HIGH)
        original.update_quality_metrics(
            coverage=TestCoverage.from_percent(85),
            ratio=TestRatio(positive=10, negative=5, edge_case=3),
        )

        # Collect events
        events = original.collect_events()

        # Reconstruct
        reconstructed = WorkItem.load_from_history(events)

        # Verify state matches
        assert reconstructed.id == original.id
        assert reconstructed.title == original.title
        assert reconstructed.status == original.status
        assert reconstructed.priority == original.priority
        assert reconstructed.test_coverage is not None
        assert reconstructed.test_coverage.percent == 85.0

    def test_load_from_empty_history_raises(self) -> None:
        """Cannot load from empty history."""
        with pytest.raises(ValueError, match="empty event history"):
            WorkItem.load_from_history([])

    def test_version_increments_with_events(self, pending_item: WorkItem) -> None:
        """Version increments with each event."""
        assert pending_item.version == 1
        pending_item.start_work()
        assert pending_item.version == 2
        pending_item.change_priority(Priority.HIGH)
        assert pending_item.version == 3

    def test_complete_emits_two_events(self, in_progress_item: WorkItem) -> None:
        """Complete emits StatusChanged and WorkItemCompleted."""
        in_progress_item.update_quality_metrics(
            ratio=TestRatio(positive=5, negative=3, edge_case=2),
        )
        in_progress_item.collect_events()  # Clear previous
        in_progress_item.complete(reason="All done")
        events = in_progress_item.collect_events()

        assert len(events) == 2
        assert isinstance(events[0], StatusChanged)
        assert isinstance(events[1], WorkItemCompleted)
        assert events[1].final_status == "done"


# =============================================================================
# Work Type Tests
# =============================================================================


class TestWorkTypes:
    """Tests for different work types."""

    def test_create_bug(self, work_item_id: WorkItemId) -> None:
        """Can create BUG work type."""
        item = WorkItem.create(
            id=work_item_id,
            title="Fix login bug",
            work_type=WorkType.BUG,
            priority=Priority.CRITICAL,
        )
        assert item.work_type == WorkType.BUG

    def test_create_story(self, work_item_id: WorkItemId) -> None:
        """Can create STORY work type."""
        item = WorkItem.create(
            id=work_item_id,
            title="User can login",
            work_type=WorkType.STORY,
        )
        assert item.work_type == WorkType.STORY

    def test_create_epic(self, work_item_id: WorkItemId) -> None:
        """Can create EPIC work type."""
        item = WorkItem.create(
            id=work_item_id,
            title="Authentication System",
            work_type=WorkType.EPIC,
        )
        assert item.work_type == WorkType.EPIC

    def test_create_subtask(self, work_item_id: WorkItemId) -> None:
        """Can create SUBTASK work type."""
        parent_id = WorkItemId.create(99999, 99)
        item = WorkItem.create(
            id=work_item_id,
            title="Write unit tests",
            work_type=WorkType.SUBTASK,
            parent_id=parent_id,
        )
        assert item.work_type == WorkType.SUBTASK
        assert item.parent_id == str(parent_id.internal_id)


# =============================================================================
# Edge Case Tests
# =============================================================================


class TestEdgeCases:
    """Edge case tests for WorkItem aggregate."""

    def test_multiple_status_transitions(self, pending_item: WorkItem) -> None:
        """Multiple status transitions work correctly."""
        pending_item.start_work()
        pending_item.block()
        pending_item.start_work()
        pending_item.update_quality_metrics(
            ratio=TestRatio(positive=5, negative=3, edge_case=2),
        )
        pending_item.complete()
        pending_item.reopen()
        assert pending_item.status == WorkItemStatus.IN_PROGRESS

    def test_unicode_in_title(self, work_item_id: WorkItemId) -> None:
        """Unicode characters in title work correctly."""
        item = WorkItem.create(
            id=work_item_id,
            title="Fix bug in 日本語 handling",
        )
        assert "日本語" in item.title

    def test_long_description(self, work_item_id: WorkItemId) -> None:
        """Long descriptions are preserved."""
        long_desc = "A" * 10000
        item = WorkItem.create(
            id=work_item_id,
            title="Test",
            description=long_desc,
        )
        assert item.description == long_desc

    def test_created_on_timestamp(self, pending_item: WorkItem) -> None:
        """created_on is set correctly."""
        assert pending_item.created_on is not None
        # Check it's recent (within last minute)
        now = datetime.now(UTC)
        delta = now - pending_item.created_on
        assert delta.total_seconds() < 60

    def test_modified_on_updates(self, pending_item: WorkItem) -> None:
        """modified_on updates with each event."""
        first_modified = pending_item.modified_on
        pending_item.start_work()
        assert pending_item.modified_on is not None
        if first_modified:
            assert pending_item.modified_on >= first_modified

    def test_dependencies_returns_tuple(self, pending_item: WorkItem) -> None:
        """dependencies property returns immutable tuple."""
        deps = pending_item.dependencies
        assert isinstance(deps, tuple)

    def test_equality_by_id(self, work_item_id: WorkItemId) -> None:
        """Work items are equal if they have the same ID."""
        item1 = WorkItem.create(id=work_item_id, title="Task 1")
        item2 = WorkItem.create(id=work_item_id, title="Task 2")
        assert item1 == item2

    def test_hash_by_id(self, work_item_id: WorkItemId) -> None:
        """Work items can be used in sets/dicts."""
        item = WorkItem.create(id=work_item_id, title="Task")
        item_set = {item}
        assert item in item_set
