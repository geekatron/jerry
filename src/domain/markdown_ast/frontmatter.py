# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BlockquoteFrontmatter - Jerry-style blockquote frontmatter extraction and write-back.

Provides structured access to the `> **Key:** Value` metadata pattern used in
Jerry entity files (worktracker items, skill definitions, spike entities, enabler
entities, etc.).

The frontmatter format validated in EN-001 R-01 PoC:
    > **Type:** story
    > **Status:** pending
    > **Priority:** high
    > **Effort:** 5

Write-back strategy (from R-01 PoC):
    - Operate at source-text level using regex substitution, NOT at the AST level.
    - set() normalizes via doc.render() before substitution to ensure idempotent results.
    - All mutation operations return a new JerryDocument rather than modifying in place.

References:
    - ST-002: Blockquote Frontmatter Extension
    - EN-001: R-01 PoC (frontmatter regex validation)
    - ST-001: JerryDocument facade (dependency)
    - H-07: Domain layer MUST NOT import application/infrastructure/interface layers

Exports:
    FrontmatterField: Dataclass representing a single frontmatter key-value pair.
    BlockquoteFrontmatter: Collection class for Jerry blockquote frontmatter.
    extract_frontmatter: Convenience function to extract frontmatter from a JerryDocument.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass

from src.domain.markdown_ast.jerry_document import JerryDocument

# ---------------------------------------------------------------------------
# Regex pattern (validated in EN-001 R-01 PoC)
# ---------------------------------------------------------------------------

_FRONTMATTER_PATTERN = re.compile(r"^>\s*\*\*(?P<key>[^*:]+):\*\*\s*(?P<value>.+)$", re.MULTILINE)


# ---------------------------------------------------------------------------
# FrontmatterField dataclass
# ---------------------------------------------------------------------------


@dataclass
class FrontmatterField:
    """
    A single key-value field extracted from a Jerry blockquote frontmatter.

    Represents one line of the form `> **Key:** Value` with its associated
    position metadata in the source text.

    Attributes:
        key: The field name (e.g., "Status", "Type", "Effort").
        value: The field value as a string (e.g., "pending", "story", "5").
        line_number: Zero-based line number in the source where this field appears.
        start: Character offset of the start of the full match in the source.
        end: Character offset of the end of the full match in the source.

    Examples:
        >>> field = FrontmatterField(key="Status", value="pending", line_number=2, start=10, end=30)
        >>> field.key
        'Status'
        >>> field.value
        'pending'
    """

    key: str
    value: str
    line_number: int
    start: int
    end: int


# ---------------------------------------------------------------------------
# BlockquoteFrontmatter collection class
# ---------------------------------------------------------------------------


class BlockquoteFrontmatter:
    """
    Collection of key-value fields extracted from a Jerry entity blockquote frontmatter.

    Provides dict-like read access to frontmatter fields and write-back operations
    that return new JerryDocument instances with modified source text.

    The frontmatter pattern extracted is: `> **Key:** Value`

    All mutation operations (set, add) are immutable -- they return a new
    JerryDocument rather than modifying the current document in place.

    The `set()` and `add()` methods operate on the mdformat-normalized source
    (via `doc.render()`) to ensure idempotent write-back results. Callers should
    be aware that the rendered source may differ from the original raw source in
    whitespace normalization.

    Attributes:
        _fields: Ordered list of FrontmatterField instances in document order.
        _doc: The JerryDocument this frontmatter was extracted from.

    Examples:
        >>> doc = JerryDocument.parse("> **Status:** pending\\n")
        >>> fm = BlockquoteFrontmatter.extract(doc)
        >>> fm.get("Status")
        'pending'
        >>> new_doc = fm.set("Status", "in-progress")
        >>> BlockquoteFrontmatter.extract(new_doc).get("Status")
        'in-progress'
    """

    def __init__(self, fields: list[FrontmatterField], doc: JerryDocument) -> None:
        """
        Initialize a BlockquoteFrontmatter collection.

        Prefer BlockquoteFrontmatter.extract() or extract_frontmatter() for
        constructing instances from a JerryDocument.

        Args:
            fields: Ordered list of FrontmatterField instances.
            doc: The JerryDocument from which these fields were extracted.
        """
        self._fields = fields
        self._doc = doc
        # Index for O(1) key lookup; last value wins for duplicate keys
        self._index: dict[str, int] = {f.key: i for i, f in enumerate(fields)}

    @classmethod
    def extract(cls, doc: JerryDocument) -> BlockquoteFrontmatter:
        """
        Extract blockquote frontmatter from a JerryDocument.

        Scans the document source for lines matching the Jerry frontmatter
        pattern `> **Key:** Value` using the validated R-01 regex. Returns
        a BlockquoteFrontmatter containing all matched fields in document order.

        Args:
            doc: The JerryDocument to extract frontmatter from.

        Returns:
            A BlockquoteFrontmatter instance. Empty (len == 0) if the document
            has no frontmatter or is empty.

        Examples:
            >>> doc = JerryDocument.parse("> **Status:** pending\\n")
            >>> fm = BlockquoteFrontmatter.extract(doc)
            >>> fm.get("Status")
            'pending'
            >>> len(fm)
            1
        """
        fields: list[FrontmatterField] = []
        source = doc.source

        if not source:
            return cls(fields, doc)

        # Pre-compute line start offsets for line_number computation
        line_starts = _compute_line_starts(source)

        for match in _FRONTMATTER_PATTERN.finditer(source):
            key = match.group("key").strip()
            value = match.group("value").strip()
            start = match.start()
            end = match.end()
            line_number = _offset_to_line(line_starts, start)
            fields.append(
                FrontmatterField(
                    key=key,
                    value=value,
                    line_number=line_number,
                    start=start,
                    end=end,
                )
            )

        return cls(fields, doc)

    # ------------------------------------------------------------------
    # Dict-like read access
    # ------------------------------------------------------------------

    def get(self, key: str, default: str | None = None) -> str | None:
        """
        Return the value for a frontmatter key, or a default if not present.

        Args:
            key: The frontmatter field name (case-sensitive).
            default: Value to return if the key is not found. Defaults to None.

        Returns:
            The field value string, or `default` if the key is not present.

        Examples:
            >>> fm.get("Status")
            'pending'
            >>> fm.get("NonExistent")
            None
            >>> fm.get("NonExistent", "fallback")
            'fallback'
        """
        idx = self._index.get(key)
        if idx is None:
            return default
        return self._fields[idx].value

    def get_field(self, key: str) -> FrontmatterField | None:
        """
        Return the FrontmatterField object for a key, or None if not present.

        Unlike ``get()`` which returns only the value string, this returns the
        full FrontmatterField including ``line_number``, ``start``, and ``end``
        metadata.

        Args:
            key: The frontmatter field name (case-sensitive).

        Returns:
            The FrontmatterField instance, or None if the key is not found.

        Examples:
            >>> field = fm.get_field("Status")
            >>> field.line_number
            3
        """
        idx = self._index.get(key)
        if idx is None:
            return None
        return self._fields[idx]

    def __contains__(self, key: object) -> bool:
        """
        Return True if the frontmatter contains the given key.

        Args:
            key: The frontmatter field name to check.

        Returns:
            True if the key exists, False otherwise.

        Examples:
            >>> "Status" in fm
            True
            >>> "Missing" in fm
            False
        """
        return key in self._index

    def __getitem__(self, key: str) -> str:
        """
        Return the value for a frontmatter key.

        Args:
            key: The frontmatter field name (case-sensitive).

        Returns:
            The field value string.

        Raises:
            KeyError: If the key is not present in the frontmatter.

        Examples:
            >>> fm["Status"]
            'pending'
        """
        idx = self._index.get(key)
        if idx is None:
            raise KeyError(key)
        return self._fields[idx].value

    def __len__(self) -> int:
        """
        Return the number of frontmatter fields.

        Returns:
            Integer count of fields.

        Examples:
            >>> len(fm)
            10
        """
        return len(self._fields)

    def keys(self) -> Iterator[str]:
        """
        Iterate over frontmatter field keys in document order.

        Returns:
            An iterator of key strings.

        Examples:
            >>> list(fm.keys())
            ['Type', 'Status', 'Priority', ...]
        """
        return (f.key for f in self._fields)

    def values(self) -> Iterator[str]:
        """
        Iterate over frontmatter field values in document order.

        Returns:
            An iterator of value strings.

        Examples:
            >>> list(fm.values())
            ['story', 'pending', 'high', ...]
        """
        return (f.value for f in self._fields)

    def items(self) -> Iterator[tuple[str, str]]:
        """
        Iterate over (key, value) pairs in document order.

        Returns:
            An iterator of (key, value) string tuples.

        Examples:
            >>> list(fm.items())
            [('Type', 'story'), ('Status', 'pending'), ...]
        """
        return ((f.key, f.value) for f in self._fields)

    # ------------------------------------------------------------------
    # Write-back operations
    # ------------------------------------------------------------------

    def set(self, key: str, value: str) -> JerryDocument:
        """
        Return a new JerryDocument with the specified frontmatter field modified.

        Performs regex substitution on the mdformat-normalized source to replace
        the current value of `key` with `value`. The returned document reflects
        the modification; all other fields and document content are preserved.

        This method is immutable -- the original JerryDocument is never modified.

        Write-back strategy:
            1. Normalize source via doc.render() for idempotent baseline.
            2. Substitute the field value using a targeted regex.
            3. Parse the modified source into a new JerryDocument.

        Args:
            key: The frontmatter field name to modify (case-sensitive).
            value: The new value for the field.

        Returns:
            A new JerryDocument with the field value updated.

        Raises:
            KeyError: If the key does not exist in the frontmatter.

        Examples:
            >>> new_doc = fm.set("Status", "in-progress")
            >>> BlockquoteFrontmatter.extract(new_doc).get("Status")
            'in-progress'
        """
        if key not in self._index:
            raise KeyError(key)

        # Normalize source with mdformat for idempotent write-back.
        # mdformat preserves the > **Key:** Value pattern, so the regex will
        # always find the key in the normalized source if it exists in the raw source.
        normalized = self._doc.render() if self._doc.source else self._doc.source

        # Build field-specific substitution pattern
        pattern = re.compile(
            rf"^(>\s*\*\*{re.escape(key)}:\*\*\s*).+$",
            re.MULTILINE,
        )
        modified, _ = pattern.subn(rf"\g<1>{_escape_replacement(value)}", normalized)

        return JerryDocument.parse(modified)

    def add(self, key: str, value: str) -> JerryDocument:
        """
        Return a new JerryDocument with a new frontmatter field appended.

        Appends `> **key:** value` after the last existing frontmatter field
        if one exists, or prepends it to the source if the document has no
        existing frontmatter.

        This method is immutable -- the original JerryDocument is never modified.

        Args:
            key: The field name to add (case-sensitive).
            value: The field value.

        Returns:
            A new JerryDocument with the new field added.

        Raises:
            ValueError: If the key already exists in the frontmatter.

        Examples:
            >>> new_doc = fm.add("Reviewer", "alice")
            >>> BlockquoteFrontmatter.extract(new_doc).get("Reviewer")
            'alice'
        """
        if key in self._index:
            raise ValueError(f"Key '{key}' already exists in frontmatter. Use set() to modify it.")

        new_line = f"> **{key}:** {value}"
        source = self._doc.source

        if self._fields:
            # Append after the last frontmatter field in the source
            last_field = self._fields[-1]
            # Determine the end position of the last field's line
            # Use the normalized source if the field was found there, else raw
            insert_pos = last_field.end
            modified = source[:insert_pos] + "\n" + new_line + source[insert_pos:]
        else:
            # No existing frontmatter: prepend to document source
            modified = new_line + "\n" + source

        return JerryDocument.parse(modified)


# ---------------------------------------------------------------------------
# Convenience function
# ---------------------------------------------------------------------------


def extract_frontmatter(doc: JerryDocument) -> BlockquoteFrontmatter:
    """
    Extract blockquote frontmatter from a JerryDocument.

    Convenience wrapper around BlockquoteFrontmatter.extract(). Returns a
    BlockquoteFrontmatter containing all `> **Key:** Value` fields found in
    the document source, in document order.

    Args:
        doc: The JerryDocument to extract frontmatter from.

    Returns:
        A BlockquoteFrontmatter instance. Empty (len == 0) if no frontmatter
        is found or the document is empty.

    Examples:
        >>> doc = JerryDocument.parse("> **Status:** pending\\n")
        >>> fm = extract_frontmatter(doc)
        >>> fm.get("Status")
        'pending'
    """
    return BlockquoteFrontmatter.extract(doc)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _compute_line_starts(source: str) -> list[int]:
    """
    Compute the character offsets of each line start in source.

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
    """
    Return the zero-based line number for a character offset using bisect.

    Args:
        line_starts: Sorted list of line start offsets from _compute_line_starts.
        offset: Character offset to map to a line number.

    Returns:
        Zero-based line number.
    """
    import bisect

    idx = bisect.bisect_right(line_starts, offset)
    return max(0, idx - 1)


def _escape_replacement(value: str) -> str:
    """
    Escape backslash sequences in the replacement string for re.sub().

    re.sub() replacement strings treat backslash as special (e.g., \\1 is a
    group reference). This function escapes literal backslashes in user-provided
    values to prevent unintended substitution behavior.

    Args:
        value: The replacement value string.

    Returns:
        The value with backslashes escaped for use in re.sub() replacement.
    """
    return value.replace("\\", "\\\\")
