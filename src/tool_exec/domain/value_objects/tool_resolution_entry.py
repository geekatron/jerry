# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tool resolution entry value object.

Represents a resolved tool command with its execution metadata: binary path,
container service, default execution mode, security zone, and owning family.

References:
    - ADR-PROJ023-001: Tool Resolution Table
    - TASK-001C: Value Objects
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ToolResolutionEntry:
    """Immutable result of resolving a tool command to its execution metadata.

    Produced by a ToolFamilyResolverPort when a tool command matches a known
    prefix in the family's resolution table.

    Attributes:
        tool_name: The resolved tool name (e.g., 'nuclei', 'impacket-GetNPUsers').
        binary_path: Absolute path to the local binary, or None if container-only.
        container_service: Docker Compose service name for container execution,
            or None if local-only.
        default_mode: Default execution mode: 'local' or 'container'.
        supported_modes: List of execution modes this tool supports.
        zone: Security zone classification: 'Zone 1', 'Zone 2', or 'Zone 3'.
        family: Name of the family that resolved this tool.
        compose_file: Path to docker-compose.yml for container execution,
            relative to project root.
        sub_skill: Sub-skill identifier for per-sub-skill mode overrides.
    """

    tool_name: str
    binary_path: str | None
    container_service: str | None
    default_mode: str
    supported_modes: list[str] = field(default_factory=lambda: ["local", "container"])
    zone: str = "Zone 1"
    family: str = ""
    compose_file: str | None = None
    sub_skill: str | None = None

    def __post_init__(self) -> None:
        """Validate resolution entry invariants."""
        valid_modes = {"local", "container"}
        if self.default_mode not in valid_modes:
            msg = (
                f"Invalid default_mode '{self.default_mode}'. "
                f"Must be one of: {', '.join(sorted(valid_modes))}"
            )
            raise ValueError(msg)

        valid_zones = {"Zone 1", "Zone 2", "Zone 3"}
        if self.zone not in valid_zones:
            msg = f"Invalid zone '{self.zone}'. Must be one of: {', '.join(sorted(valid_zones))}"
            raise ValueError(msg)
