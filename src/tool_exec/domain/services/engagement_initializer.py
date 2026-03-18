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

    def initialize(self, engagement_id: str, created_by: str = "unknown") -> Path:
        """Create the engagement directory structure.

        Creates all required subdirectories and writes an initialization
        metadata file. Idempotent: if the directory already exists, existing
        subdirectories are preserved. DR-010 (write-once): if the metadata
        file already exists, the original creation timestamp is preserved and
        the metadata file is NOT overwritten.

        CC-001-R4 (H-07): ``created_by`` is now an explicit parameter instead
        of reading ``os.environ`` inside the domain service. Domain services
        must not access environment variables (infrastructure concern). The
        CLI handler reads ``USER``/``USERNAME`` from ``os.environ`` and passes
        the resolved string here. Default ``"unknown"`` preserves the previous
        fallback behaviour for callers that do not need attribution.

        Args:
            engagement_id: Unique identifier for the engagement.
            created_by: Identity of the operator initializing the engagement.
                Defaults to ``"unknown"``. The CLI handler supplies the value
                resolved from ``os.environ.get("USER", os.environ.get("USERNAME",
                "unknown"))`` so the domain layer stays free of infrastructure
                dependencies (OWASP A05:2021 Security Misconfiguration; NIST
                SSDF PW.5).

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
        # CV-010 / UC-003 Step 6: Field names aligned with UC specification.
        # - "id" (was "engagement_id")
        # - "created_at" ISO 8601 UTC timestamp (was "initialized_at")
        # - "created_by" from parameter (CC-001-R4: domain no longer reads os.environ)
        # DR-010 write-once: if the metadata file already exists AND contains
        # valid JSON, preserve the original creation timestamp by skipping the
        # write. PM-003-R4: If the file exists but is zero-byte, truncated, or
        # contains invalid JSON (e.g., from a crashed prior write), overwrite it
        # with a fresh record rather than silently accepting corrupted metadata.
        meta_path = engagement_dir / ".engagement-meta.json"
        _meta_valid = False
        if meta_path.exists():
            try:
                _parsed = json.loads(meta_path.read_text(encoding="utf-8"))
                # Must be a non-empty mapping to be considered valid.
                _meta_valid = isinstance(_parsed, dict) and bool(_parsed)
            except (json.JSONDecodeError, OSError):
                _meta_valid = False
        if not _meta_valid:
            meta = {
                "id": engagement_id,
                "created_at": datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "created_by": created_by,
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
        # PM-003-R4: Also verify the engagement meta file exists and contains
        # valid JSON. An engagement directory populated with subdirs but missing
        # or corrupted metadata is structurally incomplete; is_initialized()
        # must not consider it valid. This eliminates the internal inconsistency
        # where initialize() preserves a valid existing meta file but is_initialized()
        # only checked subdirectory existence, meaning a corrupted meta file
        # would be silently accepted as a valid engagement.
        meta_path = engagement_dir / ".engagement-meta.json"
        if not meta_path.exists():
            return False
        try:
            _parsed = json.loads(meta_path.read_text(encoding="utf-8"))
            if not isinstance(_parsed, dict) or not _parsed:
                return False
        except (json.JSONDecodeError, OSError):
            return False
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

    def global_audit_dir(self) -> Path:
        """Get the global Zone 3 audit directory path.

        SR-003/PM-007-R3: Exposes the global fallback audit directory as a
        public method so callers do not need to access the private _base_dir
        attribute. Eliminates the Law of Demeter violation in _write_approval_audit.

        The global audit directory is used when no engagement is active, storing
        Zone 3 approval events outside any engagement scope. It is positioned
        one level above the engagements base directory to keep it easily
        discoverable in the project tree.

        Returns:
            Path to the global Zone 3 audit directory (work/.zone3-audit/).
        """
        return self._base_dir.parent / ".zone3-audit"

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
