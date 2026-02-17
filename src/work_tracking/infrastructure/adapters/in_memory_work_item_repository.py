# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
InMemoryWorkItemRepository - In-memory implementation of IWorkItemRepository.

Thread-safe in-memory repository for work items, suitable for
testing and development.

References:
    - PAT-REPO-001: Generic Repository
    - Phase 4.4: Items Namespace Implementation
"""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING

from src.shared_kernel.domain_event import DomainEvent
from src.work_tracking.domain.ports.repository import AggregateNotFoundError

if TYPE_CHECKING:
    from src.work_tracking.domain.aggregates.work_item import WorkItem
    from src.work_tracking.domain.value_objects.work_item_status import WorkItemStatus


class InMemoryWorkItemRepository:
    """
    Thread-safe in-memory work item repository.

    Stores work items in a dictionary keyed by ID. Provides
    filtering and listing capabilities for queries.

    Thread Safety:
        All public methods are protected by a threading.RLock.

    Example:
        >>> repo = InMemoryWorkItemRepository()
        >>> repo.save(work_item)
        >>> item = repo.get("12345")
    """

    def __init__(self) -> None:
        """Initialize empty repository."""
        self._items: dict[str, WorkItem] = {}
        self._lock = threading.RLock()

    def get(self, id: str) -> WorkItem | None:
        """
        Retrieve a work item by ID.

        Args:
            id: The work item identifier

        Returns:
            The work item if found, None otherwise
        """
        with self._lock:
            return self._items.get(id)

    def get_or_raise(self, id: str) -> WorkItem:
        """
        Retrieve a work item or raise if not found.

        Args:
            id: The work item identifier

        Returns:
            The work item

        Raises:
            AggregateNotFoundError: If the work item doesn't exist
        """
        with self._lock:
            item = self._items.get(id)
            if item is None:
                raise AggregateNotFoundError(id, "WorkItem")
            return item

    def save(self, work_item: WorkItem) -> list[DomainEvent]:
        """
        Persist a work item and return saved events.

        Args:
            work_item: The work item to persist

        Returns:
            List of domain events that were saved
        """
        with self._lock:
            # Collect events before storing
            events = list(work_item.collect_events())
            self._items[work_item.id] = work_item
            return events

    def delete(self, id: str) -> bool:
        """
        Remove a work item from the repository.

        Args:
            id: The work item identifier

        Returns:
            True if deleted, False if not found
        """
        with self._lock:
            if id in self._items:
                del self._items[id]
                return True
            return False

    def exists(self, id: str) -> bool:
        """
        Check if a work item exists.

        Args:
            id: The work item identifier

        Returns:
            True if the work item exists
        """
        with self._lock:
            return id in self._items

    def list_all(
        self,
        status: WorkItemStatus | None = None,
        limit: int | None = None,
    ) -> list[WorkItem]:
        """
        List all work items with optional filtering.

        Args:
            status: Optional status filter
            limit: Maximum number of items to return

        Returns:
            List of work items matching criteria
        """
        with self._lock:
            items = list(self._items.values())

            # Apply status filter
            if status is not None:
                items = [item for item in items if item.status == status]

            # Apply limit
            if limit is not None:
                items = items[:limit]

            return items

    def count(self, status: WorkItemStatus | None = None) -> int:
        """
        Count work items with optional status filter.

        Args:
            status: Optional status filter

        Returns:
            Number of work items matching criteria
        """
        with self._lock:
            if status is None:
                return len(self._items)

            return sum(1 for item in self._items.values() if item.status == status)

    def clear(self) -> None:
        """Clear all work items (for testing)."""
        with self._lock:
            self._items.clear()
