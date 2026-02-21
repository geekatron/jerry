# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
StalenessDetector -- Infrastructure adapter for ORCHESTRATION.yaml staleness detection.

Checks whether an ORCHESTRATION.yaml file's ``resumption.recovery_state.updated_at``
timestamp is stale relative to a reference time. Used by the pre-tool-use hook
(EN-006, Phase 4) to warn when orchestration state has not been updated during
the current phase.

Design Principles:
    - **Fail-open everywhere**: If the file is missing, unparseable, or the
      ``updated_at`` field is absent/null/malformed, the service returns a
      passthrough result (no warning, no exception).
    - **Path matching**: Only files whose path ends with ``ORCHESTRATION.yaml``
      are checked. All other paths pass through immediately.

References:
    - EN-005: PreToolUse Staleness Detection
    - EN-006: PreToolUse CLI Integration (Phase 4, future)
    - FEAT-002: Pre-Tool-Use Hooks
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

import yaml

from src.context_monitoring.domain.value_objects.staleness_result import (
    StalenessResult,
)

_ORCHESTRATION_FILENAME = "ORCHESTRATION.yaml"

_PASSTHROUGH = StalenessResult(is_stale=False)


class StalenessDetector:
    """Infrastructure adapter that detects stale ORCHESTRATION.yaml files.

    Reads the ORCHESTRATION.yaml file relative to a project root directory
    and compares its ``resumption.recovery_state.updated_at`` timestamp
    against a reference time to determine staleness.

    The service is designed to fail-open: any error condition (missing file,
    unparseable YAML, missing field, invalid timestamp) results in a
    passthrough (no warning) rather than an exception.

    Args:
        project_root: The root directory of the project. ORCHESTRATION.yaml
            paths are resolved relative to this directory.

    Example:
        >>> from pathlib import Path
        >>> from datetime import datetime, timezone
        >>> detector = StalenessDetector(project_root=Path("/my/project"))
        >>> result = detector.check_staleness(
        ...     tool_target_path="ORCHESTRATION.yaml",
        ...     reference_time=datetime(2026, 2, 19, 8, 0, 0, tzinfo=timezone.utc),
        ... )
        >>> result.is_stale
        False
    """

    def __init__(self, project_root: Path) -> None:
        """Initialize the staleness detector.

        Args:
            project_root: The root directory of the project. ORCHESTRATION.yaml
                paths are resolved relative to this directory.
        """
        self._project_root = project_root

    def check_staleness(
        self,
        tool_target_path: str,
        reference_time: datetime,
    ) -> StalenessResult:
        """Check whether an ORCHESTRATION.yaml file is stale.

        Performs the following steps:
        1. If ``tool_target_path`` does not end with ``ORCHESTRATION.yaml``,
           returns a passthrough (no warning).
        2. Resolves the file path relative to ``project_root``.
        3. Reads and parses the YAML content.
        4. Extracts ``resumption.recovery_state.updated_at``.
        5. Compares the timestamp against ``reference_time``.
        6. Returns a staleness warning if ``updated_at`` is older than
           ``reference_time``, or passthrough otherwise.

        All error conditions fail-open (return passthrough, no exception).

        Args:
            tool_target_path: The path of the file being targeted by the
                tool call. May be absolute or relative.
            reference_time: The reference timestamp to compare against
                (e.g., phase start time). Must be timezone-aware.

        Returns:
            A ``StalenessResult`` indicating whether the file is stale.
        """
        if not self._is_orchestration_path(tool_target_path):
            return _PASSTHROUGH

        return self._evaluate_staleness(tool_target_path, reference_time)

    def _is_orchestration_path(self, tool_target_path: str) -> bool:
        """Check if the path targets an ORCHESTRATION.yaml file.

        Args:
            tool_target_path: The path to check.

        Returns:
            True if the path ends with ORCHESTRATION.yaml, False otherwise.
        """
        # Use PurePosixPath to handle both forward and back slashes
        # and extract the filename reliably.
        posix_path = PurePosixPath(tool_target_path)
        return posix_path.name == _ORCHESTRATION_FILENAME

    def _evaluate_staleness(
        self,
        tool_target_path: str,
        reference_time: datetime,
    ) -> StalenessResult:
        """Evaluate staleness of a confirmed ORCHESTRATION.yaml path.

        Fail-open: any exception results in a passthrough.

        Args:
            tool_target_path: The path to the ORCHESTRATION.yaml file.
            reference_time: The reference timestamp.

        Returns:
            A ``StalenessResult`` with staleness determination.
        """
        try:
            return self._do_evaluate(tool_target_path, reference_time)
        except Exception:  # noqa: BLE001 -- Fail-open by design
            return _PASSTHROUGH

    def _do_evaluate(
        self,
        tool_target_path: str,
        reference_time: datetime,
    ) -> StalenessResult:
        """Perform the actual staleness evaluation.

        Args:
            tool_target_path: The path to the ORCHESTRATION.yaml file.
            reference_time: The reference timestamp.

        Returns:
            A ``StalenessResult`` with the staleness determination.

        Raises:
            Any exception -- caller is responsible for fail-open handling.
        """
        file_path = self._resolve_file_path(tool_target_path)

        if not file_path.is_file():
            return _PASSTHROUGH

        content = file_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)

        if not isinstance(data, dict):
            return _PASSTHROUGH

        updated_at_str = self._extract_updated_at(data)
        if not updated_at_str:
            return _PASSTHROUGH

        updated_at_dt = self._parse_iso_timestamp(updated_at_str)
        if updated_at_dt is None:
            return _PASSTHROUGH

        if updated_at_dt >= reference_time:
            return _PASSTHROUGH

        return StalenessResult(
            is_stale=True,
            warning_message=(
                f"ORCHESTRATION.yaml recovery state is stale. "
                f"updated_at={updated_at_str} is older than "
                f"reference_time={reference_time.isoformat()}. "
                f"Consider updating resumption.recovery_state.updated_at."
            ),
            updated_at=updated_at_str,
            reference_time=reference_time.isoformat(),
        )

    def _resolve_file_path(self, tool_target_path: str) -> Path:
        """Resolve the tool target path to an absolute file path.

        If the path is already absolute, uses it directly.
        Otherwise resolves relative to project_root.

        Args:
            tool_target_path: The path from the tool call.

        Returns:
            The resolved absolute path.
        """
        target = Path(tool_target_path)
        if target.is_absolute():
            return target
        return self._project_root / tool_target_path

    def _extract_updated_at(self, data: dict) -> str | None:
        """Extract the updated_at value from parsed ORCHESTRATION.yaml data.

        Navigates: ``resumption.recovery_state.updated_at``

        Args:
            data: Parsed YAML data as a dictionary.

        Returns:
            The updated_at string value, or None if not found or not a string.
        """
        resumption = data.get("resumption")
        if not isinstance(resumption, dict):
            return None

        recovery_state = resumption.get("recovery_state")
        if not isinstance(recovery_state, dict):
            return None

        updated_at = recovery_state.get("updated_at")
        if not isinstance(updated_at, str) or not updated_at:
            return None

        return updated_at

    def _parse_iso_timestamp(self, timestamp_str: str) -> datetime | None:
        """Parse an ISO 8601 timestamp string to a timezone-aware datetime.

        Args:
            timestamp_str: An ISO 8601 timestamp string.

        Returns:
            A timezone-aware datetime, or None if parsing fails.
        """
        try:
            dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            # Ensure timezone-aware
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except (ValueError, AttributeError):
            return None
