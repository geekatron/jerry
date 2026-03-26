# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""FirewallRule value object — immutable firewall rule for node ingress/egress control.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FirewallRule:
    """Immutable firewall rule for node ingress/egress control.

    Attributes:
        direction: 'inbound' or 'outbound'.
        protocol: 'tcp', 'udp', or 'icmp'.
        ports: Port or port range (e.g., '1080', '1080-1090').
        sources: CIDR blocks or 'any'. For inbound rules, restricts
            who can connect. For outbound, restricts where traffic goes.
    """

    direction: str
    protocol: str
    ports: str
    sources: str
