# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ApiKeyPermissionError domain exception for proxy infrastructure.

References:
    - TASK-023-048: API Key Pre-Flight Health Check
    - APIKEY-006: Pre-flight catches insufficient scope (403 Forbidden)
"""

from __future__ import annotations


class ApiKeyPermissionError(Exception):
    """Raised when a cloud provider API key exists but lacks the required scope (403).

    Distinct from ApiKeyExpiredError: the key is valid but missing the permission
    needed for the operation (e.g., droplet:write scope missing).

    Attributes:
        provider: Cloud provider name (e.g., "digitalocean").
        detail: Original error detail from the provider response.
    """

    def __init__(self, provider: str, detail: str = "") -> None:
        """Construct an ApiKeyPermissionError with provider context and remediation.

        Args:
            provider: Cloud provider name whose key lacks required scope.
            detail: Original error message from the provider (e.g., "403 Forbidden").
        """
        self.provider = provider
        self.detail = detail
        message = (
            f"API key permission denied for provider '{provider}'"
            + (f": {detail}" if detail else "")
            + " — key lacks required scope."
            " Run 'jerry proxy credentials set {provider}' to update the credential."
        )
        super().__init__(message)
