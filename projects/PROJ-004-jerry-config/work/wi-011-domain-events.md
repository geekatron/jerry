# WI-011: Configuration Domain Events

| Field | Value |
|-------|-------|
| **ID** | WI-011 |
| **Title** | Configuration Domain Events |
| **Type** | Task |
| **Status** | COMPLETED |
| **Priority** | MEDIUM |
| **Phase** | PHASE-03 |
| **Assignee** | WT-Domain |
| **Created** | 2026-01-12 |
| **Completed** | 2026-01-12 |

---

## Description

Define domain events for configuration lifecycle: loading, changes, and errors. These events enable event sourcing and audit trails for configuration state.

---

## Acceptance Criteria

- [x] AC-011.1: `ConfigurationLoaded` event with source, key count, source_path, load_time_ms
- [x] AC-011.2: `ConfigurationValueChanged` event with key, old_value, new_value, source, reason
- [x] AC-011.3: `ConfigurationError` event with error_type, error_message, recoverable, failed_keys
- [x] AC-011.4: All events are immutable (`@dataclass(frozen=True)`)
- [x] AC-011.5: Events extend `DomainEvent` base class with to_dict(), from_dict()
- [x] AC-011.6: Unit tests for event creation and serialization (40 tests)

---

## Sub-tasks

- [x] ST-011.1: Create `src/configuration/domain/events/configuration_events.py`
- [x] ST-011.2: Define `ConfigurationLoaded` event with factory, serialization
- [x] ST-011.3: Define `ConfigurationValueChanged` event with is_addition, is_removal, is_update
- [x] ST-011.4: Define `ConfigurationError` event with severity levels
- [x] ST-011.5: Write unit tests for all events (40 tests)

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-011.1 | ConfigurationLoaded with `source`, `keys_loaded`, `source_path`, `load_time_ms` | `configuration_events.py:lines 63-134` |
| AC-011.2 | ConfigurationValueChanged with `key`, `old_value`, `new_value`, `source`, `reason`, `is_addition`, `is_removal`, `is_update` | `configuration_events.py:lines 138-253` |
| AC-011.3 | ConfigurationError with `error_type`, `error_message`, `recoverable`, `failed_keys`, severity | `configuration_events.py:lines 261-380` |
| AC-011.4 | All events use `@dataclass(frozen=True)` | All event class definitions |
| AC-011.5 | Events extend `DomainEvent` with `_payload()`, `to_dict()`, `from_dict()` | All event classes |
| AC-011.6 | 40 unit tests passing | `pytest tests/unit/configuration/domain/events/ -v` |

---

## Implementation Notes

```python
# src/domain/events/configuration_events.py
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, ClassVar

from src.shared_kernel.events.domain_event import DomainEvent


@dataclass(frozen=True)
class ConfigurationLoaded(DomainEvent):
    """Raised when configuration is successfully loaded."""

    EVENT_TYPE: ClassVar[str] = "configuration.loaded"

    source: str  # "env", "project", "root", "default"
    keys_loaded: int
    loaded_at: datetime

    @classmethod
    def create(cls, source: str, keys_loaded: int) -> "ConfigurationLoaded":
        return cls(
            source=source,
            keys_loaded=keys_loaded,
            loaded_at=datetime.now(timezone.utc),
        )


@dataclass(frozen=True)
class ConfigurationValueChanged(DomainEvent):
    """Raised when a configuration value is updated."""

    EVENT_TYPE: ClassVar[str] = "configuration.value_changed"

    key: str
    old_value: Any
    new_value: Any
    changed_at: datetime

    @classmethod
    def create(cls, key: str, old_value: Any, new_value: Any) -> "ConfigurationValueChanged":
        return cls(
            key=key,
            old_value=old_value,
            new_value=new_value,
            changed_at=datetime.now(timezone.utc),
        )
```

---

## Progress Log

| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T11:00:00Z | Work item created | Claude |
| 2026-01-12T16:00:00Z | Domain events implementation started | Claude |
| 2026-01-12T16:30:00Z | ConfigurationLoaded event defined with factory and serialization | Claude |
| 2026-01-12T17:00:00Z | ConfigurationValueChanged event with change detection properties | Claude |
| 2026-01-12T17:30:00Z | ConfigurationError event with severity and recoverability | Claude |
| 2026-01-12T18:00:00Z | Unit tests written (40 tests) | Claude |
| 2026-01-12T18:30:00Z | Tests passing, work item COMPLETED | Claude |

---

## Dependencies

| Type | Work Item | Relationship |
|------|-----------|--------------|
| Depends On | WI-008 | Domain model design must be complete |
| Blocks | WI-015 | CLI integration needs events for logging |

---

## Related Artifacts

- **Plan Reference**: [PLAN.md, Phase 1: Domain Layer](../PLAN.md)
- **Pattern**: [Domain Event](../../../../.claude/patterns/event/domain-event.md)
