# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Domain Errors - Business Rule Violation Exceptions

These exceptions represent violations of domain invariants and business rules.
They should be raised when domain objects cannot be created or operations
cannot be performed due to invalid state.
"""

from __future__ import annotations


class DomainError(Exception):
    """Base class for all domain errors.

    All domain-specific exceptions should inherit from this class
    to enable consistent error handling at the application layer.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class InvalidProjectIdError(DomainError):
    """Raised when a project ID does not conform to the required format.

    Valid format: PROJ-{nnn}-{slug}
    Where:
        - nnn: Three-digit zero-padded number (001-999)
        - slug: Kebab-case alphanumeric string (1-50 chars)
    """

    def __init__(self, value: str, reason: str) -> None:
        self.value = value
        self.reason = reason
        super().__init__(f"Invalid project ID '{value}': {reason}")


class ProjectNotFoundError(DomainError):
    """Raised when a project cannot be found at the expected location."""

    def __init__(self, project_id: str, path: str | None = None) -> None:
        self.project_id = project_id
        self.path = path
        message = f"Project '{project_id}' not found"
        if path:
            message += f" at path '{path}'"
        super().__init__(message)


class ProjectValidationError(DomainError):
    """Raised when project validation fails."""

    def __init__(self, project_id: str, issues: list[str]) -> None:
        self.project_id = project_id
        self.issues = issues
        issues_str = "; ".join(issues)
        super().__init__(f"Project '{project_id}' validation failed: {issues_str}")
