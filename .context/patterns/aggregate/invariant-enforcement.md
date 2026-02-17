# PAT-AGG-004: Invariant Enforcement Pattern

> **Status**: MANDATORY
> **Category**: Aggregate Pattern
> **Location**: All aggregate methods

---

## Overview

Invariant Enforcement ensures that aggregates protect their business rules. An aggregate should never be in an invalid state - all invariants are checked and enforced within the aggregate itself.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Eric Evans** (DDD) | "Invariants are consistency rules that must be maintained whenever data changes" |
| **Bertrand Meyer** | "Design by Contract - preconditions, postconditions, and invariants" |
| **Vaughn Vernon** | "Aggregates are consistency boundaries; they enforce their own invariants" |

---

## Jerry Implementation

### Invariant Categories

| Category | Example | When Checked |
|----------|---------|--------------|
| **Creation** | Title cannot be empty | In factory method |
| **State Transition** | Can only complete from in_progress | In behavior method |
| **Business Rule** | Cannot have circular dependencies | In add_dependency |
| **Relationship** | Parent must exist before child | In domain service |

---

## Pattern Structure

```python
class WorkItem(AggregateRoot):
    """Work item with enforced invariants.

    Invariants:
    1. Title cannot be empty
    2. Status transitions must follow state machine
    3. Completed items cannot be modified
    4. Dependencies cannot be circular
    5. Quality gate must pass for completion
    """

    @classmethod
    def create(
        cls,
        id: str,
        title: str,
        **kwargs,
    ) -> WorkItem:
        """Factory with creation invariants."""
        # INVARIANT 1: Title cannot be empty
        if not title.strip():
            raise ValidationError(
                field="title",
                message="Title cannot be empty",
            )

        # Factory logic...
        item = cls.__new__(cls)
        item._initialize(id=id)
        item._raise_event(WorkItemCreated(...))
        return item

    def start(self) -> None:
        """Start work with transition invariant."""
        # INVARIANT 2: Valid state transition
        self._status.validate_transition(WorkItemStatus.IN_PROGRESS)

        self._raise_event(StatusChanged(...))

    def update_title(self, new_title: str) -> None:
        """Update title with modification invariant."""
        # INVARIANT 3: Cannot modify completed items
        if self._status.is_terminal:
            raise InvalidStateError(
                entity_type="WorkItem",
                entity_id=self._id,
                current_state=self._status.value,
                message="Cannot modify completed/cancelled work item",
            )

        # INVARIANT 1: New title cannot be empty
        if not new_title.strip():
            raise ValidationError(
                field="title",
                message="Title cannot be empty",
            )

        self._raise_event(TitleUpdated(...))

    def add_dependency(self, dependency_id: str) -> None:
        """Add dependency with relationship invariant."""
        # INVARIANT 4: Cannot depend on self
        if dependency_id == self._id:
            raise InvariantViolationError(
                invariant="no_self_dependency",
                message="Work item cannot depend on itself",
            )

        # INVARIANT 4: No duplicate dependencies
        if dependency_id in self._dependencies:
            raise InvariantViolationError(
                invariant="no_duplicate_dependency",
                message=f"Dependency {dependency_id} already exists",
            )

        self._raise_event(DependencyAdded(...))

    def complete(self, quality_passed: bool = True) -> None:
        """Complete with quality invariant."""
        # INVARIANT 2: Valid state transition
        self._status.validate_transition(WorkItemStatus.DONE)

        # INVARIANT 5: Quality gate must pass
        if not quality_passed:
            raise QualityGateError(
                work_item_id=self._id,
                message="Quality gate validation failed",
            )

        self._raise_event(WorkItemCompleted(...))
```

---

## Value Object Validation

Value objects enforce invariants at construction:

```python
@dataclass(frozen=True)
class Priority:
    """Priority value with validation invariant."""

    value: int

    def __post_init__(self) -> None:
        """Enforce value range invariant."""
        if not 1 <= self.value <= 4:
            raise ValidationError(
                field="priority",
                message=f"Priority must be 1-4, got {self.value}",
            )

    @classmethod
    def from_string(cls, value: str) -> Priority:
        """Factory with format invariant."""
        mapping = {
            "critical": 1,
            "high": 2,
            "medium": 3,
            "low": 4,
        }
        if value.lower() not in mapping:
            raise ValidationError(
                field="priority",
                message=f"Invalid priority: {value}",
            )
        return cls(mapping[value.lower()])
```

---

## State Machine Invariants

```python
class WorkItemStatus(Enum):
    """Status with state machine invariant."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    DONE = "done"
    CANCELLED = "cancelled"

    _VALID_TRANSITIONS = {
        "pending": {"in_progress", "cancelled"},
        "in_progress": {"blocked", "done", "cancelled"},
        "blocked": {"in_progress", "cancelled"},
        "done": {"in_progress"},  # Can reopen
        "cancelled": set(),  # Terminal
    }

    def can_transition_to(self, target: WorkItemStatus) -> bool:
        """Check if transition is valid."""
        return target.value in self._VALID_TRANSITIONS.get(self.value, set())

    def validate_transition(self, target: WorkItemStatus) -> None:
        """Raise if transition is invalid."""
        if not self.can_transition_to(target):
            raise InvalidStateTransitionError(
                current_state=self.value,
                target_state=target.value,
                valid_targets=self._VALID_TRANSITIONS.get(self.value, set()),
            )
```

---

## Exception Hierarchy

```python
# File: src/shared_kernel/exceptions.py

class DomainError(Exception):
    """Base for all domain errors."""
    pass

class ValidationError(DomainError):
    """Field validation failed."""
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(f"Validation failed for {field}: {message}")

class InvalidStateError(DomainError):
    """Operation invalid for current state."""
    def __init__(
        self,
        entity_type: str,
        entity_id: str,
        current_state: str,
        message: str,
    ) -> None:
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.current_state = current_state
        super().__init__(message)

class InvalidStateTransitionError(InvalidStateError):
    """State transition not allowed."""
    def __init__(
        self,
        current_state: str,
        target_state: str,
        valid_targets: set[str],
    ) -> None:
        self.target_state = target_state
        self.valid_targets = valid_targets
        super().__init__(
            entity_type="Status",
            entity_id="",
            current_state=current_state,
            message=(
                f"Cannot transition from {current_state} to {target_state}. "
                f"Valid targets: {valid_targets}"
            ),
        )

class InvariantViolationError(DomainError):
    """Business invariant violated."""
    def __init__(self, invariant: str, message: str) -> None:
        self.invariant = invariant
        super().__init__(f"Invariant '{invariant}' violated: {message}")

class QualityGateError(DomainError):
    """Quality gate check failed."""
    def __init__(self, work_item_id: str, message: str) -> None:
        self.work_item_id = work_item_id
        super().__init__(message)
```

---

## Testing Pattern

```python
def test_create_rejects_empty_title():
    """Creation invariant: title cannot be empty."""
    with pytest.raises(ValidationError) as exc_info:
        WorkItem.create(id="WORK-001", title="")

    assert exc_info.value.field == "title"
    assert "empty" in exc_info.value.message.lower()


def test_cannot_complete_from_pending():
    """State machine invariant: must be in_progress to complete."""
    item = WorkItem.create(id="WORK-001", title="Test")
    # Status is PENDING

    with pytest.raises(InvalidStateTransitionError) as exc_info:
        item.complete()

    assert exc_info.value.current_state == "pending"
    assert exc_info.value.target_state == "done"


def test_cannot_modify_completed_item():
    """Modification invariant: terminal items are read-only."""
    item = WorkItem.create(id="WORK-001", title="Test")
    item.start()
    item.complete()

    with pytest.raises(InvalidStateError) as exc_info:
        item.update_title("New Title")

    assert "completed" in exc_info.value.message.lower()


def test_cannot_add_self_dependency():
    """Relationship invariant: no self-references."""
    item = WorkItem.create(id="WORK-001", title="Test")

    with pytest.raises(InvariantViolationError) as exc_info:
        item.add_dependency("WORK-001")

    assert exc_info.value.invariant == "no_self_dependency"


def test_quality_gate_required_for_completion():
    """Quality invariant: must pass quality check."""
    item = WorkItem.create(id="WORK-001", title="Test")
    item.start()

    with pytest.raises(QualityGateError):
        item.complete(quality_passed=False)
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: All invariant violations raise specific exceptions, never generic `ValueError` or `Exception`. This enables precise error handling.

> **Jerry Decision**: State machine transitions are validated in value objects (WorkItemStatus), not in aggregate methods. This centralizes transition logic.

> **Jerry Decision**: Quality gate is enforced at completion time, not as a separate validation step. This ensures quality is always checked.

---

## Anti-Patterns

### 1. External Invariant Checking

```python
# WRONG: Caller checks invariant
if work_item.status == "pending":
    work_item.start()

# CORRECT: Aggregate enforces internally
work_item.start()  # Raises if invalid
```

### 2. Setter Methods

```python
# WRONG: Public setter bypasses invariants
class WorkItem:
    def set_status(self, status: str) -> None:
        self._status = status  # No validation!

# CORRECT: Behavior method with validation
class WorkItem:
    def start(self) -> None:
        self._status.validate_transition(WorkItemStatus.IN_PROGRESS)
        self._raise_event(StatusChanged(...))
```

### 3. Generic Exceptions

```python
# WRONG: Generic exception
if not title:
    raise Exception("Title required")

# CORRECT: Specific domain exception
if not title:
    raise ValidationError(field="title", message="Title cannot be empty")
```

---

## References

- **Eric Evans**: Domain-Driven Design (2003), Chapter 6 - Invariants
- **Bertrand Meyer**: Object-Oriented Software Construction - Design by Contract
- **Vaughn Vernon**: Implementing DDD (2013), Aggregate Invariants
- **Design Canon**: Section 5.4 - Invariant Enforcement
- **Related Patterns**: PAT-VO-002 (State Machine), PAT-ENT-003 (AggregateRoot)
