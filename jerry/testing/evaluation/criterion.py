# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Layer 2 domain value object: QualityCriterion.

A single named quality dimension for G-Eval evaluation. This module is a
DOMAIN module (H-07) — it does NOT import from DeepEval, promptfoo, scipy,
or any other adapter or framework.

H-10: This file contains exactly one class: QualityCriterion.

References:
    - FR-007: G-Eval custom criteria evaluation
    - system-design.md §2.1: Internal Interfaces (Domain Types)
    - quality-enforcement.md: S-014 LLM-as-Judge, 6-dimension weights
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QualityCriterion:
    """A single G-Eval evaluation criterion for a Jerry agent.

    Represents one named quality dimension that will be scored by the
    debiased LLM-as-Judge. The ``description`` is the natural-language
    rubric passed verbatim to G-Eval.

    Attributes:
        name: Unique identifier matching an S-014 dimension key, or an
            agent-specific criterion name (e.g., ``"adr_status_field"``).
        description: Natural-language rubric text evaluated by G-Eval.
            Must be concrete and verifiable, not vague.
        weight: Importance weight for composite score computation.
            S-014 dimensions carry canonical weights from DIMENSION_WEIGHTS.
            Agent-specific criteria carry weights assigned per-agent.
        dimension: The S-014 dimension this criterion maps to, or None
            for structural / agent-specific criteria outside S-014.

    Example::

        criterion = QualityCriterion(
            name="completeness",
            description=(
                "The output includes all required L0, L1, and L2 sections "
                "with non-empty content in each section."
            ),
            weight=0.20,
            dimension="completeness",
        )
    """

    name: str
    description: str
    weight: float
    dimension: str | None = None

    def __post_init__(self) -> None:
        """Validate weight is in (0.0, 1.0] and name is non-empty."""
        if not self.name.strip():
            raise ValueError("QualityCriterion.name must be non-empty.")
        if not 0.0 < self.weight <= 1.0:
            raise ValueError(f"QualityCriterion.weight must be in (0.0, 1.0], got {self.weight}")
        if not self.description.strip():
            raise ValueError("QualityCriterion.description must be non-empty.")
