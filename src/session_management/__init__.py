"""
Session Management Bounded Context

This bounded context handles project/session enforcement at Claude Code
session start. It validates JERRY_PROJECT environment variable and guides
users through project selection or creation.

Architecture:
    - domain/: Pure business logic (value objects, entities, events)
    - application/: Use cases (queries, commands, ports)
    - infrastructure/: Adapters (filesystem, environment)
"""

from .domain import (
    ProjectId,
    ProjectStatus,
    ProjectInfo,
    ValidationResult,
    InvalidProjectIdError,
    ProjectNotFoundError,
    ProjectValidationError,
    DomainError,
)

__all__ = [
    # Value Objects
    "ProjectId",
    "ProjectStatus",
    "ValidationResult",
    # Entities
    "ProjectInfo",
    # Exceptions
    "DomainError",
    "InvalidProjectIdError",
    "ProjectNotFoundError",
    "ProjectValidationError",
]
