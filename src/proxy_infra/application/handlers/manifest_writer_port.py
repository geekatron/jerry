# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ManifestWriterPort — Protocol for writing the pool manifest after provisioning.

Design constraints:
    H-07: Application layer port — no infrastructure imports.
    H-10: One public class per file.
    H-11: All public methods have type annotations.
    TASK-023-014: Proxy provisioning automation — manifest write stage.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode


class ManifestWriterPort(Protocol):
    """Protocol for writing provisioned node entries to the pool manifest.

    Implementations append a node to the engagement-scoped pool manifest JSON
    file so the CLM and autossh service can discover active proxy nodes.
    """

    def write(self, node: ProxyNode) -> None:
        """Append a node entry to the pool manifest.

        Args:
            node: Newly provisioned and validated proxy node to record.
        """
        ...
