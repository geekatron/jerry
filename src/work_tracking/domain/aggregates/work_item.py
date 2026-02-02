"""
WorkItem Aggregate - Core domain aggregate for work tracking.

The WorkItem aggregate is the primary entry point for work tracking.
It encapsulates all work item state and enforces business invariants.

Lifecycle:
    1. Create via WorkItem.create() factory method
    2. Mutate via command methods (start_work, complete, etc.)
    3. Persist via repository (collect_events)
    4. Reconstitute via WorkItem.load_from_history()

References:
    - IMPL-005: WorkItem Aggregate implementation
    - impl-es-e-006-workitem-schema: WorkItem design specification
    - PAT-004-e006: Status State Machine
    - DDD Aggregate pattern (Evans, 2004)

Exports:
    WorkItem: Event-sourced work item aggregate
    QualityGateNotMetError: Raised when quality requirements not satisfied
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime

from src.shared_kernel.domain_event import DomainEvent
from src.work_tracking.domain.aggregates.base import AggregateRoot
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
    Coverage,
    Priority,
    TypeRatio,
    WorkItemId,
    WorkItemStatus,
    WorkType,
)

# =============================================================================
# Domain Exceptions
# =============================================================================


class QualityGateNotMetError(ValueError):
    """
    Raised when quality gate requirements are not satisfied.

    This occurs when attempting to complete a work item that hasn't
    met the required quality thresholds.

    Attributes:
        work_item_id: ID of the work item
        failures: List of specific quality gate failures
    """

    def __init__(self, work_item_id: str, failures: list[str]) -> None:
        self.work_item_id = work_item_id
        self.failures = failures
        message = (
            f"Work item '{work_item_id}' does not meet quality requirements: {', '.join(failures)}"
        )
        super().__init__(message)


# =============================================================================
# WorkItem Aggregate
# =============================================================================


class WorkItem(AggregateRoot):
    """
    Event-sourced aggregate for work item tracking.

    WorkItem is the primary aggregate in the work tracking domain. It tracks
    tasks, bugs, stories, and other work units with full event history.

    State Management:
        All state changes emit domain events. State is modified only via
        the _apply() method when processing events, ensuring deterministic
        replay from event history.

    Business Rules:
        - Status transitions follow the state machine (WorkItemStatus)
        - Quality gates must be met before completion (except for SPIKEs)
        - Dependencies form a DAG (no cycles allowed)
        - Only one assignee at a time

    Attributes:
        id: Unique identifier (string, use WorkItemId for full identity)
        title: Human-readable title
        description: Detailed description
        work_type: Type classification (TASK, BUG, STORY, etc.)
        status: Current lifecycle status
        priority: Priority level
        test_coverage: Test coverage metrics
        test_ratio: Test type distribution
        parent_id: Parent work item ID (for hierarchy)
        dependencies: List of blocking work item IDs
        assignee: Current assignee (agent or human)
        completed_at: Timestamp when completed

    Example:
        >>> item = WorkItem.create(
        ...     id=WorkItemId.create(12345, 1),
        ...     title="Implement feature",
        ...     work_type=WorkType.TASK,
        ...     priority=Priority.HIGH,
        ... )
        >>> item.start_work()
        >>> item.update_quality_metrics(Coverage.from_percent(85), ...)
        >>> item.complete()
        >>> events = item.collect_events()
    """

    _aggregate_type: str = "WorkItem"

    # These will be initialized by _apply on WorkItemCreated
    _title: str
    _description: str
    _work_type: WorkType
    _status: WorkItemStatus
    _priority: Priority
    _test_coverage: Coverage | None
    _test_ratio: TypeRatio | None
    _parent_id: str | None
    _dependencies: list[str]
    _assignee: str | None
    _completed_at: datetime | None

    # ==========================================================================
    # Factory Methods
    # ==========================================================================

    @classmethod
    def create(
        cls,
        id: WorkItemId,
        title: str,
        work_type: WorkType = WorkType.TASK,
        priority: Priority = Priority.MEDIUM,
        description: str = "",
        parent_id: WorkItemId | None = None,
    ) -> WorkItem:
        """
        Create a new work item.

        Factory method that creates a new WorkItem aggregate by raising
        a WorkItemCreated event.

        Args:
            id: Unique work item identity
            title: Human-readable title (required, non-empty)
            work_type: Type classification (default: TASK)
            priority: Priority level (default: MEDIUM)
            description: Detailed description (default: empty)
            parent_id: Parent work item for hierarchy (optional)

        Returns:
            New WorkItem aggregate with PENDING status

        Raises:
            ValueError: If title is empty

        Example:
            >>> item = WorkItem.create(
            ...     id=WorkItemId.create(12345, 1),
            ...     title="Implement login",
            ...     work_type=WorkType.TASK,
            ...     priority=Priority.HIGH,
            ... )
            >>> item.status
            <WorkItemStatus.PENDING: 'pending'>
        """
        if not title or not title.strip():
            raise ValueError("Work item title cannot be empty")

        # Create instance without calling __init__
        item = cls.__new__(cls)
        item._initialize(str(id.internal_id))

        # Initialize mutable state that won't be set by first event
        item._dependencies = []
        item._test_coverage = None
        item._test_ratio = None
        item._assignee = None
        item._completed_at = None

        # Raise creation event
        event = WorkItemCreated(
            aggregate_id=str(id.internal_id),
            aggregate_type=cls._aggregate_type,
            version=1,
            title=title.strip(),
            work_type=work_type.value,
            priority=str(priority),
            description=description,
            parent_id=str(parent_id.internal_id) if parent_id else None,
        )
        item._raise_event(event)

        return item

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def title(self) -> str:
        """Human-readable title of the work item."""
        return self._title

    @property
    def description(self) -> str:
        """Detailed description of the work item."""
        return self._description

    @property
    def work_type(self) -> WorkType:
        """Type classification of the work item."""
        return self._work_type

    @property
    def status(self) -> WorkItemStatus:
        """Current lifecycle status."""
        return self._status

    @property
    def priority(self) -> Priority:
        """Priority level."""
        return self._priority

    @property
    def test_coverage(self) -> Coverage | None:
        """Test coverage metrics, if recorded."""
        return self._test_coverage

    @property
    def test_ratio(self) -> TypeRatio | None:
        """Test type distribution, if recorded."""
        return self._test_ratio

    @property
    def parent_id(self) -> str | None:
        """Parent work item ID for hierarchy."""
        return self._parent_id

    @property
    def dependencies(self) -> tuple[str, ...]:
        """IDs of work items that block this one."""
        return tuple(self._dependencies)

    @property
    def assignee(self) -> str | None:
        """Current assignee (agent or human)."""
        return self._assignee

    @property
    def completed_at(self) -> datetime | None:
        """Timestamp when work was completed."""
        return self._completed_at

    # ==========================================================================
    # Command Methods
    # ==========================================================================

    def start_work(self, reason: str | None = None) -> None:
        """
        Transition to IN_PROGRESS status.

        Begins work on the item. Valid from PENDING or BLOCKED status.

        Args:
            reason: Optional reason for starting work

        Raises:
            InvalidStateTransitionError: If transition not allowed
        """
        target = WorkItemStatus.IN_PROGRESS
        self._status.validate_transition(target)

        event = StatusChanged(
            aggregate_id=self._id,
            aggregate_type=self._aggregate_type,
            version=self._version + 1,
            old_status=self._status.value,
            new_status=target.value,
            reason=reason,
        )
        self._raise_event(event)

    def block(self, reason: str | None = None) -> None:
        """
        Transition to BLOCKED status.

        Indicates work is blocked by a dependency or issue.

        Args:
            reason: Reason for being blocked

        Raises:
            InvalidStateTransitionError: If transition not allowed
        """
        target = WorkItemStatus.BLOCKED
        self._status.validate_transition(target)

        event = StatusChanged(
            aggregate_id=self._id,
            aggregate_type=self._aggregate_type,
            version=self._version + 1,
            old_status=self._status.value,
            new_status=target.value,
            reason=reason,
        )
        self._raise_event(event)

    def complete(self, reason: str | None = None) -> None:
        """
        Transition to DONE status.

        Marks the work item as successfully completed. Validates quality
        gates unless this is a SPIKE work type.

        Args:
            reason: Optional completion notes

        Raises:
            InvalidStateTransitionError: If not in completable state
            QualityGateNotMetError: If quality requirements not satisfied
        """
        target = WorkItemStatus.DONE
        self._status.validate_transition(target)

        # Validate quality gates for non-SPIKE work types
        if self._work_type.requires_quality_gates:
            self._validate_quality_gates()

        # Calculate duration
        duration_seconds = 0
        if self._created_on:
            now = datetime.now(UTC)
            duration_seconds = int((now - self._created_on).total_seconds())

        # First emit status change
        status_event = StatusChanged(
            aggregate_id=self._id,
            aggregate_type=self._aggregate_type,
            version=self._version + 1,
            old_status=self._status.value,
            new_status=target.value,
            reason=reason,
        )
        self._raise_event(status_event)

        # Then emit completion event
        completion_event = WorkItemCompleted(
            aggregate_id=self._id,
            aggregate_type=self._aggregate_type,
            version=self._version + 1,
            final_status="done",
            duration_seconds=duration_seconds,
            completion_reason=reason,
        )
        self._raise_event(completion_event)

    def cancel(self, reason: str | None = None) -> None:
        """
        Transition to CANCELLED status.

        Removes the work item from scope. This is a terminal state.

        Args:
            reason: Reason for cancellation

        Raises:
            InvalidStateTransitionError: If already in terminal state
        """
        target = WorkItemStatus.CANCELLED
        self._status.validate_transition(target)

        # Calculate duration
        duration_seconds = 0
        if self._created_on:
            now = datetime.now(UTC)
            duration_seconds = int((now - self._created_on).total_seconds())

        # First emit status change
        status_event = StatusChanged(
            aggregate_id=self._id,
            aggregate_type=self._aggregate_type,
            version=self._version + 1,
            old_status=self._status.value,
            new_status=target.value,
            reason=reason,
        )
        self._raise_event(status_event)

        # Then emit completion event
        completion_event = WorkItemCompleted(
            aggregate_id=self._id,
            aggregate_type=self._aggregate_type,
            version=self._version + 1,
            final_status="cancelled",
            duration_seconds=duration_seconds,
            completion_reason=reason,
        )
        self._raise_event(completion_event)

    def reopen(self, reason: str | None = None) -> None:
        """
        Reopen a completed work item.

        Transitions from DONE back to IN_PROGRESS. Use when work
        needs revision.

        Args:
            reason: Reason for reopening

        Raises:
            InvalidStateTransitionError: If not in DONE status
        """
        target = WorkItemStatus.IN_PROGRESS
        self._status.validate_transition(target)

        event = StatusChanged(
            aggregate_id=self._id,
            aggregate_type=self._aggregate_type,
            version=self._version + 1,
            old_status=self._status.value,
            new_status=target.value,
            reason=reason,
        )
        self._raise_event(event)

        # Clear completion timestamp
        self._completed_at = None

    def change_priority(self, new_priority: Priority, reason: str | None = None) -> None:
        """
        Change the work item priority.

        Args:
            new_priority: New priority level
            reason: Reason for the change

        Note:
            No-op if priority is unchanged.
        """
        if new_priority == self._priority:
            return

        event = PriorityChanged(
            aggregate_id=self._id,
            aggregate_type=self._aggregate_type,
            version=self._version + 1,
            old_priority=str(self._priority),
            new_priority=str(new_priority),
            reason=reason,
        )
        self._raise_event(event)

    def update_quality_metrics(
        self,
        coverage: Coverage | None = None,
        ratio: TypeRatio | None = None,
    ) -> None:
        """
        Record test execution results.

        Updates quality metrics and evaluates quality gate requirements.

        Args:
            coverage: Test coverage percentage
            ratio: Test type distribution (positive/negative/edge)
        """
        # Evaluate quality gate
        gate_level, gate_passed, failures = self._evaluate_quality_gate(coverage, ratio)

        event = QualityMetricsUpdated(
            aggregate_id=self._id,
            aggregate_type=self._aggregate_type,
            version=self._version + 1,
            coverage_percent=coverage.percent if coverage else None,
            positive_tests=ratio.positive if ratio else None,
            negative_tests=ratio.negative if ratio else None,
            edge_case_tests=ratio.edge_case if ratio else None,
            gate_level=gate_level,
            gate_passed=gate_passed,
            gate_failures=tuple(failures),
        )
        self._raise_event(event)

    def add_dependency(self, dependency_id: WorkItemId, dependency_type: str = "blocks") -> None:
        """
        Add a dependency to this work item.

        Args:
            dependency_id: ID of the work item this depends on
            dependency_type: Type of dependency (blocks, related)

        Raises:
            ValueError: If dependency already exists or is self-reference
        """
        dep_str = str(dependency_id.internal_id)

        if dep_str == self._id:
            raise ValueError("Work item cannot depend on itself")

        if dep_str in self._dependencies:
            raise ValueError(f"Dependency on {dependency_id} already exists")

        event = DependencyAdded(
            aggregate_id=self._id,
            aggregate_type=self._aggregate_type,
            version=self._version + 1,
            dependency_id=dep_str,
            dependency_type=dependency_type,
        )
        self._raise_event(event)

    def remove_dependency(self, dependency_id: WorkItemId) -> None:
        """
        Remove a dependency from this work item.

        Args:
            dependency_id: ID of the dependency to remove

        Raises:
            ValueError: If dependency doesn't exist
        """
        dep_str = str(dependency_id.internal_id)

        if dep_str not in self._dependencies:
            raise ValueError(f"Dependency on {dependency_id} does not exist")

        event = DependencyRemoved(
            aggregate_id=self._id,
            aggregate_type=self._aggregate_type,
            version=self._version + 1,
            dependency_id=dep_str,
        )
        self._raise_event(event)

    def assign(self, assignee: str | None) -> None:
        """
        Assign or unassign the work item.

        Args:
            assignee: New assignee (agent or human), or None to unassign
        """
        if assignee == self._assignee:
            return

        event = AssigneeChanged(
            aggregate_id=self._id,
            aggregate_type=self._aggregate_type,
            version=self._version + 1,
            old_assignee=self._assignee,
            new_assignee=assignee,
        )
        self._raise_event(event)

    # ==========================================================================
    # Event Application
    # ==========================================================================

    def _apply(self, event: DomainEvent) -> None:
        """
        Apply an event to update aggregate state.

        This method is called during event raising and history replay.
        Must be deterministic and side-effect free.

        Args:
            event: The domain event to apply
        """
        if isinstance(event, WorkItemCreated):
            self._title = event.title
            self._description = event.description
            self._work_type = WorkType.from_string(event.work_type)
            self._status = WorkItemStatus.PENDING
            self._priority = Priority.from_string(event.priority)
            self._parent_id = event.parent_id

        elif isinstance(event, StatusChanged):
            self._status = WorkItemStatus(event.new_status)

        elif isinstance(event, PriorityChanged):
            self._priority = Priority.from_string(event.new_priority)

        elif isinstance(event, QualityMetricsUpdated):
            if event.coverage_percent is not None:
                self._test_coverage = Coverage.from_percent(event.coverage_percent)
            if (
                event.positive_tests is not None
                and event.negative_tests is not None
                and event.edge_case_tests is not None
            ):
                self._test_ratio = TypeRatio(
                    positive=event.positive_tests,
                    negative=event.negative_tests,
                    edge_case=event.edge_case_tests,
                )

        elif isinstance(event, WorkItemCompleted):
            self._completed_at = event.timestamp

        elif isinstance(event, DependencyAdded):
            if event.dependency_id not in self._dependencies:
                self._dependencies.append(event.dependency_id)

        elif isinstance(event, DependencyRemoved):
            if event.dependency_id in self._dependencies:
                self._dependencies.remove(event.dependency_id)

        elif isinstance(event, AssigneeChanged):
            self._assignee = event.new_assignee

    # ==========================================================================
    # Private Helpers
    # ==========================================================================

    def _validate_quality_gates(self) -> None:
        """
        Validate that quality gate requirements are met.

        Raises:
            QualityGateNotMetError: If requirements not satisfied
        """
        failures: list[str] = []

        # Check if any quality metrics exist
        if self._test_coverage is None and self._test_ratio is None:
            failures.append("No quality metrics recorded")

        # Additional validation could be added based on gate_level

        if failures:
            raise QualityGateNotMetError(self._id, failures)

    def _evaluate_quality_gate(
        self,
        coverage: Coverage | None,
        ratio: TypeRatio | None,
    ) -> tuple[str | None, bool, list[str]]:
        """
        Evaluate quality gate requirements.

        Returns:
            Tuple of (gate_level, passed, failures)
        """
        failures: list[str] = []

        # Determine gate level based on work type
        if self._work_type == WorkType.SPIKE:
            return (None, True, [])

        # Default to L1 requirements
        gate_level = "L1"

        if ratio is None:
            failures.append("No test ratio provided")
        else:
            if not ratio.meets_level("L1"):
                failures.append("Test ratio doesn't meet L1: need positive and negative tests")

        gate_passed = len(failures) == 0
        return (gate_level, gate_passed, failures)

    # ==========================================================================
    # History Replay
    # ==========================================================================

    @classmethod
    def load_from_history(cls, events: Sequence[DomainEvent]) -> WorkItem:
        """
        Reconstruct WorkItem by replaying events.

        Args:
            events: Historical events in version order

        Returns:
            WorkItem with state rebuilt from events

        Raises:
            ValueError: If events sequence is empty or invalid
        """
        if not events:
            raise ValueError("Cannot load from empty event history")

        # Validate events
        cls._validate_event_sequence(events)

        # Create uninitialized instance
        item = cls.__new__(cls)

        # Initialize from first event
        first_event = events[0]
        item._id = first_event.aggregate_id
        item._version = 0
        item._pending_events = []
        item._created_on = first_event.timestamp
        item._modified_on = None

        # Initialize mutable collections
        item._dependencies = []
        item._test_coverage = None
        item._test_ratio = None
        item._assignee = None
        item._completed_at = None

        # Replay all events
        for event in events:
            item._version = event.version
            item._apply(event)
            item._modified_on = event.timestamp

        return item
