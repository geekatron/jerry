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
    from src.proxy_infra.domain.services.proxy_pool_service import ProxyPoolService
    from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult


class DestroyHandler:
    """Handles DestroyNodesCommand by delegating to ProxyPoolService.

    Zone 3 approval gate (including optional --force bypass) is enforced
    at the CLI layer before this handler is called.

    References:
        - ADR-PROJ023-008: Application handler pattern
    """

    def __init__(self, pool_service: ProxyPoolService) -> None:
        """Initialize DestroyHandler with the domain service.

        Args:
            pool_service: Proxy pool domain service.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def handle(self, command: DestroyNodesCommand) -> DestroyResult:
        """Execute a destroy command.

        Args:
            command: The destroy command containing engagement_id and optional
                list of specific node IDs to destroy.

        Returns:
            DestroyResult with success/failure details per node.

        Raises:
            EngagementScopeError: If engagement_id is missing (PI-002).
            TeardownError: If cleanup fails for one or more nodes.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")
