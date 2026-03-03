# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Version application handlers."""

from __future__ import annotations

from .queries.detect_bump_type_query_handler import DetectBumpTypeQueryHandler

__all__ = [
    "DetectBumpTypeQueryHandler",
]
