"""
WorkItemStatus - Work item lifecycle status value object.

Represents the lifecycle state of a work item with validated
state transitions.

References:
    - PAT-004-e006: Status State Machine
    - WORKTRACKER: Work item lifecycle
"""
from __future__ import annotations

from enum import Enum


class InvalidStateTransitionError(ValueError):
    """
    Raised when an invalid state transition is attempted.

    Contains details about the attempted transition for debugging.
    """

    def __init__(self, from_status: str, to_status: str) -> None:
        self.from_status = from_status
        self.to_status = to_status
        super().__init__(
            f"Cannot transition from '{from_status}' to '{to_status}'"
        )


# Module-level constant for valid transitions (avoids enum member issues)
_VALID_TRANSITIONS: dict[str, set[str]] = {
    "pending": {"in_progress", "cancelled"},
    "in_progress": {"blocked", "done", "cancelled"},
    "blocked": {"in_progress", "cancelled"},
    "done": {"in_progress"},  # Reopen capability
    "cancelled": set(),  # Terminal state
}


class WorkItemStatus(Enum):
    """
    Work item lifecycle status.

    States form a directed graph with valid transitions.
    Invalid transitions raise InvalidStateTransitionError.

    State Machine:
        ```
        PENDING ──────► IN_PROGRESS ──────► DONE
           │                │    ▲            │
           │                ▼    │            │
           │            BLOCKED ─┘            │
           │                │                 │
           ▼                ▼                 ▼
        CANCELLED ◄─────────┴─────────────────┘
                          (reopen)
        ```

    Valid Transitions:
        - PENDING → IN_PROGRESS, CANCELLED
        - IN_PROGRESS → BLOCKED, DONE, CANCELLED
        - BLOCKED → IN_PROGRESS, CANCELLED
        - DONE → IN_PROGRESS (reopen capability)
        - CANCELLED → (terminal state, no transitions)

    Example:
        >>> status = WorkItemStatus.PENDING
        >>> status.can_transition_to(WorkItemStatus.IN_PROGRESS)
        True
        >>> status.can_transition_to(WorkItemStatus.DONE)
        False
    """

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    DONE = "done"
    CANCELLED = "cancelled"

    def can_transition_to(self, target: WorkItemStatus) -> bool:
        """
        Check if transition to target status is valid.

        Args:
            target: The target status to transition to

        Returns:
            True if the transition is valid, False otherwise

        Example:
            >>> WorkItemStatus.PENDING.can_transition_to(WorkItemStatus.IN_PROGRESS)
            True
            >>> WorkItemStatus.CANCELLED.can_transition_to(WorkItemStatus.PENDING)
            False
        """
        valid = _VALID_TRANSITIONS.get(self.value, set())
        return target.value in valid

    def validate_transition(self, target: WorkItemStatus) -> None:
        """
        Raise if transition is invalid.

        Args:
            target: The target status to transition to

        Raises:
            InvalidStateTransitionError: If the transition is not allowed

        Example:
            >>> status = WorkItemStatus.CANCELLED
            >>> status.validate_transition(WorkItemStatus.PENDING)
            Traceback (most recent call last):
                ...
            InvalidStateTransitionError: Cannot transition from 'cancelled' to 'pending'
        """
        if not self.can_transition_to(target):
            raise InvalidStateTransitionError(self.value, target.value)

    def get_valid_transitions(self) -> list[WorkItemStatus]:
        """
        Get list of valid target statuses from current status.

        Returns:
            List of WorkItemStatus values that can be transitioned to

        Example:
            >>> WorkItemStatus.PENDING.get_valid_transitions()
            [<WorkItemStatus.IN_PROGRESS: 'in_progress'>, <WorkItemStatus.CANCELLED: 'cancelled'>]
        """
        valid_values = _VALID_TRANSITIONS.get(self.value, set())
        return [WorkItemStatus(v) for v in sorted(valid_values)]

    @property
    def is_terminal(self) -> bool:
        """
        Check if this is a terminal state.

        Terminal states represent completed work (successfully or not).

        Returns:
            True if this is DONE or CANCELLED

        Example:
            >>> WorkItemStatus.DONE.is_terminal
            True
            >>> WorkItemStatus.IN_PROGRESS.is_terminal
            False
        """
        return self in (WorkItemStatus.DONE, WorkItemStatus.CANCELLED)

    @property
    def is_active(self) -> bool:
        """
        Check if this is an active work state.

        Active states represent work that is currently being done.

        Returns:
            True if this is IN_PROGRESS or BLOCKED

        Example:
            >>> WorkItemStatus.IN_PROGRESS.is_active
            True
            >>> WorkItemStatus.PENDING.is_active
            False
        """
        return self in (WorkItemStatus.IN_PROGRESS, WorkItemStatus.BLOCKED)

    @property
    def is_waiting(self) -> bool:
        """
        Check if this is a waiting state.

        Waiting states represent work that hasn't started yet.

        Returns:
            True if this is PENDING

        Example:
            >>> WorkItemStatus.PENDING.is_waiting
            True
        """
        return self == WorkItemStatus.PENDING

    @property
    def is_blocked(self) -> bool:
        """
        Check if work is blocked.

        Returns:
            True if this is BLOCKED

        Example:
            >>> WorkItemStatus.BLOCKED.is_blocked
            True
        """
        return self == WorkItemStatus.BLOCKED

    @property
    def is_complete(self) -> bool:
        """
        Check if work is successfully completed.

        Returns:
            True if this is DONE

        Example:
            >>> WorkItemStatus.DONE.is_complete
            True
        """
        return self == WorkItemStatus.DONE

    def __str__(self) -> str:
        """Return the status value as string."""
        return self.value

    def __repr__(self) -> str:
        """Return detailed representation for debugging."""
        return f"WorkItemStatus.{self.name}"
