"""
ValidationResult - Value Object representing the outcome of a validation operation.

This immutable value object captures whether validation succeeded or failed,
along with any messages (warnings for success, errors for failure).
"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Immutable value object representing a validation outcome.

    Attributes:
        is_valid: Whether the validation passed
        messages: List of validation messages (warnings if valid, errors if invalid)
    """

    is_valid: bool
    messages: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def success(cls, warnings: list[str] | None = None) -> ValidationResult:
        """Create a successful validation result.

        Args:
            warnings: Optional list of warning messages

        Returns:
            A ValidationResult with is_valid=True
        """
        return cls(
            is_valid=True,
            messages=tuple(warnings) if warnings else ()
        )

    @classmethod
    def failure(cls, errors: list[str]) -> ValidationResult:
        """Create a failed validation result.

        Args:
            errors: List of error messages explaining the failure

        Returns:
            A ValidationResult with is_valid=False

        Raises:
            ValueError: If errors list is empty (failure must have reasons)
        """
        if not errors:
            raise ValueError("Validation failure must include at least one error message")
        return cls(is_valid=False, messages=tuple(errors))

    @property
    def has_warnings(self) -> bool:
        """Check if there are warnings (only meaningful when valid)."""
        return self.is_valid and len(self.messages) > 0

    @property
    def has_errors(self) -> bool:
        """Check if there are errors (only meaningful when invalid)."""
        return not self.is_valid and len(self.messages) > 0

    @property
    def first_message(self) -> str | None:
        """Get the first message, if any."""
        return self.messages[0] if self.messages else None

    def __bool__(self) -> bool:
        """Allow using ValidationResult in boolean context."""
        return self.is_valid

    def __str__(self) -> str:
        """Return human-readable representation."""
        if self.is_valid:
            if self.messages:
                return f"Valid (with {len(self.messages)} warning(s))"
            return "Valid"
        return f"Invalid: {'; '.join(self.messages)}"
