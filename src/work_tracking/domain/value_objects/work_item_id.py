"""
WorkItemId - Hybrid identity value object.

Combines a Snowflake-based internal ID for technical use with a
human-readable display ID for user interaction.

References:
    - ADR-007: ID Generation Strategy
    - PHASE-IMPL-DOMAIN: IMPL-003 specification

Exports:
    WorkItemId: Hybrid identity value object
"""
from __future__ import annotations

import re
from dataclasses import dataclass


# Module-level pattern to avoid issues with slots in frozen dataclass
_DISPLAY_PATTERN: re.Pattern[str] = re.compile(r"^WORK-(\d+)$")


@dataclass(frozen=True, slots=True)
class WorkItemId:
    """
    Hybrid identity combining Snowflake internal ID with human-readable display ID.

    The internal_id is a 64-bit Snowflake ID used for technical operations
    (database keys, event references, distributed coordination).

    The display_id is a human-readable format (WORK-nnn) used in UIs,
    logs, and verbal communication.

    Attributes:
        internal_id: 64-bit Snowflake ID for technical operations
        display_id: Human-readable ID in format WORK-nnn

    Example:
        >>> work_id = WorkItemId.create(internal_id=1767053847123456789, display_number=42)
        >>> work_id.display_id
        'WORK-042'
        >>> str(work_id)
        'WORK-042'
        >>> work_id.internal_hex
        '0x188....'

    Invariants:
        - internal_id is non-negative (Snowflake IDs are always positive)
        - display_number is positive (starts at 1)
        - display_id format is WORK-{number} with 3-digit minimum padding
    """

    internal_id: int
    display_id: str

    def __post_init__(self) -> None:
        """Validate WorkItemId after initialization."""
        if self.internal_id < 0:
            raise ValueError(
                f"internal_id must be non-negative, got {self.internal_id}"
            )
        if not _DISPLAY_PATTERN.match(self.display_id):
            raise ValueError(
                f"Invalid display_id format: {self.display_id!r}. "
                f"Expected format: WORK-nnn"
            )
        # Validate display number is positive
        match = _DISPLAY_PATTERN.match(self.display_id)
        if match:
            display_num = int(match.group(1))
            if display_num < 1:
                raise ValueError(
                    f"display_number must be positive, got {display_num}"
                )

    @classmethod
    def create(cls, internal_id: int, display_number: int) -> WorkItemId:
        """
        Create a WorkItemId from an internal Snowflake ID and display number.

        Args:
            internal_id: 64-bit Snowflake ID (must be non-negative)
            display_number: Sequential display number (must be positive)

        Returns:
            New WorkItemId instance

        Raises:
            ValueError: If internal_id is negative or display_number is not positive

        Example:
            >>> WorkItemId.create(1767053847123456789, 42)
            WorkItemId(internal_id=1767053847123456789, display_id='WORK-042')
        """
        if internal_id < 0:
            raise ValueError(
                f"internal_id must be non-negative, got {internal_id}"
            )
        if display_number < 1:
            raise ValueError(
                f"display_number must be positive, got {display_number}"
            )

        # Format with minimum 3 digits, no maximum
        display_id = f"WORK-{display_number:03d}"
        return cls(internal_id=internal_id, display_id=display_id)

    @classmethod
    def from_display_id(cls, display_id: str, internal_id: int) -> WorkItemId:
        """
        Create a WorkItemId from an existing display ID string.

        Useful when parsing existing IDs from storage or user input.

        Args:
            display_id: Human-readable ID in format WORK-nnn
            internal_id: 64-bit Snowflake ID to associate

        Returns:
            New WorkItemId instance

        Raises:
            ValueError: If display_id format is invalid or internal_id is negative

        Example:
            >>> WorkItemId.from_display_id("WORK-042", internal_id=12345)
            WorkItemId(internal_id=12345, display_id='WORK-042')
        """
        if not display_id:
            raise ValueError("Invalid display_id format: empty string")

        match = _DISPLAY_PATTERN.match(display_id)
        if not match:
            raise ValueError(
                f"Invalid display_id format: {display_id!r}. "
                f"Expected format: WORK-nnn"
            )

        return cls(internal_id=internal_id, display_id=display_id)

    @property
    def display_number(self) -> int:
        """
        Extract the numeric portion of the display ID.

        Returns:
            The display number as an integer

        Example:
            >>> work_id = WorkItemId.create(12345, 42)
            >>> work_id.display_number
            42
        """
        match = _DISPLAY_PATTERN.match(self.display_id)
        if match:
            return int(match.group(1))
        # This should never happen due to __post_init__ validation
        raise ValueError(f"Invalid display_id: {self.display_id}")  # pragma: no cover

    @property
    def internal_hex(self) -> str:
        """
        Get hexadecimal representation of the internal ID.

        Useful for debugging and compact display of large Snowflake IDs.

        Returns:
            Hex string prefixed with '0x'

        Example:
            >>> work_id = WorkItemId.create(255, 1)
            >>> work_id.internal_hex
            '0xff'
        """
        return hex(self.internal_id)

    def __str__(self) -> str:
        """Return the human-readable display ID."""
        return self.display_id

    def __repr__(self) -> str:
        """Return detailed representation for debugging."""
        return f"WorkItemId(internal_id={self.internal_id}, display_id={self.display_id!r})"

    def __eq__(self, other: object) -> bool:
        """WorkItemIds are equal if they have the same internal_id."""
        if not isinstance(other, WorkItemId):
            return NotImplemented
        return self.internal_id == other.internal_id

    def __hash__(self) -> int:
        """Hash by internal_id for set/dict usage."""
        return hash(self.internal_id)
