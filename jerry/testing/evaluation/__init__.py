# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Layer 2: DeepEval evaluation backend for the Four-Layer Composite Test Harness.

This package implements debiased LLM-as-Judge evaluation using DeepEval's G-Eval
metric framework. Debiasing is mandatory (C-007) -- position randomization and
rubric shuffling are applied to every evaluation invocation.

H-10 compliance (one class per file):
    criterion.py                     -- QualityCriterion
    scoring_result.py                -- ScoringResult
    metrics.py                       -- JerryGEvalMetric
    position_randomization_result.py -- PositionRandomizationResult
    debiasing.py                     -- DebiasingStrategy
    ports.py                         -- EvaluationPort (Protocol)
    jerry_geval_deepeval_metric.py   -- JerryGEvalDeepEvalMetric
    deepeval_adapter.py              -- DeepEvalAdapter

Public API:
    JerryGEvalMetric:            Custom domain metric wrapping debiased G-Eval scoring.
    DebiasingStrategy:           Position randomization + rubric shuffling implementation.
    QualityCriterion:            Single evaluation criterion value object.
    ScoringResult:               Result of scoring one criterion against one output.
    PositionRandomizationResult: Result of a candidate position randomization.
    EvaluationPort:              Protocol interface for evaluation backend injection.

Domain Isolation (H-07):
    This package imports ONLY from:
    - stdlib (random, dataclasses, abc, typing)
    - approved domain siblings (jerry.testing.evaluation.*)
    - jerry.testing.types (shared domain types)
    Domain modules in this package do NOT import from:
    - deepeval (adapter concern only -- deepeval_adapter.py and
      jerry_geval_deepeval_metric.py only)
    - promptfoo (Layer 1 concern)
    - scipy / statsmodels (Layer 4 concern)

Usage::

    from jerry.testing.evaluation import JerryGEvalMetric, DebiasingStrategy
    from jerry.testing.evaluation.criteria.ps_researcher import PS_RESEARCHER_CRITERIA

    strategy = DebiasingStrategy()
    metric = JerryGEvalMetric(
        criteria=PS_RESEARCHER_CRITERIA,
        debiasing=strategy,
        agent_name="ps-researcher",
    )

References:
    - FR-006: DeepEval pytest plugin integration
    - FR-007: G-Eval custom criteria evaluation
    - FR-008: Deterministic property assertions
    - FR-009: Score array collection and export
    - FR-021: Debiasing requirements (C-007)
    - ADR-001 Forces F-5: Debiased LLM-as-Judge rationale
    - system-design.md: EvaluationPort, Layer 2 domain
"""

from jerry.testing.evaluation.criterion import QualityCriterion
from jerry.testing.evaluation.debiasing import DebiasingStrategy
from jerry.testing.evaluation.metrics import DIMENSION_WEIGHTS, JerryGEvalMetric
from jerry.testing.evaluation.ports import EvaluationPort
from jerry.testing.evaluation.position_randomization_result import (
    PositionRandomizationResult,
)
from jerry.testing.evaluation.scoring_result import ScoringResult

__all__ = [
    "DIMENSION_WEIGHTS",
    "DebiasingStrategy",
    "EvaluationPort",
    "JerryGEvalMetric",
    "PositionRandomizationResult",
    "QualityCriterion",
    "ScoringResult",
]
