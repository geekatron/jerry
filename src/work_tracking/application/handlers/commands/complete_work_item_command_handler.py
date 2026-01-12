"""
CompleteWorkItemCommandHandler - Handler for CompleteWorkItemCommand.

Transitions a work item to DONE status.
Validates quality gates and persists.

References:
    - PHASE-45-ITEMS-COMMANDS.md: Implementation tracker
    - PAT-CQRS-001: Command Pattern
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from src.shared_kernel.domain_event import DomainEvent
from src.work_tracking.application.commands.complete_work_item_command import (
    CompleteWorkItemCommand,
)

if TYPE_CHECKING:
    from src.work_tracking.application.ports.work_item_repository import (
        IWorkItemRepository,
    )


class CompleteWorkItemCommandHandler:
    """Handler for CompleteWorkItemCommand.

    Retrieves a work item, validates quality gates, and transitions
    it to DONE status.

    Attributes:
        _repository: Repository for work item persistence
    """

    def __init__(self, repository: IWorkItemRepository) -> None:
        """Initialize the handler with dependencies.

        Args:
            repository: Repository for work item operations
        """
        self._repository = repository

    def handle(self, command: CompleteWorkItemCommand) -> Sequence[DomainEvent]:
        """Handle the CompleteWorkItemCommand.

        Args:
            command: Command data with work item ID and optional reason

        Returns:
            List of domain events raised during the operation

        Raises:
            AggregateNotFoundError: If work item doesn't exist
            InvalidStateTransitionError: If transition not allowed
            QualityGateNotMetError: If quality requirements not satisfied
        """
        # Retrieve work item
        work_item = self._repository.get_or_raise(command.work_item_id)

        # Execute domain command (validates quality gates internally)
        work_item.complete(reason=command.reason)

        # Persist and get saved events
        events = self._repository.save(work_item)

        return events
