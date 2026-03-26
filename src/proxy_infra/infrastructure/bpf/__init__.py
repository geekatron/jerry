# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BPF infrastructure adapters for eBPF transparent SOCKS routing.

Public API:
    BpfManager   -- lifecycle management for BPF cgroup/connect4 program
    SocksBridge  -- transparent BPF-to-SOCKS5 relay with scope validation

References:
    EN-023-001  -- eBPF container PoC (findings F-1 through F-8 + OPSEC)
    TASK-023-017 -- BPF program and production manager
    TASK-023-018 -- CLM BPF attach/detach
"""

from src.proxy_infra.infrastructure.bpf.bpf_manager import BpfManager
from src.proxy_infra.infrastructure.bpf.original_destination import OriginalDestination
from src.proxy_infra.infrastructure.bpf.socks_bridge import SocksBridge

__all__ = ["BpfManager", "OriginalDestination", "SocksBridge"]
