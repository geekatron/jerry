# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""NodeHealthPort — Protocol for pre-use health gate checks on a proxy node.

Design constraints:
    H-07: Application layer port — no infrastructure imports.
    H-10: One public class per file.
    H-11: All public methods have type annotations.
    TASK-023-014: Proxy provisioning automation — health check gate.
    TASK-023-015: Proxy health monitoring and rotation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode


class NodeHealthPort(Protocol):
    """Protocol for running pre-use health gate checks on a proxy node.

    Implementations verify connectivity, egress IP correctness, and latency
    before a node is admitted to the active pool.
    """

    def check(self, node: ProxyNode) -> bool:
        """Run connectivity and egress IP health check on the node.

        Args:
            node: The proxy node to validate.

        Returns:
            True if the node passes all pre-use health checks.
        """
        ...
