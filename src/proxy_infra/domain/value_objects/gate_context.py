# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""GateContext — value object for lifecycle gate transition context.

Carries the information an operator needs to make an informed approval
or denial decision at each engagement lifecycle gate (G1-G7).

Design constraints:
    H-07: Domain layer — stdlib only.
    H-10: One public class per file.

References:
    - TASK-023-149: Operator confirmation prompts (P-020)
    - FEAT-023-015: Engagement Gate System
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class GateContext:
    """Context passed to operator at each gate.

    Attributes:
        gate_id: Gate identifier (G1-G7).
        engagement_id: Engagement being gated.
        current_state: Current lifecycle state.
        next_state: State to transition to if approved.
        description: Human-readable description of what the next phase does.
        risks: List of risks or irreversible actions in the next phase.
    """

    gate_id: str
    engagement_id: str
    current_state: str
    next_state: str
    description: str = ""
    risks: list[str] = field(default_factory=list)
