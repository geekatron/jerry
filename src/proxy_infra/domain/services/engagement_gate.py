# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Engagement gate decision service — dual-mode gate authorization.

Pure function that determines whether an engagement's lifecycle gates (G1-G7)
auto-approve or require operator confirmation. Uses two-factor authorization:
  Factor 1: Engagement ID starts with ``E2E-`` prefix
  Factor 2: ``e2e_mode: true`` in engagement config metadata

Both factors are required for pre-approved mode. Missing either factor
fails-safe to human approval per P-020 (user authority).

Design constraints:
    H-07: Domain layer — stdlib only, no infrastructure imports.
    H-10: One public class per file (this file exports a single function).

References:
    - TASK-023-146: Gate decision function design
    - FEAT-023-015: Engagement Gate System
    - RT-001/CC-004: Two-factor gate authorization security rationale
"""

from __future__ import annotations

from src.proxy_infra.domain.value_objects.full_engagement_config import (
    FullEngagementConfig,
)
from src.proxy_infra.domain.value_objects.gate_approval_mode import GateApprovalMode

_E2E_PREFIX = "E2E-"


def gate_approval_mode(engagement_id: str, config: FullEngagementConfig) -> GateApprovalMode:
    """Determine the gate approval mode for an engagement.

    Two-factor check: the engagement ID must start with ``E2E-`` AND the
    config must have ``e2e_mode: true``. Both factors are required.
    Missing either factor fails-safe to HUMAN_APPROVAL.

    Args:
        engagement_id: The engagement identifier string.
        config: Full engagement configuration with metadata.

    Returns:
        GateApprovalMode.PRE_APPROVED if both factors present,
        GateApprovalMode.HUMAN_APPROVAL otherwise.
    """
    if not engagement_id:
        return GateApprovalMode.HUMAN_APPROVAL

    has_prefix = engagement_id.startswith(_E2E_PREFIX) and len(engagement_id) > len(_E2E_PREFIX)
    has_config = config.engagement.e2e_mode is True

    if has_prefix and has_config:
        return GateApprovalMode.PRE_APPROVED

    return GateApprovalMode.HUMAN_APPROVAL
