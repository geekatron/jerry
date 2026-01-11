"""
IRepository - Generic repository port for aggregate persistence.

Defines the contract for aggregate root persistence. This is the domain's
view of persistence - it knows nothing about the underlying storage mechanism.
Infrastructure adapters implement this port to provide actual persistence.

References:
    - PAT-009: Generic Repository Port
    - DDD Repository Pattern (Evans, 2004)
    - Hexagonal Architecture Ports (Cockburn)

Exports:
    IRepository: Generic repository protocol
    AggregateNotFoundError: Raised when aggregate not found
    RepositoryError: Base exception for repository errors
"""

from __future__ import annotations

from typing import Protocol, TypeVar

from src.work_tracking.domain.aggregates.base import AggregateRoot

# =============================================================================
# Type Variables
# =============================================================================

# Type variable for aggregate types (must be AggregateRoot subclass)
TAggregate = TypeVar("TAggregate", bound=AggregateRoot)

# Type variable for ID types (typically str, but could be value object)
TId = TypeVar("TId")


# =============================================================================
# Exceptions
# =============================================================================


class RepositoryError(Exception):
    """Base exception for repository errors."""


class AggregateNotFoundError(RepositoryError):
    """
    Raised when an aggregate cannot be found.

    Attributes:
        aggregate_id: The ID that was not found
        aggregate_type: The type of aggregate being looked for

    Example:
        >>> raise AggregateNotFoundError("WORK-001", "WorkItem")
        AggregateNotFoundError: WorkItem 'WORK-001' not found
    """

    def __init__(self, aggregate_id: str, aggregate_type: str = "Aggregate") -> None:
        self.aggregate_id = aggregate_id
        self.aggregate_type = aggregate_type
        super().__init__(f"{aggregate_type} '{aggregate_id}' not found")


class ConcurrencyError(RepositoryError):
    """
    Raised when optimistic concurrency check fails during save.

    This occurs when the aggregate's version doesn't match what's
    stored, indicating another process modified it.

    Attributes:
        aggregate_id: The aggregate where the conflict occurred
        expected_version: The version the aggregate had
        actual_version: The version currently stored

    Example:
        >>> raise ConcurrencyError("WORK-001", expected=5, actual=7)
        ConcurrencyError: Aggregate 'WORK-001' version mismatch: expected 5, actual 7
    """

    def __init__(self, aggregate_id: str, expected: int, actual: int) -> None:
        self.aggregate_id = aggregate_id
        self.expected_version = expected
        self.actual_version = actual
        super().__init__(
            f"Aggregate '{aggregate_id}' version mismatch: expected {expected}, actual {actual}"
        )


# =============================================================================
# Repository Protocol
# =============================================================================


class IRepository(Protocol[TAggregate, TId]):
    """
    Generic repository port for aggregate persistence.

    The repository pattern mediates between the domain and data mapping
    layers. It provides a collection-like interface for accessing domain
    objects while hiding the complexity of data access.

    Type Parameters:
        TAggregate: The aggregate root type (bound to AggregateRoot)
        TId: The identifier type (typically str)

    Design Principles:
        - Collection semantics: Think of it as a collection of aggregates
        - Ignorance of storage: Domain doesn't know how aggregates are stored
        - One per aggregate type: Each aggregate root has its own repository
        - Optimistic concurrency: Save checks version to prevent conflicts

    Thread Safety:
        Implementations should be thread-safe for concurrent access.

    Example:
        >>> class WorkItemRepository(IRepository[WorkItem, str]):
        ...     def get(self, id: str) -> WorkItem | None:
        ...         # Load from storage
        ...         ...
        ...
        ...     def save(self, aggregate: WorkItem) -> None:
        ...         # Persist to storage
        ...         ...

    References:
        - Martin Fowler: Repository Pattern
          https://martinfowler.com/eaaCatalog/repository.html
        - Eric Evans: Domain-Driven Design, Chapter 6
    """

    def get(self, id: TId) -> TAggregate | None:
        """
        Retrieve an aggregate by its identifier.

        Args:
            id: The unique identifier of the aggregate

        Returns:
            The aggregate if found, None otherwise

        Note:
            Unlike get_or_raise, this method returns None for missing
            aggregates, allowing callers to handle absence gracefully.

        Example:
            >>> item = repository.get("WORK-001")
            >>> if item is not None:
            ...     process(item)
        """
        ...

    def get_or_raise(self, id: TId) -> TAggregate:
        """
        Retrieve an aggregate or raise if not found.

        Args:
            id: The unique identifier of the aggregate

        Returns:
            The aggregate

        Raises:
            AggregateNotFoundError: If the aggregate doesn't exist

        Example:
            >>> try:
            ...     item = repository.get_or_raise("WORK-001")
            ... except AggregateNotFoundError:
            ...     handle_not_found()
        """
        ...

    def save(self, aggregate: TAggregate) -> None:
        """
        Persist an aggregate.

        Saves both new aggregates and updates to existing ones.
        Implements optimistic concurrency - if the stored version
        doesn't match the aggregate's expected version, raises
        ConcurrencyError.

        Args:
            aggregate: The aggregate to persist

        Raises:
            ConcurrencyError: If version mismatch detected
            RepositoryError: If persistence fails

        Note:
            After save, the aggregate's pending events are consumed
            and should be published to any event handlers.

        Example:
            >>> item = WorkItem.create("WORK-001", "New Task")
            >>> repository.save(item)
        """
        ...

    def delete(self, id: TId) -> bool:
        """
        Remove an aggregate from the repository.

        Args:
            id: The unique identifier of the aggregate to delete

        Returns:
            True if the aggregate was deleted, False if it didn't exist

        Note:
            For event-sourced aggregates, this may mean writing a
            tombstone event rather than actually deleting data.

        Example:
            >>> if repository.delete("WORK-001"):
            ...     log.info("Deleted WORK-001")
        """
        ...

    def exists(self, id: TId) -> bool:
        """
        Check if an aggregate exists.

        Args:
            id: The unique identifier to check

        Returns:
            True if an aggregate with this ID exists

        Note:
            More efficient than get() when you only need to check
            existence without loading the full aggregate.

        Example:
            >>> if not repository.exists("WORK-001"):
            ...     create_new_item("WORK-001")
        """
        ...


# =============================================================================
# Type Assertions
# =============================================================================


def _assert_protocol_completeness() -> None:
    """Static assertion that IRepository has all required methods."""
    # This ensures the Protocol is complete at module load time
    methods = ["get", "get_or_raise", "save", "delete", "exists"]
    for method in methods:
        assert hasattr(IRepository, method), f"IRepository missing {method}"
