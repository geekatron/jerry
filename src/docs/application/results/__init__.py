# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Docs application results.

This module provides result data classes for docs commands.

References:
    - doc-module-spec.md Section: CLI Integration
    - PROJ-0037: Auto-Documentation Module
"""

from __future__ import annotations

from .generate_docs_result import GenerateDocsResult

__all__ = ["GenerateDocsResult"]
