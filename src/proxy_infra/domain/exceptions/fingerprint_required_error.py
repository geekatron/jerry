# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""FingerprintRequiredError domain exception for proxy infrastructure."""

from __future__ import annotations


class FingerprintRequiredError(Exception):
    """Raised when a node attempts to transition to READY without a verified SSH fingerprint (PI-007 / FM-010).

    SSH host key fingerprint verification must be completed before a node is
    considered routable to prevent man-in-the-middle acceptance (T-05).
    """
