# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ValidationFinding - A single validation finding from compose output checking.

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ValidationFinding:
    """A single validation finding from compose output checking.

    Attributes:
        check_id: Check identifier (CV-001 through CV-007, SCV-001 through SCV-006).
        severity: 'error' or 'warning'.
        message: Human-readable description.
        agent_name: Agent or skill that triggered the finding.
    """

    check_id: str
    severity: str
    message: str
    agent_name: str = ""
