"""Layer 2 adapter: JerryGEvalDeepEvalMetric — DeepEval BaseMetric subclass.

Bridges the domain layer (JerryGEvalMetric, QualityCriterion) to DeepEval's
BaseMetric interface required for pytest plugin integration (FR-006).

This is the ONLY class in this package that inherits from DeepEval's
``BaseMetric``. Domain modules (metrics.py, debiasing.py, criterion.py,
scoring_result.py, and all criteria/*.py files) do NOT import from DeepEval.

H-10: This file contains exactly one class: JerryGEvalDeepEvalMetric.
      DeepEvalAdapter lives in deepeval_adapter.py.

Architecture (H-07):
    ADAPTER layer — this module imports from deepeval (external framework).
    Domain code (JerryGEvalMetric, QualityCriterion, ScoringResult) never
    imports from this module. The dependency arrow runs:
        deepeval_adapter.py -> jerry_geval_deepeval_metric.py -> domain types

References:
    - FR-006: DeepEval pytest plugin integration
    - FR-007: G-Eval custom criteria evaluation
    - FR-021: Debiasing (applied in measure())
    - system-design.md §1.3: deepeval_adapter.py / DeepEvalAdapter in decomposition
"""

from __future__ import annotations

import asyncio
import logging

try:
    from deepeval.metrics import BaseMetric, GEval
    from deepeval.test_case import LLMTestCase, LLMTestCaseParams
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "deepeval is required for the Layer 2 evaluation adapter. "
        "Install it with: uv add deepeval\n"
        "See FR-006 (DeepEval pytest plugin integration) and "
        "projects/PROJ-036-prompt-regression-harness/requirements/harness-requirements.md"
    ) from exc

from jerry.testing.evaluation.criterion import QualityCriterion
from jerry.testing.evaluation.metrics import JerryGEvalMetric
from jerry.testing.evaluation.scoring_result import ScoringResult

logger = logging.getLogger(__name__)


class JerryGEvalDeepEvalMetric(BaseMetric):  # type: ignore[misc]
    """DeepEval BaseMetric adapter wrapping JerryGEvalMetric domain logic.

    Translates between the DeepEval pytest plugin interface and the Jerry
    domain layer. Applies mandatory debiasing (criterion order shuffling) on
    every ``measure()`` call per C-007 / FR-021.

    This class is instantiated by ``DeepEvalAdapter.build_metric_for_agent()``.
    Do not instantiate it directly in test code — use the adapter.

    Attributes:
        threshold: Minimum acceptable score for DeepEval's pass/fail assertion.
        model: LLM model identifier for G-Eval judge calls.
        include_reason: Whether to include judge rationale in output.

    References:
        - FR-006: DeepEval pytest plugin integration
        - FR-007: G-Eval custom criteria evaluation
        - FR-021: Debiasing (C-007)
    """

    def __init__(
        self,
        jerry_metric: JerryGEvalMetric,
        threshold: float = 0.82,
        model: str | None = None,
        include_reason: bool = True,
    ) -> None:
        """Initialize the DeepEval adapter for a JerryGEvalMetric.

        Args:
            jerry_metric: Domain-layer metric with criteria and debiasing.
                Must have a non-None debiasing strategy (C-007).
            threshold: Minimum score for DeepEval's binary assertion.
                Defaults to 0.82 (lowest agent quality floor across all
                five target agents). Callers should set this to the target
                agent's quality floor from behavioral-contracts.md.
            model: LLM model identifier for the G-Eval judge.
                Defaults to None (DeepEval uses its configured default).
            include_reason: If True, DeepEval includes the LLM judge's
                rationale in the metric output (P-022 traceability).

        Raises:
            ValueError: If jerry_metric.require_debiasing is True and
                jerry_metric.debiasing is None. Debiasing is MANDATORY
                (C-007 / FR-021).
        """
        self.threshold = threshold
        self.model = model
        self.include_reason = include_reason
        self._jerry_metric = jerry_metric

        # Validate debiasing is present (C-007 mandatory debiasing)
        if jerry_metric.require_debiasing and jerry_metric.debiasing is None:
            raise ValueError(
                f"G-Eval metric for agent '{jerry_metric.agent_name}': "
                "debiasing is MANDATORY (C-007 / FR-021). "
                "Pass a DebiasingStrategy instance to JerryGEvalMetric."
            )

        # DeepEval BaseMetric init; name displayed in test output
        super().__init__()
        self.name = f"Jerry-GEval [{jerry_metric.agent_name}]"

    def measure(
        self,
        test_case: LLMTestCase,
        *args: object,
        **kwargs: object,
    ) -> float:
        """Evaluate the test case output against Jerry G-Eval criteria.

        Applies debiasing (criterion shuffling) before invoking the LLM
        judge via DeepEval's G-Eval framework. Aggregates per-criterion
        scores using the domain composite computation.

        Args:
            test_case: DeepEval LLMTestCase containing:
                - input: The prompt sent to the agent under test.
                - actual_output: The agent's response to evaluate.

        Returns:
            Weighted composite quality score in [0.0, 1.0].

        References:
            - FR-007: G-Eval evaluation
            - FR-021: Debiasing (criterion shuffling applied here)
        """
        score = self._evaluate_synchronously(test_case)
        self.score = score
        self.success = score >= self.threshold
        self.reason = self._build_reason_string(score)
        return score

    async def a_measure(
        self,
        test_case: LLMTestCase,
        *args: object,
        **kwargs: object,
    ) -> float:
        """Async evaluation -- DeepEval calls this in async test contexts.

        Delegates to the synchronous evaluation via a thread executor to
        avoid blocking the event loop.

        Args:
            test_case: DeepEval LLMTestCase (same as measure()).

        Returns:
            Weighted composite quality score in [0.0, 1.0].
        """
        loop = asyncio.get_running_loop()
        score = await loop.run_in_executor(None, self._evaluate_synchronously, test_case)
        self.score = score
        self.success = score >= self.threshold
        self.reason = self._build_reason_string(score)
        return score

    def is_successful(self) -> bool:
        """Return True if the last measured score meets the threshold.

        DeepEval calls this after measure() to determine pass/fail.

        Returns:
            True if self.score >= self.threshold.
        """
        return getattr(self, "success", False)

    @property
    def __name__(self) -> str:
        """Metric name property for DeepEval test output display."""
        return self.name

    def _evaluate_synchronously(self, test_case: LLMTestCase) -> float:
        """Core evaluation: debias, build criteria, invoke G-Eval, aggregate.

        Steps:
        1. Retrieves debiased (shuffled) criteria from the domain metric.
        2. Translates each QualityCriterion to a DeepEval evaluation step.
        3. Invokes DeepEval's GEval for each criterion individually.
        4. Constructs ScoringResult objects and aggregates via
           score_composite().

        On any DeepEval error, returns 0.0 and logs the failure rather
        than raising, to prevent individual metric failures from blocking
        the full test suite.

        Args:
            test_case: DeepEval LLMTestCase with input and actual_output.

        Returns:
            Weighted composite score in [0.0, 1.0], or 0.0 on error.
        """
        try:
            # Step 1: Get debiased criteria (criterion order shuffled per FR-021)
            debiased_criteria = self._jerry_metric.get_criteria_for_debiasing()

            # Step 2: Evaluate each criterion via DeepEval GEval
            scoring_results = self.evaluate_criteria(
                criteria=debiased_criteria,
                test_case=test_case,
            )

            # Step 3: Aggregate via domain composite computation
            if not scoring_results:
                logger.warning(
                    "No scoring results produced for agent '%s'. "
                    "Returning 0.0. Check DeepEval configuration and API key.",
                    self._jerry_metric.agent_name,
                )
                return 0.0

            composite = self._jerry_metric.score_composite(scoring_results)

            classification = self._jerry_metric.classify_composite(composite)
            logger.debug(
                "Agent '%s' evaluation: composite=%.3f, classification=%s, criteria_evaluated=%d",
                self._jerry_metric.agent_name,
                composite,
                classification,
                len(scoring_results),
            )

            return composite

        except Exception as exc:  # noqa: BLE001 -- catch-all for adapter resilience
            logger.error(
                "DeepEval evaluation failed for agent '%s': %s. "
                "Returning 0.0. Inspect test output for DeepEval errors.",
                self._jerry_metric.agent_name,
                exc,
            )
            return 0.0

    def evaluate_criteria(
        self,
        criteria: list[QualityCriterion],
        test_case: LLMTestCase,
    ) -> list[ScoringResult]:
        """Evaluate each criterion via DeepEval GEval and return ScoringResults.

        Translates each QualityCriterion into a DeepEval GEval metric,
        measures it against the test case, and wraps the result in a domain
        ScoringResult for aggregation.

        Per-criterion invocation is intentional: it gives score_composite()
        the granular dimension scores needed for S-014 weighted aggregation,
        and prevents the LLM judge from conflating criteria during a
        multi-criterion evaluation call.

        Args:
            criteria: Debiased (shuffled) list of QualityCriterion.
            test_case: LLMTestCase with input and actual_output.

        Returns:
            List of ScoringResult objects, one per successfully evaluated
            criterion. Failed criteria are logged and excluded; the
            score_composite() normalizer handles partial criterion sets.
        """
        results: list[ScoringResult] = []

        for criterion in criteria:
            try:
                # Build per-criterion GEval metric with criterion description
                # as the sole evaluation step (FR-007 standard GEval pattern).
                g_eval = GEval(
                    name=criterion.name,
                    criteria=criterion.description,
                    evaluation_params=[
                        LLMTestCaseParams.INPUT,
                        LLMTestCaseParams.ACTUAL_OUTPUT,
                    ],
                    model=self.model,
                    threshold=0.0,  # Raw score only; pass/fail at adapter level
                )
                g_eval.measure(test_case)

                raw_score: float = float(g_eval.score or 0.0)
                evidence: str = str(g_eval.reason or "No rationale provided by judge.")

                # Clamp to [0.0, 1.0] to guard against DeepEval edge cases
                raw_score = max(0.0, min(1.0, raw_score))

                results.append(
                    ScoringResult(
                        criterion_name=criterion.name,
                        score=raw_score,
                        weight=criterion.weight,
                        evidence=evidence,
                        debiasing_applied=True,
                    )
                )

            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    "GEval evaluation failed for criterion '%s' on agent '%s': %s. "
                    "Criterion excluded from composite score.",
                    criterion.name,
                    self._jerry_metric.agent_name,
                    exc,
                )
                # Excluded criteria: score_composite() normalizes by the sum
                # of included weights, so partial failures degrade gracefully.

        return results

    def _build_reason_string(self, composite_score: float) -> str:
        """Build a human-readable reason string for DeepEval test output.

        Args:
            composite_score: Weighted composite score in [0.0, 1.0].

        Returns:
            Formatted reason string with score, classification, and status.
        """
        classification = self._jerry_metric.classify_composite(composite_score)
        status = "PASS" if getattr(self, "success", False) else "FAIL"
        return (
            f"[{status}] Agent={self._jerry_metric.agent_name} | "
            f"Composite={composite_score:.3f} | "
            f"Classification={classification} | "
            f"Threshold={self.threshold:.2f}"
        )
