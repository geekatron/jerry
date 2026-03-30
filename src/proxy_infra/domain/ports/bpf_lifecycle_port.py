# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""IBpfLifecyclePort — Protocol for full BPF program lifecycle management.

Extends the BpfBypassPort (bypass map only) with load/attach/detach/readiness
operations needed by the engagement lifecycle state machine.

Design constraints:
    H-07: Domain layer port — no infrastructure or application imports.
    H-10: One public class per file.
    H-11: All public methods have type annotations.

References:
    EN-023-008: eBPF transparent proxy integration
    AP-4: IBpfLifecyclePort extends BpfBypassPort contract
    DC-2: Init container pattern (load externally, tool gets read-only bpffs)
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class IBpfLifecyclePort(Protocol):
    """Port for full BPF cgroup/connect4 program lifecycle management.

    Extends the bypass map update capability with program load/attach,
    readiness verification, and teardown cleanup. Used by
    GatedLifecycleManager to wire BPF into the engagement lifecycle.

    Lifecycle:
        1. load_and_attach(container_id)  — Load BPF, attach to container cgroup
        2. populate_bypass(proxy_ips, envoy_ip) — Fill bypass_ips map
        3. is_ready() — Verify pin exists and bridge is listening
        4. detach_and_cleanup() — Unpin and detach on teardown
    """

    def load_and_attach(self, container_id: str) -> None:
        """Load BPF program and attach to the specified container's cgroup.

        Args:
            container_id: Docker container ID (short or full).

        Raises:
            RuntimeError: If BPF load, pin, or attachment fails.
        """
        ...

    def populate_bypass(self, proxy_ips: list[str], envoy_ip: str) -> None:
        """Populate the bypass_ips BPF map to prevent redirect loops.

        Must be called AFTER load_and_attach (constraint B7).

        Args:
            proxy_ips: List of SOCKS5 proxy node IPv4 addresses.
            envoy_ip: IPv4 address of the Envoy forward proxy container.

        Raises:
            RuntimeError: If any map update fails.
        """
        ...

    def update_bypass_ips(self, ips: list[str]) -> None:
        """Update the bypass map with proxy node IPs.

        Backward-compatible with BpfBypassPort contract.

        Args:
            ips: List of IPv4 addresses to add to the bypass map.
        """
        ...

    def is_ready(self) -> bool:
        """Check that the BPF program is pinned and the bridge is listening.

        Returns:
            True if BPF is fully operational.
        """
        ...

    def detach_and_cleanup(self) -> None:
        """Detach BPF program from cgroup and unpin from bpffs.

        Safe to call even if load_and_attach was never completed.
        Constraint B3: NEVER leave BPF pinned after teardown.
        """
        ...
