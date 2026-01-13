# PAT-VO-001: Immutable Value Object Pattern

> **Status**: MANDATORY
> **Category**: Value Object Pattern
> **Location**: `src/*/domain/value_objects/`

---

## Overview

Value Objects are immutable domain primitives that represent concepts with no identity. They are defined by their attributes, not by an identifier. Two value objects are equal if all their attributes are equal.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Eric Evans** | "Value Objects have no conceptual identity. They describe characteristics of a thing." |
| **Martin Fowler** | "Value Objects are small objects, like Money or DateRange" |
| **Vaughn Vernon** | "Value Objects should be immutable. Once created, they never change." |

---

## Jerry Implementation

### Basic Value Object

```python
# File: src/work_tracking/domain/value_objects/priority.py
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PriorityLevel(Enum):
    """Priority level enumeration."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass(frozen=True, slots=True)
class Priority:
    """Work item priority value object.

    Immutable value that represents task priority.
    Equality is based on the level value.

    Design Principles:
    - frozen=True: Makes instance immutable (assignment raises FrozenInstanceError)
    - slots=True: Memory optimization, prevents __dict__ creation
    - Value equality: Two Priority instances with same level are equal
    """

    level: PriorityLevel

    def __post_init__(self) -> None:
        """Validate on construction."""
        if not isinstance(self.level, PriorityLevel):
            raise ValueError(f"Invalid priority level: {self.level}")

    @classmethod
    def critical(cls) -> Priority:
        """Create critical priority."""
        return cls(PriorityLevel.CRITICAL)

    @classmethod
    def high(cls) -> Priority:
        """Create high priority."""
        return cls(PriorityLevel.HIGH)

    @classmethod
    def medium(cls) -> Priority:
        """Create medium priority (default)."""
        return cls(PriorityLevel.MEDIUM)

    @classmethod
    def low(cls) -> Priority:
        """Create low priority."""
        return cls(PriorityLevel.LOW)

    @classmethod
    def from_string(cls, value: str) -> Priority:
        """Create from string representation.

        Args:
            value: Priority string (e.g., "high", "MEDIUM")

        Returns:
            Priority value object

        Raises:
            ValueError: If invalid priority string
        """
        try:
            level = PriorityLevel(value.lower())
            return cls(level)
        except ValueError:
            valid = [p.value for p in PriorityLevel]
            raise ValueError(
                f"Invalid priority '{value}'. Valid: {valid}"
            )

    @property
    def value(self) -> str:
        """Get string value for serialization."""
        return self.level.value

    def is_higher_than(self, other: Priority) -> bool:
        """Compare priority (higher = more urgent).

        Priority order: critical > high > medium > low
        """
        order = [PriorityLevel.LOW, PriorityLevel.MEDIUM,
                 PriorityLevel.HIGH, PriorityLevel.CRITICAL]
        return order.index(self.level) > order.index(other.level)

    def __str__(self) -> str:
        return self.level.value

    def __repr__(self) -> str:
        return f"Priority({self.level.value})"
```

---

## String-Based Value Object

```python
# File: src/work_tracking/domain/value_objects/title.py
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Title:
    """Work item title value object.

    Encapsulates title validation rules:
    - Cannot be empty or whitespace only
    - Has maximum length constraint
    - Strips leading/trailing whitespace
    """

    MAX_LENGTH = 200

    value: str

    def __post_init__(self) -> None:
        """Validate and normalize on construction."""
        # Cannot use assignment in frozen dataclass
        # Use object.__setattr__ for initialization validation
        normalized = self.value.strip() if self.value else ""

        if not normalized:
            raise ValueError("Title cannot be empty")

        if len(normalized) > self.MAX_LENGTH:
            raise ValueError(
                f"Title exceeds maximum length of {self.MAX_LENGTH} characters"
            )

        # Set the normalized value
        object.__setattr__(self, 'value', normalized)

    def __str__(self) -> str:
        return self.value

    def __len__(self) -> int:
        return len(self.value)

    def starts_with(self, prefix: str) -> bool:
        """Check if title starts with prefix."""
        return self.value.startswith(prefix)

    def contains(self, substring: str) -> bool:
        """Check if title contains substring (case-insensitive)."""
        return substring.lower() in self.value.lower()
```

---

## Numeric Value Object

```python
# File: src/work_tracking/domain/value_objects/percentage.py
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Percentage:
    """Percentage value object (0-100).

    Represents a bounded numeric value with
    domain-specific operations.
    """

    value: float

    def __post_init__(self) -> None:
        """Validate percentage bounds."""
        if not 0 <= self.value <= 100:
            raise ValueError(
                f"Percentage must be between 0 and 100, got {self.value}"
            )

    @classmethod
    def zero(cls) -> Percentage:
        """Create 0% percentage."""
        return cls(0.0)

    @classmethod
    def complete(cls) -> Percentage:
        """Create 100% percentage."""
        return cls(100.0)

    @classmethod
    def from_fraction(cls, numerator: int, denominator: int) -> Percentage:
        """Create from fraction.

        Args:
            numerator: Completed count
            denominator: Total count

        Returns:
            Percentage value

        Example:
            Percentage.from_fraction(3, 10) -> 30%
        """
        if denominator == 0:
            return cls.zero()
        return cls((numerator / denominator) * 100)

    @property
    def is_complete(self) -> bool:
        """Check if 100%."""
        return self.value >= 100.0

    @property
    def is_zero(self) -> bool:
        """Check if 0%."""
        return self.value == 0.0

    def __str__(self) -> str:
        return f"{self.value:.1f}%"

    def __repr__(self) -> str:
        return f"Percentage({self.value})"

    def __add__(self, other: Percentage) -> Percentage:
        """Add percentages (capped at 100)."""
        return Percentage(min(100, self.value + other.value))
```

---

## Value Object Characteristics

### Immutability

```python
priority = Priority.high()

# This raises FrozenInstanceError
priority.level = PriorityLevel.LOW  # Error!

# Create new instance instead
new_priority = Priority.low()
```

### Value Equality

```python
# Same value = equal
p1 = Priority.high()
p2 = Priority.high()
assert p1 == p2  # True (same level)

# Different value = not equal
p3 = Priority.low()
assert p1 != p3  # True (different level)
```

### Self-Validation

```python
# Invalid values rejected at construction
try:
    Title("")  # Raises ValueError
except ValueError as e:
    print(e)  # "Title cannot be empty"

try:
    Percentage(150)  # Raises ValueError
except ValueError as e:
    print(e)  # "Percentage must be between 0 and 100"
```

---

## Testing Pattern

```python
def test_value_object_is_immutable():
    """Value objects cannot be modified after creation."""
    priority = Priority.high()

    with pytest.raises(FrozenInstanceError):
        priority.level = PriorityLevel.LOW


def test_value_objects_with_same_value_are_equal():
    """Value equality based on attributes."""
    p1 = Priority.high()
    p2 = Priority.high()

    assert p1 == p2
    assert hash(p1) == hash(p2)  # Can be used in sets/dicts


def test_value_object_validates_on_construction():
    """Invalid values rejected at creation."""
    with pytest.raises(ValueError) as exc_info:
        Title("")

    assert "empty" in str(exc_info.value).lower()


def test_value_object_factory_methods():
    """Factory methods create valid instances."""
    critical = Priority.critical()
    high = Priority.high()

    assert critical.level == PriorityLevel.CRITICAL
    assert critical.is_higher_than(high)


def test_value_object_from_string():
    """String parsing creates valid value object."""
    priority = Priority.from_string("HIGH")

    assert priority.level == PriorityLevel.HIGH


def test_value_object_serialization():
    """Value can be extracted for serialization."""
    priority = Priority.high()

    assert priority.value == "high"
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: All value objects use `@dataclass(frozen=True, slots=True)` for immutability and memory efficiency.

> **Jerry Decision**: Value objects provide `from_string` class methods for deserialization from external input.

> **Jerry Decision**: Value objects have a `.value` property for serialization to primitive types.

---

## Anti-Patterns

### 1. Mutable Value Object

```python
# WRONG: Not frozen
@dataclass
class Priority:
    level: str  # Can be changed!

# CORRECT: Frozen
@dataclass(frozen=True, slots=True)
class Priority:
    level: PriorityLevel
```

### 2. Identity in Value Object

```python
# WRONG: Value object with ID
@dataclass(frozen=True)
class Money:
    id: str  # Value objects have no identity!
    amount: Decimal
    currency: str

# CORRECT: Pure value
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str
```

### 3. External Dependencies

```python
# WRONG: Value object calls service
@dataclass(frozen=True)
class Priority:
    level: str

    def get_sla(self, sla_service: SLAService):  # External dependency!
        return sla_service.get_sla_for(self.level)

# CORRECT: Value object is pure
@dataclass(frozen=True)
class Priority:
    level: PriorityLevel

    @property
    def default_sla_hours(self) -> int:
        """Return default SLA based on level."""
        sla_map = {
            PriorityLevel.CRITICAL: 4,
            PriorityLevel.HIGH: 24,
            PriorityLevel.MEDIUM: 72,
            PriorityLevel.LOW: 168,
        }
        return sla_map[self.level]
```

---

## References

- **Eric Evans**: Domain-Driven Design (2003), Chapter 5 - Value Objects
- **Martin Fowler**: [Value Object](https://martinfowler.com/bliki/ValueObject.html)
- **Vaughn Vernon**: Implementing DDD (2013), Chapter 6
- **Design Canon**: Section 4.2 - Value Objects
- **Related Patterns**: PAT-VO-002 (Enum Value Object), PAT-VO-003 (Composite Value Object)
