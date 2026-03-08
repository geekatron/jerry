# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Integration tests: DeepEvalAdapter construction — Layer 2 adapter wiring.

Scope: ps-researcher + ps-analyst pipeline, adapter construction only.

Covers two structural construction scenarios:
    - Adapter with a Claude model succeeds when ANTHROPIC_API_KEY is present.
    - Adapter construction raises EvaluationConfigError when ANTHROPIC_API_KEY
      is absent.

No LLM API calls are made in any test. These are structural integration tests
that verify the adapter's construction contract and configuration validation
logic are wired correctly (H-07 adapter layer).

OWASP mapping:
    - AUTHN: Verifies that missing API credentials are caught at construction
      time, not silently deferred to the first LLM call (fail-fast principle).

References:
    - FR-006: DeepEval pytest plugin integration (evaluator fixture)
    - FR-021: Debiasing (C-007 mandatory, DebiasingStrategy)
    - CG-005: Typed exception hierarchy + pre-batch health check
    - OWASP AUTHN: Authentication configuration validation
    - H-11: Type hints + docstrings on public symbols
    - H-20: 90% line coverage target
"""

from __future__ import annotations

import pytest

from jerry.testing.evaluation.debiasing import DebiasingStrategy
from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter
from jerry.testing.evaluation.exceptions import EvaluationConfigError

# ---------------------------------------------------------------------------
# Integration tests: adapter construction
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestAdapterConstruction:
    """DeepEvalAdapter construction contract verification.

    All tests operate on the adapter's __post_init__ validation logic.
    No LLM API calls are performed.
    """

    def test_adapter_with_claude_model_should_not_require_openai_key(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """DeepEvalAdapter with a Claude model must not require an OpenAI API key.

        Constructs DeepEvalAdapter with model_name="claude-sonnet-4-20250514"
        and a DebiasingStrategy(). Verifies:
            - Construction succeeds (no exception raised).
            - adapter.model_name equals the supplied constructor argument.

        ANTHROPIC_API_KEY is set via monkeypatch to satisfy the Claude model
        validation in __post_init__ while keeping the test hermetic.

        OWASP AUTHN: The adapter should only require credentials appropriate
        to the configured model family; OpenAI keys are irrelevant for Claude.

        References:
            - FR-006: DeepEval pytest plugin integration
            - FR-021: Debiasing (C-007 mandatory)
        """
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-hermetic")
        # Explicitly ensure no OpenAI key influence by removing it.
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        adapter = DeepEvalAdapter(
            model_name="claude-sonnet-4-20250514",
            debiasing_strategy=DebiasingStrategy(),
        )

        assert adapter.model_name == "claude-sonnet-4-20250514", (
            f"model_name attribute must match the constructor argument; got {adapter.model_name!r}"
        )
        assert isinstance(adapter.debiasing_strategy, DebiasingStrategy), (
            "debiasing_strategy must be a DebiasingStrategy instance; "
            f"got {type(adapter.debiasing_strategy).__name__}"
        )

    def test_adapter_without_api_key_should_raise_config_error(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """DeepEvalAdapter with a Claude model must raise EvaluationConfigError
        when ANTHROPIC_API_KEY is unset.

        Removes ANTHROPIC_API_KEY from the environment via monkeypatch, then
        attempts to construct DeepEvalAdapter with a Claude model. Verifies
        that EvaluationConfigError is raised during __post_init__ before any
        LLM call can be made (fail-fast principle).

        OWASP AUTHN: Authentication configuration errors must be surfaced at
        construction time, not deferred to the first API call, to prevent
        misleading downstream failures (e.g., silent 0.0 score arrays).

        References:
            - CG-005: Typed exception hierarchy + pre-batch health check
            - FR-006: DeepEval pytest plugin integration
            - OWASP AUTHN: Authentication validation at initialization
        """
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

        with pytest.raises(EvaluationConfigError) as exc_info:
            DeepEvalAdapter(
                model_name="claude-sonnet-4-20250514",
                debiasing_strategy=DebiasingStrategy(),
            )

        raised = exc_info.value
        assert "ANTHROPIC_API_KEY" in str(raised), (
            "EvaluationConfigError message must mention ANTHROPIC_API_KEY "
            f"to guide the user toward remediation; got: {raised!r}"
        )
