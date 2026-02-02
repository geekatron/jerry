# PAT-TEST-002: BDD Red/Green/Refactor Cycle

> **Status**: MANDATORY
> **Category**: Testing Pattern
> **Location**: `tests/`

---

## Overview

The Red/Green/Refactor cycle is a disciplined approach to test-driven development. Write a failing test first (Red), write minimal code to pass (Green), then improve the code while keeping tests green (Refactor).

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Kent Beck** | "Test-Driven Development: Write a failing test before the code" |
| **Martin Fowler** | "Refactoring is improving design without changing behavior" |
| **Robert C. Martin** | "The Three Laws of TDD" |

---

## The Cycle

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

---

## Phase 1: RED

Write a test that fails for the right reason.

### Requirements

- Test MUST fail before implementation exists
- Failure should be for the right reason (not syntax error)
- Test should be minimal and focused

### Example

```python
# Step 1: Write failing test
def test_work_item_can_be_completed_when_in_progress():
    """WorkItem transitions to DONE when completed from IN_PROGRESS."""
    # Arrange
    item = WorkItem.create(id="WORK-001", title="Test Task")
    item.start()  # Transition to IN_PROGRESS

    # Act
    item.complete()  # Method doesn't exist yet!

    # Assert
    assert item.status == WorkItemStatus.DONE
```

**Run test**: `pytest tests/unit/domain/test_work_item.py::test_work_item_can_be_completed_when_in_progress`

**Expected failure**: `AttributeError: 'WorkItem' object has no attribute 'complete'`

---

## Phase 2: GREEN

Write the minimum code to make the test pass.

### Requirements

- Only enough code to pass the test
- No extra features or edge cases
- Code can be "ugly" - we'll refactor

### Example

```python
# Step 2: Minimal implementation
class WorkItem(AggregateRoot):
    def complete(self) -> None:
        """Complete the work item."""
        if self._status != WorkItemStatus.IN_PROGRESS:
            raise InvalidStateError(
                entity_type="WorkItem",
                entity_id=self._id,
                current_state=self._status.value,
                message="Can only complete from IN_PROGRESS",
            )

        self._status = WorkItemStatus.DONE
        self._raise_event(WorkItemCompleted(
            work_item_id=self._id,
            quality_passed=True,
        ))
```

**Run test**: Should pass now.

---

## Phase 3: REFACTOR

Improve code quality while keeping tests green.

### Requirements

- Tests MUST continue to pass
- Improve clarity, remove duplication
- Apply design patterns where appropriate
- Do NOT add new functionality

### Example

```python
# Step 3: Refactor to use state machine
class WorkItem(AggregateRoot):
    def complete(self, quality_passed: bool = True) -> None:
        """Complete the work item.

        Args:
            quality_passed: Whether quality gate was passed

        Raises:
            InvalidStateError: If not in completable state
        """
        self._validate_transition(WorkItemStatus.DONE)

        self._raise_event(WorkItemCompleted(
            work_item_id=self._id,
            quality_passed=quality_passed,
            completed_at=datetime.now(timezone.utc),
        ))

    def _validate_transition(self, target_status: WorkItemStatus) -> None:
        """Validate state transition is allowed."""
        if not self._status.can_transition_to(target_status):
            raise InvalidStateTransitionError(
                current_state=self._status.value,
                target_state=target_status.value,
                valid_targets=self._status.get_allowed_transitions(),
            )

    def _apply(self, event: DomainEvent) -> None:
        """Apply event to update state."""
        match event:
            case WorkItemCompleted():
                self._status = WorkItemStatus.DONE
                self._completed_at = event.completed_at
```

**Run tests**: All existing tests should still pass.

---

## Test Scenario Distribution

### Happy Path (60%)

Tests where everything works as expected.

```python
def test_create_task_when_valid_input_then_task_created():
    """Valid input creates task successfully."""
    command = CreateWorkItemCommand(title="Test Task", priority="high")
    handler = CreateWorkItemCommandHandler(repository)

    events = handler.handle(command)

    assert len(events) == 1
    assert isinstance(events[0], WorkItemCreated)
    assert events[0].title == "Test Task"
```

### Negative Cases (30%)

Tests for error conditions and validation.

```python
def test_create_task_when_empty_title_then_raises_validation_error():
    """Empty title raises ValidationError."""
    command = CreateWorkItemCommand(title="", priority="high")
    handler = CreateWorkItemCommandHandler(repository)

    with pytest.raises(ValidationError) as exc_info:
        handler.handle(command)

    assert exc_info.value.field == "title"
    assert "empty" in exc_info.value.validation_message.lower()


def test_complete_task_when_already_done_then_raises_invalid_state():
    """Cannot complete an already completed task."""
    item = WorkItem.create(id="WORK-001", title="Test")
    item.start()
    item.complete()

    with pytest.raises(InvalidStateError):
        item.complete()
```

### Edge Cases (10%)

Tests for boundary conditions.

```python
def test_create_task_when_max_length_title_then_succeeds():
    """Title at maximum length is accepted."""
    title = "x" * 200  # MAX_LENGTH = 200
    item = WorkItem.create(id="WORK-001", title=title)

    assert len(item.title) == 200


def test_create_task_when_title_exceeds_max_then_raises():
    """Title exceeding maximum is rejected."""
    title = "x" * 201

    with pytest.raises(ValidationError):
        WorkItem.create(id="WORK-001", title=title)
```

---

## Golden Rules

### 1. Never Write Code Without a Failing Test

```python
# WRONG: Writing code first
class WorkItem:
    def complete(self):
        self._status = WorkItemStatus.DONE

# CORRECT: Test first
def test_complete_transitions_to_done():
    item = ...
    item.complete()
    assert item.status == WorkItemStatus.DONE
```

### 2. One Assertion Per Test (Preferred)

```python
# ACCEPTABLE: Multiple related assertions
def test_work_item_created_event_captures_data():
    event = WorkItemCreated(work_item_id="W-1", title="Test")

    assert event.work_item_id == "W-1"
    assert event.title == "Test"
    assert event.timestamp is not None


# BETTER: Separate tests for clarity
def test_event_captures_work_item_id():
    event = WorkItemCreated(work_item_id="W-1", title="Test")
    assert event.work_item_id == "W-1"

def test_event_captures_title():
    event = WorkItemCreated(work_item_id="W-1", title="Test")
    assert event.title == "Test"
```

### 3. Refactor Only When Green

```python
# WRONG: Refactoring while red
def test_failing():
    ...  # Fails

# Now refactoring code  # NO!

# CORRECT: Get to green first
def test_passing():
    ...  # Passes

# NOW refactor code
```

---

## Test Documentation

### Docstrings

```python
def test_complete_item_when_blocked_then_raises_invalid_state():
    """Completing a blocked item raises InvalidStateError.

    Blocked items must be unblocked before completion.
    This enforces the workflow: BLOCKED -> IN_PROGRESS -> DONE
    """
    ...
```

### Test Names as Documentation

```python
# Test name should read as a specification:
def test_work_item_can_be_completed_when_in_progress(): ...
def test_work_item_cannot_be_completed_when_pending(): ...
def test_work_item_cannot_be_completed_when_already_done(): ...

# These form a readable specification:
# - Work item can be completed when in progress
# - Work item cannot be completed when pending
# - Work item cannot be completed when already done
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Follow strict RED → GREEN → REFACTOR order. Never skip steps.

> **Jerry Decision**: Test names use `test_{scenario}_when_{condition}_then_{expected}` format.

> **Jerry Decision**: Each test has an explanatory docstring.

---

## Anti-Patterns

### 1. Writing Tests After Code

```python
# WRONG: Code already written
class WorkItem:
    def complete(self): ...  # Already implemented

# Now writing test  # Test may just verify what exists, not what's needed
```

### 2. Multiple Features Per Test

```python
# WRONG: Testing multiple things
def test_work_item_lifecycle():
    item = WorkItem.create(...)
    assert item.status == PENDING  # Feature 1
    item.start()
    assert item.status == IN_PROGRESS  # Feature 2
    item.complete()
    assert item.status == DONE  # Feature 3

# CORRECT: One test per feature
def test_new_work_item_has_pending_status(): ...
def test_start_transitions_to_in_progress(): ...
def test_complete_transitions_to_done(): ...
```

### 3. Skipping Refactor Phase

```python
# WRONG: Test passes, ship it!
# (Code is messy but "works")

# CORRECT: Take time to improve
# Clean code is sustainable code
```

---

## References

- **Kent Beck**: Test-Driven Development: By Example (2002)
- **Martin Fowler**: [TDD](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
- **Robert C. Martin**: Clean Code (2008), Chapter 9
- **Design Canon**: Section 8.2 - BDD Cycle
- **Related Patterns**: PAT-TEST-001 (Test Pyramid)
