# Testing Practices Guide

> Educational companion to [testing-standards.md](../rules/testing-standards.md).
> Explains test pyramid rationale, BDD cycle walkthrough, mocking decision guide, and coverage strategy.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Test Pyramid Rationale](#test-pyramid-rationale) | Why the pyramid shape matters |
| [BDD Cycle Walkthrough](#bdd-cycle-walkthrough) | Red-Green-Refactor in practice |
| [Test Scenario Design](#test-scenario-design) | Happy path, negative cases, edge cases |
| [Mocking Decision Guide](#mocking-decision-guide) | When to mock, when not to mock |
| [AAA Pattern](#aaa-pattern) | Arrange-Act-Assert structure |
| [Coverage Strategy](#coverage-strategy) | Line, branch, function coverage |
| [Architecture Testing](#architecture-testing) | Enforcing layer boundaries |
| [Test Data Management](#test-data-management) | Fixtures, factories, builders |
| [Current vs Target](#current-vs-target) | Gap analysis between actual and ideal test state |
| [Evidence](#evidence) | Verified codebase file paths and code quotes |

---

## Test Pyramid Rationale

### The Shape

```
                    ┌─────────────┐
                    │    E2E      │ ← 5% (Slow, brittle)
                   ┌┴─────────────┴┐
                   │    System     │ ← 10% (Multiple components)
                  ┌┴───────────────┴┐
                  │   Integration   │ ← 15% (Adapters, I/O)
                 ┌┴─────────────────┴┐
                 │       Unit        │ ← 60% (Fast, focused)
                ┌┴───────────────────┴┐
                │ Contract+Architecture│ ← 10% (Interface, boundaries)
                └─────────────────────┘
```

### Why Pyramid, Not Diamond or Ice Cream Cone?

#### Anti-Pattern: Ice Cream Cone (Top-Heavy)

```
                ┌───────────────────┐
                │                   │
                │       E2E         │ ← 70% (Slow, flaky)
                │                   │
                └┬──────────────────┘
                 │   Integration    │ ← 20%
                 └┬─────────────────┘
                  │      Unit       │ ← 10% (Too few!)
                  └─────────────────┘
```

**Problems**:
1. **Slow feedback**: E2E tests take minutes to run
2. **Brittle**: Break when UI changes, even if logic is correct
3. **Hard to debug**: Failure could be anywhere in the stack
4. **Expensive to maintain**: Require full environment setup

---

#### Anti-Pattern: Hourglass (Middle-Heavy)

```
                    ┌─────────────┐
                    │    E2E      │ ← 10%
                   ┌┴─────────────┴┐
                   │               │
                   │  Integration  │ ← 70% (Over-tested)
                   │               │
                  ┌┴───────────────┴┐
                  │      Unit       │ ← 20%
                  └─────────────────┘
```

**Problems**:
1. **Slow**: Integration tests require I/O (database, filesystem)
2. **Redundant**: Testing same logic at integration and unit level
3. **Missing E2E**: User flows not validated

---

#### Correct: Pyramid (Bottom-Heavy)

**Why this works**:

| Level | Speed | Cost | Feedback Quality | Coverage Scope |
|-------|-------|------|------------------|----------------|
| E2E | Slowest | Highest | User perspective | Full stack |
| System | Slow | High | Component interaction | Multi-component |
| Integration | Medium | Medium | Adapter correctness | Single adapter |
| Unit | Fast | Low | Logic correctness | Single function |

**Trade-off**: Unit tests are **fast** and **cheap**, so we write **many**. E2E tests are **slow** and **expensive**, so we write **few**.

---

### Layer-by-Layer Breakdown

#### Unit Tests (60%)

**Focus**: Pure domain logic, value objects, aggregates.

**Characteristics**:
- No I/O (no database, no filesystem, no network)
- Fast (milliseconds per test)
- Isolated (test one function at a time)

**Example**:
```python
# (Hypothetical -- illustrative pattern)
def test_work_item_can_be_completed_when_in_progress():
    """Test domain logic: state transition."""
    # Arrange
    item = WorkItem.create(title="Test")
    item.start()  # Move to IN_PROGRESS

    # Act
    item.complete()

    # Assert
    assert item.status == Status.COMPLETED
```

**Why 60%?**
- Domain logic is the **core value**
- Most business rules live here
- Fast feedback during development

---

#### Integration Tests (15%)

**Focus**: Adapter implementations, port contracts.

**Characteristics**:
- Test adapter <-> external system interaction
- May involve I/O (filesystem, in-memory database)
- Verify port contract compliance

**Example**:
```python
def test_filesystem_adapter_saves_and_retrieves_work_item(tmp_path):
    """Test filesystem adapter implementation."""
    # Arrange
    adapter = FilesystemWorkItemAdapter(base_path=tmp_path)
    item = WorkItem.create(title="Test Item")

    # Act
    adapter.save(item)
    retrieved = adapter.get(item.id)

    # Assert
    assert retrieved is not None
    assert retrieved.id == item.id
    assert retrieved.title == "Test Item"
```

**Why 15%?**
- Fewer adapters than domain logic
- Adapters are implementation details, not core business value
- Integration tests are slower than unit tests

---

#### Contract Tests (5%)

**Focus**: External interface compliance (CLI output, API responses).

**Example**:
```python
def test_cli_list_command_outputs_valid_json():
    """Test CLI contract: JSON output format."""
    result = subprocess.run(
        ["jerry", "items", "list", "--json"],
        capture_output=True,
        text=True,
    )

    data = json.loads(result.stdout)  # Must parse
    assert "items" in data
    assert isinstance(data["items"], list)
```

**Why 5%?**
- Few external interfaces (CLI, API)
- Contract is stable (doesn't change often)

---

#### Architecture Tests (5%)

**Focus**: Layer boundary enforcement.

**Example**:
```python
def test_domain_has_no_infrastructure_imports():
    """Enforce H-07: Domain cannot import infrastructure."""
    domain_files = Path("src/domain").rglob("*.py")
    for file in domain_files:
        imports = extract_imports(file)
        forbidden = [i for i in imports if "infrastructure" in i]
        assert not forbidden, f"{file} imports {forbidden}"
```

**Why 5%?**
- Few architectural rules (H-07, H-10)
- Architectural violations are rare once established

---

#### System Tests (10%)

**Focus**: Component interaction.

**Example**:
```python
def test_create_and_complete_work_item_workflow():
    """Test workflow: create -> start -> complete."""
    # Arrange
    dispatcher = create_test_dispatcher()

    # Act: Create
    create_cmd = CreateWorkItemCommand(title="Test Task")
    events = dispatcher.dispatch(create_cmd)
    item_id = events[0].work_item_id

    # Act: Start
    start_cmd = StartWorkItemCommand(work_item_id=item_id)
    dispatcher.dispatch(start_cmd)

    # Act: Complete
    complete_cmd = CompleteWorkItemCommand(work_item_id=item_id)
    dispatcher.dispatch(complete_cmd)

    # Assert: Query final state
    query = GetWorkItemQuery(work_item_id=item_id)
    item = dispatcher.dispatch(query)
    assert item.status == "completed"
```

**Why 10%?**
- More complex workflows than unit logic
- Tests component wiring (commands, handlers, repositories)
- Slower than unit tests (involves multiple components)

---

#### E2E Tests (5%)

**Focus**: Full workflow from user perspective.

**Example**:
```python
def test_user_can_create_and_track_work_item_via_cli():
    """E2E: User creates, starts, completes work item via CLI."""
    # Arrange: Fresh environment
    env = create_test_environment()

    # Act: Create via CLI
    result = run_cli(["jerry", "items", "create", "--title", "E2E Test"])
    assert result.returncode == 0
    item_id = extract_id_from_output(result.stdout)

    # Act: Start via CLI
    result = run_cli(["jerry", "items", "start", item_id])
    assert result.returncode == 0

    # Act: Complete via CLI
    result = run_cli(["jerry", "items", "complete", item_id])
    assert result.returncode == 0

    # Assert: List shows completed item
    result = run_cli(["jerry", "items", "list", "--status", "completed"])
    assert item_id in result.stdout
```

**Why 5%?**
- Few critical user workflows
- Expensive to write and maintain
- Slow (full stack involved)

---

## BDD Cycle Walkthrough

### The Cycle: Red → Green → Refactor

```
       ┌─────────────────────────────────────┐
       │                                     │
       ▼                                     │
    ┌──────┐    ┌───────┐    ┌──────────┐   │
    │ RED  │───►│ GREEN │───►│ REFACTOR │───┘
    └──────┘    └───────┘    └──────────┘
```

---

### Phase 1: RED (Write Failing Test)

**Goal**: Write a test that fails because the feature doesn't exist yet.

**Example**: Implementing work item completion.

```python
def test_work_item_can_be_completed_when_in_progress():
    """Test that work item can transition to completed."""
    # Arrange
    item = WorkItem.create(title="Implement feature X")
    item.start()  # Move to IN_PROGRESS

    # Act
    item.complete()  # ← This method doesn't exist yet!

    # Assert
    assert item.status == Status.COMPLETED
```

**Run test**:
```bash
$ uv run pytest tests/unit/domain/test_work_item.py::test_work_item_can_be_completed_when_in_progress
```

**Expected output**:
```
FAILED: AttributeError: 'WorkItem' object has no attribute 'complete'
```

**Why write failing test first?**
1. **Proves the test works**: If it passes before implementation, test is broken
2. **Defines the API**: Forces you to think about interface before implementation
3. **TDD discipline**: Ensures test coverage

---

### Phase 2: GREEN (Make Test Pass)

**Goal**: Write **minimal** code to make the test pass. Don't over-engineer.

```python
class WorkItem:
    def __init__(self, id: str, title: str) -> None:
        self.id = id
        self.title = title
        self.status = Status.PENDING

    @classmethod
    def create(cls, title: str) -> "WorkItem":
        return cls(id=generate_id(), title=title)

    def start(self) -> None:
        self.status = Status.IN_PROGRESS

    def complete(self) -> None:  # ← Minimal implementation
        self.status = Status.COMPLETED
```

**Run test**:
```bash
$ uv run pytest tests/unit/domain/test_work_item.py::test_work_item_can_be_completed_when_in_progress
```

**Expected output**:
```
PASSED
```

**Temptation to resist**: "But what if the item is already completed? What if it's not in progress?"

**Answer**: Write those tests **next**. Right now, just make the current test pass.

---

### Phase 3: REFACTOR (Improve Code)

**Goal**: Clean up code without changing behavior. Tests must still pass.

**Refactor 1: Add validation**:
```python
def complete(self) -> None:
    if self.status != Status.IN_PROGRESS:
        raise InvalidStateError(
            entity_type="WorkItem",
            entity_id=self.id,
            current_state=self.status.value,
        )
    self.status = Status.COMPLETED
```

**Run tests**:
```bash
$ uv run pytest tests/unit/domain/test_work_item.py
```

**Expected**: All tests still pass (except now we need a test for the validation).

---

**Refactor 2: Extract method**:
```python
def complete(self) -> None:
    self._validate_can_complete()
    self._transition_to(Status.COMPLETED)

def _validate_can_complete(self) -> None:
    if self.status != Status.IN_PROGRESS:
        raise InvalidStateError(...)

def _transition_to(self, target: Status) -> None:
    self.status = target
```

**Run tests**: All still pass.

---

### RED Again: Test Validation

Now that we added validation, we need a test for it.

```python
def test_complete_work_item_when_not_in_progress_then_raises_error():
    """Test validation: cannot complete if not in progress."""
    # Arrange
    item = WorkItem.create(title="Test")
    # Note: item is PENDING, not IN_PROGRESS

    # Act & Assert
    with pytest.raises(InvalidStateError):
        item.complete()
```

**Run test**: FAILS (good! validation not implemented yet).

---

### GREEN Again: Implement Validation

Already done in Refactor phase! Test now passes.

---

### Key Principles

1. **Never skip RED phase**: Don't write code before the test fails
2. **Keep GREEN phase minimal**: Don't add features not tested
3. **Refactor fearlessly**: Tests protect you from breaking things
4. **Repeat**: One feature at a time

---

## Test Scenario Design

### Distribution: 60-30-10 Rule

| Scenario Type | Target % | Purpose |
|---------------|----------|---------|
| Happy Path | 60% | Verify correct behavior with valid inputs |
| Negative Cases | 30% | Verify error handling with invalid inputs |
| Edge Cases | 10% | Verify boundary conditions |

---

### Happy Path Tests (60%)

**Definition**: Everything works as expected.

**Examples**:
```python
def test_create_work_item_when_valid_input_then_item_created():
    """Happy path: Valid title creates work item."""
    command = CreateWorkItemCommand(title="Implement login")
    handler = CreateWorkItemCommandHandler(repository=mock_repo)

    events = handler.handle(command)

    assert len(events) == 1
    assert isinstance(events[0], WorkItemCreated)
    assert events[0].title == "Implement login"

def test_complete_work_item_when_in_progress_then_status_completed():
    """Happy path: Completing in-progress item succeeds."""
    item = WorkItem.create(title="Test")
    item.start()

    item.complete()

    assert item.status == Status.COMPLETED

def test_list_work_items_when_items_exist_then_returns_list():
    """Happy path: Query returns items."""
    repository = InMemoryRepository()
    repository.save(WorkItem.create(title="Item 1"))
    repository.save(WorkItem.create(title="Item 2"))
    handler = ListWorkItemsQueryHandler(repository=repository)

    result = handler.handle(ListWorkItemsQuery())

    assert len(result) == 2
```

**Why 60%?**
- Most usage follows happy path
- Validates core functionality
- Most important to get right

---

### Negative Cases (30%)

**Definition**: Invalid inputs, error conditions.

**Examples**:
```python
def test_create_work_item_when_empty_title_then_raises_validation_error():
    """Negative: Empty title rejected."""
    with pytest.raises(ValidationError) as exc_info:
        CreateWorkItemCommand(title="")

    assert "title" in str(exc_info.value)

def test_complete_work_item_when_not_in_progress_then_raises_error():
    """Negative: Cannot complete if not started."""
    item = WorkItem.create(title="Test")

    with pytest.raises(InvalidStateError):
        item.complete()

def test_get_work_item_when_not_found_then_raises_not_found_error():
    """Negative: Missing item raises error."""
    repository = InMemoryRepository()

    with pytest.raises(NotFoundError) as exc_info:
        repository.get_or_raise("NONEXISTENT")

    assert "NONEXISTENT" in str(exc_info.value)
```

**Why 30%?**
- Error handling is critical
- Users make mistakes
- Systems fail

---

### Edge Cases (10%)

**Definition**: Boundary conditions, unusual but valid inputs.

**Examples**:
```python
def test_create_work_item_when_max_length_title_then_succeeds():
    """Edge: Maximum title length accepted."""
    max_title = "x" * 500  # Assume 500 is max
    item = WorkItem.create(title=max_title)

    assert len(item.title) == 500

def test_create_work_item_when_unicode_emoji_title_then_succeeds():
    """Edge: Unicode and emoji in title."""
    title = "Fix bug 🐛 in module"
    item = WorkItem.create(title=title)

    assert item.title == title

def test_list_work_items_when_no_items_then_returns_empty_list():
    """Edge: Empty repository returns empty list."""
    repository = InMemoryRepository()
    handler = ListWorkItemsQueryHandler(repository=repository)

    result = handler.handle(ListWorkItemsQuery())

    assert result == []

def test_work_item_with_1000_subtasks_then_handles_correctly():
    """Edge: Large number of subtasks."""
    item = WorkItem.create(title="Parent")
    for i in range(1000):
        item.add_subtask(Task.create(title=f"Subtask {i}"))

    assert item.subtask_count == 1000
```

**Why 10%?**
- Edge cases are rare
- But can cause production issues
- Cover critical boundaries

---

## Mocking Decision Guide

### When to Mock

```
Question: Should I mock this dependency?

Mock if:
├─ External service (API, database, network)
│  Examples: GitHub API, PostgreSQL, HTTP client
│
├─ Time-dependent behavior (datetime.now(), random())
│  Examples: Timestamps, UUID generation
│
├─ Expensive operations (file I/O, heavy computation)
│  Examples: Large file processing, ML model inference
│
└─ Non-deterministic behavior
   Examples: Random number generation, external state
```

---

### When NOT to Mock

```
DO NOT mock:
├─ Domain objects (entities, aggregates, value objects)
│  Why: You're testing domain logic!
│
├─ Pure functions (no side effects)
│  Why: Actual implementation is fast and deterministic
│
├─ Value objects (immutable, simple)
│  Why: Creating real value objects is trivial
│
└─ In-memory implementations (for port testing)
   Why: In-memory adapters are designed for testing
```

---

### Ambiguous Cases

| Question | Guidance |
|----------|----------|
| **Mock the repository or use in-memory?** | For **unit tests** of handlers, mocking is fine (you are testing handler logic, not repo). For **integration tests**, use in-memory implementations (you are testing handler + repo interaction). |
| **Should I mock the event store?** | Same principle: mock for unit tests, use `InMemoryEventStore` for integration tests. Never mock for architecture tests. |
| **What about testing aggregate state transitions?** | NEVER mock the aggregate. Create a real instance, apply operations, and assert state. Aggregates are domain logic -- the core thing you are testing. |
| **Mock or stub?** | Use `Mock(spec=IRepository)` for verifying interactions (was `save()` called?). Use in-memory implementations for state-based testing (was the item actually saved?). |
| **Test fixture vs inline setup?** | Use fixtures for reusable setup shared across many tests. Use inline setup when the test is self-documenting and the setup is small (< 5 lines). |
| **How to test error paths in infrastructure?** | Inject a mock that raises the expected exception. For filesystem adapters, use `tmp_path` (pytest fixture) and manipulate files to create error conditions. |

---

### Mocking Examples

#### ✅ GOOD: Mock External Service

```python
def test_create_work_item_handler_saves_to_repository():
    """Test handler saves to repository."""
    # Arrange
    mock_repo = Mock(spec=IRepository)
    handler = CreateWorkItemCommandHandler(repository=mock_repo)
    command = CreateWorkItemCommand(title="Test")

    # Act
    handler.handle(command)

    # Assert
    mock_repo.save.assert_called_once()
    saved_item = mock_repo.save.call_args[0][0]
    assert saved_item.title == "Test"
```

**Why mock repository?**
- Repository involves I/O (filesystem, database)
- We're testing handler logic, not repository implementation
- Faster (no I/O overhead)

---

#### ✅ GOOD: Mock Time

```python
def test_work_item_created_event_has_timestamp(mocker):
    """Test event includes creation timestamp."""
    # Arrange
    fixed_time = datetime(2024, 1, 15, 10, 30, 0)
    mocker.patch("datetime.datetime")
    datetime.datetime.now.return_value = fixed_time

    # Act
    event = WorkItemCreated.create(work_item_id="123", title="Test")

    # Assert
    assert event.created_at == fixed_time
```

**Why mock time?**
- Makes test deterministic (not dependent on when it runs)
- Can test time-sensitive logic

---

#### ❌ BAD: Mock Domain Object

```python
def test_work_item_completion_BAD():
    """BAD: Mocking the thing we're testing!"""
    # Arrange
    mock_item = Mock(spec=WorkItem)
    mock_item.status = Status.IN_PROGRESS

    # Act
    mock_item.complete()

    # Assert
    mock_item.complete.assert_called_once()  # ❌ Tests nothing!
```

**Why this is bad?**
- Not testing actual domain logic
- Just verifying the mock was called
- False sense of coverage

**Fix: Use real domain object**:
```python
def test_work_item_completion_GOOD():
    """GOOD: Testing real domain logic."""
    # Arrange
    item = WorkItem.create(title="Test")
    item.start()

    # Act
    item.complete()

    # Assert
    assert item.status == Status.COMPLETED  # ✅ Tests real behavior
```

---

#### ❌ BAD: Mock Pure Function

```python
def calculate_priority_score(priority: Priority, urgency: Urgency) -> int:
    """Pure function: no side effects."""
    return priority.value * urgency.value

def test_calculate_priority_score_BAD(mocker):
    """BAD: Mocking a pure function."""
    mocker.patch("calculate_priority_score", return_value=42)

    score = calculate_priority_score(Priority("high"), Urgency("critical"))

    assert score == 42  # ❌ Not testing real calculation
```

**Fix: Use real function**:
```python
def test_calculate_priority_score_GOOD():
    """GOOD: Testing real calculation."""
    score = calculate_priority_score(Priority("high"), Urgency("critical"))

    assert score == expected_value  # ✅ Tests real logic
```

---

### In-Memory Implementations for Port Testing

**Pattern**: Use in-memory adapter instead of mocks for port contract testing.

```python
# Infrastructure: In-memory implementation
class InMemoryWorkItemRepository(IRepository):
    def __init__(self) -> None:
        self._items: dict[str, WorkItem] = {}

    def save(self, item: WorkItem) -> None:
        self._items[item.id] = item

    def get(self, id: str) -> WorkItem | None:
        return self._items.get(id)

# Test: Use in-memory implementation
def test_handler_workflow_with_in_memory_repo():
    """Test handler with real repository implementation."""
    # Arrange
    repository = InMemoryWorkItemRepository()  # Real implementation!
    handler = CreateWorkItemCommandHandler(repository=repository)

    # Act
    events = handler.handle(CreateWorkItemCommand(title="Test"))
    item_id = events[0].work_item_id

    # Assert
    item = repository.get(item_id)
    assert item is not None
    assert item.title == "Test"
```

**Why in-memory over mock?**
- Tests **real** repository behavior
- Catches bugs in repository logic
- More confidence than mocks

---

## AAA Pattern

### Structure: Arrange-Act-Assert

```python
def test_example():
    # Arrange: Set up preconditions
    item = WorkItem.create(title="Test")
    item.start()

    # Act: Execute the code under test
    item.complete()

    # Assert: Verify the outcome
    assert item.status == Status.COMPLETED
```

**Why AAA?**
- **Readable**: Clear test structure
- **Maintainable**: Easy to modify sections independently
- **Debuggable**: Failure points are obvious

---

### Arrange Phase

**Purpose**: Set up test fixtures and preconditions.

**Good practices**:
- Create test data explicitly (don't hide in fixtures)
- Use builders/factories for complex objects
- Keep minimal (only what's needed for this test)

```python
def test_example():
    # Arrange
    repository = InMemoryRepository()
    item1 = WorkItem.create(title="Item 1")
    item2 = WorkItem.create(title="Item 2")
    repository.save(item1)
    repository.save(item2)
    handler = ListWorkItemsQueryHandler(repository=repository)
```

---

### Act Phase

**Purpose**: Execute the code under test.

**Good practices**:
- **One action per test** (test one thing)
- Keep simple (ideally one line)

```python
def test_example():
    # Arrange
    item = WorkItem.create(title="Test")

    # Act
    item.start()  # One action
```

**Bad: Multiple actions**:
```python
def test_example_BAD():
    # Act
    item = WorkItem.create(title="Test")
    item.start()
    item.complete()  # ❌ Testing multiple behaviors
```

**Fix: Split into multiple tests**:
```python
def test_work_item_can_be_started():
    item = WorkItem.create(title="Test")
    item.start()
    assert item.status == Status.IN_PROGRESS

def test_work_item_can_be_completed():
    item = WorkItem.create(title="Test")
    item.start()
    item.complete()
    assert item.status == Status.COMPLETED
```

---

### Assert Phase

**Purpose**: Verify the outcome.

**Good practices**:
- Be specific (test exact values, not just truthiness)
- Test state, not implementation

```python
# ✅ GOOD: Specific assertion
assert item.status == Status.COMPLETED

# ❌ BAD: Vague assertion
assert item.status  # True if not None, but doesn't verify value
```

**Multiple assertions are OK if testing related properties**:
```python
def test_create_work_item_sets_all_properties():
    event = WorkItemCreated.create(work_item_id="123", title="Test")

    assert event.work_item_id == "123"
    assert event.title == "Test"
    assert event.created_at is not None
    assert event.EVENT_TYPE == "work_item.created"
```

---

## Coverage Strategy

### Coverage Metrics

| Metric | Target | Purpose |
|--------|--------|---------|
| Line Coverage | >= 90% | Every line executed at least once |
| Branch Coverage | >= 85% | Every if/else branch taken |
| Function Coverage | >= 95% | Every function called |

---

### Line Coverage

**What it measures**: Percentage of lines executed during tests.

**Example**:
```python
def complete(self) -> None:
    if self.status != Status.IN_PROGRESS:  # Line 1
        raise InvalidStateError(...)        # Line 2
    self.status = Status.COMPLETED          # Line 3
```

**Coverage scenarios**:
- Test 1 (happy path): Executes lines 1, 3 → 67% coverage
- Test 2 (error path): Executes lines 1, 2 → 67% coverage
- Both tests: Execute lines 1, 2, 3 → 100% coverage

---

### Branch Coverage

**What it measures**: Percentage of decision branches taken.

**Example**:
```python
def is_completable(self) -> bool:
    if self.status == Status.IN_PROGRESS and self.all_subtasks_done:
        return True
    return False
```

**Branches**:
1. `status == IN_PROGRESS` is True
2. `status == IN_PROGRESS` is False
3. `all_subtasks_done` is True
4. `all_subtasks_done` is False

**Full coverage requires testing all combinations**:
- Test 1: `status=IN_PROGRESS, all_subtasks_done=True` → True
- Test 2: `status=IN_PROGRESS, all_subtasks_done=False` → False
- Test 3: `status=PENDING, all_subtasks_done=True` → False

---

### Coverage Exclusions

**Exclude from coverage**:
- `__init__.py` (if only imports)
- Abstract methods (no implementation to test)
- `TYPE_CHECKING` blocks (type hints only)

```python
# .coveragerc or pyproject.toml
[coverage:report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "@abstractmethod",
    "raise NotImplementedError",
]
```

---

## Architecture Testing

### Purpose

**Enforce layer boundaries** via automated tests.

---

### Test Examples

#### H-07: Domain has no infrastructure imports

```python
def test_domain_has_no_infrastructure_imports():
    """Domain layer must not import infrastructure."""
    domain_path = Path("src/domain")
    for file in domain_path.rglob("*.py"):
        imports = extract_imports_from_file(file)
        forbidden = [i for i in imports if "infrastructure" in i]
        assert not forbidden, f"{file.name} imports infrastructure: {forbidden}"
```

---

#### H-07: Application has no interface imports

```python
def test_application_has_no_interface_imports():
    """Application layer must not import interface."""
    app_path = Path("src/application")
    for file in app_path.rglob("*.py"):
        imports = extract_imports_from_file(file)
        forbidden = [i for i in imports if "interface" in i]
        assert not forbidden, f"{file.name} imports interface: {forbidden}"
```

---

#### H-07: Only bootstrap instantiates infrastructure

```python
def test_only_bootstrap_imports_infrastructure_adapters():
    """Only bootstrap.py may import infrastructure adapters."""
    # Check bootstrap imports infrastructure
    bootstrap_imports = extract_imports_from_file(Path("src/bootstrap.py"))
    assert any("infrastructure" in i for i in bootstrap_imports)

    # Check no other files import infrastructure adapters
    for layer in ["application", "domain", "interface"]:
        layer_path = Path(f"src/{layer}")
        for file in layer_path.rglob("*.py"):
            imports = extract_imports_from_file(file)
            adapters = [i for i in imports if "infrastructure/adapters" in i]
            assert not adapters, f"{file.name} violates H-07: {adapters}"
```

---

## Test Data Management

### Fixtures

**Use for**: Shared, reusable test data.

```python
# tests/conftest.py
import pytest
from src.domain.aggregates.work_item import WorkItem

@pytest.fixture
def sample_work_item() -> WorkItem:
    """Create a sample work item for testing."""
    return WorkItem.create(title="Sample Work Item")

@pytest.fixture
def in_progress_work_item(sample_work_item: WorkItem) -> WorkItem:
    """Create a work item in IN_PROGRESS state."""
    sample_work_item.start()
    return sample_work_item
```

**Usage**:
```python
def test_complete_work_item(in_progress_work_item):
    """Test using fixture."""
    in_progress_work_item.complete()
    assert in_progress_work_item.status == Status.COMPLETED
```

---

### Factory Functions

**Use for**: Customizable test data.

```python
# tests/factories.py
def create_work_item(
    title: str = "Default Title",
    status: Status = Status.PENDING,
    subtasks: list[Task] | None = None,
) -> WorkItem:
    """Factory for creating work items with defaults."""
    item = WorkItem.create(title=title)

    if status == Status.IN_PROGRESS:
        item.start()
    elif status == Status.COMPLETED:
        item.start()
        item.complete()

    if subtasks:
        for task in subtasks:
            item.add_subtask(task)

    return item
```

**Usage**:
```python
def test_work_item_with_custom_data():
    item = create_work_item(title="Custom", status=Status.IN_PROGRESS)
    assert item.title == "Custom"
    assert item.status == Status.IN_PROGRESS
```

---

## Current vs Target

> Gap analysis comparing the current test suite state to the ideal described in this guide.

### Test File Distribution (Current)

Based on the actual `tests/` directory structure:

| Category | Current Files (approx.) | Target % | Current % (est.) | Status |
|----------|------------------------|----------|-------------------|--------|
| Unit | ~35 test files across `tests/unit/`, `tests/shared_kernel/`, `tests/session_management/unit/` | 60% | ~55% | Close to target |
| Integration | ~13 test files in `tests/integration/`, `tests/session_management/integration/` | 15% | ~20% | Slightly above target |
| Contract | ~3 test files in `tests/contract/` | 5% | ~5% | On target |
| Architecture | ~5 test files in `tests/architecture/`, `tests/session_management/architecture/` | 5% | ~7% | Slightly above target |
| System | ~5 test files in `tests/hooks/`, `tests/bootstrap/` | 10% | ~8% | Close to target |
| E2E | ~4 test files in `tests/e2e/`, `tests/interface/cli/integration/` | 5% | ~6% | On target |

### Coverage Status (Current)

| Metric | Target | CI Configuration | Status |
|--------|--------|-----------------|--------|
| Line Coverage | >= 90% (H-20) | `--cov-fail-under=80` in CI | Gap: CI threshold is 80%, rule says 90% |
| Branch Coverage | >= 85% | Not explicitly configured in CI | Gap: Not enforced |
| Function Coverage | >= 95% | Not explicitly configured in CI | Gap: Not enforced |

### Key Gaps

1. **Coverage threshold gap**: CI enforces 80% (`ci.yml` line 249), but H-20 requires 90%. The CI threshold should be raised to match the rule.
2. **Branch coverage not enforced**: `pyproject.toml` does not include `branch = true` in coverage configuration. Consider adding `[tool.coverage.run] branch = true`.
3. **Test markers**: `pyproject.toml` defines markers for `happy-path`, `negative`, `edge-case`, `boundary` (lines 106-111), but not all tests use these markers consistently.
4. **Coverage exclusions**: No `[tool.coverage.report] exclude_lines` configuration found in `pyproject.toml`. Should add exclusions for `TYPE_CHECKING`, `@abstractmethod`, etc.

### Recommendations

- **Short-term**: Raise CI coverage threshold to 85%, add branch coverage tracking
- **Medium-term**: Add coverage exclusion patterns, enforce marker usage on new tests
- **Long-term**: Reach 90% line coverage target, 85% branch coverage

---

## Evidence

> Verified references to actual Jerry codebase files demonstrating the testing patterns in this guide.

### Test Directory Structure -- Real Layout

```
tests/
  architecture/
    test_composition_root.py                # H-07 boundary checks
    test_config_boundaries.py               # Domain/application boundary enforcement
    test_check_architecture_boundaries.py   # Cross-module boundary checks
    test_session_hook_architecture.py        # Hook architecture compliance
  session_management/
    architecture/test_architecture.py        # Per-context architecture tests
    unit/domain/test_session.py              # Session aggregate unit tests
    unit/domain/test_project_id.py           # Value object unit tests
    unit/application/test_session_handlers.py # Handler unit tests
    integration/test_infrastructure.py        # Adapter integration tests
  shared_kernel/
    test_domain_event.py                     # DomainEvent unit tests
    test_exceptions.py                       # Exception hierarchy tests
    test_vertex_id.py                        # VertexId unit tests
    test_snowflake_id_bdd.py                 # BDD-style tests
  unit/
    application/dispatchers/test_query_dispatcher.py
    application/handlers/test_get_project_context_handler.py
    infrastructure/adapters/serialization/test_toon_serializer.py
  integration/
    test_event_sourcing_wiring.py            # Event sourcing integration
    test_filesystem_local_context_adapter.py  # Filesystem adapter integration
    test_items_commands.py                    # Work item command integration
    cli/test_cli_dispatcher_integration.py    # CLI dispatcher integration
  contract/
    test_hook_output_contract.py             # Hook output format contract
    transcript/test_chunk_schemas.py          # Transcript chunk schema contract
  e2e/
    test_config_commands.py                  # Config CLI e2e
    test_transcript_model_selection.py        # Transcript model selection e2e
```

### Architecture Testing -- Real Example

**`tests/session_management/architecture/test_architecture.py`** -- Comprehensive per-context architecture tests:
```python
# (From: tests/session_management/architecture/test_architecture.py, lines 175-219)
class TestDomainLayerArchitecture:
    def test_domain_layer_has_no_external_imports(self) -> None:
        """Domain layer MUST NOT import external (non-stdlib) packages."""
        violations = []
        for file_path in get_python_files(DOMAIN_PATH):
            external = get_external_imports(file_path)
            if external:
                rel_path = file_path.relative_to(SESSION_MGMT_ROOT)
                violations.append(f"{rel_path}: {external}")
        assert not violations, (
            "Domain layer has external imports (violates stdlib-only rule):\n"
            + "\n".join(f"  - {v}" for v in violations)
        )
```

### CI Pipeline -- Coverage Configuration

**`.github/workflows/ci.yml`** -- Coverage enforcement:
```yaml
# (From: .github/workflows/ci.yml, lines 239-251)
pytest \
  -m "not subprocess and not llm" \
  --cov=src \
  --cov-report=xml \
  --cov-report=html \
  --cov-report=term-missing \
  --cov-fail-under=80 \
  --junitxml=junit-pip-${{ matrix.python-version }}.xml \
  -v
```

### Tool Configuration -- pyproject.toml

```toml
# (From: pyproject.toml, lines 103-111)
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
markers = [
    "happy-path: marks tests as happy path scenarios",
    "negative: marks tests as negative/error scenarios",
    "edge-case: marks tests as edge case scenarios",
    "boundary: marks tests as boundary value scenarios",
]
```

### Test Dependencies

```toml
# (From: pyproject.toml, lines 46-50)
[project.optional-dependencies]
test = [
    "pytest>=8.0.0",
    "pytest-archon>=0.0.6",
    "pytest-bdd>=8.0.0",
    "pytest-cov>=4.0.0",
]
```

---

## References

### Related Documents

- [Testing Standards](../rules/testing-standards.md) - Enforcement rules (H-20)
- [Architecture Layers Guide](architecture-layers.md) - Layer responsibilities
- [Coding Practices Guide](coding-practices.md) - Mocking, fixtures

### External References

- [Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) - Martin Fowler
- [BDD](https://dannorth.net/introducing-bdd/) - Dan North
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
