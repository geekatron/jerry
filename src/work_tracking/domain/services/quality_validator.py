"""
Quality Gate Validator Domain Service.

Domain service for validating quality gate requirements and assessing
risk tiers for changes. Encapsulates the logic for L0/L1/L2 gate validation
and T1-T4 risk classification.

Design:
    - Stateless validation logic
    - Configurable thresholds per gate level
    - Pattern-based risk assessment

References:
    - IMPL-009: Domain Services
    - ADR-008: Quality Gate Layer Configuration
    - PAT-008: Value Object Quality Gates

Exports:
    IQualityGateValidator: Protocol for gate validation
    QualityGateValidator: Concrete implementation
    ValidationResult: Immutable result of validation
"""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from src.work_tracking.domain.value_objects import (
    Coverage,
    GateLevel,
    RiskTier,
    TypeRatio,
)

# =============================================================================
# Validation Result
# =============================================================================


@dataclass(frozen=True)
class ValidationResult:
    """
    Immutable result of quality gate validation.

    Attributes:
        gate_level: The gate level that was validated
        passed: Whether the validation passed
        failures: List of failure reasons (empty if passed)

    Example:
        >>> result = ValidationResult(
        ...     gate_level=GateLevel.L1,
        ...     passed=False,
        ...     failures=["Coverage below 80%"],
        ... )
        >>> result.passed
        False
    """

    gate_level: GateLevel
    passed: bool
    failures: list[str] = field(default_factory=list)


# =============================================================================
# Protocol
# =============================================================================


@runtime_checkable
class IQualityGateValidator(Protocol):
    """
    Protocol for quality gate validation.

    Implementations validate quality metrics against gate requirements
    and assess risk tiers for changes.

    Example:
        >>> def check_ready_for_merge(
        ...     validator: IQualityGateValidator,
        ...     coverage: Coverage,
        ...     ratio: TypeRatio,
        ... ) -> bool:
        ...     result = validator.validate(GateLevel.L1, coverage, ratio)
        ...     return result.passed
    """

    def validate(
        self,
        gate_level: GateLevel,
        coverage: Coverage | None,
        ratio: TypeRatio | None,
    ) -> ValidationResult:
        """
        Validate quality metrics against gate requirements.

        Args:
            gate_level: Gate level to validate against (L0, L1, L2)
            coverage: Test coverage metrics (optional)
            ratio: Test type distribution (optional)

        Returns:
            ValidationResult with pass/fail and any failure reasons
        """
        ...

    def assess_risk(
        self,
        file_patterns: list[str],
        keywords: list[str],
    ) -> RiskTier:
        """
        Assess risk tier based on file patterns and keywords.

        Args:
            file_patterns: List of file path patterns being changed
            keywords: Keywords found in commit message or changes

        Returns:
            Appropriate risk tier (T1-T4)
        """
        ...


# =============================================================================
# Gate Level Thresholds
# =============================================================================

# Coverage thresholds per gate level
_COVERAGE_THRESHOLDS: dict[GateLevel, float] = {
    GateLevel.L0: 0.0,  # No coverage requirement
    GateLevel.L1: 80.0,  # 80% for merge gate
    GateLevel.L2: 90.0,  # 90% for release gate
}

# Required test types per gate level
_REQUIRED_TEST_TYPES: dict[GateLevel, set[str]] = {
    GateLevel.L0: {"positive"},  # At least positive tests
    GateLevel.L1: {"positive", "negative"},  # Need negative tests
    GateLevel.L2: {"positive", "negative", "edge_case"},  # Full pyramid
}


# =============================================================================
# Risk Tier Patterns
# =============================================================================

# File patterns that indicate specific risk tiers
_T4_PATTERNS = [
    "**/security/**",
    "**/*auth*/**",
    "**/*credential*/**",
    "**/migration*/**",
]

_T3_PATTERNS = [
    "**/domain/**",
    "**/infrastructure/**",
    "**/ports/**",
    "**/adapters/**",
]

_T2_PATTERNS = [
    "**/tests/**",
    "**/application/**",
    "**/services/**",
]

# Keywords that elevate risk to T4
_T4_KEYWORDS = {
    "BREAKING",
    "MIGRATION",
    "SECURITY",
    "AUTH",
    "CREDENTIAL",
    "PASSWORD",
    "SECRET",
    "TOKEN",
}


# =============================================================================
# Implementation
# =============================================================================


class QualityGateValidator(IQualityGateValidator):
    """
    Quality gate validator implementation.

    Validates quality metrics against gate requirements and assesses
    risk tiers based on file patterns and keywords.

    Thread Safety:
        This class is stateless and thread-safe.

    Example:
        >>> validator = QualityGateValidator()
        >>> result = validator.validate(
        ...     gate_level=GateLevel.L1,
        ...     coverage=Coverage.from_percent(85),
        ...     ratio=TypeRatio(positive=10, negative=5, edge_case=3),
        ... )
        >>> result.passed
        True
    """

    def validate(
        self,
        gate_level: GateLevel,
        coverage: Coverage | None,
        ratio: TypeRatio | None,
    ) -> ValidationResult:
        """
        Validate quality metrics against gate requirements.

        Args:
            gate_level: Gate level to validate against (L0, L1, L2)
            coverage: Test coverage metrics (optional)
            ratio: Test type distribution (optional)

        Returns:
            ValidationResult with pass/fail and any failure reasons
        """
        failures: list[str] = []

        # Check if we have any test metrics
        if coverage is None and ratio is None:
            failures.append("No tests found - both coverage and ratio are missing")
            return ValidationResult(
                gate_level=gate_level,
                passed=False,
                failures=failures,
            )

        # Check coverage threshold
        threshold = _COVERAGE_THRESHOLDS[gate_level]
        if threshold > 0:
            if coverage is None:
                failures.append(f"Coverage required but not provided (need {int(threshold)}%)")
            elif coverage.percent < threshold:
                failures.append(
                    f"Coverage {coverage.percent:.0f}% is below required {int(threshold)}%"
                )

        # Check required test types
        required_types = _REQUIRED_TEST_TYPES[gate_level]
        if ratio is None:
            if len(required_types) > 0 and gate_level != GateLevel.L0:
                failures.append(f"Test ratio required for {gate_level.value} but not provided")
        else:
            if "positive" in required_types and ratio.positive == 0:
                failures.append("Positive (happy path) tests required but none found")
            if "negative" in required_types and ratio.negative == 0:
                failures.append("Negative (error case) tests required but none found")
            if "edge_case" in required_types and ratio.edge_case == 0:
                failures.append("Edge case tests required but none found")

        return ValidationResult(
            gate_level=gate_level,
            passed=len(failures) == 0,
            failures=failures,
        )

    def assess_risk(
        self,
        file_patterns: list[str],
        keywords: list[str],
    ) -> RiskTier:
        """
        Assess risk tier based on file patterns and keywords.

        Risk Assessment Logic:
        1. Keywords in T4_KEYWORDS immediately elevate to T4
        2. File patterns matching T4_PATTERNS → T4
        3. File patterns matching T3_PATTERNS → T3
        4. File patterns matching T2_PATTERNS → T2
        5. All other patterns → T1 (docs, config, etc.)

        Args:
            file_patterns: List of file path patterns being changed
            keywords: Keywords found in commit message or changes

        Returns:
            Appropriate risk tier (T1-T4)
        """
        # Check keywords first - they can elevate to T4
        upper_keywords = {kw.upper() for kw in keywords}
        if upper_keywords & _T4_KEYWORDS:
            return RiskTier.T4

        # If no files, default to T1
        if not file_patterns:
            return RiskTier.T1

        # Check file patterns for highest tier
        max_tier = RiskTier.T1

        for pattern in file_patterns:
            # Check T4 patterns
            if self._matches_any(pattern, _T4_PATTERNS):
                return RiskTier.T4

            # Check T3 patterns
            if self._matches_any(pattern, _T3_PATTERNS):
                if max_tier.value < RiskTier.T3.value:
                    max_tier = RiskTier.T3

            # Check T2 patterns
            if self._matches_any(pattern, _T2_PATTERNS):
                if max_tier.value < RiskTier.T2.value:
                    max_tier = RiskTier.T2

        return max_tier

    @staticmethod
    def _matches_any(path: str, patterns: list[str]) -> bool:
        """Check if path matches any of the patterns."""
        for pattern in patterns:
            if fnmatch.fnmatch(path, pattern):
                return True
        return False
