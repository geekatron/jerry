# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
QualityGate Domain Events.

Domain events for quality gate execution tracking. These events capture
the lifecycle of gate executions, check results, and threshold violations.

All events are:
    - Immutable (frozen dataclasses)
    - Named in past tense
    - Contain aggregate reference data from DomainEvent base

References:
    - IMPL-007: Domain Events (additional)
    - ADR-008: Quality Gate Layer Configuration
    - ADR-009: Event Storage Mechanism
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.shared_kernel.domain_event import DomainEvent, _current_timestamp, _generate_event_id

# =============================================================================
# Gate Execution Lifecycle Events
# =============================================================================


@dataclass(frozen=True)
class GateExecutionStarted(DomainEvent):
    """
    Emitted when a quality gate execution begins.

    This is the first event in a gate execution's event stream.
    It records which gate level is being executed and the checks to run.

    Attributes:
        gate_level: Gate level being executed (L0, L1, L2)
        risk_tier: Risk tier that triggered this execution (T1-T4)
        check_ids: IDs of checks to be executed
        timeout_seconds: Maximum execution time allowed

    Example:
        >>> event = GateExecutionStarted(
        ...     aggregate_id="exec-123",
        ...     aggregate_type="GateExecution",
        ...     gate_level="L1",
        ...     risk_tier="T2",
        ...     check_ids=("format-check", "test-run"),
        ...     timeout_seconds=300,
        ... )
    """

    gate_level: str = "L0"
    risk_tier: str = "T1"
    check_ids: tuple[str, ...] = field(default_factory=tuple)
    timeout_seconds: int = 60

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "gate_level": self.gate_level,
            "risk_tier": self.risk_tier,
            "check_ids": list(self.check_ids),
            "timeout_seconds": self.timeout_seconds,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GateExecutionStarted:
        """Deserialize from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        check_ids = data.get("check_ids", [])
        if isinstance(check_ids, list):
            check_ids = tuple(check_ids)

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "GateExecution"),
            version=data.get("version", 1),
            timestamp=timestamp,
            gate_level=data.get("gate_level", "L0"),
            risk_tier=data.get("risk_tier", "T1"),
            check_ids=check_ids,
            timeout_seconds=data.get("timeout_seconds", 60),
        )


@dataclass(frozen=True)
class GateCheckCompleted(DomainEvent):
    """
    Emitted when an individual check within a gate completes.

    Records the result of a single check execution with timing
    and optional violation details.

    Attributes:
        check_id: Unique identifier of the check
        check_name: Human-readable check name
        passed: Whether the check passed
        duration_ms: Execution time in milliseconds
        output_summary: Brief summary of check output
        violations: List of specific violations found
        artifact_path: Path to detailed evidence artifact

    Example:
        >>> event = GateCheckCompleted(
        ...     aggregate_id="exec-123",
        ...     aggregate_type="GateExecution",
        ...     check_id="coverage-check",
        ...     check_name="Test Coverage",
        ...     passed=False,
        ...     duration_ms=5000,
        ...     violations=("coverage: 72% < 80%",),
        ... )
    """

    check_id: str = ""
    check_name: str = ""
    passed: bool = False
    duration_ms: int = 0
    output_summary: str | None = None
    violations: tuple[str, ...] = field(default_factory=tuple)
    artifact_path: str | None = None

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "check_id": self.check_id,
            "check_name": self.check_name,
            "passed": self.passed,
            "duration_ms": self.duration_ms,
            "output_summary": self.output_summary,
            "violations": list(self.violations),
            "artifact_path": self.artifact_path,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GateCheckCompleted:
        """Deserialize from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        violations = data.get("violations", [])
        if isinstance(violations, list):
            violations = tuple(violations)

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "GateExecution"),
            version=data.get("version", 1),
            timestamp=timestamp,
            check_id=data.get("check_id", ""),
            check_name=data.get("check_name", ""),
            passed=data.get("passed", False),
            duration_ms=data.get("duration_ms", 0),
            output_summary=data.get("output_summary"),
            violations=violations,
            artifact_path=data.get("artifact_path"),
        )


@dataclass(frozen=True)
class GateExecutionCompleted(DomainEvent):
    """
    Emitted when a complete gate execution finishes.

    Contains aggregate results for all checks in the gate.

    Attributes:
        gate_level: Gate level that was executed
        result: Overall result (passed, failed, skipped)
        total_duration_ms: Total execution time in milliseconds
        checks_passed: Count of checks that passed
        checks_failed: Count of checks that failed
        failed_check_ids: IDs of checks that failed
        evidence_path: Path to combined evidence artifact

    Example:
        >>> event = GateExecutionCompleted(
        ...     aggregate_id="exec-123",
        ...     aggregate_type="GateExecution",
        ...     gate_level="L1",
        ...     result="passed",
        ...     total_duration_ms=60000,
        ...     checks_passed=5,
        ...     checks_failed=0,
        ... )
    """

    gate_level: str = "L0"
    result: str = "pending"
    total_duration_ms: int = 0
    checks_passed: int = 0
    checks_failed: int = 0
    failed_check_ids: tuple[str, ...] = field(default_factory=tuple)
    evidence_path: str | None = None

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "gate_level": self.gate_level,
            "result": self.result,
            "total_duration_ms": self.total_duration_ms,
            "checks_passed": self.checks_passed,
            "checks_failed": self.checks_failed,
            "failed_check_ids": list(self.failed_check_ids),
            "evidence_path": self.evidence_path,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GateExecutionCompleted:
        """Deserialize from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        failed_check_ids = data.get("failed_check_ids", [])
        if isinstance(failed_check_ids, list):
            failed_check_ids = tuple(failed_check_ids)

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "GateExecution"),
            version=data.get("version", 1),
            timestamp=timestamp,
            gate_level=data.get("gate_level", "L0"),
            result=data.get("result", "pending"),
            total_duration_ms=data.get("total_duration_ms", 0),
            checks_passed=data.get("checks_passed", 0),
            checks_failed=data.get("checks_failed", 0),
            failed_check_ids=failed_check_ids,
            evidence_path=data.get("evidence_path"),
        )


# =============================================================================
# Risk Assessment Events
# =============================================================================


@dataclass(frozen=True)
class RiskAssessed(DomainEvent):
    """
    Emitted when a change set's risk level is assessed.

    Records the risk tier classification and matching criteria.

    Attributes:
        risk_tier: Assigned risk tier (T1-T4)
        file_count: Number of files in the change set
        matched_patterns: File patterns that matched risk criteria
        matched_keywords: Keywords that matched risk criteria
        requires_human_approval: Whether T4 human approval is required

    Example:
        >>> event = RiskAssessed(
        ...     aggregate_id="change-123",
        ...     aggregate_type="ChangeSet",
        ...     risk_tier="T3",
        ...     file_count=10,
        ...     matched_patterns=("src/domain/**",),
        ... )
    """

    risk_tier: str = "T1"
    file_count: int = 0
    matched_patterns: tuple[str, ...] = field(default_factory=tuple)
    matched_keywords: tuple[str, ...] = field(default_factory=tuple)
    requires_human_approval: bool = False

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "risk_tier": self.risk_tier,
            "file_count": self.file_count,
            "matched_patterns": list(self.matched_patterns),
            "matched_keywords": list(self.matched_keywords),
            "requires_human_approval": self.requires_human_approval,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RiskAssessed:
        """Deserialize from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        matched_patterns = data.get("matched_patterns", [])
        if isinstance(matched_patterns, list):
            matched_patterns = tuple(matched_patterns)

        matched_keywords = data.get("matched_keywords", [])
        if isinstance(matched_keywords, list):
            matched_keywords = tuple(matched_keywords)

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "ChangeSet"),
            version=data.get("version", 1),
            timestamp=timestamp,
            risk_tier=data.get("risk_tier", "T1"),
            file_count=data.get("file_count", 0),
            matched_patterns=matched_patterns,
            matched_keywords=matched_keywords,
            requires_human_approval=data.get("requires_human_approval", False),
        )


# =============================================================================
# Threshold Violation Events
# =============================================================================


@dataclass(frozen=True)
class ThresholdViolation(DomainEvent):
    """
    Emitted when a metric violates its configured threshold.

    Records the specific violation with threshold and actual values.

    Attributes:
        check_id: ID of the check that found the violation
        threshold_type: Type of threshold (coverage, complexity, etc.)
        threshold_value: Configured threshold value
        actual_value: Actual measured value
        is_maximum: True if threshold is a maximum, False for minimum
        location: Optional file/location of the violation

    Example:
        >>> event = ThresholdViolation(
        ...     aggregate_id="exec-123",
        ...     aggregate_type="GateExecution",
        ...     check_id="coverage-check",
        ...     threshold_type="coverage",
        ...     threshold_value=80.0,
        ...     actual_value=72.5,
        ...     is_maximum=False,
        ... )
    """

    check_id: str = ""
    threshold_type: str = ""
    threshold_value: float = 0.0
    actual_value: float = 0.0
    is_maximum: bool = False
    location: str | None = None

    def _payload(self) -> dict[str, Any]:
        """Return event-specific payload data."""
        return {
            "check_id": self.check_id,
            "threshold_type": self.threshold_type,
            "threshold_value": self.threshold_value,
            "actual_value": self.actual_value,
            "is_maximum": self.is_maximum,
            "location": self.location,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ThresholdViolation:
        """Deserialize from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else _current_timestamp()

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data.get("aggregate_type", "GateExecution"),
            version=data.get("version", 1),
            timestamp=timestamp,
            check_id=data.get("check_id", ""),
            threshold_type=data.get("threshold_type", ""),
            threshold_value=data.get("threshold_value", 0.0),
            actual_value=data.get("actual_value", 0.0),
            is_maximum=data.get("is_maximum", False),
            location=data.get("location"),
        )
