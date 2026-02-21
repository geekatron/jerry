# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ConfigThresholdAdapter - Bridge from IThresholdConfiguration to LayeredConfigAdapter.

This adapter implements the IThresholdConfiguration port by delegating
to the LayeredConfigAdapter infrastructure. It reads context monitoring
threshold values from the ``context_monitor.*`` configuration namespace
and provides sensible defaults when keys are not explicitly configured.

Configuration Precedence (inherited from LayeredConfigAdapter):
    1. Environment variables (JERRY_CONTEXT_MONITOR__*) -- highest
    2. Project config (context_monitor.* in project TOML)
    3. Root config (context_monitor.* in root TOML)
    4. Code defaults defined in this adapter -- lowest

Configuration Keys:
    - context_monitor.nominal_threshold: 0.55
    - context_monitor.warning_threshold: 0.70
    - context_monitor.critical_threshold: 0.80
    - context_monitor.emergency_threshold: 0.88
    - context_monitor.compaction_detection_threshold: 10000
    - context_monitor.enabled: True

References:
    - EN-002: ConfigThresholdAdapter + IThresholdConfiguration Port
    - FEAT-001: Context Detection
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from src.infrastructure.adapters.configuration.layered_config_adapter import (
    LayeredConfigAdapter,
)

# ---------------------------------------------------------------------------
# Default threshold values
# ---------------------------------------------------------------------------

_DEFAULT_THRESHOLDS: dict[str, float] = {
    "nominal": 0.55,
    "warning": 0.70,
    "critical": 0.80,
    "emergency": 0.88,
}

_DEFAULT_COMPACTION_DETECTION_THRESHOLD: int = 10000
_DEFAULT_ENABLED: bool = True

# Mapping from tier name to config key suffix
_TIER_KEY_MAP: dict[str, str] = {
    "nominal": "nominal_threshold",
    "warning": "warning_threshold",
    "critical": "critical_threshold",
    "emergency": "emergency_threshold",
}

_CONFIG_NAMESPACE: str = "context_monitor"


class ConfigThresholdAdapter:
    """Adapter bridging IThresholdConfiguration to LayeredConfigAdapter.

    Reads context monitoring threshold configuration from the layered
    configuration system and provides typed access with sensible defaults.

    This class satisfies the ``IThresholdConfiguration`` protocol without
    explicitly inheriting from it, following the structural subtyping
    pattern used throughout the Jerry codebase.

    Attributes:
        config: The underlying LayeredConfigAdapter for configuration access.

    Example:
        >>> from src.infrastructure.adapters.configuration.layered_config_adapter import (
        ...     LayeredConfigAdapter,
        ... )
        >>> layered = LayeredConfigAdapter(defaults={})
        >>> adapter = ConfigThresholdAdapter(config=layered)
        >>> adapter.get_threshold("warning")
        0.70
        >>> adapter.is_enabled()
        True
    """

    def __init__(self, config: LayeredConfigAdapter) -> None:
        """Initialize with a LayeredConfigAdapter.

        Args:
            config: The layered configuration adapter to delegate to.
        """
        self._config = config

    def get_threshold(self, tier: str) -> float:
        """Get the threshold value for a context monitoring tier.

        Supported tiers: "nominal", "warning", "critical", "emergency".
        Tier names are case-insensitive.

        Args:
            tier: The threshold tier name.

        Returns:
            The threshold value as a float between 0.0 and 1.0.

        Raises:
            ValueError: If the tier name is not recognized.

        Example:
            >>> adapter.get_threshold("warning")
            0.70
        """
        tier_lower = tier.lower()

        if tier_lower not in _TIER_KEY_MAP:
            valid_tiers = ", ".join(sorted(_TIER_KEY_MAP.keys()))
            msg = (
                f"Unrecognized threshold tier: '{tier}'. "
                f"Valid tiers: {valid_tiers}"
            )
            raise ValueError(msg)

        key = f"{_CONFIG_NAMESPACE}.{_TIER_KEY_MAP[tier_lower]}"
        default = _DEFAULT_THRESHOLDS[tier_lower]
        return self._config.get_float(key, default=default)

    def is_enabled(self) -> bool:
        """Check whether context monitoring is enabled.

        Reads from ``context_monitor.enabled`` config key.
        Defaults to True if not explicitly configured.

        Returns:
            True if context monitoring is active, False otherwise.

        Example:
            >>> adapter.is_enabled()
            True
        """
        key = f"{_CONFIG_NAMESPACE}.enabled"
        return self._config.get_bool(key, default=_DEFAULT_ENABLED)

    def get_compaction_detection_threshold(self) -> int:
        """Get the compaction detection threshold in tokens.

        Reads from ``context_monitor.compaction_detection_threshold`` config key.
        Defaults to 10000 tokens.

        Returns:
            The compaction detection threshold in tokens.

        Example:
            >>> adapter.get_compaction_detection_threshold()
            10000
        """
        key = f"{_CONFIG_NAMESPACE}.compaction_detection_threshold"
        return self._config.get_int(key, default=_DEFAULT_COMPACTION_DETECTION_THRESHOLD)

    def get_all_thresholds(self) -> dict[str, float]:
        """Get all threshold tiers and their current values.

        Returns:
            Dictionary mapping tier names to threshold float values.

        Example:
            >>> adapter.get_all_thresholds()
            {'nominal': 0.55, 'warning': 0.70, 'critical': 0.80, 'emergency': 0.88}
        """
        return {tier: self.get_threshold(tier) for tier in _TIER_KEY_MAP}
