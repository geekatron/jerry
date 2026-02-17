#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Architecture Boundary Validation Script (EN-704, L5 Post-Hoc Verification).

Validates import boundaries across all Python files in src/ using AST analysis.
Enforces hexagonal architecture layer dependency rules:

    - domain: cannot import from application, infrastructure, interface
    - application: cannot import from infrastructure, interface
    - infrastructure: cannot import from interface
    - shared_kernel: cannot import from infrastructure, interface

Exemptions:
    - bootstrap.py (composition root) is exempt from all boundary checks
    - TYPE_CHECKING conditional imports are exempt

This script complements EN-703's L3 Pre-Action Gating by catching violations
in files that bypassed the PreToolUse hook. It scans ALL files in src/ for a
comprehensive post-hoc audit, whereas the engine evaluates individual files
on a per-tool-use basis.

Rule constants (LAYER_IMPORT_RULES, EXEMPT_FILES, RECOGNIZED_LAYERS,
BOUNDED_CONTEXTS) are imported from enforcement_rules.py to maintain a
single source of truth. A try/except fallback is provided for environments
where the module is not available.

Exit Codes:
    0 - All boundary checks pass
    1 - Boundary violations found

References:
    - EN-704: Pre-commit Quality Gates
    - EN-703: PreToolUse Enforcement Engine
    - .context/rules/architecture-standards.md
    - V-044: Pre-commit hook validation (scored 4.80 WCS)
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

# =============================================================================
# Layer Dependency Rules (SSOT: enforcement_rules.py)
# =============================================================================

try:
    from src.infrastructure.internal.enforcement.enforcement_rules import (
        BOUNDED_CONTEXTS,
        EXEMPT_FILES,
        LAYER_IMPORT_RULES,
        RECOGNIZED_LAYERS,
    )
except ImportError:
    # Fallback for environments where src is not importable.
    # These values MUST stay in sync with enforcement_rules.py.
    LAYER_IMPORT_RULES: dict[str, set[str]] = {  # type: ignore[no-redef]
        "domain": {"application", "infrastructure", "interface"},
        "application": {"infrastructure", "interface"},
        "infrastructure": {"interface"},
        "shared_kernel": {"infrastructure", "interface"},
    }
    EXEMPT_FILES: set[str] = {"bootstrap.py"}  # type: ignore[no-redef]
    BOUNDED_CONTEXTS: set[str] = {  # type: ignore[no-redef]
        "session_management",
        "work_tracking",
        "transcript",
        "configuration",
    }
    RECOGNIZED_LAYERS: set[str] = {  # type: ignore[no-redef]
        "domain",
        "application",
        "infrastructure",
        "interface",
        "shared_kernel",
    }


# =============================================================================
# Violation Data Structure
# =============================================================================


class Violation:
    """Represents a single architecture boundary violation."""

    def __init__(
        self,
        file_path: Path,
        line_number: int,
        source_layer: str,
        target_layer: str,
        import_name: str,
    ) -> None:
        """Initialize a violation record.

        Args:
            file_path: Path to the file containing the violation.
            line_number: Line number of the offending import.
            source_layer: The architectural layer of the source file.
            target_layer: The forbidden layer being imported.
            import_name: The full import module name.
        """
        self.file_path = file_path
        self.line_number = line_number
        self.source_layer = source_layer
        self.target_layer = target_layer
        self.import_name = import_name

    def __str__(self) -> str:
        """Format violation as human-readable string."""
        return (
            f"  {self.file_path}:{self.line_number}: "
            f"{self.source_layer} -> {self.target_layer} "
            f"(import {self.import_name})"
        )


# =============================================================================
# TYPE_CHECKING Detection
# =============================================================================


def _is_type_checking_block(node: ast.If) -> bool:
    """Check if an If node tests TYPE_CHECKING.

    Detects both ``if TYPE_CHECKING:`` and ``if typing.TYPE_CHECKING:``.

    Args:
        node: The If AST node to check.

    Returns:
        True if the If block tests TYPE_CHECKING.
    """
    test = node.test
    if isinstance(test, ast.Name) and test.id == "TYPE_CHECKING":
        return True
    if isinstance(test, ast.Attribute) and test.attr == "TYPE_CHECKING":
        return True
    return False


# =============================================================================
# Dynamic Import Detection
# =============================================================================


def _is_dynamic_import(node: ast.Call) -> bool:
    """Check if a Call node is a dynamic import.

    Detects ``__import__("module")`` and ``importlib.import_module("module")``.

    Args:
        node: The AST Call node to check.

    Returns:
        True if the call is a dynamic import.
    """
    # __import__("module")
    if isinstance(node.func, ast.Name) and node.func.id == "__import__":
        return True
    # importlib.import_module("module")
    if isinstance(node.func, ast.Attribute) and node.func.attr == "import_module":
        if isinstance(node.func.value, ast.Name) and node.func.value.id == "importlib":
            return True
    return False


def _extract_dynamic_imports_from_body(
    body: list[ast.stmt],
) -> list[tuple[str, int]]:
    """Extract dynamic import calls from a list of AST statements.

    Walks the statement body looking for ``__import__()`` and
    ``importlib.import_module()`` calls with string literal arguments.

    Args:
        body: List of AST statement nodes to search.

    Returns:
        List of (module_name, line_number) tuples for dynamic imports.
    """
    results: list[tuple[str, int]] = []
    for stmt in body:
        for node in ast.walk(stmt):
            if isinstance(node, ast.Call) and _is_dynamic_import(node):
                if node.args and isinstance(node.args[0], ast.Constant):
                    module_name = str(node.args[0].value)
                    results.append((module_name, node.lineno))
    return results


# =============================================================================
# Import Extraction
# =============================================================================


def extract_imports(file_path: Path) -> list[tuple[str, int]]:
    """Extract module-level import statements from a Python file.

    Skips imports inside TYPE_CHECKING blocks, which are used for
    forward references and do not create runtime dependencies.
    Also detects dynamic imports via ``__import__()`` and
    ``importlib.import_module()``.

    Args:
        file_path: Path to the Python file to analyze.

    Returns:
        List of (module_name, line_number) tuples for each import.
    """
    try:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(file_path))
    except (SyntaxError, UnicodeDecodeError):
        # Skip files that cannot be parsed
        return []

    imports: list[tuple[str, int]] = []

    for node in tree.body:
        # Only check top-level statements (module-level imports)
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((alias.name, node.lineno))

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append((node.module, node.lineno))

        elif isinstance(node, ast.If):
            if _is_type_checking_block(node):
                # Skip all imports inside TYPE_CHECKING
                continue
            else:
                # For other top-level if blocks, extract imports from body
                for child in node.body:
                    if isinstance(child, ast.Import):
                        for alias in child.names:
                            imports.append((alias.name, child.lineno))
                    elif isinstance(child, ast.ImportFrom):
                        if child.module:
                            imports.append((child.module, child.lineno))

        elif isinstance(node, ast.Expr):
            # Check for top-level dynamic import calls
            if isinstance(node.value, ast.Call) and _is_dynamic_import(node.value):
                if node.value.args and isinstance(node.value.args[0], ast.Constant):
                    module_name = str(node.value.args[0].value)
                    imports.append((module_name, node.lineno))

    # Also scan function/class bodies for dynamic imports
    imports.extend(_extract_dynamic_imports_from_body(tree.body))

    return imports


# =============================================================================
# Layer Detection
# =============================================================================


def detect_layer(file_path: Path, src_root: Path) -> str | None:
    """Detect which architectural layer a file belongs to.

    Handles both flat structure (src/domain/) and bounded context
    structure (src/session_management/domain/).

    Args:
        file_path: Path to the Python file.
        src_root: Path to the src/ directory.

    Returns:
        Layer name (e.g., 'domain', 'application') or None if not
        in a recognized layer.
    """
    try:
        relative = file_path.relative_to(src_root)
    except ValueError:
        return None

    parts = relative.parts

    if len(parts) < 2:
        # Top-level src files (like bootstrap.py, __init__.py)
        return None

    first_dir = parts[0]

    # Check if first directory is a recognized layer (flat structure)
    if first_dir in RECOGNIZED_LAYERS:
        return first_dir

    # Check if first directory is a bounded context
    if first_dir in BOUNDED_CONTEXTS:
        if len(parts) >= 3:
            second_dir = parts[1]
            if second_dir in RECOGNIZED_LAYERS:
                return second_dir

    return None


def detect_target_layer(import_name: str) -> str | None:
    """Detect which architectural layer an import targets.

    Handles both flat imports (src.domain.X) and bounded context
    imports (src.session_management.domain.X).

    Args:
        import_name: The fully qualified import module name.

    Returns:
        Layer name of the import target, or None if not targeting
        a recognized layer.
    """
    # Normalize the import path parts
    parts = import_name.split(".")

    # Must start with 'src' to be relevant
    if not parts or parts[0] != "src":
        return None

    if len(parts) < 2:
        return None

    second = parts[1]

    # Flat layer: src.domain.X, src.application.X, etc.
    if second in RECOGNIZED_LAYERS:
        return second

    # Bounded context: src.session_management.domain.X
    if second in BOUNDED_CONTEXTS:
        if len(parts) >= 3:
            third = parts[2]
            if third in RECOGNIZED_LAYERS:
                return third

    return None


# =============================================================================
# Boundary Validation
# =============================================================================


def check_file(file_path: Path, src_root: Path) -> list[Violation]:
    """Check a single Python file for architecture boundary violations.

    Args:
        file_path: Path to the Python file to check.
        src_root: Path to the src/ directory.

    Returns:
        List of Violation objects found in the file.
    """
    # Skip exempt files
    if file_path.name in EXEMPT_FILES:
        return []

    # Detect source layer
    source_layer = detect_layer(file_path, src_root)
    if source_layer is None:
        # File is not in a recognized layer, skip
        return []

    # Get forbidden layers for this source layer
    forbidden = LAYER_IMPORT_RULES.get(source_layer)
    if forbidden is None:
        # No rules for this layer (e.g., interface can import anything)
        return []

    violations: list[Violation] = []
    imports = extract_imports(file_path)

    for import_name, line_number in imports:
        target_layer = detect_target_layer(import_name)
        if target_layer is not None and target_layer in forbidden:
            violations.append(
                Violation(
                    file_path=file_path,
                    line_number=line_number,
                    source_layer=source_layer,
                    target_layer=target_layer,
                    import_name=import_name,
                )
            )

    return violations


def check_all_files(src_root: Path) -> list[Violation]:
    """Check all Python files in src/ for architecture boundary violations.

    Args:
        src_root: Path to the src/ directory.

    Returns:
        List of all Violation objects found across all files.
    """
    all_violations: list[Violation] = []

    for py_file in sorted(src_root.rglob("*.py")):
        # Skip __pycache__ directories
        if "__pycache__" in str(py_file):
            continue

        file_violations = check_file(py_file, src_root)
        all_violations.extend(file_violations)

    return all_violations


# =============================================================================
# Main Entry Point
# =============================================================================


def main() -> int:
    """Run architecture boundary validation.

    Scans all Python files in src/ and reports any import boundary
    violations according to hexagonal architecture rules.

    Returns:
        0 if no violations found, 1 if violations detected.
    """
    # Determine src/ root relative to project root
    # Support both running from project root and from scripts directory
    project_root = Path(__file__).parent.parent
    src_root = project_root / "src"

    if not src_root.exists():
        print(f"ERROR: Source directory not found: {src_root}")
        return 1

    print(f"Checking architecture boundaries in {src_root}...")

    violations = check_all_files(src_root)

    if violations:
        print(f"\nFound {len(violations)} architecture boundary violation(s):\n")

        # Group violations by source layer
        by_layer: dict[str, list[Violation]] = {}
        for v in violations:
            by_layer.setdefault(v.source_layer, []).append(v)

        for layer in sorted(by_layer):
            print(f"  [{layer}] layer violations:")
            for v in by_layer[layer]:
                print(f"    {v}")
            print()

        print("Architecture boundary rules:")
        for source, forbidden in sorted(LAYER_IMPORT_RULES.items()):
            print(f"  {source}: cannot import from {sorted(forbidden)}")

        print(
            "\nExempt files:",
            ", ".join(sorted(EXEMPT_FILES)),
        )
        print("Exempt: TYPE_CHECKING conditional imports")

        return 1

    print("All architecture boundary checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
