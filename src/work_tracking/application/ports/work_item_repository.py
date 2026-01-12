"""
IWorkItemRepository - Application port for work item persistence.

Extends the generic IRepository contract with work-item specific
query operations needed by the application layer.

References:
    - PAT-REPO-001: Generic Repository
    - Hexagonal Architecture Ports (Cockburn)

Exports:
    IWorkItemRepository: Work item repository protocol
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from src.work_tracking.domain.aggregates.work_item import WorkItem
    from src.work_tracking.domain.value_objects.work_item_status import WorkItemStatus


class IWorkItemRepository(Protocol):
    """
    Application port for work item persistence operations.

    This port extends the basic repository operations with
    query capabilities needed by the application layer handlers.

    Thread Safety:
        Implementations should be thread-safe for concurrent access.

    Example:
        >>> repository: IWorkItemRepository = InMemoryWorkItemRepository()
        >>> items = repository.list_all()
        >>> item = repository.get("12345")
    """

    def get(self, id: str) -> WorkItem | None:
        """
        Retrieve a work item by its identifier.

        Args:
            id: The unique identifier of the work item

        Returns:
            The work item if found, None otherwise
        """
        ...

    def get_or_raise(self, id: str) -> WorkItem:
        """
        Retrieve a work item or raise if not found.

        Args:
            id: The unique identifier of the work item

        Returns:
            The work item

        Raises:
            AggregateNotFoundError: If the work item doesn't exist
        """
        ...

    def save(self, work_item: WorkItem) -> None:
        """
        Persist a work item.

        Args:
            work_item: The work item to persist

        Raises:
            ConcurrencyError: If version mismatch detected
        """
        ...

    def delete(self, id: str) -> bool:
        """
        Remove a work item from the repository.

        Args:
            id: The unique identifier of the work item to delete

        Returns:
            True if deleted, False if not found
        """
        ...

    def exists(self, id: str) -> bool:
        """
        Check if a work item exists.

        Args:
            id: The unique identifier to check

        Returns:
            True if the work item exists
        """
        ...

    def list_all(
        self,
        status: WorkItemStatus | None = None,
        limit: int | None = None,
    ) -> list[WorkItem]:
        """
        List all work items with optional filtering.

        Args:
            status: Optional status filter
            limit: Optional maximum number of items to return

        Returns:
            List of work items matching the criteria
        """
        ...

    def count(self, status: WorkItemStatus | None = None) -> int:
        """
        Count work items with optional status filter.

        Args:
            status: Optional status filter

        Returns:
            Number of work items matching the criteria
        """
        ...
