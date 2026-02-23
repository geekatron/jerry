# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
XmlSectionParser - Regex-based extraction of XML-tagged sections.

Extracts XML-tagged sections (``<identity>``, ``<methodology>``, etc.) from
agent definition markdown bodies using regex. Does NOT use any XML parser
library (``xml.etree``, ``lxml``, ``xml.sax``) to eliminate XXE attack surface.

Security constraints:
    - MUST NOT import any XML parser library (M-11, T-XS-07 CWE-611)
    - Non-greedy content matching (M-15)
    - Tag name whitelist validation (ALLOWED_TAGS)
    - Nested same-name tag rejection
    - Section count enforcement (M-16)
    - Content length enforcement (M-17)
    - Control character stripping (M-18)
    - Sanitized error messages (M-19)

References:
    - ADR-PROJ005-003 Design Decision 6 (XmlSectionParser Implementation)
    - Threat Model: M-11, M-15, M-16, M-17, M-18, M-19
    - H-07: Domain layer constraint (no external infra/interface imports)
    - H-10: Supporting frozen dataclasses (XmlSection, XmlSectionResult)
      are co-located with primary class per ADR.

Exports:
    XmlSection: Frozen dataclass for a single XML-tagged section.
    XmlSectionResult: Frozen dataclass for the extraction result.
    XmlSectionParser: Extractor class with static ``extract()`` method.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from src.domain.markdown_ast.input_bounds import InputBounds
from src.domain.markdown_ast.jerry_document import JerryDocument

# ---------------------------------------------------------------------------
# Section extraction pattern (DD-6)
# Built dynamically per allowed tag to avoid consuming unknown wrapper tags
# like <agent> that contain the sections we want to extract.
# ---------------------------------------------------------------------------


def _build_section_pattern(allowed_tags: frozenset[str]) -> re.Pattern[str]:
    """Build a regex pattern that only matches tags in the allowed set.

    This prevents unknown wrapper tags (e.g., ``<agent>``) from consuming
    the entire content including nested allowed tags.

    Args:
        allowed_tags: Set of tag names to match.

    Returns:
        Compiled regex pattern for the allowed tags.
    """
    tags_alternation = "|".join(re.escape(tag) for tag in sorted(allowed_tags))
    return re.compile(
        rf"^<(?P<tag>{tags_alternation})>\s*\n"  # Opening allowed tag
        r"(?P<content>.*?)"  # Non-greedy content capture (M-15)
        r"\n</(?P=tag)>\s*$",  # Matching closing tag
        re.MULTILINE | re.DOTALL,
    )

# ---------------------------------------------------------------------------
# Control character pattern (M-18)
# Strips null bytes and non-printable control characters except \n, \r, \t
# ---------------------------------------------------------------------------
_CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


@dataclass(frozen=True)
class XmlSection:
    """Single XML-tagged section from an agent definition body.

    Attributes:
        tag_name: The tag name (e.g., ``"identity"``, ``"methodology"``).
        content: Text content between opening and closing tags, stripped.
        start_line: Zero-based line of the opening ``<tag>``.
        end_line: Zero-based line of the closing ``</tag>``.
    """

    tag_name: str
    content: str
    start_line: int
    end_line: int


@dataclass(frozen=True)
class XmlSectionResult:
    """Complete XML section extraction result.

    Attributes:
        sections: Extracted sections as a tuple (immutable).
        parse_error: ``None`` if parsing succeeded; error message otherwise.
        parse_warnings: Warnings (e.g., unknown tags skipped).
    """

    sections: tuple[XmlSection, ...]
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


class XmlSectionParser:
    """Extract XML-tagged sections using regex, NOT an XML parser.

    Uses ``re.MULTILINE | re.DOTALL`` with non-greedy matching.
    Validates tag names against ``ALLOWED_TAGS`` whitelist.
    Rejects nested same-name tags within content.
    """

    ALLOWED_TAGS: frozenset[str] = frozenset(
        {
            "identity",
            "purpose",
            "input",
            "capabilities",
            "methodology",
            "output",
            "guardrails",
        }
    )

    @staticmethod
    def extract(
        doc: JerryDocument,
        bounds: InputBounds | None = None,
    ) -> XmlSectionResult:
        """Extract XML-tagged sections from a JerryDocument.

        Args:
            doc: The parsed markdown document.
            bounds: Resource limits. Defaults to ``InputBounds.DEFAULT``.

        Returns:
            An ``XmlSectionResult`` with extracted sections or error info.
        """
        if bounds is None:
            bounds = InputBounds.DEFAULT

        source = doc.source
        warnings: list[str] = []
        sections: list[XmlSection] = []

        if not source:
            return XmlSectionResult(
                sections=(),
                parse_error=None,
            )

        # Pre-compute line start offsets for line number calculation
        line_starts = _compute_line_starts(source)

        pattern = _build_section_pattern(XmlSectionParser.ALLOWED_TAGS)
        for match in pattern.finditer(source):
            tag_name = match.group("tag")
            content = match.group("content")

            # --- Section count check (M-16) ---
            if len(sections) >= bounds.max_section_count:
                return XmlSectionResult(
                    sections=tuple(sections),
                    parse_error=(
                        f"Section count exceeds maximum "
                        f"({bounds.max_section_count})"
                    ),
                    parse_warnings=tuple(warnings),
                )

            # --- Nested same-name tag rejection ---
            nested_open = f"<{tag_name}>"
            if nested_open in content:
                warnings.append(
                    f"Nested '<{tag_name}>' tag detected in "
                    f"'<{tag_name}>' section; section skipped"
                )
                continue

            # --- Content processing ---
            content = content.strip()

            # Control character stripping (M-18)
            content = _strip_control_chars(content)

            # Content length check (M-17)
            if len(content) > bounds.max_value_length:
                warnings.append(
                    f"Content for '<{tag_name}>' truncated "
                    f"({len(content)} > {bounds.max_value_length} chars)"
                )
                content = content[: bounds.max_value_length]

            # --- Compute line numbers ---
            start_line = _offset_to_line(line_starts, match.start())
            end_line = _offset_to_line(line_starts, match.end())

            sections.append(
                XmlSection(
                    tag_name=tag_name,
                    content=content,
                    start_line=start_line,
                    end_line=end_line,
                )
            )

        return XmlSectionResult(
            sections=tuple(sections),
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
