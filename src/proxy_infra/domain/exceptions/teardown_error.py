# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""TeardownError domain exception for proxy infrastructure."""

from __future__ import annotations


class TeardownError(Exception):
    """Raised when engagement teardown fails."""
