"""Reusable test fixtures for model selection testing.

This module provides pytest fixtures and helper utilities for testing
the model selection feature across unit, integration, and E2E tests.

References:
    - TASK-424: Integration Testing - Track B
    - EN-031: Model Selection Capability
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.interface.cli.model_profiles import (
    BALANCED,
    ECONOMY,
    QUALITY,
    SPEED,
    ModelProfile,
    resolve_model_config,
)
from src.transcript.domain.value_objects.model_config import ModelConfig

# ============================================================================
# Profile Fixtures
# ============================================================================


@pytest.fixture
def economy_profile() -> ModelProfile:
    """Provide economy profile for testing."""
    return ECONOMY


@pytest.fixture
def balanced_profile() -> ModelProfile:
    """Provide balanced profile for testing."""
    return BALANCED


@pytest.fixture
def quality_profile() -> ModelProfile:
    """Provide quality profile for testing."""
    return QUALITY


@pytest.fixture
def speed_profile() -> ModelProfile:
    """Provide speed profile for testing."""
    return SPEED


@pytest.fixture
def all_profiles() -> dict[str, ModelProfile]:
    """Provide all profiles as a dictionary."""
    return {
        "economy": ECONOMY,
        "balanced": BALANCED,
        "quality": QUALITY,
        "speed": SPEED,
    }


# ============================================================================
# Model Configuration Fixtures
# ============================================================================


@pytest.fixture
def economy_config() -> dict[str, str]:
    """Provide economy profile model configuration."""
    return resolve_model_config(profile="economy")


@pytest.fixture
def balanced_config() -> dict[str, str]:
    """Provide balanced profile model configuration."""
    return resolve_model_config(profile="balanced")


@pytest.fixture
def quality_config() -> dict[str, str]:
    """Provide quality profile model configuration."""
    return resolve_model_config(profile="quality")


@pytest.fixture
def speed_config() -> dict[str, str]:
    """Provide speed profile model configuration."""
    return resolve_model_config(profile="speed")


@pytest.fixture
def custom_config() -> dict[str, str]:
    """Provide custom model configuration for testing overrides."""
    return {
        "parser": "opus",
        "extractor": "opus",
        "formatter": "sonnet",
        "mindmap": "sonnet",
        "critic": "opus",
    }


# ============================================================================
# ModelConfig Value Object Fixtures
# ============================================================================


@pytest.fixture
def economy_model_config() -> ModelConfig:
    """Provide economy ModelConfig instance."""
    config = resolve_model_config(profile="economy")
    return ModelConfig(**config)


@pytest.fixture
def balanced_model_config() -> ModelConfig:
    """Provide balanced ModelConfig instance."""
    config = resolve_model_config(profile="balanced")
    return ModelConfig(**config)


@pytest.fixture
def quality_model_config() -> ModelConfig:
    """Provide quality ModelConfig instance."""
    config = resolve_model_config(profile="quality")
    return ModelConfig(**config)


@pytest.fixture
def speed_model_config() -> ModelConfig:
    """Provide speed ModelConfig instance."""
    config = resolve_model_config(profile="speed")
    return ModelConfig(**config)


# ============================================================================
# Mock Fixtures
# ============================================================================


@pytest.fixture
def mock_cli_adapter() -> MagicMock:
    """Provide mock CLIAdapter for testing."""
    mock = MagicMock()
    mock.cmd_transcript_parse.return_value = 0
    return mock


@pytest.fixture
def mock_model_config() -> MagicMock:
    """Provide mock ModelConfig for testing."""
    mock = MagicMock(spec=ModelConfig)
    mock.parser = "haiku"
    mock.extractor = "sonnet"
    mock.formatter = "haiku"
    mock.mindmap = "sonnet"
    mock.critic = "sonnet"
    return mock


# ============================================================================
# Validation Helper Functions
# ============================================================================


def assert_all_haiku(config: dict[str, str]) -> None:
    """Assert that all models in config are haiku.

    Args:
        config: Model configuration dictionary

    Raises:
        AssertionError: If any model is not haiku
    """
    for agent, model in config.items():
        assert model == "haiku", f"Expected haiku for {agent}, got {model}"


def assert_all_opus(config: dict[str, str]) -> None:
    """Assert that all models in config are opus.

    Args:
        config: Model configuration dictionary

    Raises:
        AssertionError: If any model is not opus
    """
    for agent, model in config.items():
        assert model == "opus", f"Expected opus for {agent}, got {model}"


def assert_all_sonnet(config: dict[str, str]) -> None:
    """Assert that all models in config are sonnet.

    Args:
        config: Model configuration dictionary

    Raises:
        AssertionError: If any model is not sonnet
    """
    for agent, model in config.items():
        assert model == "sonnet", f"Expected sonnet for {agent}, got {model}"


def assert_config_matches_profile(config: dict[str, str], profile: ModelProfile) -> None:
    """Assert that config matches the given profile.

    Args:
        config: Model configuration dictionary
        profile: ModelProfile to compare against

    Raises:
        AssertionError: If config doesn't match profile
    """
    assert config["parser"] == profile.parser
    assert config["extractor"] == profile.extractor
    assert config["formatter"] == profile.formatter
    assert config["mindmap"] == profile.mindmap
    assert config["critic"] == profile.critic


def assert_valid_model_values(config: dict[str, str]) -> None:
    """Assert that all model values are valid (opus, sonnet, or haiku).

    Args:
        config: Model configuration dictionary

    Raises:
        AssertionError: If any model value is invalid
    """
    valid_models = {"opus", "sonnet", "haiku"}
    for agent, model in config.items():
        assert model in valid_models, (
            f"Invalid model for {agent}: {model} (must be one of {valid_models})"
        )


def assert_override_applied(config: dict[str, str], agent: str, expected_model: str) -> None:
    """Assert that override was applied for specific agent.

    Args:
        config: Model configuration dictionary
        agent: Agent name (parser, extractor, formatter, mindmap, critic)
        expected_model: Expected model value after override

    Raises:
        AssertionError: If override was not applied
    """
    assert config[agent] == expected_model, (
        f"Expected {agent} to be {expected_model}, got {config[agent]}"
    )


# ============================================================================
# Profile Comparison Functions
# ============================================================================


def configs_equal(config1: dict[str, str], config2: dict[str, str]) -> bool:
    """Compare two model configurations for equality.

    Args:
        config1: First configuration
        config2: Second configuration

    Returns:
        True if configurations are identical, False otherwise
    """
    return (
        config1["parser"] == config2["parser"]
        and config1["extractor"] == config2["extractor"]
        and config1["formatter"] == config2["formatter"]
        and config1["mindmap"] == config2["mindmap"]
        and config1["critic"] == config2["critic"]
    )


def profile_uses_model(profile: ModelProfile, model: str) -> bool:
    """Check if profile uses a specific model for any agent.

    Args:
        profile: ModelProfile to check
        model: Model value to search for

    Returns:
        True if profile uses the model for at least one agent
    """
    return (
        profile.parser == model
        or profile.extractor == model
        or profile.formatter == model
        or profile.mindmap == model
        or profile.critic == model
    )


def count_model_usage(config: dict[str, str], model: str) -> int:
    """Count how many agents use a specific model.

    Args:
        config: Model configuration dictionary
        model: Model value to count

    Returns:
        Number of agents using the specified model
    """
    return sum(1 for m in config.values() if m == model)


# ============================================================================
# Model Config Creation Helpers
# ============================================================================


def create_model_config_from_dict(config: dict[str, str]) -> ModelConfig:
    """Create ModelConfig instance from configuration dictionary.

    Args:
        config: Model configuration dictionary with keys:
            parser, extractor, formatter, mindmap, critic

    Returns:
        ModelConfig instance

    Raises:
        ValueError: If model values are invalid
    """
    return ModelConfig(
        parser=config["parser"],
        extractor=config["extractor"],
        formatter=config["formatter"],
        mindmap=config["mindmap"],
        critic=config["critic"],
    )


def create_all_haiku_config() -> ModelConfig:
    """Create ModelConfig with all agents using haiku.

    Returns:
        ModelConfig with all haiku models
    """
    return ModelConfig(
        parser="haiku",
        extractor="haiku",
        formatter="haiku",
        mindmap="haiku",
        critic="haiku",
    )


def create_all_opus_config() -> ModelConfig:
    """Create ModelConfig with all agents using opus.

    Returns:
        ModelConfig with all opus models
    """
    return ModelConfig(
        parser="opus",
        extractor="opus",
        formatter="opus",
        mindmap="opus",
        critic="opus",
    )


def create_all_sonnet_config() -> ModelConfig:
    """Create ModelConfig with all agents using sonnet.

    Returns:
        ModelConfig with all sonnet models
    """
    return ModelConfig(
        parser="sonnet",
        extractor="sonnet",
        formatter="sonnet",
        mindmap="sonnet",
        critic="sonnet",
    )


# ============================================================================
# Test Data Generators
# ============================================================================


def generate_profile_test_cases() -> list[tuple[str, dict[str, str]]]:
    """Generate test cases for all profiles.

    Returns:
        List of (profile_name, expected_config) tuples
    """
    return [
        (
            "economy",
            {
                "parser": "haiku",
                "extractor": "haiku",
                "formatter": "haiku",
                "mindmap": "haiku",
                "critic": "haiku",
            },
        ),
        (
            "balanced",
            {
                "parser": "haiku",
                "extractor": "sonnet",
                "formatter": "haiku",
                "mindmap": "sonnet",
                "critic": "sonnet",
            },
        ),
        (
            "quality",
            {
                "parser": "sonnet",
                "extractor": "opus",
                "formatter": "sonnet",
                "mindmap": "sonnet",
                "critic": "opus",
            },
        ),
        (
            "speed",
            {
                "parser": "haiku",
                "extractor": "haiku",
                "formatter": "haiku",
                "mindmap": "haiku",
                "critic": "haiku",
            },
        ),
    ]


def generate_override_test_cases() -> list[tuple[str, str, str]]:
    """Generate test cases for model overrides.

    Returns:
        List of (agent_name, base_model, override_model) tuples
    """
    agents = ["parser", "extractor", "formatter", "mindmap", "critic"]
    models = ["haiku", "sonnet", "opus"]

    test_cases = []
    for agent in agents:
        for base in models:
            for override in models:
                if base != override:
                    test_cases.append((agent, base, override))

    return test_cases


def generate_invalid_model_names() -> list[str]:
    """Generate list of invalid model names for negative testing.

    Returns:
        List of invalid model name strings
    """
    return [
        "invalid",
        "gpt-4",
        "claude-3",
        "HAIKU",
        "Sonnet",
        "Opus",
        "",
        "haiku-3",
        "sonnet-3.5",
        "opus-4",
        "anthropic/opus",
    ]
