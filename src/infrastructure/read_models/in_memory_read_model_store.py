# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
InMemoryReadModelStore - In-Memory Read Model Storage Adapter.

Provides volatile in-memory storage for read models.
Primarily used for testing and development.

Note:
    Data is lost when the process terminates.
    For production, use a persistent implementation.
"""

from __future__ import annotations

from typing import Any


class InMemoryReadModelStore:
    """In-memory implementation of IReadModelStore.

    Stores read models in nested dictionaries keyed by model_type and key.
    Thread-safety: NOT thread-safe (use for single-threaded contexts only).

    Example:
        >>> store = InMemoryReadModelStore()
        >>> store.save("project_dashboard", "proj-001", {"name": "Test"})
        >>> store.load("project_dashboard", "proj-001")
        {'name': 'Test'}
    """

    def __init__(self) -> None:
        """Initialize the store with empty storage."""
        self._storage: dict[str, dict[str, dict[str, Any]]] = {}

    def save(self, model_type: str, key: str, data: dict[str, Any]) -> None:
        """Save a read model instance.

        Args:
            model_type: Type/category of the read model
            key: Unique identifier within the model type
            data: The read model data to persist
        """
        if model_type not in self._storage:
            self._storage[model_type] = {}
        self._storage[model_type][key] = data

    def load(self, model_type: str, key: str) -> dict[str, Any] | None:
        """Load a read model instance.

        Args:
            model_type: Type/category of the read model
            key: Unique identifier within the model type

        Returns:
            The read model data if found, None otherwise
        """
        return self._storage.get(model_type, {}).get(key)

    def load_all(self, model_type: str) -> list[dict[str, Any]]:
        """Load all instances of a read model type.

        Args:
            model_type: Type/category of the read model

        Returns:
            List of all read model instances of the given type
        """
        return list(self._storage.get(model_type, {}).values())

    def delete(self, model_type: str, key: str) -> bool:
        """Delete a read model instance.

        Args:
            model_type: Type/category of the read model
            key: Unique identifier within the model type

        Returns:
            True if deleted, False if not found
        """
        if model_type in self._storage and key in self._storage[model_type]:
            del self._storage[model_type][key]
            return True
        return False

    def exists(self, model_type: str, key: str) -> bool:
        """Check if a read model instance exists.

        Args:
            model_type: Type/category of the read model
            key: Unique identifier within the model type

        Returns:
            True if exists, False otherwise
        """
        return key in self._storage.get(model_type, {})

    def clear(self) -> None:
        """Clear all stored read models.

        Useful for resetting state between tests.
        """
        self._storage.clear()

    def count(self, model_type: str) -> int:
        """Count instances of a read model type.

        Args:
            model_type: Type/category of the read model

        Returns:
            Number of instances of the given type
        """
        return len(self._storage.get(model_type, {}))
