# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Session quality context generator for L1 Static Context injection.

Produces the XML quality framework preamble that is injected into the
SessionStart hook output. The preamble contains compile-time constant
content defined by EPIC-002 EN-405 TASK-006 and is budget-constrained
to 700 tokens.

The generator uses a chars/4 * 0.83 calibration factor for token
estimation, matching the approach validated during EPIC-002 analysis.

References:
    - EN-706: SessionStart Quality Context Injection
    - EPIC-002 EN-405/TASK-006: Quality preamble specification
    - FEAT-008: Quality Framework Implementation
"""

from __future__ import annotations

from src.infrastructure.internal.enforcement.quality_context import (
    QualityContext,
)

# Maximum token budget for the quality preamble
_TOKEN_BUDGET = 700

# Calibration factor for token estimation: chars/4 * factor
_CALIBRATION_FACTOR = 0.83

# The quality framework preamble content (compile-time constant).
# Defined by EPIC-002 EN-405 TASK-006. No runtime file parsing needed.
_QUALITY_PREAMBLE = """\
<quality-framework version="1.0">
  <quality-gate>
    Target: >= 0.92 for all deliverables.
    Scoring: Use S-014 (LLM-as-Judge) with dimension-level rubrics.
    Known bias: S-014 has leniency bias. Score critically -- 0.92 means genuinely excellent.
    Cycle: Creator -> Critic -> Revision (minimum 3 iterations). Do not bypass.
    Pairing: Steelman (S-003) before Devil's Advocate (S-002) -- canonical review protocol.
    Context rot: After ~20K tokens, re-read .claude/rules/ and consider session restart for C3+ work.
  </quality-gate>

  <constitutional-principles>
    HARD constraints (cannot be overridden):
    - P-003: No recursive subagents. Max ONE level: orchestrator -> worker.
    - P-020: User authority. User decides. Never override. Ask before destructive ops.
    - P-022: No deception. Never deceive about actions, capabilities, or confidence.
    Python: UV only. Never use python/pip directly. Use 'uv run'.
  </constitutional-principles>

  <adversarial-strategies>
    Available strategies for quality enforcement:
    - S-014 (LLM-as-Judge): Rubric-based scoring. Use for all deliverables.
    - S-007 (Constitutional AI): Principle-by-principle review. Check .claude/rules/.
    - S-010 (Self-Refine): Self-review before presenting outputs. Apply always.
    - S-003 (Steelman): Charitable reconstruction before critique.
    - S-002 (Devil's Advocate): Strongest counterargument to prevailing conclusion.
    - S-013 (Inversion): Ask 'how could this fail?' before proposing.
    - S-004 (Pre-Mortem): 'Imagine it failed -- why?' for planning tasks.
    - S-012 (FMEA): Systematic failure mode enumeration for architecture.
    - S-011 (CoVe): Factual verification for claims and documentation.
    - S-001 (Red Team): Adversary simulation for security-sensitive work.
  </adversarial-strategies>

  <decision-criticality>
    Assess every task's criticality:
    - C1 (Routine): Reversible, < 3 files, no external deps -> Self-Check only
    - C2 (Standard): Reversible within 1 day, 3-10 files -> Standard Critic
    - C3 (Significant): > 1 day to reverse, > 10 files, API changes -> Deep Review
    - C4 (Critical): Irreversible, architecture/governance changes -> Tournament Review
    Strategy guidance: C1(S-010) C2(S-007+S-002+S-014) C3(6+ strategies) C4(all 10).
    AUTO-ESCALATE: governance files/rules -> C3+; new/modified ADR -> C3+; modified baselined ADR -> C4.
  </decision-criticality>
</quality-framework>"""

# Number of XML sections in the preamble
_EXPECTED_SECTIONS = 4


class SessionQualityContextGenerator:
    """Generator for SessionStart quality framework preamble.

    Produces the XML quality context that is injected into the
    SessionStart hook output. The preamble is a compile-time constant
    defined by EPIC-002 EN-405 TASK-006, budget-constrained to 700
    tokens using a chars/4 * 0.83 calibration factor.

    The generator is fail-safe: it never raises exceptions that would
    block session start. If the preamble exceeds the token budget,
    it is still returned (the budget is a design target, not a hard
    gate).

    References:
        - EN-706: SessionStart Quality Context Injection
        - EPIC-002 EN-405/TASK-006: Quality preamble specification
    """

    def generate(self) -> QualityContext:
        """Generate the quality framework preamble.

        Assembles the XML quality preamble with 4 sections (quality-gate,
        constitutional-principles, adversarial-strategies, decision-criticality)
        and returns it with token estimation metadata.

        Returns:
            QualityContext with the preamble string, estimated token count,
            and number of sections included.
        """
        token_estimate = self._estimate_tokens(_QUALITY_PREAMBLE)

        return QualityContext(
            preamble=_QUALITY_PREAMBLE,
            token_estimate=token_estimate,
            sections_included=_EXPECTED_SECTIONS,
        )

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """Estimate the token count for a text string.

        Uses the chars/4 * 0.83 calibration factor validated during
        EPIC-002 analysis for XML-heavy content.

        Args:
            text: The text to estimate tokens for.

        Returns:
            Estimated token count as an integer.
        """
        return int(len(text) / 4 * _CALIBRATION_FACTOR)
