# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for engagement gate decision function (TASK-023-146).

BDD RED phase: tests written before implementation per H-20.
Covers two-factor authorization (RT-001/CC-004):
  Factor 1: E2E-* engagement ID prefix
  Factor 2: e2e_mode: true in engagement config

References:
    - TASK-023-146: Gate decision function
    - FEAT-023-015: Engagement Gate System
"""

from __future__ import annotations

import pytest

from src.proxy_infra.domain.value_objects.full_engagement_config import (
    EngagementMetadata,
    FullEngagementConfig,
    ScopeConfig,
)
from src.proxy_infra.domain.value_objects.gate_approval_mode import GateApprovalMode


def _make_config(
    engagement_id: str = "E2E-RAINBOW-001",
    e2e_mode: bool = True,
) -> FullEngagementConfig:
    """Build a minimal FullEngagementConfig for gate testing."""
    return FullEngagementConfig(
        engagement=EngagementMetadata(
            id=engagement_id,
            name="Test Engagement",
            type="penetration_test",
            mode="single",
            start_date="2026-03-29",
            e2e_mode=e2e_mode,
        ),
        scope=ScopeConfig(targets=["10.0.0.1"]),
    )


class TestGateApprovalModeTwoFactor:
    """Two-factor authorization: BOTH E2E-* prefix AND e2e_mode required."""

    def test_both_factors_present_returns_pre_approved(self) -> None:
        """Both E2E-* prefix AND e2e_mode=True -> PRE_APPROVED."""
        from src.proxy_infra.domain.services.engagement_gate import gate_approval_mode

        config = _make_config(engagement_id="E2E-RAINBOW-001", e2e_mode=True)
        result = gate_approval_mode(config.engagement.id, config)
        assert result == GateApprovalMode.PRE_APPROVED

    def test_prefix_only_without_e2e_mode_returns_human_approval(self) -> None:
        """E2E-* prefix but e2e_mode=False -> HUMAN_APPROVAL."""
        from src.proxy_infra.domain.services.engagement_gate import gate_approval_mode

        config = _make_config(engagement_id="E2E-RAINBOW-001", e2e_mode=False)
        result = gate_approval_mode(config.engagement.id, config)
        assert result == GateApprovalMode.HUMAN_APPROVAL

    def test_e2e_mode_only_without_prefix_returns_human_approval(self) -> None:
        """e2e_mode=True but no E2E-* prefix -> HUMAN_APPROVAL."""
        from src.proxy_infra.domain.services.engagement_gate import gate_approval_mode

        config = _make_config(engagement_id="RED-0003", e2e_mode=True)
        result = gate_approval_mode(config.engagement.id, config)
        assert result == GateApprovalMode.HUMAN_APPROVAL

    def test_neither_factor_returns_human_approval(self) -> None:
        """No prefix, no e2e_mode -> HUMAN_APPROVAL."""
        from src.proxy_infra.domain.services.engagement_gate import gate_approval_mode

        config = _make_config(engagement_id="RED-0003", e2e_mode=False)
        result = gate_approval_mode(config.engagement.id, config)
        assert result == GateApprovalMode.HUMAN_APPROVAL


class TestGateApprovalModeBoundary:
    """Boundary cases: all must fail-safe to HUMAN_APPROVAL."""

    @pytest.mark.parametrize(
        "engagement_id",
        [
            "",  # empty string
            "E2E",  # no dash
            "e2e-lower",  # lowercase
            "E2E-",  # empty suffix
        ],
        ids=["empty_string", "no_dash", "lowercase", "empty_suffix"],
    )
    def test_invalid_prefix_with_e2e_mode_returns_human_approval(self, engagement_id: str) -> None:
        """Invalid prefix patterns fail-safe to HUMAN_APPROVAL even with e2e_mode."""
        from src.proxy_infra.domain.services.engagement_gate import gate_approval_mode

        # For empty string, we need special config since empty id raises ValueError
        if engagement_id == "":
            # Empty engagement_id triggers domain invariant -- test that gate function
            # handles it gracefully by returning HUMAN_APPROVAL
            config = _make_config(engagement_id="PLACEHOLDER", e2e_mode=True)
            result = gate_approval_mode("", config)
        else:
            config = _make_config(engagement_id=engagement_id, e2e_mode=True)
            result = gate_approval_mode(config.engagement.id, config)
        assert result == GateApprovalMode.HUMAN_APPROVAL

    def test_e2e_mode_field_absent_defaults_to_false(self) -> None:
        """Config without explicit e2e_mode defaults to False -> HUMAN_APPROVAL."""
        from src.proxy_infra.domain.services.engagement_gate import gate_approval_mode

        # EngagementMetadata defaults e2e_mode=False when not specified
        config = FullEngagementConfig(
            engagement=EngagementMetadata(
                id="E2E-TEST-001",
                name="Test",
                type="penetration_test",
                mode="single",
                start_date="2026-03-29",
                # e2e_mode NOT specified — defaults to False
            ),
            scope=ScopeConfig(targets=["10.0.0.1"]),
        )
        result = gate_approval_mode(config.engagement.id, config)
        assert result == GateApprovalMode.HUMAN_APPROVAL


class TestGateApprovalModePurity:
    """The function is pure: no side effects, deterministic."""

    def test_same_input_same_output(self) -> None:
        """Calling with identical inputs produces identical outputs."""
        from src.proxy_infra.domain.services.engagement_gate import gate_approval_mode

        config = _make_config(engagement_id="E2E-RAINBOW-001", e2e_mode=True)
        result1 = gate_approval_mode(config.engagement.id, config)
        result2 = gate_approval_mode(config.engagement.id, config)
        assert result1 == result2 == GateApprovalMode.PRE_APPROVED

    def test_valid_e2e_prefix_variations(self) -> None:
        """Various valid E2E-* prefixes with e2e_mode should all pre-approve."""
        from src.proxy_infra.domain.services.engagement_gate import gate_approval_mode

        for eid in ["E2E-RAINBOW-001", "E2E-SMOKE-TEST", "E2E-X"]:
            config = _make_config(engagement_id=eid, e2e_mode=True)
            result = gate_approval_mode(config.engagement.id, config)
            assert result == GateApprovalMode.PRE_APPROVED, f"Failed for {eid}"
