# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ProxyType enum for proxy transport mechanism.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from enum import Enum


class ProxyType(str, Enum):
    """Proxy transport mechanism."""

    SSH_TUNNEL = "ssh_tunnel"        # SSH -D dynamic SOCKS5
    DIRECT_SOCKS5 = "direct_socks5" # Dante/microsocks on node
