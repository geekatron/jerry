# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
HtmlCommentMetadata - HTML comment metadata extraction from markdown files.

Extracts structured metadata from HTML comments using the pipe-separated
``key: value`` pattern found in ADRs, strategy templates, and orchestration
artifacts (e.g., ``<!-- PS-ID: val | ENTRY: val | AGENT: val -->``).

Distinguishes from L2-REINJECT comments (handled by ``reinject.py``) using
a case-insensitive negative lookahead.

Security constraints:
    - First ``-->`` termination (M-13, T-HC-03 CWE-74)
    - Non-greedy matching (no ``[^>]*`` bug)
    - Case-insensitive L2-REINJECT exclusion (T-HC-04 CWE-94, T-HC-07 CWE-284)
    - Comment count enforcement (M-16)
    - Value length enforcement (M-17)
    - Control character stripping (M-18)
    - Sanitized error messages (M-19)

References:
    - ADR-PROJ005-003 Design Decision 7 (HtmlCommentMetadata Implementation)
    - Threat Model: M-13, M-16, M-17, M-18, M-19
    - H-07: Domain layer constraint (no external infra/interface imports)
    - H-10: Supporting frozen dataclasses (HtmlCommentField, HtmlCommentBlock,
      HtmlCommentResult) are co-located with primary class per ADR.

Exports:
    HtmlCommentField: Frozen dataclass for a single key-value pair.
    HtmlCommentBlock: Frozen dataclass for a single comment block.
    HtmlCommentResult: Frozen dataclass for the extraction result.
    HtmlCommentMetadata: Extractor class with static ``extract()`` method.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from src.domain.markdown_ast.input_bounds import InputBounds
from src.domain.markdown_ast.jerry_document import JerryDocument

# ---------------------------------------------------------------------------
# HTML comment extraction pattern (DD-7)
# Matches HTML comments containing at least one key: value pair.
# Case-insensitive negative lookahead excludes L2-REINJECT comments.
# Non-greedy .*? to first --> (M-13, not [^>]*)
# ---------------------------------------------------------------------------
_METADATA_COMMENT_PATTERN = re.compile(
    r"<!--\s*"
    r"(?!L2-REINJECT:)"  # Negative lookahead (case-insensitive via _is_reinject)
    r"(?P<body>.*?)"  # Non-greedy body to first -->
    r"\s*-->",
    re.DOTALL,
)

# Key-value pair pattern within a comment body (pipe-separated)
_KV_PATTERN = re.compile(
    r"(?P<key>[A-Za-z][A-Za-z0-9_-]*)\s*:\s*(?P<value>[^|]*?)(?:\s*\||$)"
)

# Control character pattern (M-18)
_CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

# Case-insensitive L2-REINJECT check for body content
_REINJECT_PREFIX_RE = re.compile(r"^\s*L2-REINJECT:", re.IGNORECASE)


@dataclass(frozen=True)
class HtmlCommentField:
    """Single key-value pair from an HTML comment metadata block.

    Attributes:
        key: The field name (e.g., ``"PS-ID"``, ``"VERSION"``).
        value: The field value as a string.
        line_number: Zero-based line number of the containing comment.
    """

    key: str
    value: str
    line_number: int


@dataclass(frozen=True)
class HtmlCommentBlock:
    """A single HTML comment metadata block with its parsed fields.

    Attributes:
        fields: Parsed key-value pairs as a tuple (immutable).
        raw_comment: The raw comment text including ``<!--`` and ``-->``.
        line_number: Zero-based line number of the comment start.
    """

    fields: tuple[HtmlCommentField, ...]
    raw_comment: str
    line_number: int


@dataclass(frozen=True)
class HtmlCommentResult:
    """Complete HTML comment metadata extraction result.

    Attributes:
        blocks: Extracted comment blocks as a tuple (immutable).
        parse_error: ``None`` if extraction succeeded; error message otherwise.
        parse_warnings: Warnings (e.g., value truncation).
    """

    blocks: tuple[HtmlCommentBlock, ...]
    parse_error: str | None
    parse_warnings: tuple[str, ...] = ()


def _strip_control_chars(value: str) -> str:
    """Strip null bytes and non-printable control characters (M-18).

    Preserves ``\\n``, ``\\r``, ``\\t``.

    Args:
        value: The string to sanitize.

    Returns:
        The sanitized string.
    """
    return _CONTROL_CHAR_RE.sub("", value)


class HtmlCommentMetadata:
    """Extract structured metadata from HTML comments in markdown files.

    Parses ``<!-- KEY: value | KEY: value -->`` patterns. Excludes
    L2-REINJECT comments (case-insensitive) to avoid duplication with
    ``reinject.py``.
    """

    @staticmethod
    def extract(
        doc: JerryDocument,
        bounds: InputBounds | None = None,
    ) -> HtmlCommentResult:
        """Extract HTML comment metadata blocks from a JerryDocument.

        Args:
            doc: The parsed markdown document.
            bounds: Resource limits. Defaults to ``InputBounds.DEFAULT``.

        Returns:
            An ``HtmlCommentResult`` with extracted blocks or error info.
        """
        if bounds is None:
            bounds = InputBounds.DEFAULT

        source = doc.source
        warnings: list[str] = []
        blocks: list[HtmlCommentBlock] = []

        if not source:
            return HtmlCommentResult(
                blocks=(),
                parse_error=None,
            )

        # Pre-compute line start offsets for line number calculation
        line_starts = _compute_line_starts(source)

        for match in _METADATA_COMMENT_PATTERN.finditer(source):
            body = match.group("body")

            # --- Case-insensitive L2-REINJECT exclusion ---
            # The regex negative lookahead handles exact "L2-REINJECT:" prefix,
            # but we also check case-insensitively for variants like
            # "l2-reinject:", "L2-Reinject:", etc.
            if _REINJECT_PREFIX_RE.match(body):
                continue

            # --- Comment count check (M-16) ---
            if len(blocks) >= bounds.max_comment_count:
                return HtmlCommentResult(
                    blocks=tuple(blocks),
                    parse_error=(
                        f"Comment count exceeds maximum "
                        f"({bounds.max_comment_count})"
                    ),
                    parse_warnings=tuple(warnings),
                )

            # --- Parse key-value pairs ---
            fields: list[HtmlCommentField] = []
            line_number = _offset_to_line(line_starts, match.start())

            for kv_match in _KV_PATTERN.finditer(body):
                key = kv_match.group("key").strip()
                value = kv_match.group("value").strip()

                # Control character stripping (M-18)
                key = _strip_control_chars(key)
                value = _strip_control_chars(value)

                # Value length check (M-17)
                if len(value) > bounds.max_value_length:
                    warnings.append(
                        f"Value for key '{key}' truncated "
                        f"({len(value)} > {bounds.max_value_length} chars)"
                    )
                    value = value[: bounds.max_value_length]

                fields.append(
                    HtmlCommentField(
                        key=key,
                        value=value,
                        line_number=line_number,
                    )
                )

            # Only include blocks that have at least one key-value pair
            if fields:
                raw_comment = match.group(0)
                blocks.append(
                    HtmlCommentBlock(
                        fields=tuple(fields),
                        raw_comment=raw_comment,
                        line_number=line_number,
                    )
                )

        return HtmlCommentResult(
            blocks=tuple(blocks),
            parse_error=None,
            parse_warnings=tuple(warnings),
        )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _compute_line_starts(source: str) -> list[int]:
    """Compute the character offsets of each line start in source.

    Args:
        source: The source text to index.

    Returns:
        A list where index i contains the character offset of line i's start.
    """
    offsets = [0]
    for i, ch in enumerate(source):
        if ch == "\n":
            offsets.append(i + 1)
    return offsets


def _offset_to_line(line_starts: list[int], offset: int) -> int:
    """Return the zero-based line number for a character offset.

    Args:
        line_starts: Sorted list of line start offsets.
        offset: Character offset to map to a line number.

    Returns:
        Zero-based line number.
    """
    import bisect

    idx = bisect.bisect_right(line_starts, offset)
    return max(0, idx - 1)
