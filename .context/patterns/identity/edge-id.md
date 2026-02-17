# PAT-ID-004: EdgeId Pattern

> **Status**: MANDATORY
> **Category**: Identity
> **Also Known As**: Relationship Identity, Compound Edge Key

---

## Intent

Generate deterministic identifiers for graph edges from source vertex, label, and target vertex.

---

## Problem

Without edge identification:
- Edges are relationships without unique identity
- Retrieval and updates are ambiguous
- No consistent naming scheme for relationships
- Graph traversal lacks predictable edge identification

---

## Solution

Generate edge IDs deterministically from source vertex, label, and target vertex.

### Edge ID Format

```
{outV}--{label}-->{inV}

Examples:
PHASE-001--CONTAINS-->TASK-001
TASK-ABC--DEPENDS_ON-->TASK-XYZ
PLAN-001--HAS_PHASE-->PHASE-001
```

### Implementation

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class EdgeId:
    """Generated identifier for graph edges.

    EdgeId is deterministic - the same source, label, and target
    always produce the same EdgeId. This enables idempotent edge
    operations.
    """
    source_id: VertexId
    label: str
    target_id: VertexId

    def __str__(self) -> str:
        return f"{self.source_id}--{self.label}-->{self.target_id}"

    def __hash__(self) -> int:
        return hash((str(self.source_id), self.label, str(self.target_id)))

    @classmethod
    def create(
        cls,
        source: VertexId,
        label: str,
        target: VertexId
    ) -> 'EdgeId':
        """Factory method for creating EdgeId.

        Args:
            source: Source vertex ID (outV)
            label: Edge label (relationship type)
            target: Target vertex ID (inV)

        Returns:
            Deterministic EdgeId
        """
        return cls(source_id=source, label=label, target_id=target)

    @classmethod
    def parse(cls, edge_id_string: str) -> 'EdgeId':
        """Parse EdgeId from string representation.

        Args:
            edge_id_string: String in format "source--label-->target"

        Returns:
            Parsed EdgeId

        Raises:
            ValueError: If format is invalid
        """
        import re
        pattern = r'^(.+)--(.+)-->(.+)$'
        match = re.match(pattern, edge_id_string)

        if not match:
            raise ValueError(f"Invalid EdgeId format: {edge_id_string}")

        return cls(
            source_id=VertexId(match.group(1)),
            label=match.group(2),
            target_id=VertexId(match.group(3))
        )
```

---

## Jerry Implementation

### File Location

`src/shared_kernel/identity/edge_id.py`

### Edge Label Vocabulary

See [PAT-GRAPH-002: Edge Labels](../graph/edge-labels.md) for the complete label vocabulary.

| Label | Semantics | Direction |
|-------|-----------|-----------|
| CONTAINS | Parent has child | parent -> child |
| BELONGS_TO | Child references parent | child -> parent |
| DEPENDS_ON | Dependency relationship | source -> target |
| EMITTED | Aggregate produced event | aggregate -> event |
| PERFORMED_BY | Actor attribution | event -> actor |

---

## Consequences

| Type | Consequence |
|------|-------------|
| (+) | Deterministic - same inputs always produce same ID |
| (+) | Human-readable edge identification |
| (+) | Enables idempotent edge operations |
| (+) | Self-documenting relationship semantics |
| (-) | Longer than simple UUIDs |

---

## Usage Examples

```python
# Create edge ID
edge_id = EdgeId.create(
    source=PhaseId("PHASE-001"),
    label="CONTAINS",
    target=TaskId("TASK-001")
)
print(edge_id)  # PHASE-001--CONTAINS-->TASK-001

# Parse from string
edge_id = EdgeId.parse("TASK-ABC--DEPENDS_ON-->TASK-XYZ")

# Use in graph operations
graph_store.add_edge(edge_id, properties={"created_at": now})
```

---

## Related Patterns

- [PAT-ID-001: VertexId](./vertex-id.md) - Base vertex identity
- [PAT-GRAPH-002: Edge Labels](../graph/edge-labels.md) - Label vocabulary
- [PAT-ENT-005: Edge](../entity/edge.md) - Edge entity class

---

## Design Canon Reference

Lines 220-258 in Jerry Design Canon v1.0

---

*Pattern documented by Claude (Opus 4.5) as part of TD-017*
