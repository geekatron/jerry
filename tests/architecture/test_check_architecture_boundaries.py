# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for scripts/check_architecture_boundaries.py.

Validates the architecture boundary validation script's core functions:
extract_imports, detect_layer, detect_target_layer, check_file,
check_all_files, and dynamic import detection.

References:
    - EN-704: Pre-commit Quality Gates
    - MAJ-1: Adversarial critique finding requiring unit tests
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path so we can import the script
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from scripts.check_architecture_boundaries import (  # noqa: E402
    Violation,
    _extract_dynamic_imports_from_body,
    _is_dynamic_import,
    _is_type_checking_block,
    check_all_files,
    check_file,
    detect_layer,
    detect_target_layer,
    extract_imports,
)

# =============================================================================
# extract_imports tests
# =============================================================================


class TestExtractImports:
    """Tests for the extract_imports function."""

    def test_extract_imports_when_normal_import_then_includes(
        self,
        tmp_path: Path,
    ) -> None:
        """Normal top-level imports are extracted correctly."""
        py_file = tmp_path / "example.py"
        py_file.write_text(
            "import os\n"
            "from pathlib import Path\n"
            "from src.domain.aggregates.work_item import WorkItem\n"
        )

        result = extract_imports(py_file)

        module_names = [name for name, _line in result]
        assert "os" in module_names
        assert "pathlib" in module_names
        assert "src.domain.aggregates.work_item" in module_names

    def test_extract_imports_when_type_checking_block_then_skips(
        self,
        tmp_path: Path,
    ) -> None:
        """Imports inside if TYPE_CHECKING: blocks are skipped."""
        py_file = tmp_path / "example.py"
        py_file.write_text(
            "from __future__ import annotations\n"
            "from typing import TYPE_CHECKING\n"
            "import os\n"
            "\n"
            "if TYPE_CHECKING:\n"
            "    from src.infrastructure.adapters.persistence import Repo\n"
        )

        result = extract_imports(py_file)

        module_names = [name for name, _line in result]
        assert "os" in module_names
        assert "src.infrastructure.adapters.persistence" not in module_names

    def test_extract_imports_when_typing_type_checking_then_skips(
        self,
        tmp_path: Path,
    ) -> None:
        """Imports inside if typing.TYPE_CHECKING: blocks are skipped."""
        py_file = tmp_path / "example.py"
        py_file.write_text(
            "import typing\n"
            "\n"
            "if typing.TYPE_CHECKING:\n"
            "    from src.infrastructure.adapters.persistence import Repo\n"
        )

        result = extract_imports(py_file)

        module_names = [name for name, _line in result]
        assert "src.infrastructure.adapters.persistence" not in module_names

    def test_extract_imports_when_syntax_error_then_returns_empty(
        self,
        tmp_path: Path,
    ) -> None:
        """Files with syntax errors return an empty list."""
        py_file = tmp_path / "bad.py"
        py_file.write_text("def broken(\n")

        result = extract_imports(py_file)

        assert result == []

    def test_extract_imports_when_non_type_checking_if_block_then_includes(
        self,
        tmp_path: Path,
    ) -> None:
        """Imports inside non-TYPE_CHECKING if blocks are extracted."""
        py_file = tmp_path / "example.py"
        py_file.write_text(
            "import sys\n"
            "\n"
            "if sys.version_info >= (3, 11):\n"
            "    from src.domain.entities.project import Project\n"
        )

        result = extract_imports(py_file)

        module_names = [name for name, _line in result]
        assert "src.domain.entities.project" in module_names

    def test_extract_imports_when_import_star_then_includes_module(
        self,
        tmp_path: Path,
    ) -> None:
        """from X import * extracts the module name."""
        py_file = tmp_path / "example.py"
        py_file.write_text("from src.domain.events import *\n")

        result = extract_imports(py_file)

        module_names = [name for name, _line in result]
        assert "src.domain.events" in module_names

    def test_extract_imports_when_dynamic_import_then_includes(
        self,
        tmp_path: Path,
    ) -> None:
        """Dynamic __import__() calls are detected."""
        py_file = tmp_path / "example.py"
        py_file.write_text('mod = __import__("src.infrastructure.adapters.persistence")\n')

        result = extract_imports(py_file)

        module_names = [name for name, _line in result]
        assert "src.infrastructure.adapters.persistence" in module_names

    def test_extract_imports_when_importlib_import_module_then_includes(
        self,
        tmp_path: Path,
    ) -> None:
        """Dynamic importlib.import_module() calls are detected."""
        py_file = tmp_path / "example.py"
        py_file.write_text(
            'import importlib\nmod = importlib.import_module("src.interface.cli.main")\n'
        )

        result = extract_imports(py_file)

        module_names = [name for name, _line in result]
        assert "src.interface.cli.main" in module_names

    def test_extract_imports_when_dynamic_import_no_string_arg_then_skips(
        self,
        tmp_path: Path,
    ) -> None:
        """Dynamic imports with non-string args are skipped (no module name)."""
        py_file = tmp_path / "example.py"
        py_file.write_text("name = 'os'\nmod = __import__(name)\n")

        result = extract_imports(py_file)

        # Should only have static imports, not the dynamic one with variable
        module_names = [name for name, _line in result]
        # 'name' variable is not extractable, so no "os" from dynamic import
        assert "os" not in module_names

    def test_extract_imports_preserves_line_numbers(
        self,
        tmp_path: Path,
    ) -> None:
        """Line numbers are correctly reported for imports."""
        py_file = tmp_path / "example.py"
        py_file.write_text("import os\n\nfrom pathlib import Path\n")

        result = extract_imports(py_file)

        line_numbers = dict(result)
        assert line_numbers["os"] == 1
        assert line_numbers["pathlib"] == 3


# =============================================================================
# detect_layer tests
# =============================================================================


class TestDetectLayer:
    """Tests for the detect_layer function."""

    def test_detect_layer_when_flat_structure_then_returns_layer(
        self,
        tmp_path: Path,
    ) -> None:
        """Flat structure src/domain/X.py returns 'domain'."""
        src_root = tmp_path / "src"
        domain_dir = src_root / "domain" / "aggregates"
        domain_dir.mkdir(parents=True)
        file_path = domain_dir / "work_item.py"
        file_path.touch()

        result = detect_layer(file_path, src_root)

        assert result == "domain"

    def test_detect_layer_when_bounded_context_then_returns_inner_layer(
        self,
        tmp_path: Path,
    ) -> None:
        """Bounded context src/session_management/domain/X.py returns 'domain'."""
        src_root = tmp_path / "src"
        bc_dir = src_root / "session_management" / "domain" / "entities"
        bc_dir.mkdir(parents=True)
        file_path = bc_dir / "session.py"
        file_path.touch()

        result = detect_layer(file_path, src_root)

        assert result == "domain"

    def test_detect_layer_when_top_level_file_then_returns_none(
        self,
        tmp_path: Path,
    ) -> None:
        """Top-level src files (bootstrap.py) return None."""
        src_root = tmp_path / "src"
        src_root.mkdir(parents=True)
        file_path = src_root / "bootstrap.py"
        file_path.touch()

        result = detect_layer(file_path, src_root)

        assert result is None

    def test_detect_layer_when_application_layer_then_returns_application(
        self,
        tmp_path: Path,
    ) -> None:
        """Flat structure src/application/X.py returns 'application'."""
        src_root = tmp_path / "src"
        app_dir = src_root / "application" / "handlers"
        app_dir.mkdir(parents=True)
        file_path = app_dir / "handler.py"
        file_path.touch()

        result = detect_layer(file_path, src_root)

        assert result == "application"

    def test_detect_layer_when_shared_kernel_then_returns_shared_kernel(
        self,
        tmp_path: Path,
    ) -> None:
        """Flat structure src/shared_kernel/X.py returns 'shared_kernel'."""
        src_root = tmp_path / "src"
        sk_dir = src_root / "shared_kernel" / "identity"
        sk_dir.mkdir(parents=True)
        file_path = sk_dir / "vertex_id.py"
        file_path.touch()

        result = detect_layer(file_path, src_root)

        assert result == "shared_kernel"

    def test_detect_layer_when_unrecognized_dir_then_returns_none(
        self,
        tmp_path: Path,
    ) -> None:
        """Unrecognized directories return None."""
        src_root = tmp_path / "src"
        misc_dir = src_root / "utilities" / "helpers"
        misc_dir.mkdir(parents=True)
        file_path = misc_dir / "util.py"
        file_path.touch()

        result = detect_layer(file_path, src_root)

        assert result is None

    def test_detect_layer_when_file_outside_src_then_returns_none(
        self,
        tmp_path: Path,
    ) -> None:
        """Files outside src_root return None."""
        src_root = tmp_path / "src"
        src_root.mkdir(parents=True)
        file_path = tmp_path / "tests" / "test_something.py"
        file_path.parent.mkdir(parents=True)
        file_path.touch()

        result = detect_layer(file_path, src_root)

        assert result is None

    def test_detect_layer_when_bounded_context_file_in_root_then_returns_none(
        self,
        tmp_path: Path,
    ) -> None:
        """BC root file (e.g., src/session_management/__init__.py) returns None
        because it has < 3 parts (no layer subdir)."""
        src_root = tmp_path / "src"
        bc_dir = src_root / "session_management"
        bc_dir.mkdir(parents=True)
        file_path = bc_dir / "__init__.py"
        file_path.touch()

        result = detect_layer(file_path, src_root)

        assert result is None


# =============================================================================
# detect_target_layer tests
# =============================================================================


class TestDetectTargetLayer:
    """Tests for the detect_target_layer function."""

    def test_detect_target_layer_when_src_prefix_then_extracts_layer(self) -> None:
        """Flat import src.domain.X extracts 'domain'."""
        result = detect_target_layer("src.domain.aggregates.work_item")

        assert result == "domain"

    def test_detect_target_layer_when_bounded_context_import_then_extracts_layer(
        self,
    ) -> None:
        """BC import src.session_management.domain.X extracts 'domain'."""
        result = detect_target_layer("src.session_management.domain.entities.session")

        assert result == "domain"

    def test_detect_target_layer_when_stdlib_import_then_returns_none(self) -> None:
        """Standard library imports return None."""
        result = detect_target_layer("os.path")

        assert result is None

    def test_detect_target_layer_when_infrastructure_then_returns_infrastructure(
        self,
    ) -> None:
        """Flat import src.infrastructure.X returns 'infrastructure'."""
        result = detect_target_layer("src.infrastructure.adapters.persistence.repo")

        assert result == "infrastructure"

    def test_detect_target_layer_when_interface_then_returns_interface(self) -> None:
        """Flat import src.interface.X returns 'interface'."""
        result = detect_target_layer("src.interface.cli.main")

        assert result == "interface"

    def test_detect_target_layer_when_shared_kernel_then_returns_shared_kernel(
        self,
    ) -> None:
        """Flat import src.shared_kernel.X returns 'shared_kernel'."""
        result = detect_target_layer("src.shared_kernel.events.domain_event")

        assert result == "shared_kernel"

    def test_detect_target_layer_when_only_src_then_returns_none(self) -> None:
        """Bare 'src' import returns None."""
        result = detect_target_layer("src")

        assert result is None

    def test_detect_target_layer_when_bc_no_layer_then_returns_none(self) -> None:
        """BC import without layer part (e.g., src.work_tracking) returns None."""
        result = detect_target_layer("src.work_tracking")

        assert result is None

    def test_detect_target_layer_when_bc_unrecognized_layer_then_returns_none(
        self,
    ) -> None:
        """BC import with unrecognized layer returns None."""
        result = detect_target_layer("src.session_management.utils.helper")

        assert result is None

    def test_detect_target_layer_when_third_party_then_returns_none(self) -> None:
        """Third-party imports return None."""
        result = detect_target_layer("pytest.fixtures")

        assert result is None


# =============================================================================
# check_file tests
# =============================================================================


class TestCheckFile:
    """Tests for the check_file function."""

    def test_check_file_when_bootstrap_then_exempt(
        self,
        tmp_path: Path,
    ) -> None:
        """bootstrap.py is exempt from boundary checks."""
        src_root = tmp_path / "src"
        src_root.mkdir()
        bootstrap = src_root / "bootstrap.py"
        bootstrap.write_text(
            "from src.infrastructure.adapters.persistence import Repo\n"
            "from src.domain.aggregates.work_item import WorkItem\n"
        )

        result = check_file(bootstrap, src_root)

        assert result == []

    def test_check_file_when_domain_imports_infrastructure_then_violation(
        self,
        tmp_path: Path,
    ) -> None:
        """Domain importing infrastructure is a violation."""
        src_root = tmp_path / "src"
        domain_dir = src_root / "domain" / "aggregates"
        domain_dir.mkdir(parents=True)
        py_file = domain_dir / "work_item.py"
        py_file.write_text("from src.infrastructure.adapters.persistence import Repo\n")

        result = check_file(py_file, src_root)

        assert len(result) == 1
        assert result[0].source_layer == "domain"
        assert result[0].target_layer == "infrastructure"
        assert result[0].import_name == "src.infrastructure.adapters.persistence"

    def test_check_file_when_domain_imports_domain_then_no_violation(
        self,
        tmp_path: Path,
    ) -> None:
        """Domain importing domain is allowed (no violation)."""
        src_root = tmp_path / "src"
        domain_dir = src_root / "domain" / "aggregates"
        domain_dir.mkdir(parents=True)
        py_file = domain_dir / "work_item.py"
        py_file.write_text("from src.domain.value_objects.priority import Priority\n")

        result = check_file(py_file, src_root)

        assert result == []

    def test_check_file_when_domain_imports_application_then_violation(
        self,
        tmp_path: Path,
    ) -> None:
        """Domain importing application is a violation."""
        src_root = tmp_path / "src"
        domain_dir = src_root / "domain" / "services"
        domain_dir.mkdir(parents=True)
        py_file = domain_dir / "service.py"
        py_file.write_text("from src.application.handlers.commands import handler\n")

        result = check_file(py_file, src_root)

        assert len(result) == 1
        assert result[0].source_layer == "domain"
        assert result[0].target_layer == "application"

    def test_check_file_when_application_imports_infrastructure_then_violation(
        self,
        tmp_path: Path,
    ) -> None:
        """Application importing infrastructure is a violation."""
        src_root = tmp_path / "src"
        app_dir = src_root / "application" / "handlers"
        app_dir.mkdir(parents=True)
        py_file = app_dir / "handler.py"
        py_file.write_text("from src.infrastructure.adapters.persistence import Repo\n")

        result = check_file(py_file, src_root)

        assert len(result) == 1
        assert result[0].source_layer == "application"
        assert result[0].target_layer == "infrastructure"

    def test_check_file_when_infrastructure_imports_domain_then_no_violation(
        self,
        tmp_path: Path,
    ) -> None:
        """Infrastructure importing domain is allowed."""
        src_root = tmp_path / "src"
        infra_dir = src_root / "infrastructure" / "adapters"
        infra_dir.mkdir(parents=True)
        py_file = infra_dir / "adapter.py"
        py_file.write_text("from src.domain.aggregates.work_item import WorkItem\n")

        result = check_file(py_file, src_root)

        assert result == []

    def test_check_file_when_interface_layer_then_no_rules(
        self,
        tmp_path: Path,
    ) -> None:
        """Interface layer has no forbidden imports."""
        src_root = tmp_path / "src"
        iface_dir = src_root / "interface" / "cli"
        iface_dir.mkdir(parents=True)
        py_file = iface_dir / "main.py"
        py_file.write_text(
            "from src.infrastructure.adapters.persistence import Repo\n"
            "from src.domain.aggregates.work_item import WorkItem\n"
            "from src.application.handlers.commands import handler\n"
        )

        result = check_file(py_file, src_root)

        assert result == []

    def test_check_file_when_type_checking_import_then_exempt(
        self,
        tmp_path: Path,
    ) -> None:
        """Imports inside TYPE_CHECKING blocks are exempt."""
        src_root = tmp_path / "src"
        domain_dir = src_root / "domain" / "aggregates"
        domain_dir.mkdir(parents=True)
        py_file = domain_dir / "work_item.py"
        py_file.write_text(
            "from __future__ import annotations\n"
            "from typing import TYPE_CHECKING\n"
            "\n"
            "if TYPE_CHECKING:\n"
            "    from src.infrastructure.adapters.persistence import Repo\n"
        )

        result = check_file(py_file, src_root)

        assert result == []

    def test_check_file_when_bc_domain_imports_infrastructure_then_violation(
        self,
        tmp_path: Path,
    ) -> None:
        """Bounded context domain importing infrastructure is a violation."""
        src_root = tmp_path / "src"
        bc_domain_dir = src_root / "session_management" / "domain" / "entities"
        bc_domain_dir.mkdir(parents=True)
        py_file = bc_domain_dir / "session.py"
        py_file.write_text("from src.infrastructure.adapters.persistence import Repo\n")

        result = check_file(py_file, src_root)

        assert len(result) == 1
        assert result[0].source_layer == "domain"
        assert result[0].target_layer == "infrastructure"

    def test_check_file_when_dynamic_import_violation_then_detected(
        self,
        tmp_path: Path,
    ) -> None:
        """Dynamic __import__() calls that violate boundaries are detected."""
        src_root = tmp_path / "src"
        domain_dir = src_root / "domain" / "services"
        domain_dir.mkdir(parents=True)
        py_file = domain_dir / "service.py"
        py_file.write_text('mod = __import__("src.infrastructure.adapters.persistence")\n')

        result = check_file(py_file, src_root)

        assert len(result) >= 1
        infra_violations = [v for v in result if v.target_layer == "infrastructure"]
        assert len(infra_violations) >= 1

    def test_check_file_when_shared_kernel_imports_infrastructure_then_violation(
        self,
        tmp_path: Path,
    ) -> None:
        """Shared kernel importing infrastructure is a violation."""
        src_root = tmp_path / "src"
        sk_dir = src_root / "shared_kernel" / "events"
        sk_dir.mkdir(parents=True)
        py_file = sk_dir / "event.py"
        py_file.write_text("from src.infrastructure.adapters.persistence import Repo\n")

        result = check_file(py_file, src_root)

        assert len(result) == 1
        assert result[0].source_layer == "shared_kernel"
        assert result[0].target_layer == "infrastructure"


# =============================================================================
# check_all_files tests
# =============================================================================


class TestCheckAllFiles:
    """Tests for the check_all_files function."""

    def test_check_all_files_when_no_violations_then_empty_list(
        self,
        tmp_path: Path,
    ) -> None:
        """Clean codebase returns empty violations list."""
        src_root = tmp_path / "src"
        domain_dir = src_root / "domain" / "aggregates"
        domain_dir.mkdir(parents=True)

        # Domain file with valid imports only
        py_file = domain_dir / "work_item.py"
        py_file.write_text("import os\nfrom src.domain.value_objects.priority import Priority\n")

        result = check_all_files(src_root)

        assert result == []

    def test_check_all_files_when_violations_then_returns_all(
        self,
        tmp_path: Path,
    ) -> None:
        """Multiple violations across files are all returned."""
        src_root = tmp_path / "src"

        # Domain file with violation
        domain_dir = src_root / "domain" / "aggregates"
        domain_dir.mkdir(parents=True)
        domain_file = domain_dir / "work_item.py"
        domain_file.write_text("from src.infrastructure.adapters.persistence import Repo\n")

        # Application file with violation
        app_dir = src_root / "application" / "handlers"
        app_dir.mkdir(parents=True)
        app_file = app_dir / "handler.py"
        app_file.write_text("from src.interface.cli.main import run\n")

        result = check_all_files(src_root)

        assert len(result) == 2

    def test_check_all_files_when_pycache_then_skips(
        self,
        tmp_path: Path,
    ) -> None:
        """__pycache__ directories are skipped."""
        src_root = tmp_path / "src"
        pycache_dir = src_root / "domain" / "__pycache__"
        pycache_dir.mkdir(parents=True)
        cached_file = pycache_dir / "work_item.cpython-311.py"
        cached_file.write_text("from src.infrastructure.adapters.persistence import Repo\n")

        result = check_all_files(src_root)

        assert result == []


# =============================================================================
# _is_type_checking_block tests
# =============================================================================


class TestIsTypeCheckingBlock:
    """Tests for the _is_type_checking_block helper."""

    def test_is_type_checking_block_when_name_then_true(self) -> None:
        """if TYPE_CHECKING: is detected."""
        import ast as _ast

        source = "if TYPE_CHECKING:\n    pass\n"
        tree = _ast.parse(source)
        if_node = tree.body[0]
        assert isinstance(if_node, _ast.If)

        result = _is_type_checking_block(if_node)

        assert result is True

    def test_is_type_checking_block_when_attribute_then_true(self) -> None:
        """if typing.TYPE_CHECKING: is detected."""
        import ast as _ast

        source = "if typing.TYPE_CHECKING:\n    pass\n"
        tree = _ast.parse(source)
        if_node = tree.body[0]
        assert isinstance(if_node, _ast.If)

        result = _is_type_checking_block(if_node)

        assert result is True

    def test_is_type_checking_block_when_other_condition_then_false(self) -> None:
        """Non-TYPE_CHECKING if blocks return False."""
        import ast as _ast

        source = "if sys.version_info >= (3, 11):\n    pass\n"
        tree = _ast.parse(source)
        if_node = tree.body[0]
        assert isinstance(if_node, _ast.If)

        result = _is_type_checking_block(if_node)

        assert result is False


# =============================================================================
# _is_dynamic_import tests
# =============================================================================


class TestIsDynamicImport:
    """Tests for the _is_dynamic_import helper."""

    def test_is_dynamic_import_when_dunder_import_then_true(self) -> None:
        """__import__("module") is detected as dynamic import."""
        import ast as _ast

        source = '__import__("os")\n'
        tree = _ast.parse(source)
        expr = tree.body[0]
        assert isinstance(expr, _ast.Expr)
        assert isinstance(expr.value, _ast.Call)

        result = _is_dynamic_import(expr.value)

        assert result is True

    def test_is_dynamic_import_when_importlib_then_true(self) -> None:
        """importlib.import_module("module") is detected."""
        import ast as _ast

        source = 'importlib.import_module("os")\n'
        tree = _ast.parse(source)
        expr = tree.body[0]
        assert isinstance(expr, _ast.Expr)
        assert isinstance(expr.value, _ast.Call)

        result = _is_dynamic_import(expr.value)

        assert result is True

    def test_is_dynamic_import_when_regular_call_then_false(self) -> None:
        """Regular function calls are not dynamic imports."""
        import ast as _ast

        source = 'print("hello")\n'
        tree = _ast.parse(source)
        expr = tree.body[0]
        assert isinstance(expr, _ast.Expr)
        assert isinstance(expr.value, _ast.Call)

        result = _is_dynamic_import(expr.value)

        assert result is False


# =============================================================================
# _extract_dynamic_imports_from_body tests
# =============================================================================


class TestExtractDynamicImportsFromBody:
    """Tests for the _extract_dynamic_imports_from_body helper."""

    def test_extract_dynamic_imports_when_in_function_then_found(self) -> None:
        """Dynamic imports inside functions are extracted."""
        import ast as _ast

        source = 'def load():\n    mod = __import__("src.infrastructure.adapters.persistence")\n'
        tree = _ast.parse(source)

        result = _extract_dynamic_imports_from_body(tree.body)

        module_names = [name for name, _line in result]
        assert "src.infrastructure.adapters.persistence" in module_names

    def test_extract_dynamic_imports_when_none_then_empty(self) -> None:
        """Files without dynamic imports return empty list."""
        import ast as _ast

        source = "import os\nx = 42\n"
        tree = _ast.parse(source)

        result = _extract_dynamic_imports_from_body(tree.body)

        assert result == []


# =============================================================================
# Violation __str__ test
# =============================================================================


class TestViolation:
    """Tests for the Violation data structure."""

    def test_violation_str_format(self, tmp_path: Path) -> None:
        """Violation string representation includes all relevant info."""
        v = Violation(
            file_path=tmp_path / "src" / "domain" / "work_item.py",
            line_number=5,
            source_layer="domain",
            target_layer="infrastructure",
            import_name="src.infrastructure.adapters.persistence",
        )

        result = str(v)

        assert "domain" in result
        assert "infrastructure" in result
        assert "src.infrastructure.adapters.persistence" in result
        assert ":5:" in result
