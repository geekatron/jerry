"""Unit tests for IQualityGateValidator domain service.

Test Categories:
    - Protocol Compliance: Interface adherence
    - Gate Validation: L0/L1/L2 validation logic
    - Risk Assessment: Risk tier determination
    - Completion Check: Can-complete evaluation

References:
    - IMPL-009: Domain Services
    - ADR-008: Quality Gate Layer Configuration
    - PAT-008: Value Object Quality Gates
"""
from __future__ import annotations

import pytest

from src.work_tracking.domain.services.quality_validator import (
    IQualityGateValidator,
    QualityGateValidator,
    ValidationResult,
)
from src.work_tracking.domain.value_objects import (
    GateLevel,
    RiskTier,
    TestCoverage,
    TestRatio,
)


# =============================================================================
# IQualityGateValidator Protocol Tests
# =============================================================================


class TestIQualityGateValidatorProtocol:
    """Tests for IQualityGateValidator protocol compliance."""

    def test_validator_implements_protocol(self) -> None:
        """QualityGateValidator implements IQualityGateValidator."""
        validator = QualityGateValidator()
        assert isinstance(validator, IQualityGateValidator)

    def test_protocol_has_validate_method(self) -> None:
        """Protocol requires validate() method."""
        assert hasattr(IQualityGateValidator, "validate")

    def test_protocol_has_assess_risk_method(self) -> None:
        """Protocol requires assess_risk() method."""
        assert hasattr(IQualityGateValidator, "assess_risk")


# =============================================================================
# ValidationResult Tests
# =============================================================================


class TestValidationResult:
    """Tests for ValidationResult value object."""

    def test_create_passed_result(self) -> None:
        """Create passed validation result."""
        result = ValidationResult(
            gate_level=GateLevel.L1,
            passed=True,
            failures=[],
        )
        assert result.passed is True
        assert len(result.failures) == 0

    def test_create_failed_result(self) -> None:
        """Create failed validation result."""
        result = ValidationResult(
            gate_level=GateLevel.L1,
            passed=False,
            failures=["Coverage below 80%", "No negative tests"],
        )
        assert result.passed is False
        assert len(result.failures) == 2

    def test_result_is_immutable(self) -> None:
        """ValidationResult is immutable."""
        result = ValidationResult(
            gate_level=GateLevel.L0,
            passed=True,
            failures=[],
        )
        with pytest.raises(Exception):  # FrozenInstanceError
            result.passed = False  # type: ignore


# =============================================================================
# Gate Validation Tests - L0
# =============================================================================


class TestL0Validation:
    """Tests for L0 (commit-gate) validation."""

    def test_l0_passes_with_any_tests(self) -> None:
        """L0 passes with any test coverage."""
        validator = QualityGateValidator()
        result = validator.validate(
            gate_level=GateLevel.L0,
            coverage=TestCoverage.from_percent(10),
            ratio=TestRatio(positive=1, negative=0, edge_case=0),
        )
        assert result.passed is True

    def test_l0_fails_without_tests(self) -> None:
        """L0 fails with no tests at all."""
        validator = QualityGateValidator()
        result = validator.validate(
            gate_level=GateLevel.L0,
            coverage=None,
            ratio=None,
        )
        assert result.passed is False
        assert "No tests" in result.failures[0]

    def test_l0_allows_zero_coverage(self) -> None:
        """L0 allows 0% coverage (tests exist but don't cover)."""
        validator = QualityGateValidator()
        result = validator.validate(
            gate_level=GateLevel.L0,
            coverage=TestCoverage.from_percent(0),
            ratio=TestRatio(positive=1, negative=0, edge_case=0),
        )
        assert result.passed is True


# =============================================================================
# Gate Validation Tests - L1
# =============================================================================


class TestL1Validation:
    """Tests for L1 (merge-gate) validation."""

    def test_l1_passes_with_full_requirements(self) -> None:
        """L1 passes with positive, negative tests and 80% coverage."""
        validator = QualityGateValidator()
        result = validator.validate(
            gate_level=GateLevel.L1,
            coverage=TestCoverage.from_percent(80),
            ratio=TestRatio(positive=5, negative=3, edge_case=2),
        )
        assert result.passed is True

    def test_l1_fails_without_negative_tests(self) -> None:
        """L1 fails without negative tests."""
        validator = QualityGateValidator()
        result = validator.validate(
            gate_level=GateLevel.L1,
            coverage=TestCoverage.from_percent(90),
            ratio=TestRatio(positive=10, negative=0, edge_case=5),
        )
        assert result.passed is False
        assert any("negative" in f.lower() for f in result.failures)

    def test_l1_fails_below_80_coverage(self) -> None:
        """L1 fails with coverage below 80%."""
        validator = QualityGateValidator()
        result = validator.validate(
            gate_level=GateLevel.L1,
            coverage=TestCoverage.from_percent(79),
            ratio=TestRatio(positive=5, negative=3, edge_case=2),
        )
        assert result.passed is False
        assert any("80%" in f for f in result.failures)

    def test_l1_fails_without_positive_tests(self) -> None:
        """L1 fails without positive tests."""
        validator = QualityGateValidator()
        result = validator.validate(
            gate_level=GateLevel.L1,
            coverage=TestCoverage.from_percent(85),
            ratio=TestRatio(positive=0, negative=3, edge_case=2),
        )
        assert result.passed is False
        assert any("positive" in f.lower() for f in result.failures)


# =============================================================================
# Gate Validation Tests - L2
# =============================================================================


class TestL2Validation:
    """Tests for L2 (release-gate) validation."""

    def test_l2_passes_with_full_requirements(self) -> None:
        """L2 passes with all test types and 90% coverage."""
        validator = QualityGateValidator()
        result = validator.validate(
            gate_level=GateLevel.L2,
            coverage=TestCoverage.from_percent(90),
            ratio=TestRatio(positive=10, negative=5, edge_case=5),
        )
        assert result.passed is True

    def test_l2_fails_without_edge_cases(self) -> None:
        """L2 fails without edge case tests."""
        validator = QualityGateValidator()
        result = validator.validate(
            gate_level=GateLevel.L2,
            coverage=TestCoverage.from_percent(95),
            ratio=TestRatio(positive=10, negative=5, edge_case=0),
        )
        assert result.passed is False
        assert any("edge" in f.lower() for f in result.failures)

    def test_l2_fails_below_90_coverage(self) -> None:
        """L2 fails with coverage below 90%."""
        validator = QualityGateValidator()
        result = validator.validate(
            gate_level=GateLevel.L2,
            coverage=TestCoverage.from_percent(89),
            ratio=TestRatio(positive=10, negative=5, edge_case=5),
        )
        assert result.passed is False
        assert any("90%" in f for f in result.failures)


# =============================================================================
# Risk Assessment Tests
# =============================================================================


class TestRiskAssessment:
    """Tests for risk tier assessment."""

    def test_assess_risk_tier_1(self) -> None:
        """T1 for docs/config/comments only."""
        validator = QualityGateValidator()
        tier = validator.assess_risk(
            file_patterns=["*.md", "*.yaml"],
            keywords=[],
        )
        assert tier == RiskTier.T1

    def test_assess_risk_tier_2(self) -> None:
        """T2 for test/application changes."""
        validator = QualityGateValidator()
        tier = validator.assess_risk(
            file_patterns=["tests/**/*.py", "src/application/**/*.py"],
            keywords=[],
        )
        assert tier == RiskTier.T2

    def test_assess_risk_tier_3(self) -> None:
        """T3 for domain/infrastructure changes."""
        validator = QualityGateValidator()
        tier = validator.assess_risk(
            file_patterns=["src/domain/**/*.py"],
            keywords=[],
        )
        assert tier == RiskTier.T3

    def test_assess_risk_tier_4(self) -> None:
        """T4 for security/breaking changes."""
        validator = QualityGateValidator()
        tier = validator.assess_risk(
            file_patterns=["src/security/**/*.py"],
            keywords=["BREAKING"],
        )
        assert tier == RiskTier.T4

    def test_keyword_elevates_risk(self) -> None:
        """Keywords can elevate risk tier."""
        validator = QualityGateValidator()
        tier = validator.assess_risk(
            file_patterns=["*.md"],  # Would be T1
            keywords=["MIGRATION"],  # Elevates to T4
        )
        assert tier == RiskTier.T4


# =============================================================================
# Edge Cases
# =============================================================================


class TestValidationEdgeCases:
    """Edge case tests for validation."""

    def test_validate_with_no_metrics(self) -> None:
        """Validate with no metrics provided."""
        validator = QualityGateValidator()
        result = validator.validate(
            gate_level=GateLevel.L1,
            coverage=None,
            ratio=None,
        )
        assert result.passed is False

    def test_validate_with_only_coverage(self) -> None:
        """Validate with only coverage, no ratio."""
        validator = QualityGateValidator()
        result = validator.validate(
            gate_level=GateLevel.L1,
            coverage=TestCoverage.from_percent(90),
            ratio=None,
        )
        assert result.passed is False
        assert any("ratio" in f.lower() for f in result.failures)

    def test_assess_risk_empty_patterns(self) -> None:
        """Assess risk with no file patterns."""
        validator = QualityGateValidator()
        tier = validator.assess_risk(
            file_patterns=[],
            keywords=[],
        )
        assert tier == RiskTier.T1  # Default to lowest risk

    def test_multiple_failure_reasons(self) -> None:
        """Can have multiple failure reasons."""
        validator = QualityGateValidator()
        result = validator.validate(
            gate_level=GateLevel.L2,
            coverage=TestCoverage.from_percent(50),  # Fails 90%
            ratio=TestRatio(positive=5, negative=0, edge_case=0),  # Fails negative + edge
        )
        assert result.passed is False
        assert len(result.failures) >= 2
