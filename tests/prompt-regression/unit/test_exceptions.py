# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Unit tests for jerry.testing.evaluation.exceptions — CG-005 exception hierarchy.

Verifies that the three typed exception classes are correctly structured,
inherit from the right base types, carry an accessible `.context` attribute,
and are independently instantiable.

No LLM calls are performed.

References:
    - CG-005: Typed exception hierarchy (EvaluationConfigError, EvaluationAPIError,
      EvaluationScoringError) with context dict
    - H-20: BDD test-first (90% line coverage target)
"""

from __future__ import annotations

import pytest

from jerry.testing.evaluation.exceptions import (
    EvaluationAPIError,
    EvaluationConfigError,
    EvaluationScoringError,
)


class TestEvaluationConfigError:
    """Unit tests for EvaluationConfigError.

    Verifies construction, inheritance, and the context attribute contract.
    """

    @pytest.mark.unit
    def test_config_error_with_message_should_be_instantiable(self) -> None:
        """EvaluationConfigError is constructable with a plain message string.

        The message is the canonical Exception first argument and must be
        accessible via str() for logging and CI output display.
        """
        exc = EvaluationConfigError("API key is missing")

        assert str(exc) == "API key is missing"

    @pytest.mark.unit
    def test_config_error_with_context_dict_should_store_context(self) -> None:
        """EvaluationConfigError stores its context dict on .context attribute.

        The context dict captures structured diagnostics (field names, values)
        without embedding them in the human-readable message string.
        """
        ctx: dict[str, str] = {"field": "ANTHROPIC_API_KEY", "model_name": "claude-sonnet-4"}
        exc = EvaluationConfigError("Missing API key", context=ctx)

        assert exc.context == ctx
        assert exc.context["field"] == "ANTHROPIC_API_KEY"

    @pytest.mark.unit
    def test_config_error_without_context_should_default_to_empty_dict(self) -> None:
        """EvaluationConfigError defaults .context to an empty dict when omitted.

        Callers that do not need structured diagnostics should not need to
        pass context=None explicitly.
        """
        exc = EvaluationConfigError("Something is wrong")

        assert exc.context == {}
        assert isinstance(exc.context, dict)

    @pytest.mark.unit
    def test_config_error_should_inherit_from_exception(self) -> None:
        """EvaluationConfigError is an Exception subclass for try/except compatibility."""
        exc = EvaluationConfigError("bad config")

        assert isinstance(exc, Exception)

    @pytest.mark.unit
    def test_config_error_should_not_inherit_from_api_or_scoring_error(self) -> None:
        """EvaluationConfigError is independent of the other two exception types.

        The three exceptions model distinct failure modes and must not form
        a sub-hierarchy among themselves, ensuring catch clauses remain precise.
        """
        exc = EvaluationConfigError("bad config")

        assert not isinstance(exc, EvaluationAPIError)
        assert not isinstance(exc, EvaluationScoringError)


class TestEvaluationAPIError:
    """Unit tests for EvaluationAPIError.

    Verifies construction, inheritance, and the context attribute contract.
    """

    @pytest.mark.unit
    def test_api_error_with_message_should_be_instantiable(self) -> None:
        """EvaluationAPIError is constructable with a plain message string."""
        exc = EvaluationAPIError("HTTP 429 rate limit")

        assert str(exc) == "HTTP 429 rate limit"

    @pytest.mark.unit
    def test_api_error_with_context_dict_should_store_context(self) -> None:
        """EvaluationAPIError stores its context dict on .context attribute."""
        ctx: dict[str, str] = {"status_code": "429", "retry_after": "60"}
        exc = EvaluationAPIError("Rate limited", context=ctx)

        assert exc.context == ctx
        assert exc.context["status_code"] == "429"

    @pytest.mark.unit
    def test_api_error_without_context_should_default_to_empty_dict(self) -> None:
        """EvaluationAPIError defaults .context to an empty dict when omitted."""
        exc = EvaluationAPIError("Network timeout")

        assert exc.context == {}
        assert isinstance(exc.context, dict)

    @pytest.mark.unit
    def test_api_error_should_inherit_from_exception(self) -> None:
        """EvaluationAPIError is an Exception subclass for try/except compatibility."""
        exc = EvaluationAPIError("transient failure")

        assert isinstance(exc, Exception)

    @pytest.mark.unit
    def test_api_error_should_not_inherit_from_config_or_scoring_error(self) -> None:
        """EvaluationAPIError is independent of the other two exception types."""
        exc = EvaluationAPIError("transient failure")

        assert not isinstance(exc, EvaluationConfigError)
        assert not isinstance(exc, EvaluationScoringError)


class TestEvaluationScoringError:
    """Unit tests for EvaluationScoringError.

    Verifies construction, inheritance, and the context attribute contract.
    """

    @pytest.mark.unit
    def test_scoring_error_with_message_should_be_instantiable(self) -> None:
        """EvaluationScoringError is constructable with a plain message string."""
        exc = EvaluationScoringError("DeepEval returned NaN for g_eval.score")

        assert str(exc) == "DeepEval returned NaN for g_eval.score"

    @pytest.mark.unit
    def test_scoring_error_with_context_dict_should_store_context(self) -> None:
        """EvaluationScoringError stores its context dict on .context attribute."""
        ctx: dict[str, str] = {
            "criterion": "completeness",
            "agent": "ps-researcher",
            "zero_fraction": "0.250",
        }
        exc = EvaluationScoringError("25% zero scores", context=ctx)

        assert exc.context == ctx
        assert exc.context["criterion"] == "completeness"

    @pytest.mark.unit
    def test_scoring_error_without_context_should_default_to_empty_dict(self) -> None:
        """EvaluationScoringError defaults .context to an empty dict when omitted."""
        exc = EvaluationScoringError("Score extraction failed")

        assert exc.context == {}
        assert isinstance(exc.context, dict)

    @pytest.mark.unit
    def test_scoring_error_should_inherit_from_exception(self) -> None:
        """EvaluationScoringError is an Exception subclass for try/except compatibility."""
        exc = EvaluationScoringError("bad score")

        assert isinstance(exc, Exception)

    @pytest.mark.unit
    def test_scoring_error_should_not_inherit_from_config_or_api_error(self) -> None:
        """EvaluationScoringError is independent of the other two exception types."""
        exc = EvaluationScoringError("bad score")

        assert not isinstance(exc, EvaluationConfigError)
        assert not isinstance(exc, EvaluationAPIError)
