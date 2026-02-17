# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Transcript Bounded Context.

This bounded context handles transcript parsing, extraction, and formatting
for the Jerry Transcript Skill.

Architecture:
- domain/: Pure business logic, value objects, ports
- application/: Use cases and handlers
- infrastructure/: Adapters (VTTParser, SRTParser, etc.)

Reference: TDD-FEAT-004-hybrid-infrastructure.md v1.2.0
"""

try:
    from importlib.metadata import version

    __version__ = version("jerry")
except Exception:
    __version__ = "dev"
