"""Layer 2 domain value object: ScoringResult.

Represents the result of evaluating a single QualityCriterion against one
LLM output. This module is a DOMAIN module (H-07) — it does NOT import from
DeepEval, promptfoo, scipy, or any other adapter or framework.

H-10: This file contains exactly one class: ScoringResult.

References:
    - FR-007: G-Eval custom criteria evaluation
    - FR-009: Score array collection and export
    - system-design.md §2.1: Internal Interfaces (Domain Types)
    - quality-enforcement.md: S-014 LLM-as-Judge, 6-dimension weights
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ScoringResult:
    """Score produced by evaluating one QualityCriterion against one LLM output.

    Produced by JerryGEvalMetric.score_criterion() and aggregated into the
    composite score by score_composite().

    Attributes:
        criterion_name: The ``QualityCriterion.name`` that was evaluated.
        score: Raw score in [0.0, 1.0] from the LLM judge.
        weight: Weight applied to this score in the composite calculation.
        weighted_score: Precomputed ``score * weight`` for aggregation.
        evidence: LLM judge's rationale for the score. Required for traceability.
        debiasing_applied: Whether position randomization + rubric shuffling
            were applied to this evaluation invocation.

    Example::

        result = ScoringResult(
            criterion_name="completeness",
            score=0.85,
            weight=0.20,
            evidence="Output contains L0, L1, and L2 sections with substantive content.",
            debiasing_applied=True,
        )
    """

    criterion_name: str
    score: float
    weight: float
    evidence: str
    debiasing_applied: bool
    weighted_score: float = field(init=False)

    def __post_init__(self) -> None:
        """Validate score range and compute weighted_score."""
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(f"ScoringResult.score must be in [0.0, 1.0], got {self.score}")
        object.__setattr__(self, "weighted_score", self.score * self.weight)
