# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
IVendorAdapter - Port for vendor-specific agent file generation.

References:
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.agents.domain.entities.canonical_agent import CanonicalAgent
from src.agents.domain.entities.generated_artifact import GeneratedArtifact
from src.agents.domain.value_objects.vendor_target import VendorTarget


class IVendorAdapter(ABC):
    """Port for generating vendor-specific agent files from canonical source.

    Each vendor adapter implements this interface to produce files
    in the format required by that vendor's runtime.
    """

    @property
    @abstractmethod
    def vendor(self) -> VendorTarget:
        """Return the vendor target this adapter generates for."""

    @abstractmethod
    def generate(self, agent: CanonicalAgent) -> list[GeneratedArtifact]:
        """Generate vendor-specific files from a canonical agent.

        Args:
            agent: Parsed canonical agent definition.

        Returns:
            List of generated artifacts (files to write).
        """

    @abstractmethod
    def extract(
        self,
        agent_md_path: str,
        governance_yaml_path: str | None = None,
    ) -> CanonicalAgent:
        """Extract a canonical agent from existing vendor-specific files.

        This is the inverse of generate() — used for migration from
        existing vendor files to canonical source format.

        Args:
            agent_md_path: Path to existing agent .md file.
            governance_yaml_path: Path to existing .governance.yaml file.

        Returns:
            Extracted CanonicalAgent entity.
        """
