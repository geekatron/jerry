"""G-Eval criteria definitions for the ps-researcher agent.

ps-researcher is a divergent-mode research agent in the problem-solving skill.
Its primary function is landscape survey and research output structured with
L0/L1/L2 progressive disclosure sections.

Quality floor:   0.82 (behavioral-contracts.md §B.3)
Cognitive mode:  Divergent
Output format:   L0 Executive Summary / L1 Technical Detail / L2 Strategic Implications

Dimension weights follow S-014 SSOT (quality-enforcement.md). The sum of all
criterion weights must equal 1.0. Agent-specific structural criteria are
included here as subordinate checks within the Completeness dimension weight.

Per-dimension bounds (behavioral-contracts.md §B.4 ps-researcher):
    Completeness:         [0.78, 1.00]
    Internal Consistency: [0.80, 1.00]
    Methodological Rigor: [0.75, 1.00]
    Evidence Quality:     [0.82, 1.00]  -- core competency
    Actionability:        [0.65, 1.00]  -- lower floor; research may surface findings
    Traceability:         [0.78, 1.00]

Structural invariants (behavioral-contracts.md §A.2, verified via G-Eval):
    SI-RSRCH-001: Output contains ## L0 section
    SI-RSRCH-002: Output contains ## L1 section
    SI-RSRCH-003: Output contains ## L2 section
    SI-RSRCH-004: At least 3 distinct cited sources
    SI-RSRCH-006: L0 section <= 500 words

Domain isolation (H-07): imports only from jerry.testing.evaluation.criterion and stdlib.

References:
    - FR-007: G-Eval custom criteria
    - contracts/behavioral-contracts.md §A.2, §B.3, §B.4
    - quality-enforcement.md: S-014 weights
"""

from jerry.testing.evaluation.criterion import QualityCriterion

PS_RESEARCHER_CRITERIA: list[QualityCriterion] = [
    QualityCriterion(
        name="completeness",
        description=(
            "The output comprehensively covers the research topic without omitting "
            "essential subtopics or findings. It contains a clearly labeled L0 "
            "executive summary section (## L0), an L1 technical detail section "
            "(## L1), and an L2 strategic implications section (## L2). Each section "
            "has substantive, non-placeholder content. Research scope matches the "
            "stated research question -- no major relevant areas are left unexplored."
        ),
        weight=0.20,
        dimension="completeness",
    ),
    QualityCriterion(
        name="internal_consistency",
        description=(
            "The output does not contain contradictory statements across sections. "
            "Findings stated in L0 are consistent with the detailed evidence in L1. "
            "Strategic implications in L2 logically follow from L1 findings. "
            "Any uncertainty or caveats are consistently expressed throughout "
            "rather than asserting certainty in one section and uncertainty in another."
        ),
        weight=0.20,
        dimension="internal_consistency",
    ),
    QualityCriterion(
        name="methodological_rigor",
        description=(
            "The research follows a systematic approach appropriate to the topic. "
            "The scope and boundaries of the research are stated or implied. "
            "Sources are selected purposefully rather than arbitrarily -- the "
            "selection criteria are evident (recency, authority, relevance). "
            "The research distinguishes between primary observations, secondary "
            "synthesis, and the agent's own analytical conclusions."
        ),
        weight=0.20,
        dimension="methodological_rigor",
    ),
    QualityCriterion(
        name="evidence_quality",
        description=(
            "Claims are supported by cited sources. At least 3 distinct sources are "
            "referenced using hyperlink format [text](url) or inline citation format "
            "[Source]. Cited sources are authoritative for the domain (e.g., official "
            "documentation, peer-reviewed work, primary sources -- not unsupported "
            "blog posts without attribution). Any unverified claim is appropriately "
            "qualified (e.g., 'reportedly', 'according to', 'estimated'). "
            "The L0 section does not introduce new uncited claims not present in L1."
        ),
        weight=0.15,
        dimension="evidence_quality",
    ),
    QualityCriterion(
        name="actionability",
        description=(
            "The L2 Strategic Implications section provides at least one concrete "
            "next step, recommendation, or decision-enabling insight. Research "
            "findings are contextualized for the stakeholder's situation -- not "
            "purely descriptive without application guidance. Even if the research "
            "concludes that more information is needed, it specifies what information "
            "is needed and why."
        ),
        weight=0.15,
        dimension="actionability",
    ),
    QualityCriterion(
        name="traceability",
        description=(
            "The L0 summary can be traced to specific L1 findings. L1 findings can "
            "be traced to cited sources. L2 implications trace to L1 evidence. "
            "The progressive disclosure structure (L0 -> L1 -> L2) is maintained "
            "consistently, allowing a reader to follow the reasoning chain from "
            "high-level summary down to supporting evidence. No assertion appears "
            "in the output without a traceable basis."
        ),
        weight=0.10,
        dimension="traceability",
    ),
]

# Verify weights sum to 1.0 (invariant: S-014 canonical set)
_weight_sum = sum(c.weight for c in PS_RESEARCHER_CRITERIA)
assert abs(_weight_sum - 1.0) < 1e-9, (
    f"PS_RESEARCHER_CRITERIA weights must sum to 1.0, got {_weight_sum}"
)
