# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BlockWorkItemCommandHandler - Handler for BlockWorkItemCommand.

Transitions a work item to BLOCKED status.
Requires a reason to document the blocker.

References:
    - PHASE-45-ITEMS-COMMANDS.md: Implementation tracker
    - PAT-CQRS-001: Command Pattern
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from src.shared_kernel.domain_event import DomainEvent
from src.work_tracking.application.commands.block_work_item_command import (
    BlockWorkItemCommand,
)

if TYPE_CHECKING:
    from src.work_tracking.application.ports.work_item_repository import (
        IWorkItemRepository,
    )


class BlockWorkItemCommandHandler:
    """Handler for BlockWorkItemCommand.

    Retrieves a work item and transitions it to BLOCKED status.

    Attributes:
        _repository: Repository for work item persistence
    """

    def __init__(self, repository: IWorkItemRepository) -> None:
        """Initialize the handler with dependencies.

        Args:
            repository: Repository for work item operations
        """
        self._repository = repository

    def handle(self, command: BlockWorkItemCommand) -> Sequence[DomainEvent]:
        """Handle the BlockWorkItemCommand.

        Args:
            command: Command data with work item ID and blocking reason

        Returns:
            List of domain events raised during the operation

        Raises:
            AggregateNotFoundError: If work item doesn't exist
            InvalidStateTransitionError: If transition not allowed
        """
        # Retrieve work item
        work_item = self._repository.get_or_raise(command.work_item_id)

        # Execute domain command
        work_item.block(reason=command.reason)

        # Persist and get saved events
        events = self._repository.save(work_item)

        return events
