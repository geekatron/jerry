# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
FilesystemVendorOverrideProvider - Reads per-agent vendor overrides from the filesystem.

Override files are expected at:
  skills/{skill}/composition/{agent}.{vendor-slug}.yaml

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.agents.application.ports.vendor_override_provider import IVendorOverrideProvider

# Vendor slug mapping: vendor identifier -> filename slug
_VENDOR_SLUG_MAP: dict[str, str] = {
    "claude_code": "claude-code",
    "openai": "openai",
    "google_adk": "google-adk",
    "ollama": "ollama",
}


class FilesystemVendorOverrideProvider(IVendorOverrideProvider):
    """Reads per-agent vendor override files from skill composition directories.

    Attributes:
        _skills_dir: Root skills/ directory.
    """

    def __init__(self, skills_dir: Path) -> None:
        """Initialize with skills directory.

        Args:
            skills_dir: Path to the skills/ directory.
        """
        self._skills_dir = skills_dir

    def get_overrides(self, agent_name: str, skill: str, vendor: str) -> dict[str, Any]:
        """Load per-agent vendor overrides from composition directory.

        Looks for: skills/{skill}/composition/{agent}.{vendor-slug}.yaml

        Args:
            agent_name: Agent identifier (e.g., 'ps-architect').
            skill: Parent skill name (e.g., 'problem-solving').
            vendor: Vendor identifier (e.g., 'claude_code').

        Returns:
            Parsed override dictionary. Empty dict if no override file exists.
        """
        slug = _VENDOR_SLUG_MAP.get(vendor, vendor.replace("_", "-"))
        filename = f"{agent_name}.{slug}.yaml"
        path = self._skills_dir / skill / "composition" / filename

        if not path.exists():
            return {}

        try:
            content = path.read_text(encoding="utf-8")
            data = yaml.safe_load(content)
            return data if isinstance(data, dict) else {}
        except (yaml.YAMLError, OSError):
            return {}
