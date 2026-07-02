# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
OutputResolver - Application service for resolving the output base path.

Implements a four-step fallback chain:
1. Explicit config: output.base_path from IConfigurationProvider
2. (Covered by step 1 via env adapter: JERRY_OUTPUT__BASE_PATH)
3. Project fallback: projects/{JERRY_PROJECT}/ when JERRY_PROJECT is set
4. Terminal fallback: work/

References:
    - GitHub Issue #192: Configurable output base path for skill agents
    - REQ-OBP-003: OutputResolver application service specification
    - ADR-PROJ021-001: Output path resolution architecture (Decision D-2)

Exports:
    OutputResolver: Application service for output base path resolution
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from src.configuration.domain.value_objects.output_base_path import OutputBasePath

if TYPE_CHECKING:
    from src.infrastructure.adapters.configuration.layered_config_adapter import (
        IConfigurationProvider,
    )

_TERMINAL_FALLBACK = "work/"
_CONFIG_KEY = "output.base_path"


class OutputResolver:
    """Application service that resolves the effective output base path.

    Uses a four-step fallback chain to determine where agents should
    write their output. The resolver guarantees a trailing slash on
    the returned path and never returns an empty string.

    Args:
        config_provider: Configuration provider implementing IConfigurationProvider.

    Examples:
        >>> resolver = OutputResolver(config_provider=adapter)
        >>> resolver.resolve()
        'work/'
    """

    def __init__(self, config_provider: IConfigurationProvider) -> None:
        """Initialize with a configuration provider.

        Args:
            config_provider: An IConfigurationProvider instance
                (typically LayeredConfigAdapter wired at the composition root).
        """
        self._config = config_provider

    def resolve(self) -> str:
        """Resolve the effective output base path.

        Follows the four-step fallback chain:
        1. output.base_path from config (includes env var override)
        2. projects/{JERRY_PROJECT}/ when JERRY_PROJECT is set
        3. work/ as terminal fallback

        Returns:
            The resolved output base path, always ending with '/'.

        Raises:
            ValueError: If the configured path contains null bytes
                (propagated from OutputBasePath value object per REQ-OBP-003h).
        """
        # Step 1: Check explicit configuration (env > project > root > defaults)
        value = self._config.get(_CONFIG_KEY)
        if value is not None and str(value) != "":
            path = OutputBasePath(str(value))
            return self._ensure_trailing_slash(path.value)

        # Step 2: JERRY_PROJECT fallback
        project_id = os.environ.get("JERRY_PROJECT", "")
        if project_id:
            return self._ensure_trailing_slash(f"projects/{project_id}")

        # Step 3: Terminal fallback
        return _TERMINAL_FALLBACK

    @staticmethod
    def _ensure_trailing_slash(path: str) -> str:
        """Ensure the path ends with exactly one forward slash.

        Args:
            path: The path string to normalize.

        Returns:
            The path with exactly one trailing slash.
        """
        if path.endswith("/"):
            return path
        return f"{path}/"
