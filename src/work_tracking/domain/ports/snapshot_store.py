"""
ISnapshotStore - Snapshot store port for aggregate state caching.

Defines the contract for snapshot storage, which caches aggregate state
at specific versions to optimize event replay. Snapshots are optional
performance optimization for event-sourced systems.

References:
    - IMPL-ES-002: ISnapshotStore Port
    - PAT-001: Event Store Interface Pattern
    - Event Sourcing: Snapshot Pattern
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Protocol, runtime_checkable
from uuid import UUID, uuid4

# =============================================================================
# Exceptions
# =============================================================================


class SnapshotStoreError(Exception):
    """Base exception for snapshot store errors."""


class SnapshotNotFoundError(SnapshotStoreError):
    """
    Raised when attempting to load a non-existent snapshot.

    Attributes:
        aggregate_id: The aggregate for which snapshot was not found

    Example:
        >>> raise SnapshotNotFoundError("WORK-999")
        SnapshotNotFoundError: Snapshot for aggregate 'WORK-999' not found
    """

    def __init__(self, aggregate_id: str) -> None:
        self.aggregate_id = aggregate_id
        super().__init__(f"Snapshot for aggregate '{aggregate_id}' not found")


# =============================================================================
# Value Objects
# =============================================================================


def _current_utc() -> datetime:
    """Get current UTC timestamp."""
    return datetime.now(UTC)


@dataclass(frozen=True, slots=True)
class StoredSnapshot:
    """
    Immutable wrapper for a persisted aggregate snapshot.

    StoredSnapshot captures the complete state of an aggregate at a specific
    version. It's used to optimize event replay by providing a starting point
    closer to the desired version.

    Attributes:
        aggregate_id: Unique identifier for the aggregate
        aggregate_type: Type name of the aggregate (for deserialization)
        version: Event version at which this snapshot was taken
        state: Complete serialized aggregate state
        timestamp: When the snapshot was created (UTC)
        snapshot_id: Globally unique identifier for this snapshot

    Invariants:
        - aggregate_id must not be empty
        - aggregate_type must not be empty
        - version must be >= 1
        - state must be a dictionary

    Example:
        >>> snapshot = StoredSnapshot(
        ...     aggregate_id="WORK-001",
        ...     aggregate_type="WorkItem",
        ...     version=100,
        ...     state={"title": "Feature", "status": "completed"},
        ... )
        >>> snapshot.version
        100
    """

    aggregate_id: str
    aggregate_type: str
    version: int
    state: dict[str, Any]
    timestamp: datetime = field(default_factory=_current_utc)
    snapshot_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        """Validate stored snapshot after initialization."""
        if not self.aggregate_id:
            raise ValueError("aggregate_id cannot be empty")
        if not self.aggregate_type:
            raise ValueError("aggregate_type cannot be empty")
        if self.version < 1:
            raise ValueError(f"version must be >= 1, got {self.version}")
        if not isinstance(self.state, dict):
            raise TypeError(f"state must be a dict, got {type(self.state).__name__}")

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize to dictionary for persistence.

        Returns:
            Dictionary representation suitable for JSON serialization.
        """
        return {
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "version": self.version,
            "state": self.state,
            "timestamp": self.timestamp.isoformat(),
            "snapshot_id": str(self.snapshot_id),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StoredSnapshot:
        """
        Deserialize from dictionary.

        Args:
            data: Dictionary from persistence layer

        Returns:
            Reconstructed StoredSnapshot instance
        """
        timestamp = data.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        elif timestamp is None:
            timestamp = _current_utc()

        snapshot_id = data.get("snapshot_id")
        if isinstance(snapshot_id, str):
            snapshot_id = UUID(snapshot_id)
        elif snapshot_id is None:
            snapshot_id = uuid4()

        return cls(
            aggregate_id=data["aggregate_id"],
            aggregate_type=data["aggregate_type"],
            version=data["version"],
            state=data["state"],
            timestamp=timestamp,
            snapshot_id=snapshot_id,
        )


# =============================================================================
# Port Interface
# =============================================================================


@runtime_checkable
class ISnapshotStore(Protocol):
    """
    Port: Snapshot Store for caching aggregate state.

    Snapshots provide an optimization for event-sourced aggregates by
    storing complete state at specific versions. This reduces the number
    of events that need to be replayed when reconstituting an aggregate.

    Thread Safety:
        Implementations MUST ensure thread-safe operations.

    Storage Model:
        Each aggregate has at most one snapshot at any time.
        Saving a new snapshot replaces the previous one.

    References:
        - IMPL-ES-002: ISnapshotStore Port
        - PAT-001: Event Store Interface Pattern
        - Event Sourcing: Snapshot Pattern

    Example Usage:
        >>> store = InMemorySnapshotStore()
        >>> snapshot = StoredSnapshot(
        ...     aggregate_id="WORK-001",
        ...     aggregate_type="WorkItem",
        ...     version=100,
        ...     state={"title": "Feature"},
        ... )
        >>> store.save(snapshot)
        >>> loaded = store.load("WORK-001")
        >>> loaded.version
        100
    """

    def save(self, snapshot: StoredSnapshot) -> None:
        """
        Save a snapshot, replacing any existing snapshot for the aggregate.

        Args:
            snapshot: The snapshot to save

        Example:
            >>> store.save(snapshot)
        """
        ...

    def load(self, aggregate_id: str) -> StoredSnapshot:
        """
        Load the snapshot for an aggregate.

        Args:
            aggregate_id: The aggregate to load snapshot for

        Returns:
            The stored snapshot

        Raises:
            SnapshotNotFoundError: If no snapshot exists for the aggregate

        Example:
            >>> snapshot = store.load("WORK-001")
            >>> snapshot.version
            100
        """
        ...

    def delete(self, aggregate_id: str) -> bool:
        """
        Delete the snapshot for an aggregate.

        Args:
            aggregate_id: The aggregate whose snapshot to delete

        Returns:
            True if a snapshot was deleted, False if none existed

        Example:
            >>> store.delete("WORK-001")
            True
            >>> store.delete("non-existent")
            False
        """
        ...

    def exists(self, aggregate_id: str) -> bool:
        """
        Check if a snapshot exists for an aggregate.

        Args:
            aggregate_id: The aggregate to check

        Returns:
            True if a snapshot exists

        Example:
            >>> store.exists("WORK-001")
            True
            >>> store.exists("non-existent")
            False
        """
        ...

    def get_version(self, aggregate_id: str) -> int | None:
        """
        Get the version of the snapshot for an aggregate.

        Args:
            aggregate_id: The aggregate to check

        Returns:
            The snapshot version, or None if no snapshot exists

        Example:
            >>> store.get_version("WORK-001")
            100
            >>> store.get_version("non-existent")
            None
        """
        ...


# =============================================================================
# In-Memory Implementation
# =============================================================================


class InMemorySnapshotStore(ISnapshotStore):
    """
    In-memory implementation of ISnapshotStore for testing.

    Stores snapshots in a dictionary. Not thread-safe and not persistent.
    Use only for unit testing and development.

    Example:
        >>> store = InMemorySnapshotStore()
        >>> store.save(StoredSnapshot(...))
        >>> store.load("WORK-001")
    """

    def __init__(self) -> None:
        """Initialize empty snapshot store."""
        self._snapshots: dict[str, StoredSnapshot] = {}

    def save(self, snapshot: StoredSnapshot) -> None:
        """Save snapshot, replacing any existing one for this aggregate."""
        self._snapshots[snapshot.aggregate_id] = snapshot

    def load(self, aggregate_id: str) -> StoredSnapshot:
        """Load snapshot or raise SnapshotNotFoundError."""
        if aggregate_id not in self._snapshots:
            raise SnapshotNotFoundError(aggregate_id)
        # Return the snapshot (it's frozen, so safe to return directly)
        # Make a deep copy of state to prevent mutation
        original = self._snapshots[aggregate_id]
        return StoredSnapshot(
            aggregate_id=original.aggregate_id,
            aggregate_type=original.aggregate_type,
            version=original.version,
            state=copy.deepcopy(original.state),
            timestamp=original.timestamp,
            snapshot_id=original.snapshot_id,
        )

    def delete(self, aggregate_id: str) -> bool:
        """Delete snapshot if it exists."""
        if aggregate_id in self._snapshots:
            del self._snapshots[aggregate_id]
            return True
        return False

    def exists(self, aggregate_id: str) -> bool:
        """Check if snapshot exists."""
        return aggregate_id in self._snapshots

    def get_version(self, aggregate_id: str) -> int | None:
        """Get snapshot version or None."""
        snapshot = self._snapshots.get(aggregate_id)
        return snapshot.version if snapshot else None
