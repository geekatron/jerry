# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""AutoProvisionHandler — orchestrates the full proxy node provisioning workflow.

Pipeline stages (provision → ssh-wait → health → manifest):
    1. Provision VPS node via ProxyProvisionerPort
    2. Wait for SSH availability via SshReadinessPort
    3. Run pre-use health check via NodeHealthPort
    4. Write node to pool manifest via ManifestWriterPort

Addresses TASK-023-014 (proxy provisioning automation) and AUTO-001 through
AUTO-006 requirements from the OPSEC proxy requirements document.

Design constraints:
    H-07: Application layer — imports domain ports only, no direct infrastructure.
    H-10: One public class per file.
    H-11: All public methods have type annotations.
    TASK-023-014: Proxy provisioning automation.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.application.handlers.manifest_writer_port import ManifestWriterPort
    from src.proxy_infra.application.handlers.node_health_port import NodeHealthPort
    from src.proxy_infra.application.handlers.ssh_readiness_port import SshReadinessPort
    from src.proxy_infra.domain.ports.proxy_provisioner_port import ProxyProvisionerPort
    from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode

logger = logging.getLogger(__name__)


from src.proxy_infra.application.handlers.provision_result import ProvisionResult  # noqa: E402


class AutoProvisionHandler:
    """Orchestrates the full proxy node provisioning pipeline.

    Pipeline stages:
        1. provision  — cloud API call via ProxyProvisionerPort
        2. ssh_wait   — SSH readiness gate via SshReadinessPort
        3. health     — pre-use connectivity check via NodeHealthPort
        4. manifest   — write to pool manifest via ManifestWriterPort

    Each stage must pass before the next begins. A failure returns a
    ProvisionResult identifying the failing stage so callers can decide
    whether to retry or alert the operator.

    Args:
        provisioner: Port for cloud VPS provisioning.
        ssh_readiness: Port for SSH availability polling.
        health_checker: Port for pre-use health gate.
        manifest_writer: Port for pool manifest persistence.
        ssh_timeout_seconds: SSH polling timeout (default 120s).
    """

    def __init__(
        self,
        provisioner: ProxyProvisionerPort,
        ssh_readiness: SshReadinessPort,
        health_checker: NodeHealthPort,
        manifest_writer: ManifestWriterPort,
        ssh_timeout_seconds: int = 120,
    ) -> None:
        """Initialise AutoProvisionHandler with all required ports.

        Args:
            provisioner: Cloud provisioning port.
            ssh_readiness: SSH availability polling port.
            health_checker: Pre-use health gate port.
            manifest_writer: Pool manifest writer port.
            ssh_timeout_seconds: Max seconds to wait for SSH on new node.
        """
        self._provisioner = provisioner
        self._ssh_readiness = ssh_readiness
        self._health_checker = health_checker
        self._manifest_writer = manifest_writer
        self._ssh_timeout_seconds = ssh_timeout_seconds

    def handle(self, config: ProvisionConfig) -> ProvisionResult:
        """Execute the full provision → ssh-wait → health → manifest pipeline.

        Args:
            config: Provisioning configuration (provider, region, engagement_id, etc.).

        Returns:
            ProvisionResult with success=True and the node when all stages pass,
            or success=False with stage_failed identifying the first failing stage.
        """
        # Stage 1: Provision
        logger.info(
            "Stage 1/4 — provisioning node: provider=%s region=%s engagement=%s",
            config.provider,
            config.region,
            config.engagement_id,
        )
        nodes = self._provisioner.provision(config)
        if not nodes:
            return ProvisionResult(
                success=False,
                node=None,
                stage_failed="provision",
                error="Provisioner returned empty node list",
            )
        node = nodes[0]
        logger.info("Stage 1/4 complete — ip=%s id=%s", node.ip, node.id)

        # Stage 2: SSH readiness gate
        logger.info(
            "Stage 2/4 — SSH readiness gate: ip=%s timeout=%ds",
            node.ip,
            self._ssh_timeout_seconds,
        )
        if not self._ssh_readiness.wait_for_ssh(node.ip, self._ssh_timeout_seconds):
            return ProvisionResult(
                success=False,
                node=node,
                stage_failed="ssh_wait",
                error=f"SSH not available on {node.ip} within {self._ssh_timeout_seconds}s",
            )

        # Stage 3: Pre-use health check
        logger.info("Stage 3/4 — pre-use health check: %s", node.ip)
        if not self._health_checker.check(node):
            return ProvisionResult(
                success=False,
                node=node,
                stage_failed="health",
                error=f"Pre-use health check failed for node {node.id} ({node.ip})",
            )

        # Stage 4: Write manifest
        logger.info("Stage 4/4 — writing node to pool manifest: %s", node.id)
        self._manifest_writer.write(node)

        logger.info(
            "AutoProvision pipeline complete — node %s (%s) ready", node.id, node.ip
        )
        return ProvisionResult(success=True, node=node)
