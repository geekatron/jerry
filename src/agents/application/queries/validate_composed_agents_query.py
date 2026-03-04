# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ValidateComposedAgentsQuery - Query to validate composed agent .md files.

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidateComposedAgentsQuery:
    """Query to validate composed agent .md files against CV-001 through CV-007.

    Attributes:
        agent_name: Optional specific agent to validate. None = validate all.
    """

    agent_name: str | None = None
