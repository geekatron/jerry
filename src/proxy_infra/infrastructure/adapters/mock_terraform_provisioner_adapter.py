# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""MockTerraformProvisionerAdapter — CI-safe ProxyProvisionerPort implementation.

Provides in-memory mock provisioning for E2E tests that run without real cloud
infrastructure. Returns deterministic localhost ProxyNode objects so the
engagement lifecycle pipeline can execute end-to-end in CI without DigitalOcean
credentials or Terraform state.

Mode selection:
    JERRY_E2E_TERRAFORM_MODE=mock  -> always use mock
    JERRY_E2E_TERRAFORM_MODE=real  -> always use real (requires DIGITALOCEAN_TOKEN)
    (unset/auto)                   -> mock when DIGITALOCEAN_TOKEN absent, real when present

References:
    - EN-023-006: CI-Safe Terraform Mode
    - FEAT-023-014: Real E2E Engagement Lifecycle
"""

from __future__ import annotations

import logging
import os
from datetime import UTC, datetime

from src.proxy_infra.domain.ports.proxy_provisioner_port import ProxyProvisionerPort
from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult
from src.proxy_infra.domain.value_objects.firewall_rule import FirewallRule
from src.proxy_infra.domain.value_objects.health_status import HealthStatus
from src.proxy_infra.domain.value_objects.node_status import NodeStatus
from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode

logger = logging.getLogger(__name__)

#: Maximum droplets per engagement (cost guardrail).
_MAX_DROPLETS_PER_ENGAGEMENT: int = 2


def select_provisioner_mode() -> str:
    """Determine provisioner mode from environment variables.

    Returns:
        "mock" or "real" based on JERRY_E2E_TERRAFORM_MODE and DIGITALOCEAN_TOKEN.

    Raises:
        ValueError: If mode is explicitly "real" but DIGITALOCEAN_TOKEN is absent.
    """
    mode = os.environ.get("JERRY_E2E_TERRAFORM_MODE", "").lower()
    has_token = bool(os.environ.get("DIGITALOCEAN_TOKEN", ""))

    if mode == "mock":
        return "mock"
    if mode == "real":
        if not has_token:
            msg = (
                "JERRY_E2E_TERRAFORM_MODE=real requires DIGITALOCEAN_TOKEN env var. "
                "Use JERRY_E2E_TERRAFORM_MODE=mock for CI without credentials."
            )
            raise ValueError(msg)
        return "real"

    # Auto-detect: mock when no token, real when token present
    return "real" if has_token else "mock"


class MockTerraformProvisionerAdapter(ProxyProvisionerPort):
    """CI-safe mock implementation of ProxyProvisionerPort.

    All operations are in-memory. Provision returns localhost nodes.
    Destroy is a no-op that reports success. Health checks always pass.
    """

    def __init__(self) -> None:
        """Initialise with empty node registry."""
        self._nodes: list[ProxyNode] = []

    def provision(self, config: ProvisionConfig) -> list[ProxyNode]:
        """Return deterministic localhost ProxyNode objects.

        Args:
            config: Provisioning parameters.

        Returns:
            List of mock ProxyNode instances with ip=127.0.0.1.

        Raises:
            ValueError: If count exceeds cost guardrail (max 2).
        """
        if config.count > _MAX_DROPLETS_PER_ENGAGEMENT:
            msg = (
                f"Cost guardrail: max {_MAX_DROPLETS_PER_ENGAGEMENT} droplets per "
                f"engagement, requested {config.count}"
            )
            raise ValueError(msg)

        now = datetime.now(tz=UTC)
        nodes = []
        for i in range(config.count):
            node = ProxyNode(
                id=f"mock-{config.engagement_id}-{i}",
                provider="mock",
                ip="127.0.0.1",
                region=config.region,
                role=config.role,
                proxy_type=config.proxy_type,
                status=NodeStatus.READY,
                ssh_key_id=f"mock-key-{i}",
                created_at=now,
                engagement_id=config.engagement_id,
                socks_port=config.socks_port,
            )
            nodes.append(node)

        self._nodes.extend(nodes)
        logger.info(
            "Mock provisioner: created %d node(s) for %s",
            len(nodes),
            config.engagement_id,
        )
        return nodes

    def destroy(self, node_ids: list[str], engagement_id: str = "") -> DestroyResult:
        """Report all requested nodes as successfully destroyed.

        Args:
            node_ids: Node IDs to "destroy".
            engagement_id: Engagement scope (unused in mock).

        Returns:
            DestroyResult with all nodes in destroyed list.
        """
        self._nodes = [n for n in self._nodes if n.id not in node_ids]
        logger.info("Mock provisioner: destroyed %d node(s)", len(node_ids))
        return DestroyResult(destroyed=list(node_ids), failed=[])

    def health_check(self, node_id: str) -> HealthStatus:
        """Return healthy status for any node ID.

        Args:
            node_id: Node ID to check.

        Returns:
            HealthStatus with all indicators True.
        """
        return HealthStatus(
            node_id=node_id,
            reachable=True,
            socks_port_open=True,
            ssh_accessible=True,
            checked_at=datetime.now(tz=UTC),
        )

    def list_nodes(self) -> list[ProxyNode]:
        """Return all provisioned mock nodes.

        Returns:
            List of mock ProxyNode instances.
        """
        return list(self._nodes)

    def list_instances(self, engagement_tag: str) -> list[ProxyNode]:
        """Return mock nodes matching the engagement tag.

        Args:
            engagement_tag: Tag to filter by.

        Returns:
            Filtered list of ProxyNode instances.
        """
        return [n for n in self._nodes if f"jerry-e2e-{n.engagement_id}" == engagement_tag]

    def upload_ssh_key(self, public_key: str) -> str:
        """Return a mock SSH key ID.

        Args:
            public_key: SSH public key (unused in mock).

        Returns:
            Deterministic mock key ID.
        """
        return "mock-ssh-key-id"

    def remove_ssh_key(self, key_id: str) -> None:
        """No-op for mock adapter.

        Args:
            key_id: Key ID to remove (unused).
        """

    def configure_firewall(self, node_id: str, rules: list[FirewallRule]) -> None:
        """No-op for mock adapter.

        Args:
            node_id: Node ID (unused).
            rules: Firewall rules (unused).
        """
