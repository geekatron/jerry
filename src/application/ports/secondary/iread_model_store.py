# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
IReadModelStore - Read Model Storage Port.

Defines the contract for storing and retrieving materialized views
(projections) optimized for read operations.

This is a secondary port (driven) used by projection handlers
to persist read-optimized data structures.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class IReadModelStore(Protocol):
    """Protocol for read model storage operations.

    Read models are denormalized, pre-computed views optimized for
    query performance. They are updated by projection handlers in
    response to domain events.

    Example:
        >>> store = InMemoryReadModelStore()
        >>> store.save("project_dashboard", "proj-001", {"name": "Test"})
        >>> data = store.load("project_dashboard", "proj-001")
    """

    def save(self, model_type: str, key: str, data: dict[str, Any]) -> None:
        """Save a read model instance.

        Args:
            model_type: Type/category of the read model (e.g., "project_dashboard")
            key: Unique identifier within the model type
            data: The read model data to persist
        """
        ...

    def load(self, model_type: str, key: str) -> dict[str, Any] | None:
        """Load a read model instance.

        Args:
            model_type: Type/category of the read model
            key: Unique identifier within the model type

        Returns:
            The read model data if found, None otherwise
        """
        ...

    def load_all(self, model_type: str) -> list[dict[str, Any]]:
        """Load all instances of a read model type.

        Args:
            model_type: Type/category of the read model

        Returns:
            List of all read model instances of the given type
        """
        ...

    def delete(self, model_type: str, key: str) -> bool:
        """Delete a read model instance.

        Args:
            model_type: Type/category of the read model
            key: Unique identifier within the model type

        Returns:
            True if deleted, False if not found
        """
        ...

    def exists(self, model_type: str, key: str) -> bool:
        """Check if a read model instance exists.

        Args:
            model_type: Type/category of the read model
            key: Unique identifier within the model type

        Returns:
            True if exists, False otherwise
        """
        ...
