# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Architecture tests for configuration module boundaries.

Tests the hexagonal architecture constraints for the configuration system:
- AC-017.1: Domain layer has no infrastructure imports
- AC-017.2: Domain layer has no application imports
- AC-017.3: Adapters implement port interfaces
- AC-017.4: Composition root is sole infrastructure importer (see test_composition_root.py)

References:
    - WI-017: Architecture Tests
    - .claude/rules/architecture-standards.md
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

import pytest

# =============================================================================
# Helper Functions
# =============================================================================


def get_module_imports(file_path: Path) -> list[str]:
    """Extract module-level imports from a Python file.

    Args:
        file_path: Path to the Python file

    Returns:
        List of imported module names
    """
    with open(file_path) as f:
        tree = ast.parse(f.read())

    imports = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return imports


def has_layer_import(imports: list[str], layer: str) -> bool:
    """Check if any import is from a specific layer.

    Args:
        imports: List of import module names
        layer: Layer name to check (e.g., 'infrastructure', 'application')

    Returns:
        True if any import is from the specified layer
    """
    layer_patterns = [
        f"src.{layer}",
        f"src.session_management.{layer}",
        f"src.work_tracking.{layer}",
    ]

    for imp in imports:
        for pattern in layer_patterns:
            if imp.startswith(pattern) or pattern in imp:
                return True
    return False


# =============================================================================
# Domain Layer Boundary Tests
# =============================================================================


class TestDomainLayerBoundaries:
    """Verify domain layer has no external dependencies (AC-017.1, AC-017.2)."""

    def test_work_tracking_domain_has_no_infrastructure_imports(self) -> None:
        """Work tracking domain layer must not import infrastructure."""
        domain_dir = Path("src/work_tracking/domain")
        if not domain_dir.exists():
            pytest.skip("work_tracking/domain directory not found")

        violations = []
        for file in domain_dir.rglob("*.py"):
            if "__pycache__" in str(file):
                continue

            imports = get_module_imports(file)
            if has_layer_import(imports, "infrastructure"):
                violations.append(f"{file.name}: {imports}")

        assert not violations, f"Domain files import infrastructure: {violations}"

    def test_work_tracking_domain_has_no_application_imports(self) -> None:
        """Work tracking domain layer must not import application layer."""
        domain_dir = Path("src/work_tracking/domain")
        if not domain_dir.exists():
            pytest.skip("work_tracking/domain directory not found")

        violations = []
        for file in domain_dir.rglob("*.py"):
            if "__pycache__" in str(file):
                continue

            imports = get_module_imports(file)
            if has_layer_import(imports, "application"):
                violations.append(f"{file.name}: {imports}")

        assert not violations, f"Domain files import application: {violations}"

    def test_session_management_domain_has_no_infrastructure_imports(self) -> None:
        """Session management domain layer must not import infrastructure."""
        domain_dir = Path("src/session_management/domain")
        if not domain_dir.exists():
            pytest.skip("session_management/domain directory not found")

        violations = []
        for file in domain_dir.rglob("*.py"):
            if "__pycache__" in str(file):
                continue

            imports = get_module_imports(file)
            if has_layer_import(imports, "infrastructure"):
                violations.append(f"{file.name}: {imports}")

        assert not violations, f"Domain files import infrastructure: {violations}"

    def test_session_management_domain_has_no_application_imports(self) -> None:
        """Session management domain layer must not import application layer."""
        domain_dir = Path("src/session_management/domain")
        if not domain_dir.exists():
            pytest.skip("session_management/domain directory not found")

        violations = []
        for file in domain_dir.rglob("*.py"):
            if "__pycache__" in str(file):
                continue

            imports = get_module_imports(file)
            if has_layer_import(imports, "application"):
                violations.append(f"{file.name}: {imports}")

        assert not violations, f"Domain files import application: {violations}"

    def test_shared_kernel_has_no_infrastructure_imports(self) -> None:
        """Shared kernel must not import infrastructure."""
        kernel_dir = Path("src/shared_kernel")
        if not kernel_dir.exists():
            pytest.skip("shared_kernel directory not found")

        violations = []
        for file in kernel_dir.rglob("*.py"):
            if "__pycache__" in str(file):
                continue

            imports = get_module_imports(file)
            if has_layer_import(imports, "infrastructure"):
                violations.append(f"{file.name}: {imports}")

        assert not violations, f"Shared kernel imports infrastructure: {violations}"


# =============================================================================
# Port-Adapter Contract Tests
# =============================================================================


class TestPortAdapterContracts:
    """Verify adapters implement their port interfaces (AC-017.3)."""

    def test_layered_config_adapter_has_required_methods(self) -> None:
        """LayeredConfigAdapter must have configuration provider methods."""
        from src.infrastructure.adapters.configuration.layered_config_adapter import (
            LayeredConfigAdapter,
        )

        # Required methods for a configuration provider
        required_methods = {"get", "get_source", "all_keys"}

        adapter_methods = {m for m in dir(LayeredConfigAdapter) if not m.startswith("_")}

        missing = required_methods - adapter_methods
        assert not missing, f"LayeredConfigAdapter missing methods: {missing}"

    def test_atomic_file_adapter_has_required_methods(self) -> None:
        """AtomicFileAdapter must have file operation methods."""
        from src.infrastructure.adapters.persistence.atomic_file_adapter import (
            AtomicFileAdapter,
        )

        # Required methods for atomic file operations
        required_methods = {"read_with_lock", "write_atomic"}

        adapter_methods = {m for m in dir(AtomicFileAdapter) if not m.startswith("_")}

        missing = required_methods - adapter_methods
        assert not missing, f"AtomicFileAdapter missing methods: {missing}"

    def test_env_config_adapter_has_required_methods(self) -> None:
        """EnvConfigAdapter must have environment variable methods."""
        from src.infrastructure.adapters.configuration.env_config_adapter import (
            EnvConfigAdapter,
        )

        # Required methods for environment configuration
        required_methods = {"get", "keys", "has", "refresh"}

        adapter_methods = {m for m in dir(EnvConfigAdapter) if not m.startswith("_")}

        missing = required_methods - adapter_methods
        assert not missing, f"EnvConfigAdapter missing methods: {missing}"


# =============================================================================
# Adapter Implementation Tests
# =============================================================================


class TestAdapterImplementations:
    """Verify adapters are properly implemented."""

    def test_layered_config_adapter_can_be_instantiated(self) -> None:
        """LayeredConfigAdapter can be instantiated with default values."""
        from src.infrastructure.adapters.configuration.layered_config_adapter import (
            LayeredConfigAdapter,
        )

        # Should not raise
        adapter = LayeredConfigAdapter(
            env_prefix="TEST_",
            defaults={"test.key": "value"},
        )

        assert adapter.get("test.key") == "value"

    def test_atomic_file_adapter_can_be_instantiated(self) -> None:
        """AtomicFileAdapter can be instantiated."""
        from src.infrastructure.adapters.persistence.atomic_file_adapter import (
            AtomicFileAdapter,
        )

        # Should not raise
        adapter = AtomicFileAdapter()
        assert adapter is not None

    def test_env_config_adapter_can_be_instantiated(self) -> None:
        """EnvConfigAdapter can be instantiated."""
        from src.infrastructure.adapters.configuration.env_config_adapter import (
            EnvConfigAdapter,
        )

        # Should not raise
        adapter = EnvConfigAdapter(prefix="TEST_")
        assert adapter is not None


# =============================================================================
# Bootstrap Validation Tests
# =============================================================================


class TestBootstrapConfiguration:
    """Verify bootstrap properly wires configuration dependencies."""

    def test_bootstrap_creates_query_dispatcher(self) -> None:
        """Bootstrap can create a query dispatcher."""
        from src.bootstrap import create_query_dispatcher

        dispatcher = create_query_dispatcher()
        assert dispatcher is not None

    def test_bootstrap_has_projects_directory_function(self) -> None:
        """Bootstrap exposes projects directory function."""
        from src.bootstrap import get_projects_directory

        # Should return a string
        projects_dir = get_projects_directory()
        assert isinstance(projects_dir, str)

    def test_bootstrap_has_session_handlers_function(self) -> None:
        """Bootstrap exposes session handlers creation function."""
        from src.bootstrap import create_session_command_handlers

        handlers = create_session_command_handlers()
        assert isinstance(handlers, dict)
        assert "create" in handlers
        assert "end" in handlers
