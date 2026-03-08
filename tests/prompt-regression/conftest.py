# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Shared pytest configuration for tests/prompt-regression/.

Adds the tests/prompt-regression directory to sys.path so that the
standalone version_keys.py module (which does not reside in the jerry
package) can be imported by test files without per-file path manipulation.

Moved from test_version_keys.py per eng-qa iter2 fix: Actionability (0.90
→ 0.93+) — sys.path manipulation belongs in conftest.py, not individual
test files.

Fixtures:
    evaluator: Session-scoped DeepEvalAdapter configured as an EvaluationPort.
        Model is resolved from ANTHROPIC_MODEL env var with fallback to
        "claude-sonnet-4-20250514". Applies a default DebiasingStrategy()
        per C-007 mandatory debiasing requirement.

References:
    - FR-004: Version key composite format {commit_hash}:{file_path}
    - FR-006: DeepEval pytest plugin integration (evaluator fixture)
    - FR-021: Debiasing (C-007 mandatory, DebiasingStrategy)
    - tests/prompt-regression/version_keys.py
"""

from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter

# Ensure the tests/prompt-regression directory is on sys.path so that
# `from version_keys import ...` works in unit test files.
_PR_TEST_DIR = os.path.dirname(__file__)
if _PR_TEST_DIR not in sys.path:
    sys.path.insert(0, _PR_TEST_DIR)

#: Default model identifier when ANTHROPIC_MODEL is not set.
_DEFAULT_MODEL: str = "claude-sonnet-4-20250514"


# CG-011
@pytest.fixture(scope="session")
def evaluator() -> DeepEvalAdapter:
    """Return a session-scoped DeepEvalAdapter configured as an EvaluationPort.

    The adapter is constructed once per test session and shared across all
    tests, avoiding redundant initialisation overhead for the LLM judge
    client (FR-006 efficiency).

    Model resolution order:
        1. ``ANTHROPIC_MODEL`` environment variable (allows CI overrides).
        2. Hard-coded default ``"claude-sonnet-4-20250514"`` (design spec §2.2).

    The ``DebiasingStrategy()`` instance is constructed with default
    parameters (random seed unset, all debiasing modes active) per C-007
    mandatory debiasing requirement (FR-021).

    Returns:
        DeepEvalAdapter: Fully configured adapter implementing the
        EvaluationPort protocol, ready for use with
        ``adapter.build_metric_for_agent()`` and ``deepeval.assert_test()``.

    Raises:
        EvaluationConfigError: If ``ANTHROPIC_API_KEY`` is not set and the
            resolved model name contains "claude" (checked at construction).

    Example::

        def test_ps_researcher_quality(evaluator):
            metric = evaluator.build_metric_for_agent(
                agent_name="ps-researcher",
                criteria=PS_RESEARCHER_CRITERIA,
                quality_floor=0.82,
            )
            deepeval.assert_test(test_case, [metric])

    References:
        - FR-006: DeepEval pytest plugin integration
        - FR-021: Debiasing (C-007 mandatory)
        - system-design.md §2.2: EvaluationPort protocol
    """
    from jerry.testing.evaluation.debiasing import DebiasingStrategy
    from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter

    model_name: str = os.environ.get("ANTHROPIC_MODEL", _DEFAULT_MODEL)
    return DeepEvalAdapter(
        model_name=model_name,
        debiasing_strategy=DebiasingStrategy(),
    )
