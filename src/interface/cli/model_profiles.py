# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Model Profiles for Transcript Skill.

This module defines predefined model configurations that optimize for
different use cases: cost, quality, speed, or a balanced approach.

Profile Selection:
    - economy: Minimize cost (all haiku)
    - balanced: Optimize cost/quality (default)
    - quality: Maximize quality (opus for critical agents)
    - speed: Minimize latency (all haiku)

Priority Resolution:
    1. Explicit --model-* flags (highest priority)
    2. --profile flag
    3. Default profile (balanced)

References:
    - TASK-423: Implement Model Profiles - Track B
    - EN-031: Model Selection Capability
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelProfile:
    """A predefined model configuration for transcript processing.

    Attributes:
        name: Profile identifier (e.g., "economy", "balanced")
        description: Human-readable description of the profile
        use_case: Recommended use case for this profile
        trade_off: What is traded off in this profile
        parser: Model for ts-parser agent
        extractor: Model for ts-extractor agent
        formatter: Model for ts-formatter agent
        mindmap: Model for ts-mindmap-* agents
        critic: Model for ps-critic agent
    """

    name: str
    description: str
    use_case: str
    trade_off: str
    parser: str
    extractor: str
    formatter: str
    mindmap: str
    critic: str

    def __str__(self) -> str:
        """Format profile for display."""
        return f"{self.name}: {self.description}"


# Profile definitions
ECONOMY = ModelProfile(
    name="economy",
    description="Minimize cost - use Haiku for all agents",
    use_case="High-volume processing, budget constraints",
    trade_off="Lower extraction quality",
    parser="haiku",
    extractor="haiku",
    formatter="haiku",
    mindmap="haiku",
    critic="haiku",
)

BALANCED = ModelProfile(
    name="balanced",
    description="Optimize cost/quality balance (default)",
    use_case="General purpose processing",
    trade_off="Balanced cost and quality",
    parser="haiku",
    extractor="sonnet",
    formatter="haiku",
    mindmap="sonnet",
    critic="sonnet",
)

QUALITY = ModelProfile(
    name="quality",
    description="Maximize quality - use Opus for critical agents",
    use_case="Critical meetings, complex content",
    trade_off="Higher cost",
    parser="sonnet",
    extractor="opus",
    formatter="sonnet",
    mindmap="sonnet",
    critic="opus",
)

SPEED = ModelProfile(
    name="speed",
    description="Minimize latency - use Haiku for all agents",
    use_case="Real-time processing, quick turnaround",
    trade_off="Quality for speed",
    parser="haiku",
    extractor="haiku",
    formatter="haiku",
    mindmap="haiku",
    critic="haiku",
)

# Profile registry
PROFILES: dict[str, ModelProfile] = {
    "economy": ECONOMY,
    "balanced": BALANCED,
    "quality": QUALITY,
    "speed": SPEED,
}

DEFAULT_PROFILE = "balanced"


def get_profile(name: str) -> ModelProfile:
    """Get a model profile by name.

    Args:
        name: Profile name (economy, balanced, quality, speed)

    Returns:
        ModelProfile instance

    Raises:
        KeyError: If profile name is not recognized
    """
    if name not in PROFILES:
        valid = ", ".join(PROFILES.keys())
        raise KeyError(f"Unknown profile '{name}'. Valid profiles: {valid}")
    return PROFILES[name]


def resolve_model_config(
    profile: str | None = None,
    model_parser: str | None = None,
    model_extractor: str | None = None,
    model_formatter: str | None = None,
    model_mindmap: str | None = None,
    model_critic: str | None = None,
) -> dict[str, str]:
    """Resolve final model configuration from profile and individual overrides.

    Priority (highest to lowest):
        1. Explicit --model-* flags
        2. --profile flag
        3. Default profile (balanced)

    Args:
        profile: Profile name (economy, balanced, quality, speed)
        model_parser: Override for ts-parser model
        model_extractor: Override for ts-extractor model
        model_formatter: Override for ts-formatter model
        model_mindmap: Override for ts-mindmap-* models
        model_critic: Override for ps-critic model

    Returns:
        Dictionary with final model configuration:
        {
            "parser": "haiku",
            "extractor": "sonnet",
            "formatter": "haiku",
            "mindmap": "sonnet",
            "critic": "sonnet"
        }

    Example:
        >>> resolve_model_config(profile="economy")
        {"parser": "haiku", "extractor": "haiku", ...}

        >>> resolve_model_config(profile="economy", model_extractor="opus")
        {"parser": "haiku", "extractor": "opus", ...}
    """
    # Start with profile (or default)
    profile_name = profile or DEFAULT_PROFILE
    base_profile = get_profile(profile_name)

    # Apply individual overrides
    return {
        "parser": model_parser or base_profile.parser,
        "extractor": model_extractor or base_profile.extractor,
        "formatter": model_formatter or base_profile.formatter,
        "mindmap": model_mindmap or base_profile.mindmap,
        "critic": model_critic or base_profile.critic,
    }
