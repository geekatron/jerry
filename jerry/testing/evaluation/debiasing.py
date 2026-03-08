# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Debiasing strategy for LLM-as-Judge evaluation (Layer 2 domain).

Implements position randomization and rubric criterion shuffling to mitigate
LLM judge positional bias (recency bias, primacy bias) as required by C-007.

Background:
    Vanilla LLM-as-Judge evaluation is explicitly rejected in this architecture
    (C-007, ADR-001 Forces F-5). The two primary bias types addressed here are:

    1. Positional bias: LLM judges favor outputs presented first (primacy) or
       last (recency). Mitigated by randomizing candidate presentation order.

    2. Criterion ordering bias: Criteria evaluated earlier anchor the LLM's
       reasoning, inflating scores for criteria evaluated later in the same
       prompt. Mitigated by shuffling criterion order per evaluation call.

Domain isolation (H-07):
    This module imports ONLY from stdlib (random, dataclasses) and sibling
    domain modules in this package. It does NOT import from DeepEval,
    promptfoo, scipy, or any adapter.

H-10: This file contains exactly one class: DebiasingStrategy.
      PositionRandomizationResult lives in position_randomization_result.py.

References:
    - FR-021: Debiasing requirements
    - C-007: Vanilla LLM-as-Judge rejection rationale
    - ADR-001 Forces F-5: Debiased LLM-as-Judge selection
    - system-design.md §1.2: DebiasingStrategy in domain core
    - contracts/behavioral-contracts.md §B.5: Score stability bounds
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

from jerry.testing.evaluation.position_randomization_result import (
    PositionRandomizationResult,
)

if TYPE_CHECKING:
    from jerry.testing.evaluation.criterion import QualityCriterion


@dataclass
class DebiasingStrategy:
    """Position randomization and rubric shuffling for LLM-as-Judge debiasing.

    This class is the mandatory debiasing component for all Layer 2 evaluations.
    It implements two complementary bias mitigation techniques:

    1. **Position randomization** (``randomize_candidate_positions``):
       Randomly swaps the order in which two candidate outputs are presented
       to the LLM judge. When aggregated over N evaluations, each candidate
       appears first approximately N/2 times, eliminating systematic positional
       advantage.

    2. **Rubric criterion shuffling** (``shuffle_criteria``):
       Randomly permutes the order of evaluation criteria in each LLM judge
       prompt. Anchoring effects from criterion ordering are randomized across
       evaluations, producing unbiased aggregate scores.

    The ``seed`` attribute controls reproducibility for testing. In production,
    ``seed=None`` (default) produces non-deterministic randomization, which is
    required for the debiasing to be effective across N evaluation runs.

    Attributes:
        seed: Optional integer seed for the random number generator.
            Use ``None`` (default) for production to ensure true randomization.
            Set a fixed value only in deterministic unit tests.
        swap_probability: Probability [0.0, 1.0] of swapping candidate order
            per invocation. Default 0.5 ensures equal presentation frequency.

    Example::

        strategy = DebiasingStrategy()

        # Randomize which candidate appears first in the judge prompt
        position_result = strategy.randomize_candidate_positions(
            candidate_a="Output from Version A of the prompt...",
            candidate_b="Output from Version B of the prompt...",
        )

        # Shuffle criteria to prevent ordering anchoring bias
        shuffled = strategy.shuffle_criteria(criteria_list)
    """

    seed: int | None = None
    swap_probability: float = 0.5

    def __post_init__(self) -> None:
        """Validate swap_probability range."""
        if not 0.0 <= self.swap_probability <= 1.0:
            raise ValueError(f"swap_probability must be in [0.0, 1.0], got {self.swap_probability}")
        self._rng = random.Random(self.seed)

    def randomize_candidate_positions(
        self,
        candidate_a: str,
        candidate_b: str,
        label_a: str = "Version A",
        label_b: str = "Version B",
    ) -> PositionRandomizationResult:
        """Randomly swap candidate presentation order to eliminate positional bias.

        The LLM judge should receive the returned ``presented_first`` /
        ``presented_second`` texts rather than ``candidate_a`` / ``candidate_b``
        directly. The ``swapped`` flag tells the caller how to re-attribute
        the judge's comparative verdict to the correct version.

        This method is called once per evaluation invocation. Over N=30 runs,
        each candidate will appear first approximately N/2 = 15 times, ensuring
        that any positional advantage is balanced across the sample.

        Args:
            candidate_a: Text of the first candidate (baseline version output).
            candidate_b: Text of the second candidate (PR version output).
            label_a: Human-readable label for candidate_a (default: "Version A").
            label_b: Human-readable label for candidate_b (default: "Version B").

        Returns:
            PositionRandomizationResult with the (possibly swapped) presentation
            order and a flag indicating whether swapping occurred.

        Example::

            result = strategy.randomize_candidate_positions(
                candidate_a=baseline_output,
                candidate_b=pr_output,
            )
            judge_prompt = build_comparison_prompt(
                first=result.presented_first,
                first_label=result.label_first,
                second=result.presented_second,
                second_label=result.label_second,
            )
        """
        should_swap = self._rng.random() < self.swap_probability

        if should_swap:
            return PositionRandomizationResult(
                swapped=True,
                presented_first=candidate_b,
                presented_second=candidate_a,
                label_first=label_b,
                label_second=label_a,
            )
        return PositionRandomizationResult(
            swapped=False,
            presented_first=candidate_a,
            presented_second=candidate_b,
            label_first=label_a,
            label_second=label_b,
        )

    def shuffle_criteria(
        self,
        criteria: list[QualityCriterion],
    ) -> list[QualityCriterion]:
        """Shuffle criterion order to prevent LLM anchoring bias.

        Returns a new list with the same criteria in a randomized order.
        The original list is NOT modified (pure function).

        Anchoring bias occurs when the LLM judge's scoring of later criteria
        is influenced by its previous scores for earlier criteria. By shuffling
        the order on every evaluation call, anchoring effects are randomized
        across the N evaluation runs, producing unbiased aggregate dimension scores.

        Args:
            criteria: List of QualityCriterion objects defining the evaluation
                rubric. Must be non-empty.

        Returns:
            New list containing the same criteria in a uniformly random order.

        Raises:
            ValueError: If ``criteria`` is empty.

        Example::

            shuffled = strategy.shuffle_criteria(PS_RESEARCHER_CRITERIA)
            # shuffled contains same items as PS_RESEARCHER_CRITERIA in random order
            assert set(c.name for c in shuffled) == set(c.name for c in PS_RESEARCHER_CRITERIA)
        """
        if not criteria:
            raise ValueError("Cannot shuffle an empty criteria list.")

        shuffled = list(criteria)
        self._rng.shuffle(shuffled)
        return shuffled

    def build_debiased_prompt_section(
        self,
        criteria: list[QualityCriterion],
        output_text: str,
    ) -> str:
        """Build a debiased evaluation prompt section for single-output G-Eval.

        Constructs the rubric portion of a G-Eval prompt with shuffled criterion
        order. The output text is fixed (single-output evaluation, not comparison).
        Position randomization is only relevant for comparative (A/B) evaluations;
        this method handles the single-output case used by JerryGEvalMetric.

        Args:
            criteria: Evaluation criteria (will be shuffled before inclusion).
            output_text: The LLM output to be evaluated. Truncated to 4000
                characters to prevent context overflow in the judge prompt.

        Returns:
            Formatted string containing the shuffled rubric and output text,
            ready for inclusion in a G-Eval prompt.

        Example::

            prompt_section = strategy.build_debiased_prompt_section(
                criteria=PS_RESEARCHER_CRITERIA,
                output_text=agent_output,
            )
        """
        shuffled = self.shuffle_criteria(criteria)

        # Truncate output to prevent context overflow
        truncated_output = output_text[:4000]
        if len(output_text) > 4000:
            truncated_output += "\n\n[... output truncated for evaluation ...]"

        criteria_lines = "\n".join(
            f"{i + 1}. [{c.name}] (weight={c.weight:.2f}): {c.description}"
            for i, c in enumerate(shuffled)
        )

        return (
            f"Evaluate the following output against each criterion below.\n"
            f"Score each criterion from 0.0 (completely fails) to 1.0 (fully meets).\n"
            f"Provide a brief evidence statement for each score.\n\n"
            f"CRITERIA (shuffled order to reduce anchoring bias):\n"
            f"{criteria_lines}\n\n"
            f"OUTPUT TO EVALUATE:\n"
            f"---\n"
            f"{truncated_output}\n"
            f"---"
        )

    def reset_rng(self) -> None:
        """Reset the random number generator to its initial seed.

        Useful in testing to produce deterministic sequences across multiple
        calls. In production, this method should not be called (randomization
        must not be reset between evaluations).

        Note: Calling reset_rng() on a DebiasingStrategy with seed=None
        re-seeds from the system entropy source, which effectively produces
        a new random sequence rather than repeating the previous one.
        """
        self._rng = random.Random(self.seed)
