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

from src.context_monitoring.application.ports.context_state import ContextState
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
    repo.get_latest_unacknowledged.return_value = None
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
        mock_checkpoint_repository.get_latest_unacknowledged.return_value = checkpoint
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
        failing_repo.get_latest_unacknowledged.side_effect = RuntimeError("Checkpoint load failed")

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

    # =============================================================================
    # BDD Scenario: TASK-002 WORKTRACKER.md auto-injection
    # =============================================================================

    def test_none_stdin_returns_valid_json(
        self,
        handler: HooksSessionStartHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """FOS-001: None stdin (TypeError) still returns valid JSON with exit 0."""
        exit_code = handler.handle(None)  # type: ignore[arg-type]

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "additionalContext" in result


class TestWorktrackerAutoInjection:
    """Scenario: Handler injects WORKTRACKER.md into additionalContext.

    TASK-002: When WORKTRACKER.md exists for the active project, its content
    is included in the additionalContext wrapped in <worktracker> XML tags.
    """

    def test_worktracker_injected_when_present(
        self,
        mock_query_dispatcher: MagicMock,
        mock_checkpoint_repository: MagicMock,
        mock_resumption_generator: MagicMock,
        mock_quality_context_generator: MagicMock,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """WORKTRACKER.md content appears in additionalContext when file exists."""
        # Set up project environment
        monkeypatch.setenv("JERRY_PROJECT", "PROJ-004-context-resilience")
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))

        # Create WORKTRACKER.md
        projects_dir = tmp_path / "projects" / "PROJ-004-context-resilience"
        projects_dir.mkdir(parents=True)
        worktracker = projects_dir / "WORKTRACKER.md"
        worktracker.write_text("# WORKTRACKER\n\n- EN-008: pending\n", encoding="utf-8")

        handler = HooksSessionStartHandler(
            query_dispatcher=mock_query_dispatcher,
            projects_dir=str(tmp_path),
            checkpoint_repository=mock_checkpoint_repository,
            resumption_generator=mock_resumption_generator,
            quality_context_generator=mock_quality_context_generator,
        )

        hook_input = json.dumps({"hook_event_name": "SessionStart"})
        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "<worktracker>" in result["additionalContext"]
        assert "EN-008: pending" in result["additionalContext"]
        assert "</worktracker>" in result["additionalContext"]

    def test_worktracker_not_injected_without_jerry_project(
        self,
        mock_query_dispatcher: MagicMock,
        mock_checkpoint_repository: MagicMock,
        mock_resumption_generator: MagicMock,
        mock_quality_context_generator: MagicMock,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """WORKTRACKER.md is not injected when JERRY_PROJECT is not set."""
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        handler = HooksSessionStartHandler(
            query_dispatcher=mock_query_dispatcher,
            projects_dir=str(tmp_path),
            checkpoint_repository=mock_checkpoint_repository,
            resumption_generator=mock_resumption_generator,
            quality_context_generator=mock_quality_context_generator,
        )

        hook_input = json.dumps({"hook_event_name": "SessionStart"})
        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "<worktracker>" not in result["additionalContext"]

    def test_worktracker_not_injected_when_file_missing(
        self,
        mock_query_dispatcher: MagicMock,
        mock_checkpoint_repository: MagicMock,
        mock_resumption_generator: MagicMock,
        mock_quality_context_generator: MagicMock,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """WORKTRACKER.md is not injected when the file does not exist."""
        monkeypatch.setenv("JERRY_PROJECT", "PROJ-004-context-resilience")
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
        # Do NOT create the file

        handler = HooksSessionStartHandler(
            query_dispatcher=mock_query_dispatcher,
            projects_dir=str(tmp_path),
            checkpoint_repository=mock_checkpoint_repository,
            resumption_generator=mock_resumption_generator,
            quality_context_generator=mock_quality_context_generator,
        )

        hook_input = json.dumps({"hook_event_name": "SessionStart"})
        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "<worktracker>" not in result["additionalContext"]

    def test_worktracker_truncated_when_large(
        self,
        mock_query_dispatcher: MagicMock,
        mock_checkpoint_repository: MagicMock,
        mock_resumption_generator: MagicMock,
        mock_quality_context_generator: MagicMock,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """WORKTRACKER.md content is truncated at 4000 chars to prevent context bloat."""
        monkeypatch.setenv("JERRY_PROJECT", "PROJ-004-context-resilience")
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))

        projects_dir = tmp_path / "projects" / "PROJ-004-context-resilience"
        projects_dir.mkdir(parents=True)
        worktracker = projects_dir / "WORKTRACKER.md"
        # Write content larger than 4000 chars
        large_content = "# WORKTRACKER\n" + ("x" * 5000)
        worktracker.write_text(large_content, encoding="utf-8")

        handler = HooksSessionStartHandler(
            query_dispatcher=mock_query_dispatcher,
            projects_dir=str(tmp_path),
            checkpoint_repository=mock_checkpoint_repository,
            resumption_generator=mock_resumption_generator,
            quality_context_generator=mock_quality_context_generator,
        )

        hook_input = json.dumps({"hook_event_name": "SessionStart"})
        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "<worktracker>" in result["additionalContext"]
        assert "... (truncated)" in result["additionalContext"]

    def test_worktracker_empty_file_not_injected(
        self,
        mock_query_dispatcher: MagicMock,
        mock_checkpoint_repository: MagicMock,
        mock_resumption_generator: MagicMock,
        mock_quality_context_generator: MagicMock,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Empty WORKTRACKER.md is not injected."""
        monkeypatch.setenv("JERRY_PROJECT", "PROJ-004-context-resilience")
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))

        projects_dir = tmp_path / "projects" / "PROJ-004-context-resilience"
        projects_dir.mkdir(parents=True)
        worktracker = projects_dir / "WORKTRACKER.md"
        worktracker.write_text("   \n  \n", encoding="utf-8")

        handler = HooksSessionStartHandler(
            query_dispatcher=mock_query_dispatcher,
            projects_dir=str(tmp_path),
            checkpoint_repository=mock_checkpoint_repository,
            resumption_generator=mock_resumption_generator,
            quality_context_generator=mock_quality_context_generator,
        )

        hook_input = json.dumps({"hook_event_name": "SessionStart"})
        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "<worktracker>" not in result["additionalContext"]

    def test_worktracker_fail_open_on_read_error(
        self,
        mock_query_dispatcher: MagicMock,
        mock_checkpoint_repository: MagicMock,
        mock_resumption_generator: MagicMock,
        mock_quality_context_generator: MagicMock,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Handler still returns valid JSON even if WORKTRACKER.md read fails."""
        monkeypatch.setenv("JERRY_PROJECT", "PROJ-004-context-resilience")
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))

        # Create a directory where a file is expected (causes read error)
        projects_dir = tmp_path / "projects" / "PROJ-004-context-resilience"
        projects_dir.mkdir(parents=True)
        worktracker_as_dir = projects_dir / "WORKTRACKER.md"
        worktracker_as_dir.mkdir()  # This will cause IsADirectoryError on read

        handler = HooksSessionStartHandler(
            query_dispatcher=mock_query_dispatcher,
            projects_dir=str(tmp_path),
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

    def test_worktracker_xml_special_chars_escaped(
        self,
        mock_query_dispatcher: MagicMock,
        mock_checkpoint_repository: MagicMock,
        mock_resumption_generator: MagicMock,
        mock_quality_context_generator: MagicMock,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """XML special characters in WORKTRACKER.md are escaped."""
        monkeypatch.setenv("JERRY_PROJECT", "PROJ-004-context-resilience")
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))

        projects_dir = tmp_path / "projects" / "PROJ-004-context-resilience"
        projects_dir.mkdir(parents=True)
        worktracker = projects_dir / "WORKTRACKER.md"
        worktracker.write_text("# WORKTRACKER\n\n- task: x < y & z > 0\n", encoding="utf-8")

        handler = HooksSessionStartHandler(
            query_dispatcher=mock_query_dispatcher,
            projects_dir=str(tmp_path),
            checkpoint_repository=mock_checkpoint_repository,
            resumption_generator=mock_resumption_generator,
            quality_context_generator=mock_quality_context_generator,
        )

        hook_input = json.dumps({"hook_event_name": "SessionStart"})
        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        ctx = result["additionalContext"]
        assert "<worktracker>" in ctx
        assert "&lt;" in ctx
        assert "&amp;" in ctx
        assert "&gt;" in ctx


# =============================================================================
# EN-016: Compaction/Clear detection from state file
# =============================================================================


def _make_state(
    *,
    previous_session_id: str = "session-abc-123",
    last_tier: str = "CRITICAL",
    previous_tokens: int = 160000,
    last_rotation_action: str = "CHECKPOINT",
) -> ContextState:
    """Helper to create ContextState for tests."""
    return ContextState(
        previous_tokens=previous_tokens,
        previous_session_id=previous_session_id,
        last_tier=last_tier,
        last_rotation_action=last_rotation_action,
    )


class TestCompactionDetection:
    """BDD: Handler detects compaction from state file and injects notice."""

    def test_compaction_detected_same_session_id(
        self,
        mock_query_dispatcher: MagicMock,
        mock_checkpoint_repository: MagicMock,
        mock_resumption_generator: MagicMock,
        mock_quality_context_generator: MagicMock,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
    ) -> None:
        """When session_id matches state file, inject <compaction-notice>."""
        mock_state_store = MagicMock()
        mock_state_store.load.return_value = _make_state(
            previous_session_id="session-xyz",
            last_tier="CRITICAL",
            previous_tokens=160000,
        )

        handler = HooksSessionStartHandler(
            query_dispatcher=mock_query_dispatcher,
            projects_dir=str(tmp_path),
            checkpoint_repository=mock_checkpoint_repository,
            resumption_generator=mock_resumption_generator,
            quality_context_generator=mock_quality_context_generator,
            context_state_store=mock_state_store,
        )

        hook_input = json.dumps({"hook_event_name": "SessionStart", "session_id": "session-xyz"})
        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        ctx = result["additionalContext"]
        assert "<compaction-notice>" in ctx
        assert "CRITICAL" in ctx
        assert "160000" in ctx
        assert "Re-read ORCHESTRATION.yaml" in ctx

    def test_clear_detected_different_session_id(
        self,
        mock_query_dispatcher: MagicMock,
        mock_checkpoint_repository: MagicMock,
        mock_resumption_generator: MagicMock,
        mock_quality_context_generator: MagicMock,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
    ) -> None:
        """When session_id differs from state file, inject <session-reset>."""
        mock_state_store = MagicMock()
        mock_state_store.load.return_value = _make_state(
            previous_session_id="old-session",
            last_tier="WARNING",
        )

        handler = HooksSessionStartHandler(
            query_dispatcher=mock_query_dispatcher,
            projects_dir=str(tmp_path),
            checkpoint_repository=mock_checkpoint_repository,
            resumption_generator=mock_resumption_generator,
            quality_context_generator=mock_quality_context_generator,
            context_state_store=mock_state_store,
        )

        hook_input = json.dumps({"hook_event_name": "SessionStart", "session_id": "new-session"})
        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        ctx = result["additionalContext"]
        assert "<session-reset>" in ctx
        assert "WARNING" in ctx
        assert "New session started" in ctx

    def test_no_state_file_no_notice(
        self,
        mock_query_dispatcher: MagicMock,
        mock_checkpoint_repository: MagicMock,
        mock_resumption_generator: MagicMock,
        mock_quality_context_generator: MagicMock,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
    ) -> None:
        """When state file doesn't exist, no compaction/clear notice injected."""
        mock_state_store = MagicMock()
        mock_state_store.load.return_value = None

        handler = HooksSessionStartHandler(
            query_dispatcher=mock_query_dispatcher,
            projects_dir=str(tmp_path),
            checkpoint_repository=mock_checkpoint_repository,
            resumption_generator=mock_resumption_generator,
            quality_context_generator=mock_quality_context_generator,
            context_state_store=mock_state_store,
        )

        hook_input = json.dumps({"hook_event_name": "SessionStart", "session_id": "any-session"})
        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        ctx = result["additionalContext"]
        assert "<compaction-notice>" not in ctx
        assert "<session-reset>" not in ctx

    def test_no_state_store_backward_compatible(
        self,
        handler: HooksSessionStartHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Without state store, handler works as before (no notice)."""
        hook_input = json.dumps({"hook_event_name": "SessionStart", "session_id": "any-session"})

        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        ctx = result["additionalContext"]
        assert "<compaction-notice>" not in ctx
        assert "<session-reset>" not in ctx

    def test_state_store_failure_is_fail_open(
        self,
        mock_query_dispatcher: MagicMock,
        mock_checkpoint_repository: MagicMock,
        mock_resumption_generator: MagicMock,
        mock_quality_context_generator: MagicMock,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
    ) -> None:
        """When state store read fails, handler continues without notice."""
        mock_state_store = MagicMock()
        mock_state_store.load.side_effect = RuntimeError("State read failed")

        handler = HooksSessionStartHandler(
            query_dispatcher=mock_query_dispatcher,
            projects_dir=str(tmp_path),
            checkpoint_repository=mock_checkpoint_repository,
            resumption_generator=mock_resumption_generator,
            quality_context_generator=mock_quality_context_generator,
            context_state_store=mock_state_store,
        )

        hook_input = json.dumps({"hook_event_name": "SessionStart", "session_id": "any-session"})
        exit_code = handler.handle(hook_input)

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "additionalContext" in result
        assert "State read failed" in captured.err

    def test_no_session_id_in_hook_input_no_notice(
        self,
        mock_query_dispatcher: MagicMock,
        mock_checkpoint_repository: MagicMock,
        mock_resumption_generator: MagicMock,
        mock_quality_context_generator: MagicMock,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
    ) -> None:
        """When hook input has no session_id, no compaction/clear notice."""
        mock_state_store = MagicMock()
        mock_state_store.load.return_value = _make_state()

        handler = HooksSessionStartHandler(
            query_dispatcher=mock_query_dispatcher,
            projects_dir=str(tmp_path),
            checkpoint_repository=mock_checkpoint_repository,
            resumption_generator=mock_resumption_generator,
            quality_context_generator=mock_quality_context_generator,
            context_state_store=mock_state_store,
        )

        hook_input = json.dumps({"hook_event_name": "SessionStart"})
        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        ctx = result["additionalContext"]
        assert "<compaction-notice>" not in ctx
        assert "<session-reset>" not in ctx

    def test_empty_previous_session_id_in_state_no_notice(
        self,
        mock_query_dispatcher: MagicMock,
        mock_checkpoint_repository: MagicMock,
        mock_resumption_generator: MagicMock,
        mock_quality_context_generator: MagicMock,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
    ) -> None:
        """When state has empty previous_session_id, no notice injected."""
        mock_state_store = MagicMock()
        mock_state_store.load.return_value = _make_state(previous_session_id="")

        handler = HooksSessionStartHandler(
            query_dispatcher=mock_query_dispatcher,
            projects_dir=str(tmp_path),
            checkpoint_repository=mock_checkpoint_repository,
            resumption_generator=mock_resumption_generator,
            quality_context_generator=mock_quality_context_generator,
            context_state_store=mock_state_store,
        )

        hook_input = json.dumps({"hook_event_name": "SessionStart", "session_id": "any-session"})
        handler.handle(hook_input)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        ctx = result["additionalContext"]
        assert "<compaction-notice>" not in ctx
        assert "<session-reset>" not in ctx
