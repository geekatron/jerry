# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Domain exceptions for Jerry Framework.

All domain-specific exceptions should be defined here.
Application and infrastructure layers may wrap these in their own exceptions.

References:
    - Canon PAT-011 (L1812-1859)
    - Gap Analysis G-001 (L288-301)
"""

from __future__ import annotations


class DomainError(Exception):
    """Base class for all domain errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class NotFoundError(DomainError):
    """Entity not found."""

    def __init__(self, entity_type: str, entity_id: str) -> None:
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} '{entity_id}' not found")


class InvalidStateError(DomainError):
    """Operation invalid for current state."""

    def __init__(self, current_state: str, attempted_action: str) -> None:
        self.current_state = current_state
        self.attempted_action = attempted_action
        super().__init__(f"Cannot {attempted_action} in state {current_state}")


class InvalidStateTransitionError(DomainError):
    """State transition not allowed."""

    def __init__(self, from_state: str, to_state: str) -> None:
        self.from_state = from_state
        self.to_state = to_state
        super().__init__(f"Transition from {from_state} to {to_state} not allowed")


class InvariantViolationError(DomainError):
    """Domain invariant violated."""

    def __init__(self, invariant: str, details: str) -> None:
        self.invariant = invariant
        self.details = details
        super().__init__(f"Invariant '{invariant}' violated: {details}")


class ConcurrencyError(DomainError):
    """Optimistic concurrency conflict."""

    def __init__(self, expected_version: int, actual_version: int) -> None:
        self.expected_version = expected_version
        self.actual_version = actual_version
        super().__init__(
            f"Concurrency conflict: expected version {expected_version}, "
            f"actual version {actual_version}"
        )


class ValidationError(DomainError):
    """Input validation failed."""

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.validation_message = message
        super().__init__(f"Validation failed for '{field}': {message}")
