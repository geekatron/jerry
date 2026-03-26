# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""AddProviderHandler — application handler for AddProviderCommand.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from src.proxy_infra.domain.exceptions.credential_not_found_error import CredentialNotFoundError

if TYPE_CHECKING:
    from src.proxy_infra.application.commands.add_provider_command import AddProviderCommand
    from src.proxy_infra.domain.ports.credential_store_port import CredentialStorePort


class AddProviderHandler:
    """Handles AddProviderCommand to register a cloud provider credential.

    Stores provider configuration via the credential store port.
    Follows tiered precedence: env var primary, keyring optional (DA-001).

    References:
        - ADR-PROJ023-008: Tiered credential storage design (DA-001)
    """

    def __init__(self, credential_store: CredentialStorePort) -> None:
        """Initialize AddProviderHandler with the credential store.

        Args:
            credential_store: Credential storage port implementation.
        """
        self._credential_store = credential_store

    def handle(self, command: AddProviderCommand) -> None:
        """Execute an add-provider command.

        Reads the API key from the environment variable specified in the
        command and stores it via the credential store port.

        Args:
            command: The add-provider command containing provider name,
                env var reference, and keyring flag.

        Raises:
            CredentialNotFoundError: If the referenced env var is not set
                and use_keyring is False.
        """
        api_key = os.environ.get(command.api_key_env, "")
        if not api_key:
            raise CredentialNotFoundError(
                f"Environment variable {command.api_key_env!r} is not set. "
                f"Cannot register provider {command.name!r} without an API key."
            )
        self._credential_store.store_credential(command.name, api_key)
