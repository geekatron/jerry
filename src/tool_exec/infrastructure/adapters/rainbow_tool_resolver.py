# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Rainbow tool family resolver adapter.

Implements ToolFamilyResolverPort for the Rainbow cybersecurity tool suite.
Loads tool resolution entries from skills/rainbow/config/tool-exec.yaml
and resolves tool commands using longest-prefix matching.

References:
    - ADR-PROJ023-001: Tool Resolution Table
    - TASK-002: RainbowToolResolver
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.shared_kernel.exceptions import NotFoundError
from src.tool_exec.domain.ports.tool_family_resolver_port import (
    ToolFamilyResolverPort,
)
from src.tool_exec.domain.value_objects.security_policy import SecurityPolicy
from src.tool_exec.domain.value_objects.tool_resolution_entry import (
    ToolResolutionEntry,
)


class RainbowToolResolver(ToolFamilyResolverPort):
    """Resolves tool commands for the Rainbow cybersecurity tool suite.

    Supports 30+ tools across 6 sub-skills: exploit, recon, runtime,
    cloud, supply-chain, and blue-team detection. Uses longest-prefix
    matching against the tool resolution table from tool-exec.yaml.

    Zone-based security policies:
    - Zone 1: Audit/analysis, no engagement required
    - Zone 2: Active reconnaissance, engagement required
    - Zone 3: Exploitation, engagement + per-operation approval required
    """

    FAMILY_NAME = "rainbow"

    # Zone-to-security-policy mapping
    _ZONE_POLICIES: dict[str, dict[str, Any]] = {
        "1": {
            "requires_engagement": False,
            "requires_approval": False,
            "credential_filter_enabled": True,
            "container_required": False,
            "network_access": "none",
        },
        "2": {
            "requires_engagement": True,
            "requires_approval": False,
            "credential_filter_enabled": True,
            "container_required": False,
            "network_access": "restricted",
        },
        "3": {
            "requires_engagement": True,
            "requires_approval": True,
            "credential_filter_enabled": True,
            "container_required": True,
            "network_access": "full",
        },
    }

    def __init__(self, config_path: str | None = None) -> None:
        """Initialize the resolver, optionally loading a config file.

        Args:
            config_path: Path to tool-exec.yaml. If None, the resolver
                is created without loading a configuration (useful for
                testing or deferred loading).
        """
        self._entries: list[dict[str, Any]] = []
        self._config: dict[str, Any] = {}
        if config_path is not None:
            self._config = self.load_config(config_path)
            self._entries = self._config.get("tool_resolution", [])

    def can_resolve(self, tool_command: str) -> bool:
        """Check whether the rainbow family can resolve this tool command.

        Args:
            tool_command: The tool command to check.

        Returns:
            True if the command matches any prefix in the resolution table.
        """
        return self._find_entry(tool_command) is not None

    def resolve(self, tool_command: str) -> ToolResolutionEntry:
        """Resolve a tool command to its execution metadata.

        Uses longest-prefix matching: if the tool command starts with a
        known prefix, or if a wildcard prefix (ending in '-*') matches
        the tool command's base, the entry is returned.

        Args:
            tool_command: The tool command to resolve.

        Returns:
            ToolResolutionEntry with execution metadata.

        Raises:
            NotFoundError: If the tool command cannot be resolved.
        """
        entry = self._find_entry(tool_command)
        if entry is None:
            raise NotFoundError(
                entity_type="RainbowTool",
                entity_id=tool_command,
            )

        zone_num = str(entry.get("zone", "1"))
        return ToolResolutionEntry(
            tool_name=tool_command,
            binary_path=None,  # Rainbow tools are container-first
            container_service=entry.get("service"),
            default_mode="container",
            supported_modes=["local", "container"],
            zone=f"Zone {zone_num}",
            family=self.FAMILY_NAME,
            compose_file=entry.get("compose_file"),
            sub_skill=entry.get("sub_skill"),
        )

    def security_policy(self, tool_command: str) -> SecurityPolicy:
        """Get the security policy for a tool command.

        Maps the tool's zone classification to a SecurityPolicy with
        appropriate engagement, approval, container, and network constraints.

        Args:
            tool_command: The tool command to look up.

        Returns:
            SecurityPolicy with zone-appropriate constraints.

        Raises:
            NotFoundError: If the tool command cannot be resolved.
        """
        entry = self._find_entry(tool_command)
        if entry is None:
            raise NotFoundError(
                entity_type="RainbowTool",
                entity_id=tool_command,
            )

        zone_num = str(entry.get("zone", "1"))
        policy_defaults = self._ZONE_POLICIES.get(zone_num, self._ZONE_POLICIES["1"])

        return SecurityPolicy(
            requires_engagement=policy_defaults["requires_engagement"],
            requires_approval=policy_defaults["requires_approval"],
            credential_filter_enabled=policy_defaults["credential_filter_enabled"],
            credential_filter_patterns=[],
            container_required=policy_defaults["container_required"],
            network_access=policy_defaults["network_access"],
            redacted_env_vars=[
                "AWS_SECRET_ACCESS_KEY",
                "AWS_SESSION_TOKEN",
                "GITHUB_TOKEN",
                "SNYK_TOKEN",
            ],
            family_zone_label=f"Zone {zone_num}",
        )

    def load_config(self, config_path: str) -> dict:
        """Load and parse the rainbow tool-exec.yaml configuration.

        Args:
            config_path: Path to the YAML configuration file.

        Returns:
            Parsed configuration dictionary.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            ValueError: If the YAML is malformed or missing required keys.
        """
        path = Path(config_path)
        if not path.exists():
            msg = f"Rainbow config file not found: {config_path}"
            raise FileNotFoundError(msg)

        with open(path, encoding="utf-8") as f:
            config = yaml.safe_load(f)

        if not isinstance(config, dict):
            msg = f"Rainbow config must be a YAML mapping, got: {type(config).__name__}"
            raise ValueError(msg)

        return config

    def _find_entry(self, tool_command: str) -> dict[str, Any] | None:
        """Find the best-matching entry for a tool command.

        Implements longest-prefix matching:
        1. Exact prefix match (e.g., 'nuclei' matches prefix 'nuclei')
        2. Wildcard match (e.g., 'impacket-GetNPUsers' matches 'impacket-*')
        3. Starts-with match (e.g., 'frida-trace' matches prefix 'frida-trace',
           then falls back to 'frida')

        Longer prefixes take precedence over shorter ones.

        Args:
            tool_command: The tool command to match.

        Returns:
            The matching entry dictionary, or None if no match.
        """
        best_match: dict[str, Any] | None = None
        best_length = -1

        for entry in self._entries:
            prefix = entry.get("prefix", "")

            if prefix.endswith("-*"):
                # Wildcard: match base prefix before the -*
                base = prefix[:-2]  # Remove '-*'
                if tool_command == base or tool_command.startswith(base + "-"):
                    if len(base) > best_length:
                        best_match = entry
                        best_length = len(base)
            else:
                # Exact or starts-with match
                if tool_command == prefix:
                    if len(prefix) > best_length:
                        best_match = entry
                        best_length = len(prefix)
                elif tool_command.startswith(prefix + "-"):
                    if len(prefix) > best_length:
                        best_match = entry
                        best_length = len(prefix)

        return best_match
