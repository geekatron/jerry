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
from jerry.testing.evaluation.jerry_geval_deepeval_metric import (
    JerryGEvalDeepEvalMetric,
)
from jerry.testing.evaluation.metrics import JerryGEvalMetric
from jerry.testing.types import ScoreArray

logger = logging.getLogger(__name__)


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

            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    "Batch evaluation failed on output %d/%d for agent '%s': %s. "
                    "Appending 0.0 for this run across all criteria.",
                    i + 1,
                    len(outputs),
                    agent_name,
                    exc,
                )
                for criterion in criteria:
                    score_lists[criterion.name].append(0.0)
                score_lists["composite"].append(0.0)

        return score_lists
