"""
EndSessionCommandHandler - Handler for EndSessionCommand.

Completes the current active session.
Uses the Session aggregate complete() method and persists via repository.

References:
    - ENFORCE-008d.3.2: Session aggregate
    - PAT-CQRS-001: Command Pattern
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.shared_kernel.domain_event import DomainEvent

from src.session_management.application.commands.end_session_command import (
    EndSessionCommand,
)
from src.session_management.application.ports.session_repository import ISessionRepository

if TYPE_CHECKING:
    from collections.abc import Sequence


@dataclass
class NoActiveSessionError(Exception):
    """Raised when trying to end a session when none is active."""

    def __str__(self) -> str:
        return "Cannot end session: no active session found"


class EndSessionCommandHandler:
    """Handler for EndSessionCommand.

    Completes the current active session with an optional summary.

    Attributes:
        _repository: Repository for session persistence
    """

    def __init__(self, repository: ISessionRepository) -> None:
        """Initialize the handler with dependencies.

        Args:
            repository: Repository for session operations
        """
        self._repository = repository

    def handle(self, command: EndSessionCommand) -> Sequence[DomainEvent]:
        """Handle the EndSessionCommand.

        Args:
            command: Command data with optional summary

        Returns:
            List of domain events raised during session completion

        Raises:
            NoActiveSessionError: If no session is currently active
        """
        # Get active session
        session = self._repository.get_active()
        if session is None:
            raise NoActiveSessionError()

        # Complete the session
        session.complete(summary=command.summary or "")

        # Persist
        self._repository.save(session)

        # Return raised events
        return session.collect_events()
