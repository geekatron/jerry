# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""KeyringCredentialStore — CredentialStorePort implementation using OS keyring.

Uses the ``keyring`` Python library backed by macOS Keychain (Secure Enclave),
Linux Secret Service, or Windows Credential Manager. Credentials are encrypted
at rest by the OS and gated by the user's authentication (Touch ID on macOS).

Naming convention (jerry/{namespace}.{scope}.{type}):
    service_name: "jerry"  (constant — all Jerry credentials under one service)
    username:     "proxy.{provider}.api-key"  (for cloud provider API keys)

Security properties:
    - Credential values never appear in environment variables, process arguments,
      or tool output
    - APIKEY-002: credential values never logged — only the provider name is logged
    - FM-011: get_credential raises CredentialNotFoundError, never returns None
    - The keyring library handles encryption/decryption transparently via the OS

Design constraints:
    H-07: Infrastructure layer adapter implementing domain port.
    H-10: One public class per file.
    H-11: All public methods have type annotations.

References:
    - TASK-023-066: KeyringCredentialStore implementation
    - STORY-023-010: macOS Keychain Credential Store
    - ADR-PROJ023-011: Credential storage architecture + naming convention
"""

from __future__ import annotations

import logging

import keyring
import keyring.errors

from src.proxy_infra.domain.exceptions.credential_not_found_error import CredentialNotFoundError
from src.proxy_infra.domain.ports.credential_store_port import CredentialStorePort

logger = logging.getLogger(__name__)

#: Keyring service name — all Jerry credentials stored under this service.
_SERVICE_NAME: str = "jerry"

#: Namespace for cloud provider API keys.
_PROXY_NAMESPACE: str = "proxy"

#: Type suffix for API keys.
_API_KEY_TYPE: str = "api-key"


class KeyringCredentialStore(CredentialStorePort):
    """CredentialStorePort implementation backed by the OS keyring (macOS Keychain).

    Stores credentials using the ``keyring`` Python library with the naming
    convention ``jerry/proxy.{provider}.api-key``.

    On macOS: backed by Keychain (Secure Enclave, Touch ID gated).
    On Linux: backed by Secret Service (gnome-keyring/kwallet).
    On Windows: backed by Windows Credential Manager.

    The credential value never appears in logs, repr, or process arguments.
    """

    @staticmethod
    def _key_name(provider_name: str) -> str:
        """Construct the keyring username for a provider.

        Args:
            provider_name: Provider identifier (e.g., "digitalocean").

        Returns:
            Dot-delimited key name (e.g., "proxy.digitalocean.api-key").
        """
        return f"{_PROXY_NAMESPACE}.{provider_name.lower()}.{_API_KEY_TYPE}"

    def get_credential(self, provider_name: str) -> str:
        """Retrieve the API key for a cloud provider from the OS keyring.

        Args:
            provider_name: Provider identifier (e.g., "digitalocean").

        Returns:
            API key string. Never returns None (FM-011).

        Raises:
            CredentialNotFoundError: If no credential is stored for the provider.
        """
        key_name = self._key_name(provider_name)
        value = keyring.get_password(_SERVICE_NAME, key_name)

        if value is None:
            raise CredentialNotFoundError(
                f"No credential found in keychain for provider {provider_name!r}. "
                f"Store one with: jerry proxy credentials set {provider_name}"
            )

        logger.debug("Retrieved credential from keychain for provider=%r", provider_name)
        return value

    def store_credential(self, provider_name: str, api_key: str) -> None:
        """Store an API key in the OS keyring.

        Args:
            provider_name: Provider identifier.
            api_key: API key to store. Never logged.
        """
        key_name = self._key_name(provider_name)
        keyring.set_password(_SERVICE_NAME, key_name, api_key)
        logger.debug("Stored credential in keychain for provider=%r", provider_name)

    def delete_credential(self, provider_name: str) -> bool:
        """Remove a stored API key from the OS keyring.

        Args:
            provider_name: Provider identifier.

        Returns:
            True if credential was found and deleted, False if not found.
        """
        key_name = self._key_name(provider_name)
        try:
            keyring.delete_password(_SERVICE_NAME, key_name)
            logger.debug("Deleted credential from keychain for provider=%r", provider_name)
            return True
        except keyring.errors.PasswordDeleteError:
            logger.debug("No credential to delete in keychain for provider=%r", provider_name)
            return False
