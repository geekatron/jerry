# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
UniversalParseResult - Complete parse result from universal document parsing.

Frozen dataclass aggregating results from all type-specific parsers invoked
by ``UniversalDocument.parse()``. All container fields use ``tuple`` (not
``list``) to ensure deep immutability.

Each parser result is ``None`` when the parser was not invoked. The
``parse_errors`` tuple collects errors from parsers that were invoked but
failed, enabling callers to distinguish "not invoked" from "invoked and
failed" (DD-9).

Security constraints:
    - Deep immutability via ``frozen=True`` + ``tuple`` containers
    - Parse errors aggregated per DD-9 (no exceptions for parse failures)
    - Dual-signal type detection warning from DocumentTypeDetector (M-14)

References:
    - ADR-PROJ005-003 Design Decision 3 (UniversalDocument Facade)
    - ADR-PROJ005-003 Design Decision 9 (Error Handling Strategy)
    - H-07: Domain layer constraint (no external infra/interface imports)
    - H-10: One class per file

Exports:
    UniversalParseResult: Frozen dataclass for the complete parse result.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.domain.markdown_ast.document_type import DocumentType
from src.domain.markdown_ast.frontmatter import BlockquoteFrontmatter
from src.domain.markdown_ast.html_comment import HtmlCommentBlock
from src.domain.markdown_ast.jerry_document import JerryDocument
from src.domain.markdown_ast.nav_table import NavEntry
from src.domain.markdown_ast.reinject import ReinjectDirective
from src.domain.markdown_ast.xml_section import XmlSection
from src.domain.markdown_ast.yaml_frontmatter import YamlFrontmatterResult


@dataclass(frozen=True)
class UniversalParseResult:
    """Complete parse result from UniversalDocument.

    Attributes:
        document_type: The detected or explicitly specified document type.
        jerry_document: The base JerryDocument (always present).
        yaml_frontmatter: YAML frontmatter result, or ``None`` if not invoked.
        blockquote_frontmatter: Blockquote frontmatter, or ``None`` if not invoked.
        xml_sections: Extracted XML sections, or ``None`` if not invoked.
        html_comments: Extracted HTML comment blocks, or ``None`` if not invoked.
        reinject_directives: L2-REINJECT directives, or ``None`` if not invoked.
        nav_entries: Navigation table entries, or ``None`` if not invoked.
        type_detection_warning: Warning when path/structure mismatch (M-14).
        parse_errors: Aggregated errors from all invoked parsers (DD-9).
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
