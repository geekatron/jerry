# Canon-Implementation Gap Analysis v2.0: Jerry Design Canon v1.0

> **Document ID**: PROJ-001-e-012-v2-canon-implementation-gap
> **PS ID**: PROJ-001
> **Entry ID**: e-012-v2
> **Date**: 2026-01-10
> **Analyst**: ps-analyst agent v2.0.0 (Opus 4.5)
> **Methodology**: 5W1H Framework + NASA SE Risk Assessment
> **Supersedes**: PROJ-001-e-012-v1-canon-implementation-gap.md

---

## L0: Executive Summary

### Overview

The Jerry Framework implementation has made **substantial progress** since the prior gap analysis (e-012-v1, dated 2026-01-09). Current implementation is estimated at **40-50% of canonical architecture**, up from 15-20% in v1 analysis.

**Key Progress Since v1**:
- Shared Kernel created (`src/shared_kernel/`) with 9 exported components
- VertexId hierarchy fully implemented (TaskId, PhaseId, PlanId, SubtaskId, KnowledgeId, ActorId, EventId, EdgeId)
- ProjectId now properly extends VertexId (Canon PAT-ID-001 compliant)
- IAuditable and IVersioned protocols implemented
- EntityBase and DomainEvent base classes implemented
- IEventStore and ISnapshotStore ports implemented in work_tracking domain
- AggregateRoot base class with full event lifecycle management
- JerryUri value object implemented
- Domain exception hierarchy complete
- Test infrastructure established (45+ test files)

**Critical Gaps Remaining**:
1. **CloudEvents 1.0 Envelope**: DomainEvent base class lacks CloudEvents format compliance
2. **Graph Primitives**: Vertex/Edge base classes missing; IGraphStore port absent
3. **CQRS Infrastructure**: No IProjection interface, IUnitOfWork, or command/query handlers
4. **Canonical Work Management**: Task/Phase/Plan aggregates per canon not yet implemented (WorkItem exists but differs)

### Overall Risk Assessment: **MEDIUM**

The foundation is now solid. Remaining gaps are extensions rather than fundamental redesign. Primary risk is divergence between work_tracking implementation and canonical Work Management context definitions.

### Top 3 Critical Gaps Requiring Immediate Attention

| Priority | Gap | Impact | Evidence |
|----------|-----|--------|----------|
| P0 | CloudEvents 1.0 non-compliance | External system interop blocked | `domain_event.py` lacks specversion, source, subject fields |
| P1 | Graph primitives missing (Vertex/Edge) | No graph traversal, Neo4j migration blocked | No Vertex/Edge classes in shared_kernel, IGraphStore absent |
| P1 | Canonical Task/Phase/Plan aggregates | Work Management context incomplete | WorkItem in work_tracking differs from canonical Task |

---

## L1: Technical Gap Analysis

### 5W1H Framework Analysis

| Question | Analysis |
|----------|----------|
| **What** | Gaps exist in CloudEvents compliance, graph layer, CQRS projections, and canonical aggregate definitions |
| **Why** | These gaps block: (1) external event streaming, (2) graph-based navigation, (3) read-optimized queries, (4) canonical domain model |
| **Who** | Affects: Claude agents (skill execution), future MCP integrations, potential ADO sync |
| **Where** | `src/shared_kernel/domain_event.py` (CloudEvents), `src/shared_kernel/` (Vertex/Edge), `src/work_tracking/` (canonical aggregates) |
| **When** | P0 gaps before external integration; P1 gaps before Work Management context completion |
| **How** | Extend DomainEvent with CloudEvents fields; add Vertex/Edge base classes; implement IGraphStore; create canonical aggregates |

---

### Pattern Compliance Checklist

#### Identity Patterns (4/4 PASS)

| Pattern ID | Pattern Name | Canon Status | Implementation Status | Compliance |
|------------|--------------|--------------|----------------------|------------|
| PAT-ID-001 | VertexId | MANDATORY | `src/shared_kernel/vertex_id.py` - Abstract base with validation | **PASS** |
| PAT-ID-002 | Domain-Specific IDs | MANDATORY | TaskId, PhaseId, PlanId, SubtaskId, KnowledgeId, ActorId, EventId all implemented | **PASS** |
| PAT-ID-003 | JerryUri | RECOMMENDED | `src/shared_kernel/jerry_uri.py` - Fully implemented with nested entity support | **PASS** |
| PAT-ID-004 | EdgeId | MANDATORY | `src/shared_kernel/vertex_id.py:221` - Implemented with deterministic format | **PASS** |

**Evidence**:
- `vertex_id.py` line 26-68: `@dataclass(frozen=True) class VertexId(ABC)` with abstract `_is_valid_format()` and `generate()` methods
- `project_id.py` line 23: `from src.shared_kernel.vertex_id import VertexId` followed by line 36: `class ProjectId(VertexId)`

#### Entity Patterns (3/5 - 2 FAIL)

| Pattern ID | Pattern Name | Canon Status | Implementation Status | Compliance |
|------------|--------------|--------------|----------------------|------------|
| PAT-ENT-001 | IAuditable | MANDATORY | `src/shared_kernel/auditable.py` - Protocol with created_by/at, updated_by/at | **PASS** |
| PAT-ENT-002 | IVersioned | MANDATORY | `src/shared_kernel/versioned.py` - Protocol with version property and get_expected_version() | **PASS** |
| PAT-ENT-003 | AggregateRoot | MANDATORY | `src/work_tracking/domain/aggregates/base.py` - Event lifecycle, load_from_history | **PARTIAL** |
| PAT-ENT-004 | Vertex | MANDATORY | NOT FOUND | **FAIL** |
| PAT-ENT-005 | Edge | MANDATORY | NOT FOUND | **FAIL** |

**PAT-ENT-003 Partial Compliance**:
- AggregateRoot exists with full event lifecycle (_raise_event, collect_events, load_from_history)
- Located in work_tracking but should be in shared_kernel for cross-context reuse
- Uses `created_on/modified_on` (datetime) instead of canon's `created_by/created_at` (IAuditable)

**Evidence (work_tracking/domain/aggregates/base.py lines 36-115)**:
```python
class AggregateRoot(ABC):
    _aggregate_type: str = "Aggregate"

    def __init__(self, id: str) -> None:
        self._initialize(id)

    def _initialize(self, id: str, version: int = 0) -> None:
        self._id = id
        self._version = version
        self._pending_events: list[DomainEvent] = []
        self._created_on: datetime | None = None  # Not IAuditable compliant
        self._modified_on: datetime | None = None
```

#### Event Patterns (2/4 - 1 FAIL, 1 PARTIAL)

| Pattern ID | Pattern Name | Canon Status | Implementation Status | Compliance |
|------------|--------------|--------------|----------------------|------------|
| PAT-EVT-001 | CloudEvents 1.0 Envelope | MANDATORY | Schema exists but DomainEvent lacks compliance | **FAIL** |
| PAT-EVT-002 | DomainEvent Base | MANDATORY | `src/shared_kernel/domain_event.py` with EventRegistry | **PARTIAL** |
| PAT-EVT-003 | Work Tracker Events | MANDATORY | `src/work_tracking/domain/events/` has events | **PASS** |
| PAT-EVT-004 | IEventStore | MANDATORY | `src/work_tracking/domain/ports/event_store.py` - Complete interface | **PASS** |

**CloudEvents Gap Evidence**:

Canon specifies (L639-666):
```json
{
  "specversion": "1.0",
  "type": "com.jerry.task.completed.v1",
  "source": "/jerry/tasks/TASK-ABC123",
  "id": "EVT-a1b2c3d4",
  "subject": "TASK-ABC123",
  "datacontenttype": "application/json",
  ...
}
```

Current `DomainEvent.to_dict()` (lines 92-114) returns:
```python
{
    "event_type": self.__class__.__name__,  # Should be 'type' in com.jerry.* format
    "event_id": self.event_id,              # Should be 'id'
    "aggregate_id": self.aggregate_id,      # Should be 'source' or 'subject'
    # Missing: specversion, datacontenttype
}
```

#### CQRS Patterns (1/3 - 2 FAIL)

| Pattern ID | Pattern Name | Canon Status | Implementation Status | Compliance |
|------------|--------------|--------------|----------------------|------------|
| PAT-CQRS-001 | Command Pattern | MANDATORY | NOT FOUND (no command objects/handlers) | **FAIL** |
| PAT-CQRS-002 | Query Pattern | MANDATORY | session_management has queries but handlers embedded | **PARTIAL** |
| PAT-CQRS-003 | Projection Pattern | MANDATORY | NOT FOUND (no IProjection interface) | **FAIL** |

#### Repository Patterns (2/3 - 1 FAIL)

| Pattern ID | Pattern Name | Canon Status | Implementation Status | Compliance |
|------------|--------------|--------------|----------------------|------------|
| PAT-REPO-001 | Generic Repository | MANDATORY | `src/work_tracking/domain/ports/repository.py` - IRepository[T, TId] | **PASS** |
| PAT-REPO-002 | Unit of Work | MANDATORY | NOT FOUND | **FAIL** |
| PAT-REPO-003 | Snapshot Pattern | MANDATORY | `src/work_tracking/domain/ports/snapshot_store.py` - ISnapshotStore + InMemorySnapshotStore | **PASS** |

**Evidence (repository.py lines 96-131)**: Generic `IRepository[TAggregate, TId]` protocol with get(), get_or_raise(), save(), delete(), exists() methods.

#### Graph Patterns (0/3 - ALL FAIL)

| Pattern ID | Pattern Name | Canon Status | Implementation Status | Compliance |
|------------|--------------|--------------|----------------------|------------|
| PAT-GRAPH-001 | IGraphStore | MANDATORY | NOT FOUND | **FAIL** |
| PAT-GRAPH-002 | Edge Labels | MANDATORY | NOT FOUND (no EdgeLabels constants) | **FAIL** |
| PAT-GRAPH-003 | Gremlin Compatibility | RECOMMENDED | NOT FOUND | **FAIL** |

#### Architecture Patterns (3/3 PASS or PARTIAL)

| Pattern ID | Pattern Name | Canon Status | Implementation Status | Compliance |
|------------|--------------|--------------|----------------------|------------|
| PAT-ARCH-001 | Hexagonal Architecture | HARD | Both session_management and work_tracking follow hexagonal layers | **PASS** |
| PAT-ARCH-002 | Primary/Secondary Ports | MANDATORY | Port interfaces exist (IProjectRepository, IEventStore, ISnapshotStore, IRepository) | **PASS** |
| PAT-ARCH-003 | Bounded Contexts | MANDATORY | session_management and work_tracking exist; Work Management incomplete | **PARTIAL** |

---

### Shared Kernel Implementation Status

#### Components Present

| Component | Canonical Path | Implementation Path | Status |
|-----------|---------------|---------------------|--------|
| VertexId | `shared_kernel/identity/vertex_id.py` | `shared_kernel/vertex_id.py` | **EXISTS** |
| TaskId, PhaseId, PlanId, etc. | `shared_kernel/identity/domain_ids.py` | `shared_kernel/vertex_id.py` (same file) | **EXISTS** |
| EdgeId | `shared_kernel/identity/edge_id.py` | `shared_kernel/vertex_id.py` (same file) | **EXISTS** |
| JerryUri | `shared_kernel/identity/jerry_uri.py` | `shared_kernel/jerry_uri.py` | **EXISTS** |
| IAuditable | `shared_kernel/interfaces/auditable.py` | `shared_kernel/auditable.py` | **EXISTS** |
| IVersioned | `shared_kernel/interfaces/versioned.py` | `shared_kernel/versioned.py` | **EXISTS** |
| EntityBase | `shared_kernel/entities/entity_base.py` | `shared_kernel/entity_base.py` | **EXISTS** |
| DomainEvent | `shared_kernel/events/domain_event.py` | `shared_kernel/domain_event.py` | **EXISTS** |
| Domain Exceptions | `shared_kernel/exceptions/domain_errors.py` | `shared_kernel/exceptions.py` | **EXISTS** |
| SnowflakeIdGenerator | N/A (bonus) | `shared_kernel/snowflake_id.py` | **EXISTS** |

#### Components Missing

| Component | Canonical Path | Status | Impact |
|-----------|---------------|--------|--------|
| AggregateRoot | `shared_kernel/entities/aggregate_root.py` | **MISPLACED** (in work_tracking) | Cross-context reuse blocked |
| Vertex | `shared_kernel/entities/vertex.py` | **MISSING** | Graph model blocked |
| Edge | `shared_kernel/entities/edge.py` | **MISSING** | Graph model blocked |
| CloudEventEnvelope | `shared_kernel/events/cloud_events.py` | **MISSING** | External interop blocked |
| StreamEvent | `shared_kernel/events/stream_event.py` | **MISSING** | StoredEvent exists in work_tracking |
| Status Enums | `shared_kernel/value_objects/status.py` | **MISSING** in shared_kernel | In work_tracking |
| Priority Enum | `shared_kernel/value_objects/priority.py` | **MISPLACED** (in work_tracking) | Should be shared |

---

### NASA SE Risk Assessment

| Gap ID | Gap Description | Probability (1-5) | Impact (1-5) | Risk Score (P x I) | Mitigation Strategy |
|--------|-----------------|-------------------|--------------|-------------------|---------------------|
| GAP-001 | CloudEvents 1.0 non-compliance | 5 | 4 | **20 CRITICAL** | Add to_cloud_event() method to DomainEvent |
| GAP-002 | Vertex/Edge base classes missing | 5 | 4 | **20 CRITICAL** | Create in shared_kernel; implement IGraphStore |
| GAP-003 | AggregateRoot misplaced | 4 | 3 | **12 HIGH** | Move to shared_kernel; update imports |
| GAP-004 | Canonical Task/Phase/Plan missing | 4 | 4 | **16 CRITICAL** | Implement per canon PAT-AGG-001/002/003 |
| GAP-005 | IProjection missing | 4 | 3 | **12 HIGH** | Create IProjection protocol |
| GAP-006 | IUnitOfWork missing | 3 | 4 | **12 HIGH** | Create interface; implement adapter |
| GAP-007 | Edge Labels missing | 4 | 2 | **8 MEDIUM** | Define EdgeLabels class with constants |
| GAP-008 | Command handlers missing | 3 | 3 | **9 MEDIUM** | Implement CreateTask, CompleteTask commands |
| GAP-009 | Priority/Status in wrong location | 2 | 2 | **4 LOW** | Refactor to shared_kernel |

**Risk Legend**:
- **CRITICAL (15-25)**: GAP-001, GAP-002, GAP-004 - Blocks external integration, graph model, core domain
- **HIGH (10-14)**: GAP-003, GAP-005, GAP-006 - Impacts cross-context reuse, read optimization
- **MEDIUM (5-9)**: GAP-007, GAP-008 - Future capability, current functionality unaffected
- **LOW (1-4)**: GAP-009 - Code organization only

---

### Dependency Graph

```
                    +------------------+
                    | CloudEvents 1.0  |
                    | Envelope         |
                    +--------+---------+
                             |
                             | blocks
                             v
               +-------------+---------------+
               |    External Event           |
               |    Streaming / ADO Sync     |
               +-----------------------------+

+----------------+     +----------------+     +----------------+
| Vertex/Edge    | --> | IGraphStore    | --> | Graph DB       |
| Base Classes   |     | Port           |     | Migration      |
+----------------+     +----------------+     +----------------+
        |
        | blocks
        v
+----------------+
| Edge Labels    |
| (CONTAINS,     |
| EMITTED, etc.) |
+----------------+

+----------------+     +----------------+     +----------------+
| AggregateRoot  | --> | Task/Phase/    | --> | Work           |
| in shared_kernel|     | Plan Aggregates|     | Management BC  |
+----------------+     +----------------+     +----------------+

+----------------+     +----------------+
| IUnitOfWork    | --> | Transaction    |
| Interface      |     | Coordination   |
+----------------+     +----------------+

+----------------+     +----------------+     +----------------+
| IProjection    | --> | TaskList       | --> | Optimized      |
| Interface      |     | Projection     |     | Read Queries   |
+----------------+     +----------------+     +----------------+
```

---

### Prioritized Remediation Backlog

#### Phase 1: Foundation Completion (P0) - 2-3 days

| # | Task | Depends On | Files to Create/Modify |
|---|------|------------|------------------------|
| 1.1 | Add `to_cloud_event()` method to DomainEvent | None | `shared_kernel/domain_event.py` |
| 1.2 | Create `CloudEventEnvelope` wrapper class | 1.1 | `shared_kernel/cloud_events.py` |
| 1.3 | Create `Vertex` base class | None | `shared_kernel/vertex.py` |
| 1.4 | Create `Edge` base class | 1.3 | `shared_kernel/edge.py` |
| 1.5 | Move `AggregateRoot` to shared_kernel | None | `shared_kernel/aggregate_root.py` |

#### Phase 2: Graph Layer (P1) - 3-4 days

| # | Task | Depends On | Files to Create/Modify |
|---|------|------------|------------------------|
| 2.1 | Define `EdgeLabels` constants | 1.4 | `shared_kernel/edge_labels.py` |
| 2.2 | Create `IGraphStore` port | 1.3, 1.4 | `domain/ports/graph_store.py` |
| 2.3 | Implement NetworkX adapter | 2.2 | `infrastructure/graph/networkx_adapter.py` |
| 2.4 | Add graph traversal tests | 2.3 | `tests/infrastructure/graph/` |

#### Phase 3: Canonical Aggregates (P1) - 5-7 days

| # | Task | Depends On | Files to Create/Modify |
|---|------|------------|------------------------|
| 3.1 | Implement canonical `Task` aggregate | 1.5 | `work_management/domain/aggregates/task.py` |
| 3.2 | Implement canonical `Phase` aggregate | 3.1 | `work_management/domain/aggregates/phase.py` |
| 3.3 | Implement canonical `Plan` aggregate | 3.2 | `work_management/domain/aggregates/plan.py` |
| 3.4 | Define TaskStatus, PhaseStatus state machines | 3.1 | `shared_kernel/value_objects/status.py` |
| 3.5 | Implement Task domain events | 3.1 | `work_management/domain/events/task_events.py` |

#### Phase 4: CQRS Completion (P2) - 3-4 days

| # | Task | Depends On | Files to Create/Modify |
|---|------|------------|------------------------|
| 4.1 | Create `IProjection` interface | None | `application/ports/projection.py` |
| 4.2 | Implement `TaskListProjection` | 4.1, 3.5 | `application/projections/task_list.py` |
| 4.3 | Create `IUnitOfWork` interface | None | `application/ports/unit_of_work.py` |
| 4.4 | Implement SQLite UnitOfWork | 4.3 | `infrastructure/persistence/sqlite_uow.py` |

---

## L2: Strategic Implications

### Impact on Project Timeline if Gaps Not Addressed

| Gap | Timeline Impact | Downstream Blockers |
|-----|-----------------|---------------------|
| CloudEvents non-compliance | Blocks ADO integration | External event streaming, audit interop |
| Graph layer missing | Blocks relationship navigation | Plan->Phase->Task traversal, dependency graphs |
| Canonical aggregates missing | Blocks Work Management BC | Task creation, phase management, plan lifecycle |
| CQRS incomplete | Blocks read-optimized queries | Performance with large datasets |

### Architectural Drift Risk Assessment

**Current Risk Level**: MEDIUM

The work_tracking bounded context has evolved independently with `WorkItem` aggregate that differs from canonical `Task`:
- WorkItem uses string ID; canonical Task uses TaskId (VertexId subclass)
- WorkItem has different state machine than canonical Task
- WorkItem in work_tracking vs Task in work_management (different context names)

**Recommendation**: Evaluate alignment strategy:
1. **Option A**: Rename work_tracking to work_management, refactor WorkItem to Task
2. **Option B**: Keep both contexts, create mapping layer
3. **Option C**: Treat work_tracking as implementation-specific, create canonical work_management separately

### Shared Kernel Implementation Order

**Recommended Order**:

1. **Phase 1**: Complete shared_kernel foundation
   - CloudEventEnvelope for external interop
   - Move AggregateRoot to shared_kernel
   - Add Vertex, Edge base classes

2. **Phase 2**: Graph primitives
   - IGraphStore port
   - EdgeLabels constants
   - NetworkX adapter

3. **Phase 3**: Value Objects
   - Move Priority to shared_kernel
   - Add canonical Status enums (TaskStatus, PhaseStatus, PlanStatus)

4. **Phase 4**: CQRS infrastructure
   - IProjection interface
   - IUnitOfWork interface

---

## Summary Statistics

| Metric | v1 Analysis (e-012-v1) | v2 Analysis (e-012-v2) | Delta |
|--------|------------------------|------------------------|-------|
| Implementation Progress | ~15-20% | ~40-50% | **+25-30%** |
| Shared Kernel Components | 0 | 9 | **+9** |
| Pattern Compliance PASS | 1-2 | 12 | **+10-11** |
| Pattern Compliance FAIL | ~21 | 8 | **-13** |
| Test Files | 0 | 45+ | **+45** |
| Critical Gaps | 5 (P0) | 3 (P0) | **-2** |

### Compliance Summary by Category

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

---

## References

### Source Documents

| ID | Title | Location |
|----|-------|----------|
| e-011-v1 | Jerry Design Canon v1.0 | `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md` |
| e-012-v1 | Prior Gap Analysis v1 | `projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-012-v1-canon-implementation-gap.md` |
| e-007 | Initial Gap Analysis | `projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-007-implementation-gap-analysis.md` |

### Implementation Files Analyzed

| Path | Purpose |
|------|---------|
| `src/shared_kernel/__init__.py` | Shared kernel exports (9 components) |
| `src/shared_kernel/vertex_id.py` | VertexId hierarchy + EdgeId (251 lines) |
| `src/shared_kernel/domain_event.py` | DomainEvent base + EventRegistry (261 lines) |
| `src/shared_kernel/entity_base.py` | EntityBase with audit/version (99 lines) |
| `src/shared_kernel/auditable.py` | IAuditable protocol (53 lines) |
| `src/shared_kernel/versioned.py` | IVersioned protocol (41 lines) |
| `src/shared_kernel/jerry_uri.py` | JerryUri value object (109 lines) |
| `src/shared_kernel/exceptions.py` | Domain exception hierarchy (77 lines) |
| `src/session_management/domain/value_objects/project_id.py` | ProjectId extending VertexId (233 lines) |
| `src/work_tracking/domain/aggregates/base.py` | AggregateRoot base class (366 lines) |
| `src/work_tracking/domain/ports/event_store.py` | IEventStore port + StoredEvent (342 lines) |
| `src/work_tracking/domain/ports/snapshot_store.py` | ISnapshotStore port + InMemory impl (345 lines) |
| `src/work_tracking/domain/ports/repository.py` | IRepository generic port (253 lines) |

---

*Document created by ps-analyst agent v2.0.0*
*Analysis methodology: 5W1H Framework + NASA SE Risk Assessment*
*Analysis completed: 2026-01-10*
*Version: 2.0 (supersedes v1)*
