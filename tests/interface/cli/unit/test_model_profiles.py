"""Unit tests for model profile resolution.

Tests the model profile system including:
- Profile definitions
- Profile retrieval
- Model configuration resolution
- Override precedence

References:
    - TASK-423: Implement Model Profiles - Track B
    - EN-031: Model Selection Capability
"""

from __future__ import annotations

import pytest

from src.interface.cli.model_profiles import (
    BALANCED,
    DEFAULT_PROFILE,
    ECONOMY,
    PROFILES,
    QUALITY,
    SPEED,
    get_profile,
    resolve_model_config,
)


class TestProfileDefinitions:
    """Test that all profiles are properly defined."""

    def test_all_profiles_exist(self) -> None:
        """All expected profiles should be in the registry."""
        expected = {"economy", "balanced", "quality", "speed"}
        assert set(PROFILES.keys()) == expected

    def test_economy_profile(self) -> None:
        """Economy profile should use haiku for all agents."""
        assert ECONOMY.parser == "haiku"
        assert ECONOMY.extractor == "haiku"
        assert ECONOMY.formatter == "haiku"
        assert ECONOMY.mindmap == "haiku"
        assert ECONOMY.critic == "haiku"

    def test_balanced_profile(self) -> None:
        """Balanced profile should mix haiku and sonnet."""
        assert BALANCED.parser == "haiku"
        assert BALANCED.extractor == "sonnet"
        assert BALANCED.formatter == "haiku"
        assert BALANCED.mindmap == "sonnet"
        assert BALANCED.critic == "sonnet"

    def test_quality_profile(self) -> None:
        """Quality profile should use opus for critical agents."""
        assert QUALITY.parser == "sonnet"
        assert QUALITY.extractor == "opus"
        assert QUALITY.formatter == "sonnet"
        assert QUALITY.mindmap == "sonnet"
        assert QUALITY.critic == "opus"

    def test_speed_profile(self) -> None:
        """Speed profile should use haiku for all agents."""
        assert SPEED.parser == "haiku"
        assert SPEED.extractor == "haiku"
        assert SPEED.formatter == "haiku"
        assert SPEED.mindmap == "haiku"
        assert SPEED.critic == "haiku"

    def test_default_profile_is_balanced(self) -> None:
        """Default profile should be balanced."""
        assert DEFAULT_PROFILE == "balanced"


class TestGetProfile:
    """Test profile retrieval."""

    def test_get_profile_economy(self) -> None:
        """Should retrieve economy profile."""
        profile = get_profile("economy")
        assert profile.name == "economy"

    def test_get_profile_balanced(self) -> None:
        """Should retrieve balanced profile."""
        profile = get_profile("balanced")
        assert profile.name == "balanced"

    def test_get_profile_quality(self) -> None:
        """Should retrieve quality profile."""
        profile = get_profile("quality")
        assert profile.name == "quality"

    def test_get_profile_speed(self) -> None:
        """Should retrieve speed profile."""
        profile = get_profile("speed")
        assert profile.name == "speed"

    def test_get_profile_invalid_raises_key_error(self) -> None:
        """Should raise KeyError for unknown profile."""
        with pytest.raises(KeyError) as exc_info:
            get_profile("nonexistent")
        assert "Unknown profile" in str(exc_info.value)
        assert "nonexistent" in str(exc_info.value)


class TestResolveModelConfig:
    """Test model configuration resolution."""

    # Test default behavior

    def test_resolve_no_args_uses_balanced(self) -> None:
        """No arguments should use balanced profile."""
        config = resolve_model_config()
        assert config["parser"] == "haiku"
        assert config["extractor"] == "sonnet"
        assert config["formatter"] == "haiku"
        assert config["mindmap"] == "sonnet"
        assert config["critic"] == "sonnet"

    # Test profile selection

    def test_resolve_economy_profile(self) -> None:
        """Economy profile should use haiku for all."""
        config = resolve_model_config(profile="economy")
        assert config["parser"] == "haiku"
        assert config["extractor"] == "haiku"
        assert config["formatter"] == "haiku"
        assert config["mindmap"] == "haiku"
        assert config["critic"] == "haiku"

    def test_resolve_quality_profile(self) -> None:
        """Quality profile should use opus for critical agents."""
        config = resolve_model_config(profile="quality")
        assert config["parser"] == "sonnet"
        assert config["extractor"] == "opus"
        assert config["formatter"] == "sonnet"
        assert config["mindmap"] == "sonnet"
        assert config["critic"] == "opus"

    def test_resolve_speed_profile(self) -> None:
        """Speed profile should use haiku for all."""
        config = resolve_model_config(profile="speed")
        assert config["parser"] == "haiku"
        assert config["extractor"] == "haiku"
        assert config["formatter"] == "haiku"
        assert config["mindmap"] == "haiku"
        assert config["critic"] == "haiku"

    # Test individual overrides

    def test_resolve_override_single_model(self) -> None:
        """Individual override should take precedence over profile."""
        config = resolve_model_config(
            profile="economy",
            model_extractor="opus",
        )
        assert config["parser"] == "haiku"  # From economy
        assert config["extractor"] == "opus"  # Override
        assert config["formatter"] == "haiku"  # From economy
        assert config["mindmap"] == "haiku"  # From economy
        assert config["critic"] == "haiku"  # From economy

    def test_resolve_override_multiple_models(self) -> None:
        """Multiple overrides should all take precedence."""
        config = resolve_model_config(
            profile="economy",
            model_parser="sonnet",
            model_extractor="opus",
            model_critic="sonnet",
        )
        assert config["parser"] == "sonnet"  # Override
        assert config["extractor"] == "opus"  # Override
        assert config["formatter"] == "haiku"  # From economy
        assert config["mindmap"] == "haiku"  # From economy
        assert config["critic"] == "sonnet"  # Override

    def test_resolve_override_all_models(self) -> None:
        """All individual overrides should work."""
        config = resolve_model_config(
            profile="economy",
            model_parser="opus",
            model_extractor="opus",
            model_formatter="sonnet",
            model_mindmap="sonnet",
            model_critic="opus",
        )
        assert config["parser"] == "opus"
        assert config["extractor"] == "opus"
        assert config["formatter"] == "sonnet"
        assert config["mindmap"] == "sonnet"
        assert config["critic"] == "opus"

    def test_resolve_override_without_profile_uses_default(self) -> None:
        """Override without profile should use default (balanced)."""
        config = resolve_model_config(model_extractor="opus")
        assert config["parser"] == "haiku"  # From balanced
        assert config["extractor"] == "opus"  # Override
        assert config["formatter"] == "haiku"  # From balanced
        assert config["mindmap"] == "sonnet"  # From balanced
        assert config["critic"] == "sonnet"  # From balanced

    # Test precedence

    def test_resolve_precedence_explicit_over_profile(self) -> None:
        """Explicit flag should override profile."""
        # Quality profile would give opus, but override to haiku
        config = resolve_model_config(
            profile="quality",
            model_extractor="haiku",
        )
        assert config["extractor"] == "haiku"

    def test_resolve_precedence_profile_over_default(self) -> None:
        """Profile should override default."""
        # Balanced default would give sonnet, economy gives haiku
        config = resolve_model_config(profile="economy")
        assert config["extractor"] == "haiku"

    # Edge cases

    def test_resolve_none_values_ignored(self) -> None:
        """None values in overrides should be ignored."""
        config = resolve_model_config(
            profile="quality",
            model_parser=None,
            model_extractor=None,
        )
        # Should use quality profile values
        assert config["parser"] == "sonnet"
        assert config["extractor"] == "opus"

    def test_resolve_invalid_profile_raises_error(self) -> None:
        """Invalid profile name should raise KeyError."""
        with pytest.raises(KeyError):
            resolve_model_config(profile="invalid")


class TestProfileMetadata:
    """Test profile metadata and descriptions."""

    def test_all_profiles_have_metadata(self) -> None:
        """All profiles should have complete metadata."""
        for profile in PROFILES.values():
            assert profile.name
            assert profile.description
            assert profile.use_case
            assert profile.trade_off

    def test_profile_str_representation(self) -> None:
        """Profile should have readable string representation."""
        assert "economy" in str(ECONOMY)
        assert "Minimize cost" in str(ECONOMY)

    def test_economy_metadata(self) -> None:
        """Economy profile should describe cost optimization."""
        assert "cost" in ECONOMY.description.lower()
        assert "haiku" in ECONOMY.description.lower()

    def test_balanced_metadata(self) -> None:
        """Balanced profile should describe cost/quality balance."""
        assert (
            "balance" in BALANCED.description.lower() or "default" in BALANCED.description.lower()
        )

    def test_quality_metadata(self) -> None:
        """Quality profile should describe quality optimization."""
        assert "quality" in QUALITY.description.lower()
        assert "opus" in QUALITY.description.lower()

    def test_speed_metadata(self) -> None:
        """Speed profile should describe latency optimization."""
        assert "latency" in SPEED.description.lower() or "speed" in SPEED.description.lower()
