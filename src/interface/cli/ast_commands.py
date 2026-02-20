# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""AST CLI command implementations for the jerry ast namespace.

Provides the core functions that implement `jerry ast` subcommands:
    - ast_parse: Parse a markdown file and output the AST as JSON.
    - ast_render: Roundtrip parse-render a markdown file through mdformat.
    - ast_validate: Validate a markdown file against an optional entity schema.
    - ast_query: Query AST nodes by type and output structured JSON.

Helper serializers:
    - token_to_dict: Convert a markdown-it-py Token to a JSON-serializable dict.
    - node_to_dict: Convert a SyntaxTreeNode to a JSON-serializable dict.

Exit codes:
    0 -- Success
    1 -- Validation failure (schema violations found)
    2 -- Parse error (file not found, unreadable, unknown schema type, etc.)

References:
    - ST-004: Add jerry ast CLI Commands
    - ST-006: Schema Validation Engine
    - ST-001: JerryDocument Facade
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from markdown_it.token import Token
from markdown_it.tree import SyntaxTreeNode

from src.domain.markdown_ast.jerry_document import JerryDocument
from src.domain.markdown_ast.schema import get_entity_schema, validate_document


def token_to_dict(token: Token) -> dict[str, Any]:
    """Convert a markdown-it-py Token to a JSON-serializable dictionary.

    Extracts the fields most useful for CLI inspection: type, tag, nesting,
    map (line range), and content.

    Args:
        token: A Token object produced by markdown-it-py.

    Returns:
        A dictionary with keys: type, tag, nesting, map, content.
        The ``map`` value is either a list of two ints [start, end] or None.
    """
    return {
        "type": token.type,
        "tag": token.tag,
        "nesting": token.nesting,
        "map": list(token.map) if token.map is not None else None,
        "content": token.content,
    }


def _tree_to_dict(node: SyntaxTreeNode) -> dict[str, Any]:
    """Recursively convert a SyntaxTreeNode to a JSON-serializable dictionary.

    The root node is handled specially: its tag, map, and content attributes
    raise AttributeError (by design in markdown-it-py), so we use safe defaults
    for the root and use direct property accessors for all other nodes.

    Args:
        node: A SyntaxTreeNode from the parsed AST.

    Returns:
        A nested dictionary representing the node and all its children,
        with keys: type, tag, map, content, children.
    """
    if node.is_root:
        return {
            "type": node.type,
            "tag": "",
            "map": None,
            "content": "",
            "children": [_tree_to_dict(child) for child in node.children],
        }

    # Non-root nodes: direct property accessors are always available
    map_raw = node.map
    map_val: list[int] | None = list(map_raw) if map_raw is not None else None

    return {
        "type": node.type,
        "tag": node.tag,
        "map": map_val,
        "content": node.content or "",
        "children": [_tree_to_dict(child) for child in node.children],
    }


def node_to_dict(node: SyntaxTreeNode) -> dict[str, Any]:
    """Convert a SyntaxTreeNode to a flat JSON-serializable dictionary.

    Extracts the node type, tag, line map, and text content. For compound
    nodes (e.g., heading, blockquote) where node.content is empty, content
    is sourced from the first inline child token.

    Args:
        node: A SyntaxTreeNode from the parsed AST.

    Returns:
        A dictionary with keys: type, tag, map, content.
        ``map`` is either a list of two ints [start, end] or None.
    """
    # Use direct SyntaxTreeNode property accessors (available on all non-root nodes)
    map_raw = node.map
    map_val: list[int] | None = list(map_raw) if map_raw is not None else None
    content = node.content or ""

    # For compound nodes (heading, blockquote, etc.), node.content is empty.
    # Extract inline child content for richer output.
    if not content:
        for child in node.children:
            if child.type == "inline":
                content = child.content or ""
                break

    return {
        "type": node.type,
        "tag": node.tag,
        "map": map_val,
        "content": content,
    }


def _read_file(file_path: str) -> tuple[str | None, int]:
    """Read a file and return its contents and an exit code.

    Args:
        file_path: Path to the file to read.

    Returns:
        A tuple of (content, exit_code). If the file is not found or
        cannot be read, content is None and exit_code is 2.
    """
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}")
        return None, 2
    try:
        content = path.read_text(encoding="utf-8")
        return content, 0
    except OSError as exc:
        print(f"Error reading file {file_path}: {exc}")
        return None, 2


def ast_parse(file_path: str, json_output: bool = True) -> int:
    """Parse a markdown file and output the AST as JSON.

    Reads the file, parses it with JerryDocument, and prints a JSON object
    containing the file path, the flat token list, and the full AST tree.

    Args:
        file_path: Path to the markdown file to parse.
        json_output: Unused flag kept for API symmetry; output is always JSON.

    Returns:
        0 on success, 2 if the file cannot be read.
    """
    source, exit_code = _read_file(file_path)
    if source is None:
        return exit_code

    doc = JerryDocument.parse(source)

    output = {
        "file": file_path,
        "tokens": [token_to_dict(t) for t in doc.tokens],
        "tree": _tree_to_dict(doc.tree),
    }
    print(json.dumps(output, indent=2))
    return 0


def ast_render(file_path: str) -> int:
    """Roundtrip parse-render a markdown file through mdformat.

    Reads the file, parses it with JerryDocument, renders it via mdformat
    normalization, and writes the result to stdout.

    Args:
        file_path: Path to the markdown file to render.

    Returns:
        0 on success, 2 if the file cannot be read.
    """
    source, exit_code = _read_file(file_path)
    if source is None:
        return exit_code

    doc = JerryDocument.parse(source)
    rendered = doc.render()
    print(rendered, end="")
    return 0


def ast_validate(file_path: str, schema: str | None = None) -> int:
    """Validate a markdown file against an optional entity schema.

    Parses the file to ensure it is valid markdown.  When ``schema`` is
    provided it must be one of the built-in WORKTRACKER entity type names
    (``epic``, ``feature``, ``story``, ``enabler``, ``task``, ``bug``).  The
    document is then validated against the corresponding EntitySchema and a
    JSON report is printed to stdout.

    Without ``--schema``: validates that the file is parseable and prints a
    simple OK message.

    With ``--schema <type>``: performs full structural validation (frontmatter
    fields, required sections, nav table) and prints a structured JSON report.
    Returns exit code 1 if any violations are found.

    Args:
        file_path: Path to the markdown file to validate.
        schema: Optional entity type string (e.g., "epic", "story").  When
            provided the document is validated against the corresponding
            built-in EntitySchema.

    Returns:
        0 on success, 1 if schema violations are found, 2 if the file cannot
        be read or the schema type is unknown.
    """
    source, exit_code = _read_file(file_path)
    if source is None:
        return exit_code

    doc = JerryDocument.parse(source)

    if schema is None:
        print(f"Validation OK: {file_path}")
        return 0

    # Look up the entity schema; treat unknown schema type as a usage error.
    try:
        entity_schema = get_entity_schema(schema)
    except ValueError as exc:
        print(f"Error: {exc}")
        return 2

    report = validate_document(doc, entity_schema)

    output: dict[str, Any] = {
        "file": file_path,
        "schema": schema,
        "entity_type": report.entity_type,
        "is_valid": report.is_valid,
        "field_count": report.field_count,
        "section_count": report.section_count,
        "violation_count": len(report.violations),
        "violations": [
            {
                "field_path": v.field_path,
                "expected": v.expected,
                "actual": v.actual,
                "severity": v.severity,
                "message": v.message,
            }
            for v in report.violations
        ],
    }
    print(json.dumps(output, indent=2))

    return 0 if report.is_valid else 1


def ast_query(file_path: str, selector: str, json_output: bool = True) -> int:
    """Query AST nodes by type and output structured JSON.

    Reads the file, parses it with JerryDocument, queries all nodes matching
    the given selector (node type), and prints a JSON object with the
    selector name, match count, and serialized node list.

    Args:
        file_path: Path to the markdown file to query.
        selector: The node type string to query (e.g., "heading", "blockquote").
        json_output: Unused flag kept for API symmetry; output is always JSON.

    Returns:
        0 on success (including when no nodes match), 2 if the file cannot
        be read.
    """
    source, exit_code = _read_file(file_path)
    if source is None:
        return exit_code

    doc = JerryDocument.parse(source)
    nodes = doc.query(selector)

    output = {
        "selector": selector,
        "count": len(nodes),
        "nodes": [node_to_dict(n) for n in nodes],
    }
    print(json.dumps(output, indent=2))
    return 0
