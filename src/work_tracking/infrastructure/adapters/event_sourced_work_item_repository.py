"""
EventSourcedWorkItemRepository - Event-sourced implementation of IWorkItemRepository.

Persists WorkItem aggregates via event streams, enabling full history tracking
and event replay. Uses IEventStore for persistence (injected dependency).

Architecture:
    - Implements IWorkItemRepository port
    - Uses IEventStore secondary port for persistence
    - Converts between DomainEvent and StoredEvent
    - Reconstitutes WorkItems via load_from_history()

References:
    - PAT-REPO-002: Event-Sourced Repository Pattern
    - TD-018: Event Sourcing for WorkItem Repository
    - DISC-019: InMemoryEventStore Not Persistent

Exports:
    EventSourcedWorkItemRepository: Event-sourced work item repository
"""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Protocol
from uuid import UUID

from src.shared_kernel.domain_event import DomainEvent, EventRegistry
from src.work_tracking.domain.aggregates.work_item import WorkItem
from src.work_tracking.domain.events.work_item_events import (
    AssigneeChanged,
    DependencyAdded,
    DependencyRemoved,
    PriorityChanged,
    QualityMetricsUpdated,
    StatusChanged,
    WorkItemCompleted,
    WorkItemCreated,
)
from src.work_tracking.domain.ports.event_store import (
    IEventStore,
    StoredEvent,
    StreamNotFoundError,
)
from src.work_tracking.domain.ports.repository import AggregateNotFoundError

if TYPE_CHECKING:
    from src.work_tracking.domain.value_objects.work_item_status import WorkItemStatus


# Extended event store protocol with utility methods
class IEventStoreWithUtilities(IEventStore, Protocol):
    """Extended event store with utility methods for listing streams."""

    def get_all_stream_ids(self) -> list[str]:
        """Get all stream IDs in the store."""
        ...


# =============================================================================
# Event Registry for WorkItem Events
# =============================================================================

# Create a registry for all WorkItem domain events
_work_item_event_registry = EventRegistry()
_work_item_event_registry.register(WorkItemCreated)
_work_item_event_registry.register(StatusChanged)
_work_item_event_registry.register(WorkItemCompleted)
_work_item_event_registry.register(PriorityChanged)
_work_item_event_registry.register(QualityMetricsUpdated)
_work_item_event_registry.register(DependencyAdded)
_work_item_event_registry.register(DependencyRemoved)
_work_item_event_registry.register(AssigneeChanged)


def get_work_item_event_registry() -> EventRegistry:
    """Get the event registry for WorkItem events."""
    return _work_item_event_registry


# =============================================================================
# Stream ID Convention
# =============================================================================


def _make_stream_id(work_item_id: str) -> str:
    """Create stream ID from work item ID."""
    return f"work_item-{work_item_id}"


def _extract_work_item_id(stream_id: str) -> str:
    """Extract work item ID from stream ID."""
    if stream_id.startswith("work_item-"):
        return stream_id[len("work_item-") :]
    return stream_id


# =============================================================================
# Event Conversion Utilities
# =============================================================================


def _domain_event_to_stored_event(
    event: DomainEvent,
    stream_id: str,
) -> StoredEvent:
    """
    Convert a DomainEvent to a StoredEvent for persistence.

    Args:
        event: The domain event to convert
        stream_id: The stream ID for storage

    Returns:
        StoredEvent ready for persistence
    """
    # Get event data including event_type
    event_data = event.to_dict()

    # Extract event_id - it's a string, convert to UUID if possible
    event_id_str = event.event_id
    try:
        event_uuid = UUID(event_id_str.replace("EVT-", ""))
    except (ValueError, AttributeError):
        # If can't convert, let StoredEvent generate a new one
        from uuid import uuid4

        event_uuid = uuid4()

    return StoredEvent(
        stream_id=stream_id,
        version=event.version,
        event_type=type(event).__name__,
        data=event_data,
        timestamp=event.timestamp,
        event_id=event_uuid,
    )


def _stored_event_to_domain_event(
    stored_event: StoredEvent,
    registry: EventRegistry,
) -> DomainEvent:
    """
    Convert a StoredEvent back to a DomainEvent.

    Args:
        stored_event: The stored event from persistence
        registry: Event registry for type lookup

    Returns:
        Reconstituted DomainEvent

    Raises:
        ValueError: If event type is not registered
    """
    return registry.deserialize(stored_event.data)


# =============================================================================
# EventSourcedWorkItemRepository
# =============================================================================


class EventSourcedWorkItemRepository:
    """
    Event-sourced implementation of IWorkItemRepository.

    Persists WorkItem aggregates as event streams using the injected IEventStore.
    WorkItems are reconstituted by replaying their event history.

    Thread Safety:
        All public methods are protected by a threading.RLock for in-process
        thread safety. File-level locking is handled by the underlying
        FileSystemEventStore.

    Performance Note:
        The list_all() and count() methods load ALL work items from all streams.
        For high-volume scenarios, consider using a read model/projection.

    Example:
        >>> event_store = FileSystemEventStore(project_path)
        >>> repository = EventSourcedWorkItemRepository(event_store)
        >>> work_item = WorkItem.create(id=id, title="Test")
        >>> repository.save(work_item)
        >>> loaded = repository.get(str(id.internal_id))
    """

    def __init__(self, event_store: IEventStoreWithUtilities) -> None:
        """
        Initialize event-sourced repository.

        Args:
            event_store: The event store for persistence (must support get_all_stream_ids)
        """
        self._event_store = event_store
        self._registry = get_work_item_event_registry()
        self._lock = threading.RLock()

    def get(self, id: str) -> WorkItem | None:
        """
        Retrieve a work item by ID.

        Reads all events for the work item and reconstitutes it
        via load_from_history().

        Args:
            id: The work item identifier

        Returns:
            The work item if found, None otherwise
        """
        with self._lock:
            stream_id = _make_stream_id(id)

            if not self._event_store.stream_exists(stream_id):
                return None

            try:
                stored_events = self._event_store.read(stream_id)
            except StreamNotFoundError:
                return None

            if not stored_events:
                return None

            # Convert StoredEvents to DomainEvents
            domain_events = [
                _stored_event_to_domain_event(se, self._registry) for se in stored_events
            ]

            # Reconstitute WorkItem from event history
            return WorkItem.load_from_history(domain_events)

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
        work_item = self.get(id)
        if work_item is None:
            raise AggregateNotFoundError(id, "WorkItem")
        return work_item

    def save(self, work_item: WorkItem) -> list[DomainEvent]:
        """
        Persist a work item by saving its pending events.

        Collects uncommitted events from the work item and appends
        them to the event store with optimistic concurrency checking.

        Args:
            work_item: The work item to persist

        Returns:
            List of domain events that were saved.

        Raises:
            ConcurrencyError: If version mismatch detected
        """
        with self._lock:
            stream_id = _make_stream_id(work_item.id)

            # Collect pending events from the aggregate
            pending_events = list(work_item.collect_events())

            if not pending_events:
                return []  # Nothing to save

            # Convert to stored events
            stored_events = [
                _domain_event_to_stored_event(event, stream_id) for event in pending_events
            ]

            # Calculate expected version
            # If first event is version 1, expected_version should be 0 (new stream)
            # Otherwise, expected_version is the version before the first pending event
            first_event_version = stored_events[0].version
            expected_version = first_event_version - 1

            # For new streams, use -1 (or 0, both accepted)
            if expected_version <= 0:
                expected_version = -1

            # Append to event store
            self._event_store.append(stream_id, stored_events, expected_version)

            # Return the events that were saved
            return pending_events

    def delete(self, id: str) -> bool:
        """
        Remove a work item from the repository.

        Deletes the entire event stream for the work item.

        Args:
            id: The work item identifier

        Returns:
            True if deleted, False if not found
        """
        with self._lock:
            stream_id = _make_stream_id(id)
            return self._event_store.delete_stream(stream_id)

    def exists(self, id: str) -> bool:
        """
        Check if a work item exists.

        Args:
            id: The work item identifier

        Returns:
            True if the work item exists
        """
        with self._lock:
            stream_id = _make_stream_id(id)
            return self._event_store.stream_exists(stream_id)

    def list_all(
        self,
        status: WorkItemStatus | None = None,
        limit: int | None = None,
    ) -> list[WorkItem]:
        """
        List all work items with optional filtering.

        Note: This method loads ALL work items from all streams.
        For large datasets, consider using a read model.

        Args:
            status: Optional status filter
            limit: Maximum number of items to return

        Returns:
            List of work items matching criteria
        """
        with self._lock:
            # Get all stream IDs
            stream_ids = self._event_store.get_all_stream_ids()

            # Filter to only work_item streams
            work_item_stream_ids = [sid for sid in stream_ids if sid.startswith("work_item-")]

            items: list[WorkItem] = []

            for stream_id in work_item_stream_ids:
                work_item_id = _extract_work_item_id(stream_id)
                work_item = self.get(work_item_id)

                if work_item is None:
                    continue

                # Apply status filter
                if status is not None and work_item.status != status:
                    continue

                items.append(work_item)

                # Apply limit
                if limit is not None and len(items) >= limit:
                    break

            return items

    def count(self, status: WorkItemStatus | None = None) -> int:
        """
        Count work items with optional status filter.

        Note: This method loads ALL work items to filter by status.
        For large datasets, consider using a read model.

        Args:
            status: Optional status filter

        Returns:
            Number of work items matching criteria
        """
        with self._lock:
            if status is None:
                # Fast path: just count work_item streams
                stream_ids = self._event_store.get_all_stream_ids()
                return sum(1 for sid in stream_ids if sid.startswith("work_item-"))

            # Slow path: must load all items to check status
            return len(self.list_all(status=status))

    def clear(self) -> None:
        """
        Clear all work items (for testing).

        Removes all work_item streams from the event store.
        """
        with self._lock:
            stream_ids = self._event_store.get_all_stream_ids()

            for stream_id in stream_ids:
                if stream_id.startswith("work_item-"):
                    self._event_store.delete_stream(stream_id)


# =============================================================================
# Protocol Compliance Assertion
# =============================================================================


def _assert_protocol_compliance() -> None:
    """Static assertion that EventSourcedWorkItemRepository implements IWorkItemRepository."""
    from src.work_tracking.application.ports.work_item_repository import (
        IWorkItemRepository,
    )
    from src.work_tracking.infrastructure.persistence.filesystem_event_store import (
        FileSystemEventStore,
    )

    store: IEventStoreWithUtilities = FileSystemEventStore("/tmp")
    repository: IWorkItemRepository = EventSourcedWorkItemRepository(store)
    _ = repository  # Suppress unused variable warning
