# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""SocksRelayManager — manages the userspace SOCKS5 relay for the proxy pool.

Wraps either socks5lb (Option D / eBPF path) or redsocks (Option C / iptables
path) as a subprocess, writing the appropriate config file before start and
supporting hot-reload via SIGHUP or process restart.

References:
    - TASK-023-016: SOCKS relay container (socks5lb / redsocks)
    - STORY-023-002: SOCKS proxy support for Envoy forward proxy infrastructure
    - design/ebpf-socks-implementation-design.md: Section 2 — SOCKS5 proxy selection
"""

from __future__ import annotations

import logging
import os
import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.proxy_pool import ProxyPool

logger = logging.getLogger(__name__)

#: Port the relay listens on for redirected connections (SO_MARK loop-prevention).
_DEFAULT_RELAY_PORT: int = 1080
#: SO_MARK value set by relay on its own outbound sockets (loop prevention).
_SO_MARK_LOOP_PREVENT: int = 100
#: Subprocess health-check poll interval in seconds.
_HEALTH_POLL_TIMEOUT: int = 5


class SocksRelayManager:
    """Manages a userspace SOCKS5 relay subprocess for the proxy pool.

    Supports two backend binaries:
      - ``socks5lb``: Go-based SOCKS5 load-balancer (Option D / eBPF path).
      - ``redsocks``: C-based transparent SOCKS redirector (Option C / iptables path).

    The backend is selected at construction time via ``backend``. Both backends
    read a generated config file whose path is managed by this class.

    Attributes:
        backend: Relay binary name, ``"socks5lb"`` or ``"redsocks"``.
        relay_port: Local port the relay listens on (default 1080).
        config_path: Path to the generated relay config file.
        _process: Running relay subprocess, or ``None`` when stopped.
        _pool: Most recently configured ``ProxyPool`` snapshot.
    """

    def __init__(
        self,
        backend: str = "socks5lb",
        relay_port: int = _DEFAULT_RELAY_PORT,
        config_path: str | None = None,
    ) -> None:
        """Initialise the relay manager.

        Args:
            backend: Binary name to execute — ``"socks5lb"`` or ``"redsocks"``.
            relay_port: Port the relay listens on for redirected connections.
            config_path: File path for the generated config.  When ``None`` a
                temporary file is created on first ``configure_pool`` call.
        """
        self.backend: str = backend
        self.relay_port: int = relay_port
        self.config_path: Path | None = Path(config_path) if config_path else None
        self._process: subprocess.Popen[str] | None = None
        self._pool: ProxyPool | None = None

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def configure_pool(self, pool: ProxyPool) -> None:
        """Write the relay config file from the pool manifest.

        Generates a backend-specific config file listing all active proxy nodes
        from *pool*.  The config path is created as a temp file when
        ``config_path`` was not specified at construction.

        Args:
            pool: Immutable pool snapshot to derive the config from.
        """
        self._pool = pool
        if self.config_path is None:
            tmp = tempfile.NamedTemporaryFile(
                mode="w", suffix=".conf", delete=False, prefix="socks_relay_"
            )
            self.config_path = Path(tmp.name)
            tmp.close()

        config_content = self._render_config(pool)
        self.config_path.write_text(config_content, encoding="utf-8")
        logger.debug(
            "Wrote %s config to %s (%d nodes)",
            self.backend,
            self.config_path,
            len(pool.nodes),
        )

    def start(self) -> None:
        """Start the relay subprocess.

        ``configure_pool`` must be called before ``start``.

        Raises:
            RuntimeError: When no pool has been configured yet.
            FileNotFoundError: When the backend binary is not found on PATH.
        """
        if self._pool is None or self.config_path is None:
            raise RuntimeError(
                "configure_pool() must be called before start()"
            )

        cmd = self._build_start_command()
        logger.info("Starting %s: %s", self.backend, " ".join(cmd))
        self._process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        logger.info("%s started with PID %d", self.backend, self._process.pid)

    def stop(self) -> None:
        """Stop the relay subprocess gracefully, then forcefully if needed.

        No-op when the relay is not running.
        """
        if self._process is None:
            logger.debug("stop() called but relay is not running — no-op")
            return

        logger.info("Stopping %s (PID %d)", self.backend, self._process.pid)
        self._process.terminate()
        try:
            self._process.wait(timeout=_HEALTH_POLL_TIMEOUT)
        except subprocess.TimeoutExpired:
            logger.warning(
                "%s did not terminate within %ds — sending SIGKILL",
                self.backend,
                _HEALTH_POLL_TIMEOUT,
            )
            self._process.kill()
            self._process.wait()
        self._process = None

    def health_check(self) -> bool:
        """Return ``True`` when the relay subprocess is alive.

        Uses ``Popen.poll()`` — a return value of ``None`` means the process
        is still running.  This is a lightweight OS-level liveness check; it
        does NOT verify that the relay can reach the proxy pool.

        Returns:
            ``True`` if the relay process is running, ``False`` otherwise.
        """
        if self._process is None:
            return False
        return self._process.poll() is None

    def update_pool(self, pool: ProxyPool) -> None:
        """Hot-reload pool changes into the running relay.

        Writes an updated config file and sends SIGHUP to the relay process so
        it reloads without dropping existing connections.  If the relay is not
        running, only the config file is updated (idempotent — ``start`` will
        pick up the new config).

        Args:
            pool: Updated pool snapshot to write into the config.
        """
        self.configure_pool(pool)
        if self._process is not None and self._process.poll() is None:
            logger.info(
                "Sending SIGHUP to %s (PID %d) for pool hot-reload",
                self.backend,
                self._process.pid,
            )
            self._process.send_signal(
                __import__("signal").SIGHUP
            )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _render_config(self, pool: ProxyPool) -> str:
        """Render the backend-specific config from *pool*.

        Args:
            pool: Immutable pool snapshot.

        Returns:
            Config file content as a string.
        """
        if self.backend == "redsocks":
            return self._render_redsocks_config(pool)
        return self._render_socks5lb_config(pool)

    def _render_socks5lb_config(self, pool: ProxyPool) -> str:
        """Render a socks5lb YAML config listing all pool nodes.

        Args:
            pool: Immutable pool snapshot.

        Returns:
            socks5lb YAML config as a string.
        """
        lines: list[str] = [
            "# socks5lb config — generated by SocksRelayManager",
            f"listen_port: {self.relay_port}",
            f"lb_strategy: {pool.lb_strategy}",
            f"so_mark: {_SO_MARK_LOOP_PREVENT}",
            "proxies:",
        ]
        for node in pool.nodes:
            lines.append(f"  - host: {node.ip}")
            lines.append(f"    port: {node.socks_port}")
        return "\n".join(lines) + "\n"

    def _render_redsocks_config(self, pool: ProxyPool) -> str:
        """Render a redsocks.conf for the first active node in *pool*.

        redsocks does not natively load-balance across multiple proxies; for
        multi-node pools a separate LB layer (HAProxy or shell rotation) is
        required.  This renderer uses the first node as the upstream proxy.

        Args:
            pool: Immutable pool snapshot.

        Returns:
            redsocks.conf content as a string.
        """
        first_node = pool.nodes[0] if pool.nodes else None
        proxy_ip = first_node.ip if first_node else "127.0.0.1"
        proxy_port = first_node.socks_port if first_node else _DEFAULT_RELAY_PORT

        return (
            "# redsocks.conf — generated by SocksRelayManager\n"
            "base {\n"
            "    log_debug = off;\n"
            "    log_info = on;\n"
            "    daemon = off;\n"
            "    redirector = iptables;\n"
            "}\n"
            "\n"
            "redsocks {\n"
            f"    local_ip = 127.0.0.1;\n"
            f"    local_port = {self.relay_port};\n"
            f"    ip = {proxy_ip};\n"
            f"    port = {proxy_port};\n"
            "    type = socks5;\n"
            "}\n"
        )

    def _build_start_command(self) -> list[str]:
        """Build the subprocess command list for the chosen backend.

        Returns:
            Command and arguments as a list of strings.
        """
        if self.backend == "redsocks":
            return ["redsocks", "-c", str(self.config_path)]
        # socks5lb: accepts --config flag
        return ["socks5lb", "--config", str(self.config_path)]
