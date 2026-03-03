# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Version - Bounded Context for conventional commit version bump detection.

Provides case-insensitive parsing of conventional commits and
determination of the appropriate semantic version bump type.

References:
    - BUG-002: Version bump regex rejects uppercase scopes
    - Conventional Commits v1.0.0 specification
"""

from __future__ import annotations
