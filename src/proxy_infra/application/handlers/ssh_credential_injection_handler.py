# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""SshCredentialInjectionHandler — 7-step on-node credential injection.

Executes the post-boot credential injection sequence documented in
``CloudInitTemplateGenerator.get_post_boot_injection_steps()``:

  1. Poll SSH availability (via SshReadinessPort)
  2. Connect to node via SSH using engagement Ed25519 key
  3. Generate SOCKS5 credentials on-node (openssl rand)
  4. Write /etc/microsocks.env + chmod 0600
  5. Start microsocks service (systemctl start microsocks)
  6. Verify SOCKS5 connectivity
  7. Update pool manifest to READY status

Failure at any step halts the pipeline for that node and reports
which step failed via ``SshInjectionResult.stage_failed``.

Design constraints:
    H-07: Application layer — imports domain ports only, no direct subprocess.
    H-10: One public class per file.
    H-11: All public methods have type annotations.

References:
    - TASK-023-055: SSH credential injection handler
    - FEAT-023-004: Hands-Free Engagement Pipeline Automation
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.application.handlers.manifest_writer_port import ManifestWriterPort
    from src.proxy_infra.application.handlers.ssh_executor_port import SshExecutorPort
    from src.proxy_infra.application.handlers.ssh_readiness_port import SshReadinessPort
    from src.proxy_infra.application.handlers.socks_verifier_port import SocksVerifierPort
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode

logger = logging.getLogger(__name__)


from src.proxy_infra.application.handlers.ssh_injection_result import SshInjectionResult  # noqa: E402


class SshCredentialInjectionHandler:
    """Executes the 7-step credential injection sequence on a proxy node.

    Each step must succeed before the next proceeds. On failure, returns
    an ``SshInjectionResult`` identifying which step failed.

    Args:
        ssh_readiness: Port for SSH availability polling (step 1).
        ssh_executor: Port for remote command execution (steps 2-5).
        socks_verifier: Port for SOCKS5 connectivity verification (step 6).
        manifest_writer: Port for pool manifest update (step 7).
        ssh_timeout: SSH readiness timeout in seconds (default 180).
    """

    def __init__(
        self,
        ssh_readiness: SshReadinessPort,
        ssh_executor: SshExecutorPort,
        socks_verifier: SocksVerifierPort,
        manifest_writer: ManifestWriterPort,
        ssh_timeout: int = 180,
    ) -> None:
        """Initialise the injection handler with all required ports.

        Args:
            ssh_readiness: SSH availability polling port.
            ssh_executor: Remote command execution port.
            socks_verifier: SOCKS5 verification port.
            manifest_writer: Pool manifest writer port.
            ssh_timeout: Maximum seconds to wait for SSH.
        """
        self._ssh_readiness = ssh_readiness
        self._ssh_executor = ssh_executor
        self._socks_verifier = socks_verifier
        self._manifest_writer = manifest_writer
        self._ssh_timeout = ssh_timeout

    def inject(
        self,
        node: ProxyNode,
        private_key_path: Path,
    ) -> SshInjectionResult:
        """Execute the 7-step injection sequence on a single node.

        Args:
            node: The proxy node to inject credentials into.
            private_key_path: Path to the engagement SSH private key.

        Returns:
            SshInjectionResult with success=True when all steps complete,
            or success=False with stage_failed identifying the failing step.
        """
        node_id = node.id
        ip = node.ip
        port = getattr(node, "socks_port", 1080)

        # Step 1: SSH readiness gate
        logger.info("Step 1/7 — SSH readiness: %s", ip)
        if not self._ssh_readiness.wait_for_ssh(ip, self._ssh_timeout):
            return SshInjectionResult(
                success=False,
                node_id=node_id,
                stage_failed="ssh_wait",
                error=f"SSH not available on {ip} within {self._ssh_timeout}s",
            )

        key_path = str(private_key_path)

        # Steps 2-4: Generate creds on-node + write env file + set permissions
        logger.info("Step 2-4/7 — credential generation + env write: %s", ip)
        cred_cmd = (
            "PROXY_USER=$(openssl rand -hex 16) && "
            "PROXY_PASS=$(openssl rand -hex 32) && "
            "printf 'PROXY_USER=%s\\nPROXY_PASS=%s\\n' \"$PROXY_USER\" \"$PROXY_PASS\" "
            "| sudo tee /etc/microsocks.env > /dev/null && "
            "sudo chmod 0600 /etc/microsocks.env && "
            "echo \"${PROXY_USER}:${PROXY_PASS}\""
        )
        result = self._ssh_executor.execute(ip, key_path, cred_cmd)

        if result.returncode != 0 or not result.stdout.strip():
            return SshInjectionResult(
                success=False,
                node_id=node_id,
                stage_failed="credential_generation",
                error=f"On-node credential generation failed: rc={result.returncode}",
            )

        # Parse returned username:password
        cred_line = result.stdout.strip().split("\n")[-1]
        parts = cred_line.split(":", 1)
        if len(parts) != 2:
            return SshInjectionResult(
                success=False,
                node_id=node_id,
                stage_failed="credential_generation",
                error=f"Credential output parse failed: {cred_line!r}",
            )
        username, password = parts[0], parts[1]

        # Step 5: Start microsocks
        logger.info("Step 5/7 — start microsocks: %s", ip)
        start_result = self._ssh_executor.execute(
            ip, key_path, "sudo systemctl start microsocks"
        )
        if start_result.returncode != 0:
            return SshInjectionResult(
                success=False,
                node_id=node_id,
                stage_failed="service_start",
                error=f"microsocks start failed: rc={start_result.returncode}",
            )

        # Step 6: Verify SOCKS5 connectivity
        logger.info("Step 6/7 — SOCKS5 verification: %s:%d", ip, port)
        if not self._socks_verifier.verify(ip, port, username, password):
            return SshInjectionResult(
                success=False,
                node_id=node_id,
                stage_failed="socks_verify",
                error=f"SOCKS5 verification failed on {ip}:{port}",
            )

        # Step 7: Update pool manifest to READY
        logger.info("Step 7/7 — manifest update: %s → READY", node_id)
        self._manifest_writer.write(node)

        logger.info("Injection complete for node %s (%s)", node_id, ip)
        return SshInjectionResult(
            success=True,
            node_id=node_id,
            username=username,
            password=password,
        )
