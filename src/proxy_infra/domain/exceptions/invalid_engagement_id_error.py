# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""InvalidEngagementIdError domain exception for proxy infrastructure."""

from __future__ import annotations


class InvalidEngagementIdError(Exception):
    """Raised when a mutating operation is attempted with a missing or blank engagement_id (PI-002).

    A valid engagement_id must be a non-empty, non-whitespace string.
    """
