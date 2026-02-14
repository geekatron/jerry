"""
Enforcement Engine for Pre-Tool-Use Architecture Validation.

This module provides AST-based enforcement of architectural constraints
at the PreToolUse hook layer (L3 Pre-Action Gating). It deterministically
validates Python code against import boundary rules (V-038) and
one-class-per-file rules (V-041) before file writes are committed.

Components:
    - PreToolEnforcementEngine: Core enforcement engine
    - EnforcementDecision: Structured enforcement result
    - enforcement_rules: Static rule definitions

Design Source:
    - EPIC-002 EN-403/TASK-003 (PreToolUse design)
    - EN-402 (Priority analysis: V-038 scored 4.92 WCS)

References:
    - EN-703: PreToolUse Enforcement Engine
    - FEAT-008: Quality Framework Implementation
"""

from __future__ import annotations

from .enforcement_decision import EnforcementDecision
from .pre_tool_enforcement_engine import PreToolEnforcementEngine

__all__ = [
    "EnforcementDecision",
    "PreToolEnforcementEngine",
]
