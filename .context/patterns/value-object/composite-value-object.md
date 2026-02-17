# PAT-VO-003: Composite Value Object Pattern

> **Status**: RECOMMENDED
> **Category**: Value Object Pattern
> **Location**: `src/*/domain/value_objects/`

---

## Overview

Composite Value Objects combine multiple related attributes into a single cohesive concept. They encapsulate validation and behavior for complex domain values that consist of multiple parts working together.

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Eric Evans** | "Group related attributes that commonly change together into Value Objects" |
| **Martin Fowler** | "Replace Data Clump with a Value Object" |
| **Vaughn Vernon** | "Value Objects model whole values, not fragments" |

---

## Jerry Implementation

### DateRange Value Object

```python
# File: src/work_tracking/domain/value_objects/date_range.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass(frozen=True, slots=True)
class DateRange:
    """Date range value object.

    Represents a time period with start and optional end.
    Encapsulates date range validation and operations.

    Invariants:
    - Start date is required
    - End date (if present) must be >= start date
    - All dates are UTC
    """

    start: datetime
    end: datetime | None = None

    def __post_init__(self) -> None:
        """Validate date range invariants."""
        if self.end is not None and self.end < self.start:
            raise ValueError(
                f"End date ({self.end}) cannot be before start date ({self.start})"
            )

        # Ensure UTC timezone
        if self.start.tzinfo is None:
            object.__setattr__(
                self,
                'start',
                self.start.replace(tzinfo=timezone.utc)
            )

        if self.end is not None and self.end.tzinfo is None:
            object.__setattr__(
                self,
                'end',
                self.end.replace(tzinfo=timezone.utc)
            )

    @classmethod
    def starting_now(cls) -> DateRange:
        """Create range starting now with no end."""
        return cls(start=datetime.now(timezone.utc))

    @classmethod
    def for_days(cls, days: int, start: datetime | None = None) -> DateRange:
        """Create range for specified number of days.

        Args:
            days: Duration in days
            start: Start date (defaults to now)

        Returns:
            DateRange spanning the specified days
        """
        start_date = start or datetime.now(timezone.utc)
        end_date = start_date + timedelta(days=days)
        return cls(start=start_date, end=end_date)

    @property
    def is_open(self) -> bool:
        """Check if range has no end date."""
        return self.end is None

    @property
    def is_closed(self) -> bool:
        """Check if range has both start and end."""
        return self.end is not None

    @property
    def duration(self) -> timedelta | None:
        """Get duration if range is closed."""
        if self.end is None:
            return None
        return self.end - self.start

    @property
    def days(self) -> int | None:
        """Get duration in days if range is closed."""
        duration = self.duration
        return duration.days if duration else None

    def contains(self, date: datetime) -> bool:
        """Check if date falls within range.

        Args:
            date: Date to check

        Returns:
            True if date is within range (inclusive)
        """
        if date < self.start:
            return False
        if self.end is not None and date > self.end:
            return False
        return True

    def overlaps(self, other: DateRange) -> bool:
        """Check if this range overlaps with another.

        Args:
            other: Another date range

        Returns:
            True if ranges overlap
        """
        # If either is open-ended, check start overlap
        if self.end is None and other.end is None:
            return True  # Both open = always overlap from some point

        if self.end is None:
            return other.end >= self.start

        if other.end is None:
            return self.end >= other.start

        # Both closed: check for overlap
        return self.start <= other.end and other.start <= self.end

    def with_end(self, end: datetime) -> DateRange:
        """Create new range with specified end date.

        Args:
            end: New end date

        Returns:
            New DateRange with updated end
        """
        return DateRange(start=self.start, end=end)

    def extend_by(self, days: int) -> DateRange:
        """Create new range extended by days.

        Args:
            days: Days to extend (can be negative)

        Returns:
            New DateRange with extended end
        """
        if self.end is None:
            raise ValueError("Cannot extend open-ended range")
        return DateRange(start=self.start, end=self.end + timedelta(days=days))

    def __str__(self) -> str:
        if self.end is None:
            return f"{self.start.date()} - ongoing"
        return f"{self.start.date()} - {self.end.date()}"
```

---

### Address Value Object

```python
# File: src/shared_kernel/domain/value_objects/address.py
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Address:
    """Physical address value object.

    Encapsulates address validation and formatting.
    All components must be present for a valid address.
    """

    street: str
    city: str
    state: str
    postal_code: str
    country: str = "USA"

    def __post_init__(self) -> None:
        """Validate all required fields are present."""
        if not self.street.strip():
            raise ValueError("Street is required")
        if not self.city.strip():
            raise ValueError("City is required")
        if not self.state.strip():
            raise ValueError("State is required")
        if not self.postal_code.strip():
            raise ValueError("Postal code is required")

    @property
    def single_line(self) -> str:
        """Format as single line."""
        return f"{self.street}, {self.city}, {self.state} {self.postal_code}, {self.country}"

    @property
    def multiline(self) -> str:
        """Format as multiple lines."""
        return f"{self.street}\n{self.city}, {self.state} {self.postal_code}\n{self.country}"

    def is_same_city(self, other: Address) -> bool:
        """Check if same city."""
        return (
            self.city.lower() == other.city.lower()
            and self.state.lower() == other.state.lower()
        )
```

---

### Money Value Object

```python
# File: src/shared_kernel/domain/value_objects/money.py
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True, slots=True)
class Money:
    """Money value object with currency.

    Represents monetary amounts with precise decimal handling.

    Invariants:
    - Amount cannot be negative
    - Currency is required
    - Operations require matching currencies
    """

    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        """Validate money value."""
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")
        if not self.currency:
            raise ValueError("Currency is required")

        # Normalize currency to uppercase
        object.__setattr__(self, 'currency', self.currency.upper())

    @classmethod
    def usd(cls, amount: float | Decimal | str) -> Money:
        """Create USD money value."""
        return cls(amount=Decimal(str(amount)), currency="USD")

    @classmethod
    def zero(cls, currency: str) -> Money:
        """Create zero amount in currency."""
        return cls(amount=Decimal("0"), currency=currency)

    def add(self, other: Money) -> Money:
        """Add two money values.

        Args:
            other: Money to add

        Returns:
            New Money with sum

        Raises:
            ValueError: If currencies don't match
        """
        self._ensure_same_currency(other)
        return Money(
            amount=self.amount + other.amount,
            currency=self.currency,
        )

    def subtract(self, other: Money) -> Money:
        """Subtract money value.

        Args:
            other: Money to subtract

        Returns:
            New Money with difference

        Raises:
            ValueError: If currencies don't match or result negative
        """
        self._ensure_same_currency(other)
        result = self.amount - other.amount
        if result < 0:
            raise ValueError("Subtraction would result in negative amount")
        return Money(amount=result, currency=self.currency)

    def multiply(self, factor: Decimal | int | float) -> Money:
        """Multiply by factor.

        Args:
            factor: Multiplication factor

        Returns:
            New Money with product
        """
        result = self.amount * Decimal(str(factor))
        # Round to 2 decimal places for money
        result = result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return Money(amount=result, currency=self.currency)

    @property
    def is_zero(self) -> bool:
        """Check if amount is zero."""
        return self.amount == 0

    def _ensure_same_currency(self, other: Money) -> None:
        """Ensure currencies match for operations."""
        if self.currency != other.currency:
            raise ValueError(
                f"Currency mismatch: {self.currency} vs {other.currency}"
            )

    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"

    def __repr__(self) -> str:
        return f"Money({self.amount}, '{self.currency}')"

    def __add__(self, other: Money) -> Money:
        return self.add(other)

    def __sub__(self, other: Money) -> Money:
        return self.subtract(other)

    def __mul__(self, factor: Decimal | int | float) -> Money:
        return self.multiply(factor)
```

---

### QualityMetrics Value Object

```python
# File: src/work_tracking/domain/value_objects/quality_metrics.py
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class QualityMetrics:
    """Quality gate metrics composite value.

    Encapsulates multiple quality measurements for a work item.
    Used in quality gate checks before completion.
    """

    test_coverage: float  # 0.0 to 1.0
    documentation_complete: bool
    code_reviewed: bool
    acceptance_criteria_met: bool

    def __post_init__(self) -> None:
        """Validate metrics."""
        if not 0.0 <= self.test_coverage <= 1.0:
            raise ValueError(
                f"Test coverage must be between 0 and 1, got {self.test_coverage}"
            )

    @classmethod
    def incomplete(cls) -> QualityMetrics:
        """Create incomplete/default metrics."""
        return cls(
            test_coverage=0.0,
            documentation_complete=False,
            code_reviewed=False,
            acceptance_criteria_met=False,
        )

    @classmethod
    def fully_passing(cls, test_coverage: float = 0.8) -> QualityMetrics:
        """Create fully passing metrics."""
        return cls(
            test_coverage=test_coverage,
            documentation_complete=True,
            code_reviewed=True,
            acceptance_criteria_met=True,
        )

    @property
    def test_coverage_percentage(self) -> float:
        """Get test coverage as percentage."""
        return self.test_coverage * 100

    def passes_gate(self, required_coverage: float = 0.8) -> bool:
        """Check if metrics pass quality gate.

        Args:
            required_coverage: Minimum test coverage (0.0 to 1.0)

        Returns:
            True if all quality criteria met
        """
        return (
            self.test_coverage >= required_coverage
            and self.documentation_complete
            and self.code_reviewed
            and self.acceptance_criteria_met
        )

    def get_failures(self, required_coverage: float = 0.8) -> list[str]:
        """Get list of failing quality criteria.

        Args:
            required_coverage: Minimum test coverage

        Returns:
            List of failure descriptions
        """
        failures = []

        if self.test_coverage < required_coverage:
            failures.append(
                f"Test coverage {self.test_coverage_percentage:.1f}% "
                f"below required {required_coverage * 100:.1f}%"
            )

        if not self.documentation_complete:
            failures.append("Documentation incomplete")

        if not self.code_reviewed:
            failures.append("Code review not completed")

        if not self.acceptance_criteria_met:
            failures.append("Acceptance criteria not met")

        return failures

    def with_coverage(self, coverage: float) -> QualityMetrics:
        """Create new metrics with updated coverage."""
        return QualityMetrics(
            test_coverage=coverage,
            documentation_complete=self.documentation_complete,
            code_reviewed=self.code_reviewed,
            acceptance_criteria_met=self.acceptance_criteria_met,
        )

    def with_review_completed(self) -> QualityMetrics:
        """Create new metrics with code review marked complete."""
        return QualityMetrics(
            test_coverage=self.test_coverage,
            documentation_complete=self.documentation_complete,
            code_reviewed=True,
            acceptance_criteria_met=self.acceptance_criteria_met,
        )
```

---

## Testing Pattern

```python
def test_date_range_validates_start_before_end():
    """Date range rejects invalid range."""
    start = datetime(2026, 1, 15)
    end = datetime(2026, 1, 10)  # Before start!

    with pytest.raises(ValueError) as exc_info:
        DateRange(start=start, end=end)

    assert "before" in str(exc_info.value).lower()


def test_date_range_contains():
    """Date range containment check."""
    range = DateRange(
        start=datetime(2026, 1, 1),
        end=datetime(2026, 1, 31),
    )

    assert range.contains(datetime(2026, 1, 15))
    assert not range.contains(datetime(2026, 2, 15))


def test_money_requires_same_currency():
    """Money operations require matching currencies."""
    usd = Money.usd(100)
    eur = Money(Decimal("50"), "EUR")

    with pytest.raises(ValueError) as exc_info:
        usd.add(eur)

    assert "currency" in str(exc_info.value).lower()


def test_money_arithmetic():
    """Money supports arithmetic operations."""
    m1 = Money.usd(100)
    m2 = Money.usd(50)

    assert (m1 + m2).amount == Decimal("150")
    assert (m1 - m2).amount == Decimal("50")
    assert (m1 * 2).amount == Decimal("200")


def test_quality_metrics_gate_check():
    """Quality metrics gate validation."""
    passing = QualityMetrics.fully_passing(test_coverage=0.9)
    failing = QualityMetrics.incomplete()

    assert passing.passes_gate(required_coverage=0.8)
    assert not failing.passes_gate()
    assert len(failing.get_failures()) == 4
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Composite value objects provide factory methods for common creation patterns.

> **Jerry Decision**: Value objects that can be partially updated provide `with_*` methods that return new instances.

> **Jerry Decision**: Quality metrics use 0.0-1.0 scale internally, percentage conversion via property.

---

## Anti-Patterns

### 1. Data Clump Without Value Object

```python
# WRONG: Related data as separate parameters
def schedule_work(
    start_date: datetime,
    end_date: datetime,
    start_time: time,
    end_time: time,
) -> None:
    ...

# CORRECT: Composite value object
def schedule_work(time_slot: TimeSlot) -> None:
    ...
```

### 2. Mutable Composite

```python
# WRONG: Mutable composite
class DateRange:
    def extend(self, days: int) -> None:
        self.end += timedelta(days=days)  # Mutation!

# CORRECT: Immutable with new instance
class DateRange:
    def extend_by(self, days: int) -> DateRange:
        return DateRange(start=self.start, end=self.end + timedelta(days=days))
```

---

## References

- **Eric Evans**: Domain-Driven Design (2003), Chapter 5
- **Martin Fowler**: [Replace Data Clump](https://refactoring.guru/smells/data-clumps)
- **Design Canon**: Section 4.2.3 - Composite Value Objects
- **Related Patterns**: PAT-VO-001 (Immutable Value Object), PAT-VO-002 (Enum Value Object)
