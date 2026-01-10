"""
TestCoverage - Test coverage percentage value object.

Represents test coverage as a validated percentage with comparison
and threshold checking capabilities.

References:
    - PAT-005-e006: Quality Gate Value Objects
    - Constraint c-004: Code Coverage Requirements
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TestCoverage:
    """
    Test coverage percentage with validation.

    A value object representing test coverage as a percentage.
    Immutable and self-validating.

    Attributes:
        percent: Coverage percentage (0.0 to 100.0)

    Invariants:
        - percent is between 0.0 and 100.0 inclusive
        - Can be compared, sorted, and used in quality gate calculations

    Example:
        >>> coverage = TestCoverage.from_percent(85.5)
        >>> coverage.meets_threshold(80.0)
        True
        >>> str(coverage)
        '85.5%'
    """

    percent: float

    def __post_init__(self) -> None:
        """Validate coverage percentage after initialization."""
        if not isinstance(self.percent, (int, float)):
            raise TypeError(
                f"percent must be a number, got {type(self.percent).__name__}"
            )
        if not 0.0 <= self.percent <= 100.0:
            raise ValueError(
                f"Coverage must be between 0 and 100, got {self.percent}"
            )

    @classmethod
    def from_percent(cls, value: float) -> TestCoverage:
        """
        Create from percentage value, rounding to 2 decimal places.

        Args:
            value: Coverage percentage (0.0 to 100.0)

        Returns:
            New TestCoverage instance

        Raises:
            ValueError: If value is out of range
            TypeError: If value is not a number

        Example:
            >>> TestCoverage.from_percent(85.567)
            TestCoverage(percent=85.57)
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"value must be a number, got {type(value).__name__}")
        return cls(percent=round(value, 2))

    @classmethod
    def from_fraction(cls, covered: int, total: int) -> TestCoverage:
        """
        Create from lines covered / total lines.

        Args:
            covered: Number of lines covered
            total: Total number of lines

        Returns:
            New TestCoverage instance (0% if total is 0)

        Raises:
            ValueError: If covered or total is negative
            ValueError: If covered > total

        Example:
            >>> TestCoverage.from_fraction(85, 100)
            TestCoverage(percent=85.0)
        """
        if covered < 0:
            raise ValueError(f"covered must be non-negative, got {covered}")
        if total < 0:
            raise ValueError(f"total must be non-negative, got {total}")
        if total == 0:
            return cls(percent=0.0)
        if covered > total:
            raise ValueError(
                f"covered ({covered}) cannot exceed total ({total})"
            )
        return cls(percent=round((covered / total) * 100, 2))

    def meets_threshold(self, threshold: float) -> bool:
        """
        Check if coverage meets or exceeds threshold.

        Args:
            threshold: Minimum required coverage percentage

        Returns:
            True if coverage >= threshold

        Example:
            >>> coverage = TestCoverage.from_percent(85.0)
            >>> coverage.meets_threshold(80.0)
            True
            >>> coverage.meets_threshold(90.0)
            False
        """
        return self.percent >= threshold

    def gap_to_threshold(self, threshold: float) -> float:
        """
        Calculate gap to reach threshold.

        Args:
            threshold: Target coverage percentage

        Returns:
            Positive value if below threshold, 0 if at or above

        Example:
            >>> coverage = TestCoverage.from_percent(75.0)
            >>> coverage.gap_to_threshold(90.0)
            15.0
        """
        return max(0.0, threshold - self.percent)

    def __str__(self) -> str:
        """Return human-readable percentage string."""
        return f"{self.percent:.1f}%"

    def __repr__(self) -> str:
        """Return detailed representation for debugging."""
        return f"TestCoverage(percent={self.percent})"

    def __lt__(self, other: object) -> bool:
        """Compare coverage percentages."""
        if not isinstance(other, TestCoverage):
            return NotImplemented
        return self.percent < other.percent

    def __le__(self, other: object) -> bool:
        """Compare coverage percentages."""
        if not isinstance(other, TestCoverage):
            return NotImplemented
        return self.percent <= other.percent

    def __gt__(self, other: object) -> bool:
        """Compare coverage percentages."""
        if not isinstance(other, TestCoverage):
            return NotImplemented
        return self.percent > other.percent

    def __ge__(self, other: object) -> bool:
        """Compare coverage percentages."""
        if not isinstance(other, TestCoverage):
            return NotImplemented
        return self.percent >= other.percent
