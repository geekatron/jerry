# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ProxyRole enum for operational role within an engagement.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from enum import Enum


class ProxyRole(str, Enum):
    """Operational role within an engagement."""

    RECON = "recon"      # Reconnaissance traffic only
    ACTIVE = "active"    # Active scanning and enumeration
    EXPLOIT = "exploit"  # Exploitation and post-exploitation
    RESERVE = "reserve"  # Pre-provisioned, not yet assigned
