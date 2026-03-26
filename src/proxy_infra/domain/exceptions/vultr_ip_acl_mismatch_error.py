# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""VultrIpAclMismatchError domain exception for proxy infrastructure.

References:
    - TASK-023-048: API Key Pre-Flight Health Check
    - FM-009: Vultr IP ACL is set at key creation; mismatch silently rejects calls
"""

from __future__ import annotations


class VultrIpAclMismatchError(Exception):
    """Raised when the operator's current egress IP does not match the Vultr key ACL.

    FM-009: Vultr API keys can be restricted to specific IPs at creation time.
    When the operator's egress IP changes (mobile, VPN, NAT rotation), calls are
    rejected with 403 and no indication that an ACL is the cause.

    Attributes:
        current_ip: The operator's detected egress IP at pre-flight time.
    """

    def __init__(self, current_ip: str) -> None:
        """Construct a VultrIpAclMismatchError with egress IP context.

        Args:
            current_ip: The operator's current egress IP address.
        """
        self.current_ip = current_ip
        message = (
            f"Vultr API key ACL mismatch. Current egress IP: {current_ip}"
            " is not permitted by the key's IP allowlist."
            " Update the Vultr API key ACL at https://my.vultr.com/settings/#settingsapi"
            " or run 'jerry proxy credentials set vultr' to configure a key without ACL restrictions."
        )
        super().__init__(message)
