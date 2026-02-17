# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
GetSessionStatusQueryHandler - Handler for GetSessionStatusQuery.

Retrieves the status of the current active session.

References:
    - ENFORCE-008d.3.2: Session aggregate
    - PAT-CQRS-002: Query Pattern
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.session_management.application.ports.session_repository import ISessionRepository
from src.session_management.application.queries.get_session_status_query import (
    GetSessionStatusQuery,
)


@dataclass
class SessionStatusDTO:
    """Data Transfer Object for session status.

    Attributes:
        has_active_session: Whether there is an active session
        session_id: Active session ID (if any)
        status: Session status string (active/completed/abandoned)
        description: Session description (if any)
        project_id: Linked project ID (if any)
        started_at: Session start time (if any)
    """

    has_active_session: bool
    session_id: str | None = None
    status: str | None = None
    description: str | None = None
    project_id: str | None = None
    started_at: datetime | None = None


class GetSessionStatusQueryHandler:
    """Handler for GetSessionStatusQuery.

    Retrieves the status of the current active session.

    Attributes:
        _repository: Repository for session retrieval
    """

    def __init__(self, repository: ISessionRepository) -> None:
        """Initialize the handler with dependencies.

        Args:
            repository: Repository for session operations
        """
        self._repository = repository

    def handle(self, query: GetSessionStatusQuery) -> SessionStatusDTO:
        """Handle the GetSessionStatusQuery.

        Args:
            query: Query object (parameterless)

        Returns:
            SessionStatusDTO with current session information
        """
        session = self._repository.get_active()

        if session is None:
            return SessionStatusDTO(has_active_session=False)

        return SessionStatusDTO(
            has_active_session=True,
            session_id=session.id,
            status=session.status.value,
            description=session.description,
            project_id=session.project_id,
            started_at=session.created_on,
        )
