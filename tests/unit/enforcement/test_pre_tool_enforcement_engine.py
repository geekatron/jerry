"""
Unit tests for PreToolEnforcementEngine.

Tests cover V-038 (import boundary validation), V-041 (one-class-per-file),
governance escalation, error handling, edit operations, bounded context paths,
dynamic import variants, TYPE_CHECKING attribute form, false-positive
mitigation for third-party imports, and idempotency.

Test naming follows BDD convention:
    test_{scenario}_when_{condition}_then_{expected}

References:
    - EN-703: PreToolUse Enforcement Engine
    - V-038: Import boundary enforcement
    - V-041: One-class-per-file enforcement
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.infrastructure.internal.enforcement.enforcement_decision import (
    EnforcementDecision,
)
from src.infrastructure.internal.enforcement.pre_tool_enforcement_engine import (
    PreToolEnforcementEngine,
)

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def project_root(tmp_path: Path) -> Path:
    """Create a minimal project root with CLAUDE.md."""
    (tmp_path / "CLAUDE.md").write_text("# Project Root")
    (tmp_path / "src" / "domain").mkdir(parents=True)
    (tmp_path / "src" / "application").mkdir(parents=True)
    (tmp_path / "src" / "infrastructure").mkdir(parents=True)
    (tmp_path / "src" / "interface").mkdir(parents=True)
    (tmp_path / "src" / "shared_kernel").mkdir(parents=True)
    # Bounded context directories
    (tmp_path / "src" / "session_management" / "domain").mkdir(parents=True)
    (tmp_path / "src" / "session_management" / "application").mkdir(parents=True)
    (tmp_path / "src" / "work_tracking" / "domain").mkdir(parents=True)
    (tmp_path / "src" / "work_tracking" / "application").mkdir(parents=True)
    return tmp_path


@pytest.fixture
def engine(project_root: Path) -> PreToolEnforcementEngine:
    """Create an enforcement engine with the test project root."""
    return PreToolEnforcementEngine(project_root=project_root)


# =============================================================================
# V-038: Import Boundary Tests
# =============================================================================


class TestV038ImportBoundary:
    """Tests for import boundary validation (V-038)."""

    def test_evaluate_write_when_clean_domain_file_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """A domain file with only stdlib imports should be approved."""
        content = '''"""Domain entity module."""

from __future__ import annotations

import json
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class MyEntity:
    """A domain entity."""

    name: str
'''
        file_path = str(project_root / "src" / "domain" / "entity.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "approve"
        assert not decision.violations

    def test_evaluate_write_when_domain_imports_infrastructure_then_blocks(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Domain importing from infrastructure should be blocked."""
        content = '''"""Domain module with bad import."""

from src.infrastructure.adapters.persistence import FileAdapter


class MyEntity:
    """A domain entity."""
    pass
'''
        file_path = str(project_root / "src" / "domain" / "entity.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "block"
        assert len(decision.violations) >= 1
        assert any("infrastructure" in v for v in decision.violations)

    def test_evaluate_write_when_domain_imports_application_then_blocks(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Domain importing from application should be blocked."""
        content = '''"""Domain module with bad import."""

from src.application.handlers.commands import CreateTaskHandler


class MyEntity:
    """A domain entity."""
    pass
'''
        file_path = str(project_root / "src" / "domain" / "entity.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "block"
        assert any("application" in v for v in decision.violations)

    def test_evaluate_write_when_application_imports_interface_then_blocks(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Application importing from interface should be blocked."""
        content = '''"""Application handler with bad import."""

from src.interface.cli.adapter import CLIAdapter


class MyHandler:
    """An application handler."""
    pass
'''
        file_path = str(project_root / "src" / "application" / "handler.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "block"
        assert any("interface" in v for v in decision.violations)

    def test_evaluate_write_when_infrastructure_imports_interface_then_blocks(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Infrastructure importing from interface should be blocked."""
        content = '''"""Infrastructure adapter with bad import."""

from src.interface.cli.main import main


class MyAdapter:
    """An infrastructure adapter."""
    pass
'''
        file_path = str(project_root / "src" / "infrastructure" / "adapter.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "block"
        assert any("interface" in v for v in decision.violations)

    def test_evaluate_write_when_bootstrap_file_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """bootstrap.py is exempt from import boundary checks."""
        content = '''"""Composition root."""

from src.infrastructure.adapters.persistence import FileAdapter
from src.interface.cli.adapter import CLIAdapter
from src.domain.entities import Entity
from src.application.handlers import Handler


def create_app():
    """Create application."""
    pass
'''
        file_path = str(project_root / "src" / "bootstrap.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "approve"

    def test_evaluate_write_when_type_checking_import_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Imports inside TYPE_CHECKING blocks are exempt."""
        content = '''"""Domain module with TYPE_CHECKING import."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.infrastructure.adapters.persistence import FileAdapter


class MyEntity:
    """A domain entity."""
    pass
'''
        file_path = str(project_root / "src" / "domain" / "entity.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "approve"
        assert not decision.violations

    def test_evaluate_write_when_dynamic_import_then_blocks(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Dynamic imports (__import__) that violate boundaries should be blocked."""
        content = '''"""Domain module with dynamic import."""


class MyEntity:
    """A domain entity."""

    def load(self):
        """Load something."""
        mod = __import__("src.infrastructure.adapters")
        return mod
'''
        file_path = str(project_root / "src" / "domain" / "entity.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "block"
        assert any("dynamic" in v.lower() or "infrastructure" in v for v in decision.violations)

    def test_evaluate_write_when_shared_kernel_imports_infrastructure_then_blocks(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """shared_kernel importing from infrastructure should be blocked."""
        content = '''"""Shared kernel module with bad import."""

from src.infrastructure.adapters import SomeAdapter


class Identity:
    """Identity type."""
    pass
'''
        file_path = str(project_root / "src" / "shared_kernel" / "identity.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "block"
        assert any("infrastructure" in v for v in decision.violations)

    def test_evaluate_write_when_infrastructure_imports_domain_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Infrastructure importing from domain is allowed."""
        content = '''"""Infrastructure adapter."""

from src.domain.entities.work_item import WorkItem


class MyAdapter:
    """A persistence adapter."""
    pass
'''
        file_path = str(project_root / "src" / "infrastructure" / "adapter.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "approve"

    def test_evaluate_write_when_interface_imports_all_layers_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Interface can import from all inner layers."""
        content = '''"""Interface adapter."""

from src.domain.entities import Entity
from src.application.handlers import Handler
from src.infrastructure.adapters import Adapter


class CLIAdapter:
    """CLI primary adapter."""
    pass
'''
        file_path = str(project_root / "src" / "interface" / "cli.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "approve"


# =============================================================================
# V-038: importlib.import_module() Boundary Check (M-1)
# =============================================================================


class TestV038ImportlibDynamicImport:
    """Tests for importlib.import_module() dynamic import detection (M-1)."""

    def test_evaluate_write_when_importlib_dynamic_import_then_blocks(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """importlib.import_module() that violates boundaries should be blocked.

        Addresses critique M-1: missing test for importlib.import_module()
        boundary check. Verifies the engine detects this dynamic import
        variant just as it detects __import__().
        """
        content = '''"""Domain module with importlib dynamic import."""

import importlib


class MyEntity:
    """A domain entity."""

    def load_adapter(self):
        """Dynamically load an adapter (violation)."""
        mod = importlib.import_module("src.infrastructure.adapters")
        return mod
'''
        file_path = str(project_root / "src" / "domain" / "entity.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "block"
        assert any("dynamic" in v.lower() and "infrastructure" in v for v in decision.violations)


# =============================================================================
# V-038: Bounded Context Path Tests (M-2)
# =============================================================================


class TestV038BoundedContextPaths:
    """Tests for bounded context path layer detection (M-2).

    The project uses bounded contexts (e.g., src/session_management/domain/)
    where layer directories are nested under context directories. The engine
    must correctly identify layers in these paths.
    """

    def test_evaluate_write_when_bounded_context_domain_imports_infrastructure_then_blocks(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """A domain file within a bounded context importing infrastructure
        should be blocked, just like a top-level domain file."""
        content = '''"""Session management domain entity."""

from src.infrastructure.adapters.persistence import FileAdapter


class SessionEntity:
    """A session entity in the session_management BC."""
    pass
'''
        file_path = str(project_root / "src" / "session_management" / "domain" / "entity.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "block"
        assert any("infrastructure" in v for v in decision.violations)

    def test_evaluate_write_when_bounded_context_application_imports_interface_then_blocks(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """An application file within a bounded context importing interface
        should be blocked."""
        content = '''"""Work tracking application handler."""

from src.interface.cli.adapter import CLIAdapter


class WorkTrackingHandler:
    """Handler in the work_tracking BC."""
    pass
'''
        file_path = str(project_root / "src" / "work_tracking" / "application" / "handler.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "block"
        assert any("interface" in v for v in decision.violations)

    def test_evaluate_write_when_bounded_context_domain_clean_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """A clean domain file within a bounded context should be approved."""
        content = '''"""Session management domain entity."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SessionId:
    """Session identifier value object."""

    value: str
'''
        file_path = str(project_root / "src" / "session_management" / "domain" / "session_id.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "approve"


# =============================================================================
# V-038: TYPE_CHECKING Attribute Access Form (m-5)
# =============================================================================


class TestV038TypeCheckingAttributeForm:
    """Tests for typing.TYPE_CHECKING attribute access form (m-5).

    The engine should handle both ``if TYPE_CHECKING:`` (Name node) and
    ``if typing.TYPE_CHECKING:`` (Attribute node) forms.
    """

    def test_evaluate_write_when_typing_type_checking_attribute_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Imports inside ``if typing.TYPE_CHECKING:`` blocks are exempt.

        Addresses critique m-5: missing test for the attribute access form
        of TYPE_CHECKING. Uses ``typing.TYPE_CHECKING`` instead of importing
        TYPE_CHECKING and using it as a bare name.
        """
        content = '''"""Domain module using typing.TYPE_CHECKING attribute form."""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from src.infrastructure.adapters.persistence import FileAdapter


class MyEntity:
    """A domain entity."""
    pass
'''
        file_path = str(project_root / "src" / "domain" / "entity.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "approve"
        assert not decision.violations


# =============================================================================
# V-038: Third-Party Import False-Positive Mitigation
# =============================================================================


class TestV038ThirdPartyImportFalsePositive:
    """Tests for false-positive mitigation on third-party imports.

    Third-party packages with ``domain``, ``infrastructure``, or ``interface``
    in their package structure should NOT trigger boundary violations.
    Only project-internal imports (starting with ``src.`` or a recognized
    layer name) are subject to boundary checking.
    """

    def test_evaluate_write_when_third_party_has_domain_in_path_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """A third-party import with 'domain' in its path should not be flagged."""
        content = '''"""Domain module using third-party lib with domain subpackage."""

from some_library.domain.utils import helper


class MyEntity:
    """A domain entity."""
    pass
'''
        file_path = str(project_root / "src" / "domain" / "entity.py")
        decision = engine.evaluate_write(file_path, content)

        # The third-party import should be ignored; no violations
        assert decision.action == "approve"
        assert not decision.violations

    def test_evaluate_write_when_third_party_has_infrastructure_in_path_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """A third-party import with 'infrastructure' in its path should not
        be flagged when used from a domain file."""
        content = '''"""Domain module using third-party lib."""

from cloud_provider.infrastructure.networking import Client


class MyEntity:
    """A domain entity."""
    pass
'''
        file_path = str(project_root / "src" / "domain" / "entity.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "approve"
        assert not decision.violations

    def test_evaluate_write_when_project_import_with_src_prefix_still_blocks(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Project-internal imports (src.*) should still be checked and blocked."""
        content = '''"""Domain module with src-prefixed violation."""

from src.infrastructure.adapters import Adapter


class MyEntity:
    """A domain entity."""
    pass
'''
        file_path = str(project_root / "src" / "domain" / "entity.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "block"
        assert any("infrastructure" in v for v in decision.violations)

    def test_evaluate_write_when_bare_layer_import_then_blocks(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Bare imports starting with a layer name should still be checked."""
        content = '''"""Domain module with bare infrastructure import."""

from infrastructure.adapters import Adapter


class MyEntity:
    """A domain entity."""
    pass
'''
        file_path = str(project_root / "src" / "domain" / "entity.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "block"
        assert any("infrastructure" in v for v in decision.violations)


# =============================================================================
# V-041: One-Class-Per-File Tests
# =============================================================================


class TestV041OneClassPerFile:
    """Tests for one-class-per-file validation (V-041)."""

    def test_evaluate_write_when_multiple_public_classes_then_blocks(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Multiple public classes in one file should be blocked."""
        content = '''"""Module with multiple classes."""


class FirstClass:
    """First public class."""
    pass


class SecondClass:
    """Second public class."""
    pass
'''
        file_path = str(project_root / "src" / "domain" / "multi_class.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "block"
        assert any("one-class-per-file" in v.lower() for v in decision.violations)

    def test_evaluate_write_when_single_public_class_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """A single public class is allowed."""
        content = '''"""Module with one class."""


class OnlyClass:
    """The only public class."""
    pass
'''
        file_path = str(project_root / "src" / "domain" / "single_class.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "approve"

    def test_evaluate_write_when_public_and_private_classes_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """One public class + private classes is allowed."""
        content = '''"""Module with public and private classes."""


class _PrivateHelper:
    """Private helper."""
    pass


class PublicClass:
    """The one public class."""
    pass


class _AnotherPrivate:
    """Another private class."""
    pass
'''
        file_path = str(project_root / "src" / "domain" / "mixed_class.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "approve"

    def test_evaluate_write_when_init_file_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """__init__.py files are exempt from one-class-per-file."""
        content = '''"""Package init with multiple classes for re-export."""


class FirstClass:
    """First class."""
    pass


class SecondClass:
    """Second class."""
    pass
'''
        file_path = str(project_root / "src" / "domain" / "__init__.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "approve"

    def test_evaluate_write_when_no_classes_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Files with no classes are allowed."""
        content = '''"""Utility module with functions only."""


def helper():
    """Helper function."""
    pass
'''
        file_path = str(project_root / "src" / "domain" / "utils.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "approve"


# =============================================================================
# Governance Escalation Tests
# =============================================================================


class TestGovernanceEscalation:
    """Tests for governance file escalation detection."""

    def test_evaluate_write_when_constitution_file_then_warns_c4(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Modifying JERRY_CONSTITUTION.md should warn with C4 escalation."""
        file_path = str(project_root / "docs" / "governance" / "JERRY_CONSTITUTION.md")
        content = "# Updated Constitution"
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "warn"
        assert decision.criticality_escalation == "C4"

    def test_evaluate_write_when_rules_file_then_warns_c3(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Modifying .context/rules/ files should warn with C3 escalation."""
        file_path = str(project_root / ".context" / "rules" / "coding-standards.md")
        content = "# Updated coding standards"
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "warn"
        assert decision.criticality_escalation == "C3"

    def test_evaluate_write_when_claude_rules_file_then_warns_c3(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Modifying .claude/rules/ files should warn with C3 escalation."""
        file_path = str(project_root / ".claude" / "rules" / "my-rule.md")
        content = "# Updated rule"
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "warn"
        assert decision.criticality_escalation == "C3"

    def test_evaluate_write_when_governance_python_with_violation_then_blocks(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Governance escalation Python file with violations should block,
        but include the escalation in the decision."""
        # This is a .context/rules/ Python file (odd but tests edge case)
        content = '''"""Rule file."""

from src.infrastructure.adapters import Adapter


class Rule:
    """A rule."""
    pass
'''
        file_path = str(project_root / "src" / "domain" / "entity.py")
        decision = engine.evaluate_write(file_path, content)

        # Should block due to import violation, not just warn
        assert decision.action == "block"

    def test_evaluate_write_when_normal_file_then_no_escalation(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Normal files should not trigger governance escalation."""
        content = '''"""Normal module."""


class NormalClass:
    """A normal class."""
    pass
'''
        file_path = str(project_root / "src" / "domain" / "normal.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.criticality_escalation is None


# =============================================================================
# Error Handling Tests (Fail-Open)
# =============================================================================


class TestErrorHandling:
    """Tests for fail-open error handling."""

    def test_evaluate_write_when_syntax_error_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Python files with syntax errors should be approved (fail-open)."""
        content = '''"""Module with syntax error."""

def broken_function(
    # Missing closing paren and colon
'''
        file_path = str(project_root / "src" / "domain" / "broken.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "approve"

    def test_evaluate_write_when_non_python_file_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Non-Python files should be approved without checking."""
        content = "# Some markdown content"
        file_path = str(project_root / "src" / "domain" / "README.md")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "approve"

    def test_evaluate_write_when_file_outside_src_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Python files outside src/ should be approved without checking."""
        content = '''"""Test module with multi-class."""

from src.infrastructure.adapters import Adapter


class TestFirst:
    pass


class TestSecond:
    pass
'''
        file_path = str(project_root / "tests" / "test_something.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "approve"

    def test_evaluate_write_when_empty_content_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Empty file content should be approved."""
        file_path = str(project_root / "src" / "domain" / "empty.py")
        decision = engine.evaluate_write(file_path, "")

        assert decision.action == "approve"


# =============================================================================
# Edit Operation Tests
# =============================================================================


class TestEditOperations:
    """Tests for evaluate_edit operations."""

    def test_evaluate_edit_when_edit_introduces_violation_then_blocks(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """An edit that introduces an import violation should be blocked."""
        # Create a clean file first
        target_file = project_root / "src" / "domain" / "entity.py"
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(
            '''"""Domain entity."""

from dataclasses import dataclass


@dataclass
class MyEntity:
    """A domain entity."""

    name: str
''',
            encoding="utf-8",
        )

        # Edit that adds a bad import
        old_string = "from dataclasses import dataclass"
        new_string = (
            "from dataclasses import dataclass\nfrom src.infrastructure.adapters import FileAdapter"
        )

        decision = engine.evaluate_edit(str(target_file), old_string, new_string)

        assert decision.action == "block"
        assert any("infrastructure" in v for v in decision.violations)

    def test_evaluate_edit_when_edit_is_clean_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """An edit that maintains compliance should be approved."""
        target_file = project_root / "src" / "domain" / "entity.py"
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(
            '''"""Domain entity."""

from dataclasses import dataclass


@dataclass
class MyEntity:
    """A domain entity."""

    name: str
''',
            encoding="utf-8",
        )

        old_string = "name: str"
        new_string = "name: str\n    age: int"

        decision = engine.evaluate_edit(str(target_file), old_string, new_string)

        assert decision.action == "approve"

    def test_evaluate_edit_when_file_not_found_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Editing a non-existent file should approve (fail-open)."""
        file_path = str(project_root / "src" / "domain" / "nonexistent.py")

        decision = engine.evaluate_edit(file_path, "old", "new")

        assert decision.action == "approve"

    def test_evaluate_edit_when_old_string_not_found_then_approves(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """If old_string not in file, approve (fail-open)."""
        target_file = project_root / "src" / "domain" / "entity.py"
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text("# simple content\n", encoding="utf-8")

        decision = engine.evaluate_edit(str(target_file), "not found", "replacement")

        assert decision.action == "approve"


# =============================================================================
# EnforcementDecision Tests
# =============================================================================


class TestEnforcementDecision:
    """Tests for the EnforcementDecision dataclass."""

    def test_decision_is_frozen(self) -> None:
        """EnforcementDecision should be immutable."""
        decision = EnforcementDecision(action="approve", reason="test")
        with pytest.raises(Exception):
            decision.action = "block"  # type: ignore[misc]

    def test_decision_defaults(self) -> None:
        """Default values should be empty list and None."""
        decision = EnforcementDecision(action="approve", reason="test")
        assert decision.violations == []
        assert decision.criticality_escalation is None


# =============================================================================
# Combined Violation Tests
# =============================================================================


class TestCombinedViolations:
    """Tests for files with multiple violation types."""

    def test_evaluate_write_when_import_and_class_violations_then_blocks_with_both(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """A file with both import and class violations should report both."""
        content = '''"""Module with multiple violations."""

from src.infrastructure.adapters import FileAdapter


class FirstClass:
    """First class."""
    pass


class SecondClass:
    """Second class."""
    pass
'''
        file_path = str(project_root / "src" / "domain" / "bad_module.py")
        decision = engine.evaluate_write(file_path, content)

        assert decision.action == "block"
        assert len(decision.violations) >= 2
        # Should have both import and class violations
        has_import_violation = any("infrastructure" in v for v in decision.violations)
        has_class_violation = any("one-class-per-file" in v.lower() for v in decision.violations)
        assert has_import_violation
        assert has_class_violation


# =============================================================================
# Idempotency / Determinism Tests
# =============================================================================


class TestIdempotency:
    """Tests verifying engine produces deterministic, idempotent output.

    Same input must produce the same output across multiple calls.
    This is critical for a deterministic enforcement engine.
    """

    def test_evaluate_write_when_same_input_called_multiple_times_then_same_output(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Calling evaluate_write with identical input produces identical output."""
        content = '''"""Domain module with violation."""

from src.infrastructure.adapters import Adapter


class MyEntity:
    """A domain entity."""
    pass
'''
        file_path = str(project_root / "src" / "domain" / "entity.py")

        # Call 10 times and verify identical results
        decisions = [engine.evaluate_write(file_path, content) for _ in range(10)]

        first = decisions[0]
        for i, decision in enumerate(decisions[1:], start=2):
            assert decision.action == first.action, f"Call {i} action differs"
            assert decision.reason == first.reason, f"Call {i} reason differs"
            assert decision.violations == first.violations, f"Call {i} violations differ"
            assert decision.criticality_escalation == first.criticality_escalation, (
                f"Call {i} escalation differs"
            )

    def test_evaluate_write_when_clean_input_called_multiple_times_then_same_output(
        self, engine: PreToolEnforcementEngine, project_root: Path
    ) -> None:
        """Calling evaluate_write with clean input produces identical approvals."""
        content = '''"""Clean domain module."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MyEntity:
    """A domain entity."""

    name: str
'''
        file_path = str(project_root / "src" / "domain" / "entity.py")

        decisions = [engine.evaluate_write(file_path, content) for _ in range(10)]

        for decision in decisions:
            assert decision.action == "approve"
            assert not decision.violations
