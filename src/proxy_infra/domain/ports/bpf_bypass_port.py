# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BpfBypassPort — Protocol for updating the BPF bypass IP map (H-10).

Design constraints:
    H-07: Domain layer port — no infrastructure or application imports.
    H-10: One public class per file.
    H-11: All public methods have type annotations.
"""

from __future__ import annotations

from typing import Protocol


class BpfBypassPort(Protocol):
    """Port for updating the BPF cgroup/connect4 bypass IP map.

    Implementations populate the bypass map with proxy node IPs so that
    BPF-redirected traffic doesn't loop back through the proxy itself.
    """

    def update_bypass_ips(self, ips: list[str]) -> None:
        """Update the bypass map with proxy node IPs.

        Args:
            ips: List of IPv4 addresses to add to the bypass map.
        """
        ...
