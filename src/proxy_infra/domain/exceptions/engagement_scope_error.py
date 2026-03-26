# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""EngagementScopeError domain exception for proxy infrastructure."""

from __future__ import annotations


class EngagementScopeError(Exception):
    """Raised when a mutating operation is attempted without a valid engagement_id (PI-002)."""
