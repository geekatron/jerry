# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Layer 2 adapter: DeepEvalAdapter — public evaluation API.

This is the ONLY module in jerry.testing.evaluation that imports from the
deepeval library (transitively, via jerry_geval_deepeval_metric.py). All
other domain modules in this package are pure domain code (H-07) and must
NOT import from deepeval. If deepeval is not installed, this adapter raises
an ImportError with a clear remediation message.

Architecture (H-07 compliance):
    - ADAPTER layer: this module imports the DeepEval-coupled metric class
      from jerry_geval_deepeval_metric.py (external framework dependency
      contained in that module).
    - DOMAIN layer: JerryGEvalMetric, QualityCriterion, ScoringResult,
      DebiasingStrategy remain in their respective domain modules with no
      deepeval imports.
    - Domain code NEVER imports from this module (inward dependency rule).

H-10: This file contains exactly one class: DeepEvalAdapter.
      JerryGEvalDeepEvalMetric lives in jerry_geval_deepeval_metric.py.

The DeepEvalAdapter class implements the EvaluationPort protocol defined in
jerry/testing/evaluation/ports.py, enabling the pytest conftest to inject it
without coupling to the deepeval library directly.

pytest plugin integration (FR-006):
    DeepEvalAdapter produces metrics usable via ``deepeval.assert_test()``.
    Each metric is a subclass of ``deepeval.metrics.BaseMetric`` and integrates
    with DeepEval's pytest plugin for automatic test reporting.

Debiasing (FR-021 / C-007):
    MANDATORY. The adapter applies ``DebiasingStrategy.shuffle_criteria()``
    and ``DebiasingStrategy.randomize_candidate_positions()`` on every
    measure() call. Debiasing CANNOT be disabled at runtime -- attempts to
    do so raise ``ValueError`` to prevent silent leniency bias.

G-Eval translation:
    ``QualityCriterion`` -> DeepEval ``GEval`` criteria string format.
    Criterion names and descriptions are passed to DeepEval's GEval metric
    as evaluation steps. The DeepEval GEval framework handles the LLM judge
    call; this adapter manages the criterion ordering debiasing and score
    aggregation via ``JerryGEvalMetric.score_composite()``.

References:
    - FR-006: DeepEval pytest plugin integration
    - FR-007: G-Eval custom criteria evaluation
    - FR-009: Score array collection and export
    - FR-021: Debiasing (position randomization + rubric shuffling, C-007)
    - system-design.md §1.3: deepeval_adapter.py in module decomposition
    - system-design.md §1.4: Dependency graph -- adapter imports domain, not vice versa
    - system-design.md §2.2: EvaluationPort protocol
    - contracts/behavioral-contracts.md §D.2: Score array format
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field

try:
    from deepeval.metrics import BaseMetric
    from deepeval.test_case import LLMTestCase
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "deepeval is required for the Layer 2 evaluation adapter. "
        "Install it with: uv add deepeval\n"
        "See FR-006 (DeepEval pytest plugin integration) and "
        "projects/PROJ-036-prompt-regression-harness/requirements/harness-requirements.md"
    ) from exc

from jerry.testing.evaluation.criterion import QualityCriterion
from jerry.testing.evaluation.debiasing import DebiasingStrategy
from jerry.testing.evaluation.exceptions import (
    EvaluationAPIError,
    EvaluationConfigError,
    EvaluationScoringError,
)
from jerry.testing.evaluation.jerry_geval_deepeval_metric import (
    JerryGEvalDeepEvalMetric,
)
from jerry.testing.evaluation.metrics import JerryGEvalMetric
from jerry.testing.metamorphic.base import MetamorphicRelation
from jerry.testing.types import ScoreArray

logger = logging.getLogger(__name__)

#: Maximum character length for LLMTestCase actual_output.
#: Outputs exceeding this length are truncated before DeepEval metric
#: construction to prevent unbounded token consumption in the LLM judge
#: and to guard against oversized payloads crashing the evaluation pipeline.
_MAX_OUTPUT_CHARS: int = 8000


@dataclass
class DeepEvalAdapter:
    """Public evaluation adapter implementing the EvaluationPort protocol.

    This is the primary entry point for Layer 2 evaluation and the sole
    named class defined in this module (H-10). It creates configured
    DeepEval BaseMetric instances for specific agents and provides batch
    evaluation for score array collection (FR-009).

    The adapter is injected via the pytest conftest.py ``evaluator`` fixture
    (FR-006). It is not imported by any domain module (H-07 enforcement).

    Attributes:
        model_name: LLM model identifier for DeepEval's G-Eval judge.
            Defaults to ``claude-sonnet-4-20250514`` per design spec.
        debiasing_strategy: DebiasingStrategy for position randomization
            and rubric shuffling (C-007 mandatory).
        default_threshold: Default pass/fail threshold for metric assertions.
            Per-agent thresholds override this when creating agent-specific
            metrics via ``build_metric_for_agent()``.

    Example::

        from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter
        from jerry.testing.evaluation.debiasing import DebiasingStrategy
        from jerry.testing.evaluation.criteria.ps_researcher import (
            PS_RESEARCHER_CRITERIA,
        )

        adapter = DeepEvalAdapter(
            model_name="claude-sonnet-4-20250514",
            debiasing_strategy=DebiasingStrategy(),
        )
        metric = adapter.build_metric_for_agent(
            agent_name="ps-researcher",
            criteria=PS_RESEARCHER_CRITERIA,
            quality_floor=0.82,
        )
        # metric is a BaseMetric subclass ready for deepeval.assert_test()

    References:
        - FR-006: DeepEval pytest plugin integration (conftest evaluator fixture)
        - FR-009: Score array collection and export
        - system-design.md §2.2: EvaluationPort protocol
    """

    model_name: str = "claude-sonnet-4-20250514"
    debiasing_strategy: DebiasingStrategy = field(default_factory=DebiasingStrategy)
    default_threshold: float = 0.82

    def __post_init__(self) -> None:
        """Validate configuration at construction time."""
        if not 0.0 < self.default_threshold <= 1.0:
            raise ValueError(
                f"default_threshold must be in (0.0, 1.0], got {self.default_threshold}"
            )
        if self.debiasing_strategy is None:
            raise ValueError(
                "DeepEvalAdapter requires a DebiasingStrategy (C-007 mandatory). "
                "Pass an explicit DebiasingStrategy() instance."
            )
        if "claude" in self.model_name.lower():
            api_key = os.environ.get("ANTHROPIC_API_KEY", "")
            if not api_key:
                raise EvaluationConfigError(
                    f"ANTHROPIC_API_KEY environment variable is required when using Claude models "
                    f"(model_name='{self.model_name}'). Set it in .env or CI secrets.",
                    context={
                        "field": "ANTHROPIC_API_KEY",
                        "model_name": self.model_name,
                    },
                )

    def build_metric_for_agent(
        self,
        agent_name: str,
        criteria: list[QualityCriterion],
        quality_floor: float | None = None,
    ) -> BaseMetric:
        """Build a DeepEval BaseMetric for a specific Jerry agent.

        Creates a JerryGEvalMetric domain object with the provided criteria
        and debiasing strategy, then wraps it in a JerryGEvalDeepEvalMetric
        adapter ready for use in DeepEval test cases.

        Args:
            agent_name: Name of the target agent (e.g., ``"ps-researcher"``).
                Used for logging and score labeling.
            criteria: List of QualityCriterion objects for this agent.
                Source: ``jerry.testing.evaluation.criteria.{agent_module}``.
            quality_floor: Minimum acceptable score for DeepEval's binary
                assertion. Should be the agent's ``overall_floor`` from
                behavioral-contracts.md. Defaults to ``self.default_threshold``.

        Returns:
            Configured JerryGEvalDeepEvalMetric instance ready for pytest
            integration. The returned metric applies S-014 weighted scoring
            with mandatory debiasing on every ``measure()`` call.

        Example::

            metric = adapter.build_metric_for_agent(
                agent_name="ps-researcher",
                criteria=PS_RESEARCHER_CRITERIA,
                quality_floor=0.82,
            )
            deepeval.assert_test(test_case, [metric])

        References:
            - FR-006: DeepEval pytest plugin integration
            - FR-007: G-Eval custom criteria evaluation
        """
        threshold = quality_floor if quality_floor is not None else self.default_threshold

        domain_metric = JerryGEvalMetric(
            criteria=criteria,
            debiasing=self.debiasing_strategy,
            agent_name=agent_name,
            require_debiasing=True,
        )

        return JerryGEvalDeepEvalMetric(
            jerry_metric=domain_metric,
            threshold=threshold,
            model=self.model_name,
            include_reason=True,
        )

    def build_metric_for_mr(  # CG-010
        self,
        mr: MetamorphicRelation,
        quality_floor: float | None = None,
    ) -> JerryGEvalDeepEvalMetric:
        """Build a JerryGEvalDeepEvalMetric configured for a metamorphic relation.

        Constructs a single ``QualityCriterion`` from the MR's ``mr_id`` and
        ``mr_name`` class attributes and wraps it in a ``JerryGEvalDeepEvalMetric``
        ready for use in DeepEval test cases.  The criterion rubric asks the
        LLM judge to assess whether the output satisfies the named metamorphic
        relation invariant, providing a G-Eval score for MR-level quality
        gating in the Four-Layer Composite Test Harness.

        The returned metric applies mandatory debiasing (C-007 / FR-021) on
        every ``measure()`` call, consistent with ``build_metric_for_agent()``.

        Args:
            mr: A ``MetamorphicRelation`` instance (e.g., ``ParaphraseConsistency()``).
                Must have non-empty ``mr_id`` and ``mr_name`` class attributes.
            quality_floor: Minimum acceptable G-Eval score for DeepEval's binary
                assertion.  Defaults to ``self.default_threshold``.

        Returns:
            Configured ``JerryGEvalDeepEvalMetric`` instance.  The metric name
            is ``mr.mr_id`` (e.g., ``"MR-001"``); the single criterion weight
            is 1.0 (only one criterion, so composite == criterion score).

        Raises:
            ValueError: If ``mr.mr_id`` or ``mr.mr_name`` is empty, since both
                are required to construct a meaningful criterion description.

        Example::

            from jerry.testing.metamorphic.mr_001_paraphrase import ParaphraseConsistency
            from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter

            mr = ParaphraseConsistency()
            adapter = DeepEvalAdapter()
            metric = adapter.build_metric_for_mr(mr, quality_floor=0.80)
            # metric is a JerryGEvalDeepEvalMetric ready for deepeval.assert_test()

        Design note — G-Eval as quality-signal proxy:
            This method uses G-Eval (LLM-as-Judge) as a *proxy* quality signal
            for pytest-level pass/fail gating.  It asks the judge whether the
            output appears to satisfy the named MR invariant, yielding a
            continuous score that can be threshold-gated in the same way as
            agent-level criteria scores.  This is distinct from the *full MR
            evaluation protocol*, which involves ``mr.transform()`` to produce
            a transformed input, ``mr.evaluate()`` to compare paired score
            distributions (original vs. transformed), and Wilcoxon signed-rank
            statistics for rigorous invariant verification.  Use this method
            (G-Eval proxy path) for fast, single-output quality gating inside
            individual pytest test cases; use the full MR protocol
            (``mr.transform()`` + ``mr.evaluate()``) for statistical MR results
            across batches of N >= 20 paired runs (Layer 3 / Layer 4 of the
            Four-Layer Composite Test Harness).

        References:
            - CG-010: build_metric_for_mr() addition to DeepEvalAdapter
            - FR-010: Five Universal Metamorphic Relations
            - FR-021: Debiasing (position randomization + rubric shuffling, C-007)
            - system-design.md §1.4: Dependency graph and G-Eval-as-proxy design path
            - GAP-L3-BASECLASS: Domain ABC pattern vs. DeepEval BaseMetric inheritance
        """
        if not mr.mr_id:
            raise ValueError(
                "MetamorphicRelation.mr_id must be non-empty to build a metric. "
                "Ensure the concrete MR subclass sets mr_id as a class attribute."
            )
        if not mr.mr_name:
            raise ValueError(
                "MetamorphicRelation.mr_name must be non-empty to build a metric. "
                "Ensure the concrete MR subclass sets mr_name as a class attribute."
            )

        threshold = quality_floor if quality_floor is not None else self.default_threshold

        criterion = QualityCriterion(
            name=mr.mr_id,
            description=(
                f"The output satisfies the '{mr.mr_name}' metamorphic relation "
                f"invariant ({mr.mr_id}): the quality of the LLM response is "
                f"stable under the transformation defined by this relation. "
                f"Score 1.0 if the response would receive a similar quality "
                f"assessment regardless of the transformation; score 0.0 if the "
                f"transformation produces a meaningfully different output quality."
            ),
            weight=1.0,
            dimension=mr.mr_id,
        )

        domain_metric = JerryGEvalMetric(
            criteria=[criterion],
            debiasing=self.debiasing_strategy,
            agent_name=mr.mr_id,
            require_debiasing=True,
        )

        return JerryGEvalDeepEvalMetric(
            jerry_metric=domain_metric,
            threshold=threshold,
            model=self.model_name,
            include_reason=True,
        )

    def evaluate(
        self,
        prompt: str,
        output: str,
        criteria: list[str],
        agent_name: str,
    ) -> dict[str, float]:
        """Evaluate a single LLM output against named criteria (EvaluationPort).

        Implements the ``EvaluationPort.evaluate()`` protocol. This method
        accepts criterion names as strings for protocol compatibility.

        Note: The recommended evaluation path is ``build_metric_for_agent()``
        combined with ``deepeval.assert_test()``. This method provides
        programmatic single-shot access for callers that cannot use the
        pytest plugin integration (FR-006). Criterion name strings are
        resolved to ``QualityCriterion`` objects by the caller-registered
        criteria sets; this method raises ``NotImplementedError`` when
        string-to-criterion resolution is required but not yet implemented
        in this adapter revision.

        Args:
            prompt: The input prompt sent to the agent under test.
            output: The agent's response text to evaluate.
            criteria: List of criterion names to evaluate. Must match names
                in the agent's QualityCriterion list.
            agent_name: Name of the agent being evaluated.

        Returns:
            Dictionary mapping criterion name to score in [0.0, 1.0].

        Raises:
            ValueError: If ``criteria`` is empty.
            NotImplementedError: String-name criterion resolution is not yet
                implemented. Pass ``QualityCriterion`` objects via
                ``build_metric_for_agent()`` for real evaluation.

        References:
            - system-design.md §2.2: EvaluationPort.evaluate() signature
        """
        if not criteria:
            raise ValueError("evaluate() requires at least one criterion name.")

        raise NotImplementedError(
            f"DeepEvalAdapter.evaluate() requires QualityCriterion objects, not "
            f"criterion name strings. For programmatic single-shot evaluation of "
            f"agent '{agent_name}', use build_metric_for_agent() with a "
            f"QualityCriterion list and call metric.measure(LLMTestCase(...)) "
            f"directly. String-name resolution is not implemented in this adapter. "
            f"See FR-006 and system-design.md §2.2."
        )

    def _pre_batch_health_check(
        self,
        outputs: list[str],
        criteria: list[QualityCriterion],
    ) -> None:
        """Validate batch pre-conditions before the evaluation loop (PAT-001).

        Raises ``EvaluationConfigError`` for any condition that would cause
        every output in the batch to fail, preventing silent all-zero arrays.

        Checks performed:
        1. ``self.model_name`` is not empty.
        2. ``criteria`` list is not empty.
        3. ``outputs`` list is not empty.
        4. ``ANTHROPIC_API_KEY`` is set when ``model_name`` contains "claude".

        Args:
            outputs: List of LLM response texts to be evaluated.
            criteria: List of QualityCriterion objects for this batch.

        Raises:
            EvaluationConfigError: If any pre-condition fails. The batch
                MUST be aborted; these errors are not transient.
        """
        if not self.model_name:
            raise EvaluationConfigError(
                "model_name is empty. Set a valid LLM model identifier "
                "(e.g., 'claude-sonnet-4-20250514') on the DeepEvalAdapter.",
                context={"field": "model_name", "value": repr(self.model_name)},
            )
        if not criteria:
            raise EvaluationConfigError(
                "criteria list is empty. Provide at least one QualityCriterion "
                "to evaluate_batch().",
                context={"field": "criteria", "value": "[]"},
            )
        if not outputs:
            raise EvaluationConfigError(
                "outputs list is empty. Provide at least one LLM response text "
                "to evaluate_batch().",
                context={"field": "outputs", "value": "[]"},
            )
        if "claude" in self.model_name.lower():
            api_key = os.environ.get("ANTHROPIC_API_KEY", "")
            if not api_key:
                raise EvaluationConfigError(
                    f"ANTHROPIC_API_KEY is not set. This environment variable is "
                    f"required when model_name='{self.model_name}' (Claude model). "
                    f"Set it in .env or CI secrets before running the evaluation batch.",
                    context={
                        "field": "ANTHROPIC_API_KEY",
                        "model_name": self.model_name,
                    },
                )

    def evaluate_batch(
        self,
        prompt: str,
        outputs: list[str],
        criteria: list[QualityCriterion],
        agent_name: str,
        version_key: str | None = None,
    ) -> dict[str, ScoreArray]:
        """Evaluate N outputs and return score arrays per criterion (FR-009).

        Runs the metric against each output individually, collecting one
        score per criterion per output. Debiasing is applied independently
        on each evaluation call: criterion order is reshuffled for every
        output, ensuring positional bias cannot accumulate across the batch.

        Each criterion in the returned dictionary has a list of N float scores,
        one per output in the batch. The ``"composite"`` key additionally maps
        to the weighted composite score array.

        Args:
            prompt: The input prompt (same for all outputs in the batch).
            outputs: List of N LLM response texts to evaluate.
            criteria: List of QualityCriterion objects (not just names).
            agent_name: Name of the agent being evaluated.
            version_key: Optional version identifier for this set of outputs.
                Passed through for caller's baseline-store bookkeeping; not
                used internally by this method.

        Returns:
            Dictionary with one key per criterion name (populated with N
            per-criterion scores) plus a ``"composite"`` key (weighted
            composite score list). All values are lists of N floats in
            [0.0, 1.0]. Length of each list equals ``len(outputs)``.
            Suitable for ScoreArray construction by Layer 4 statistical
            engine (FR-009).

        Raises:
            ValueError: If ``outputs`` or ``criteria`` is empty.

        Example::

            scores = adapter.evaluate_batch(
                prompt="Survey authentication patterns...",
                outputs=["## L0...\\n## L1...\\n## L2..."] * 30,
                criteria=PS_RESEARCHER_CRITERIA,
                agent_name="ps-researcher",
            )
            # scores["composite"] is a list of 30 floats
            # scores["completeness"] is a list of 30 per-criterion floats

        References:
            - FR-009: Score array collection and export ("one array of N scores per metric")
            - FR-021: Debiasing applied per-evaluation (not per-batch)
        """
        if not outputs:
            raise ValueError("evaluate_batch() requires at least one output.")
        if not criteria:
            raise ValueError("evaluate_batch() requires at least one criterion.")

        # PAT-001: pre-batch health check — raises EvaluationConfigError on
        # any condition that would cause every output to silently score 0.0.
        self._pre_batch_health_check(outputs=outputs, criteria=criteria)

        # Initialize per-criterion score lists (FR-009: one array per metric)
        score_lists: dict[str, ScoreArray] = {c.name: [] for c in criteria}
        score_lists["composite"] = []

        domain_metric = JerryGEvalMetric(
            criteria=criteria,
            debiasing=self.debiasing_strategy,
            agent_name=agent_name,
            require_debiasing=True,
        )

        deepeval_metric = JerryGEvalDeepEvalMetric(
            jerry_metric=domain_metric,
            threshold=self.default_threshold,
            model=self.model_name,
        )

        for i, output_text in enumerate(outputs):
            # CG-017: Truncate oversized outputs before LLMTestCase construction
            # to prevent unbounded token consumption in the DeepEval LLM judge.
            if len(output_text) > _MAX_OUTPUT_CHARS:
                logger.warning(
                    "Batch evaluation run %d/%d for agent '%s': output_text truncated "
                    "from %d to %d characters (CG-017 _MAX_OUTPUT_CHARS limit).",
                    i + 1,
                    len(outputs),
                    agent_name,
                    len(output_text),
                    _MAX_OUTPUT_CHARS,
                )
                output_text = output_text[:_MAX_OUTPUT_CHARS]
            test_case = LLMTestCase(
                input=prompt,
                actual_output=output_text,
            )
            try:
                # evaluate_criteria returns per-criterion ScoringResults with
                # the domain composite logic, capturing both composite and
                # individual scores for FR-009 score array collection.
                debiased_criteria = domain_metric.get_criteria_for_debiasing()
                scoring_results = deepeval_metric.evaluate_criteria(
                    criteria=debiased_criteria,
                    test_case=test_case,
                )

                # Accumulate per-criterion scores (FR-009: one array per metric)
                criterion_name_to_score: dict[str, float] = {
                    r.criterion_name: r.score for r in scoring_results
                }
                for criterion in criteria:
                    per_criterion_score = criterion_name_to_score.get(criterion.name, 0.0)
                    score_lists[criterion.name].append(per_criterion_score)

                # Accumulate composite score
                if scoring_results:
                    composite = domain_metric.score_composite(scoring_results)
                else:
                    composite = 0.0
                score_lists["composite"].append(composite)

                logger.debug(
                    "Batch evaluation run %d/%d for agent '%s': composite=%.3f, criteria_scored=%d",
                    i + 1,
                    len(outputs),
                    agent_name,
                    composite,
                    len(scoring_results),
                )

            except EvaluationConfigError:
                # Config errors abort the entire batch — do not swallow.
                # A config error on one output will affect every output.
                raise
            except EvaluationAPIError as exc:
                logger.warning(
                    "Transient API error on output %d/%d for agent '%s': %s. "
                    "Appending 0.0 for this run across all criteria.",
                    i + 1,
                    len(outputs),
                    agent_name,
                    exc,
                )
                for criterion in criteria:
                    score_lists[criterion.name].append(0.0)
                score_lists["composite"].append(0.0)
            except EvaluationScoringError as exc:
                logger.warning(
                    "Scoring failure on output %d/%d for agent '%s': %s. "
                    "Appending 0.0 for this run across all criteria.",
                    i + 1,
                    len(outputs),
                    agent_name,
                    exc,
                )
                for criterion in criteria:
                    score_lists[criterion.name].append(0.0)
                score_lists["composite"].append(0.0)
            except Exception as exc:  # noqa: BLE001 -- last resort; wrap and log
                logger.warning(
                    "Unexpected error on output %d/%d for agent '%s': %s. "
                    "Appending 0.0 for this run across all criteria.",
                    i + 1,
                    len(outputs),
                    agent_name,
                    exc,
                )
                for criterion in criteria:
                    score_lists[criterion.name].append(0.0)
                score_lists["composite"].append(0.0)

        # Post-batch zero-array assertion: if more than 20% of composite scores
        # are 0.0, the batch likely experienced systemic failures (e.g., all API
        # calls failed, credentials invalid, model unavailable). Surface this as
        # EvaluationScoringError rather than returning a silent all-zero array.
        composite_scores: ScoreArray = score_lists["composite"]
        if composite_scores:
            zero_count = sum(1 for s in composite_scores if s == 0.0)
            zero_fraction = zero_count / len(composite_scores)
            if zero_fraction > 0.20:
                raise EvaluationScoringError(
                    f"Batch evaluation for agent '{agent_name}' produced "
                    f"{zero_count}/{len(composite_scores)} zero composite scores "
                    f"({zero_fraction:.0%}), exceeding the 20% systemic-failure "
                    f"threshold. Inspect logs for per-output errors. "
                    f"Common causes: API key invalid, model unavailable, rate limit "
                    f"exhausted, or DeepEval internal error on most outputs.",
                    context={
                        "agent": agent_name,
                        "zero_count": str(zero_count),
                        "total": str(len(composite_scores)),
                        "zero_fraction": f"{zero_fraction:.3f}",
                    },
                )

        return score_lists
