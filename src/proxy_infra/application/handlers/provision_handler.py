# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ProvisionHandler — application handler for ProvisionNodesCommand.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.application.commands.provision_nodes_command import ProvisionNodesCommand
    from src.proxy_infra.domain.services.proxy_pool_service import ProxyPoolService
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode


class ProvisionHandler:
    """Handles ProvisionNodesCommand by delegating to ProxyPoolService.

    Validates the command, builds a ProvisionConfig, and invokes the
    domain service. Zone 3 approval gate is enforced at the CLI layer
    before this handler is called.

    References:
        - ADR-PROJ023-008: Application handler pattern
    """

    def __init__(self, pool_service: ProxyPoolService) -> None:
        """Initialize ProvisionHandler with the domain service.

        Args:
            pool_service: Proxy pool domain service.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def handle(self, command: ProvisionNodesCommand) -> list[ProxyNode]:
        """Execute a provision command.

        Args:
            command: The provision command containing provider, count, regions,
                role, and engagement_id.

        Returns:
            List of newly provisioned ProxyNode instances.

        Raises:
            EngagementScopeError: If engagement_id is missing (PI-002).
            PoolLimitExceededError: If provision would exceed max_nodes (PI-001).
            ProvisionError: If the cloud provider returns an error.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")
