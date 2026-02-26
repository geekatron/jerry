# Proposal: PS-EXPORT-SPECIFICATION and Domain Model Alignment

> **Proposal ID:** PROP-001
> **Status:** REVISED (v1.2)
> **Created:** 2026-01-08
> **Revised:** 2026-01-08
> **Author:** Claude (Session claude/create-code-plugin-skill-MG1nh)

---

## Executive Summary

This proposal recommends enhancing PS-EXPORT-SPECIFICATION v2.1 to align with Jerry's planned Domain Model properties. The alignment ensures:

1. **Consistency** - Same property patterns across PS entities and Domain entities
2. **Serialization** - Unified JSON + TOON export for all entities
3. **Graph Readiness** - Both PS and Domain entities map to Vertex/Edge model
4. **Provenance** - Common audit trail patterns (IAuditable: created_on, updated_on, created_by, updated_by)
5. **Extensibility** - Metadata dictionary and tags for future needs
6. **Unified Identity** - Jerry URI scheme for all resources (see SPEC-001)

**Recommendation:** Adopt a unified **Entity Base Specification** that both PS-EXPORT and Domain Model inherit from.

**Related Specifications:**
- **SPEC-001:** Jerry URI Scheme (`docs/specifications/JERRY_URI_SPECIFICATION.md`)

---

## I. Current State Analysis

### A. PS-EXPORT-SPECIFICATION v2.1 Common Properties

> **ADDRESSED (AN: feedback):**
> - Added `created_by`, `updated_by` (IAuditable pattern)
> - Added `hash_algorithm` property
> - Added `version` property (Date+Hash composite)
> - Defined slug max length (75 characters, per SEO best practices)
> - Clarified ID as strongly-typed object (JerryId)

| Property | Format | Description | Constraint |
|----------|--------|-------------|------------|
| `id` | `JerryId` object | Strongly typed identifier | Required, immutable |
| `uri` | `JerryUri` | Full resource URI (SPEC-001) | Computed from id |
| `slug` | `kebab-case` | URL-safe identifier | ≤75 chars (SEO optimal) |
| `name` | Free text | Human-readable display name | ≤80 chars |
| `short_description` | Free text | Brief summary | ≤200 chars |
| `long_description` | Markdown | Detailed content | Unlimited |
| `created_on` | ISO 8601 | Creation timestamp | Required |
| `updated_on` | ISO 8601 | Last modification | Required |
| `created_by` | String | User/system that created | Required (IAuditable) |
| `updated_by` | String | User/system that last modified | Required (IAuditable) |
| `session_id` | String | Session provenance | Required |
| `content_hash` | Hex (16 chars) | Content hash for change detection | Required |
| `hash_algorithm` | String | Algorithm used (e.g., "sha256") | Required |
| `version` | String | Composite version (timestamp+hash) | Required |

**Citations:**
- IAuditable pattern: [Clean DDD lessons: audit metadata](https://medium.com/unil-ci-software-engineering/clean-ddd-lessons-audit-metadata-for-domain-entities-5935a5c6db5b)
- Slug length: [Backlinko SEO URL Best Practices](https://backlinko.com/hub/seo/url-slug) - Average top-10 URL is 66 chars; ≤75 recommended

### B. Planned Domain Model Properties (from PLAN.md)

**Task Entity:**

| Property | Type | Description |
|----------|------|-------------|
| `id` | `TaskId` (JerryId) | Strongly typed identifier object |
| `title` | `str` | Task name |
| `description` | `str` | Task details |
| `status` | `TaskStatus` | State machine |
| `created_at` | `datetime` | Creation timestamp |
| `updated_at` | `datetime` | Last update |
| `created_by` | `str` | Creator (IAuditable) |
| `updated_by` | `str` | Last modifier (IAuditable) |
| `subtask_ids` | `List[SubtaskId]` | Child references |
| `metadata` | `Dict[str, str]` | Extensibility |
| `tags` | `List[str]` | Categorization |

**Phase Entity:**

| Property | Type | Description |
|----------|------|-------------|
| `id` | `PhaseId` (JerryId) | Strongly typed identifier object |
| `name` | `str` | Phase name |
| `status` | `PhaseStatus` | State machine |
| `task_ids` | `List[TaskId]` | Child references |
| `metadata` | `Dict[str, str]` | Extensibility |
| `tags` | `List[str]` | Categorization |

### C. Identified Gaps (UPDATED)

> **ADDRESSED (AN: feedback):**
> - Added Metadata dictionary for extensibility
> - Added Tags array for categorization/filtering
> - Clarified relationship representation (see Section IV.B)

| Gap | PS-EXPORT | Domain Model | Resolution |
|-----|-----------|--------------|------------|
| ID Format | Prefix-based (c-001) | Strongly typed (TaskId) | JerryId object with prefix+sequence+uuid |
| Session Tracking | `session_id` | Not planned | Add to Domain |
| Hash | Content hash | Not planned | Add to Domain with algorithm indicator |
| Hash Algorithm | Not specified | Not planned | Add `hash_algorithm` property |
| Version | Not specified | Not planned | Add composite version (timestamp+hash) |
| Slug | URL-safe | Not planned | Add to Domain (max 75 chars) |
| Status | Entity-specific | State machine | PS adopts state machine |
| References | KB refs (kb:type:id) | ID references | Unify reference format |
| Metadata | Not present | Not planned | Add `Dict[str, str]` for extensibility |
| Tags | Not present | Not planned | Add `List[str]` for categorization |
| Relationships | Implicit | Implicit | Explicit Edge entities (Section IV.B) |
| IAuditable | Partial | Partial | Full IAuditable interface |

---

## II. Proposed Unified Entity Base

### A. IAuditable Interface (Prior Art)

Following DDD best practices for audit metadata:

```python
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

class IAuditable(ABC):
    """
    Interface for entities requiring audit trail.

    Prior Art:
    - Clean DDD: Audit metadata for domain entities (UNIL Engineering)
    - EF Core: IAuditableEntity pattern
    - DDD Aggregate Root: Audit information in base class

    Citation: https://medium.com/unil-ci-software-engineering/clean-ddd-lessons-audit-metadata-for-domain-entities-5935a5c6db5b
    """

    @property
    @abstractmethod
    def created_on(self) -> datetime:
        """When the entity was created."""
        ...

    @property
    @abstractmethod
    def updated_on(self) -> datetime:
        """When the entity was last modified."""
        ...

    @property
    @abstractmethod
    def created_by(self) -> str:
        """User or system that created the entity."""
        ...

    @property
    @abstractmethod
    def updated_by(self) -> str:
        """User or system that last modified the entity."""
        ...
```

### B. IVersioned Interface

```python
class IVersioned(ABC):
    """
    Interface for versioned entities with optimistic concurrency support.

    Version format: "{ISO8601_timestamp}_{content_hash[:8]}"
    Example: "2026-01-08T10:30:00Z_a1b2c3d4"
    """

    @property
    @abstractmethod
    def version(self) -> str:
        """Composite version for optimistic concurrency."""
        ...

    @property
    @abstractmethod
    def content_hash(self) -> str:
        """Hash of content fields (16 hex chars)."""
        ...

    @property
    @abstractmethod
    def hash_algorithm(self) -> str:
        """Algorithm used for hashing (e.g., 'sha256')."""
        ...
```

### C. Entity Base Specification (REVISED)

All entities (PS and Domain) should inherit these common properties:

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional

@dataclass
class EntityBase(IAuditable, IVersioned):
    """
    Common base for all Jerry entities.
    Aligns PS-EXPORT-SPECIFICATION with Domain Model.

    Implements:
    - IAuditable: Full audit trail (created_on/by, updated_on/by)
    - IVersioned: Optimistic concurrency (version, content_hash, hash_algorithm)
    - Graph-ready: Vertex label and properties
    - Extensible: Metadata dictionary and tags
    """

    # Identity (Graph-Ready) - ID is a strongly-typed object
    id: "JerryId"                 # Strongly typed, extends VertexId
    uri: "JerryUri" = field(init=False)  # Full resource URI (SPEC-001), computed from id
    slug: str                     # URL-safe identifier (≤75 chars, kebab-case)

    # Display
    name: str                     # Human-readable (≤80 chars)
    short_description: str        # Brief summary (≤200 chars, 1 sentence)
    long_description: str         # Detailed content (Markdown, unlimited)

    # Provenance (IAuditable)
    created_on: datetime          # Creation timestamp (ISO 8601)
    updated_on: datetime          # Last modification (ISO 8601)
    created_by: str               # User/system that created ("user:alice" or "system:scheduler")
    updated_by: str               # User/system that last modified
    session_id: str               # Session that created/modified

    # Change Detection (IVersioned)
    content_hash: str             # SHA-256 of content fields (16 hex chars)
    hash_algorithm: str = "sha256"  # Algorithm used for hashing
    version: str = ""             # Computed: "{timestamp}_{hash[:8]}"

    # Graph Properties
    label: str = ""               # Vertex label for graph storage
    properties: Dict[str, Any] = field(default_factory=dict)  # Additional vertex properties

    # Extensibility (NEW - per feedback)
    metadata: Dict[str, str] = field(default_factory=dict)  # Key-value for extensibility
    tags: List[str] = field(default_factory=list)           # Categorization and filtering

    def __post_init__(self):
        """Compute derived fields."""
        if not self.version:
            self.version = self._compute_version()
        # Compute URI from ID (see SPEC-001: Jerry URI Specification)
        object.__setattr__(self, 'uri', self._compute_uri())

    def _compute_version(self) -> str:
        """
        Compute composite version from timestamp and hash.
        Format: "{ISO8601}_{hash[:8]}"
        """
        timestamp = self.updated_on.strftime("%Y-%m-%dT%H:%M:%SZ")
        return f"{timestamp}_{self.content_hash[:8]}"

    def _compute_uri(self) -> "JerryUri":
        """
        Compute Jerry URI from entity ID.
        See SPEC-001: Jerry URI Specification.

        Format: jer:<partition>:<domain>:<entity_type>:<id>[+<version>]
        Example: jer:jer:work-tracker:task:task-042+a1b2c3d4
        """
        from src.domain.identity import JerryUri  # Deferred import
        return JerryUri.for_entity(
            domain=self.label.lower().replace(" ", "-"),  # e.g., "work-tracker"
            entity_type=self.id.prefix,                   # e.g., "task"
            entity_id=self.id.full_form,                  # e.g., "task-042"
            version=self.content_hash[:8] if self.content_hash else None
        )

    @classmethod
    def compute_content_hash(cls, content_fields: Dict[str, Any], algorithm: str = "sha256") -> str:
        """
        Compute content hash for change detection.

        Args:
            content_fields: Fields to include in hash
            algorithm: Hash algorithm ('sha256', 'sha1', 'md5')

        Returns:
            16-character hexadecimal hash
        """
        import hashlib
        import json

        serialized = json.dumps(content_fields, sort_keys=True, default=str)
        hasher = hashlib.new(algorithm)
        hasher.update(serialized.encode('utf-8'))
        return hasher.hexdigest()[:16]
```

### D. JerryId - Strongly Typed Identity Object

> **ADDRESSED (AN: feedback):** ID is an object in DDD aggregates

```python
@dataclass(frozen=True)
class JerryId:
    """
    Unified strongly-typed identity for all Jerry entities.

    Extends VertexId for graph compatibility while providing:
    - Type safety (TaskId, PhaseId, etc.)
    - Human-readable short form (c-001, task-042)
    - Globally unique full form (c-001-a1b2c3d4)

    DDD Prior Art:
    - Evans, E. (2003). Domain-Driven Design. Value Objects chapter.
    - Vernon, V. (2013). Implementing DDD. Identity chapter.
    """
    prefix: str       # Entity type prefix (task, phase, c, e, etc.)
    sequence: int     # Sequence number within prefix
    uuid: str = ""    # Optional UUID for global uniqueness

    def __post_init__(self):
        """Validate ID components."""
        if not self.prefix:
            raise ValueError("ID prefix is required")
        if self.sequence < 0:
            raise ValueError("ID sequence must be non-negative")

    @property
    def short_form(self) -> str:
        """Return prefix-sequence format (c-001, task-042)."""
        return f"{self.prefix}-{self.sequence:03d}"

    @property
    def full_form(self) -> str:
        """Return full unique identifier."""
        if self.uuid:
            return f"{self.prefix}-{self.sequence:03d}-{self.uuid[:8]}"
        return self.short_form

    @property
    def vertex_id(self) -> str:
        """Return ID suitable for graph vertex."""
        return self.full_form

    def __str__(self) -> str:
        return self.short_form

    def __eq__(self, other) -> bool:
        if isinstance(other, JerryId):
            return self.prefix == other.prefix and self.sequence == other.sequence
        return False

    def __hash__(self) -> int:
        return hash((self.prefix, self.sequence))


# Type-specific aliases for compile-time safety
class TaskId(JerryId):
    """Strongly typed Task identifier."""
    def __init__(self, sequence: int, uuid: str = ""):
        super().__init__(prefix="task", sequence=sequence, uuid=uuid)

class PhaseId(JerryId):
    """Strongly typed Phase identifier."""
    def __init__(self, sequence: int, uuid: str = ""):
        super().__init__(prefix="phase", sequence=sequence, uuid=uuid)

class PlanId(JerryId):
    """Strongly typed Plan identifier."""
    def __init__(self, sequence: int, uuid: str = ""):
        super().__init__(prefix="plan", sequence=sequence, uuid=uuid)

class ConstraintId(JerryId):
    """Strongly typed Constraint identifier."""
    def __init__(self, sequence: int, uuid: str = ""):
        super().__init__(prefix="c", sequence=sequence, uuid=uuid)
```

---

## III. Schema Alignment

### A. Unified YAML Frontmatter (REVISED)

```yaml
---
# Entity Identity (JerryId object, JerryUri - SPEC-001)
id: "{prefix}-{sequence}"      # Short form: "task-042", "c-001"
id_full: "{prefix}-{sequence}-{uuid[:8]}"  # Full form (optional)
uri: "jer:jer:{domain}:{type}:{id}+{version}"  # Jerry URI (SPEC-001)
slug: "{kebab-case-slug}"      # Max 75 chars
label: "{vertex-label}"        # e.g., "Task", "Constraint"

# Display
name: "{human-readable-name}"  # Max 80 chars
short_description: "{one-sentence}"  # Max 200 chars

# Status (State Machine)
status: "{DRAFT|ACTIVE|BLOCKED|COMPLETED|CLOSED}"

# Provenance (IAuditable)
created_on: "{ISO-8601}T{HH:MM:SS}Z"
updated_on: "{ISO-8601}T{HH:MM:SS}Z"
created_by: "{user:username|system:name}"
updated_by: "{user:username|system:name}"
session_id: "{session-identifier}"

# Change Detection (IVersioned)
content_hash: "{16-hex-chars}"
hash_algorithm: "sha256"
version: "{ISO-8601}_{hash[:8]}"

# Extensibility
metadata:
  key1: "value1"
  key2: "value2"
tags:
  - tag1
  - tag2

# Type-Specific Properties
# (varies by entity type)
---
```

### B. JSON/TOON Export Schema (REVISED)

```json
{
  "$schema": "https://jerry.dev/schemas/entity-base-v1.2.json",
  "$id": "jer:jer:jerry:schemas/EntityBase+1.2.0",
  "type": "object",
  "required": ["id", "uri", "slug", "label", "name", "status", "created_on", "created_by", "content_hash", "hash_algorithm", "version"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^[a-z]+-[0-9]{3,}(-[a-f0-9]{8})?$",
      "description": "JerryId in short or full form"
    },
    "uri": {
      "type": "string",
      "pattern": "^jer(\\+[0-9]+)?:[a-z]+:([a-z0-9-]+:)?[a-z0-9-]+:.+(\\+[a-z0-9.-]+)?$",
      "description": "Jerry URI per SPEC-001 (jer:<partition>:<domain>:<resource>[+version])"
    },
    "slug": {
      "type": "string",
      "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$",
      "maxLength": 75,
      "description": "URL-safe identifier (max 75 chars per SEO best practice)"
    },
    "label": {
      "type": "string",
      "enum": ["Task", "Phase", "Plan", "Constraint", "Question", "Exploration", "Experience", "Wisdom"]
    },
    "name": {
      "type": "string",
      "maxLength": 80
    },
    "short_description": {
      "type": "string",
      "maxLength": 200
    },
    "long_description": {
      "type": "string"
    },
    "status": {
      "type": "string"
    },
    "created_on": {
      "type": "string",
      "format": "date-time"
    },
    "updated_on": {
      "type": "string",
      "format": "date-time"
    },
    "created_by": {
      "type": "string",
      "pattern": "^(user|system):.+$",
      "description": "Format: 'user:username' or 'system:name'"
    },
    "updated_by": {
      "type": "string",
      "pattern": "^(user|system):.+$"
    },
    "session_id": {
      "type": "string"
    },
    "content_hash": {
      "type": "string",
      "pattern": "^[a-f0-9]{16}$"
    },
    "hash_algorithm": {
      "type": "string",
      "enum": ["sha256", "sha1", "md5"],
      "default": "sha256"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z_[a-f0-9]{8}$",
      "description": "Composite version: timestamp_hash[:8]"
    },
    "metadata": {
      "type": "object",
      "additionalProperties": { "type": "string" },
      "description": "Key-value pairs for extensibility"
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Tags for categorization and filtering"
    }
  }
}
```

---

## IV. Graph Model Alignment

### A. Vertex Mapping (Entities)

| Entity Type | Vertex Label | ID Pattern | Key Properties |
|-------------|--------------|------------|----------------|
| Task | `Task` | `task-NNN` | status, priority, metadata, tags |
| Phase | `Phase` | `phase-NNN` | status, progress, metadata, tags |
| Plan | `Plan` | `plan-NNN` | status, metadata, tags |
| Constraint | `Constraint` | `c-NNN` | status, priority, category, metadata, tags |
| Question | `Question` | `q-NNN` | status, answer, metadata, tags |
| Exploration | `Exploration` | `e-NNN` | entry_type, severity, metadata, tags |
| Experience | `Experience` | `exp-NNN` | applicability, metadata, tags |
| Wisdom | `Wisdom` | `wiz-NNN` | confidence, metadata, tags |

### B. Edge Types (Relationships)

> **ADDRESSED (AN: feedback):** Relationships are represented as **Edge entities** in the graph model, NOT as NodeProperty or EdgeProperty. This follows TinkerPop's property graph model where:
> - **Vertices** = Entities (Task, Phase, Constraint, etc.)
> - **Edges** = Relationships with their own properties
> - **VertexProperty** = Properties on vertices (with meta-properties for audit)
> - **EdgeProperty** = Simple key-value on edges (no meta-properties)

```python
@dataclass
class Edge:
    """
    Relationship between two vertices in the graph model.

    Edges are first-class entities with:
    - Unique ID
    - Label (relationship type)
    - Direction (from → to)
    - Properties (edge metadata)

    TinkerPop Prior Art: Edge is an Element with id, label, properties
    """
    id: str                       # Unique edge identifier
    label: str                    # Relationship type (e.g., "CONTAINS")
    from_vertex_id: str           # Source vertex ID
    to_vertex_id: str             # Target vertex ID
    properties: Dict[str, Any] = field(default_factory=dict)

    # Audit (optional for edges)
    created_on: Optional[datetime] = None
    created_by: Optional[str] = None
```

**Defined Edge Types:**

| Edge Label | From | To | Properties | Semantics |
|------------|------|----|-----------|-----------|
| `CONTAINS` | Phase | Task | position: int | Phase contains Task at position |
| `CONTAINS` | Plan | Phase | position: int | Plan contains Phase at position |
| `HAS_SUBTASK` | Task | Task | position: int | Parent → Child subtask |
| `REFERENCES` | Constraint | Knowledge | kb_type: str | Constraint references KB item |
| `VALIDATES` | Exploration | Constraint | evidence: str | Exploration validates Constraint |
| `SYNTHESIZES` | Wisdom | Experience | weight: float | Wisdom synthesized from Experience |
| `EMITS` | Entity | CloudEvent | timestamp: datetime | Entity emitted event |
| `BLOCKS` | Task | Task | reason: str | Task A blocks Task B |
| `DEPENDS_ON` | Task | Task | type: str | Task A depends on Task B |
| `TAGGED_WITH` | Entity | Tag | - | Entity has tag (optional pattern) |

**Relationship Query Examples (Gremlin):**
```groovy
// Find all tasks in a phase
g.V('phase-001').out('CONTAINS').hasLabel('Task')

// Find blocked tasks
g.V().hasLabel('Task').as('blocked').in('BLOCKS').as('blocker').select('blocked', 'blocker')

// Find wisdom synthesized from experiences
g.V('wiz-001').out('SYNTHESIZES').hasLabel('Experience')
```

---

## V. Implementation Plan (REVISED)

### A. Phase 1: Update PS-EXPORT-SPECIFICATION (v2.2)

1. Add IAuditable fields (`created_by`, `updated_by`)
2. Add IVersioned fields (`version`, `hash_algorithm`)
3. Add extensibility fields (`metadata`, `tags`)
4. Update slug constraint (max 75 chars)
5. Add graph-alignment section
6. Add relationship documentation (Edge types)

### B. Phase 2: Domain Model Base Class

1. Create `IAuditable` interface
2. Create `IVersioned` interface
3. Create `EntityBase` dataclass with all common properties
4. Create `JerryId` strongly-typed identity object
5. Create type-specific IDs (TaskId, PhaseId, etc.)
6. Create `Edge` dataclass for relationships
7. Task, Phase, Plan extend EntityBase
8. Implement `content_hash` computation with algorithm selector
9. Implement `version` computation
10. Add `slug` generation utility with length validation

### C. Phase 3: Serialization Adapters

1. JSON adapter produces unified schema v1.1
2. TOON adapter produces tabular format
3. Both handle EntityBase properties automatically
4. Both handle metadata and tags

### D. Phase 4: Migration

1. Update existing PS entities to unified format
2. Add IAuditable fields to historical data (default: "system:migration")
3. Add IVersioned fields to historical data
4. Generate `content_hash` for all entities
5. Add empty metadata and tags where missing

---

## VI. Benefits (UPDATED)

| Benefit | Description |
|---------|-------------|
| **Consistency** | Single property model for all entities |
| **Serialization** | One serializer handles PS and Domain entities |
| **Graph Ready** | All entities map to vertices; relationships to edges |
| **Audit Trail** | Full IAuditable interface (who created/modified, when) |
| **Change Detection** | Content hash + algorithm enables verification |
| **Optimistic Concurrency** | Composite version enables conflict detection |
| **URL Safety** | Slug enables clean API routes (max 75 chars for SEO) |
| **Extensibility** | Metadata dictionary for future needs |
| **Categorization** | Tags array for filtering and organization |
| **Type Safety** | JerryId as object prevents ID type mixing |

---

## VII. Risks & Mitigations (UPDATED)

| Risk | Mitigation |
|------|------------|
| Migration complexity | Phase incrementally; maintain backward compatibility |
| ID format changes | Support both short (c-001) and full (c-001-abc123) forms |
| Breaking existing PS exports | Version bumps (v2.2, v3.0) with migration guides |
| Hash algorithm changes | Store algorithm name; support multiple algorithms |
| Metadata abuse | Document intended use; consider size limits |
| Tag explosion | Consider tag registry; normalize case |

---

## VIII. Decision

**Recommendation:** APPROVE (v1.1)

This revised alignment provides:
- Unified data model for Jerry with full audit trail
- Clean serialization path (JSON + TOON)
- Graph database migration readiness with explicit Edge types
- Consistent audit/provenance tracking (IAuditable)
- Optimistic concurrency support (IVersioned)
- Extensibility for future needs (metadata, tags)
- Type-safe identity objects (JerryId)

**Next Steps:**
1. Review and approve proposal v1.1
2. Update PS-EXPORT-SPECIFICATION to v2.2
3. Implement IAuditable and IVersioned interfaces
4. Implement EntityBase and JerryId in Domain Layer
5. Implement Edge dataclass for relationships
6. Update serialization adapters

---

## IX. References

### Specification Documents
- PS-EXPORT-SPECIFICATION v2.1: `docs/knowledge/exemplars/templates/PS-EXPORT-SPECIFICATION.md`
- Domain Model Plan: `docs/PLAN.md`
- Graph Data Model: `docs/research/GRAPH_DATA_MODEL_ANALYSIS.md`
- TOON Format: `docs/research/TOON_FORMAT_ANALYSIS.md`

### Industry Sources
- [Clean DDD: Audit metadata for domain entities](https://medium.com/unil-ci-software-engineering/clean-ddd-lessons-audit-metadata-for-domain-entities-5935a5c6db5b) - IAuditable pattern
- [EF Core Auditing](https://dev.to/rickystam/ef-core-how-to-implement-basic-auditing-on-your-entities-1mbm) - Automatic audit field population
- [DDD Aggregate Root](https://dev.to/leelanagaramya/updating-audit-columns-in-aggregate-roots-and-child-entities-with-ef-core-and-ddd-481b) - Audit in base class
- [Backlinko SEO URL Best Practices](https://backlinko.com/hub/seo/url-slug) - Slug length recommendation (≤75 chars)
- [Evans, E. (2003). Domain-Driven Design](https://www.oreilly.com/library/view/domain-driven-design/9780321125217/) - Value Objects, Identity
- [Vernon, V. (2013). Implementing DDD](https://www.oreilly.com/library/view/implementing-domain-driven-design/9780133039900/) - Aggregate Root, Identity

---

## X. Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-08 | Initial proposal |
| 1.1 | 2026-01-08 | Addressed user feedback (AN:): IAuditable, hash_algorithm, version, slug limits, metadata, tags, Edge relationships |
| 1.2 | 2026-01-08 | Integrated Jerry URI scheme (SPEC-001): Added `uri` property to EntityBase, updated JSON schema to v1.2 with `$id` using Jerry URI |
