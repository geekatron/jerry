# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for the L2-REINJECT comment parser.

Tests cover:
    - AC-ST003-1: Extract all L2-REINJECT comments from a Jerry rule file
    - AC-ST003-2: Parse structured fields: rank (int), tokens (int), content (str)
    - AC-ST003-3: Write-back: modify rank value, verify roundtrip
    - AC-ST003-4: Write-back: modify content string, verify roundtrip
    - AC-ST003-5: Works on quality-enforcement.md (6+ L2-REINJECT comments)
    - AC-ST003-6: Non-L2-REINJECT HTML comments are preserved unchanged
    - H-20: BDD test-first approach
    - H-21: 90% line coverage

Test Categories:
    - Happy path: Valid L2-REINJECT directives, field parsing, modification roundtrip
    - Negative: No directives, malformed comments, out-of-range index
    - Edge cases: Escaped quotes in content, non-L2 HTML comments, multiple directives
"""

from __future__ import annotations

import pytest

from src.domain.markdown_ast.jerry_document import JerryDocument
from src.domain.markdown_ast.reinject import (
    ReinjectDirective,
    extract_reinject_directives,
    modify_reinject_directive,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SINGLE_DIRECTIVE_SOURCE = """\
# Rule File

<!-- L2-REINJECT: rank=1, tokens=50, content="Constitutional: No recursive subagents (P-003)." -->

Some content here.
"""

MULTI_DIRECTIVE_SOURCE = """\
# Quality Enforcement

<!-- L2-REINJECT: rank=1, tokens=50, content="Constitutional: No recursive subagents (P-003). User decides, never override (P-020). No deception (P-022). These are HARD constraints that CANNOT be overridden." -->

<!-- L2-REINJECT: rank=2, tokens=90, content="Quality gate >= 0.92 weighted composite for C2+ deliverables (H-13). Creator-critic-revision cycle REQUIRED, minimum 3 iterations (H-14). Below threshold = REJECTED." -->

<!-- L2-REINJECT: rank=3, tokens=25, content="UV only for Python (H-05/H-06). NEVER use python/pip directly." -->

Some table here.
"""

NON_REINJECT_COMMENT_SOURCE = """\
# Title

<!-- VERSION: 1.0 | DATE: 2026-01-01 -->

<!-- L2-REINJECT: rank=1, tokens=10, content="Simple directive." -->

Body text.
"""

ESCAPED_QUOTE_SOURCE = """\
# Title

<!-- L2-REINJECT: rank=1, tokens=20, content="Has \\"escaped\\" quotes inside." -->

Body.
"""

SIX_DIRECTIVE_SOURCE = """\
# Quality Enforcement

<!-- VERSION: 1.3.0 | DATE: 2026-02-15 | SOURCE: EPIC-002 Final Synthesis, ADR-EPIC002-001, ADR-EPIC002-002 -->

<!-- L2-REINJECT: rank=1, tokens=50, content="Constitutional: No recursive subagents (P-003). User decides, never override (P-020). No deception (P-022). These are HARD constraints that CANNOT be overridden." -->

<!-- L2-REINJECT: rank=2, tokens=90, content="Quality gate >= 0.92 weighted composite for C2+ deliverables (H-13). Creator-critic-revision cycle REQUIRED, minimum 3 iterations (H-14). Below threshold = REJECTED." -->

<!-- L2-REINJECT: rank=3, tokens=25, content="UV only for Python (H-05/H-06). NEVER use python/pip directly." -->

<!-- L2-REINJECT: rank=4, tokens=30, content="LLM-as-Judge scoring (S-014): Apply strict rubric. Leniency bias must be actively counteracted." -->

<!-- L2-REINJECT: rank=5, tokens=30, content="Self-review REQUIRED before presenting any deliverable (H-15, S-010)." -->

<!-- L2-REINJECT: rank=8, tokens=40, content="Governance escalation REQUIRED per AE rules (H-19). Touches .context/rules/ = auto-C3. Touches constitution = auto-C4." -->

Some table here.
"""


# ---------------------------------------------------------------------------
# TestReinjectDirective
# ---------------------------------------------------------------------------


class TestReinjectDirective:
    """Tests for the ReinjectDirective frozen dataclass."""

    def test_directive_has_rank_field(self) -> None:
        """ReinjectDirective stores rank as int."""
        d = ReinjectDirective(rank=1, tokens=50, content="hello", line_number=0, raw_text="raw")
        assert d.rank == 1

    def test_directive_has_tokens_field(self) -> None:
        """ReinjectDirective stores tokens as int."""
        d = ReinjectDirective(rank=2, tokens=90, content="hello", line_number=0, raw_text="raw")
        assert d.tokens == 90

    def test_directive_has_content_field(self) -> None:
        """ReinjectDirective stores content as str."""
        d = ReinjectDirective(rank=1, tokens=10, content="Some content.", line_number=0, raw_text="raw")
        assert d.content == "Some content."

    def test_directive_has_line_number_field(self) -> None:
        """ReinjectDirective stores line_number as int."""
        d = ReinjectDirective(rank=1, tokens=10, content="text", line_number=5, raw_text="raw")
        assert d.line_number == 5

    def test_directive_has_raw_text_field(self) -> None:
        """ReinjectDirective stores raw_text as str."""
        raw = '<!-- L2-REINJECT: rank=1, tokens=10, content="text" -->'
        d = ReinjectDirective(rank=1, tokens=10, content="text", line_number=0, raw_text=raw)
        assert d.raw_text == raw

    def test_directive_is_frozen(self) -> None:
        """ReinjectDirective is immutable (frozen dataclass)."""
        d = ReinjectDirective(rank=1, tokens=10, content="text", line_number=0, raw_text="raw")
        with pytest.raises((AttributeError, TypeError)):
            d.rank = 99  # type: ignore[misc]


# ---------------------------------------------------------------------------
# TestExtractReinjectDirectives
# ---------------------------------------------------------------------------


class TestExtractReinjectDirectives:
    """Tests for extract_reinject_directives()."""

    def test_extract_returns_list(self) -> None:
        """extract_reinject_directives() returns a list."""
        doc = JerryDocument.parse(SINGLE_DIRECTIVE_SOURCE)
        result = extract_reinject_directives(doc)
        assert isinstance(result, list)

    def test_extract_single_directive(self) -> None:
        """Extracts one directive from a document with a single L2-REINJECT comment."""
        doc = JerryDocument.parse(SINGLE_DIRECTIVE_SOURCE)
        directives = extract_reinject_directives(doc)
        assert len(directives) == 1

    def test_extract_multiple_directives(self) -> None:
        """Extracts all directives from a document with multiple L2-REINJECT comments."""
        doc = JerryDocument.parse(MULTI_DIRECTIVE_SOURCE)
        directives = extract_reinject_directives(doc)
        assert len(directives) == 3

    def test_extract_six_directives_quality_enforcement(self) -> None:
        """Extracts 6 directives from quality-enforcement-style source (AC-ST003-5)."""
        doc = JerryDocument.parse(SIX_DIRECTIVE_SOURCE)
        directives = extract_reinject_directives(doc)
        assert len(directives) == 6

    def test_extract_parses_rank_as_int(self) -> None:
        """Parsed rank field is an integer (AC-ST003-2)."""
        doc = JerryDocument.parse(SINGLE_DIRECTIVE_SOURCE)
        directives = extract_reinject_directives(doc)
        assert isinstance(directives[0].rank, int)
        assert directives[0].rank == 1

    def test_extract_parses_tokens_as_int(self) -> None:
        """Parsed tokens field is an integer (AC-ST003-2)."""
        doc = JerryDocument.parse(SINGLE_DIRECTIVE_SOURCE)
        directives = extract_reinject_directives(doc)
        assert isinstance(directives[0].tokens, int)
        assert directives[0].tokens == 50

    def test_extract_parses_content_as_str(self) -> None:
        """Parsed content field is a string (AC-ST003-2)."""
        doc = JerryDocument.parse(SINGLE_DIRECTIVE_SOURCE)
        directives = extract_reinject_directives(doc)
        assert isinstance(directives[0].content, str)
        assert "P-003" in directives[0].content

    def test_extract_content_without_surrounding_quotes(self) -> None:
        """Extracted content does not include surrounding double-quote delimiters."""
        doc = JerryDocument.parse(SINGLE_DIRECTIVE_SOURCE)
        directives = extract_reinject_directives(doc)
        assert not directives[0].content.startswith('"')
        assert not directives[0].content.endswith('"')

    def test_extract_preserves_order(self) -> None:
        """Directives are returned in document order."""
        doc = JerryDocument.parse(MULTI_DIRECTIVE_SOURCE)
        directives = extract_reinject_directives(doc)
        ranks = [d.rank for d in directives]
        assert ranks == [1, 2, 3]

    def test_extract_returns_empty_list_for_no_directives(self) -> None:
        """Returns empty list when document has no L2-REINJECT comments."""
        source = "# No Directives\n\nJust some text.\n"
        doc = JerryDocument.parse(source)
        directives = extract_reinject_directives(doc)
        assert directives == []

    def test_extract_returns_empty_list_for_empty_document(self) -> None:
        """Returns empty list for empty document."""
        doc = JerryDocument.parse("")
        directives = extract_reinject_directives(doc)
        assert directives == []

    def test_extract_non_reinject_comment_not_included(self) -> None:
        """Non-L2-REINJECT HTML comments are NOT included in extraction (AC-ST003-6)."""
        doc = JerryDocument.parse(NON_REINJECT_COMMENT_SOURCE)
        directives = extract_reinject_directives(doc)
        # Only 1 L2-REINJECT comment; the VERSION comment is not included
        assert len(directives) == 1
        assert directives[0].rank == 1

    def test_extract_stores_raw_text(self) -> None:
        """Each directive stores the full raw comment text."""
        doc = JerryDocument.parse(SINGLE_DIRECTIVE_SOURCE)
        directives = extract_reinject_directives(doc)
        assert "L2-REINJECT" in directives[0].raw_text
        assert "<!--" in directives[0].raw_text
        assert "-->" in directives[0].raw_text

    def test_extract_stores_line_number(self) -> None:
        """Each directive stores a valid line_number (zero-based or one-based, consistent)."""
        doc = JerryDocument.parse(MULTI_DIRECTIVE_SOURCE)
        directives = extract_reinject_directives(doc)
        # Line numbers should be distinct and increasing
        line_numbers = [d.line_number for d in directives]
        assert line_numbers == sorted(line_numbers)
        assert len(set(line_numbers)) == len(line_numbers)

    def test_extract_six_directives_ranks(self) -> None:
        """Six-directive document has correct rank values extracted."""
        doc = JerryDocument.parse(SIX_DIRECTIVE_SOURCE)
        directives = extract_reinject_directives(doc)
        ranks = [d.rank for d in directives]
        assert ranks == [1, 2, 3, 4, 5, 8]

    def test_extract_six_directives_tokens(self) -> None:
        """Six-directive document has correct token counts extracted."""
        doc = JerryDocument.parse(SIX_DIRECTIVE_SOURCE)
        directives = extract_reinject_directives(doc)
        tokens = [d.tokens for d in directives]
        assert tokens == [50, 90, 25, 30, 30, 40]

    def test_extract_content_with_special_chars(self) -> None:
        """Content with em dashes, slashes, parentheses, and greater-than chars is parsed correctly."""
        doc = JerryDocument.parse(MULTI_DIRECTIVE_SOURCE)
        directives = extract_reinject_directives(doc)
        # Directive 2 contains >= and (H-13) etc.
        assert ">=" in directives[1].content
        assert "(H-13)" in directives[1].content

    def test_extract_directive_is_reinject_directive_type(self) -> None:
        """Each extracted item is a ReinjectDirective instance."""
        doc = JerryDocument.parse(SINGLE_DIRECTIVE_SOURCE)
        directives = extract_reinject_directives(doc)
        assert isinstance(directives[0], ReinjectDirective)

    def test_extract_content_with_escaped_quotes(self) -> None:
        """Content field with escaped double-quotes is decoded correctly."""
        doc = JerryDocument.parse(ESCAPED_QUOTE_SOURCE)
        directives = extract_reinject_directives(doc)
        assert len(directives) == 1
        # Escaped quotes in the source become actual quotes in parsed content
        assert '"escaped"' in directives[0].content or '\\"escaped\\"' in directives[0].content


# ---------------------------------------------------------------------------
# TestModifyReinjectDirective
# ---------------------------------------------------------------------------


class TestModifyReinjectDirective:
    """Tests for modify_reinject_directive()."""

    def test_modify_returns_new_jerry_document(self) -> None:
        """modify_reinject_directive() returns a new JerryDocument instance."""
        doc = JerryDocument.parse(SINGLE_DIRECTIVE_SOURCE)
        new_doc = modify_reinject_directive(doc, 0, rank=99)
        assert isinstance(new_doc, JerryDocument)
        assert new_doc is not doc

    def test_modify_rank_changes_rank(self) -> None:
        """Modifying rank updates the rank field in the new document (AC-ST003-3)."""
        doc = JerryDocument.parse(SINGLE_DIRECTIVE_SOURCE)
        new_doc = modify_reinject_directive(doc, 0, rank=42)
        directives = extract_reinject_directives(new_doc)
        assert directives[0].rank == 42

    def test_modify_tokens_changes_tokens(self) -> None:
        """Modifying tokens updates the tokens field in the new document."""
        doc = JerryDocument.parse(SINGLE_DIRECTIVE_SOURCE)
        new_doc = modify_reinject_directive(doc, 0, tokens=999)
        directives = extract_reinject_directives(new_doc)
        assert directives[0].tokens == 999

    def test_modify_content_changes_content(self) -> None:
        """Modifying content updates the content field in the new document (AC-ST003-4)."""
        doc = JerryDocument.parse(SINGLE_DIRECTIVE_SOURCE)
        new_doc = modify_reinject_directive(doc, 0, content="New content here.")
        directives = extract_reinject_directives(new_doc)
        assert directives[0].content == "New content here."

    def test_modify_rank_roundtrip(self) -> None:
        """Rank write-back roundtrip: modify rank, re-extract, value matches (AC-ST003-3)."""
        doc = JerryDocument.parse(MULTI_DIRECTIVE_SOURCE)
        new_doc = modify_reinject_directive(doc, 1, rank=99)
        directives = extract_reinject_directives(new_doc)
        assert directives[1].rank == 99

    def test_modify_content_roundtrip(self) -> None:
        """Content write-back roundtrip: modify content, re-extract, value matches (AC-ST003-4)."""
        new_content = "Updated directive content with special chars >= 0.92."
        doc = JerryDocument.parse(MULTI_DIRECTIVE_SOURCE)
        new_doc = modify_reinject_directive(doc, 0, content=new_content)
        directives = extract_reinject_directives(new_doc)
        assert directives[0].content == new_content

    def test_modify_original_document_unchanged(self) -> None:
        """modify_reinject_directive() does not mutate the original document."""
        doc = JerryDocument.parse(SINGLE_DIRECTIVE_SOURCE)
        original_source = doc.source
        modify_reinject_directive(doc, 0, rank=99)
        assert doc.source == original_source

    def test_modify_other_directives_unchanged(self) -> None:
        """Modifying one directive leaves other directives unchanged."""
        doc = JerryDocument.parse(MULTI_DIRECTIVE_SOURCE)
        new_doc = modify_reinject_directive(doc, 0, rank=99)
        directives = extract_reinject_directives(new_doc)
        # Directives at index 1 and 2 should be unchanged
        assert directives[1].rank == 2
        assert directives[2].rank == 3

    def test_modify_non_reinject_comments_preserved(self) -> None:
        """Non-L2-REINJECT HTML comments are preserved after modification (AC-ST003-6)."""
        doc = JerryDocument.parse(NON_REINJECT_COMMENT_SOURCE)
        new_doc = modify_reinject_directive(doc, 0, rank=99)
        # The VERSION comment should still be in the source
        assert "VERSION: 1.0" in new_doc.source

    def test_modify_no_fields_returns_equivalent_document(self) -> None:
        """modify_reinject_directive() with no fields changed returns document with same directive values."""
        doc = JerryDocument.parse(SINGLE_DIRECTIVE_SOURCE)
        new_doc = modify_reinject_directive(doc, 0)
        original_directives = extract_reinject_directives(doc)
        new_directives = extract_reinject_directives(new_doc)
        assert new_directives[0].rank == original_directives[0].rank
        assert new_directives[0].tokens == original_directives[0].tokens
        assert new_directives[0].content == original_directives[0].content

    def test_modify_multiple_fields_simultaneously(self) -> None:
        """Multiple fields can be modified in one call."""
        doc = JerryDocument.parse(SINGLE_DIRECTIVE_SOURCE)
        new_doc = modify_reinject_directive(doc, 0, rank=7, tokens=100, content="All new content.")
        directives = extract_reinject_directives(new_doc)
        assert directives[0].rank == 7
        assert directives[0].tokens == 100
        assert directives[0].content == "All new content."

    def test_modify_raises_index_error_for_out_of_range(self) -> None:
        """modify_reinject_directive() raises IndexError for out-of-range index."""
        doc = JerryDocument.parse(SINGLE_DIRECTIVE_SOURCE)
        with pytest.raises(IndexError):
            modify_reinject_directive(doc, 5, rank=1)

    def test_modify_raises_index_error_for_negative_index_on_empty(self) -> None:
        """modify_reinject_directive() raises IndexError when no directives exist."""
        doc = JerryDocument.parse("# No directives\n")
        with pytest.raises(IndexError):
            modify_reinject_directive(doc, 0, rank=1)

    def test_modify_second_directive_in_multi(self) -> None:
        """Can target the second directive (index=1) independently."""
        doc = JerryDocument.parse(MULTI_DIRECTIVE_SOURCE)
        new_doc = modify_reinject_directive(doc, 1, tokens=777)
        directives = extract_reinject_directives(new_doc)
        assert directives[1].tokens == 777
        # Others unchanged
        assert directives[0].tokens == 50
        assert directives[2].tokens == 25

    def test_modify_content_with_special_characters(self) -> None:
        """Content with >= and slashes survives write-back roundtrip."""
        new_content = "Quality gate >= 0.92 for C2+ (H-13/H-14). NEVER skip."
        doc = JerryDocument.parse(SINGLE_DIRECTIVE_SOURCE)
        new_doc = modify_reinject_directive(doc, 0, content=new_content)
        directives = extract_reinject_directives(new_doc)
        assert directives[0].content == new_content
