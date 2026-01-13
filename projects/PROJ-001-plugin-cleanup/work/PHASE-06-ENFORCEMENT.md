# Phase 6: Project Enforcement

> **Status**: 🔄 IN PROGRESS (60%)
> **Goal**: Implement hard enforcement that validates JERRY_PROJECT at session start.

---

## Navigation

| Link | Description |
|------|-------------|
| [← WORKTRACKER](../WORKTRACKER.md) | Back to index |
| [← Phase 5](PHASE-05-VALIDATION.md) | Previous phase |
| [Phase 7 →](PHASE-07-DESIGN-SYNTHESIS.md) | Next phase (completed) |
| [BUGS](PHASE-BUGS.md) | Bug tracking |
| [TECHDEBT](PHASE-TECHDEBT.md) | Technical debt |

---

## Phase Overview

### Dependencies

```
Phase 5 (Validation) ──┐
                       ├──► Phase 6 (Enforcement)
Phase 7 (Design Synthesis) ─┘
```

### Task Graph

```
ENFORCE-001 ──► ENFORCE-002 ──► ENFORCE-003 ──► ENFORCE-004 ──► ENFORCE-005
     │              │              │              │              │
     ▼              ▼              ▼              ▼              ▼
  Research       ADR-002        Hooks         Domain        Application
  (5W1H)        Created        Created        Layer          Layer
     │                                           │              │
     └───────────────────────────────────────────┴──────────────┘
                                │
                                ▼
                         ENFORCE-006 ──► ENFORCE-007 ──► ENFORCE-008
                              │              │              │
                              ▼              ▼              ▼
                          Infra           CLI           Domain
                          Layer          Entry          Tests
                                                          │
                    ┌─────────────────────────────────────┘
                    ▼
              ENFORCE-008d (CURRENT)
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
 008d.0          008d.1-3        008d.4
Research      Implementation   Infrastructure
 (5W1H)         (Domain)        Updates
                    │
                    ▼
    ┌───────────────┼───────────────────────┐
    ▼               ▼               ▼       ▼
ENFORCE-009   ENFORCE-010   ENFORCE-011  ENFORCE-012-016
 App Tests    Infra Tests    E2E Tests    Final Tasks
```

---

## Task Status Summary

| Task ID | Title | Status | Subtasks | Dependencies |
|---------|-------|--------|----------|--------------|
| ENFORCE-001 | Research & Design | ✅ DONE | 4/4 | None |
| ENFORCE-002 | Persist Design Decision (ADR-002) | ✅ DONE | 4/4 | 001 |
| ENFORCE-003 | Create Plugin Hook Structure | ✅ DONE | 4/4 | 002 |
| ENFORCE-004 | Implement Domain Layer | ✅ DONE | 5/5 | 003 |
| ENFORCE-005 | Implement Application Layer | ✅ DONE | 5/5 | 004 |
| ENFORCE-006 | Implement Infrastructure Layer | ✅ DONE | 2/2 | 005 |
| ENFORCE-007 | Implement Interface Layer (CLI) | ✅ DONE | 3/3 | 006 |
| ENFORCE-008 | Domain Unit Tests | ✅ DONE | 57/57 | 004 |
| ENFORCE-008b | Code Restructuring | ✅ DONE | - | 008 |
| ENFORCE-008c | Unified Design Analysis | ✅ DONE | - | 008b |
| **ENFORCE-008d** | **Refactor to Unified Design** | **🔄 IN PROGRESS** | **1/20** | **008c, Phase 7** |
| ENFORCE-009 | Application Layer Tests | ⏳ PENDING | 0/23 | 008d |
| ENFORCE-010 | Infrastructure Tests | ⏳ PENDING | 0/19 | 008d |
| ENFORCE-011 | E2E Tests | ⏳ PENDING | 0/18 | 009, 010 |
| ENFORCE-012 | Contract Tests | ⏳ PENDING | 0/5 | 011 |
| ENFORCE-013 | Architecture Tests | ⏳ PENDING | 0/5 | 008d |
| ENFORCE-014 | Update CLAUDE.md | ⏳ PENDING | 0/5 | 011 |
| ENFORCE-015 | Update Manifest | ⏳ PENDING | 0/3 | 014 |
| ENFORCE-016 | Final Validation | ⏳ PENDING | 0/10 | ALL |

---

## Completed Tasks (001-008c)

<details>
<summary>Click to expand completed tasks</summary>

### ENFORCE-001: Research and Design ✅

- **Status**: COMPLETED
- **Output**: 5W1H analysis, Context7 research
- **Sources**: Claude Code Hooks Reference, Plugin Structure docs

### ENFORCE-002: Persist Design Decision ✅

- **Status**: COMPLETED
- **Output**: `design/ADR-002-project-enforcement.md`

### ENFORCE-003: Create Plugin Hook Structure ✅

- **Status**: COMPLETED
- **Output**: `hooks/hooks.json`, `scripts/session_start.py`

### ENFORCE-004: Implement Domain Layer ✅

- **Status**: COMPLETED
- **Output**: `scripts/domain/` (ProjectId, ProjectInfo, etc.)

### ENFORCE-005: Implement Application Layer ✅

- **Status**: COMPLETED
- **Output**: `scripts/application/` (Ports, Queries)

### ENFORCE-006: Implement Infrastructure Layer ✅

- **Status**: COMPLETED
- **Output**: `scripts/infrastructure/` (Adapters)

### ENFORCE-007: Implement Interface Layer ✅

- **Status**: COMPLETED
- **Output**: `scripts/session_start.py` (CLI entry point)

### ENFORCE-008: Domain Unit Tests ✅

- **Status**: COMPLETED
- **Result**: 57 tests pass (100%)
- **Output**: `scripts/tests/unit/test_domain.py`

### ENFORCE-008b: Code Restructuring ✅

- **Status**: COMPLETED
- **Commit**: `d6bf24f`
- **Output**: `src/session_management/` (bounded context structure)

### ENFORCE-008c: Unified Design Analysis ✅

- **Status**: COMPLETED
- **Outputs**:
  - `design/ADR-004-session-management-alignment.md`
  - `design/EXPLORATION-001-unified-design-alignment.md`

</details>

---

## ENFORCE-008d: Refactor to Unified Design 🔄

> **Status**: IN PROGRESS
> **Prerequisites**: Shared Kernel ✅, Phase 7 Design Canon ✅
> **Goal**: Refactor `src/session_management/` to use Shared Kernel patterns

### Phase Structure (per Work Item Schema)

| Phase | ID | Description | Status |
|-------|-----|-------------|--------|
| **Research** | R-008d | 5W1H + Context7 + Industry Research | 🔄 |
| **Implementation** | I-008d | BDD Red/Green/Refactor Cycles | ⏳ |
| **Test** | T-008d | Full Test Pyramid | ⏳ |
| **Evidence** | E-008d | Verification + Commit | ⏳ |

### Aggregated Test Matrix

| Category | Subcategory | Count | Location | Status |
|----------|-------------|-------|----------|--------|
| Unit | Happy Path | 35 | `tests/session_management/unit/test_*.py` | ⏳ |
| Unit | Edge Cases | 20 | `tests/session_management/unit/test_*.py` | ⏳ |
| Unit | Negative | 15 | `tests/session_management/unit/test_*.py` | ⏳ |
| Unit | Boundary | 10 | `tests/session_management/unit/test_*.py` | ⏳ |
| Integration | Adapters | 12 | `tests/session_management/integration/test_*.py` | ⏳ |
| Contract | Interfaces | 5 | `tests/session_management/contract/test_*.py` | ⏳ |
| Architecture | Boundaries | 5 | `tests/session_management/architecture/test_*.py` | ⏳ |
| **Total** | | **102** | | |

### Verification Checklist (E-008d)

Before marking ENFORCE-008d complete:

- [ ] 5W1H research documented in `research/PROJ-001-R-008d-domain-refactoring.md`
- [ ] Context7 research with 3+ citations persisted
- [ ] All 102 tests implemented (no placeholders)
- [ ] BDD cycles completed (RED → GREEN → REFACTOR) for each subtask
- [ ] Happy path, edge, negative, boundary scenarios covered
- [ ] Coverage ≥ 90%
- [ ] Zero regressions (full test suite passes)
- [ ] Architecture tests validate layer boundaries
- [ ] Commit created with evidence hash
- [ ] WORKTRACKER updated

### Subtask Dependency Graph

```
R-008d.0 (Research Phase)
    │
    ├─────────────────────────────────────────┐
    ▼                                         ▼
I-008d.1 (Value Objects) ──────────┐    I-008d.3 (New Objects)
    │                              │          │
    ├──► I-008d.1.1 (VertexId)     │          ├──► I-008d.3.1 (SessionId)
    ├──► I-008d.1.2 (slug)         │ SEQ      ├──► I-008d.3.2 (Session)    PARALLEL
    └──► T-008d.1.3 (VO tests)     │          └──► I-008d.3.3 (session_id)
                                   │                      │
I-008d.2 (Entities) ◄──────────────┘                      │
    │                                                     │
    ├──► I-008d.2.1 (EntityBase)   │                      │
    ├──► I-008d.2.2 (JerryUri)     │ SEQ                  │
    └──► I-008d.2.3 (metadata)     │                      │
                                   │                      │
                                   └──────────┬───────────┘
                                              │
I-008d.4 (Infrastructure) ◄───────────────────┘
    │
    ├──► I-008d.4.1 (adapters)
    ├──► I-008d.4.2 (migration)
    └──► T-008d.4.3 (infra tests)
                │
                ▼
         E-008d (Evidence)
```

---

### R-008d.0: Research & Analysis Phase 🔄

> **Phase ID**: R-008d
> **Status**: IN PROGRESS
> **Output Artifact**: `research/PROJ-001-R-008d-domain-refactoring.md`

#### 5W1H Framework

| Question | Analysis | Evidence Required |
|----------|----------|-------------------|
| **What** | Refactor ProjectId/ProjectInfo to use Shared Kernel patterns | Current vs target state comparison |
| **Why** | Unify identity model across bounded contexts per ADR-013 | Business justification, technical debt cost |
| **Who** | Impacts: session_management domain, all tests, CLI | Component dependency map |
| **Where** | `src/session_management/`, `src/shared_kernel/` | File inventory with change types |
| **When** | After Shared Kernel complete (✅), before Application tests | Dependency graph validation |
| **How** | BDD Red/Green/Refactor with full test pyramid | Pattern citations from Context7 |

#### Research Tasks

| ID | Task | Status | Output Location |
|----|------|--------|-----------------|
| R-008d.0.1 | Review ADR-013 Shared Kernel spec | ⏳ | `research/PROJ-001-R-008d-domain-refactoring.md#adr-review` |
| R-008d.0.2 | Review existing session_management domain | ⏳ | `research/PROJ-001-R-008d-domain-refactoring.md#current-state` |
| R-008d.0.3 | Context7: DDD Value Object migration patterns | ⏳ | `research/PROJ-001-R-008d-domain-refactoring.md#context7-vo` |
| R-008d.0.4 | Context7: Entity refactoring best practices | ⏳ | `research/PROJ-001-R-008d-domain-refactoring.md#context7-entity` |
| R-008d.0.5 | Industry: Breaking changes migration strategies | ⏳ | `research/PROJ-001-R-008d-domain-refactoring.md#migration` |
| R-008d.0.6 | Compile findings with full citations | ⏳ | `research/PROJ-001-R-008d-domain-refactoring.md` |

#### Context7 Research Requirements

| Topic | Library/Source | Required Citations |
|-------|----------------|-------------------|
| Value Object patterns | pyeventsourcing, domain-driven-hexagon | 2+ |
| Entity refactoring | Martin Fowler, Vaughn Vernon | 2+ |
| Migration strategies | Feature toggles, strangler fig | 1+ |

#### Acceptance Criteria (R-008d)

- [ ] 5W1H analysis documented with evidence
- [ ] Context7 research with 5+ authoritative citations
- [ ] Gap analysis: current state vs target state matrix
- [ ] File change inventory (MODIFY/CREATE/DELETE)
- [ ] Breaking change assessment with mitigation
- [ ] Migration plan for existing PROJ-001 directory
- [ ] Research artifact persisted: `research/PROJ-001-R-008d-domain-refactoring.md`

---

### I-008d.1: Value Object Refactoring (Implementation Phase)

> **Phase ID**: I-008d.1
> **Status**: PENDING
> **Depends On**: R-008d.0
> **Approach**: BDD Red/Green/Refactor
> **Test Phase**: T-008d.1

#### I-008d.1.1: Refactor ProjectId to Extend VertexId

| Phase | Description | Files | Tests |
|-------|-------------|-------|-------|
| **RED** | Write failing tests for new ProjectId format | `test_domain.py` | 10+ |
| **GREEN** | Implement ProjectId extending VertexId | `project_id.py` | - |
| **REFACTOR** | Clean up, ensure no regressions | All domain | - |

**File Changes:**

| File | Change Type | Description |
|------|-------------|-------------|
| `src/session_management/domain/value_objects/project_id.py` | MODIFY | Extend VertexId, change format to `PROJ-{uuid8}` |
| `src/shared_kernel/vertex_id.py` | MODIFY | Add ProjectId to exports if needed |
| `tests/session_management/unit/test_project_id.py` | CREATE | New focused test file |

**Test Cases (BDD):**

| Category | Test | Status |
|----------|------|--------|
| **Unit - Happy** | `test_project_id_extends_vertex_id` | ⏳ |
| **Unit - Happy** | `test_project_id_generate_creates_valid_format` | ⏳ |
| **Unit - Happy** | `test_project_id_from_string_parses_valid` | ⏳ |
| **Unit - Edge** | `test_project_id_with_uuid_boundary_values` | ⏳ |
| **Unit - Negative** | `test_project_id_rejects_old_format_with_slug` | ⏳ |
| **Unit - Negative** | `test_project_id_rejects_invalid_hex` | ⏳ |
| **Architecture** | `test_project_id_in_domain_has_no_infra_imports` | ⏳ |

**Acceptance Criteria:**

- [ ] ProjectId extends VertexId base class
- [ ] Format changed to `PROJ-{uuid8}` (8 hex chars)
- [ ] `generate()` method works correctly
- [ ] `from_string()` validates new format
- [ ] Old format rejected with clear error
- [ ] All existing tests updated or replaced
- [ ] 0 regressions

---

#### I-008d.1.2: Extract Slug as Separate Property

| Phase | Description | Files | Tests |
|-------|-------------|-------|-------|
| **RED** | Write failing tests for slug on ProjectInfo | `test_project_info.py` | 5+ |
| **GREEN** | Add slug property to ProjectInfo | `project_info.py` | - |
| **REFACTOR** | Ensure slug populated from filesystem | Adapter | - |

**File Changes:**

| File | Change Type | Description |
|------|-------------|-------------|
| `src/session_management/domain/entities/project_info.py` | MODIFY | Add `slug: str` property |
| `src/session_management/infrastructure/adapters/filesystem_adapter.py` | MODIFY | Populate slug from directory name |

**Test Cases (BDD):**

| Category | Test | Status |
|----------|------|--------|
| **Unit - Happy** | `test_project_info_has_slug_property` | ⏳ |
| **Unit - Happy** | `test_project_info_slug_can_be_empty` | ⏳ |
| **Unit - Edge** | `test_project_info_slug_with_special_chars` | ⏳ |
| **Integration** | `test_adapter_populates_slug_from_directory` | ⏳ |

**Acceptance Criteria:**

- [ ] ProjectInfo has `slug: str` property
- [ ] Slug is NOT part of ProjectId (separation of concerns)
- [ ] Slug populated from directory name by adapter
- [ ] All tests pass

---

#### T-008d.1.3: Update Domain Value Object Tests

| Phase | Description | Files | Tests |
|-------|-------------|-------|-------|
| **RED** | Identify failing tests from format change | All test files | - |
| **GREEN** | Update tests to use new format | Test files | - |
| **REFACTOR** | Consolidate duplicate tests | Test files | - |

**Test Categories:**

| Category | Count | Status |
|----------|-------|--------|
| Unit - Happy Path | 15 | ⏳ |
| Unit - Edge Cases | 10 | ⏳ |
| Unit - Negative | 10 | ⏳ |
| Unit - Boundary | 5 | ⏳ |

**Acceptance Criteria:**

- [ ] All 57 existing domain tests updated
- [ ] New tests for VertexId integration added
- [ ] Test coverage >= 90%
- [ ] 0 regressions

---

### I-008d.2: Entity Refactoring (Implementation Phase)

> **Phase ID**: I-008d.2
> **Status**: PENDING
> **Depends On**: I-008d.1
> **Approach**: BDD Red/Green/Refactor
> **Test Phase**: T-008d.2

#### I-008d.2.1: Refactor ProjectInfo to Extend EntityBase

| Phase | Description | Files | Tests |
|-------|-------------|-------|-------|
| **RED** | Write tests for IAuditable/IVersioned on ProjectInfo | Test files | 15+ |
| **GREEN** | Refactor ProjectInfo to extend EntityBase | `project_info.py` | - |
| **REFACTOR** | Ensure clean inheritance, no duplication | Domain | - |

**File Changes:**

| File | Change Type | Description |
|------|-------------|-------------|
| `src/session_management/domain/entities/project_info.py` | MODIFY | Extend EntityBase |
| `tests/session_management/unit/test_project_info.py` | CREATE | Focused entity tests |

**Test Cases (BDD):**

| Category | Test | Status |
|----------|------|--------|
| **Unit - Happy** | `test_project_info_extends_entity_base` | ⏳ |
| **Unit - Happy** | `test_project_info_implements_iauditable` | ⏳ |
| **Unit - Happy** | `test_project_info_implements_iversioned` | ⏳ |
| **Unit - Happy** | `test_project_info_has_created_by_property` | ⏳ |
| **Unit - Happy** | `test_project_info_has_created_at_property` | ⏳ |
| **Unit - Happy** | `test_project_info_has_updated_by_property` | ⏳ |
| **Unit - Happy** | `test_project_info_has_updated_at_property` | ⏳ |
| **Unit - Happy** | `test_project_info_has_version_property` | ⏳ |
| **Unit - Edge** | `test_project_info_touch_updates_metadata` | ⏳ |
| **Unit - Edge** | `test_project_info_increment_version` | ⏳ |
| **Architecture** | `test_project_info_satisfies_iauditable_protocol` | ⏳ |
| **Architecture** | `test_project_info_satisfies_iversioned_protocol` | ⏳ |

**Acceptance Criteria:**

- [ ] ProjectInfo extends EntityBase
- [ ] Inherits IAuditable properties (created_by/at, updated_by/at)
- [ ] Inherits IVersioned properties (version, get_expected_version)
- [ ] Protocol checks pass (`isinstance(project, IAuditable)`)
- [ ] All tests pass

---

#### I-008d.2.2: Add JerryUri Computation

| Phase | Description | Files | Tests |
|-------|-------------|-------|-------|
| **RED** | Write tests for `jerry_uri` property | Test files | 5+ |
| **GREEN** | Add `jerry_uri` computed property | `project_info.py` | - |
| **REFACTOR** | Ensure URI format matches spec | - | - |

**Test Cases (BDD):**

| Category | Test | Status |
|----------|------|--------|
| **Unit - Happy** | `test_project_info_has_jerry_uri_property` | ⏳ |
| **Unit - Happy** | `test_project_info_jerry_uri_format_correct` | ⏳ |
| **Unit - Edge** | `test_project_info_jerry_uri_with_special_id` | ⏳ |
| **Contract** | `test_jerry_uri_matches_spec_001` | ⏳ |

**Acceptance Criteria:**

- [ ] `jerry_uri` property returns JerryUri instance
- [ ] Format: `jerry://project/{project_id}`
- [ ] Matches JERRY_URI_SPECIFICATION.md

---

#### I-008d.2.3: Add Extensibility (metadata, tags)

| Phase | Description | Files | Tests |
|-------|-------------|-------|-------|
| **RED** | Write tests for metadata and tags | Test files | 8+ |
| **GREEN** | Add `metadata: dict` and `tags: list[str]` | `project_info.py` | - |
| **REFACTOR** | Ensure immutability | - | - |

**Test Cases (BDD):**

| Category | Test | Status |
|----------|------|--------|
| **Unit - Happy** | `test_project_info_has_metadata_property` | ⏳ |
| **Unit - Happy** | `test_project_info_has_tags_property` | ⏳ |
| **Unit - Happy** | `test_project_info_metadata_defaults_empty` | ⏳ |
| **Unit - Happy** | `test_project_info_tags_defaults_empty` | ⏳ |
| **Unit - Edge** | `test_project_info_metadata_with_nested_values` | ⏳ |
| **Unit - Negative** | `test_project_info_metadata_rejects_non_dict` | ⏳ |
| **Unit - Negative** | `test_project_info_tags_rejects_non_list` | ⏳ |

**Acceptance Criteria:**

- [ ] `metadata: dict[str, Any]` property with default `{}`
- [ ] `tags: list[str]` property with default `[]`
- [ ] Both are optional on construction
- [ ] All tests pass

---

### I-008d.3: New Domain Objects (Implementation Phase)

> **Phase ID**: I-008d.3
> **Status**: PENDING
> **Depends On**: R-008d.0 (can parallel with I-008d.2)
> **Approach**: BDD Red/Green/Refactor
> **Test Phase**: T-008d.3

#### I-008d.3.1: Create SessionId Value Object

| Phase | Description | Files | Tests |
|-------|-------------|-------|-------|
| **RED** | Write tests for SessionId | Test files | 10+ |
| **GREEN** | Implement SessionId extending VertexId | `session_id.py` | - |
| **REFACTOR** | Ensure consistency with other IDs | - | - |

**File Changes:**

| File | Change Type | Description |
|------|-------------|-------------|
| `src/session_management/domain/value_objects/session_id.py` | CREATE | New file |
| `src/shared_kernel/vertex_id.py` | MODIFY | Add SessionId type |
| `tests/session_management/unit/test_session_id.py` | CREATE | New test file |

**Test Cases (BDD):**

| Category | Test | Status |
|----------|------|--------|
| **Unit - Happy** | `test_session_id_extends_vertex_id` | ⏳ |
| **Unit - Happy** | `test_session_id_generate_creates_valid_format` | ⏳ |
| **Unit - Happy** | `test_session_id_format_is_sess_uuid8` | ⏳ |
| **Unit - Happy** | `test_session_id_from_string_parses_valid` | ⏳ |
| **Unit - Edge** | `test_session_id_equality` | ⏳ |
| **Unit - Edge** | `test_session_id_hash` | ⏳ |
| **Unit - Negative** | `test_session_id_rejects_invalid_format` | ⏳ |
| **Unit - Negative** | `test_session_id_rejects_wrong_prefix` | ⏳ |
| **Architecture** | `test_session_id_no_infra_imports` | ⏳ |

**Acceptance Criteria:**

- [ ] SessionId extends VertexId
- [ ] Format: `SESS-{uuid8}`
- [ ] Standard VertexId interface (generate, from_string)
- [ ] All tests pass

---

#### I-008d.3.2: Create Session Aggregate Root

| Phase | Description | Files | Tests |
|-------|-------------|-------|-------|
| **RED** | Write tests for Session aggregate | Test files | 15+ |
| **GREEN** | Implement Session extending EntityBase | `session.py` | - |
| **REFACTOR** | Ensure aggregate invariants | - | - |

**File Changes:**

| File | Change Type | Description |
|------|-------------|-------------|
| `src/session_management/domain/aggregates/session.py` | CREATE | New file |
| `tests/session_management/unit/test_session.py` | CREATE | New test file |

**Test Cases (BDD):**

| Category | Test | Status |
|----------|------|--------|
| **Unit - Happy** | `test_session_extends_entity_base` | ⏳ |
| **Unit - Happy** | `test_session_has_session_id` | ⏳ |
| **Unit - Happy** | `test_session_has_started_at` | ⏳ |
| **Unit - Happy** | `test_session_has_project_id_optional` | ⏳ |
| **Unit - Happy** | `test_session_can_set_project` | ⏳ |
| **Unit - Happy** | `test_session_implements_iauditable` | ⏳ |
| **Unit - Edge** | `test_session_without_project_is_valid` | ⏳ |
| **Unit - Edge** | `test_session_project_can_be_changed` | ⏳ |
| **Unit - Negative** | `test_session_rejects_invalid_project_id` | ⏳ |
| **Architecture** | `test_session_is_aggregate_root` | ⏳ |

**Acceptance Criteria:**

- [ ] Session extends EntityBase
- [ ] Has SessionId as identity
- [ ] Has optional ProjectId reference
- [ ] Has started_at timestamp
- [ ] Implements IAuditable
- [ ] All tests pass

---

#### I-008d.3.3: Add session_id to ProjectInfo

| Phase | Description | Files | Tests |
|-------|-------------|-------|-------|
| **RED** | Write tests for session_id on ProjectInfo | Test files | 5+ |
| **GREEN** | Add `last_session_id: SessionId | None` | `project_info.py` | - |
| **REFACTOR** | Ensure provenance tracking | - | - |

**Test Cases (BDD):**

| Category | Test | Status |
|----------|------|--------|
| **Unit - Happy** | `test_project_info_has_last_session_id` | ⏳ |
| **Unit - Happy** | `test_project_info_session_id_defaults_none` | ⏳ |
| **Unit - Edge** | `test_project_info_session_id_can_be_set` | ⏳ |

**Acceptance Criteria:**

- [ ] `last_session_id: SessionId | None` property
- [ ] Defaults to None
- [ ] Provides provenance tracking

---

### I-008d.4: Infrastructure Updates (Implementation Phase)

> **Phase ID**: I-008d.4
> **Status**: PENDING
> **Depends On**: I-008d.1, I-008d.2, I-008d.3
> **Approach**: BDD Red/Green/Refactor
> **Test Phase**: T-008d.4

#### I-008d.4.1: Update FilesystemProjectAdapter

| Phase | Description | Files | Tests |
|-------|-------------|-------|-------|
| **RED** | Write integration tests for new ID format | Test files | 10+ |
| **GREEN** | Update adapter for new ProjectId format | Adapter | - |
| **REFACTOR** | Ensure backward compatibility handling | - | - |

**File Changes:**

| File | Change Type | Description |
|------|-------------|-------------|
| `src/session_management/infrastructure/adapters/filesystem_adapter.py` | MODIFY | Handle new ID format |
| `tests/session_management/integration/test_filesystem_adapter.py` | CREATE | Integration tests |

**Test Cases (BDD):**

| Category | Test | Status |
|----------|------|--------|
| **Integration - Happy** | `test_adapter_scans_new_format_directories` | ⏳ |
| **Integration - Happy** | `test_adapter_populates_all_entity_properties` | ⏳ |
| **Integration - Edge** | `test_adapter_handles_mixed_old_new_format` | ⏳ |
| **Integration - Edge** | `test_adapter_extracts_slug_from_directory` | ⏳ |
| **Integration - Negative** | `test_adapter_rejects_invalid_directory_format` | ⏳ |
| **Integration - Failure** | `test_adapter_handles_permission_denied` | ⏳ |

**Acceptance Criteria:**

- [ ] Adapter scans directories with new `PROJ-{uuid8}` format
- [ ] Extracts slug from directory name (after ID)
- [ ] Populates all EntityBase properties
- [ ] Handles old format gracefully (warning, not error)
- [ ] All integration tests pass

---

#### I-008d.4.2: Migrate Existing Projects

| Phase | Description | Files | Tests |
|-------|-------------|-------|-------|
| **RED** | Write tests for migration script | Test files | 5+ |
| **GREEN** | Create migration script/logic | Migration script | - |
| **REFACTOR** | Ensure idempotent migration | - | - |

**Migration Plan:**

| Step | Action | Risk |
|------|--------|------|
| 1 | Backup existing `projects/` | LOW |
| 2 | Generate new PROJ-{uuid8} IDs | LOW |
| 3 | Rename directories (preserve slug) | MEDIUM |
| 4 | Update internal references | MEDIUM |
| 5 | Validate migration | LOW |

**Acceptance Criteria:**

- [ ] Migration script created
- [ ] Existing PROJ-001-plugin-cleanup migrated
- [ ] All references updated
- [ ] Rollback plan documented

---

#### T-008d.4.3: Update Infrastructure Tests

| Phase | Description | Files | Tests |
|-------|-------------|-------|-------|
| **RED** | Identify failing infrastructure tests | Test files | - |
| **GREEN** | Update tests for new format | Test files | - |
| **REFACTOR** | Consolidate test fixtures | - | - |

**Acceptance Criteria:**

- [ ] All infrastructure tests updated
- [ ] Test fixtures use new format
- [ ] 0 regressions

---

## ENFORCE-009: Application Layer Tests

> **Status**: PENDING
> **Depends On**: ENFORCE-008d
> **Test File**: `tests/session_management/unit/test_application.py`

### Test Matrix

| Category | Count | Status |
|----------|-------|--------|
| Happy Path | 5 | ⏳ |
| Edge Cases | 9 | ⏳ |
| Negative | 5 | ⏳ |
| Failure Scenarios | 4 | ⏳ |
| **Total** | **23** | **⏳** |

<details>
<summary>Click to expand test list</summary>

#### Happy Path Tests

- [ ] `test_scan_projects_returns_sorted_list`
- [ ] `test_scan_projects_returns_project_info_with_status`
- [ ] `test_validate_project_when_exists_returns_valid`
- [ ] `test_validate_project_includes_warnings_for_missing_files`
- [ ] `test_get_next_number_returns_incremented_value`

#### Edge Case Tests

- [ ] `test_scan_projects_with_empty_repo_returns_empty_list`
- [ ] `test_scan_projects_ignores_hidden_directories`
- [ ] `test_scan_projects_ignores_non_project_directories`
- [ ] `test_scan_projects_ignores_archive_directory`
- [ ] `test_scan_projects_handles_gaps_in_numbering`
- [ ] `test_scan_projects_sorts_by_number_not_alphabetically`
- [ ] `test_get_next_number_with_no_projects_returns_001`
- [ ] `test_get_next_number_with_gaps_uses_max_plus_one`
- [ ] `test_get_next_number_with_archived_projects_excludes_them`

#### Negative Tests

- [ ] `test_scan_projects_with_null_repo_raises_error`
- [ ] `test_validate_project_with_nonexistent_id_returns_invalid`
- [ ] `test_validate_project_with_invalid_id_format_returns_invalid`
- [ ] `test_validate_project_with_archived_project_returns_invalid`
- [ ] `test_get_next_number_with_corrupted_repo_raises_error`

#### Failure Scenario Tests

- [ ] `test_scan_projects_when_repo_unavailable_returns_error`
- [ ] `test_validate_project_when_file_read_fails_returns_error`
- [ ] `test_get_next_number_when_scan_fails_propagates_error`
- [ ] `test_validate_project_with_missing_plan_returns_warning`

</details>

---

## ENFORCE-010: Infrastructure Tests

> **Status**: PENDING
> **Depends On**: ENFORCE-008d
> **Test File**: `tests/session_management/integration/test_infrastructure.py`

### Test Matrix

| Category | Count | Status |
|----------|-------|--------|
| Happy Path | 4 | ⏳ |
| Edge Cases | 9 | ⏳ |
| Negative | 3 | ⏳ |
| Failure Scenarios | 6 | ⏳ |
| **Total** | **22** | **⏳** |

<details>
<summary>Click to expand test list</summary>

#### Happy Path Tests

- [ ] `test_filesystem_adapter_scans_real_project_directory`
- [ ] `test_filesystem_adapter_reads_worktracker_status`
- [ ] `test_filesystem_adapter_detects_plan_existence`
- [ ] `test_os_environment_adapter_reads_jerry_project`

#### Edge Case Tests

- [ ] `test_filesystem_adapter_with_empty_directory`
- [ ] `test_filesystem_adapter_with_only_archive_directory`
- [ ] `test_filesystem_adapter_with_mixed_valid_invalid_dirs`
- [ ] `test_filesystem_adapter_with_symlinked_project`
- [ ] `test_filesystem_adapter_with_deeply_nested_structure`
- [ ] `test_filesystem_adapter_handles_unicode_in_paths`
- [ ] `test_filesystem_adapter_handles_spaces_in_paths`
- [ ] `test_os_environment_adapter_with_empty_var`
- [ ] `test_os_environment_adapter_with_whitespace_only_var`

#### Negative Tests

- [ ] `test_filesystem_adapter_with_nonexistent_base_path`
- [ ] `test_filesystem_adapter_with_file_instead_of_directory`
- [ ] `test_os_environment_adapter_with_unset_var_returns_none`

#### Failure Scenario Tests

- [ ] `test_filesystem_adapter_handles_permission_denied`
- [ ] `test_filesystem_adapter_handles_io_error_on_read`
- [ ] `test_filesystem_adapter_handles_corrupt_worktracker`
- [ ] `test_filesystem_adapter_handles_binary_file_as_worktracker`
- [ ] `test_filesystem_adapter_handles_extremely_large_worktracker`
- [ ] `test_filesystem_adapter_recovers_from_partial_read`

</details>

---

## ENFORCE-011: E2E Tests

> **Status**: PENDING
> **Depends On**: ENFORCE-009, ENFORCE-010
> **Test File**: `tests/session_management/e2e/test_session_start.py`

### Test Matrix

| Category | Count | Status |
|----------|-------|--------|
| Happy Path | 6 | ⏳ |
| Edge Cases | 6 | ⏳ |
| Negative | 3 | ⏳ |
| Failure Scenarios | 4 | ⏳ |
| Output Format | 4 | ⏳ |
| **Total** | **23** | **⏳** |

<details>
<summary>Click to expand test list</summary>

(Full test list preserved from original WORKTRACKER)

</details>

---

## ENFORCE-012: Contract Tests

> **Status**: PENDING
> **Depends On**: ENFORCE-011
> **Test File**: `tests/session_management/contract/test_hook_contract.py`

### Test Matrix

| Test | Status |
|------|--------|
| `test_output_contains_required_project_context_tag` | ⏳ |
| `test_output_contains_required_project_required_tag` | ⏳ |
| `test_output_json_matches_schema` | ⏳ |
| `test_output_action_required_message_present_when_needed` | ⏳ |
| `test_output_exit_code_semantics_match_hook_spec` | ⏳ |

---

## ENFORCE-013: Architecture Tests

> **Status**: PENDING
> **Depends On**: ENFORCE-008d
> **Test File**: `tests/session_management/architecture/test_architecture.py`

### Test Matrix

| Test | Status |
|------|--------|
| `test_domain_layer_has_no_external_imports` | ⏳ |
| `test_domain_layer_has_no_infrastructure_imports` | ⏳ |
| `test_application_layer_only_imports_domain` | ⏳ |
| `test_infrastructure_implements_port_interfaces` | ⏳ |
| `test_dependency_direction_flows_inward` | ⏳ |

---

## ENFORCE-014: Update CLAUDE.md

> **Status**: PENDING
> **Depends On**: ENFORCE-011

### Subtasks

| ID | Task | Status |
|----|------|--------|
| 014.1 | Add "Project Enforcement (Hard Rule)" section | ⏳ |
| 014.2 | Document structured hook output format | ⏳ |
| 014.3 | Document required AskUserQuestion flow | ⏳ |
| 014.4 | Document project creation flow with auto-ID | ⏳ |
| 014.5 | Add behavior test scenario to BEHAVIOR_TESTS.md | ⏳ |

---

## ENFORCE-015: Update Manifest and Settings

> **Status**: PENDING
> **Depends On**: ENFORCE-014

### Subtasks

| ID | Task | Status |
|----|------|--------|
| 015.1 | Update `.claude-plugin/manifest.json` hooks section | ⏳ |
| 015.2 | Update `.claude/settings.json` SessionStart hook | ⏳ |
| 015.3 | Ensure backward compatibility | ⏳ |

---

## ENFORCE-016: Final Validation

> **Status**: PENDING
> **Depends On**: ALL previous tasks

### Subtasks

| ID | Task | Status |
|----|------|--------|
| 016.1 | Run full test suite (all categories pass) | ⏳ |
| 016.2 | Manual test: session start with JERRY_PROJECT set | ⏳ |
| 016.3 | Manual test: session start without JERRY_PROJECT | ⏳ |
| 016.4 | Manual test: project creation flow | ⏳ |
| 016.5 | Manual test: project selection flow | ⏳ |
| 016.6 | Manual test: invalid project handling | ⏳ |
| 016.7 | Security review (no path traversal, injection) | ⏳ |
| 016.8 | Commit with conventional commit message | ⏳ |
| 016.9 | Update WORKTRACKER with completion status | ⏳ |
| 016.10 | Create PR for review | ⏳ |

---

## Session Context

> **Purpose**: Information needed to resume work after context compaction

### Current State (2026-01-09)

- **Active Phase**: R-008d (Research)
- **Active Subtask**: R-008d.0 - Research & Analysis
- **Last Completed**: Shared Kernel implementation (58 tests), Phase 7 Design Canon (✅)
- **Blocker**: None
- **Next Action**: Complete 5W1H research for R-008d per WORKTRACKER schema

### Key Files

| File | Purpose |
|------|---------|
| `src/shared_kernel/` | Shared Kernel (complete, 58 tests) |
| `src/session_management/` | Current domain to refactor |
| `design/ADR-013-shared-kernel.md` | Implementation spec |
| `synthesis/PROJ-001-e-011-v1-jerry-design-canon.md` | Design canon |

### Important Decisions

1. ProjectId format changing from `PROJ-NNN-slug` to `PROJ-{uuid8}`
2. Slug extracted to separate property on ProjectInfo
3. Session aggregate root for provenance tracking
4. Migration required for existing projects

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-09 | Claude | Created from WORKTRACKER restructuring |
| 2026-01-09 | Claude | Added detailed 008d breakdown with BDD approach |
| 2026-01-09 | Claude | Enhanced with Work Item Schema (R/I/T/E phases) |
| 2026-01-09 | Claude | Added Aggregated Test Matrix and Verification Checklist |
