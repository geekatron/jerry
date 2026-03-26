# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""EngagePipelineOrchestrator — full engage-to-route pipeline.

Wires the complete hands-free pipeline:
  config → provision N nodes → ssh_wait → credential_inject per node →
  health check → pool manifest → BPF bypass map → Docker Compose sidecar

Produces:
  - Provisioned and injected proxy nodes
  - SOCKS5 credential files in the engagement credential directory
  - BPF bypass map populated with proxy IPs
  - Docker Compose sidecar file at {engagement_dir}/docker-compose.socks.yaml

Design constraints:
    H-07: Application layer — imports domain ports only.
    H-10: One public class per file.
    H-11: All public methods have type annotations.

References:
    - TASK-023-059: Pool manifest → BPF bypass map + Docker Compose
    - TASK-023-060: E2E integration test
    - FEAT-023-004: Hands-Free Engagement Pipeline Automation
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.application.handlers.manifest_writer_port import ManifestWriterPort
    from src.proxy_infra.application.handlers.node_health_port import NodeHealthPort
    from src.proxy_infra.application.handlers.ssh_credential_injection_handler import SshCredentialInjectionHandler
    from src.proxy_infra.application.handlers.ssh_readiness_port import SshReadinessPort
    from src.proxy_infra.domain.ports.proxy_provisioner_port import ProxyProvisionerPort
    from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class EngagePipelineResult:
    """Result of the full engage pipeline.

    Attributes:
        success: True when all nodes provisioned, injected, and compose generated.
        nodes: List of provisioned ProxyNode instances.
        compose_path: Path to generated Docker Compose file, or None on failure.
        error: Human-readable error message if success is False.
    """

    success: bool
    nodes: list | None = None
    compose_path: str | None = None
    error: str | None = None


class EngagePipelineOrchestrator:
    """Orchestrates the full engage-to-route pipeline.

    Args:
        provisioner: Cloud provisioning port.
        ssh_readiness: SSH readiness polling port.
        credential_injector: SSH credential injection handler.
        health_checker: Pre-use health gate port.
        manifest_writer: Pool manifest writer port.
        bpf_port: BPF bypass map update port.
        engagement_dir: Directory for engagement artifacts.
    """

    def __init__(
        self,
        provisioner: ProxyProvisionerPort,
        ssh_readiness: SshReadinessPort,
        credential_injector: SshCredentialInjectionHandler,
        health_checker: NodeHealthPort,
        manifest_writer: ManifestWriterPort,
        bpf_port: object,
        engagement_dir: Path,
    ) -> None:
        """Initialise the pipeline orchestrator.

        Args:
            provisioner: Cloud provisioning port.
            ssh_readiness: SSH readiness polling port.
            credential_injector: SSH credential injection handler.
            health_checker: Pre-use health gate port.
            manifest_writer: Pool manifest writer port.
            bpf_port: Object with update_bypass_ips(ips: list[str]) method.
            engagement_dir: Base directory for engagement artifacts.
        """
        self._provisioner = provisioner
        self._ssh_readiness = ssh_readiness
        self._credential_injector = credential_injector
        self._health_checker = health_checker
        self._manifest_writer = manifest_writer
        self._bpf_port = bpf_port
        self._engagement_dir = engagement_dir

    def orchestrate(
        self,
        config: ProvisionConfig,
        private_key_path: Path,
    ) -> EngagePipelineResult:
        """Execute the full engage pipeline.

        Args:
            config: Provisioning configuration.
            private_key_path: Path to the engagement SSH private key.

        Returns:
            EngagePipelineResult with success=True and compose path when complete.
        """
        # Stage 1: Provision
        logger.info("Engage pipeline — provisioning %d nodes", config.count)
        nodes = self._provisioner.provision(config)
        if not nodes:
            return EngagePipelineResult(
                success=False,
                error="Provisioner returned empty node list",
            )

        # Stage 2-5: For each node: ssh_wait → inject → health → manifest
        cred_dir = self._engagement_dir / "credentials"
        cred_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(cred_dir, 0o700)

        injected_nodes: list[ProxyNode] = []
        for node in nodes:
            # SSH wait
            if not self._ssh_readiness.wait_for_ssh(node.ip, 180):
                logger.warning("SSH timeout for node %s — skipping", node.id)
                continue

            # Credential injection
            inject_result = self._credential_injector.inject(
                node=node, private_key_path=private_key_path,
            )
            if not inject_result.success:
                logger.warning("Injection failed for node %s — skipping", node.id)
                continue

            # Health check
            if not self._health_checker.check(node):
                logger.warning("Health check failed for node %s — skipping", node.id)
                continue

            # Manifest update
            self._manifest_writer.write(node)

            # Write credential return file
            cred_file = cred_dir / f"socks5_creds_{node.id}"
            cred_file.write_text(
                f"{inject_result.username}:{inject_result.password}",
                encoding="utf-8",
            )
            os.chmod(cred_file, 0o600)

            injected_nodes.append(node)

        if not injected_nodes:
            return EngagePipelineResult(
                success=False,
                nodes=[],
                error="No nodes successfully injected",
            )

        # Stage 6: Update BPF bypass map with all proxy IPs
        proxy_ips = [n.ip for n in injected_nodes]
        logger.info("Updating BPF bypass map with %d proxy IPs", len(proxy_ips))
        self._bpf_port.update_bypass_ips(proxy_ips)

        # Stage 7: Generate Docker Compose sidecar config
        compose_path = self._engagement_dir / "docker-compose.socks.yaml"
        compose_content = self._generate_compose(injected_nodes, config.socks_port)
        compose_path.write_text(compose_content, encoding="utf-8")
        logger.info("Docker Compose sidecar written to %s", compose_path)

        return EngagePipelineResult(
            success=True,
            nodes=injected_nodes,
            compose_path=str(compose_path),
        )

    @staticmethod
    def _generate_compose(nodes: list[ProxyNode], socks_port: int) -> str:
        """Generate a Docker Compose YAML for the socks-bridge sidecar.

        Args:
            nodes: List of injected proxy nodes.
            socks_port: SOCKS5 port on each node.

        Returns:
            Docker Compose YAML string.
        """
        # Build SOCKS proxy pool as comma-separated list
        pool_entries = [f"{n.ip}:{socks_port}" for n in nodes]
        pool_str = ",".join(pool_entries)

        return f"""# Generated by EngagePipelineOrchestrator
# Proxy pool: {len(nodes)} nodes
# Usage: docker compose -f docker-compose.socks.yaml --profile socks up -d

services:
  socks-bridge:
    image: ghcr.io/geekatron/socks-bridge:latest
    profiles: ["socks"]
    environment:
      SOCKS_PROXY_POOL: "{pool_str}"
      SOCKS_PROXY_HOST: "{nodes[0].ip}"
      SOCKS_PROXY_PORT: "{socks_port}"
      SOCKS_LB_STRATEGY: "round-robin"
      SOCKS_FAIL_CLOSED: "true"
    networks:
      - proxy-egress
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:8080/health || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3

networks:
  proxy-egress:
    driver: bridge
"""
