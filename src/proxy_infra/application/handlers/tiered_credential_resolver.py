# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""TieredCredentialResolver — tries credential stores in priority order.

Resolution order (injected at construction, not hardcoded):
  1. Primary store (typically KeyringCredentialStore — Keychain)
  2. Fallback store (typically EnvCredentialStore — env vars)
  3. Raise CredentialNotFoundError with actionable message

Design constraints:
    H-07: Application layer — imports domain port only. Concrete stores
        are injected by the composition root (interface layer).
    H-10: One public class per file.
    H-11: All public methods have type annotations.

References:
    - TASK-023-068: Tiered credential resolution
    - STORY-023-010: macOS Keychain Credential Store
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from src.proxy_infra.domain.exceptions.credential_not_found_error import CredentialNotFoundError
from src.proxy_infra.domain.ports.credential_store_port import CredentialStorePort

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class TieredCredentialResolver(CredentialStorePort):
    """Resolves credentials by trying injected stores in priority order.

    The resolver itself implements ``CredentialStorePort`` so it can be used
    as a drop-in replacement anywhere a credential store is expected.

    Concrete stores are injected at construction — the resolver never imports
    infrastructure directly (H-07 compliant).

    Args:
        primary: First store to try (e.g., KeyringCredentialStore).
        fallback: Second store to try (e.g., EnvCredentialStore).
        primary_label: Human-readable name for error messages (default: "keychain").
        fallback_label: Human-readable name for error messages (default: "environment variable").
    """

    def __init__(
        self,
        primary: CredentialStorePort,
        fallback: CredentialStorePort,
        primary_label: str = "keychain",
        fallback_label: str = "environment variable",
    ) -> None:
        """Initialise with injected store chain.

        Args:
            primary: First credential store to try.
            fallback: Second credential store to try.
            primary_label: Label for the primary store in error messages.
            fallback_label: Label for the fallback store in error messages.
        """
        self._primary = primary
        self._fallback = fallback
        self._primary_label = primary_label
        self._fallback_label = fallback_label

    def get_credential(self, provider_name: str) -> str:
        """Resolve a credential by trying stores in priority order.

        Args:
            provider_name: Provider identifier (e.g., "digitalocean").

        Returns:
            API key string from the first store that has it.

        Raises:
            CredentialNotFoundError: If no store has the credential, with
                an actionable message listing both resolution methods.
        """
        # Tier 1: Primary store
        try:
            value = self._primary.get_credential(provider_name)
            logger.debug(
                "Credential resolved from %s for provider=%r",
                self._primary_label, provider_name,
            )
            return value
        except CredentialNotFoundError:
            pass

        # Tier 2: Fallback store
        try:
            value = self._fallback.get_credential(provider_name)
            logger.debug(
                "Credential resolved from %s for provider=%r",
                self._fallback_label, provider_name,
            )
            return value
        except CredentialNotFoundError:
            pass

        # Neither tier has the credential
        raise CredentialNotFoundError(
            f"No credential found for provider {provider_name!r}. "
            f"Configure access using one of:\n"
            f"  1. macOS Keychain (recommended — keychain encrypted, Touch ID gated):\n"
            f"     jerry proxy credentials set {provider_name}\n"
            f"  2. Environment variable (fallback — for CI/Docker):\n"
            f"     export JERRY_PROXY_{provider_name.upper()}_API_KEY=<your-api-key>"
        )

    def store_credential(self, provider_name: str, api_key: str) -> None:
        """Store a credential in the primary store.

        Args:
            provider_name: Provider identifier.
            api_key: API key to store.
        """
        self._primary.store_credential(provider_name, api_key)

    def delete_credential(self, provider_name: str) -> bool:
        """Delete a credential from the primary store.

        Args:
            provider_name: Provider identifier.

        Returns:
            True if deleted, False if not found.
        """
        return self._primary.delete_credential(provider_name)
