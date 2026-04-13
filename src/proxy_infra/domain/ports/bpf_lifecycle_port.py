# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""IBpfLifecyclePort — Protocol for full BPF program lifecycle management.

EN-023-010: Unified Envoy architecture with SO_MARK loop prevention.
No bypass maps needed — Envoy upstream sockets are marked with SO_MARK=100
and the BPF connect4 program skips marked connections.

Design constraints:
    H-07: Domain layer port — no infrastructure or application imports.
    H-10: One public class per file.
    H-11: All public methods have type annotations.

References:
    EN-023-010: Envoy unified traffic path with SO_MARK loop prevention
    DC-2: Init container pattern (load externally, tool gets read-only bpffs)
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class IBpfLifecyclePort(Protocol):
    """Port for BPF program lifecycle management (3-program architecture).

    Manages connect4, sockops, and getsockopt programs as a single unit.
    Used by GatedLifecycleManager to wire BPF into the engagement lifecycle.

    EN-023-010 lifecycle:
        1. load_and_attach(container_id)  — Load all 3 BPF programs, attach to cgroup
        2. is_ready() — Verify all pins exist and Envoy is listening on port 15001
        3. detach_and_cleanup() — Unpin and detach all programs on teardown
    """

    def load_and_attach(
        self,
        container_id: str,
        envoy_container_id: str | None = None,
    ) -> None:
        """Load BPF programs and attach to appropriate cgroups.

        BUG-023-001 split-cgroup attachment:
          - connect4 + sockops → tool container cgroup
          - getsockopt → envoy container cgroup (or tool cgroup if sidecar)

        Args:
            container_id: Tool container Docker ID (short or full).
            envoy_container_id: Envoy container Docker ID. If None,
                getsockopt attaches to tool container cgroup (sidecar mode).

        Raises:
            RuntimeError: If BPF load, pin, or attachment fails.
        """
        ...

    def is_ready(self) -> bool:
        """Check that BPF programs are pinned and Envoy is listening on port 15001.

        Returns:
            True if BPF is fully operational.
        """
        ...

    def detach_and_cleanup(self) -> None:
        """Detach BPF programs from cgroup and unpin from bpffs.

        Safe to call even if load_and_attach was never completed.
        Constraint B3: NEVER leave BPF pinned after teardown.
        """
        ...
