"""
Exception Hierarchy Pattern - Canonical implementation for Jerry Framework.

All domain exceptions inherit from DomainError base class.
Include entity type, ID, and suggested action in error messages.

References:
    - coding-standards.md (Error Handling section)
    - shared_kernel/exceptions.py
    - quality-enforcement.md (exception table)

Exports:
    DomainError hierarchy following Jerry conventions
"""

from __future__ import annotations

# =============================================================================
# Base Exception
# =============================================================================


class DomainError(Exception):
    """
    Base class for all domain errors.

    All domain-specific exceptions SHOULD inherit from this base class.
    Application and infrastructure layers may wrap these in their own exceptions.

    Attributes:
        message: Human-readable error message

    Example:
        >>> try:
        ...     raise ValidationError("email", "Invalid format")
        ... except DomainError as e:
        ...     print(e.message)
        'Validation failed for 'email': Invalid format'
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


# =============================================================================
# Validation Errors
# =============================================================================


class ValidationError(DomainError):
    """
    Input validation failed.

    Use when user input or command data fails validation rules.

    Attributes:
        field: Field name that failed validation
        validation_message: Reason for validation failure

    Example:
        >>> raise ValidationError("email", "Must contain @ character")
        ValidationError: Validation failed for 'email': Must contain @ character
    """

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.validation_message = message
        super().__init__(f"Validation failed for '{field}': {message}")


# =============================================================================
# Entity Not Found
# =============================================================================


class NotFoundError(DomainError):
    """
    Entity not found in repository.

    Use when attempting to retrieve an entity that doesn't exist.

    Attributes:
        entity_type: Type of entity (e.g., "WorkItem", "Project")
        entity_id: Identifier that was not found

    Example:
        >>> raise NotFoundError("WorkItem", "WORK-001")
        NotFoundError: WorkItem 'WORK-001' not found
    """

    def __init__(self, entity_type: str, entity_id: str) -> None:
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} '{entity_id}' not found")


# =============================================================================
# State Management Errors
# =============================================================================


class InvalidStateError(DomainError):
    """
    Operation invalid for current state.

    Use when an operation cannot be performed in the current aggregate state.

    Attributes:
        current_state: Current state value
        attempted_action: Action that was attempted

    Example:
        >>> raise InvalidStateError("cancelled", "assign to user")
        InvalidStateError: Cannot assign to user in state cancelled
    """

    def __init__(self, current_state: str, attempted_action: str) -> None:
        self.current_state = current_state
        self.attempted_action = attempted_action
        super().__init__(f"Cannot {attempted_action} in state {current_state}")


class InvalidStateTransitionError(DomainError):
    """
    State transition not allowed by state machine rules.

    Use when attempting an invalid state transition.

    Attributes:
        from_state: Current state
        to_state: Attempted target state

    Example:
        >>> raise InvalidStateTransitionError("done", "in_progress")
        InvalidStateTransitionError: Transition from done to in_progress not allowed
    """

    def __init__(self, from_state: str, to_state: str) -> None:
        self.from_state = from_state
        self.to_state = to_state
        super().__init__(f"Transition from {from_state} to {to_state} not allowed")


# =============================================================================
# Business Rule Violations
# =============================================================================


class InvariantViolationError(DomainError):
    """
    Domain invariant violated.

    Use when a business rule or invariant is violated.

    Attributes:
        invariant: Name of the invariant that was violated
        details: Detailed explanation

    Example:
        >>> raise InvariantViolationError(
        ...     "unique_title",
        ...     "Work item with title 'Implement login' already exists"
        ... )
        InvariantViolationError: Invariant 'unique_title' violated: Work item with title...
    """

    def __init__(self, invariant: str, details: str) -> None:
        self.invariant = invariant
        self.details = details
        super().__init__(f"Invariant '{invariant}' violated: {details}")


# =============================================================================
# Concurrency Errors
# =============================================================================


class ConcurrencyError(DomainError):
    """
    Optimistic concurrency conflict detected.

    Use when attempting to save an aggregate with a stale version.

    Attributes:
        expected_version: Version the operation expected
        actual_version: Actual version in storage

    Example:
        >>> raise ConcurrencyError(expected_version=5, actual_version=7)
        ConcurrencyError: Concurrency conflict: expected version 5, actual version 7
    """

    def __init__(self, expected_version: int, actual_version: int) -> None:
        self.expected_version = expected_version
        self.actual_version = actual_version
        super().__init__(
            f"Concurrency conflict: expected version {expected_version}, "
            f"actual version {actual_version}"
        )


# =============================================================================
# Quality Gate Errors
# =============================================================================


class QualityGateError(DomainError):
    """
    Quality gate check failed.

    Use when work item fails to meet quality threshold.

    Attributes:
        work_item_id: ID of the work item
        gate_level: Quality gate level (L0, L1, L2, etc.)
        failures: List of specific failures

    Example:
        >>> raise QualityGateError(
        ...     "WORK-001",
        ...     "L2",
        ...     ["Coverage below 90%", "Missing negative tests"]
        ... )
        QualityGateError: Quality gate L2 failed for WORK-001: Coverage below 90%, ...
    """

    def __init__(
        self,
        work_item_id: str,
        gate_level: str,
        failures: list[str] | None = None,
    ) -> None:
        self.work_item_id = work_item_id
        self.gate_level = gate_level
        self.failures = failures or []

        failure_msg = ", ".join(self.failures) if self.failures else "No details"
        super().__init__(f"Quality gate {gate_level} failed for {work_item_id}: {failure_msg}")


# =============================================================================
# Usage Guidelines
# =============================================================================

"""
Exception Selection Guide:

| Scenario                          | Exception                        |
|-----------------------------------|----------------------------------|
| Invalid input values              | ValidationError                  |
| Entity not found                  | NotFoundError                    |
| Wrong state for operation         | InvalidStateError                |
| State machine violation           | InvalidStateTransitionError      |
| Business rule violation           | InvariantViolationError          |
| Version conflict                  | ConcurrencyError                 |
| Quality check failed              | QualityGateError                 |

Error Message Guidelines:
1. Include entity type and ID
2. Describe what went wrong
3. Suggest corrective action when possible
4. Use present tense for clarity

Example:
    ✓ "Cannot transition from done to in_progress. Work items in done state are immutable."
    ✗ "Invalid state transition"

Re-raising Pattern:
    try:
        operation()
    except IOError as e:
        raise InfrastructureError("Failed to read file") from e
        # ^^ Use 'from e' to preserve exception context
"""
