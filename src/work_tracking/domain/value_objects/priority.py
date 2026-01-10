"""
Priority - Work item priority value object.

Represents the priority level of a work item with natural ordering.
Uses IntEnum for numeric comparison (lower value = higher priority).

References:
    - PAT-005-e006: Quality Gate Value Objects
    - impl-es-e-006-workitem-schema: Priority specification
"""
from __future__ import annotations

from enum import IntEnum


class Priority(IntEnum):
    """
    Work item priority with numeric ordering.

    Uses IntEnum for natural sorting (lower value = higher priority).
    CRITICAL items are processed before HIGH, which are before MEDIUM, etc.

    Attributes:
        CRITICAL: Highest priority, immediate attention required (value 1)
        HIGH: High priority, should be addressed soon (value 2)
        MEDIUM: Normal priority, scheduled work (value 3)
        LOW: Low priority, can be deferred (value 4)

    Example:
        >>> Priority.CRITICAL < Priority.HIGH
        True
        >>> sorted([Priority.LOW, Priority.CRITICAL, Priority.MEDIUM])
        [<Priority.CRITICAL: 1>, <Priority.MEDIUM: 3>, <Priority.LOW: 4>]
        >>> Priority.from_string("high")
        <Priority.HIGH: 2>
    """

    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

    @classmethod
    def from_string(cls, value: str) -> Priority:
        """
        Parse case-insensitive priority string.

        Args:
            value: Priority name (case-insensitive, spaces converted to underscores)

        Returns:
            Matching Priority enum value, or MEDIUM as default fallback

        Example:
            >>> Priority.from_string("critical")
            <Priority.CRITICAL: 1>
            >>> Priority.from_string("HIGH")
            <Priority.HIGH: 2>
            >>> Priority.from_string("unknown")
            <Priority.MEDIUM: 3>
        """
        normalized = value.strip().upper().replace(" ", "_")
        try:
            return cls[normalized]
        except KeyError:
            return cls.MEDIUM  # Default fallback

    @classmethod
    def from_int(cls, value: int) -> Priority:
        """
        Create Priority from integer value.

        Args:
            value: Integer priority value (1-4)

        Returns:
            Matching Priority enum value

        Raises:
            ValueError: If value is not a valid priority (1-4)

        Example:
            >>> Priority.from_int(1)
            <Priority.CRITICAL: 1>
            >>> Priority.from_int(5)
            Traceback (most recent call last):
                ...
            ValueError: Invalid priority value: 5. Valid range is 1-4
        """
        for priority in cls:
            if priority.value == value:
                return priority
        raise ValueError(f"Invalid priority value: {value}. Valid range is 1-4")

    @property
    def is_high_priority(self) -> bool:
        """
        Check if this is a high-priority item (CRITICAL or HIGH).

        Returns:
            True if priority is CRITICAL or HIGH

        Example:
            >>> Priority.CRITICAL.is_high_priority
            True
            >>> Priority.MEDIUM.is_high_priority
            False
        """
        return self in (Priority.CRITICAL, Priority.HIGH)

    @property
    def is_low_priority(self) -> bool:
        """
        Check if this is a low-priority item (LOW only).

        Returns:
            True if priority is LOW

        Example:
            >>> Priority.LOW.is_low_priority
            True
            >>> Priority.MEDIUM.is_low_priority
            False
        """
        return self == Priority.LOW

    def __str__(self) -> str:
        """Return lowercase name for display."""
        return self.name.lower()

    def __repr__(self) -> str:
        """Return detailed representation for debugging."""
        return f"Priority.{self.name}"
