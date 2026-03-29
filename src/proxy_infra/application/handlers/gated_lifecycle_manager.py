# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""GatedLifecycleManager — engagement lifecycle with gate enforcement.

Wraps EngagementLifecycleManager to enforce gate checks at each transition.
Gate behavior depends on the approval mode returned by ``gate_approval_mode()``:
  PRE_APPROVED: gate auto-proceeds without operator prompt.
  HUMAN_APPROVAL: gate invokes the OperatorConfirmationPort for approval.

Design constraints:
    H-07: Application layer — imports domain only.
    H-10: One public class per file.

References:
    - TASK-023-147: Integrate gates into lifecycle (G1-G7)
    - TASK-023-149: Operator confirmation prompts (P-020)
    - TASK-023-150: Gate timeout behavior
    - FEAT-023-015: Engagement Gate System
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from src.proxy_infra.application.handlers.engagement_lifecycle_manager import (
    EngagementLifecycleManager,
)
from src.proxy_infra.application.handlers.engagement_state import EngagementState
from src.proxy_infra.domain.exceptions.gate_denied_error import GateDeniedError
from src.proxy_infra.domain.exceptions.gate_timeout_error import GateTimeoutError
from src.proxy_infra.domain.services.engagement_gate import gate_approval_mode
from src.proxy_infra.domain.value_objects.gate_approval_mode import GateApprovalMode
from src.proxy_infra.domain.value_objects.gate_context import GateContext

if TYPE_CHECKING:
    from src.proxy_infra.domain.ports.operator_confirmation_port import (
        OperatorConfirmationPort,
    )
    from src.proxy_infra.domain.value_objects.full_engagement_config import (
        FullEngagementConfig,
    )

# Re-export errors so tests can import from this module.
__all__ = ["GatedLifecycleManager", "GateDeniedError", "GateTimeoutError"]

logger = logging.getLogger(__name__)

#: Default gate timeout in seconds (5 minutes).
_DEFAULT_GATE_TIMEOUT = 300

#: Gate definitions: gate_id -> (current_state, next_state, description).
_GATES: dict[str, tuple[str, str, str]] = {
    "G1": ("DEFINED", "PROVISIONING", "Approve engagement scope"),
    "G3": ("PROVISIONING", "ACTIVE", "Infrastructure ready — approve activation"),
    "G5": ("REPORTING", "TEARDOWN", "Review report — approve teardown"),
    "G6": ("TEARDOWN", "ARCHIVED", "Confirm teardown and archive"),
}


class GatedLifecycleManager:
    """Engagement lifecycle manager with gate enforcement at transitions.

    Delegates state management to EngagementLifecycleManager and adds
    gate checks before gated transitions (G1, G3, G5, G6). Non-gated
    transitions (ACTIVE->ANALYZING, ANALYZING->REPORTING) pass through
    without gate checks.

    Args:
        engagement_dir: Base directory for engagement artifacts.
        confirmation_port: Port for operator confirmation prompts.
        gate_timeout_seconds: Timeout for human approval gates.
    """

    def __init__(
        self,
        engagement_dir: Path,
        confirmation_port: OperatorConfirmationPort,
        gate_timeout_seconds: int = _DEFAULT_GATE_TIMEOUT,
    ) -> None:
        """Initialize with lifecycle manager and confirmation port.

        Args:
            engagement_dir: Base directory for engagements.
            confirmation_port: Adapter for operator confirmation.
            gate_timeout_seconds: Timeout for human gates.
        """
        self._lifecycle = EngagementLifecycleManager(engagement_dir)
        self._confirmation = confirmation_port
        self._gate_timeout = gate_timeout_seconds
        self._configs: dict[str, FullEngagementConfig] = {}

    def create(self, config_path: Path) -> EngagementState:
        """Create engagement and cache its config for gate decisions.

        Args:
            config_path: Path to engagement config YAML.

        Returns:
            EngagementState in DEFINED state.
        """
        state = self._lifecycle.create(config_path)
        from src.proxy_infra.application.handlers.full_engagement_config_parser import (
            FullEngagementConfigParser,
        )

        config = FullEngagementConfigParser().parse(config_path)
        self._configs[state.engagement_id] = config
        return state

    def approve_scope(self, engagement_id: str) -> EngagementState:
        """G1: DEFINED -> PROVISIONING with gate check.

        Args:
            engagement_id: Engagement identifier.

        Returns:
            Updated EngagementState.

        Raises:
            GateDeniedError: If operator denies the gate.
            GateTimeoutError: If gate times out.
        """
        self._check_gate("G1", engagement_id, "DEFINED", "PROVISIONING")
        return self._lifecycle.approve_scope(engagement_id)

    def activate(self, engagement_id: str) -> EngagementState:
        """G3: PROVISIONING -> ACTIVE with gate check.

        Args:
            engagement_id: Engagement identifier.

        Returns:
            Updated EngagementState.

        Raises:
            GateDeniedError: If operator denies the gate.
            GateTimeoutError: If gate times out.
        """
        self._check_gate("G3", engagement_id, "PROVISIONING", "ACTIVE")
        return self._lifecycle.activate(engagement_id)

    def complete_execution(self, engagement_id: str) -> EngagementState:
        """ACTIVE -> ANALYZING (no gate — automatic transition).

        Args:
            engagement_id: Engagement identifier.

        Returns:
            Updated EngagementState.
        """
        return self._lifecycle.complete_execution(engagement_id)

    def complete_analysis(self, engagement_id: str) -> EngagementState:
        """ANALYZING -> REPORTING (no gate — automatic transition).

        Args:
            engagement_id: Engagement identifier.

        Returns:
            Updated EngagementState.
        """
        return self._lifecycle.complete_analysis(engagement_id)

    def approve_report(self, engagement_id: str) -> EngagementState:
        """G5: REPORTING -> TEARDOWN with gate check.

        Args:
            engagement_id: Engagement identifier.

        Returns:
            Updated EngagementState.

        Raises:
            GateDeniedError: If operator denies the gate.
            GateTimeoutError: If gate times out.
        """
        self._check_gate("G5", engagement_id, "REPORTING", "TEARDOWN")
        return self._lifecycle.approve_report(engagement_id)

    def complete_teardown(self, engagement_id: str) -> EngagementState:
        """G6: TEARDOWN -> ARCHIVED with gate check.

        Args:
            engagement_id: Engagement identifier.

        Returns:
            Updated EngagementState.

        Raises:
            GateDeniedError: If operator denies the gate.
            GateTimeoutError: If gate times out.
        """
        self._check_gate("G6", engagement_id, "TEARDOWN", "ARCHIVED")
        return self._lifecycle.complete_teardown(engagement_id)

    def get_state(self, engagement_id: str) -> EngagementState:
        """Get current engagement state.

        Args:
            engagement_id: Engagement identifier.

        Returns:
            Current EngagementState.

        Raises:
            KeyError: If engagement not found.
        """
        state = self._lifecycle._states.get(engagement_id)
        if state is None:
            raise KeyError(f"Engagement {engagement_id!r} not found")
        return state

    def _check_gate(
        self,
        gate_id: str,
        engagement_id: str,
        current_state: str,
        next_state: str,
    ) -> None:
        """Check gate approval before allowing transition.

        Args:
            gate_id: Gate identifier (G1-G7).
            engagement_id: Engagement identifier.
            current_state: Current lifecycle state.
            next_state: Target state.

        Raises:
            GateDeniedError: If operator denies.
            GateTimeoutError: If gate times out.
        """
        config = self._configs.get(engagement_id)
        if config is None:
            raise KeyError(f"No config cached for engagement {engagement_id!r}")

        mode = gate_approval_mode(engagement_id, config)
        gate_desc = _GATES.get(gate_id, (current_state, next_state, ""))

        if mode == GateApprovalMode.PRE_APPROVED:
            logger.info(
                "Gate %s: %s -> %s [PRE_APPROVED] for %s",
                gate_id,
                current_state,
                next_state,
                engagement_id,
            )
            return

        # HUMAN_APPROVAL path
        context = GateContext(
            gate_id=gate_id,
            engagement_id=engagement_id,
            current_state=current_state,
            next_state=next_state,
            description=gate_desc[2],
        )

        if self._gate_timeout > 0:
            result = self._confirmation.request_approval_with_timeout(context, self._gate_timeout)
            if result is None:
                logger.warning(
                    "Gate %s: TIMEOUT for %s after %ds",
                    gate_id,
                    engagement_id,
                    self._gate_timeout,
                )
                raise GateTimeoutError(gate_id, engagement_id)
        else:
            result = self._confirmation.request_approval(context)

        if result:
            logger.info(
                "Gate %s: %s -> %s [HUMAN_APPROVAL: APPROVED] for %s",
                gate_id,
                current_state,
                next_state,
                engagement_id,
            )
        else:
            logger.info(
                "Gate %s: %s -> %s [HUMAN_APPROVAL: DENIED] for %s",
                gate_id,
                current_state,
                next_state,
                engagement_id,
            )
            raise GateDeniedError(gate_id, engagement_id)
