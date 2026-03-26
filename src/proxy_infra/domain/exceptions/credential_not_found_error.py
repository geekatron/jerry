# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""CredentialNotFoundError domain exception for proxy infrastructure."""

from __future__ import annotations


class CredentialNotFoundError(Exception):
    """Raised when credential store cannot find a token for the provider."""
