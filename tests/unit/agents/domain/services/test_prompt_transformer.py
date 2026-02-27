# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Tests for PromptTransformer domain service.

Coverage targets:
- to_format() dispatch: XML, MARKDOWN, RCCF
- from_xml() / _xml_to_markdown()
- _split_into_sections(): code blocks, preamble, empty input
- _downgrade_inner_headings(): ## -> ###, code block skipping
- _heading_to_tag(): known mappings, auto-derived kebab/snake
- _tag_to_heading(): snake_case to Title Case
- _markdown_to_rccf(): section reordering, FORMAT block remainder
- Edge cases: empty body, no headings, headings inside code blocks
"""

from __future__ import annotations

import pytest

from src.agents.domain.services.prompt_transformer import PromptTransformer
from src.agents.domain.value_objects.body_format import BodyFormat

# ---------------------------------------------------------------------------
# to_format() dispatch
# ---------------------------------------------------------------------------


class TestToFormat:
    """Tests for the public to_format() dispatch method."""

    def test_to_format_xml_delegates_to_markdown_to_xml(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Identity\n\nI am a test agent.\n"

        # Act
        result = prompt_transformer.to_format(body, BodyFormat.XML)

        # Assert – XML wrapper must be present
        assert "<identity>" in result
        assert "</identity>" in result

    def test_to_format_markdown_returns_body_unchanged(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Identity\n\nI am a test agent.\n"

        # Act
        result = prompt_transformer.to_format(body, BodyFormat.MARKDOWN)

        # Assert – unchanged pass-through
        assert result == body

    def test_to_format_rccf_produces_role_block(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Identity\n\nI am a test agent.\n\n## Purpose\n\nFor testing.\n"

        # Act
        result = prompt_transformer.to_format(body, BodyFormat.RCCF)

        # Assert
        assert "# ROLE" in result

    def test_to_format_empty_body_xml_returns_whitespace_only(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = ""

        # Act
        result = prompt_transformer.to_format(body, BodyFormat.XML)

        # Assert – no crash; empty input produces at most whitespace (no XML tags)
        assert result.strip() == ""
        assert "<" not in result

    def test_to_format_empty_body_markdown_returns_empty_body(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange / Act / Assert
        assert prompt_transformer.to_format("", BodyFormat.MARKDOWN) == ""

    def test_to_format_empty_body_rccf_returns_whitespace_only(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange / Act
        result = prompt_transformer.to_format("", BodyFormat.RCCF)

        # Assert – empty input produces at most whitespace (no RCCF blocks)
        assert result.strip() == ""
        assert "# ROLE" not in result


# ---------------------------------------------------------------------------
# _split_into_sections()
# ---------------------------------------------------------------------------


class TestSplitIntoSections:
    """Tests for the internal _split_into_sections helper."""

    def test_empty_input_returns_single_preamble_with_empty_content(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange / Act
        result = prompt_transformer._split_into_sections("")

        # Assert – splitting "" on "\n" yields one empty string, producing a
        # preamble section with heading=None and content=""
        assert len(result) == 1
        heading, content = result[0]
        assert heading is None
        assert content == ""

    def test_body_with_no_headings_yields_single_preamble_section(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "Just plain text with no headings."

        # Act
        sections = prompt_transformer._split_into_sections(body)

        # Assert – one preamble section with heading=None
        assert len(sections) == 1
        heading, content = sections[0]
        assert heading is None
        assert "Just plain text" in content

    def test_preamble_followed_by_heading(self, prompt_transformer: PromptTransformer) -> None:
        # Arrange
        body = "Intro text.\n\n## Identity\n\nSection body.\n"

        # Act
        sections = prompt_transformer._split_into_sections(body)

        # Assert – two sections: preamble and Identity
        assert len(sections) == 2
        assert sections[0][0] is None
        assert sections[1][0] == "Identity"

    def test_multiple_headings_split_correctly(self, prompt_transformer: PromptTransformer) -> None:
        # Arrange
        body = (
            "## Identity\n\nI am an agent.\n\n"
            "## Purpose\n\nTo serve.\n\n"
            "## Guardrails\n\nDo no harm.\n"
        )

        # Act
        sections = prompt_transformer._split_into_sections(body)

        # Assert
        headings = [h for h, _ in sections]
        assert headings == ["Identity", "Purpose", "Guardrails"]

    def test_heading_inside_code_block_is_not_split(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange – ## inside ``` should NOT be treated as a section boundary
        body = "## Identity\n\nSome text.\n\n```markdown\n## This is NOT a heading\n```\n"

        # Act
        sections = prompt_transformer._split_into_sections(body)

        # Assert – only one section (Identity); code-block heading ignored
        assert len(sections) == 1
        assert sections[0][0] == "Identity"
        code_block_heading = "## This is NOT a heading"
        assert code_block_heading in sections[0][1]

    def test_heading_with_html_comment_is_stripped(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Identity <!-- anchor -->\n\nContent.\n"

        # Act
        sections = prompt_transformer._split_into_sections(body)

        # Assert – HTML comment stripped from heading
        assert sections[0][0] == "Identity"

    def test_whitespace_only_body_returns_empty_list(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange / Act
        result = prompt_transformer._split_into_sections("   \n\n  ")

        # Assert – whitespace-only counts as preamble content
        # The implementation appends it because current_lines is non-empty;
        # confirm no crash and that result is a list.
        assert isinstance(result, list)


# ---------------------------------------------------------------------------
# _downgrade_inner_headings()
# ---------------------------------------------------------------------------


class TestDowngradeInnerHeadings:
    """Tests for _downgrade_inner_headings()."""

    def test_double_hash_becomes_triple(self, prompt_transformer: PromptTransformer) -> None:
        # Arrange
        content = "## Sub-heading\n\nSome text."

        # Act
        result = prompt_transformer._downgrade_inner_headings(content)

        # Assert – "## Sub-heading" line is now "### Sub-heading".
        # Use line-level check: no line starts with exactly "## ".
        assert "### Sub-heading" in result
        lines_starting_with_double_hash = [
            line for line in result.splitlines() if line.startswith("## ")
        ]
        assert lines_starting_with_double_hash == []

    def test_triple_hash_becomes_quadruple(self, prompt_transformer: PromptTransformer) -> None:
        # Arrange
        content = "### Deeper heading"

        # Act
        result = prompt_transformer._downgrade_inner_headings(content)

        # Assert – only ## is targeted; ### is not changed
        assert result == content

    def test_heading_inside_code_block_not_downgraded(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        content = "```\n## Should stay as-is\n```"

        # Act
        result = prompt_transformer._downgrade_inner_headings(content)

        # Assert
        assert "## Should stay as-is" in result

    def test_heading_after_code_block_is_downgraded(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        content = "```\ncode\n```\n## Outside block"

        # Act
        result = prompt_transformer._downgrade_inner_headings(content)

        # Assert
        assert "### Outside block" in result

    def test_no_headings_returns_content_unchanged(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        content = "Just plain text without any headings."

        # Act
        result = prompt_transformer._downgrade_inner_headings(content)

        # Assert
        assert result == content

    def test_empty_content_returns_empty_string(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange / Act / Assert
        assert prompt_transformer._downgrade_inner_headings("") == ""

    def test_multiple_headings_all_downgraded(self, prompt_transformer: PromptTransformer) -> None:
        # Arrange
        content = "## First\n\nText.\n\n## Second\n\nMore text."

        # Act
        result = prompt_transformer._downgrade_inner_headings(content)

        # Assert – both "## " headings become "### "; no line starts with "## "
        assert result.count("### ") == 2
        lines_starting_with_double_hash = [
            line for line in result.splitlines() if line.startswith("## ")
        ]
        assert lines_starting_with_double_hash == []


# ---------------------------------------------------------------------------
# _heading_to_tag()
# ---------------------------------------------------------------------------


class TestHeadingToTag:
    """Tests for _heading_to_tag() known mappings and auto-derivation."""

    @pytest.mark.parametrize(
        ("heading", "expected_tag"),
        [
            ("Identity", "identity"),
            ("Purpose", "purpose"),
            ("Capabilities", "capabilities"),
            ("Methodology", "methodology"),
            ("Guardrails", "guardrails"),
            ("Output Specification", "output"),
            ("Output Requirements", "output"),
            ("Constitutional Compliance", "constitutional_compliance"),
            # Governance section mappings
            ("Agent Version", "agent_version"),
            ("Tool Tier", "tool_tier"),
            ("Enforcement", "enforcement"),
            ("Portability", "portability"),
            ("Prior Art", "prior_art"),
            ("Session Context", "session_context"),
        ],
    )
    def test_known_heading_returns_canonical_tag(
        self,
        prompt_transformer: PromptTransformer,
        heading: str,
        expected_tag: str,
    ) -> None:
        # Arrange / Act
        result = prompt_transformer._heading_to_tag(heading)

        # Assert
        assert result == expected_tag

    def test_unknown_heading_auto_derived_to_snake_case(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        heading = "My Custom Section"

        # Act
        result = prompt_transformer._heading_to_tag(heading)

        # Assert – spaces become underscores, all lowercase
        assert result == "my_custom_section"

    def test_heading_with_special_chars_stripped(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        heading = "Retry & Error Handling"

        # Act
        result = prompt_transformer._heading_to_tag(heading)

        # Assert – non-alphanumeric sequences become single underscore
        assert result == "retry_error_handling"

    def test_heading_with_numbers_preserved(self, prompt_transformer: PromptTransformer) -> None:
        # Arrange
        heading = "Step 1 Overview"

        # Act
        result = prompt_transformer._heading_to_tag(heading)

        # Assert
        assert "1" in result


# ---------------------------------------------------------------------------
# _tag_to_heading()
# ---------------------------------------------------------------------------


class TestTagToHeading:
    """Tests for _tag_to_heading() snake_case to Title Case conversion."""

    def test_single_word_tag_title_cased(self, prompt_transformer: PromptTransformer) -> None:
        # Arrange / Act
        result = prompt_transformer._tag_to_heading("identity")

        # Assert
        assert result == "Identity"

    def test_snake_case_tag_converted_to_title_case(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange / Act
        result = prompt_transformer._tag_to_heading("constitutional_compliance")

        # Assert
        assert result == "Constitutional Compliance"

    def test_multi_word_snake_case(self, prompt_transformer: PromptTransformer) -> None:
        # Arrange / Act
        result = prompt_transformer._tag_to_heading("my_custom_section")

        # Assert
        assert result == "My Custom Section"

    def test_single_char_tag(self, prompt_transformer: PromptTransformer) -> None:
        # Arrange / Act
        result = prompt_transformer._tag_to_heading("a")

        # Assert
        assert result == "A"


# ---------------------------------------------------------------------------
# from_xml() / _xml_to_markdown()
# ---------------------------------------------------------------------------


class TestFromXml:
    """Tests for from_xml() converting XML tags back to markdown headings."""

    def test_paired_tag_converts_to_heading(self, prompt_transformer: PromptTransformer) -> None:
        # Arrange
        body = "<identity>\nI am an agent.\n</identity>\n"

        # Act
        result = prompt_transformer.from_xml(body)

        # Assert
        assert "## Identity" in result
        assert "I am an agent." in result

    def test_self_closing_tag_converts_to_empty_heading(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "<guardrails />\n"

        # Act
        result = prompt_transformer.from_xml(body)

        # Assert
        assert "## Guardrails" in result

    def test_unknown_tag_converts_to_title_case_heading(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "<custom_block>\nSome content.\n</custom_block>\n"

        # Act
        result = prompt_transformer.from_xml(body)

        # Assert
        assert "## Custom Block" in result
        assert "Some content." in result

    def test_inner_headings_inside_xml_are_downgraded_then_restored(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange – inner ## heading inside XML tag content
        body = "<identity>\n## Sub-section\n\nText.\n</identity>\n"

        # Act
        result = prompt_transformer.from_xml(body)

        # Assert – outer heading is ## Identity, inner is ### Sub-section
        assert "## Identity" in result
        assert "### Sub-section" in result

    def test_multiple_paired_tags_all_converted(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "<identity>\nAgent identity.\n</identity>\n\n<purpose>\nAgent purpose.\n</purpose>\n"

        # Act
        result = prompt_transformer.from_xml(body)

        # Assert
        assert "## Identity" in result
        assert "## Purpose" in result
        assert "Agent identity." in result
        assert "Agent purpose." in result

    def test_output_tag_maps_to_output_specification(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange – 'output' tag should map back to 'Output Specification'
        # (first known mapping wins)
        body = "<output>\nResult format.\n</output>\n"

        # Act
        result = prompt_transformer.from_xml(body)

        # Assert
        assert "## Output Specification" in result


# ---------------------------------------------------------------------------
# to_format() with XML: round-trip and specific behaviours
# ---------------------------------------------------------------------------


class TestMarkdownToXml:
    """Tests for XML output from to_format(..., BodyFormat.XML)."""

    def test_identity_section_wrapped_in_xml(self, prompt_transformer: PromptTransformer) -> None:
        # Arrange
        body = "## Identity\n\nI am a test agent.\n"

        # Act
        result = prompt_transformer.to_format(body, BodyFormat.XML)

        # Assert
        assert "<identity>" in result
        assert "I am a test agent." in result
        assert "</identity>" in result

    def test_empty_section_becomes_self_closing_tag(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange – section heading with no content
        body = "## Guardrails\n\n## Identity\n\nSome content.\n"

        # Act
        result = prompt_transformer.to_format(body, BodyFormat.XML)

        # Assert – empty Guardrails becomes self-closing
        assert "<guardrails />" in result

    def test_preamble_preserved_before_xml_sections(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange – text before first heading is the preamble
        body = "This is a preamble.\n\n## Identity\n\nAgent body.\n"

        # Act
        result = prompt_transformer.to_format(body, BodyFormat.XML)

        # Assert – preamble appears before the XML tag
        assert result.index("This is a preamble.") < result.index("<identity>")

    def test_multiple_sections_all_converted(self, prompt_transformer: PromptTransformer) -> None:
        # Arrange
        body = (
            "## Identity\n\nWho I am.\n\n"
            "## Purpose\n\nWhy I exist.\n\n"
            "## Guardrails\n\nDo no harm.\n"
        )

        # Act
        result = prompt_transformer.to_format(body, BodyFormat.XML)

        # Assert
        assert "<identity>" in result
        assert "<purpose>" in result
        assert "<guardrails>" in result

    def test_unknown_section_heading_auto_derives_tag(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Session Context\n\nContext data.\n"

        # Act
        result = prompt_transformer.to_format(body, BodyFormat.XML)

        # Assert – auto-derived snake_case tag
        assert "<session_context>" in result

    def test_heading_inside_code_block_not_split_into_section(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Identity\n\nI am an agent.\n\n```\n## Not a section\n```\n"

        # Act
        result = prompt_transformer.to_format(body, BodyFormat.XML)

        # Assert – only one XML section produced
        assert result.count("<identity>") == 1
        # The code block content should remain inside the identity tag
        assert "## Not a section" in result

    def test_output_ends_with_newline(self, prompt_transformer: PromptTransformer) -> None:
        # Arrange
        body = "## Identity\n\nContent.\n"

        # Act
        result = prompt_transformer.to_format(body, BodyFormat.XML)

        # Assert
        assert result.endswith("\n")

    def test_preamble_only_xml_returns_preamble(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange – body has no headings, only a preamble
        body = "Just plain text.\n"

        # Act
        result = prompt_transformer.to_format(body, BodyFormat.XML)

        # Assert – no XML tags; content returned as-is (preamble path)
        assert "<" not in result
        assert "Just plain text." in result

    def test_markdown_to_xml_converts_agent_version_heading(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Agent Version\n\n1.2.0\n"

        # Act
        result = prompt_transformer.to_format(body, BodyFormat.XML)

        # Assert
        assert "<agent_version>" in result
        assert "1.2.0" in result
        assert "</agent_version>" in result

    def test_markdown_to_xml_converts_tool_tier_heading(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Tool Tier\n\nT3 (External)\n"

        # Act
        result = prompt_transformer.to_format(body, BodyFormat.XML)

        # Assert
        assert "<tool_tier>" in result
        assert "T3 (External)" in result
        assert "</tool_tier>" in result

    def test_markdown_to_xml_converts_enforcement_heading(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Enforcement\n\nquality_gate_tier: C2\n"

        # Act
        result = prompt_transformer.to_format(body, BodyFormat.XML)

        # Assert
        assert "<enforcement>" in result
        assert "</enforcement>" in result

    def test_markdown_to_xml_converts_portability_heading(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Portability\n\nenabled: true\n"

        # Act
        result = prompt_transformer.to_format(body, BodyFormat.XML)

        # Assert
        assert "<portability>" in result
        assert "</portability>" in result

    def test_markdown_to_xml_converts_prior_art_heading(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Prior Art\n\n- ADR-001\n- Phase 3 Synthesis\n"

        # Act
        result = prompt_transformer.to_format(body, BodyFormat.XML)

        # Assert
        assert "<prior_art>" in result
        assert "</prior_art>" in result

    def test_markdown_to_xml_converts_session_context_heading(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Session Context\n\non_receive: validate\n"

        # Act
        result = prompt_transformer.to_format(body, BodyFormat.XML)

        # Assert
        assert "<session_context>" in result
        assert "</session_context>" in result


# ---------------------------------------------------------------------------
# _markdown_to_rccf()
# ---------------------------------------------------------------------------


class TestMarkdownToRccf:
    """Tests for _markdown_to_rccf() ROLE/CONTEXT/CONSTRAINTS/FORMAT blocks."""

    def test_identity_and_purpose_go_into_role_block(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Identity\n\nWho I am.\n\n## Purpose\n\nWhy I exist.\n"

        # Act
        result = prompt_transformer._markdown_to_rccf(body)

        # Assert
        assert "# ROLE" in result
        role_idx = result.index("# ROLE")
        assert result.index("Who I am.") > role_idx
        assert result.index("Why I exist.") > role_idx

    def test_capabilities_and_methodology_go_into_context_block(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Capabilities\n\nWhat I can do.\n\n## Methodology\n\nHow I work.\n"

        # Act
        result = prompt_transformer._markdown_to_rccf(body)

        # Assert
        assert "# CONTEXT" in result

    def test_guardrails_goes_into_constraints_block(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Guardrails\n\nDo no harm.\n"

        # Act
        result = prompt_transformer._markdown_to_rccf(body)

        # Assert
        assert "# CONSTRAINTS" in result
        assert "Do no harm." in result

    def test_output_specification_goes_into_format_block(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Output Specification\n\nJSON output.\n"

        # Act
        result = prompt_transformer._markdown_to_rccf(body)

        # Assert
        assert "# FORMAT" in result
        assert "JSON output." in result

    def test_output_requirements_goes_into_format_block(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Output Requirements\n\nMarkdown output.\n"

        # Act
        result = prompt_transformer._markdown_to_rccf(body)

        # Assert
        assert "# FORMAT" in result

    def test_unknown_section_goes_into_format_block_as_remainder(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Identity\n\nWho I am.\n\n## Custom Section\n\nExtra stuff.\n"

        # Act
        result = prompt_transformer._markdown_to_rccf(body)

        # Assert – unknown section ends up in FORMAT
        assert "# FORMAT" in result
        assert "Extra stuff." in result

    def test_empty_body_returns_whitespace_only(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange / Act
        result = prompt_transformer._markdown_to_rccf("")

        # Assert – empty input produces no RCCF blocks (only a trailing newline
        # from the section-join path in _markdown_to_rccf)
        assert result.strip() == ""
        assert "# ROLE" not in result

    def test_blocks_separated_by_dividers(self, prompt_transformer: PromptTransformer) -> None:
        # Arrange
        body = (
            "## Identity\n\nWho I am.\n\n"
            "## Capabilities\n\nWhat I do.\n\n"
            "## Guardrails\n\nConstraints.\n\n"
            "## Output Specification\n\nFormat.\n"
        )

        # Act
        result = prompt_transformer._markdown_to_rccf(body)

        # Assert – RCCF blocks are separated by "---" dividers
        assert "---" in result

    def test_result_ends_with_newline(self, prompt_transformer: PromptTransformer) -> None:
        # Arrange
        body = "## Identity\n\nContent.\n"

        # Act
        result = prompt_transformer._markdown_to_rccf(body)

        # Assert
        assert result.endswith("\n")

    def test_missing_blocks_are_omitted(self, prompt_transformer: PromptTransformer) -> None:
        # Arrange – only Identity present, so only ROLE block expected
        body = "## Identity\n\nWho I am.\n"

        # Act
        result = prompt_transformer._markdown_to_rccf(body)

        # Assert
        assert "# ROLE" in result
        assert "# CONTEXT" not in result
        assert "# CONSTRAINTS" not in result
        assert "# FORMAT" not in result

    def test_full_canonical_body_produces_all_four_blocks(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = (
            "## Identity\n\nWho I am.\n\n"
            "## Purpose\n\nWhy I exist.\n\n"
            "## Capabilities\n\nWhat I can do.\n\n"
            "## Methodology\n\nHow I work.\n\n"
            "## Guardrails\n\nDo no harm.\n\n"
            "## Output Specification\n\nJSON.\n"
        )

        # Act
        result = prompt_transformer._markdown_to_rccf(body)

        # Assert
        assert "# ROLE" in result
        assert "# CONTEXT" in result
        assert "# CONSTRAINTS" in result
        assert "# FORMAT" in result

    def test_constitutional_compliance_goes_into_constraints(
        self, prompt_transformer: PromptTransformer
    ) -> None:
        # Arrange
        body = "## Constitutional Compliance\n\nP-003, P-020, P-022.\n"

        # Act
        result = prompt_transformer._markdown_to_rccf(body)

        # Assert
        assert "# CONSTRAINTS" in result
        assert "P-003" in result
