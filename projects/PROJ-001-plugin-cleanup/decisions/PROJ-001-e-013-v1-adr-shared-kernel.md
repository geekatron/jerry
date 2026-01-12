# ADR-013: Shared Kernel Module Implementation

> **Document ID**: PROJ-001-e-013-v1-adr-shared-kernel
> **PS ID**: PROJ-001
> **Entry ID**: e-013-v1
> **Date**: 2026-01-09
> **Author**: ps-architect agent v2.0.0
> **Cycle**: 1 (Initial)
> **Status**: PROPOSED
>
> **Sources**:
> - **Canon**: `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md`
> - **Gap Analysis**: `projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-012-v1-canon-implementation-gap.md`

---

## L0: Executive Summary (ELI5)

### What decision is being made?

We need to create a **Shared Kernel** module - a set of foundational building blocks that will be used by all parts of Jerry. Think of it like the foundation of a house: before you can build walls (aggregates), rooms (bounded contexts), or the roof (API), you need a solid foundation.

### Why does it matter?

Without the Shared Kernel:
- Every bounded context will invent its own IDs, causing inconsistency
- We cannot implement event sourcing (the audit trail system)
- We cannot build the core aggregates (Task, Phase, Plan)
- The codebase will have no common language for identity, versioning, and auditing

### What's the recommendation?

**Create `src/shared_kernel/` with 6 core modules:**

1. `exceptions.py` - Common error types
2. `vertex_id.py` - Base class for all IDs (VertexId, TaskId, PhaseId, etc.)
3. `jerry_uri.py` - URI-based entity references
4. `auditable.py` - Tracking who created/modified what
5. `versioned.py` - Optimistic concurrency control
6. `entity_base.py` - Foundation for all domain entities

---

## Context

### Problem Statement

The Gap Analysis (e-012-v1) identified **Gap G-001** as the highest priority issue:

> "The Shared Kernel is the foundation for all other patterns. Without it, each bounded context will reinvent these wheels inconsistently."

**Current State (from Gap Analysis L60-107)**:
- `src/shared_kernel/` directory does not exist
- Only identity type is `ProjectId` which does NOT extend `VertexId`
- No `IAuditable`, `IVersioned`, or `EntityBase` implementations
- Domain exceptions are partial (4 types vs 7 required)
- Pattern compliance is ~15-20% (4 of 26 patterns implemented)

**Target State (from Canon L1716-1860)**:
- Shared Kernel provides cross-cutting value objects
- All bounded contexts share common identity patterns
- Graph-ready IDs enable future migration to graph databases
- Consistent audit and versioning across all entities

### Why Shared Kernel First?

Per the Gap Analysis dependency graph (L466-498):

```
Phase 1: Shared Kernel (blocks all else)
    ├── VertexId hierarchy
    ├── IAuditable, IVersioned
    └── EntityBase
         │
         v
Phase 2: Event Sourcing (blocks aggregates)
         │
         v
Phase 3: Aggregate Foundation
         │
         v
Phase 4: Work Management Context
```

The Shared Kernel is a **blocking dependency** for:
- Event Sourcing infrastructure (needs EventId, DomainError)
- AggregateRoot base class (needs VertexId, EntityBase, IAuditable, IVersioned)
- All domain aggregates (need AggregateRoot)

---

## L1: Technical Decision (Software Engineer)

### Decision

Implement Shared Kernel at `src/shared_kernel/` with the following module structure:

```
src/shared_kernel/
├── __init__.py           # Public API exports
├── exceptions.py         # DomainError hierarchy (7 exception types)
├── vertex_id.py          # VertexId base + domain-specific IDs + EdgeId
├── jerry_uri.py          # JerryUri value object
├── auditable.py          # IAuditable protocol
├── versioned.py          # IVersioned protocol
└── entity_base.py        # EntityBase combining VertexId + IAuditable + IVersioned
```

### Alternatives Considered

| Option | Description | Pros | Cons | Decision |
|--------|-------------|------|------|----------|
| **A: Dedicated Shared Kernel module** | Create `src/shared_kernel/` as standalone module | Clean separation; explicit sharing; follows Canon | New directory; migration needed for existing code | **SELECTED** |
| **B: Inline in each bounded context** | Each context defines its own base types | No cross-context dependency; context autonomy | Code duplication; inconsistent patterns; violates DRY; contradicts Canon | REJECTED |
| **C: External package** | Publish as `jerry-kernel` pip package | Version isolation; can be reused in other projects | Over-engineering for single repo; deployment complexity; synchronization overhead | REJECTED |
| **D: Place in src/domain/** | Put shared types at top-level domain | Follows traditional DDD structure | Conflicts with bounded context isolation; Canon explicitly specifies `shared_kernel/` | REJECTED |

**Rationale for Option A:**

1. **Canon Compliance**: Canon (L1297-1305) explicitly specifies `src/shared_kernel/` as the location
2. **DDD Best Practice**: Eric Evans describes Shared Kernel as a bounded context of its own
3. **Dependency Direction**: Inner layers (domain) can depend on shared_kernel without violating hexagonal architecture
4. **Migration Path**: Existing `ProjectId` can be adapted to extend `VertexId` with minimal refactoring

### Interface Contracts

#### 1. exceptions.py (PAT-011 partial)

```python
"""
Domain exceptions for Jerry Framework.

All domain-specific exceptions should be defined here.
Application and infrastructure layers may wrap these in their own exceptions.

References:
    - Canon PAT-011 (L1812-1859)
    - Gap Analysis G-001 (L288-301)
"""
from __future__ import annotations


class DomainError(Exception):
    """Base class for all domain errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class NotFoundError(DomainError):
    """Entity not found."""

    def __init__(self, entity_type: str, entity_id: str) -> None:
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} '{entity_id}' not found")


class InvalidStateError(DomainError):
    """Operation invalid for current state."""

    def __init__(self, current_state: str, attempted_action: str) -> None:
        self.current_state = current_state
        self.attempted_action = attempted_action
        super().__init__(f"Cannot {attempted_action} in state {current_state}")


class InvalidStateTransitionError(DomainError):
    """State transition not allowed."""

    def __init__(self, from_state: str, to_state: str) -> None:
        self.from_state = from_state
        self.to_state = to_state
        super().__init__(f"Transition from {from_state} to {to_state} not allowed")


class InvariantViolationError(DomainError):
    """Domain invariant violated."""

    def __init__(self, invariant: str, details: str) -> None:
        self.invariant = invariant
        self.details = details
        super().__init__(f"Invariant '{invariant}' violated: {details}")


class ConcurrencyError(DomainError):
    """Optimistic concurrency conflict."""

    def __init__(self, expected_version: int, actual_version: int) -> None:
        self.expected_version = expected_version
        self.actual_version = actual_version
        super().__init__(
            f"Concurrency conflict: expected version {expected_version}, "
            f"actual version {actual_version}"
        )


class ValidationError(DomainError):
    """Input validation failed."""

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.validation_message = message
        super().__init__(f"Validation failed for '{field}': {message}")
```

**Usage Example**:
```python
from shared_kernel.exceptions import NotFoundError, InvalidStateTransitionError

# In repository adapter
def find_by_id(self, task_id: TaskId) -> Task:
    task = self._store.get(task_id.value)
    if task is None:
        raise NotFoundError("Task", task_id.value)
    return task

# In aggregate
def transition_status(self, target: TaskStatus) -> None:
    if not self._can_transition_to(target):
        raise InvalidStateTransitionError(self._status.value, target.value)
```

#### 2. vertex_id.py (PAT-001, PAT-002, PAT-004)

```python
"""
VertexId - Base class for all entity identifiers.

This module defines the VertexId base class and all domain-specific ID subclasses.
VertexId provides graph-ready abstraction enabling future migration to native graph databases.

References:
    - Canon PAT-001 (L56-117): VertexId base class
    - Canon PAT-002 (L119-165): Domain-specific IDs
    - Canon PAT-004 (L222-260): EdgeId

Exports:
    VertexId (base class)
    TaskId, PhaseId, PlanId, SubtaskId, KnowledgeId, ActorId, EventId (subclasses)
    EdgeId (relationship identifier)
"""
from __future__ import annotations

import re
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Pattern


@dataclass(frozen=True)
class VertexId(ABC):
    """
    Graph-ready abstraction for all entity IDs.

    Invariants:
        - Immutable (frozen dataclass)
        - Value equality (two VertexIds with same value are equal)
        - Valid format (subclass-specific validation)

    Usage:
        task_id = TaskId.generate()
        task_id = TaskId.from_string("TASK-a1b2c3d4")
    """

    value: str

    def __post_init__(self) -> None:
        if not self._is_valid_format(self.value):
            raise ValueError(f"Invalid {self.__class__.__name__} format: {self.value}")

    @classmethod
    @abstractmethod
    def _is_valid_format(cls, value: str) -> bool:
        """Subclass-specific format validation."""
        ...

    @classmethod
    @abstractmethod
    def generate(cls) -> VertexId:
        """Generate a new ID with proper format."""
        ...

    @classmethod
    def from_string(cls, value: str) -> VertexId:
        """Parse ID from string representation."""
        return cls(value)

    def __str__(self) -> str:
        return self.value

    def __hash__(self) -> int:
        return hash(self.value)


# Domain-Specific ID Classes

@dataclass(frozen=True)
class TaskId(VertexId):
    """Task entity identifier. Format: TASK-{uuid8}"""

    _PATTERN: ClassVar[Pattern[str]] = re.compile(r"^TASK-[a-f0-9]{8}$")

    @classmethod
    def _is_valid_format(cls, value: str) -> bool:
        return bool(cls._PATTERN.match(value))

    @classmethod
    def generate(cls) -> TaskId:
        return cls(f"TASK-{uuid.uuid4().hex[:8]}")


@dataclass(frozen=True)
class PhaseId(VertexId):
    """Phase entity identifier. Format: PHASE-{uuid8}"""

    _PATTERN: ClassVar[Pattern[str]] = re.compile(r"^PHASE-[a-f0-9]{8}$")

    @classmethod
    def _is_valid_format(cls, value: str) -> bool:
        return bool(cls._PATTERN.match(value))

    @classmethod
    def generate(cls) -> PhaseId:
        return cls(f"PHASE-{uuid.uuid4().hex[:8]}")


@dataclass(frozen=True)
class PlanId(VertexId):
    """Plan entity identifier. Format: PLAN-{uuid8}"""

    _PATTERN: ClassVar[Pattern[str]] = re.compile(r"^PLAN-[a-f0-9]{8}$")

    @classmethod
    def _is_valid_format(cls, value: str) -> bool:
        return bool(cls._PATTERN.match(value))

    @classmethod
    def generate(cls) -> PlanId:
        return cls(f"PLAN-{uuid.uuid4().hex[:8]}")


@dataclass(frozen=True)
class SubtaskId(VertexId):
    """Subtask entity identifier. Format: TASK-{uuid8}.{n}"""

    _PATTERN: ClassVar[Pattern[str]] = re.compile(r"^TASK-[a-f0-9]{8}\.\d+$")

    @classmethod
    def _is_valid_format(cls, value: str) -> bool:
        return bool(cls._PATTERN.match(value))

    @classmethod
    def generate(cls) -> SubtaskId:
        raise NotImplementedError("SubtaskId requires parent TaskId; use from_parent()")

    @classmethod
    def from_parent(cls, parent_id: TaskId, sequence: int) -> SubtaskId:
        """Create SubtaskId from parent TaskId and sequence number."""
        if sequence < 1:
            raise ValueError("Subtask sequence must be >= 1")
        return cls(f"{parent_id.value}.{sequence}")

    @property
    def parent_id(self) -> TaskId:
        """Extract parent TaskId from subtask ID."""
        parent_value = self.value.rsplit(".", 1)[0]
        return TaskId(parent_value)

    @property
    def sequence(self) -> int:
        """Extract sequence number from subtask ID."""
        return int(self.value.rsplit(".", 1)[1])


@dataclass(frozen=True)
class KnowledgeId(VertexId):
    """Knowledge entity identifier. Format: KNOW-{uuid8}"""

    _PATTERN: ClassVar[Pattern[str]] = re.compile(r"^KNOW-[a-f0-9]{8}$")

    @classmethod
    def _is_valid_format(cls, value: str) -> bool:
        return bool(cls._PATTERN.match(value))

    @classmethod
    def generate(cls) -> KnowledgeId:
        return cls(f"KNOW-{uuid.uuid4().hex[:8]}")


@dataclass(frozen=True)
class ActorId(VertexId):
    """Actor entity identifier. Format: ACTOR-{TYPE}-{id}"""

    _PATTERN: ClassVar[Pattern[str]] = re.compile(r"^ACTOR-[A-Z]+-[a-z0-9]+$")

    @classmethod
    def _is_valid_format(cls, value: str) -> bool:
        return bool(cls._PATTERN.match(value))

    @classmethod
    def generate(cls) -> ActorId:
        raise NotImplementedError("ActorId requires type and id; use for_type()")

    @classmethod
    def for_type(cls, actor_type: str, actor_id: str) -> ActorId:
        """Create ActorId for specific actor type."""
        if not actor_type.isupper():
            raise ValueError("Actor type must be uppercase")
        if not actor_id.islower() or not actor_id.replace("-", "").isalnum():
            raise ValueError("Actor id must be lowercase alphanumeric")
        return cls(f"ACTOR-{actor_type}-{actor_id}")

    @classmethod
    def claude(cls, instance: str = "main") -> ActorId:
        """Create ActorId for Claude agent."""
        return cls.for_type("CLAUDE", instance)

    @classmethod
    def system(cls) -> ActorId:
        """Create ActorId for system operations."""
        return cls.for_type("SYSTEM", "internal")


@dataclass(frozen=True)
class EventId(VertexId):
    """Event entity identifier. Format: EVT-{uuid}"""

    _PATTERN: ClassVar[Pattern[str]] = re.compile(
        r"^EVT-[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"
    )

    @classmethod
    def _is_valid_format(cls, value: str) -> bool:
        return bool(cls._PATTERN.match(value))

    @classmethod
    def generate(cls) -> EventId:
        return cls(f"EVT-{uuid.uuid4()}")


# EdgeId for graph relationships

@dataclass(frozen=True)
class EdgeId:
    """
    Deterministic edge identifier generated from endpoints and label.

    Format: "{source_id}--{label}-->{target_id}"

    References:
        - Canon PAT-004 (L222-260)
    """

    source_id: VertexId
    target_id: VertexId
    label: str

    def __post_init__(self) -> None:
        if not self.label:
            raise ValueError("Edge label cannot be empty")
        if not self.label.isupper():
            raise ValueError("Edge label must be uppercase")

    @property
    def value(self) -> str:
        return f"{self.source_id}--{self.label}-->{self.target_id}"

    def __str__(self) -> str:
        return self.value

    def __hash__(self) -> int:
        return hash(self.value)
```

**Usage Example**:
```python
from shared_kernel.vertex_id import TaskId, PhaseId, SubtaskId, EdgeId

# Generate new IDs
task_id = TaskId.generate()  # TaskId(value="TASK-a1b2c3d4")
phase_id = PhaseId.generate()  # PhaseId(value="PHASE-e5f6g7h8")

# Parse from string
task_id = TaskId.from_string("TASK-a1b2c3d4")

# Create subtask from parent
subtask_id = SubtaskId.from_parent(task_id, sequence=1)  # TASK-a1b2c3d4.1

# Create edge relationship
edge = EdgeId(phase_id, task_id, "CONTAINS")
print(edge.value)  # "PHASE-e5f6g7h8--CONTAINS-->TASK-a1b2c3d4"

# Value equality
assert TaskId("TASK-a1b2c3d4") == TaskId("TASK-a1b2c3d4")
```

**Validation Rules**:

| ID Type | Format Pattern | Regex | Example |
|---------|----------------|-------|---------|
| TaskId | `TASK-{uuid8}` | `^TASK-[a-f0-9]{8}$` | `TASK-a1b2c3d4` |
| PhaseId | `PHASE-{uuid8}` | `^PHASE-[a-f0-9]{8}$` | `PHASE-e5f6g7h8` |
| PlanId | `PLAN-{uuid8}` | `^PLAN-[a-f0-9]{8}$` | `PLAN-12345678` |
| SubtaskId | `TASK-{uuid8}.{n}` | `^TASK-[a-f0-9]{8}\.\d+$` | `TASK-a1b2c3d4.1` |
| KnowledgeId | `KNOW-{uuid8}` | `^KNOW-[a-f0-9]{8}$` | `KNOW-xyz98765` |
| ActorId | `ACTOR-{TYPE}-{id}` | `^ACTOR-[A-Z]+-[a-z0-9]+$` | `ACTOR-CLAUDE-main` |
| EventId | `EVT-{uuid}` | `^EVT-[a-f0-9-]{36}$` | `EVT-a1b2c3d4-...` |

#### 3. jerry_uri.py (PAT-003)

```python
"""
JerryUri - URI-based entity reference format.

Provides cross-system identification using jerry:// scheme.
Format: jerry://{entity_type}/{id}[/{sub_entity}/{sub_id}]

References:
    - Canon PAT-003 (L167-220)

Exports:
    JerryUri (value object)
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class JerryUri:
    """
    URI-based entity reference for cross-system identification.

    Invariants:
        - Scheme is always "jerry"
        - Path segments alternate: entity_type/id/sub_type/sub_id
        - Valid entity types: task, phase, plan, knowledge, actor, event

    Examples:
        jerry://task/TASK-a1b2c3d4
        jerry://plan/PLAN-12345678
        jerry://plan/PLAN-12345678/phase/PHASE-e5f6g7h8
        jerry://knowledge/pattern/KNOW-xyz98765
    """

    path_segments: tuple[str, ...]

    VALID_ENTITY_TYPES: ClassVar[frozenset[str]] = frozenset({
        "task", "phase", "plan", "knowledge", "actor", "event", "subtask"
    })
    SCHEME: ClassVar[str] = "jerry"

    def __post_init__(self) -> None:
        if len(self.path_segments) < 2:
            raise ValueError("JerryUri requires at least entity_type and id")
        if len(self.path_segments) % 2 != 0:
            raise ValueError("JerryUri path segments must be pairs of type/id")
        # Validate entity types
        for i in range(0, len(self.path_segments), 2):
            entity_type = self.path_segments[i]
            if entity_type not in self.VALID_ENTITY_TYPES:
                raise ValueError(f"Invalid entity type: {entity_type}")

    @classmethod
    def parse(cls, uri: str) -> JerryUri:
        """Parse jerry:// URI string."""
        prefix = f"{cls.SCHEME}://"
        if not uri.startswith(prefix):
            raise ValueError(f"Invalid JerryUri scheme: {uri}")
        path = uri[len(prefix):]
        if not path:
            raise ValueError("JerryUri path cannot be empty")
        segments = tuple(path.split("/"))
        return cls(segments)

    @classmethod
    def for_entity(cls, entity_type: str, entity_id: str) -> JerryUri:
        """Create JerryUri for a single entity."""
        return cls((entity_type, entity_id))

    @classmethod
    def for_nested(
        cls,
        parent_type: str,
        parent_id: str,
        child_type: str,
        child_id: str
    ) -> JerryUri:
        """Create JerryUri for a nested entity."""
        return cls((parent_type, parent_id, child_type, child_id))

    def __str__(self) -> str:
        return f"{self.SCHEME}://{'/'.join(self.path_segments)}"

    @property
    def entity_type(self) -> str:
        """Primary entity type (first path segment)."""
        return self.path_segments[0]

    @property
    def entity_id(self) -> str:
        """Primary entity ID (second path segment)."""
        return self.path_segments[1]

    @property
    def is_nested(self) -> bool:
        """True if this URI references a nested entity."""
        return len(self.path_segments) > 2

    @property
    def leaf_type(self) -> str:
        """Innermost entity type (last type segment)."""
        return self.path_segments[-2]

    @property
    def leaf_id(self) -> str:
        """Innermost entity ID (last id segment)."""
        return self.path_segments[-1]
```

**Usage Example**:
```python
from shared_kernel.jerry_uri import JerryUri

# Parse from string
uri = JerryUri.parse("jerry://task/TASK-a1b2c3d4")
print(uri.entity_type)  # "task"
print(uri.entity_id)    # "TASK-a1b2c3d4"

# Create directly
uri = JerryUri.for_entity("plan", "PLAN-12345678")
print(str(uri))  # "jerry://plan/PLAN-12345678"

# Nested entity
uri = JerryUri.for_nested("plan", "PLAN-12345678", "phase", "PHASE-e5f6g7h8")
print(str(uri))  # "jerry://plan/PLAN-12345678/phase/PHASE-e5f6g7h8"
print(uri.is_nested)  # True
print(uri.leaf_type)  # "phase"
print(uri.leaf_id)    # "PHASE-e5f6g7h8"
```

#### 4. auditable.py (PAT-005)

```python
"""
IAuditable - Audit metadata protocol.

Defines contract for tracking entity creation and modification.

References:
    - Canon PAT-005 (L266-309)

Exports:
    IAuditable (Protocol)
"""
from __future__ import annotations

from datetime import datetime
from typing import Protocol, runtime_checkable


@runtime_checkable
class IAuditable(Protocol):
    """
    Audit metadata contract for all entities.

    Invariants:
        - created_at is immutable after entity creation
        - updated_at >= created_at
        - created_by/updated_by are non-empty strings

    Values for created_by/updated_by:
        - User email (e.g., "user@example.com")
        - "Claude" for AI agent operations
        - "System" for automated/internal operations
    """

    @property
    def created_by(self) -> str:
        """User email, "Claude", or "System"."""
        ...

    @property
    def created_at(self) -> datetime:
        """UTC timestamp of entity creation."""
        ...

    @property
    def updated_by(self) -> str:
        """User email, "Claude", or "System"."""
        ...

    @property
    def updated_at(self) -> datetime:
        """UTC timestamp of last modification."""
        ...
```

**Usage Example**:
```python
from shared_kernel.auditable import IAuditable
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class MyEntity:
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

    @property
    def updated_by(self) -> str:
        return self._updated_by

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

# Runtime check
entity = MyEntity()
assert isinstance(entity, IAuditable)  # True
```

#### 5. versioned.py (PAT-006)

```python
"""
IVersioned - Optimistic concurrency control protocol.

Defines contract for version tracking to prevent lost updates.

References:
    - Canon PAT-006 (L311-340)

Exports:
    IVersioned (Protocol)
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class IVersioned(Protocol):
    """
    Version tracking for optimistic concurrency control.

    Invariants:
        - version starts at 0 (no events yet) or 1 (after creation event)
        - version increments by 1 for each persisted event
        - expected_version check prevents lost updates

    Usage:
        When saving an aggregate, the repository checks that the current
        version in storage matches the expected_version. If not, another
        process modified the aggregate, and a ConcurrencyError is raised.
    """

    @property
    def version(self) -> int:
        """Current version (number of events in stream)."""
        ...

    def get_expected_version(self) -> int:
        """Return version for concurrency check on save."""
        ...
```

**Usage Example**:
```python
from shared_kernel.versioned import IVersioned
from shared_kernel.exceptions import ConcurrencyError

def save_with_optimistic_locking(
    aggregate: IVersioned,
    store: dict,
    stream_id: str
) -> None:
    expected = aggregate.get_expected_version()
    current = store.get(f"{stream_id}_version", -1)

    if current != expected:
        raise ConcurrencyError(expected, current)

    # Save logic here...
    store[f"{stream_id}_version"] = aggregate.version
```

#### 6. entity_base.py (PAT-007)

```python
"""
EntityBase - Base class for all domain entities.

Combines VertexId identity with IAuditable and IVersioned.
All domain entities should inherit from this class.

References:
    - Canon PAT-007 (L342-407)

Exports:
    EntityBase (dataclass)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .vertex_id import VertexId


@dataclass
class EntityBase:
    """
    Base class for all domain entities.

    Combines:
        - VertexId identity (graph-ready)
        - IAuditable metadata (audit trail)
        - IVersioned concurrency control

    Subclasses must override _id type with specific VertexId subclass.

    Note: This class does NOT implement IAuditable/IVersioned protocols
    directly as they are runtime_checkable Protocols. Instead, it provides
    the required properties that make instances pass isinstance() checks.
    """

    _id: VertexId
    _version: int = 0
    _created_by: str = "System"
    _created_at: datetime = field(default_factory=datetime.utcnow)
    _updated_by: str = "System"
    _updated_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def id(self) -> VertexId:
        """Entity identifier."""
        return self._id

    @property
    def version(self) -> int:
        """Current version for optimistic concurrency."""
        return self._version

    @property
    def created_by(self) -> str:
        """User who created this entity."""
        return self._created_by

    @property
    def created_at(self) -> datetime:
        """UTC timestamp of entity creation."""
        return self._created_at

    @property
    def updated_by(self) -> str:
        """User who last modified this entity."""
        return self._updated_by

    @property
    def updated_at(self) -> datetime:
        """UTC timestamp of last modification."""
        return self._updated_at

    def get_expected_version(self) -> int:
        """Return version for concurrency check on save."""
        return self._version

    def _touch(self, by: str) -> None:
        """
        Update modification metadata.

        Should be called after any mutation to the entity.

        Args:
            by: Identifier of who made the change (email, "Claude", or "System")
        """
        self._updated_by = by
        self._updated_at = datetime.utcnow()

    def _increment_version(self) -> None:
        """Increment version after event is raised."""
        self._version += 1
```

**Usage Example**:
```python
from dataclasses import dataclass
from shared_kernel.entity_base import EntityBase
from shared_kernel.vertex_id import TaskId
from shared_kernel.auditable import IAuditable
from shared_kernel.versioned import IVersioned

@dataclass
class Task(EntityBase):
    title: str = ""
    description: str = ""

    @classmethod
    def create(cls, title: str, created_by: str = "Claude") -> "Task":
        task = cls(
            _id=TaskId.generate(),
            _created_by=created_by,
            _updated_by=created_by,
            title=title
        )
        return task

# Create a task
task = Task.create("Implement feature X", created_by="Claude")

# Protocol compliance (runtime checkable)
assert isinstance(task, IAuditable)  # True
assert isinstance(task, IVersioned)  # True

# Identity
print(task.id)  # TaskId(value="TASK-a1b2c3d4")

# Audit trail
print(task.created_by)  # "Claude"
print(task.created_at)  # datetime(...)

# Version tracking
print(task.version)  # 0
```

#### 7. __init__.py (Public API)

```python
"""
Shared Kernel - Cross-cutting value objects for Jerry Framework.

This module contains foundational types shared across all bounded contexts:
- Identity: VertexId hierarchy, EdgeId, JerryUri
- Audit: IAuditable protocol
- Concurrency: IVersioned protocol
- Base classes: EntityBase
- Exceptions: Domain error hierarchy

References:
    - Canon Section "Shared Kernel Specification" (L1716-1860)
"""
from __future__ import annotations

# Exceptions
from .exceptions import (
    ConcurrencyError,
    DomainError,
    InvariantViolationError,
    InvalidStateError,
    InvalidStateTransitionError,
    NotFoundError,
    ValidationError,
)

# Identity
from .vertex_id import (
    ActorId,
    EdgeId,
    EventId,
    KnowledgeId,
    PhaseId,
    PlanId,
    SubtaskId,
    TaskId,
    VertexId,
)
from .jerry_uri import JerryUri

# Protocols
from .auditable import IAuditable
from .versioned import IVersioned

# Base classes
from .entity_base import EntityBase


__all__ = [
    # Exceptions
    "DomainError",
    "NotFoundError",
    "InvalidStateError",
    "InvalidStateTransitionError",
    "InvariantViolationError",
    "ConcurrencyError",
    "ValidationError",
    # Identity
    "VertexId",
    "TaskId",
    "PhaseId",
    "PlanId",
    "SubtaskId",
    "KnowledgeId",
    "ActorId",
    "EventId",
    "EdgeId",
    "JerryUri",
    # Protocols
    "IAuditable",
    "IVersioned",
    # Base classes
    "EntityBase",
]
```

---

## L2: Strategic Implications (Principal Architect)

### Consequences

**Positive:**

1. **Foundation for all future bounded contexts**: Every aggregate, event, and entity will share consistent patterns
2. **Graph-ready from day one**: VertexId enables seamless migration to native graph databases (Neo4j, Neptune)
3. **Audit compliance**: IAuditable ensures all entities track creation/modification metadata
4. **Concurrency safety**: IVersioned prevents lost updates in multi-user/multi-agent scenarios
5. **Consistent error handling**: Domain exception hierarchy provides semantic errors across the codebase
6. **Type safety**: Strong typing with frozen dataclasses prevents accidental mutations
7. **Testability**: Small, focused modules with clear contracts are easy to unit test

**Negative:**

1. **Learning curve**: Developers must understand VertexId hierarchy and when to use each ID type
2. **Indirection**: Simple ID comparisons now require understanding value objects
3. **Migration burden**: Existing `ProjectId` needs to be adapted or aliased
4. **Protocol overhead**: Runtime checkable protocols have slight performance cost

**Risks:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| ID format conflicts with external systems | Medium | Medium | JerryUri provides translation layer |
| Performance impact from frozen dataclasses | Low | Low | Benchmark before production; immutability benefits outweigh costs |
| Over-engineering for current needs | Medium | Low | Start minimal; each component has clear purpose |
| Developer confusion between ID types | Medium | Medium | Clear documentation; IDE autocomplete; architecture tests |

### Implementation Order (Dependencies)

Implementation must follow this dependency order:

```
1. First: exceptions.py (no dependencies)
   └── All other modules may raise domain exceptions

2. Then: vertex_id.py (depends on exceptions)
   └── Used by: jerry_uri.py, entity_base.py

3. Then: jerry_uri.py (depends on vertex_id - optional)
   └── Used by: external integrations

4. Then: auditable.py (no dependencies - protocol only)
   └── Used by: entity_base.py

5. Then: versioned.py (no dependencies - protocol only)
   └── Used by: entity_base.py

6. Then: entity_base.py (depends on vertex_id, auditable, versioned)
   └── Used by: all domain aggregates

7. Last: __init__.py (exports all - depends on all above)
   └── Public API surface
```

**Dependency Graph:**

```
                    ┌─────────────┐
                    │ exceptions  │
                    │ (step 1)    │
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              v                         v
       ┌─────────────┐           ┌─────────────┐
       │  vertex_id  │           │  auditable  │
       │  (step 2)   │           │  (step 4)   │
       └──────┬──────┘           └──────┬──────┘
              │                         │
    ┌─────────┴────────┐               │
    │                  │               │
    v                  v               v
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  jerry_uri  │  │  versioned  │  │  (merge)    │
│  (step 3)   │  │  (step 5)   │  │             │
└─────────────┘  └──────┬──────┘  └──────┬──────┘
                       │                │
                       └────────┬───────┘
                                │
                                v
                         ┌─────────────┐
                         │ entity_base │
                         │  (step 6)   │
                         └──────┬──────┘
                                │
                                v
                         ┌─────────────┐
                         │  __init__   │
                         │  (step 7)   │
                         └─────────────┘
```

### Migration Path for src/session_management/

The existing `src/session_management/` bounded context has `ProjectId` which does NOT extend `VertexId`. Here's the migration path:

#### Option A: Adapt ProjectId to extend VertexId (RECOMMENDED)

**File**: `src/session_management/domain/value_objects/project_id.py`

```python
# Before (current)
@dataclass(frozen=True, slots=True)
class ProjectId:
    value: str
    number: int
    slug: str

# After (migrated)
from shared_kernel import VertexId
import re

@dataclass(frozen=True)
class ProjectId(VertexId):
    """Project identifier. Format: PROJ-{nnn}-{slug}"""

    _PATTERN = re.compile(r"^PROJ-(\d{3})-([a-z0-9-]+)$")

    # Additional fields stored separately for convenience
    number: int = 0
    slug: str = ""

    def __post_init__(self):
        # Override parent post_init to extract number and slug
        match = self._PATTERN.match(self.value)
        if not match:
            raise ValueError(f"Invalid ProjectId format: {self.value}")
        object.__setattr__(self, "number", int(match.group(1)))
        object.__setattr__(self, "slug", match.group(2))

    @classmethod
    def _is_valid_format(cls, value: str) -> bool:
        return bool(cls._PATTERN.match(value))

    @classmethod
    def generate(cls) -> "ProjectId":
        raise NotImplementedError("ProjectId requires number and slug; use from_parts()")

    @classmethod
    def from_parts(cls, number: int, slug: str) -> "ProjectId":
        return cls(value=f"PROJ-{number:03d}-{slug}")
```

**Files requiring import updates:**
1. `src/session_management/domain/entities/project_info.py`
2. `src/session_management/application/queries/*.py`
3. `src/session_management/infrastructure/adapters/filesystem_project_adapter.py`

#### Option B: Create alias (TRANSITIONAL)

If full migration is delayed, create a transitional alias:

```python
# src/session_management/domain/value_objects/__init__.py
from .project_id import ProjectId

# Type alias for VertexId compatibility
# TODO: Migrate ProjectId to extend VertexId
SessionProjectId = ProjectId
```

#### Migration Steps:

1. Create `src/shared_kernel/` with all modules
2. Add `src/shared_kernel/` to Python path (update `pyproject.toml`)
3. Update `ProjectId` to extend `VertexId` (Option A)
4. Update imports in affected files
5. Run tests to verify compatibility
6. Update domain exceptions to import from shared_kernel

### Test Strategy

#### Unit Tests (per module)

| Module | Test File | Test Cases |
|--------|-----------|------------|
| `exceptions.py` | `tests/shared_kernel/test_exceptions.py` | Exception instantiation, inheritance hierarchy, message formatting |
| `vertex_id.py` | `tests/shared_kernel/test_vertex_id.py` | ID generation, format validation, equality, hashing, from_string |
| `jerry_uri.py` | `tests/shared_kernel/test_jerry_uri.py` | Parsing, construction, nested URIs, invalid inputs |
| `auditable.py` | `tests/shared_kernel/test_auditable.py` | Protocol compliance checking |
| `versioned.py` | `tests/shared_kernel/test_versioned.py` | Protocol compliance checking |
| `entity_base.py` | `tests/shared_kernel/test_entity_base.py` | Creation, touch, version increment, protocol compliance |

#### Integration Tests

| Test File | Purpose |
|-----------|---------|
| `tests/shared_kernel/test_integration.py` | Verify modules work together; EntityBase with all protocols |

#### Architecture Tests

| Test File | Purpose |
|-----------|---------|
| `tests/architecture/test_shared_kernel_dependencies.py` | Verify shared_kernel has NO external dependencies (stdlib only) |

**Sample Architecture Test:**

```python
# tests/architecture/test_shared_kernel_dependencies.py
import ast
from pathlib import Path

STDLIB_MODULES = {
    "abc", "dataclasses", "datetime", "re", "typing", "uuid",
    "__future__"
}

def test_shared_kernel_only_uses_stdlib():
    """Shared Kernel must only import from Python stdlib."""
    shared_kernel_path = Path("src/shared_kernel")

    for py_file in shared_kernel_path.glob("*.py"):
        tree = ast.parse(py_file.read_text())

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_root = alias.name.split(".")[0]
                    assert module_root in STDLIB_MODULES or module_root.startswith("."), \
                        f"{py_file.name}: imports non-stdlib '{alias.name}'"

            elif isinstance(node, ast.ImportFrom):
                if node.module and not node.module.startswith("."):
                    module_root = node.module.split(".")[0]
                    assert module_root in STDLIB_MODULES, \
                        f"{py_file.name}: imports from non-stdlib '{node.module}'"


def test_shared_kernel_no_circular_imports():
    """Verify no circular dependencies within shared_kernel."""
    # Import all modules to trigger circular import errors
    from shared_kernel import (
        DomainError, VertexId, TaskId, JerryUri,
        IAuditable, IVersioned, EntityBase
    )
    # If we get here, no circular imports
    assert True
```

---

## Implementation Guide

### Step-by-Step Instructions

#### Step 1: Create Directory Structure

```bash
mkdir -p src/shared_kernel
touch src/shared_kernel/__init__.py
touch src/shared_kernel/exceptions.py
touch src/shared_kernel/vertex_id.py
touch src/shared_kernel/jerry_uri.py
touch src/shared_kernel/auditable.py
touch src/shared_kernel/versioned.py
touch src/shared_kernel/entity_base.py
```

#### Step 2: Implement exceptions.py

Copy the code from [Interface Contracts: exceptions.py](#1-exceptionspy-pat-011-partial) above.

**Verification:**
```python
from shared_kernel.exceptions import DomainError, NotFoundError

try:
    raise NotFoundError("Task", "TASK-12345678")
except DomainError as e:
    print(e)  # "Task 'TASK-12345678' not found"
```

#### Step 3: Implement vertex_id.py

Copy the code from [Interface Contracts: vertex_id.py](#2-vertex_idpy-pat-001-pat-002-pat-004) above.

**Verification:**
```python
from shared_kernel.vertex_id import TaskId, PhaseId

task_id = TaskId.generate()
print(task_id)  # TASK-a1b2c3d4

# Invalid format should raise
try:
    TaskId("invalid")
except ValueError as e:
    print(e)  # "Invalid TaskId format: invalid"
```

#### Step 4: Implement jerry_uri.py

Copy the code from [Interface Contracts: jerry_uri.py](#3-jerry_uripy-pat-003) above.

**Verification:**
```python
from shared_kernel.jerry_uri import JerryUri

uri = JerryUri.parse("jerry://task/TASK-a1b2c3d4")
print(uri.entity_type)  # "task"
print(uri.entity_id)    # "TASK-a1b2c3d4"
```

#### Step 5: Implement auditable.py

Copy the code from [Interface Contracts: auditable.py](#4-auditablepy-pat-005) above.

#### Step 6: Implement versioned.py

Copy the code from [Interface Contracts: versioned.py](#5-versionedpy-pat-006) above.

#### Step 7: Implement entity_base.py

Copy the code from [Interface Contracts: entity_base.py](#6-entity_basepy-pat-007) above.

**Verification:**
```python
from shared_kernel.entity_base import EntityBase
from shared_kernel.vertex_id import TaskId
from shared_kernel.auditable import IAuditable
from shared_kernel.versioned import IVersioned
from dataclasses import dataclass

@dataclass
class TestEntity(EntityBase):
    name: str = ""

entity = TestEntity(_id=TaskId.generate(), name="Test")
assert isinstance(entity, IAuditable)
assert isinstance(entity, IVersioned)
print(entity.id)         # TaskId(value="TASK-...")
print(entity.version)    # 0
print(entity.created_by) # "System"
```

#### Step 8: Implement __init__.py

Copy the code from [Interface Contracts: __init__.py](#7-__init__py-public-api) above.

**Final Verification:**
```python
# All exports should work
from shared_kernel import (
    DomainError, NotFoundError, ConcurrencyError,
    VertexId, TaskId, PhaseId, PlanId, EdgeId,
    JerryUri,
    IAuditable, IVersioned,
    EntityBase
)

print("Shared Kernel implementation complete!")
```

#### Step 9: Update pyproject.toml

Add shared_kernel to the Python path:

```toml
[tool.pytest.ini_options]
pythonpath = ["src"]

[project]
packages = [
    {include = "shared_kernel", from = "src"},
    {include = "session_management", from = "src"},
]
```

#### Step 10: Create Test Infrastructure

```bash
mkdir -p tests/shared_kernel
mkdir -p tests/architecture
touch tests/shared_kernel/__init__.py
touch tests/shared_kernel/test_exceptions.py
touch tests/shared_kernel/test_vertex_id.py
touch tests/shared_kernel/test_jerry_uri.py
touch tests/shared_kernel/test_entity_base.py
touch tests/architecture/test_shared_kernel_dependencies.py
```

---

## Decision Record

| Field | Value |
|-------|-------|
| **Decision** | Create `src/shared_kernel/` module with foundational types |
| **Status** | PROPOSED |
| **Deciders** | ps-architect agent v2.0.0 |
| **Date** | 2026-01-09 |
| **Technical Debt** | TD-001: Migrate `ProjectId` to extend `VertexId` |

---

## References

### Source Documents

| ID | Title | Location |
|----|-------|----------|
| e-011-v1 | Jerry Design Canon | `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md` |
| e-012-v1 | Canon-Implementation Gap Analysis | `projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-012-v1-canon-implementation-gap.md` |

### Industry References

| Reference | URL/Citation |
|-----------|--------------|
| Domain-Driven Design | Eric Evans - Domain-Driven Design (2003), Chapter 14: "Shared Kernel" |
| Implementing DDD | Vaughn Vernon - Implementing Domain-Driven Design (2013) |
| Value Objects | Martin Fowler - https://martinfowler.com/bliki/ValueObject.html |
| Python Protocols | PEP 544 - https://peps.python.org/pep-0544/ |
| Frozen Dataclasses | Python docs - https://docs.python.org/3/library/dataclasses.html |

### Canon Pattern References

| Pattern ID | Pattern Name | Canon Lines |
|------------|--------------|-------------|
| PAT-001 | VertexId Base Class | L56-117 |
| PAT-002 | Domain-Specific IDs | L119-165 |
| PAT-003 | JerryUri | L167-220 |
| PAT-004 | EdgeId | L222-260 |
| PAT-005 | IAuditable Interface | L266-309 |
| PAT-006 | IVersioned Interface | L311-340 |
| PAT-007 | EntityBase Class | L342-407 |

---

*Document created by ps-architect agent v2.0.0*
*ADR-013 Cycle 1 completed: 2026-01-09*
*Status: PROPOSED - Ready for implementation*
