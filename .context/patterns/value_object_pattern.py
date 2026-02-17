"""
Value Object Pattern - Canonical implementation for Jerry Framework.

Value objects are immutable objects defined by their values, not identity.
Use frozen dataclasses with validation in __post_init__.

References:
    - architecture-standards.md (line 97)
    - DDD Value Object pattern (Evans, 2004)

Exports:
    Example value objects following Jerry conventions
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# =============================================================================
# Pattern 1: Simple Value Object with Validation
# =============================================================================


@dataclass(frozen=True, slots=True)
class EmailAddress:
    """
    Example value object - Email address with validation.

    Value objects SHOULD use @dataclass(frozen=True, slots=True) for
    immutability and memory efficiency.

    Attributes:
        value: The email address string

    Example:
        >>> email = EmailAddress("user@example.com")
        >>> str(email)
        'user@example.com'
        >>> email == EmailAddress("user@example.com")
        True

    Invariants:
        - Must contain '@' character
        - Must have non-empty local and domain parts
    """

    value: str

    def __post_init__(self) -> None:
        """Validate email address after initialization."""
        if not self.value:
            raise ValueError("Email address cannot be empty")
        if "@" not in self.value:
            raise ValueError(f"Invalid email address: {self.value!r}")

        local, domain = self.value.rsplit("@", 1)
        if not local or not domain:
            raise ValueError(f"Invalid email address: {self.value!r}")

    def __str__(self) -> str:
        """Return string representation for display."""
        return self.value


# =============================================================================
# Pattern 2: Complex Value Object with Multiple Fields
# =============================================================================


@dataclass(frozen=True, slots=True)
class Money:
    """
    Example value object - Money with amount and currency.

    Demonstrates multi-field value object with validation and
    custom equality semantics.

    Attributes:
        amount: Decimal amount
        currency: ISO 4217 currency code

    Example:
        >>> price = Money(99.99, "USD")
        >>> tax = Money(9.99, "USD")
        >>> price == Money(99.99, "USD")
        True

    Invariants:
        - amount must be non-negative
        - currency must be 3-letter ISO code (uppercase)
    """

    amount: float
    currency: str

    def __post_init__(self) -> None:
        """Validate money value after initialization."""
        if self.amount < 0:
            raise ValueError(f"Amount must be non-negative, got {self.amount}")

        if not self.currency:
            raise ValueError("Currency cannot be empty")

        if len(self.currency) != 3 or not self.currency.isupper():
            raise ValueError(
                f"Currency must be 3-letter ISO code (uppercase), got {self.currency!r}"
            )

    def __str__(self) -> str:
        """Return formatted money string."""
        return f"{self.amount:.2f} {self.currency}"


# =============================================================================
# Pattern 3: Value Object with Factory Methods
# =============================================================================


_DISPLAY_PATTERN: re.Pattern[str] = re.compile(r"^WORK-(\d+)$")


@dataclass(frozen=True, slots=True)
class WorkItemId:
    """
    Example hybrid identity value object.

    Demonstrates factory methods for different construction scenarios.
    Based on actual Jerry codebase value object.

    Attributes:
        internal_id: Technical ID for persistence
        display_id: Human-readable ID for UI

    Example:
        >>> work_id = WorkItemId.create(12345, 42)
        >>> work_id.display_id
        'WORK-042'
        >>> str(work_id)
        'WORK-042'

    Invariants:
        - internal_id must be non-negative
        - display_id must match WORK-nnn format
        - display_number must be positive
    """

    internal_id: int
    display_id: str

    def __post_init__(self) -> None:
        """Validate WorkItemId after initialization."""
        if self.internal_id < 0:
            raise ValueError(f"internal_id must be non-negative, got {self.internal_id}")

        if not _DISPLAY_PATTERN.match(self.display_id):
            raise ValueError(
                f"Invalid display_id format: {self.display_id!r}. Expected format: WORK-nnn"
            )

        # Validate display number is positive
        match = _DISPLAY_PATTERN.match(self.display_id)
        if match:
            display_num = int(match.group(1))
            if display_num < 1:
                raise ValueError(f"display_number must be positive, got {display_num}")

    @classmethod
    def create(cls, internal_id: int, display_number: int) -> WorkItemId:
        """
        Create a WorkItemId from internal ID and display number.

        Args:
            internal_id: Technical ID (must be non-negative)
            display_number: Sequential display number (must be positive)

        Returns:
            New WorkItemId instance

        Raises:
            ValueError: If internal_id is negative or display_number is not positive

        Example:
            >>> WorkItemId.create(12345, 42)
            WorkItemId(internal_id=12345, display_id='WORK-042')
        """
        if internal_id < 0:
            raise ValueError(f"internal_id must be non-negative, got {internal_id}")
        if display_number < 1:
            raise ValueError(f"display_number must be positive, got {display_number}")

        # Format with minimum 3 digits
        display_id = f"WORK-{display_number:03d}"
        return cls(internal_id=internal_id, display_id=display_id)

    @classmethod
    def from_display_id(cls, display_id: str, internal_id: int) -> WorkItemId:
        """
        Create a WorkItemId from existing display ID string.

        Useful when parsing from storage or user input.

        Args:
            display_id: Human-readable ID in format WORK-nnn
            internal_id: Technical ID to associate

        Returns:
            New WorkItemId instance

        Raises:
            ValueError: If display_id format is invalid or internal_id is negative

        Example:
            >>> WorkItemId.from_display_id("WORK-042", 12345)
            WorkItemId(internal_id=12345, display_id='WORK-042')
        """
        if not display_id:
            raise ValueError("Invalid display_id format: empty string")

        match = _DISPLAY_PATTERN.match(display_id)
        if not match:
            raise ValueError(
                f"Invalid display_id format: {display_id!r}. Expected format: WORK-nnn"
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
        raise ValueError(f"Invalid display_id: {self.display_id}")  # pragma: no cover

    def __str__(self) -> str:
        """Return the human-readable display ID."""
        return self.display_id

    def __eq__(self, other: object) -> bool:
        """Value objects are equal if internal_id matches."""
        if not isinstance(other, WorkItemId):
            return NotImplemented
        return self.internal_id == other.internal_id

    def __hash__(self) -> int:
        """Hash by internal_id for set/dict usage."""
        return hash(self.internal_id)
