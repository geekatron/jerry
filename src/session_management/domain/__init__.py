"""
Domain Layer - Session Management Bounded Context

Pure business logic with NO external dependencies.
All imports must be from Python stdlib or within this package.

Components:
    - value_objects/: Immutable values (ProjectId, ProjectStatus, ValidationResult)
    - entities/: Objects with identity (ProjectInfo)
    - events/: Domain events (future)
    - exceptions.py: Domain-specific errors

Rules:
    1. NO imports from application/, infrastructure/, or interface/
    2. NO imports from external packages (except stdlib)
    3. Entities enforce their own invariants
    4. Value objects are immutable
"""

# Value Objects
from .value_objects.project_id import ProjectId
from .value_objects.project_status import ProjectStatus
from .value_objects.validation_result import ValidationResult

# Entities
from .entities.project_info import ProjectInfo

# Exceptions
from .exceptions import (
    DomainError,
    InvalidProjectIdError,
    ProjectNotFoundError,
    ProjectValidationError,
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
