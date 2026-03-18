# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Port interface for tool family resolvers.

Defines the abstract contract that all tool family resolver plugins must
implement. Each family (e.g., rainbow, blue-team) provides a concrete
adapter that knows how to resolve tool commands within that family's
domain.

References:
    - ADR-PROJ023-001: Multi-family ToolFamilyResolverPort plugin architecture
    - TASK-001B: Port Interface
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.tool_exec.domain.value_objects.security_policy import SecurityPolicy
    from src.tool_exec.domain.value_objects.tool_resolution_entry import (
        ToolResolutionEntry,
    )


class ToolFamilyResolverPort(ABC):
    """Abstract port for tool family resolution.

    Each tool family (rainbow, blue-team, etc.) implements this port to
    provide tool resolution, security policy lookup, and configuration
    loading for its set of tools.

    The port follows hexagonal architecture: the domain layer defines this
    interface, and infrastructure adapters provide concrete implementations.
    """

    @abstractmethod
    def can_resolve(self, tool_command: str) -> bool:
        """Check whether this family can resolve the given tool command.

        Uses longest-prefix matching against the family's tool resolution
        table. Returns True if the tool command matches any known prefix.

        Args:
            tool_command: The tool command to check (e.g., 'nuclei', 'impacket-GetNPUsers').

        Returns:
            True if this family can resolve the tool command, False otherwise.
        """

    @abstractmethod
    def resolve(self, tool_command: str) -> ToolResolutionEntry:
        """Resolve a tool command to its execution metadata.

        Performs longest-prefix matching against the family's resolution table
        and returns the full execution metadata including binary path, container
        service, security zone, and supported modes.

        Args:
            tool_command: The tool command to resolve.

        Returns:
            ToolResolutionEntry with execution metadata for the tool.

        Raises:
            src.shared_kernel.exceptions.NotFoundError: If the tool command
                cannot be resolved by this family.
        """

    @abstractmethod
    def security_policy(self, tool_command: str) -> SecurityPolicy:
        """Get the security policy for a tool command.

        Returns the security constraints that apply to the given tool,
        including engagement requirements, credential filter configuration,
        container isolation, and network access controls.

        Args:
            tool_command: The tool command to look up.

        Returns:
            SecurityPolicy with the applicable security constraints.

        Raises:
            src.shared_kernel.exceptions.NotFoundError: If the tool command
                cannot be resolved by this family.
        """

    @abstractmethod
    def load_config(self, config_path: str) -> dict:
        """Load and parse the family's tool resolution configuration.

        Reads the YAML configuration file and returns the parsed content
        as a dictionary. The configuration typically includes the tool
        resolution table, default settings, and container configuration.

        Args:
            config_path: Path to the YAML configuration file, either
                absolute or relative to the project root.

        Returns:
            Parsed configuration dictionary.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            ValueError: If the configuration file is malformed.
        """
