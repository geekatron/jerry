"""
ProjectInfo - Entity representing a Jerry project.

This entity has identity (the ProjectId) and can have different states
over its lifecycle. It aggregates information about a project's
configuration and status.
"""

from __future__ import annotations
from dataclasses import dataclass

from ..value_objects.project_id import ProjectId
from ..value_objects.project_status import ProjectStatus


@dataclass(frozen=True, slots=True)
class ProjectInfo:
    """Entity representing a Jerry project.

    This is an immutable snapshot of project information at a point in time.
    For mutability, create a new instance with updated values.

    Attributes:
        id: The unique project identifier
        status: Current lifecycle status
        has_plan: Whether PLAN.md exists
        has_tracker: Whether WORKTRACKER.md exists
        path: Optional filesystem path to the project
    """

    id: ProjectId
    status: ProjectStatus = ProjectStatus.UNKNOWN
    has_plan: bool = False
    has_tracker: bool = False
    path: str | None = None

    @classmethod
    def create(
        cls,
        project_id: ProjectId | str,
        status: ProjectStatus | str = ProjectStatus.UNKNOWN,
        has_plan: bool = False,
        has_tracker: bool = False,
        path: str | None = None,
    ) -> ProjectInfo:
        """Create a ProjectInfo with flexible input types.

        Args:
            project_id: ProjectId instance or string to parse
            status: ProjectStatus enum or string to parse
            has_plan: Whether PLAN.md exists
            has_tracker: Whether WORKTRACKER.md exists
            path: Filesystem path to the project

        Returns:
            A new ProjectInfo instance

        Raises:
            InvalidProjectIdError: If project_id string is invalid
        """
        # Parse project_id if string
        if isinstance(project_id, str):
            project_id = ProjectId.parse(project_id)

        # Parse status if string
        if isinstance(status, str):
            status = ProjectStatus.from_string(status)

        return cls(
            id=project_id,
            status=status,
            has_plan=has_plan,
            has_tracker=has_tracker,
            path=path,
        )

    @property
    def is_complete(self) -> bool:
        """Check if project has all required files."""
        return self.has_plan and self.has_tracker

    @property
    def is_active(self) -> bool:
        """Check if project is in an active state (not archived)."""
        return self.status not in (ProjectStatus.ARCHIVED, ProjectStatus.COMPLETED)

    @property
    def warnings(self) -> list[str]:
        """Get list of warning messages for incomplete configuration."""
        warnings = []
        if not self.has_plan:
            warnings.append("Missing PLAN.md")
        if not self.has_tracker:
            warnings.append("Missing WORKTRACKER.md")
        return warnings

    def __str__(self) -> str:
        """Return human-readable representation."""
        status_str = str(self.status)
        if self.is_complete:
            return f"{self.id} [{status_str}]"
        return f"{self.id} [{status_str}] (incomplete)"

    def __repr__(self) -> str:
        """Return detailed representation."""
        return (
            f"ProjectInfo(id={self.id!r}, status={self.status}, "
            f"has_plan={self.has_plan}, has_tracker={self.has_tracker})"
        )
