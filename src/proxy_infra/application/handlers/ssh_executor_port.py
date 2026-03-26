# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""SshExecutorPort — Protocol for executing commands on remote nodes via SSH (H-10).

Design constraints:
    H-07: Application layer port — no infrastructure imports.
    H-10: One public class per file.
    H-11: All public methods have type annotations.
"""

from __future__ import annotations

from typing import Any, Protocol


class SshExecutorPort(Protocol):
    """Port for executing commands on a remote node via SSH.

    Implementations wrap an SSH client (paramiko, subprocess ssh, etc.)
    to run shell commands on provisioned proxy nodes.
    """

    def execute(self, ip: str, private_key_path: str, command: str) -> Any:
        """Execute a command on a remote node.

        Args:
            ip: Node IP address.
            private_key_path: Path to the SSH private key.
            command: Shell command to execute remotely.

        Returns:
            Object with ``stdout`` (str) and ``returncode`` (int) attributes.
        """
        ...
