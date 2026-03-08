# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Tests for EN-036-001: Model Flexibility for G-Eval Judge and Agent Execution.

Covers the five surface areas added by EN-036-001:
    1. ModelPricing frozen dataclass and MODEL_PRICING lookup table
    2. Composite model version formatting and parsing helpers
    3. Layer4Pipeline._validate_model_versions() apples-to-apples guard
    4. DeepEvalAdapter JERRY_JUDGE_MODEL env var override

No real API calls are made.  All tests are deterministic.

References:
    - EN-036-001: Model Flexibility for G-Eval Judge and Agent Execution
    - H-20: 90% line coverage target
    - OWASP INPVAL: Input validation testing (boundary and edge cases)
"""

from __future__ import annotations

import dataclasses
import os
from unittest.mock import patch

import pytest

from jerry.testing.types import (
    MODEL_PRICING,
    ModelPricing,
    format_composite_model_version,
    lookup_model_pricing,
    parse_composite_model_version,
)

pytestmark = [pytest.mark.unit]


# ---------------------------------------------------------------------------
# ModelPricing dataclass
# ---------------------------------------------------------------------------


class TestModelPricing:
    """Tests for ModelPricing frozen dataclass and MODEL_PRICING lookup table."""

    def test_model_pricing_is_frozen_should_reject_field_mutation(self) -> None:
        """ModelPricing is frozen — field assignment must raise after construction."""
        pricing = ModelPricing(input_cost_per_million=3.0, output_cost_per_million=15.0)
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            pricing.input_cost_per_million = 5.0  # type: ignore[misc]

    def test_model_pricing_is_frozen_should_reject_output_cost_mutation(self) -> None:
        """ModelPricing output_cost_per_million cannot be reassigned after construction."""
        pricing = ModelPricing(input_cost_per_million=0.80, output_cost_per_million=4.0)
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            pricing.output_cost_per_million = 99.0  # type: ignore[misc]

    def test_model_pricing_fields_should_be_accessible(self) -> None:
        """ModelPricing fields are accessible and hold the values passed in."""
        pricing = ModelPricing(input_cost_per_million=15.0, output_cost_per_million=75.0)
        assert pricing.input_cost_per_million == pytest.approx(15.0)
        assert pricing.output_cost_per_million == pytest.approx(75.0)

    def test_pricing_table_should_contain_opus_entry(self) -> None:
        """MODEL_PRICING must include a 'claude-opus-4' key."""
        assert "claude-opus-4" in MODEL_PRICING

    def test_pricing_table_should_contain_sonnet_entry(self) -> None:
        """MODEL_PRICING must include a 'claude-sonnet-4' key."""
        assert "claude-sonnet-4" in MODEL_PRICING

    def test_pricing_table_should_contain_haiku_entry(self) -> None:
        """MODEL_PRICING must include a 'claude-haiku-4' key."""
        assert "claude-haiku-4" in MODEL_PRICING

    def test_pricing_table_opus_input_cost_should_be_positive(self) -> None:
        """Opus input cost per million must be > 0."""
        assert MODEL_PRICING["claude-opus-4"].input_cost_per_million > 0

    def test_pricing_table_opus_output_cost_should_be_positive(self) -> None:
        """Opus output cost per million must be > 0."""
        assert MODEL_PRICING["claude-opus-4"].output_cost_per_million > 0

    def test_pricing_table_all_values_should_be_model_pricing_instances(self) -> None:
        """Every value in MODEL_PRICING must be a ModelPricing instance."""
        for key, value in MODEL_PRICING.items():
            assert isinstance(value, ModelPricing), (
                f"MODEL_PRICING['{key}'] is {type(value)}, expected ModelPricing"
            )

    def test_pricing_opus_most_expensive_input_cost(self) -> None:
        """Opus input cost must be strictly higher than sonnet and haiku."""
        opus = MODEL_PRICING["claude-opus-4"]
        sonnet = MODEL_PRICING["claude-sonnet-4"]
        haiku = MODEL_PRICING["claude-haiku-4"]
        assert opus.input_cost_per_million > sonnet.input_cost_per_million
        assert sonnet.input_cost_per_million > haiku.input_cost_per_million

    def test_pricing_opus_most_expensive_output_cost(self) -> None:
        """Opus output cost must be strictly higher than sonnet and haiku."""
        opus = MODEL_PRICING["claude-opus-4"]
        sonnet = MODEL_PRICING["claude-sonnet-4"]
        haiku = MODEL_PRICING["claude-haiku-4"]
        assert opus.output_cost_per_million > sonnet.output_cost_per_million
        assert sonnet.output_cost_per_million > haiku.output_cost_per_million


# ---------------------------------------------------------------------------
# lookup_model_pricing
# ---------------------------------------------------------------------------


class TestLookupModelPricing:
    """Tests for the lookup_model_pricing() prefix-match helper."""

    def test_lookup_sonnet_by_full_versioned_name_should_match(self) -> None:
        """lookup_model_pricing matches 'claude-sonnet-4-20250514' to sonnet pricing."""
        result = lookup_model_pricing("claude-sonnet-4-20250514")
        assert result is not None
        assert result.input_cost_per_million == pytest.approx(3.0)
        assert result.output_cost_per_million == pytest.approx(15.0)

    def test_lookup_haiku_by_full_versioned_name_should_match(self) -> None:
        """lookup_model_pricing matches 'claude-haiku-4-5-20251001' to haiku pricing."""
        result = lookup_model_pricing("claude-haiku-4-5-20251001")
        assert result is not None
        assert result.input_cost_per_million == pytest.approx(1.0)
        assert result.output_cost_per_million == pytest.approx(5.0)

    def test_lookup_opus_46_should_match_current_pricing(self) -> None:
        """lookup_model_pricing matches 'claude-opus-4-6' to current $5/$25 pricing."""
        result = lookup_model_pricing("claude-opus-4-6")
        assert result is not None
        assert result.input_cost_per_million == pytest.approx(5.0)
        assert result.output_cost_per_million == pytest.approx(25.0)

    def test_lookup_opus_legacy_should_match_legacy_pricing(self) -> None:
        """lookup_model_pricing matches 'claude-opus-4-20250514' to legacy $15/$75 pricing."""
        result = lookup_model_pricing("claude-opus-4-20250514")
        assert result is not None
        assert result.input_cost_per_million == pytest.approx(15.0)
        assert result.output_cost_per_million == pytest.approx(75.0)

    def test_lookup_should_be_case_insensitive_for_sonnet(self) -> None:
        """lookup_model_pricing is case-insensitive: 'Claude-Sonnet-4' matches."""
        result = lookup_model_pricing("Claude-Sonnet-4-20250514")
        assert result is not None
        assert result.input_cost_per_million == pytest.approx(3.0)

    def test_lookup_should_be_case_insensitive_for_opus(self) -> None:
        """lookup_model_pricing is case-insensitive: 'CLAUDE-OPUS-4' matches."""
        result = lookup_model_pricing("CLAUDE-OPUS-4-20250514")
        assert result is not None
        assert result.input_cost_per_million == pytest.approx(15.0)

    def test_lookup_unknown_model_should_return_none(self) -> None:
        """lookup_model_pricing returns None when no prefix matches."""
        assert lookup_model_pricing("gpt-4o") is None

    def test_lookup_empty_string_should_return_none(self) -> None:
        """lookup_model_pricing returns None for empty string input."""
        assert lookup_model_pricing("") is None

    def test_lookup_partial_prefix_no_match_should_return_none(self) -> None:
        """lookup_model_pricing returns None when partial prefix does not match any key."""
        assert lookup_model_pricing("claude") is None

    def test_lookup_exact_key_should_match(self) -> None:
        """lookup_model_pricing matches when model_name equals a key exactly."""
        result = lookup_model_pricing("claude-sonnet-4")
        assert result is not None

    def test_lookup_sonnet_returns_model_pricing_instance(self) -> None:
        """lookup_model_pricing returns a ModelPricing instance for sonnet."""
        result = lookup_model_pricing("claude-sonnet-4-20250514")
        assert isinstance(result, ModelPricing)


# ---------------------------------------------------------------------------
# format_composite_model_version / parse_composite_model_version
# ---------------------------------------------------------------------------


class TestCompositeModelVersion:
    """Tests for composite model version formatting and parsing helpers."""

    def test_format_should_produce_colon_separated_string(self) -> None:
        """format_composite_model_version produces '{agent}:{judge}' format."""
        result = format_composite_model_version(
            "claude-opus-4-20250514",
            "claude-sonnet-4-20250514",
        )
        assert result == "claude-opus-4-20250514:claude-sonnet-4-20250514"

    def test_format_should_preserve_agent_model_before_colon(self) -> None:
        """The agent model appears before the colon in the composite string."""
        agent = "claude-opus-4-20250514"
        judge = "claude-haiku-4-20250514"
        composite = format_composite_model_version(agent, judge)
        assert composite.startswith(agent + ":")

    def test_format_should_preserve_judge_model_after_colon(self) -> None:
        """The judge model appears after the colon in the composite string."""
        agent = "claude-opus-4-20250514"
        judge = "claude-haiku-4-20250514"
        composite = format_composite_model_version(agent, judge)
        assert composite.endswith(":" + judge)

    def test_format_same_model_for_agent_and_judge(self) -> None:
        """format_composite_model_version handles identical agent and judge models."""
        result = format_composite_model_version(
            "claude-sonnet-4-20250514",
            "claude-sonnet-4-20250514",
        )
        assert result == "claude-sonnet-4-20250514:claude-sonnet-4-20250514"

    def test_parse_valid_composite_should_return_tuple(self) -> None:
        """parse_composite_model_version parses a valid '{agent}:{judge}' string."""
        result = parse_composite_model_version("claude-opus-4-20250514:claude-sonnet-4-20250514")
        assert result == ("claude-opus-4-20250514", "claude-sonnet-4-20250514")

    def test_parse_valid_composite_agent_component(self) -> None:
        """First element of the parsed tuple is the agent model."""
        result = parse_composite_model_version("claude-opus-4-20250514:claude-haiku-4-20250514")
        assert result is not None
        agent_model, _ = result
        assert agent_model == "claude-opus-4-20250514"

    def test_parse_valid_composite_judge_component(self) -> None:
        """Second element of the parsed tuple is the judge model."""
        result = parse_composite_model_version("claude-opus-4-20250514:claude-haiku-4-20250514")
        assert result is not None
        _, judge_model = result
        assert judge_model == "claude-haiku-4-20250514"

    def test_parse_no_colon_should_return_none(self) -> None:
        """parse_composite_model_version returns None for strings without a colon."""
        assert parse_composite_model_version("claude-sonnet-4-20250514") is None

    def test_parse_empty_agent_part_should_return_none(self) -> None:
        """parse_composite_model_version returns None when agent part is empty."""
        assert parse_composite_model_version(":claude-sonnet-4-20250514") is None

    def test_parse_empty_judge_part_should_return_none(self) -> None:
        """parse_composite_model_version returns None when judge part is empty."""
        assert parse_composite_model_version("claude-opus-4-20250514:") is None

    def test_parse_only_colon_should_return_none(self) -> None:
        """parse_composite_model_version returns None for ':' (both parts empty)."""
        assert parse_composite_model_version(":") is None

    def test_parse_empty_string_should_return_none(self) -> None:
        """parse_composite_model_version returns None for empty string."""
        assert parse_composite_model_version("") is None

    def test_roundtrip_format_then_parse_should_recover_originals(self) -> None:
        """format then parse recovers the original agent and judge model strings."""
        agent = "claude-opus-4-20250514"
        judge = "claude-sonnet-4-20250514"
        composite = format_composite_model_version(agent, judge)
        parsed = parse_composite_model_version(composite)
        assert parsed == (agent, judge)

    def test_roundtrip_multiple_colons_in_judge_name(self) -> None:
        """parse_composite_model_version splits on the first colon only."""
        # Hypothetical model name with a colon — should split at the first colon.
        composite = "claude-opus-4-20250514:provider:claude-sonnet-4-20250514"
        result = parse_composite_model_version(composite)
        assert result is not None
        agent_part, judge_part = result
        assert agent_part == "claude-opus-4-20250514"
        assert judge_part == "provider:claude-sonnet-4-20250514"


# ---------------------------------------------------------------------------
# Layer4Pipeline._validate_model_versions
# ---------------------------------------------------------------------------


class TestLayer4ModelVersionValidation:
    """Tests for the Layer4Pipeline apples-to-apples model version guard."""

    def test_matching_versions_should_not_raise(self) -> None:
        """No exception when baseline and candidate model versions are identical."""
        from jerry.testing.layer4_stats import Layer4Pipeline

        # Should not raise
        Layer4Pipeline._validate_model_versions(
            metric_scores={},
            baseline_model_version="claude-opus-4-20250514:claude-sonnet-4-20250514",
            candidate_model_version="claude-opus-4-20250514:claude-sonnet-4-20250514",
        )

    def test_mismatched_versions_should_raise_value_error(self) -> None:
        """ValueError is raised when baseline and candidate model versions differ."""
        from jerry.testing.layer4_stats import Layer4Pipeline

        with pytest.raises(ValueError, match="Model version mismatch"):
            Layer4Pipeline._validate_model_versions(
                metric_scores={},
                baseline_model_version="claude-opus-4-20250514:claude-sonnet-4-20250514",
                candidate_model_version="claude-sonnet-4-20250514:claude-sonnet-4-20250514",
            )

    def test_error_message_includes_baseline_version(self) -> None:
        """ValueError message mentions the baseline model version."""
        from jerry.testing.layer4_stats import Layer4Pipeline

        baseline = "claude-opus-4-20250514:claude-sonnet-4-20250514"
        with pytest.raises(ValueError, match=baseline):
            Layer4Pipeline._validate_model_versions(
                metric_scores={},
                baseline_model_version=baseline,
                candidate_model_version="claude-haiku-4-20250514:claude-haiku-4-20250514",
            )

    def test_error_message_includes_candidate_version(self) -> None:
        """ValueError message mentions the candidate model version."""
        from jerry.testing.layer4_stats import Layer4Pipeline

        candidate = "claude-haiku-4-20250514:claude-haiku-4-20250514"
        with pytest.raises(ValueError, match=candidate):
            Layer4Pipeline._validate_model_versions(
                metric_scores={},
                baseline_model_version="claude-opus-4-20250514:claude-sonnet-4-20250514",
                candidate_model_version=candidate,
            )

    def test_both_none_should_not_raise(self) -> None:
        """Validation is skipped (no error) when both model versions are None."""
        from jerry.testing.layer4_stats import Layer4Pipeline

        # Should not raise — None skips validation for backwards compatibility.
        Layer4Pipeline._validate_model_versions(
            metric_scores={},
            baseline_model_version=None,
            candidate_model_version=None,
        )

    def test_only_baseline_provided_should_not_raise(self) -> None:
        """Validation is skipped when only baseline_model_version is provided."""
        from jerry.testing.layer4_stats import Layer4Pipeline

        # Should not raise — validation requires both to be non-None.
        Layer4Pipeline._validate_model_versions(
            metric_scores={},
            baseline_model_version="claude-opus-4-20250514:claude-sonnet-4-20250514",
            candidate_model_version=None,
        )

    def test_only_candidate_provided_should_not_raise(self) -> None:
        """Validation is skipped when only candidate_model_version is provided."""
        from jerry.testing.layer4_stats import Layer4Pipeline

        # Should not raise — validation requires both to be non-None.
        Layer4Pipeline._validate_model_versions(
            metric_scores={},
            baseline_model_version=None,
            candidate_model_version="claude-sonnet-4-20250514:claude-sonnet-4-20250514",
        )

    def test_validate_accepts_non_empty_metric_scores_context(self) -> None:
        """_validate_model_versions does not error on a non-empty metric_scores dict."""
        from jerry.testing.layer4_stats import Layer4Pipeline

        metric_scores = {"composite": ([0.9, 0.91], [0.88, 0.90])}
        # Should not raise — metric_scores is context-only, not used for validation.
        Layer4Pipeline._validate_model_versions(
            metric_scores=metric_scores,
            baseline_model_version="opus:sonnet",
            candidate_model_version="opus:sonnet",
        )


# ---------------------------------------------------------------------------
# DeepEvalAdapter JERRY_JUDGE_MODEL env var override
# ---------------------------------------------------------------------------


class TestDeepEvalAdapterJudgeModelOverride:
    """Tests for the JERRY_JUDGE_MODEL environment variable override in DeepEvalAdapter."""

    def _make_env_with_api_key(self, **extras: str) -> dict[str, str]:
        """Return a minimal env dict with ANTHROPIC_API_KEY set."""
        return {"ANTHROPIC_API_KEY": "test-api-key-not-real", **extras}

    def test_env_var_overrides_default_model_name(self) -> None:
        """JERRY_JUDGE_MODEL env var overrides the dataclass default model_name."""
        env = self._make_env_with_api_key(JERRY_JUDGE_MODEL="claude-haiku-4-20250514")
        with patch.dict(os.environ, env, clear=True):
            from importlib import reload

            import jerry.testing.evaluation.deepeval_adapter as adapter_mod

            reload(adapter_mod)
            from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter

            adapter = DeepEvalAdapter()
            assert adapter.model_name == "claude-haiku-4-20250514"

    def test_env_var_overrides_explicit_constructor_model_name(self) -> None:
        """JERRY_JUDGE_MODEL overrides model_name even when explicitly passed to constructor."""
        env = self._make_env_with_api_key(JERRY_JUDGE_MODEL="claude-haiku-4-20250514")
        with patch.dict(os.environ, env, clear=True):
            from importlib import reload

            import jerry.testing.evaluation.deepeval_adapter as adapter_mod

            reload(adapter_mod)
            from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter

            adapter = DeepEvalAdapter(model_name="claude-opus-4-20250514")
            assert adapter.model_name == "claude-haiku-4-20250514"

    def test_no_env_var_uses_dataclass_default(self) -> None:
        """Without JERRY_JUDGE_MODEL, the default model_name 'claude-sonnet-4-20250514' is used."""
        env = self._make_env_with_api_key()
        # Ensure JERRY_JUDGE_MODEL is absent
        env.pop("JERRY_JUDGE_MODEL", None)
        with patch.dict(os.environ, env, clear=True):
            from importlib import reload

            import jerry.testing.evaluation.deepeval_adapter as adapter_mod

            reload(adapter_mod)
            from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter

            adapter = DeepEvalAdapter()
            assert adapter.model_name == "claude-sonnet-4-20250514"

    def test_no_env_var_preserves_explicit_constructor_model_name(self) -> None:
        """Without JERRY_JUDGE_MODEL, the model_name passed to the constructor is preserved."""
        env = self._make_env_with_api_key()
        env.pop("JERRY_JUDGE_MODEL", None)
        with patch.dict(os.environ, env, clear=True):
            from importlib import reload

            import jerry.testing.evaluation.deepeval_adapter as adapter_mod

            reload(adapter_mod)
            from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter

            adapter = DeepEvalAdapter(model_name="claude-opus-4-20250514")
            assert adapter.model_name == "claude-opus-4-20250514"

    def test_env_var_set_to_opus_is_reflected(self) -> None:
        """JERRY_JUDGE_MODEL=claude-opus-4-20250514 is reflected in model_name."""
        env = self._make_env_with_api_key(JERRY_JUDGE_MODEL="claude-opus-4-20250514")
        with patch.dict(os.environ, env, clear=True):
            from importlib import reload

            import jerry.testing.evaluation.deepeval_adapter as adapter_mod

            reload(adapter_mod)
            from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter

            adapter = DeepEvalAdapter()
            assert adapter.model_name == "claude-opus-4-20250514"
