# PAT-ENT-001: IAuditable Protocol

> **Status**: MANDATORY
> **Category**: Entity
> **Also Known As**: Audit Metadata, Timestamp Tracking

---

## Intent

Define a protocol for tracking creation and modification metadata on all entities.

---

## Problem

Without audit tracking:
- No visibility into when entities were created or modified
- Cannot determine who made changes
- Debugging and forensics are difficult
- Compliance requirements cannot be met

---

## Solution

Define a protocol for audit metadata that all entities implement.

### Implementation

```python
from typing import Protocol
from datetime import datetime

class IAuditable(Protocol):
    """Tracking metadata for entity creation and modification.

    All domain entities that persist state should implement this
    protocol to provide audit trail capabilities.
    """

    @property
    def created_by(self) -> str:
        """Who created this entity.

        Values:
        - User email (e.g., "user@example.com")
        - "Claude" for AI agent actions
        - "System" for automated processes
        """
        ...

    @property
    def created_at(self) -> datetime:
        """When this entity was created (UTC)."""
        ...

    @property
    def updated_by(self) -> str:
        """Who last modified this entity."""
        ...

    @property
    def updated_at(self) -> datetime:
        """When this entity was last modified (UTC)."""
        ...
```

---

## Jerry Implementation

### File Location

`src/shared_kernel/interfaces/auditable.py`

### Actor Types

| Actor | Format | Example |
|-------|--------|---------|
| Human User | Email address | user@example.com |
| Claude Agent | "Claude" or "ACTOR-CLAUDE-{id}" | Claude |
| Sub-Agent | "ACTOR-{type}-{id}" | ACTOR-RESEARCHER-001 |
| System | "System" | System |

### Integration with AggregateRoot

```python
@dataclass
class AggregateRoot(ABC):
    """Base class implementing IAuditable."""
    _created_by: str = "System"
    _created_at: datetime = field(default_factory=datetime.utcnow)
    _updated_by: str = "System"
    _updated_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def created_by(self) -> str:
        return self._created_by

    @property
    def created_at(self) -> datetime:
        return self._created_at

    # ... remaining properties
```

---

## Consequences

| Type | Consequence |
|------|-------------|
| (+) | Full audit trail for all entities |
| (+) | Enables "who changed what when" queries |
| (+) | Supports compliance requirements |
| (+) | Protocol enables duck typing |
| (-) | Additional storage per entity |

---

## Related Patterns

- [PAT-ENT-002: IVersioned](./iversioned.md) - Version tracking
- [PAT-ENT-003: AggregateRoot](./aggregate-root.md) - Implements IAuditable
- [PAT-EVT-002: DomainEvent](../event/domain-event.md) - Events include caused_by

---

## Design Canon Reference

Lines 260-288 in Jerry Design Canon v1.0

---

*Pattern documented by Claude (Opus 4.5) as part of TD-017*
