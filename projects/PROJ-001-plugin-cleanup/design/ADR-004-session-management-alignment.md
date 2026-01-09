# ADR-004: Session Management Bounded Context Alignment

> **ADR ID:** ADR-004
> **Status:** PROPOSED
> **Created:** 2026-01-09
> **Author:** Claude (Session cc/task-subtask)
> **Supersedes:** ADR-003-code-structure.md (partial)
> **References:**
> - PS_EXPORT_DOMAIN_ALIGNMENT.md (PROP-001)
> - JERRY_URI_SPECIFICATION.md (SPEC-001)
> - work-034-e-003-unified-design.md

---

## Executive Summary

This ADR documents the analysis of existing design documents and proposes alignment of the
`session_management` bounded context with the Jerry unified design patterns. The current
implementation deviates from established patterns (IAuditable, IVersioned, VertexId, JerryUri)
that were designed for graph database readiness and cross-context consistency.

**Key Findings:**
1. Current `ProjectId` format (`PROJ-NNN-slug`) does not follow `VertexId` pattern
2. Domain entities lack IAuditable properties (created_by, updated_by, created_on, updated_on)
3. Domain entities lack IVersioned properties (content_hash, hash_algorithm, version)
4. No JerryUri integration for unified resource identification
5. `session-management` not registered as a Jerry-owned domain in SPEC-001

**Recommendation:** Refactor `session_management` bounded context to align with unified design,
treating it as a **core subdomain** essential to solving context rot.

---

## I. Document Analysis

### A. Documents Reviewed

| Document | Key Insights |
|----------|--------------|
| `PS_EXPORT_DOMAIN_ALIGNMENT.md` | IAuditable, IVersioned, EntityBase, JerryId patterns |
| `JERRY_URI_SPECIFICATION.md` | Jerry URI scheme for all resources (`jer:partition:tenant:domain:resource`) |
| `work-034-e-003-unified-design.md` | Shared Kernel, VertexId hierarchy, bounded context relationships |

### B. Shared Kernel Components (from unified-design)

The Shared Kernel defines common infrastructure that all bounded contexts inherit:

```
Shared Kernel
├── VertexId (abstract base for all IDs)
├── JerryUri (unified resource naming)
├── CloudEventEnvelope (event sourcing)
├── IAuditable (audit trail interface)
├── IVersioned (optimistic concurrency)
├── IGraphStore (graph port)
├── IEventStore (event port)
└── ISemanticIndex (vector search port)
```

### C. IAuditable Interface Requirements

From `PS_EXPORT_DOMAIN_ALIGNMENT.md`:

```python
class IAuditable(ABC):
    """All entities must track who created/modified and when."""

    @property
    def created_on(self) -> datetime: ...

    @property
    def updated_on(self) -> datetime: ...

    @property
    def created_by(self) -> str: ...  # Format: "user:name" or "system:name"

    @property
    def updated_by(self) -> str: ...
```

**Current Gap:** `ProjectInfo` has no audit properties.

### D. IVersioned Interface Requirements

From `PS_EXPORT_DOMAIN_ALIGNMENT.md`:

```python
class IVersioned(ABC):
    """Entities with optimistic concurrency support."""

    @property
    def content_hash(self) -> str: ...  # 16 hex chars, SHA-256

    @property
    def hash_algorithm(self) -> str: ...  # e.g., "sha256"

    @property
    def version(self) -> str: ...  # "{timestamp}_{hash[:8]}"
```

**Current Gap:** `ProjectInfo` has no versioning/hashing.

### E. VertexId Pattern Requirements

From `work-034-e-003-unified-design.md`:

```python
class VertexId(ABC):
    """Abstract base for all graph-ready identifiers."""
    value: str

    def __str__(self) -> str: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other) -> bool: ...

class TaskId(VertexId):
    """Format: WORK-NNN"""
    pass

class PhaseId(VertexId):
    """Format: PHASE-NNN"""
    pass
```

**Current Gap:** `ProjectId` uses `PROJ-NNN-slug` format which:
- Embeds human-readable slug in the ID (non-standard)
- Does not extend `VertexId`
- Is not graph-ready

### F. JerryUri Requirements

From `JERRY_URI_SPECIFICATION.md` (SPEC-001):

```
Pattern: jer[+version]:<partition>:[tenant]:<domain>:<resource_type>:<resource_id>[+version]

Examples:
- jer:jer::work-tracker:task:task-042+abc123
- jer:jer:victor-lau:knowledge:wisdom:wiz-001
```

**Current Gap:** No JerryUri integration in `session_management`.

---

## II. Current Implementation Analysis

### A. Current `ProjectId` Structure

```python
# Current: src/session_management/domain/value_objects/project_id.py
@dataclass(frozen=True)
class ProjectId:
    value: str      # Full ID: "PROJ-001-plugin-cleanup"
    number: int     # Extracted: 1
    slug: str       # Extracted: "plugin-cleanup"

    # Pattern: PROJ-NNN-slug (kebab-case)
```

**Issues:**
1. **Format mismatch**: `PROJ-NNN-slug` vs unified `prefix-NNN` pattern
2. **Slug in ID**: Human-readable slug embedded in identifier
3. **Not VertexId**: Does not extend shared kernel base class
4. **Not graph-ready**: No vertex label or properties

### B. Current `ProjectInfo` Structure

```python
# Current: src/session_management/domain/entities/project_info.py
@dataclass
class ProjectInfo:
    id: ProjectId
    status: ProjectStatus = ProjectStatus.UNKNOWN
    has_plan: bool = False
    has_tracker: bool = False
    path: str | None = None
```

**Issues:**
1. **No IAuditable**: Missing created_on/by, updated_on/by
2. **No IVersioned**: Missing content_hash, version
3. **No JerryUri**: Missing unified resource identifier
4. **No session_id**: Missing provenance tracking
5. **No metadata/tags**: Missing extensibility fields

### C. Design Intent Questions

The current design raises questions:

| Question | Current Answer | Unified Answer |
|----------|----------------|----------------|
| Where is project info stored? | Filesystem (directory) | Could be graph vertex |
| Is project ID the directory name? | Yes (`PROJ-001-plugin-cleanup/`) | ID separate from path |
| Why slug in ID? | Human-readable directories | Slug as separate property |
| Is project graph-ready? | No | Yes (via VertexId) |

---

## III. Proposed Alignment

### A. Register `session-management` Domain

Add to `JERRY_URI_SPECIFICATION.md` Section IV.B:

| Domain | Description |
|--------|-------------|
| `session-management` | Session and project workspace management |

### B. New Entity Types

| Entity Type | Domain | Description | ID Pattern |
|-------------|--------|-------------|------------|
| `session` | session-management | Claude Code working session | `SES-NNN` |
| `project` | session-management | Project workspace | `PROJ-NNN` |

### C. Aligned `ProjectId` Value Object

```python
from src.shared_kernel.identity import VertexId

@dataclass(frozen=True)
class ProjectId(VertexId):
    """
    Strongly-typed project identifier following VertexId pattern.

    Format: PROJ-NNN (e.g., PROJ-001, PROJ-042)

    Note: The human-readable slug is stored in ProjectInfo.slug,
    NOT in the identifier. This separates identity from display.
    """
    PREFIX = "PROJ"

    sequence: int
    uuid: str = ""

    @property
    def value(self) -> str:
        """Short form: PROJ-001"""
        return f"{self.PREFIX}-{self.sequence:03d}"

    @property
    def full_form(self) -> str:
        """Full form with UUID: PROJ-001-abc12345"""
        if self.uuid:
            return f"{self.PREFIX}-{self.sequence:03d}-{self.uuid[:8]}"
        return self.value

    def to_uri(self, tenant_id: str = "") -> JerryUri:
        """Generate Jerry URI for this project."""
        return JerryUri.for_entity(
            domain="session-management",
            entity_type="project",
            entity_id=self.full_form,
            tenant_id=tenant_id
        )

    @classmethod
    def parse(cls, value: str) -> "ProjectId":
        """Parse PROJ-NNN or PROJ-NNN-uuid format."""
        # Implementation
```

### D. Aligned `ProjectInfo` Entity

```python
from src.shared_kernel.base import EntityBase

@dataclass
class ProjectInfo(EntityBase):
    """
    Project workspace entity with full unified design compliance.

    Implements: IAuditable, IVersioned, graph-ready
    """
    # Identity (from EntityBase)
    id: ProjectId
    uri: JerryUri = field(init=False)  # Computed

    # Display (from EntityBase)
    slug: str                           # URL-safe: "plugin-cleanup" (max 75 chars)
    name: str                           # Human-readable: "Plugin Cleanup Project"
    short_description: str = ""         # Brief summary (max 200 chars)
    long_description: str = ""          # Detailed description (Markdown)

    # Status
    status: ProjectStatus = ProjectStatus.UNKNOWN

    # Provenance (IAuditable)
    created_on: datetime = field(default_factory=datetime.utcnow)
    updated_on: datetime = field(default_factory=datetime.utcnow)
    created_by: str = "system:unknown"  # Format: "user:name" or "system:name"
    updated_by: str = "system:unknown"
    session_id: str = ""                # Session that created/modified

    # Change Detection (IVersioned)
    content_hash: str = ""              # SHA-256, 16 hex chars
    hash_algorithm: str = "sha256"
    version: str = ""                   # Computed: "{timestamp}_{hash[:8]}"

    # Graph Properties
    label: str = "Project"              # Vertex label
    properties: dict = field(default_factory=dict)

    # Extensibility
    metadata: dict = field(default_factory=dict)
    tags: list = field(default_factory=list)

    # Project-specific
    path: str = ""                      # Filesystem path (for filesystem adapter)
    has_plan: bool = False
    has_tracker: bool = False

    def __post_init__(self):
        """Compute derived fields."""
        # Compute URI
        if not hasattr(self, 'uri') or self.uri is None:
            object.__setattr__(self, 'uri', self.id.to_uri())

        # Compute content hash if not provided
        if not self.content_hash:
            self.content_hash = self._compute_content_hash()

        # Compute version
        if not self.version:
            self.version = self._compute_version()
```

### E. New `SessionId` Value Object

```python
@dataclass(frozen=True)
class SessionId(VertexId):
    """
    Strongly-typed session identifier.

    Format: SES-NNN (e.g., SES-001) or SES-{uuid}
    """
    PREFIX = "SES"

    sequence: int | None = None
    uuid: str = ""

    @property
    def value(self) -> str:
        if self.uuid:
            return f"{self.PREFIX}-{self.uuid[:8]}"
        return f"{self.PREFIX}-{self.sequence:03d}"
```

### F. Directory Structure with Shared Kernel

```
src/
├── shared_kernel/                     # NEW: Shared Kernel
│   ├── __init__.py
│   ├── identity/
│   │   ├── __init__.py
│   │   ├── vertex_id.py              # VertexId abstract base
│   │   ├── jerry_id.py               # JerryId implementation
│   │   └── jerry_uri.py              # JerryUri value object
│   ├── base/
│   │   ├── __init__.py
│   │   ├── auditable.py              # IAuditable interface
│   │   ├── versioned.py              # IVersioned interface
│   │   └── entity_base.py            # EntityBase dataclass
│   └── events/
│       ├── __init__.py
│       └── cloud_event.py            # CloudEventEnvelope
│
├── session_management/                # Bounded Context
│   ├── domain/
│   │   ├── value_objects/
│   │   │   ├── project_id.py         # REFACTOR: Extend VertexId
│   │   │   ├── session_id.py         # NEW: Session identifier
│   │   │   ├── project_status.py
│   │   │   └── validation_result.py
│   │   ├── entities/
│   │   │   ├── project_info.py       # REFACTOR: Extend EntityBase
│   │   │   └── session.py            # NEW: Session aggregate root
│   │   └── ...
│   └── ...
```

---

## IV. Migration Strategy

### A. Phase 1: Create Shared Kernel (Prerequisites)

1. Create `src/shared_kernel/` directory structure
2. Implement `VertexId` abstract base class
3. Implement `JerryUri` value object (from SPEC-001)
4. Implement `IAuditable` and `IVersioned` interfaces
5. Implement `EntityBase` dataclass

### B. Phase 2: Refactor ProjectId

1. Change format from `PROJ-NNN-slug` to `PROJ-NNN`
2. Extend `VertexId`
3. Add `to_uri()` method
4. Move slug to `ProjectInfo.slug` property
5. Update filesystem adapter to map ID to directory name

### C. Phase 3: Refactor ProjectInfo

1. Extend `EntityBase`
2. Add IAuditable properties
3. Add IVersioned properties
4. Add JerryUri computation
5. Add metadata and tags

### D. Phase 4: Update Adapters

1. Update `FilesystemProjectAdapter` to:
   - Map `ProjectId` (PROJ-NNN) to directory name (`PROJ-NNN-{slug}/`)
   - Read/write IAuditable fields from metadata file
   - Compute content_hash from project contents
2. Update tests

### E. Backward Compatibility

The filesystem uses `PROJ-NNN-slug/` directory names. Options:

| Option | Pros | Cons |
|--------|------|------|
| **A: Directory = ID** | Simple mapping | Slug in ID (current problem) |
| **B: Directory = ID-slug** | Human-readable dirs | ID ≠ directory name |
| **C: Metadata file** | Clean separation | Extra file |

**Recommendation:** Option B - Directory name `PROJ-NNN-slug/` but ID is `PROJ-NNN`.
The adapter maps between them using a `project.yaml` metadata file.

---

## V. Jerry URI Examples for Session Management

| Resource | Jerry URI |
|----------|-----------|
| Project entity | `jer:jer::session-management:project:PROJ-001+abc12345` |
| Session entity | `jer:jer:victor-lau:session-management:session:SES-042` |
| CreateProject command | `jer:jer::session-management:actions/CreateProject` |
| ProjectCreated event | `jer:jer::session-management:facts/ProjectCreated` |
| Project schema | `jer:jer::session-management:project:CreateProjectRequest+1.0.0` |

---

## VI. Discoveries

### DISC-060: Session Management is Core Domain

**ID:** DISC-060
**Name:** Session Management is a Core Subdomain for Context Rot Solution

**Description:**
Session management is not merely infrastructure - it is a core subdomain essential to Jerry's
mission of solving context rot. Multiple working sessions, session continuity, and project
isolation are fundamental to the framework. Therefore, `session_management` entities must
adhere to the same unified design patterns (IAuditable, IVersioned, VertexId, JerryUri) as
Work Tracker and Knowledge Management.

**Evidence:**
- Context rot research (Chroma) identifies session state loss as key degradation factor
- Jerry's architecture document lists session persistence as primary goal
- CLAUDE.md states "Jerry addresses [context rot] through filesystem as infinite memory"

**Impact:**
- L0: Sessions and projects get proper identity and tracking like other Jerry things
- L1: Implement IAuditable, IVersioned, VertexId for session_management entities
- L2: Enables future graph queries across sessions, project analytics, and audit trails

### DISC-061: Slug-in-ID Anti-Pattern

**ID:** DISC-061
**Name:** Embedding Slug in Identifier is an Anti-Pattern

**Description:**
The current `ProjectId` format `PROJ-NNN-slug` embeds a human-readable slug directly in the
identifier. This violates separation of concerns - identity should be stable while display
names may change. The unified design separates these: `JerryId` provides stable identity,
while `slug` is a separate property on `EntityBase`.

**Evidence:**
- PS_EXPORT_DOMAIN_ALIGNMENT.md defines `slug` as a separate property (max 75 chars)
- VertexId pattern uses `prefix-NNN` without embedded names
- Renaming a project would require changing its ID (identity instability)

**Impact:**
- L0: Project IDs should be short like `PROJ-001`, with name separate
- L1: Refactor ProjectId to `PROJ-NNN` format, add slug to ProjectInfo
- L2: Stable identity enables rename operations without breaking references

---

## VII. Open Questions

1. **Session lifecycle**: When is a Session created vs. resumed? What triggers SessionCreated event?

2. **Tenant ID**: For single-user Claude Code, is tenant_id always empty, or should it be the
   user's identifier?

3. **Graph storage**: Will session_management entities be stored in the graph, or only
   filesystem? If graph, what edges connect them to Work Tracker?

4. **Event sourcing**: Should ProjectCreated, SessionStarted events be persisted in the
   event store for audit/replay?

---

## VIII. Decision

**Status:** PROPOSED

**Recommendation:** Approve and implement alignment in the following order:

1. Create `src/shared_kernel/` with VertexId, JerryUri, IAuditable, IVersioned, EntityBase
2. Refactor `ProjectId` to extend VertexId, remove slug from ID
3. Refactor `ProjectInfo` to extend EntityBase with all required properties
4. Add `SessionId` and `Session` entities
5. Update adapters and tests

**Next Steps:**
1. Review this ADR with user
2. Update JERRY_URI_SPECIFICATION.md to register `session-management` domain
3. Begin implementation of shared kernel

---

## IX. References

### Specification Documents
- [SPEC-001] JERRY_URI_SPECIFICATION.md
- [PROP-001] PS_EXPORT_DOMAIN_ALIGNMENT.md
- work-034-e-003-unified-design.md

### Prior ADRs
- ADR-003-code-structure.md (bounded context directory structure)

### External
- [RFC 8141: URN Syntax](https://www.rfc-editor.org/rfc/rfc8141.html)
- [Clean DDD: Audit Metadata](https://medium.com/unil-ci-software-engineering/clean-ddd-lessons-audit-metadata-for-domain-entities-5935a5c6db5b)
- [Evans, E. Domain-Driven Design](https://www.oreilly.com/library/view/domain-driven-design/9780321125217/)

---

## X. Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-09 | Initial proposal based on document analysis |
