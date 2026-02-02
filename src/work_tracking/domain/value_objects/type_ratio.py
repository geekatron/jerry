"""
TypeRatio - Test type distribution value object.

Represents the distribution of test types (positive/negative/edge cases)
with quality level validation.

Note: Renamed from TestRatio to TypeRatio to avoid pytest collection
warnings (classes starting with "Test" are collected by pytest).

References:
    - PAT-005-e006: Quality Gate Value Objects
    - Constraint c-006: Test Distribution Requirements
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class QualityLevel(Enum):
    """
    Quality gate levels for test distribution.

    L0: Basic - positive tests only
    L1: Standard - positive + negative tests
    L2: Comprehensive - positive + negative + edge case tests
    """

    L0 = "L0"
    L1 = "L1"
    L2 = "L2"


@dataclass(frozen=True, slots=True)
class TypeRatio:
    """
    Distribution of test types (positive/negative/edge cases).

    A value object representing the balance of different test types
    in a test suite. Used for quality gate validation.

    Attributes:
        positive: Number of happy path tests
        negative: Number of error handling tests
        edge_case: Number of boundary condition tests

    Invariants:
        - All counts are non-negative
        - At least one test must exist (total > 0)

    Quality Gate Integration (c-006):
        - L0: Positive tests only is acceptable
        - L1: Must have positive + negative tests
        - L2: Must have positive + negative + edge case tests

    Example:
        >>> ratio = TypeRatio(positive=5, negative=3, edge_case=2)
        >>> ratio.total
        10
        >>> ratio.positive_percent
        50.0
        >>> ratio.meets_level(QualityLevel.L2)
        True
    """

    positive: int  # Happy path tests
    negative: int  # Error handling tests
    edge_case: int  # Boundary condition tests

    def __post_init__(self) -> None:
        """Validate test counts after initialization."""
        if not isinstance(self.positive, int):
            raise TypeError(f"positive must be an integer, got {type(self.positive).__name__}")
        if not isinstance(self.negative, int):
            raise TypeError(f"negative must be an integer, got {type(self.negative).__name__}")
        if not isinstance(self.edge_case, int):
            raise TypeError(f"edge_case must be an integer, got {type(self.edge_case).__name__}")
        if self.positive < 0:
            raise ValueError(f"positive must be non-negative, got {self.positive}")
        if self.negative < 0:
            raise ValueError(f"negative must be non-negative, got {self.negative}")
        if self.edge_case < 0:
            raise ValueError(f"edge_case must be non-negative, got {self.edge_case}")
        if self.total == 0:
            raise ValueError("At least one test is required")

    @property
    def total(self) -> int:
        """Total number of tests."""
        return self.positive + self.negative + self.edge_case

    @property
    def positive_percent(self) -> float:
        """Percentage of positive tests."""
        return round((self.positive / self.total) * 100, 2)

    @property
    def negative_percent(self) -> float:
        """Percentage of negative tests."""
        return round((self.negative / self.total) * 100, 2)

    @property
    def edge_case_percent(self) -> float:
        """Percentage of edge case tests."""
        return round((self.edge_case / self.total) * 100, 2)

    def meets_level(self, level: QualityLevel | str) -> bool:
        """
        Check if ratio meets quality gate level requirements.

        Args:
            level: Quality level to check (L0, L1, or L2)

        Returns:
            True if the test distribution meets the level requirements

        Level Requirements:
            - L0: positive > 0
            - L1: positive > 0 and negative > 0
            - L2: positive > 0 and negative > 0 and edge_case > 0

        Example:
            >>> ratio = TypeRatio(positive=5, negative=3, edge_case=0)
            >>> ratio.meets_level(QualityLevel.L1)
            True
            >>> ratio.meets_level(QualityLevel.L2)
            False
        """
        # Convert string to enum if needed
        if isinstance(level, str):
            try:
                level = QualityLevel(level)
            except ValueError:
                raise ValueError(f"Unknown quality level: {level}") from None

        if level == QualityLevel.L0:
            return self.positive > 0
        elif level == QualityLevel.L1:
            return self.positive > 0 and self.negative > 0
        elif level == QualityLevel.L2:
            return self.positive > 0 and self.negative > 0 and self.edge_case > 0
        else:
            raise ValueError(f"Unknown quality level: {level}")

    def highest_met_level(self) -> QualityLevel:
        """
        Return the highest quality level this ratio meets.

        Returns:
            The highest QualityLevel that passes meets_level()

        Example:
            >>> ratio = TypeRatio(positive=5, negative=3, edge_case=0)
            >>> ratio.highest_met_level()
            <QualityLevel.L1: 'L1'>
        """
        if self.meets_level(QualityLevel.L2):
            return QualityLevel.L2
        elif self.meets_level(QualityLevel.L1):
            return QualityLevel.L1
        else:
            return QualityLevel.L0

    def __str__(self) -> str:
        """Return compact string representation."""
        return f"P:{self.positive}/N:{self.negative}/E:{self.edge_case}"

    def __repr__(self) -> str:
        """Return detailed representation for debugging."""
        return (
            f"TypeRatio(positive={self.positive}, "
            f"negative={self.negative}, edge_case={self.edge_case})"
        )
