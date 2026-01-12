# Jerry Pattern Catalog

> Comprehensive index of architecture and design patterns used in Jerry.
> This catalog provides quick reference and links to authoritative sources.

**Last Updated**: 2026-01-12
**Authoritative Source**: `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md`
**Total Patterns**: 31 patterns across 9 categories

---

## Quick Reference

| Category | Count | Patterns |
|----------|-------|----------|
| [Identity](#identity-patterns) | 4 | VertexId, Domain-Specific IDs, JerryUri, EdgeId |
| [Entity](#entity-patterns) | 5 | IAuditable, IVersioned, AggregateRoot, Vertex, Edge |
| [Aggregate](#aggregate-patterns) | 4 | Task, Phase, Plan, Knowledge |
| [Event](#event-patterns) | 4 | CloudEvents, DomainEvent, Work Tracker Events, IEventStore |
| [CQRS](#cqrs-patterns) | 3 | Command, Query, Projection |
| [Repository](#repository-patterns) | 3 | Generic Repository, Unit of Work, Snapshot |
| [Graph](#graph-patterns) | 3 | IGraphStore, Edge Labels, Gremlin Compatibility |
| [Architecture](#architecture-patterns) | 3 | Hexagonal, Ports, Bounded Contexts |
| [Testing](#testing-patterns) | 3 | BDD, Test Pyramid, Architecture Tests |

---

## Identity Patterns

### PAT-ID-001: VertexId (Base Identity)
**Status**: MANDATORY | **Category**: Identity

Base identity for all domain entities. Implements snowflake-based globally unique IDs.

**Location**: `src/shared_kernel/identity/vertex_id.py`

```python
@dataclass(frozen=True)
class VertexId:
    value: int  # Snowflake ID

    @classmethod
    def generate(cls) -> "VertexId":
        return cls(value=SnowflakeIdGenerator.generate())
```

**Design Canon Reference**: Lines 180-220

---

### PAT-ID-002: Domain-Specific IDs
**Status**: MANDATORY | **Category**: Identity

Extend VertexId for type-safe domain-specific identifiers.

**Pattern**:
```python
@dataclass(frozen=True)
class ProjectId(VertexId):
    """Project-specific identifier with slug."""
    slug: str

    @classmethod
    def from_string(cls, value: str) -> "ProjectId":
        # Parse PROJ-NNN-slug format
```

**Examples**: `ProjectId`, `SessionId`, `WorkItemId`, `TaskId`

**Design Canon Reference**: Lines 221-280

---

### PAT-ID-003: JerryUri
**Status**: RECOMMENDED | **Category**: Identity

Unified resource identifier for cross-system references.

**Format**: `jerry://{context}/{type}/{id}[?version={n}]`

**Examples**:
- `jerry://session-management/project/PROJ-001-plugin-cleanup`
- `jerry://work-tracking/task/12345?version=3`

**Design Canon Reference**: Lines 281-320

---

### PAT-ID-004: EdgeId
**Status**: RECOMMENDED | **Category**: Identity

Compound identity for graph relationships.

**Structure**:
```python
@dataclass(frozen=True)
class EdgeId:
    source_id: VertexId
    target_id: VertexId
    label: EdgeLabel
```

**Design Canon Reference**: Lines 321-350

---

## Entity Patterns

### PAT-ENT-001: IAuditable Protocol
**Status**: MANDATORY | **Category**: Entity

Protocol for audit metadata on entities.

```python
@runtime_checkable
class IAuditable(Protocol):
    created_at: datetime
    created_by: str
    modified_at: datetime | None
    modified_by: str | None
```

**Design Canon Reference**: Lines 360-400

---

### PAT-ENT-002: IVersioned Protocol
**Status**: MANDATORY | **Category**: Entity

Protocol for optimistic concurrency control.

```python
@runtime_checkable
class IVersioned(Protocol):
    version: int

    def increment_version(self) -> None: ...
```

**Design Canon Reference**: Lines 401-440

---

### PAT-ENT-003: AggregateRoot Base
**Status**: MANDATORY | **Category**: Entity

Base class for domain aggregates with event sourcing support.

```python
class AggregateRoot(ABC):
    _events: list[DomainEvent]
    _version: int

    def apply_event(self, event: DomainEvent) -> None: ...
    def collect_events(self) -> list[DomainEvent]: ...
```

**Location**: `src/shared_kernel/domain/aggregate_root.py`

**Design Canon Reference**: Lines 441-520

---

### PAT-ENT-004: Vertex (Graph Entity)
**Status**: RECOMMENDED | **Category**: Entity

Base for entities that participate in graph relationships.

**Properties**: `id: VertexId`, `labels: set[str]`, `properties: dict`

**Design Canon Reference**: Lines 521-560

---

### PAT-ENT-005: Edge (Graph Relationship)
**Status**: RECOMMENDED | **Category**: Entity

Graph relationship between vertices.

**Properties**: `id: EdgeId`, `source: Vertex`, `target: Vertex`, `label: EdgeLabel`

**Design Canon Reference**: Lines 561-600

---

## Aggregate Patterns

### PAT-AGG-001: Task Aggregate
**Status**: MANDATORY | **Category**: Aggregate

Core work tracking aggregate.

**Invariants**:
- Status transitions follow state machine
- Completed tasks cannot be modified
- Parent-child relationships maintain consistency

**Events**: `TaskCreated`, `TaskStarted`, `TaskCompleted`, `TaskBlocked`

**Design Canon Reference**: Lines 610-700

---

### PAT-AGG-002: Phase Aggregate
**Status**: RECOMMENDED | **Category**: Aggregate

Groups related tasks into phases.

**Invariants**:
- Phase complete only when all tasks complete
- Phases maintain order

**Design Canon Reference**: Lines 701-750

---

### PAT-AGG-003: Plan Aggregate
**Status**: RECOMMENDED | **Category**: Aggregate

Top-level aggregate organizing phases.

**Design Canon Reference**: Lines 751-800

---

### PAT-AGG-004: Knowledge Aggregate
**Status**: RECOMMENDED | **Category**: Aggregate

Captures patterns, lessons, assumptions.

**Types**: `Pattern`, `Lesson`, `Assumption`

**Design Canon Reference**: Lines 801-850

---

## Event Patterns

### PAT-EVT-001: CloudEvents Envelope
**Status**: MANDATORY | **Category**: Event

Standard envelope for external event interchange.

**Location**: Interface layer only (`src/interface/`)

```python
# Use cloudevents SDK for protocol bindings
from cloudevents.http import CloudEvent
```

**ADR**: `decisions/PROJ-001-e-016-v1-adr-cloudevents-sdk.md`

**Design Canon Reference**: Lines 860-920

---

### PAT-EVT-002: DomainEvent Base
**Status**: MANDATORY | **Category**: Event

Base class for all domain events.

**Location**: `src/shared_kernel/events/domain_event.py`

```python
@dataclass(frozen=True)
class DomainEvent:
    event_id: str
    occurred_at: datetime
    aggregate_id: str
    aggregate_type: str
```

**Design Canon Reference**: Lines 921-980

---

### PAT-EVT-003: Work Tracker Events
**Status**: MANDATORY | **Category**: Event

Domain events for work tracking.

**Events**:
- `WorkItemCreated`, `WorkItemUpdated`, `WorkItemCompleted`
- `TaskCreated`, `TaskStarted`, `TaskCompleted`, `TaskBlocked`
- `GateChecked`, `GatePassed`, `GateFailed`

**Design Canon Reference**: Lines 981-1050

---

### PAT-EVT-004: IEventStore Port
**Status**: MANDATORY | **Category**: Event

Port for event persistence.

```python
class IEventStore(Protocol):
    def append(self, stream_id: str, events: list[DomainEvent], expected_version: int) -> None: ...
    def read(self, stream_id: str, from_version: int = 0) -> list[DomainEvent]: ...
```

**Design Canon Reference**: Lines 1051-1100

---

## CQRS Patterns

### PAT-CQRS-001: Command Pattern
**Status**: MANDATORY | **Category**: CQRS

Commands for write operations.

**File Naming**: `{verb}_{noun}_command.py` (e.g., `create_task_command.py`)

**Structure**:
```python
@dataclass(frozen=True)
class CreateTaskCommand:
    title: str
    description: str | None = None

class CreateTaskCommandHandler:
    def handle(self, command: CreateTaskCommand) -> list[DomainEvent]: ...
```

**Design Canon Reference**: Lines 1110-1180

---

### PAT-CQRS-002: Query Pattern
**Status**: MANDATORY | **Category**: CQRS

Queries for read operations.

**File Naming**: `retrieve_{noun}_query.py` (e.g., `retrieve_project_context_query.py`)

**Structure**:
```python
@dataclass(frozen=True)
class RetrieveProjectContextQuery:
    base_path: str

class RetrieveProjectContextQueryHandler:
    def handle(self, query: RetrieveProjectContextQuery) -> ProjectContextDTO: ...
```

**Design Canon Reference**: Lines 1181-1250

---

### PAT-CQRS-003: Projection Pattern
**Status**: RECOMMENDED | **Category**: CQRS

Materialized views for optimized reads.

**Location**: `src/application/projections/`

**Design Canon Reference**: Lines 1251-1300

---

## Repository Patterns

### PAT-REPO-001: Generic Repository Port
**Status**: MANDATORY | **Category**: Repository

Domain-level repository abstraction.

```python
class IRepository(Protocol[T, TId]):
    def get(self, id: TId) -> T | None: ...
    def save(self, aggregate: T) -> None: ...
    def delete(self, id: TId) -> None: ...
    def exists(self, id: TId) -> bool: ...
```

**Location**: `src/domain/ports/repository.py`

**Design Canon Reference**: Lines 1310-1380

---

### PAT-REPO-002: Unit of Work
**Status**: RECOMMENDED | **Category**: Repository

Transaction boundary pattern.

**Design Canon Reference**: Lines 1381-1420

---

### PAT-REPO-003: Snapshot Store
**Status**: RECOMMENDED | **Category**: Repository

Aggregate snapshot persistence for event sourcing.

```python
class ISnapshotStore(Protocol):
    def save_snapshot(self, aggregate_id: str, snapshot: bytes, version: int) -> None: ...
    def get_snapshot(self, aggregate_id: str) -> tuple[bytes, int] | None: ...
```

**Design Canon Reference**: Lines 1421-1470

---

## Graph Patterns

### PAT-GRAPH-001: IGraphStore Port
**Status**: RECOMMENDED | **Category**: Graph

Port for graph persistence.

```python
class IGraphStore(Protocol):
    def add_vertex(self, vertex: Vertex) -> None: ...
    def add_edge(self, edge: Edge) -> None: ...
    def query(self, traversal: str) -> list[Vertex]: ...
```

**Design Canon Reference**: Lines 1480-1540

---

### PAT-GRAPH-002: Edge Labels
**Status**: RECOMMENDED | **Category**: Graph

Standardized relationship types.

**Labels**: `DEPENDS_ON`, `BLOCKS`, `PARENT_OF`, `CHILD_OF`, `RELATED_TO`, `IMPLEMENTS`

**Design Canon Reference**: Lines 1541-1580

---

### PAT-GRAPH-003: Gremlin Compatibility
**Status**: RECOMMENDED | **Category**: Graph

Traversal query compatibility.

**Design Canon Reference**: Lines 1581-1620

---

## Architecture Patterns

### PAT-ARCH-001: Hexagonal Architecture
**Status**: MANDATORY | **Category**: Architecture

Ports and Adapters architecture.

**Layer Structure**:
```
src/
├── domain/           # Core business logic (NO external deps)
├── application/      # Use cases, CQRS handlers
├── infrastructure/   # Adapters, persistence
└── interface/        # Primary adapters (CLI, API)
```

**Dependency Rule**: Outer layers depend on inner layers, never reverse.

**Design Canon Reference**: Lines 1630-1750

---

### PAT-ARCH-002: Primary/Secondary Ports
**Status**: MANDATORY | **Category**: Architecture

Port classification.

**Primary Ports**: Interface layer drives application (CLI, API)
**Secondary Ports**: Application drives infrastructure (Repository, EventStore)

**Naming**:
- Primary: `src/application/ports/primary/`
- Secondary: `src/application/ports/secondary/`

**Design Canon Reference**: Lines 1751-1820

---

### PAT-ARCH-003: Bounded Contexts
**Status**: MANDATORY | **Category**: Architecture

Domain separation.

**Contexts in Jerry**:
- `session_management/` - Project and session handling
- `work_tracking/` - Task and work item management
- `shared_kernel/` - Cross-context shared code

**Design Canon Reference**: Lines 1821-1900

---

## Testing Patterns

### PAT-TEST-001: BDD Red/Green/Refactor
**Status**: MANDATORY | **Category**: Testing

Test-first development cycle.

**Cycle**:
1. **RED**: Write failing test first
2. **GREEN**: Write minimal code to pass
3. **REFACTOR**: Improve without changing behavior

**Design Canon Reference**: Lines 1910-1960

---

### PAT-TEST-002: Test Pyramid
**Status**: MANDATORY | **Category**: Testing

Test distribution.

```
                    ┌─────────────┐
                    │    E2E      │ ← Full workflow validation
                   ┌┴─────────────┴┐
                   │    System     │ ← Component interaction
                  ┌┴───────────────┴┐
                  │   Integration   │ ← Adapter/port testing
                 ┌┴─────────────────┴┐
                 │       Unit        │ ← Domain logic
                ┌┴───────────────────┴┐
                │ Contract+Architecture│ ← Interface compliance
                └─────────────────────┘
```

**Required Coverage**: 90%+

**Design Canon Reference**: Lines 1961-2020

---

### PAT-TEST-003: Architecture Tests
**Status**: MANDATORY | **Category**: Testing

Layer boundary enforcement.

**Tools**: pytest-archon, PyTestArch

**Location**: `tests/architecture/`

**Example**:
```python
def test_domain_has_no_infrastructure_imports():
    imports = get_imports_from_file(domain_file)
    assert not has_infrastructure_import(imports)
```

**Design Canon Reference**: Lines 2021-2080

---

## Lessons Learned

| ID | Lesson | Priority |
|----|--------|----------|
| LES-001 | Event Schemas Are Forever | HIGH |
| LES-002 | Layer Violations Compound | HIGH |
| LES-003 | Retry is Not Optional | HIGH |
| LES-004 | Test at Boundaries First | MEDIUM |
| LES-005 | Document Decisions Immediately | MEDIUM |
| LES-006 | Validate Early, Fail Fast | MEDIUM |

**Design Canon Reference**: Lines 2090-2116

---

## Assumptions

| ID | Assumption | Validity |
|----|------------|----------|
| ASM-001 | Filesystem durability sufficient for MVP | MEDIUM |
| ASM-002 | Single-writer assumption holds | MEDIUM |
| ASM-003 | Event replay under 100ms | MEDIUM |
| ASM-004 | TOON suitable for LLM interface | HIGH |

**Design Canon Reference**: Lines 2117-2150

---

## References

### Primary Sources
- **Jerry Design Canon**: `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md`
- **Architecture Teaching Edition**: `docs/knowledge/exemplars/architecture/work_tracker_architecture_hexagonal_ddd_cqrs_layered_teaching_edition.md`
- **CloudEvents ADR**: `decisions/PROJ-001-e-016-v1-adr-cloudevents-sdk.md`
- **Shared Kernel ADR**: `decisions/e-013-v2-shared-kernel-adr.md`

### Industry References
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Alistair Cockburn
- [Domain-Driven Design](https://www.domainlanguage.com/ddd/) - Eric Evans
- [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) - Martin Fowler
- [CQRS](https://martinfowler.com/bliki/CQRS.html) - Martin Fowler
- [CloudEvents Specification](https://cloudevents.io/) - CNCF

### Enforcement Tools
- [pytest-archon](https://github.com/jwbargsten/pytest-archon) - Architecture boundary testing
- [PyTestArch](https://pypi.org/project/PyTestArch/) - ArchUnit-inspired Python testing
