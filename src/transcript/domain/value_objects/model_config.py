# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ModelConfig - Value object for transcript skill model selection.

This value object encapsulates the Claude model choices for each
transcript skill agent.

References:
    - TASK-420: Add CLI parameters for model selection
    - TASK-419: Validate Task tool model parameter
    - EN-031: Model Selection Capability
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModelConfig:
    """Value object representing model configuration for transcript agents.

    Attributes:
        parser: Model for ts-parser agent (default: haiku)
        extractor: Model for ts-extractor agent (default: sonnet)
        formatter: Model for ts-formatter agent (default: sonnet)
        mindmap: Model for ts-mindmap-* agents (default: sonnet)
        critic: Model for ps-critic agent (default: sonnet)

    Valid model values: 'opus', 'sonnet', 'haiku'

    Note:
        All model values are simple strings (opus|sonnet|haiku).
        No provider prefix needed per TASK-419 validation.
    """

    parser: str = "haiku"
    extractor: str = "sonnet"
    formatter: str = "sonnet"
    mindmap: str = "sonnet"
    critic: str = "sonnet"

    VALID_MODELS = {"opus", "sonnet", "haiku"}

    def __post_init__(self) -> None:
        """Validate all model values."""
        for field_name in ["parser", "extractor", "formatter", "mindmap", "critic"]:
            value = getattr(self, field_name)
            if value not in self.VALID_MODELS:
                raise ValueError(
                    f"Invalid model for {field_name}: '{value}'. "
                    f"Must be one of: {', '.join(sorted(self.VALID_MODELS))}"
                )

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary mapping agent names to model values.

        Returns:
            Dictionary with keys like 'ts-parser', 'ts-extractor', etc.
            and values like 'haiku', 'sonnet', 'opus'.
        """
        return {
            "ts-parser": self.parser,
            "ts-extractor": self.extractor,
            "ts-formatter": self.formatter,
            "ts-mindmap-mermaid": self.mindmap,
            "ts-mindmap-ascii": self.mindmap,
            "ps-critic": self.critic,
        }
