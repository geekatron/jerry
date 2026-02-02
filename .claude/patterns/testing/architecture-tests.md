# PAT-TEST-003: Architecture Tests Pattern

> **Status**: MANDATORY
> **Category**: Testing Pattern
> **Location**: `tests/architecture/`

---

## Overview

Architecture Tests automatically enforce architectural constraints such as layer dependencies, naming conventions, and module boundaries. They catch violations at test time rather than code review.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **ArchUnit (Java)** | "Unit tests for your architecture" |
| **pytest-archon** | "Python architecture testing" |
| **Simon Brown** | "Architecture as code using fitness functions" |

---

## Jerry Architecture Tests

### Layer Dependency Tests

```python
# tests/architecture/test_layer_boundaries.py
"""Tests that enforce hexagonal architecture layer boundaries."""

import ast
from pathlib import Path

import pytest


def extract_imports(file_path: Path) -> list[str]:
    """Extract all import statements from a Python file."""
    tree = ast.parse(file_path.read_text())
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return imports


class TestDomainLayerBoundaries:
    """Domain layer must have no external dependencies."""

    @pytest.fixture
    def domain_files(self) -> list[Path]:
        """Get all Python files in domain layers."""
        patterns = [
            "src/work_tracking/domain/**/*.py",
            "src/session_management/domain/**/*.py",
        ]
        files = []
        for pattern in patterns:
            files.extend(Path(".").glob(pattern))
        return [f for f in files if f.name != "__init__.py"]

    def test_domain_has_no_infrastructure_imports(self, domain_files):
        """Domain layer must not import from infrastructure."""
        for file_path in domain_files:
            imports = extract_imports(file_path)

            for imp in imports:
                assert "infrastructure" not in imp, (
                    f"{file_path} imports infrastructure: {imp}"
                )

    def test_domain_has_no_application_imports(self, domain_files):
        """Domain layer must not import from application layer."""
        for file_path in domain_files:
            imports = extract_imports(file_path)

            for imp in imports:
                # Allow shared_kernel imports
                if "shared_kernel" in imp:
                    continue
                assert "application" not in imp, (
                    f"{file_path} imports application: {imp}"
                )

    def test_domain_has_no_interface_imports(self, domain_files):
        """Domain layer must not import from interface layer."""
        for file_path in domain_files:
            imports = extract_imports(file_path)

            for imp in imports:
                assert "interface" not in imp, (
                    f"{file_path} imports interface: {imp}"
                )

    def test_domain_has_no_external_dependencies(self, domain_files):
        """Domain layer must only use stdlib and shared_kernel."""
        allowed_prefixes = {
            "src.shared_kernel",
            "src.work_tracking.domain",
            "src.session_management.domain",
            # Python stdlib
            "dataclasses",
            "datetime",
            "enum",
            "typing",
            "abc",
            "uuid",
            "collections",
            "pathlib",
            "__future__",
        }

        for file_path in domain_files:
            imports = extract_imports(file_path)

            for imp in imports:
                is_allowed = any(
                    imp.startswith(prefix) or imp == prefix
                    for prefix in allowed_prefixes
                )
                assert is_allowed, (
                    f"{file_path} imports disallowed module: {imp}"
                )


class TestApplicationLayerBoundaries:
    """Application layer can import domain but not interface/infrastructure."""

    @pytest.fixture
    def application_files(self) -> list[Path]:
        """Get all Python files in application layer."""
        files = list(Path("src/application").glob("**/*.py"))
        return [f for f in files if f.name != "__init__.py"]

    def test_application_has_no_interface_imports(self, application_files):
        """Application layer must not import from interface."""
        for file_path in application_files:
            imports = extract_imports(file_path)

            for imp in imports:
                assert "interface" not in imp, (
                    f"{file_path} imports interface: {imp}"
                )

    def test_application_has_no_infrastructure_imports(self, application_files):
        """Application layer must not import from infrastructure (except ports)."""
        for file_path in application_files:
            imports = extract_imports(file_path)

            for imp in imports:
                # Allow ports, not adapters
                if "ports" in imp:
                    continue
                assert "infrastructure" not in imp, (
                    f"{file_path} imports infrastructure: {imp}"
                )
```

---

### Composition Root Tests

```python
# tests/architecture/test_composition_root.py
"""Tests for composition root (dependency injection wiring)."""

from pathlib import Path

import pytest


class TestCompositionRoot:
    """Bootstrap.py is the only place that wires infrastructure."""

    def test_bootstrap_imports_infrastructure(self):
        """Bootstrap.py should import infrastructure adapters."""
        bootstrap_path = Path("src/bootstrap.py")

        if not bootstrap_path.exists():
            pytest.skip("bootstrap.py not yet created")

        imports = extract_imports(bootstrap_path)

        # Should have infrastructure imports
        has_infrastructure = any(
            "infrastructure" in imp for imp in imports
        )
        assert has_infrastructure, (
            "bootstrap.py should import infrastructure adapters"
        )

    def test_cli_adapter_does_not_import_infrastructure(self):
        """CLI adapter receives dispatcher via DI, no infrastructure imports."""
        adapter_path = Path("src/interface/cli/adapter.py")

        if not adapter_path.exists():
            pytest.skip("adapter.py not yet created")

        imports = extract_imports(adapter_path)

        for imp in imports:
            assert "infrastructure" not in imp, (
                f"CLI adapter imports infrastructure directly: {imp}. "
                f"Should receive via dependency injection."
            )

    def test_handlers_do_not_instantiate_adapters(self):
        """Handlers receive ports, don't create adapters."""
        handler_files = Path("src/application/handlers").glob("**/*.py")

        for file_path in handler_files:
            if file_path.name == "__init__.py":
                continue

            imports = extract_imports(file_path)

            for imp in imports:
                # Ports are allowed
                if "ports" in imp:
                    continue
                assert "adapters" not in imp, (
                    f"{file_path} imports adapter directly: {imp}. "
                    f"Should use port interface."
                )
```

---

### Bounded Context Tests

```python
# tests/architecture/test_bounded_contexts.py
"""Tests for bounded context isolation."""


class TestBoundedContextIsolation:
    """Bounded contexts should not import from each other."""

    def test_work_tracking_does_not_import_session_management(self):
        """work_tracking BC must not import from session_management."""
        work_tracking_files = Path("src/work_tracking").glob("**/*.py")

        for file_path in work_tracking_files:
            if file_path.name == "__init__.py":
                continue

            imports = extract_imports(file_path)

            for imp in imports:
                # shared_kernel is allowed
                if "shared_kernel" in imp:
                    continue
                assert "session_management" not in imp, (
                    f"{file_path} imports across BC: {imp}"
                )

    def test_session_management_does_not_import_work_tracking(self):
        """session_management BC must not import from work_tracking."""
        session_files = Path("src/session_management").glob("**/*.py")

        for file_path in session_files:
            if file_path.name == "__init__.py":
                continue

            imports = extract_imports(file_path)

            for imp in imports:
                if "shared_kernel" in imp:
                    continue
                assert "work_tracking" not in imp, (
                    f"{file_path} imports across BC: {imp}"
                )

    def test_shared_kernel_has_no_bc_imports(self):
        """Shared kernel must not import from bounded contexts."""
        shared_files = Path("src/shared_kernel").glob("**/*.py")

        for file_path in shared_files:
            if file_path.name == "__init__.py":
                continue

            imports = extract_imports(file_path)

            for imp in imports:
                assert "work_tracking" not in imp, (
                    f"shared_kernel imports work_tracking: {imp}"
                )
                assert "session_management" not in imp, (
                    f"shared_kernel imports session_management: {imp}"
                )
```

---

### Naming Convention Tests

```python
# tests/architecture/test_naming_conventions.py
"""Tests for file and class naming conventions."""


class TestNamingConventions:
    """Enforce consistent naming across codebase."""

    def test_command_files_end_with_command(self):
        """Command files should be named *_command.py."""
        command_files = Path("src/application/commands").glob("*.py")

        for file_path in command_files:
            if file_path.name == "__init__.py":
                continue

            assert file_path.name.endswith("_command.py"), (
                f"Command file should end with _command.py: {file_path.name}"
            )

    def test_query_files_end_with_query(self):
        """Query files should be named *_query.py."""
        query_files = Path("src/application/queries").glob("*.py")

        for file_path in query_files:
            if file_path.name == "__init__.py":
                continue

            assert file_path.name.endswith("_query.py"), (
                f"Query file should end with _query.py: {file_path.name}"
            )

    def test_handler_files_end_with_handler(self):
        """Handler files should be named *_handler.py."""
        handler_patterns = [
            "src/application/handlers/commands/*.py",
            "src/application/handlers/queries/*.py",
        ]

        for pattern in handler_patterns:
            for file_path in Path(".").glob(pattern):
                if file_path.name == "__init__.py":
                    continue

                assert file_path.name.endswith("_handler.py"), (
                    f"Handler file should end with _handler.py: {file_path.name}"
                )

    def test_port_files_start_with_i(self):
        """Port interface files should start with i (e.g., irepository.py)."""
        port_patterns = [
            "src/*/ports/*.py",
            "src/application/ports/**/*.py",
        ]

        for pattern in port_patterns:
            for file_path in Path(".").glob(pattern):
                if file_path.name == "__init__.py":
                    continue

                assert file_path.name.startswith("i"), (
                    f"Port file should start with 'i': {file_path.name}"
                )
```

---

### One Class Per File Test

```python
# tests/architecture/test_one_class_per_file.py
"""Tests for one-class-per-file pattern."""


class TestOneClassPerFile:
    """Each file should contain at most one public class."""

    def test_command_files_have_one_class(self):
        """Command files should have exactly one command class."""
        command_files = Path("src/application/commands").glob("*.py")

        for file_path in command_files:
            if file_path.name == "__init__.py":
                continue

            tree = ast.parse(file_path.read_text())
            classes = [
                node for node in ast.walk(tree)
                if isinstance(node, ast.ClassDef)
                and not node.name.startswith("_")
            ]

            assert len(classes) <= 1, (
                f"{file_path.name} has {len(classes)} public classes. "
                f"Should have at most 1."
            )

    def test_aggregate_files_have_one_class(self):
        """Aggregate files should have exactly one aggregate class."""
        aggregate_patterns = [
            "src/*/domain/aggregates/*.py",
        ]

        for pattern in aggregate_patterns:
            for file_path in Path(".").glob(pattern):
                if file_path.name == "__init__.py":
                    continue

                tree = ast.parse(file_path.read_text())
                classes = [
                    node for node in ast.walk(tree)
                    if isinstance(node, ast.ClassDef)
                    and not node.name.startswith("_")
                ]

                # Allow one aggregate + related exceptions
                aggregate_classes = [
                    c for c in classes
                    if not c.name.endswith("Error")
                    and not c.name.endswith("Exception")
                ]

                assert len(aggregate_classes) <= 1, (
                    f"{file_path.name} has multiple aggregates: "
                    f"{[c.name for c in aggregate_classes]}"
                )
```

---

## Running Architecture Tests

```bash
# Run all architecture tests
pytest tests/architecture/ -v

# Run specific category
pytest tests/architecture/test_layer_boundaries.py -v

# Run as part of CI
pytest tests/architecture/ --tb=short
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Architecture tests run with every PR. Failures block merge.

> **Jerry Decision**: New architectural rules are added as tests before being documented.

> **Jerry Decision**: Shared kernel is the only allowed cross-boundary import.

---

## References

- **ArchUnit**: [Java Architecture Testing](https://www.archunit.org/)
- **pytest-archon**: [Python Architecture Tests](https://github.com/jwbargsten/pytest-archon)
- **Simon Brown**: [Architecture Fitness Functions](https://www.thoughtworks.com/insights/articles/fitness-function-driven-development)
- **Design Canon**: Section 8.3 - Architecture Tests
- **Related Patterns**: PAT-TEST-001 (Test Pyramid), PAT-ARCH-001 (Composition Root)
