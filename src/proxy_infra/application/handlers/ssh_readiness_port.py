# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""SshReadinessPort — Protocol for polling SSH availability on a new proxy node.

Design constraints:
    H-07: Application layer port — no infrastructure imports.
    H-10: One public class per file.
    H-11: All public methods have type annotations.
    TASK-023-014: Proxy provisioning automation — SSH readiness gate.
"""

from __future__ import annotations

from typing import Protocol


class SshReadinessPort(Protocol):
    """Protocol for polling SSH availability on a freshly provisioned proxy node.

    Implementations open a TCP socket to port 22 of the node and return True
    when the SSH daemon answers within the timeout window.
    """

    def wait_for_ssh(self, ip: str, timeout_seconds: int = 120) -> bool:
        """Poll until SSH is accepting connections on port 22.

        Args:
            ip: Public IPv4 address of the node.
            timeout_seconds: Maximum wait time in seconds before returning False.

        Returns:
            True when SSH is available within the timeout, False otherwise.
        """
        ...
