# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tool family info value object.

Describes a registered tool family plugin, including its resolver module
and class for dynamic loading via importlib.

References:
    - ADR-PROJ023-001: Multi-family plugin architecture
    - TASK-001C: Value Objects
    - DA-004/IN-004 (FIX-16): Explicit priority field for auto-detection ordering
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ToolFamilyInfo:
    """Immutable descriptor for a registered tool family.

    Each tool family is a plugin that provides a resolver implementing
    the ToolFamilyResolverPort interface. Families are loaded from
    tool_families.yaml at startup.

    Attributes:
        name: Unique family identifier (e.g., 'rainbow').
        description: Human-readable description of the family's purpose.
        resolver_module: Fully qualified Python module path for the resolver.
        resolver_class: Class name within the module that implements
            ToolFamilyResolverPort.
        config_path: Path to the family's tool resolution configuration file,
            relative to the project root.
        enabled: Whether this family is active in the current configuration.
        priority: Explicit priority for auto-detection ordering. Lower value
            means higher priority (checked first during auto-detection).
            Default 100 keeps existing entries at standard priority.
            DA-004/IN-004 (FIX-16): Replaces implicit YAML dict insertion order.
        tool_count: Number of tools registered for this family, or None if the
            count could not be determined (config unreadable or not loaded).
            CV-013B: Required by UC-004 Step 3 for --list-families display.
    """

    name: str
    description: str
    resolver_module: str
    resolver_class: str
    config_path: str
    enabled: bool = True
    priority: int = field(default=100)
    tool_count: int | None = field(default=None)
