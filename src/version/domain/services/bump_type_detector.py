# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BumpTypeDetector domain service.

Pure service that determines the highest-severity version bump type
from a collection of commit subjects and optional commit bodies.

References:
    - BUG-002: Version bump regex rejects uppercase scopes
    - Conventional Commits v1.0.0 specification
"""

from __future__ import annotations

import re

from src.version.domain.value_objects.bump_type import BumpType
from src.version.domain.value_objects.conventional_commit import ConventionalCommit

# Case-insensitive pattern for BREAKING CHANGE footer in commit body.
# ReDoS safety: anchored to start of line, no nested quantifiers.
_BREAKING_CHANGE_FOOTER = re.compile(
    r"^BREAKING[ -]CHANGE:\s*",
    re.IGNORECASE | re.MULTILINE,
)


class BumpTypeDetector:
    """Determines the highest-severity version bump from commit messages.

    This is a pure domain service with no infrastructure dependencies.
    It accepts commit subjects and bodies as strings and returns the
    appropriate BumpType.
    """

    def detect(
        self,
        subjects: list[str],
        bodies: list[str] | None = None,
    ) -> BumpType:
        """Detect the highest-severity bump type from commit messages.

        Scans all subjects for conventional commit patterns and all
        bodies for BREAKING CHANGE footers. Returns the highest-severity
        bump found.

        Args:
            subjects: List of commit subject lines.
            bodies: Optional list of full commit bodies (for BREAKING CHANGE
                footer detection). May be shorter than subjects.

        Returns:
            The highest-severity BumpType found across all commits.
            Returns BumpType.NONE if no bump-worthy commits exist.
        """
        if not subjects:
            return BumpType.NONE

        highest = BumpType.NONE

        # Check subjects for conventional commit patterns
        for subject in subjects:
            try:
                commit = ConventionalCommit.parse(subject)
            except Exception:
                # Non-conventional commits don't trigger bumps
                continue

            if commit.bump_type > highest:
                highest = commit.bump_type

            # Short-circuit: can't go higher than MAJOR
            if highest == BumpType.MAJOR:
                return highest

        # Check bodies for BREAKING CHANGE footer
        if bodies and highest < BumpType.MAJOR:
            for body in bodies:
                if _BREAKING_CHANGE_FOOTER.search(body):
                    return BumpType.MAJOR

        return highest
