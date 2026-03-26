# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""EnvCredentialStore — CredentialStorePort implementation using environment variables.

References:
    - ADR-PROJ023-008: Tiered credential storage design (DA-001)
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from src.proxy_infra.domain.ports.credential_store_port import CredentialStorePort


class EnvCredentialStore(CredentialStorePort):
    """CredentialStorePort implementation using environment variables.

    Reads API keys from environment variables following the naming
    convention: JERRY_PROXY_{PROVIDER}_API_KEY (uppercase, underscores).

    This is the PRIMARY credential tier (DA-001): works in all contexts
    including headless CI where keyring is unavailable.

    Example env var: JERRY_PROXY_DIGITALOCEAN_API_KEY

    References:
        - ADR-PROJ023-008: DA-001 env vars as primary tier
    """

    ENV_VAR_PREFIX = "JERRY_PROXY_"
    ENV_VAR_SUFFIX = "_API_KEY"

    def get_credential(self, provider_name: str) -> str | None:
        """Retrieve the API key for a cloud provider from environment variables.

        Args:
            provider_name: Provider identifier (e.g., "digitalocean").

        Returns:
            API key string, or None if the environment variable is not set.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def store_credential(self, provider_name: str, api_key: str) -> None:
        """Store operation is not supported for environment variable store.

        Environment variables cannot be written by the process at runtime.
        Use KeyringCredentialStore for writable credential storage.

        Args:
            provider_name: Provider identifier.
            api_key: API key (ignored).

        Raises:
            NotImplementedError: Always — env vars cannot be set at runtime.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def delete_credential(self, provider_name: str) -> bool:
        """Delete operation is not supported for environment variable store.

        Args:
            provider_name: Provider identifier.

        Returns:
            Always False — env vars cannot be deleted at runtime.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")
