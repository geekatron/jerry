# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
SchemaRegistry - Dynamic schema registration with freeze support.

Provides the ``SchemaRegistry`` class for managing entity schema registration
with collision detection (T-SV-04) and post-initialization ``freeze()`` for
runtime poisoning prevention (T-SV-05). The ``schemas`` property returns a
``MappingProxyType`` for read-only access.

This class remediates V-06 (mutable module-level ``_SCHEMA_REGISTRY`` dict in
``schema.py``). The default registry is constructed, populated, and frozen at
module load time in ``schema.py``.

Security constraints:
    - Collision detection prevents duplicate key registration (T-SV-04, CWE-694)
    - ``freeze()`` prevents runtime schema poisoning (T-SV-05, CWE-915)
    - ``schemas`` property returns ``MappingProxyType`` for read-only view

References:
    - ADR-PROJ005-003 Design Decision 4 (Schema Extension Architecture)
    - Threat Model: T-SV-04, T-SV-05
    - H-07: Domain layer constraint (no external infra/interface imports)
    - H-10: One class per file (SchemaRegistry in its own module)

Exports:
    SchemaRegistry: Registry for file-type schemas with freeze() support.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.markdown_ast.schema import EntitySchema


class SchemaRegistry:
    """Registry for file-type schemas with dynamic registration and freeze support.

    Supports ``register()``, ``freeze()``, ``get()``, ``list_types()``, and a
    ``schemas`` property returning ``MappingProxyType`` for read-only access.

    Registration protocol:
        1. Call ``register()`` for each schema at module load time.
        2. Call ``freeze()`` after all registrations are complete.
        3. After ``freeze()``, ``register()`` raises ``RuntimeError``.

    Security:
        - Collision detection prevents duplicate key registration (T-SV-04).
        - ``freeze()`` prevents runtime schema poisoning (T-SV-05).
        - ``schemas`` property returns ``MappingProxyType`` for read-only view.

    Examples:
        >>> from src.domain.markdown_ast.schema import EPIC_SCHEMA
        >>> registry = SchemaRegistry()
        >>> registry.register(EPIC_SCHEMA)
        >>> registry.freeze()
        >>> registry.get("epic").entity_type
        'epic'
        >>> registry.register(EPIC_SCHEMA)  # Raises RuntimeError (frozen)
    """

    def __init__(self) -> None:
        """Initialize an empty, unfrozen schema registry."""
        self._schemas: dict[str, EntitySchema] = {}
        self._frozen: bool = False

    def register(self, schema: EntitySchema) -> None:
        """Register a schema. Raises ValueError on key collision (T-SV-04).

        Raises RuntimeError if registry is frozen (T-SV-05).

        Args:
            schema: The EntitySchema to register. Uses ``schema.entity_type``
                as the registry key.

        Raises:
            RuntimeError: If the registry has been frozen via ``freeze()``.
            ValueError: If a schema with the same ``entity_type`` is already
                registered.
        """
        if self._frozen:
            raise RuntimeError(
                f"Cannot register schema '{schema.entity_type}': registry is frozen. "
                f"Call register() before freeze()."
            )
        if schema.entity_type in self._schemas:
            raise ValueError(
                f"Schema '{schema.entity_type}' already registered. "
                f"Key collision detected (T-SV-04)."
            )
        self._schemas[schema.entity_type] = schema

    def freeze(self) -> None:
        """Freeze the registry. After this call, register() raises RuntimeError.

        The ``schemas`` property continues to work, returning a
        ``MappingProxyType`` for read-only access. This method is idempotent.
        """
        self._frozen = True

    @property
    def frozen(self) -> bool:
        """Return whether the registry has been frozen.

        Returns:
            True if ``freeze()`` has been called, False otherwise.
        """
        return self._frozen

    @property
    def schemas(self) -> MappingProxyType[str, EntitySchema]:
        """Read-only view of registered schemas.

        Returns:
            A ``MappingProxyType`` wrapping the internal schema dict.
            Mutations via this proxy raise ``TypeError``.
        """
        return MappingProxyType(self._schemas)

    def get(self, entity_type: str) -> EntitySchema:
        """Look up a schema by entity type.

        Args:
            entity_type: The entity type string to look up (e.g., "epic").

        Returns:
            The corresponding EntitySchema instance.

        Raises:
            ValueError: If ``entity_type`` is not registered.
        """
        schema = self._schemas.get(entity_type)
        if schema is None:
            valid = ", ".join(sorted(self._schemas.keys()))
            raise ValueError(f"Unknown entity type '{entity_type}'. Valid types: {valid}.")
        return schema

    def list_types(self) -> list[str]:
        """Return all registered entity type names, sorted alphabetically.

        Returns:
            Sorted list of entity type strings.
        """
        return sorted(self._schemas.keys())
