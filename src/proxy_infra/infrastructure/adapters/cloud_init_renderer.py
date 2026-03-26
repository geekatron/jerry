# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""CloudInitRenderer — renders cloud-init user-data scripts for proxy node provisioning.

Generates cloud-init YAML for installing and configuring SOCKS5 proxy
software (SSH daemon hardening, Dante/microsocks installation) on
newly provisioned VPS instances.

References:
    - ADR-PROJ023-008: Proxy node provisioning workflow
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig


class CloudInitRenderer:
    """Renders cloud-init user-data YAML for proxy node configuration.

    Produces a cloud-init script that:
    - Installs and configures SSH daemon (key-only auth, no password auth)
    - Installs SOCKS5 proxy software (Dante or microsocks)
    - Configures the SOCKS5 listener on the specified port
    - Applies OS hardening (ufw rules, fail2ban)

    References:
        - ADR-PROJ023-008: Node configuration at provisioning time
    """

    def render(self, config: ProvisionConfig) -> str:
        """Render a cloud-init user-data script for the given provision config.

        Args:
            config: Provisioning parameters including proxy_type and socks_port.

        Returns:
            Cloud-init YAML string suitable for passing as VPS user-data.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")
