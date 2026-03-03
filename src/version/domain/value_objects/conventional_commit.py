# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ConventionalCommit value object for parsing commit subjects.

Parses conventional commit subjects with case-insensitive matching
per Conventional Commits v1.0.0 specification.

References:
    - BUG-002: Version bump regex rejects uppercase scopes
    - Conventional Commits v1.0.0: https://www.conventionalcommits.org/en/v1.0.0/
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from src.version.domain.exceptions import CommitParseError
from src.version.domain.value_objects.bump_type import BumpType

# Compiled regex with IGNORECASE for case-insensitive matching.
# Pattern breakdown:
#   ^(?P<type>[a-z]+)        - commit type (feat, fix, etc.)
#   (?:\((?P<scope>[^)]+)\))? - optional scope in parentheses
#   (?P<breaking>!)?         - optional breaking change indicator
#   :\s*                     - colon separator with optional whitespace
#   (?P<description>.+)$    - description (rest of the line)
#
# ReDoS safety: No nested quantifiers. All groups are bounded.
# The scope group uses [^)]+ (no nesting) and the description uses .+
# anchored to $ (linear scan).
_COMMIT_PATTERN = re.compile(
    r"^(?P<type>[a-z]+)"
    r"(?:\((?P<scope>[^)]+)\))?"
    r"(?P<breaking>!)?"
    r":\s*"
    r"(?P<description>.+)$",
    re.IGNORECASE,
)

# Commit types that trigger version bumps (case-insensitive comparison)
_MINOR_TYPES = frozenset({"feat"})
_PATCH_TYPES = frozenset({"fix", "perf"})


@dataclass(frozen=True)
class ConventionalCommit:
    """Immutable representation of a parsed conventional commit subject.

    Attributes:
        commit_type: The commit type (e.g., 'feat', 'fix', 'docs').
            Stored as lowercase regardless of input case.
        scope: Optional scope (e.g., 'ci', 'GH-122'). Preserved as-is.
        is_breaking: Whether the commit includes '!' breaking indicator.
        description: The commit description text.
    """

    commit_type: str
    scope: str | None
    is_breaking: bool
    description: str

    @classmethod
    def parse(cls, subject: str) -> ConventionalCommit:
        """Parse a conventional commit subject line.

        Case-insensitive: 'feat', 'FEAT', and 'Feat' all match.
        Scope characters are unrestricted (anything except closing paren).

        Args:
            subject: The commit subject line to parse.

        Returns:
            Parsed ConventionalCommit instance.

        Raises:
            CommitParseError: If the subject does not match conventional
                commit format.
        """
        subject = subject.strip()
        if not subject:
            raise CommitParseError(subject, "empty commit subject")

        match = _COMMIT_PATTERN.match(subject)
        if match is None:
            raise CommitParseError(subject, "does not match conventional commit format")

        return cls(
            commit_type=match.group("type").lower(),
            scope=match.group("scope"),
            is_breaking=match.group("breaking") is not None,
            description=match.group("description"),
        )

    @property
    def bump_type(self) -> BumpType:
        """Determine the version bump type for this commit.

        Precedence: breaking change (MAJOR) > feat (MINOR) > fix/perf (PATCH) > other (NONE).

        Returns:
            The appropriate BumpType for this commit.
        """
        if self.is_breaking:
            return BumpType.MAJOR
        if self.commit_type in _MINOR_TYPES:
            return BumpType.MINOR
        if self.commit_type in _PATCH_TYPES:
            return BumpType.PATCH
        return BumpType.NONE
