# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Engagement initializer service for creating engagement directory structures.

Creates the standard engagement directory layout required for evidence
persistence, report generation, and credential quarantine.

References:
    - ADR-PROJ023-001: Engagement Management
    - TASK-008: EngagementInitializer
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


class EngagementInitializer:
    """Creates and validates engagement directory structures.

    Each engagement gets a standard directory layout under the configured
    base directory (default: work/engagements/):

        work/engagements/{id}/
            evidence/                 -- raw tool output + SHA-256 metadata
            reports/                  -- final deliverables
            .credential-quarantine/   -- quarantined credential-bearing output
    """

    EVIDENCE_DIR = "evidence"
    REPORTS_DIR = "reports"
    QUARANTINE_DIR = ".credential-quarantine"

    def __init__(self, base_dir: str | Path = "work/engagements") -> None:
        """Initialize with the engagement base directory.

        Args:
            base_dir: Root directory for all engagements, relative to the
                project root or absolute.
        """
        self._base_dir = Path(base_dir)

    def initialize(self, engagement_id: str) -> Path:
        """Create the engagement directory structure.

        Creates all required subdirectories and writes an initialization
        metadata file. Idempotent: if the directory already exists, the
        metadata file is updated but existing contents are preserved.

        Args:
            engagement_id: Unique identifier for the engagement.

        Returns:
            Path to the created engagement root directory.

        Raises:
            ValueError: If the engagement_id is empty or contains
                path-traversal characters.
        """
        self._validate_id(engagement_id)

        engagement_dir = self._base_dir / engagement_id
        evidence_dir = engagement_dir / self.EVIDENCE_DIR
        reports_dir = engagement_dir / self.REPORTS_DIR
        quarantine_dir = engagement_dir / self.QUARANTINE_DIR

        evidence_dir.mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)
        quarantine_dir.mkdir(parents=True, exist_ok=True)

        # Write initialization metadata
        meta_path = engagement_dir / ".engagement-meta.json"
        meta = {
            "engagement_id": engagement_id,
            "initialized_at": datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%SZ"),
            "directories": {
                "evidence": str(evidence_dir),
                "reports": str(reports_dir),
                "quarantine": str(quarantine_dir),
            },
        }
        meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

        return engagement_dir

    def is_initialized(self, engagement_id: str) -> bool:
        """Check whether an engagement directory exists and is properly structured.

        Args:
            engagement_id: The engagement identifier to check.

        Returns:
            True if all required subdirectories exist, False otherwise.
        """
        engagement_dir = self._base_dir / engagement_id
        return (
            (engagement_dir / self.EVIDENCE_DIR).is_dir()
            and (engagement_dir / self.REPORTS_DIR).is_dir()
            and (engagement_dir / self.QUARANTINE_DIR).is_dir()
        )

    def evidence_dir(self, engagement_id: str) -> Path:
        """Get the evidence directory path for an engagement.

        Args:
            engagement_id: The engagement identifier.

        Returns:
            Path to the evidence directory.
        """
        return self._base_dir / engagement_id / self.EVIDENCE_DIR

    def quarantine_dir(self, engagement_id: str) -> Path:
        """Get the credential quarantine directory path for an engagement.

        Args:
            engagement_id: The engagement identifier.

        Returns:
            Path to the quarantine directory.
        """
        return self._base_dir / engagement_id / self.QUARANTINE_DIR

    def _validate_id(self, engagement_id: str) -> None:
        """Validate the engagement ID format.

        Args:
            engagement_id: The ID to validate.

        Raises:
            ValueError: If the ID is empty or contains path-traversal characters.
        """
        if not engagement_id or not engagement_id.strip():
            msg = "Engagement ID must not be empty"
            raise ValueError(msg)
        if ".." in engagement_id or "/" in engagement_id or "\\" in engagement_id:
            msg = f"Engagement ID '{engagement_id}' contains path-traversal characters (.. / \\)"
            raise ValueError(msg)
