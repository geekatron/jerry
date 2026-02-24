# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Tests for ContextEstimateHandler CLI handler.

BDD scenarios from EN-012:
    - Valid Claude Code JSON produces structured JSON output
    - Empty stdin produces degraded estimate
    - Invalid JSON produces degraded estimate
    - Null current_usage (before first API call) handled gracefully
    - Full session passthrough included in output
    - Always returns exit code 0 (fail-open)
    - Compaction detected when previous state exists

References:
    - EN-012: jerry context estimate CLI Command
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.context_monitoring.application.services.context_estimate_service import (
    ContextEstimateService,
)
from src.context_monitoring.domain.services.context_estimate_computer import (
    ContextEstimateComputer,
)
from src.context_monitoring.infrastructure.adapters.filesystem_context_state_store import (
    FilesystemContextStateStore,
)
from src.interface.cli.context.context_estimate_handler import (
    ContextEstimateHandler,
)

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def handler(tmp_path: Path) -> ContextEstimateHandler:
    """Create a ContextEstimateHandler with temp state directory."""
    state_dir = tmp_path / "jerry-local"
    computer = ContextEstimateComputer()
    state_store = FilesystemContextStateStore(state_dir=state_dir)
    service = ContextEstimateService(computer, state_store)
    return ContextEstimateHandler(service)


def _claude_code_json(
    *,
    session_id: str = "abc123",
    input_tokens: int = 8500,
    cache_creation: int = 5000,
    cache_read: int = 12000,
    window_size: int = 200000,
    used_pct: float | None = 12.75,
    remaining_pct: float | None = 87.25,
    current_usage_null: bool = False,
    model_id: str = "claude-opus-4-6",
    cost_usd: float = 2.45,
) -> str:
    """Build a Claude Code status line JSON string."""
    current_usage = (
        None
        if current_usage_null
        else {
            "input_tokens": input_tokens,
            "output_tokens": 1200,
            "cache_creation_input_tokens": cache_creation,
            "cache_read_input_tokens": cache_read,
        }
    )
    data = {
        "session_id": session_id,
        "version": "1.0.80",
        "model": {"id": model_id, "display_name": "Opus"},
        "context_window": {
            "total_input_tokens": 1200000,
            "total_output_tokens": 350000,
            "context_window_size": window_size,
            "used_percentage": used_pct,
            "remaining_percentage": remaining_pct,
            "current_usage": current_usage,
        },
        "cost": {"total_cost_usd": cost_usd},
        "workspace": {
            "current_dir": "/workspace",
            "project_dir": "/workspace",
        },
    }
    return json.dumps(data)


# =============================================================================
# Valid JSON input
# =============================================================================


class TestValidInput:
    """Test handler with valid Claude Code JSON."""

    def test_returns_zero(self, handler: ContextEstimateHandler) -> None:
        """Handler always returns 0."""
        exit_code = handler.handle(_claude_code_json())
        assert exit_code == 0

    def test_output_has_context_block(
        self, handler: ContextEstimateHandler, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Output contains domain-computed context block."""
        handler.handle(_claude_code_json())
        output = json.loads(capsys.readouterr().out)

        assert "context" in output
        ctx = output["context"]
        assert ctx["used_tokens"] == 25500  # 8500 + 5000 + 12000
        assert ctx["window_size"] == 200000
        assert ctx["is_estimated"] is False
        assert "tier" in ctx
        assert "fill_percentage" in ctx

    def test_output_has_compaction_block(
        self, handler: ContextEstimateHandler, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Output contains compaction detection block."""
        handler.handle(_claude_code_json())
        output = json.loads(capsys.readouterr().out)

        assert "compaction" in output
        comp = output["compaction"]
        assert comp["detected"] is False

    def test_output_has_thresholds(
        self, handler: ContextEstimateHandler, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Output contains 5-tier threshold configuration."""
        handler.handle(_claude_code_json())
        output = json.loads(capsys.readouterr().out)

        assert "thresholds" in output
        assert "nominal" in output["thresholds"]
        assert "emergency" in output["thresholds"]

    def test_output_has_action(
        self, handler: ContextEstimateHandler, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Output contains recommended action."""
        handler.handle(_claude_code_json())
        output = json.loads(capsys.readouterr().out)

        assert "action" in output

    def test_session_passthrough(
        self, handler: ContextEstimateHandler, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Full Claude Code JSON passed through in session block."""
        handler.handle(_claude_code_json(session_id="test-session", cost_usd=5.00))
        output = json.loads(capsys.readouterr().out)

        assert "session" in output
        session = output["session"]
        assert session["session_id"] == "test-session"
        assert session["cost"]["total_cost_usd"] == 5.00
        assert session["model"]["id"] == "claude-opus-4-6"


# =============================================================================
# Fail-open: degraded input
# =============================================================================


class TestFailOpen:
    """Test fail-open behavior with degraded input."""

    def test_empty_stdin(
        self, handler: ContextEstimateHandler, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Empty stdin produces degraded estimate."""
        exit_code = handler.handle("")
        assert exit_code == 0

        output = json.loads(capsys.readouterr().out)
        assert output["context"]["is_estimated"] is True
        assert output["context"]["tier"] == "nominal"

    def test_invalid_json(
        self, handler: ContextEstimateHandler, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Invalid JSON produces degraded estimate."""
        exit_code = handler.handle("not json {{{")
        assert exit_code == 0

        output = json.loads(capsys.readouterr().out)
        assert output["context"]["is_estimated"] is True

    def test_non_dict_json(
        self, handler: ContextEstimateHandler, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """JSON array (not dict) produces degraded estimate."""
        exit_code = handler.handle("[1, 2, 3]")
        assert exit_code == 0

        output = json.loads(capsys.readouterr().out)
        assert output["context"]["is_estimated"] is True

    def test_null_current_usage(
        self, handler: ContextEstimateHandler, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Null current_usage (before first API call) handled gracefully."""
        exit_code = handler.handle(_claude_code_json(current_usage_null=True, used_pct=5.0))
        assert exit_code == 0

        output = json.loads(capsys.readouterr().out)
        # With no token data but used_pct available, fill should use percentage
        assert output["context"]["used_tokens"] == 0
        # fill_percentage should use the used_pct fallback
        assert output["context"]["fill_percentage"] == pytest.approx(0.05)

    def test_missing_context_window(
        self, handler: ContextEstimateHandler, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Missing context_window block still produces valid output."""
        exit_code = handler.handle(json.dumps({"session_id": "abc"}))
        assert exit_code == 0

        output = json.loads(capsys.readouterr().out)
        assert output["context"]["used_tokens"] == 0


# =============================================================================
# State persistence across calls
# =============================================================================


class TestStatePersistence:
    """Test cross-invocation state behavior."""

    def test_second_call_detects_compaction(
        self, handler: ContextEstimateHandler, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Second call detects compaction when tokens drop significantly."""
        # First call: high fill
        handler.handle(
            _claude_code_json(
                input_tokens=80000,
                cache_creation=50000,
                cache_read=50000,
                session_id="same-session",
            )
        )
        capsys.readouterr()  # Clear first output

        # Second call: much lower fill (same session = compaction)
        handler.handle(
            _claude_code_json(
                input_tokens=10000,
                cache_creation=5000,
                cache_read=5000,
                session_id="same-session",
            )
        )
        output = json.loads(capsys.readouterr().out)

        assert output["compaction"]["detected"] is True
        assert output["compaction"]["from_tokens"] == 180000
        assert output["compaction"]["to_tokens"] == 20000
