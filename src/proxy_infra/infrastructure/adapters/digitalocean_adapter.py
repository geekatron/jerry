# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""DigitalOceanProvisionerAdapter — ProxyProvisionerPort implementation for DigitalOcean.

Uses the `pydo` SDK to manage Droplets, SSH keys, and firewall rules.

References:
    - ADR-PROJ023-008: Direct API over Terraform decision
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.proxy_infra.domain.ports.proxy_provisioner_port import ProxyProvisionerPort
from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.firewall_rule import FirewallRule
    from src.proxy_infra.domain.value_objects.health_status import HealthStatus
    from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
    from src.proxy_infra.infrastructure.persistence.audit_log_store import AuditLogStore


class DigitalOceanProvisionerAdapter(ProxyProvisionerPort):
    """ProxyProvisionerPort implementation for DigitalOcean via the pydo SDK.

    Manages Droplet lifecycle (create, delete, status), SSH key upload/removal,
    and Cloud Firewall rule configuration.

    Service name in providers.yaml: "digitalocean"

    References:
        - ADR-PROJ023-008: DigitalOcean adapter design
    """

    def __init__(
        self,
        client: Any,
        audit_store: Any,
        preflight_checker: Any | None = None,
        api_key: str = "",
    ) -> None:
        """Initialize the DigitalOcean adapter.

        Args:
            client: pydo Client instance configured with the DigitalOcean API key.
            audit_store: AuditLogStore for recording all provisioner operations.
            preflight_checker: Optional ApiKeyPreflightChecker.  When provided,
                ``run()`` is called before every mutating operation (TASK-023-048).
            api_key: Deprecated; kept for backwards compatibility.  Prefer
                constructing the pydo Client externally and passing via ``client``.
        """
        self._client = client
        self._audit_store = audit_store
        self._preflight = preflight_checker

    def provision(self, config: ProvisionConfig) -> list[ProxyNode]:
        """Provision Droplets on DigitalOcean.

        Runs the API key pre-flight check before making any Droplet create calls.

        Args:
            config: Provisioning parameters.

        Returns:
            List of provisioned ProxyNode instances.

        Raises:
            ApiKeyExpiredError: If the pre-flight check finds the key expired.
            ProvisionError: If Droplet creation fails.
        """
        if self._preflight is not None:
            self._preflight.run()
        raise NotImplementedError("TASK-023-027: full provision not yet implemented")

    def destroy(self, node_ids: list[str]) -> DestroyResult:
        """Destroy Droplets by provider ID.

        Runs the API key pre-flight check before making any Droplet delete calls.

        Args:
            node_ids: DigitalOcean Droplet IDs to destroy.

        Returns:
            DestroyResult with per-node success/failure details.

        Raises:
            ApiKeyExpiredError: If the pre-flight check finds the key expired.
        """
        if self._preflight is not None:
            self._preflight.run()
        raise NotImplementedError("TASK-023-027: full destroy not yet implemented")

    def health_check(self, node_id: str) -> HealthStatus:
        """Check health via DigitalOcean API and network probes.

        Args:
            node_id: DigitalOcean Droplet ID.

        Returns:
            HealthStatus with reachability and service status.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def list_nodes(self) -> list[ProxyNode]:
        """List all Droplets managed by this adapter.

        Returns:
            List of all ProxyNode instances from this provider.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def list_instances(self, engagement_tag: str) -> list[ProxyNode]:
        """List Droplets filtered by engagement tag.

        Args:
            engagement_tag: Engagement tag to filter by (ISOLATION-001).

        Returns:
            List of ProxyNode instances matching the tag.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def upload_ssh_key(self, public_key: str) -> str:
        """Upload an SSH public key to DigitalOcean.

        Args:
            public_key: OpenSSH public key string.

        Returns:
            DigitalOcean-assigned key ID.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def remove_ssh_key(self, key_id: str) -> None:
        """Remove an SSH key from DigitalOcean.

        Args:
            key_id: DigitalOcean-assigned key ID.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def configure_firewall(self, node_id: str, rules: list[FirewallRule]) -> None:
        """Apply Cloud Firewall rules to a Droplet.

        Args:
            node_id: DigitalOcean Droplet ID.
            rules: Firewall rules to apply.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")
