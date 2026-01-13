# ADR-013: Shared Kernel Module Implementation (Cycle 2)

> **Document ID**: PROJ-001-e-013-v2-adr-shared-kernel
> **PS ID**: PROJ-001
> **Entry ID**: e-013-v2
> **Date**: 2026-01-10
> **Author**: ps-architect agent v2.0.0 (Opus 4.5)
> **Cycle**: 2 (Implementation Complete, Extension Required)
> **Status**: ACCEPTED (Foundation) / PROPOSED (Extensions)
> **Supersedes**: PROJ-001-e-013-v1-adr-shared-kernel.md
>
> **Sources**:
> - **Canon**: `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md`
> - **Gap Analysis v2**: `projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-012-v2-canon-implementation-gap.md`
> - **Prior ADR**: `projects/PROJ-001-plugin-cleanup/decisions/PROJ-001-e-013-v1-adr-shared-kernel.md`

---

## L0: Executive Summary

### What Has Been Accomplished

The Shared Kernel foundation from ADR-013-v1 has been **successfully implemented**. The `src/shared_kernel/` module now contains 9 exported components providing:

- **Identity Layer**: Complete VertexId hierarchy (TaskId, PhaseId, PlanId, SubtaskId, KnowledgeId, ActorId, EventId, EdgeId)
- **Protocols**: IAuditable and IVersioned runtime-checkable protocols
- **Base Classes**: EntityBase combining identity, audit, and versioning
- **Events**: DomainEvent base class with EventRegistry
- **Exceptions**: Complete domain error hierarchy (7 exception types)
- **Utilities**: JerryUri for cross-system references, SnowflakeIdGenerator

**Implementation Progress**: Foundation is 100% complete. Canon compliance has improved from ~15-20% to ~40-50% overall.

### What Still Needs Implementation

Three critical gaps remain per Gap Analysis v2:

| Priority | Gap | Impact |
|----------|-----|--------|
| **P0** | CloudEvents 1.0 Envelope | External system interop blocked (ADO sync, event streaming) |
| **P1** | Graph Primitives (Vertex/Edge base classes, IGraphStore) | Graph traversal, Neo4j migration blocked |
| **P1** | CQRS Infrastructure (IProjection, IUnitOfWork) | Read-optimized queries blocked |

### Decision

**ACCEPT** the current Shared Kernel implementation as the foundation. **EXTEND** with:

1. CloudEvents 1.0 support in DomainEvent
2. Vertex and Edge base classes for graph model
3. EdgeLabels constants for semantic relationships
4. IGraphStore port interface
5. Move AggregateRoot to shared_kernel (currently in work_tracking)
6. IProjection and IUnitOfWork interfaces for CQRS

---

## Context

### Current Implementation Status

**Files Implemented in `src/shared_kernel/`**:

| File | Lines | Canon Patterns | Status |
|------|-------|----------------|--------|
| `__init__.py` | 81 | - | **COMPLETE** |
| `vertex_id.py` | 251 | PAT-ID-001, PAT-ID-002, PAT-ID-004 | **COMPLETE** |
| `jerry_uri.py` | 109 | PAT-ID-003 | **COMPLETE** |
| `auditable.py` | 53 | PAT-ENT-001 | **COMPLETE** |
| `versioned.py` | 41 | PAT-ENT-002 | **COMPLETE** |
| `entity_base.py` | 99 | PAT-ENT-007 | **COMPLETE** |
| `domain_event.py` | 261 | PAT-EVT-002 (partial) | **PARTIAL** - Missing CloudEvents |
| `exceptions.py` | 77 | - | **COMPLETE** |
| `snowflake_id.py` | ~100 | - | **BONUS** |

**Canon Pattern Compliance**:

| Category | Pass | Partial | Fail | Total |
|----------|------|---------|------|-------|
| Identity Patterns | 4 | 0 | 0 | 4 |
| Entity Patterns | 2 | 1 | 2 | 5 |
| Event Patterns | 2 | 1 | 1 | 4 |
| CQRS Patterns | 0 | 1 | 2 | 3 |
| Repository Patterns | 2 | 0 | 1 | 3 |
| Graph Patterns | 0 | 0 | 3 | 3 |
| Architecture Patterns | 2 | 1 | 0 | 3 |
| **Total** | **12** | **4** | **9** | **25** |

### Gap Analysis Findings

From Gap Analysis v2 (e-012-v2), the remaining critical gaps are:

**GAP-001: CloudEvents 1.0 Non-Compliance** (Risk Score: 20 CRITICAL)
- Current `DomainEvent.to_dict()` returns non-standard format
- Missing: `specversion`, `source`, `subject`, `datacontenttype`
- Blocks: External event streaming, ADO integration, audit interoperability

**GAP-002: Graph Primitives Missing** (Risk Score: 20 CRITICAL)
- No `Vertex` or `Edge` base classes
- No `IGraphStore` port interface
- No `EdgeLabels` constants
- Blocks: Graph-based navigation, relationship traversal, Neo4j migration

**GAP-003: AggregateRoot Misplaced** (Risk Score: 12 HIGH)
- Currently in `work_tracking/domain/aggregates/base.py`
- Should be in `shared_kernel/` for cross-context reuse
- Uses `created_on/modified_on` instead of `created_by/created_at` (not IAuditable compliant)

**GAP-005: IProjection Missing** (Risk Score: 12 HIGH)
- No projection interface for CQRS read models
- Blocks: Optimized queries, event-driven read model updates

**GAP-006: IUnitOfWork Missing** (Risk Score: 12 HIGH)
- No transaction boundary abstraction
- Blocks: Atomic multi-aggregate operations

---

## L1: Technical Decision

### Decision

Extend `src/shared_kernel/` with the following new modules:

```
src/shared_kernel/
├── __init__.py              # UPDATE: Add new exports
├── vertex_id.py             # EXISTING (no changes)
├── jerry_uri.py             # EXISTING (no changes)
├── auditable.py             # EXISTING (no changes)
├── versioned.py             # EXISTING (no changes)
├── entity_base.py           # EXISTING (no changes)
├── domain_event.py          # UPDATE: Add to_cloud_event() method
├── exceptions.py            # EXISTING (no changes)
├── snowflake_id.py          # EXISTING (no changes)
│
├── cloud_events.py          # NEW: CloudEventEnvelope wrapper
├── vertex.py                # NEW: Vertex base class (PAT-ENT-004)
├── edge.py                  # NEW: Edge base class (PAT-ENT-005)
├── edge_labels.py           # NEW: EdgeLabels constants (PAT-GRAPH-002)
├── aggregate_root.py        # NEW: Move from work_tracking (PAT-ENT-003)
├── ports/                   # NEW: Port interfaces subdirectory
│   ├── __init__.py
│   ├── graph_store.py       # NEW: IGraphStore port (PAT-GRAPH-001)
│   ├── projection.py        # NEW: IProjection interface (PAT-CQRS-003)
│   └── unit_of_work.py      # NEW: IUnitOfWork interface (PAT-REPO-002)
└── value_objects/           # NEW: Shared value objects
    ├── __init__.py
    ├── priority.py          # NEW: Priority enum (move from work_tracking)
    └── status.py            # NEW: TaskStatus, PhaseStatus, PlanStatus
```

### Implementation Order (Based on Dependencies)

```
Phase 1: CloudEvents Support (P0) - Unblocks external interop
├── 1.1 cloud_events.py (no dependencies)
├── 1.2 Update domain_event.py (depends on 1.1)
└── 1.3 Unit tests

Phase 2: Graph Primitives (P1) - Unblocks graph model
├── 2.1 vertex.py (depends on vertex_id.py)
├── 2.2 edge.py (depends on vertex.py, vertex_id.py)
├── 2.3 edge_labels.py (no dependencies)
├── 2.4 ports/graph_store.py (depends on 2.1, 2.2)
└── 2.5 Unit tests

Phase 3: Aggregate Support (P1) - Unblocks cross-context aggregates
├── 3.1 aggregate_root.py (move + refactor from work_tracking)
├── 3.2 Update work_tracking imports
└── 3.3 Unit tests

Phase 4: CQRS Infrastructure (P2) - Unblocks read optimization
├── 4.1 ports/projection.py (no dependencies)
├── 4.2 ports/unit_of_work.py (no dependencies)
├── 4.3 value_objects/priority.py (no dependencies)
├── 4.4 value_objects/status.py (no dependencies)
└── 4.5 Unit tests
```

---

### Interface Contracts

#### 1. cloud_events.py (PAT-EVT-001)

```python
"""
CloudEvents 1.0 Envelope for domain events.

Implements CNCF CloudEvents 1.0 specification for standardized
event format enabling external system interoperability.

References:
    - Canon PAT-EVT-001 (L621-667)
    - CNCF CloudEvents Spec: https://cloudevents.io/

Exports:
    CloudEventEnvelope: Wrapper for CloudEvents 1.0 format
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class CloudEventEnvelope:
    """
    CloudEvents 1.0 compliant envelope for domain events.

    Required Fields (CloudEvents Core):
        specversion: CloudEvents spec version (always "1.0")
        type: Event type in reverse-DNS notation (e.g., "com.jerry.task.created.v1")
        source: URI identifying event context (e.g., "/jerry/tasks/TASK-abc123")
        id: Unique event identifier

    Optional Fields (CloudEvents Core):
        time: RFC 3339 timestamp
        subject: Event subject (aggregate ID)
        datacontenttype: MIME type of data (default "application/json")
        data: Event payload

    Invariants:
        - specversion is always "1.0"
        - type follows "com.jerry.{aggregate}.{action}.v{version}" pattern
        - source starts with "/jerry/"
        - id format is "EVT-{uuid}"
    """

    specversion: str = "1.0"
    type: str = ""
    source: str = ""
    id: str = ""
    time: str = ""
    subject: str = ""
    datacontenttype: str = "application/json"
    data: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.specversion != "1.0":
            raise ValueError("specversion must be '1.0'")
        if not self.type:
            raise ValueError("type is required")
        if not self.source:
            raise ValueError("source is required")
        if not self.id:
            raise ValueError("id is required")

    def to_dict(self) -> dict[str, Any]:
        """Serialize to CloudEvents JSON format."""
        result = {
            "specversion": self.specversion,
            "type": self.type,
            "source": self.source,
            "id": self.id,
        }
        if self.time:
            result["time"] = self.time
        if self.subject:
            result["subject"] = self.subject
        if self.datacontenttype:
            result["datacontenttype"] = self.datacontenttype
        if self.data is not None:
            result["data"] = self.data
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CloudEventEnvelope:
        """Parse from CloudEvents JSON format."""
        return cls(
            specversion=data.get("specversion", "1.0"),
            type=data["type"],
            source=data["source"],
            id=data["id"],
            time=data.get("time", ""),
            subject=data.get("subject", ""),
            datacontenttype=data.get("datacontenttype", "application/json"),
            data=data.get("data"),
        )


def format_event_type(aggregate: str, action: str, version: int = 1) -> str:
    """
    Format CloudEvents type field.

    Args:
        aggregate: Aggregate name (e.g., "task", "phase")
        action: Action name (e.g., "created", "completed")
        version: Event version (default 1)

    Returns:
        Formatted type string: "com.jerry.{aggregate}.{action}.v{version}"

    Example:
        >>> format_event_type("task", "completed")
        'com.jerry.task.completed.v1'
    """
    return f"com.jerry.{aggregate.lower()}.{action.lower()}.v{version}"


def format_source(aggregate_type: str, aggregate_id: str) -> str:
    """
    Format CloudEvents source field.

    Args:
        aggregate_type: Type name (e.g., "Task", "Phase")
        aggregate_id: Aggregate identifier

    Returns:
        Formatted source URI: "/jerry/{type_plural}/{id}"

    Example:
        >>> format_source("Task", "TASK-abc123")
        '/jerry/tasks/TASK-abc123'
    """
    type_plural = aggregate_type.lower() + "s"
    return f"/jerry/{type_plural}/{aggregate_id}"
```

**Usage Example**:
```python
from shared_kernel.cloud_events import CloudEventEnvelope, format_event_type, format_source

envelope = CloudEventEnvelope(
    type=format_event_type("task", "completed"),
    source=format_source("Task", "TASK-abc123"),
    id="EVT-12345678-1234-1234-1234-123456789abc",
    time="2026-01-10T14:30:00Z",
    subject="TASK-abc123",
    data={"completed_at": "2026-01-10T14:30:00Z"}
)

print(envelope.to_dict())
# {
#   "specversion": "1.0",
#   "type": "com.jerry.task.completed.v1",
#   "source": "/jerry/tasks/TASK-abc123",
#   "id": "EVT-12345678-1234-1234-1234-123456789abc",
#   "time": "2026-01-10T14:30:00Z",
#   "subject": "TASK-abc123",
#   "datacontenttype": "application/json",
#   "data": {"completed_at": "2026-01-10T14:30:00Z"}
# }
```

---

#### 2. domain_event.py Updates (PAT-EVT-002)

**Add to existing DomainEvent class**:

```python
# Add import at top
from .cloud_events import CloudEventEnvelope, format_event_type, format_source

# Add method to DomainEvent class
def to_cloud_event(self) -> CloudEventEnvelope:
    """
    Convert to CloudEvents 1.0 envelope.

    Returns:
        CloudEventEnvelope with standardized format

    Example:
        >>> event = TaskCompleted(aggregate_id="TASK-abc", ...)
        >>> envelope = event.to_cloud_event()
        >>> envelope.type
        'com.jerry.task.taskcompleted.v1'
    """
    # Derive event type from class name
    class_name = self.__class__.__name__
    # Extract aggregate type from class name (e.g., TaskCompleted -> Task)
    aggregate = self.aggregate_type.lower()
    action = class_name.lower()

    return CloudEventEnvelope(
        type=format_event_type(aggregate, action),
        source=format_source(self.aggregate_type, self.aggregate_id),
        id=self.event_id,
        time=self.timestamp.isoformat() + "Z",
        subject=self.aggregate_id,
        data=self._payload(),
    )
```

---

#### 3. vertex.py (PAT-ENT-004)

```python
"""
Vertex - Base class for property graph nodes.

Implements the property graph vertex model enabling graph-based
navigation and future migration to native graph databases.

References:
    - Canon PAT-ENT-004 (L416-443)
    - TinkerPop Vertex: https://tinkerpop.apache.org/docs/current/reference/

Exports:
    Vertex: Base node class for property graph model
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .vertex_id import VertexId


@dataclass
class Vertex:
    """
    Base node class for property graph model.

    A vertex represents an entity in the graph. It has:
        - id: Unique identifier (VertexId subclass)
        - label: Type name for categorization (e.g., "Task", "Phase")
        - properties: Key-value pairs for additional data

    Invariants:
        - id is immutable once set
        - label is non-empty
        - properties keys are strings

    Usage:
        >>> vertex = Vertex(
        ...     id=TaskId.generate(),
        ...     label="Task",
        ...     properties={"title": "Implement feature", "status": "IN_PROGRESS"}
        ... )

    References:
        - Apache TinkerPop Vertex concept
        - Neo4j Node concept
    """

    id: VertexId
    label: str
    properties: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.label:
            raise ValueError("Vertex label cannot be empty")

    def get_property(self, key: str, default: Any = None) -> Any:
        """Get property value by key."""
        return self.properties.get(key, default)

    def set_property(self, key: str, value: Any) -> None:
        """Set property value."""
        self.properties[key] = value

    def has_property(self, key: str) -> bool:
        """Check if property exists."""
        return key in self.properties

    def remove_property(self, key: str) -> Any | None:
        """Remove property and return its value."""
        return self.properties.pop(key, None)

    def __hash__(self) -> int:
        """Hash by ID for set/dict usage."""
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        """Vertices are equal if they have the same ID."""
        if not isinstance(other, Vertex):
            return NotImplemented
        return self.id == other.id
```

---

#### 4. edge.py (PAT-ENT-005)

```python
"""
Edge - Base class for property graph relationships.

Implements the property graph edge model enabling directed
relationships between vertices.

References:
    - Canon PAT-ENT-005 (L445-471)
    - TinkerPop Edge: https://tinkerpop.apache.org/docs/current/reference/

Exports:
    Edge: Base relationship class for property graph model
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .vertex_id import EdgeId, VertexId


@dataclass
class Edge:
    """
    Base relationship class for property graph model.

    An edge represents a directed relationship between two vertices.
    It has:
        - id: Deterministic identifier (EdgeId from source-label-target)
        - label: Relationship type (e.g., "CONTAINS", "DEPENDS_ON")
        - out_v: Source vertex ID (outgoing vertex)
        - in_v: Target vertex ID (incoming vertex)
        - properties: Key-value pairs for additional data

    Direction Convention:
        out_v --{label}--> in_v

        Example: Phase --CONTAINS--> Task
                 out_v = PhaseId, in_v = TaskId

    Invariants:
        - id is deterministically generated from (out_v, label, in_v)
        - label is uppercase and non-empty
        - out_v and in_v are valid VertexIds

    Usage:
        >>> edge = Edge.create(
        ...     out_v=phase_id,
        ...     in_v=task_id,
        ...     label="CONTAINS",
        ...     properties={"order": 1}
        ... )

    References:
        - Apache TinkerPop Edge concept
        - Neo4j Relationship concept
    """

    id: EdgeId
    label: str
    out_v: VertexId  # Source vertex (outgoing)
    in_v: VertexId   # Target vertex (incoming)
    properties: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.label:
            raise ValueError("Edge label cannot be empty")
        if not self.label.isupper():
            raise ValueError("Edge label must be uppercase")

    @classmethod
    def create(
        cls,
        out_v: VertexId,
        in_v: VertexId,
        label: str,
        properties: dict[str, Any] | None = None,
    ) -> Edge:
        """
        Factory method to create edge with generated ID.

        Args:
            out_v: Source vertex ID
            in_v: Target vertex ID
            label: Relationship type (uppercase)
            properties: Optional edge properties

        Returns:
            New Edge instance with deterministic ID
        """
        edge_id = EdgeId(source_id=out_v, target_id=in_v, label=label)
        return cls(
            id=edge_id,
            label=label,
            out_v=out_v,
            in_v=in_v,
            properties=properties or {},
        )

    def get_property(self, key: str, default: Any = None) -> Any:
        """Get property value by key."""
        return self.properties.get(key, default)

    def set_property(self, key: str, value: Any) -> None:
        """Set property value."""
        self.properties[key] = value

    def __hash__(self) -> int:
        """Hash by ID for set/dict usage."""
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        """Edges are equal if they have the same ID."""
        if not isinstance(other, Edge):
            return NotImplemented
        return self.id == other.id
```

---

#### 5. edge_labels.py (PAT-GRAPH-002)

```python
"""
EdgeLabels - Standard edge label vocabulary.

Defines the canonical set of relationship types used in Jerry's
property graph model. All graph traversals should use these labels.

References:
    - Canon PAT-GRAPH-002 (L1282-1320)

Exports:
    EdgeLabels: Constants for graph edge labels
"""
from __future__ import annotations


class EdgeLabels:
    """
    Standard vocabulary for graph edge labels.

    Usage:
        >>> from shared_kernel.edge_labels import EdgeLabels
        >>> edge = Edge.create(phase_id, task_id, EdgeLabels.CONTAINS)

    Label Semantics:
        CONTAINS: Parent-child containment (Phase CONTAINS Task)
        BELONGS_TO: Inverse of CONTAINS (Task BELONGS_TO Phase)
        DEPENDS_ON: Dependency relationship (Task DEPENDS_ON Task)
        EMITTED: Event emission (Task EMITTED TaskCompleted)
        PERFORMED_BY: Actor attribution (Event PERFORMED_BY Actor)
        REFERENCES: Evidence linkage (Task REFERENCES Evidence)
        APPLIES: Pattern application (Task APPLIES Pattern)
        PRECEDES: Ordering relationship (Phase PRECEDES Phase)
        BLOCKS: Blocking relationship (Task BLOCKS Task)
        BLOCKED_BY: Inverse of BLOCKS (Task BLOCKED_BY Task)
    """

    # Containment relationships
    CONTAINS = "CONTAINS"
    BELONGS_TO = "BELONGS_TO"

    # Dependency relationships
    DEPENDS_ON = "DEPENDS_ON"
    BLOCKS = "BLOCKS"
    BLOCKED_BY = "BLOCKED_BY"

    # Event relationships
    EMITTED = "EMITTED"
    PERFORMED_BY = "PERFORMED_BY"

    # Reference relationships
    REFERENCES = "REFERENCES"
    APPLIES = "APPLIES"

    # Ordering relationships
    PRECEDES = "PRECEDES"
    FOLLOWS = "FOLLOWS"

    @classmethod
    def all_labels(cls) -> frozenset[str]:
        """Return all defined edge labels."""
        return frozenset({
            cls.CONTAINS, cls.BELONGS_TO,
            cls.DEPENDS_ON, cls.BLOCKS, cls.BLOCKED_BY,
            cls.EMITTED, cls.PERFORMED_BY,
            cls.REFERENCES, cls.APPLIES,
            cls.PRECEDES, cls.FOLLOWS,
        })

    @classmethod
    def is_valid(cls, label: str) -> bool:
        """Check if label is a valid EdgeLabel."""
        return label in cls.all_labels()
```

---

#### 6. ports/graph_store.py (PAT-GRAPH-001)

```python
"""
IGraphStore - Port interface for graph persistence.

Defines the secondary port for graph storage operations,
enabling abstraction over different graph implementations
(NetworkX, Neo4j, Amazon Neptune, etc.)

References:
    - Canon PAT-GRAPH-001 (L1206-1278)

Exports:
    IGraphStore: Abstract port for graph operations
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from ..vertex import Vertex
from ..edge import Edge
from ..vertex_id import VertexId, EdgeId


class IGraphStore(ABC):
    """
    Secondary port for graph persistence operations.

    Implementations:
        - NetworkXGraphStore: In-memory for development/testing
        - Neo4jGraphStore: Production graph database
        - SQLiteGraphStore: Lightweight persistence

    Thread Safety:
        Implementations should document their thread safety guarantees.

    Transaction Support:
        Complex operations may require transaction boundaries.
        See IUnitOfWork for transaction coordination.

    Usage:
        >>> graph: IGraphStore = get_graph_store()
        >>> graph.add_vertex(Vertex(id=task_id, label="Task"))
        >>> graph.add_edge(Edge.create(phase_id, task_id, "CONTAINS"))
        >>> tasks = graph.traverse(phase_id, "CONTAINS", depth=1)
    """

    # Vertex operations

    @abstractmethod
    def add_vertex(self, vertex: Vertex) -> None:
        """
        Add vertex to graph.

        Args:
            vertex: Vertex to add

        Raises:
            ValueError: If vertex with same ID already exists
        """
        ...

    @abstractmethod
    def get_vertex(self, id: VertexId) -> Vertex | None:
        """
        Retrieve vertex by ID.

        Args:
            id: Vertex identifier

        Returns:
            Vertex if found, None otherwise
        """
        ...

    @abstractmethod
    def update_vertex(self, vertex: Vertex) -> None:
        """
        Update vertex properties.

        Args:
            vertex: Vertex with updated properties

        Raises:
            NotFoundError: If vertex does not exist
        """
        ...

    @abstractmethod
    def remove_vertex(self, id: VertexId) -> bool:
        """
        Remove vertex and all connected edges.

        Args:
            id: Vertex identifier

        Returns:
            True if vertex was removed, False if not found
        """
        ...

    @abstractmethod
    def vertex_exists(self, id: VertexId) -> bool:
        """Check if vertex exists."""
        ...

    # Edge operations

    @abstractmethod
    def add_edge(self, edge: Edge) -> None:
        """
        Add edge to graph.

        Args:
            edge: Edge to add

        Raises:
            ValueError: If edge with same ID already exists
            NotFoundError: If source or target vertex does not exist
        """
        ...

    @abstractmethod
    def get_edge(self, id: EdgeId) -> Edge | None:
        """
        Retrieve edge by ID.

        Args:
            id: Edge identifier

        Returns:
            Edge if found, None otherwise
        """
        ...

    @abstractmethod
    def remove_edge(self, id: EdgeId) -> bool:
        """
        Remove edge from graph.

        Args:
            id: Edge identifier

        Returns:
            True if edge was removed, False if not found
        """
        ...

    @abstractmethod
    def get_edges(
        self,
        vertex_id: VertexId,
        direction: str = "both",
        label: str | None = None,
    ) -> Sequence[Edge]:
        """
        Get edges connected to vertex.

        Args:
            vertex_id: Vertex to query edges for
            direction: "in", "out", or "both" (default)
            label: Optional filter by edge label

        Returns:
            Sequence of matching edges
        """
        ...

    # Traversal operations

    @abstractmethod
    def traverse(
        self,
        start: VertexId,
        label: str,
        direction: str = "out",
        depth: int = 1,
    ) -> Sequence[Vertex]:
        """
        Traverse graph following edges.

        Args:
            start: Starting vertex ID
            label: Edge label to follow
            direction: "in" or "out" (default)
            depth: Maximum traversal depth (default 1)

        Returns:
            Sequence of reachable vertices

        Example:
            >>> # Get all tasks in a phase
            >>> tasks = graph.traverse(phase_id, "CONTAINS", "out", depth=1)
        """
        ...

    @abstractmethod
    def find_path(
        self,
        start: VertexId,
        end: VertexId,
        labels: Sequence[str] | None = None,
        max_depth: int = 10,
    ) -> Sequence[VertexId] | None:
        """
        Find shortest path between vertices.

        Args:
            start: Starting vertex ID
            end: Target vertex ID
            labels: Optional edge labels to follow (None = any)
            max_depth: Maximum path length

        Returns:
            Sequence of vertex IDs in path, or None if no path exists
        """
        ...

    # Query operations

    @abstractmethod
    def find_vertices_by_label(self, label: str) -> Sequence[Vertex]:
        """
        Find all vertices with given label.

        Args:
            label: Vertex label to match

        Returns:
            Sequence of matching vertices
        """
        ...

    @abstractmethod
    def count_vertices(self, label: str | None = None) -> int:
        """
        Count vertices, optionally filtered by label.

        Args:
            label: Optional label filter

        Returns:
            Count of matching vertices
        """
        ...
```

---

#### 7. ports/projection.py (PAT-CQRS-003)

```python
"""
IProjection - Port interface for CQRS read models.

Defines the contract for event-driven projections that build
read-optimized views from domain events.

References:
    - Canon PAT-CQRS-003 (L956-1010)

Exports:
    IProjection: Abstract base for read model projections
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from ..domain_event import DomainEvent


class IProjection(ABC):
    """
    Read model projection for CQRS pattern.

    Projections subscribe to domain events and build read-optimized
    views. They are eventually consistent with the write side.

    Lifecycle:
        1. Subscribe to event bus
        2. Receive events via project()
        3. Update read model state
        4. Serve queries from read model

    Rebuilding:
        If projection state is corrupted or schema changes, call
        reset() then replay all events from event store.

    Thread Safety:
        Implementations should be thread-safe for concurrent
        event processing.

    Usage:
        >>> projection = TaskListProjection(database)
        >>> for event in event_store.read_all():
        ...     projection.project(event)
        >>> tasks = projection.list_tasks(status="IN_PROGRESS")
    """

    @abstractmethod
    def project(self, event: DomainEvent) -> None:
        """
        Apply event to update projection state.

        Args:
            event: Domain event to process

        Note:
            - Must be idempotent (replaying same event produces same state)
            - Should ignore events it doesn't handle
            - Should track last processed event position
        """
        ...

    @abstractmethod
    def reset(self) -> None:
        """
        Clear projection state for rebuild.

        Called before replaying events from the beginning.
        """
        ...

    @property
    @abstractmethod
    def last_position(self) -> int:
        """
        Last processed event position.

        Used for resuming projection after restart and
        tracking how far behind the projection is.
        """
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Projection name for logging and monitoring.

        Should be unique across all projections.
        """
        ...
```

---

#### 8. ports/unit_of_work.py (PAT-REPO-002)

```python
"""
IUnitOfWork - Port interface for transaction boundaries.

Defines the contract for coordinating atomic commits across
multiple repositories and services.

References:
    - Canon PAT-REPO-002 (L1078-1131)
    - Martin Fowler: Unit of Work pattern

Exports:
    IUnitOfWork: Abstract transaction boundary
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..aggregate_root import AggregateRoot


class IUnitOfWork(ABC):
    """
    Atomic commit boundary for domain operations.

    Coordinates repository changes, event persistence, and
    event publishing within a single transaction.

    Usage:
        >>> with unit_of_work as uow:
        ...     task = task_repo.get(task_id)
        ...     task.complete()
        ...     uow.register(task)
        ...     uow.commit()

    Context Manager Protocol:
        - __enter__: Begin transaction
        - __exit__: Rollback on exception, otherwise no-op
        - commit(): Explicitly commit changes
        - rollback(): Explicitly rollback changes

    Thread Safety:
        One UnitOfWork per thread/request. Do not share across threads.
    """

    @abstractmethod
    def __enter__(self) -> IUnitOfWork:
        """Begin unit of work scope."""
        ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit unit of work scope.

        If exception occurred, rollback. Otherwise, no-op
        (explicit commit required).
        """
        ...

    @abstractmethod
    def register(self, aggregate: AggregateRoot) -> None:
        """
        Register aggregate for change tracking.

        Args:
            aggregate: Aggregate with pending events

        Note:
            Aggregates must be registered before commit to
            have their events persisted.
        """
        ...

    @abstractmethod
    def commit(self) -> None:
        """
        Commit all changes atomically.

        Order of operations:
            1. Append events to event store (with optimistic concurrency check)
            2. Update snapshots if threshold reached
            3. Publish events to event bus
            4. Clear pending events from aggregates

        Raises:
            ConcurrencyError: If optimistic concurrency check fails
        """
        ...

    @abstractmethod
    def rollback(self) -> None:
        """
        Rollback all pending changes.

        Clears registered aggregates without persisting.
        """
        ...

    @property
    @abstractmethod
    def is_committed(self) -> bool:
        """Whether this unit of work has been committed."""
        ...

    @property
    @abstractmethod
    def is_rolled_back(self) -> bool:
        """Whether this unit of work has been rolled back."""
        ...
```

---

#### 9. aggregate_root.py (PAT-ENT-003 - Moved from work_tracking)

**Changes from current work_tracking version**:

1. Move to `src/shared_kernel/aggregate_root.py`
2. Add IAuditable compliance (created_by/updated_by in addition to timestamps)
3. Add IVersioned compliance (get_expected_version method)
4. Reference shared_kernel types instead of work_tracking

```python
"""
AggregateRoot - Base class for event-sourced aggregates.

Provides the foundation for all event-sourced domain aggregates.
This is a cross-cutting concern shared across all bounded contexts.

References:
    - Canon PAT-ENT-003 (L320-412)
    - pyeventsourcing Aggregate pattern
    - DDD Aggregate pattern (Evans, 2004)

Exports:
    AggregateRoot: Abstract base class for event-sourced aggregates
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Sequence, TypeVar

from .domain_event import DomainEvent
from .vertex_id import VertexId

TAggregateRoot = TypeVar("TAggregateRoot", bound="AggregateRoot")


class AggregateRoot(ABC):
    """
    Base class for event-sourced aggregates.

    Implements:
        - IAuditable: created_by, created_at, updated_by, updated_at
        - IVersioned: version, get_expected_version()

    Lifecycle:
        1. Create: Factory method constructs via creation event
        2. Mutate: Commands call _raise_event()
        3. Apply: Events mutate state via _apply()
        4. Persist: collect_events() returns pending events
        5. Load: load_from_history() reconstructs from events

    Invariants:
        - ID is immutable once set
        - Version increments with each event
        - Events are applied in version order
    """

    _aggregate_type: str = "Aggregate"

    def __init__(self, id: VertexId) -> None:
        """Initialize aggregate with typed identity."""
        self._initialize(id)

    def _initialize(
        self,
        id: VertexId,
        version: int = 0,
        created_by: str = "System",
    ) -> None:
        """Initialize aggregate internal state."""
        self._id = id
        self._version = version
        self._pending_events: list[DomainEvent] = []
        # IAuditable fields
        self._created_by = created_by
        self._created_at: datetime | None = None
        self._updated_by = created_by
        self._updated_at: datetime | None = None

    @property
    def id(self) -> VertexId:
        """Unique identifier (VertexId subclass)."""
        return self._id

    @property
    def version(self) -> int:
        """Current version for optimistic concurrency."""
        return self._version

    def get_expected_version(self) -> int:
        """Return version for concurrency check (IVersioned)."""
        return self._version

    # IAuditable properties
    @property
    def created_by(self) -> str:
        return self._created_by

    @property
    def created_at(self) -> datetime | None:
        return self._created_at

    @property
    def updated_by(self) -> str:
        return self._updated_by

    @property
    def updated_at(self) -> datetime | None:
        return self._updated_at

    def _raise_event(self, event: DomainEvent) -> None:
        """
        Record a new domain event.

        Increments version, applies event, adds to pending list.
        """
        self._version += 1
        self._apply(event)
        self._pending_events.append(event)
        self._updated_at = event.timestamp
        self._updated_by = getattr(event, 'caused_by', 'System')

        if self._created_at is None:
            self._created_at = event.timestamp
            self._created_by = getattr(event, 'caused_by', 'System')

    @abstractmethod
    def _apply(self, event: DomainEvent) -> None:
        """Apply event to update aggregate state."""
        ...

    def collect_events(self) -> Sequence[DomainEvent]:
        """Return and clear pending events."""
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    def has_pending_events(self) -> bool:
        """Check if there are uncommitted events."""
        return len(self._pending_events) > 0

    @classmethod
    def load_from_history(
        cls: type[TAggregateRoot],
        events: Sequence[DomainEvent],
    ) -> TAggregateRoot:
        """Reconstruct aggregate by replaying events."""
        if not events:
            raise ValueError("Cannot load from empty event history")

        aggregate = cls.__new__(cls)
        first_event = events[0]

        # Initialize with ID from first event
        # Note: Subclasses must handle ID type conversion
        aggregate._id = cls._extract_id(first_event)
        aggregate._version = 0
        aggregate._pending_events = []
        aggregate._created_at = first_event.timestamp
        aggregate._created_by = getattr(first_event, 'caused_by', 'System')
        aggregate._updated_at = None
        aggregate._updated_by = aggregate._created_by

        for event in events:
            aggregate._version = event.version
            aggregate._apply(event)
            aggregate._updated_at = event.timestamp
            aggregate._updated_by = getattr(event, 'caused_by', 'System')

        return aggregate

    @classmethod
    def _extract_id(cls, event: DomainEvent) -> VertexId:
        """
        Extract typed ID from creation event.

        Override in subclasses to return proper VertexId subclass.
        Default implementation raises NotImplementedError.
        """
        raise NotImplementedError(
            f"{cls.__name__} must implement _extract_id() to convert "
            f"event.aggregate_id to proper VertexId subclass"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AggregateRoot):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)
```

---

#### 10. Updated __init__.py

```python
"""
Shared Kernel - Cross-cutting value objects for Jerry Framework.

This module contains foundational types shared across all bounded contexts:
- Identity: VertexId hierarchy, EdgeId, JerryUri
- Graph: Vertex, Edge, EdgeLabels
- Audit: IAuditable protocol
- Concurrency: IVersioned protocol
- Base classes: EntityBase, AggregateRoot
- Events: DomainEvent, CloudEventEnvelope
- Exceptions: Domain error hierarchy
- Ports: IGraphStore, IProjection, IUnitOfWork

References:
    - Canon Section "Shared Kernel Specification" (L1769-1948)
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
from .snowflake_id import SnowflakeIdGenerator

# Graph primitives
from .vertex import Vertex
from .edge import Edge
from .edge_labels import EdgeLabels

# Events
from .domain_event import DomainEvent, EventRegistry, get_global_registry
from .cloud_events import CloudEventEnvelope, format_event_type, format_source

# Protocols
from .auditable import IAuditable
from .versioned import IVersioned

# Base classes
from .entity_base import EntityBase
from .aggregate_root import AggregateRoot

# Ports
from .ports import IGraphStore, IProjection, IUnitOfWork


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
    "SnowflakeIdGenerator",
    # Graph primitives
    "Vertex",
    "Edge",
    "EdgeLabels",
    # Events
    "DomainEvent",
    "EventRegistry",
    "get_global_registry",
    "CloudEventEnvelope",
    "format_event_type",
    "format_source",
    # Protocols
    "IAuditable",
    "IVersioned",
    # Base classes
    "EntityBase",
    "AggregateRoot",
    # Ports
    "IGraphStore",
    "IProjection",
    "IUnitOfWork",
]
```

---

## L2: Strategic Implications

### Consequences

**Positive**:

1. **CloudEvents 1.0 compliance** enables:
   - ADO integration via webhook events
   - External event streaming to Kafka/RabbitMQ
   - Standardized audit trail format

2. **Graph primitives** enable:
   - Relationship-based navigation (Plan -> Phase -> Task)
   - Dependency graph analysis
   - Future migration to Neo4j/Amazon Neptune

3. **Centralized AggregateRoot** enables:
   - Consistent event sourcing across all bounded contexts
   - IAuditable/IVersioned compliance everywhere
   - Reduced code duplication

4. **CQRS ports** enable:
   - Read-optimized projections for fast queries
   - Event-driven read model updates
   - Atomic transaction coordination

**Negative**:

1. **Migration effort**: work_tracking must update imports after AggregateRoot move
2. **Learning curve**: Graph concepts (Vertex, Edge, traversal) require documentation
3. **Complexity**: More moving parts in shared_kernel

### Migration Path for work_tracking

After implementing Phase 3 (AggregateRoot move):

1. Update imports in `src/work_tracking/domain/aggregates/`:
   ```python
   # Before
   from src.work_tracking.domain.aggregates.base import AggregateRoot

   # After
   from src.shared_kernel import AggregateRoot
   ```

2. Update WorkItem to use typed VertexId:
   ```python
   # Before
   def __init__(self, id: str) -> None:

   # After
   from src.shared_kernel import TaskId

   def __init__(self, id: TaskId) -> None:
   ```

3. Implement `_extract_id` class method in WorkItem

### Test Requirements

| Component | Test File | Test Cases |
|-----------|-----------|------------|
| CloudEventEnvelope | `tests/shared_kernel/test_cloud_events.py` | Envelope creation, to_dict, from_dict, format_event_type, format_source |
| DomainEvent.to_cloud_event | `tests/shared_kernel/test_domain_event.py` | CloudEvents conversion for various event types |
| Vertex | `tests/shared_kernel/test_vertex.py` | Creation, properties, equality, hashing |
| Edge | `tests/shared_kernel/test_edge.py` | Creation, factory method, properties, equality |
| EdgeLabels | `tests/shared_kernel/test_edge_labels.py` | All labels defined, is_valid() |
| IGraphStore | `tests/shared_kernel/test_graph_store_contract.py` | Contract tests for adapter compliance |
| IProjection | `tests/shared_kernel/test_projection_contract.py` | Contract tests |
| IUnitOfWork | `tests/shared_kernel/test_unit_of_work_contract.py` | Contract tests |
| AggregateRoot | `tests/shared_kernel/test_aggregate_root.py` | Event lifecycle, history replay, IAuditable/IVersioned compliance |

### Architecture Tests

Add to `tests/architecture/test_shared_kernel_dependencies.py`:

```python
def test_shared_kernel_only_uses_stdlib():
    """Shared Kernel must only import from Python stdlib."""
    ALLOWED_STDLIB = {
        "abc", "dataclasses", "datetime", "re", "typing", "uuid",
        "__future__", "enum"
    }
    # ... (validation logic)

def test_shared_kernel_ports_have_no_implementation():
    """Port interfaces must be abstract with no concrete logic."""
    # Verify IGraphStore, IProjection, IUnitOfWork are pure ABCs
```

---

## Implementation Checklist

### Phase 1: CloudEvents Support (P0)

- [ ] Create `src/shared_kernel/cloud_events.py`
- [ ] Add `to_cloud_event()` to `src/shared_kernel/domain_event.py`
- [ ] Create `tests/shared_kernel/test_cloud_events.py`
- [ ] Verify CloudEvents JSON schema compliance

### Phase 2: Graph Primitives (P1)

- [ ] Create `src/shared_kernel/vertex.py`
- [ ] Create `src/shared_kernel/edge.py`
- [ ] Create `src/shared_kernel/edge_labels.py`
- [ ] Create `src/shared_kernel/ports/__init__.py`
- [ ] Create `src/shared_kernel/ports/graph_store.py`
- [ ] Create tests for all graph components

### Phase 3: Aggregate Support (P1)

- [ ] Create `src/shared_kernel/aggregate_root.py` (adapted from work_tracking)
- [ ] Update `src/work_tracking/domain/aggregates/base.py` to re-export or deprecate
- [ ] Update imports in work_tracking aggregates
- [ ] Create `tests/shared_kernel/test_aggregate_root.py`

### Phase 4: CQRS Infrastructure (P2)

- [ ] Create `src/shared_kernel/ports/projection.py`
- [ ] Create `src/shared_kernel/ports/unit_of_work.py`
- [ ] Create `src/shared_kernel/value_objects/__init__.py`
- [ ] Create `src/shared_kernel/value_objects/priority.py`
- [ ] Create `src/shared_kernel/value_objects/status.py`
- [ ] Create tests for CQRS ports

### Phase 5: Final Integration

- [ ] Update `src/shared_kernel/__init__.py` with all new exports
- [ ] Update architecture tests
- [ ] Run full test suite
- [ ] Update CLAUDE.md if needed

---

## Decision Record

| Field | Value |
|-------|-------|
| **Decision** | Extend shared_kernel with CloudEvents, Graph primitives, and CQRS ports |
| **Status** | PROPOSED (Extensions) / ACCEPTED (Foundation) |
| **Deciders** | ps-architect agent v2.0.0 |
| **Date** | 2026-01-10 |
| **Supersedes** | PROJ-001-e-013-v1-adr-shared-kernel.md |

---

## References

### Source Documents

| ID | Title | Location |
|----|-------|----------|
| e-011-v1 | Jerry Design Canon v1.0 | `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md` |
| e-012-v2 | Gap Analysis v2 | `projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-012-v2-canon-implementation-gap.md` |
| e-013-v1 | Prior ADR | `projects/PROJ-001-plugin-cleanup/decisions/PROJ-001-e-013-v1-adr-shared-kernel.md` |

### Canon Pattern References

| Pattern ID | Pattern Name | Canon Lines | Status |
|------------|--------------|-------------|--------|
| PAT-EVT-001 | CloudEvents Envelope | L621-667 | **PROPOSED** |
| PAT-ENT-003 | AggregateRoot | L320-412 | **PROPOSED** (move) |
| PAT-ENT-004 | Vertex | L416-443 | **PROPOSED** |
| PAT-ENT-005 | Edge | L445-471 | **PROPOSED** |
| PAT-GRAPH-001 | IGraphStore | L1206-1278 | **PROPOSED** |
| PAT-GRAPH-002 | EdgeLabels | L1282-1320 | **PROPOSED** |
| PAT-CQRS-003 | IProjection | L956-1010 | **PROPOSED** |
| PAT-REPO-002 | IUnitOfWork | L1078-1131 | **PROPOSED** |

### Industry References

| Reference | URL/Citation |
|-----------|--------------|
| CNCF CloudEvents 1.0 | https://cloudevents.io/ |
| Apache TinkerPop | https://tinkerpop.apache.org/ |
| Martin Fowler - Unit of Work | https://martinfowler.com/eaaCatalog/unitOfWork.html |
| CQRS Pattern | https://martinfowler.com/bliki/CQRS.html |

---

*Document created by ps-architect agent v2.0.0*
*ADR-013 Cycle 2 completed: 2026-01-10*
*Status: PROPOSED - Ready for implementation*
