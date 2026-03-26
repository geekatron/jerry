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
    from src.proxy_infra.domain.ports.proxy_provisioner_port import ProxyProvisionerPort
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode


class ProvisionHandler:
    """Handles ProvisionNodesCommand by delegating to the provisioner port.

    The application layer owns the translation from command object to port
    call.  Zone 3 approval gate is enforced at the CLI layer before this
    handler is called.

    The handler does NOT import infrastructure adapters — it operates only
    through the ProxyProvisionerPort interface (H-07 application-layer rule).

    References:
        - ADR-PROJ023-008: Application handler pattern
    """

    def __init__(self, provisioner: ProxyProvisionerPort) -> None:
        """Initialize ProvisionHandler with the provisioner port.

        Args:
            provisioner: ProxyProvisionerPort implementation that performs
                the actual cloud API calls.
        """
        self._provisioner = provisioner

    def handle(self, command: ProvisionNodesCommand) -> list[ProxyNode]:
        """Execute a provision command.

        Builds a minimal ProvisionConfig from the command's fields and
        delegates to ``self._provisioner.provision()``.

        For full ProvisionConfig parameters (ssh_public_key, operator_ip,
        image, size, socks_port) the handler uses safe defaults; callers that
        need custom values should construct and pass a ProvisionConfig directly
        via the CLI layer.

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
        from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
        from src.proxy_infra.domain.value_objects.proxy_type import ProxyType
        from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig

        region = command.regions[0] if command.regions else "nyc1"
        role = command.role if command.role is not None else ProxyRole.ACTIVE
        proxy_type = command.proxy_type if command.proxy_type is not None else ProxyType.DIRECT_SOCKS5

        config = ProvisionConfig(
            provider=command.provider,
            region=region,
            engagement_id=command.engagement_id,
            engagement_tag=command.engagement_id,
            count=command.count,
            role=role,
            proxy_type=proxy_type,
            ssh_public_key="",
            operator_ip="0.0.0.0",
        )
        return self._provisioner.provision(config)
