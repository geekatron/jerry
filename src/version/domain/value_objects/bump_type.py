# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BumpType value object for semantic version bump classification.

References:
    - BUG-002: Version bump regex rejects uppercase scopes
    - Semantic Versioning 2.0.0 specification
"""

from __future__ import annotations

import enum


class BumpType(enum.Enum):
    """Semantic version bump type with precedence ordering.

    Members are ordered by severity: MAJOR > MINOR > PATCH > NONE.
    The ``max()`` builtin selects the highest-severity bump when
    comparing multiple commits.
    """

    NONE = 0
    PATCH = 1
    MINOR = 2
    MAJOR = 3

    def __gt__(self, other: object) -> bool:
        """Compare bump types by severity.

        Args:
            other: Another BumpType to compare against.

        Returns:
            True if this bump type has higher severity.
        """
        if not isinstance(other, BumpType):
            return NotImplemented
        return self.value > other.value

    def __ge__(self, other: object) -> bool:
        """Compare bump types by severity (greater-than-or-equal).

        Args:
            other: Another BumpType to compare against.

        Returns:
            True if this bump type has equal or higher severity.
        """
        if not isinstance(other, BumpType):
            return NotImplemented
        return self.value >= other.value

    def __lt__(self, other: object) -> bool:
        """Compare bump types by severity (less-than).

        Args:
            other: Another BumpType to compare against.

        Returns:
            True if this bump type has lower severity.
        """
        if not isinstance(other, BumpType):
            return NotImplemented
        return self.value < other.value

    def __le__(self, other: object) -> bool:
        """Compare bump types by severity (less-than-or-equal).

        Args:
            other: Another BumpType to compare against.

        Returns:
            True if this bump type has equal or lower severity.
        """
        if not isinstance(other, BumpType):
            return NotImplemented
        return self.value <= other.value

    @property
    def label(self) -> str:
        """Return the lowercase label for CLI output.

        Returns:
            Lowercase string: 'major', 'minor', 'patch', or 'none'.
        """
        return self.name.lower()
