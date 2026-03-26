# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""DestroyHandler — application handler for DestroyNodesCommand.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.application.commands.destroy_nodes_command import DestroyNodesCommand
    from src.proxy_infra.domain.ports.proxy_provisioner_port import ProxyProvisionerPort
    from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult


class DestroyHandler:
    """Handles DestroyNodesCommand by delegating to the provisioner port.

    Zone 3 approval gate (including optional --force bypass) is enforced
    at the CLI layer before this handler is called.

    The handler does NOT import infrastructure adapters — it operates only
    through the ProxyProvisionerPort interface (H-07 application-layer rule).

    References:
        - ADR-PROJ023-008: Application handler pattern
    """

    def __init__(self, provisioner: ProxyProvisionerPort) -> None:
        """Initialize DestroyHandler with the provisioner port.

        Args:
            provisioner: ProxyProvisionerPort implementation that performs
                the actual cloud API calls.
        """
        self._provisioner = provisioner

    def handle(self, command: DestroyNodesCommand) -> DestroyResult:
        """Execute a destroy command.

        Delegates ``command.node_ids`` directly to
        ``self._provisioner.destroy()``.

        Args:
            command: The destroy command containing engagement_id and optional
                list of specific node IDs to destroy.

        Returns:
            DestroyResult with success/failure details per node.

        Raises:
            EngagementScopeError: If engagement_id is missing (PI-002).
            TeardownError: If cleanup fails for one or more nodes.
        """
        return self._provisioner.destroy(list(command.node_ids))
