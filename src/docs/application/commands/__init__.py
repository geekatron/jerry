# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Docs application commands.

This module provides command data classes for the docs skill.

References:
    - doc-module-spec.md Section: CLI Integration
    - PROJ-0037: Auto-Documentation Module
"""

from __future__ import annotations

from .generate_docs_command import GenerateDocsCommand

__all__ = ["GenerateDocsCommand"]
