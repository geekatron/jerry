"""
CreateSessionCommand - Command to create a new session.

Data class containing the information needed to start a new session.
Logic is in CreateSessionCommandHandler.

References:
    - ENFORCE-008d.3.2: Session aggregate
    - PAT-CQRS-001: Command Pattern
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateSessionCommand:
    """Command to create a new session.

    This command starts a new work session, optionally with a name
    and description. If there's already an active session, the handler
    will raise an error.

    Attributes:
        name: Optional session name (for display)
        description: Optional session description
        project_id: Optional project ID to link to

    Example:
        >>> command = CreateSessionCommand(
        ...     name="Feature Implementation",
        ...     description="Working on new login feature",
        ... )
    """

    name: str | None = None
    description: str | None = None
    project_id: str | None = None
