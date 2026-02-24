# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
GeneratedArtifact - Generated vendor-specific agent file.

Represents a single output file produced by a vendor adapter
from a CanonicalAgent source.

References:
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.agents.domain.value_objects.vendor_target import VendorTarget


@dataclass(frozen=True)
class GeneratedArtifact:
    """A generated vendor-specific file.

    Attributes:
        path: Target file path for the generated file.
        content: Generated file content as string.
        vendor: Vendor target this artifact was generated for.
        source_agent: Name of the canonical agent this was generated from.
        artifact_type: Type of artifact (e.g., 'agent_definition', 'governance').
    """

    path: Path
    content: str
    vendor: VendorTarget
    source_agent: str
    artifact_type: str

    @property
    def filename(self) -> str:
        """Return the filename portion of the path."""
        return self.path.name
