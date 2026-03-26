# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ProviderConfigStore — reads and writes provider configuration from ~/.jerry/providers.yaml.

This file stores provider metadata (regions, image defaults, SSH key names)
but NEVER raw API keys (stored via CredentialStorePort instead).

References:
    - ADR-PROJ023-008: Provider configuration design
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations


class ProviderConfigStore:
    """Reads and writes provider configuration from ~/.jerry/providers.yaml.

    Manages the non-secret provider metadata: default regions, images, sizes,
    SSH key names, and api_key_source preference. Raw API keys are NEVER
    stored here (they live in the OS keychain or environment variables).

    Config location: ~/.jerry/providers.yaml

    References:
        - ADR-PROJ023-008: providers.yaml schema
    """

    CONFIG_PATH_TEMPLATE = "~/.jerry/providers.yaml"

    def load_provider(self, provider_name: str) -> dict[str, str]:
        """Load configuration for a specific cloud provider.

        Args:
            provider_name: Provider identifier (e.g., "digitalocean").

        Returns:
            Provider configuration dictionary with region, image, size,
            and api_key_source fields.

        Raises:
            KeyError: If the provider is not configured.
            FileNotFoundError: If providers.yaml does not exist.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def save_provider(self, provider_name: str, config: dict[str, str]) -> None:
        """Save configuration for a cloud provider.

        Creates or updates the provider entry in providers.yaml. Never
        writes raw API keys to this file.

        Args:
            provider_name: Provider identifier.
            config: Provider configuration dictionary. Must not contain
                raw API keys.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def list_providers(self) -> list[str]:
        """Return a list of all configured provider names.

        Returns:
            Sorted list of provider identifier strings.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")
