# PAT-AGG-001: WorkItem Aggregate

> **Status**: MANDATORY
> **Category**: Aggregate Pattern
> **Location**: `src/work_tracking/domain/aggregates/work_item.py`

---

## Overview

WorkItem is the primary aggregate root in the Work Tracking bounded context. It represents a unit of work (task, bug, story, etc.) with lifecycle management, status tracking, and quality gate enforcement.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Eric Evans** (DDD) | "Aggregate is a cluster of associated objects treated as a unit for data changes" |
| **Vaughn Vernon** | "Design small aggregates - a single aggregate should be small enough to load quickly" |
| **Greg Young** | "Aggregates are consistency boundaries for event sourcing" |

---

## Jerry Implementation

```python
# File: src/work_tracking/domain/aggregates/work_item.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from src.work_tracking.domain.aggregates.base import AggregateRoot
from src.work_tracking.domain.events.work_item_events import (
    WorkItemCreated,
    StatusChanged,
    PriorityChanged,
    WorkItemCompleted,
)
from src.work_tracking.domain.value_objects.priority import Priority
from src.work_tracking.domain.value_objects.work_item_status import WorkItemStatus


@dataclass
class WorkItem(AggregateRoot):
    """Work item aggregate root.

    Represents a unit of work in the system with:
    - Lifecycle management (status transitions)
    - Priority tracking
    - Quality gate enforcement
    - Event sourcing support

    Invariants:
    - Title cannot be empty
    - Status transitions must follow state machine
    - Completed items require quality gate pass
    - Only in_progress items can be completed

    Lifecycle:
        1. Create via WorkItem.create()
        2. Start work via start()
        3. Block/unblock as needed
        4. Complete via complete()
        5. Optionally cancel via cancel()

    References:
        - PAT-ENT-003: AggregateRoot base class
        - PAT-VO-002: WorkItemStatus state machine
        - PAT-SVC-001: Quality gate validation
    """

    @classmethod
    def create(
        cls,
        id: str,
        title: str,
        work_type: str = "task",
        priority: str = "medium",
        description: str = "",
        parent_id: str | None = None,
    ) -> WorkItem:
        """Factory method to create new work item.

        Args:
            id: Unique work item identifier
            title: Work item title (required, non-empty)
            work_type: Type of work (task, bug, story, spike, etc.)
            priority: Priority level (critical, high, medium, low)
            description: Detailed description
            parent_id: Optional parent work item ID

        Returns:
            New WorkItem instance with WorkItemCreated event

        Raises:
            ValueError: If title is empty
        """
        if not title.strip():
            raise ValueError("Title cannot be empty")

        item = cls.__new__(cls)
        item._initialize(id=id)

        event = WorkItemCreated(
            aggregate_id=id,
            aggregate_type="WorkItem",
            title=title,
            work_type=work_type,
            priority=priority,
            description=description,
            parent_id=parent_id,
        )
        item._raise_event(event)

        return item

    def start(self) -> None:
        """Transition to in_progress status.

        Raises:
            InvalidStateTransitionError: If not in pending status
        """
        self._status.validate_transition(WorkItemStatus.IN_PROGRESS)

        event = StatusChanged(
            aggregate_id=self._id,
            aggregate_type="WorkItem",
            old_status=self._status.value,
            new_status=WorkItemStatus.IN_PROGRESS.value,
        )
        self._raise_event(event)

    def block(self, reason: str = "") -> None:
        """Transition to blocked status.

        Args:
            reason: Why the work is blocked

        Raises:
            InvalidStateTransitionError: If not in in_progress status
        """
        self._status.validate_transition(WorkItemStatus.BLOCKED)

        event = StatusChanged(
            aggregate_id=self._id,
            aggregate_type="WorkItem",
            old_status=self._status.value,
            new_status=WorkItemStatus.BLOCKED.value,
            reason=reason,
        )
        self._raise_event(event)

    def unblock(self) -> None:
        """Resume work after being blocked.

        Raises:
            InvalidStateTransitionError: If not in blocked status
        """
        self._status.validate_transition(WorkItemStatus.IN_PROGRESS)

        event = StatusChanged(
            aggregate_id=self._id,
            aggregate_type="WorkItem",
            old_status=self._status.value,
            new_status=WorkItemStatus.IN_PROGRESS.value,
        )
        self._raise_event(event)

    def complete(self, quality_passed: bool = True) -> None:
        """Complete the work item.

        Args:
            quality_passed: Whether quality gate validation passed

        Raises:
            InvalidStateTransitionError: If not in in_progress status
            QualityGateError: If quality validation failed
        """
        self._status.validate_transition(WorkItemStatus.DONE)

        if not quality_passed:
            raise QualityGateError(
                f"Work item {self._id} failed quality gate validation"
            )

        event = WorkItemCompleted(
            aggregate_id=self._id,
            aggregate_type="WorkItem",
            quality_passed=quality_passed,
        )
        self._raise_event(event)

    def cancel(self, reason: str = "") -> None:
        """Cancel the work item.

        Args:
            reason: Why the work was cancelled

        Raises:
            InvalidStateTransitionError: If already in terminal state
        """
        self._status.validate_transition(WorkItemStatus.CANCELLED)

        event = StatusChanged(
            aggregate_id=self._id,
            aggregate_type="WorkItem",
            old_status=self._status.value,
            new_status=WorkItemStatus.CANCELLED.value,
            reason=reason,
        )
        self._raise_event(event)

    def set_priority(self, priority: Priority) -> None:
        """Change work item priority.

        Args:
            priority: New priority level
        """
        if self._status.is_terminal:
            raise InvalidStateError(
                f"Cannot modify completed/cancelled work item {self._id}"
            )

        event = PriorityChanged(
            aggregate_id=self._id,
            aggregate_type="WorkItem",
            old_priority=self._priority.value,
            new_priority=priority.value,
        )
        self._raise_event(event)

    def _apply(self, event: DomainEvent) -> None:
        """Apply event to update aggregate state.

        This method is deterministic and side-effect free.
        Called during both event recording and history replay.
        """
        match event:
            case WorkItemCreated():
                self._title = event.title
                self._work_type = event.work_type
                self._priority = Priority.from_string(event.priority)
                self._description = event.description
                self._parent_id = event.parent_id
                self._status = WorkItemStatus.PENDING

            case StatusChanged():
                self._status = WorkItemStatus(event.new_status)

            case PriorityChanged():
                self._priority = Priority(event.new_priority)

            case WorkItemCompleted():
                self._status = WorkItemStatus.DONE
                self._quality_passed = event.quality_passed

    # Properties
    @property
    def title(self) -> str:
        return self._title

    @property
    def status(self) -> WorkItemStatus:
        return self._status

    @property
    def priority(self) -> Priority:
        return self._priority

    @property
    def work_type(self) -> str:
        return self._work_type
```

---

## State Machine

```
                    ┌───────────────────────────────────────┐
                    │                                       │
                    ▼                                       │
┌──────────┐    ┌──────────────┐    ┌──────────┐    ┌─────┴────┐
│ PENDING  │───►│ IN_PROGRESS  │◄──►│ BLOCKED  │    │ CANCELLED│
└────┬─────┘    └──────┬───────┘    └──────────┘    └──────────┘
     │                 │                                  ▲
     │                 ▼                                  │
     │          ┌──────────┐                             │
     └─────────►│   DONE   │                             │
                └──────────┘                             │
                      │                                  │
                      └──────────────────────────────────┘
                           (reopen)
```

Valid Transitions:
- `PENDING` → `IN_PROGRESS`, `CANCELLED`
- `IN_PROGRESS` → `BLOCKED`, `DONE`, `CANCELLED`
- `BLOCKED` → `IN_PROGRESS`, `CANCELLED`
- `DONE` → `IN_PROGRESS` (reopen)
- `CANCELLED` → (terminal, no transitions)

---

## Usage Examples

### Create and Complete

```python
# Create new work item
item = WorkItem.create(
    id="WORK-001",
    title="Implement user authentication",
    work_type="story",
    priority="high",
)

# Start work
item.start()

# Complete with quality check
item.complete(quality_passed=True)

# Get events for persistence
events = item.collect_events()
repository.save(item)
event_publisher.publish(events)
```

### Handle Blocking

```python
item = WorkItem.create(id="WORK-002", title="API integration")
item.start()

# Work is blocked by external dependency
item.block(reason="Waiting for API credentials")

# Later, unblock and continue
item.unblock()
item.complete()
```

---

## Testing Pattern

```python
def test_work_item_lifecycle_happy_path():
    """Work item follows expected lifecycle."""
    item = WorkItem.create(id="WORK-001", title="Test Task")
    assert item.status == WorkItemStatus.PENDING

    item.start()
    assert item.status == WorkItemStatus.IN_PROGRESS

    item.complete()
    assert item.status == WorkItemStatus.DONE

    events = item.collect_events()
    assert len(events) == 3
    assert isinstance(events[0], WorkItemCreated)
    assert isinstance(events[1], StatusChanged)
    assert isinstance(events[2], WorkItemCompleted)


def test_work_item_rejects_invalid_transition():
    """Cannot complete from pending status."""
    item = WorkItem.create(id="WORK-001", title="Test Task")

    with pytest.raises(InvalidStateTransitionError):
        item.complete()  # Must start() first


def test_work_item_reconstitutes_from_history():
    """Aggregate can be rebuilt from event stream."""
    events = [
        WorkItemCreated(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            title="Test",
            work_type="task",
            priority="medium",
        ),
        StatusChanged(
            aggregate_id="WORK-001",
            aggregate_type="WorkItem",
            old_status="pending",
            new_status="in_progress",
        ),
    ]

    item = WorkItem.load_from_history(events)

    assert item.id == "WORK-001"
    assert item.title == "Test"
    assert item.status == WorkItemStatus.IN_PROGRESS
    assert item.version == 2
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: WorkItem is the only aggregate in work tracking. Phase and Plan are separate aggregates referenced by ID, not nested. This keeps aggregates small and focused.

> **Jerry Decision**: Quality gate check is enforced at completion time. Cannot complete without `quality_passed=True` (or explicit override).

> **Jerry Decision**: Cancelled items are terminal. To "uncancel", create a new work item referencing the old one.

---

## References

- **Eric Evans**: Domain-Driven Design (2003), Chapter 6 - Aggregates
- **Vaughn Vernon**: Implementing DDD (2013), Chapter 10 - Aggregates
- **Design Canon**: Section 5.4 - Aggregate Root Pattern
- **Related Patterns**: PAT-ENT-003 (AggregateRoot), PAT-VO-002 (WorkItemStatus)
