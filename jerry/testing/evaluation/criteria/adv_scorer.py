# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""G-Eval criteria definitions for the adv-scorer agent.

adv-scorer is a systematic-mode LLM-as-Judge quality scoring agent in the
adversary skill. It applies the S-014 six-dimension rubric from quality-enforcement.md
to evaluate deliverables and produce PASS/REVISE/REJECTED verdicts with numeric
scores and evidence-grounded rationale.

Quality floor:   0.90 (behavioral-contracts.md §B.3)
Cognitive mode:  Systematic
Output format:   Per-dimension scores (0.0-1.0), weighted composite, PASS/REVISE/REJECTED
                 classification, dimension rationale, anti-leniency evidence

adv-scorer has the highest quality floor among the five target agents because it
performs a systematic, rubric-driven task with a fully specified output format.
Higher consistency is expected compared to divergent or convergent agents.

Dimension weights follow S-014 SSOT (quality-enforcement.md). Sum must equal 1.0.

Per-dimension bounds (behavioral-contracts.md §B.4 adv-scorer):
    Completeness:         [0.88, 1.00]  -- all 6 S-014 dimensions must be scored
    Internal Consistency: [0.90, 1.00]  -- arithmetic consistency required
    Methodological Rigor: [0.90, 1.00]  -- highest rigor; systematic rubric application
    Evidence Quality:     [0.85, 1.00]  -- scores must cite artifact evidence
    Actionability:        [0.82, 1.00]  -- PASS/REVISE/REJECTED must be stated
    Traceability:         [0.90, 1.00]  -- every score traces to a rubric criterion

Structural invariants (behavioral-contracts.md §A.6 -- adv-scorer):
    SI-SCOR-001: Numeric score in range [0.0, 1.0] present
    SI-SCOR-002: All 6 S-014 dimensions scored by name
    SI-SCOR-003: Weighted composite consistent with dimension scores (|delta| <= 0.01)
    SI-SCOR-004: PASS, REVISE, or REJECTED classification present
    SI-SCOR-005: PASS only when composite >= 0.92
    SI-SCOR-006: REVISE only when 0.85 <= composite < 0.92
    SI-SCOR-007: REJECTED only when composite < 0.85
    SI-SCOR-008: Each dimension score has accompanying rationale
    SI-SCOR-011: Anti-leniency check (uniformly high scores require evidence)

Anti-leniency note (SI-SCOR-011):
    adv-scorer is explicitly designed to counteract leniency bias in LLM judges.
    The criteria below encode anti-leniency requirements. A score of 1.0 on any
    dimension must be justified by artifact-specific evidence, not default generosity.

Domain isolation (H-07): imports only from jerry.testing.evaluation.criterion and stdlib.

References:
    - FR-007: G-Eval custom criteria
    - contracts/behavioral-contracts.md §A.6, §B.3, §B.4
    - quality-enforcement.md: S-014 weights, H-17 quality scoring required
    - quality-enforcement.md §Strategy Catalog: S-014 LLM-as-Judge
"""

from jerry.testing.evaluation.criterion import QualityCriterion

ADV_SCORER_CRITERIA: list[QualityCriterion] = [
    QualityCriterion(
        name="completeness",
        description=(
            "The scoring output includes individual scores for all six S-014 dimensions "
            "by their exact names: Completeness, Internal Consistency, Methodological "
            "Rigor, Evidence Quality, Actionability, and Traceability. No dimension is "
            "omitted or merged with another. The weighted composite score is explicitly "
            "stated as a single numeric value in [0.0, 1.0]. The output includes a "
            "PASS, REVISE, or REJECTED classification (exact string). The score for "
            "each dimension is a numeric value in [0.0, 1.0], not a qualitative label "
            "such as 'high' or 'low'."
        ),
        weight=0.20,
        dimension="completeness",
    ),
    QualityCriterion(
        name="internal_consistency",
        description=(
            "The weighted composite score is arithmetically consistent with the "
            "six dimension scores. Verification: composite = 0.20 * Completeness + "
            "0.20 * InternalConsistency + 0.20 * MethodologicalRigor + "
            "0.15 * EvidenceQuality + 0.15 * Actionability + 0.10 * Traceability. "
            "The absolute difference between the stated composite and the formula "
            "result must be <= 0.01. The PASS/REVISE/REJECTED classification is "
            "consistent with the composite: PASS requires >= 0.92, REVISE requires "
            "0.85 <= composite < 0.92, REJECTED requires composite < 0.85. "
            "No classification contradicts the arithmetic."
        ),
        weight=0.20,
        dimension="internal_consistency",
    ),
    QualityCriterion(
        name="methodological_rigor",
        description=(
            "The scoring applies the S-014 rubric systematically: each dimension is "
            "evaluated independently against its own criterion, not conflated with "
            "others. The rubric application is consistent -- the same quality properties "
            "produce the same scores across similar artifacts. The scoring explicitly "
            "resists leniency bias: if all six dimension scores are >= 0.90 (uniformly "
            "high), the rationale section provides artifact-specific evidence for each "
            "high score rather than generic approval language. Scores of 1.0 are only "
            "assigned when the artifact fully satisfies the dimension criterion with "
            "no identifiable gaps."
        ),
        weight=0.20,
        dimension="methodological_rigor",
    ),
    QualityCriterion(
        name="evidence_quality",
        description=(
            "Each dimension score is accompanied by a specific evidence statement "
            "citing content from the artifact being evaluated. The evidence is artifact-"
            "specific -- it references actual sections, claims, or properties of the "
            "artifact, not generic statements that could apply to any artifact. "
            "The evidence statement justifies the numeric score: a score of 0.75 is "
            "accompanied by evidence of both what is present (justifying > 0.5) and "
            "what is missing (justifying < 1.0). A score without evidence is not "
            "acceptable -- the evidence field must be non-empty for every dimension."
        ),
        weight=0.15,
        dimension="evidence_quality",
    ),
    QualityCriterion(
        name="actionability",
        description=(
            "The scoring output enables a quality gate decision: the PASS/REVISE/"
            "REJECTED classification is clearly stated and unambiguous. For REVISE "
            "or REJECTED verdicts, the output identifies which dimensions are below "
            "threshold and provides enough specificity for the artifact author to "
            "understand what must be improved. The output does not require the reader "
            "to infer the verdict from the scores -- it states the verdict explicitly. "
            "The scoring is decision-ready: a human or automated system can act on "
            "the output without additional interpretation."
        ),
        weight=0.15,
        dimension="actionability",
    ),
    QualityCriterion(
        name="traceability",
        description=(
            "Every dimension score traces to the corresponding S-014 criterion "
            "definition. The scoring rationale does not apply evaluation criteria "
            "that were not part of the S-014 rubric (no ad-hoc criteria introduced "
            "mid-scoring). The composite score computation is visible: either the "
            "formula is stated or the intermediate products (score * weight) are shown. "
            "The PASS/REVISE/REJECTED threshold applied is stated explicitly "
            "(PASS >= 0.92, REVISE 0.85-0.91, REJECTED < 0.85) and matches "
            "quality-enforcement.md. A reader can independently verify the verdict "
            "from the stated scores and stated thresholds."
        ),
        weight=0.10,
        dimension="traceability",
    ),
]

# Verify weights sum to 1.0 (invariant: S-014 canonical set)
_weight_sum = sum(c.weight for c in ADV_SCORER_CRITERIA)
assert abs(_weight_sum - 1.0) < 1e-9, (
    f"ADV_SCORER_CRITERIA weights must sum to 1.0, got {_weight_sum}"
)
