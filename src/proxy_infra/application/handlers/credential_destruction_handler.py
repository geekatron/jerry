# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""CredentialDestructionHandler — application handler for secure credential teardown.

Implements TASK-023-035: F-003 remediation — ``destroy_all()`` overwrites every
credential file in the generated_dir with urandom data before unlinking,
preventing credential recovery after engagement teardown.

Destruction model:
  1. Enumerate all regular files in generated_dir
  2. For each file: overwrite with os.urandom bytes, then unlink
  3. If a file cannot be destroyed (PermissionError, file locked): log
     a warning, record in failed_files, and continue with remaining files
  4. Return a DestructionReport listing every file processed

Security invariants:
  - File contents are never read into log output during destruction
  - urandom overwrite occurs before unlink (one full-length pass minimum)
  - Partial failure does not abort the sweep (all files attempted)

References:
  - TASK-023-035: Credential destruction specification
  - STORY-023-005: Ephemeral Credential Lifecycle
  - credential-security-assessment.md: ASVS V8.1.2 (temp file cleanup)
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

from src.proxy_infra.domain.value_objects.destruction_entry import DestructionEntry
from src.proxy_infra.domain.value_objects.destruction_report import DestructionReport

_logger = logging.getLogger(__name__)


class CredentialDestructionHandler:
    """Securely destroys all credential material in the engagement's generated_dir.

    Overwrites each file with cryptographically random bytes (one full-length
    pass using os.urandom) before unlinking. This mitigates file-system-level
    recovery of credential material after teardown.

    If a file cannot be destroyed (e.g. locked by another process), a warning
    is logged and the file is recorded in DestructionReport.failed_files.
    Processing continues for all remaining files rather than aborting.

    Args:
        generated_dir: The engagement's generated credential directory. All
            regular files within this directory will be destroyed.
    """

    def __init__(self, generated_dir: Path) -> None:
        """Initialise CredentialDestructionHandler.

        Args:
            generated_dir: Directory whose credential files will be destroyed.
                Must exist before this handler is used.

        Raises:
            NotADirectoryError: If generated_dir does not exist or is not a
                directory.
        """
        if not generated_dir.exists() or not generated_dir.is_dir():
            raise NotADirectoryError(
                f"generated_dir {generated_dir!r} does not exist or is not a directory. "
                "Create the directory before instantiating CredentialDestructionHandler."
            )
        self._generated_dir = generated_dir

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def destroy_all(self) -> DestructionReport:
        """Overwrite and unlink every credential file in generated_dir.

        Enumerates all regular files in the generated_dir, overwrites each with
        os.urandom data (matching the original file size), and then unlinks it.
        Symbolic links and subdirectories are skipped.

        If a file cannot be overwritten or unlinked, the failure is recorded in
        DestructionReport.failed_files and a WARNING is logged. Processing
        continues for remaining files.

        Returns:
            DestructionReport with lists of successfully destroyed files and
            any files that could not be destroyed.
        """
        report = DestructionReport()

        credential_files = [
            p for p in self._generated_dir.iterdir()
            if p.is_file() and not p.is_symlink()
        ]

        if not credential_files:
            _logger.debug(
                "destroy_all: no credential files found in %r",
                str(self._generated_dir),
            )
            return report

        _logger.debug(
            "destroy_all: beginning destruction sweep of %d files in %r",
            len(credential_files),
            str(self._generated_dir),
        )

        for file_path in credential_files:
            self._destroy_single_file(file_path, report)

        _logger.info(
            "destroy_all: destroyed %d files, %d failures in %r",
            len(report.destroyed_files),
            len(report.failed_files),
            str(self._generated_dir),
        )

        return report

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def _destroy_single_file(file_path: Path, report: DestructionReport) -> None:
        """Attempt to overwrite and unlink a single credential file.

        Args:
            file_path: Path to the file to destroy.
            report: DestructionReport to update in-place (append to either
                destroyed_files or failed_files).
        """
        overwrite_ok = False
        try:
            file_size = file_path.stat().st_size
            # Guard against zero-length files: always write at least 1 byte
            overwrite_size = max(file_size, 1)
            random_data = os.urandom(overwrite_size)
            file_path.write_bytes(random_data)
            overwrite_ok = True
        except OSError as exc:
            _logger.warning(
                "destroy_all: cannot overwrite %r: %s — attempting unlink anyway",
                str(file_path),
                exc,
            )

        try:
            file_path.unlink(missing_ok=True)
        except (PermissionError, OSError) as exc:
            _logger.warning(
                "destroy_all: cannot unlink %r: %s",
                str(file_path),
                exc,
            )
            report.failed_files.append((str(file_path), str(exc)))
            return

        report.destroyed_files.append(
            DestructionEntry(
                file_path=str(file_path),
                overwrite_confirmed=overwrite_ok,
            )
        )
