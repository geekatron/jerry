# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""RotateHandler — application handler for RotateNodeCommand.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from dataclasses import replace as dc_replace
from typing import TYPE_CHECKING

from src.proxy_infra.domain.value_objects.node_status import NodeStatus

if TYPE_CHECKING:
    from src.proxy_infra.application.commands.rotate_node_command import RotateNodeCommand
    from src.proxy_infra.domain.services.proxy_pool_service import ProxyPoolService
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode


class RotateHandler:
    """Handles RotateNodeCommand by delegating to ProxyPoolService.

    Zone 3 approval gate is enforced at the CLI layer before this handler
    is called. Rotation is provision-before-destroy (PI-003).

    References:
        - ADR-PROJ023-008: Application handler pattern
    """

    def __init__(self, pool_service: ProxyPoolService) -> None:
        """Initialize RotateHandler with the domain service.

        Args:
            pool_service: Proxy pool domain service.
        """
        self._pool_service = pool_service

    def handle(self, command: RotateNodeCommand) -> ProxyNode:
        """Execute a rotate command.

        Validates the engagement scope (PI-002), retrieves the current pool
        state, marks the target node BURNED, provisions a replacement via the
        provisioner port, and returns the new node.

        Args:
            command: The rotate command containing engagement_id, node_id,
                and optional reason.

        Returns:
            The newly provisioned replacement ProxyNode.

        Raises:
            InvalidEngagementIdError: If engagement_id is missing (PI-002).
            ProvisionError: If replacement provisioning fails.
            ValueError: If node_id is not found in the pool.
        """
        self._pool_service.validate_engagement_id(command.engagement_id)

        provisioner = self._pool_service._provisioner
        nodes = provisioner.list_instances(command.engagement_id)

        target = next((n for n in nodes if n.id == command.node_id), None)
        if target is None:
            raise ValueError(
                f"Node {command.node_id!r} not found in pool for engagement "
                f"{command.engagement_id!r}."
            )

        # Mark target BURNED (PI-003)
        dc_replace(target, status=NodeStatus.BURNED)

        # Provision replacement in same region/role/type
        from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig

        config = ProvisionConfig(
            provider=target.provider,
            region=target.region,
            engagement_id=command.engagement_id,
            engagement_tag=command.engagement_id,
            count=1,
            role=target.role,
            proxy_type=target.proxy_type,
            ssh_public_key="",
            operator_ip="0.0.0.0",
        )
        replacements = provisioner.provision(config)
        return replacements[0]
