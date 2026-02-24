# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
AbandonSessionCommandHandler - Handler for AbandonSessionCommand.

Abandons the current active session.
Uses the Session aggregate abandon() method and persists via repository.

References:
    - ENFORCE-008d.3.2: Session aggregate
    - PAT-CQRS-001: Command Pattern
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.session_management.application.commands.abandon_session_command import (
    AbandonSessionCommand,
)
from src.session_management.application.ports.session_repository import ISessionRepository
from src.shared_kernel.domain_event import DomainEvent

if TYPE_CHECKING:
    from collections.abc import Sequence


class NoActiveSessionError(Exception):
    """Raised when trying to abandon a session when none is active."""

    def __str__(self) -> str:
        return "Cannot abandon session: no active session found"


class AbandonSessionCommandHandler:
    """Handler for AbandonSessionCommand.

    Abandons the current active session with an optional reason.

    Attributes:
        _repository: Repository for session persistence
    """

    def __init__(self, repository: ISessionRepository) -> None:
        """Initialize the handler with dependencies.

        Args:
            repository: Repository for session operations
        """
        self._repository = repository

    def handle(self, command: AbandonSessionCommand) -> Sequence[DomainEvent]:
        """Handle the AbandonSessionCommand.

        Args:
            command: Command data with optional reason

        Returns:
            List of domain events raised during session abandonment

        Raises:
            NoActiveSessionError: If no session is currently active
        """
        # Get active session
        session = self._repository.get_active()
        if session is None:
            raise NoActiveSessionError()

        # Abandon the session
        session.abandon(reason=command.reason or "")

        # Persist and return raised events
        return self._repository.save(session)
