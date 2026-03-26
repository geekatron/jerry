# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""IptablesRedirect — iptables NAT REDIRECT fallback for transparent SOCKS proxying.

When eBPF (CAP_BPF) is unavailable (kernel < 5.7 or restricted container
policy), this class programmes iptables REDIRECT rules in the nat table so
that all outbound TCP from the container is captured and forwarded to redsocks
on localhost at the configured SOCKS relay port.

Loop prevention follows the SO_MARK = 100 pattern from Option D so that
redsocks's own outbound sockets are excluded from the redirect chain.

References:
    - TASK-023-019: Implement iptables+redsocks MVP (Option C)
    - STORY-023-002: SOCKS proxy support for Envoy forward proxy infrastructure
    - research/ebpf-socks-deep-feasibility.md: redsocks loop-prevention via SO_MARK
"""

from __future__ import annotations

import logging
import os
import subprocess

logger = logging.getLogger(__name__)

#: Custom iptables chain name for the SOCKS redirect rules.
_CHAIN_NAME: str = "REDSOCKS"
#: SO_MARK value matching redsocks's outbound sockets — excluded from redirect.
_SO_MARK_LOOP_PREVENT: int = 100
#: Loopback CIDR excluded from redirect so IPC traffic is never proxied.
_LOCALHOST_CIDR: str = "127.0.0.0/8"


class IptablesRedirect:
    """Manages iptables NAT REDIRECT rules for transparent SOCKS proxying.

    Implements the iptables half of Option C (iptables + redsocks). On
    ``configure_redirect`` it:

    1. Creates a custom ``REDSOCKS`` chain in the ``nat`` table.
    2. Adds exception rules for localhost and marked (redsocks-owned) packets.
    3. Adds exception rules for the upstream proxy IPs (loop prevention).
    4. Adds a catch-all REDIRECT rule forwarding remaining TCP to *socks_port*.
    5. Hooks the chain into the ``OUTPUT`` chain.

    On ``remove_redirect`` it flushes and deletes the chain and removes the
    OUTPUT jump rule — restoring the pre-configuration state exactly.

    Attributes:
        socks_port: Local port redsocks listens on (default 1080).
        proxy_ips: Upstream proxy IPs excluded from the redirect chain to
            prevent redirect loops.
        _active: Whether the iptables rules are currently installed.
    """

    def __init__(
        self,
        socks_port: int = 1080,
        proxy_ips: list[str] | None = None,
    ) -> None:
        """Initialise with the target relay port.

        Args:
            socks_port: Port redsocks listens on for redirected connections.
            proxy_ips: List of upstream proxy IP addresses to exempt from
                redirection (prevents redsocks outbound from looping).
        """
        self.socks_port: int = socks_port
        self.proxy_ips: list[str] = proxy_ips or []
        self._active: bool = False

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def configure_redirect(self, socks_port: int) -> None:
        """Install iptables REDIRECT rules to capture all outbound TCP.

        Creates the ``REDSOCKS`` nat chain, populates exception rules for
        localhost, SO_MARK-100 packets, and upstream proxy IPs, then adds
        the catch-all REDIRECT rule and hooks the chain into OUTPUT.

        All commands run as subprocess calls to ``iptables``.  The caller is
        responsible for ensuring ``CAP_NET_ADMIN`` is granted to the process.

        Args:
            socks_port: Port redsocks listens on for redirected connections.
                Updates ``self.socks_port`` in place.
        """
        self.socks_port = socks_port

        # Create custom chain
        self._run_iptables(["-t", "nat", "-N", _CHAIN_NAME])

        # Exception: loopback traffic must never be proxied
        self._run_iptables(
            ["-t", "nat", "-A", _CHAIN_NAME, "-d", _LOCALHOST_CIDR, "-j", "RETURN"]
        )

        # Exception: redsocks's own outbound sockets (SO_MARK = 100)
        self._run_iptables(
            [
                "-t", "nat", "-A", _CHAIN_NAME,
                "-m", "mark", "--mark", str(_SO_MARK_LOOP_PREVENT),
                "-j", "RETURN",
            ]
        )

        # Exception: upstream proxy IPs (prevent redirect loop through redsocks)
        for proxy_ip in self.proxy_ips:
            self._run_iptables(
                ["-t", "nat", "-A", _CHAIN_NAME, "-d", proxy_ip, "-j", "RETURN"]
            )

        # Catch-all: redirect all remaining TCP to redsocks
        self._run_iptables(
            [
                "-t", "nat", "-A", _CHAIN_NAME,
                "-p", "tcp",
                "-j", "REDIRECT", "--to-ports", str(self.socks_port),
            ]
        )

        # Hook into OUTPUT chain (traffic originating from this container)
        self._run_iptables(
            ["-t", "nat", "-A", "OUTPUT", "-p", "tcp", "-j", _CHAIN_NAME]
        )

        self._active = True
        logger.info(
            "iptables REDIRECT rules installed: TCP -> localhost:%d via %s chain",
            self.socks_port,
            _CHAIN_NAME,
        )

    def remove_redirect(self) -> None:
        """Remove all iptables REDIRECT rules installed by ``configure_redirect``.

        Removes the OUTPUT jump rule first, then flushes and deletes the
        ``REDSOCKS`` chain.  Safe to call when rules are not installed (no-op).
        """
        if not self._active:
            logger.debug("remove_redirect() called but rules not active — no-op")
            return

        # Remove OUTPUT -> REDSOCKS jump rule
        self._run_iptables(
            ["-t", "nat", "-D", "OUTPUT", "-p", "tcp", "-j", _CHAIN_NAME],
            check=False,
        )

        # Flush all rules from the custom chain
        self._run_iptables(["-t", "nat", "-F", _CHAIN_NAME], check=False)

        # Delete the now-empty chain
        self._run_iptables(["-t", "nat", "-X", _CHAIN_NAME], check=False)

        self._active = False
        logger.info("iptables REDIRECT rules removed")

    def is_active(self) -> bool:
        """Return ``True`` if the REDIRECT rules are currently installed.

        This is a Python-level state flag — it does not re-query ``iptables``.
        The flag is set to ``True`` by ``configure_redirect`` and to ``False``
        by ``remove_redirect``.

        Returns:
            ``True`` if rules are in place, ``False`` otherwise.
        """
        return self._active

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _run_iptables(self, args: list[str], *, check: bool = True) -> None:
        """Execute an ``iptables`` command as a subprocess.

        Args:
            args: Command arguments appended to ``["iptables"]``.
            check: When ``True`` (default), raise on non-zero exit code.
        """
        cmd = ["iptables"] + args
        logger.debug("Running: %s", " ".join(cmd))
        subprocess.run(cmd, check=check, capture_output=True, text=True)
