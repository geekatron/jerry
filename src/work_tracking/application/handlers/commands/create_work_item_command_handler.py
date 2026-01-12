"""
CreateWorkItemCommandHandler - Handler for CreateWorkItemCommand.

Creates a new work item using the WorkItem aggregate factory method.
Generates a unique ID and persists via repository.

References:
    - PHASE-45-ITEMS-COMMANDS.md: Implementation tracker
    - PAT-CQRS-001: Command Pattern
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from src.shared_kernel.domain_event import DomainEvent
from src.work_tracking.application.commands.create_work_item_command import (
    CreateWorkItemCommand,
)
from src.work_tracking.domain.aggregates.work_item import WorkItem
from src.work_tracking.domain.value_objects import Priority, WorkItemId, WorkType

if TYPE_CHECKING:
    from src.work_tracking.application.ports.work_item_repository import (
        IWorkItemRepository,
    )
    from src.work_tracking.domain.services.id_generator import IWorkItemIdGenerator


class CreateWorkItemCommandHandler:
    """Handler for CreateWorkItemCommand.

    Creates a new work item with a unique ID, validates input,
    and persists via repository.

    Attributes:
        _repository: Repository for work item persistence
        _id_generator: Service for generating unique work item IDs
    """

    def __init__(
        self,
        repository: IWorkItemRepository,
        id_generator: IWorkItemIdGenerator,
    ) -> None:
        """Initialize the handler with dependencies.

        Args:
            repository: Repository for work item operations
            id_generator: Service for generating unique IDs
        """
        self._repository = repository
        self._id_generator = id_generator

    def handle(self, command: CreateWorkItemCommand) -> Sequence[DomainEvent]:
        """Handle the CreateWorkItemCommand.

        Args:
            command: Command data with work item details

        Returns:
            List of domain events raised during creation

        Raises:
            ValueError: If title is empty or work_type/priority is invalid
        """
        # Validate and parse value objects
        work_type = WorkType.from_string(command.work_type)
        priority = Priority.from_string(command.priority)

        # Parse parent_id if provided
        parent_id: WorkItemId | None = None
        if command.parent_id:
            # For parent_id, we need to look up the internal ID from repository
            parent = self._repository.get(command.parent_id)
            if parent:
                parent_id = WorkItemId.create(
                    internal_id=int(parent.id),
                    display_number=int(command.parent_id),
                )

        # Generate unique ID
        work_item_id = self._id_generator.create()

        # Create the work item
        work_item = WorkItem.create(
            id=work_item_id,
            title=command.title,
            work_type=work_type,
            priority=priority,
            description=command.description,
            parent_id=parent_id,
        )

        # Persist and get saved events
        # Repository saves and returns the events that were persisted
        events = self._repository.save(work_item)

        return events
