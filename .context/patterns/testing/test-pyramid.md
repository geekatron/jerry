# PAT-TEST-001: Test Pyramid Pattern

> **Status**: MANDATORY
> **Category**: Testing Pattern
> **Location**: `tests/`

---

## Overview

The Test Pyramid defines the distribution and focus of different test types. Jerry follows a balanced pyramid with strong unit tests at the base, integration tests in the middle, and fewer end-to-end tests at the top.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Mike Cohn** | "The Test Pyramid provides guidance for test distribution" |
| **Martin Fowler** | "Unit tests should form the bulk of your tests" |
| **Google Testing** | "Small, medium, and large tests have different purposes" |

---

## Jerry Test Pyramid

```
                    ┌─────────────────┐
                    │      E2E        │  5%  - Full workflows
                   ┌┴─────────────────┴┐
                   │      System       │ 10%  - Component interaction
                  ┌┴───────────────────┴┐
                  │    Integration      │ 15%  - Adapter testing
                 ┌┴─────────────────────┴┐
                 │        Unit           │ 60%  - Domain logic
                ┌┴───────────────────────┴┐
                │ Contract + Architecture │ 10%  - Interface compliance
                └─────────────────────────┘
```

---

## Test Categories

### Unit Tests (60%)

Test individual classes and functions in isolation.

**Location**: `tests/unit/`

**Characteristics**:
- Fast (< 1ms each)
- No I/O (filesystem, network, database)
- No external dependencies
- Test domain logic

```python
# tests/unit/domain/test_work_item.py
def test_work_item_can_be_completed_when_in_progress():
    """Work item transitions to DONE when completed from IN_PROGRESS."""
    # Arrange
    item = WorkItem.create(id="WORK-001", title="Test")
    item.start()

    # Act
    item.complete()

    # Assert
    assert item.status == WorkItemStatus.DONE


def test_work_item_cannot_be_completed_when_pending():
    """Work item cannot be completed directly from PENDING."""
    item = WorkItem.create(id="WORK-001", title="Test")

    with pytest.raises(InvalidStateError):
        item.complete()
```

---

### Integration Tests (15%)

Test adapters with real infrastructure.

**Location**: `tests/integration/`

**Characteristics**:
- Medium speed (10-100ms each)
- Real I/O operations
- Test port/adapter contracts
- Use test fixtures/containers

```python
# tests/integration/test_filesystem_adapter.py
def test_filesystem_adapter_persists_project(tmp_path):
    """Adapter persists and retrieves project from filesystem."""
    # Arrange
    adapter = FilesystemProjectAdapter(base_path=tmp_path)
    project = ProjectInfo(id="PROJ-001", path="", status="ACTIVE")

    # Act
    adapter.save(project)
    loaded = adapter.get(ProjectId("PROJ-001"))

    # Assert
    assert loaded is not None
    assert loaded.id == "PROJ-001"
    assert (tmp_path / "projects/PROJ-001").exists()


def test_event_store_maintains_order(tmp_path):
    """Event store preserves event order."""
    store = JsonFileEventStore(tmp_path)

    events = [
        WorkItemCreated(work_item_id="W-1", title="First"),
        WorkItemStarted(work_item_id="W-1"),
        WorkItemCompleted(work_item_id="W-1"),
    ]

    for i, event in enumerate(events):
        store.append("stream-1", [event], expected_version=i)

    loaded = store.read("stream-1")
    assert len(loaded) == 3
    assert isinstance(loaded[0], WorkItemCreated)
    assert isinstance(loaded[2], WorkItemCompleted)
```

---

### Contract Tests (5%)

Verify external interface compliance.

**Location**: `tests/contract/`

**Characteristics**:
- Test public API contracts
- Verify output formats
- Test hook outputs
- Document expectations

```python
# tests/contract/test_cli_output.py
def test_cli_json_output_is_valid_json():
    """CLI --json flag produces valid JSON."""
    result = subprocess.run(
        ["python", "-m", "jerry", "list-tasks", "--json"],
        capture_output=True,
        text=True,
    )

    # Must be valid JSON
    data = json.loads(result.stdout)
    assert isinstance(data, (dict, list))


def test_session_hook_output_format():
    """Session hook outputs expected tags."""
    result = subprocess.run(
        ["python", "scripts/session_start.py"],
        capture_output=True,
        text=True,
    )

    # Must contain project context or required tag
    assert (
        "<project-context>" in result.stdout
        or "<project-required>" in result.stdout
        or "<project-error>" in result.stdout
    )
```

---

### Architecture Tests (5%)

Enforce architectural constraints.

**Location**: `tests/architecture/`

**Characteristics**:
- Static analysis
- Dependency validation
- Layer boundary checks
- Import verification

```python
# tests/architecture/test_layer_boundaries.py
def test_domain_has_no_infrastructure_imports():
    """Domain layer must not import from infrastructure."""
    domain_files = Path("src/work_tracking/domain").rglob("*.py")

    for file_path in domain_files:
        imports = extract_imports(file_path)

        for imp in imports:
            assert "infrastructure" not in imp, (
                f"{file_path.name} imports infrastructure: {imp}"
            )


def test_application_has_no_interface_imports():
    """Application layer must not import from interface."""
    app_files = Path("src/application").rglob("*.py")

    for file_path in app_files:
        imports = extract_imports(file_path)

        for imp in imports:
            assert "interface" not in imp, (
                f"{file_path.name} imports interface: {imp}"
            )


def test_composition_root_is_only_infrastructure_importer():
    """Only bootstrap.py should import concrete adapters."""
    src_files = list(Path("src").rglob("*.py"))
    bootstrap_path = Path("src/bootstrap.py")

    infrastructure_importers = []

    for file_path in src_files:
        if file_path == bootstrap_path:
            continue

        imports = extract_imports(file_path)
        for imp in imports:
            if "infrastructure.adapters" in imp:
                infrastructure_importers.append(file_path.name)

    assert not infrastructure_importers, (
        f"Files importing infrastructure (should be bootstrap only): "
        f"{infrastructure_importers}"
    )
```

---

### System Tests (10%)

Test component interaction.

**Location**: `tests/system/`

**Characteristics**:
- Multi-component tests
- In-process integration
- No external services
- Real dispatcher flow

```python
# tests/system/test_create_and_complete_flow.py
def test_create_and_complete_workflow():
    """Complete workflow: create task, start, complete."""
    # Arrange - real dispatchers with in-memory adapters
    dispatcher = create_test_command_dispatcher()

    # Act - create task
    create_events = dispatcher.dispatch(
        CreateWorkItemCommand(title="Test Task", priority="high")
    )
    task_id = create_events[0].work_item_id

    # Act - start task
    dispatcher.dispatch(StartWorkItemCommand(work_item_id=task_id))

    # Act - complete task
    complete_events = dispatcher.dispatch(
        CompleteWorkItemCommand(work_item_id=task_id)
    )

    # Assert
    assert len(complete_events) == 1
    assert isinstance(complete_events[0], WorkItemCompleted)
```

---

### E2E Tests (5%)

Test full system behavior.

**Location**: `tests/e2e/`

**Characteristics**:
- Slowest (seconds)
- Full stack
- Real CLI invocation
- External dependencies

```python
# tests/e2e/test_cli_workflow.py
def test_full_cli_workflow(tmp_path, monkeypatch):
    """Test complete CLI workflow end-to-end."""
    # Setup environment
    monkeypatch.setenv("JERRY_PROJECTS_DIR", str(tmp_path / "projects"))

    # Create project
    result = subprocess.run(
        ["python", "-m", "jerry", "init", "PROJ-001-test"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

    # Create task
    result = subprocess.run(
        ["python", "-m", "jerry", "create-task", "Test Task"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Created" in result.stdout

    # List tasks
    result = subprocess.run(
        ["python", "-m", "jerry", "list-tasks", "--json"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    tasks = json.loads(result.stdout)
    assert len(tasks) > 0
```

---

## Test Naming Convention

```python
def test_{scenario}_when_{condition}_then_{expected}():
    """Docstring describing the test."""
```

**Examples**:
```python
def test_complete_item_when_in_progress_then_status_becomes_done(): ...
def test_create_task_when_empty_title_then_raises_validation_error(): ...
def test_dispatch_query_when_no_handler_then_raises_not_found(): ...
```

---

## Test Structure (AAA Pattern)

```python
def test_example():
    # Arrange - Setup test fixtures and dependencies
    repository = InMemoryRepository()
    handler = CreateWorkItemCommandHandler(repository=repository)
    command = CreateWorkItemCommand(title="Test Task")

    # Act - Execute the code under test
    events = handler.handle(command)

    # Assert - Verify the results
    assert len(events) == 1
    assert isinstance(events[0], WorkItemCreated)
    assert repository.exists(events[0].work_item_id)
```

---

## Coverage Requirements

| Metric | Target |
|--------|--------|
| Line Coverage | ≥ 90% |
| Branch Coverage | ≥ 85% |
| Function Coverage | ≥ 95% |

**Exclusions**:
- `__init__.py` (imports only)
- Abstract base classes (no concrete logic)
- Type stubs

---

## Jerry-Specific Decisions

> **Jerry Decision**: Unit tests use InMemoryRepository, not mocks for domain testing.

> **Jerry Decision**: Integration tests use temporary directories (tmp_path fixture).

> **Jerry Decision**: Architecture tests enforce layer boundaries automatically.

---

## References

- **Mike Cohn**: Succeeding with Agile (2009)
- **Martin Fowler**: [Test Pyramid](https://martinfowler.com/bliki/TestPyramid.html)
- **Design Canon**: Section 8.1 - Test Pyramid
- **Related Patterns**: PAT-TEST-002 (BDD Cycle), PAT-TEST-003 (Architecture Tests)
