# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ValidateAgentsQuery - Query to validate canonical agent definitions.

References:
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidateAgentsQuery:
    """Query to validate all canonical agent definitions against schema.

    Attributes:
        agent_name: Optional specific agent to validate. None = validate all.
    """

    agent_name: str | None = None
