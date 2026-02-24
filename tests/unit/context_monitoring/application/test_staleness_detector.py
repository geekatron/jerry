# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for StalenessDetector application service.

Tests cover BDD scenarios from EN-005:
    - Non-ORCHESTRATION.yaml tool call passes through
    - Stale ORCHESTRATION.yaml triggers warning
    - Fresh ORCHESTRATION.yaml passes through
    - Unparseable ORCHESTRATION.yaml is fail-open
    - Missing ORCHESTRATION.yaml is fail-open
    - Missing updated_at field is fail-open

References:
    - EN-005: PreToolUse Staleness Detection
    - FEAT-002: Pre-Tool-Use Hooks
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from src.context_monitoring.domain.value_objects.staleness_result import (
    StalenessResult,
)
from src.context_monitoring.infrastructure.adapters.staleness_detector import (
    StalenessDetector,
)

# =============================================================================
# Helpers
# =============================================================================


def _make_orchestration_yaml(
    project_root: Path,
    content: str,
    *,
    subpath: str = "ORCHESTRATION.yaml",
) -> Path:
    """Write an ORCHESTRATION.yaml file under project_root.

    Args:
        project_root: Root directory for the project.
        content: YAML content to write.
        subpath: Relative path within project_root for the file.

    Returns:
        The full path to the written file.
    """
    target = project_root / subpath
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target


def _make_detector(project_root: Path) -> StalenessDetector:
    """Create a StalenessDetector for the given project root.

    Args:
        project_root: Root directory for the project.

    Returns:
        A configured StalenessDetector instance.
    """
    return StalenessDetector(project_root=project_root)


# =============================================================================
# BDD Scenario: Non-ORCHESTRATION.yaml tool call passes through
# =============================================================================


class TestNonOrchestrationPassthrough:
    """Scenario: Non-ORCHESTRATION.yaml tool call passes through.

    Given a pre-tool-use payload targeting a non-ORCHESTRATION file,
    staleness detection should return no warning.
    """

    def test_python_file_passes_through(self, tmp_path: Path) -> None:
        """A Python source file path should not trigger staleness detection."""
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)

        result = detector.check_staleness(
            tool_target_path="src/context_monitoring/domain/value_objects/threshold_tier.py",
            reference_time=reference,
        )

        assert result.is_stale is False
        assert result.warning_message is None

    def test_markdown_file_passes_through(self, tmp_path: Path) -> None:
        """A markdown file path should not trigger staleness detection."""
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)

        result = detector.check_staleness(
            tool_target_path="docs/PLAN.md",
            reference_time=reference,
        )

        assert result.is_stale is False
        assert result.warning_message is None

    def test_orchestration_plan_md_passes_through(self, tmp_path: Path) -> None:
        """ORCHESTRATION_PLAN.md should not trigger staleness detection."""
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)

        result = detector.check_staleness(
            tool_target_path="ORCHESTRATION_PLAN.md",
            reference_time=reference,
        )

        assert result.is_stale is False
        assert result.warning_message is None

    def test_partial_name_match_passes_through(self, tmp_path: Path) -> None:
        """A file whose name contains ORCHESTRATION but is not .yaml passes through."""
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)

        result = detector.check_staleness(
            tool_target_path="ORCHESTRATION.yml",
            reference_time=reference,
        )

        assert result.is_stale is False
        assert result.warning_message is None


# =============================================================================
# BDD Scenario: Stale ORCHESTRATION.yaml triggers warning
# =============================================================================


class TestStaleOrchestrationWarning:
    """Scenario: Stale ORCHESTRATION.yaml triggers warning.

    Given an ORCHESTRATION.yaml with updated_at older than reference time,
    staleness detection should return is_stale=True with a warning.
    """

    def test_stale_orchestration_returns_warning(self, tmp_path: Path) -> None:
        """Stale ORCHESTRATION.yaml should trigger a staleness warning."""
        _make_orchestration_yaml(
            tmp_path,
            ("resumption:\n  recovery_state:\n    updated_at: '2026-02-18T10:00:00Z'\n"),
            subpath="projects/PROJ-004/ORCHESTRATION.yaml",
        )
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)

        result = detector.check_staleness(
            tool_target_path="projects/PROJ-004/ORCHESTRATION.yaml",
            reference_time=reference,
        )

        assert result.is_stale is True
        assert result.warning_message is not None
        assert "stale" in result.warning_message.lower()
        assert result.updated_at == "2026-02-18T10:00:00Z"

    def test_stale_with_absolute_path(self, tmp_path: Path) -> None:
        """Stale detection works with absolute tool target paths."""
        _make_orchestration_yaml(
            tmp_path,
            ("resumption:\n  recovery_state:\n    updated_at: '2026-02-18T10:00:00Z'\n"),
        )
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)
        absolute_path = str(tmp_path / "ORCHESTRATION.yaml")

        result = detector.check_staleness(
            tool_target_path=absolute_path,
            reference_time=reference,
        )

        assert result.is_stale is True
        assert result.warning_message is not None

    def test_stale_with_nested_path(self, tmp_path: Path) -> None:
        """Stale detection works with deeply nested ORCHESTRATION.yaml paths."""
        _make_orchestration_yaml(
            tmp_path,
            ("resumption:\n  recovery_state:\n    updated_at: '2026-02-15T12:00:00Z'\n"),
            subpath="projects/PROJ-004/orchestration/feat001/ORCHESTRATION.yaml",
        )
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)

        result = detector.check_staleness(
            tool_target_path="projects/PROJ-004/orchestration/feat001/ORCHESTRATION.yaml",
            reference_time=reference,
        )

        assert result.is_stale is True

    def test_result_includes_reference_time(self, tmp_path: Path) -> None:
        """Stale result should include the reference time for diagnostics."""
        _make_orchestration_yaml(
            tmp_path,
            ("resumption:\n  recovery_state:\n    updated_at: '2026-02-18T10:00:00Z'\n"),
        )
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)

        result = detector.check_staleness(
            tool_target_path="ORCHESTRATION.yaml",
            reference_time=reference,
        )

        assert result.reference_time is not None


# =============================================================================
# BDD Scenario: Fresh ORCHESTRATION.yaml passes through
# =============================================================================


class TestFreshOrchestrationPassthrough:
    """Scenario: Fresh ORCHESTRATION.yaml passes through.

    Given an ORCHESTRATION.yaml with updated_at newer than reference time,
    staleness detection should return no warning.
    """

    def test_fresh_orchestration_passes_through(self, tmp_path: Path) -> None:
        """Fresh ORCHESTRATION.yaml should not trigger a staleness warning."""
        _make_orchestration_yaml(
            tmp_path,
            ("resumption:\n  recovery_state:\n    updated_at: '2026-02-19T09:30:00Z'\n"),
        )
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)

        result = detector.check_staleness(
            tool_target_path="ORCHESTRATION.yaml",
            reference_time=reference,
        )

        assert result.is_stale is False
        assert result.warning_message is None

    def test_equal_timestamps_pass_through(self, tmp_path: Path) -> None:
        """ORCHESTRATION.yaml with updated_at equal to reference time passes through."""
        _make_orchestration_yaml(
            tmp_path,
            ("resumption:\n  recovery_state:\n    updated_at: '2026-02-19T08:00:00Z'\n"),
        )
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)

        result = detector.check_staleness(
            tool_target_path="ORCHESTRATION.yaml",
            reference_time=reference,
        )

        assert result.is_stale is False
        assert result.warning_message is None


# =============================================================================
# BDD Scenario: Unparseable ORCHESTRATION.yaml is fail-open
# =============================================================================


class TestUnparseableOrchestrationFailOpen:
    """Scenario: Unparseable ORCHESTRATION.yaml is fail-open.

    Given an ORCHESTRATION.yaml with invalid YAML content,
    staleness detection should return no warning and no exception should propagate.
    """

    def test_invalid_yaml_fails_open(self, tmp_path: Path) -> None:
        """Invalid YAML should not cause an exception and should pass through."""
        _make_orchestration_yaml(
            tmp_path,
            "{{{{ not valid yaml: ][",
        )
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)

        result = detector.check_staleness(
            tool_target_path="ORCHESTRATION.yaml",
            reference_time=reference,
        )

        assert result.is_stale is False
        assert result.warning_message is None

    def test_binary_content_fails_open(self, tmp_path: Path) -> None:
        """Binary content should not cause an exception and should pass through."""
        target = tmp_path / "ORCHESTRATION.yaml"
        target.write_bytes(b"\x00\x01\x02\x03\xff\xfe")
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)

        result = detector.check_staleness(
            tool_target_path="ORCHESTRATION.yaml",
            reference_time=reference,
        )

        assert result.is_stale is False
        assert result.warning_message is None


# =============================================================================
# BDD Scenario: Missing ORCHESTRATION.yaml is fail-open
# =============================================================================


class TestMissingOrchestrationFailOpen:
    """Scenario: Missing ORCHESTRATION.yaml is fail-open.

    Given no ORCHESTRATION.yaml file exists at the target path,
    staleness detection should return no warning.
    """

    def test_missing_file_fails_open(self, tmp_path: Path) -> None:
        """Missing ORCHESTRATION.yaml should pass through without error."""
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)

        result = detector.check_staleness(
            tool_target_path="ORCHESTRATION.yaml",
            reference_time=reference,
        )

        assert result.is_stale is False
        assert result.warning_message is None

    def test_missing_nested_file_fails_open(self, tmp_path: Path) -> None:
        """Missing nested ORCHESTRATION.yaml should pass through without error."""
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)

        result = detector.check_staleness(
            tool_target_path="projects/PROJ-004/ORCHESTRATION.yaml",
            reference_time=reference,
        )

        assert result.is_stale is False
        assert result.warning_message is None


# =============================================================================
# BDD Scenario: Missing updated_at field is fail-open
# =============================================================================


class TestMissingUpdatedAtFailOpen:
    """Scenario: Missing updated_at field is fail-open.

    Given an ORCHESTRATION.yaml with no resumption.recovery_state.updated_at,
    staleness detection should return no warning.
    """

    def test_missing_resumption_key_fails_open(self, tmp_path: Path) -> None:
        """ORCHESTRATION.yaml with no resumption key passes through."""
        _make_orchestration_yaml(
            tmp_path,
            "phase: implementation\nstatus: active\n",
        )
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)

        result = detector.check_staleness(
            tool_target_path="ORCHESTRATION.yaml",
            reference_time=reference,
        )

        assert result.is_stale is False
        assert result.warning_message is None

    def test_missing_recovery_state_key_fails_open(self, tmp_path: Path) -> None:
        """ORCHESTRATION.yaml with resumption but no recovery_state passes through."""
        _make_orchestration_yaml(
            tmp_path,
            "resumption:\n  checkpoint_id: abc123\n",
        )
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)

        result = detector.check_staleness(
            tool_target_path="ORCHESTRATION.yaml",
            reference_time=reference,
        )

        assert result.is_stale is False
        assert result.warning_message is None

    def test_null_updated_at_fails_open(self, tmp_path: Path) -> None:
        """ORCHESTRATION.yaml with null updated_at passes through."""
        _make_orchestration_yaml(
            tmp_path,
            "resumption:\n  recovery_state:\n    updated_at: null\n",
        )
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)

        result = detector.check_staleness(
            tool_target_path="ORCHESTRATION.yaml",
            reference_time=reference,
        )

        assert result.is_stale is False
        assert result.warning_message is None

    def test_empty_updated_at_fails_open(self, tmp_path: Path) -> None:
        """ORCHESTRATION.yaml with empty string updated_at passes through."""
        _make_orchestration_yaml(
            tmp_path,
            "resumption:\n  recovery_state:\n    updated_at: ''\n",
        )
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)

        result = detector.check_staleness(
            tool_target_path="ORCHESTRATION.yaml",
            reference_time=reference,
        )

        assert result.is_stale is False
        assert result.warning_message is None

    def test_invalid_timestamp_format_fails_open(self, tmp_path: Path) -> None:
        """ORCHESTRATION.yaml with invalid timestamp format passes through."""
        _make_orchestration_yaml(
            tmp_path,
            "resumption:\n  recovery_state:\n    updated_at: 'not-a-timestamp'\n",
        )
        detector = _make_detector(tmp_path)
        reference = datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC)

        result = detector.check_staleness(
            tool_target_path="ORCHESTRATION.yaml",
            reference_time=reference,
        )

        assert result.is_stale is False
        assert result.warning_message is None


# =============================================================================
# StalenessResult value object tests
# =============================================================================


class TestStalenessResultValueObject:
    """Tests for the StalenessResult frozen dataclass."""

    def test_passthrough_factory(self) -> None:
        """StalenessResult with is_stale=False represents passthrough."""
        result = StalenessResult(is_stale=False)
        assert result.is_stale is False
        assert result.warning_message is None
        assert result.updated_at is None
        assert result.reference_time is None

    def test_stale_result_with_all_fields(self) -> None:
        """StalenessResult with all fields set represents a stale detection."""
        result = StalenessResult(
            is_stale=True,
            warning_message="ORCHESTRATION.yaml is stale",
            updated_at="2026-02-18T10:00:00Z",
            reference_time="2026-02-19T08:00:00Z",
        )
        assert result.is_stale is True
        assert result.warning_message == "ORCHESTRATION.yaml is stale"
        assert result.updated_at == "2026-02-18T10:00:00Z"
        assert result.reference_time == "2026-02-19T08:00:00Z"

    def test_frozen_dataclass_is_immutable(self) -> None:
        """StalenessResult should be immutable (frozen dataclass)."""
        result = StalenessResult(is_stale=False)
        with pytest.raises(AttributeError):
            result.is_stale = True  # type: ignore[misc]

    def test_equality(self) -> None:
        """Two StalenessResult instances with same values should be equal."""
        a = StalenessResult(is_stale=False)
        b = StalenessResult(is_stale=False)
        assert a == b

    def test_inequality(self) -> None:
        """Two StalenessResult instances with different values should not be equal."""
        a = StalenessResult(is_stale=False)
        b = StalenessResult(is_stale=True, warning_message="stale")
        assert a != b
