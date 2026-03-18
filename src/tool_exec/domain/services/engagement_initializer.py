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
import os
import re
from datetime import UTC, datetime
from pathlib import Path

# M-05 (T-08, DREAD 28, MEDIUM): Engagement ID character-class allowlist.
# Replace the blocklist (.. / \) with a strict allowlist.
# Allowed: alphanumeric, hyphen, underscore; must start with alphanumeric.
# This prevents engagement IDs like $(whoami) or `id` from polluting the
# filesystem, even though subprocess shell=False prevents command execution.
_ENGAGEMENT_ID_PATTERN: re.Pattern[str] = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,127}$")


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
        # M-10 (T-21, DREAD 24, MEDIUM): Restrict quarantine directory permissions.
        # Default umask may allow other users to read quarantined credential-bearing
        # output. Set 0o700 (owner read/write/execute only) after mkdir.
        # NIST CSF PR.DS-1 (data-at-rest protection).
        os.chmod(str(quarantine_dir), 0o700)

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

        FINDING-002 (CWE-22): _validate_id() is called here to close the path-traversal
        gap where is_initialized(), evidence_dir(), and quarantine_dir() previously
        accepted unvalidated engagement ID strings. Defence-in-depth: validation is
        enforced at every trust boundary crossing, not only in initialize().

        Args:
            engagement_id: The engagement identifier to check.

        Returns:
            True if all required subdirectories exist, False otherwise.

        Raises:
            ValueError: If engagement_id contains invalid characters (M-05).
        """
        self._validate_id(engagement_id)
        engagement_dir = self._base_dir / engagement_id
        return (
            (engagement_dir / self.EVIDENCE_DIR).is_dir()
            and (engagement_dir / self.REPORTS_DIR).is_dir()
            and (engagement_dir / self.QUARANTINE_DIR).is_dir()
        )

    def evidence_dir(self, engagement_id: str) -> Path:
        """Get the evidence directory path for an engagement.

        FINDING-002 (CWE-22): _validate_id() enforced before path composition
        to prevent path traversal via unvalidated caller input.

        Args:
            engagement_id: The engagement identifier.

        Returns:
            Path to the evidence directory.

        Raises:
            ValueError: If engagement_id contains invalid characters (M-05).
        """
        self._validate_id(engagement_id)
        return self._base_dir / engagement_id / self.EVIDENCE_DIR

    def quarantine_dir(self, engagement_id: str) -> Path:
        """Get the credential quarantine directory path for an engagement.

        FINDING-002 (CWE-22): _validate_id() enforced before path composition
        to prevent path traversal via unvalidated caller input.

        Args:
            engagement_id: The engagement identifier.

        Returns:
            Path to the quarantine directory.

        Raises:
            ValueError: If engagement_id contains invalid characters (M-05).
        """
        self._validate_id(engagement_id)
        return self._base_dir / engagement_id / self.QUARANTINE_DIR

    def _validate_id(self, engagement_id: str) -> None:
        """Validate the engagement ID format using a character-class allowlist.

        M-05 mitigation for T-08 (DREAD 28 -> 10 post-mitigation).
        Replaces the blocklist approach (blocking .. / \\) with a strict
        allowlist: only alphanumeric characters, hyphens, and underscores
        are permitted. The ID must start with an alphanumeric character and
        may be 1-128 characters long.

        This prevents IDs like $(whoami) or `id` from polluting the filesystem
        even though they are not exploitable via subprocess (shell=False).

        Args:
            engagement_id: The ID to validate.

        Raises:
            ValueError: If the ID is empty, exceeds 128 characters, or contains
                characters outside [a-zA-Z0-9_-].
        """
        if not engagement_id or not engagement_id.strip():
            msg = "Engagement ID must not be empty"
            raise ValueError(msg)
        if not _ENGAGEMENT_ID_PATTERN.match(engagement_id):
            msg = (
                f"Engagement ID '{engagement_id}' contains invalid characters. "
                f"Only alphanumeric characters, hyphens (-), and underscores (_) "
                f"are allowed. The ID must start with an alphanumeric character "
                f"and be 1-128 characters long."
            )
            raise ValueError(msg)
