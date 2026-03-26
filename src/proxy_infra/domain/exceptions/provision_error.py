# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ProvisionError domain exception for proxy infrastructure."""

from __future__ import annotations


class ProvisionError(Exception):
    """Raised when VPS provisioning fails."""
