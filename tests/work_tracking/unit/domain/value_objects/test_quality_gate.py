# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for QualityGate value objects.

Test Categories:
    - GateLevel: Gate level enumeration (L0/L1/L2)
    - RiskTier: Risk classification (T1-T4)
    - GateResult: Gate execution result states
    - Threshold: Numeric threshold with validation
    - GateCheckDefinition: Individual check definition

References:
    - IMPL-006: QualityGate Entity
    - ADR-008: Quality Gate Layer Configuration
    - dev-skill-e-002: Quality Gate Enforcement patterns
"""

from __future__ import annotations

import pytest

from src.work_tracking.domain.value_objects.quality_gate import (
    GateCheckDefinition,
    GateLevel,
    GateResult,
    RiskTier,
    Threshold,
    ThresholdType,
)

# =============================================================================
# GateLevel Tests
# =============================================================================


class TestGateLevelValues:
    """Tests for GateLevel enum values."""

    def test_l0_value(self) -> None:
        """L0 has correct value."""
        assert GateLevel.L0.value == "L0"

    def test_l1_value(self) -> None:
        """L1 has correct value."""
        assert GateLevel.L1.value == "L1"

    def test_l2_value(self) -> None:
        """L2 has correct value."""
        assert GateLevel.L2.value == "L2"

    def test_has_three_levels(self) -> None:
        """There are exactly 3 gate levels."""
        assert len(GateLevel) == 3


class TestGateLevelOrdering:
    """Tests for GateLevel ordering (lower value = earlier execution)."""

    def test_l0_less_than_l1(self) -> None:
        """L0 executes before L1."""
        assert GateLevel.L0.order < GateLevel.L1.order

    def test_l1_less_than_l2(self) -> None:
        """L1 executes before L2."""
        assert GateLevel.L1.order < GateLevel.L2.order

    def test_sorting(self) -> None:
        """Gate levels sort by execution order."""
        levels = [GateLevel.L2, GateLevel.L0, GateLevel.L1]
        sorted_levels = sorted(levels, key=lambda x: x.order)
        assert sorted_levels == [GateLevel.L0, GateLevel.L1, GateLevel.L2]


class TestGateLevelProperties:
    """Tests for GateLevel properties."""

    def test_l0_name(self) -> None:
        """L0 has correct display name."""
        assert GateLevel.L0.display_name == "Syntax & Basic"

    def test_l1_name(self) -> None:
        """L1 has correct display name."""
        assert GateLevel.L1.display_name == "Semantic & Quality"

    def test_l2_name(self) -> None:
        """L2 has correct display name."""
        assert GateLevel.L2.display_name == "Distinguished Review"

    def test_l0_is_mandatory(self) -> None:
        """L0 is mandatory."""
        assert GateLevel.L0.is_mandatory is True

    def test_l1_is_mandatory(self) -> None:
        """L1 is mandatory."""
        assert GateLevel.L1.is_mandatory is True

    def test_l2_is_not_mandatory(self) -> None:
        """L2 is not mandatory by default."""
        assert GateLevel.L2.is_mandatory is False

    def test_l0_timeout(self) -> None:
        """L0 has 60 second timeout."""
        assert GateLevel.L0.default_timeout_seconds == 60

    def test_l1_timeout(self) -> None:
        """L1 has 300 second timeout."""
        assert GateLevel.L1.default_timeout_seconds == 300

    def test_l2_timeout(self) -> None:
        """L2 has 600 second timeout."""
        assert GateLevel.L2.default_timeout_seconds == 600


class TestGateLevelFromString:
    """Tests for GateLevel.from_string() factory method."""

    def test_parse_l0(self) -> None:
        """Parse 'L0' string."""
        assert GateLevel.from_string("L0") == GateLevel.L0

    def test_parse_l1(self) -> None:
        """Parse 'L1' string."""
        assert GateLevel.from_string("L1") == GateLevel.L1

    def test_parse_l2(self) -> None:
        """Parse 'L2' string."""
        assert GateLevel.from_string("L2") == GateLevel.L2

    def test_parse_lowercase(self) -> None:
        """Parse lowercase strings."""
        assert GateLevel.from_string("l0") == GateLevel.L0
        assert GateLevel.from_string("l1") == GateLevel.L1

    def test_parse_with_whitespace(self) -> None:
        """Parse strings with whitespace."""
        assert GateLevel.from_string("  L0  ") == GateLevel.L0

    def test_invalid_raises(self) -> None:
        """Invalid string raises ValueError."""
        with pytest.raises(ValueError, match="Invalid gate level"):
            GateLevel.from_string("L3")

    def test_empty_raises(self) -> None:
        """Empty string raises ValueError."""
        with pytest.raises(ValueError, match="Invalid gate level"):
            GateLevel.from_string("")


# =============================================================================
# RiskTier Tests
# =============================================================================


class TestRiskTierValues:
    """Tests for RiskTier enum values."""

    def test_t1_value(self) -> None:
        """T1 has correct value."""
        assert RiskTier.T1.value == 1

    def test_t2_value(self) -> None:
        """T2 has correct value."""
        assert RiskTier.T2.value == 2

    def test_t3_value(self) -> None:
        """T3 has correct value."""
        assert RiskTier.T3.value == 3

    def test_t4_value(self) -> None:
        """T4 has correct value."""
        assert RiskTier.T4.value == 4

    def test_has_four_tiers(self) -> None:
        """There are exactly 4 risk tiers."""
        assert len(RiskTier) == 4


class TestRiskTierOrdering:
    """Tests for RiskTier ordering (higher value = higher risk)."""

    def test_t1_less_than_t2(self) -> None:
        """T1 < T2 (lower risk)."""
        assert RiskTier.T1 < RiskTier.T2

    def test_t2_less_than_t3(self) -> None:
        """T2 < T3."""
        assert RiskTier.T2 < RiskTier.T3

    def test_t3_less_than_t4(self) -> None:
        """T3 < T4."""
        assert RiskTier.T3 < RiskTier.T4

    def test_sorting(self) -> None:
        """Risk tiers sort by risk level."""
        tiers = [RiskTier.T4, RiskTier.T1, RiskTier.T3, RiskTier.T2]
        sorted_tiers = sorted(tiers)
        assert sorted_tiers == [RiskTier.T1, RiskTier.T2, RiskTier.T3, RiskTier.T4]


class TestRiskTierProperties:
    """Tests for RiskTier properties."""

    def test_t1_description(self) -> None:
        """T1 has correct description."""
        assert RiskTier.T1.description == "Low Risk"

    def test_t2_description(self) -> None:
        """T2 has correct description."""
        assert RiskTier.T2.description == "Medium Risk"

    def test_t3_description(self) -> None:
        """T3 has correct description."""
        assert RiskTier.T3.description == "High Risk"

    def test_t4_description(self) -> None:
        """T4 has correct description."""
        assert RiskTier.T4.description == "Critical Risk"

    def test_t1_requires_l2(self) -> None:
        """T1 does not require L2."""
        assert RiskTier.T1.requires_l2 is False

    def test_t2_requires_l2(self) -> None:
        """T2 does not require L2."""
        assert RiskTier.T2.requires_l2 is False

    def test_t3_requires_l2(self) -> None:
        """T3 requires L2."""
        assert RiskTier.T3.requires_l2 is True

    def test_t4_requires_l2(self) -> None:
        """T4 requires L2."""
        assert RiskTier.T4.requires_l2 is True

    def test_t4_requires_human_approval(self) -> None:
        """T4 requires human approval."""
        assert RiskTier.T4.requires_human_approval is True

    def test_t3_no_human_approval(self) -> None:
        """T3 does not require human approval."""
        assert RiskTier.T3.requires_human_approval is False


class TestRiskTierGateLevels:
    """Tests for RiskTier.required_gate_levels()."""

    def test_t1_levels(self) -> None:
        """T1 requires L0 and L1."""
        levels = RiskTier.T1.required_gate_levels()
        assert levels == [GateLevel.L0, GateLevel.L1]

    def test_t2_levels(self) -> None:
        """T2 requires L0 and L1."""
        levels = RiskTier.T2.required_gate_levels()
        assert levels == [GateLevel.L0, GateLevel.L1]

    def test_t3_levels(self) -> None:
        """T3 requires L0, L1, and L2."""
        levels = RiskTier.T3.required_gate_levels()
        assert levels == [GateLevel.L0, GateLevel.L1, GateLevel.L2]

    def test_t4_levels(self) -> None:
        """T4 requires L0, L1, and L2."""
        levels = RiskTier.T4.required_gate_levels()
        assert levels == [GateLevel.L0, GateLevel.L1, GateLevel.L2]


class TestRiskTierFromString:
    """Tests for RiskTier.from_string() factory method."""

    def test_parse_t1(self) -> None:
        """Parse 'T1' string."""
        assert RiskTier.from_string("T1") == RiskTier.T1

    def test_parse_lowercase(self) -> None:
        """Parse lowercase strings."""
        assert RiskTier.from_string("t4") == RiskTier.T4

    def test_parse_with_whitespace(self) -> None:
        """Parse strings with whitespace."""
        assert RiskTier.from_string("  T2  ") == RiskTier.T2

    def test_invalid_raises(self) -> None:
        """Invalid string raises ValueError."""
        with pytest.raises(ValueError, match="Invalid risk tier"):
            RiskTier.from_string("T5")


# =============================================================================
# GateResult Tests
# =============================================================================


class TestGateResultValues:
    """Tests for GateResult enum values."""

    def test_pending_value(self) -> None:
        """PENDING has correct value."""
        assert GateResult.PENDING.value == "pending"

    def test_passed_value(self) -> None:
        """PASSED has correct value."""
        assert GateResult.PASSED.value == "passed"

    def test_failed_value(self) -> None:
        """FAILED has correct value."""
        assert GateResult.FAILED.value == "failed"

    def test_skipped_value(self) -> None:
        """SKIPPED has correct value."""
        assert GateResult.SKIPPED.value == "skipped"

    def test_has_four_results(self) -> None:
        """There are exactly 4 result states."""
        assert len(GateResult) == 4


class TestGateResultProperties:
    """Tests for GateResult properties."""

    def test_pending_is_terminal(self) -> None:
        """PENDING is not terminal."""
        assert GateResult.PENDING.is_terminal is False

    def test_passed_is_terminal(self) -> None:
        """PASSED is terminal."""
        assert GateResult.PASSED.is_terminal is True

    def test_failed_is_terminal(self) -> None:
        """FAILED is terminal."""
        assert GateResult.FAILED.is_terminal is True

    def test_skipped_is_terminal(self) -> None:
        """SKIPPED is terminal."""
        assert GateResult.SKIPPED.is_terminal is True

    def test_passed_is_success(self) -> None:
        """PASSED is success."""
        assert GateResult.PASSED.is_success is True

    def test_failed_is_not_success(self) -> None:
        """FAILED is not success."""
        assert GateResult.FAILED.is_success is False

    def test_skipped_is_not_success(self) -> None:
        """SKIPPED is not considered success."""
        assert GateResult.SKIPPED.is_success is False

    def test_pending_is_not_success(self) -> None:
        """PENDING is not success."""
        assert GateResult.PENDING.is_success is False


class TestGateResultFromString:
    """Tests for GateResult.from_string() factory method."""

    def test_parse_passed(self) -> None:
        """Parse 'passed' string."""
        assert GateResult.from_string("passed") == GateResult.PASSED

    def test_parse_uppercase(self) -> None:
        """Parse uppercase strings."""
        assert GateResult.from_string("FAILED") == GateResult.FAILED

    def test_parse_mixed_case(self) -> None:
        """Parse mixed case strings."""
        assert GateResult.from_string("Skipped") == GateResult.SKIPPED

    def test_invalid_raises(self) -> None:
        """Invalid string raises ValueError."""
        with pytest.raises(ValueError, match="Invalid gate result"):
            GateResult.from_string("unknown")


# =============================================================================
# ThresholdType Tests
# =============================================================================


class TestThresholdTypeValues:
    """Tests for ThresholdType enum values."""

    def test_coverage_value(self) -> None:
        """COVERAGE has correct value."""
        assert ThresholdType.COVERAGE.value == "coverage"

    def test_complexity_value(self) -> None:
        """COMPLEXITY has correct value."""
        assert ThresholdType.COMPLEXITY.value == "complexity"

    def test_duplication_value(self) -> None:
        """DUPLICATION has correct value."""
        assert ThresholdType.DUPLICATION.value == "duplication"

    def test_has_expected_types(self) -> None:
        """There are at least 3 threshold types."""
        assert len(ThresholdType) >= 3


class TestThresholdTypeProperties:
    """Tests for ThresholdType properties."""

    def test_coverage_is_percentage(self) -> None:
        """COVERAGE is a percentage type."""
        assert ThresholdType.COVERAGE.is_percentage is True

    def test_complexity_is_not_percentage(self) -> None:
        """COMPLEXITY is not a percentage type."""
        assert ThresholdType.COMPLEXITY.is_percentage is False

    def test_coverage_higher_is_better(self) -> None:
        """For COVERAGE, higher values are better."""
        assert ThresholdType.COVERAGE.higher_is_better is True

    def test_complexity_lower_is_better(self) -> None:
        """For COMPLEXITY, lower values are better."""
        assert ThresholdType.COMPLEXITY.higher_is_better is False


# =============================================================================
# Threshold Tests
# =============================================================================


class TestThresholdCreation:
    """Tests for Threshold creation."""

    def test_create_coverage_threshold(self) -> None:
        """Create a coverage threshold."""
        threshold = Threshold(
            threshold_type=ThresholdType.COVERAGE,
            minimum=80.0,
        )
        assert threshold.threshold_type == ThresholdType.COVERAGE
        assert threshold.minimum == 80.0

    def test_create_complexity_threshold(self) -> None:
        """Create a complexity threshold with maximum."""
        threshold = Threshold(
            threshold_type=ThresholdType.COMPLEXITY,
            maximum=10,
        )
        assert threshold.threshold_type == ThresholdType.COMPLEXITY
        assert threshold.maximum == 10

    def test_create_with_min_and_max(self) -> None:
        """Create threshold with both minimum and maximum."""
        threshold = Threshold(
            threshold_type=ThresholdType.COVERAGE,
            minimum=70.0,
            maximum=100.0,
        )
        assert threshold.minimum == 70.0
        assert threshold.maximum == 100.0


class TestThresholdValidation:
    """Tests for Threshold validation."""

    def test_percentage_minimum_capped_at_0(self) -> None:
        """Percentage minimum cannot be negative."""
        with pytest.raises(ValueError, match="cannot be negative"):
            Threshold(threshold_type=ThresholdType.COVERAGE, minimum=-1.0)

    def test_percentage_maximum_capped_at_100(self) -> None:
        """Percentage maximum cannot exceed 100."""
        with pytest.raises(ValueError, match="cannot exceed 100"):
            Threshold(threshold_type=ThresholdType.COVERAGE, maximum=101.0)

    def test_minimum_greater_than_maximum_raises(self) -> None:
        """Minimum cannot be greater than maximum."""
        with pytest.raises(ValueError, match="cannot be greater than maximum"):
            Threshold(
                threshold_type=ThresholdType.COMPLEXITY,
                minimum=20,
                maximum=10,
            )

    def test_no_bounds_raises(self) -> None:
        """At least one bound must be specified."""
        with pytest.raises(ValueError, match="At least one of minimum or maximum"):
            Threshold(threshold_type=ThresholdType.COVERAGE)


class TestThresholdEvaluation:
    """Tests for Threshold.evaluate() method."""

    def test_coverage_above_minimum_passes(self) -> None:
        """Coverage above minimum passes."""
        threshold = Threshold(threshold_type=ThresholdType.COVERAGE, minimum=80.0)
        assert threshold.evaluate(85.0) is True

    def test_coverage_at_minimum_passes(self) -> None:
        """Coverage at exactly minimum passes."""
        threshold = Threshold(threshold_type=ThresholdType.COVERAGE, minimum=80.0)
        assert threshold.evaluate(80.0) is True

    def test_coverage_below_minimum_fails(self) -> None:
        """Coverage below minimum fails."""
        threshold = Threshold(threshold_type=ThresholdType.COVERAGE, minimum=80.0)
        assert threshold.evaluate(79.9) is False

    def test_complexity_below_maximum_passes(self) -> None:
        """Complexity below maximum passes."""
        threshold = Threshold(threshold_type=ThresholdType.COMPLEXITY, maximum=10)
        assert threshold.evaluate(8) is True

    def test_complexity_at_maximum_passes(self) -> None:
        """Complexity at exactly maximum passes."""
        threshold = Threshold(threshold_type=ThresholdType.COMPLEXITY, maximum=10)
        assert threshold.evaluate(10) is True

    def test_complexity_above_maximum_fails(self) -> None:
        """Complexity above maximum fails."""
        threshold = Threshold(threshold_type=ThresholdType.COMPLEXITY, maximum=10)
        assert threshold.evaluate(11) is False


class TestThresholdEdgeCases:
    """Edge case tests for Threshold."""

    def test_immutable(self) -> None:
        """Threshold is immutable."""
        threshold = Threshold(threshold_type=ThresholdType.COVERAGE, minimum=80.0)
        with pytest.raises(Exception):  # FrozenInstanceError
            threshold.minimum = 90.0  # type: ignore

    def test_hashable(self) -> None:
        """Threshold can be used in sets."""
        t1 = Threshold(threshold_type=ThresholdType.COVERAGE, minimum=80.0)
        t2 = Threshold(threshold_type=ThresholdType.COVERAGE, minimum=80.0)
        t3 = Threshold(threshold_type=ThresholdType.COVERAGE, minimum=90.0)
        threshold_set = {t1, t2, t3}
        assert len(threshold_set) == 2


class TestThresholdStringRepresentation:
    """Tests for Threshold string representations."""

    def test_str_minimum_only(self) -> None:
        """str() with minimum only."""
        threshold = Threshold(threshold_type=ThresholdType.COVERAGE, minimum=80.0)
        assert "coverage" in str(threshold).lower()
        assert "80" in str(threshold)

    def test_repr(self) -> None:
        """repr includes class name."""
        threshold = Threshold(threshold_type=ThresholdType.COVERAGE, minimum=80.0)
        assert "Threshold" in repr(threshold)


# =============================================================================
# GateCheckDefinition Tests
# =============================================================================


class TestGateCheckDefinitionCreation:
    """Tests for GateCheckDefinition creation."""

    def test_create_basic_check(self) -> None:
        """Create a basic check definition."""
        check = GateCheckDefinition(
            check_id="format-check",
            name="Code Formatting",
            command="ruff format --check .",
        )
        assert check.check_id == "format-check"
        assert check.name == "Code Formatting"
        assert check.command == "ruff format --check ."

    def test_create_with_threshold(self) -> None:
        """Create check with threshold."""
        check = GateCheckDefinition(
            check_id="coverage-check",
            name="Test Coverage",
            command="pytest --cov",
            threshold=Threshold(threshold_type=ThresholdType.COVERAGE, minimum=80.0),
        )
        assert check.threshold is not None
        assert check.threshold.minimum == 80.0

    def test_create_with_fix_command(self) -> None:
        """Create check with fix command."""
        check = GateCheckDefinition(
            check_id="format-check",
            name="Code Formatting",
            command="ruff format --check .",
            fix_command="ruff format .",
            auto_fix=True,
        )
        assert check.fix_command == "ruff format ."
        assert check.auto_fix is True

    def test_create_critical_check(self) -> None:
        """Create a critical check."""
        check = GateCheckDefinition(
            check_id="secret-scan",
            name="Secrets Detection",
            command="detect-secrets scan",
            is_critical=True,
        )
        assert check.is_critical is True


class TestGateCheckDefinitionValidation:
    """Tests for GateCheckDefinition validation."""

    def test_empty_check_id_raises(self) -> None:
        """Empty check_id raises ValueError."""
        with pytest.raises(ValueError, match="check_id cannot be empty"):
            GateCheckDefinition(check_id="", name="Test", command="test")

    def test_empty_name_raises(self) -> None:
        """Empty name raises ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            GateCheckDefinition(check_id="test", name="", command="test")

    def test_empty_command_raises(self) -> None:
        """Empty command raises ValueError."""
        with pytest.raises(ValueError, match="command cannot be empty"):
            GateCheckDefinition(check_id="test", name="Test", command="")


class TestGateCheckDefinitionDefaults:
    """Tests for GateCheckDefinition default values."""

    def test_default_threshold_is_none(self) -> None:
        """Default threshold is None."""
        check = GateCheckDefinition(check_id="test", name="Test", command="test")
        assert check.threshold is None

    def test_default_fix_command_is_none(self) -> None:
        """Default fix_command is None."""
        check = GateCheckDefinition(check_id="test", name="Test", command="test")
        assert check.fix_command is None

    def test_default_auto_fix_is_false(self) -> None:
        """Default auto_fix is False."""
        check = GateCheckDefinition(check_id="test", name="Test", command="test")
        assert check.auto_fix is False

    def test_default_is_critical_is_false(self) -> None:
        """Default is_critical is False."""
        check = GateCheckDefinition(check_id="test", name="Test", command="test")
        assert check.is_critical is False


class TestGateCheckDefinitionEdgeCases:
    """Edge case tests for GateCheckDefinition."""

    def test_immutable(self) -> None:
        """GateCheckDefinition is immutable."""
        check = GateCheckDefinition(check_id="test", name="Test", command="test")
        with pytest.raises(Exception):  # FrozenInstanceError
            check.name = "Changed"  # type: ignore

    def test_hashable(self) -> None:
        """GateCheckDefinition can be used in sets."""
        c1 = GateCheckDefinition(check_id="a", name="A", command="a")
        c2 = GateCheckDefinition(check_id="a", name="A", command="a")
        c3 = GateCheckDefinition(check_id="b", name="B", command="b")
        check_set = {c1, c2, c3}
        assert len(check_set) == 2

    def test_equality(self) -> None:
        """GateCheckDefinition equality based on all fields."""
        c1 = GateCheckDefinition(check_id="a", name="A", command="a")
        c2 = GateCheckDefinition(check_id="a", name="A", command="a")
        assert c1 == c2


class TestGateCheckDefinitionStringRepresentation:
    """Tests for GateCheckDefinition string representations."""

    def test_str(self) -> None:
        """str() returns readable representation."""
        check = GateCheckDefinition(
            check_id="format-check",
            name="Code Formatting",
            command="ruff format --check .",
        )
        result = str(check)
        assert "format-check" in result or "Code Formatting" in result

    def test_repr(self) -> None:
        """repr includes class name."""
        check = GateCheckDefinition(check_id="test", name="Test", command="test")
        assert "GateCheckDefinition" in repr(check)
