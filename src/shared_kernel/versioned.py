"""
IVersioned - Optimistic concurrency control protocol.

Defines contract for version tracking to prevent lost updates.

References:
    - Canon PAT-006 (L311-340)

Exports:
    IVersioned (Protocol)
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class IVersioned(Protocol):
    """
    Version tracking for optimistic concurrency control.

    Invariants:
        - version starts at 0 (no events yet) or 1 (after creation event)
        - version increments by 1 for each persisted event
        - expected_version check prevents lost updates

    Usage:
        When saving an aggregate, the repository checks that the current
        version in storage matches the expected_version. If not, another
        process modified the aggregate, and a ConcurrencyError is raised.
    """

    @property
    def version(self) -> int:
        """Current version (number of events in stream)."""
        ...

    def get_expected_version(self) -> int:
        """Return version for concurrency check on save."""
        ...
