# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
markdown_ast - Domain package for Jerry markdown AST operations.

Provides the JerryDocument facade for all markdown parsing, querying,
transforming, and rendering in the Jerry Framework. Also provides the
L2-REINJECT comment parser, navigation table helpers, BlockquoteFrontmatter,
schema validation engine, and the universal markdown parser components:
YamlFrontmatter, XmlSectionParser, HtmlCommentMetadata, DocumentTypeDetector,
UniversalDocument, InputBounds, and SchemaRegistry.

References:
    - ST-001: JerryDocument Facade
    - ST-002: BlockquoteFrontmatter Extension
    - ST-003: L2-REINJECT Parser
    - ST-006: Schema Validation Engine
    - ST-008: Navigation Table Helpers
    - ADR-PROJ005-003: Universal Markdown Parser Architecture
    - H-07: Domain layer constraint (no external infra/interface imports)

Exports:
    JerryDocument: Unified facade for markdown AST operations
    FrontmatterField: Dataclass for a single frontmatter key-value field
    BlockquoteFrontmatter: Collection class for Jerry blockquote frontmatter
    extract_frontmatter: Convenience function to extract frontmatter
    ReinjectDirective: Frozen dataclass for a parsed L2-REINJECT comment
    extract_reinject_directives: Extract all L2-REINJECT directives
    modify_reinject_directive: Return a new document with one directive modified
    NavEntry: Frozen dataclass for one navigation table row
    NavValidationResult: Result of nav table validation
    extract_nav_table: Parse the first navigation table
    validate_nav_table: Validate H-23/H-24 compliance
    heading_to_anchor: Convert heading text to anchor slug
    FieldRule: Rule for a single frontmatter field
    SectionRule: Rule for a required section heading
    EntitySchema: Schema definition for an entity type
    ValidationViolation: A single schema violation
    ValidationReport: Complete validation report
    validate_document: Validate a JerryDocument against an EntitySchema
    get_entity_schema: Look up a built-in schema by entity type name
    EPIC_SCHEMA through BUG_SCHEMA: Built-in worktracker schemas
    InputBounds: Configurable resource limits for parser input validation
    YamlFrontmatterField: Single YAML frontmatter field
    YamlFrontmatterResult: YAML frontmatter extraction result
    YamlFrontmatter: YAML frontmatter extractor
    XmlSection: Single XML-tagged section
    XmlSectionResult: XML section extraction result
    XmlSectionParser: XML section extractor (regex-only)
    HtmlCommentField: Single HTML comment key-value pair
    HtmlCommentBlock: Single HTML comment metadata block
    HtmlCommentResult: HTML comment metadata extraction result
    HtmlCommentMetadata: HTML comment metadata extractor
    DocumentType: Jerry markdown file type enum
    DocumentTypeDetector: File type detector
    UniversalParseResult: Complete universal parse result
    UniversalDocument: Unified parsing facade
    SchemaRegistry: Schema registry with freeze support
"""

from src.domain.markdown_ast.document_type import DocumentType, DocumentTypeDetector
from src.domain.markdown_ast.frontmatter import (
    BlockquoteFrontmatter,
    FrontmatterField,
    extract_frontmatter,
)
from src.domain.markdown_ast.html_comment import (
    HtmlCommentBlock,
    HtmlCommentField,
    HtmlCommentMetadata,
    HtmlCommentResult,
)
from src.domain.markdown_ast.input_bounds import InputBounds
from src.domain.markdown_ast.jerry_document import JerryDocument
from src.domain.markdown_ast.nav_table import (
    NavEntry,
    NavValidationResult,
    extract_nav_table,
    heading_to_anchor,
    validate_nav_table,
)
from src.domain.markdown_ast.reinject import (
    ReinjectDirective,
    extract_reinject_directives,
    modify_reinject_directive,
)
from src.domain.markdown_ast.schema import (
    BUG_SCHEMA,
    ENABLER_SCHEMA,
    EPIC_SCHEMA,
    FEATURE_SCHEMA,
    STORY_SCHEMA,
    TASK_SCHEMA,
    EntitySchema,
    FieldRule,
    SectionRule,
    ValidationReport,
    ValidationViolation,
    get_entity_schema,
    validate_document,
)
from src.domain.markdown_ast.schema_registry import SchemaRegistry
from src.domain.markdown_ast.universal_document import (
    UniversalDocument,
    UniversalParseResult,
)
from src.domain.markdown_ast.xml_section import (
    XmlSection,
    XmlSectionParser,
    XmlSectionResult,
)
from src.domain.markdown_ast.yaml_frontmatter import (
    YamlFrontmatter,
    YamlFrontmatterField,
    YamlFrontmatterResult,
)

__all__ = [
    # ST-001: JerryDocument
    "JerryDocument",
    # ST-002: BlockquoteFrontmatter
    "BlockquoteFrontmatter",
    "FrontmatterField",
    "extract_frontmatter",
    # ST-003: L2-REINJECT
    "ReinjectDirective",
    "extract_reinject_directives",
    "modify_reinject_directive",
    # ST-008: Navigation Table
    "NavEntry",
    "NavValidationResult",
    "extract_nav_table",
    "heading_to_anchor",
    "validate_nav_table",
    # ST-006: Schema Validation
    "FieldRule",
    "SectionRule",
    "EntitySchema",
    "ValidationViolation",
    "ValidationReport",
    "validate_document",
    "get_entity_schema",
    "EPIC_SCHEMA",
    "FEATURE_SCHEMA",
    "STORY_SCHEMA",
    "ENABLER_SCHEMA",
    "TASK_SCHEMA",
    "BUG_SCHEMA",
    # RE-001: InputBounds
    "InputBounds",
    # RE-001: YamlFrontmatter
    "YamlFrontmatterField",
    "YamlFrontmatterResult",
    "YamlFrontmatter",
    # RE-002: XmlSectionParser
    "XmlSection",
    "XmlSectionResult",
    "XmlSectionParser",
    # RE-003: HtmlCommentMetadata
    "HtmlCommentField",
    "HtmlCommentBlock",
    "HtmlCommentResult",
    "HtmlCommentMetadata",
    # RE-004: DocumentTypeDetector
    "DocumentType",
    "DocumentTypeDetector",
    # RE-005: SchemaRegistry
    "SchemaRegistry",
    # RE-007: UniversalDocument
    "UniversalParseResult",
    "UniversalDocument",
]
