# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Structured result type for enforcement engine evaluations.

Provides the immutable ``EnforcementDecision`` dataclass used by the
PreToolEnforcementEngine to communicate pass/fail/warn decisions back
to the PreToolUse hook.

References:
    - EN-703: PreToolUse Enforcement Engine
    - EPIC-002 EN-403/TASK-003: PreToolUse hook design
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class EnforcementDecision:
    """Structured result of an enforcement evaluation.

    Attributes:
        action: One of "block", "warn", or "approve".
        reason: Human-readable explanation of the decision.
        violations: List of specific violation descriptions.
        criticality_escalation: Criticality level if governance escalation
            is required (e.g., "C3", "C4"), or None.
    """

    action: str
    reason: str
    violations: list[str] = field(default_factory=list)
    criticality_escalation: str | None = None
