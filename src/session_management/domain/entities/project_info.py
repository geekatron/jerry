"""
ProjectInfo - Entity representing a Jerry project.

This entity has identity (the ProjectId) and can have different states
over its lifecycle. It aggregates information about a project's
configuration and status.

Implements IAuditable and IVersioned protocols directly (not via EntityBase)
because ProjectInfo is an immutable snapshot (frozen=True). See DISC-002.

References:
    - ENFORCE-008d: Domain Refactoring
    - DISC-002: ProjectInfo EntityBase Design Tension
    - Canon PAT-007: EntityBase Class (approach adapted for immutability)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from ..value_objects.project_id import ProjectId
from ..value_objects.project_status import ProjectStatus
from ..value_objects.session_id import SessionId


def _utc_now() -> datetime:
    """Return current UTC time."""
    return datetime.now(UTC)


@dataclass(frozen=True, slots=True)
class ProjectInfo:
    """Entity representing a Jerry project.

    This is an immutable snapshot of project information at a point in time.
    For mutability, create a new instance with updated values.

    Implements IAuditable and IVersioned protocols for compatibility with
    shared_kernel patterns while maintaining immutability.

    Attributes:
        id: The unique project identifier
        status: Current lifecycle status
        has_plan: Whether PLAN.md exists
        has_tracker: Whether WORKTRACKER.md exists
        path: Optional filesystem path to the project
        session_id: Optional session ID linking to the active session
        version: Optimistic concurrency version (IVersioned)
        created_by: Who created this entity (IAuditable)
        created_at: When this entity was created (IAuditable)
        updated_by: Who last updated this entity (IAuditable)
        updated_at: When this entity was last updated (IAuditable)
    """

    id: ProjectId
    status: ProjectStatus = ProjectStatus.UNKNOWN
    has_plan: bool = False
    has_tracker: bool = False
    path: str | None = None
    # Session linking
    session_id: str | None = None
    # IVersioned compliance
    version: int = 0
    # IAuditable compliance
    created_by: str = "System"
    created_at: datetime = field(default_factory=_utc_now)
    updated_by: str = "System"
    updated_at: datetime = field(default_factory=_utc_now)

    @classmethod
    def create(
        cls,
        project_id: ProjectId | str,
        status: ProjectStatus | str = ProjectStatus.UNKNOWN,
        has_plan: bool = False,
        has_tracker: bool = False,
        path: str | None = None,
        session_id: SessionId | str | None = None,
        version: int = 0,
        created_by: str = "System",
        created_at: datetime | None = None,
        updated_by: str | None = None,
        updated_at: datetime | None = None,
    ) -> ProjectInfo:
        """Create a ProjectInfo with flexible input types.

        Args:
            project_id: ProjectId instance or string to parse
            status: ProjectStatus enum or string to parse
            has_plan: Whether PLAN.md exists
            has_tracker: Whether WORKTRACKER.md exists
            path: Filesystem path to the project
            session_id: SessionId instance or string linking to active session
            version: Optimistic concurrency version (default 0)
            created_by: Who created this entity (default "System")
            created_at: When created (default now)
            updated_by: Who last updated (default same as created_by)
            updated_at: When last updated (default same as created_at)

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

        # Extract session_id value if SessionId instance
        session_id_value: str | None = None
        if session_id is not None:
            if isinstance(session_id, SessionId):
                session_id_value = session_id.value
            else:
                session_id_value = session_id

        # Default audit timestamps
        now = _utc_now()
        if created_at is None:
            created_at = now
        if updated_by is None:
            updated_by = created_by
        if updated_at is None:
            updated_at = created_at

        return cls(
            id=project_id,
            status=status,
            has_plan=has_plan,
            has_tracker=has_tracker,
            path=path,
            session_id=session_id_value,
            version=version,
            created_by=created_by,
            created_at=created_at,
            updated_by=updated_by,
            updated_at=updated_at,
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

    def get_expected_version(self) -> int:
        """Return version for concurrency check on save (IVersioned compliance)."""
        return self.version

    def __str__(self) -> str:
        """Return human-readable representation."""
        status_str = str(self.status)
        if self.is_complete:
            return f"{self.id} [{status_str}]"
        return f"{self.id} [{status_str}] (incomplete)"

    def __repr__(self) -> str:
        """Return detailed representation."""
        parts = [
            f"ProjectInfo(id={self.id!r}",
            f"status={self.status}",
            f"has_plan={self.has_plan}",
            f"has_tracker={self.has_tracker}",
        ]
        if self.session_id is not None:
            parts.append(f"session_id={self.session_id!r}")
        return ", ".join(parts) + ")"
