# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
FilesystemDefaultsProvider - Reads defaults YAML from the filesystem.

Supports both the legacy single-file mode (backward compat) and the
split-file mode (governance + per-vendor defaults).

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.agents.application.ports.defaults_provider import IDefaultsProvider

# Vendor slug mapping: vendor identifier -> filename slug
_VENDOR_SLUG_MAP: dict[str, str] = {
    "claude_code": "claude-code",
    "openai": "openai",
    "google_adk": "google-adk",
    "ollama": "ollama",
}


class FilesystemDefaultsProvider(IDefaultsProvider):
    """Loads base defaults from YAML files on the filesystem.

    Supports two modes:
    - Legacy: single defaults_path for backward compatibility.
    - Split: governance_defaults_path + vendor_defaults_dir for 4-layer merge.

    Attributes:
        _governance_defaults_path: Path to governance defaults YAML.
        _vendor_defaults_dir: Directory containing vendor defaults files.
        _defaults_cache: Cached parsed governance defaults.
        _vendor_cache: Cached parsed vendor defaults by vendor name.
    """

    def __init__(
        self,
        governance_defaults_path: Path,
        vendor_defaults_dir: Path | None = None,
    ) -> None:
        """Initialize with defaults file paths.

        Args:
            governance_defaults_path: Path to governance defaults YAML.
                In legacy mode, this is the single combined defaults file.
            vendor_defaults_dir: Directory containing jerry-{vendor-slug}-defaults.yaml
                files. None for legacy single-file mode.
        """
        self._governance_defaults_path = governance_defaults_path
        self._vendor_defaults_dir = vendor_defaults_dir
        self._defaults_cache: dict[str, Any] | None = None
        self._vendor_cache: dict[str, dict[str, Any]] = {}

    def get_defaults(self) -> dict[str, Any]:
        """Load the base governance defaults configuration.

        Returns:
            Parsed defaults dictionary. Empty dict if file doesn't exist.
        """
        if self._defaults_cache is None:
            self._defaults_cache = self._load_yaml(self._governance_defaults_path)
        return dict(self._defaults_cache)

    def get_vendor_defaults(self, vendor: str) -> dict[str, Any]:
        """Load vendor-specific defaults configuration.

        Resolves vendor identifier to filename via slug mapping:
        claude_code -> jerry-claude-code-defaults.yaml

        Args:
            vendor: Vendor identifier (e.g., 'claude_code').

        Returns:
            Parsed vendor defaults dictionary. Empty dict if not found
            or if vendor_defaults_dir was not provided.
        """
        if self._vendor_defaults_dir is None:
            return {}

        if vendor in self._vendor_cache:
            return dict(self._vendor_cache[vendor])

        slug = _VENDOR_SLUG_MAP.get(vendor, vendor.replace("_", "-"))
        filename = f"jerry-{slug}-defaults.yaml"
        path = self._vendor_defaults_dir / filename

        data = self._load_yaml(path)
        self._vendor_cache[vendor] = data
        return dict(data)

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

    @staticmethod
    def _load_yaml(path: Path) -> dict[str, Any]:
        """Load and parse a YAML file.

        Args:
            path: Path to the YAML file.

        Returns:
            Parsed YAML dict, or empty dict if file is missing or invalid.
        """
        if not path.exists():
            return {}
        try:
            content = path.read_text(encoding="utf-8")
            data = yaml.safe_load(content)
            return data if isinstance(data, dict) else {}
        except (yaml.YAMLError, OSError):
            return {}
