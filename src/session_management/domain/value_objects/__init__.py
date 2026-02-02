"""
Value Objects - Immutable objects defined by their attributes.

Value objects have no identity; they are equal if all their attributes are equal.
They should be immutable (use @dataclass(frozen=True)).
"""

from .project_id import ProjectId
from .project_status import ProjectStatus
from .session_id import SessionId
from .validation_result import ValidationResult

__all__ = [
    "ProjectId",
    "ProjectStatus",
    "SessionId",
    "ValidationResult",
]
