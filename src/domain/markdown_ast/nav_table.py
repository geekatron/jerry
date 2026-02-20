# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Navigation table helpers for Jerry markdown documents.

Provides AST-based helpers for querying and validating navigation tables in
Jerry markdown files. Enforces H-23 (navigation table required for docs over
30 lines) and H-24 (anchor links required in navigation table entries).

Navigation table format (from markdown-navigation-standards.md):

    ## Document Sections

    | Section | Purpose |
    |---------|---------|
    | [Summary](#summary) | What this covers |
    | [Problem Statement](#problem-statement) | Why this matters |

Rules:
    - H-23: All Claude-consumed markdown files >30 lines MUST include a nav table.
    - H-24: Navigation table section names MUST use anchor links.
    - Anchor format: lowercase, hyphens for spaces, remove special characters.

References:
    - ST-008: Navigation Table Helpers
    - .context/rules/markdown-navigation-standards.md

Exports:
    NavEntry: Frozen dataclass representing one navigation table row.
    NavValidationResult: Result of nav table validation against document headings.
    extract_nav_table: Parse the first navigation table from a JerryDocument.
    validate_nav_table: Validate H-23/H-24 compliance for a JerryDocument.
    heading_to_anchor: Convert heading text to a GitHub-style anchor slug.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from src.domain.markdown_ast.jerry_document import JerryDocument

# Regex to match a nav table row containing an anchor link.
# Matches lines like: | [Section Name](#anchor-slug) | Description |
_NAV_ENTRY_RE = re.compile(
    r"^\|\s*\[([^\]]+)\]\(#([^)]+)\)\s*\|\s*([^|]*?)\s*\|",
)

# Heading names that serve as the nav table container itself and should be
# excluded from missing-entry checks.
_NAV_CONTAINER_HEADINGS = frozenset(
    {"Document Sections", "document-sections"}
)


@dataclass(frozen=True)
class NavEntry:
    """
    Represents one row in a Jerry navigation table.

    Attributes:
        section_name: The display text of the section link (e.g. "Summary").
        anchor: The anchor slug from the link (e.g. "summary").
        description: The purpose/description column text.
        line_number: 1-based line number of this row in the source document.
    """

    section_name: str
    anchor: str
    description: str
    line_number: int


@dataclass
class NavValidationResult:
    """
    Result of validating a navigation table against document headings.

    Attributes:
        is_valid: True when the document has a nav table and all ## headings
            are covered with correct anchor links.
        missing_entries: Heading text for ## headings absent from the nav table.
        orphaned_entries: NavEntry objects whose anchor does not match any
            ## heading in the document.
        entries: All NavEntry objects extracted from the nav table (empty list
            if no nav table was found).
    """

    is_valid: bool
    missing_entries: list[str] = field(default_factory=list)
    orphaned_entries: list[NavEntry] = field(default_factory=list)
    entries: list[NavEntry] = field(default_factory=list)


def heading_to_anchor(heading_text: str) -> str:
    """
    Convert a heading text string to a GitHub-style anchor slug.

    Follows the rules from markdown-navigation-standards.md:
    - Strip leading/trailing whitespace.
    - Lowercase the entire string.
    - Remove characters that are not alphanumeric, spaces, or hyphens.
    - Replace one or more spaces with a single hyphen.
    - Collapse multiple consecutive hyphens to one.
    - Strip any leading or trailing hyphens.

    Args:
        heading_text: The heading text as it appears in the markdown source
            (e.g. "Problem Statement", "Children (Tasks)").

    Returns:
        The anchor slug string (e.g. "problem-statement", "children-tasks").
        Returns an empty string for empty or whitespace-only input.

    Examples:
        >>> heading_to_anchor("Summary")
        'summary'
        >>> heading_to_anchor("Problem Statement")
        'problem-statement'
        >>> heading_to_anchor("Children (Tasks)")
        'children-tasks'
        >>> heading_to_anchor("Standards (MEDIUM)")
        'standards-medium'
    """
    text = heading_text.strip().lower()
    # Remove characters that are not alphanumeric, spaces, or hyphens
    text = re.sub(r"[^\w\s-]", "", text)
    # Replace underscores left by \w with hyphens
    text = text.replace("_", "-")
    # Replace one or more whitespace characters with a single hyphen
    text = re.sub(r"\s+", "-", text)
    # Collapse multiple hyphens
    text = re.sub(r"-{2,}", "-", text)
    # Strip leading/trailing hyphens
    text = text.strip("-")
    return text


def extract_nav_table(doc: JerryDocument) -> list[NavEntry] | None:
    """
    Find and parse the first navigation table in a JerryDocument.

    Scans the document source line by line looking for lines that match the
    Jerry navigation table row pattern: ``| [Name](#anchor) | Description |``.
    The first contiguous block of such rows is returned as the navigation table.
    Rows that do not contain anchor links (e.g. header separator rows, plain
    text table rows) are skipped.

    Args:
        doc: A parsed JerryDocument to inspect.

    Returns:
        A list of NavEntry objects, one per nav table row, or None if no
        navigation table is found in the document.

    Examples:
        >>> source = "# Doc\\n\\n## Document Sections\\n\\n| Section | Purpose |\\n|---------|---------|\\n| [Summary](#summary) | Text |\\n"
        >>> doc = JerryDocument.parse(source)
        >>> entries = extract_nav_table(doc)
        >>> entries[0].section_name
        'Summary'
    """
    entries: list[NavEntry] = []
    lines = doc.source.splitlines()

    for line_idx, line in enumerate(lines):
        match = _NAV_ENTRY_RE.match(line)
        if match:
            section_name = match.group(1).strip()
            anchor = match.group(2).strip()
            description = match.group(3).strip()
            entries.append(
                NavEntry(
                    section_name=section_name,
                    anchor=anchor,
                    description=description,
                    line_number=line_idx + 1,  # 1-based
                )
            )

    return entries if entries else None


def _extract_h2_headings(doc: JerryDocument) -> list[str]:
    """
    Extract all ## heading texts from the document using the AST.

    Uses the SyntaxTreeNode.tag attribute (e.g. "h2") which is available
    directly on the heading node even though node.token is None for virtual
    heading nodes in markdown-it-py.

    Args:
        doc: A parsed JerryDocument.

    Returns:
        List of heading text strings (e.g. ["Summary", "Details"]) for every
        ``##`` level heading in the document.
    """
    headings: list[str] = []
    for node in doc.query("heading"):
        # heading nodes are virtual in markdown-it-py: node.token is None
        # but node.tag ("h1", "h2", ...) and node.markup ("#", "##", ...)
        # are available directly on the node.
        if node.tag != "h2":
            continue
        # The inline text content is in the first inline child node.
        for child in node.children:
            if child.type == "inline":
                headings.append(child.content)
                break
    return headings


def validate_nav_table(doc: JerryDocument) -> NavValidationResult:
    """
    Validate H-23 and H-24 compliance for a JerryDocument.

    Checks that:
    - The document contains a navigation table (H-23).
    - Every ``##`` heading (except the nav table container heading) has a
      corresponding entry in the nav table (H-23 coverage).
    - Every nav table entry's anchor matches the expected anchor computed from
      its section name via heading_to_anchor() (H-24).

    An entry is considered to match a heading when the entry's anchor equals
    the heading_to_anchor() of any ``##`` heading text in the document.

    Args:
        doc: A parsed JerryDocument to validate.

    Returns:
        A NavValidationResult describing the validation outcome. ``is_valid``
        is True only when the nav table exists and there are no missing or
        orphaned entries.

    Examples:
        >>> source = "# Title\\n\\n## Document Sections\\n\\n| Section | Purpose |\\n|---------|---------|\\n| [Summary](#summary) | Text |\\n\\n## Summary\\n\\nContent.\\n"
        >>> doc = JerryDocument.parse(source)
        >>> result = validate_nav_table(doc)
        >>> result.is_valid
        True
    """
    entries = extract_nav_table(doc)

    if entries is None:
        # No nav table found — collect all ## headings as missing
        h2_headings = _extract_h2_headings(doc)
        missing = [h for h in h2_headings if h not in _NAV_CONTAINER_HEADINGS]
        return NavValidationResult(
            is_valid=False,
            missing_entries=missing,
            orphaned_entries=[],
            entries=[],
        )

    # Build a set of all ## heading anchors present in the document
    h2_headings = _extract_h2_headings(doc)
    # Exclude the nav table container heading from coverage checks
    content_headings = [
        h for h in h2_headings if h not in _NAV_CONTAINER_HEADINGS
    ]
    heading_anchors: set[str] = {heading_to_anchor(h) for h in content_headings}

    # Detect orphaned entries: nav entries whose anchor has no matching heading
    orphaned: list[NavEntry] = []
    covered_anchors: set[str] = set()
    for entry in entries:
        if entry.anchor in heading_anchors:
            covered_anchors.add(entry.anchor)
        else:
            orphaned.append(entry)

    # Detect missing entries: ## headings whose anchor is not in nav table
    missing: list[str] = []
    for heading in content_headings:
        anchor = heading_to_anchor(heading)
        if anchor not in covered_anchors:
            missing.append(heading)

    is_valid = len(orphaned) == 0 and len(missing) == 0

    return NavValidationResult(
        is_valid=is_valid,
        missing_entries=missing,
        orphaned_entries=orphaned,
        entries=entries,
    )
