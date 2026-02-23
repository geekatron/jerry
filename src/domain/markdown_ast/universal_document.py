# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
UniversalDocument - Unified facade for parsing any Jerry markdown file type.

Wraps ``JerryDocument`` and adds type-specific parsed results as attributes
of a ``UniversalParseResult`` frozen dataclass. Delegates to type-specific
parsers based on the ``DocumentType`` and the parser invocation matrix from
ADR-PROJ005-003 DD-3.

All container fields use ``tuple`` (not ``list``) to ensure deep immutability.
Parse errors from all invoked parsers are aggregated into ``parse_errors``.

References:
    - ADR-PROJ005-003 Design Decision 3 (UniversalDocument Facade)
    - ADR-PROJ005-003 Design Decision 9 (Error Handling Strategy)
    - Threat Model: aggregated error reporting per DD-9
    - H-07: Domain layer constraint (no external infra/interface imports)
    - H-10: Supporting frozen dataclass (UniversalParseResult) co-located
      with primary class per ADR.

Exports:
    UniversalParseResult: Frozen dataclass with complete parse results.
    UniversalDocument: Facade class with static ``parse()`` method.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.domain.markdown_ast.document_type import DocumentType, DocumentTypeDetector
from src.domain.markdown_ast.frontmatter import BlockquoteFrontmatter
from src.domain.markdown_ast.html_comment import (
    HtmlCommentBlock,
    HtmlCommentMetadata,
)
from src.domain.markdown_ast.input_bounds import InputBounds
from src.domain.markdown_ast.jerry_document import JerryDocument
from src.domain.markdown_ast.nav_table import NavEntry, extract_nav_table
from src.domain.markdown_ast.reinject import (
    ReinjectDirective,
    extract_reinject_directives,
)
from src.domain.markdown_ast.xml_section import XmlSection, XmlSectionParser
from src.domain.markdown_ast.yaml_frontmatter import (
    YamlFrontmatter,
    YamlFrontmatterResult,
)


@dataclass(frozen=True)
class UniversalParseResult:
    """Complete parse result from UniversalDocument.

    All container fields use ``tuple`` for deep immutability. Optional fields
    are ``None`` when the corresponding parser was not invoked for this
    document type.

    Attributes:
        document_type: Detected or explicitly provided document type.
        jerry_document: The base JerryDocument (always present).
        yaml_frontmatter: YAML frontmatter result, or ``None`` if not invoked.
        blockquote_frontmatter: Blockquote frontmatter, or ``None`` if not
            invoked.
        xml_sections: Extracted XML sections as tuple, or ``None`` if not
            invoked.
        html_comments: Extracted HTML comment blocks as tuple, or ``None``
            if not invoked.
        reinject_directives: Extracted L2-REINJECT directives as tuple, or
            ``None`` if not invoked.
        nav_entries: Extracted navigation entries as tuple, or ``None`` if
            not invoked.
        type_detection_warning: Set when path/structure mismatch detected
            (M-14).
        parse_errors: Aggregated error strings from all invoked parsers
            (DD-9).
    """

    document_type: DocumentType
    jerry_document: JerryDocument
    yaml_frontmatter: YamlFrontmatterResult | None
    blockquote_frontmatter: BlockquoteFrontmatter | None
    xml_sections: tuple[XmlSection, ...] | None
    html_comments: tuple[HtmlCommentBlock, ...] | None
    reinject_directives: tuple[ReinjectDirective, ...] | None
    nav_entries: tuple[NavEntry, ...] | None
    type_detection_warning: str | None
    parse_errors: tuple[str, ...] = ()


# ---------------------------------------------------------------------------
# Parser invocation matrix (ADR-PROJ005-003 DD-3)
# Maps DocumentType -> set of parser names to invoke
# ---------------------------------------------------------------------------
_PARSER_MATRIX: dict[DocumentType, set[str]] = {
    DocumentType.AGENT_DEFINITION: {"yaml", "xml", "nav"},
    DocumentType.SKILL_DEFINITION: {"yaml", "nav"},
    DocumentType.RULE_FILE: {"reinject", "nav"},
    DocumentType.ADR: {"html_comment", "nav"},
    DocumentType.STRATEGY_TEMPLATE: {"blockquote"},
    DocumentType.WORKTRACKER_ENTITY: {"blockquote", "nav"},
    DocumentType.FRAMEWORK_CONFIG: {"reinject", "nav"},
    DocumentType.ORCHESTRATION_ARTIFACT: {"html_comment", "nav"},
    DocumentType.PATTERN_DOCUMENT: {"blockquote", "nav"},
    DocumentType.KNOWLEDGE_DOCUMENT: {"nav"},
    DocumentType.UNKNOWN: {"nav"},
}


class UniversalDocument:
    """Unified facade for parsing any Jerry markdown file type.

    Delegates to type-specific parsers based on the parser invocation matrix.
    Always creates a base ``JerryDocument``; additional parsers are invoked
    conditionally based on ``DocumentType``.
    """

    @staticmethod
    def parse(
        content: str,
        file_path: str | None = None,
        document_type: DocumentType | None = None,
        bounds: InputBounds | None = None,
    ) -> UniversalParseResult:
        """Parse content into a type-specific UniversalParseResult.

        If ``document_type`` is provided, it is used directly (explicit
        override). If ``file_path`` is provided without ``document_type``,
        auto-detection is used. If neither is provided, structure-only
        detection is attempted.

        Args:
            content: The raw markdown content to parse.
            file_path: Optional file path for type detection.
            document_type: Optional explicit type override.
            bounds: Resource limits. Defaults to ``InputBounds.DEFAULT``.

        Returns:
            A ``UniversalParseResult`` with all applicable parse results.
        """
        if bounds is None:
            bounds = InputBounds.DEFAULT

        # --- Base parse ---
        doc = JerryDocument.parse(content)

        # --- Type detection ---
        detection_warning: str | None = None
        if document_type is not None:
            detected_type = document_type
        elif file_path is not None:
            detected_type, detection_warning = DocumentTypeDetector.detect(file_path, content)
        else:
            # Structure-only detection
            detected_type, detection_warning = DocumentTypeDetector.detect("", content)

        # --- Determine which parsers to invoke ---
        parsers_to_run = _PARSER_MATRIX.get(detected_type, set())
        parse_errors: list[str] = []

        # --- Invoke parsers conditionally ---
        yaml_result: YamlFrontmatterResult | None = None
        blockquote_result: BlockquoteFrontmatter | None = None
        xml_result: tuple[XmlSection, ...] | None = None
        html_result: tuple[HtmlCommentBlock, ...] | None = None
        reinject_result: tuple[ReinjectDirective, ...] | None = None
        nav_result: tuple[NavEntry, ...] | None = None

        if "yaml" in parsers_to_run:
            yaml_result = YamlFrontmatter.extract(doc, bounds)
            if yaml_result.parse_error is not None:
                parse_errors.append(f"YamlFrontmatter: {yaml_result.parse_error}")

        if "blockquote" in parsers_to_run:
            blockquote_result = BlockquoteFrontmatter.extract(doc)

        if "xml" in parsers_to_run:
            xml_parsed = XmlSectionParser.extract(doc, bounds)
            xml_result = xml_parsed.sections
            if xml_parsed.parse_error is not None:
                parse_errors.append(f"XmlSectionParser: {xml_parsed.parse_error}")

        if "html_comment" in parsers_to_run:
            html_parsed = HtmlCommentMetadata.extract(doc, bounds)
            html_result = html_parsed.blocks
            if html_parsed.parse_error is not None:
                parse_errors.append(f"HtmlCommentMetadata: {html_parsed.parse_error}")

        if "reinject" in parsers_to_run:
            reinject_list = extract_reinject_directives(doc)
            reinject_result = tuple(reinject_list)

        if "nav" in parsers_to_run:
            nav_list = extract_nav_table(doc)
            if nav_list is not None:
                nav_result = tuple(nav_list)
            else:
                nav_result = ()

        return UniversalParseResult(
            document_type=detected_type,
            jerry_document=doc,
            yaml_frontmatter=yaml_result,
            blockquote_frontmatter=blockquote_result,
            xml_sections=xml_result,
            html_comments=html_result,
            reinject_directives=reinject_result,
            nav_entries=nav_result,
            type_detection_warning=detection_warning,
            parse_errors=tuple(parse_errors),
        )
