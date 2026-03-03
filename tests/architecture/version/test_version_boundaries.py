# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Architecture tests for src/version/ bounded context.

Verifies H-07 layer isolation and H-10 one class per file rules.

References:
    - BUG-002: Version bump regex rejects uppercase scopes
    - H-07: Architecture layer isolation
    - H-10: One class per file
"""

from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest

# Root of the version bounded context
VERSION_ROOT = Path("src/version")


class TestLayerIsolation:
    """H-07: Architecture layer isolation tests."""

    @pytest.mark.happy_path
    def test_domain_has_no_infrastructure_imports(self) -> None:
        """Domain layer must not import from infrastructure."""
        domain_files = list((VERSION_ROOT / "domain").rglob("*.py"))
        assert len(domain_files) > 0, "No domain files found"

        for py_file in domain_files:
            if py_file.name == "__init__.py":
                continue
            source = py_file.read_text()
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import | ast.ImportFrom):
                    module = ""
                    if isinstance(node, ast.ImportFrom) and node.module:
                        module = node.module
                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            module = alias.name
                    assert "infrastructure" not in module, (
                        f"{py_file}: domain imports infrastructure module '{module}'"
                    )

    @pytest.mark.happy_path
    def test_domain_has_no_application_imports(self) -> None:
        """Domain layer must not import from application."""
        domain_files = list((VERSION_ROOT / "domain").rglob("*.py"))

        for py_file in domain_files:
            if py_file.name == "__init__.py":
                continue
            source = py_file.read_text()
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    assert "application" not in node.module, (
                        f"{py_file}: domain imports application module '{node.module}'"
                    )

    @pytest.mark.happy_path
    def test_application_has_no_infrastructure_imports(self) -> None:
        """Application layer must not import from infrastructure."""
        app_files = list((VERSION_ROOT / "application").rglob("*.py"))
        assert len(app_files) > 0, "No application files found"

        for py_file in app_files:
            if py_file.name == "__init__.py":
                continue
            source = py_file.read_text()
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    assert "infrastructure" not in node.module, (
                        f"{py_file}: application imports infrastructure module '{node.module}'"
                    )

    @pytest.mark.happy_path
    def test_domain_only_imports_stdlib_and_shared_kernel(self) -> None:
        """Domain layer should only import stdlib and shared_kernel."""
        allowed_prefixes = ("src.shared_kernel", "src.version.domain")
        domain_files = list((VERSION_ROOT / "domain").rglob("*.py"))

        for py_file in domain_files:
            if py_file.name == "__init__.py":
                continue
            source = py_file.read_text()
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    if node.module.startswith("src."):
                        assert any(node.module.startswith(p) for p in allowed_prefixes), (
                            f"{py_file}: domain imports non-domain module '{node.module}'"
                        )


class TestOneClassPerFile:
    """H-10: One class per file tests."""

    @pytest.mark.happy_path
    def test_domain_value_objects_one_class_per_file(self) -> None:
        """Each domain value object file should contain at most one public class."""
        vo_dir = VERSION_ROOT / "domain" / "value_objects"
        for py_file in vo_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
            source = py_file.read_text()
            tree = ast.parse(source)
            public_classes = [
                node
                for node in ast.walk(tree)
                if isinstance(node, ast.ClassDef) and not node.name.startswith("_")
            ]
            assert len(public_classes) <= 1, (
                f"{py_file}: contains {len(public_classes)} public classes "
                f"({[c.name for c in public_classes]})"
            )

    @pytest.mark.happy_path
    def test_domain_services_one_class_per_file(self) -> None:
        """Each domain service file should contain at most one public class."""
        svc_dir = VERSION_ROOT / "domain" / "services"
        for py_file in svc_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
            source = py_file.read_text()
            tree = ast.parse(source)
            public_classes = [
                node
                for node in ast.walk(tree)
                if isinstance(node, ast.ClassDef) and not node.name.startswith("_")
            ]
            assert len(public_classes) <= 1, (
                f"{py_file}: contains {len(public_classes)} public classes"
            )

    @pytest.mark.happy_path
    def test_infrastructure_adapters_one_class_per_file(self) -> None:
        """Each infrastructure adapter file should contain at most one public class."""
        adapter_dir = VERSION_ROOT / "infrastructure" / "adapters"
        for py_file in adapter_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
            source = py_file.read_text()
            tree = ast.parse(source)
            public_classes = [
                node
                for node in ast.walk(tree)
                if isinstance(node, ast.ClassDef) and not node.name.startswith("_")
            ]
            assert len(public_classes) <= 1, (
                f"{py_file}: contains {len(public_classes)} public classes"
            )


class TestModuleStructure:
    """Tests for correct module structure."""

    @pytest.mark.happy_path
    def test_version_package_importable(self) -> None:
        mod = importlib.import_module("src.version")
        assert mod is not None

    @pytest.mark.happy_path
    def test_domain_package_importable(self) -> None:
        mod = importlib.import_module("src.version.domain")
        assert mod is not None

    @pytest.mark.happy_path
    def test_application_package_importable(self) -> None:
        mod = importlib.import_module("src.version.application")
        assert mod is not None

    @pytest.mark.happy_path
    def test_infrastructure_package_importable(self) -> None:
        mod = importlib.import_module("src.version.infrastructure")
        assert mod is not None

    @pytest.mark.happy_path
    def test_all_init_files_exist(self) -> None:
        """Every directory in the version package must have an __init__.py."""
        for dir_path in VERSION_ROOT.rglob("*"):
            if dir_path.is_dir() and not dir_path.name.startswith("__"):
                init_file = dir_path / "__init__.py"
                assert init_file.exists(), f"Missing __init__.py in {dir_path}"
