# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""OperatorConfirmationPort — port for gate confirmation prompts.

Abstracts the mechanism by which an operator approves or denies a
lifecycle gate transition. Implementations may use CLI prompts,
webhook callbacks, or auto-approve for E2E testing.

Design constraints:
    H-07: Domain layer — stdlib only.
    H-10: One public class per file.

References:
    - TASK-023-149: Operator confirmation prompts (P-020)
    - FEAT-023-015: Engagement Gate System
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.gate_context import GateContext


class OperatorConfirmationPort(Protocol):
    """Port for requesting operator approval at lifecycle gates.

    Implementations:
        - AutoApproveAdapter: Always approves (for PRE_APPROVED mode).
        - CliConfirmationAdapter: CLI prompt (for HUMAN_APPROVAL mode).
    """

    def request_approval(self, context: GateContext) -> bool:
        """Request operator approval for a gate transition.

        Args:
            context: Gate context with state and risk information.

        Returns:
            True if approved, False if denied.
        """
        ...

    def request_approval_with_timeout(
        self, context: GateContext, timeout_seconds: int
    ) -> bool | None:
        """Request approval with a timeout.

        Args:
            context: Gate context.
            timeout_seconds: Seconds before timeout.

        Returns:
            True if approved, False if denied, None if timed out.
        """
        ...
