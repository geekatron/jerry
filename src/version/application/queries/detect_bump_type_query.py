# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
DetectBumpTypeQuery for requesting version bump detection.

References:
    - BUG-002: Version bump regex rejects uppercase scopes
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DetectBumpTypeQuery:
    """Query to detect the appropriate version bump type.

    Exactly one of since_tag, range_spec, or commits_from_stdin should be set.

    Attributes:
        since_tag: If True, detect commits since the latest version tag.
        range_spec: Git range spec (e.g., 'v0.22.1..HEAD').
        commits_from_stdin: If True, read commit subjects from stdin.
    """

    since_tag: bool = False
    range_spec: str | None = None
    commits_from_stdin: bool = False
