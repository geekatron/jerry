# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""FormattingVariant enumeration for MR-004 Formatting Perturbation.

Extracted to a separate file per H-10 (one class per file).

Domain isolation: MUST NOT import DeepEval, promptfoo, or any adapter (H-07).
"""

from __future__ import annotations

from enum import Enum


class FormattingVariant(str, Enum):
    """Enumeration of supported formatting transformation variants.

    Corresponds to the transformation variants listed in behavioral-contracts.md
    Section C.4.
    """

    MARKDOWN_TO_PLAIN = "markdown_to_plain"
    BULLETS_TO_NUMBERED = "bullets_to_numbered"
    REMOVE_CODE_BLOCKS = "remove_code_blocks"
    TABLES_TO_PROSE = "tables_to_prose"
