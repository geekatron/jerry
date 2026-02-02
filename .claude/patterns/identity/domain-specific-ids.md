# PAT-ID-002: Domain-Specific IDs Pattern

> **Status**: MANDATORY
> **Category**: Identity
> **Also Known As**: Typed Identifiers, Semantic IDs

---

## Intent

Create type-specific identifier subclasses with human-readable prefixes and deterministic formats.

---

## Problem

Without domain-specific IDs:
- Generic UUIDs are hard to identify and debug
- Mixing entity types causes subtle bugs at runtime
- No type safety at compile time
- Logs and debug output lack context

---

## Solution

Create type-specific subclasses of VertexId with deterministic format prefixes.

### ID Hierarchy

```
VertexId (base)
├── TaskId      # Format: "TASK-{uuid8}"     Example: TASK-a1b2c3d4
├── PhaseId     # Format: "PHASE-{uuid8}"    Example: PHASE-e5f6g7h8
├── PlanId      # Format: "PLAN-{uuid8}"     Example: PLAN-xyz98765
├── SubtaskId   # Format: "TASK-{parent}.{seq}"  Example: TASK-a1b2c3d4.1
├── KnowledgeId # Format: "KNOW-{uuid8}"     Example: KNOW-pat00001
├── ActorId     # Format: "ACTOR-{type}-{id}"    Example: ACTOR-CLAUDE-main
└── EventId     # Format: "EVT-{uuid}"       Example: EVT-a1b2c3d4
```

### Implementation

```python
from dataclasses import dataclass
from uuid import uuid4

@dataclass(frozen=True)
class TaskId(VertexId):
    """Strongly typed Task identifier."""

    @classmethod
    def generate(cls) -> 'TaskId':
        """Generate a new TaskId with TASK- prefix."""
        return cls(f"TASK-{uuid4().hex[:8]}")

    @classmethod
    def from_string(cls, value: str) -> 'TaskId':
        """Parse TaskId from string, validating format."""
        if not value.startswith("TASK-"):
            raise ValueError(f"Invalid TaskId format: {value}")
        return cls(value)


@dataclass(frozen=True)
class PhaseId(VertexId):
    """Strongly typed Phase identifier."""

    @classmethod
    def generate(cls) -> 'PhaseId':
        return cls(f"PHASE-{uuid4().hex[:8]}")

    @classmethod
    def from_string(cls, value: str) -> 'PhaseId':
        if not value.startswith("PHASE-"):
            raise ValueError(f"Invalid PhaseId format: {value}")
        return cls(value)


@dataclass(frozen=True)
class PlanId(VertexId):
    """Strongly typed Plan identifier."""

    @classmethod
    def generate(cls) -> 'PlanId':
        return cls(f"PLAN-{uuid4().hex[:8]}")

    @classmethod
    def from_string(cls, value: str) -> 'PlanId':
        if not value.startswith("PLAN-"):
            raise ValueError(f"Invalid PlanId format: {value}")
        return cls(value)


@dataclass(frozen=True)
class KnowledgeId(VertexId):
    """Strongly typed Knowledge item identifier."""

    @classmethod
    def generate(cls) -> 'KnowledgeId':
        return cls(f"KNOW-{uuid4().hex[:8]}")


@dataclass(frozen=True)
class ActorId(VertexId):
    """Actor identifier with type and instance."""
    actor_type: str = "SYSTEM"

    @classmethod
    def create(cls, actor_type: str, instance_id: str) -> 'ActorId':
        return cls(f"ACTOR-{actor_type}-{instance_id}", actor_type)


@dataclass(frozen=True)
class EventId(VertexId):
    """Event identifier."""

    @classmethod
    def generate(cls) -> 'EventId':
        return cls(f"EVT-{uuid4().hex[:8]}")
```

---

## Jerry Implementation

### File Location

`src/shared_kernel/identity/domain_ids.py`

### ID Format Table

| Type | Prefix | Format | Example |
|------|--------|--------|---------|
| TaskId | TASK- | TASK-{uuid8} | TASK-a1b2c3d4 |
| PhaseId | PHASE- | PHASE-{uuid8} | PHASE-e5f6g7h8 |
| PlanId | PLAN- | PLAN-{uuid8} | PLAN-xyz98765 |
| SubtaskId | TASK- | TASK-{parent}.{seq} | TASK-a1b2c3d4.1 |
| KnowledgeId | KNOW- | KNOW-{uuid8} | KNOW-pat00001 |
| ActorId | ACTOR- | ACTOR-{type}-{id} | ACTOR-CLAUDE-main |
| EventId | EVT- | EVT-{uuid8} | EVT-a1b2c3d4 |

---

## Consequences

| Type | Consequence |
|------|-------------|
| (+) | Self-documenting IDs in logs and debug output |
| (+) | Type system prevents ID mixing at compile time |
| (+) | Enables pattern matching in CLI parsing |
| (+) | Factory methods enforce format consistency |
| (-) | Slightly longer identifiers |

---

## Usage Examples

```python
# Generate new IDs
task_id = TaskId.generate()  # TASK-a1b2c3d4
phase_id = PhaseId.generate()  # PHASE-e5f6g7h8

# Parse from string
task_id = TaskId.from_string("TASK-a1b2c3d4")

# Type safety - this raises TypeError at type check time
phase_id: PhaseId = task_id  # Error: TaskId is not PhaseId

# CLI pattern matching
if id_string.startswith("TASK-"):
    task_id = TaskId.from_string(id_string)
elif id_string.startswith("PHASE-"):
    phase_id = PhaseId.from_string(id_string)
```

---

## Related Patterns

- [PAT-ID-001: VertexId](./vertex-id.md) - Base class
- [PAT-AGG-001: Task Aggregate](../aggregate/task-aggregate.md) - Uses TaskId
- [PAT-AGG-002: Phase Aggregate](../aggregate/phase-aggregate.md) - Uses PhaseId

---

## Design Canon Reference

Lines 117-167 in Jerry Design Canon v1.0

---

*Pattern documented by Claude (Opus 4.5) as part of TD-017*
