# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""AST CLI command implementations for the jerry ast namespace.

Provides the core functions that implement `jerry ast` subcommands:
    - ast_parse: Parse a markdown file and output the AST as JSON.
    - ast_render: Roundtrip parse-render a markdown file through mdformat.
    - ast_validate: Validate a markdown file against an optional entity schema.
    - ast_query: Query AST nodes by type and output structured JSON.
    - ast_frontmatter: Extract blockquote frontmatter fields as JSON.
    - ast_modify: Modify a frontmatter field and write back to file.
    - ast_reinject: Extract L2-REINJECT directives as JSON.

Helper serializers:
    - token_to_dict: Convert a markdown-it-py Token to a JSON-serializable dict.
    - node_to_dict: Convert a SyntaxTreeNode to a JSON-serializable dict.

Exit codes:
    0 -- Success
    1 -- Validation failure (schema violations found) or modify key error
    2 -- Parse error (file not found, unreadable, unknown schema type, etc.)

References:
    - ST-004: Add jerry ast CLI Commands
    - ST-006: Schema Validation Engine
    - ST-001: JerryDocument Facade
    - BUG-002: Route /ast Skill Through CLI
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

from markdown_it.token import Token
from markdown_it.tree import SyntaxTreeNode

from src.domain.markdown_ast import (
    JerryDocument,
    extract_frontmatter,
    extract_nav_table,
    extract_reinject_directives,
    get_entity_schema,
    validate_document,
    validate_nav_table,
)
from src.interface.cli.containment_policy import ContainmentRoot
from src.interface.cli.project_root import get_containment_roots

# ---------------------------------------------------------------------------
# Path containment constants (WI-018, M-08, M-10)
# ---------------------------------------------------------------------------

#: Maximum file size in bytes (1 MB) per M-05.
_MAX_FILE_SIZE_BYTES: int = 1_048_576

#: When True, path containment checks are enforced.
#: Set to False in test environments where temp files are outside the repo.
#: Also respects JERRY_DISABLE_PATH_CONTAINMENT env var for subprocess tests.
_ENFORCE_PATH_CONTAINMENT: bool = os.environ.get("JERRY_DISABLE_PATH_CONTAINMENT", "") != "1"

#: Short actionable remediation hint appended to containment-escape error
#: messages (A-6, BUG-010 C4 tournament, FM-007): tells the user how to
#: grant `jerry ast` access to the path they attempted, rather than
#: leaving them to guess.
_CONTAINMENT_ESCAPE_HINT: str = "configure ast.trusted_roots or pass --root"


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


def _note_if_configured_root_match(matched: ContainmentRoot, file_path: str, quiet: bool) -> None:
    """Print a stderr transparency note when containment matched via a
    configured trusted root.

    R-4 (generalized, BUG-010 Option C): when a file is allowed only
    because it falls under a user-declared ``ast.trusted_roots`` entry
    rather than the project root, the user gets a one-line signal that
    ``jerry ast`` is operating outside the project via a configured
    trusted root. Fires only for ``classification == "configured"`` --
    never for a project-root match (the expected common case) and never
    for an explicit ``--root`` match (that is the user's own deliberate
    choice, not a fallback).

    Args:
        matched: The ``ContainmentRoot`` the resolved path fell under.
        file_path: The original (un-resolved) file path, for the message.
        quiet: When True, suppresses this note (C6).
    """
    if quiet or matched.classification != "configured":
        return
    print(
        f"Note: '{file_path}' is outside the project root; jerry ast is "
        f"operating outside the project root via a configured trusted "
        f"root: {matched.path}.",
        file=sys.stderr,
    )


def _check_path_containment(
    file_path: str, explicit_root: str | None = None, quiet: bool = False
) -> tuple[Path | None, str | None]:
    """Verify that a file path is contained within an allowed root (M-08, M-10).

    Resolves the path, resolves symlinks, and verifies containment within
    at least one of the allowed containment roots (see
    ``project_root.get_containment_roots``). Also enforces the 1 MB file
    size limit (M-05).

    When ``explicit_root`` is None, the allowed roots default to the
    user's project root plus zero-or-more user-declared
    ``ast.trusted_roots`` entries (BUG-010 Option C) -- a one-line stderr
    transparency note fires when a path is allowed only via a configured
    trusted root rather than the project root (R-4). When
    ``explicit_root`` is supplied, the allowed set is EXACTLY that one
    resolved directory -- an explicit, user-discretion escape hatch so
    ``jerry ast`` can be used anywhere. Jerry's containment check is
    best-effort defense against accidental traversal, not a security
    boundary against a user who has already chosen to grant the tool
    broad access.

    Args:
        file_path: Path to the file to check.
        explicit_root: The CLI ``--root`` value, or None to use the
            default allowed-roots set.
        quiet: When True, suppresses the R-3 broad-root warning and the
            R-4 configured-root transparency note (C6).

    Returns:
        Tuple of (resolved_path, error_message). If the path is valid and
        contained, error_message is None. Otherwise, resolved_path is None
        and error_message describes the violation.
    """
    allowed_roots = get_containment_roots(explicit_root, quiet=quiet)

    # Resolve the path (follows symlinks)
    try:
        resolved = Path(file_path).resolve()
    except (OSError, ValueError) as exc:
        return None, f"Cannot resolve path: {exc}"

    # Also resolve via os.path.realpath for symlink detection (M-10)
    realpath = Path(os.path.realpath(file_path))

    # Check containment against the allowed roots (matched by
    # classification, never by array index -- BUG-010 Option C, C1 fix)
    matched = next((r for r in allowed_roots if resolved.is_relative_to(r.path)), None)
    if matched is None:
        return None, (
            f"Path escapes allowed containment roots: {file_path} ({_CONTAINMENT_ESCAPE_HINT})"
        )

    _note_if_configured_root_match(matched, file_path, quiet)

    # Check symlink resolution matches (M-10)
    if resolved != realpath:
        # Symlink detected -- verify the real path is also within an allowed root
        if not any(realpath.is_relative_to(r.path) for r in allowed_roots):
            return None, (
                f"Symlink target escapes allowed containment roots: {file_path} "
                f"({_CONTAINMENT_ESCAPE_HINT})"
            )

    # File size check (M-05)
    if resolved.exists():
        try:
            size = resolved.stat().st_size
            if size > _MAX_FILE_SIZE_BYTES:
                return None, (
                    f"File exceeds maximum size "
                    f"({size} bytes > {_MAX_FILE_SIZE_BYTES} bytes): {file_path}"
                )
        except OSError as exc:
            return None, f"Cannot stat file: {exc}"

    return resolved, None


def _read_file(
    file_path: str, root: str | None = None, quiet: bool = False
) -> tuple[str | None, int]:
    """Read a file with path containment checks and return its contents.

    Verifies path containment within an allowed root (M-08), resolves
    symlinks (M-10), and enforces file size limits (M-05) before reading.

    Args:
        file_path: Path to the file to read.
        root: Optional ``--root`` override. When supplied, containment is
            restricted to exactly this directory (BUG-010 Option C).
            When None, the default allowed-roots set applies (project
            root plus zero-or-more user-declared ``ast.trusted_roots``
            entries).
        quiet: When True, suppresses stderr transparency notes and
            broad-root warnings for this invocation (C6).

    Returns:
        A tuple of (content, exit_code). If the file is not found,
        escapes all allowed containment roots, or cannot be read, content
        is None and exit_code is 2.
    """
    # --- Path containment check (WI-018, M-08, M-10) ---
    if _ENFORCE_PATH_CONTAINMENT:
        resolved, error = _check_path_containment(file_path, root, quiet)
        if error is not None:
            print(f"Error: {error}", file=sys.stderr)
            return None, 2
        assert resolved is not None  # guaranteed by _check_path_containment
    else:
        resolved = Path(file_path).resolve()

    if not resolved.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return None, 2
    try:
        content = resolved.read_text(encoding="utf-8")
        return content, 0
    except OSError as exc:
        print(f"Error reading file {file_path}: {exc}", file=sys.stderr)
        return None, 2


def ast_parse(
    file_path: str, root: str | None = None, quiet: bool = False
) -> int:
    """Parse a markdown file and output the AST as JSON.

    Reads the file, parses it with JerryDocument, and prints a JSON object
    containing the file path, the flat token list, and the full AST tree.

    Args:
        file_path: Path to the markdown file to parse.
        root: Optional ``--root`` containment override (BUG-010 Option C).
            See ``_read_file`` for semantics.
        quiet: Suppress stderr transparency notes and broad-root warnings
            for this invocation (C6).

    Returns:
        0 on success, 2 if the file cannot be read.
    """
    source, exit_code = _read_file(file_path, root, quiet)
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


def ast_render(file_path: str, root: str | None = None, quiet: bool = False) -> int:
    """Roundtrip parse-render a markdown file through mdformat.

    Reads the file, parses it with JerryDocument, renders it via mdformat
    normalization, and writes the result to stdout.

    Args:
        file_path: Path to the markdown file to render.
        root: Optional ``--root`` containment override (BUG-010 Option C).
            See ``_read_file`` for semantics.
        quiet: Suppress stderr transparency notes and broad-root warnings
            for this invocation (C6).

    Returns:
        0 on success, 2 if the file cannot be read.
    """
    source, exit_code = _read_file(file_path, root, quiet)
    if source is None:
        return exit_code

    doc = JerryDocument.parse(source)
    rendered = doc.render()
    print(rendered, end="")
    return 0


def ast_validate(
    file_path: str,
    schema: str | None = None,
    nav: bool = False,
    root: str | None = None,
    quiet: bool = False,
) -> int:
    """Validate a markdown file against an optional entity schema.

    Parses the file to ensure it is valid markdown.  When ``schema`` is
    provided it must be one of the built-in WORKTRACKER entity type names
    (``epic``, ``feature``, ``story``, ``enabler``, ``task``, ``bug``).  The
    document is then validated against the corresponding EntitySchema and a
    JSON report is printed to stdout.

    Without ``--schema``: outputs a JSON report with nav table validation
    results (is_valid, nav_table_valid, missing/orphaned entries).

    With ``--schema <type>``: performs full structural validation (frontmatter
    fields, required sections, nav table) and prints a structured JSON report.
    Returns exit code 1 if any violations are found.

    With ``--nav``: includes detailed nav table entries in the output
    (section_name, anchor, description, line_number).

    Args:
        file_path: Path to the markdown file to validate.
        schema: Optional entity type string (e.g., "epic", "story").  When
            provided the document is validated against the corresponding
            built-in EntitySchema.
        nav: When True, include detailed nav table entries in the output.
        root: Optional ``--root`` containment override (BUG-010 Option C).
            See ``_read_file`` for semantics.
        quiet: Suppress stderr transparency notes and broad-root warnings
            for this invocation (C6).

    Returns:
        0 on success, 1 if schema violations are found, 2 if the file cannot
        be read or the schema type is unknown.
    """
    source, exit_code = _read_file(file_path, root, quiet)
    if source is None:
        return exit_code

    doc = JerryDocument.parse(source)
    nav_result = validate_nav_table(doc)

    if schema is None:
        output: dict[str, Any] = {
            "file": file_path,
            "is_valid": nav_result.is_valid,
            "nav_table_valid": nav_result.is_valid,
            "missing_nav_entries": nav_result.missing_entries,
            "orphaned_nav_entries": [entry.section_name for entry in nav_result.orphaned_entries],
            "schema_valid": True,
            "schema_violations": [],
        }
        if nav:
            raw_entries = extract_nav_table(doc) or []
            output["nav_entries"] = [
                {
                    "section_name": e.section_name,
                    "anchor": e.anchor,
                    "description": e.description,
                    "line_number": e.line_number,
                }
                for e in raw_entries
            ]
        print(json.dumps(output, indent=2))
        return 0

    # Look up the entity schema; treat unknown schema type as a usage error.
    try:
        entity_schema = get_entity_schema(schema)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    report = validate_document(doc, entity_schema)

    output = {
        "file": file_path,
        "schema": schema,
        "entity_type": report.entity_type,
        "is_valid": report.is_valid and nav_result.is_valid,
        "nav_table_valid": nav_result.is_valid,
        "missing_nav_entries": nav_result.missing_entries,
        "orphaned_nav_entries": [entry.section_name for entry in nav_result.orphaned_entries],
        "schema_valid": report.is_valid,
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
    if nav:
        raw_entries = extract_nav_table(doc) or []
        output["nav_entries"] = [
            {
                "section_name": e.section_name,
                "anchor": e.anchor,
                "description": e.description,
                "line_number": e.line_number,
            }
            for e in raw_entries
        ]
    print(json.dumps(output, indent=2))

    return 0 if (report.is_valid and nav_result.is_valid) else 1


def ast_query(
    file_path: str,
    selector: str,
    root: str | None = None,
    quiet: bool = False,
) -> int:
    """Query AST nodes by type and output structured JSON.

    Reads the file, parses it with JerryDocument, queries all nodes matching
    the given selector (node type), and prints a JSON object with the
    selector name, match count, and serialized node list.

    Args:
        file_path: Path to the markdown file to query.
        selector: The node type string to query (e.g., "heading", "blockquote").
        root: Optional ``--root`` containment override (BUG-010 Option C).
            See ``_read_file`` for semantics.
        quiet: Suppress stderr transparency notes and broad-root warnings
            for this invocation (C6).

    Returns:
        0 on success (including when no nodes match), 2 if the file cannot
        be read.
    """
    source, exit_code = _read_file(file_path, root, quiet)
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


def ast_frontmatter(file_path: str, root: str | None = None, quiet: bool = False) -> int:
    """Extract blockquote frontmatter fields from a markdown file as JSON.

    Reads the file, parses it with JerryDocument, and prints a JSON object
    mapping frontmatter key strings to value strings.  Prints ``{}`` if no
    frontmatter is found.

    Args:
        file_path: Path to the markdown file.
        root: Optional ``--root`` containment override (BUG-010 Option C).
            See ``_read_file`` for semantics.
        quiet: Suppress stderr transparency notes and broad-root warnings
            for this invocation (C6).

    Returns:
        0 on success, 2 if the file cannot be read.
    """
    source, exit_code = _read_file(file_path, root, quiet)
    if source is None:
        return exit_code

    doc = JerryDocument.parse(source)
    fm = extract_frontmatter(doc)
    print(json.dumps(dict(fm.items()), indent=2))
    return 0


def ast_modify(
    file_path: str, key: str, value: str, root: str | None = None, quiet: bool = False
) -> int:
    """Modify a frontmatter field in a markdown file and write back.

    Reads the file, parses it, modifies the named frontmatter field to the
    new value, writes the updated content back to disk using atomic write
    (temp file + rename) with TOCTOU mitigation (M-21, WI-020), and prints
    a JSON status object to stdout.

    Args:
        file_path: Path to the markdown file.
        key: The frontmatter field name to modify (case-sensitive).
        value: The new value for the field.
        root: Optional ``--root`` containment override (BUG-010 Option C).
            Threaded identically into the read-time check and the
            write-time TOCTOU recheck below, so a single invocation never
            disagrees on the allowed containment set between read and
            write.
        quiet: Suppress stderr transparency notes and broad-root warnings
            at read time (C6). The write-time internal recheck below
            always suppresses its own note independent of this flag
            (DD-3) -- see the recheck comment for rationale.

    Returns:
        0 on success, 1 if the key does not exist in frontmatter, 2 if the
        file cannot be read.
    """
    source, exit_code = _read_file(file_path, root, quiet)
    if source is None:
        return exit_code

    doc = JerryDocument.parse(source)
    fm = extract_frontmatter(doc)

    try:
        new_doc = fm.set(key, value)
    except KeyError:
        print(f"Error: Key '{key}' not found in frontmatter", file=sys.stderr)
        return 1

    new_content = new_doc.render()

    # --- Atomic write with TOCTOU mitigation (WI-020, M-21) ---
    # Re-verify path containment immediately before write (WI-020, M-21,
    # C2 fix; write-path check=use fix, BUG-010 C4 tournament A-1): calls
    # the IDENTICAL _check_path_containment routine used at read time --
    # including a fresh os.path.realpath() symlink re-resolution -- so a
    # symlink swapped between read and write is caught. The WRITE TARGET
    # is the exact resolved path THIS check validates -- never a
    # separately-resolved value captured earlier -- closing a CWE-367
    # gap where the check's own resolution was discarded and the write
    # instead used a stale `Path(file_path).resolve()` computed before
    # the check ran. This makes read-time and write-time containment
    # literally the same function call, not merely "the same algorithm
    # re-implemented" -- closing the prior TOCTOU gap at the design
    # level. quiet=True is hard-coded here (DD-3), independent of the
    # caller's ``quiet`` value -- a deliberate choice to avoid printing
    # the R-3/R-4 note twice for one logical invocation (it already
    # printed once at read time, if at all); the containment
    # ENFORCEMENT itself remains fully unconditional.
    if _ENFORCE_PATH_CONTAINMENT:
        resolved, write_time_error = _check_path_containment(file_path, root, quiet=True)
        if write_time_error is not None:
            print(
                f"Error: Path escapes allowed containment roots at write time: {file_path} "
                f"({_CONTAINMENT_ESCAPE_HINT})",
                file=sys.stderr,
            )
            return 2
        assert resolved is not None  # guaranteed by _check_path_containment
        target_path = resolved
    else:
        target_path = Path(file_path).resolve()

    temp_fd = None
    temp_path_str = None
    try:
        # Write to temp file in the same directory (ensures same filesystem for rename)
        temp_fd, temp_path_str = tempfile.mkstemp(
            dir=str(target_path.parent),
            suffix=".tmp",
            prefix=".ast_modify_",
        )
        os.write(temp_fd, new_content.encode("utf-8"))
        os.close(temp_fd)
        temp_fd = None  # Mark as closed

        # Atomic rename
        os.replace(temp_path_str, str(target_path))
        temp_path_str = None  # Mark as renamed (no cleanup needed)
    except OSError as exc:
        print(f"Error writing file {file_path}: {exc}", file=sys.stderr)
        return 2
    finally:
        # Clean up temp file descriptor if still open
        if temp_fd is not None:
            try:
                os.close(temp_fd)
            except OSError:
                pass
        # Clean up temp file if rename failed
        if temp_path_str is not None:
            try:
                os.unlink(temp_path_str)
            except OSError:
                pass

    output = {
        "file": file_path,
        "key": key,
        "value": value,
        "status": "modified",
    }
    print(json.dumps(output, indent=2))
    return 0


def ast_reinject(file_path: str, root: str | None = None, quiet: bool = False) -> int:
    """Extract all L2-REINJECT directives from a markdown file as JSON.

    Reads the file, parses it with JerryDocument, and prints a JSON list
    of directive objects.  Each object contains rank, tokens, content, and
    line_number fields.  Prints ``[]`` if no directives are found.

    Args:
        file_path: Path to the markdown file.
        root: Optional ``--root`` containment override (BUG-010 Option C).
            See ``_read_file`` for semantics.
        quiet: Suppress stderr transparency notes and broad-root warnings
            for this invocation (C6).

    Returns:
        0 on success, 2 if the file cannot be read.
    """
    source, exit_code = _read_file(file_path, root, quiet)
    if source is None:
        return exit_code

    doc = JerryDocument.parse(source)
    directives = extract_reinject_directives(doc)
    output = [
        {
            "rank": d.rank,
            "tokens": d.tokens,
            "content": d.content,
            "line_number": d.line_number,
        }
        for d in directives
    ]
    print(json.dumps(output, indent=2))
    return 0


# ---------------------------------------------------------------------------
# RE-006: New CLI subcommands (WI-017)
# ---------------------------------------------------------------------------


def ast_detect(file_path: str, root: str | None = None, quiet: bool = False) -> int:
    """Detect the document type of a markdown file.

    Uses ``DocumentTypeDetector`` with path-first, structure-fallback
    detection. Returns JSON with ``type``, ``method``, and optional
    ``warning`` fields.

    Args:
        file_path: Path to the markdown file.
        root: Optional ``--root`` containment override (BUG-010 Option C).
            See ``_read_file`` for semantics.
        quiet: Suppress stderr transparency notes and broad-root warnings
            for this invocation (C6).

    Returns:
        0 on success, 2 if the file cannot be read.
    """
    from src.domain.markdown_ast.document_type import DocumentTypeDetector

    source, exit_code = _read_file(file_path, root, quiet)
    if source is None:
        return exit_code

    doc_type, warning = DocumentTypeDetector.detect(file_path, source)

    # Determine detection method
    method = "path"
    path_type = DocumentTypeDetector._detect_from_path(_normalize_for_detection(file_path))
    if path_type is None:
        method = "structure"

    output: dict[str, str | None] = {
        "type": doc_type.value,
        "method": method,
    }
    if warning:
        output["warning"] = warning

    print(json.dumps(output, indent=2))
    return 0


def ast_sections(file_path: str, root: str | None = None, quiet: bool = False) -> int:
    """Extract XML-tagged sections from a markdown file as JSON.

    Uses ``XmlSectionParser`` to extract sections. Returns JSON list
    of section objects with ``tag_name``, ``content``, ``start_line``,
    and ``end_line`` fields.

    Args:
        file_path: Path to the markdown file.
        root: Optional ``--root`` containment override (BUG-010 Option C).
            See ``_read_file`` for semantics.
        quiet: Suppress stderr transparency notes and broad-root warnings
            for this invocation (C6).

    Returns:
        0 on success, 2 if the file cannot be read.
    """
    from src.domain.markdown_ast.input_bounds import InputBounds
    from src.domain.markdown_ast.xml_section import XmlSectionParser

    source, exit_code = _read_file(file_path, root, quiet)
    if source is None:
        return exit_code

    doc = JerryDocument.parse(source)
    result = XmlSectionParser.extract(doc, InputBounds.DEFAULT)

    sections_output = [
        {
            "tag_name": s.tag_name,
            "content": s.content,
            "start_line": s.start_line,
            "end_line": s.end_line,
        }
        for s in result.sections
    ]

    output: dict[str, Any] = {"sections": sections_output}
    if result.parse_error:
        output["parse_error"] = result.parse_error
    if result.parse_warnings:
        output["parse_warnings"] = list(result.parse_warnings)

    print(json.dumps(output, indent=2))
    return 0


def ast_metadata(file_path: str, root: str | None = None, quiet: bool = False) -> int:
    """Extract HTML comment metadata from a markdown file as JSON.

    Uses ``HtmlCommentMetadata`` to extract metadata blocks. Returns
    JSON list of block objects, each containing fields and raw comment.

    Args:
        file_path: Path to the markdown file.
        root: Optional ``--root`` containment override (BUG-010 Option C).
            See ``_read_file`` for semantics.
        quiet: Suppress stderr transparency notes and broad-root warnings
            for this invocation (C6).

    Returns:
        0 on success, 2 if the file cannot be read.
    """
    from src.domain.markdown_ast.html_comment import HtmlCommentMetadata
    from src.domain.markdown_ast.input_bounds import InputBounds

    source, exit_code = _read_file(file_path, root, quiet)
    if source is None:
        return exit_code

    doc = JerryDocument.parse(source)
    result = HtmlCommentMetadata.extract(doc, InputBounds.DEFAULT)

    blocks_output = [
        {
            "fields": [
                {"key": f.key, "value": f.value, "line_number": f.line_number} for f in block.fields
            ],
            "raw_comment": block.raw_comment,
            "line_number": block.line_number,
        }
        for block in result.blocks
    ]

    output: dict[str, Any] = {"blocks": blocks_output}
    if result.parse_error:
        output["parse_error"] = result.parse_error
    if result.parse_warnings:
        output["parse_warnings"] = list(result.parse_warnings)

    print(json.dumps(output, indent=2))
    return 0


def _normalize_for_detection(file_path: str) -> str:
    """Normalize a file path for document type detection.

    Converts to forward-slash form and strips leading ``./``.

    Args:
        file_path: Raw file path.

    Returns:
        Normalized path string.
    """
    from src.domain.markdown_ast.document_type import _normalize_path

    return _normalize_path(file_path)
