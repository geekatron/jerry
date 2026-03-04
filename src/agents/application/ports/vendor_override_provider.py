# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
IVendorOverrideProvider - Port for loading per-agent vendor overrides.

Separated from IAgentRepository because the repository is vendor-agnostic
by design; vendor overrides are a composition-time concern.

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IVendorOverrideProvider(ABC):
    """Port for loading per-agent vendor-specific override configuration.

    Override files live in composition directories alongside canonical
    agent sources: skills/{skill}/composition/{agent}.{vendor-slug}.yaml
    """

    @abstractmethod
    def get_overrides(self, agent_name: str, skill: str, vendor: str) -> dict[str, Any]:
        """Load per-agent vendor overrides.

        Args:
            agent_name: Agent identifier (e.g., 'ps-architect').
            skill: Parent skill name (e.g., 'problem-solving').
            vendor: Vendor identifier (e.g., 'claude_code').

        Returns:
            Parsed override dictionary. Empty dict if no override file exists.
        """
