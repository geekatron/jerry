# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ListWorkItemsQueryHandler - Handler for ListWorkItemsQuery.

Retrieves a list of work items with optional filtering.

References:
    - PAT-CQRS-002: Query Pattern
    - Phase 4.4: Items Namespace Implementation
"""

from __future__ import annotations

from dataclasses import dataclass

from src.work_tracking.application.ports.work_item_repository import IWorkItemRepository
from src.work_tracking.application.queries.list_work_items_query import ListWorkItemsQuery
from src.work_tracking.domain.value_objects.work_item_status import WorkItemStatus


@dataclass
class WorkItemDTO:
    """Data Transfer Object for work item summary.

    Used in list views where full details are not needed.

    Attributes:
        id: Work item identifier
        title: Human-readable title
        status: Current status (pending, in_progress, etc.)
        priority: Priority level
        work_type: Type classification (task, bug, etc.)
        assignee: Current assignee (if any)
    """

    id: str
    title: str
    status: str
    priority: str
    work_type: str
    assignee: str | None = None


@dataclass
class WorkItemListDTO:
    """Data Transfer Object for work item list response.

    Attributes:
        items: List of work item summaries
        total_count: Total number of items matching filter
        has_more: Whether there are more items beyond the limit
    """

    items: list[WorkItemDTO]
    total_count: int
    has_more: bool = False


class ListWorkItemsQueryHandler:
    """Handler for ListWorkItemsQuery.

    Retrieves a list of work items from the repository with
    optional filtering by status and pagination.

    Attributes:
        _repository: Repository for work item retrieval
    """

    def __init__(self, repository: IWorkItemRepository) -> None:
        """Initialize the handler with dependencies.

        Args:
            repository: Repository for work item operations
        """
        self._repository = repository

    def handle(self, query: ListWorkItemsQuery) -> WorkItemListDTO:
        """Handle the ListWorkItemsQuery.

        Args:
            query: Query with optional status filter and limit

        Returns:
            WorkItemListDTO with matching work items
        """
        # Parse status filter if provided
        status_filter: WorkItemStatus | None = None
        if query.status:
            try:
                status_filter = WorkItemStatus(query.status)
            except ValueError:
                # Invalid status filter, return empty result
                return WorkItemListDTO(items=[], total_count=0, has_more=False)

        # Get total count for pagination info
        total_count = self._repository.count(status=status_filter)

        # Get items with optional limit
        work_items = self._repository.list_all(
            status=status_filter,
            limit=query.limit,
        )

        # Convert to DTOs
        items = [
            WorkItemDTO(
                id=item.id,
                title=item.title,
                status=item.status.value,
                priority=str(item.priority),
                work_type=item.work_type.value,
                assignee=item.assignee,
            )
            for item in work_items
        ]

        # Determine if there are more items
        has_more = query.limit is not None and total_count > query.limit

        return WorkItemListDTO(
            items=items,
            total_count=total_count,
            has_more=has_more,
        )
