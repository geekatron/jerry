# Phase DISCOVERY: Technical Discoveries

> **Status**: 🔄 ONGOING
> **Purpose**: Track technical discoveries, insights, and findings during implementation work.

---

## Navigation

| Link | Description |
|------|-------------|
| [← WORKTRACKER](../WORKTRACKER.md) | Back to index |
| [BUGS](PHASE-BUGS.md) | Bug tracking |
| [TECHDEBT](PHASE-TECHDEBT.md) | Technical debt |

---

## Discovery Log

### Format

Each discovery follows this format:

```
### DISC-{nnn}: {Title}

**Date**: YYYY-MM-DD
**Context**: {Where/how this was discovered}
**Finding**: {What was discovered}
**Impact**: {How this affects the project}
**Action**: {What should be done, if anything}
**Status**: LOGGED | INVESTIGATED | ACTIONED | ARCHIVED
```

---

## Active Discoveries

### DISC-001: ProjectId Already Extends VertexId

**Date**: 2026-01-10
**Context**: Starting 008d.1.1 (ProjectId VertexId compliance), reviewed current implementation
**Finding**: `src/session_management/domain/value_objects/project_id.py` already extends `VertexId`:
- Line 23: `from src.shared_kernel.vertex_id import VertexId`
- Line 36: `class ProjectId(VertexId):`
- Implements `_is_valid_format()`, `from_string()`, `generate()` (raises NotImplementedError)
- Has `number` and `slug` convenience properties (lines 204-228)

**Impact**: 008d.1 (Value Object Refactoring) is FULLY COMPLETE:
- 008d.1.1: VertexId compliance (10 tests) ✅
- 008d.1.2: number/slug properties (5 tests) ✅
- 008d.1.3: Format + Edge case tests (21 tests) ✅
- Total: 36 tests all passing

**Action**: Mark 008d.1 as complete, proceed to 008d.2 (Entity Refactoring)
**Status**: ACTIONED

### DISC-002: ProjectInfo EntityBase Design Tension

**Date**: 2026-01-10
**Context**: Starting 008d.2 (ProjectInfo extends EntityBase), reviewed both implementations
**Finding**: Design tension between R-008d and current implementation:
- R-008d specifies: "ProjectInfo extends EntityBase"
- Current ProjectInfo: `@dataclass(frozen=True, slots=True)` - immutable snapshot
- EntityBase: Mutable, has `_touch()` and `_increment_version()` methods
- These are incompatible: frozen dataclass cannot have mutation methods

**Options**:
1. Make ProjectInfo mutable (extend EntityBase, lose immutability)
2. Keep ProjectInfo frozen (add audit fields directly, don't extend EntityBase)
3. Create ImmutableEntityBase variant (new base class)

**Analysis (Distinguished Engineer)**:
- ProjectInfo is described as "immutable snapshot" - this is VALUE OBJECT pattern
- Entities typically have identity AND mutable state
- ProjectInfo acts more like a read-only projection than a mutable entity
- Changing to mutable would break existing code expecting frozen behavior

**Decision**: Option 2 - Add audit metadata directly to ProjectInfo without extending EntityBase.
This preserves immutability guarantees and backward compatibility.

**Impact**: R-008d revision applied - ProjectInfo does NOT extend EntityBase
**Action**: Implemented audit fields on frozen ProjectInfo, updated tests (35 pass)
**Status**: ACTIONED

### DISC-003: link-artifact CLI Command Does Not Exist

**Date**: 2026-01-11
**Context**: Preparing to execute INIT-WT-SKILLS orchestration with ps-* agents
**Finding**: All 8 ps-* agents reference `python3 scripts/cli.py link-artifact` in their MANDATORY PERSISTENCE protocol, but this command does not exist:
- `scripts/cli.py` does not exist (only `scripts/session_start.py` found)
- `src/**/cli*.py` pattern returns no matches
- `link-artifact` is referenced in 25 files:
  - 8 ps-* agent definitions
  - 1 PS_AGENT_TEMPLATE.md
  - 6 template files in `docs/knowledge/exemplars/templates/`
  - 1 orchestration doc
  - 9 aspiration/archive files

**Scope of References**:
```
skills/problem-solving/agents/*.md (9 files)
docs/knowledge/exemplars/templates/*.md (6 files)
skills/problem-solving/docs/ORCHESTRATION.md
docs/knowledge/DISCOVERIES_EXPANDED.md
projects/archive/**/*.md (2 files)
docs/knowledge/dragonsbelurkin/**/*.md (5 files)
```

**Impact**:
- ps-* agents cannot complete their mandatory persistence protocol as designed
- Artifact linking is aspirational, not functional
- Orchestration dependent on non-existent infrastructure

**Action**: Created TD-010 to implement `scripts/cli.py link-artifact` command
**Status**: LOGGED → Elevated to TECHDEBT (TD-010)

---

## Archived Discoveries

*None yet*

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-10 | Claude | Initial creation |
