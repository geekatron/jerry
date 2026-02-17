# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Structured result type for prompt reinforcement generation.

Provides the immutable ``ReinforcementContent`` dataclass used by the
PromptReinforcementEngine to communicate the assembled reinforcement
preamble back to the UserPromptSubmit hook.

References:
    - EN-705: L2 Per-Prompt Reinforcement Hook
    - ADR-EPIC002-002: 5-layer enforcement architecture
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReinforcementContent:
    """Structured result of reinforcement generation.

    Attributes:
        preamble: The assembled reinforcement text to inject.
        token_estimate: Estimated token count of the preamble.
        items_included: Number of L2-REINJECT items included.
        items_total: Total number of L2-REINJECT items found.
    """

    preamble: str
    token_estimate: int
    items_included: int
    items_total: int
