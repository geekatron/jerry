"""
Architecture tests for cross-platform (Windows) compatibility.

These tests verify that:
1. No Unix-only modules are imported (fcntl, pwd, grp, termios, etc.)
2. No split("\\n") is used on file-sourced data (use splitlines() instead)
3. All write_text()/read_text() calls include encoding="utf-8"
4. No hardcoded Unix paths in production code

Test methodology: AST analysis and regex scanning of source files.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

# =========================================================================
# Configuration
# =========================================================================

# Directories to scan for cross-platform issues
SOURCE_DIRS = [
    Path("src"),
    Path("scripts"),
    Path("skills"),
]

# Unix-only modules that will crash on Windows with ImportError
UNIX_ONLY_MODULES = {
    "fcntl",
    "pwd",
    "grp",
    "termios",
    "resource",
    "syslog",
    "crypt",
    "nis",
    "posixpath",
}

# Files where split("\n") on in-memory-constructed data is acceptable.
# Each entry is (file_stem, line_number) for known-safe usages.
SPLIT_N_ALLOWLIST = {
    # toon_serializer line 290: splits output of _encode_object which
    # builds strings with "\n".join() - never from file I/O
    ("toon_serializer", 290),
}


# =========================================================================
# Helpers
# =========================================================================


def _collect_python_files(dirs: list[Path]) -> list[Path]:
    """Collect all .py files from the given directories."""
    files = []
    for d in dirs:
        if d.exists():
            files.extend(d.rglob("*.py"))
    return sorted(files)


def _get_module_level_imports(file_path: Path) -> list[tuple[str, int]]:
    """Extract module-level import names with line numbers.

    Returns:
        List of (module_name, line_number) tuples.
    """
    with open(file_path, encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return []

    imports = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((alias.name, node.lineno))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append((node.module, node.lineno))
    return imports


# =========================================================================
# Tests: Unix-Only Module Imports
# =========================================================================


class TestNoUnixOnlyImports:
    """Verify no Unix-only modules are imported in production code."""

    @pytest.fixture
    def python_files(self) -> list[Path]:
        return _collect_python_files(SOURCE_DIRS)

    def test_no_fcntl_import(self, python_files: list[Path]) -> None:
        """fcntl is Unix-only; use filelock instead."""
        violations = []
        for f in python_files:
            for module, lineno in _get_module_level_imports(f):
                if module == "fcntl" or module.startswith("fcntl."):
                    violations.append(f"{f}:{lineno}")

        assert not violations, (
            f"Unix-only 'fcntl' imported in {len(violations)} file(s). "
            f"Use 'filelock' instead:\n" + "\n".join(violations)
        )

    def test_no_unix_only_modules(self, python_files: list[Path]) -> None:
        """No Unix-only stdlib modules in production code."""
        violations = []
        for f in python_files:
            for module, lineno in _get_module_level_imports(f):
                base_module = module.split(".")[0]
                if base_module in UNIX_ONLY_MODULES:
                    violations.append(f"{f}:{lineno} imports '{module}'")

        assert not violations, (
            f"Unix-only module(s) imported in {len(violations)} location(s):\n"
            + "\n".join(violations)
        )


# =========================================================================
# Tests: Line Splitting
# =========================================================================


class TestSplitLineHandling:
    r"""Verify split("\\n") is not used on potentially file-sourced data.

    On Windows, files may contain \\r\\n (CRLF) line endings.
    split("\\n") leaves trailing \\r on each line, causing subtle bugs.
    Use splitlines() which handles \\n, \\r\\n, and \\r correctly.
    """

    # Pattern: .split("\n") or .split('\n')
    SPLIT_N_PATTERN = re.compile(r'\.split\(["\']\\n["\']\)')

    @pytest.fixture
    def python_files(self) -> list[Path]:
        return _collect_python_files(SOURCE_DIRS)

    def test_no_split_newline_in_source(self, python_files: list[Path]) -> None:
        r"""Production code should use splitlines() instead of split("\\n").

        Allowlisted exceptions are tracked in SPLIT_N_ALLOWLIST for cases
        where split("\\n") is used on in-memory-constructed strings that
        are guaranteed to use \\n only.
        """
        violations = []
        for f in python_files:
            try:
                content = f.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue

            for i, line in enumerate(content.splitlines(), start=1):
                if self.SPLIT_N_PATTERN.search(line):
                    # Check allowlist
                    if (f.stem, i) not in SPLIT_N_ALLOWLIST:
                        violations.append(f"{f}:{i}: {line.strip()}")

        assert not violations, (
            f'split("\\n") found in {len(violations)} location(s). '
            f"Use splitlines() for cross-platform compatibility:\n" + "\n".join(violations)
        )


# =========================================================================
# Tests: File Encoding
# =========================================================================


class TestFileEncoding:
    """Verify text file I/O specifies encoding explicitly.

    On Windows, the default encoding is the system codepage (e.g., CP1252),
    not UTF-8. All write_text()/read_text() calls should specify
    encoding="utf-8" to avoid data corruption with Unicode content.
    """

    # Patterns for write_text() and read_text() WITHOUT encoding=
    # Matches: .write_text(anything) where "encoding" is NOT in the args
    # Matches: .read_text() with no args or .read_text(something) without encoding
    WRITE_TEXT_NO_ENC = re.compile(r"\.write_text\([^)]*\)(?!.*encoding)")
    READ_TEXT_NO_ENC = re.compile(r"\.read_text\(\s*\)(?!.*encoding)")

    @pytest.fixture
    def source_files(self) -> list[Path]:
        """Only check src/ - scripts and skills may have less strict needs."""
        return _collect_python_files([Path("src")])

    def test_write_text_specifies_encoding(self, source_files: list[Path]) -> None:
        """All write_text() calls in src/ must include encoding='utf-8'."""
        violations = []
        for f in source_files:
            try:
                content = f.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue

            for i, line in enumerate(content.splitlines(), start=1):
                if ".write_text(" in line and "encoding" not in line:
                    # Skip comments
                    stripped = line.strip()
                    if not stripped.startswith("#"):
                        violations.append(f"{f}:{i}: {stripped}")

        assert not violations, (
            f"write_text() without encoding= found in {len(violations)} location(s). "
            f"Add encoding='utf-8' for Windows compatibility:\n" + "\n".join(violations)
        )

    def test_read_text_specifies_encoding(self, source_files: list[Path]) -> None:
        """All read_text() calls in src/ must include encoding='utf-8'."""
        violations = []
        for f in source_files:
            try:
                content = f.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue

            for i, line in enumerate(content.splitlines(), start=1):
                if ".read_text()" in line and "encoding" not in line:
                    # Skip comments
                    stripped = line.strip()
                    if not stripped.startswith("#"):
                        violations.append(f"{f}:{i}: {stripped}")

        assert not violations, (
            f"read_text() without encoding= found in {len(violations)} location(s). "
            f"Add encoding='utf-8' for Windows compatibility:\n" + "\n".join(violations)
        )


# =========================================================================
# Tests: Hardcoded Unix Paths
# =========================================================================


class TestNoHardcodedUnixPaths:
    """Verify no hardcoded Unix-specific paths in production code."""

    # Match /tmp/ or /var/ or /etc/ in string literals (not in comments)
    UNIX_PATH_PATTERN = re.compile(r"""['"](/tmp/|/var/|/etc/|/usr/)""")

    @pytest.fixture
    def source_files(self) -> list[Path]:
        return _collect_python_files([Path("src")])

    def test_no_hardcoded_tmp_paths(self, source_files: list[Path]) -> None:
        """Production code should use tempfile module, not /tmp/."""
        violations = []
        for f in source_files:
            try:
                content = f.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue

            for i, line in enumerate(content.splitlines(), start=1):
                stripped = line.strip()
                # Skip comments and docstrings
                if stripped.startswith("#"):
                    continue
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    continue
                # Skip docstring example lines (>>> prefix)
                if stripped.startswith(">>>"):
                    continue

                if self.UNIX_PATH_PATTERN.search(line):
                    violations.append(f"{f}:{i}: {stripped}")

        assert not violations, (
            f"Hardcoded Unix path found in {len(violations)} location(s). "
            f"Use tempfile or pathlib for cross-platform paths:\n" + "\n".join(violations)
        )
