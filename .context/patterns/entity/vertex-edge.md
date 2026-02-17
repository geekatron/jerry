# PAT-ENT-005: Vertex and Edge Pattern

> **Status**: RECOMMENDED
> **Category**: Entity Pattern
> **Location**: Future implementation

---

## Overview

The Vertex and Edge pattern enables graph-based modeling of domain relationships. Vertices represent entities, and Edges represent typed relationships between them.

This pattern supports:
- Knowledge graphs (entities linked by semantic relationships)
- Dependency graphs (work items depending on each other)
- Hierarchy traversal (parent-child relationships)

---

## Industry Prior Art

| Source | Key Insight |
|--------|-------------|
| **Property Graph Model** | "Nodes (vertices) have properties and labels; edges have types, direction, and properties" |
| **Apache TinkerPop** | "Gremlin traversal language for graph queries" |
| **Neo4j** | "Labeled property graphs with first-class relationships" |
| **Event Sourcing + Graphs** | "Edge changes can be event-sourced like entity changes" |

---

## Jerry Implementation

### Vertex Base

```python
# File: src/shared_kernel/graph/vertex.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from src.shared_kernel.entity_base import EntityBase
from src.shared_kernel.vertex_id import VertexId

if TYPE_CHECKING:
    from src.shared_kernel.graph.edge import Edge


@dataclass
class Vertex(EntityBase):
    """Graph-ready entity base.

    Extends EntityBase with graph navigation capabilities.
    Vertices can have incoming and outgoing edges.

    Usage:
        @dataclass
        class Task(Vertex):
            title: str

        task1 = Task.create(title="Research")
        task2 = Task.create(title="Implement")
        edge = Edge.create(task1.id, task2.id, EdgeLabel.BLOCKS)

    References:
        - PAT-ID-001: VertexId pattern
        - PAT-ENT-004: EntityBase pattern
        - PAT-ID-004: EdgeId pattern
    """

    _outgoing_edge_ids: list[str] = field(default_factory=list)
    _incoming_edge_ids: list[str] = field(default_factory=list)

    @property
    def outgoing_edges(self) -> list[str]:
        """IDs of edges originating from this vertex."""
        return self._outgoing_edge_ids.copy()

    @property
    def incoming_edges(self) -> list[str]:
        """IDs of edges pointing to this vertex."""
        return self._incoming_edge_ids.copy()

    def add_outgoing_edge(self, edge_id: str) -> None:
        """Record an outgoing edge."""
        if edge_id not in self._outgoing_edge_ids:
            self._outgoing_edge_ids.append(edge_id)
            self._mark_updated()

    def add_incoming_edge(self, edge_id: str) -> None:
        """Record an incoming edge."""
        if edge_id not in self._incoming_edge_ids:
            self._incoming_edge_ids.append(edge_id)
            self._mark_updated()

    def remove_outgoing_edge(self, edge_id: str) -> None:
        """Remove an outgoing edge reference."""
        if edge_id in self._outgoing_edge_ids:
            self._outgoing_edge_ids.remove(edge_id)
            self._mark_updated()

    def remove_incoming_edge(self, edge_id: str) -> None:
        """Remove an incoming edge reference."""
        if edge_id in self._incoming_edge_ids:
            self._incoming_edge_ids.remove(edge_id)
            self._mark_updated()
```

### Edge

```python
# File: src/shared_kernel/graph/edge.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class EdgeLabel(str, Enum):
    """Standardized relationship types.

    Semantic edges for domain relationships.
    """

    # Dependency relationships
    BLOCKS = "blocks"           # Source blocks target
    DEPENDS_ON = "depends_on"   # Source depends on target

    # Hierarchy relationships
    PARENT_OF = "parent_of"     # Source is parent of target
    CHILD_OF = "child_of"       # Source is child of target

    # Association relationships
    RELATED_TO = "related_to"   # General relationship
    REFERENCES = "references"   # Source references target

    # Ownership relationships
    OWNS = "owns"               # Source owns target
    BELONGS_TO = "belongs_to"   # Source belongs to target

    # Workflow relationships
    PRECEDES = "precedes"       # Source comes before target
    FOLLOWS = "follows"         # Source comes after target


@dataclass(frozen=True)
class EdgeId:
    """Compound identity for graph relationships.

    Format: {source_id}--{label}-->{target_id}

    Examples:
        - TASK-abc12345--blocks-->TASK-def67890
        - PHASE-001--parent_of-->TASK-abc12345
    """

    source_id: str
    target_id: str
    label: EdgeLabel

    @property
    def value(self) -> str:
        """String representation of edge ID."""
        return f"{self.source_id}--{self.label.value}-->{self.target_id}"

    @classmethod
    def from_string(cls, value: str) -> EdgeId:
        """Parse edge ID from string."""
        parts = value.split("-->")
        if len(parts) != 2:
            raise ValueError(f"Invalid edge ID format: {value}")

        source_and_label = parts[0].rsplit("--", 1)
        if len(source_and_label) != 2:
            raise ValueError(f"Invalid edge ID format: {value}")

        return cls(
            source_id=source_and_label[0],
            label=EdgeLabel(source_and_label[1]),
            target_id=parts[1],
        )


@dataclass
class Edge:
    """Graph edge representing a relationship between vertices.

    Edges are first-class domain objects with:
    - Identity (EdgeId)
    - Direction (source -> target)
    - Label (relationship type)
    - Properties (metadata)
    - Timestamps (created_at)

    References:
        - PAT-ID-004: EdgeId pattern
        - PAT-ENT-005: Vertex pattern
    """

    _id: EdgeId
    _properties: dict[str, Any] = field(default_factory=dict)
    _created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @property
    def id(self) -> EdgeId:
        """Edge identity."""
        return self._id

    @property
    def source_id(self) -> str:
        """Source vertex ID."""
        return self._id.source_id

    @property
    def target_id(self) -> str:
        """Target vertex ID."""
        return self._id.target_id

    @property
    def label(self) -> EdgeLabel:
        """Relationship type."""
        return self._id.label

    @property
    def properties(self) -> dict[str, Any]:
        """Edge properties/metadata."""
        return self._properties.copy()

    @classmethod
    def create(
        cls,
        source_id: str,
        target_id: str,
        label: EdgeLabel,
        properties: dict[str, Any] | None = None,
    ) -> Edge:
        """Factory method to create new edge."""
        return cls(
            _id=EdgeId(
                source_id=source_id,
                target_id=target_id,
                label=label,
            ),
            _properties=properties or {},
        )

    def with_property(self, key: str, value: Any) -> Edge:
        """Return new edge with added property (immutable update)."""
        new_properties = self._properties.copy()
        new_properties[key] = value
        return Edge(
            _id=self._id,
            _properties=new_properties,
            _created_at=self._created_at,
        )
```

---

## Graph Store Port

```python
# File: src/domain/ports/graph_store.py
from typing import Protocol, Sequence

from src.shared_kernel.graph.edge import Edge, EdgeLabel
from src.shared_kernel.vertex_id import VertexId


class IGraphStore(Protocol):
    """Port for graph persistence.

    Enables graph queries without coupling to specific graph database.
    """

    def add_edge(self, edge: Edge) -> None:
        """Add edge to graph."""
        ...

    def remove_edge(self, source_id: str, target_id: str, label: EdgeLabel) -> bool:
        """Remove edge. Returns True if edge existed."""
        ...

    def get_outgoing(
        self,
        vertex_id: str,
        label: EdgeLabel | None = None,
    ) -> Sequence[Edge]:
        """Get edges originating from vertex."""
        ...

    def get_incoming(
        self,
        vertex_id: str,
        label: EdgeLabel | None = None,
    ) -> Sequence[Edge]:
        """Get edges pointing to vertex."""
        ...

    def traverse(
        self,
        start_id: str,
        labels: Sequence[EdgeLabel],
        max_depth: int = 3,
    ) -> Sequence[str]:
        """Traverse graph following specified edge labels.

        Returns list of vertex IDs reachable from start.
        """
        ...
```

---

## Usage Examples

### Dependency Tracking

```python
# Task dependencies
task1 = Task.create(title="Design API")
task2 = Task.create(title="Implement API")
task3 = Task.create(title="Test API")

# task2 depends on task1, task3 depends on task2
edge1 = Edge.create(task2.id, task1.id, EdgeLabel.DEPENDS_ON)
edge2 = Edge.create(task3.id, task2.id, EdgeLabel.DEPENDS_ON)

graph_store.add_edge(edge1)
graph_store.add_edge(edge2)

# Find all dependencies of task3
deps = graph_store.traverse(
    start_id=str(task3.id),
    labels=[EdgeLabel.DEPENDS_ON],
    max_depth=10,
)
# Returns: [task2.id, task1.id]
```

### Hierarchy Navigation

```python
# Phase contains tasks
phase = Phase.create(title="Phase 1")
task1 = Task.create(title="Task 1.1")
task2 = Task.create(title="Task 1.2")

edge1 = Edge.create(phase.id, task1.id, EdgeLabel.PARENT_OF)
edge2 = Edge.create(phase.id, task2.id, EdgeLabel.PARENT_OF)

# Find all children of phase
children = graph_store.get_outgoing(
    vertex_id=str(phase.id),
    label=EdgeLabel.PARENT_OF,
)
```

### Knowledge Graph

```python
# Link knowledge to tasks
lesson = Knowledge.create(type="lesson_learned", content="...")
task = Task.create(title="Implementation")

edge = Edge.create(
    source_id=str(lesson.id),
    target_id=str(task.id),
    label=EdgeLabel.REFERENCES,
    properties={"relevance": 0.95},
)
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Edge labels are domain-specific enums, not arbitrary strings. This ensures consistent semantics across the system.

> **Jerry Decision**: Edges are immutable with copy-on-modify pattern (`with_property()`). This aligns with event sourcing principles.

> **Jerry Decision**: Graph traversal is limited to 3 levels by default to prevent runaway queries.

---

## Gremlin Compatibility

The graph model is designed for future Gremlin compatibility:

```python
# Jerry graph model maps to Gremlin concepts
# Vertex -> g.V()
# Edge -> g.E()
# EdgeLabel -> edge labels
# traverse() -> g.V().out().out()...

# Example Gremlin equivalent
# graph_store.traverse(task_id, [DEPENDS_ON], max_depth=2)
# g.V(task_id).out('depends_on').out('depends_on')
```

---

## Testing Pattern

```python
def test_edge_creates_with_correct_id_format():
    """Edge ID follows compound format."""
    edge = Edge.create(
        source_id="TASK-abc12345",
        target_id="TASK-def67890",
        label=EdgeLabel.BLOCKS,
    )

    assert edge.id.value == "TASK-abc12345--blocks-->TASK-def67890"


def test_edge_id_parses_from_string():
    """EdgeId can be parsed from string representation."""
    edge_id = EdgeId.from_string("TASK-abc--depends_on-->TASK-def")

    assert edge_id.source_id == "TASK-abc"
    assert edge_id.target_id == "TASK-def"
    assert edge_id.label == EdgeLabel.DEPENDS_ON


def test_traverse_follows_edge_chain():
    """Graph traversal follows edge chains."""
    graph = InMemoryGraphStore()

    graph.add_edge(Edge.create("A", "B", EdgeLabel.DEPENDS_ON))
    graph.add_edge(Edge.create("B", "C", EdgeLabel.DEPENDS_ON))
    graph.add_edge(Edge.create("C", "D", EdgeLabel.DEPENDS_ON))

    result = graph.traverse("A", [EdgeLabel.DEPENDS_ON], max_depth=3)

    assert result == ["B", "C", "D"]
```

---

## References

- **Apache TinkerPop**: [Gremlin Documentation](https://tinkerpop.apache.org/gremlin.html)
- **Neo4j**: [Graph Data Modeling](https://neo4j.com/developer/data-modeling/)
- **Design Canon**: Section 5.6 - Graph Patterns
- **Related Patterns**: PAT-ID-001 (VertexId), PAT-ID-004 (EdgeId), PAT-ENT-004 (EntityBase)
