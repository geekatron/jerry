# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
EntityBase - Base class for all domain entities.

Combines VertexId identity with IAuditable and IVersioned.
All domain entities should inherit from this class.

References:
    - Canon PAT-007 (L342-407)

Exports:
    EntityBase (dataclass)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from .vertex_id import VertexId


def _utc_now() -> datetime:
    """Return current UTC time."""
    return datetime.now(UTC)


@dataclass
class EntityBase:
    """
    Base class for all domain entities.

    Combines:
        - VertexId identity (graph-ready)
        - IAuditable metadata (audit trail)
        - IVersioned concurrency control

    Subclasses must override _id type with specific VertexId subclass.

    Note: This class does NOT implement IAuditable/IVersioned protocols
    directly as they are runtime_checkable Protocols. Instead, it provides
    the required properties that make instances pass isinstance() checks.
    """

    _id: VertexId
    _version: int = 0
    _created_by: str = "System"
    _created_at: datetime = field(default_factory=_utc_now)
    _updated_by: str = "System"
    _updated_at: datetime = field(default_factory=_utc_now)

    @property
    def id(self) -> VertexId:
        """Entity identifier."""
        return self._id

    @property
    def version(self) -> int:
        """Current version for optimistic concurrency."""
        return self._version

    @property
    def created_by(self) -> str:
        """User who created this entity."""
        return self._created_by

    @property
    def created_at(self) -> datetime:
        """UTC timestamp of entity creation."""
        return self._created_at

    @property
    def updated_by(self) -> str:
        """User who last modified this entity."""
        return self._updated_by

    @property
    def updated_at(self) -> datetime:
        """UTC timestamp of last modification."""
        return self._updated_at

    def get_expected_version(self) -> int:
        """Return version for concurrency check on save."""
        return self._version

    def _touch(self, by: str) -> None:
        """
        Update modification metadata.

        Should be called after any mutation to the entity.

        Args:
            by: Identifier of who made the change (email, "Claude", or "System")
        """
        self._updated_by = by
        self._updated_at = _utc_now()

    def _increment_version(self) -> None:
        """Increment version after event is raised."""
        self._version += 1
