# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""KeyringCredentialStore — CredentialStorePort implementation using OS keychain.

References:
    - ADR-PROJ023-008: Tiered credential storage design (DA-001)
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from src.proxy_infra.domain.ports.credential_store_port import CredentialStorePort


class KeyringCredentialStore(CredentialStorePort):
    """CredentialStorePort implementation using OS keychain via the keyring library.

    Uses the `keyring` library for cross-platform secure credential
    storage: macOS Keychain, Windows Credential Locker, GNOME Keyring.

    This is the OPTIONAL SECONDARY credential tier (DA-001): enhances
    security for interactive desktop sessions where keyring is available.

    Service name: "jerry-proxy"
    Username: provider name (e.g., "digitalocean")
    Password: API key

    References:
        - ADR-PROJ023-008: OS keychain as secondary tier
    """

    SERVICE_NAME = "jerry-proxy"

    def get_credential(self, provider_name: str) -> str | None:
        """Retrieve the API key from the OS keychain for a cloud provider.

        Args:
            provider_name: Provider identifier (e.g., "digitalocean").
                Used as the keychain username under SERVICE_NAME.

        Returns:
            API key string, or None if not stored in the keychain.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def store_credential(self, provider_name: str, api_key: str) -> None:
        """Store an API key in the OS keychain for a cloud provider.

        Args:
            provider_name: Provider identifier. Used as the keychain username.
            api_key: API key to store. Encrypted at rest by the OS.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def delete_credential(self, provider_name: str) -> bool:
        """Remove a stored API key from the OS keychain.

        Args:
            provider_name: Provider identifier.

        Returns:
            True if the credential was found and deleted, False if not found.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")
