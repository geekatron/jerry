"""
ProjectStatus - Enum representing project lifecycle states.

This is a simple enumeration with no external dependencies.
"""

from __future__ import annotations
from enum import Enum, auto


class ProjectStatus(Enum):
    """Lifecycle status of a Jerry project.

    States:
        UNKNOWN: Status could not be determined (e.g., missing WORKTRACKER.md)
        DRAFT: Project created but not yet started
        IN_PROGRESS: Active development
        COMPLETED: All work finished
        ARCHIVED: Moved to archive (no longer active)
    """

    UNKNOWN = auto()
    DRAFT = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    ARCHIVED = auto()

    @classmethod
    def from_string(cls, value: str) -> ProjectStatus:
        """Parse a status string into a ProjectStatus enum.

        Args:
            value: String representation of status (case-insensitive)

        Returns:
            Matching ProjectStatus enum value, or UNKNOWN if not recognized
        """
        normalized = value.upper().replace(" ", "_").replace("-", "_")
        try:
            return cls[normalized]
        except KeyError:
            return cls.UNKNOWN

    def __str__(self) -> str:
        """Return human-readable status string."""
        return self.name.replace("_", " ").title()
