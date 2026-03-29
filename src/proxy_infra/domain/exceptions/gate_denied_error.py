# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""GateDeniedError — raised when an operator denies a lifecycle gate.

Design constraints:
    H-07: Domain layer — stdlib only.
    H-10: One public class per file.

References:
    - TASK-023-149: Operator confirmation prompts (P-020)
    - FEAT-023-015: Engagement Gate System
"""

from __future__ import annotations


class GateDeniedError(Exception):
    """Raised when an operator denies a gate transition.

    Attributes:
        gate_id: The gate that was denied (G1-G7).
        engagement_id: The engagement at the gate.
    """

    def __init__(self, gate_id: str, engagement_id: str) -> None:
        """Initialize GateDeniedError.

        Args:
            gate_id: The gate that was denied.
            engagement_id: The engagement at the gate.
        """
        self.gate_id = gate_id
        self.engagement_id = engagement_id
        super().__init__(f"Gate {gate_id} denied for engagement {engagement_id}")
