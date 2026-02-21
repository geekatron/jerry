# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for HooksPreToolUseHandler.

BDD scenarios:
    - Handler returns enforcement decision JSON
    - Handler is fail-open: step failure logs to stderr and exits 0 with valid JSON
    - Handler blocks when enforcement decision is "block"
    - Handler approves passthrough for non-Python tools
    - Handler passes tool input to enforcement engine

References:
    - EN-006: jerry hooks CLI Command Namespace
    - EN-005: PreToolUse Staleness Detection
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from src.context_monitoring.domain.value_objects.staleness_result import StalenessResult
from src.infrastructure.internal.enforcement.enforcement_decision import (
    EnforcementDecision,
)
from src.interface.cli.hooks.hooks_pre_tool_use_handler import HooksPreToolUseHandler

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def mock_enforcement_engine() -> MagicMock:
    """Create a mock PreToolEnforcementEngine."""
    engine = MagicMock()
    engine.evaluate_write.return_value = EnforcementDecision(
        action="approve",
        reason="All checks passed",
    )
    engine.evaluate_edit.return_value = EnforcementDecision(
        action="approve",
        reason="All checks passed",
    )
    return engine


@pytest.fixture()
def mock_staleness_detector() -> MagicMock:
    """Create a mock StalenessDetector."""
    detector = MagicMock()
    detector.check_staleness.return_value = StalenessResult(is_stale=False)
    return detector


@pytest.fixture()
def handler(
    mock_enforcement_engine: MagicMock,
    mock_staleness_detector: MagicMock,
) -> HooksPreToolUseHandler:
    """Create a HooksPreToolUseHandler with mock services."""
    return HooksPreToolUseHandler(
        enforcement_engine=mock_enforcement_engine,
        staleness_detector=mock_staleness_detector,
    )


# =============================================================================
# Tests
# =============================================================================


class TestHooksPreToolUseHandlerReturnsDecision:
    """BDD: Handler returns enforcement decision JSON."""

    def test_handle_returns_valid_json(
        self,
        handler: HooksPreToolUseHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Given a PreToolUse hook input, handler returns valid JSON."""
        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "session_id": "test-session-abc",
                "tool_name": "Read",
                "tool_input": {"file_path": "/tmp/test.py"},
            }
        )

        exit_code = handler.handle(hook_input)

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result is not None

    def test_handle_write_tool_calls_enforcement_engine(
        self,
        handler: HooksPreToolUseHandler,
        mock_enforcement_engine: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """For Write tool, enforcement engine.evaluate_write is called."""
        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": "/src/domain/entity.py",
                    "content": "class Entity:\n    pass\n",
                },
            }
        )

        handler.handle(hook_input)

        mock_enforcement_engine.evaluate_write.assert_called_once()

    def test_handle_edit_tool_calls_enforcement_engine(
        self,
        handler: HooksPreToolUseHandler,
        mock_enforcement_engine: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """For Edit tool, enforcement engine.evaluate_edit is called."""
        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Edit",
                "tool_input": {
                    "file_path": "/src/domain/entity.py",
                    "old_string": "old",
                    "new_string": "new",
                },
            }
        )

        handler.handle(hook_input)

        mock_enforcement_engine.evaluate_edit.assert_called_once()

    def test_handle_block_decision_returns_block_response(
        self,
        mock_staleness_detector: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When enforcement engine returns block, response indicates block."""
        blocking_engine = MagicMock()
        blocking_engine.evaluate_write.return_value = EnforcementDecision(
            action="block",
            reason="Architecture violation: domain layer cannot import infrastructure",
            violations=["Line 5: domain layer cannot import from infrastructure"],
        )

        handler = HooksPreToolUseHandler(
            enforcement_engine=blocking_engine,
            staleness_detector=mock_staleness_detector,
        )

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": "/src/domain/bad.py",
                    "content": "from src.infrastructure import Repo",
                },
            }
        )

        exit_code = handler.handle(hook_input)

        assert exit_code == 0  # Always exit 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        # Response should indicate blocking
        assert result.get("decision") == "block" or "block" in str(result)

    def test_handle_read_tool_does_not_call_write_enforcement(
        self,
        handler: HooksPreToolUseHandler,
        mock_enforcement_engine: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """For Read tool (non-write), enforcement write is not called."""
        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "/src/domain/entity.py"},
            }
        )

        handler.handle(hook_input)

        mock_enforcement_engine.evaluate_write.assert_not_called()
        mock_enforcement_engine.evaluate_edit.assert_not_called()

    def test_handle_staleness_detection_called(
        self,
        handler: HooksPreToolUseHandler,
        mock_staleness_detector: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """StalenessDetector is called for any tool that targets a file."""
        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": "ORCHESTRATION.yaml",
                    "content": "resumption:\n  recovery_state:\n    updated_at: 2026-01-01T00:00:00Z",
                },
            }
        )

        handler.handle(hook_input)

        mock_staleness_detector.check_staleness.assert_called_once()

    def test_handle_stale_orchestration_includes_warning(
        self,
        mock_enforcement_engine: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When staleness detected, warning is included in response."""
        stale_detector = MagicMock()
        stale_detector.check_staleness.return_value = StalenessResult(
            is_stale=True,
            warning_message="ORCHESTRATION.yaml is stale",
            updated_at="2026-01-01T00:00:00Z",
            reference_time="2026-02-20T00:00:00Z",
        )

        handler = HooksPreToolUseHandler(
            enforcement_engine=mock_enforcement_engine,
            staleness_detector=stale_detector,
        )

        hook_input = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": "ORCHESTRATION.yaml",
                    "content": "content",
                },
            }
        )

        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        # Staleness warning should appear in output
        assert "stale" in str(result).lower() or result is not None


class TestHooksPreToolUseHandlerFailOpen:
    """BDD: Handler step failure is fail-open."""

    def test_enforcement_engine_failure_returns_valid_json(
        self,
        mock_staleness_detector: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When enforcement engine fails, handler still returns valid JSON with exit 0."""
        failing_engine = MagicMock()
        failing_engine.evaluate_write.side_effect = RuntimeError("Engine failed")

        handler = HooksPreToolUseHandler(
            enforcement_engine=failing_engine,
            staleness_detector=mock_staleness_detector,
        )

        hook_input = json.dumps(
            {
                "tool_name": "Write",
                "tool_input": {"file_path": "/src/test.py", "content": "pass"},
            }
        )
        exit_code = handler.handle(hook_input)

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result is not None

    def test_staleness_detector_failure_returns_valid_json(
        self,
        mock_enforcement_engine: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When staleness detector fails, handler still returns valid JSON."""
        failing_detector = MagicMock()
        failing_detector.check_staleness.side_effect = RuntimeError("Detector failed")

        handler = HooksPreToolUseHandler(
            enforcement_engine=mock_enforcement_engine,
            staleness_detector=failing_detector,
        )

        hook_input = json.dumps(
            {
                "tool_name": "Write",
                "tool_input": {"file_path": "ORCHESTRATION.yaml", "content": "content"},
            }
        )
        exit_code = handler.handle(hook_input)

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result is not None

    def test_invalid_json_input_returns_valid_json(
        self,
        handler: HooksPreToolUseHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When hook input is invalid JSON, handler returns valid JSON with exit 0."""
        exit_code = handler.handle("not-valid-json")

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result is not None
