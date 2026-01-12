# WI-011: Configuration Domain Events

| Field | Value |
|-------|-------|
| **ID** | WI-011 |
| **Title** | Configuration Domain Events |
| **Type** | Task |
| **Status** | PENDING |
| **Priority** | MEDIUM |
| **Phase** | PHASE-03 |
| **Assignee** | WT-Domain |
| **Created** | 2026-01-12 |
| **Completed** | - |

---

## Description

Define domain events for configuration lifecycle: loading, changes, and errors. These events enable event sourcing and audit trails for configuration state.

---

## Acceptance Criteria

- [ ] AC-011.1: `ConfigurationLoaded` event with source and key count
- [ ] AC-011.2: `ConfigurationValueChanged` event with key, old value, new value
- [ ] AC-011.3: `ConfigurationError` event for parsing/loading failures
- [ ] AC-011.4: All events are immutable (`@dataclass(frozen=True)`)
- [ ] AC-011.5: Events extend `DomainEvent` base class
- [ ] AC-011.6: Unit tests for event creation and serialization

---

## Sub-tasks

- [ ] ST-011.1: Create `src/domain/events/configuration_events.py`
- [ ] ST-011.2: Define `ConfigurationLoaded` event
- [ ] ST-011.3: Define `ConfigurationValueChanged` event
- [ ] ST-011.4: Define `ConfigurationError` event
- [ ] ST-011.5: Write unit tests for all events

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-011.1 | - | - |
| AC-011.2 | - | - |
| AC-011.3 | - | - |
| AC-011.4 | - | - |
| AC-011.5 | - | - |
| AC-011.6 | - | - |

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
