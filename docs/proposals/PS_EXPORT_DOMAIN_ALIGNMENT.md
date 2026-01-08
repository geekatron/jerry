# Proposal: PS-EXPORT-SPECIFICATION and Domain Model Alignment

> **Proposal ID:** PROP-001
> **Status:** DRAFT
> **Created:** 2026-01-08
> **Author:** Claude (Session claude/create-code-plugin-skill-MG1nh)

---

## Executive Summary

This proposal recommends enhancing PS-EXPORT-SPECIFICATION v2.1 to align with Jerry's planned Domain Model properties. The alignment ensures:

1. **Consistency** - Same property patterns across PS entities and Domain entities
2. **Serialization** - Unified JSON + TOON export for all entities
3. **Graph Readiness** - Both PS and Domain entities map to Vertex/Edge model
4. **Provenance** - Common audit trail patterns (created_on, updated_on, session_id)

**Recommendation:** Adopt a unified **Entity Base Specification** that both PS-EXPORT and Domain Model inherit from.

---

## I. Current State Analysis

### A. PS-EXPORT-SPECIFICATION v2.1 Common Properties
> AN: created_on. updated_on, created_by, updated_by are required IAuditable fields
> AN: we need a property to indicate the hash algorithm
> AN: we need a version property to indicate the version of the object (Date+Hash)
> AN: id needs to be an object in the DDD aggregates and models - can we leverage that here? 
> AN: What's the upper limit of slug?

| Property | Format | Description |
|----------|--------|-------------|
| `id` | `{prefix}-NNN` | Unique identifier (c-001, e-012) |
| `slug` | `kebab-case` | URL-safe identifier |
| `name` | Free text (≤80 chars) | Human-readable display name |
| `short_description` | Free text (≤200 chars) | Brief summary |
| `long_description` | Markdown | Detailed content |
| `created_on` | ISO 8601 + Session | Creation timestamp |
| `updated_on` | ISO 8601 + Session | Last modification |
| `session_id` | String | Session provenance |
| `hash` | Hex (16 chars) | Content hash for change detection |

### B. Planned Domain Model Properties (from PLAN.md)

**Task Entity:**

>AN: You need a space, otherwise the table will not render

| Property | Type | Description |
|----------|------|-------------|
| `id` | `TaskId` (VertexId) | Strongly typed identifier |
| `title` | `str` | Task name |
| `description` | `str` | Task details |
| `status` | `TaskStatus` | State machine |
| `created_at` | `datetime` | Creation timestamp |
| `updated_at` | `datetime` | Last update |
| `subtask_ids` | `List[SubtaskId]` | Child references |

**Phase Entity:**

>AN: You need a space, otherwise the table will not render

| Property | Type | Description |
|----------|------|-------------|
| `id` | `PhaseId` (VertexId) | Strongly typed identifier |
| `name` | `str` | Phase name |
| `status` | `PhaseStatus` | State machine |
| `task_ids` | `List[TaskId]` | Child references |

### C. Identified Gaps

> AN: We should add additional Jerry data that is common to all objects:
>  - Metadata : Dictionary <string, string> - for extensibility
>  - Tags : string[] - For categorization and filtering
>  - Where are we representing relationships? Edges in graph model? EdgePropery? NodeProperty?

| Gap | PS-EXPORT | Domain Model | Resolution |
|-----|-----------|--------------|------------|
| ID Format | Prefix-based (c-001) | Strongly typed (TaskId) | Unify to strongly typed + prefix | 
| Session Tracking | `session_id` | Not planned | Add to Domain |
| Hash | Content hash | Not planned | Add to Domain |
| Slug | URL-safe | Not planned | Add to Domain |
| Status | Entity-specific | State machine | PS adopts state machine |
| References | KB refs (kb:type:id) | ID references | Unify reference format |

---

## II. Proposed Unified Entity Base

### A. Entity Base Specification

All entities (PS and Domain) should inherit these common properties:

```python
@dataclass
class EntityBase:
    """
    Common base for all Jerry entities.
    Aligns PS-EXPORT-SPECIFICATION with Domain Model.
    """
    # Identity (Graph-Ready)
    id: VertexId              # Strongly typed, extends graph primitive
    slug: str                 # URL-safe identifier (kebab-case)

    # Display
    name: str                 # Human-readable (≤80 chars)
    short_description: str    # Brief summary (≤200 chars, 1 sentence)
    long_description: str     # Detailed content (Markdown)

    # Provenance
    created_on: datetime      # Creation timestamp (ISO 8601)
    updated_on: datetime      # Last modification (ISO 8601)
    created_by: str           # User that created the entity
    updated_by: str           # User that last modified the entity
    session_id: str           # Session that created/modified

    # Change Detection
    content_hash: str         # SHA-256 of content fields (16 hex chars)

    # Graph Properties
    label: str                # Vertex label for graph storage
    properties: Dict[str, Any]  # Additional key-value properties
```

### B. ID Unification Strategy

**Current PS IDs:**
```
c-001, q-005, e-012, exp-003, wiz-001, ADR-001, LES-030
```

**Current Domain IDs:**
```
TaskId(value="uuid"), PhaseId(value="uuid"), PlanId(value="uuid")
```

**Proposed Unified Format:**
```python
@dataclass
class JerryId(VertexId):
    """Unified identity for all Jerry entities."""
    prefix: str       # Entity type prefix (task, phase, c, e, etc.)
    sequence: int     # Sequence number within prefix
    uuid: str         # Optional UUID for global uniqueness

    @property
    def short_form(self) -> str:
        """Return prefix-sequence format (c-001, task-042)."""
        return f"{self.prefix}-{self.sequence:03d}"

    @property
    def full_form(self) -> str:
        """Return full unique identifier."""
        return f"{self.prefix}-{self.sequence:03d}-{self.uuid[:8]}"
```

**Migration Path:**
| Current | Unified |
|---------|---------|
| `c-001` | `JerryId(prefix="c", sequence=1)` |
| `TaskId(uuid)` | `JerryId(prefix="task", sequence=42, uuid=...)` |

### C. Common Property Additions

**Add to Domain Model (from PS-EXPORT):**
| Property | Rationale |
|----------|-----------|
| `slug` | Enables URL-safe references, file naming |
| `short_description` | Supports L0/L1/L2 output generation |
| `long_description` | Full entity documentation |
| `session_id` | Provenance tracking for audit |
| `content_hash` | Change detection for sync/export |

**Add to PS-EXPORT (from Domain):**
| Property | Rationale |
|----------|-----------|
| `label` | Graph vertex label for future migration |
| `status` | State machine pattern (DRAFT → ACTIVE → CLOSED) |

---

## III. Schema Alignment

### A. Unified YAML Frontmatter

```yaml
---
# Entity Identity
id: "{prefix}-{sequence}"      # e.g., "task-042", "c-001"
slug: "{kebab-case-slug}"
label: "{vertex-label}"         # e.g., "Task", "Constraint"

# Display
name: "{human-readable-name}"
short_description: "{one-sentence}"

# Status (State Machine)
status: "{DRAFT|ACTIVE|BLOCKED|COMPLETED|CLOSED}"

# Provenance
created_on: "{ISO-8601}T{HH:MM:SS}Z"
updated_on: "{ISO-8601}T{HH:MM:SS}Z"
session_id: "{session-identifier}"

# Change Detection
content_hash: "{16-hex-chars}"

# Type-Specific Properties
# (varies by entity type)
---
```

### B. JSON/TOON Export Schema

```json
{
  "$schema": "https://jerry.dev/schemas/entity-base.json",
  "type": "object",
  "required": ["id", "slug", "label", "name", "status", "created_on"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^[a-z]+-[0-9]{3,}(-[a-f0-9]{8})?$"
    },
    "slug": {
      "type": "string",
      "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$"
    },
    "label": {
      "type": "string",
      "enum": ["Task", "Phase", "Plan", "Constraint", "Question", "Exploration"]
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
    "session_id": {
      "type": "string"
    },
    "content_hash": {
      "type": "string",
      "pattern": "^[a-f0-9]{16}$"
    }
  }
}
```

### C. TOON Representation

```toon
entities[3]{id,slug,label,name,status,created_on}:
  task-042,implement-auth,Task,Implement Authentication,ACTIVE,2026-01-08T10:30:00Z
  c-001,cloudevents-required,Constraint,CloudEvents 1.0 Required,VALIDATED,2026-01-07T14:00:00Z
  phase-001,core-impl,Phase,Core Implementation,IN_PROGRESS,2026-01-06T09:00:00Z
```

---

## IV. Graph Model Alignment

### A. Vertex Mapping

| Entity Type | Vertex Label | ID Pattern | Key Properties |
|-------------|--------------|------------|----------------|
| Task | `Task` | `task-NNN` | status, priority |
| Phase | `Phase` | `phase-NNN` | status, progress |
| Plan | `Plan` | `plan-NNN` | status |
| Constraint | `Constraint` | `c-NNN` | status, priority, category |
| Question | `Question` | `q-NNN` | status, answer |
| Exploration | `Exploration` | `e-NNN` | entry_type, severity |
| Experience | `Experience` | `exp-NNN` | applicability |
| Wisdom | `Wisdom` | `wiz-NNN` | confidence |

### B. Edge Types

| Edge Label | From | To | Properties |
|------------|------|----|-----------|
| `CONTAINS` | Phase | Task | position |
| `REFERENCES` | Constraint | Knowledge | kb_type |
| `VALIDATES` | Exploration | Constraint | evidence |
| `SYNTHESIZES` | Wisdom | Experience | weight |
| `EMITS` | Task | CloudEvent | timestamp |

---

## V. Implementation Plan

### A. Phase 1: Update PS-EXPORT-SPECIFICATION

1. Add `label` property to Common Properties (v2.2)
2. Add `status` with state machine values
3. Update ID format documentation to support unified IDs
4. Add graph-alignment section

### B. Phase 2: Domain Model Base Class

1. Create `EntityBase` dataclass with all common properties
2. Task, Phase, Plan extend EntityBase
3. Implement `content_hash` computation
4. Add `slug` generation utility

### C. Phase 3: Serialization Adapters

1. JSON adapter produces unified schema
2. TOON adapter produces tabular format
3. Both handle EntityBase properties automatically

### D. Phase 4: Migration

1. Update existing PS entities to unified format
2. Add `label` and `status` to historical data
3. Generate `content_hash` for all entities

---

## VI. Benefits

| Benefit | Description |
|---------|-------------|
| **Consistency** | Single property model for all entities |
| **Serialization** | One serializer handles PS and Domain entities |
| **Graph Ready** | All entities map to vertices with unified labeling |
| **Audit Trail** | Common provenance properties everywhere |
| **Change Detection** | Content hash enables efficient sync |
| **URL Safety** | Slug enables clean API routes and file naming |

---

## VII. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Migration complexity | Phase incrementally; maintain backward compatibility |
| ID format changes | Support both short (c-001) and full (c-001-abc123) forms |
| Breaking existing PS exports | Version bumps (v2.2, v3.0) with migration guides |

---

## VIII. Decision

**Recommendation:** APPROVE

This alignment provides:
- Unified data model for Jerry
- Clean serialization path (JSON + TOON)
- Graph database migration readiness
- Consistent audit/provenance tracking

**Next Steps:**
1. Review and approve proposal
2. Update PS-EXPORT-SPECIFICATION to v2.2
3. Implement EntityBase in Domain Layer
4. Update serialization adapters

---

## IX. References

- PS-EXPORT-SPECIFICATION v2.1: `docs/knowledge/exemplars/templates/PS-EXPORT-SPECIFICATION.md`
- Domain Model Plan: `docs/PLAN.md`
- Graph Data Model: `docs/research/GRAPH_DATA_MODEL_ANALYSIS.md`
- TOON Format: `docs/research/TOON_FORMAT_ANALYSIS.md`
