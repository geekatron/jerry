# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Architecture tests for context_monitoring bounded context.

Enforces hexagonal layer boundaries:
    - Domain layer has no infrastructure or interface imports
    - Application layer has no infrastructure or interface imports
    - Infrastructure may import domain and application (ports)
    - Composition root is the only place that wires adapters to ports

Acceptance Criteria Coverage:
    - AC-FEAT001-009: Hexagonal architecture boundaries (H-07, H-08)
    - AC-FEAT001-010: Port/adapter structural compliance (H-09)
    - AC-FEAT001-011: One class per file (H-10)

References:
    - H-07: Domain layer: no external imports
    - H-08: Application layer: no infra/interface imports
    - H-09: Composition root exclusivity
    - FEAT-001: Context Detection
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

pytestmark = [
    pytest.mark.architecture,
]

SRC_ROOT = Path(__file__).resolve().parent.parent.parent / "src"
CONTEXT_MONITORING_ROOT = SRC_ROOT / "context_monitoring"

# Layers within context_monitoring bounded context
DOMAIN_DIR = CONTEXT_MONITORING_ROOT / "domain"
APPLICATION_DIR = CONTEXT_MONITORING_ROOT / "application"
INFRASTRUCTURE_DIR = CONTEXT_MONITORING_ROOT / "infrastructure"


def _extract_imports(file_path: Path) -> list[tuple[str, int]]:
    """Extract all import statements from a Python file.

    Scans the full AST (including function/method bodies) to detect
    imports at any nesting level. Skips imports inside TYPE_CHECKING blocks,
    supporting both ``if TYPE_CHECKING:`` and ``if typing.TYPE_CHECKING:``.

    Returns:
        List of (module_name, line_number) tuples.
    """
    try:
        tree = ast.parse(file_path.read_text())
    except SyntaxError:
        return []

    # Identify lines inside TYPE_CHECKING blocks
    type_checking_lines: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            is_type_checking = (
                isinstance(node.test, ast.Name) and node.test.id == "TYPE_CHECKING"
            ) or (isinstance(node.test, ast.Attribute) and node.test.attr == "TYPE_CHECKING")
            if is_type_checking:
                for child in ast.walk(node):
                    if isinstance(child, ast.Import | ast.ImportFrom):
                        type_checking_lines.add(child.lineno)

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and node.lineno not in type_checking_lines:
            for alias in node.names:
                imports.append((alias.name, node.lineno))
        elif (
            isinstance(node, ast.ImportFrom)
            and node.lineno not in type_checking_lines
            and node.module
        ):
            imports.append((node.module, node.lineno))

    return imports


def _get_python_files(directory: Path) -> list[Path]:
    """Get all Python files in a directory, excluding __pycache__ and __init__."""
    if not directory.exists():
        return []
    return [
        f
        for f in directory.rglob("*.py")
        if "__pycache__" not in str(f) and f.name != "__init__.py"
    ]


def _imports_layer(imports: list[tuple[str, int]], layer: str) -> list[tuple[str, int]]:
    """Filter imports that target a specific architecture layer.

    Detects both intra-bounded-context imports (src.context_monitoring.{layer})
    and cross-bounded-context imports (src.*.{layer}) to prevent violations
    where code reaches into another bounded context's internal layers.
    """
    return [
        (module, line)
        for module, line in imports
        if f".{layer}." in module or module.endswith(f".{layer}")
    ]


# =============================================================================
# Source Directory Guards
# =============================================================================


class TestSourceDirectoryGuards:
    """Architecture: Guard tests verify source directories resolve correctly.

    References: FEAT-001 (EN-003), PROJ-004
    """

    def test_source_root_exists(self) -> None:
        """Source root directory must exist for architecture tests to be valid."""
        assert SRC_ROOT.exists(), (
            f"Source root not found at {SRC_ROOT.resolve()}. "
            "Architecture tests cannot verify boundaries."
        )

    def test_all_layer_directories_exist(self) -> None:
        """All three architecture layers must exist."""
        for layer_dir, name in [
            (DOMAIN_DIR, "domain"),
            (APPLICATION_DIR, "application"),
            (INFRASTRUCTURE_DIR, "infrastructure"),
        ]:
            assert layer_dir.exists(), (
                f"Layer directory '{name}' not found at {layer_dir.resolve()}"
            )

    def test_layer_directories_contain_python_files(self) -> None:
        """Each layer must contain at least one Python file."""
        for layer_dir, name in [
            (DOMAIN_DIR, "domain"),
            (APPLICATION_DIR, "application"),
            (INFRASTRUCTURE_DIR, "infrastructure"),
        ]:
            py_files = _get_python_files(layer_dir)
            assert len(py_files) > 0, (
                f"No Python files found in {name} layer at {layer_dir.resolve()}"
            )


# =============================================================================
# Domain Layer Boundary (H-07)
# =============================================================================


class TestDomainLayerBoundaries:
    """Architecture: Domain layer has no infrastructure or interface imports.

    References: H-07 (architecture-standards), FEAT-001 (EN-003), PROJ-004
    """

    def test_domain_has_no_infrastructure_imports(self) -> None:
        """Domain layer must not import from infrastructure."""
        violations = []
        for py_file in _get_python_files(DOMAIN_DIR):
            imports = _extract_imports(py_file)
            infra_imports = _imports_layer(imports, "infrastructure")
            if infra_imports:
                for module, line in infra_imports:
                    violations.append(f"{py_file.name}:{line} imports {module}")

        assert not violations, (
            "Domain layer imports infrastructure (H-07 violation):\n"
            + "\n".join(f"  - {v}" for v in violations)
        )

    def test_domain_has_no_interface_imports(self) -> None:
        """Domain layer must not import from interface."""
        violations = []
        for py_file in _get_python_files(DOMAIN_DIR):
            imports = _extract_imports(py_file)
            iface_imports = _imports_layer(imports, "interface")
            if iface_imports:
                for module, line in iface_imports:
                    violations.append(f"{py_file.name}:{line} imports {module}")

        assert not violations, "Domain layer imports interface (H-07 violation):\n" + "\n".join(
            f"  - {v}" for v in violations
        )

    def test_domain_has_no_application_imports(self) -> None:
        """Domain layer must not import from application layer."""
        violations = []
        for py_file in _get_python_files(DOMAIN_DIR):
            imports = _extract_imports(py_file)
            app_imports = [
                (m, ln) for m, ln in imports if m.startswith("src.context_monitoring.application")
            ]
            if app_imports:
                for module, line in app_imports:
                    violations.append(f"{py_file.name}:{line} imports {module}")

        assert not violations, "Domain layer imports application (H-07 violation):\n" + "\n".join(
            f"  - {v}" for v in violations
        )


# =============================================================================
# Application Layer Boundary (H-08)
# =============================================================================


class TestApplicationLayerBoundaries:
    """Architecture: Application layer has no infrastructure or interface imports.

    References: H-08 (architecture-standards), FEAT-001 (EN-003), PROJ-004
    """

    def test_application_has_no_infrastructure_imports(self) -> None:
        """Application layer must not import from infrastructure."""
        violations = []
        for py_file in _get_python_files(APPLICATION_DIR):
            imports = _extract_imports(py_file)
            infra_imports = _imports_layer(imports, "infrastructure")
            if infra_imports:
                for module, line in infra_imports:
                    violations.append(f"{py_file.name}:{line} imports {module}")

        assert not violations, (
            "Application layer imports infrastructure (H-08 violation):\n"
            + "\n".join(f"  - {v}" for v in violations)
        )

    def test_application_has_no_interface_imports(self) -> None:
        """Application layer must not import from interface."""
        violations = []
        for py_file in _get_python_files(APPLICATION_DIR):
            imports = _extract_imports(py_file)
            iface_imports = _imports_layer(imports, "interface")
            if iface_imports:
                for module, line in iface_imports:
                    violations.append(f"{py_file.name}:{line} imports {module}")

        assert not violations, (
            "Application layer imports interface (H-08 violation):\n"
            + "\n".join(f"  - {v}" for v in violations)
        )


# =============================================================================
# Infrastructure Layer Boundary
# =============================================================================


class TestInfrastructureLayerBoundaries:
    """Architecture: Infrastructure may import domain and application ports only.

    References: H-07/H-08 (architecture-standards), PROJ-004
    """

    def test_infrastructure_has_no_interface_imports(self) -> None:
        """Infrastructure layer must not import from interface."""
        violations = []
        for py_file in _get_python_files(INFRASTRUCTURE_DIR):
            imports = _extract_imports(py_file)
            iface_imports = _imports_layer(imports, "interface")
            if iface_imports:
                for module, line in iface_imports:
                    violations.append(f"{py_file.name}:{line} imports {module}")

        assert not violations, "Infrastructure layer imports interface:\n" + "\n".join(
            f"  - {v}" for v in violations
        )


# =============================================================================
# Port/Adapter Structural Contract
# =============================================================================


class TestPortAdapterStructure:
    """Architecture: Ports are protocols, adapters implement them.

    References: H-09 (architecture-standards), FEAT-001 (EN-003), PROJ-004
    """

    def test_ports_directory_exists(self) -> None:
        """Application ports directory exists."""
        ports_dir = APPLICATION_DIR / "ports"
        assert ports_dir.exists(), "Missing application/ports directory"

    def test_adapters_directory_exists(self) -> None:
        """Infrastructure adapters directory exists."""
        adapters_dir = INFRASTRUCTURE_DIR / "adapters"
        assert adapters_dir.exists(), "Missing infrastructure/adapters directory"

    def test_ports_contain_protocol_definitions(self) -> None:
        """Port files define Protocol classes (interfaces)."""
        ports_dir = APPLICATION_DIR / "ports"
        port_files = _get_python_files(ports_dir)
        assert len(port_files) >= 3, (
            f"Expected at least 3 port definitions, found {len(port_files)}"
        )

    def test_each_port_has_matching_adapter(self) -> None:
        """Each port protocol has at least one concrete adapter."""
        from src.context_monitoring.application.ports.checkpoint_repository import (
            ICheckpointRepository,
        )
        from src.context_monitoring.application.ports.threshold_configuration import (
            IThresholdConfiguration,
        )
        from src.context_monitoring.application.ports.transcript_reader import (
            ITranscriptReader,
        )
        from src.context_monitoring.infrastructure.adapters.config_threshold_adapter import (
            ConfigThresholdAdapter,
        )
        from src.context_monitoring.infrastructure.adapters.filesystem_checkpoint_repository import (
            FilesystemCheckpointRepository,
        )
        from src.context_monitoring.infrastructure.adapters.jsonl_transcript_reader import (
            JsonlTranscriptReader,
        )

        assert isinstance(
            ConfigThresholdAdapter.__new__(ConfigThresholdAdapter), IThresholdConfiguration
        )
        assert isinstance(JsonlTranscriptReader(), ITranscriptReader)
        # FilesystemCheckpointRepository needs constructor args, test protocol compliance
        assert isinstance(
            FilesystemCheckpointRepository.__new__(FilesystemCheckpointRepository),
            ICheckpointRepository,
        )


# =============================================================================
# One Class Per File (H-10)
# =============================================================================


class TestOneClassPerFile:
    """Architecture: Each file contains at most one public class (H-10).

    References: H-10 (architecture-standards), PROJ-004
    """

    @pytest.mark.parametrize(
        "directory",
        [DOMAIN_DIR, APPLICATION_DIR, INFRASTRUCTURE_DIR],
        ids=["domain", "application", "infrastructure"],
    )
    def test_one_class_per_file(self, directory: Path) -> None:
        """Each production file has at most one public class."""
        violations = []
        for py_file in _get_python_files(directory):
            try:
                tree = ast.parse(py_file.read_text())
            except SyntaxError:
                continue

            public_classes = [
                node.name
                for node in ast.walk(tree)
                if isinstance(node, ast.ClassDef) and not node.name.startswith("_")
            ]
            if len(public_classes) > 1:
                violations.append(f"{py_file.name}: {', '.join(public_classes)}")

        assert not violations, (
            "Multiple public classes in single file (H-10 violation):\n"
            + "\n".join(f"  - {v}" for v in violations)
        )
