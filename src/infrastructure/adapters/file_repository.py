# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
FileRepository - File-based repository adapter.

Implements IRepository port using file storage. Composes IFileStore and
ISerializer for actual I/O operations.

References:
    - IMPL-REPO-003: FileRepository<T>
    - PAT-009: Generic Repository Port
    - PAT-010: Composed Infrastructure Adapters
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from typing import Generic, TypeVar

from src.infrastructure.internal.file_store import IFileStore
from src.infrastructure.internal.serializer import ISerializer
from src.work_tracking.domain.aggregates.base import AggregateRoot
from src.work_tracking.domain.ports.repository import (
    AggregateNotFoundError,
    ConcurrencyError,
)

# Type variables
TAggregate = TypeVar("TAggregate", bound=AggregateRoot)
TId = TypeVar("TId")


class FileRepository(Generic[TAggregate, TId]):
    """
    File-based repository implementing IRepository port.

    Composes IFileStore and ISerializer to provide aggregate persistence.
    Uses optimistic concurrency control via aggregate version.

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
        >>> store = InMemoryFileStore()
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
        # Sanitize ID for filesystem safety
        safe_id = self._sanitize_id(str(aggregate_id))
        return f"{self._base_path}/{safe_id}.json"

    def _sanitize_id(self, id_str: str) -> str:
        """Sanitize ID for use in file path.

        Handles special characters that might cause issues in filenames.
        """
        # For IDs with special characters, use a hash
        if any(c in id_str for c in '/\\:*?"<>|'):
            return (
                hashlib.sha256(id_str.encode()).hexdigest()[:16]
                + "_"
                + id_str.replace("/", "_").replace(":", "_")[:32]
            )
        return id_str

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

    def get_or_raise(self, id: TId) -> TAggregate:
        """
        Retrieve an aggregate or raise if not found.

        Args:
            id: The aggregate identifier

        Returns:
            The aggregate

        Raises:
            AggregateNotFoundError: If aggregate doesn't exist
        """
        aggregate = self.get(id)
        if aggregate is None:
            raise AggregateNotFoundError(str(id), self._aggregate_type.__name__)
        return aggregate

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
                existing_version = existing.version

                # Version in storage should match expected version
                # The aggregate's current version should be >= existing version
                # If aggregate.version equals existing, it means no changes (ok to save)
                # If aggregate.version > existing, it means local changes (ok to save)
                # But if we loaded with version N, didn't change, and someone else
                # changed to N+1, then our aggregate still at N but storage at N+1 = conflict

                # For proper optimistic concurrency:
                # We need to track the "original version" when loaded
                # For now, check if stored version > aggregate version = conflict
                if existing_version > aggregate.version:
                    raise ConcurrencyError(
                        str(aggregate_id),
                        expected=aggregate.version,
                        actual=existing_version,
                    )
            except AggregateNotFoundError:
                pass  # File was deleted between exists() and read()

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
