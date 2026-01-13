"""
Guardrail Pattern Library

Work Item: WI-SAO-015

This package provides pattern-based validation for Claude Code hooks.

Usage:
    from patterns import load_patterns

    library = load_patterns()
    result = library.validate_input("Write", {"file_path": "/etc/passwd"})
    if result.decision == "block":
        print(f"Blocked: {result.reason}")
"""

from .loader import (
    PatternGroup,
    PatternLibrary,
    PatternMatch,
    PatternRule,
    ValidationResult,
    load_patterns,
)

__all__ = [
    "PatternLibrary",
    "PatternGroup",
    "PatternMatch",
    "PatternRule",
    "ValidationResult",
    "load_patterns",
]
