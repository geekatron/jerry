"""Layer 2 domain value object: PositionRandomizationResult.

Records the outcome of a single position-randomized candidate comparison,
enabling correct score re-attribution after the candidate order is swapped
in the LLM judge prompt.

This module is a DOMAIN module (H-07) — it does NOT import from DeepEval,
promptfoo, scipy, or any other adapter or framework.

H-10: This file contains exactly one class: PositionRandomizationResult.
      DebiasingStrategy lives in debiasing.py.

References:
    - FR-021: Debiasing requirements (position randomization, C-007)
    - ADR-001 Forces F-5: Debiased LLM-as-Judge selection
    - system-design.md §1.2: DebiasingStrategy in domain core
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PositionRandomizationResult:
    """Result of a single position-randomized candidate comparison.

    Records whether the candidate order was swapped and the original mapping,
    so the evaluation result can be correctly attributed to each candidate.

    Attributes:
        swapped: True if candidate_a and candidate_b were swapped in the
            prompt presented to the LLM judge.
        presented_first: The candidate text presented first to the judge.
        presented_second: The candidate text presented second to the judge.
        label_first: Human-readable label for the first-presented candidate
            (e.g., ``"Version A"`` or ``"Version B"``).
        label_second: Human-readable label for the second-presented candidate.

    Example::

        result = strategy.randomize_candidate_positions(
            candidate_a="Version A output text...",
            candidate_b="Version B output text...",
        )
        # Use result.presented_first / presented_second in judge prompt.
        # Use result.swapped to re-attribute scores correctly.
    """

    swapped: bool
    presented_first: str
    presented_second: str
    label_first: str
    label_second: str
