"""
Enforcement Engines for Quality Framework.

This module provides enforcement engines for the quality framework:

L1 Static Context:
    - SessionQualityContextGenerator: Quality preamble injection at session start
    - QualityContext: Structured quality context result

L2 Per-Prompt Reinforcement:
    - PromptReinforcementEngine: Token-budgeted quality rule re-injection
    - ReinforcementContent: Structured reinforcement result

L3 Pre-Action Gating:
    - PreToolEnforcementEngine: AST-based enforcement of architectural constraints
    - EnforcementDecision: Structured enforcement result
    - enforcement_rules: Static rule definitions

Design Source:
    - EPIC-002 EN-403/TASK-003 (PreToolUse design)
    - EN-402 (Priority analysis: V-038 scored 4.92 WCS)

References:
    - EN-703: PreToolUse Enforcement Engine
    - EN-705: L2 Per-Prompt Reinforcement Hook
    - EN-706: SessionStart Quality Context Injection
    - FEAT-008: Quality Framework Implementation
"""

from __future__ import annotations

from .enforcement_decision import EnforcementDecision
from .pre_tool_enforcement_engine import PreToolEnforcementEngine
from .prompt_reinforcement_engine import PromptReinforcementEngine
from .quality_context import QualityContext
from .reinforcement_content import ReinforcementContent
from .session_quality_context_generator import SessionQualityContextGenerator

__all__ = [
    "EnforcementDecision",
    "PreToolEnforcementEngine",
    "PromptReinforcementEngine",
    "QualityContext",
    "ReinforcementContent",
    "SessionQualityContextGenerator",
]
