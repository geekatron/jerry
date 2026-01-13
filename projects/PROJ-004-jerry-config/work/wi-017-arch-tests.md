# WI-017: Architecture Tests

| Field | Value |
|-------|-------|
| **ID** | WI-017 |
| **Title** | Architecture Tests |
| **Type** | Task |
| **Status** | COMPLETED |
| **Priority** | HIGH |
| **Phase** | PHASE-06 |
| **Assignee** | WT-Test |
| **Created** | 2026-01-12 |
| **Completed** | 2026-01-12 |

---

## Description

Implement architecture tests to validate hexagonal architecture constraints: domain has no external imports, ports define contracts, adapters implement ports, and composition root wires everything.

---

## Acceptance Criteria

- [x] AC-017.1: Test domain layer has no infrastructure imports
- [x] AC-017.2: Test domain layer has no application imports
- [x] AC-017.3: Test all adapters implement port interfaces
- [x] AC-017.4: Test composition root is sole infrastructure importer
- [x] AC-017.5: All architecture tests pass in CI

---

## Sub-tasks

- [x] ST-017.1: Create `tests/architecture/test_config_boundaries.py`
- [x] ST-017.2: Implement import validation for domain layer
- [x] ST-017.3: Implement port-adapter contract validation
- [x] ST-017.4: Implement composition root validation
- [x] ST-017.5: All tests pass (21/21 architecture tests)

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-017.1 | `test_*_has_no_infrastructure_imports` validates work_tracking, session_management domains | `tests/architecture/test_config_boundaries.py:75-108` |
| AC-017.2 | `test_*_has_no_application_imports` validates domain layer isolation | `tests/architecture/test_config_boundaries.py:86-141` |
| AC-017.3 | `TestPortAdapterContracts` validates LayeredConfigAdapter, AtomicFileAdapter, EnvConfigAdapter | `tests/architecture/test_config_boundaries.py:177-221` |
| AC-017.4 | `test_bootstrap_imports_infrastructure` validates composition root | `tests/architecture/test_composition_root.py:65-73` |
| AC-017.5 | 21/21 architecture tests pass | `pytest tests/architecture/ -v` |

### Test Results

| Test Suite | Count | Status |
|------------|-------|--------|
| test_composition_root.py | 7 | PASSED |
| test_config_boundaries.py | 14 | PASSED |
| **Total Architecture Tests** | **21** | **PASSED** |

---

## Implementation Notes

```python
# tests/architecture/test_config_boundaries.py
import ast
from pathlib import Path
import pytest


class TestDomainLayerBoundaries:
    """Verify domain layer has no external dependencies."""

    def test_domain_has_no_infrastructure_imports(self):
        """Domain layer must not import infrastructure."""
        domain_files = Path("src/domain").rglob("*.py")

        for file in domain_files:
            imports = self._get_imports(file)
            infrastructure_imports = [
                imp for imp in imports
                if "infrastructure" in imp or "adapters" in imp
            ]
            assert not infrastructure_imports, (
                f"{file.name} has infrastructure imports: {infrastructure_imports}"
            )

    def test_domain_has_no_application_imports(self):
        """Domain layer must not import application layer."""
        domain_files = Path("src/domain").rglob("*.py")

        for file in domain_files:
            imports = self._get_imports(file)
            application_imports = [
                imp for imp in imports
                if "application" in imp
            ]
            assert not application_imports, (
                f"{file.name} has application imports: {application_imports}"
            )

    def _get_imports(self, file: Path) -> list[str]:
        """Extract all imports from a Python file."""
        with open(file) as f:
            tree = ast.parse(f.read())

        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
        return imports


class TestPortAdapterContracts:
    """Verify adapters implement port interfaces."""

    def test_layered_config_implements_provider(self):
        """LayeredConfigAdapter must implement IConfigurationProvider."""
        from src.domain.ports.configuration import IConfigurationProvider
        from src.infrastructure.adapters.configuration.layered_config_adapter import (
            LayeredConfigAdapter,
        )

        # Verify structural subtyping
        provider_methods = {m for m in dir(IConfigurationProvider) if not m.startswith("_")}
        adapter_methods = {m for m in dir(LayeredConfigAdapter) if not m.startswith("_")}

        missing = provider_methods - adapter_methods
        assert not missing, f"LayeredConfigAdapter missing methods: {missing}"
```

---

## Progress Log

| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T11:00:00Z | Work item created | Claude |
| 2026-01-12T22:30:00Z | Started WI-017 implementation | Claude |
| 2026-01-12T22:35:00Z | Fixed `get_imports_from_file` to only check module-level imports | Claude |
| 2026-01-12T22:40:00Z | Created `tests/architecture/test_config_boundaries.py` with 14 tests | Claude |
| 2026-01-12T22:45:00Z | All 21 architecture tests pass | Claude |
| 2026-01-12T22:50:00Z | Updated evidence table and marked COMPLETED | Claude |

---

## Dependencies

| Type | Work Item | Relationship |
|------|-----------|--------------|
| Depends On | WI-015 | Need working integration to test |
| Blocks | - | Final validation |

---

## Related Artifacts

- **Testing Standards**: `.claude/rules/testing-standards.md`
- **Architecture Standards**: `.claude/rules/architecture-standards.md`
