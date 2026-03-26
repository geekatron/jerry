# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Value object representing an original TCP destination recovered from the BPF map.

The BPF cgroup/connect4 program stores the pre-rewrite destination in the
dst_latest array map. The SocksBridge reads that map entry and returns it
as an OriginalDestination so the SOCKS5 tunnel can connect to the real target.

References:
    EN-023-001 F-1  -- BPF map key design (array[0] for bridge reads)
    TASK-023-017    -- dst_latest map specification
"""

from __future__ import annotations

from typing import NamedTuple


class OriginalDestination(NamedTuple):
    """Original TCP destination recovered from the BPF dst_latest array map.

    Attributes:
        ip: IPv4 address string of the intended destination before BPF rewrite.
        port: TCP port of the intended destination before BPF rewrite.
    """

    ip: str
    port: int
