# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
FilesystemDefaultsProvider - Reads defaults YAML from the filesystem.

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.agents.application.ports.defaults_provider import IDefaultsProvider


class FilesystemDefaultsProvider(IDefaultsProvider):
    """Loads base defaults from a YAML file on the filesystem.

    Attributes:
        _defaults_path: Path to the defaults YAML file.
        _defaults: Cached parsed defaults (loaded lazily).
    """

    def __init__(self, defaults_path: Path) -> None:
        """Initialize with defaults file path.

        Args:
            defaults_path: Path to the jerry-claude-agent-defaults.yaml file.
        """
        self._defaults_path = defaults_path
        self._defaults: dict[str, Any] | None = None

    def get_defaults(self) -> dict[str, Any]:
        """Load the base defaults configuration.

        Returns:
            Parsed defaults dictionary. Empty dict if file doesn't exist.
        """
        if self._defaults is None:
            self._defaults = self._load()
        return dict(self._defaults)

    def get_config_var(self, key: str) -> str | None:
        """Resolve a ${jerry.*} config variable.

        Currently returns None for all keys (no config variable resolution).
        Future: integrate with LayeredConfigAdapter for env/project/root resolution.

        Args:
            key: Config variable key (e.g., 'jerry.project.name').

        Returns:
            None (config variable resolution not yet implemented).
        """
        return None

    def _load(self) -> dict[str, Any]:
        """Load and parse the defaults YAML file.

        Returns:
            Parsed YAML dict, or empty dict if file is missing or invalid.
        """
        if not self._defaults_path.exists():
            return {}
        try:
            content = self._defaults_path.read_text(encoding="utf-8")
            data = yaml.safe_load(content)
            return data if isinstance(data, dict) else {}
        except (yaml.YAMLError, OSError):
            return {}
