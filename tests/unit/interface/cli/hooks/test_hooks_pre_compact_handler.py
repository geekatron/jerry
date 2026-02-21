# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for HooksPreCompactHandler.

BDD scenarios:
    - Handler creates checkpoint and abandons session, returns JSON
    - Handler is fail-open: step failure logs to stderr and exits 0 with valid JSON
    - Handler returns valid JSON even when checkpoint creation fails
    - Handler returns valid JSON even when abandon session fails

References:
    - EN-006: jerry hooks CLI Command Namespace
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from src.context_monitoring.domain.value_objects.checkpoint_data import CheckpointData
from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier
from src.interface.cli.hooks.hooks_pre_compact_handler import HooksPreCompactHandler


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def mock_checkpoint_service() -> MagicMock:
    """Create a mock CheckpointService."""
    service = MagicMock()
    fill_estimate = FillEstimate(
        fill_percentage=0.88,
        tier=ThresholdTier.EMERGENCY,
        token_count=176000,
    )
    checkpoint = CheckpointData(
        checkpoint_id="cx-001",
        context_state=fill_estimate,
        created_at="2026-02-20T10:00:00+00:00",
        resumption_state={"orchestration": "yaml content here"},
    )
    service.create_checkpoint.return_value = checkpoint
    return service


@pytest.fixture()
def mock_context_fill_estimator() -> MagicMock:
    """Create a mock ContextFillEstimator."""
    estimator = MagicMock()
    fill_estimate = FillEstimate(
        fill_percentage=0.88,
        tier=ThresholdTier.EMERGENCY,
        token_count=176000,
    )
    estimator.estimate.return_value = fill_estimate
    return estimator


@pytest.fixture()
def mock_abandon_handler() -> MagicMock:
    """Create a mock AbandonSessionCommandHandler."""
    handler = MagicMock()
    mock_event = MagicMock()
    mock_event.aggregate_id = "session-abc-123"
    handler.handle.return_value = [mock_event]
    return handler


@pytest.fixture()
def handler(
    mock_checkpoint_service: MagicMock,
    mock_context_fill_estimator: MagicMock,
    mock_abandon_handler: MagicMock,
) -> HooksPreCompactHandler:
    """Create a HooksPreCompactHandler with mock services."""
    return HooksPreCompactHandler(
        checkpoint_service=mock_checkpoint_service,
        context_fill_estimator=mock_context_fill_estimator,
        abandon_handler=mock_abandon_handler,
    )


# =============================================================================
# Tests
# =============================================================================


class TestHooksPreCompactHandlerCreatesCheckpoint:
    """BDD: Handler creates checkpoint and abandons session."""

    def test_handle_returns_valid_json(
        self,
        handler: HooksPreCompactHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Given a PreCompact hook input, handler returns valid JSON."""
        hook_input = json.dumps({
            "hook_event_name": "PreCompact",
            "session_id": "test-session-789",
            "transcript_path": "/tmp/test-transcript.jsonl",
        })

        exit_code = handler.handle(hook_input)

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result is not None

    def test_handle_calls_create_checkpoint(
        self,
        handler: HooksPreCompactHandler,
        mock_checkpoint_service: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Handler calls checkpoint_service.create_checkpoint with trigger='pre_compact'."""
        hook_input = json.dumps({
            "hook_event_name": "PreCompact",
            "transcript_path": "/tmp/transcript.jsonl",
        })

        handler.handle(hook_input)

        mock_checkpoint_service.create_checkpoint.assert_called_once()
        call_kwargs = mock_checkpoint_service.create_checkpoint.call_args
        assert call_kwargs[1].get("trigger") == "pre_compact" or (
            len(call_kwargs[0]) >= 2 and call_kwargs[0][1] == "pre_compact"
        )

    def test_handle_calls_abandon_session(
        self,
        handler: HooksPreCompactHandler,
        mock_abandon_handler: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Handler calls abandon handler with reason 'compaction'."""
        hook_input = json.dumps({
            "hook_event_name": "PreCompact",
            "transcript_path": "/tmp/transcript.jsonl",
        })

        handler.handle(hook_input)

        mock_abandon_handler.handle.assert_called_once()
        # Verify the command passed to abandon has reason="compaction"
        command = mock_abandon_handler.handle.call_args[0][0]
        assert command.reason == "compaction"

    def test_handle_response_includes_checkpoint_id(
        self,
        handler: HooksPreCompactHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Response JSON includes checkpoint_id."""
        hook_input = json.dumps({
            "hook_event_name": "PreCompact",
            "transcript_path": "/tmp/transcript.jsonl",
        })

        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "checkpoint_id" in result


class TestHooksPreCompactHandlerFailOpen:
    """BDD: Handler step failure is fail-open."""

    def test_checkpoint_failure_returns_valid_json(
        self,
        mock_context_fill_estimator: MagicMock,
        mock_abandon_handler: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When checkpoint service fails, handler still returns valid JSON with exit 0."""
        failing_service = MagicMock()
        failing_service.create_checkpoint.side_effect = RuntimeError("Checkpoint failed")

        handler = HooksPreCompactHandler(
            checkpoint_service=failing_service,
            context_fill_estimator=mock_context_fill_estimator,
            abandon_handler=mock_abandon_handler,
        )

        hook_input = json.dumps({
            "hook_event_name": "PreCompact",
            "transcript_path": "/tmp/transcript.jsonl",
        })
        exit_code = handler.handle(hook_input)

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result is not None

    def test_abandon_failure_returns_valid_json(
        self,
        mock_checkpoint_service: MagicMock,
        mock_context_fill_estimator: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When abandon handler fails, handler still returns valid JSON."""
        failing_abandon = MagicMock()
        failing_abandon.handle.side_effect = RuntimeError("Abandon failed")

        handler = HooksPreCompactHandler(
            checkpoint_service=mock_checkpoint_service,
            context_fill_estimator=mock_context_fill_estimator,
            abandon_handler=failing_abandon,
        )

        hook_input = json.dumps({
            "hook_event_name": "PreCompact",
            "transcript_path": "/tmp/transcript.jsonl",
        })
        exit_code = handler.handle(hook_input)

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result is not None

    def test_invalid_json_input_returns_valid_json(
        self,
        handler: HooksPreCompactHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When hook input is invalid JSON, handler returns valid JSON with exit 0."""
        exit_code = handler.handle("not-valid-json")

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result is not None
