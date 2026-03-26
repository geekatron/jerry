# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Socks5CredentialReturnHandler — writes injected SOCKS5 credentials to operator.

After on-node injection, retrieves SOCKS5 username:password and writes them
to the engagement credential directory as Docker-secret-compatible files
(mode 0600, format ``username:password``).

Design constraints:
    H-07: Application layer — no infrastructure imports.
    H-10: One public class per file.
    H-11: All public methods have type annotations.

References:
    - TASK-023-056: SOCKS5 credential return flow
    - FEAT-023-004: Hands-Free Engagement Pipeline Automation
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

#: File permission for credential files: owner read/write only.
_SECRET_FILE_MODE: int = 0o600

#: Prefix for per-node SOCKS5 credential files.
_SOCKS5_CREDS_PREFIX: str = "socks5_creds"


@dataclass(frozen=True)
class CredentialReturnResult:
    """Result of a SOCKS5 credential return operation.

    Attributes:
        success: True when the credential file was written.
        node_id: The proxy node this result is for.
        written_path: Path to the written credential file, or empty on failure.
        error: Human-readable error message if success is False.
    """

    success: bool
    node_id: str
    written_path: str = ""
    error: str = ""


class Socks5CredentialReturnHandler:
    """Writes SOCKS5 credentials from injected nodes to the operator's credential directory.

    Each node's credentials are written as ``socks5_creds_{node_id}`` with
    0600 permissions in Docker-secret-compatible ``username:password`` format.

    Args:
        credential_dir: Path to the engagement credential directory.
    """

    def __init__(self, credential_dir: Path) -> None:
        """Initialise the credential return handler.

        Args:
            credential_dir: Directory where credential files are written.
        """
        self._credential_dir = credential_dir

    def write_credentials(
        self,
        node_id: str,
        username: str,
        password: str,
    ) -> CredentialReturnResult:
        """Write SOCKS5 credentials for a node to the credential directory.

        Args:
            node_id: Provider-assigned node identifier.
            username: SOCKS5 username generated on the node.
            password: SOCKS5 password generated on the node.

        Returns:
            CredentialReturnResult with success=True and the written path.
        """
        if not username or not username.strip():
            return CredentialReturnResult(
                success=False,
                node_id=node_id,
                error="username must not be empty",
            )
        if not password:
            return CredentialReturnResult(
                success=False,
                node_id=node_id,
                error="password must not be empty",
            )

        target = self._credential_dir / f"{_SOCKS5_CREDS_PREFIX}_{node_id}"
        try:
            target.write_text(f"{username}:{password}", encoding="utf-8")
            os.chmod(target, _SECRET_FILE_MODE)
            logger.debug(
                "SOCKS5 credentials written for node=%r (values redacted)", node_id
            )
            return CredentialReturnResult(
                success=True,
                node_id=node_id,
                written_path=str(target),
            )
        except OSError as exc:
            logger.warning("Failed to write SOCKS5 creds for node=%r: %s", node_id, exc)
            return CredentialReturnResult(
                success=False,
                node_id=node_id,
                error=str(exc),
            )
