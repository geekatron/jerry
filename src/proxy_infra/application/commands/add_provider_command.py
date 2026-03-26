# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""AddProviderCommand — application-layer command for configuring a cloud provider.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AddProviderCommand:
    """Command to configure a cloud provider for proxy provisioning.

    Stores provider API key via the configured credential store
    (env var or OS keychain per ADR-PROJ023-008 DA-001).

    Attributes:
        name: Provider identifier (e.g., "digitalocean").
        api_key_env: Name of the environment variable holding the API key.
        use_keyring: If True, store the key in the OS keychain as well.
    """

    name: str
    api_key_env: str = ""
    use_keyring: bool = False
