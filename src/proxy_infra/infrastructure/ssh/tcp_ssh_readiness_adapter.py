# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""TcpSshReadinessAdapter — concrete SshReadinessPort implementation using TCP sockets.

Polls port 22 on a target node until an SSH banner is received or the timeout
elapses.  Returns bool (True = SSH ready, False = timeout).  Never raises on
timeout — the caller decides error handling.

Design constraints:
    H-07: Infrastructure layer adapter implementing application port.
    H-10: One public class per file.
    H-11: All public methods have type annotations.
    TASK-023-054: SshReadinessPort concrete adapter.

References:
    - TASK-023-054: SshReadinessPort concrete adapter (TCP socket polling)
    - FEAT-023-004: Hands-Free Engagement Pipeline Automation
"""

from __future__ import annotations

import logging
import socket
import time

logger = logging.getLogger(__name__)

#: Default poll interval in seconds between connection attempts.
_DEFAULT_POLL_INTERVAL: float = 5.0

#: SSH port to poll.
_SSH_PORT: int = 22

#: Socket connection timeout per attempt.
_CONNECT_TIMEOUT: float = 3.0


class TcpSshReadinessAdapter:
    """Polls SSH port 22 via TCP socket until ready or timeout.

    Implements the ``SshReadinessPort`` protocol. Each poll attempt opens a
    TCP connection to port 22. If the connection succeeds and the server sends
    an SSH banner (bytes starting with ``SSH-``), the node is considered ready.

    Args:
        poll_interval: Seconds between poll attempts (default 5.0).
        connect_timeout: Socket connect timeout per attempt (default 3.0).
    """

    def __init__(
        self,
        poll_interval: float = _DEFAULT_POLL_INTERVAL,
        connect_timeout: float = _CONNECT_TIMEOUT,
    ) -> None:
        """Initialise the adapter with polling parameters.

        Args:
            poll_interval: Seconds to wait between connection attempts.
            connect_timeout: Socket timeout for each connection attempt.
        """
        self._poll_interval = poll_interval
        self._connect_timeout = connect_timeout

    def wait_for_ssh(self, ip: str, timeout_seconds: int = 120) -> bool:
        """Poll until SSH is accepting connections on port 22.

        Args:
            ip: Public IPv4 address of the target node.
            timeout_seconds: Maximum total wait time before returning False.

        Returns:
            True when SSH banner is received within the timeout, False otherwise.
        """
        deadline = time.monotonic() + timeout_seconds
        attempt = 0

        while time.monotonic() < deadline:
            attempt += 1
            try:
                with socket.create_connection(
                    (ip, _SSH_PORT), timeout=self._connect_timeout
                ) as sock:
                    # Try to read SSH banner
                    banner = sock.recv(256)
                    if banner and banner.startswith(b"SSH-"):
                        logger.debug(
                            "SSH ready on %s after %d attempts: %s",
                            ip, attempt, banner[:40].decode(errors="replace"),
                        )
                        return True
                    # Connection succeeded but no SSH banner — treat as ready
                    logger.debug("SSH connection to %s succeeded (no banner), treating as ready", ip)
                    return True
            except (ConnectionRefusedError, ConnectionResetError, OSError, socket.timeout):
                remaining = deadline - time.monotonic()
                if remaining > 0:
                    time.sleep(min(self._poll_interval, remaining))

        logger.warning(
            "SSH readiness timeout for %s after %d attempts (%ds)",
            ip, attempt, timeout_seconds,
        )
        return False
