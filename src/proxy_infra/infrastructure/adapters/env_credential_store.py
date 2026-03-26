# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""EnvCredentialStore — CredentialStorePort implementation using environment variables.

References:
    - ADR-PROJ023-008: Tiered credential storage design (DA-001)
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

import os

from src.proxy_infra.domain.exceptions.credential_not_found_error import CredentialNotFoundError
from src.proxy_infra.domain.ports.credential_store_port import CredentialStorePort


class EnvCredentialStore(CredentialStorePort):
    """CredentialStorePort implementation backed by environment variables.

    Reads API keys from environment variables following the naming convention:
        JERRY_PROXY_{PROVIDER}_API_KEY  (provider name uppercased)

    Example:
        JERRY_PROXY_DIGITALOCEAN_API_KEY=dop_v1_...
        JERRY_PROXY_VULTR_API_KEY=v_...
        JERRY_PROXY_HETZNER_API_KEY=hcloud_...

    This is the PRIMARY credential tier (DA-001): env vars work in all
    contexts including headless CI where the OS keyring is unavailable.

    Security: APIKEY-002 — API key values must never be logged. This
    implementation does not pass credential values to any logging call.

    References:
        - ADR-PROJ023-008: DA-001 env vars as primary tier
    """

    ENV_VAR_PREFIX = "JERRY_PROXY_"
    ENV_VAR_SUFFIX = "_API_KEY"

    def _env_var_name(self, provider_name: str) -> str:
        """Construct the environment variable name for a provider.

        Args:
            provider_name: Provider identifier string (case-insensitive).

        Returns:
            Uppercase environment variable name following JERRY_PROXY_{PROVIDER}_API_KEY.
        """
        return f"{self.ENV_VAR_PREFIX}{provider_name.upper()}{self.ENV_VAR_SUFFIX}"

    def get_credential(self, provider_name: str) -> str:
        """Retrieve the API key for a cloud provider from environment variables.

        Args:
            provider_name: Provider identifier (e.g., "digitalocean").

        Returns:
            API key string. Never returns None.

        Raises:
            CredentialNotFoundError: If the environment variable is not set.
        """
        env_var = self._env_var_name(provider_name)
        value = os.environ.get(env_var)
        if value is None:
            raise CredentialNotFoundError(
                f"Credential not found for provider {provider_name!r}. "
                f"Set the environment variable {env_var} to configure access."
            )
        return value

    def store_credential(self, provider_name: str, api_key: str) -> None:
        """Store an API key by setting the corresponding environment variable in the current process.

        Note: environment variable writes are process-scoped and do not persist
        across process restarts. Use KeyringCredentialStore for durable storage.

        Args:
            provider_name: Provider identifier.
            api_key: API key to store in the process environment.
        """
        env_var = self._env_var_name(provider_name)
        os.environ[env_var] = api_key

    def delete_credential(self, provider_name: str) -> bool:
        """Remove the environment variable for a provider from the current process.

        Args:
            provider_name: Provider identifier.

        Returns:
            True if the environment variable existed and was removed; False otherwise.
        """
        env_var = self._env_var_name(provider_name)
        if env_var in os.environ:
            del os.environ[env_var]
            return True
        return False
