"""Unit tests for work_tracking.domain.value_objects.work_item_status module.

Test Categories:
    - Happy Path: Valid state transitions
    - Edge Cases: Terminal states, reopen capability
    - Negative Cases: Invalid transitions
    - State Machine: Full transition graph validation

References:
    - PAT-004-e006: Status State Machine
    - WORKTRACKER: Work item lifecycle
"""

from __future__ import annotations

import pytest

from src.work_tracking.domain.value_objects.work_item_status import (
    InvalidStateTransitionError,
    WorkItemStatus,
)


class TestWorkItemStatusValues:
    """Tests for WorkItemStatus enum values."""

    def test_pending_value(self) -> None:
        """PENDING has value 'pending'."""
        assert WorkItemStatus.PENDING.value == "pending"

    def test_in_progress_value(self) -> None:
        """IN_PROGRESS has value 'in_progress'."""
        assert WorkItemStatus.IN_PROGRESS.value == "in_progress"

    def test_blocked_value(self) -> None:
        """BLOCKED has value 'blocked'."""
        assert WorkItemStatus.BLOCKED.value == "blocked"

    def test_done_value(self) -> None:
        """DONE has value 'done'."""
        assert WorkItemStatus.DONE.value == "done"

    def test_cancelled_value(self) -> None:
        """CANCELLED has value 'cancelled'."""
        assert WorkItemStatus.CANCELLED.value == "cancelled"

    def test_can_construct_from_string(self) -> None:
        """WorkItemStatus can be constructed from string value."""
        assert WorkItemStatus("pending") == WorkItemStatus.PENDING
        assert WorkItemStatus("in_progress") == WorkItemStatus.IN_PROGRESS


class TestWorkItemStatusTransitions:
    """Tests for valid state transitions."""

    # PENDING transitions
    def test_pending_to_in_progress(self) -> None:
        """PENDING can transition to IN_PROGRESS."""
        assert WorkItemStatus.PENDING.can_transition_to(WorkItemStatus.IN_PROGRESS)

    def test_pending_to_cancelled(self) -> None:
        """PENDING can transition to CANCELLED."""
        assert WorkItemStatus.PENDING.can_transition_to(WorkItemStatus.CANCELLED)

    def test_pending_cannot_go_to_done(self) -> None:
        """PENDING cannot transition directly to DONE."""
        assert not WorkItemStatus.PENDING.can_transition_to(WorkItemStatus.DONE)

    def test_pending_cannot_go_to_blocked(self) -> None:
        """PENDING cannot transition directly to BLOCKED."""
        assert not WorkItemStatus.PENDING.can_transition_to(WorkItemStatus.BLOCKED)

    # IN_PROGRESS transitions
    def test_in_progress_to_blocked(self) -> None:
        """IN_PROGRESS can transition to BLOCKED."""
        assert WorkItemStatus.IN_PROGRESS.can_transition_to(WorkItemStatus.BLOCKED)

    def test_in_progress_to_done(self) -> None:
        """IN_PROGRESS can transition to DONE."""
        assert WorkItemStatus.IN_PROGRESS.can_transition_to(WorkItemStatus.DONE)

    def test_in_progress_to_cancelled(self) -> None:
        """IN_PROGRESS can transition to CANCELLED."""
        assert WorkItemStatus.IN_PROGRESS.can_transition_to(WorkItemStatus.CANCELLED)

    def test_in_progress_cannot_go_to_pending(self) -> None:
        """IN_PROGRESS cannot transition back to PENDING."""
        assert not WorkItemStatus.IN_PROGRESS.can_transition_to(WorkItemStatus.PENDING)

    # BLOCKED transitions
    def test_blocked_to_in_progress(self) -> None:
        """BLOCKED can transition back to IN_PROGRESS."""
        assert WorkItemStatus.BLOCKED.can_transition_to(WorkItemStatus.IN_PROGRESS)

    def test_blocked_to_cancelled(self) -> None:
        """BLOCKED can transition to CANCELLED."""
        assert WorkItemStatus.BLOCKED.can_transition_to(WorkItemStatus.CANCELLED)

    def test_blocked_cannot_go_to_done(self) -> None:
        """BLOCKED cannot transition directly to DONE."""
        assert not WorkItemStatus.BLOCKED.can_transition_to(WorkItemStatus.DONE)

    # DONE transitions (reopen capability)
    def test_done_to_in_progress(self) -> None:
        """DONE can transition to IN_PROGRESS (reopen)."""
        assert WorkItemStatus.DONE.can_transition_to(WorkItemStatus.IN_PROGRESS)

    def test_done_cannot_go_to_pending(self) -> None:
        """DONE cannot transition to PENDING."""
        assert not WorkItemStatus.DONE.can_transition_to(WorkItemStatus.PENDING)

    def test_done_cannot_go_to_cancelled(self) -> None:
        """DONE cannot transition to CANCELLED."""
        assert not WorkItemStatus.DONE.can_transition_to(WorkItemStatus.CANCELLED)

    # CANCELLED transitions (terminal)
    def test_cancelled_cannot_transition(self) -> None:
        """CANCELLED is terminal - no transitions allowed."""
        assert not WorkItemStatus.CANCELLED.can_transition_to(WorkItemStatus.PENDING)
        assert not WorkItemStatus.CANCELLED.can_transition_to(WorkItemStatus.IN_PROGRESS)
        assert not WorkItemStatus.CANCELLED.can_transition_to(WorkItemStatus.BLOCKED)
        assert not WorkItemStatus.CANCELLED.can_transition_to(WorkItemStatus.DONE)


class TestWorkItemStatusValidateTransition:
    """Tests for validate_transition method."""

    def test_valid_transition_does_not_raise(self) -> None:
        """validate_transition succeeds for valid transitions."""
        # Should not raise
        WorkItemStatus.PENDING.validate_transition(WorkItemStatus.IN_PROGRESS)

    def test_invalid_transition_raises(self) -> None:
        """validate_transition raises for invalid transitions."""
        with pytest.raises(InvalidStateTransitionError) as exc_info:
            WorkItemStatus.PENDING.validate_transition(WorkItemStatus.DONE)

        assert exc_info.value.from_status == "pending"
        assert exc_info.value.to_status == "done"

    def test_error_message_format(self) -> None:
        """InvalidStateTransitionError has descriptive message."""
        with pytest.raises(InvalidStateTransitionError) as exc_info:
            WorkItemStatus.CANCELLED.validate_transition(WorkItemStatus.PENDING)

        assert "cancelled" in str(exc_info.value)
        assert "pending" in str(exc_info.value)


class TestWorkItemStatusGetValidTransitions:
    """Tests for get_valid_transitions method."""

    def test_pending_valid_transitions(self) -> None:
        """PENDING has correct valid transitions."""
        valid = WorkItemStatus.PENDING.get_valid_transitions()
        assert set(valid) == {WorkItemStatus.IN_PROGRESS, WorkItemStatus.CANCELLED}

    def test_in_progress_valid_transitions(self) -> None:
        """IN_PROGRESS has correct valid transitions."""
        valid = WorkItemStatus.IN_PROGRESS.get_valid_transitions()
        assert set(valid) == {
            WorkItemStatus.BLOCKED,
            WorkItemStatus.DONE,
            WorkItemStatus.CANCELLED,
        }

    def test_blocked_valid_transitions(self) -> None:
        """BLOCKED has correct valid transitions."""
        valid = WorkItemStatus.BLOCKED.get_valid_transitions()
        assert set(valid) == {WorkItemStatus.IN_PROGRESS, WorkItemStatus.CANCELLED}

    def test_done_valid_transitions(self) -> None:
        """DONE has correct valid transitions (reopen only)."""
        valid = WorkItemStatus.DONE.get_valid_transitions()
        assert valid == [WorkItemStatus.IN_PROGRESS]

    def test_cancelled_valid_transitions(self) -> None:
        """CANCELLED has no valid transitions."""
        valid = WorkItemStatus.CANCELLED.get_valid_transitions()
        assert valid == []


class TestWorkItemStatusProperties:
    """Tests for status property methods."""

    def test_is_terminal_done(self) -> None:
        """DONE is a terminal state."""
        assert WorkItemStatus.DONE.is_terminal is True

    def test_is_terminal_cancelled(self) -> None:
        """CANCELLED is a terminal state."""
        assert WorkItemStatus.CANCELLED.is_terminal is True

    def test_is_terminal_in_progress(self) -> None:
        """IN_PROGRESS is not a terminal state."""
        assert WorkItemStatus.IN_PROGRESS.is_terminal is False

    def test_is_terminal_pending(self) -> None:
        """PENDING is not a terminal state."""
        assert WorkItemStatus.PENDING.is_terminal is False

    def test_is_active_in_progress(self) -> None:
        """IN_PROGRESS is an active state."""
        assert WorkItemStatus.IN_PROGRESS.is_active is True

    def test_is_active_blocked(self) -> None:
        """BLOCKED is an active state."""
        assert WorkItemStatus.BLOCKED.is_active is True

    def test_is_active_pending(self) -> None:
        """PENDING is not an active state."""
        assert WorkItemStatus.PENDING.is_active is False

    def test_is_active_done(self) -> None:
        """DONE is not an active state."""
        assert WorkItemStatus.DONE.is_active is False

    def test_is_waiting_pending(self) -> None:
        """PENDING is a waiting state."""
        assert WorkItemStatus.PENDING.is_waiting is True

    def test_is_waiting_in_progress(self) -> None:
        """IN_PROGRESS is not a waiting state."""
        assert WorkItemStatus.IN_PROGRESS.is_waiting is False

    def test_is_blocked_blocked(self) -> None:
        """BLOCKED is blocked."""
        assert WorkItemStatus.BLOCKED.is_blocked is True

    def test_is_blocked_in_progress(self) -> None:
        """IN_PROGRESS is not blocked."""
        assert WorkItemStatus.IN_PROGRESS.is_blocked is False

    def test_is_complete_done(self) -> None:
        """DONE is complete."""
        assert WorkItemStatus.DONE.is_complete is True

    def test_is_complete_cancelled(self) -> None:
        """CANCELLED is not complete (it's cancelled, not done)."""
        assert WorkItemStatus.CANCELLED.is_complete is False


class TestWorkItemStatusStringRepresentation:
    """Tests for string representations."""

    def test_str_returns_value(self) -> None:
        """str() returns the status value."""
        assert str(WorkItemStatus.PENDING) == "pending"
        assert str(WorkItemStatus.IN_PROGRESS) == "in_progress"

    def test_repr_format(self) -> None:
        """repr() shows enum member name."""
        assert repr(WorkItemStatus.PENDING) == "WorkItemStatus.PENDING"
        assert repr(WorkItemStatus.IN_PROGRESS) == "WorkItemStatus.IN_PROGRESS"


class TestInvalidStateTransitionError:
    """Tests for InvalidStateTransitionError exception."""

    def test_error_has_from_status(self) -> None:
        """Error stores from_status."""
        error = InvalidStateTransitionError("pending", "done")
        assert error.from_status == "pending"

    def test_error_has_to_status(self) -> None:
        """Error stores to_status."""
        error = InvalidStateTransitionError("pending", "done")
        assert error.to_status == "done"

    def test_error_is_value_error(self) -> None:
        """Error is a ValueError subclass."""
        error = InvalidStateTransitionError("pending", "done")
        assert isinstance(error, ValueError)

    def test_error_message(self) -> None:
        """Error has descriptive message."""
        error = InvalidStateTransitionError("pending", "done")
        assert "pending" in str(error)
        assert "done" in str(error)
        assert "Cannot transition" in str(error)


class TestWorkItemStatusStateMachine:
    """Integration tests for the full state machine."""

    def test_happy_path_workflow(self) -> None:
        """Test typical workflow: PENDING -> IN_PROGRESS -> DONE."""
        status = WorkItemStatus.PENDING

        # Start work
        status.validate_transition(WorkItemStatus.IN_PROGRESS)
        status = WorkItemStatus.IN_PROGRESS

        # Complete work
        status.validate_transition(WorkItemStatus.DONE)
        status = WorkItemStatus.DONE

        assert status.is_complete

    def test_blocked_then_resumed(self) -> None:
        """Test blocked workflow: IN_PROGRESS -> BLOCKED -> IN_PROGRESS -> DONE."""
        status = WorkItemStatus.IN_PROGRESS

        # Get blocked
        status.validate_transition(WorkItemStatus.BLOCKED)
        status = WorkItemStatus.BLOCKED
        assert status.is_blocked

        # Resume work
        status.validate_transition(WorkItemStatus.IN_PROGRESS)
        status = WorkItemStatus.IN_PROGRESS
        assert status.is_active

        # Complete
        status.validate_transition(WorkItemStatus.DONE)
        status = WorkItemStatus.DONE
        assert status.is_complete

    def test_reopen_workflow(self) -> None:
        """Test reopen: DONE -> IN_PROGRESS -> DONE."""
        status = WorkItemStatus.DONE

        # Reopen
        status.validate_transition(WorkItemStatus.IN_PROGRESS)
        status = WorkItemStatus.IN_PROGRESS

        # Complete again
        status.validate_transition(WorkItemStatus.DONE)
        status = WorkItemStatus.DONE

        assert status.is_complete

    def test_cancelled_is_final(self) -> None:
        """Test that cancelled is truly terminal."""
        status = WorkItemStatus.CANCELLED

        for target in WorkItemStatus:
            if target != status:
                assert not status.can_transition_to(target)
