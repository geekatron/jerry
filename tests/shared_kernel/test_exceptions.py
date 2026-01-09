"""Unit tests for shared_kernel.exceptions module."""
from __future__ import annotations

import pytest

from src.shared_kernel.exceptions import (
    ConcurrencyError,
    DomainError,
    InvariantViolationError,
    InvalidStateError,
    InvalidStateTransitionError,
    NotFoundError,
    ValidationError,
)


class TestDomainError:
    """Tests for DomainError base class."""

    def test_domain_error_message(self) -> None:
        """DomainError stores message."""
        error = DomainError("Something went wrong")
        assert error.message == "Something went wrong"
        assert str(error) == "Something went wrong"

    def test_domain_error_is_exception(self) -> None:
        """DomainError is an Exception."""
        assert issubclass(DomainError, Exception)


class TestNotFoundError:
    """Tests for NotFoundError."""

    def test_not_found_error_message(self) -> None:
        """NotFoundError formats message correctly."""
        error = NotFoundError("Task", "TASK-12345678")
        assert error.entity_type == "Task"
        assert error.entity_id == "TASK-12345678"
        assert str(error) == "Task 'TASK-12345678' not found"

    def test_not_found_error_inheritance(self) -> None:
        """NotFoundError inherits from DomainError."""
        error = NotFoundError("Task", "TASK-12345678")
        assert isinstance(error, DomainError)


class TestInvalidStateError:
    """Tests for InvalidStateError."""

    def test_invalid_state_error_message(self) -> None:
        """InvalidStateError formats message correctly."""
        error = InvalidStateError("COMPLETED", "complete")
        assert error.current_state == "COMPLETED"
        assert error.attempted_action == "complete"
        assert str(error) == "Cannot complete in state COMPLETED"


class TestInvalidStateTransitionError:
    """Tests for InvalidStateTransitionError."""

    def test_invalid_state_transition_error_message(self) -> None:
        """InvalidStateTransitionError formats message correctly."""
        error = InvalidStateTransitionError("PENDING", "COMPLETED")
        assert error.from_state == "PENDING"
        assert error.to_state == "COMPLETED"
        assert str(error) == "Transition from PENDING to COMPLETED not allowed"


class TestInvariantViolationError:
    """Tests for InvariantViolationError."""

    def test_invariant_violation_error_message(self) -> None:
        """InvariantViolationError formats message correctly."""
        error = InvariantViolationError("non_empty_title", "Title cannot be empty")
        assert error.invariant == "non_empty_title"
        assert error.details == "Title cannot be empty"
        assert str(error) == "Invariant 'non_empty_title' violated: Title cannot be empty"


class TestConcurrencyError:
    """Tests for ConcurrencyError."""

    def test_concurrency_error_message(self) -> None:
        """ConcurrencyError formats message correctly."""
        error = ConcurrencyError(expected_version=5, actual_version=7)
        assert error.expected_version == 5
        assert error.actual_version == 7
        assert "expected version 5" in str(error)
        assert "actual version 7" in str(error)


class TestValidationError:
    """Tests for ValidationError."""

    def test_validation_error_message(self) -> None:
        """ValidationError formats message correctly."""
        error = ValidationError("email", "must be a valid email address")
        assert error.field == "email"
        assert error.validation_message == "must be a valid email address"
        assert str(error) == "Validation failed for 'email': must be a valid email address"
