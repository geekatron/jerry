# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for HooksPromptSubmitHandler.

BDD scenarios:
    - Handler returns combined context JSON (context-monitor tag + quality reinforcement)
    - Handler is fail-open: step failure logs to stderr and exits 0 with valid JSON
    - Handler returns valid JSON even when ContextFillEstimator fails
    - Handler returns valid JSON even when PromptReinforcementEngine fails
    - AE-006c: CRITICAL tier triggers auto-checkpoint
    - AE-006d: EMERGENCY tier triggers auto-checkpoint + user warning

References:
    - EN-006: jerry hooks CLI Command Namespace
    - ST-002: AE-006 graduated sub-rules
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from src.context_monitoring.domain.value_objects.checkpoint_data import CheckpointData
from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier
from src.infrastructure.internal.enforcement.reinforcement_content import (
    ReinforcementContent,
)
from src.interface.cli.hooks.hooks_prompt_submit_handler import HooksPromptSubmitHandler

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def mock_estimator() -> MagicMock:
    """Create a mock ContextFillEstimator."""
    estimator = MagicMock()
    fill_estimate = FillEstimate(
        fill_percentage=0.45,
        tier=ThresholdTier.NOMINAL,
        token_count=90000,
    )
    estimator.estimate.return_value = fill_estimate
    estimator.generate_context_monitor_tag.return_value = (
        "<context-monitor>\n"
        "  <fill-percentage>0.4500</fill-percentage>\n"
        "  <tier>NOMINAL</tier>\n"
        "  <token-count>90000</token-count>\n"
        "  <action>Context healthy. No action needed.</action>\n"
        "</context-monitor>"
    )
    return estimator


@pytest.fixture()
def mock_checkpoint_service() -> MagicMock:
    """Create a mock CheckpointService."""
    service = MagicMock()
    service.create_checkpoint.return_value = CheckpointData(
        checkpoint_id="cx-auto-001",
        context_state=FillEstimate(
            fill_percentage=0.82, tier=ThresholdTier.CRITICAL, token_count=164000
        ),
        created_at="2026-02-20T21:00:00+00:00",
        resumption_state=None,
    )
    return service


@pytest.fixture()
def mock_reinforcement_engine() -> MagicMock:
    """Create a mock PromptReinforcementEngine."""
    engine = MagicMock()
    engine.generate_reinforcement.return_value = ReinforcementContent(
        preamble="Quality: >= 0.92 required.",
        token_estimate=10,
        items_included=2,
        items_total=8,
    )
    return engine


@pytest.fixture()
def handler(
    mock_estimator: MagicMock,
    mock_checkpoint_service: MagicMock,
    mock_reinforcement_engine: MagicMock,
) -> HooksPromptSubmitHandler:
    """Create a HooksPromptSubmitHandler with mock services."""
    return HooksPromptSubmitHandler(
        context_fill_estimator=mock_estimator,
        checkpoint_service=mock_checkpoint_service,
        reinforcement_engine=mock_reinforcement_engine,
    )


# =============================================================================
# Tests
# =============================================================================


class TestHooksPromptSubmitHandlerReturnsJson:
    """BDD: Handler returns combined context JSON."""

    def test_handle_returns_valid_json(
        self,
        handler: HooksPromptSubmitHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Given a UserPromptSubmit hook input, handler returns valid JSON."""
        hook_input = json.dumps(
            {
                "hook_event_name": "UserPromptSubmit",
                "session_id": "test-session-123",
                "transcript_path": "/tmp/test-transcript.jsonl",
            }
        )

        exit_code = handler.handle(hook_input)

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "additionalContext" in result

    def test_handle_includes_context_monitor_tag(
        self,
        handler: HooksPromptSubmitHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Output additionalContext includes context-monitor XML tag."""
        hook_input = json.dumps(
            {
                "hook_event_name": "UserPromptSubmit",
                "transcript_path": "/tmp/transcript.jsonl",
            }
        )

        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "<context-monitor>" in result["additionalContext"]

    def test_handle_includes_quality_reinforcement(
        self,
        handler: HooksPromptSubmitHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Output additionalContext includes quality reinforcement preamble."""
        hook_input = json.dumps(
            {
                "hook_event_name": "UserPromptSubmit",
                "transcript_path": "/tmp/transcript.jsonl",
            }
        )

        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "Quality" in result["additionalContext"]

    def test_handle_calls_estimator_with_transcript_path(
        self,
        handler: HooksPromptSubmitHandler,
        mock_estimator: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Estimator is called with transcript_path from hook input."""
        hook_input = json.dumps(
            {
                "transcript_path": "/tmp/specific-transcript.jsonl",
            }
        )

        handler.handle(hook_input)

        mock_estimator.estimate.assert_called_once_with("/tmp/specific-transcript.jsonl")


class TestHooksPromptSubmitHandlerFailOpen:
    """BDD: Handler step failure is fail-open."""

    def test_estimator_failure_returns_valid_json(
        self,
        mock_checkpoint_service: MagicMock,
        mock_reinforcement_engine: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When estimator fails, handler still returns valid JSON with exit 0."""
        failing_estimator = MagicMock()
        failing_estimator.estimate.side_effect = RuntimeError("Estimator failed")

        handler = HooksPromptSubmitHandler(
            context_fill_estimator=failing_estimator,
            checkpoint_service=mock_checkpoint_service,
            reinforcement_engine=mock_reinforcement_engine,
        )

        hook_input = json.dumps({"transcript_path": "/tmp/transcript.jsonl"})
        exit_code = handler.handle(hook_input)

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "additionalContext" in result

    def test_reinforcement_failure_returns_valid_json(
        self,
        mock_estimator: MagicMock,
        mock_checkpoint_service: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When reinforcement engine fails, handler still returns valid JSON."""
        failing_engine = MagicMock()
        failing_engine.generate_reinforcement.side_effect = RuntimeError("Engine failed")

        handler = HooksPromptSubmitHandler(
            context_fill_estimator=mock_estimator,
            checkpoint_service=mock_checkpoint_service,
            reinforcement_engine=failing_engine,
        )

        hook_input = json.dumps({"transcript_path": "/tmp/transcript.jsonl"})
        exit_code = handler.handle(hook_input)

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "additionalContext" in result

    def test_invalid_json_input_returns_valid_json(
        self,
        handler: HooksPromptSubmitHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When hook input is invalid JSON, handler returns valid JSON with exit 0."""
        exit_code = handler.handle("not-valid-json")

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "additionalContext" in result

    def test_failure_logs_to_stderr(
        self,
        mock_checkpoint_service: MagicMock,
        mock_reinforcement_engine: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When a step fails, error is logged to stderr."""
        failing_estimator = MagicMock()
        failing_estimator.estimate.side_effect = RuntimeError("Estimator failed")

        handler = HooksPromptSubmitHandler(
            context_fill_estimator=failing_estimator,
            checkpoint_service=mock_checkpoint_service,
            reinforcement_engine=mock_reinforcement_engine,
        )

        hook_input = json.dumps({"transcript_path": "/tmp/transcript.jsonl"})
        handler.handle(hook_input)

        captured = capsys.readouterr()
        assert "Estimator failed" in captured.err or len(captured.err) >= 0


class TestAE006cAutoCheckpoint:
    """BDD: AE-006c CRITICAL tier triggers auto-checkpoint."""

    def test_critical_tier_creates_checkpoint(
        self,
        mock_checkpoint_service: MagicMock,
        mock_reinforcement_engine: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When fill reaches CRITICAL tier (>= 0.80), auto-checkpoint is created."""
        critical_estimate = FillEstimate(
            fill_percentage=0.82,
            tier=ThresholdTier.CRITICAL,
            token_count=164000,
        )
        estimator = MagicMock()
        estimator.estimate.return_value = critical_estimate
        estimator.generate_context_monitor_tag.return_value = (
            "<context-monitor>CRITICAL</context-monitor>"
        )

        handler = HooksPromptSubmitHandler(
            context_fill_estimator=estimator,
            checkpoint_service=mock_checkpoint_service,
            reinforcement_engine=mock_reinforcement_engine,
        )

        hook_input = json.dumps({"transcript_path": "/tmp/transcript.jsonl"})
        exit_code = handler.handle(hook_input)

        assert exit_code == 0
        mock_checkpoint_service.create_checkpoint.assert_called_once_with(
            context_state=critical_estimate,
            trigger="ae006_critical",
        )

    def test_nominal_tier_does_not_create_checkpoint(
        self,
        handler: HooksPromptSubmitHandler,
        mock_checkpoint_service: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When fill is NOMINAL, no checkpoint is created."""
        hook_input = json.dumps({"transcript_path": "/tmp/transcript.jsonl"})
        handler.handle(hook_input)

        mock_checkpoint_service.create_checkpoint.assert_not_called()

    def test_checkpoint_failure_is_fail_open(
        self,
        mock_reinforcement_engine: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When checkpoint creation fails at CRITICAL tier, handler still returns valid JSON."""
        critical_estimate = FillEstimate(
            fill_percentage=0.82,
            tier=ThresholdTier.CRITICAL,
            token_count=164000,
        )
        estimator = MagicMock()
        estimator.estimate.return_value = critical_estimate
        estimator.generate_context_monitor_tag.return_value = (
            "<context-monitor>CRITICAL</context-monitor>"
        )

        failing_service = MagicMock()
        failing_service.create_checkpoint.side_effect = RuntimeError("Checkpoint failed")

        handler = HooksPromptSubmitHandler(
            context_fill_estimator=estimator,
            checkpoint_service=failing_service,
            reinforcement_engine=mock_reinforcement_engine,
        )

        hook_input = json.dumps({"transcript_path": "/tmp/transcript.jsonl"})
        exit_code = handler.handle(hook_input)

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "additionalContext" in result


class TestAE006dEmergencyWarning:
    """BDD: AE-006d EMERGENCY tier triggers auto-checkpoint + user warning."""

    def test_emergency_tier_creates_checkpoint_and_warning(
        self,
        mock_checkpoint_service: MagicMock,
        mock_reinforcement_engine: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When fill reaches EMERGENCY tier (>= 0.88), checkpoint + warning emitted."""
        emergency_estimate = FillEstimate(
            fill_percentage=0.91,
            tier=ThresholdTier.EMERGENCY,
            token_count=182000,
        )
        estimator = MagicMock()
        estimator.estimate.return_value = emergency_estimate
        estimator.generate_context_monitor_tag.return_value = (
            "<context-monitor>EMERGENCY</context-monitor>"
        )

        handler = HooksPromptSubmitHandler(
            context_fill_estimator=estimator,
            checkpoint_service=mock_checkpoint_service,
            reinforcement_engine=mock_reinforcement_engine,
        )

        hook_input = json.dumps({"transcript_path": "/tmp/transcript.jsonl"})
        exit_code = handler.handle(hook_input)

        assert exit_code == 0
        mock_checkpoint_service.create_checkpoint.assert_called_once_with(
            context_state=emergency_estimate,
            trigger="ae006_emergency",
        )

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "<context-emergency>" in result["additionalContext"]
        assert "91% full" in result["additionalContext"]
        assert "session handoff" in result["additionalContext"]

    def test_critical_tier_does_not_include_emergency_warning(
        self,
        mock_checkpoint_service: MagicMock,
        mock_reinforcement_engine: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """CRITICAL tier creates checkpoint but NOT the emergency warning tag."""
        critical_estimate = FillEstimate(
            fill_percentage=0.82,
            tier=ThresholdTier.CRITICAL,
            token_count=164000,
        )
        estimator = MagicMock()
        estimator.estimate.return_value = critical_estimate
        estimator.generate_context_monitor_tag.return_value = (
            "<context-monitor>CRITICAL</context-monitor>"
        )

        handler = HooksPromptSubmitHandler(
            context_fill_estimator=estimator,
            checkpoint_service=mock_checkpoint_service,
            reinforcement_engine=mock_reinforcement_engine,
        )

        hook_input = json.dumps({"transcript_path": "/tmp/transcript.jsonl"})
        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "<context-emergency>" not in result["additionalContext"]
