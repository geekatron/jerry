# PAT-VO-002: Enum Value Object Pattern

> **Status**: MANDATORY
> **Category**: Value Object Pattern
> **Location**: `src/*/domain/value_objects/`

---

## Overview

Enum Value Objects represent a fixed set of domain-specific values. They combine Python's Enum type safety with value object semantics, providing type-safe, self-documenting domain concepts.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Eric Evans** | "Enumeration-like value objects represent a small, fixed set of values" |
| **Martin Fowler** | "Enum types prevent invalid values at compile time" |
| **Joshua Bloch** | "Use enums instead of int constants for type safety" |

---

## Jerry Implementation

### Status Enum

```python
# File: src/work_tracking/domain/value_objects/work_item_status.py
from __future__ import annotations

from enum import Enum, auto


class WorkItemStatus(Enum):
    """Work item lifecycle status.

    Represents the current state of a work item in its lifecycle.
    Each status has allowed transitions defined by the state machine.

    Design Notes:
    - Enum provides type safety (no invalid status strings)
    - String values for serialization/display
    - Class methods for state machine transitions
    """

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    DONE = "done"
    CANCELLED = "cancelled"

    @classmethod
    def initial(cls) -> WorkItemStatus:
        """Return the initial status for new work items."""
        return cls.PENDING

    @classmethod
    def terminal_states(cls) -> set[WorkItemStatus]:
        """Return statuses that cannot transition to other states."""
        return {cls.DONE, cls.CANCELLED}

    @classmethod
    def active_states(cls) -> set[WorkItemStatus]:
        """Return statuses representing active work."""
        return {cls.PENDING, cls.IN_PROGRESS, cls.BLOCKED}

    @property
    def is_terminal(self) -> bool:
        """Check if this is a terminal (final) state."""
        return self in self.terminal_states()

    @property
    def is_active(self) -> bool:
        """Check if this represents active work."""
        return self in self.active_states()

    def can_transition_to(self, target: WorkItemStatus) -> bool:
        """Check if transition to target status is allowed.

        State Machine:
            PENDING -> IN_PROGRESS, CANCELLED
            IN_PROGRESS -> BLOCKED, DONE, CANCELLED
            BLOCKED -> IN_PROGRESS, CANCELLED
            DONE -> (terminal)
            CANCELLED -> (terminal)

        Args:
            target: Target status to transition to

        Returns:
            True if transition is allowed
        """
        transitions = {
            WorkItemStatus.PENDING: {
                WorkItemStatus.IN_PROGRESS,
                WorkItemStatus.CANCELLED,
            },
            WorkItemStatus.IN_PROGRESS: {
                WorkItemStatus.BLOCKED,
                WorkItemStatus.DONE,
                WorkItemStatus.CANCELLED,
            },
            WorkItemStatus.BLOCKED: {
                WorkItemStatus.IN_PROGRESS,
                WorkItemStatus.CANCELLED,
            },
            WorkItemStatus.DONE: set(),  # Terminal
            WorkItemStatus.CANCELLED: set(),  # Terminal
        }
        return target in transitions.get(self, set())

    def get_allowed_transitions(self) -> set[WorkItemStatus]:
        """Get all statuses this can transition to."""
        transitions = {
            WorkItemStatus.PENDING: {
                WorkItemStatus.IN_PROGRESS,
                WorkItemStatus.CANCELLED,
            },
            WorkItemStatus.IN_PROGRESS: {
                WorkItemStatus.BLOCKED,
                WorkItemStatus.DONE,
                WorkItemStatus.CANCELLED,
            },
            WorkItemStatus.BLOCKED: {
                WorkItemStatus.IN_PROGRESS,
                WorkItemStatus.CANCELLED,
            },
            WorkItemStatus.DONE: set(),
            WorkItemStatus.CANCELLED: set(),
        }
        return transitions.get(self, set())

    def __str__(self) -> str:
        return self.value
```

---

### Work Type Enum

```python
# File: src/work_tracking/domain/value_objects/work_type.py
from __future__ import annotations

from enum import Enum


class WorkType(Enum):
    """Type of work item.

    Classifies work items by their nature and granularity.
    Each type has semantic meaning for planning and tracking.
    """

    # High-level groupings
    EPIC = "epic"
    INITIATIVE = "initiative"

    # Standard work
    TASK = "task"
    SUBTASK = "subtask"

    # Specialized work
    BUG = "bug"
    TECH_DEBT = "tech_debt"
    SPIKE = "spike"
    DISCOVERY = "discovery"

    @classmethod
    def hierarchical_types(cls) -> set[WorkType]:
        """Types that can contain other work items."""
        return {cls.EPIC, cls.INITIATIVE, cls.TASK}

    @classmethod
    def leaf_types(cls) -> set[WorkType]:
        """Types that cannot contain children."""
        return {cls.SUBTASK}

    @property
    def can_have_children(self) -> bool:
        """Check if this type can contain child work items."""
        return self in self.hierarchical_types()

    @property
    def can_have_subtasks(self) -> bool:
        """Check if this type can have subtasks."""
        return self in {WorkType.TASK, WorkType.BUG, WorkType.TECH_DEBT}

    @property
    def default_priority(self) -> str:
        """Get default priority for this work type."""
        priority_map = {
            WorkType.EPIC: "high",
            WorkType.INITIATIVE: "high",
            WorkType.BUG: "high",
            WorkType.TASK: "medium",
            WorkType.SUBTASK: "medium",
            WorkType.TECH_DEBT: "low",
            WorkType.SPIKE: "medium",
            WorkType.DISCOVERY: "low",
        }
        return priority_map.get(self, "medium")

    @classmethod
    def from_string(cls, value: str) -> WorkType:
        """Parse work type from string.

        Args:
            value: Work type string (case-insensitive)

        Returns:
            WorkType enum value

        Raises:
            ValueError: If invalid work type
        """
        try:
            return cls(value.lower())
        except ValueError:
            valid = [t.value for t in cls]
            raise ValueError(
                f"Invalid work type '{value}'. Valid types: {valid}"
            )

    def __str__(self) -> str:
        return self.value
```

---

### Phase Status Enum

```python
# File: src/work_tracking/domain/value_objects/phase_status.py
from enum import Enum


class PhaseStatus(Enum):
    """Project phase status.

    Tracks the lifecycle of project phases.
    """

    DRAFT = "draft"
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETE = "complete"
    ARCHIVED = "archived"

    @property
    def is_editable(self) -> bool:
        """Check if phase can be modified."""
        return self in {PhaseStatus.DRAFT, PhaseStatus.PLANNED, PhaseStatus.ACTIVE}

    @property
    def is_active(self) -> bool:
        """Check if phase is currently active."""
        return self == PhaseStatus.ACTIVE

    def __str__(self) -> str:
        return self.value
```

---

## Enum with Auto Values

```python
# For internal-only enums where string value doesn't matter
from enum import Enum, auto


class ProcessingState(Enum):
    """Internal processing state (not persisted)."""

    IDLE = auto()
    LOADING = auto()
    PROCESSING = auto()
    SAVING = auto()
    ERROR = auto()
```

---

## Enum Pattern Benefits

### Type Safety

```python
def set_status(self, status: WorkItemStatus) -> None:
    """Type checker ensures only valid status values."""
    self._status = status

# Type error caught at development time
set_status("invalid")  # Type error: expected WorkItemStatus
```

### Exhaustive Matching

```python
def get_status_color(status: WorkItemStatus) -> str:
    """Match must handle all cases."""
    match status:
        case WorkItemStatus.PENDING:
            return "gray"
        case WorkItemStatus.IN_PROGRESS:
            return "blue"
        case WorkItemStatus.BLOCKED:
            return "red"
        case WorkItemStatus.DONE:
            return "green"
        case WorkItemStatus.CANCELLED:
            return "gray"
    # Type checker warns if case missing
```

### Self-Documenting

```python
# Clear intent
status = WorkItemStatus.IN_PROGRESS

# vs magic string
status = "in_progress"  # What values are valid?
```

---

## Testing Pattern

```python
def test_enum_has_expected_values():
    """Enum contains all expected values."""
    assert WorkItemStatus.PENDING.value == "pending"
    assert WorkItemStatus.DONE.value == "done"


def test_enum_state_machine_transitions():
    """State machine allows valid transitions."""
    pending = WorkItemStatus.PENDING

    assert pending.can_transition_to(WorkItemStatus.IN_PROGRESS)
    assert pending.can_transition_to(WorkItemStatus.CANCELLED)
    assert not pending.can_transition_to(WorkItemStatus.DONE)


def test_terminal_states_have_no_transitions():
    """Terminal states cannot transition."""
    done = WorkItemStatus.DONE
    cancelled = WorkItemStatus.CANCELLED

    assert len(done.get_allowed_transitions()) == 0
    assert len(cancelled.get_allowed_transitions()) == 0
    assert done.is_terminal
    assert cancelled.is_terminal


def test_enum_from_string_parsing():
    """Enum parses from string correctly."""
    work_type = WorkType.from_string("TASK")
    assert work_type == WorkType.TASK

    work_type = WorkType.from_string("bug")
    assert work_type == WorkType.BUG


def test_enum_from_string_invalid_raises():
    """Invalid string raises ValueError."""
    with pytest.raises(ValueError) as exc_info:
        WorkType.from_string("invalid")

    assert "invalid" in str(exc_info.value).lower()
```

---

## Serialization

```python
# To string (for JSON/storage)
status = WorkItemStatus.IN_PROGRESS
json_value = status.value  # "in_progress"

# From string (deserialization)
status = WorkItemStatus(json_value)  # WorkItemStatus.IN_PROGRESS

# Or use factory method with validation
status = WorkType.from_string(user_input)
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Enum value objects use string values for human-readable serialization.

> **Jerry Decision**: State machine logic (transitions) is embedded in the enum class itself.

> **Jerry Decision**: Each enum provides `from_string` class method for safe deserialization with error messages.

---

## Anti-Patterns

### 1. String Instead of Enum

```python
# WRONG: Magic strings
class WorkItem:
    def __init__(self):
        self.status = "pending"  # What values are valid?

    def complete(self):
        self.status = "done"  # Typo risk!

# CORRECT: Type-safe enum
class WorkItem:
    def __init__(self):
        self._status = WorkItemStatus.PENDING

    def complete(self):
        self._status = WorkItemStatus.DONE
```

### 2. Logic Outside Enum

```python
# WRONG: Transition logic scattered
def can_start(status: WorkItemStatus) -> bool:
    return status == WorkItemStatus.PENDING

def can_complete(status: WorkItemStatus) -> bool:
    return status == WorkItemStatus.IN_PROGRESS

# CORRECT: Transition logic in enum
class WorkItemStatus(Enum):
    def can_transition_to(self, target: WorkItemStatus) -> bool:
        # All transition logic in one place
        ...
```

---

## References

- **Eric Evans**: Domain-Driven Design (2003)
- **Python Docs**: [Enum](https://docs.python.org/3/library/enum.html)
- **Design Canon**: Section 4.2.2 - Enum Value Objects
- **Related Patterns**: PAT-VO-001 (Immutable Value Object), PAT-AGG-001 (State Machine)
