# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for gate integration into engagement lifecycle (TASK-023-147, 023-149).

BDD RED phase per H-20. Covers:
  - Pre-approved mode auto-proceeds at all gates
  - Human-approval mode invokes confirmation at all gates
  - Denial halts lifecycle at current gate
  - Gate transitions logged regardless of mode

References:
    - TASK-023-147: Integrate gates into lifecycle (G1-G7)
    - TASK-023-149: Operator confirmation prompts (P-020)
    - TASK-023-150: Gate timeout behavior
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.proxy_infra.domain.value_objects.gate_context import GateContext

# ---------------------------------------------------------------------------
# Gate descriptions for G1-G7 (from state-machine.md)
# ---------------------------------------------------------------------------

_GATE_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "G1": {
        "current": "DEFINED",
        "next": "PROVISIONING",
        "description": "Approve engagement scope",
    },
    "G3": {
        "current": "PROVISIONING",
        "next": "ACTIVE",
        "description": "Infrastructure ready, approve activation",
    },
    "G5": {
        "current": "REPORTING",
        "next": "TEARDOWN",
        "description": "Review report, approve teardown",
    },
    "G6": {
        "current": "TEARDOWN",
        "next": "ARCHIVED",
        "description": "Confirm teardown and archive",
    },
}


# ---------------------------------------------------------------------------
# Gated lifecycle manager tests
# ---------------------------------------------------------------------------


class TestGatedLifecyclePreApproved:
    """E2E-* engagements with e2e_mode auto-approve all gates."""

    def test_approve_scope_auto_proceeds_when_pre_approved(self, tmp_path: Path) -> None:
        """G1: DEFINED -> PROVISIONING auto-proceeds for E2E-*."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )

        confirmation = MagicMock()
        manager = GatedLifecycleManager(
            engagement_dir=tmp_path,
            confirmation_port=confirmation,
        )
        state = _create_e2e_engagement(manager, tmp_path)

        result = manager.approve_scope(state.engagement_id)

        assert result.current_state == "PROVISIONING"
        confirmation.request_approval.assert_not_called()

    def test_activate_auto_proceeds_when_pre_approved(self, tmp_path: Path) -> None:
        """G3: PROVISIONING -> ACTIVE auto-proceeds for E2E-*."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )

        confirmation = MagicMock()
        manager = GatedLifecycleManager(
            engagement_dir=tmp_path,
            confirmation_port=confirmation,
        )
        state = _create_e2e_engagement(manager, tmp_path)
        manager.approve_scope(state.engagement_id)

        result = manager.activate(state.engagement_id)

        assert result.current_state == "ACTIVE"
        confirmation.request_approval.assert_not_called()

    def test_full_lifecycle_auto_proceeds_when_pre_approved(self, tmp_path: Path) -> None:
        """All gates auto-proceed for E2E-* engagement through full lifecycle."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )

        confirmation = MagicMock()
        manager = GatedLifecycleManager(
            engagement_dir=tmp_path,
            confirmation_port=confirmation,
        )
        state = _create_e2e_engagement(manager, tmp_path)

        manager.approve_scope(state.engagement_id)
        manager.activate(state.engagement_id)
        manager.complete_execution(state.engagement_id)
        manager.complete_analysis(state.engagement_id)
        manager.approve_report(state.engagement_id)
        result = manager.complete_teardown(state.engagement_id)

        assert result.current_state == "ARCHIVED"
        confirmation.request_approval.assert_not_called()


class TestGatedLifecycleHumanApproval:
    """Non-E2E engagements require operator confirmation at gated transitions."""

    def test_approve_scope_invokes_confirmation_when_human_approval(self, tmp_path: Path) -> None:
        """G1: DEFINED -> PROVISIONING invokes confirmation for non-E2E."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )

        confirmation = MagicMock()
        confirmation.request_approval_with_timeout.return_value = True
        manager = GatedLifecycleManager(
            engagement_dir=tmp_path,
            confirmation_port=confirmation,
        )
        state = _create_production_engagement(manager, tmp_path)

        result = manager.approve_scope(state.engagement_id)

        assert result.current_state == "PROVISIONING"
        confirmation.request_approval_with_timeout.assert_called_once()
        ctx = confirmation.request_approval_with_timeout.call_args[0][0]
        assert isinstance(ctx, GateContext)
        assert ctx.gate_id == "G1"

    def test_denial_halts_lifecycle_at_current_gate(self, tmp_path: Path) -> None:
        """Operator denial halts lifecycle — state does not change."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GateDeniedError,
            GatedLifecycleManager,
        )

        confirmation = MagicMock()
        confirmation.request_approval_with_timeout.return_value = False
        manager = GatedLifecycleManager(
            engagement_dir=tmp_path,
            confirmation_port=confirmation,
        )
        state = _create_production_engagement(manager, tmp_path)

        with pytest.raises(GateDeniedError):
            manager.approve_scope(state.engagement_id)

        # State preserved at DEFINED
        current = manager.get_state(state.engagement_id)
        assert current.current_state == "DEFINED"


class TestGateTimeout:
    """Gate timeout behavior (TASK-023-150)."""

    def test_timeout_returns_none_triggers_halt(self, tmp_path: Path) -> None:
        """Timeout at gate halts lifecycle (fail-safe, not auto-approve)."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
            GateTimeoutError,
        )

        confirmation = MagicMock()
        confirmation.request_approval_with_timeout.return_value = None
        manager = GatedLifecycleManager(
            engagement_dir=tmp_path,
            confirmation_port=confirmation,
            gate_timeout_seconds=300,
        )
        state = _create_production_engagement(manager, tmp_path)

        with pytest.raises(GateTimeoutError):
            manager.approve_scope(state.engagement_id)


class TestGateLogging:
    """Gate transitions logged regardless of approval mode."""

    def test_pre_approved_gate_logged(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Pre-approved gate transitions are logged."""
        import logging

        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )

        with caplog.at_level(logging.INFO):
            confirmation = MagicMock()
            manager = GatedLifecycleManager(
                engagement_dir=tmp_path,
                confirmation_port=confirmation,
            )
            state = _create_e2e_engagement(manager, tmp_path)
            manager.approve_scope(state.engagement_id)

        assert any("G1" in r.message and "PRE_APPROVED" in r.message for r in caplog.records)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_config(tmp_path: Path, engagement_id: str, e2e_mode: bool) -> Path:
    """Write a minimal engagement config YAML and return its path."""
    import yaml

    config_data = {
        "engagement": {
            "id": engagement_id,
            "name": "Test",
            "type": "penetration_test",
            "mode": "single",
            "start_date": "2026-03-29",
            "e2e_mode": e2e_mode,
        },
        "scope": {
            "targets": ["10.0.0.1"],
        },
    }
    config_path = tmp_path / f"{engagement_id}-config.yaml"
    config_path.write_text(yaml.dump(config_data, default_flow_style=False))
    return config_path


def _create_e2e_engagement(manager: object, tmp_path: Path) -> object:
    """Create an E2E-* engagement in DEFINED state."""
    config_path = _write_config(tmp_path, "E2E-RAINBOW-001", e2e_mode=True)
    return manager.create(config_path)  # type: ignore[union-attr]


def _create_production_engagement(manager: object, tmp_path: Path) -> object:
    """Create a production engagement in DEFINED state."""
    config_path = _write_config(tmp_path, "RED-0003", e2e_mode=False)
    return manager.create(config_path)  # type: ignore[union-attr]
