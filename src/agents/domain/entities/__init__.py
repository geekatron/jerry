# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Domain entities for the agents bounded context."""

from src.agents.domain.entities.canonical_agent import CanonicalAgent
from src.agents.domain.entities.generated_artifact import GeneratedArtifact

__all__ = ["CanonicalAgent", "GeneratedArtifact"]
