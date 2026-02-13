# PAT-ID-001: VertexId Pattern

> **Status**: MANDATORY
> **Category**: Identity
> **Also Known As**: Base Identity, Graph-Ready ID

---

## Intent

Provide a graph-ready base identity class for all domain entities using validated UUIDs with value equality semantics.

---

## Problem

Without a unified identity pattern:
- Raw strings or UUIDs lack type safety (TaskId could be mistakenly used as PhaseId)
- Identifiers don't carry semantic meaning
- Future graph database migration requires identity refactoring
- No validation of identifier format

---

## Solution

Create a frozen dataclass base class that validates UUID format and provides value equality.

### Implementation

```python
from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class VertexId:
    """
    Graph-ready abstraction for all entity IDs.
    Immutable value object with UUID format validation.

    Design Decisions:
    - frozen=True: Immutability guarantees hash consistency
    - UUID validation: Ensures valid identifiers
    - Graph-compatible: Ready for TinkerPop migration
    """
    value: str

    def __post_init__(self) -> None:
        # Validate UUID format (raises ValueError if invalid)
        UUID(self.value.replace("-", "")[:32], version=4)

    def __str__(self) -> str:
        return self.value

    def __hash__(self) -> int:
        return hash(self.value)
```

---

## Jerry Implementation

### File Location

`src/shared_kernel/identity/vertex_id.py`

### Key Characteristics

| Characteristic | Value |
|----------------|-------|
| Mutability | Immutable (frozen=True) |
| Equality | Value-based |
| Validation | UUID format |
| Graph Ready | Yes (TinkerPop compatible) |

---

## Consequences

| Type | Consequence |
|------|-------------|
| (+) | Type safety prevents mixing ID types |
| (+) | Graph-compatible for future TinkerPop migration |
| (+) | Immutable guarantees consistency |
| (+) | Value equality enables use as dict keys and set members |
| (-) | Slightly more verbose than raw strings |

---

## Industry Prior Art

| Source | Description |
|--------|-------------|
| [Apache TinkerPop](https://tinkerpop.apache.org/) | Graph database vertex identification |
| [Vaughn Vernon](https://vaughnvernon.com/) | Identity as Value Object pattern |
| [pyeventsourcing](https://github.com/pyeventsourcing/eventsourcing) | Aggregate ID patterns |

---

## Related Patterns

- [PAT-ID-002: Domain-Specific IDs](./domain-specific-ids.md) - Extends VertexId
- [PAT-ID-004: EdgeId](./edge-id.md) - Compound identity for edges
- [PAT-ENT-003: AggregateRoot](../entity/aggregate-root.md) - Uses VertexId for identity

---

## Design Canon Reference

Lines 70-114 in Jerry Design Canon v1.0

---

*Pattern documented by Claude (Opus 4.5) as part of TD-017*
