"""Unit tests for QualityGate domain events.

Test Categories:
    - Event Creation: Each event type creates correctly
    - Serialization: to_dict and from_dict work correctly
    - Payload: _payload returns event-specific data

References:
    - IMPL-007: Domain Events (additional)
    - ADR-008: Quality Gate Layer Configuration
    - ADR-009: Event Storage Mechanism
"""

from __future__ import annotations

from datetime import datetime

import pytest

from src.work_tracking.domain.events.quality_gate_events import (
    GateCheckCompleted,
    GateExecutionCompleted,
    GateExecutionStarted,
    RiskAssessed,
    ThresholdViolation,
)

# =============================================================================
# GateExecutionStarted Tests
# =============================================================================


class TestGateExecutionStarted:
    """Tests for GateExecutionStarted event."""

    def test_create_with_required_fields(self) -> None:
        """Create event with required fields."""
        event = GateExecutionStarted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            gate_level="L0",
            risk_tier="T2",
        )
        assert event.aggregate_id == "exec-123"
        assert event.gate_level == "L0"
        assert event.risk_tier == "T2"

    def test_create_with_checks(self) -> None:
        """Create event with check list."""
        event = GateExecutionStarted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            gate_level="L1",
            risk_tier="T3",
            check_ids=("format-check", "lint-check", "test-run"),
        )
        assert event.check_ids == ("format-check", "lint-check", "test-run")

    def test_payload_includes_all_fields(self) -> None:
        """Payload includes all event-specific fields."""
        event = GateExecutionStarted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            gate_level="L2",
            risk_tier="T4",
            check_ids=("adr-check", "agent-review"),
            timeout_seconds=600,
        )
        payload = event._payload()

        assert payload["gate_level"] == "L2"
        assert payload["risk_tier"] == "T4"
        assert payload["check_ids"] == ["adr-check", "agent-review"]
        assert payload["timeout_seconds"] == 600

    def test_to_dict_includes_event_type(self) -> None:
        """to_dict includes event_type for deserialization."""
        event = GateExecutionStarted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            gate_level="L0",
            risk_tier="T1",
        )
        data = event.to_dict()

        assert data["event_type"] == "GateExecutionStarted"
        assert data["aggregate_id"] == "exec-123"

    def test_from_dict_restores_event(self) -> None:
        """from_dict restores event from dictionary."""
        original = GateExecutionStarted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            gate_level="L1",
            risk_tier="T2",
            check_ids=("check-a", "check-b"),
            timeout_seconds=300,
        )
        data = original.to_dict()
        restored = GateExecutionStarted.from_dict(data)

        assert restored.aggregate_id == original.aggregate_id
        assert restored.gate_level == original.gate_level
        assert restored.risk_tier == original.risk_tier
        assert restored.check_ids == original.check_ids
        assert restored.timeout_seconds == original.timeout_seconds

    def test_default_values(self) -> None:
        """Default values are set correctly."""
        event = GateExecutionStarted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
        )
        assert event.gate_level == "L0"
        assert event.risk_tier == "T1"
        assert event.check_ids == ()
        assert event.timeout_seconds == 60


# =============================================================================
# GateCheckCompleted Tests
# =============================================================================


class TestGateCheckCompleted:
    """Tests for GateCheckCompleted event."""

    def test_create_passed_check(self) -> None:
        """Create event for passed check."""
        event = GateCheckCompleted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            check_id="format-check",
            check_name="Code Formatting",
            passed=True,
            duration_ms=1234,
        )
        assert event.check_id == "format-check"
        assert event.passed is True
        assert event.duration_ms == 1234

    def test_create_failed_check(self) -> None:
        """Create event for failed check with output."""
        event = GateCheckCompleted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            check_id="coverage-check",
            check_name="Test Coverage",
            passed=False,
            duration_ms=5000,
            output_summary="Coverage 72% is below 80% threshold",
            violations=("coverage: 72% < 80%",),
        )
        assert event.passed is False
        assert event.output_summary == "Coverage 72% is below 80% threshold"
        assert event.violations == ("coverage: 72% < 80%",)

    def test_payload_includes_all_fields(self) -> None:
        """Payload includes all event-specific fields."""
        event = GateCheckCompleted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            check_id="test-run",
            check_name="Test Suite",
            passed=True,
            duration_ms=45000,
            output_summary="All 100 tests passed",
            artifact_path=".jerry/evidence/test-run-123.xml",
        )
        payload = event._payload()

        assert payload["check_id"] == "test-run"
        assert payload["check_name"] == "Test Suite"
        assert payload["passed"] is True
        assert payload["duration_ms"] == 45000
        assert payload["output_summary"] == "All 100 tests passed"
        assert payload["artifact_path"] == ".jerry/evidence/test-run-123.xml"

    def test_from_dict_restores_event(self) -> None:
        """from_dict restores event correctly."""
        original = GateCheckCompleted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            check_id="lint-check",
            check_name="Linting",
            passed=False,
            duration_ms=2000,
            violations=("E501: line too long", "W503: line break"),
        )
        data = original.to_dict()
        restored = GateCheckCompleted.from_dict(data)

        assert restored.check_id == original.check_id
        assert restored.passed == original.passed
        assert restored.violations == original.violations

    def test_default_values(self) -> None:
        """Default values are set correctly."""
        event = GateCheckCompleted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
        )
        assert event.check_id == ""
        assert event.check_name == ""
        assert event.passed is False
        assert event.duration_ms == 0
        assert event.output_summary is None
        assert event.violations == ()
        assert event.artifact_path is None


# =============================================================================
# GateExecutionCompleted Tests
# =============================================================================


class TestGateExecutionCompleted:
    """Tests for GateExecutionCompleted event."""

    def test_create_passed_execution(self) -> None:
        """Create event for passed gate execution."""
        event = GateExecutionCompleted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            gate_level="L1",
            result="passed",
            total_duration_ms=60000,
            checks_passed=5,
            checks_failed=0,
        )
        assert event.result == "passed"
        assert event.checks_passed == 5
        assert event.checks_failed == 0

    def test_create_failed_execution(self) -> None:
        """Create event for failed gate execution."""
        event = GateExecutionCompleted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            gate_level="L0",
            result="failed",
            total_duration_ms=30000,
            checks_passed=3,
            checks_failed=2,
            failed_check_ids=("secret-scan", "merge-conflict"),
        )
        assert event.result == "failed"
        assert event.failed_check_ids == ("secret-scan", "merge-conflict")

    def test_payload_includes_all_fields(self) -> None:
        """Payload includes all event-specific fields."""
        event = GateExecutionCompleted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            gate_level="L2",
            result="passed",
            total_duration_ms=120000,
            checks_passed=4,
            checks_failed=0,
            evidence_path=".jerry/evidence/L2-exec-123.json",
        )
        payload = event._payload()

        assert payload["gate_level"] == "L2"
        assert payload["result"] == "passed"
        assert payload["total_duration_ms"] == 120000
        assert payload["checks_passed"] == 4
        assert payload["checks_failed"] == 0
        assert payload["evidence_path"] == ".jerry/evidence/L2-exec-123.json"

    def test_from_dict_restores_event(self) -> None:
        """from_dict restores event correctly."""
        original = GateExecutionCompleted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            gate_level="L1",
            result="failed",
            total_duration_ms=45000,
            checks_passed=3,
            checks_failed=1,
            failed_check_ids=("coverage-check",),
        )
        data = original.to_dict()
        restored = GateExecutionCompleted.from_dict(data)

        assert restored.gate_level == original.gate_level
        assert restored.result == original.result
        assert restored.checks_passed == original.checks_passed
        assert restored.failed_check_ids == original.failed_check_ids

    def test_default_values(self) -> None:
        """Default values are set correctly."""
        event = GateExecutionCompleted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
        )
        assert event.gate_level == "L0"
        assert event.result == "pending"
        assert event.total_duration_ms == 0
        assert event.checks_passed == 0
        assert event.checks_failed == 0
        assert event.failed_check_ids == ()
        assert event.evidence_path is None


# =============================================================================
# RiskAssessed Tests
# =============================================================================


class TestRiskAssessed:
    """Tests for RiskAssessed event."""

    def test_create_with_classification(self) -> None:
        """Create event with risk classification."""
        event = RiskAssessed(
            aggregate_id="change-123",
            aggregate_type="ChangeSet",
            risk_tier="T3",
            file_count=15,
            matched_patterns=("src/domain/**", "src/ports/**"),
        )
        assert event.risk_tier == "T3"
        assert event.file_count == 15
        assert event.matched_patterns == ("src/domain/**", "src/ports/**")

    def test_payload_includes_all_fields(self) -> None:
        """Payload includes all event-specific fields."""
        event = RiskAssessed(
            aggregate_id="change-123",
            aggregate_type="ChangeSet",
            risk_tier="T4",
            file_count=5,
            matched_patterns=("**/security/**",),
            matched_keywords=("BREAKING", "MIGRATION"),
            requires_human_approval=True,
        )
        payload = event._payload()

        assert payload["risk_tier"] == "T4"
        assert payload["file_count"] == 5
        assert payload["matched_patterns"] == ["**/security/**"]
        assert payload["matched_keywords"] == ["BREAKING", "MIGRATION"]
        assert payload["requires_human_approval"] is True

    def test_from_dict_restores_event(self) -> None:
        """from_dict restores event correctly."""
        original = RiskAssessed(
            aggregate_id="change-123",
            aggregate_type="ChangeSet",
            risk_tier="T2",
            file_count=8,
            matched_patterns=("src/application/**",),
        )
        data = original.to_dict()
        restored = RiskAssessed.from_dict(data)

        assert restored.risk_tier == original.risk_tier
        assert restored.file_count == original.file_count
        assert restored.matched_patterns == original.matched_patterns

    def test_default_values(self) -> None:
        """Default values are set correctly."""
        event = RiskAssessed(
            aggregate_id="change-123",
            aggregate_type="ChangeSet",
        )
        assert event.risk_tier == "T1"
        assert event.file_count == 0
        assert event.matched_patterns == ()
        assert event.matched_keywords == ()
        assert event.requires_human_approval is False


# =============================================================================
# ThresholdViolation Tests
# =============================================================================


class TestThresholdViolation:
    """Tests for ThresholdViolation event."""

    def test_create_coverage_violation(self) -> None:
        """Create event for coverage violation."""
        event = ThresholdViolation(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            check_id="coverage-check",
            threshold_type="coverage",
            threshold_value=80.0,
            actual_value=72.5,
        )
        assert event.threshold_type == "coverage"
        assert event.threshold_value == 80.0
        assert event.actual_value == 72.5

    def test_create_complexity_violation(self) -> None:
        """Create event for complexity violation."""
        event = ThresholdViolation(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            check_id="complexity-check",
            threshold_type="complexity",
            threshold_value=10,
            actual_value=15,
            is_maximum=True,
        )
        assert event.threshold_type == "complexity"
        assert event.is_maximum is True

    def test_payload_includes_all_fields(self) -> None:
        """Payload includes all event-specific fields."""
        event = ThresholdViolation(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            check_id="duplication-check",
            threshold_type="duplication",
            threshold_value=3.0,
            actual_value=5.5,
            is_maximum=True,
            location="src/module/file.py",
        )
        payload = event._payload()

        assert payload["check_id"] == "duplication-check"
        assert payload["threshold_type"] == "duplication"
        assert payload["threshold_value"] == 3.0
        assert payload["actual_value"] == 5.5
        assert payload["is_maximum"] is True
        assert payload["location"] == "src/module/file.py"

    def test_from_dict_restores_event(self) -> None:
        """from_dict restores event correctly."""
        original = ThresholdViolation(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            check_id="mutation-check",
            threshold_type="mutation",
            threshold_value=85.0,
            actual_value=78.0,
            is_maximum=False,
        )
        data = original.to_dict()
        restored = ThresholdViolation.from_dict(data)

        assert restored.threshold_type == original.threshold_type
        assert restored.threshold_value == original.threshold_value
        assert restored.actual_value == original.actual_value

    def test_default_values(self) -> None:
        """Default values are set correctly."""
        event = ThresholdViolation(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
        )
        assert event.check_id == ""
        assert event.threshold_type == ""
        assert event.threshold_value == 0.0
        assert event.actual_value == 0.0
        assert event.is_maximum is False
        assert event.location is None


# =============================================================================
# Event Base Class Integration Tests
# =============================================================================


class TestQualityGateEventBaseIntegration:
    """Tests for DomainEvent base class integration."""

    def test_event_has_event_id(self) -> None:
        """All events have auto-generated event_id."""
        event = GateExecutionStarted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
        )
        assert event.event_id is not None
        assert len(event.event_id) > 0

    def test_event_has_timestamp(self) -> None:
        """All events have timestamp."""
        event = GateCheckCompleted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            check_id="test",
            check_name="Test",
        )
        assert event.timestamp is not None
        assert isinstance(event.timestamp, datetime)

    def test_event_has_version(self) -> None:
        """All events have version number."""
        event = GateExecutionCompleted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
            version=5,
        )
        assert event.version == 5

    def test_events_are_immutable(self) -> None:
        """Events are frozen dataclasses."""
        event = RiskAssessed(
            aggregate_id="change-123",
            aggregate_type="ChangeSet",
            risk_tier="T2",
        )
        with pytest.raises(Exception):  # FrozenInstanceError
            event.risk_tier = "T3"  # type: ignore

    def test_events_are_hashable(self) -> None:
        """Events can be used in sets."""
        event1 = GateExecutionStarted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
        )
        event2 = GateCheckCompleted(
            aggregate_id="exec-123",
            aggregate_type="GateExecution",
        )
        event_set = {event1, event2}
        assert len(event_set) == 2
