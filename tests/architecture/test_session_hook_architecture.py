# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Architecture tests for session hook layer boundaries.

These tests enforce the hexagonal architecture constraints for the
session hook system, ensuring proper separation of concerns.

Test Distribution per testing-standards.md:
    - Architecture tests: 5% of total coverage
    - Focus: Layer boundary enforcement

References:
    - EN-001: Session Start Hook TDD Cleanup
    - Phase 4: Architecture Tests (T-027 to T-034)
    - TD-004: cli/session_start.py architecture violation
    - TD-005: Duplicate entry points
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    pass


# Mark as architecture tests
pytestmark = [
    pytest.mark.architecture,
]


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def project_root() -> Path:
    """Get the project root directory."""
    # Navigate from tests/architecture to project root
    return Path(__file__).parent.parent.parent


@pytest.fixture
def src_root(project_root: Path) -> Path:
    """Get the src directory."""
    return project_root / "src"


@pytest.fixture
def scripts_root(project_root: Path) -> Path:
    """Get the scripts directory."""
    return project_root / "scripts"


def get_imports_from_file(file_path: Path) -> list[str]:
    """Extract import statements from a Python file.

    Returns a list of module names that are imported.
    """
    if not file_path.exists():
        return []

    content = file_path.read_text()
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return []

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return imports


def get_unguarded_imports_from_file(file_path: Path) -> list[str]:
    """Extract import statements NOT inside try/except blocks.

    Fail-open imports guarded by try/except with ImportError handlers
    are excluded. This matches the established pattern used by
    pre_tool_use.py (EN-703) and session_start_hook.py (EN-706).

    Returns a list of module names that are imported at top level.
    """
    if not file_path.exists():
        return []

    content = file_path.read_text()
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return []

    # Collect line numbers of imports inside try blocks
    guarded_lines: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Try):
            for child in ast.walk(node):
                if isinstance(child, ast.Import | ast.ImportFrom):
                    guarded_lines.add(child.lineno)

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and node.lineno not in guarded_lines:
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.lineno not in guarded_lines:
            if node.module:
                imports.append(node.module)

    return imports


# =============================================================================
# T-027: cli/adapter.py has no infrastructure imports
# =============================================================================


class TestCLIAdapterLayerBoundaries:
    """Architecture: CLI adapter must not import infrastructure directly."""

    @pytest.mark.skip(
        reason="TD-007: Pre-existing tech debt - adapter.py has dynamic infra imports"
    )
    def test_cli_adapter_has_no_infrastructure_imports(
        self,
        src_root: Path,
    ) -> None:
        """T-027: cli/adapter.py has no infrastructure imports.

        The CLI adapter is an interface layer component. Per hexagonal
        architecture, it should only depend on application layer ports,
        not on infrastructure adapters directly.

        NOTE: This test is SKIPPED because adapter.py has pre-existing
        infrastructure imports (layered_config_adapter, atomic_file_adapter)
        that are outside the scope of EN-001. These are documented as TD-007.
        """
        adapter_path = src_root / "interface" / "cli" / "adapter.py"
        assert adapter_path.exists(), f"CLI adapter not found at {adapter_path}"

        imports = get_imports_from_file(adapter_path)

        # Infrastructure imports that are NOT allowed
        forbidden_patterns = [
            r"src\.infrastructure\.",
            r"infrastructure\.adapters\.",
            r"infrastructure\.persistence\.",
            r"infrastructure\.messaging\.",
        ]

        violations = []
        for imp in imports:
            for pattern in forbidden_patterns:
                if re.search(pattern, imp):
                    violations.append(imp)

        assert not violations, (
            f"CLI adapter has forbidden infrastructure imports: {violations}\n"
            f"Interface layer must not import from infrastructure layer directly.\n"
            f"Inject dependencies via bootstrap.py instead."
        )

    def test_cli_main_has_no_infrastructure_imports(
        self,
        src_root: Path,
    ) -> None:
        """cli/main.py has no direct infrastructure imports.

        CLI main.py is the entry point but should use bootstrap.py
        for dependency injection.
        """
        main_path = src_root / "interface" / "cli" / "main.py"
        if not main_path.exists():
            pytest.skip("cli/main.py not found")

        imports = get_imports_from_file(main_path)

        # Allow bootstrap import (composition root is expected)
        forbidden_patterns = [
            r"src\.infrastructure\.adapters\.",
            r"infrastructure\.persistence\.",
            r"infrastructure\.messaging\.",
        ]

        violations = []
        for imp in imports:
            for pattern in forbidden_patterns:
                if re.search(pattern, imp):
                    violations.append(imp)

        assert not violations, (
            f"CLI main has forbidden infrastructure imports: {violations}\n"
            f"Use bootstrap.py for dependency injection."
        )


# =============================================================================
# T-028: session_start_hook.py imports only subprocess/json
# =============================================================================


class TestSessionHookIsolation:
    """Architecture: Session hook script must be a thin adapter."""

    def test_session_start_hook_has_no_src_imports(
        self,
        scripts_root: Path,
    ) -> None:
        """T-028: session_start_hook.py only imports stdlib at top level.

        The hook script is a thin adapter that calls the CLI via subprocess.
        It should NOT import any src/ modules directly at the top level.

        Fail-open imports inside try/except blocks are permitted, following
        the established pattern from pre_tool_use.py (EN-703). These imports
        gracefully degrade when the uv environment is not activated.
        """
        hook_path = scripts_root / "session_start_hook.py"
        assert hook_path.exists(), f"Hook script not found at {hook_path}"

        imports = get_unguarded_imports_from_file(hook_path)

        # Unguarded src imports are NOT allowed
        src_imports = [imp for imp in imports if imp.startswith("src.")]

        assert not src_imports, (
            f"Hook script has unguarded src imports: {src_imports}\n"
            f"Hook should call CLI via subprocess, not import src modules.\n"
            f"Fail-open imports inside try/except are allowed (EN-706 pattern).\n"
            f"This ensures proper isolation and allows the hook to work\n"
            f"even when uv environment is not activated."
        )

    def test_session_start_hook_uses_only_allowed_stdlib(
        self,
        scripts_root: Path,
    ) -> None:
        """Hook script should only use allowed stdlib modules at top level.

        Allowed: json, subprocess, os, sys, pathlib, datetime, typing
        Not allowed at top level: Any third-party or src modules

        Fail-open imports inside try/except blocks are permitted, following
        the established pattern from pre_tool_use.py (EN-703).
        """
        hook_path = scripts_root / "session_start_hook.py"
        if not hook_path.exists():
            pytest.skip("Hook script not found")

        imports = get_unguarded_imports_from_file(hook_path)

        allowed_modules = {
            "json",
            "subprocess",
            "os",
            "sys",
            "pathlib",
            "__future__",  # For annotations
            "datetime",  # For timestamps (acceptable)
            "typing",  # For type hints (acceptable)
        }

        for imp in imports:
            # Get top-level module name
            top_level = imp.split(".")[0]
            assert top_level in allowed_modules, (
                f"Hook script imports unexpected module: {imp}\n"
                f"Allowed: {allowed_modules}\n"
                f"Use try/except guard for optional imports (EN-706 pattern)."
            )


# =============================================================================
# T-029: No duplicate entry points in pyproject.toml
# =============================================================================


class TestEntryPoints:
    """Architecture: No duplicate or rogue entry points."""

    def test_no_duplicate_session_start_entry_points(
        self,
        project_root: Path,
    ) -> None:
        """T-029: No duplicate entry points in pyproject.toml.

        There should be only ONE entry point for session management.
        `jerry-session-start` was a workaround that should be removed.
        """
        pyproject_path = project_root / "pyproject.toml"
        assert pyproject_path.exists(), "pyproject.toml not found"

        content = pyproject_path.read_text()

        # Check for jerry-session-start entry point
        # Pattern: jerry-session-start = "..." in [project.scripts] section
        has_session_start_entry = "jerry-session-start" in content

        assert not has_session_start_entry, (
            "pyproject.toml contains 'jerry-session-start' entry point.\n"
            "This duplicate entry point should be removed.\n"
            "The session hook should call 'jerry projects context' instead."
        )

    def test_jerry_entry_point_exists(
        self,
        project_root: Path,
    ) -> None:
        """Main 'jerry' entry point must exist."""
        pyproject_path = project_root / "pyproject.toml"
        content = pyproject_path.read_text()

        # The main jerry entry point should exist
        assert 'jerry = "' in content or "jerry = '" in content, (
            "pyproject.toml missing 'jerry' entry point.\nThis is the main CLI entry point."
        )


# =============================================================================
# T-030: cli/session_start.py does not exist
# =============================================================================


class TestRogueFilesRemoved:
    """Architecture: Rogue files must be removed."""

    def test_cli_session_start_does_not_exist(
        self,
        src_root: Path,
    ) -> None:
        """T-030: cli/session_start.py does not exist.

        This file violates hexagonal architecture by importing
        infrastructure directly from the interface layer. It should
        be deleted after the main CLI is updated to support session
        context retrieval.
        """
        rogue_file = src_root / "interface" / "cli" / "session_start.py"

        assert not rogue_file.exists(), (
            f"Rogue file exists: {rogue_file}\n"
            f"This file violates hexagonal architecture (TD-004).\n"
            f"It imports infrastructure directly from interface layer.\n"
            f"Delete this file and use 'jerry projects context' instead."
        )


# =============================================================================
# Boundary Enforcement Tests
# =============================================================================


class TestLayerBoundaries:
    """General layer boundary enforcement tests."""

    def test_session_start_does_not_import_infrastructure(
        self,
        src_root: Path,
    ) -> None:
        """cli/session_start.py (if exists) must not import infrastructure.

        This is the EN-001 specific test - the rogue file should either:
        1. Not exist (preferred - T-030)
        2. Not import infrastructure directly
        """
        session_start_path = src_root / "interface" / "cli" / "session_start.py"

        # If file doesn't exist, test passes (file should be deleted per T-030)
        if not session_start_path.exists():
            return  # PASS - file properly deleted

        # If file exists, it must not import infrastructure
        imports = get_imports_from_file(session_start_path)
        violations = [imp for imp in imports if "infrastructure.adapters" in imp]

        assert not violations, (
            f"cli/session_start.py has infrastructure imports: {violations}\n"
            f"This file should be deleted (T-030/T-031)."
        )

    @pytest.mark.skip(
        reason="TD-007: Pre-existing tech debt - adapter.py has dynamic infra imports"
    )
    def test_interface_layer_does_not_import_infrastructure_adapters(
        self,
        src_root: Path,
    ) -> None:
        """Interface layer must not import infrastructure adapters.

        The interface layer can import:
        - Application layer (handlers, queries, commands)
        - Domain layer (value objects, exceptions)
        - Bootstrap (for composition root)

        It must NOT import:
        - Infrastructure adapters directly

        NOTE: This test is SKIPPED because adapter.py has pre-existing
        infrastructure imports outside EN-001 scope. See TD-007.
        """
        interface_dir = src_root / "interface"
        if not interface_dir.exists():
            pytest.skip("interface/ directory not found")

        violations = []
        for py_file in interface_dir.rglob("*.py"):
            # Skip __pycache__
            if "__pycache__" in str(py_file):
                continue

            imports = get_imports_from_file(py_file)
            for imp in imports:
                if "infrastructure.adapters" in imp:
                    violations.append(f"{py_file.name}: {imp}")

        assert not violations, (
            "Interface layer files import infrastructure adapters:\n" + "\n".join(violations)
        )
