# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ast_ops - Thin wrapper over the markdown_ast domain layer for the /ast skill.

Provides file-level operations that Claude can invoke during interactive sessions
to parse, query, modify, validate, and render Jerry markdown documents. Each
function reads from disk, delegates to the domain layer, and returns structured
Python data (dict or str) suitable for Claude to inspect and reason over.

All functions raise FileNotFoundError for missing files and propagate domain
layer exceptions (KeyError, IndexError, ValueError) unchanged to the caller.

References:
    - ST-005: /ast Claude Skill
    - ST-006: Schema Validation Engine
    - ST-007: Migrate /worktracker Agents to AST
    - ST-001: JerryDocument Facade
    - ST-002: BlockquoteFrontmatter Extension
    - ST-003: L2-REINJECT Parser
    - ST-008: Navigation Table Helpers
    - H-07: Domain layer constraint (no external infra/interface imports)
    - H-11: Type hints REQUIRED on all public functions
    - H-12: Docstrings REQUIRED on all public functions

Exports:
    parse_file: Parse a markdown file and return structured AST info.
    query_frontmatter: Extract frontmatter fields as a plain dict.
    modify_frontmatter: Modify a frontmatter field and write back to file.
    validate_file: Validate file structure (nav table + entity schema).
    render_file: Parse and render normalized markdown from a file.
    extract_reinject: Extract all L2-REINJECT directives from a file.
    validate_nav_table_file: Validate H-23/H-24 nav table compliance for a file.
"""

from __future__ import annotations

from src.domain.markdown_ast import (
    JerryDocument,
    extract_frontmatter,
    extract_nav_table,
    extract_reinject_directives,
    get_entity_schema,
    validate_document,
    validate_nav_table,
)

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _read_file(file_path: str) -> str:
    """
    Read a file from disk and return its content as a string.

    Args:
        file_path: Absolute or relative path to the file.

    Returns:
        The file content as a UTF-8 decoded string.

    Raises:
        FileNotFoundError: If the file does not exist at the given path.
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError as err:
        raise FileNotFoundError(
            f"File not found: '{file_path}'. Ensure the path is correct and the file exists."
        ) from err


def _write_file(file_path: str, content: str) -> None:
    """
    Write content to a file on disk.

    Args:
        file_path: Absolute or relative path to the file.
        content: The string content to write (UTF-8 encoded).
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse_file(file_path: str) -> dict[str, object]:
    """
    Parse a markdown file and return structured information about it.

    Reads the file, parses it with JerryDocument, and returns a summary dict
    containing the file path, source length, node types present in the AST,
    heading count, and whether the file has blockquote frontmatter.

    Args:
        file_path: Path to the markdown file to parse.

    Returns:
        A dict with the following keys:
            - file_path (str): The path as provided.
            - source_length (int): Total character count of the source.
            - node_types (list[str]): Unique AST node types present.
            - heading_count (int): Total number of heading nodes.
            - has_frontmatter (bool): True if any `> **Key:** Value` fields found.

    Raises:
        FileNotFoundError: If the file does not exist.

    Examples:
        >>> info = parse_file("path/to/file.md")
        >>> info["has_frontmatter"]
        True
        >>> info["heading_count"]
        3
    """
    source = _read_file(file_path)
    doc = JerryDocument.parse(source)

    # Collect unique node types from the AST (excluding root)
    node_types: list[str] = []
    seen: set[str] = set()
    for node in doc.tree.walk():
        if node.is_root:
            continue
        if node.type not in seen:
            seen.add(node.type)
            node_types.append(node.type)

    heading_count = len(doc.query("heading"))
    fm = extract_frontmatter(doc)
    has_frontmatter = len(fm) > 0

    return {
        "file_path": file_path,
        "source_length": len(source),
        "node_types": node_types,
        "heading_count": heading_count,
        "has_frontmatter": has_frontmatter,
    }


def query_frontmatter(file_path: str) -> dict[str, str]:
    """
    Extract all blockquote frontmatter fields from a file as a plain dict.

    Reads the file, parses it, and returns all `> **Key:** Value` fields as a
    Python dict mapping key strings to value strings. Returns an empty dict if
    no frontmatter is found.

    Args:
        file_path: Path to the markdown file.

    Returns:
        A dict mapping frontmatter key strings to value strings.
        Empty dict if the file has no frontmatter.

    Raises:
        FileNotFoundError: If the file does not exist.

    Examples:
        >>> fm = query_frontmatter("path/to/story.md")
        >>> fm["Status"]
        'pending'
        >>> fm["Type"]
        'story'
    """
    source = _read_file(file_path)
    doc = JerryDocument.parse(source)
    fm = extract_frontmatter(doc)
    return dict(fm.items())


def modify_frontmatter(file_path: str, key: str, value: str) -> str:
    """
    Modify a frontmatter field in a file and write the result back to disk.

    Reads the file, extracts frontmatter, modifies the named field to the
    new value, writes the updated content back to the file, and returns the
    new file content as a string.

    This operation is idempotent in the sense that calling it again with the
    same key and value will produce the same result. The underlying write-back
    uses mdformat normalization (see BlockquoteFrontmatter.set()).

    Args:
        file_path: Path to the markdown file.
        key: The frontmatter field name to modify (case-sensitive).
        value: The new value for the field.

    Returns:
        The new file content as a string after modification.

    Raises:
        FileNotFoundError: If the file does not exist.
        KeyError: If the key does not exist in the frontmatter.

    Examples:
        >>> new_content = modify_frontmatter("path/to/story.md", "Status", "done")
        >>> "done" in new_content
        True
    """
    source = _read_file(file_path)
    doc = JerryDocument.parse(source)
    fm = extract_frontmatter(doc)
    new_doc = fm.set(key, value)
    new_content = new_doc.render()
    _write_file(file_path, new_content)
    return new_content


def validate_file(
    file_path: str,
    schema: str | None = None,
) -> dict[str, object]:
    """
    Validate the structure of a markdown file.

    Performs two validation checks:
    1. Navigation table validation (H-23/H-24): Checks whether the document
       has a navigation table and whether it covers all ## headings.
    2. Schema validation: When a schema name is provided (e.g., "epic",
       "story", "enabler", "task", "bug", "feature"), the document is
       validated against the corresponding built-in entity schema from
       ST-006.  When no schema is provided, schema_valid defaults to True.

    Args:
        file_path: Path to the markdown file to validate.
        schema: Optional schema name (e.g., "story", "enabler", "task",
            "bug", "epic", "feature"). When provided, the document is
            validated against the built-in entity schema. When None,
            schema validation is skipped (schema_valid defaults to True).

    Returns:
        A dict with the following keys:
            - is_valid (bool): True only when nav_table_valid and schema_valid are both True.
            - nav_table_valid (bool): True if the nav table exists and covers all ## headings.
            - missing_nav_entries (list[str]): Heading texts absent from the nav table.
            - orphaned_nav_entries (list[str]): Nav entries whose anchor has no matching heading.
            - schema_valid (bool): True when schema validation passes or no schema provided.
            - schema (str | None): The schema name provided, or None.
            - schema_violations (list[dict]): List of violation dicts when schema
              validation is performed. Each dict has: field_path, expected, actual,
              severity, message.  Empty list when no schema is provided or when
              validation passes with no violations.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the schema name is not a known entity type.

    Examples:
        >>> result = validate_file("path/to/file.md")
        >>> result["nav_table_valid"]
        True
        >>> result = validate_file("path/to/story.md", schema="story")
        >>> result["schema_valid"]
        True
    """
    source = _read_file(file_path)
    doc = JerryDocument.parse(source)
    nav_result = validate_nav_table(doc)

    schema_valid = True
    schema_violations: list[dict[str, str]] = []

    if schema is not None:
        entity_schema = get_entity_schema(schema)
        report = validate_document(doc, entity_schema)
        schema_valid = report.is_valid
        schema_violations = [
            {
                "field_path": v.field_path,
                "expected": v.expected,
                "actual": v.actual,
                "severity": v.severity,
                "message": v.message,
            }
            for v in report.violations
        ]

    is_valid = nav_result.is_valid and schema_valid

    return {
        "is_valid": is_valid,
        "nav_table_valid": nav_result.is_valid,
        "missing_nav_entries": nav_result.missing_entries,
        "orphaned_nav_entries": [entry.section_name for entry in nav_result.orphaned_entries],
        "schema_valid": schema_valid,
        "schema": schema,
        "schema_violations": schema_violations,
    }


def render_file(file_path: str) -> str:
    """
    Parse a markdown file and return it as normalized (mdformat) markdown.

    Reads the file, parses it with JerryDocument, and renders it via mdformat
    normalization. The output is idempotent: rendering the output again produces
    the same result.

    Args:
        file_path: Path to the markdown file to render.

    Returns:
        The normalized markdown content as a string. Returns an empty string
        for empty files.

    Raises:
        FileNotFoundError: If the file does not exist.

    Examples:
        >>> content = render_file("path/to/file.md")
        >>> isinstance(content, str)
        True
    """
    source = _read_file(file_path)
    doc = JerryDocument.parse(source)
    return doc.render()


def extract_reinject(file_path: str) -> list[dict[str, object]]:
    """
    Extract all L2-REINJECT directives from a markdown file.

    Reads the file, parses it, and returns all L2-REINJECT HTML comment
    directives as a list of plain dicts. Each dict contains the structured
    fields from the directive: rank, tokens, content, and line_number.

    Args:
        file_path: Path to the markdown file.

    Returns:
        A list of dicts, one per directive, each containing:
            - rank (int): Priority rank (lower = injected first).
            - tokens (int): Estimated token count of the content.
            - content (str): The reinject payload string.
            - line_number (int): Zero-based line index of the directive.
        Returns an empty list if no L2-REINJECT directives are found.

    Raises:
        FileNotFoundError: If the file does not exist.

    Examples:
        >>> directives = extract_reinject("path/to/rule-file.md")
        >>> directives[0]["rank"]
        1
        >>> directives[0]["content"]
        'Constitutional: No recursive subagents.'
    """
    source = _read_file(file_path)
    doc = JerryDocument.parse(source)
    directives = extract_reinject_directives(doc)
    return [
        {
            "rank": d.rank,
            "tokens": d.tokens,
            "content": d.content,
            "line_number": d.line_number,
        }
        for d in directives
    ]


def validate_nav_table_file(file_path: str) -> dict[str, object]:
    """
    Validate H-23/H-24 navigation table compliance for a markdown file.

    Reads the file, parses it, and runs the full nav table validation:
    - H-23: Navigation table MUST be present for docs over 30 lines.
    - H-24: Nav table entries MUST use anchor links.

    All entries in the result are serializable (plain dicts, not domain objects).

    Args:
        file_path: Path to the markdown file to validate.

    Returns:
        A dict with the following keys:
            - is_valid (bool): True if nav table exists and all headings are covered.
            - missing_entries (list[str]): ## heading texts absent from the nav table.
            - orphaned_entries (list[str]): Section names in nav table with no matching heading.
            - entries (list[dict]): All nav table entries found. Each entry dict has:
                - section_name (str): The display text of the section link.
                - anchor (str): The anchor slug from the link.
                - description (str): The purpose column text.
                - line_number (int): 1-based line number of this row.

    Raises:
        FileNotFoundError: If the file does not exist.

    Examples:
        >>> result = validate_nav_table_file("path/to/file.md")
        >>> result["is_valid"]
        True
        >>> result["entries"][0]["section_name"]
        'Overview'
    """
    source = _read_file(file_path)
    doc = JerryDocument.parse(source)
    nav_result = validate_nav_table(doc)

    # Extract nav table entries for serializable output (extract_nav_table may return None)
    raw_entries = extract_nav_table(doc) or []

    return {
        "is_valid": nav_result.is_valid,
        "missing_entries": nav_result.missing_entries,
        "orphaned_entries": [entry.section_name for entry in nav_result.orphaned_entries],
        "entries": [
            {
                "section_name": e.section_name,
                "anchor": e.anchor,
                "description": e.description,
                "line_number": e.line_number,
            }
            for e in raw_entries
        ],
    }
