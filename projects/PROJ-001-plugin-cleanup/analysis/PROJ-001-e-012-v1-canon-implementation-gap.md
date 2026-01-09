# Canon-Implementation Gap Analysis

> **Document ID**: PROJ-001-e-012-v1-canon-implementation-gap
> **PS ID**: PROJ-001
> **Entry ID**: e-012-v1
> **Date**: 2026-01-09
> **Author**: ps-analyst agent v2.0.0
> **Cycle**: 1 (Initial)
> **Status**: ANALYSIS COMPLETE
>
> **Sources**:
> - **Canon (target state)**: `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md`
> - **Current implementation**: `src/session_management/` (24 Python files)
> - **Previous gap analysis**: `projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-007-implementation-gap-analysis.md`

---

## L0: Executive Summary (ELI5)

### What's missing between canon and implementation?

The Jerry Design Canon (e-011-v1) defines a comprehensive event-sourced architecture with 26 patterns. The current implementation in `src/session_management/` implements only **~15-20%** of these patterns, focusing exclusively on read-only project scanning functionality.

**Key Missing Components:**
1. **Shared Kernel** - The foundational building blocks (`VertexId`, `IAuditable`, `IVersioned`, `EntityBase`, `DomainEvent`) do not exist
2. **Event Sourcing** - No event store, no domain events, no event replay capability
3. **Core Aggregates** - Task, Phase, Plan aggregates are completely absent
4. **Graph Layer** - No graph primitives or storage

### How big is the gap?

**Scale: LARGE**

| Category | Canon Patterns | Implemented | Gap |
|----------|---------------|-------------|-----|
| Identity (PAT-001 to PAT-004) | 4 | 0 (partial: ProjectId exists) | 4 |
| Entity Base (PAT-005 to PAT-009) | 5 | 0 | 5 |
| Event Patterns (PAT-010 to PAT-013) | 4 | 0 | 4 |
| CQRS Patterns (PAT-014 to PAT-016) | 3 | 1 (queries only) | 2 |
| Repository Patterns (PAT-017 to PAT-019) | 3 | 0.5 (IProjectRepository) | 2.5 |
| Architecture (PAT-020 to PAT-021) | 2 | 1 (hexagonal mostly) | 1 |
| Graph Patterns (PAT-022 to PAT-024) | 3 | 0 | 3 |
| Testing Patterns (PAT-025 to PAT-026) | 2 | 0 | 2 |
| **Total** | **26** | **~4** | **~22** |

### What's the top priority to fix?

**Priority 1 (P0): Create Shared Kernel**

The Shared Kernel is the foundation for all other patterns. Without it:
- Cannot implement VertexId hierarchy (required for graph-ready IDs)
- Cannot implement AggregateRoot (required for event sourcing)
- Cannot implement domain events (required for audit trail)
- Each bounded context will reinvent these wheels inconsistently

---

## L1: Technical Gap Analysis (Software Engineer)

### 1. Shared Kernel Gap

The canon specifies `src/shared_kernel/` as a cross-cutting module containing foundational types. This directory **does not exist**.

| Canon Component | File Path (Canon) | Current Implementation | Gap Status |
|-----------------|-------------------|----------------------|------------|
| `VertexId` base class | `shared_kernel/vertex_id.py` | **Not found** | MISSING |
| `TaskId` (extends VertexId) | `shared_kernel/vertex_id.py` | Not found | MISSING |
| `PhaseId` (extends VertexId) | `shared_kernel/vertex_id.py` | Not found | MISSING |
| `PlanId` (extends VertexId) | `shared_kernel/vertex_id.py` | Not found | MISSING |
| `SubtaskId` (extends VertexId) | `shared_kernel/vertex_id.py` | Not found | MISSING |
| `KnowledgeId` (extends VertexId) | `shared_kernel/vertex_id.py` | Not found | MISSING |
| `ActorId` (extends VertexId) | `shared_kernel/vertex_id.py` | Not found | MISSING |
| `EventId` (extends VertexId) | `shared_kernel/vertex_id.py` | Not found | MISSING |
| `EdgeId` | `shared_kernel/vertex_id.py` | Not found | MISSING |
| `JerryUri` | `shared_kernel/jerry_uri.py` | Not found | MISSING |
| `IAuditable` | `shared_kernel/auditable.py` | Not found | MISSING |
| `IVersioned` | `shared_kernel/versioned.py` | Not found | MISSING |
| `EntityBase` | `shared_kernel/entity_base.py` | Not found | MISSING |
| Domain exceptions | `shared_kernel/exceptions.py` | `session_management/domain/exceptions.py` (partial) | PARTIAL |

**Evidence (Canon L65-111)**:
```python
# Canon specifies VertexId as frozen dataclass with validation
@dataclass(frozen=True)
class VertexId(ABC):
    value: str
    def __post_init__(self):
        if not self._is_valid_format(self.value):
            raise ValueError(f"Invalid {self.__class__.__name__} format: {self.value}")
```

**Evidence (Current Implementation)**:
The only identity type is `ProjectId` at `src/session_management/domain/value_objects/project_id.py`:
```python
# ProjectId uses PROJ-{nnn}-{slug} format, NOT the canonical PLAN-{uuid8}
@dataclass(frozen=True, slots=True)
class ProjectId:
    value: str
    number: int
    slug: str
```

**Gap Assessment**: `ProjectId` is similar in concept (frozen dataclass, validation) but:
1. Does not extend `VertexId` base class
2. Uses different format (`PROJ-{nnn}-{slug}` vs `PLAN-{uuid8}`)
3. Is context-specific, not shared

### 2. Pattern Compliance Analysis

| Pattern ID | Pattern Name | Canon Specification | Implementation Status | Gap |
|------------|--------------|--------------------|-----------------------|-----|
| **PAT-001** | VertexId Base | Abstract frozen dataclass with format validation | Not implemented | MISSING |
| **PAT-002** | Domain-Specific IDs | TaskId, PhaseId, PlanId extending VertexId | Not implemented | MISSING |
| **PAT-003** | JerryUri | URI format `jerry://{type}/{id}` | Not implemented | MISSING |
| **PAT-004** | EdgeId | Format `{outV}--{label}-->{inV}` | Not implemented | MISSING |
| **PAT-005** | IAuditable | Protocol with created_by/at, updated_by/at | Not implemented | MISSING |
| **PAT-006** | IVersioned | Protocol with version counter | Not implemented | MISSING |
| **PAT-007** | EntityBase | Combines VertexId + IAuditable + IVersioned | Not implemented | MISSING |
| **PAT-008** | AggregateRoot | Event-sourced base with _raise_event() | Not implemented | MISSING |
| **PAT-009** | Vaughn Vernon Rules | 4 rules for aggregate design | Cannot assess (no aggregates) | MISSING |
| **PAT-010** | CloudEvents 1.0 | Event envelope with specversion, type, source | Not implemented | MISSING |
| **PAT-011** | DomainEvent | Base class with event_id, occurred_at | Not implemented (events/__init__.py is empty) | MISSING |
| **PAT-012** | Event Naming | Past tense, aggregate prefix | No events exist | MISSING |
| **PAT-013** | IEventStore | append(), read(), get_current_position() | Not implemented | MISSING |
| **PAT-014** | Command Pattern | Frozen dataclass commands | Not implemented | MISSING |
| **PAT-015** | Query Pattern | Frozen dataclass queries | **PARTIAL** - 4 queries exist but not frozen | PARTIAL |
| **PAT-016** | Projection Pattern | IProjection interface | Not implemented | MISSING |
| **PAT-017** | IRepository Generic | `IRepository[TAggregate, TId]` | **PARTIAL** - IProjectRepository (specific) | PARTIAL |
| **PAT-018** | ISnapshotStore | Snapshot storage port | Not implemented | MISSING |
| **PAT-019** | IUnitOfWork | Transaction boundary | Not implemented | MISSING |
| **PAT-020** | Hexagonal Architecture | Domain/Application/Infrastructure layers | **COMPLIANT** - Layers properly separated | COMPLIANT |
| **PAT-021** | Bounded Contexts | Explicit context boundaries | **PARTIAL** - Only session_management exists | PARTIAL |
| **PAT-022** | Vertex/Edge Base | Graph primitives | Not implemented | MISSING |
| **PAT-023** | Edge Labels | CONTAINS, EMITTED, PERFORMED_BY | Not implemented | MISSING |
| **PAT-024** | IGraphStore | Graph persistence port | Not implemented | MISSING |
| **PAT-025** | Test Pyramid | Unit/Integration/E2E | Not implemented (no tests/) | MISSING |
| **PAT-026** | Architecture Tests | Layer dependency validation | Not implemented | MISSING |

### 3. Directory Structure Gap

**Canon Specification (L1295-1369)**:
```
src/
├── shared_kernel/        # Cross-cutting value objects
│   ├── vertex_id.py
│   ├── jerry_uri.py
│   ├── auditable.py
│   ├── versioned.py
│   ├── entity_base.py
│   └── exceptions.py
│
├── domain/               # Pure business logic
│   ├── aggregates/
│   │   ├── task.py
│   │   ├── phase.py
│   │   └── plan.py
│   ├── value_objects/
│   ├── events/
│   └── ports/
│
├── application/          # Use cases
│   ├── commands/
│   ├── queries/
│   ├── handlers/
│   └── dtos/
│
├── infrastructure/       # Adapters
│   ├── persistence/
│   ├── graph/
│   └── messaging/
│
└── interface/            # CLI, API
```

**Actual Structure**:
```
src/
└── session_management/   # Single bounded context only
    ├── domain/
    │   ├── entities/
    │   │   └── project_info.py
    │   ├── value_objects/
    │   │   ├── project_id.py
    │   │   ├── project_status.py
    │   │   └── validation_result.py
    │   ├── events/
    │   │   └── __init__.py (EMPTY)
    │   └── exceptions.py
    ├── application/
    │   ├── ports/
    │   │   ├── project_repository.py
    │   │   ├── environment.py
    │   │   └── exceptions.py
    │   └── queries/
    │       ├── scan_projects.py
    │       ├── validate_project.py
    │       ├── get_next_number.py
    │       └── get_project_context.py
    └── infrastructure/
        └── adapters/
            ├── filesystem_project_adapter.py
            └── os_environment_adapter.py
```

**Gap Summary**:
| Directory | Canon | Actual | Status |
|-----------|-------|--------|--------|
| `src/shared_kernel/` | Required | Missing | MISSING |
| `src/domain/` | Top-level | Only under `session_management/` | MISALIGNED |
| `src/domain/aggregates/` | Task, Phase, Plan | Not present | MISSING |
| `src/domain/ports/` | Required | Under `application/ports/` | MISALIGNED |
| `src/application/commands/` | Required | Not present | MISSING |
| `src/application/handlers/` | Required | Handlers embedded in queries | MISALIGNED |
| `src/infrastructure/persistence/` | Event store adapters | Not present | MISSING |
| `src/infrastructure/graph/` | NetworkX adapter | Not present | MISSING |
| `src/interface/` | CLI composition root | Not present | MISSING |
| `tests/` | Required | Not present | MISSING |

### 4. CQRS Implementation Analysis

**Queries (PARTIAL)**:

The current implementation has 4 queries:

| Query | Frozen? | Separate Handler? | Returns DTO? | Canon Compliance |
|-------|---------|-------------------|--------------|------------------|
| `ScanProjectsQuery` | No (`@dataclass`) | No (embedded) | `list[ProjectInfo]` | PARTIAL |
| `ValidateProjectQuery` | No (`@dataclass`) | No (embedded) | `tuple[ProjectId, ValidationResult]` | PARTIAL |
| `GetNextNumberQuery` | No | No (embedded) | `int` | PARTIAL |
| `GetProjectContextQuery` | No | No (embedded) | varies | PARTIAL |

**Evidence (Canon L906-934)**:
```python
# Canon specifies frozen dataclass queries
@dataclass(frozen=True)
class Query(ABC):
    pass

@dataclass(frozen=True)
class GetTaskByIdQuery(Query):
    task_id: str
```

**Evidence (Current L15-22, scan_projects.py)**:
```python
# Current implementation - NOT frozen, handler embedded
@dataclass
class ScanProjectsQuery:
    repository: IProjectRepository
    base_path: str

    def execute(self) -> list[ProjectInfo]:  # Handler embedded
        return self.repository.scan_projects(self.base_path)
```

**Commands (MISSING)**: No commands exist in the codebase.

### 5. Event Sourcing Infrastructure

**Status**: COMPLETELY MISSING

| Component | Canon Location | Implementation | Gap |
|-----------|----------------|----------------|-----|
| `DomainEvent` base | PAT-011 (L594-654) | `events/__init__.py` is empty | MISSING |
| `IEventStore` port | PAT-013 (L726-817) | Not found | MISSING |
| SQLite event store | Infrastructure | Not found | MISSING |
| `ISnapshotStore` | PAT-018 (L1119-1189) | Not found | MISSING |
| Event serialization | CloudEvents 1.0 | Not found | MISSING |

**Evidence (Canon L594-611)**:
```python
@dataclass(frozen=True)
class DomainEvent(ABC):
    event_id: str = field(default_factory=lambda: f"EVT-{uuid.uuid4()}")
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    caused_by: str = "Claude"
```

**Evidence (Current - events/__init__.py L1-9)**:
```python
"""Domain Events - Facts that happened in the past."""
# No events defined yet for this bounded context
__all__: list[str] = []
```

### 6. Domain Exceptions Comparison

The current implementation has partial domain exceptions:

| Canon Exception | Current Implementation | Status |
|-----------------|----------------------|--------|
| `DomainError` (base) | `DomainError` in `exceptions.py` | COMPLIANT |
| `NotFoundError` | `ProjectNotFoundError` (specific) | PARTIAL |
| `InvalidStateError` | Not found | MISSING |
| `InvalidStateTransitionError` | Not found | MISSING |
| `InvariantViolationError` | Not found | MISSING |
| `ConcurrencyError` | Not found | MISSING |
| `ValidationError` | `InvalidProjectIdError`, `ProjectValidationError` | PARTIAL |

**Evidence (Canon L1812-1859 specifies 7 exception types)**
**Evidence (Current has only 4 exception types)**

### 7. Hexagonal Compliance Verification

**Layer Boundary Analysis**:

| Layer | Imports From | Canon Requirement | Current Status |
|-------|--------------|-------------------|----------------|
| Domain | stdlib only | NO external imports | COMPLIANT |
| Application | domain only | NO infra/interface | COMPLIANT |
| Infrastructure | domain, app | NO interface | COMPLIANT |

**Evidence (current domain layer imports - exceptions.py)**:
```python
from __future__ import annotations  # stdlib only - COMPLIANT
```

**Evidence (current application layer imports - scan_projects.py)**:
```python
from ...domain import ProjectInfo  # Domain import - COMPLIANT
from ..ports import IProjectRepository  # Application import - COMPLIANT
```

**Issue Found**: `RepositoryError` is defined in `application/ports/exceptions.py` but should be in `infrastructure/`.

---

## L2: Strategic Implications (Principal Architect)

### 5W1H Analysis

#### **What**: What exactly needs to change?

1. **Create `src/shared_kernel/`** with all foundational types
2. **Implement Event Sourcing** infrastructure (DomainEvent, IEventStore, adapters)
3. **Build Work Management** bounded context with Task, Phase, Plan aggregates
4. **Separate CQRS handlers** from query/command definitions
5. **Add test infrastructure** with architecture tests
6. **Implement graph layer** for relationship storage

#### **Why**: Why is the change necessary?

| Gap | Business Impact | Technical Impact |
|-----|-----------------|------------------|
| Missing Shared Kernel | Inconsistent identity across contexts | Code duplication, refactoring burden |
| No Event Sourcing | No audit trail, no history | Cannot implement task tracking |
| No Aggregates | No work management capability | Jerry's core value undelivered |
| Embedded handlers | Testing difficulty | Cannot mock/substitute handlers |
| No tests | Regression risk | Cannot safely refactor |

#### **Who**: Who is affected by the gap?

| Stakeholder | Impact |
|-------------|--------|
| **Developers** | Cannot implement new bounded contexts without Shared Kernel |
| **Users** | Cannot use work tracking (core feature) |
| **Ops** | No audit trail for compliance |
| **Future maintainers** | Inconsistent patterns make understanding harder |

#### **Where**: Where in the codebase?

| Location | Gap Type |
|----------|----------|
| `src/shared_kernel/` | Does not exist (CRITICAL) |
| `src/domain/` | Exists only under session_management |
| `src/work_management/` | Does not exist (CRITICAL) |
| `src/infrastructure/persistence/` | Does not exist |
| `tests/` | Does not exist |

#### **When**: What's the dependency order?

```
Phase 1: Shared Kernel (blocks all else)
    ├── VertexId hierarchy
    ├── IAuditable, IVersioned
    └── EntityBase
         │
         v
Phase 2: Event Sourcing (blocks aggregates)
    ├── DomainEvent base
    ├── IEventStore port
    └── SQLite adapter
         │
         v
Phase 3: Aggregate Foundation (blocks Work Management)
    ├── AggregateRoot base
    └── Generic IRepository
         │
         v
Phase 4: Work Management Context (blocks user value)
    ├── Task aggregate
    ├── Phase aggregate
    └── Plan aggregate
         │
         v
Phase 5: CQRS Completion (can parallel Phase 4)
    ├── Separate handlers
    └── Projections
         │
         v
Phase 6: Graph Layer (can parallel Phase 5)
    └── IGraphStore + NetworkX
```

#### **How**: How to remediate?

**Recommended Approach**: Bottom-up implementation starting with Shared Kernel.

1. Create `src/shared_kernel/__init__.py` exposing all shared types
2. Migrate `ProjectId` to extend `VertexId` (or create alias)
3. Implement minimal event infrastructure
4. Build Task aggregate as proof-of-concept
5. Add architecture tests to enforce layer boundaries

### NASA SE Risk Assessment

| Gap ID | Gap Description | Likelihood (1-5) | Impact (1-5) | Risk Score | Priority |
|--------|-----------------|------------------|--------------|------------|----------|
| **G-001** | Shared Kernel missing | 5 (certain) | 5 (blocks all) | **25** | P0 |
| **G-002** | Event Sourcing missing | 5 (certain) | 5 (core feature) | **25** | P0 |
| **G-003** | VertexId hierarchy missing | 5 (certain) | 4 (graph unusable) | **20** | P1 |
| **G-004** | AggregateRoot missing | 5 (certain) | 5 (no aggregates) | **25** | P0 |
| **G-005** | Task/Phase/Plan missing | 5 (certain) | 5 (core feature) | **25** | P0 |
| **G-006** | Test coverage zero | 5 (certain) | 4 (regression risk) | **20** | P1 |
| **G-007** | CQRS handlers embedded | 4 (confirmed) | 3 (testing impact) | **12** | P2 |
| **G-008** | Graph layer missing | 5 (certain) | 3 (future feature) | **15** | P3 |
| **G-009** | JerryUri missing | 5 (certain) | 2 (cross-system) | **10** | P3 |
| **G-010** | RepositoryError misplaced | 4 (confirmed) | 1 (minor) | **4** | P4 |

**Risk Matrix Visualization**:
```
         IMPACT
         1    2    3    4    5
     ┌────┬────┬────┬────┬────┐
   5 │    │G-09│G-08│G-03│G-01│
L    │    │    │    │G-06│G-02│
I  4 │G-10│    │G-07│    │G-04│
K    │    │    │    │    │G-05│
E  3 │    │    │    │    │    │
L    │    │    │    │    │    │
I  2 │    │    │    │    │    │
H    │    │    │    │    │    │
O  1 │    │    │    │    │    │
O    │    │    │    │    │    │
D    └────┴────┴────┴────┴────┘
```

### Prioritized Remediation Plan

| Priority | Gap IDs | Description | Effort | Dependency |
|----------|---------|-------------|--------|------------|
| **P0** | G-001, G-004 | Create Shared Kernel with EntityBase | 2-3 days | None |
| **P0** | G-002 | Implement Event Sourcing core | 3-4 days | P0 (Shared Kernel) |
| **P0** | G-005 | Build Task aggregate | 2-3 days | P0 (Event Sourcing) |
| **P1** | G-003 | Complete VertexId hierarchy | 1-2 days | P0 (Shared Kernel) |
| **P1** | G-006 | Add test infrastructure | 3-4 days | Parallel with P0 |
| **P2** | G-007 | Separate CQRS handlers | 1-2 days | After P0 |
| **P3** | G-008 | Graph layer | 3-4 days | P0 (VertexId) |
| **P3** | G-009 | JerryUri implementation | 0.5 days | P0 (Shared Kernel) |
| **P4** | G-010 | Move RepositoryError | 0.5 days | Any time |

**Total Estimated Effort**: 17-24 days

### Dependency Graph

```
                    ┌─────────────────┐
                    │ Shared Kernel   │
                    │ (P0: G-001)     │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        v                    v                    v
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ VertexId      │   │ Event         │   │ EntityBase    │
│ Hierarchy     │   │ Sourcing      │   │ (IAuditable   │
│ (P1: G-003)   │   │ (P0: G-002)   │   │ +IVersioned)  │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        │                   v                   │
        │           ┌───────────────┐           │
        │           │ AggregateRoot │           │
        │           │ (P0: G-004)   │<──────────┘
        │           └───────┬───────┘
        │                   │
        v                   v
┌───────────────┐   ┌───────────────┐
│ Graph Layer   │   │ Task/Phase/   │
│ (P3: G-008)   │   │ Plan          │
└───────────────┘   │ (P0: G-005)   │
                    └───────┬───────┘
                            │
                            v
                    ┌───────────────┐
                    │ CQRS Handlers │
                    │ (P2: G-007)   │
                    └───────────────┘
```

---

## Evidence Citations

### Canon Evidence

| Pattern | Canon Section | Line Numbers | Key Quote |
|---------|---------------|--------------|-----------|
| VertexId | PAT-001 | L65-111 | `@dataclass(frozen=True) class VertexId(ABC)` |
| IAuditable | PAT-005 | L276-309 | `created_by`, `created_at`, `updated_by`, `updated_at` |
| IVersioned | PAT-006 | L311-340 | `version starts at 0 or 1 after creation event` |
| AggregateRoot | PAT-008 | L414-505 | `_raise_event()`, `load_from_history()` |
| DomainEvent | PAT-011 | L584-654 | `event_id`, `occurred_at`, `to_cloud_event()` |
| IEventStore | PAT-013 | L723-818 | `append()`, `read()`, `get_current_position()` |
| Command | PAT-014 | L824-894 | `@dataclass(frozen=True) class Command(ABC)` |
| Query | PAT-015 | L896-970 | `@dataclass(frozen=True) class Query(ABC)` |
| Hexagonal | PAT-020 | L1261-1370 | `Domain ONLY stdlib, Application MAY domain` |

### Implementation Evidence

| Component | File Path | Line Numbers | Finding |
|-----------|-----------|--------------|---------|
| ProjectId | `domain/value_objects/project_id.py` | L32-99 | Uses `PROJ-{nnn}-{slug}`, not VertexId |
| DomainError | `domain/exceptions.py` | L12-22 | Base class exists, partial hierarchy |
| ProjectInfo | `domain/entities/project_info.py` | L16-109 | No IAuditable, no IVersioned |
| IProjectRepository | `application/ports/project_repository.py` | L14-72 | Specific, not generic |
| ScanProjectsQuery | `application/queries/scan_projects.py` | L15-31 | Not frozen, handler embedded |
| events/__init__.py | `domain/events/__init__.py` | L1-9 | Empty, no events defined |
| RepositoryError | `application/ports/exceptions.py` | L11-20 | In wrong layer (should be infra) |

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Canon Patterns Defined | 26 |
| Patterns Fully Implemented | 1 (Hexagonal) |
| Patterns Partially Implemented | 4 |
| Patterns Missing | 21 |
| Implementation Percentage | ~15-20% |
| Critical Gaps (P0) | 5 |
| High Priority Gaps (P1) | 2 |
| Estimated Remediation Effort | 17-24 days |

---

## Recommendations

### Immediate Actions (This Sprint)

1. **Create `src/shared_kernel/` directory** with stub files
2. **Implement `VertexId` base class** following PAT-001 specification
3. **Add `TaskId`, `PhaseId`, `PlanId`** following PAT-002 specification
4. **Set up `tests/architecture/`** with layer dependency checks

### Short-Term (Next 2 Sprints)

1. **Complete Event Sourcing foundation** (DomainEvent, IEventStore)
2. **Implement AggregateRoot** following PAT-008
3. **Build Task aggregate** as proof-of-concept
4. **Separate CQRS handlers** from definitions

### Long-Term (Future Sprints)

1. **Complete Phase and Plan aggregates**
2. **Implement Graph layer**
3. **Add Knowledge Management** bounded context
4. **Implement projections and read models**

---

## References

### Source Documents

| ID | Title | Location |
|----|-------|----------|
| e-011-v1 | Jerry Design Canon | `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md` |
| e-007 | Previous Gap Analysis | `projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-e-007-implementation-gap-analysis.md` |

### Implementation Files Analyzed

| Path | Purpose |
|------|---------|
| `src/session_management/domain/exceptions.py` | Domain exceptions |
| `src/session_management/domain/value_objects/project_id.py` | ProjectId value object |
| `src/session_management/domain/value_objects/project_status.py` | ProjectStatus enum |
| `src/session_management/domain/entities/project_info.py` | ProjectInfo entity |
| `src/session_management/application/ports/project_repository.py` | IProjectRepository port |
| `src/session_management/application/queries/scan_projects.py` | ScanProjectsQuery |
| `src/session_management/infrastructure/adapters/filesystem_project_adapter.py` | Filesystem adapter |

---

*Document created by ps-analyst agent v2.0.0*
*Cycle 1 Analysis completed: 2026-01-09*
*Ready for ps-evaluator review*
