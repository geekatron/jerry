# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""SubprocessSshExecutor — concrete SshExecutorPort adapter using SSH subprocess.

Executes shell commands on remote proxy nodes via ``ssh -i {key} root@{ip}``.
This is the infrastructure adapter that makes the 7-step credential injection
handler work against real VPS nodes.

Security properties:
    - Private key passed as -i flag (file path, not key content)
    - StrictHostKeyChecking=accept-new auto-accepts first connection
      (acceptable for ephemeral engagement nodes)
    - No password authentication — key-only
    - Command timeout prevents hanging on unresponsive nodes

Design constraints:
    H-07: Infrastructure layer adapter implementing application port.
    H-10: One public class per file.
    H-11: All public methods have type annotations.

References:
    - TASK-023-073: SubprocessSshExecutor concrete adapter
    - TASK-023-055: SSH credential injection handler (consumer)
"""

from __future__ import annotations

import logging
import subprocess
from dataclasses import dataclass

logger = logging.getLogger(__name__)

#: Default SSH connection + command timeout in seconds.
_DEFAULT_TIMEOUT: int = 30


@dataclass(frozen=True)
class SshCommandResult:
    """Result of a remote SSH command execution.

    Attributes:
        stdout: Standard output from the remote command.
        returncode: Exit code of the remote command.
        stderr: Standard error from the remote command.
    """

    stdout: str
    returncode: int
    stderr: str = ""


class SubprocessSshExecutor:
    """Executes commands on remote nodes via SSH subprocess.

    Implements the ``SshExecutorPort`` protocol. Uses ``ssh -i {key}``
    to connect to ephemeral proxy nodes provisioned by the engagement
    pipeline.

    Args:
        timeout: Maximum seconds for SSH connection + command execution.
        ssh_user: Remote user to connect as (default: root).
    """

    def __init__(
        self,
        timeout: int = _DEFAULT_TIMEOUT,
        ssh_user: str = "root",
    ) -> None:
        """Initialise the SSH executor.

        Args:
            timeout: SSH command timeout in seconds.
            ssh_user: Remote user for SSH connections.
        """
        self._timeout = timeout
        self._ssh_user = ssh_user

    def execute(self, ip: str, private_key_path: str, command: str) -> SshCommandResult:
        """Execute a command on a remote node via SSH.

        Args:
            ip: Node IPv4 address.
            private_key_path: Path to the SSH private key file.
            command: Shell command to execute on the remote node.

        Returns:
            SshCommandResult with stdout, returncode, and stderr.
        """
        ssh_cmd = [
            "ssh",
            "-i", private_key_path,
            "-o", "StrictHostKeyChecking=accept-new",
            "-o", "BatchMode=yes",
            "-o", f"ConnectTimeout={min(self._timeout, 10)}",
            "-o", "LogLevel=ERROR",
            f"{self._ssh_user}@{ip}",
            command,
        ]

        logger.debug("SSH exec: %s@%s (key=%s)", self._ssh_user, ip, private_key_path)

        try:
            result = subprocess.run(
                ssh_cmd,
                capture_output=True,
                text=True,
                timeout=self._timeout,
            )
            return SshCommandResult(
                stdout=result.stdout,
                returncode=result.returncode,
                stderr=result.stderr,
            )
        except subprocess.TimeoutExpired:
            logger.warning("SSH command timed out after %ds: %s@%s", self._timeout, self._ssh_user, ip)
            return SshCommandResult(
                stdout="",
                returncode=-1,
                stderr=f"SSH command timed out after {self._timeout}s",
            )
        except FileNotFoundError:
            logger.error("ssh binary not found in PATH")
            return SshCommandResult(
                stdout="",
                returncode=-1,
                stderr="ssh binary not found in PATH",
            )
