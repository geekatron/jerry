# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Port interface for secure credential storage and retrieval.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class CredentialStorePort(ABC):
    """Port interface for secure credential storage and retrieval.

    Abstracts the credential storage backend (OS keychain, env vars)
    so the domain layer never depends on a specific storage mechanism.

    References:
        - ADR-PROJ023-008: Tiered credential storage design
    """

    @abstractmethod
    def get_credential(self, provider_name: str) -> str | None:
        """Retrieve the API key for a cloud provider.

        Args:
            provider_name: Provider identifier (e.g., "digitalocean").

        Returns:
            API key string, or None if not configured.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    @abstractmethod
    def store_credential(self, provider_name: str, api_key: str) -> None:
        """Store an API key for a cloud provider.

        Args:
            provider_name: Provider identifier.
            api_key: API key to store securely.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    @abstractmethod
    def delete_credential(self, provider_name: str) -> bool:
        """Remove a stored API key.

        Args:
            provider_name: Provider identifier.

        Returns:
            True if credential was found and deleted, False if not found.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")
