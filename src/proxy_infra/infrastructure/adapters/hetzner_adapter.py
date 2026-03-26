# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""HetznerProvisionerAdapter — ProxyProvisionerPort implementation for Hetzner Cloud.

Uses the `hcloud` SDK to manage server instances, SSH keys, and firewall rules.

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


class HetznerProvisionerAdapter(ProxyProvisionerPort):
    """ProxyProvisionerPort implementation for Hetzner Cloud via the hcloud SDK.

    Manages Server lifecycle, SSH key upload/removal, and Firewall rule
    configuration.

    Service name in providers.yaml: "hetzner"

    References:
        - ADR-PROJ023-008: Multi-provider adapter design
    """

    def __init__(self, api_key: str) -> None:
        """Initialize the Hetzner adapter with an API key.

        Args:
            api_key: Hetzner Cloud API token. Must not be empty.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def provision(self, config: ProvisionConfig) -> list[ProxyNode]:
        """Provision Servers on Hetzner Cloud.

        Args:
            config: Provisioning parameters.

        Returns:
            List of provisioned ProxyNode instances.

        Raises:
            ProvisionError: If server creation fails.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def destroy(self, node_ids: list[str]) -> DestroyResult:
        """Destroy Servers by provider ID.

        Args:
            node_ids: Hetzner Server IDs to destroy.

        Returns:
            DestroyResult with per-node success/failure details.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def health_check(self, node_id: str) -> HealthStatus:
        """Check health via Hetzner API and network probes.

        Args:
            node_id: Hetzner Server ID.

        Returns:
            HealthStatus with reachability and service status.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def list_nodes(self) -> list[ProxyNode]:
        """List all Servers managed by this adapter.

        Returns:
            List of all ProxyNode instances from this provider.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def upload_ssh_key(self, public_key: str) -> str:
        """Upload an SSH public key to Hetzner Cloud.

        Args:
            public_key: OpenSSH public key string.

        Returns:
            Hetzner-assigned key ID.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def remove_ssh_key(self, key_id: str) -> None:
        """Remove an SSH key from Hetzner Cloud.

        Args:
            key_id: Hetzner-assigned key ID.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def configure_firewall(self, node_id: str, rules: list[FirewallRule]) -> None:
        """Apply Firewall rules to a Hetzner Server.

        Args:
            node_id: Hetzner Server ID.
            rules: Firewall rules to apply.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")
