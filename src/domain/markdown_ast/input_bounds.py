# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
InputBounds - Centralized resource limits for parser input validation.

Provides a frozen dataclass with configurable upper bounds for all parsers
in the universal markdown parser. Default values are security-conscious;
callers may relax them with documented justification by constructing a
custom InputBounds instance.

All bounds reference specific threat model mitigations (M-XX) from the
PROJ-005 threat model (eng-architect-001-threat-model.md).

References:
    - ADR-PROJ005-003 Design Decision 8 (Input Bounds Enforcement)
    - Threat Model: M-05, M-06, M-07, M-16, M-17, M-20
    - H-07: Domain layer constraint (no external infra/interface imports)

Exports:
    InputBounds: Frozen dataclass with configurable resource limits.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class InputBounds:
    """Configurable resource limits for parser input validation.

    All parsers accept an optional ``InputBounds`` parameter, defaulting to
    ``InputBounds.DEFAULT`` when ``None``. Each field references the threat
    model mitigation that justifies its default value.

    Attributes:
        max_file_bytes: Maximum file size in bytes (M-05). Default 1 MB.
        max_yaml_block_bytes: Maximum YAML block size before parsing (M-07).
            Default 32 KB.
        max_yaml_result_bytes: Maximum serialized result size after
            ``yaml.safe_load()`` (M-20). Closes the temporal gap where
            anchor expansion occurs in memory. Default 64 KB.
        max_alias_count: Maximum YAML anchor/alias references (M-20).
            Pre-parse defense against billion-laughs expansion. Default 10.
        max_frontmatter_keys: Maximum number of frontmatter keys (M-16).
            Default 100.
        max_nesting_depth: Maximum nesting depth for YAML structures (M-06).
            Default 5.
        max_section_count: Maximum XML-tagged sections per document (M-16).
            Default 20.
        max_comment_count: Maximum HTML comment metadata blocks (M-16).
            Default 50.
        max_value_length: Maximum characters per extracted value (M-17).
            Default 10,000.
        max_reinject_count: Maximum L2-REINJECT directives per document (M-16).
            Default 50.
    """

    max_file_bytes: int = 1_048_576
    max_yaml_block_bytes: int = 32_768
    max_yaml_result_bytes: int = 65_536
    max_alias_count: int = 10
    max_frontmatter_keys: int = 100
    max_nesting_depth: int = 5
    max_section_count: int = 20
    max_comment_count: int = 50
    max_value_length: int = 10_000
    max_reinject_count: int = 50

    DEFAULT: ClassVar[InputBounds]


InputBounds.DEFAULT = InputBounds()
