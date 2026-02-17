# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
CreateSessionCommandHandler - Handler for CreateSessionCommand.

Creates a new session if no active session exists.
Uses the Session aggregate factory method and persists via repository.

References:
    - ENFORCE-008d.3.2: Session aggregate
    - PAT-CQRS-001: Command Pattern
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.session_management.application.commands.create_session_command import (
    CreateSessionCommand,
)
from src.session_management.application.ports.session_repository import ISessionRepository
from src.session_management.domain.aggregates.session import Session
from src.session_management.domain.value_objects.project_id import ProjectId
from src.session_management.domain.value_objects.session_id import SessionId
from src.shared_kernel.domain_event import DomainEvent

if TYPE_CHECKING:
    from collections.abc import Sequence


@dataclass
class SessionAlreadyActiveError(Exception):
    """Raised when trying to create a session while one is already active."""

    active_session_id: str

    def __str__(self) -> str:
        return f"Cannot start new session: session '{self.active_session_id}' is already active"


class CreateSessionCommandHandler:
    """Handler for CreateSessionCommand.

    Creates a new work session. Validates that no session is currently
    active before creating a new one.

    Attributes:
        _repository: Repository for session persistence
    """

    def __init__(self, repository: ISessionRepository) -> None:
        """Initialize the handler with dependencies.

        Args:
            repository: Repository for session operations
        """
        self._repository = repository

    def handle(self, command: CreateSessionCommand) -> Sequence[DomainEvent]:
        """Handle the CreateSessionCommand.

        Args:
            command: Command data with session details

        Returns:
            List of domain events raised during session creation

        Raises:
            SessionAlreadyActiveError: If a session is already active
        """
        # Check for existing active session
        active = self._repository.get_active()
        if active is not None:
            raise SessionAlreadyActiveError(active_session_id=active.id)

        # Create description from name and description
        description = ""
        if command.name:
            description = command.name
        if command.description:
            if description:
                description = f"{description}: {command.description}"
            else:
                description = command.description

        # Parse project ID if provided
        project_id = None
        if command.project_id:
            project_id = ProjectId.parse(command.project_id)

        # Create the session
        session = Session.create(
            session_id=SessionId.generate(),
            description=description,
            project_id=project_id,
        )

        # Persist
        self._repository.save(session)

        # Return raised events
        return session.collect_events()
