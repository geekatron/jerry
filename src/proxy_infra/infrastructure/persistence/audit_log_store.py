# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""AuditLogStore — engagement-scoped append-only operation audit log.

References:
    - ADR-PROJ023-008: Engagement-scoped audit log (T-13 repudiation mitigation)
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from datetime import datetime


class AuditLogStore:
    """Engagement-scoped append-only operation audit log.

    Records all mutating proxy infrastructure operations (provision, destroy,
    rotate) with timestamp, engagement_id, operation type, and outcome.
    Enforces PI-007: every mutation must produce an audit log entry.

    Log location: work/engagements/{engagement_id}/proxy-audit.log

    Security properties:
        - Append-only: entries cannot be modified after writing (T-13)
        - Engagement-scoped: each engagement has its own log file
        - No sensitive data: IP addresses logged, API keys NEVER logged

    References:
        - ADR-PROJ023-008: T-13 repudiation mitigation (DREAD Medium)
    """

    def append(
        self,
        engagement_id: str,
        operation: str,
        details: str,
        occurred_at: datetime | None = None,
    ) -> None:
        """Append an operation record to the engagement audit log.

        Args:
            engagement_id: Owning engagement identifier (PI-002).
            operation: Operation type (e.g., "provision", "destroy", "rotate").
            details: Human-readable description of the operation and outcome.
            occurred_at: UTC timestamp of the operation. Defaults to now.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def read_all(self, engagement_id: str) -> list[str]:
        """Read all audit log entries for an engagement.

        Args:
            engagement_id: Owning engagement identifier.

        Returns:
            List of raw log entry strings in chronological order.

        Raises:
            FileNotFoundError: If no audit log exists for the engagement.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")
