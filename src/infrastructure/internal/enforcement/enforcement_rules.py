# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Static rule definitions for the PreToolUse enforcement engine.

Contains constants for governance file paths, enforced directories,
exempt patterns, and layer dependency rules. These definitions are
the single source of truth for enforcement configuration.

References:
    - EN-703: PreToolUse Enforcement Engine
    - H-07, H-08: Hexagonal Architecture import boundary rules
    - H-10: One-class-per-file rule
"""

from __future__ import annotations

# Governance files requiring criticality escalation
# Key: file path pattern (prefix match), Value: criticality level
GOVERNANCE_FILES: dict[str, str] = {
    "docs/governance/JERRY_CONSTITUTION.md": "C4",
    "docs/governance/": "C3",
    ".claude/rules/": "C3",
    ".context/rules/": "C3",
}

# File extensions subject to AST enforcement
PYTHON_EXTENSIONS: set[str] = {".py"}

# Directories subject to enforcement
ENFORCED_DIRECTORIES: set[str] = {"src"}

# Directories exempt from enforcement
EXEMPT_DIRECTORIES: set[str] = {"tests", "scripts", "hooks"}

# Files exempt from import boundary checks (composition root)
EXEMPT_FILES: set[str] = {"bootstrap.py"}

# Layer dependency rules (H-07, H-08)
# Key: source layer, Value: set of forbidden import targets
LAYER_IMPORT_RULES: dict[str, set[str]] = {
    "domain": {"application", "infrastructure", "interface"},
    "application": {"infrastructure", "interface"},
    "infrastructure": {"interface"},
    "shared_kernel": {"infrastructure", "interface"},
}

# Recognized layers for dependency checking
RECOGNIZED_LAYERS: set[str] = {
    "domain",
    "application",
    "infrastructure",
    "interface",
    "shared_kernel",
}

# Recognized bounded contexts that have internal layer structure
BOUNDED_CONTEXTS: set[str] = {
    "session_management",
    "work_tracking",
    "transcript",
    "configuration",
}
