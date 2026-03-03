# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
DetectBumpTypeQueryHandler for version bump detection.

Constructor-injected handler that delegates to the domain service.

References:
    - BUG-002: Version bump regex rejects uppercase scopes
"""

from __future__ import annotations

from src.version.application.ports.commit_log_reader import ICommitLogReader
from src.version.domain.services.bump_type_detector import BumpTypeDetector
from src.version.domain.value_objects.bump_type import BumpType


class DetectBumpTypeQueryHandler:
    """Handles version bump type detection queries.

    Reads commits via the injected ICommitLogReader port and delegates
    bump type determination to the BumpTypeDetector domain service.
    """

    def __init__(
        self,
        commit_reader: ICommitLogReader,
        detector: BumpTypeDetector,
    ) -> None:
        """Initialize with injected dependencies.

        Args:
            commit_reader: Port for reading commit history.
            detector: Domain service for determining bump type.
        """
        self._commit_reader = commit_reader
        self._detector = detector

    def handle(
        self,
        since_tag: str | None = None,
        range_spec: str | None = None,
    ) -> BumpType:
        """Execute bump type detection.

        Args:
            since_tag: Read commits since this tag.
            range_spec: Git range spec (e.g., 'v0.22.1..HEAD').

        Returns:
            The highest-severity BumpType found.
        """
        entries = self._commit_reader.read_commits(
            since_tag=since_tag,
            range_spec=range_spec,
        )

        subjects = [e.subject for e in entries]
        bodies = [e.body for e in entries if e.body]

        return self._detector.detect(subjects, bodies if bodies else None)
