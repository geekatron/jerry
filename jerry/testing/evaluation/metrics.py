# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Layer 2 domain class: JerryGEvalMetric.

Debiased G-Eval metric encapsulating criterion weighting, score aggregation,
and debiasing integration for Jerry agent quality evaluation. This module is
a DOMAIN module (H-07) — it does NOT import from DeepEval, promptfoo, scipy,
or any other adapter or framework.

H-10: This file contains exactly one class: JerryGEvalMetric.
      QualityCriterion lives in criterion.py.
      ScoringResult lives in scoring_result.py.
      DIMENSION_WEIGHTS is a module-level constant (not a class).

The six S-014 dimension weights are sourced from quality-enforcement.md (SSOT).
Any change to those weights requires updating this module and re-baselining
all agents.

Dimension weights (S-014 SSOT, quality-enforcement.md):
    Completeness:         0.20
    Internal Consistency: 0.20
    Methodological Rigor: 0.20
    Evidence Quality:     0.15
    Actionability:        0.15
    Traceability:         0.10

References:
    - FR-007: G-Eval custom criteria evaluation
    - FR-009: Score array collection and export
    - FR-021: Debiasing requirements (C-007)
    - system-design.md §2.1: Internal Interfaces (Domain Types)
    - quality-enforcement.md: S-014 LLM-as-Judge, 6-dimension weights
    - ADR-001 Forces F-5
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from jerry.testing.evaluation.criterion import QualityCriterion
from jerry.testing.evaluation.scoring_result import ScoringResult

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# S-014 Dimension Weights (SSOT: quality-enforcement.md)
# ---------------------------------------------------------------------------

DIMENSION_WEIGHTS: dict[str, float] = {
    "completeness": 0.20,
    "internal_consistency": 0.20,
    "methodological_rigor": 0.20,
    "evidence_quality": 0.15,
    "actionability": 0.15,
    "traceability": 0.10,
}


# ---------------------------------------------------------------------------
# Domain metric class
# ---------------------------------------------------------------------------


@dataclass
class JerryGEvalMetric:
    """Debiased G-Eval metric for Jerry agent quality evaluation (Layer 2 domain).

    This class is the domain logic for the evaluation backend. It does NOT
    inherit from DeepEval's BaseMetric — that adapter coupling is performed
    in deepeval_adapter.py. This class contains only pure domain logic:
    criterion weighting, score aggregation, and debiasing integration.

    The debiasing pipeline (position randomization + rubric shuffling) is
    MANDATORY per C-007. Evaluations without debiasing are rejected at
    construction time if ``debiasing`` is None and the class is instantiated
    with ``require_debiasing=True`` (default).

    Attributes:
        criteria: Ordered list of QualityCriterion objects defining the rubric.
        debiasing: DebiasingStrategy instance. Must not be None when
            ``require_debiasing=True``.
        agent_name: Name of the target agent (e.g., ``"ps-researcher"``).
            Used for logging and score array labeling.
        require_debiasing: If True (default), raises ValueError when
            ``debiasing`` is None. Set to False only in unit tests.

    Weight normalization:
        If the sum of criterion weights != 1.0, scores are normalized by
        dividing by the sum of weights. Canonical S-014 criteria sum to 1.0
        exactly. Agent-specific addenda may shift the sum slightly.

    Example::

        from jerry.testing.evaluation import JerryGEvalMetric, DebiasingStrategy
        from jerry.testing.evaluation.criteria.ps_researcher import PS_RESEARCHER_CRITERIA

        metric = JerryGEvalMetric(
            criteria=PS_RESEARCHER_CRITERIA,
            debiasing=DebiasingStrategy(),
            agent_name="ps-researcher",
        )
        results = metric.score_all_criteria(
            prompt="Survey authentication patterns...",
            output="## L0 Executive Summary\\n...",
        )
        composite = metric.score_composite(results)

    References:
        - FR-007: G-Eval custom criteria evaluation
        - FR-021: Debiasing requirements (C-007)
        - ADR-001 Forces F-5
    """

    criteria: list[QualityCriterion]
    debiasing: object  # DebiasingStrategy | None -- avoid circular import
    agent_name: str
    require_debiasing: bool = True

    def __post_init__(self) -> None:
        """Validate configuration at construction time."""
        if not self.criteria:
            raise ValueError(
                f"JerryGEvalMetric for agent '{self.agent_name}' must have at least one criterion."
            )
        if self.require_debiasing and self.debiasing is None:
            raise ValueError(
                f"JerryGEvalMetric for agent '{self.agent_name}': debiasing is "
                "MANDATORY (C-007). Pass a DebiasingStrategy instance. "
                "To suppress this check in tests, set require_debiasing=False."
            )
        weight_sum = sum(c.weight for c in self.criteria)
        if abs(weight_sum - 1.0) > 0.01:
            logger.warning(
                "JerryGEvalMetric for agent '%s': criterion weight sum is %.4f "
                "(expected 1.0). Normalization will be applied in score_composite(). "
                "Verify criterion weights sum to 1.0 or accept normalized scoring.",
                self.agent_name,
                weight_sum,
            )

    def score_composite(self, results: list[ScoringResult]) -> float:
        """Compute the weighted composite score from individual dimension scores.

        Normalizes by the total weight sum so that partial criterion sets
        (e.g., when only a subset of criteria are evaluated) still produce
        a valid [0.0, 1.0] score.

        Args:
            results: List of ScoringResult objects from score_all_criteria().
                Must be non-empty.

        Returns:
            Weighted composite score in [0.0, 1.0].

        Raises:
            ValueError: If ``results`` is empty or weight sum is zero.

        Example::

            results = metric.score_all_criteria(prompt="...", output="...")
            composite = metric.score_composite(results)
            assert 0.0 <= composite <= 1.0
        """
        if not results:
            raise ValueError("Cannot compute composite score from empty results list.")

        total_weight = sum(r.weight for r in results)
        if total_weight == 0.0:
            raise ValueError("Total criterion weight is zero; cannot normalize.")

        weighted_sum = sum(r.weighted_score for r in results)
        return min(1.0, max(0.0, weighted_sum / total_weight))

    def get_criteria_for_debiasing(self) -> list[QualityCriterion]:
        """Return criteria list, shuffled by the debiasing strategy if set.

        The debiasing strategy shuffles criterion order on every call to reduce
        position bias in the LLM judge. If debiasing is None (test mode only),
        returns the original order.

        Returns:
            List of QualityCriterion objects in potentially shuffled order.

        References:
            - FR-021: Debiasing (position randomization + rubric shuffling)
        """
        if self.debiasing is None:
            return list(self.criteria)
        return self.debiasing.shuffle_criteria(self.criteria)  # type: ignore[union-attr]

    def classify_composite(self, composite_score: float) -> str:
        """Map a composite score to a Jerry quality band classification.

        Applies the S-014 quality band thresholds from quality-enforcement.md:
        - PASS:     score >= 0.92
        - REVISE:   0.85 <= score < 0.92
        - REJECTED: score < 0.85

        Args:
            composite_score: Weighted composite score in [0.0, 1.0].

        Returns:
            One of: ``"PASS"``, ``"REVISE"``, ``"REJECTED"``.

        Raises:
            ValueError: If score is outside [0.0, 1.0].
        """
        if not 0.0 <= composite_score <= 1.0:
            raise ValueError(f"composite_score must be in [0.0, 1.0], got {composite_score}")
        if composite_score >= 0.92:
            return "PASS"
        if composite_score >= 0.85:
            return "REVISE"
        return "REJECTED"
