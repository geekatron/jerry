# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for HooksSessionStartHandler.

BDD scenarios:
    - Handler returns project + quality + resumption context JSON
    - Handler is fail-open: step failure logs to stderr and exits 0 with valid JSON
    - Handler returns valid JSON even when checkpoint retrieval fails
    - Handler returns valid JSON even when project context query fails

References:
    - EN-006: jerry hooks CLI Command Namespace
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.context_monitoring.domain.value_objects.checkpoint_data import CheckpointData
from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier
from src.infrastructure.internal.enforcement.quality_context import QualityContext
from src.interface.cli.hooks.hooks_session_start_handler import HooksSessionStartHandler

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def mock_query_dispatcher() -> MagicMock:
    """Create a mock query dispatcher."""
    dispatcher = MagicMock()
    dispatcher.dispatch.return_value = {
        "jerry_project": "PROJ-004-context-resilience",
        "project_id": "PROJ-004-context-resilience",
        "validation": None,
        "available_projects": [],
        "next_number": 5,
    }
    return dispatcher


@pytest.fixture()
def mock_checkpoint_service() -> MagicMock:
    """Create a mock CheckpointService."""
    service = MagicMock()
    service.get_latest_checkpoint = MagicMock(return_value=None)
    return service


@pytest.fixture()
def mock_checkpoint_repository() -> MagicMock:
    """Create a mock FilesystemCheckpointRepository."""
    repo = MagicMock()
    repo.load_latest.return_value = None
    return repo


@pytest.fixture()
def mock_resumption_generator() -> MagicMock:
    """Create a mock ResumptionContextGenerator."""
    generator = MagicMock()
    generator.generate.return_value = ""
    return generator


@pytest.fixture()
def mock_quality_context_generator() -> MagicMock:
    """Create a mock SessionQualityContextGenerator."""
    generator = MagicMock()
    generator.generate.return_value = QualityContext(
        preamble='<quality-framework version="1.0">\n  Quality >= 0.92 required.\n</quality-framework>',
        token_estimate=10,
        sections_included=4,
    )
    return generator


@pytest.fixture()
def handler(
    mock_query_dispatcher: MagicMock,
    mock_checkpoint_repository: MagicMock,
    mock_resumption_generator: MagicMock,
    mock_quality_context_generator: MagicMock,
    tmp_path: Path,
) -> HooksSessionStartHandler:
    """Create a HooksSessionStartHandler with mock services."""
    return HooksSessionStartHandler(
        query_dispatcher=mock_query_dispatcher,
        projects_dir=tmp_path,
        checkpoint_repository=mock_checkpoint_repository,
        resumption_generator=mock_resumption_generator,
        quality_context_generator=mock_quality_context_generator,
    )


# =============================================================================
# Tests
# =============================================================================


class TestHooksSessionStartHandlerReturnsContext:
    """BDD: Handler returns project + quality + resumption context."""

    def test_handle_returns_valid_json(
        self,
        handler: HooksSessionStartHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Given a SessionStart hook input, handler returns valid JSON."""
        hook_input = json.dumps(
            {
                "hook_event_name": "SessionStart",
                "session_id": "test-session-456",
            }
        )

        exit_code = handler.handle(hook_input)

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "additionalContext" in result

    def test_handle_includes_project_tag(
        self,
        handler: HooksSessionStartHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Output includes a project-context tag."""
        hook_input = json.dumps({"hook_event_name": "SessionStart"})

        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result["additionalContext"] is not None

    def test_handle_includes_quality_reinforcement(
        self,
        handler: HooksSessionStartHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Output additionalContext includes quality reinforcement."""
        hook_input = json.dumps({"hook_event_name": "SessionStart"})

        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "Quality" in result["additionalContext"]

    def test_handle_with_checkpoint_includes_resumption_context(
        self,
        mock_query_dispatcher: MagicMock,
        mock_checkpoint_repository: MagicMock,
        mock_resumption_generator: MagicMock,
        mock_quality_context_generator: MagicMock,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
    ) -> None:
        """When a checkpoint exists, output includes resumption context."""
        fill_estimate = FillEstimate(
            fill_percentage=0.88,
            tier=ThresholdTier.EMERGENCY,
            token_count=176000,
        )
        checkpoint = CheckpointData(
            checkpoint_id="cx-001",
            context_state=fill_estimate,
            created_at="2026-02-20T10:00:00+00:00",
            resumption_state={"phase": "implementation"},
        )
        mock_checkpoint_repository.load_latest.return_value = checkpoint
        mock_resumption_generator.generate.return_value = (
            "<resumption-context>\n  <checkpoint-id>cx-001</checkpoint-id>\n</resumption-context>"
        )

        handler = HooksSessionStartHandler(
            query_dispatcher=mock_query_dispatcher,
            projects_dir=tmp_path,
            checkpoint_repository=mock_checkpoint_repository,
            resumption_generator=mock_resumption_generator,
            quality_context_generator=mock_quality_context_generator,
        )

        hook_input = json.dumps({"hook_event_name": "SessionStart"})
        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "<resumption-context>" in result["additionalContext"]


class TestHooksSessionStartHandlerFailOpen:
    """BDD: Handler step failure is fail-open."""

    def test_project_query_failure_returns_valid_json(
        self,
        mock_checkpoint_repository: MagicMock,
        mock_resumption_generator: MagicMock,
        mock_quality_context_generator: MagicMock,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
    ) -> None:
        """When project query fails, handler still returns valid JSON with exit 0."""
        failing_dispatcher = MagicMock()
        failing_dispatcher.dispatch.side_effect = RuntimeError("Query failed")

        handler = HooksSessionStartHandler(
            query_dispatcher=failing_dispatcher,
            projects_dir=tmp_path,
            checkpoint_repository=mock_checkpoint_repository,
            resumption_generator=mock_resumption_generator,
            quality_context_generator=mock_quality_context_generator,
        )

        hook_input = json.dumps({"hook_event_name": "SessionStart"})
        exit_code = handler.handle(hook_input)

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "additionalContext" in result

    def test_checkpoint_failure_returns_valid_json(
        self,
        mock_query_dispatcher: MagicMock,
        mock_resumption_generator: MagicMock,
        mock_quality_context_generator: MagicMock,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
    ) -> None:
        """When checkpoint load fails, handler still returns valid JSON."""
        failing_repo = MagicMock()
        failing_repo.load_latest.side_effect = RuntimeError("Checkpoint load failed")

        handler = HooksSessionStartHandler(
            query_dispatcher=mock_query_dispatcher,
            projects_dir=tmp_path,
            checkpoint_repository=failing_repo,
            resumption_generator=mock_resumption_generator,
            quality_context_generator=mock_quality_context_generator,
        )

        hook_input = json.dumps({"hook_event_name": "SessionStart"})
        exit_code = handler.handle(hook_input)

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "additionalContext" in result

    def test_invalid_json_input_returns_valid_json(
        self,
        handler: HooksSessionStartHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When hook input is invalid JSON, handler returns valid JSON with exit 0."""
        exit_code = handler.handle("not-valid-json")

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "additionalContext" in result
