"""
Repository Pattern - Canonical implementation for Jerry Framework.

Repositories implement IRepository protocol and provide aggregate persistence.
Use composition of IFileStore and ISerializer adapters.

References:
    - architecture-standards.md (line 100)
    - infrastructure/adapters/file_repository.py
    - Repository pattern (Fowler, PofEAA)

Exports:
    IRepository protocol and example implementations
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Generic, Protocol, TypeVar

# Type variables for generic repository
TAggregate = TypeVar("TAggregate")
TId = TypeVar("TId")


# =============================================================================
# Repository Port (Protocol)
# =============================================================================


class IRepository(Protocol[TAggregate, TId]):
    """
    Generic repository port for aggregate persistence.

    Repositories SHOULD:
    - Implement this protocol
    - Use I{Noun} naming pattern
    - Be defined as domain ports or application secondary ports
    - Provide CRUD operations for aggregates
    - Handle optimistic concurrency control

    Type Parameters:
        TAggregate: The aggregate type being stored
        TId: The identifier type for the aggregate

    Example:
        >>> repo: IRepository[WorkItem, str] = FileRepository(...)
        >>> repo.save(work_item)
        >>> item = repo.get("WORK-001")
    """

    def get(self, id: TId) -> TAggregate | None:
        """
        Retrieve an aggregate by ID.

        Args:
            id: The aggregate identifier

        Returns:
            The aggregate if found, None otherwise
        """
        ...

    def save(self, aggregate: TAggregate) -> None:
        """
        Persist an aggregate.

        Args:
            aggregate: The aggregate to save

        Raises:
            ConcurrencyError: If version mismatch detected
        """
        ...

    def delete(self, id: TId) -> bool:
        """
        Delete an aggregate.

        Args:
            id: The aggregate identifier

        Returns:
            True if deleted, False if didn't exist
        """
        ...

    def exists(self, id: TId) -> bool:
        """
        Check if an aggregate exists.

        Args:
            id: The aggregate identifier

        Returns:
            True if exists
        """
        ...


# =============================================================================
# In-Memory Repository (for testing)
# =============================================================================


class InMemoryRepository(Generic[TAggregate, TId]):
    """
    In-memory repository implementation for testing.

    Provides simple dict-based storage without persistence.
    Useful for unit tests and rapid prototyping.

    Type Parameters:
        TAggregate: The aggregate type being stored
        TId: The identifier type for the aggregate

    Example:
        >>> repo = InMemoryRepository[WorkItem, str]()
        >>> repo.save(work_item)
        >>> item = repo.get("WORK-001")
    """

    def __init__(self) -> None:
        """Initialize empty repository."""
        self._store: dict[TId, TAggregate] = {}

    def get(self, id: TId) -> TAggregate | None:
        """Retrieve an aggregate by ID."""
        return self._store.get(id)

    def save(self, aggregate: TAggregate) -> None:
        """
        Persist an aggregate in memory.

        Note: This implementation does not check version for concurrency.
        For production use, implement optimistic locking.
        """
        # Extract ID from aggregate (assumes aggregate has 'id' property)
        aggregate_id = aggregate.id
        self._store[aggregate_id] = aggregate  # type: ignore

    def delete(self, id: TId) -> bool:
        """Delete an aggregate."""
        if id in self._store:
            del self._store[id]
            return True
        return False

    def exists(self, id: TId) -> bool:
        """Check if an aggregate exists."""
        return id in self._store

    def clear(self) -> None:
        """Clear all aggregates (useful for testing)."""
        self._store.clear()

    def count(self) -> int:
        """Return count of stored aggregates."""
        return len(self._store)


# =============================================================================
# File-Based Repository (Adapter)
# =============================================================================


class FileRepository(Generic[TAggregate, TId]):
    """
    File-based repository implementing IRepository port.

    Composes IFileStore and ISerializer to provide aggregate persistence.
    Uses optimistic concurrency control via aggregate version.

    Adapters SHOULD:
    - Use {Tech}{Entity}Adapter naming pattern
    - Compose infrastructure services (FileStore, Serializer)
    - Only be instantiated in bootstrap.py (H-09)
    - Map domain concepts to infrastructure concerns

    Type Parameters:
        TAggregate: The aggregate type being stored
        TId: The identifier type for the aggregate

    Attributes:
        file_store: File operations abstraction
        serializer: Serialization abstraction
        aggregate_type: The type of aggregate being stored
        base_path: Directory path for storing aggregate files
        id_extractor: Function to extract ID from aggregate

    Example:
        >>> from collections.abc import Callable
        >>> store = FilesystemFileStore()
        >>> serializer = JsonSerializer[WorkItem]()
        >>> repo = FileRepository(
        ...     file_store=store,
        ...     serializer=serializer,
        ...     aggregate_type=WorkItem,
        ...     base_path="work_items",
        ...     id_extractor=lambda w: w.id,
        ... )
        >>> repo.save(work_item)
        >>> loaded = repo.get("WORK-001")
    """

    def __init__(
        self,
        file_store: IFileStore,
        serializer: ISerializer[TAggregate],
        aggregate_type: type[TAggregate],
        base_path: str,
        id_extractor: Callable[[TAggregate], TId],
    ) -> None:
        """
        Initialize FileRepository.

        Args:
            file_store: File operations implementation
            serializer: Serialization implementation
            aggregate_type: Type of aggregate being stored
            base_path: Base directory for aggregate files
            id_extractor: Function to extract ID from aggregate instance
        """
        self._file_store = file_store
        self._serializer = serializer
        self._aggregate_type = aggregate_type
        self._base_path = base_path
        self._id_extractor = id_extractor

    def _get_file_path(self, aggregate_id: TId) -> str:
        """Get file path for an aggregate ID."""
        safe_id = str(aggregate_id).replace("/", "_").replace(":", "_")
        return f"{self._base_path}/{safe_id}.json"

    def get(self, id: TId) -> TAggregate | None:
        """
        Retrieve an aggregate by ID.

        Args:
            id: The aggregate identifier

        Returns:
            The aggregate if found, None otherwise
        """
        file_path = self._get_file_path(id)

        if not self._file_store.exists(file_path):
            return None

        try:
            data = self._file_store.read(file_path)
            return self._serializer.deserialize(data, self._aggregate_type)
        except Exception:
            return None

    def save(self, aggregate: TAggregate) -> None:
        """
        Persist an aggregate with optimistic concurrency.

        Args:
            aggregate: The aggregate to save

        Raises:
            ConcurrencyError: If version mismatch detected
        """
        aggregate_id = self._id_extractor(aggregate)
        file_path = self._get_file_path(aggregate_id)

        # Check for concurrency conflict
        if self._file_store.exists(file_path):
            try:
                data = self._file_store.read(file_path)
                existing = self._serializer.deserialize(data, self._aggregate_type)
                existing_version = getattr(existing, "version", 0)
                aggregate_version = getattr(aggregate, "version", 0)

                # If stored version > aggregate version = conflict
                if existing_version > aggregate_version:
                    raise ConcurrencyError(
                        str(aggregate_id),
                        expected=aggregate_version,
                        actual=existing_version,
                    )
            except Exception:
                pass  # File was deleted or corrupted

        # Serialize and save
        serialized = self._serializer.serialize(aggregate)
        self._file_store.write(file_path, serialized)

    def delete(self, id: TId) -> bool:
        """
        Delete an aggregate.

        Args:
            id: The aggregate identifier

        Returns:
            True if deleted, False if didn't exist
        """
        file_path = self._get_file_path(id)
        return self._file_store.delete(file_path)

    def exists(self, id: TId) -> bool:
        """
        Check if an aggregate exists.

        Args:
            id: The aggregate identifier

        Returns:
            True if exists
        """
        file_path = self._get_file_path(id)
        return self._file_store.exists(file_path)


# =============================================================================
# Supporting Infrastructure Protocols
# =============================================================================


class IFileStore(Protocol):
    """
    Protocol for file operations.

    Abstracts filesystem operations for testing and flexibility.
    """

    def exists(self, path: str) -> bool:
        """Check if file exists."""
        ...

    def read(self, path: str) -> str:
        """Read file contents."""
        ...

    def write(self, path: str, data: str) -> None:
        """Write file contents."""
        ...

    def delete(self, path: str) -> bool:
        """Delete file."""
        ...


class ISerializer(Protocol[TAggregate]):
    """
    Protocol for serialization.

    Abstracts serialization format (JSON, MessagePack, etc.).
    """

    def serialize(self, aggregate: TAggregate) -> str:
        """Serialize aggregate to string."""
        ...

    def deserialize(self, data: str, aggregate_type: type[TAggregate]) -> TAggregate:
        """Deserialize string to aggregate."""
        ...


# =============================================================================
# Domain Exceptions
# =============================================================================


class ConcurrencyError(Exception):
    """Optimistic concurrency conflict."""

    def __init__(self, aggregate_id: str, expected: int, actual: int) -> None:
        self.aggregate_id = aggregate_id
        self.expected_version = expected
        self.actual_version = actual
        super().__init__(
            f"Concurrency conflict for {aggregate_id}: "
            f"expected version {expected}, actual version {actual}"
        )
