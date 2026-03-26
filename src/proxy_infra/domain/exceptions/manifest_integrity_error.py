# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ManifestIntegrityError domain exception for proxy infrastructure."""

from __future__ import annotations


class ManifestIntegrityError(Exception):
    """Raised when pool manifest SHA-256 integrity check fails on read (PI-004)."""
