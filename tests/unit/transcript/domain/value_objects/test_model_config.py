# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for ModelConfig value object.

References:
    - TASK-420: Add CLI parameters for model selection
    - EN-031: Model Selection Capability
"""

from __future__ import annotations

import pytest

from src.transcript.domain.value_objects.model_config import ModelConfig


class TestModelConfigCreation:
    """Test ModelConfig creation and defaults."""

    def test_default_values(self) -> None:
        """Default models match recommended defaults from TASK-419."""
        config = ModelConfig()

        assert config.parser == "haiku"
        assert config.extractor == "sonnet"
        assert config.formatter == "sonnet"
        assert config.mindmap == "sonnet"
        assert config.critic == "sonnet"

    def test_custom_values(self) -> None:
        """Custom model values are accepted."""
        config = ModelConfig(
            parser="opus",
            extractor="haiku",
            formatter="opus",
            mindmap="haiku",
            critic="opus",
        )

        assert config.parser == "opus"
        assert config.extractor == "haiku"
        assert config.formatter == "opus"
        assert config.mindmap == "haiku"
        assert config.critic == "opus"

    def test_immutability(self) -> None:
        """ModelConfig is immutable (frozen dataclass)."""
        config = ModelConfig()

        with pytest.raises(AttributeError):
            config.parser = "opus"  # type: ignore


class TestModelConfigValidation:
    """Test ModelConfig validation."""

    def test_invalid_parser_model(self) -> None:
        """Invalid parser model raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            ModelConfig(parser="gpt-4")

        assert "Invalid model for parser" in str(exc_info.value)
        assert "gpt-4" in str(exc_info.value)

    def test_invalid_extractor_model(self) -> None:
        """Invalid extractor model raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            ModelConfig(extractor="llama")

        assert "Invalid model for extractor" in str(exc_info.value)

    def test_invalid_formatter_model(self) -> None:
        """Invalid formatter model raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            ModelConfig(formatter="gemini")

        assert "Invalid model for formatter" in str(exc_info.value)

    def test_invalid_mindmap_model(self) -> None:
        """Invalid mindmap model raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            ModelConfig(mindmap="chatgpt")

        assert "Invalid model for mindmap" in str(exc_info.value)

    def test_invalid_critic_model(self) -> None:
        """Invalid critic model raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            ModelConfig(critic="bard")

        assert "Invalid model for critic" in str(exc_info.value)

    def test_valid_model_values(self) -> None:
        """All valid model values (opus, sonnet, haiku) are accepted."""
        # Test each valid model for each field
        for model in ["opus", "sonnet", "haiku"]:
            config = ModelConfig(
                parser=model,
                extractor=model,
                formatter=model,
                mindmap=model,
                critic=model,
            )
            assert config.parser == model
            assert config.extractor == model
            assert config.formatter == model
            assert config.mindmap == model
            assert config.critic == model


class TestModelConfigToDict:
    """Test ModelConfig.to_dict() method."""

    def test_to_dict_structure(self) -> None:
        """to_dict() returns correct agent name mapping."""
        config = ModelConfig()
        result = config.to_dict()

        assert isinstance(result, dict)
        assert "ts-parser" in result
        assert "ts-extractor" in result
        assert "ts-formatter" in result
        assert "ts-mindmap-mermaid" in result
        assert "ts-mindmap-ascii" in result
        assert "ps-critic" in result

    def test_to_dict_values(self) -> None:
        """to_dict() maps model values correctly."""
        config = ModelConfig(
            parser="haiku",
            extractor="opus",
            formatter="sonnet",
            mindmap="opus",
            critic="haiku",
        )
        result = config.to_dict()

        assert result["ts-parser"] == "haiku"
        assert result["ts-extractor"] == "opus"
        assert result["ts-formatter"] == "sonnet"
        assert result["ts-mindmap-mermaid"] == "opus"
        assert result["ts-mindmap-ascii"] == "opus"  # Both mindmap agents use same model
        assert result["ps-critic"] == "haiku"

    def test_to_dict_mindmap_shared(self) -> None:
        """Both mindmap agents share the same model value."""
        config = ModelConfig(mindmap="opus")
        result = config.to_dict()

        assert result["ts-mindmap-mermaid"] == "opus"
        assert result["ts-mindmap-ascii"] == "opus"


class TestModelConfigEquality:
    """Test ModelConfig equality and hashing."""

    def test_equality(self) -> None:
        """Two configs with same values are equal."""
        config1 = ModelConfig(parser="opus", extractor="sonnet")
        config2 = ModelConfig(parser="opus", extractor="sonnet")

        assert config1 == config2

    def test_inequality(self) -> None:
        """Two configs with different values are not equal."""
        config1 = ModelConfig(parser="opus")
        config2 = ModelConfig(parser="haiku")

        assert config1 != config2

    def test_hashable(self) -> None:
        """ModelConfig is hashable (can be used in sets/dicts)."""
        config1 = ModelConfig()
        config2 = ModelConfig()

        # Should be able to use in a set
        config_set = {config1, config2}
        assert len(config_set) == 1  # Same values = same hash
