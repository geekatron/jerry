# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""AuditLogStore — engagement-scoped append-only JSONL operation audit log.

Security properties (APICALL-004):
    - write_entry() has NO response_body or raw_response parameter — response
      bodies containing API tokens or credentials are structurally excluded.
    - Only response_code and resource_id are recorded from provider responses.

Log location: {base_log_dir}/{engagement_id}/provisioner.jsonl
Production default: ./logs/audit/{engagement_id}/provisioner.jsonl

The log directory is intentionally separate from ./secrets/ which is purged
during engagement teardown (TASK-023-046 AC: logs survive teardown).

Rotation (FM-025):
    - MAX_FILE_SIZE_BYTES: 10MB maximum per file
    - RETENTION_DAYS: 90-day retention

References:
    - TASK-023-046: CLM Audit Logging for Provisioner API Calls
    - ADR-PROJ023-008: Engagement-scoped audit log (T-13 repudiation mitigation)
    - APICALL-004: Never log response bodies containing tokens or credentials
    - FM-025: Audit log rotation and retention policy
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


class AuditLogStore:
    """Engagement-scoped append-only JSONL operation audit log.

    Records all proxy infrastructure operations with structured metadata.
    Each call to write_entry() appends exactly one JSON object on a new line
    (JSONL format) to the engagement-scoped log file.

    Security invariant (APICALL-004): write_entry() accepts only response_code
    and resource_id from the provider response — never the response body.
    This structural constraint prevents accidental logging of API tokens,
    SSH private keys, or SOCKS5 credentials.

    Rotation constants (FM-025):
        MAX_FILE_SIZE_BYTES: Maximum log file size before rotation (10MB).
        RETENTION_DAYS: Maximum retention period in days (90).

    Attributes:
        base_log_dir: Root directory for all engagement audit logs.
            In production this is ``./logs/audit/``.  Tests inject a
            temporary directory.
    """

    #: Maximum log file size in bytes before rotation (FM-025: 10MB).
    MAX_FILE_SIZE_BYTES: int = 10 * 1024 * 1024

    #: Maximum retention period in days (FM-025: 90 days).
    RETENTION_DAYS: int = 90

    def __init__(self, base_log_dir: Path | None = None) -> None:
        """Initialise the AuditLogStore with an optional base directory.

        Args:
            base_log_dir: Root directory under which engagement sub-directories
                are created.  Defaults to ``./logs/audit/`` relative to the
                working directory.  Must NOT be under ``./secrets/`` as that
                directory is purged during engagement teardown (TASK-023-046 AC).
        """
        self.base_log_dir: Path = base_log_dir if base_log_dir is not None else Path("logs") / "audit"

    def write_entry(
        self,
        engagement_id: str,
        action: str,
        provider: str,
        resource_id: str,
        response_code: int,
    ) -> None:
        """Append one JSONL audit record for a provisioner API call.

        APICALL-004: This method intentionally has no ``response_body`` or
        ``raw_response`` parameter.  Only the structured fields below are
        persisted — never the raw provider response body which may contain
        API tokens, SSH keys, or SOCKS5 credentials.

        Args:
            engagement_id: Owning engagement identifier (PI-002).  Used to
                scope the log file to the engagement directory.
            action: Operation type, one of: "provision", "destroy",
                "list_instances", "health_check", "preflight", "rotate".
            provider: Cloud provider name (e.g., "digitalocean", "vultr").
            resource_id: Provider-assigned resource identifier for the
                affected node (e.g., "do-12345").  Must not contain
                credential material.
            response_code: HTTP response code returned by the provider API
                (e.g., 200, 201, 204, 401, 403, 429).
        """
        log_path = self._log_path(engagement_id)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "engagement_id": engagement_id,
            "action": action,
            "provider": provider,
            "resource_id": resource_id,
            "response_code": response_code,
        }
        with log_path.open(mode="a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")

    def _log_path(self, engagement_id: str) -> Path:
        """Return the JSONL log file path for the given engagement.

        Args:
            engagement_id: Owning engagement identifier.

        Returns:
            Path to ``{base_log_dir}/{engagement_id}/provisioner.jsonl``.
        """
        return self.base_log_dir / engagement_id / "provisioner.jsonl"
