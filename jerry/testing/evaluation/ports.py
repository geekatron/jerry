# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Layer 2 port interface: EvaluationPort protocol.

Defines the inbound hexagonal port for metric evaluation backends. Any
evaluation backend that integrates with the Four-Layer Composite Test Harness
must satisfy this protocol.

Current implementation: DeepEvalAdapter
    (jerry/testing/evaluation/deepeval_adapter.py)

Architecture (H-07):
    This is a PORT module in the hexagonal sense. It imports ONLY from stdlib
    and from domain types. It does NOT import from DeepEval, promptfoo, scipy,
    or any concrete adapter. The protocol enables the pytest conftest to inject
    a DeepEvalAdapter without coupling to the deepeval library at the fixture
    definition level.

H-10: This file contains exactly one class: EvaluationPort.

References:
    - system-design.md §2.2: EvaluationPort protocol definition
    - FR-006: DeepEval pytest plugin integration (conftest evaluator fixture)
    - FR-009: Score array collection and export
    - contracts/behavioral-contracts.md §D.2: Score array format
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from jerry.testing.types import ScoreArray

if TYPE_CHECKING:
    from jerry.testing.evaluation.criterion import QualityCriterion


@runtime_checkable
class EvaluationPort(Protocol):
    """Port for evaluating LLM outputs against quality criteria.

    Any evaluation backend must satisfy this protocol. The ``evaluate()``
    method accepts criterion names as strings for simple single-shot usage.
    The ``evaluate_batch()`` method accepts ``QualityCriterion`` objects
    for full rubric-based evaluation with debiasing.

    Current implementation: ``DeepEvalAdapter`` in
    ``jerry/testing/evaluation/deepeval_adapter.py``.

    Usage via pytest fixture::

        # conftest.py
        @pytest.fixture
        def evaluator() -> EvaluationPort:
            return DeepEvalAdapter()

        # test file
        def test_ps_researcher(evaluator: EvaluationPort) -> None:
            scores = evaluator.evaluate(
                prompt="Survey authentication patterns...",
                output=agent_output,
                criteria=["completeness", "evidence_quality"],
                agent_name="ps-researcher",
            )
            assert scores["completeness"] >= 0.82

    References:
        - system-design.md §2.2: EvaluationPort (Layer 2 inbound)
        - FR-006: DeepEval pytest plugin integration
        - FR-009: Score array collection and export
    """

    def evaluate(
        self,
        prompt: str,
        output: str,
        criteria: list[str],
        agent_name: str,
    ) -> dict[str, float]:
        """Evaluate a single LLM output against named criteria.

        Performs a single evaluation run of the given output against each
        named criterion. The recommended path for statistical evaluation is
        ``evaluate_batch()`` (N=30 runs per FR-009).

        Args:
            prompt: The input prompt sent to the LLM under test.
            output: The LLM's response text to evaluate.
            criteria: List of criterion names to score. Names must match
                criterion names registered for the given agent.
            agent_name: Name of the agent being evaluated
                (e.g., ``"ps-researcher"``).

        Returns:
            Dictionary mapping each criterion name to a score in [0.0, 1.0].

        Raises:
            ValueError: If ``criteria`` is empty.

        References:
            - system-design.md §2.2: EvaluationPort.evaluate() signature
        """
        ...

    def evaluate_batch(
        self,
        prompt: str,
        outputs: list[str],
        criteria: list[QualityCriterion],
        agent_name: str,
        version_key: str | None = None,
    ) -> dict[str, ScoreArray]:
        """Evaluate N outputs and return score arrays per criterion (FR-009).

        Runs each output through the evaluation backend independently,
        collecting one score per criterion per output. Debiasing is applied
        independently on each run so positional bias cannot accumulate across
        the batch.

        Args:
            prompt: The input prompt (same for all outputs in the batch).
            outputs: List of N LLM response texts to evaluate.
            criteria: List of QualityCriterion objects defining the rubric.
            agent_name: Name of the agent being evaluated.
            version_key: Optional version identifier for this set of outputs.
                Used by the baseline store to index the resulting ScoreArrays.

        Returns:
            Dictionary mapping each criterion name to a ``ScoreArray``
            (a list of N float scores in [0.0, 1.0]). The ``"composite"``
            key additionally maps to the weighted composite score array.

        Raises:
            ValueError: If ``outputs`` or ``criteria`` is empty.

        References:
            - FR-009: Score array collection and export
            - system-design.md §2.2: EvaluationPort.evaluate_batch() signature
            - contracts/behavioral-contracts.md §D.2: Score array format
        """
        ...
