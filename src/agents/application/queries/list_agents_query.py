# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ListAgentsQuery - Query to list all canonical agents.

References:
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ListAgentsQuery:
    """Query to list agents with their metadata.

    Attributes:
        skill: Optional skill filter. None = list all skills.
    """

    skill: str | None = None
