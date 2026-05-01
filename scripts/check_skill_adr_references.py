#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
CI check: assert every docs/adrs/ADR-NNN*.md reference in any skills/*/SKILL.md
resolves to a real file in the repository.

Detection algorithm (from ci-check-spec.md):
  1. Discover all skills/*/SKILL.md files (single-level glob).
  2. Extract Markdown link targets matching ``docs/adrs/ADR-<digits>*.md``.
  3. Resolve each target relative to the SKILL.md's directory (or repo-root if
     path does not start with ``./`` or ``../``).
  4. Assert the resolved path exists under the repository root.
  5. Report all violations with source file, line number, raw path, and resolved
     path; exit 1 if any violation found.

Usage:
    uv run python scripts/check_skill_adr_references.py          # auto-discover
    uv run python scripts/check_skill_adr_references.py skills/transcript/SKILL.md

Exit Codes:
    0 - All ADR cross-references resolve (or no references found).
    1 - One or more broken ADR cross-references detected.

References:
    - TASK-008: Add CI check: every SKILL.md ADR cross-reference resolves
    - ci-check-spec.md: Detection algorithm and error message format
    - H-05: UV only for Python execution
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Matches Markdown link targets that reference docs/adrs/ADR-<digits>*.md.
# Capture group 1: the raw path string as written in the file.
# Anchor fragments (#...) are stripped before filesystem resolution.
_ADR_LINK_RE = re.compile(r"\]\(([^)]*docs/adrs/ADR-\d+[^)]*\.md)[^)]*\)")

# Single-level glob for SKILL.md files. Nested agent sub-dirs do not have
# SKILL.md files per the spec (skills/*/SKILL.md only, not recursive).
_SKILL_GLOB = "skills/*/SKILL.md"


# ---------------------------------------------------------------------------
# Repository root detection
# ---------------------------------------------------------------------------


def get_repo_root() -> Path:
    """Return the repository root as an absolute Path.

    Runs ``git rev-parse --show-toplevel`` to locate the root. Falls back to
    the current working directory if git is unavailable (e.g., unit tests that
    set cwd to a temp directory with a fake repo structure).

    Returns:
        Absolute Path to the repository root.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        if result.returncode == 0:
            return Path(result.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return Path.cwd()


# ---------------------------------------------------------------------------
# SKILL.md discovery
# ---------------------------------------------------------------------------


def discover_skill_files(repo_root: Path) -> list[Path]:
    """Glob for all skills/*/SKILL.md files under *repo_root*.

    Uses a single-level glob (not recursive) per ci-check-spec.md Step 1.
    Paths returned are absolute.

    Args:
        repo_root: Absolute path to the repository root.

    Returns:
        Sorted list of absolute paths to discovered SKILL.md files.
    """
    return sorted(repo_root.glob(_SKILL_GLOB))


# ---------------------------------------------------------------------------
# ADR reference extraction
# ---------------------------------------------------------------------------


def extract_adr_references(skill_file: Path) -> list[tuple[int, str]]:
    """Extract all ADR cross-reference link targets from *skill_file*.

    Scans each line with ``_ADR_LINK_RE`` and returns matched raw path strings
    together with their 1-based line numbers. Anchor fragments (``#...``) are
    stripped from the captured path before returning.

    Args:
        skill_file: Absolute path to the SKILL.md file to scan.

    Returns:
        List of (line_number, raw_path) tuples; empty if none found or file
        cannot be read.
    """
    try:
        lines = skill_file.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []

    refs: list[tuple[int, str]] = []
    for lineno, line in enumerate(lines, start=1):
        for match in _ADR_LINK_RE.finditer(line):
            raw_path = match.group(1)
            # Strip anchor fragment (e.g. "...file.md#section" -> "...file.md")
            raw_path = raw_path.split("#")[0]
            refs.append((lineno, raw_path))
    return refs


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------


def resolve_adr_path(skill_file: Path, raw_path: str, repo_root: Path) -> Path:
    """Resolve *raw_path* to a repo-root-relative Path.

    Resolution rule (ci-check-spec.md Step 3):
    - If *raw_path* starts with ``./`` or ``../``, resolve relative to the
      directory containing *skill_file*.
    - Otherwise, treat *raw_path* as already repo-root-relative.

    Args:
        skill_file: Absolute path to the SKILL.md file that contains the link.
        raw_path: The raw link target string extracted from the file.
        repo_root: Absolute path to the repository root.

    Returns:
        Path relative to *repo_root* after normalization.
    """
    if raw_path.startswith("./") or raw_path.startswith("../"):
        skill_dir = skill_file.parent
        resolved_abs = (skill_dir / raw_path).resolve()
        try:
            return resolved_abs.relative_to(repo_root.resolve())
        except ValueError:
            # Path escaped the repo root; return as-is for violation reporting
            return Path(raw_path)
    else:
        # Already repo-root-relative; normalize to remove any redundant separators
        return Path(os.path.normpath(raw_path))


# ---------------------------------------------------------------------------
# Violation collection and reporting
# ---------------------------------------------------------------------------


def collect_violations(
    skill_files: list[Path],
    repo_root: Path,
) -> list[tuple[Path, int, str, Path]]:
    """Collect all broken ADR cross-references across *skill_files*.

    For each SKILL.md, extracts ADR references, resolves each one, and checks
    whether the resolved file exists under *repo_root*. Returns a list of
    (skill_file, line_number, raw_path, resolved_path) tuples for every
    reference that does NOT resolve to an existing file.

    Args:
        skill_files: Absolute paths to SKILL.md files to check.
        repo_root: Absolute path to the repository root.

    Returns:
        List of violation tuples; empty if all references resolve.
    """
    violations: list[tuple[Path, int, str, Path]] = []
    for skill_file in skill_files:
        refs = extract_adr_references(skill_file)
        for lineno, raw_path in refs:
            resolved = resolve_adr_path(skill_file, raw_path, repo_root)
            abs_resolved = repo_root / resolved
            if not abs_resolved.is_file():
                violations.append((skill_file, lineno, raw_path, resolved))
    return violations


def format_violation_line(
    repo_root: Path,
    skill_file: Path,
    lineno: int,
    raw_path: str,
    resolved: Path,
) -> str:
    """Format a single violation as an error line per ci-check-spec.md.

    Output format:
        BROKEN ADR REF: {skill_file}:{line_number}: '{raw_path}' -> resolved
        '{resolved_path}' does not exist

    *skill_file* is reported relative to *repo_root* for clean output.

    Args:
        repo_root: Absolute path to the repository root.
        skill_file: Absolute path to the SKILL.md containing the broken ref.
        lineno: 1-based line number of the broken reference.
        raw_path: Raw link target string as written in the file.
        resolved: Resolved repo-root-relative path that does not exist.

    Returns:
        Formatted error string (single line, no trailing newline).
    """
    try:
        rel_skill = skill_file.relative_to(repo_root)
    except ValueError:
        rel_skill = skill_file
    return (
        f"BROKEN ADR REF: {rel_skill}:{lineno}: '{raw_path}' "
        f"-> resolved '{resolved}' does not exist"
    )


def format_summary_line(broken_count: int, file_count: int) -> str:
    """Format the summary line printed after all violations.

    Args:
        broken_count: Number of broken ADR references found.
        file_count: Number of SKILL.md files that contained at least one broken ref.

    Returns:
        Summary string per ci-check-spec.md Failure Mode section.
    """
    return (
        f"ADR cross-reference check: {broken_count} broken reference(s) found "
        f"in {file_count} SKILL.md file(s). "
        "Fix the paths or vendor the missing ADR files."
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """Run the ADR cross-reference integrity check.

    Accepts zero or more SKILL.md file paths as positional arguments. If none
    are provided, auto-discovers all skills/*/SKILL.md files under the
    repository root.

    Args:
        argv: Command-line arguments (file paths). Defaults to ``sys.argv[1:]``.

    Returns:
        0 if all ADR references resolve; 1 if any broken reference found.
    """
    if argv is None:
        argv = sys.argv[1:]

    repo_root = get_repo_root()

    if argv:
        skill_files = [Path(p).resolve() for p in argv]
    else:
        skill_files = discover_skill_files(repo_root)

    if not skill_files:
        print("ADR cross-reference check: no SKILL.md files found. OK.")
        return 0

    violations = collect_violations(skill_files, repo_root)

    if not violations:
        print(
            f"ADR cross-reference check: all references resolve "
            f"({len(skill_files)} SKILL.md file(s) checked). OK."
        )
        return 0

    # Report each violation
    broken_files: set[Path] = set()
    for skill_file, lineno, raw_path, resolved in violations:
        print(format_violation_line(repo_root, skill_file, lineno, raw_path, resolved))
        broken_files.add(skill_file)

    # Print summary
    print(format_summary_line(len(violations), len(broken_files)))
    return 1


if __name__ == "__main__":
    sys.exit(main())
