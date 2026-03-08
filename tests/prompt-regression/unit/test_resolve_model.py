# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Unit tests for JerryGEvalDeepEvalMetric._resolve_model().

Verifies that model string resolution correctly maps:
  - Lowercase Claude identifiers -> AnthropicModel instance
  - None                         -> None (passthrough)
  - Non-Claude strings (e.g. OpenAI) -> original string (passthrough)
  - Mixed-case Claude identifiers -> AnthropicModel instance (CG-013 fix)
  - Bedrock/Vertex-style identifiers -> ValueError (CG-024)

No LLM calls performed. AnthropicModel construction is exercised but
inference methods (load_model, generate) are never called, so no API key
is required for these tests.

Pytest markers used:
    @pytest.mark.unit  -- fast, no I/O, no LLM API calls

References:
    - CG-014: Unit tests for _resolve_model() (gap-analysis-20260307-001)
    - CG-013: Case-insensitive Claude detection in _resolve_model()
    - CG-024: Reject Bedrock/Vertex-style model identifiers
    - H-20: BDD test-first (90% line coverage target)
"""

from __future__ import annotations

import pytest
from deepeval.models import AnthropicModel

from jerry.testing.evaluation.criterion import QualityCriterion
from jerry.testing.evaluation.jerry_geval_deepeval_metric import JerryGEvalDeepEvalMetric
from jerry.testing.evaluation.metrics import JerryGEvalMetric

# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------


def _minimal_criterion() -> QualityCriterion:
    """Return the smallest valid QualityCriterion for fixture construction."""
    return QualityCriterion(
        name="completeness",
        description="The output covers all required sections with non-empty content.",
        weight=1.0,
        dimension="completeness",
    )


def _minimal_jerry_metric() -> JerryGEvalMetric:
    """Return a JerryGEvalMetric with debiasing disabled (unit test mode).

    ``require_debiasing=False`` bypasses the C-007 mandatory debiasing guard
    in ``JerryGEvalDeepEvalMetric.__init__``, allowing unit tests to exercise
    ``_resolve_model()`` without constructing a full DebiasingStrategy.
    """
    return JerryGEvalMetric(
        criteria=[_minimal_criterion()],
        debiasing=None,
        agent_name="test-agent",
        require_debiasing=False,
    )


def _make_adapter(model: str | None) -> JerryGEvalDeepEvalMetric:
    """Construct a JerryGEvalDeepEvalMetric with the given model string."""
    return JerryGEvalDeepEvalMetric(
        jerry_metric=_minimal_jerry_metric(),
        model=model,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestResolveModel:
    """Unit tests for JerryGEvalDeepEvalMetric._resolve_model().

    Each test exercises a distinct input class and asserts the expected
    return type (or raised exception). Tests use BDD-style names per H-20.
    """

    @pytest.mark.unit
    def test_lowercase_claude_model_should_return_anthropic_model_instance(self) -> None:
        """Standard lowercase Claude model name returns an AnthropicModel.

        Verifies the primary happy path: a well-formed lowercase Claude
        model identifier is wrapped in DeepEval's AnthropicModel so that
        the correct Anthropic SDK backend is used (not GPTModel).
        """
        adapter = _make_adapter("claude-sonnet-4-20250514")

        result = adapter._resolve_model()

        assert isinstance(result, AnthropicModel), (
            f"Expected AnthropicModel for 'claude-sonnet-4-20250514', got {type(result)}"
        )

    @pytest.mark.unit
    def test_none_model_should_return_none(self) -> None:
        """None model passthrough: _resolve_model returns None.

        When no model is configured, DeepEval falls back to its own
        default. Returning None preserves that delegation.
        """
        adapter = _make_adapter(None)

        result = adapter._resolve_model()

        assert result is None, f"Expected None for model=None, got {result!r}"

    @pytest.mark.unit
    def test_non_claude_model_string_should_be_returned_as_is(self) -> None:
        """Non-Claude model strings pass through unchanged as raw strings.

        OpenAI and other provider model names must not be wrapped in
        AnthropicModel; DeepEval handles them via its default GPTModel path.
        """
        adapter = _make_adapter("gpt-4")

        result = adapter._resolve_model()

        assert result == "gpt-4", f"Expected 'gpt-4' passthrough, got {result!r}"
        assert isinstance(result, str), (
            f"Non-Claude model should remain a string, got {type(result)}"
        )

    @pytest.mark.unit
    def test_mixed_case_claude_model_should_return_anthropic_model_instance(self) -> None:
        """CG-013: Mixed-case Claude model names are detected case-insensitively.

        Before CG-013, 'Claude-Sonnet' (capital C) was not recognised as a
        Claude model and fell through to the string passthrough branch.
        After the fix, .lower().startswith('claude') catches all variants.
        """
        adapter = _make_adapter("Claude-Sonnet")

        result = adapter._resolve_model()

        assert isinstance(result, AnthropicModel), (
            f"Expected AnthropicModel for 'Claude-Sonnet' (CG-013 case-insensitive fix), "
            f"got {type(result)}"
        )

    @pytest.mark.unit
    def test_bedrock_style_claude_model_should_raise_value_error(self) -> None:
        """CG-024: Bedrock/Vertex-style 'anthropic.claude*' identifiers raise ValueError.

        The direct AnthropicModel wrapper requires a standard Anthropic API
        identifier, not the 'anthropic.claude-*' Bedrock naming convention.
        Raising early surfaces the misconfiguration before any LLM call.
        """
        adapter = _make_adapter("anthropic.claude-3-sonnet")

        with pytest.raises(ValueError, match="Bedrock/Vertex"):
            adapter._resolve_model()

    @pytest.mark.unit
    def test_mixed_case_claude_identifier_should_produce_anthropic_model(self) -> None:
        """CG-013: Full mixed-case Claude model identifier produces AnthropicModel.

        Validates that a versioned model string with capital 'C' (e.g.
        'Claude-Sonnet-4-20250514') is correctly classified as a Claude model
        and wrapped in AnthropicModel. This exercises the .lower().startswith('claude')
        path added by CG-013; before the fix, the capital-C form fell through
        to the raw string passthrough branch.
        """
        adapter = _make_adapter("Claude-Sonnet-4-20250514")

        result = adapter._resolve_model()

        assert isinstance(result, AnthropicModel), (
            f"Expected AnthropicModel for 'Claude-Sonnet-4-20250514' (CG-013 fix), "
            f"got {type(result)}"
        )

    @pytest.mark.unit
    def test_lowercase_bedrock_identifier_should_raise_value_error(self) -> None:
        """CG-024: Lowercase Bedrock-style 'anthropic.claude-3-5-*' raises ValueError.

        Real-world Bedrock model identifiers use the 'anthropic.claude-3-5-*'
        naming convention. Verifies that the full versioned form raises
        ValueError with 'Bedrock/Vertex' in the message, catching the
        misconfiguration before any LLM call is attempted.
        """
        adapter = _make_adapter("anthropic.claude-3-5-sonnet-20241022")

        with pytest.raises(ValueError, match="Bedrock/Vertex"):
            adapter._resolve_model()

    @pytest.mark.unit
    def test_mixed_case_bedrock_identifier_should_raise_value_error(self) -> None:
        """CG-013 + CG-024: Mixed-case Bedrock identifier is rejected case-insensitively.

        'Anthropic.Claude-3-5-sonnet-20241022' (capital A and C) must still
        trigger the Bedrock rejection branch. The .lower() normalisation
        introduced in CG-013 must also apply to the CG-024 Bedrock guard,
        so that users who accidentally capitalise the provider prefix are
        given a clear misconfiguration error rather than a silent wrong path.
        """
        adapter = _make_adapter("Anthropic.Claude-3-5-sonnet-20241022")

        with pytest.raises(ValueError, match="Bedrock/Vertex"):
            adapter._resolve_model()

    @pytest.mark.unit
    def test_non_claude_identifier_should_return_raw_string(self) -> None:
        """Non-Claude model identifiers are returned as-is (raw string passthrough).

        Provider model names that do not start with 'claude' (case-insensitive)
        must pass through unchanged so that DeepEval can route them to the
        appropriate backend (e.g., GPTModel for OpenAI identifiers).
        Verifies both the value and the type of the returned object.
        """
        adapter = _make_adapter("gpt-4o")

        result = adapter._resolve_model()

        assert result == "gpt-4o", f"Expected 'gpt-4o' passthrough, got {result!r}"
        assert isinstance(result, str), (
            f"Non-Claude model should remain a plain string, got {type(result)}"
        )
