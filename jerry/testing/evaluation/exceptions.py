# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Typed exception hierarchy for the evaluation layer.

Three exception types capture distinct failure modes that require different
recovery strategies in ``evaluate_batch()``, ``evaluate_criteria()``, and
``a_measure_single_score()``.

H-10: This file contains only exception classes, not a primary domain class.
      It is a shared infrastructure module, not a class-per-file violation.

References:
    - CG-005: Typed exception hierarchy + pre-batch health check
    - gap-analysis-20260307-001
"""

from __future__ import annotations


class EvaluationConfigError(Exception):
    """Authentication or configuration error that MUST fail CI.

    Raised when the evaluation environment is misconfigured in a way that
    cannot recover at runtime: missing API key, invalid model identifier,
    or malformed criteria. These errors indicate a test-environment setup
    problem, not a transient API issue.

    Not retryable. The batch MUST be aborted and the CI run MUST fail.

    Examples:
        - ``ANTHROPIC_API_KEY`` not set when using a Claude model.
        - ``model_name`` is empty or contains a Bedrock/Vertex identifier.
        - ``criteria`` list is empty at batch-start time.

    Args:
        message: Human-readable error description.
        context: Optional structured diagnostics dict. Useful for capturing
            field names, model names, or environment variable names that
            triggered the error without embedding them in the message string.
    """

    def __init__(self, message: str, *, context: dict[str, str] | None = None) -> None:
        """Initialize EvaluationConfigError.

        Args:
            message: Human-readable error description.
            context: Optional structured diagnostics dict (key=field name,
                value=observed or expected value).
        """
        super().__init__(message)
        self.context: dict[str, str] = context or {}


class EvaluationAPIError(Exception):
    """Transient API error that may resolve on retry.

    Raised for ephemeral failures in the upstream LLM API: rate limits,
    request timeouts, and transient network errors. These failures do not
    indicate a configuration problem and may succeed on retry.

    In a batch context, individual outputs that raise ``EvaluationAPIError``
    are scored as 0.0 to allow the batch to continue; callers SHOULD inspect
    the zero fraction after the batch completes.

    Examples:
        - HTTP 429 rate-limit response from the Anthropic API.
        - Request timeout after the configured deadline.
        - Transient network error (connection reset, DNS failure).

    Args:
        message: Human-readable error description.
        context: Optional structured diagnostics dict. Useful for capturing
            HTTP status codes, retry-after headers, or endpoint URLs.
    """

    def __init__(self, message: str, *, context: dict[str, str] | None = None) -> None:
        """Initialize EvaluationAPIError.

        Args:
            message: Human-readable error description.
            context: Optional structured diagnostics dict (key=field name,
                value=observed or expected value).
        """
        super().__init__(message)
        self.context: dict[str, str] = context or {}


class EvaluationScoringError(Exception):
    """Scoring calculation failure where a 0.0 fallback is acceptable.

    Raised when the LLM judge returns an unusable score: NaN, out-of-range
    values, or an internal DeepEval error that prevents score extraction.
    Individual criteria or outputs that raise this error are excluded from
    the aggregate; ``score_composite()`` normalizes over included weights.

    For individual criteria: the criterion is excluded from the composite.
    For entire outputs in a batch: the output is scored as 0.0.
    For systemic batch failures (>20% zeros): re-raised to surface the issue.

    Examples:
        - DeepEval returns ``NaN`` or ``None`` for ``g_eval.score``.
        - DeepEval raises an internal exception during score extraction.
        - More than 20% of batch composite scores are 0.0 (systemic failure).

    Args:
        message: Human-readable error description.
        context: Optional structured diagnostics dict. Useful for capturing
            criterion names, score values, or batch statistics.
    """

    def __init__(self, message: str, *, context: dict[str, str] | None = None) -> None:
        """Initialize EvaluationScoringError.

        Args:
            message: Human-readable error description.
            context: Optional structured diagnostics dict (key=field name,
                value=observed or expected value).
        """
        super().__init__(message)
        self.context: dict[str, str] = context or {}
