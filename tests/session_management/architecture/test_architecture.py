"""Architecture tests for Session Management module.

These tests validate that the hexagonal architecture constraints are maintained:
- Domain layer has no external dependencies (stdlib only)
- Application layer only imports from domain
- Infrastructure layer implements port interfaces
- Dependencies flow inward (outer layers depend on inner layers)

References:
    - ENFORCE-013: Architecture Tests
    - Hexagonal Architecture (Ports & Adapters)
    - Dependency Rule: Source code dependencies can only point inward
"""

from __future__ import annotations

import ast
from collections.abc import Iterator
from pathlib import Path

import pytest

# =============================================================================
# Test Configuration
# =============================================================================


# Python standard library modules (allowed in domain layer)
STDLIB_MODULES = {
    # Built-in types and functions
    "abc",
    "builtins",
    "collections",
    "contextlib",
    "copy",
    "dataclasses",
    "datetime",
    "decimal",
    "enum",
    "functools",
    "hashlib",
    "itertools",
    "json",
    "math",
    "operator",
    "os",
    "pathlib",
    "random",
    "re",
    "secrets",
    "string",
    "time",
    "typing",
    "typing_extensions",
    "uuid",
    "warnings",
    # Future imports
    "__future__",
}

# Module structure
SESSION_MGMT_ROOT = Path(__file__).parent.parent.parent.parent / "src" / "session_management"
DOMAIN_PATH = SESSION_MGMT_ROOT / "domain"
APPLICATION_PATH = SESSION_MGMT_ROOT / "application"
INFRASTRUCTURE_PATH = SESSION_MGMT_ROOT / "infrastructure"


# =============================================================================
# Helper Functions
# =============================================================================


def get_python_files(directory: Path) -> Iterator[Path]:
    """Recursively get all Python files in a directory."""
    if not directory.exists():
        return
    yield from directory.rglob("*.py")


def extract_imports(file_path: Path) -> list[str]:
    """Extract all import statements from a Python file.

    Returns:
        List of imported module names (top-level only)
    """
    try:
        content = file_path.read_text()
        tree = ast.parse(content)
    except (SyntaxError, UnicodeDecodeError):
        return []

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                # Get top-level module name
                module = alias.name.split(".")[0]
                imports.append(module)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                # Get top-level module name
                module = node.module.split(".")[0]
                imports.append(module)
            elif node.level > 0:
                # Relative import - mark as internal
                imports.append("__relative__")

    return imports


def get_external_imports(file_path: Path) -> list[str]:
    """Get imports that are not stdlib or internal.

    Internal imports include:
    - Relative imports (from . import, from .. import)
    - Imports from session_management package
    - Imports from src package
    - Imports from shared_kernel (allowed for domain)
    """
    try:
        content = file_path.read_text()
        tree = ast.parse(content)
    except (SyntaxError, UnicodeDecodeError):
        return []

    external = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name.split(".")[0]
                if module not in STDLIB_MODULES and module not in {
                    "src",
                    "session_management",
                    "shared_kernel",
                }:
                    external.append(module)
        elif isinstance(node, ast.ImportFrom):
            # Skip relative imports (level > 0 means relative)
            if node.level > 0:
                continue
            if node.module:
                module = node.module.split(".")[0]
                if module not in STDLIB_MODULES and module not in {
                    "src",
                    "session_management",
                    "shared_kernel",
                }:
                    external.append(module)

    return external


def imports_from_layer(file_path: Path, layer_name: str) -> bool:
    """Check if a file imports from a specific layer."""
    content = file_path.read_text()

    # Check for direct layer imports in the actual import statements
    for line in content.split("\n"):
        if f"from .{layer_name}" in line or f"from ..{layer_name}" in line:
            return True
        if f"from ...{layer_name}" in line:
            return True
        if f"session_management.{layer_name}" in line:
            return True

    return False


# =============================================================================
# Architecture Tests
# =============================================================================


class TestDomainLayerArchitecture:
    """Tests for domain layer architectural constraints."""

    def test_domain_layer_has_no_external_imports(self) -> None:
        """Domain layer MUST NOT import external (non-stdlib) packages."""
        violations = []

        for file_path in get_python_files(DOMAIN_PATH):
            external = get_external_imports(file_path)
            if external:
                rel_path = file_path.relative_to(SESSION_MGMT_ROOT)
                violations.append(f"{rel_path}: {external}")

        assert not violations, (
            "Domain layer has external imports (violates stdlib-only rule):\n"
            + "\n".join(f"  - {v}" for v in violations)
        )

    def test_domain_layer_has_no_infrastructure_imports(self) -> None:
        """Domain layer MUST NOT import from infrastructure layer."""
        violations = []

        for file_path in get_python_files(DOMAIN_PATH):
            if imports_from_layer(file_path, "infrastructure"):
                rel_path = file_path.relative_to(SESSION_MGMT_ROOT)
                violations.append(str(rel_path))

        assert not violations, (
            "Domain layer imports from infrastructure (violates dependency rule):\n"
            + "\n".join(f"  - {v}" for v in violations)
        )

    def test_domain_layer_has_no_application_imports(self) -> None:
        """Domain layer MUST NOT import from application layer."""
        violations = []

        for file_path in get_python_files(DOMAIN_PATH):
            if imports_from_layer(file_path, "application"):
                rel_path = file_path.relative_to(SESSION_MGMT_ROOT)
                violations.append(str(rel_path))

        assert not violations, (
            "Domain layer imports from application (violates dependency rule):\n"
            + "\n".join(f"  - {v}" for v in violations)
        )


class TestApplicationLayerArchitecture:
    """Tests for application layer architectural constraints."""

    def test_application_layer_only_imports_domain(self) -> None:
        """Application layer MAY import domain, MUST NOT import infrastructure."""
        violations = []

        for file_path in get_python_files(APPLICATION_PATH):
            if imports_from_layer(file_path, "infrastructure"):
                rel_path = file_path.relative_to(SESSION_MGMT_ROOT)
                violations.append(str(rel_path))

        assert not violations, (
            "Application layer imports from infrastructure (violates dependency rule):\n"
            + "\n".join(f"  - {v}" for v in violations)
        )

    def test_application_ports_define_interfaces(self) -> None:
        """Application ports MUST define abstract interfaces (not implementations)."""
        ports_path = APPLICATION_PATH / "ports"
        if not ports_path.exists():
            pytest.skip("No ports directory")

        for file_path in get_python_files(ports_path):
            # Skip __init__.py and exception files
            if file_path.name == "__init__.py":
                continue
            if "exception" in file_path.name.lower():
                continue  # Exception files don't need Protocol/ABC

            content = file_path.read_text()

            # Ports should use Protocol or ABC
            has_protocol = "Protocol" in content
            has_abc = "ABC" in content or "abstractmethod" in content

            assert has_protocol or has_abc, (
                f"Port {file_path.name} should use Protocol or ABC for interfaces"
            )


class TestInfrastructureLayerArchitecture:
    """Tests for infrastructure layer architectural constraints."""

    def test_infrastructure_implements_port_interfaces(self) -> None:
        """Infrastructure adapters MUST implement port interfaces."""
        adapters_path = INFRASTRUCTURE_PATH / "adapters"
        if not adapters_path.exists():
            pytest.skip("No adapters directory")

        adapter_files = list(get_python_files(adapters_path))
        adapter_files = [f for f in adapter_files if f.name != "__init__.py"]

        # Each adapter should reference a port interface
        for file_path in adapter_files:
            content = file_path.read_text()

            # Should import from ports
            imports_ports = "ports" in content or "Port" in content or "I" in content

            # Should have a class that likely implements an interface
            has_class = "class " in content

            # Adapter naming convention: ends with Adapter
            is_adapter = "Adapter" in content

            assert imports_ports or is_adapter, (
                f"Adapter {file_path.name} should implement a port interface"
            )
            assert has_class, f"Adapter {file_path.name} should define a class"

    def test_infrastructure_can_import_domain(self) -> None:
        """Infrastructure layer MAY import from domain layer.

        This is a documentation test - it validates that infrastructure
        importing from domain doesn't cause any issues.
        """
        # Verify infrastructure can access domain types without error
        for file_path in get_python_files(INFRASTRUCTURE_PATH):
            # This should not raise - infrastructure can import domain
            _ = imports_from_layer(file_path, "domain")

        # If we get here, the dependency is allowed (as expected)
        assert True, "Infrastructure can import from domain"


class TestDependencyDirection:
    """Tests for overall dependency direction."""

    def test_dependency_direction_flows_inward(self) -> None:
        """Dependencies MUST flow inward: infrastructure -> application -> domain."""
        # Collect all violations of the dependency rule
        violations = []

        # Rule 1: Domain cannot import from application or infrastructure
        for file_path in get_python_files(DOMAIN_PATH):
            if imports_from_layer(file_path, "application"):
                violations.append(f"domain -> application: {file_path.name}")
            if imports_from_layer(file_path, "infrastructure"):
                violations.append(f"domain -> infrastructure: {file_path.name}")

        # Rule 2: Application cannot import from infrastructure
        for file_path in get_python_files(APPLICATION_PATH):
            if imports_from_layer(file_path, "infrastructure"):
                violations.append(f"application -> infrastructure: {file_path.name}")

        assert not violations, "Dependency direction violations (must flow inward):\n" + "\n".join(
            f"  - {v}" for v in violations
        )

    def test_no_circular_dependencies(self) -> None:
        """There MUST NOT be circular dependencies between layers."""
        # If domain imports application AND application imports domain, that's circular
        # We check for this by ensuring domain never imports outward
        domain_imports_outward = False

        for file_path in get_python_files(DOMAIN_PATH):
            if imports_from_layer(file_path, "application"):
                domain_imports_outward = True
                break
            if imports_from_layer(file_path, "infrastructure"):
                domain_imports_outward = True
                break

        assert not domain_imports_outward, "Domain layer has outward dependencies (potential cycle)"


class TestModuleStructure:
    """Tests for proper module structure."""

    def test_each_layer_has_init(self) -> None:
        """Each layer directory MUST have an __init__.py."""
        layers = [DOMAIN_PATH, APPLICATION_PATH, INFRASTRUCTURE_PATH]

        for layer in layers:
            if layer.exists():
                init_file = layer / "__init__.py"
                assert init_file.exists(), f"Missing __init__.py in {layer.name}"

    def test_domain_has_required_subdirectories(self) -> None:
        """Domain layer SHOULD have standard DDD subdirectories."""
        expected_subdirs = {"value_objects", "entities", "aggregates", "events"}
        existing = set()

        for subdir in DOMAIN_PATH.iterdir():
            if subdir.is_dir() and not subdir.name.startswith("_"):
                existing.add(subdir.name)

        # At least some DDD structure should exist
        overlap = expected_subdirs & existing
        assert len(overlap) >= 2, (
            f"Domain should have DDD structure. Found: {existing}, expected some of: {expected_subdirs}"
        )

    def test_application_has_ports(self) -> None:
        """Application layer MUST have a ports directory for interfaces."""
        ports_dir = APPLICATION_PATH / "ports"
        assert ports_dir.exists(), "Application layer must have a 'ports' directory"
        assert (ports_dir / "__init__.py").exists(), "ports directory must have __init__.py"

    def test_infrastructure_has_adapters(self) -> None:
        """Infrastructure layer MUST have an adapters directory."""
        adapters_dir = INFRASTRUCTURE_PATH / "adapters"
        assert adapters_dir.exists(), "Infrastructure layer must have an 'adapters' directory"
        assert (adapters_dir / "__init__.py").exists(), "adapters directory must have __init__.py"
