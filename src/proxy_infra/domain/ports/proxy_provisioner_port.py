# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Port interface for cloud provider proxy node provisioning.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult
    from src.proxy_infra.domain.value_objects.firewall_rule import FirewallRule
    from src.proxy_infra.domain.value_objects.health_status import HealthStatus
    from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode


class ProxyProvisionerPort(ABC):
    """Port interface for cloud provider proxy node provisioning.

    Each cloud provider adapter implements this abstract class to provide
    vendor-specific provisioning, lifecycle management, and configuration.

    The port defines WHAT operations the domain needs; adapters define HOW
    each provider implements them.

    References:
        - ADR-PROJ023-008: Hexagonal architecture for proxy_infra bounded context
    """

    @abstractmethod
    def provision(self, config: ProvisionConfig) -> list[ProxyNode]:
        """Provision one or more proxy nodes.

        Creates cloud instances, uploads SSH keys, configures firewalls,
        and installs SOCKS5 proxy software.

        Args:
            config: Provisioning parameters (count, region, role, type).

        Returns:
            List of provisioned ProxyNode instances.

        Raises:
            ProvisionError: If provisioning fails for any node.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    @abstractmethod
    def destroy(self, node_ids: list[str]) -> DestroyResult:
        """Destroy one or more proxy nodes.

        Removes cloud instances and cleans up associated resources
        (SSH keys, firewall rules, DNS records).

        Args:
            node_ids: Provider-assigned node identifiers to destroy.

        Returns:
            DestroyResult with success/failure details per node.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    @abstractmethod
    def health_check(self, node_id: str) -> HealthStatus:
        """Check the health of a specific proxy node.

        Verifies the node is reachable, the SOCKS5 port is listening,
        and the SSH tunnel (if applicable) is functional.

        Args:
            node_id: Provider-assigned node identifier.

        Returns:
            HealthStatus with reachability and service status.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    @abstractmethod
    def list_nodes(self) -> list[ProxyNode]:
        """List all nodes managed by this provider.

        Returns:
            List of all ProxyNode instances from this provider.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    @abstractmethod
    def list_instances(self, engagement_tag: str) -> list[ProxyNode]:
        """List instances filtered by engagement tag.

        Args:
            engagement_tag: Tag to filter by (ISOLATION-002).

        Returns:
            List of ProxyNode instances matching the tag.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    @abstractmethod
    def upload_ssh_key(self, public_key: str) -> str:
        """Upload an SSH public key to the provider.

        Args:
            public_key: OpenSSH public key string.

        Returns:
            Provider-assigned key identifier.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    @abstractmethod
    def remove_ssh_key(self, key_id: str) -> None:
        """Remove an SSH key from the provider.

        Args:
            key_id: Provider-assigned key identifier.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    @abstractmethod
    def configure_firewall(self, node_id: str, rules: list[FirewallRule]) -> None:
        """Apply firewall rules to a node.

        Replaces the current firewall configuration with the provided rules.

        Args:
            node_id: Provider-assigned node identifier.
            rules: Firewall rules to apply.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")
