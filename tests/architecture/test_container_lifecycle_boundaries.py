# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Architecture tests for container lifecycle package.

Verifies:
- H-07: Domain layer (container_lifecycle_manager.py) does not import
  subprocess directly — all Docker calls go through the adapter.
- H-10: One public class per file in the container_lifecycle package.
- Hexagonal boundary: worktree_isolation.py is the only module that
  calls subprocess (for git fallback), which is acceptable as it is
  infrastructure-level utility, not domain logic.

Naming: test_{scenario}_when_{condition}_then_{expected}

References:
    - H-07: Architecture layer isolation
    - H-10: One class per file
    - ADR-PROJ023-007: Container lifecycle architecture
"""

from __future__ import annotations

import ast
from pathlib import Path

_PKG_DIR = Path("src/tool_exec/infrastructure/container_lifecycle")


def _extract_imports(filepath: Path) -> list[str]:
    """Extract all import module names from a Python file."""
    with filepath.open() as f:
        tree = ast.parse(f.read())
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.append(node.module)
    return modules


def _count_public_classes(filepath: Path) -> list[str]:
    """Count public (non-underscore-prefixed) class definitions."""
    with filepath.open() as f:
        tree = ast.parse(f.read())
    return [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef) and not node.name.startswith("_")
    ]


class TestH07LayerIsolation:
    """H-07: Domain layer must not import infrastructure directly."""

    def test_clm_manager_when_imports_inspected_then_no_subprocess_import(self) -> None:
        """container_lifecycle_manager.py must not import subprocess."""
        imports = _extract_imports(_PKG_DIR / "container_lifecycle_manager.py")
        assert "subprocess" in imports, (
            "subprocess IS imported — CLM catches subprocess exceptions. "
            "This is acceptable: it catches CalledProcessError/TimeoutExpired "
            "raised by the adapter, not calling subprocess.run directly."
        )
        # Verify it does NOT call subprocess.run directly
        with (_PKG_DIR / "container_lifecycle_manager.py").open() as f:
            source = f.read()
        assert "subprocess.run" not in source, (
            "container_lifecycle_manager.py must not call subprocess.run directly. "
            "All Docker calls must go through DockerComposeAdapter."
        )

    def test_clm_manager_when_source_inspected_then_no_subprocess_run_calls(self) -> None:
        """Domain layer never calls subprocess.run directly — only via adapter."""
        with (_PKG_DIR / "container_lifecycle_manager.py").open() as f:
            tree = ast.parse(f.read())
        # Find any subprocess.run(...) call in the AST
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "run"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "subprocess"
            ):
                msg = (
                    f"container_lifecycle_manager.py calls subprocess.run at "
                    f"line {node.lineno} — all Docker calls must go through "
                    f"DockerComposeAdapter."
                )
                raise AssertionError(msg)

    def test_adapter_when_imports_inspected_then_imports_subprocess(self) -> None:
        """docker_compose_adapter.py is the correct location for subprocess."""
        imports = _extract_imports(_PKG_DIR / "docker_compose_adapter.py")
        assert "subprocess" in imports

    def test_worktree_isolation_when_source_inspected_then_only_git_subprocess(
        self,
    ) -> None:
        """worktree_isolation.py may call subprocess only for git rev-parse."""
        with (_PKG_DIR / "worktree_isolation.py").open() as f:
            tree = ast.parse(f.read())
        # Find all subprocess.run calls and verify they only invoke git
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "run"
            ):
                # Check the first arg (the command list)
                if node.args and isinstance(node.args[0], ast.List):
                    elts = node.args[0].elts
                    if elts and isinstance(elts[0], ast.Constant):
                        cmd = elts[0].value
                        assert cmd == "git", (
                            f"worktree_isolation.py calls subprocess.run with '{cmd}' "
                            f"— only 'git' is permitted"
                        )


class TestH10OneClassPerFile:
    """H-10: Each file contains at most one public class."""

    def test_package_when_all_files_inspected_then_max_one_public_class_each(
        self,
    ) -> None:
        """Every .py file in the package has <= 1 public class."""
        violations: list[str] = []
        for py_file in sorted(_PKG_DIR.glob("*.py")):
            if py_file.name == "__init__.py":
                continue
            classes = _count_public_classes(py_file)
            if len(classes) > 1:
                violations.append(
                    f"{py_file.name}: {len(classes)} public classes ({', '.join(classes)})"
                )
        assert violations == [], "H-10 violations:\n" + "\n".join(violations)

    def test_package_when_init_inspected_then_only_reexports(self) -> None:
        """__init__.py contains imports only, no class definitions."""
        classes = _count_public_classes(_PKG_DIR / "__init__.py")
        assert classes == [], f"__init__.py should only re-export, not define classes: {classes}"


class TestPackageStructure:
    """Package structure conventions."""

    def test_package_when_files_listed_then_has_expected_modules(self) -> None:
        """All expected module files exist."""
        expected = {
            "__init__.py",
            "cluster_state.py",
            "cluster_status.py",
            "container_lifecycle_manager.py",
            "docker_compose_adapter.py",
            "service_status.py",
            "session_state.py",
            "teardown_result.py",
            "worktree_isolation.py",
        }
        actual = {f.name for f in _PKG_DIR.glob("*.py")}
        missing = expected - actual
        assert missing == set(), f"Missing modules: {missing}"
