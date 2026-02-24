# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
PromptTransformer - Transforms system prompt body between formats.

Converts markdown heading-based canonical prompts to vendor-optimal formats:
- XML tags for Claude (## Identity -> <identity>...</identity>)
- Markdown pass-through for GPT/general
- RCCF (Role-Context-Constraints-Format) for open-source models

References:
    - ADR-PROJ010-003: LLM Portability Architecture
    - agent-development-standards.md: Markdown Body Sections
"""

from __future__ import annotations

import re

from src.agents.domain.value_objects.body_format import BodyFormat

# Known section heading -> XML tag mappings
_HEADING_TO_TAG: dict[str, str] = {
    "Identity": "identity",
    "Purpose": "purpose",
    "Capabilities": "capabilities",
    "Methodology": "methodology",
    "Guardrails": "guardrails",
    "Output Specification": "output",
    "Output Requirements": "output",
    "Constitutional Compliance": "constitutional_compliance",
}


class PromptTransformer:
    """Transforms prompt body content between canonical and vendor formats.

    The canonical format uses markdown ## headings. Vendor adapters may
    require different delimiters (XML tags, RCCF blocks, etc.).
    """

    def to_format(self, body: str, target: BodyFormat) -> str:
        """Transform prompt body to the target format.

        Args:
            body: Prompt body in canonical format (markdown ## headings).
            target: Target body format.

        Returns:
            Transformed body string.
        """
        if target == BodyFormat.XML:
            return self._markdown_to_xml(body)
        if target == BodyFormat.RCCF:
            return self._markdown_to_rccf(body)
        # MARKDOWN: pass through unchanged
        return body

    def from_xml(self, body: str) -> str:
        """Convert XML-tagged body back to canonical markdown headings.

        Args:
            body: Body with XML tags (e.g., <identity>...</identity>).

        Returns:
            Body with markdown ## headings.
        """
        return self._xml_to_markdown(body)

    def _markdown_to_xml(self, body: str) -> str:
        """Convert ## headings to XML tags.

        Handles the canonical section mapping and auto-derives tags
        for sections not in the known map.
        """
        sections = self._split_into_sections(body)
        if not sections:
            return body

        parts: list[str] = []

        # Handle any content before the first heading (preamble)
        if sections[0][0] is None:
            preamble = sections[0][1].strip()
            if preamble:
                parts.append(preamble)
                parts.append("")
            sections = sections[1:]

        for heading, content in sections:
            if heading is None:
                parts.append(content.strip())
                continue

            tag = self._heading_to_tag(heading)
            content_stripped = content.strip()
            if content_stripped:
                parts.append(f"<{tag}>")
                parts.append(content_stripped)
                parts.append(f"</{tag}>")
            else:
                parts.append(f"<{tag} />")
            parts.append("")

        return "\n".join(parts).rstrip() + "\n"

    def _xml_to_markdown(self, body: str) -> str:
        """Convert XML tags to ## headings.

        Handles both paired tags and self-closing tags.
        Downgrades ## headings inside XML content to ### to avoid
        collision with section-level ## headings.
        """
        result = body

        # Build reverse tag -> heading map
        tag_to_heading: dict[str, str] = {}
        for heading, tag in _HEADING_TO_TAG.items():
            # Prefer the first mapping (don't overwrite)
            if tag not in tag_to_heading:
                tag_to_heading[tag] = heading

        # Replace paired XML tags: <tag>content</tag>
        def replace_paired(match: re.Match[str]) -> str:
            tag = match.group(1)
            content = match.group(2).strip()
            # Downgrade ## headings inside content to ### to prevent
            # them from being treated as section delimiters
            content = self._downgrade_inner_headings(content)
            heading = tag_to_heading.get(tag, self._tag_to_heading(tag))
            return f"## {heading}\n\n{content}"

        result = re.sub(
            r"<([a-z_]+)>\s*\n?(.*?)\n?\s*</\1>",
            replace_paired,
            result,
            flags=re.DOTALL,
        )

        # Replace self-closing tags: <tag />
        def replace_self_closing(match: re.Match[str]) -> str:
            tag = match.group(1)
            heading = tag_to_heading.get(tag, self._tag_to_heading(tag))
            return f"## {heading}\n"

        result = re.sub(r"<([a-z_]+)\s*/>", replace_self_closing, result)

        return result

    def _downgrade_inner_headings(self, content: str) -> str:
        """Downgrade ## headings to ### inside XML section content.

        Prevents inner headings from colliding with section-level ##
        delimiters when the content is later split into sections.
        Skips headings inside fenced code blocks.

        Args:
            content: Content extracted from inside an XML tag.

        Returns:
            Content with ## headings replaced by ### headings.
        """
        lines = content.split("\n")
        result_lines: list[str] = []
        in_code_block = False

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                result_lines.append(line)
                continue

            if in_code_block:
                result_lines.append(line)
                continue

            # Downgrade ## to ###, ### to ####, etc.
            if re.match(r"^##(?!#)", line):
                result_lines.append("#" + line)
            else:
                result_lines.append(line)

        return "\n".join(result_lines)

    def _markdown_to_rccf(self, body: str) -> str:
        """Convert to Role-Context-Constraints-Format.

        RCCF reorders sections into four blocks:
        - ROLE: Identity + Purpose
        - CONTEXT: Capabilities + Methodology
        - CONSTRAINTS: Guardrails + Constitutional Compliance
        - FORMAT: Output Specification + remaining sections
        """
        sections = self._split_into_sections(body)
        if not sections:
            return body

        section_map: dict[str, str] = {}
        for heading, content in sections:
            if heading is not None:
                section_map[heading] = content.strip()

        rccf_blocks: list[str] = []

        # ROLE
        role_parts = []
        for key in ("Identity", "Purpose"):
            if key in section_map:
                role_parts.append(section_map[key])
        if role_parts:
            rccf_blocks.append("# ROLE\n\n" + "\n\n".join(role_parts))

        # CONTEXT
        context_parts = []
        for key in ("Capabilities", "Methodology"):
            if key in section_map:
                context_parts.append(section_map[key])
        if context_parts:
            rccf_blocks.append("# CONTEXT\n\n" + "\n\n".join(context_parts))

        # CONSTRAINTS
        constraint_parts = []
        for key in ("Guardrails", "Constitutional Compliance"):
            if key in section_map:
                constraint_parts.append(section_map[key])
        if constraint_parts:
            rccf_blocks.append("# CONSTRAINTS\n\n" + "\n\n".join(constraint_parts))

        # FORMAT (output + remaining)
        format_parts = []
        used_keys = {
            "Identity",
            "Purpose",
            "Capabilities",
            "Methodology",
            "Guardrails",
            "Constitutional Compliance",
            "Output Specification",
            "Output Requirements",
        }
        for key in ("Output Specification", "Output Requirements"):
            if key in section_map:
                format_parts.append(section_map[key])
        for heading, content in sections:
            if heading is not None and heading not in used_keys:
                format_parts.append(f"### {heading}\n\n{content.strip()}")
        if format_parts:
            rccf_blocks.append("# FORMAT\n\n" + "\n\n".join(format_parts))

        return "\n\n---\n\n".join(rccf_blocks) + "\n"

    def _split_into_sections(self, body: str) -> list[tuple[str | None, str]]:
        """Split markdown body into (heading, content) pairs.

        Returns a list of (heading, content) tuples. The first entry
        may have heading=None for content before the first heading.

        Ignores ## headings inside fenced code blocks (``` markers).
        """
        sections: list[tuple[str | None, str]] = []
        current_heading: str | None = None
        current_lines: list[str] = []
        in_code_block = False

        for line in body.split("\n"):
            # Track fenced code blocks
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                current_lines.append(line)
                continue

            if in_code_block:
                current_lines.append(line)
                continue

            match = re.match(r"^##\s+(.+?)(?:\s*<!--.*-->)?\s*$", line)
            if match:
                # Save previous section
                if current_heading is not None or current_lines:
                    sections.append((current_heading, "\n".join(current_lines)))
                current_heading = match.group(1).strip()
                current_lines = []
            else:
                current_lines.append(line)

        # Save last section
        if current_heading is not None or current_lines:
            sections.append((current_heading, "\n".join(current_lines)))

        return sections

    def _heading_to_tag(self, heading: str) -> str:
        """Convert a markdown heading to an XML tag name.

        Uses known mappings first, then auto-derives via kebab-case.

        Args:
            heading: Markdown heading text.

        Returns:
            XML tag name in snake_case.
        """
        if heading in _HEADING_TO_TAG:
            return _HEADING_TO_TAG[heading]
        # Auto-derive: convert to snake_case
        return re.sub(r"[^a-z0-9]+", "_", heading.lower()).strip("_")

    def _tag_to_heading(self, tag: str) -> str:
        """Convert an XML tag name back to a heading.

        Args:
            tag: XML tag in snake_case.

        Returns:
            Title-cased heading string.
        """
        return tag.replace("_", " ").title()
