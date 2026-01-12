# Testing Standards

> Test pyramid, BDD cycle, and coverage requirements for Jerry.
> These standards are enforced via CI pipeline.

**Authoritative Pattern Source**: `.claude/patterns/PATTERN-CATALOG.md`

---

## Test Pyramid

```
                    ┌─────────────┐
                    │    E2E      │ ← Full workflow (5%)
                   ┌┴─────────────┴┐
                   │    System     │ ← Component interaction (10%)
                  ┌┴───────────────┴┐
                  │   Integration   │ ← Adapter/port testing (15%)
                 ┌┴─────────────────┴┐
                 │       Unit        │ ← Domain logic (60%)
                ┌┴───────────────────┴┐
                │ Contract+Architecture│ ← Interface compliance (10%)
                └─────────────────────┘
```

### Test Distribution per Feature

| Category | Target % | Focus |
|----------|----------|-------|
| Unit | 60% | Domain logic, value objects, aggregates |
| Integration | 15% | Adapter implementations, port contracts |
| Contract | 5% | External interface compliance |
| Architecture | 5% | Layer boundary enforcement |
| System | 10% | Component interaction |
| E2E | 5% | Full workflow validation |

---

## BDD Red/Green/Refactor Cycle

### The Cycle

```
       ┌─────────────────────────────────────┐
       │                                     │
       ▼                                     │
    ┌──────┐    ┌───────┐    ┌──────────┐   │
    │ RED  │───►│ GREEN │───►│ REFACTOR │───┘
    └──────┘    └───────┘    └──────────┘

    1. RED:      Write a failing test first
    2. GREEN:    Write minimal code to pass
    3. REFACTOR: Improve without changing behavior
```

### RED Phase Requirements

```python
def test_work_item_can_be_completed_when_in_progress():
    """Test MUST fail before implementation."""
    # Arrange
    item = WorkItem.create(title="Test Task")
    item.start()

    # Act
    item.complete()

    # Assert
    assert item.status == Status.COMPLETED
```

**Rule**: NEVER write implementation before the test fails.

### GREEN Phase Requirements

- Write the **minimum** code to make the test pass
- Do not over-engineer
- Do not add features not tested

### REFACTOR Phase Requirements

- Tests must still pass after refactoring
- Improve code clarity and structure
- Remove duplication
- Apply design patterns where appropriate

---

## Test Scenarios

### Happy Path (60%)

Tests where everything works as expected.

```python
def test_create_task_when_valid_input_then_task_created():
    """Happy path: Valid input creates task."""
    command = CreateTaskCommand(title="Implement feature X")
    handler = CreateTaskCommandHandler(repository=mock_repo)

    events = handler.handle(command)

    assert len(events) == 1
    assert isinstance(events[0], TaskCreated)
```

### Negative Cases (30%)

Tests for invalid inputs, error conditions.

```python
def test_create_task_when_empty_title_then_raises_validation_error():
    """Negative: Empty title rejected."""
    with pytest.raises(ValidationError) as exc_info:
        CreateTaskCommand(title="")

    assert "title cannot be empty" in str(exc_info.value)

def test_complete_task_when_already_completed_then_raises_invalid_state():
    """Negative: Cannot complete twice."""
    task = Task.create(title="Test")
    task.start()
    task.complete()

    with pytest.raises(InvalidStateError):
        task.complete()
```

### Edge Cases (10%)

Tests for boundary conditions, unusual but valid inputs.

```python
def test_create_task_when_max_length_title_then_succeeds():
    """Edge: Maximum title length accepted."""
    title = "x" * 500  # Max length
    task = Task.create(title=title)
    assert len(task.title) == 500

def test_create_task_when_unicode_title_then_succeeds():
    """Edge: Unicode characters in title."""
    title = "任务 🎯 Tâche"
    task = Task.create(title=title)
    assert task.title == title
```

---

## Test File Organization

### Location

| Test Type | Location |
|-----------|----------|
| Unit | `tests/unit/{layer}/test_{module}.py` |
| Integration | `tests/integration/test_{adapter}.py` |
| E2E | `tests/e2e/test_{workflow}.py` |
| Contract | `tests/contract/test_{contract}.py` |
| Architecture | `tests/architecture/test_{concern}.py` |

### Naming Convention

```python
def test_{scenario}_when_{condition}_then_{expected}():
    """Docstring describes the test case."""
```

**Examples**:
```python
def test_complete_item_when_in_progress_then_status_becomes_completed(): ...
def test_create_task_when_empty_title_then_raises_validation_error(): ...
def test_dispatch_query_when_no_handler_then_raises_not_found(): ...
```

---

## Test Structure (AAA Pattern)

```python
def test_example():
    # Arrange - Set up test fixtures
    repository = InMemoryRepository()
    handler = CreateTaskCommandHandler(repository=repository)
    command = CreateTaskCommand(title="Test Task")

    # Act - Execute the code under test
    events = handler.handle(command)

    # Assert - Verify the results
    assert len(events) == 1
    assert isinstance(events[0], TaskCreated)
    assert repository.exists(events[0].task_id)
```

---

## Coverage Requirements

### Minimum Thresholds

| Metric | Minimum |
|--------|---------|
| Line Coverage | 90% |
| Branch Coverage | 85% |
| Function Coverage | 95% |

### Exclusions

Coverage may exclude:
- `__init__.py` files (if only imports)
- Abstract base classes (if no concrete logic)
- Type stubs

### CI Enforcement

```yaml
# .github/workflows/ci.yml
- name: Test with coverage
  run: |
    pytest --cov=src --cov-report=term-missing --cov-fail-under=90
```

---

## Architecture Tests

### Purpose

Enforce layer boundaries and dependency rules via automated tests.

### Location

`tests/architecture/test_*.py`

### Examples

```python
def test_domain_has_no_infrastructure_imports():
    """Domain layer must not import infrastructure."""
    domain_path = Path("src/domain")
    for file in domain_path.rglob("*.py"):
        imports = get_imports_from_file(file)
        assert not has_infrastructure_import(imports), f"{file.name} violates boundary"

def test_bootstrap_is_sole_infrastructure_importer():
    """Only bootstrap.py may import infrastructure adapters."""
    bootstrap_imports = get_imports_from_file(Path("src/bootstrap.py"))
    assert has_infrastructure_import(bootstrap_imports)

def test_cli_adapter_receives_dispatcher_via_injection():
    """CLI adapter must not instantiate infrastructure directly."""
    adapter_path = Path("src/interface/cli/adapter.py")
    imports = get_imports_from_file(adapter_path)
    assert not has_infrastructure_import(imports)
```

---

## Contract Tests

### Purpose

Verify external interface compliance (CLI output, API responses, hook formats).

### Examples

```python
def test_session_start_hook_outputs_valid_format():
    """Hook output must match documented format."""
    result = subprocess.run(
        ["python", "src/interface/cli/session_start.py"],
        capture_output=True,
        text=True,
    )

    # Must contain either project-context or project-required tag
    assert (
        "<project-context>" in result.stdout
        or "<project-required>" in result.stdout
        or "<project-error>" in result.stdout
    )

def test_cli_json_output_is_valid_json():
    """CLI JSON output must be parseable."""
    result = subprocess.run(
        ["jerry", "projects", "list", "--json"],
        capture_output=True,
        text=True,
    )

    data = json.loads(result.stdout)
    assert "projects" in data
```

---

## Test Fixtures

### Shared Fixtures in conftest.py

```python
# tests/conftest.py
import pytest
from src.work_tracking.domain.aggregates.work_item import WorkItem

@pytest.fixture
def sample_work_item() -> WorkItem:
    """Create a sample work item for testing."""
    return WorkItem.create(title="Test Work Item")

@pytest.fixture
def in_memory_repository() -> InMemoryRepository:
    """Create an in-memory repository for testing."""
    return InMemoryRepository()
```

### Factory Functions for Complex Objects

```python
# tests/factories.py
def create_work_item(
    title: str = "Test",
    status: Status = Status.PENDING,
    **kwargs,
) -> WorkItem:
    """Factory for creating work items with defaults."""
    item = WorkItem.create(title=title, **kwargs)
    if status == Status.IN_PROGRESS:
        item.start()
    elif status == Status.COMPLETED:
        item.start()
        item.complete()
    return item
```

---

## Mocking Guidelines

### When to Mock

- External services (APIs, databases)
- Time-dependent operations
- Random/non-deterministic behavior
- Expensive operations

### When NOT to Mock

- Domain objects
- Value objects
- Pure functions
- In-memory implementations for ports

### Example

```python
def test_handler_saves_to_repository():
    """Use mock for repository to verify interactions."""
    mock_repo = Mock(spec=IRepository)
    handler = CreateTaskCommandHandler(repository=mock_repo)

    handler.handle(CreateTaskCommand(title="Test"))

    mock_repo.save.assert_called_once()
```

---

## Test Data

### Principles

1. **Minimal**: Use smallest data that tests the behavior
2. **Explicit**: Make test data visible in the test
3. **Isolated**: Each test has its own data
4. **Realistic**: Use domain-appropriate values

### Bad Example

```python
def test_bad():
    item = create_default_item()  # What properties?
    process(item)
    assert item.status == "done"  # Magic string
```

### Good Example

```python
def test_good():
    item = WorkItem.create(title="Implement login feature")
    item.start()

    item.complete()

    assert item.status == Status.COMPLETED
```

---

## References

- **Pattern Catalog**: `.claude/patterns/PATTERN-CATALOG.md`
- **Design Canon**: `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md`
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-archon](https://github.com/jwbargsten/pytest-archon) - Architecture testing
- [PyTestArch](https://pypi.org/project/PyTestArch/) - ArchUnit for Python
