# SPDX-License-Identifier: Apache-2.0
# Architecture test: H-07 layer boundary enforcement for proxy_infra bounded context.

"""Verify that the proxy_infra domain layer does not import infrastructure packages.

H-07: domain/ MUST NOT import from application/, infrastructure/, or interface/.
Only stdlib and shared_kernel imports are permitted in the domain layer.
"""

import ast
import pathlib

import pytest

_DOMAIN_DIR = pathlib.Path("src/proxy_infra/domain")
_FORBIDDEN_PREFIXES = (
    "pydo",
    "hcloud",
    "requests",
    "keyring",
    "yaml",
    "subprocess",
    "pathlib",
    "src.proxy_infra.infrastructure",
    "src.proxy_infra.application",
    "src.proxy_infra.interface",
)


@pytest.mark.architecture
class TestProxyInfraLayerBoundaries:
    """H-07 architecture boundary tests for proxy_infra bounded context."""

    def test_domain_layer_has_no_infrastructure_imports(self) -> None:
        """H-07: domain/ must not import infrastructure packages."""
        violations = []
        for py_file in _DOMAIN_DIR.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue
            tree = ast.parse(py_file.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    for prefix in _FORBIDDEN_PREFIXES:
                        if node.module.startswith(prefix):
                            violations.append(
                                f"{py_file}:{node.lineno}: imports {node.module}"
                            )
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        for prefix in _FORBIDDEN_PREFIXES:
                            if alias.name.startswith(prefix):
                                violations.append(
                                    f"{py_file}:{node.lineno}: imports {alias.name}"
                                )
        assert not violations, (
            f"H-07 violations in domain layer:\n" + "\n".join(violations)
        )

    def test_one_class_per_file_in_bounded_context(self) -> None:
        """H-10: each Python file should contain exactly one public class."""
        violations = []
        for py_file in pathlib.Path("src/proxy_infra").rglob("*.py"):
            if py_file.name == "__init__.py":
                continue
            tree = ast.parse(py_file.read_text())
            classes = [
                n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)
            ]
            if len(classes) > 1:
                violations.append(
                    f"{py_file}: {len(classes)} classes ({', '.join(classes)})"
                )
        assert not violations, (
            f"H-10 violations:\n" + "\n".join(violations)
        )
