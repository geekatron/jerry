"""
IAuditable - Audit metadata protocol.

Defines contract for tracking entity creation and modification.

References:
    - Canon PAT-005 (L266-309)

Exports:
    IAuditable (Protocol)
"""
from __future__ import annotations

from datetime import datetime
from typing import Protocol, runtime_checkable


@runtime_checkable
class IAuditable(Protocol):
    """
    Audit metadata contract for all entities.

    Invariants:
        - created_at is immutable after entity creation
        - updated_at >= created_at
        - created_by/updated_by are non-empty strings

    Values for created_by/updated_by:
        - User email (e.g., "user@example.com")
        - "Claude" for AI agent operations
        - "System" for automated/internal operations
    """

    @property
    def created_by(self) -> str:
        """User email, "Claude", or "System"."""
        ...

    @property
    def created_at(self) -> datetime:
        """UTC timestamp of entity creation."""
        ...

    @property
    def updated_by(self) -> str:
        """User email, "Claude", or "System"."""
        ...

    @property
    def updated_at(self) -> datetime:
        """UTC timestamp of last modification."""
        ...
