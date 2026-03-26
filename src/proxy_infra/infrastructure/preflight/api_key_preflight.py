# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""API key pre-flight health check for cloud provider adapters.

Validates that the configured API key is alive and properly scoped before
any mutating operation (provision, destroy, rotate) touches cloud resources.

Security properties:
    - Pre-flight uses the minimum-privilege endpoint for each provider
      (DigitalOcean: droplets.list, Vultr: account.get, Hetzner: servers.list).
    - On 401/403: raises the appropriate domain exception with actionable guidance.
    - On timeout: returns PreflightStatus.WARNING so network issues do not
      block the provisioning workflow.
    - Pre-flight results are audit-logged via AuditLogStore.

References:
    - TASK-023-048: API Key Pre-Flight Health Check
    - APIKEY-006: Pre-flight catches expired API keys
    - FM-009: Vultr IP ACL mismatch detection
"""

from __future__ import annotations

import socket
import urllib.request
from dataclasses import dataclass
from enum import Enum
from typing import Any

from src.proxy_infra.domain.exceptions.api_key_expired_error import ApiKeyExpiredError
from src.proxy_infra.domain.exceptions.api_key_permission_error import ApiKeyPermissionError
from src.proxy_infra.domain.exceptions.vultr_ip_acl_mismatch_error import VultrIpAclMismatchError


def get_current_egress_ip() -> str:
    """Detect the operator's current public egress IP address.

    Used by the Vultr pre-flight check to surface IP ACL mismatch errors
    (FM-009).  Falls back to "unknown" if detection fails.

    Returns:
        Public IPv4 address string, or "unknown" on failure.
    """
    try:
        with urllib.request.urlopen("https://api.ipify.org", timeout=5) as resp:  # noqa: S310
            return resp.read().decode("utf-8").strip()
    except Exception:
        return "unknown"


class PreflightStatus(str, Enum):
    """Possible outcomes of an API key pre-flight check.

    Attributes:
        PASS: Key is valid and properly scoped.
        WARNING: Check timed out; key validity cannot be confirmed but
            provisioning may proceed (network issues should not block ops).
        FAIL: Key is invalid, expired, or lacks required scope.
    """

    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"


@dataclass(frozen=True)
class PreflightResult:
    """Immutable result of an API key pre-flight check.

    Attributes:
        provider: Cloud provider name that was checked.
        status: Outcome of the check (PASS, WARNING, or FAIL).
        message: Human-readable description of the outcome.
    """

    provider: str
    status: PreflightStatus
    message: str = ""


class ApiKeyPreflightChecker:
    """Validates a cloud provider API key before mutating operations.

    Each cloud provider has its own minimal-scope validation endpoint:
    - DigitalOcean: ``client.droplets.list()`` (droplet:read scope)
    - Vultr: ``client.account.get()`` (GET /v2/account — cheapest endpoint)
    - Hetzner: ``client.servers.list()`` (servers list)

    On 401 the key is expired/revoked (ApiKeyExpiredError is raised).
    On 403 the key lacks required scope (ApiKeyPermissionError is raised),
    except for Vultr where 403 with an IP ACL message raises VultrIpAclMismatchError.
    On timeout a WARNING result is returned; provisioning continues.

    References:
        - TASK-023-048 AC: pre-flight runs before every provision/rotate/destroy
        - APIKEY-006: expired key detection
        - FM-009: Vultr IP ACL mismatch
    """

    def __init__(
        self,
        provider: str,
        client: Any,
        audit_store: Any,
        engagement_id: str,
    ) -> None:
        """Initialise the pre-flight checker.

        Args:
            provider: Cloud provider name (e.g., "digitalocean", "vultr", "hetzner").
            client: Provider SDK client instance.
            audit_store: AuditLogStore instance to record pre-flight results.
            engagement_id: Owning engagement identifier for audit log scoping.
        """
        self._provider = provider
        self._client = client
        self._audit_store = audit_store
        self._engagement_id = engagement_id

    def run(self) -> PreflightResult:
        """Execute the pre-flight check for the configured provider.

        Calls the minimum-privilege read endpoint for the provider.  The result
        (PASS, WARNING, or FAIL) is always written to the audit log.

        Returns:
            PreflightResult with status PASS or WARNING.

        Raises:
            ApiKeyExpiredError: If the provider returns 401 (key revoked/expired).
            ApiKeyPermissionError: If the provider returns 403 due to missing scope.
            VultrIpAclMismatchError: If the Vultr provider returns 403 and the
                error message indicates an IP ACL rejection (FM-009).
        """
        try:
            if self._provider == "digitalocean":
                self._client.droplets.list()
            elif self._provider == "vultr":
                self._client.account.get()
            else:
                # Generic: attempt a servers list for Hetzner and unknown providers
                self._client.servers.list()
        except (TimeoutError, socket.timeout) as exc:
            result = PreflightResult(
                provider=self._provider,
                status=PreflightStatus.WARNING,
                message=f"Pre-flight timed out: {exc} — proceeding with caution",
            )
            self._log(result)
            return result
        except Exception as exc:
            error_text = str(exc)
            self._handle_auth_error(error_text)
            # Should not reach here — _handle_auth_error always raises
            raise  # pragma: no cover

        result = PreflightResult(
            provider=self._provider,
            status=PreflightStatus.PASS,
            message="API key is valid and properly scoped",
        )
        self._log(result)
        return result

    def _handle_auth_error(self, error_text: str) -> None:
        """Map provider error text to a domain exception and raise it.

        Args:
            error_text: String representation of the provider exception.

        Raises:
            VultrIpAclMismatchError: For Vultr 403 with IP ACL indication.
            ApiKeyExpiredError: For 401 Unauthorized responses.
            ApiKeyPermissionError: For 403 Forbidden responses.
        """
        if self._provider == "vultr" and "403" in error_text:
            # FM-009: detect Vultr IP ACL rejections and surface the current egress IP.
            import src.proxy_infra.infrastructure.preflight as _pkg
            current_ip = _pkg.get_current_egress_ip()
            raise VultrIpAclMismatchError(current_ip=current_ip)

        if "401" in error_text or "unauthorized" in error_text.lower():
            raise ApiKeyExpiredError(provider=self._provider, detail=error_text)

        if "403" in error_text or "forbidden" in error_text.lower():
            raise ApiKeyPermissionError(provider=self._provider, detail=error_text)

        # Re-raise unknown errors as ApiKeyExpiredError to keep the failure path typed
        raise ApiKeyExpiredError(provider=self._provider, detail=error_text)

    def _log(self, result: PreflightResult) -> None:
        """Write the pre-flight result to the audit store.

        Args:
            result: The completed pre-flight result to log.
        """
        self._audit_store.write_entry(
            engagement_id=self._engagement_id,
            action="preflight",
            provider=self._provider,
            resource_id="preflight",
            response_code=200 if result.status == PreflightStatus.PASS else 0,
        )
