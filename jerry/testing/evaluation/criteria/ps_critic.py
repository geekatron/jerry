# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""G-Eval criteria definitions for the ps-critic agent.

ps-critic is a convergent-mode adversarial quality review agent in the
problem-solving skill. It implements the creator-critic-revision cycle (H-14)
by applying adversarial strategies (S-002 Devil's Advocate, S-003 Steelman,
S-004 Pre-Mortem, S-010 Self-Refine, S-014 LLM-as-Judge) to assess deliverables.

Quality floor:   0.83 (behavioral-contracts.md §B.3)
Cognitive mode:  Convergent
Output format:   Structured critique with findings, severity ratings, and
                 actionable revision guidance; overall quality score

Dimension weights follow S-014 SSOT (quality-enforcement.md). Sum must equal 1.0.

Per-dimension bounds (behavioral-contracts.md §B.4 ps-critic):
    Completeness:         [0.78, 1.00]  -- critique covers all artifact dimensions
    Internal Consistency: [0.82, 1.00]  -- findings must not contradict each other
    Methodological Rigor: [0.80, 1.00]  -- adversarial strategies applied
    Evidence Quality:     [0.72, 1.00]  -- lower floor; depends on artifact quality
    Actionability:        [0.83, 1.00]  -- critique must produce actionable guidance
    Traceability:         [0.78, 1.00]  -- findings trace to artifact sections

Structural invariants (behavioral-contracts.md §A.5 -- ps-critic):
    SI-CRIT-001: At least one specific finding or issue (not generic approval)
    SI-CRIT-002: Overall quality assessment or score stated
    SI-CRIT-003: Artifact being reviewed is cited or quoted
    SI-CRIT-004: Output length >= 400 characters
    SI-CRIT-005: Contains at least one non-positive finding
    SI-CRIT-006: Actionable guidance for any identified issue

Domain isolation (H-07): imports only from jerry.testing.evaluation.criterion and stdlib.

References:
    - FR-007: G-Eval custom criteria
    - contracts/behavioral-contracts.md §A.5, §B.3, §B.4
    - quality-enforcement.md: S-014 weights, H-14 creator-critic-revision
    - quality-enforcement.md: Strategy catalog (S-002, S-003, S-004, S-010, S-014)
"""

from jerry.testing.evaluation.criterion import QualityCriterion

PS_CRITIC_CRITERIA: list[QualityCriterion] = [
    QualityCriterion(
        name="completeness",
        description=(
            "The critique covers all major quality dimensions of the artifact under "
            "review. It does not restrict itself to a single dimension (e.g., only "
            "structure) while ignoring others (e.g., evidence quality, actionability). "
            "The overall quality assessment includes a score or rating that characterizes "
            "the artifact's overall quality level. The critique identifies both "
            "strengths and weaknesses -- a critique that only finds fault without "
            "acknowledging what works is incomplete, as is a critique that provides "
            "only praise without identifying improvement areas."
        ),
        weight=0.20,
        dimension="completeness",
    ),
    QualityCriterion(
        name="internal_consistency",
        description=(
            "The critique's findings do not contradict each other. If Finding A states "
            "that the artifact's evidence quality is strong and Finding B states that "
            "claims lack support, the contradiction is resolved or acknowledged -- "
            "not left as an implicit inconsistency. The overall score is consistent "
            "with the dimension-level findings: a high overall score is not assigned "
            "when multiple critical findings are present, and a low overall score is "
            "not assigned when no substantive issues are found. "
            "Severity classifications are applied consistently across findings."
        ),
        weight=0.20,
        dimension="internal_consistency",
    ),
    QualityCriterion(
        name="methodological_rigor",
        description=(
            "The critique applies at least one named adversarial strategy from the "
            "quality-enforcement.md catalog: S-002 Devil's Advocate (challenging core "
            "assumptions), S-003 Steelman (identifying the strongest version of the "
            "artifact's argument before critiquing it), S-004 Pre-Mortem (imagining "
            "future failure modes), S-010 Self-Refine (identifying what the artifact "
            "would say if asked to critique itself), or S-013 Inversion. "
            "The critique distinguishes between defects (things that are wrong) and "
            "improvements (things that could be better but are not wrong). "
            "Findings are rated by severity or impact."
        ),
        weight=0.20,
        dimension="methodological_rigor",
    ),
    QualityCriterion(
        name="evidence_quality",
        description=(
            "Each finding in the critique cites specific evidence from the artifact "
            "being reviewed. The critique does not assert defects in the abstract -- "
            "it quotes or paraphrases the specific artifact content that exhibits "
            "the defect. Where the critique draws on external standards or frameworks "
            "(e.g., OWASP, SOLID principles, Nygard ADR format), the standard is "
            "named and its application to the artifact is explained. "
            "The critique does not fabricate defects that are not present in the artifact."
        ),
        weight=0.15,
        dimension="evidence_quality",
    ),
    QualityCriterion(
        name="actionability",
        description=(
            "Every identified defect or improvement is accompanied by concrete, "
            "specific revision guidance. The guidance is specific enough for the "
            "artifact author to act on it without additional clarification. "
            "Guidance uses actionable language: 'Add a section covering X', "
            "'Replace the assertion at line Y with evidence from Z', rather than "
            "'Improve the evidence quality'. Where the critique recommends a revision, "
            "it does not merely say 'this needs improvement' -- it specifies what "
            "the improved version should contain or how it should differ."
        ),
        weight=0.15,
        dimension="actionability",
    ),
    QualityCriterion(
        name="traceability",
        description=(
            "Each finding traces to a specific section, paragraph, or element of "
            "the artifact under review. A reader of both the critique and the artifact "
            "can identify precisely which part of the artifact the finding refers to. "
            "The overall quality score traces to the dimension-level findings -- "
            "the score is not assigned arbitrarily but follows from the weighted "
            "assessment of individual quality dimensions. If the critique references "
            "prior iterations of the artifact or prior critique rounds, those "
            "references are specific and traceable."
        ),
        weight=0.10,
        dimension="traceability",
    ),
]

# Verify weights sum to 1.0 (invariant: S-014 canonical set)
_weight_sum = sum(c.weight for c in PS_CRITIC_CRITERIA)
assert abs(_weight_sum - 1.0) < 1e-9, (
    f"PS_CRITIC_CRITERIA weights must sum to 1.0, got {_weight_sum}"
)
