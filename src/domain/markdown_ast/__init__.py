# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
markdown_ast - Domain package for Jerry markdown AST operations.

Provides the JerryDocument facade for all markdown parsing, querying,
transforming, and rendering in the Jerry Framework. Also provides the
L2-REINJECT comment parser for extracting and modifying enforcement
directives embedded in Jerry rule files, navigation table helpers
for querying and validating Jerry navigation tables,
BlockquoteFrontmatter for structured access to Jerry entity metadata,
and the schema validation engine for checking Jerry markdown files against
structural schemas.

References:
    - ST-001: JerryDocument Facade
    - ST-002: BlockquoteFrontmatter Extension
    - ST-003: L2-REINJECT Parser
    - ST-006: Schema Validation Engine
    - ST-008: Navigation Table Helpers
    - H-07: Domain layer constraint (no external infra/interface imports)

Exports:
    JerryDocument: Unified facade for markdown AST operations
    FrontmatterField: Dataclass for a single frontmatter key-value field
    BlockquoteFrontmatter: Collection class for Jerry blockquote frontmatter
    extract_frontmatter: Convenience function to extract frontmatter from a JerryDocument
    ReinjectDirective: Frozen dataclass representing a parsed L2-REINJECT comment
    extract_reinject_directives: Extract all L2-REINJECT directives from a JerryDocument
    modify_reinject_directive: Return a new document with one directive modified
    NavEntry: Frozen dataclass representing one navigation table row
    NavValidationResult: Result of nav table validation against document headings
    extract_nav_table: Parse the first navigation table from a JerryDocument
    validate_nav_table: Validate H-23/H-24 compliance for a JerryDocument
    heading_to_anchor: Convert heading text to a GitHub-style anchor slug
    FieldRule: Rule for a single frontmatter field in a schema definition
    SectionRule: Rule for a required ## heading section in a schema definition
    EntitySchema: Schema definition for a Jerry worktracker entity type
    ValidationViolation: A single schema violation found during validation
    ValidationReport: Complete validation report for a document against a schema
    validate_document: Validate a JerryDocument against an EntitySchema
    get_entity_schema: Look up a built-in schema by entity type name
    EPIC_SCHEMA: Built-in schema for Epic entities
    FEATURE_SCHEMA: Built-in schema for Feature entities
    STORY_SCHEMA: Built-in schema for Story entities
    ENABLER_SCHEMA: Built-in schema for Enabler entities
    TASK_SCHEMA: Built-in schema for Task entities
    BUG_SCHEMA: Built-in schema for Bug entities
"""

from src.domain.markdown_ast.frontmatter import (
    BlockquoteFrontmatter,
    FrontmatterField,
    extract_frontmatter,
)
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

__all__ = [
    "JerryDocument",
    "BlockquoteFrontmatter",
    "FrontmatterField",
    "extract_frontmatter",
    "NavEntry",
    "NavValidationResult",
    "ReinjectDirective",
    "extract_nav_table",
    "extract_reinject_directives",
    "heading_to_anchor",
    "modify_reinject_directive",
    "validate_nav_table",
    # ST-006: Schema Validation Engine
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
]
