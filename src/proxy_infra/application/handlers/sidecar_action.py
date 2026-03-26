# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""SidecarAction enum — lifecycle operations for the socks-bridge sidecar (H-10)."""

from enum import Enum


class SidecarAction(str, Enum):
    """Supported lifecycle operations for the socks-bridge sidecar."""

    START = "start"
    STOP = "stop"
    RESTART = "restart"
    STATUS = "status"
