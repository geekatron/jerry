#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Pre-commit hook: Markdown schema validation for Jerry worktracker entities.

Validates staged markdown files against their entity schemas. Only files
in the ``projects/*/work/`` hierarchy with recognized entity prefixes
(EN-, ST-, TASK-, BUG-, FEAT-, EPIC-) are validated. All other markdown
files are silently skipped.

Schema detection uses file path patterns:
    - ``EN-*`` directories/files -> "enabler" schema
    - ``ST-*`` directories/files -> "story" schema
    - ``TASK-*`` directories/files -> "task" schema
    - ``BUG-*`` directories/files -> "bug" schema
    - ``FEAT-*`` directories/files -> "feature" schema
    - ``EPIC-*`` directories/files -> "epic" schema

Exit Codes:
    0 - No violations found (or no entity files staged)
    1 - Schema violations found (commit should be blocked)

References:
    - ST-009: Add Pre-Commit Validation Hook
    - ST-006: Schema Validation Engine
    - H-05: UV only for Python execution
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from src.domain.markdown_ast.jerry_document import JerryDocument
from src.domain.markdown_ast.schema import (
    ValidationViolation,
    get_entity_schema,
    validate_document,
)

# ---------------------------------------------------------------------------
# Schema detection from file paths
# ---------------------------------------------------------------------------

# Patterns match entity prefixes in filenames (the .md file's own name).
# Each pattern maps to an entity schema type. Matching against the filename
# (not the full path) prevents ancestor directories from causing misclassification
# (e.g., a SPIKE-001.md under FEAT-001/ should NOT be detected as "feature").
_ENTITY_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^EN-\d+"), "enabler"),
    (re.compile(r"^ST-\d+"), "story"),
    (re.compile(r"^TASK-\d+"), "task"),
    (re.compile(r"^BUG-\d+"), "bug"),
    (re.compile(r"^FEAT-\d+"), "feature"),
    (re.compile(r"^EPIC-\d+"), "epic"),
]

# Only files under projects/*/work/ are entity candidates.
_WORK_DIR_PATTERN = re.compile(r"^projects/[^/]+/work/")


def detect_schema_from_path(file_path: str) -> str | None:
    """Detect the entity schema type from a file path.

    Examines the filename for entity prefix patterns (EN-, ST-, TASK-, BUG-,
    FEAT-, EPIC-) within the ``projects/*/work/`` directory hierarchy. Returns
    the corresponding schema type string, or None if the file is not a
    recognized entity document.

    Matches against the filename only (not ancestor directories) to prevent
    misclassification of files nested under parent entity directories
    (e.g., a SPIKE-001.md under FEAT-001/ is correctly skipped).

    Args:
        file_path: Relative file path (as returned by git diff --name-only).

    Returns:
        Schema type string (e.g., "story", "epic") or None if no schema
        applies to this file path.

    Examples:
        >>> detect_schema_from_path("projects/P1/work/EPIC-001/ST-001/ST-001.md")
        'story'
        >>> detect_schema_from_path("README.md")
        None
    """
    # Must be under projects/*/work/ to be an entity file
    if not _WORK_DIR_PATTERN.search(file_path):
        return None

    # Extract filename and match against entity patterns
    filename = file_path.rsplit("/", 1)[-1] if "/" in file_path else file_path

    for pattern, schema_type in _ENTITY_PATTERNS:
        if pattern.search(filename):
            return schema_type

    return None


# ---------------------------------------------------------------------------
# File validation
# ---------------------------------------------------------------------------


def validate_file(file_path: str, schema_type: str) -> list[ValidationViolation]:
    """Validate a single file against the specified entity schema.

    Reads the file, parses it as a JerryDocument, and validates it against
    the built-in schema for the given entity type. Returns any violations
    found. If the file cannot be read, returns an empty list (graceful skip).

    Args:
        file_path: Path to the markdown file to validate.
        schema_type: Entity schema type (e.g., "story", "epic").

    Returns:
        List of ValidationViolation objects. Empty list means the file
        is valid (or could not be read).

    Examples:
        >>> violations = validate_file("projects/P1/work/ST-001/ST-001.md", "story")
        >>> len(violations)
        0
    """
    path = Path(file_path)
    if not path.exists():
        return []

    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []

    doc = JerryDocument.parse(source)
    schema = get_entity_schema(schema_type)
    report = validate_document(doc, schema)

    return list(report.violations)


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------


def format_violation(file_path: str, violation: ValidationViolation) -> str:
    """Format a validation violation for IDE-friendly output.

    Produces output in ``file:line:message`` format when a line number is
    available, or ``file:message`` format otherwise.  Both formats are
    recognized by most editors and CI systems for error navigation.

    Args:
        file_path: Path to the file containing the violation.
        violation: The validation violation to format.

    Returns:
        Formatted string in ``file:line:message`` or ``file:message`` format.

    Examples:
        >>> format_violation("ST-001.md", violation_with_line)
        "ST-001.md:3:Field 'Status' value 'bad' is not in allowed values: ..."
        >>> format_violation("ST-001.md", violation_without_line)
        "ST-001.md:Required field 'Type' is missing from frontmatter."
    """
    if violation.line_number is not None:
        # Display as 1-based line number for human/IDE consumption
        return f"{file_path}:{violation.line_number + 1}:{violation.message}"
    return f"{file_path}:{violation.message}"


def format_summary(files_checked: int, violation_count: int) -> str:
    """Format the summary line for the validation run.

    Args:
        files_checked: Number of entity files checked.
        violation_count: Total number of violations found.

    Returns:
        Summary string (e.g., "5 files checked, 0 violations found").

    Examples:
        >>> format_summary(5, 0)
        '5 files checked, 0 violations found'
    """
    return f"{files_checked} files checked, {violation_count} violations found"


# ---------------------------------------------------------------------------
# Git interaction
# ---------------------------------------------------------------------------


def get_staged_markdown_files() -> list[str]:
    """Get a list of staged markdown files from git.

    Runs ``git diff --cached --name-only --diff-filter=ACMR -- '*.md'``
    to retrieve markdown files that are staged for commit (Added, Copied,
    Modified, or Renamed).

    Returns:
        List of relative file paths for staged markdown files.
        Returns an empty list if the git command fails.

    Examples:
        >>> get_staged_markdown_files()
        ['README.md', 'projects/P1/work/ST-001/ST-001.md']
    """
    try:
        result = subprocess.run(
            [
                "git",
                "diff",
                "--cached",
                "--name-only",
                "--diff-filter=ACMR",
                "--",
                "*.md",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        if result.returncode != 0:
            return []
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def main() -> int:
    """Run pre-commit markdown schema validation on staged files.

    Detects staged markdown files, determines which ones have entity schemas,
    validates them, and reports any violations found.

    Returns:
        0 if no violations found, 1 if violations are present.
    """
    staged_files = get_staged_markdown_files()

    if not staged_files:
        return 0

    all_violations: list[tuple[str, ValidationViolation]] = []
    files_checked = 0

    for file_path in staged_files:
        schema_type = detect_schema_from_path(file_path)
        if schema_type is None:
            # Not an entity file, skip
            continue

        files_checked += 1
        violations = validate_file(file_path, schema_type)

        for v in violations:
            all_violations.append((file_path, v))

    if files_checked == 0:
        return 0

    # Print violations
    for file_path, violation in all_violations:
        print(format_violation(file_path, violation))

    # Print summary
    print(format_summary(files_checked, len(all_violations)))

    return 1 if all_violations else 0


if __name__ == "__main__":
    sys.exit(main())
