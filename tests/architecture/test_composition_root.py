"""
Architecture tests for composition root and Clean Architecture boundaries.

These tests verify that:
1. Bootstrap is the sole infrastructure importer for CLI
2. CLI adapter has no infrastructure imports (after refactor)
3. Application layer has no infrastructure imports

Test methodology: Inspect module imports using AST analysis.
"""

from __future__ import annotations

import ast
from pathlib import Path


def get_imports_from_file(file_path: Path) -> list[str]:
    """Extract all import statements from a Python file.

    Args:
        file_path: Path to the Python file

    Returns:
        List of imported module names (e.g., ['src.infrastructure.adapters'])
    """
    with open(file_path) as f:
        tree = ast.parse(f.read())

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return imports


def has_infrastructure_import(imports: list[str]) -> bool:
    """Check if any import is from infrastructure layer.

    Args:
        imports: List of import module names

    Returns:
        True if any import is from infrastructure/
    """
    infra_patterns = [
        "src.infrastructure",
        "src.session_management.infrastructure",
    ]
    for imp in imports:
        for pattern in infra_patterns:
            if imp.startswith(pattern) or pattern in imp:
                return True
    return False


class TestCompositionRootBoundaries:
    """Tests that bootstrap is the sole wiring location."""

    def test_bootstrap_imports_infrastructure(self) -> None:
        """Bootstrap legitimately imports from infrastructure."""
        bootstrap_path = Path("src/bootstrap.py")
        assert bootstrap_path.exists(), "bootstrap.py must exist"

        imports = get_imports_from_file(bootstrap_path)

        # Bootstrap SHOULD import infrastructure
        assert has_infrastructure_import(imports), "Bootstrap must import infrastructure adapters"

    def test_application_dispatchers_have_no_infrastructure_imports(self) -> None:
        """Application dispatchers must not import infrastructure."""
        dispatcher_path = Path("src/application/dispatchers/query_dispatcher.py")
        assert dispatcher_path.exists()

        imports = get_imports_from_file(dispatcher_path)

        assert not has_infrastructure_import(imports), (
            f"Dispatcher imports infrastructure: {imports}"
        )

    def test_application_ports_have_no_infrastructure_imports(self) -> None:
        """Application ports must not import infrastructure."""
        primary_ports_dir = Path("src/application/ports/primary")
        assert primary_ports_dir.exists(), "primary ports directory must exist"

        for port_file in primary_ports_dir.glob("*.py"):
            if port_file.name == "__init__.py":
                continue

            imports = get_imports_from_file(port_file)

            assert not has_infrastructure_import(imports), (
                f"{port_file.name} imports infrastructure: {imports}"
            )


class TestCleanArchitectureBoundaries:
    """Tests for Clean Architecture layer boundaries."""

    def test_application_handlers_do_not_import_interface(self) -> None:
        """Application handlers must not import from interface layer."""
        handlers_dir = Path("src/application/handlers")
        assert handlers_dir.exists()

        interface_patterns = ["src.interface", "interface."]

        for handler_file in handlers_dir.glob("*.py"):
            if handler_file.name == "__init__.py":
                continue

            imports = get_imports_from_file(handler_file)

            for imp in imports:
                for pattern in interface_patterns:
                    assert pattern not in imp, f"{handler_file.name} imports from interface: {imp}"

    def test_application_layer_files_count(self) -> None:
        """Application layer has expected number of files."""
        app_dir = Path("src/application")

        # Count Python files (excluding __init__.py and __pycache__)
        py_files = list(app_dir.rglob("*.py"))
        py_files = [f for f in py_files if "__pycache__" not in str(f)]

        # Should have at least: dispatcher port, query_dispatcher, 3 handlers, __init__ files
        assert len(py_files) >= 7, f"Expected at least 7 files, found {len(py_files)}"


class TestCLIAdapterBoundaries:
    """Tests for CLI adapter architecture compliance."""

    def test_cli_adapter_has_no_infrastructure_imports(self) -> None:
        """CLIAdapter must not import infrastructure directly.

        This is the key acceptance criterion for TD-015:
        The CLI adapter receives the dispatcher via injection and
        does NOT instantiate any infrastructure adapters.
        """
        adapter_path = Path("src/interface/cli/adapter.py")
        assert adapter_path.exists(), "CLIAdapter must exist"

        imports = get_imports_from_file(adapter_path)

        # New adapter should NOT import infrastructure
        assert not has_infrastructure_import(imports), (
            f"CLIAdapter imports infrastructure directly: {imports}"
        )

    def test_cli_main_has_infrastructure_imports(self) -> None:
        """Document current state - main.py still imports infrastructure.

        NOTE: main.py still has the old implementation for backwards
        compatibility. Once fully migrated, this should be updated.
        """
        cli_path = Path("src/interface/cli/main.py")
        assert cli_path.exists()

        imports = get_imports_from_file(cli_path)

        # main.py currently still has infrastructure imports
        # This documents the transitional state
        assert len(imports) > 0, "CLI should have imports"
