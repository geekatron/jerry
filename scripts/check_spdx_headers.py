#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
SPDX License Header Validation Script (EN-935, FEAT-015).

Scans Python files in specified directories (src/, scripts/, hooks/, tests/)
and validates that each file contains the required SPDX license identifier
and copyright notice in the first 5 lines.

Required headers:
    - ``# SPDX-License-Identifier: Apache-2.0``
    - ``# Copyright (c) <year> Adam Nowak`` (year-flexible pattern)

Empty ``__init__.py`` files (0 bytes) are exempt from header requirements,
as they serve only as package markers and contain no copyrightable content.

Exit Codes:
    0 - All files have valid SPDX headers
    1 - One or more files are missing required headers

References:
    - EN-935: SPDX License Header Enforcement
    - FEAT-015: License Migration Workflow
    - Apache-2.0: https://spdx.org/licenses/Apache-2.0.html
"""

from __future__ import annotations

import sys
from pathlib import Path

# =============================================================================
# Constants
# =============================================================================

SPDX_IDENTIFIER = "# SPDX-License-Identifier: Apache-2.0"
COPYRIGHT_PREFIX = "# Copyright (c)"
COPYRIGHT_HOLDER = "Adam Nowak"
SCAN_DIRECTORIES = ("src", "scripts", "hooks", "tests")
HEADER_SCAN_LINES = 5


# =============================================================================
# Validation Logic
# =============================================================================


def is_empty_init_file(file_path: Path) -> bool:
    """Check if a file is an empty ``__init__.py``.

    Empty init files (0 bytes) are package markers and do not require
    license headers.

    Args:
        file_path: Path to the file to check.

    Returns:
        True if the file is an ``__init__.py`` with 0 bytes.
    """
    return file_path.name == "__init__.py" and file_path.stat().st_size == 0


def check_file_headers(file_path: Path) -> list[str]:
    """Validate SPDX license headers in a single Python file.

    Reads the first 5 lines of the file and checks for the presence of
    both the SPDX license identifier and copyright notice.

    Args:
        file_path: Path to the Python file to validate.

    Returns:
        List of error messages. Empty list means the file passes.
    """
    errors: list[str] = []

    try:
        with open(file_path, encoding="utf-8") as f:
            head_lines = [f.readline() for _ in range(HEADER_SCAN_LINES)]
    except (OSError, UnicodeDecodeError) as exc:
        return [f"{file_path}: Could not read file: {exc}"]

    head_text = "".join(head_lines)

    if SPDX_IDENTIFIER not in head_text:
        errors.append(
            f"{file_path}: Missing '{SPDX_IDENTIFIER}' in first {HEADER_SCAN_LINES} lines"
        )

    has_copyright = any(
        line.startswith(COPYRIGHT_PREFIX) and COPYRIGHT_HOLDER in line for line in head_lines
    )
    if not has_copyright:
        errors.append(
            f"{file_path}: Missing '{COPYRIGHT_PREFIX} <year> {COPYRIGHT_HOLDER}' in first"
            f" {HEADER_SCAN_LINES} lines"
        )

    return errors


def collect_python_files(project_root: Path) -> list[Path]:
    """Collect all Python files from the scan directories.

    Scans ``src/``, ``scripts/``, ``hooks/``, and ``tests/`` for ``.py``
    files, excluding ``__pycache__`` directories.

    Args:
        project_root: Path to the project root directory.

    Returns:
        Sorted list of Python file paths to validate.
    """
    py_files: list[Path] = []

    for dir_name in SCAN_DIRECTORIES:
        scan_dir = project_root / dir_name
        if not scan_dir.exists():
            continue

        for py_file in scan_dir.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            py_files.append(py_file)

    return sorted(py_files)


# =============================================================================
# Main Entry Point
# =============================================================================


def main() -> int:
    """Run SPDX license header validation.

    Scans all Python files in the configured directories and reports
    any files missing the required SPDX license identifier or copyright
    notice.

    Returns:
        0 if all files pass validation, 1 if any failures are found.
    """
    project_root = Path(__file__).parent.parent

    print(f"Checking SPDX license headers in {project_root}...")
    print(f"  Directories: {', '.join(SCAN_DIRECTORIES)}")
    print(f"  Required: {SPDX_IDENTIFIER}")
    print(f"  Required: {COPYRIGHT_PREFIX} <year> {COPYRIGHT_HOLDER}")
    print()

    py_files = collect_python_files(project_root)

    if not py_files:
        print("WARNING: No Python files found to check.")
        return 0

    all_errors: list[str] = []
    checked_count = 0
    skipped_count = 0

    for py_file in py_files:
        if is_empty_init_file(py_file):
            skipped_count += 1
            continue

        checked_count += 1
        errors = check_file_headers(py_file)
        all_errors.extend(errors)

    print(f"Scanned {checked_count} file(s), skipped {skipped_count} empty __init__.py file(s).")

    if all_errors:
        print(f"\nFAILED: {len(all_errors)} header violation(s) found:\n")
        for error in all_errors:
            print(f"  {error}")
        print(
            "\nTo fix, add the following to the top of each file (after shebang line if present):"
        )
        print(f"  {SPDX_IDENTIFIER}")
        print(f"  {COPYRIGHT_PREFIX} <year> {COPYRIGHT_HOLDER}")
        return 1

    print("\nAll SPDX license header checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
