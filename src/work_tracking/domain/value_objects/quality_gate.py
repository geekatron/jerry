# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
QualityGate Value Objects.

Value objects for quality gate configuration and evaluation.

Components:
    - GateLevel: Gate level enumeration (L0/L1/L2)
    - RiskTier: Risk classification (T1-T4)
    - GateResult: Gate execution result states
    - ThresholdType: Types of threshold metrics
    - Threshold: Numeric threshold with validation
    - GateCheckDefinition: Individual check definition

References:
    - IMPL-006: QualityGate Entity
    - ADR-008: Quality Gate Layer Configuration
    - dev-skill-e-002: Quality Gate Enforcement patterns
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum


class GateLevel(Enum):
    """
    Quality gate level enumeration.

    Levels execute in sequence: L0 -> L1 -> L2.
    Each level has different characteristics and timeout.

    Attributes:
        L0: Syntax & Basic validation (mandatory, 60s timeout)
        L1: Semantic & Quality validation (mandatory, 300s timeout)
        L2: Distinguished Review (optional, 600s timeout)

    References:
        - ADR-008: Quality Gate Layer Configuration
    """

    L0 = "L0"
    L1 = "L1"
    L2 = "L2"

    @property
    def order(self) -> int:
        """Return execution order (0, 1, 2)."""
        return {"L0": 0, "L1": 1, "L2": 2}[self.value]

    @property
    def display_name(self) -> str:
        """Return human-readable name."""
        names = {
            "L0": "Syntax & Basic",
            "L1": "Semantic & Quality",
            "L2": "Distinguished Review",
        }
        return names[self.value]

    @property
    def is_mandatory(self) -> bool:
        """Check if this level is mandatory."""
        return self != GateLevel.L2

    @property
    def default_timeout_seconds(self) -> int:
        """Return default timeout in seconds."""
        timeouts = {"L0": 60, "L1": 300, "L2": 600}
        return timeouts[self.value]

    @classmethod
    def from_string(cls, value: str) -> GateLevel:
        """
        Parse case-insensitive gate level string.

        Args:
            value: Gate level name (case-insensitive)

        Returns:
            Matching GateLevel enum value

        Raises:
            ValueError: If value is not a valid gate level

        Example:
            >>> GateLevel.from_string("l0")
            <GateLevel.L0: 'L0'>
        """
        normalized = value.strip().upper()
        for level in cls:
            if level.value == normalized:
                return level
        raise ValueError(f"Invalid gate level: '{value}'. Valid values: L0, L1, L2")


class RiskTier(IntEnum):
    """
    Risk classification for changes.

    Uses IntEnum for natural ordering (T1 < T2 < T3 < T4).
    Higher tier = higher risk = more validation required.

    Attributes:
        T1: Low Risk - documentation, config, tests
        T2: Medium Risk - feature changes, bug fixes
        T3: High Risk - domain logic, ports, API
        T4: Critical Risk - security, migrations, breaking changes

    References:
        - ADR-008: Risk Classification section
    """

    T1 = 1
    T2 = 2
    T3 = 3
    T4 = 4

    @property
    def description(self) -> str:
        """Return human-readable description."""
        descriptions = {
            1: "Low Risk",
            2: "Medium Risk",
            3: "High Risk",
            4: "Critical Risk",
        }
        return descriptions[self.value]

    @property
    def requires_l2(self) -> bool:
        """Check if this tier requires L2 gate."""
        return self >= RiskTier.T3

    @property
    def requires_human_approval(self) -> bool:
        """Check if this tier requires human approval."""
        return self == RiskTier.T4

    def required_gate_levels(self) -> list[GateLevel]:
        """
        Return list of required gate levels for this risk tier.

        Returns:
            List of GateLevel values in execution order
        """
        if self.requires_l2:
            return [GateLevel.L0, GateLevel.L1, GateLevel.L2]
        return [GateLevel.L0, GateLevel.L1]

    @classmethod
    def from_string(cls, value: str) -> RiskTier:
        """
        Parse case-insensitive risk tier string.

        Args:
            value: Risk tier name (e.g., "T1", "t2")

        Returns:
            Matching RiskTier enum value

        Raises:
            ValueError: If value is not a valid risk tier

        Example:
            >>> RiskTier.from_string("t1")
            <RiskTier.T1: 1>
        """
        normalized = value.strip().upper()
        tier_map = {"T1": cls.T1, "T2": cls.T2, "T3": cls.T3, "T4": cls.T4}
        if normalized in tier_map:
            return tier_map[normalized]
        raise ValueError(f"Invalid risk tier: '{value}'. Valid values: T1, T2, T3, T4")


class GateResult(Enum):
    """
    Gate execution result states.

    Attributes:
        PENDING: Gate has not completed execution
        PASSED: Gate passed all checks
        FAILED: Gate failed one or more checks
        SKIPPED: Gate was skipped (not required)
    """

    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"

    @property
    def is_terminal(self) -> bool:
        """Check if this is a terminal state."""
        return self != GateResult.PENDING

    @property
    def is_success(self) -> bool:
        """Check if this is a successful result."""
        return self == GateResult.PASSED

    @classmethod
    def from_string(cls, value: str) -> GateResult:
        """
        Parse case-insensitive result string.

        Args:
            value: Result name (case-insensitive)

        Returns:
            Matching GateResult enum value

        Raises:
            ValueError: If value is not a valid result

        Example:
            >>> GateResult.from_string("PASSED")
            <GateResult.PASSED: 'passed'>
        """
        normalized = value.strip().lower()
        for result in cls:
            if result.value == normalized:
                return result
        raise ValueError(
            f"Invalid gate result: '{value}'. Valid values: pending, passed, failed, skipped"
        )


class ThresholdType(Enum):
    """
    Types of threshold metrics.

    Attributes:
        COVERAGE: Code coverage percentage
        COMPLEXITY: Cyclomatic complexity score
        DUPLICATION: Code duplication percentage
        MUTATION: Mutation testing score
    """

    COVERAGE = "coverage"
    COMPLEXITY = "complexity"
    DUPLICATION = "duplication"
    MUTATION = "mutation"

    @property
    def is_percentage(self) -> bool:
        """Check if this type is measured as a percentage (0-100)."""
        return self in (ThresholdType.COVERAGE, ThresholdType.DUPLICATION, ThresholdType.MUTATION)

    @property
    def higher_is_better(self) -> bool:
        """Check if higher values are better for this type."""
        # For coverage and mutation, higher is better
        # For complexity and duplication, lower is better
        return self in (ThresholdType.COVERAGE, ThresholdType.MUTATION)


@dataclass(frozen=True, slots=True)
class Threshold:
    """
    Numeric threshold with validation.

    Represents a threshold that can have a minimum and/or maximum value.
    Percentage types (coverage, duplication) are validated to 0-100 range.

    Attributes:
        threshold_type: The type of metric being measured
        minimum: Minimum acceptable value (inclusive)
        maximum: Maximum acceptable value (inclusive)

    Example:
        >>> coverage_threshold = Threshold(
        ...     threshold_type=ThresholdType.COVERAGE,
        ...     minimum=80.0
        ... )
        >>> coverage_threshold.evaluate(85.0)
        True
    """

    threshold_type: ThresholdType
    minimum: float | None = None
    maximum: float | None = None

    def __post_init__(self) -> None:
        """Validate threshold bounds."""
        if self.minimum is None and self.maximum is None:
            raise ValueError("At least one of minimum or maximum must be specified")

        if self.threshold_type.is_percentage:
            if self.minimum is not None and self.minimum < 0:
                raise ValueError(f"Percentage minimum cannot be negative: {self.minimum}")
            if self.maximum is not None and self.maximum > 100:
                raise ValueError(f"Percentage maximum cannot exceed 100: {self.maximum}")

        if self.minimum is not None and self.maximum is not None:
            if self.minimum > self.maximum:
                raise ValueError(
                    f"Minimum ({self.minimum}) cannot be greater than maximum ({self.maximum})"
                )

    def evaluate(self, value: float) -> bool:
        """
        Evaluate whether a value meets this threshold.

        Args:
            value: The value to evaluate

        Returns:
            True if the value meets the threshold requirements
        """
        if self.minimum is not None and value < self.minimum:
            return False
        if self.maximum is not None and value > self.maximum:
            return False
        return True

    def __str__(self) -> str:
        """Return readable representation."""
        parts = [f"{self.threshold_type.value}"]
        if self.minimum is not None:
            parts.append(f"min={self.minimum}")
        if self.maximum is not None:
            parts.append(f"max={self.maximum}")
        return f"Threshold({', '.join(parts)})"

    def __repr__(self) -> str:
        """Return detailed representation."""
        return (
            f"Threshold(threshold_type={self.threshold_type!r}, "
            f"minimum={self.minimum!r}, maximum={self.maximum!r})"
        )


@dataclass(frozen=True, slots=True)
class GateCheckDefinition:
    """
    Definition of a single quality check.

    Immutable value object representing a check that can be executed
    as part of a quality gate.

    Attributes:
        check_id: Unique identifier for this check
        name: Human-readable name
        command: Shell command to execute
        threshold: Optional threshold for evaluation
        fix_command: Optional command to auto-fix issues
        auto_fix: Whether to automatically run fix_command on failure
        is_critical: Whether failure of this check should block all progress

    Example:
        >>> check = GateCheckDefinition(
        ...     check_id="format-check",
        ...     name="Code Formatting",
        ...     command="ruff format --check .",
        ...     fix_command="ruff format .",
        ...     auto_fix=True
        ... )
    """

    check_id: str
    name: str
    command: str
    threshold: Threshold | None = None
    fix_command: str | None = None
    auto_fix: bool = False
    is_critical: bool = False

    def __post_init__(self) -> None:
        """Validate check definition."""
        if not self.check_id or not self.check_id.strip():
            raise ValueError("check_id cannot be empty")
        if not self.name or not self.name.strip():
            raise ValueError("name cannot be empty")
        if not self.command or not self.command.strip():
            raise ValueError("command cannot be empty")

    def __str__(self) -> str:
        """Return readable representation."""
        return f"GateCheckDefinition({self.check_id}: {self.name})"

    def __repr__(self) -> str:
        """Return detailed representation."""
        return (
            f"GateCheckDefinition(check_id={self.check_id!r}, name={self.name!r}, "
            f"command={self.command!r}, threshold={self.threshold!r}, "
            f"fix_command={self.fix_command!r}, auto_fix={self.auto_fix!r}, "
            f"is_critical={self.is_critical!r})"
        )
