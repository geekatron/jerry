"""G-Eval criteria definitions for the ps-analyst agent.

ps-analyst is a convergent-mode structured analysis agent in the problem-solving
skill. Its primary function is trade-off analysis using methods such as FMEA,
weighted scoring matrices, and comparative option evaluation.

Quality floor:   0.85 (behavioral-contracts.md §B.3)
Cognitive mode:  Convergent
Output format:   Structured analysis with tables, criteria, and a clear recommendation

Dimension weights follow S-014 SSOT (quality-enforcement.md). Sum must equal 1.0.

Per-dimension bounds (behavioral-contracts.md §B.4 ps-analyst):
    Completeness:         [0.82, 1.00]  -- all options and criteria addressed
    Internal Consistency: [0.84, 1.00]  -- conclusions follow from criteria scores
    Methodological Rigor: [0.83, 1.00]  -- FMEA, trade study methods correct
    Evidence Quality:     [0.78, 1.00]  -- depends on upstream research quality
    Actionability:        [0.85, 1.00]  -- core competency; must produce conclusions
    Traceability:         [0.80, 1.00]  -- criteria traceable to input evidence

Structural invariants (behavioral-contracts.md §A.3, verified via G-Eval):
    SI-ANLT-001: At least one markdown table with column headers
    SI-ANLT-002: Explicit evaluation criteria or dimensions
    SI-ANLT-003: At least one recommendation or conclusion
    SI-ANLT-005: All compared options are addressed (G-Eval semantic check)

Domain isolation (H-07): imports only from jerry.testing.evaluation.criterion and stdlib.

References:
    - FR-007: G-Eval custom criteria
    - contracts/behavioral-contracts.md §A.3, §B.3, §B.4
    - quality-enforcement.md: S-014 weights
"""

from jerry.testing.evaluation.criterion import QualityCriterion

PS_ANALYST_CRITERIA: list[QualityCriterion] = [
    QualityCriterion(
        name="completeness",
        description=(
            "The analysis addresses all options presented in the input without "
            "selectively omitting any. All relevant evaluation dimensions or criteria "
            "are applied to each option -- no option is assessed against a subset "
            "of criteria while others receive full treatment. The output includes "
            "at least one structured markdown table (using | delimiters) presenting "
            "the comparative evaluation. If multiple options are present, all are "
            "explicitly named and evaluated."
        ),
        weight=0.20,
        dimension="completeness",
    ),
    QualityCriterion(
        name="internal_consistency",
        description=(
            "The final recommendation or conclusion is consistent with the scores "
            "or assessments assigned to each option in the analysis. An option "
            "ranked highest on the evaluation dimensions is the one recommended, "
            "unless a stated overriding constraint justifies the deviation. "
            "No option is simultaneously described as superior on key criteria and "
            "then not recommended without explicit explanation. Numeric scores in "
            "tables are consistent with narrative descriptions."
        ),
        weight=0.20,
        dimension="internal_consistency",
    ),
    QualityCriterion(
        name="methodological_rigor",
        description=(
            "A named analytical method is applied (e.g., FMEA, weighted scoring, "
            "trade study matrix, MoSCoW, pairwise comparison). The method is applied "
            "correctly and consistently across all options. Evaluation dimensions are "
            "explicitly defined before options are scored -- not post-hoc justifications. "
            "If quantitative scoring is used, the scoring scale is defined. "
            "The analysis distinguishes between objective criteria (measurable) and "
            "subjective criteria (judgment-based), and applies appropriate evidence "
            "to each type."
        ),
        weight=0.20,
        dimension="methodological_rigor",
    ),
    QualityCriterion(
        name="evidence_quality",
        description=(
            "Scores or assessments assigned to options are grounded in evidence "
            "from the input context (prior research, provided data, stated requirements). "
            "The output does not assert scores without basis -- each criterion score "
            "is accompanied by a brief rationale citing the evidence that supports it. "
            "Where evidence is limited or uncertain, the analysis acknowledges this "
            "and appropriately widens confidence bounds rather than asserting false precision."
        ),
        weight=0.15,
        dimension="evidence_quality",
    ),
    QualityCriterion(
        name="actionability",
        description=(
            "The output produces a concrete, actionable recommendation or decision. "
            "The recommended option is clearly identified (not buried in hedging). "
            "The recommendation includes conditions or caveats that would change it, "
            "enabling the decision-maker to validate the recommendation's applicability. "
            "If the analysis is inconclusive, it specifies what additional information "
            "would be needed to reach a recommendation -- it does not simply decline "
            "to conclude."
        ),
        weight=0.15,
        dimension="actionability",
    ),
    QualityCriterion(
        name="traceability",
        description=(
            "The recommendation traces back through the evaluation to the criterion "
            "scores, which trace back to the evidence. A reader can follow the chain: "
            "recommendation <- highest-scoring option <- dimension scores <- evidence. "
            "If a weighting scheme is used, the weights are stated and their application "
            "is visible (e.g., weighted score = raw score * weight). "
            "The analysis does not introduce new criteria after the scoring that were "
            "not part of the stated evaluation framework."
        ),
        weight=0.10,
        dimension="traceability",
    ),
]

# Verify weights sum to 1.0 (invariant: S-014 canonical set)
_weight_sum = sum(c.weight for c in PS_ANALYST_CRITERIA)
assert abs(_weight_sum - 1.0) < 1e-9, (
    f"PS_ANALYST_CRITERIA weights must sum to 1.0, got {_weight_sum}"
)
