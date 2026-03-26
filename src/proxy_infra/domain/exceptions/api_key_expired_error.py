# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ApiKeyExpiredError domain exception for proxy infrastructure.

References:
    - TASK-023-048: API Key Pre-Flight Health Check
    - APIKEY-006: Pre-flight catches expired or revoked API keys
"""

from __future__ import annotations


class ApiKeyExpiredError(Exception):
    """Raised when a cloud provider API key is expired, revoked, or returns 401.

    Includes actionable remediation guidance directing the operator to the
    credential management command.

    Attributes:
        provider: Cloud provider name (e.g., "digitalocean").
        detail: Original error detail from the provider response.
    """

    def __init__(self, provider: str, detail: str = "") -> None:
        """Construct an ApiKeyExpiredError with provider context and remediation.

        Args:
            provider: Cloud provider name whose key is expired/revoked.
            detail: Original error message from the provider (e.g., "401 Unauthorized").
        """
        self.provider = provider
        self.detail = detail
        message = (
            f"API key validation failed for provider '{provider}'"
            + (f": {detail}" if detail else "")
            + " — key is expired or unauthorized."
            " Run 'jerry proxy credentials set {provider}' to update the credential."
        )
        super().__init__(message)
