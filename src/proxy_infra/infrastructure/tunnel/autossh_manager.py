# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""AutosshManager — manages autossh tunnel processes for Type A proxy nodes.

Spawns one autossh subprocess per Type A (SSH tunnel) proxy node. Each process
creates a local SOCKS5 endpoint via SSH dynamic port forwarding (-D). The
manager runs as a SEPARATE Docker service from Envoy so the eBPF cgroup/connect4
program never intercepts the SSH tunnel traffic (separate cgroup — see TASK-023-022).

Design constraints:
    H-07: Infrastructure layer — subprocess use is permitted here.
    H-10: One public class per file.
    H-11: All public methods have type annotations.
    TASK-023-022: autossh tunnel manager.
    OPSEC: StrictHostKeyChecking=no, UserKnownHostsFile=/dev/null (engagement VPS).
    OPSEC: SSH private key referenced by path, never passed as argument value.
"""

from __future__ import annotations

import logging
import shlex
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

from src.proxy_infra.domain.value_objects.proxy_type import ProxyType

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode

logger = logging.getLogger(__name__)

#: Starting local port for SSH dynamic forwarding tunnels.
_BASE_TUNNEL_PORT: int = 12000

#: autossh environment variable defaults (per TASK-023-022 spec).
_AUTOSSH_GATETIME: str = "0"
_AUTOSSH_POLL: str = "30"
_AUTOSSH_FIRST_POLL: str = "30"
_AUTOSSH_MAXSTART: str = "0"

#: SSH proxy user on VPS nodes.
_PROXY_USER: str = "proxyuser"

#: SSH port.
_SSH_PORT: int = 22


class AutosshManager:
    """Manages autossh tunnel processes for Type A (SSH-tunnel) proxy nodes.

    Lifecycle:
        1. ``start_tunnels(nodes, ssh_key_path)`` — spawn one autossh per node
        2. ``health_check()``                     — verify all processes running
        3. ``stop_all()``                         — terminate all tunnels

    The local port for each tunnel is assigned sequentially starting at
    ``_BASE_TUNNEL_PORT + 1`` (12001, 12002, …). socks5lb reads these ports
    from the pool manifest to build its upstream list.

    Args:
        ssh_key_path: Path to the engagement SSH private key (Docker secret
            mount at /run/secrets/eng_ssh_key).
        base_port: First local SOCKS5 port to bind (default 12001).
        proxy_user: Username on the VPS node (default ``"proxyuser"``).
    """

    def __init__(
        self,
        ssh_key_path: str | Path,
        base_port: int = _BASE_TUNNEL_PORT,
        proxy_user: str = _PROXY_USER,
    ) -> None:
        """Initialise AutosshManager.

        Args:
            ssh_key_path: Path to the Ed25519 private key for SSH authentication.
            base_port: Starting port; first tunnel binds to base_port + 1.
            proxy_user: SSH username on VPS nodes.
        """
        self._ssh_key_path = Path(ssh_key_path)
        self._base_port = base_port
        self._proxy_user = proxy_user
        # Maps node_id -> (process, local_port)
        self._tunnels: dict[str, tuple[subprocess.Popen[str], int]] = {}

    # ------------------------------------------------------------------
    # Public lifecycle API
    # ------------------------------------------------------------------

    def start_tunnels(self, nodes: list[ProxyNode]) -> dict[str, int]:
        """Spawn one autossh tunnel per node, returning node_id -> local_port mapping.

        Only nodes with proxy_type == "ssh_tunnel" (ProxyType.SSH_TUNNEL) are
        processed. Other node types are skipped with a debug log.

        Args:
            nodes: List of proxy nodes from the pool manifest.

        Returns:
            Dict mapping node_id to the local SOCKS5 port bound for that node.

        Raises:
            FileNotFoundError: If the autossh binary is not on PATH.
            RuntimeError: If the SSH key file does not exist.
        """
        if not self._ssh_key_path.exists():
            raise RuntimeError(
                f"SSH key file not found: {self._ssh_key_path}. "
                "Ensure Docker secret is mounted before starting tunnels."
            )

        port_map: dict[str, int] = {}
        for idx, node in enumerate(nodes):
            # Filter: only SSH tunnel type nodes
            if not self._is_ssh_tunnel_node(node):
                logger.debug("Skipping non-ssh_tunnel node %s (%s)", node.id, node.proxy_type)
                continue

            local_port = self._base_port + idx + 1
            proc = self._spawn_autossh(node.ip, local_port, node.id)
            self._tunnels[node.id] = (proc, local_port)
            port_map[node.id] = local_port
            logger.info(
                "autossh tunnel started: node=%s ip=%s local_port=%d pid=%d",
                node.id,
                node.ip,
                local_port,
                proc.pid,
            )

        return port_map

    def health_check(self) -> dict[str, bool]:
        """Return liveness status for each managed tunnel.

        Uses ``Popen.poll()`` — None means the process is still running.

        Returns:
            Dict mapping node_id to True (alive) or False (dead/exited).
        """
        status: dict[str, bool] = {}
        for node_id, (proc, _port) in self._tunnels.items():
            alive = proc.poll() is None
            status[node_id] = alive
            if not alive:
                logger.warning(
                    "autossh tunnel for node %s has exited (returncode=%s)",
                    node_id,
                    proc.returncode,
                )
        return status

    def stop_all(self) -> None:
        """Terminate all managed autossh tunnels gracefully then forcefully.

        Safe to call when no tunnels are running (no-op).
        """
        for node_id, (proc, port) in list(self._tunnels.items()):
            logger.info("Stopping autossh tunnel: node=%s port=%d pid=%d", node_id, port, proc.pid)
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning("autossh pid=%d did not stop — SIGKILL", proc.pid)
                proc.kill()
                proc.wait()
        self._tunnels.clear()

    def stop_tunnel(self, node_id: str) -> bool:
        """Stop the tunnel for a specific node.

        Args:
            node_id: Node whose tunnel should be terminated.

        Returns:
            True if the tunnel was found and stopped, False if not managed.
        """
        entry = self._tunnels.pop(node_id, None)
        if entry is None:
            logger.debug("stop_tunnel: no tunnel for node %s", node_id)
            return False

        proc, port = entry
        logger.info("Stopping tunnel for node %s (port=%d pid=%d)", node_id, port, proc.pid)
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
        return True

    def tunnel_count(self) -> int:
        """Return the number of currently managed tunnel processes.

        Returns:
            Integer count of active (tracked) tunnels.
        """
        return len(self._tunnels)

    def local_port_for(self, node_id: str) -> int | None:
        """Return the local SOCKS5 port for a given node, or None if not managed.

        Args:
            node_id: Node identifier.

        Returns:
            Local port integer, or None.
        """
        entry = self._tunnels.get(node_id)
        return entry[1] if entry else None

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _spawn_autossh(self, ip: str, local_port: int, node_id: str) -> subprocess.Popen[str]:
        """Spawn a single autossh subprocess for the given VPS node.

        Args:
            ip: Public IPv4 of the VPS node.
            local_port: Local port to bind the SOCKS5 endpoint on.
            node_id: Node identifier used for the log file name.

        Returns:
            Running Popen instance.

        Raises:
            FileNotFoundError: If autossh binary is not on PATH.
        """
        env = self._build_autossh_env(node_id)
        cmd = self._build_ssh_command(ip, local_port)
        logger.debug("spawning: %s", shlex.join(cmd))
        return subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def _build_autossh_env(self, node_id: str) -> dict[str, str]:
        """Build the environment dict for an autossh subprocess.

        Args:
            node_id: Node identifier used for log file naming.

        Returns:
            Environment variable dict with AUTOSSH_* settings.
        """
        import os as _os
        env = dict(_os.environ)
        env["AUTOSSH_GATETIME"] = _AUTOSSH_GATETIME
        env["AUTOSSH_POLL"] = _AUTOSSH_POLL
        env["AUTOSSH_FIRST_POLL"] = _AUTOSSH_FIRST_POLL
        env["AUTOSSH_MAXSTART"] = _AUTOSSH_MAXSTART
        env["AUTOSSH_LOGFILE"] = f"/var/log/autossh-{node_id}.log"
        return env

    def _build_ssh_command(self, ip: str, local_port: int) -> list[str]:
        """Build the autossh command list for dynamic port forwarding.

        Args:
            ip: VPS public IPv4 address.
            local_port: Local port to bind the SOCKS5 endpoint.

        Returns:
            Command list suitable for subprocess.Popen.
        """
        return [
            "autossh",
            "-M", "0",                                # Disable autossh monitoring port
            "-N",                                     # No remote command (tunnel only)
            "-D", f"127.0.0.1:{local_port}",         # Dynamic SOCKS5 forwarding
            "-o", "StrictHostKeyChecking=no",         # Engagement VPS, no host key check
            "-o", "UserKnownHostsFile=/dev/null",     # No fingerprint persistence (OPSEC)
            "-o", "ServerAliveInterval=15",           # Keepalive every 15s
            "-o", "ServerAliveCountMax=3",            # 3 missed = disconnect
            "-o", "ExitOnForwardFailure=yes",         # Fail fast on forward error
            "-o", "ConnectTimeout=10",                # 10s connect timeout
            "-p", str(_SSH_PORT),
            "-i", str(self._ssh_key_path),
            f"{self._proxy_user}@{ip}",
        ]

    @staticmethod
    def _is_ssh_tunnel_node(node: ProxyNode) -> bool:
        """Return True if the node uses SSH tunnel transport.

        Args:
            node: ProxyNode to inspect.

        Returns:
            True when proxy_type is SSH_TUNNEL.
        """
        return node.proxy_type == ProxyType.SSH_TUNNEL
