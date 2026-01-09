# Exploration: Unified Design Alignment Analysis

**Document ID**: EXPLORATION-001
**Date**: 2026-01-09
**Author**: Claude (Session cc/task-subtask)
**Status**: COMPLETE
**Entry Type**: Analysis & Synthesis
**Severity**: HIGH (architectural alignment)

---

## Executive Summary

This exploration documents the comprehensive analysis of Jerry's unified design patterns and
their required application to the `session_management` bounded context. The analysis revealed
significant gaps between the current implementation and the established architectural patterns
designed for graph database readiness, audit compliance, and cross-context consistency.

**Key Finding**: The `session_management` bounded context must be refactored to align with
the unified design patterns (VertexId, IAuditable, IVersioned, JerryUri, EntityBase) that
were established in prior design documents but not implemented in the recent restructuring.

---

## 1. Analysis Scope

### 1.1 Documents Analyzed

| Document | Location | Key Content |
|----------|----------|-------------|
| PS_EXPORT_DOMAIN_ALIGNMENT.md | `projects/archive/proposals/` | IAuditable, IVersioned, EntityBase, JerryId |
| JERRY_URI_SPECIFICATION.md | `docs/specifications/` | Jerry URI scheme (SPEC-001) |
| work-034-e-003-unified-design.md | `projects/archive/design/` | Shared Kernel, VertexId, bounded contexts |
| work-034-e-002-domain-synthesis.md | `projects/archive/design/` | Domain model synthesis (referenced) |

### 1.2 Analysis Questions

1. What patterns were established for domain entities?
2. How should `session_management` entities comply with these patterns?
3. What is the migration path from current to aligned implementation?
4. What are the implications for graph database readiness?

---

## 2. Unified Design Patterns Discovered

### 2.1 IAuditable Interface

**Source**: PS_EXPORT_DOMAIN_ALIGNMENT.md (Section II.A)

**Purpose**: Track provenance for all domain entities.

**Required Properties**:

| Property | Type | Format | Description |
|----------|------|--------|-------------|
| `created_on` | datetime | ISO 8601 | When entity was created |
| `updated_on` | datetime | ISO 8601 | When entity was last modified |
| `created_by` | str | `user:name` or `system:name` | Who/what created |
| `updated_by` | str | `user:name` or `system:name` | Who/what last modified |

**Implementation Pattern**:

```python
class IAuditable(ABC):
    """
    Interface for entities requiring audit trail.

    Prior Art:
    - Clean DDD: Audit metadata for domain entities (UNIL Engineering)
    - EF Core: IAuditableEntity pattern

    Citation: https://medium.com/unil-ci-software-engineering/
              clean-ddd-lessons-audit-metadata-for-domain-entities-5935a5c6db5b
    """

    @property
    @abstractmethod
    def created_on(self) -> datetime: ...

    @property
    @abstractmethod
    def updated_on(self) -> datetime: ...

    @property
    @abstractmethod
    def created_by(self) -> str: ...

    @property
    @abstractmethod
    def updated_by(self) -> str: ...
```

**Rationale**:
- Compliance requirements (who changed what, when)
- Debugging and troubleshooting
- Event sourcing integration
- Graph vertex meta-properties

### 2.2 IVersioned Interface

**Source**: PS_EXPORT_DOMAIN_ALIGNMENT.md (Section II.B)

**Purpose**: Enable optimistic concurrency and change detection.

**Required Properties**:

| Property | Type | Format | Description |
|----------|------|--------|-------------|
| `content_hash` | str | 16 hex chars | SHA-256 of content fields |
| `hash_algorithm` | str | e.g., "sha256" | Algorithm used |
| `version` | str | `{timestamp}_{hash[:8]}` | Composite version |

**Implementation Pattern**:

```python
class IVersioned(ABC):
    """
    Interface for versioned entities with optimistic concurrency support.

    Version format: "{ISO8601_timestamp}_{content_hash[:8]}"
    Example: "2026-01-08T10:30:00Z_a1b2c3d4"
    """

    @property
    @abstractmethod
    def version(self) -> str: ...

    @property
    @abstractmethod
    def content_hash(self) -> str: ...

    @property
    @abstractmethod
    def hash_algorithm(self) -> str: ...
```

**Rationale**:
- Optimistic concurrency control
- Change detection without full content comparison
- Cache invalidation
- Event sourcing version tracking

### 2.3 VertexId Abstract Base

**Source**: work-034-e-003-unified-design.md (Section 4.1)

**Purpose**: Unified identity base for graph database readiness.

**Pattern**:

```python
class VertexId(ABC):
    """
    Abstract base for all graph-ready identifiers.

    All entity IDs (TaskId, PhaseId, ProjectId, etc.) extend this
    to ensure consistent identity behavior across the system.
    """
    value: str

    def __str__(self) -> str:
        return self.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other) -> bool:
        if isinstance(other, VertexId):
            return self.value == other.value
        return False
```

**Derived ID Classes**:

| Class | Format | Domain |
|-------|--------|--------|
| TaskId | `WORK-NNN` | work-tracker |
| PhaseId | `PHASE-NNN` | work-tracker |
| PlanId | `PLAN-NNN` | work-tracker |
| KnowledgeId | `PAT-NNN`, `LES-NNN`, `ASM-NNN` | knowledge |
| ProjectId | `PROJ-NNN` | session-management |
| SessionId | `SES-NNN` | session-management |

**Key Insight**: ID format is `PREFIX-NNN`, NOT `PREFIX-NNN-slug`. Human-readable
slugs are stored as separate properties on the entity.

### 2.4 JerryUri Value Object

**Source**: JERRY_URI_SPECIFICATION.md (SPEC-001)

**Purpose**: Unified resource identification across the system.

**Format**:
```
jer[+scheme_version]:<partition>:[tenant_id]:<domain>:<resource_type>:<resource_id>[+version]
```

**Examples**:

| Resource | Jerry URI |
|----------|-----------|
| Task | `jer:jer::work-tracker:task:WORK-042+abc12345` |
| Phase | `jer:jer::work-tracker:phase:PHASE-001` |
| Project | `jer:jer::session-management:project:PROJ-001` |
| Session | `jer:jer:victor-lau:session-management:session:SES-042` |
| CreateTask action | `jer:jer::work-tracker:actions/CreateTask` |
| TaskCreated event | `jer:jer::work-tracker:facts/TaskCreated` |

**Implementation**: See `JerryUri` value object in SPEC-001 Section V.A.

### 2.5 EntityBase Dataclass

**Source**: PS_EXPORT_DOMAIN_ALIGNMENT.md (Section II.C)

**Purpose**: Common base for all domain entities.

**Required Properties**:

| Category | Properties |
|----------|------------|
| Identity | `id` (JerryId), `uri` (JerryUri), `slug`, `label` |
| Display | `name`, `short_description`, `long_description` |
| Provenance | `created_on`, `updated_on`, `created_by`, `updated_by`, `session_id` |
| Versioning | `content_hash`, `hash_algorithm`, `version` |
| Graph | `label`, `properties` |
| Extensibility | `metadata` (Dict), `tags` (List) |

### 2.6 Edge Types for Relationships

**Source**: PS_EXPORT_DOMAIN_ALIGNMENT.md (Section IV.B)

**Pattern**: Relationships are first-class Edge entities, not embedded properties.

| Edge Label | From | To | Properties |
|------------|------|----|------------|
| `CONTAINS` | Phase | Task | position: int |
| `CONTAINS` | Plan | Phase | position: int |
| `HAS_SUBTASK` | Task | Task | position: int |
| `BLOCKS` | Task | Task | reason: str |
| `DEPENDS_ON` | Task | Task | type: str |

**Future Session Management Edges**:

| Edge Label | From | To | Properties |
|------------|------|----|------------|
| `BELONGS_TO` | Session | Project | - |
| `CREATED_IN` | Task | Session | - |
| `MODIFIED_IN` | Entity | Session | timestamp |

---

## 3. Gap Analysis

### 3.1 Current Implementation State

The `session_management` bounded context was recently restructured to:

```
src/session_management/
├── domain/
│   ├── value_objects/
│   │   ├── project_id.py       # PROJ-NNN-slug format
│   │   ├── project_status.py   # Enum
│   │   └── validation_result.py
│   ├── entities/
│   │   └── project_info.py     # Basic entity
│   └── exceptions.py
├── application/
│   ├── ports/
│   └── queries/
└── infrastructure/
    └── adapters/
```

### 3.2 Identified Gaps

| Gap | Current | Required | Severity |
|-----|---------|----------|----------|
| **ID Format** | `PROJ-NNN-slug` | `PROJ-NNN` (VertexId) | HIGH |
| **VertexId inheritance** | No | Yes | HIGH |
| **IAuditable** | No | Yes | HIGH |
| **IVersioned** | No | Yes | MEDIUM |
| **JerryUri** | No | Yes | MEDIUM |
| **EntityBase** | No | Yes | HIGH |
| **session_id tracking** | No | Yes | HIGH |
| **metadata/tags** | No | Yes | LOW |
| **Shared Kernel** | Does not exist | Must create | HIGH |

### 3.3 Root Cause

The restructuring in this session focused on directory organization (bounded context
structure) without reviewing the existing design documents that defined entity patterns.
This was an oversight - the documents existed and had clear patterns that should have
been followed.

---

## 4. Synthesis: Alignment Requirements

### 4.1 Shared Kernel Creation

The Shared Kernel must be created as a prerequisite for alignment:

```
src/shared_kernel/
├── __init__.py
├── identity/
│   ├── __init__.py
│   ├── vertex_id.py          # Abstract base
│   ├── jerry_id.py           # prefix/sequence/uuid
│   └── jerry_uri.py          # URI value object
├── base/
│   ├── __init__.py
│   ├── auditable.py          # IAuditable
│   ├── versioned.py          # IVersioned
│   └── entity_base.py        # EntityBase
└── events/
    ├── __init__.py
    └── cloud_event.py        # CloudEventEnvelope
```

### 4.2 ProjectId Refactoring

**From**:
```python
@dataclass(frozen=True)
class ProjectId:
    value: str      # "PROJ-001-plugin-cleanup"
    number: int     # 1
    slug: str       # "plugin-cleanup"
```

**To**:
```python
@dataclass(frozen=True)
class ProjectId(VertexId):
    PREFIX = "PROJ"
    sequence: int
    uuid: str = ""

    @property
    def value(self) -> str:
        return f"{self.PREFIX}-{self.sequence:03d}"
```

### 4.3 ProjectInfo Refactoring

**From**:
```python
@dataclass
class ProjectInfo:
    id: ProjectId
    status: ProjectStatus = ProjectStatus.UNKNOWN
    has_plan: bool = False
    has_tracker: bool = False
    path: str | None = None
```

**To**:
```python
@dataclass
class ProjectInfo(EntityBase):
    # Identity (inherited)
    id: ProjectId
    uri: JerryUri  # computed

    # Display
    slug: str                    # "plugin-cleanup" (moved from ID)
    name: str                    # "Plugin Cleanup Project"
    short_description: str = ""
    long_description: str = ""

    # Status
    status: ProjectStatus = ProjectStatus.UNKNOWN

    # Provenance (IAuditable)
    created_on: datetime
    updated_on: datetime
    created_by: str              # "user:adam" or "system:hook"
    updated_by: str
    session_id: str              # Session that created/modified

    # Versioning (IVersioned)
    content_hash: str
    hash_algorithm: str = "sha256"
    version: str                 # computed

    # Graph
    label: str = "Project"
    properties: dict = field(default_factory=dict)

    # Extensibility
    metadata: dict = field(default_factory=dict)
    tags: list = field(default_factory=list)

    # Project-specific
    path: str = ""
    has_plan: bool = False
    has_tracker: bool = False
```

### 4.4 Filesystem Adapter Considerations

The filesystem uses directory names like `PROJ-001-plugin-cleanup/`. Options:

| Approach | Implementation | Trade-off |
|----------|----------------|-----------|
| **A: project.yaml metadata** | Store slug in metadata file | Extra file, clean separation |
| **B: Directory naming convention** | Parse directory name `PROJ-NNN-{slug}/` | Convention-based, adapter logic |
| **C: Symlinks** | `PROJ-001/` symlink to `PROJ-001-plugin-cleanup/` | Unix-specific |

**Recommendation**: Approach B - Adapter parses directory name to extract ID and slug.

---

## 5. Discoveries

### DISC-060: Session Management is Core Domain

**ID**: DISC-060
**Slug**: session-management-core-domain
**Name**: Session Management is a Core Subdomain

**Short Description**: Session management is not infrastructure - it is a core subdomain
essential to Jerry's mission of solving context rot.

**Long Description**:
The initial assumption that `session_management` was merely infrastructure (filesystem
operations) was incorrect. Session and project management are fundamental to Jerry's
architecture because:

1. Context rot mitigation requires persistent session state
2. Multiple working sessions enable parallel work streams
3. Project isolation prevents cross-contamination of context
4. Session provenance is critical for audit and debugging

Therefore, session_management entities must implement the same patterns (IAuditable,
IVersioned, VertexId, JerryUri) as Work Tracker and Knowledge Management entities.

**Evidence**:
- Chroma research identifies session state loss as key context degradation factor
- CLAUDE.md states "filesystem as infinite memory" as primary mitigation strategy
- User explicitly stated: "Session management is a core domain entity"

**Level Impact**:
- L0: Sessions and projects are important Jerry things that need proper tracking
- L1: Implement IAuditable, IVersioned, VertexId for session_management entities
- L2: Core subdomain status means session entities participate in graph queries,
      event sourcing, and cross-context relationships

### DISC-061: Slug-in-ID Anti-Pattern

**ID**: DISC-061
**Slug**: slug-in-id-antipattern
**Name**: Embedding Slug in Identifier is an Anti-Pattern

**Short Description**: Including human-readable slugs in entity IDs violates separation
of concerns and creates identity instability.

**Long Description**:
The current `ProjectId` format `PROJ-NNN-slug` embeds a display name directly in the
identifier. This is problematic because:

1. **Identity instability**: Renaming a project would change its ID
2. **Separation of concerns**: Identity and display are different concerns
3. **Pattern violation**: Unified design uses `PREFIX-NNN` format
4. **Graph complications**: ID changes would break edge references

The correct approach separates identity (`PROJ-001`) from display (`slug: "plugin-cleanup"`).

**Evidence**:
- PS_EXPORT_DOMAIN_ALIGNMENT.md defines `slug` as a separate property (max 75 chars)
- VertexId pattern in unified design uses `prefix-NNN` without embedded names
- TaskId, PhaseId, PlanId all use `PREFIX-NNN` format

**Level Impact**:
- L0: Project IDs should be short numbers, names are separate
- L1: Refactor ProjectId to `PROJ-NNN`, add `slug` property to ProjectInfo
- L2: Stable identity enables rename operations without breaking references

### DISC-062: Shared Kernel Prerequisite

**ID**: DISC-062
**Slug**: shared-kernel-prerequisite
**Name**: Shared Kernel Must Exist Before Context Alignment

**Short Description**: The Shared Kernel (`src/shared_kernel/`) must be created before
any bounded context can properly align with the unified design.

**Long Description**:
The unified design establishes a Shared Kernel containing:
- VertexId (abstract base for all IDs)
- JerryUri (unified resource naming)
- IAuditable, IVersioned (behavior interfaces)
- EntityBase (common entity properties)
- CloudEventEnvelope (event format)

Without this Shared Kernel, each bounded context would duplicate these definitions,
leading to inconsistency and maintenance burden. The Shared Kernel must be implemented
first, then bounded contexts import and extend its components.

**Evidence**:
- work-034-e-003-unified-design.md Section 2 (Bounded Context Diagram)
- All bounded contexts shown with dependency on Shared Kernel
- DDD pattern: Shared Kernel defines common model subset

**Level Impact**:
- L0: Some code is shared between all parts of Jerry
- L1: Create `src/shared_kernel/` with VertexId, JerryUri, EntityBase
- L2: Shared Kernel is first implementation priority before any context alignment

### DISC-063: Session ID for Provenance

**ID**: DISC-063
**Slug**: session-id-provenance
**Name**: Session ID Required for Provenance Tracking

**Short Description**: All entities must track which session created/modified them
via a `session_id` property.

**Long Description**:
The unified design requires `session_id` on all entities (per PS_EXPORT_DOMAIN_ALIGNMENT.md).
This enables:

1. **Audit trail**: Which session made which changes
2. **Debugging**: Trace issues to specific sessions
3. **Analytics**: Understand work patterns across sessions
4. **Graph queries**: Find all entities created in a session

For session_management entities specifically, this creates a recursive relationship
where Projects and Sessions reference their creating session.

**Evidence**:
- PS_EXPORT_DOMAIN_ALIGNMENT.md EntityBase includes `session_id: str`
- User stated: "we will need to keep track of the session ID"
- CloudEvents use `source` to identify originating session/entity

**Level Impact**:
- L0: Know which Claude Code session created or changed something
- L1: Add `session_id: str` to all entity classes
- L2: Enables session-scoped queries and change tracking

---

## 6. Recommendations

### 6.1 Implementation Priority

| Priority | Task | Rationale |
|----------|------|-----------|
| P0 | Create Shared Kernel | Prerequisite for all alignment |
| P1 | Refactor ProjectId | Core identity fix |
| P1 | Refactor ProjectInfo | Full entity alignment |
| P2 | Add SessionId, Session | New entities for session tracking |
| P2 | Update adapters | Handle ID/slug separation |
| P3 | Add tests | Verify alignment |

### 6.2 Open Questions for User

1. **Session lifecycle**: What triggers SessionCreated? Session resume?
2. **Tenant ID**: Single-user mode - should tenant_id be empty or user identifier?
3. **Graph storage**: Will session_management entities be in graph or filesystem only?
4. **Event sourcing**: Persist ProjectCreated, SessionStarted events?

---

## 7. References

### Specification Documents
- SPEC-001: JERRY_URI_SPECIFICATION.md
- PROP-001: PS_EXPORT_DOMAIN_ALIGNMENT.md
- work-034-e-003-unified-design.md

### Industry Sources
- [RFC 8141: URN Syntax](https://www.rfc-editor.org/rfc/rfc8141.html)
- [Clean DDD: Audit Metadata](https://medium.com/unil-ci-software-engineering/clean-ddd-lessons-audit-metadata-for-domain-entities-5935a5c6db5b)
- [AWS ARN Format](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html)
- [CloudEvents Specification](https://cloudevents.io/)

### Related ADRs
- ADR-003-code-structure.md (directory structure)
- ADR-004-session-management-alignment.md (alignment proposal)

---

## 8. Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-09 | Initial exploration document |
