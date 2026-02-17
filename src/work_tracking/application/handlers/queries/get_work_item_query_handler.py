# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
GetWorkItemQueryHandler - Handler for GetWorkItemQuery.

Retrieves a single work item by ID with full details.

References:
    - PAT-CQRS-002: Query Pattern
    - Phase 4.4: Items Namespace Implementation
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.work_tracking.application.ports.work_item_repository import IWorkItemRepository
from src.work_tracking.application.queries.get_work_item_query import GetWorkItemQuery


class WorkItemNotFoundError(Exception):
    """Raised when a work item cannot be found.

    Attributes:
        work_item_id: The ID that was not found
    """

    def __init__(self, work_item_id: str) -> None:
        self.work_item_id = work_item_id
        super().__init__(f"Work item '{work_item_id}' not found")


@dataclass
class WorkItemDetailDTO:
    """Data Transfer Object for full work item details.

    Used when displaying a single work item with all information.

    Attributes:
        id: Work item identifier
        title: Human-readable title
        description: Detailed description
        status: Current status (pending, in_progress, etc.)
        priority: Priority level
        work_type: Type classification (task, bug, etc.)
        assignee: Current assignee (if any)
        parent_id: Parent work item ID (if any)
        dependencies: List of dependency work item IDs
        test_coverage: Test coverage percentage (if recorded)
        created_at: Creation timestamp
        completed_at: Completion timestamp (if completed)
    """

    id: str
    title: str
    description: str
    status: str
    priority: str
    work_type: str
    assignee: str | None = None
    parent_id: str | None = None
    dependencies: list[str] | None = None
    test_coverage: float | None = None
    created_at: datetime | None = None
    completed_at: datetime | None = None


class GetWorkItemQueryHandler:
    """Handler for GetWorkItemQuery.

    Retrieves a single work item from the repository by ID.

    Attributes:
        _repository: Repository for work item retrieval
    """

    def __init__(self, repository: IWorkItemRepository) -> None:
        """Initialize the handler with dependencies.

        Args:
            repository: Repository for work item operations
        """
        self._repository = repository

    def handle(self, query: GetWorkItemQuery) -> WorkItemDetailDTO:
        """Handle the GetWorkItemQuery.

        Args:
            query: Query with work item ID

        Returns:
            WorkItemDetailDTO with full work item details

        Raises:
            WorkItemNotFoundError: If work item doesn't exist
        """
        work_item = self._repository.get(query.work_item_id)

        if work_item is None:
            raise WorkItemNotFoundError(query.work_item_id)

        return WorkItemDetailDTO(
            id=work_item.id,
            title=work_item.title,
            description=work_item.description,
            status=work_item.status.value,
            priority=str(work_item.priority),
            work_type=work_item.work_type.value,
            assignee=work_item.assignee,
            parent_id=work_item.parent_id,
            dependencies=list(work_item.dependencies) if work_item.dependencies else None,
            test_coverage=work_item.test_coverage.percent if work_item.test_coverage else None,
            created_at=work_item.created_on,
            completed_at=work_item.completed_at,
        )
