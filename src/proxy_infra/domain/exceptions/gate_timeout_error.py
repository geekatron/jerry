# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""GateTimeoutError — raised when a gate times out waiting for operator.

Design constraints:
    H-07: Domain layer — stdlib only.
    H-10: One public class per file.

References:
    - TASK-023-150: Gate timeout behavior
    - FEAT-023-015: Engagement Gate System
"""

from __future__ import annotations


class GateTimeoutError(Exception):
    """Raised when a gate times out waiting for operator response.

    The fail-safe behavior on timeout is halt (not auto-approve),
    consistent with P-020 (user authority).

    Attributes:
        gate_id: The gate that timed out (G1-G7).
        engagement_id: The engagement at the gate.
    """

    def __init__(self, gate_id: str, engagement_id: str) -> None:
        """Initialize GateTimeoutError.

        Args:
            gate_id: The gate that timed out.
            engagement_id: The engagement at the gate.
        """
        self.gate_id = gate_id
        self.engagement_id = engagement_id
        super().__init__(f"Gate {gate_id} timed out for engagement {engagement_id}")
