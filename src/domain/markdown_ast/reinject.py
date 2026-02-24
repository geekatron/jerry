# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
L2-REINJECT comment parser for Jerry Framework rule files.

Provides types and functions to parse, extract, and modify L2-REINJECT HTML
comment directives embedded in Jerry markdown files. These directives carry
structured metadata used by Jerry's L2 enforcement layer to re-inject critical
rules into every LLM prompt, making them immune to context rot.

Format example::

    <!-- L2-REINJECT: rank=1, tokens=50, content="Constitutional: No recursive
    subagents (P-003). User decides, never override (P-020)." -->

    <!-- L2-REINJECT: rank=2, content="UV only for Python (H-05)." -->

Security constraints:
    - Trusted path whitelist (M-22): directives from untrusted file paths
      are silently excluded when ``file_path`` is provided.
    - Case-insensitive matching for ``L2-REINJECT:`` prefix.
    - ``tokens=`` field is optional (many production directives omit it).

References:
    - ST-003: L2-REINJECT Parser
    - ADR-PROJ005-003 Mitigation M-22 (Trusted Path Whitelist)
    - H-07: Domain layer constraint (no external infra/interface imports)
    - H-11: Type hints REQUIRED on all public functions
    - H-12: Docstrings REQUIRED on all public functions/classes/modules

Exports:
    TRUSTED_REINJECT_PATHS: Tuple of trusted path prefixes for L2-REINJECT directives.
    ReinjectDirective: Frozen dataclass representing a parsed L2-REINJECT comment.
    extract_reinject_directives: Extract all directives from a JerryDocument.
    modify_reinject_directive: Return a new document with one directive modified.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass

from src.domain.markdown_ast.jerry_document import JerryDocument

# ---------------------------------------------------------------------------
# Trusted path whitelist (M-22, WI-019)
# ---------------------------------------------------------------------------

TRUSTED_REINJECT_PATHS: tuple[str, ...] = (
    ".context/rules/",
    ".claude/rules/",
    "CLAUDE.md",
)
"""Path prefixes (or exact filenames) from which L2-REINJECT directives are trusted.

Directives from untrusted paths are silently excluded when ``file_path`` is
provided to ``extract_reinject_directives()``.
"""

# ---------------------------------------------------------------------------
# Regex pattern
# ---------------------------------------------------------------------------

# Matches a full L2-REINJECT HTML comment on a single line.
# Case-insensitive for "L2-REINJECT:" prefix.
# tokens= field is optional (many production directives omit it).
# Groups:
#   1 - rank  (integer string)
#   2 - tokens (integer string or None if omitted)
#   3 - content (everything inside the outer double-quotes; may contain \" escapes)
_REINJECT_PATTERN: re.Pattern[str] = re.compile(
    r'<!--\s*L2-REINJECT:\s*rank=(\d+),\s*(?:tokens=(\d+),\s*)?content="((?:[^"\\]|\\.)*)"\s*-->',
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ReinjectDirective:
    """
    A parsed L2-REINJECT HTML comment directive.

    Immutable value object representing a single L2-REINJECT comment extracted
    from a Jerry rule file. Carries all structured fields plus provenance
    information (line number and the original raw comment text) to support
    reliable write-back.

    Attributes:
        rank: Integer priority rank. Lower values are injected first.
        tokens: Estimated token count of the content string.
        content: The reinject payload string (outer quotes stripped, escape
            sequences preserved as-is from the source).
        line_number: Zero-based line index of the directive in the source text.
        raw_text: The full original comment string including ``<!--`` and ``-->``.

    Examples:
        >>> d = ReinjectDirective(rank=1, tokens=50, content="Rule text.", line_number=5,
        ...                       raw_text='<!-- L2-REINJECT: rank=1, tokens=50, content="Rule text." -->')
        >>> d.rank
        1
        >>> d.content
        'Rule text.'
    """

    rank: int
    tokens: int
    content: str
    line_number: int
    raw_text: str


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------


def extract_reinject_directives(
    doc: JerryDocument,
    file_path: str | None = None,
) -> list[ReinjectDirective]:
    """
    Extract all L2-REINJECT directives from a JerryDocument.

    Scans the document source line by line using the canonical L2-REINJECT
    regex pattern (case-insensitive). HTML comments that do not match the
    L2-REINJECT format are silently ignored.

    When ``file_path`` is provided, directives are only returned if the
    file path is within the trusted path whitelist (``TRUSTED_REINJECT_PATHS``).
    Directives from untrusted paths are silently excluded (M-22).
    When ``file_path`` is ``None``, no trust check is performed (backward
    compatible).

    Directives are returned in document order (ascending line number).

    Args:
        doc: A JerryDocument whose source will be searched for L2-REINJECT
            comments. May be empty; returns an empty list in that case.
        file_path: Optional file path for trust checking. When provided,
            directives are excluded from untrusted paths. When ``None``
            (default), no trust check is applied.

    Returns:
        A list of ReinjectDirective instances, one per matched comment, in
        document order. Returns an empty list if no L2-REINJECT comments are
        found or the file is untrusted.

    Examples:
        >>> doc = JerryDocument.parse('<!-- L2-REINJECT: rank=1, tokens=10, content="Hi." -->\\n')
        >>> directives = extract_reinject_directives(doc)
        >>> len(directives)
        1
        >>> directives[0].rank
        1
    """
    # --- Trusted path check (M-22, WI-019) ---
    if file_path is not None and not _is_trusted_path(file_path):
        return []

    directives: list[ReinjectDirective] = []
    for line_number, line in enumerate(doc.source.splitlines()):
        match = _REINJECT_PATTERN.search(line)
        if match:
            rank = int(match.group(1))
            tokens_str = match.group(2)
            tokens_val = int(tokens_str) if tokens_str is not None else 0
            content = match.group(3)
            raw_text = match.group(0)
            directives.append(
                ReinjectDirective(
                    rank=rank,
                    tokens=tokens_val,
                    content=content,
                    line_number=line_number,
                    raw_text=raw_text,
                )
            )
    return directives


def modify_reinject_directive(
    doc: JerryDocument,
    index: int,
    *,
    rank: int | None = None,
    tokens: int | None = None,
    content: str | None = None,
) -> JerryDocument:
    """
    Return a new JerryDocument with one L2-REINJECT directive modified.

    Locates the directive at ``index`` in document order, applies the requested
    field overrides, rebuilds the raw comment string, substitutes it in the
    source text, and re-parses the result. All other directives and all
    non-L2-REINJECT HTML comments are left unchanged.

    This function is immutable: the original ``doc`` is never modified.

    Args:
        doc: The source JerryDocument. Must contain at least ``index + 1``
            L2-REINJECT directives.
        index: Zero-based index of the directive to modify (document order).
        rank: New rank value. If None, the existing rank is kept.
        tokens: New tokens value. If None, the existing tokens value is kept.
        content: New content string. If None, the existing content is kept.
            Do not include surrounding double-quotes; they are added automatically.

    Returns:
        A new JerryDocument parsed from the modified source text.

    Raises:
        IndexError: If ``index`` is out of range for the number of directives
            present in ``doc``.

    Examples:
        >>> doc = JerryDocument.parse('<!-- L2-REINJECT: rank=1, tokens=10, content="Old." -->\\n')
        >>> new_doc = modify_reinject_directive(doc, 0, rank=5)
        >>> extract_reinject_directives(new_doc)[0].rank
        5
    """
    directives = extract_reinject_directives(doc)

    if index < 0 or index >= len(directives):
        raise IndexError(
            f"Directive index {index} is out of range; document contains {len(directives)} directive(s)."
        )

    target = directives[index]

    new_rank = rank if rank is not None else target.rank
    new_tokens = tokens if tokens is not None else target.tokens
    new_content = content if content is not None else target.content

    new_raw = f'<!-- L2-REINJECT: rank={new_rank}, tokens={new_tokens}, content="{new_content}" -->'

    modified_source = doc.source.replace(target.raw_text, new_raw, 1)
    return JerryDocument.parse(modified_source)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _is_trusted_path(file_path: str) -> bool:
    """Check if a file path is within the trusted path whitelist (M-22).

    Normalizes the path to forward slashes and checks against
    ``TRUSTED_REINJECT_PATHS``. For directory prefixes, checks if the
    normalized path contains the prefix. For exact filenames (no trailing
    slash), checks if the path ends with the filename.

    Args:
        file_path: The file path to check (relative or absolute).

    Returns:
        ``True`` if the path is trusted, ``False`` otherwise.
    """
    normalized = file_path.replace(os.sep, "/")

    # Strip leading ./ if present
    if normalized.startswith("./"):
        normalized = normalized[2:]

    for trusted in TRUSTED_REINJECT_PATHS:
        if trusted.endswith("/"):
            # Directory prefix: check if the path contains this prefix
            if trusted in normalized:
                return True
        else:
            # Exact filename: check if path ends with it or equals it
            if normalized == trusted or normalized.endswith("/" + trusted):
                return True

    return False
