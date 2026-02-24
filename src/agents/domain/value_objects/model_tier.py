# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ModelTier - Abstract model capability classification.

Maps to vendor-specific model names at build time via mappings.yaml.

References:
    - ADR-PROJ010-003: LLM Portability Architecture
    - agent-development-standards.md: AD-M-009 model selection
"""

from __future__ import annotations

from enum import Enum


class ModelTier(Enum):
    """Abstract model capability tier.

    Attributes:
        REASONING_HIGH: Complex reasoning, research, architecture, synthesis.
        REASONING_STANDARD: Balanced analysis, standard production tasks.
        FAST: Quick repetitive tasks, formatting, validation.

    Example:
        >>> ModelTier.from_string("reasoning_high")
        <ModelTier.REASONING_HIGH: 'reasoning_high'>
    """

    REASONING_HIGH = "reasoning_high"
    REASONING_STANDARD = "reasoning_standard"
    FAST = "fast"

    @classmethod
    def from_string(cls, value: str) -> ModelTier:
        """Parse model tier from string.

        Args:
            value: Tier name (case-insensitive).

        Returns:
            Matching ModelTier enum value.

        Raises:
            ValueError: If value is not a valid model tier.
        """
        normalized = value.lower().strip()
        for tier in cls:
            if tier.value == normalized:
                return tier
        valid = [t.value for t in cls]
        raise ValueError(f"Invalid model tier: {value!r}. Valid tiers: {', '.join(valid)}")

    @classmethod
    def from_vendor_model(cls, vendor: str, model_name: str) -> ModelTier:
        """Reverse-map a vendor-specific model name to abstract tier.

        Args:
            vendor: Vendor identifier (e.g., 'claude_code').
            model_name: Vendor-specific model name (e.g., 'opus').

        Returns:
            Corresponding abstract model tier.

        Raises:
            ValueError: If model name is not recognized for this vendor.
        """
        reverse_map: dict[str, dict[str, ModelTier]] = {
            "claude_code": {
                "opus": ModelTier.REASONING_HIGH,
                "sonnet": ModelTier.REASONING_STANDARD,
                "haiku": ModelTier.FAST,
            },
        }
        vendor_map = reverse_map.get(vendor, {})
        tier = vendor_map.get(model_name.lower().strip())
        if tier is None:
            raise ValueError(
                f"Unknown model '{model_name}' for vendor '{vendor}'. "
                f"Known models: {', '.join(vendor_map.keys())}"
            )
        return tier
