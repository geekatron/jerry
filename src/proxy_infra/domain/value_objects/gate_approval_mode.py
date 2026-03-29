# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""GateApprovalMode — dual-mode gate authorization for engagement lifecycle.

Two modes determine how lifecycle gates (G1-G7) behave:
  PRE_APPROVED: Gate auto-proceeds without operator prompt (E2E testing).
  HUMAN_APPROVAL: Gate requires explicit operator confirmation (production).

Design constraints:
    H-07: Domain layer — stdlib only, no infrastructure imports.
    H-10: One public class per file.

References:
    - TASK-023-146: Gate decision function design
    - FEAT-023-015: Engagement Gate System
    - RT-001/CC-004: Two-factor gate authorization
"""

from __future__ import annotations

from enum import Enum


class GateApprovalMode(Enum):
    """Engagement lifecycle gate approval mode.

    PRE_APPROVED: Both factors present (E2E-* prefix AND e2e_mode config).
        All 7 gates (G1-G7) auto-proceed without operator prompts.
    HUMAN_APPROVAL: Default fail-safe mode. Operator must explicitly
        approve each gate transition per P-020 (user authority).
    """

    PRE_APPROVED = "pre_approved"
    HUMAN_APPROVAL = "human_approval"
