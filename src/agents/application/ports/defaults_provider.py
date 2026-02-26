# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
IDefaultsProvider - Port for loading agent defaults configuration.

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IDefaultsProvider(ABC):
    """Port for loading base defaults and resolving config variables.

    Implementations load the defaults YAML and provide config variable
    resolution for ${jerry.*} pattern substitution.
    """

    @abstractmethod
    def get_defaults(self) -> dict[str, Any]:
        """Load the base defaults configuration.

        Returns:
            Parsed defaults dictionary.
        """

    @abstractmethod
    def get_vendor_defaults(self, vendor: str) -> dict[str, Any]:
        """Load vendor-specific defaults configuration.

        Args:
            vendor: Vendor identifier (e.g., 'claude_code').

        Returns:
            Parsed vendor defaults dictionary. Empty dict if not found.
        """

    @abstractmethod
    def get_config_var(self, key: str) -> str | None:
        """Resolve a ${jerry.*} config variable.

        Args:
            key: Config variable key (e.g., 'jerry.project.name').

        Returns:
            Resolved value, or None if the key is not defined.
        """
