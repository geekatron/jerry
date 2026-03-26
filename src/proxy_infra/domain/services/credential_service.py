# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Domain service for generating ephemeral proxy node credentials.

Produces per-node SOCKS5 credentials and SSH key descriptors. This is a
pure domain service: it imports only stdlib modules (H-07 compliant).
File I/O (ssh-keygen, file writes) is the responsibility of infrastructure
adapters, not this service.

References:
    - TASK-023-033: Credential Generation (per-node SSH keys + SOCKS5 creds)
    - TASK-023-034: Credential Injection (Docker secrets)
    - F-002 (credential-security-assessment): SSH keys per VPS node
    - F-003 (credential-security-assessment): Cleanup at teardown
"""

from __future__ import annotations

import hashlib
import logging
import secrets

_logger = logging.getLogger(__name__)

#: Default SOCKS5 password entropy in bytes (16 bytes = 128 bits).
_SOCKS5_PASSWORD_BYTES: int = 16

#: Username prefix for generated SOCKS5 credentials.
_SOCKS5_USERNAME_PREFIX: str = "jerry-"


class CredentialService:
    """Domain service producing per-node ephemeral credentials.

    This is a pure domain service: it imports only stdlib modules and has
    no dependency on application or infrastructure layers (H-07).

    All methods return credential VALUES (strings/tuples). File I/O
    (writing keys to disk, running ssh-keygen) belongs in infrastructure.
    """

    def generate_socks5_credentials(self, node_id: str) -> tuple[str, str]:
        """Generate a unique SOCKS5 username and password for a proxy node.

        Args:
            node_id: Provider-assigned node identifier.

        Returns:
            Tuple of (username, password). Username is deterministic from
            node_id (jerry-{hash[:8]}). Password is 128-bit random.
        """
        self._validate_node_id(node_id)

        node_hash = hashlib.sha256(node_id.encode()).hexdigest()[:8]
        username = f"{_SOCKS5_USERNAME_PREFIX}{node_hash}"
        password = secrets.token_urlsafe(_SOCKS5_PASSWORD_BYTES)

        _logger.debug("Generated SOCKS5 credentials for node %r (username=%r)", node_id, username)
        return username, password

    def generate_ssh_key_comment(self, node_id: str) -> str:
        """Generate the SSH key comment string for a proxy node.

        Args:
            node_id: Provider-assigned node identifier.

        Returns:
            Comment string for the SSH key (e.g., "jerry-proxy-do-12345").
        """
        self._validate_node_id(node_id)
        return f"jerry-proxy-{node_id}"

    def generate_credential_filename(self, node_id: str, suffix: str = "") -> str:
        """Generate a deterministic filename for credential storage.

        Args:
            node_id: Provider-assigned node identifier.
            suffix: File suffix (e.g., ".pub" for public key).

        Returns:
            Filename string (e.g., "id_ed25519_do-12345.pub").
        """
        self._validate_node_id(node_id)
        return f"id_ed25519_{node_id}{suffix}"

    @staticmethod
    def _validate_node_id(node_id: str) -> None:
        """Validate that node_id is non-empty and safe for filenames.

        Args:
            node_id: Provider-assigned node identifier.

        Raises:
            ValueError: If node_id is empty or contains unsafe characters.
        """
        if not node_id or not node_id.strip():
            raise ValueError("node_id must be a non-empty string")
        unsafe = set(node_id) & set("/\\..;|&$`\"'")
        if unsafe:
            raise ValueError(
                f"node_id contains unsafe characters: {unsafe!r}"
            )
