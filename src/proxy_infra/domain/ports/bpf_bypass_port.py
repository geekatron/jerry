# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BpfBypassPort — DEPRECATED, replaced by IBpfLifecyclePort.

EN-023-010: The bypass map architecture has been replaced by Envoy SO_MARK
loop prevention. This port is retained as an empty protocol for backward
compatibility with existing imports. New code should use IBpfLifecyclePort.

Design constraints:
    H-07: Domain layer port — no infrastructure or application imports.
    H-10: One public class per file.
"""

from __future__ import annotations

from typing import Protocol


class BpfBypassPort(Protocol):
    """DEPRECATED: Bypass map port replaced by SO_MARK loop prevention.

    EN-023-010: The unified Envoy architecture uses SO_MARK=100 on upstream
    sockets instead of a mutable bypass map. This protocol is retained
    as an empty interface for backward compatibility.
    """

    ...
