# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Tests for HooksStopGateHandler CLI handler.

BDD scenarios from EN-014:
    - EMERGENCY tier blocks Claude from stopping (decision=block)
    - CRITICAL tier allows stop (decision=approve)
    - WARNING tier allows stop
    - NOMINAL tier allows stop
    - No state file allows stop (fail-open)
    - State file read failure allows stop (fail-open)
    - Always returns exit code 0
    - Block response includes reason and systemMessage

References:
    - EN-014: Stop Hook Gate (context-stop-gate.py)
    - ST-006: Automatic Session Rotation
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from src.context_monitoring.application.ports.context_state import ContextState
from src.interface.cli.hooks.hooks_stop_gate_handler import HooksStopGateHandler

# =============================================================================
# Fixtures
# =============================================================================


def _make_state(*, tier: str = "nominal", tokens: int = 50000) -> ContextState:
    return ContextState(
        previous_tokens=tokens,
        previous_session_id="sess-1",
        last_tier=tier,
        last_rotation_action="none",
    )


@pytest.fixture()
def mock_state_store() -> MagicMock:
    """Create a mock IContextStateStore returning NOMINAL state."""
    store = MagicMock()
    store.load.return_value = _make_state(tier="nominal")
    return store


@pytest.fixture()
def handler(mock_state_store: MagicMock) -> HooksStopGateHandler:
    """Create a HooksStopGateHandler with mock state store."""
    return HooksStopGateHandler(context_state_store=mock_state_store)


# =============================================================================
# EMERGENCY tier blocks stop
# =============================================================================


class TestEmergencyBlocks:
    """BDD: EMERGENCY tier blocks Claude from stopping."""

    def test_emergency_tier_blocks_stop(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """EMERGENCY tier returns decision=block."""
        store = MagicMock()
        store.load.return_value = _make_state(tier="emergency", tokens=180000)

        handler = HooksStopGateHandler(context_state_store=store)
        exit_code = handler.handle("{}")

        assert exit_code == 0
        output = json.loads(capsys.readouterr().out)
        assert output["decision"] == "block"

    def test_emergency_block_includes_reason(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """EMERGENCY block response includes reason with action guidance."""
        store = MagicMock()
        store.load.return_value = _make_state(tier="emergency", tokens=180000)

        handler = HooksStopGateHandler(context_state_store=store)
        handler.handle("{}")

        output = json.loads(capsys.readouterr().out)
        assert "reason" in output
        assert "/compact" in output["reason"]
        assert "/clear" in output["reason"]

    def test_emergency_block_includes_system_message(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """EMERGENCY block response includes systemMessage for context."""
        store = MagicMock()
        store.load.return_value = _make_state(tier="emergency", tokens=180000)

        handler = HooksStopGateHandler(context_state_store=store)
        handler.handle("{}")

        output = json.loads(capsys.readouterr().out)
        assert "systemMessage" in output
        assert "EMERGENCY" in output["systemMessage"]


# =============================================================================
# Non-emergency tiers allow stop
# =============================================================================


class TestNonEmergencyAllows:
    """BDD: Non-emergency tiers allow Claude to stop."""

    def test_critical_allows_stop(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """CRITICAL tier allows stop (only EMERGENCY blocks)."""
        store = MagicMock()
        store.load.return_value = _make_state(tier="critical", tokens=165000)

        handler = HooksStopGateHandler(context_state_store=store)
        exit_code = handler.handle("{}")

        assert exit_code == 0
        output = json.loads(capsys.readouterr().out)
        assert output["decision"] == "approve"

    def test_warning_allows_stop(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """WARNING tier allows stop."""
        store = MagicMock()
        store.load.return_value = _make_state(tier="warning", tokens=140000)

        handler = HooksStopGateHandler(context_state_store=store)
        handler.handle("{}")

        output = json.loads(capsys.readouterr().out)
        assert output["decision"] == "approve"

    def test_nominal_allows_stop(
        self,
        handler: HooksStopGateHandler,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """NOMINAL tier allows stop."""
        handler.handle("{}")

        output = json.loads(capsys.readouterr().out)
        assert output["decision"] == "approve"


# =============================================================================
# Fail-open behavior
# =============================================================================


class TestFailOpen:
    """BDD: Handler is fail-open — always allows stop on errors."""

    def test_no_state_file_allows_stop(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When state file doesn't exist, allows stop."""
        store = MagicMock()
        store.load.return_value = None

        handler = HooksStopGateHandler(context_state_store=store)
        exit_code = handler.handle("{}")

        assert exit_code == 0
        output = json.loads(capsys.readouterr().out)
        assert output["decision"] == "approve"

    def test_state_read_failure_allows_stop(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When state store throws, allows stop (fail-open)."""
        store = MagicMock()
        store.load.side_effect = RuntimeError("disk error")

        handler = HooksStopGateHandler(context_state_store=store)
        exit_code = handler.handle("{}")

        assert exit_code == 0
        output = json.loads(capsys.readouterr().out)
        assert output["decision"] == "approve"

    def test_invalid_tier_in_state_allows_stop(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When state has invalid tier value, allows stop (fail-open)."""
        store = MagicMock()
        store.load.return_value = ContextState(
            previous_tokens=100000,
            previous_session_id="sess-1",
            last_tier="invalid_tier_value",
            last_rotation_action="none",
        )

        handler = HooksStopGateHandler(context_state_store=store)
        exit_code = handler.handle("{}")

        assert exit_code == 0
        output = json.loads(capsys.readouterr().out)
        assert output["decision"] == "approve"

    def test_always_returns_zero(
        self,
        handler: HooksStopGateHandler,
    ) -> None:
        """Handler always returns exit code 0."""
        exit_code = handler.handle("{}")
        assert exit_code == 0
