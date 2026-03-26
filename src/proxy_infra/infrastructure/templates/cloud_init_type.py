# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Cloud-init template type enum (H-10: one class per file)."""

from enum import Enum


class CloudInitType(Enum):
    """Proxy node cloud-init template type selector."""

    TYPE_A_SSH_ENDPOINT = "type_a_ssh_endpoint"
    TYPE_B_MICROSOCKS = "type_b_microsocks"
