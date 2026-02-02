"""Integration tests for model selection feature.

Tests the end-to-end flow of model selection from CLI arguments
through profile resolution to final ModelConfig creation.

This integration test suite validates:
1. Profile application works correctly
2. CLI overrides take precedence
3. Invalid inputs are rejected with proper error messages
4. Model configuration flows through to adapter correctly

References:
    - TASK-424: Integration Testing - Track B
    - EN-031: Model Selection Capability
    - TASK-423: Implement Model Profiles
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.interface.cli.main import main
from src.interface.cli.model_profiles import (
    BALANCED,
    ECONOMY,
    QUALITY,
    SPEED,
    resolve_model_config,
)
from src.transcript.domain.value_objects.model_config import ModelConfig


class TestProfileApplicationIntegration:
    """Integration tests for profile application."""

    def test_economy_profile_applies_all_haiku(self) -> None:
        """Economy profile should set all agents to haiku."""
        config = resolve_model_config(profile="economy")

        assert config["parser"] == "haiku"
        assert config["extractor"] == "haiku"
        assert config["formatter"] == "haiku"
        assert config["mindmap"] == "haiku"
        assert config["critic"] == "haiku"

    def test_balanced_profile_applies_mixed_models(self) -> None:
        """Balanced profile should use cost-optimized mix."""
        config = resolve_model_config(profile="balanced")

        assert config["parser"] == "haiku"
        assert config["extractor"] == "sonnet"
        assert config["formatter"] == "haiku"
        assert config["mindmap"] == "sonnet"
        assert config["critic"] == "sonnet"

    def test_quality_profile_applies_high_quality_models(self) -> None:
        """Quality profile should use opus for critical agents."""
        config = resolve_model_config(profile="quality")

        assert config["parser"] == "sonnet"
        assert config["extractor"] == "opus"
        assert config["formatter"] == "sonnet"
        assert config["mindmap"] == "sonnet"
        assert config["critic"] == "opus"

    def test_speed_profile_applies_all_haiku(self) -> None:
        """Speed profile should use haiku for minimal latency."""
        config = resolve_model_config(profile="speed")

        assert config["parser"] == "haiku"
        assert config["extractor"] == "haiku"
        assert config["formatter"] == "haiku"
        assert config["mindmap"] == "haiku"
        assert config["critic"] == "haiku"

    def test_default_profile_when_none_specified(self) -> None:
        """No profile specified should use balanced default."""
        config = resolve_model_config()

        # Should match balanced profile
        assert config == {
            "parser": "haiku",
            "extractor": "sonnet",
            "formatter": "haiku",
            "mindmap": "sonnet",
            "critic": "sonnet",
        }


class TestCLIOverrideIntegration:
    """Integration tests for CLI override behavior."""

    def test_single_override_preserves_profile_for_others(self) -> None:
        """Single model override should preserve profile for other agents."""
        config = resolve_model_config(
            profile="economy",
            model_extractor="opus",
        )

        assert config["parser"] == "haiku"  # From economy
        assert config["extractor"] == "opus"  # Override
        assert config["formatter"] == "haiku"  # From economy
        assert config["mindmap"] == "haiku"  # From economy
        assert config["critic"] == "haiku"  # From economy

    def test_multiple_overrides_all_apply(self) -> None:
        """Multiple overrides should all take precedence over profile."""
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

    def test_all_overrides_replace_profile_completely(self) -> None:
        """All five overrides should replace profile completely."""
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

    def test_override_without_profile_uses_default(self) -> None:
        """Override without profile should use balanced default as base."""
        config = resolve_model_config(model_extractor="opus")

        assert config["parser"] == "haiku"  # From balanced
        assert config["extractor"] == "opus"  # Override
        assert config["formatter"] == "haiku"  # From balanced
        assert config["mindmap"] == "sonnet"  # From balanced
        assert config["critic"] == "sonnet"  # From balanced

    def test_override_can_downgrade_quality_profile(self) -> None:
        """Override can downgrade from quality profile to haiku."""
        config = resolve_model_config(
            profile="quality",
            model_extractor="haiku",
        )

        assert config["parser"] == "sonnet"  # From quality
        assert config["extractor"] == "haiku"  # Override (downgrade)
        assert config["formatter"] == "sonnet"  # From quality
        assert config["mindmap"] == "sonnet"  # From quality
        assert config["critic"] == "opus"  # From quality


class TestModelConfigCreationIntegration:
    """Integration tests for ModelConfig value object creation."""

    def test_economy_profile_creates_valid_model_config(self) -> None:
        """Economy profile should create valid ModelConfig."""
        config_dict = resolve_model_config(profile="economy")

        model_config = ModelConfig(
            parser=config_dict["parser"],
            extractor=config_dict["extractor"],
            formatter=config_dict["formatter"],
            mindmap=config_dict["mindmap"],
            critic=config_dict["critic"],
        )

        assert model_config.parser == "haiku"
        assert model_config.extractor == "haiku"
        assert model_config.formatter == "haiku"
        assert model_config.mindmap == "haiku"
        assert model_config.critic == "haiku"

    def test_quality_profile_creates_valid_model_config(self) -> None:
        """Quality profile should create valid ModelConfig."""
        config_dict = resolve_model_config(profile="quality")

        model_config = ModelConfig(
            parser=config_dict["parser"],
            extractor=config_dict["extractor"],
            formatter=config_dict["formatter"],
            mindmap=config_dict["mindmap"],
            critic=config_dict["critic"],
        )

        assert model_config.parser == "sonnet"
        assert model_config.extractor == "opus"
        assert model_config.critic == "opus"

    def test_override_config_creates_valid_model_config(self) -> None:
        """Override configuration should create valid ModelConfig."""
        config_dict = resolve_model_config(
            profile="economy",
            model_extractor="opus",
        )

        model_config = ModelConfig(
            parser=config_dict["parser"],
            extractor=config_dict["extractor"],
            formatter=config_dict["formatter"],
            mindmap=config_dict["mindmap"],
            critic=config_dict["critic"],
        )

        assert model_config.parser == "haiku"
        assert model_config.extractor == "opus"

    def test_model_config_validation_rejects_invalid_models(self) -> None:
        """ModelConfig should reject invalid model values."""
        config_dict = resolve_model_config(profile="economy")
        config_dict["parser"] = "invalid-model"

        with pytest.raises(ValueError) as exc_info:
            ModelConfig(
                parser=config_dict["parser"],
                extractor=config_dict["extractor"],
                formatter=config_dict["formatter"],
                mindmap=config_dict["mindmap"],
                critic=config_dict["critic"],
            )

        assert "invalid-model" in str(exc_info.value).lower()
        assert "parser" in str(exc_info.value).lower()


class TestCLIToAdapterIntegration:
    """Integration tests for CLI arguments flowing to adapter."""

    @pytest.fixture(autouse=True)
    def mock_adapter(self) -> MagicMock:
        """Mock the CLIAdapter to capture method calls."""
        with patch("src.interface.cli.main.CLIAdapter") as mock_class:
            mock_instance = MagicMock()
            mock_instance.cmd_transcript_parse.return_value = 0
            mock_class.return_value = mock_instance
            yield mock_instance

    @pytest.fixture(autouse=True)
    def mock_args(self) -> None:
        """Mock sys.argv to avoid test runner args interference."""
        with patch("sys.argv", ["jerry"]):
            yield

    def test_economy_profile_flows_to_adapter(self, mock_adapter: MagicMock) -> None:
        """Economy profile models should flow through to adapter call."""
        with patch(
            "sys.argv",
            ["jerry", "transcript", "parse", "test.vtt", "--profile", "economy"],
        ):
            main()

        call_args = mock_adapter.cmd_transcript_parse.call_args

        assert call_args.kwargs["model_parser"] == "haiku"
        assert call_args.kwargs["model_extractor"] == "haiku"
        assert call_args.kwargs["model_formatter"] == "haiku"
        assert call_args.kwargs["model_mindmap"] == "haiku"
        assert call_args.kwargs["model_critic"] == "haiku"

    def test_quality_profile_flows_to_adapter(self, mock_adapter: MagicMock) -> None:
        """Quality profile models should flow through to adapter call."""
        with patch(
            "sys.argv",
            ["jerry", "transcript", "parse", "test.vtt", "--profile", "quality"],
        ):
            main()

        call_args = mock_adapter.cmd_transcript_parse.call_args

        assert call_args.kwargs["model_parser"] == "sonnet"
        assert call_args.kwargs["model_extractor"] == "opus"
        assert call_args.kwargs["model_formatter"] == "sonnet"
        assert call_args.kwargs["model_mindmap"] == "sonnet"
        assert call_args.kwargs["model_critic"] == "opus"

    def test_mixed_profile_and_overrides_flow_to_adapter(self, mock_adapter: MagicMock) -> None:
        """Profile with overrides should flow correctly to adapter."""
        with patch(
            "sys.argv",
            [
                "jerry",
                "transcript",
                "parse",
                "test.vtt",
                "--profile",
                "economy",
                "--model-extractor",
                "opus",
                "--model-critic",
                "sonnet",
            ],
        ):
            main()

        call_args = mock_adapter.cmd_transcript_parse.call_args

        assert call_args.kwargs["model_parser"] == "haiku"  # From economy
        assert call_args.kwargs["model_extractor"] == "opus"  # Override
        assert call_args.kwargs["model_formatter"] == "haiku"  # From economy
        assert call_args.kwargs["model_mindmap"] == "haiku"  # From economy
        assert call_args.kwargs["model_critic"] == "sonnet"  # Override

    def test_all_five_overrides_flow_to_adapter(self, mock_adapter: MagicMock) -> None:
        """All five individual overrides should flow to adapter."""
        with patch(
            "sys.argv",
            [
                "jerry",
                "transcript",
                "parse",
                "test.vtt",
                "--model-parser",
                "opus",
                "--model-extractor",
                "opus",
                "--model-formatter",
                "sonnet",
                "--model-mindmap",
                "sonnet",
                "--model-critic",
                "opus",
            ],
        ):
            main()

        call_args = mock_adapter.cmd_transcript_parse.call_args

        assert call_args.kwargs["model_parser"] == "opus"
        assert call_args.kwargs["model_extractor"] == "opus"
        assert call_args.kwargs["model_formatter"] == "sonnet"
        assert call_args.kwargs["model_mindmap"] == "sonnet"
        assert call_args.kwargs["model_critic"] == "opus"


class TestValidationIntegration:
    """Integration tests for validation behavior."""

    def test_invalid_profile_name_raises_key_error(self) -> None:
        """Invalid profile name should raise KeyError with helpful message."""
        with pytest.raises(KeyError) as exc_info:
            resolve_model_config(profile="nonexistent")

        assert "nonexistent" in str(exc_info.value)
        assert "economy" in str(exc_info.value)
        assert "balanced" in str(exc_info.value)
        assert "quality" in str(exc_info.value)
        assert "speed" in str(exc_info.value)

    def test_profile_constants_match_registry(self) -> None:
        """Profile constants should match registry definitions."""
        from src.interface.cli.model_profiles import PROFILES

        assert PROFILES["economy"] == ECONOMY
        assert PROFILES["balanced"] == BALANCED
        assert PROFILES["quality"] == QUALITY
        assert PROFILES["speed"] == SPEED

    def test_all_profiles_have_complete_metadata(self) -> None:
        """All profiles should have all required metadata fields."""
        from src.interface.cli.model_profiles import PROFILES

        for profile in PROFILES.values():
            assert profile.name
            assert profile.description
            assert profile.use_case
            assert profile.trade_off
            assert profile.parser in {"haiku", "sonnet", "opus"}
            assert profile.extractor in {"haiku", "sonnet", "opus"}
            assert profile.formatter in {"haiku", "sonnet", "opus"}
            assert profile.mindmap in {"haiku", "sonnet", "opus"}
            assert profile.critic in {"haiku", "sonnet", "opus"}


class TestEdgeCases:
    """Integration tests for edge cases and boundary conditions."""

    def test_none_values_in_overrides_are_ignored(self) -> None:
        """None values in overrides should be ignored (use profile value)."""
        config = resolve_model_config(
            profile="quality",
            model_parser=None,
            model_extractor=None,
        )

        # Should use quality profile values
        assert config["parser"] == "sonnet"
        assert config["extractor"] == "opus"

    def test_empty_string_profile_uses_default(self) -> None:
        """Empty string profile should be treated as None (use default).

        Empty string is falsy in Python, so the 'profile or DEFAULT_PROFILE'
        expression will use DEFAULT_PROFILE when profile is an empty string.
        """
        # Empty string is falsy, so should use default (balanced)
        config = resolve_model_config(profile="")

        # Should use balanced profile (empty string is falsy)
        assert config["parser"] == "haiku"
        assert config["extractor"] == "sonnet"
        assert config["formatter"] == "haiku"
        assert config["mindmap"] == "sonnet"
        assert config["critic"] == "sonnet"

    def test_profile_override_precedence_is_consistent(self) -> None:
        """Override precedence should be consistent across all agents."""
        # Test that explicit flags always win, even with quality profile
        config = resolve_model_config(
            profile="quality",
            model_parser="haiku",
            model_extractor="haiku",
            model_formatter="haiku",
            model_mindmap="haiku",
            model_critic="haiku",
        )

        # All should be haiku despite quality profile
        assert all(v == "haiku" for v in config.values())

    def test_model_config_to_dict_includes_all_agents(self) -> None:
        """ModelConfig.to_dict() should include all transcript agents."""
        config_dict = resolve_model_config(profile="balanced")
        model_config = ModelConfig(**config_dict)

        agent_dict = model_config.to_dict()

        assert "ts-parser" in agent_dict
        assert "ts-extractor" in agent_dict
        assert "ts-formatter" in agent_dict
        assert "ts-mindmap-mermaid" in agent_dict
        assert "ts-mindmap-ascii" in agent_dict
        assert "ps-critic" in agent_dict

    def test_mindmap_agents_share_same_model(self) -> None:
        """Both mindmap agents should use same model from config."""
        config_dict = resolve_model_config(
            profile="balanced",
            model_mindmap="opus",
        )
        model_config = ModelConfig(**config_dict)

        agent_dict = model_config.to_dict()

        assert agent_dict["ts-mindmap-mermaid"] == "opus"
        assert agent_dict["ts-mindmap-ascii"] == "opus"
        assert agent_dict["ts-mindmap-mermaid"] == agent_dict["ts-mindmap-ascii"]
