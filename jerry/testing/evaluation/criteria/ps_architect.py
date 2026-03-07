"""G-Eval criteria definitions for the ps-architect agent.

ps-architect is a convergent-mode architecture decision agent in the
problem-solving skill. It produces Architecture Decision Records (ADRs) in
Nygard format with Jerry's L0/L1/L2 progressive disclosure overlay.

Quality floor:   0.88 (behavioral-contracts.md §B.3)
Cognitive mode:  Convergent
Output format:   Nygard ADR with Status, Context, Decision, Consequences sections;
                 L0/L1/L2 progressive disclosure; navigation table (H-23)

Dimension weights follow S-014 SSOT (quality-enforcement.md). Sum must equal 1.0.

Per-dimension bounds (behavioral-contracts.md §B.4 ps-architect):
    Completeness:         [0.85, 1.00]  -- all Nygard sections required
    Internal Consistency: [0.86, 1.00]  -- decision consistent with context
    Methodological Rigor: [0.87, 1.00]  -- weighted scoring, steelman, sensitivity
    Evidence Quality:     [0.82, 1.00]  -- evidence-grounded architecture decisions
    Actionability:        [0.84, 1.00]  -- concrete architectural decision required
    Traceability:         [0.88, 1.00]  -- highest traceability requirement

Structural invariants (behavioral-contracts.md §A.4 -- Nygard ADR Format):
    SI-ARCH-001: Status field: Draft/Proposed/Accepted/Deprecated/Superseded
    SI-ARCH-002: Context section present
    SI-ARCH-003: Decision section present
    SI-ARCH-004: Consequences section present
    SI-ARCH-005: At least 2 alternatives evaluated
    SI-ARCH-006: At least one negative consequence stated
    SI-ARCH-007: Length >= 1200 characters
    SI-ARCH-008: ## L0 summary section
    SI-ARCH-009: ## L2 architectural implications section
    SI-ARCH-010: Navigation table with section links

Domain isolation (H-07): imports only from jerry.testing.evaluation.criterion and stdlib.

References:
    - FR-007: G-Eval custom criteria
    - contracts/behavioral-contracts.md §A.4, §B.3, §B.4
    - quality-enforcement.md: S-014 weights
    - skills/adversary/SKILL.md: Nygard ADR format standard
"""

from jerry.testing.evaluation.criterion import QualityCriterion

PS_ARCHITECT_CRITERIA: list[QualityCriterion] = [
    QualityCriterion(
        name="completeness",
        description=(
            "The ADR contains all required Nygard format sections: Status (with a "
            "valid status value: Draft, Proposed, Accepted, Deprecated, or Superseded), "
            "Context section explaining why this decision is needed, Decision section "
            "stating the chosen option, and Consequences section describing the effects. "
            "Additionally, the output contains a ## L0 executive summary section and a "
            "## L2 strategic implications section. A navigation table with anchor links "
            "to all major sections is present. At least 2 distinct alternatives are "
            "evaluated (not just one option and a null alternative). "
            "All evaluation dimensions used in scoring are defined."
        ),
        weight=0.20,
        dimension="completeness",
    ),
    QualityCriterion(
        name="internal_consistency",
        description=(
            "The chosen decision is consistent with the stated constraints and context. "
            "If context identifies a constraint (e.g., 'must work without a server "
            "process'), the selected option satisfies that constraint or explicitly "
            "acknowledges the trade-off. Dimension scores assigned to each option "
            "support the selected choice -- the highest-scored option is chosen, or "
            "the deviation is explicitly justified. The Status field value is consistent "
            "with the document's stated maturity (e.g., Status: Draft is appropriate "
            "for an ADR being developed; Status: Accepted should not appear on an ADR "
            "that ends with unresolved open questions)."
        ),
        weight=0.20,
        dimension="internal_consistency",
    ),
    QualityCriterion(
        name="methodological_rigor",
        description=(
            "The architecture decision process follows a systematic evaluation method. "
            "Options are scored against named evaluation dimensions using a consistent "
            "scoring approach. At least one adversarial analysis element is present: "
            "either a steelman of rejected options (acknowledging their genuine strengths), "
            "a sensitivity analysis (showing how the decision would change if assumptions "
            "shifted), or a pre-mortem analysis (identifying how the chosen option could "
            "fail). The decision is grounded in evidence rather than assertion -- "
            "specific claims about option properties are supported."
        ),
        weight=0.20,
        dimension="methodological_rigor",
    ),
    QualityCriterion(
        name="evidence_quality",
        description=(
            "Claims about option properties (performance, complexity, reliability, etc.) "
            "are supported by references to prior research, cited technical sources, "
            "empirical data, or explicit reasoning chains. The output does not assert "
            "relative option quality without basis (e.g., 'Option A is more reliable' "
            "without explaining why). Cited evidence is authoritative for the domain. "
            "The Context section accurately characterizes the problem -- it does not "
            "misstate facts that would change the decision."
        ),
        weight=0.15,
        dimension="evidence_quality",
    ),
    QualityCriterion(
        name="actionability",
        description=(
            "The ADR produces a concrete, implementable architectural decision. "
            "The Decision section states a clear choice among the evaluated options -- "
            "not a hedge or a deferral without a stated trigger condition. "
            "The Consequences section provides enough detail for an implementation "
            "engineer to understand what changes are required and what the known "
            "risks are. At least one negative consequence is explicitly stated -- "
            "an ADR that lists only positive consequences is likely incomplete."
        ),
        weight=0.15,
        dimension="actionability",
    ),
    QualityCriterion(
        name="traceability",
        description=(
            "Every claim in the Decision and Consequences sections traces to the "
            "Context or to cited evidence. The evaluation dimension scores in the "
            "options comparison trace to specific properties of each option. "
            "If the ADR supersedes a prior decision, the superseded ADR is referenced. "
            "The L0 summary accurately summarizes the decision in the L1 body -- "
            "it does not introduce new claims. All evidence cited can be traced to "
            "an identifiable source (document, experiment, expert, or logical derivation)."
        ),
        weight=0.10,
        dimension="traceability",
    ),
]

# Verify weights sum to 1.0 (invariant: S-014 canonical set)
_weight_sum = sum(c.weight for c in PS_ARCHITECT_CRITERIA)
assert abs(_weight_sum - 1.0) < 1e-9, (
    f"PS_ARCHITECT_CRITERIA weights must sum to 1.0, got {_weight_sum}"
)
