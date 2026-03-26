# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""VultrProvisionerAdapter — ProxyProvisionerPort implementation for Vultr.

Uses the `vultr-python` SDK to manage VPS instances, SSH keys, and firewall groups.

References:
    - ADR-PROJ023-008: Direct API over Terraform decision
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.proxy_infra.domain.ports.proxy_provisioner_port import ProxyProvisionerPort

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult
    from src.proxy_infra.domain.value_objects.firewall_rule import FirewallRule
    from src.proxy_infra.domain.value_objects.health_status import HealthStatus
    from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode


class VultrProvisionerAdapter(ProxyProvisionerPort):
    """ProxyProvisionerPort implementation for Vultr via the vultr-python SDK.

    Manages VPS instance lifecycle, SSH key upload/removal,
    and firewall group rule configuration.

    Service name in providers.yaml: "vultr"

    References:
        - ADR-PROJ023-008: Multi-provider adapter design
    """

    def __init__(self, api_key: str) -> None:
        """Initialize the Vultr adapter with an API key.

        Args:
            api_key: Vultr personal access token. Must not be empty.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def provision(self, config: ProvisionConfig) -> list[ProxyNode]:
        """Provision VPS instances on Vultr.

        Args:
            config: Provisioning parameters.

        Returns:
            List of provisioned ProxyNode instances.

        Raises:
            ProvisionError: If VPS creation fails.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def destroy(self, node_ids: list[str]) -> DestroyResult:
        """Destroy VPS instances by provider ID.

        Args:
            node_ids: Vultr instance IDs to destroy.

        Returns:
            DestroyResult with per-node success/failure details.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def health_check(self, node_id: str) -> HealthStatus:
        """Check health via Vultr API and network probes.

        Args:
            node_id: Vultr instance ID.

        Returns:
            HealthStatus with reachability and service status.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def list_nodes(self) -> list[ProxyNode]:
        """List all VPS instances managed by this adapter.

        Returns:
            List of all ProxyNode instances from this provider.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def upload_ssh_key(self, public_key: str) -> str:
        """Upload an SSH public key to Vultr.

        Args:
            public_key: OpenSSH public key string.

        Returns:
            Vultr-assigned key ID.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def remove_ssh_key(self, key_id: str) -> None:
        """Remove an SSH key from Vultr.

        Args:
            key_id: Vultr-assigned key ID.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def configure_firewall(self, node_id: str, rules: list[FirewallRule]) -> None:
        """Apply firewall group rules to a VPS instance.

        Args:
            node_id: Vultr instance ID.
            rules: Firewall rules to apply.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")
