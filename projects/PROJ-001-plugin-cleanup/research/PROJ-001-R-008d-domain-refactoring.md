# R-008d Domain Refactoring - 5W1H Analysis

> **Document ID**: PROJ-001-R-008d-domain-refactoring
> **Date**: 2026-01-10
> **Author**: Claude Opus 4.5
> **Task**: ENFORCE-008d - Refactor to Unified Design
> **Status**: COMPLETE

---

## 5W1H Analysis

### What (WHAT needs to be done?)

Refactor `src/session_management/domain/` to use Shared Kernel patterns:

1. **ProjectId Value Object** → Extend `VertexId` from shared_kernel
2. **ProjectInfo Entity** → Extend `EntityBase` from shared_kernel
3. **New Domain Objects** → Create `SessionId` and `Session` aggregate
4. **Infrastructure** → Update adapters for new domain contracts

### Why (WHY is this needed?)

| Reason | Justification |
|--------|---------------|
| **Consistency** | All bounded contexts must use unified identity patterns (Canon PAT-001) |
| **Graph Readiness** | VertexId enables future graph database migration (PAT-001, L56-117) |
| **Audit Compliance** | IAuditable provides consistent creation/modification tracking (PAT-005) |
| **Concurrency Safety** | IVersioned prevents lost updates (PAT-006) |
| **DDD Alignment** | Shared Kernel is standard DDD pattern (Eric Evans) |

**Risk of NOT doing**: Each bounded context invents its own ID patterns, leading to inconsistent behavior and integration difficulties.

### Who (WHO is affected?)

| Stakeholder | Impact |
|-------------|--------|
| **Domain Layer** | ProjectId, ProjectInfo contracts change |
| **Infrastructure** | FilesystemProjectAdapter uses new contracts |
| **Tests** | 57 existing tests may need updates |
| **Consumers** | Any code using ProjectId.number/slug directly |

### Where (WHERE in the codebase?)

#### Files to MODIFY

| File | Changes |
|------|---------|
| `src/session_management/domain/value_objects/project_id.py` | Extend VertexId |
| `src/session_management/domain/entities/project_info.py` | Extend EntityBase |
| `src/session_management/infrastructure/adapters/filesystem_project_adapter.py` | Use new contracts |
| `tests/session_management/unit/domain/test_project_id.py` | Update for new format |
| `tests/session_management/unit/domain/test_project_info.py` | Update for EntityBase |

#### Files to CREATE

| File | Purpose |
|------|---------|
| `src/session_management/domain/value_objects/session_id.py` | SessionId extending VertexId |
| `src/session_management/domain/aggregates/session.py` | Session aggregate |
| `tests/session_management/unit/domain/test_session_id.py` | SessionId tests |
| `tests/session_management/unit/domain/test_session.py` | Session aggregate tests |

### When (WHEN can this start? Dependencies?)

#### Prerequisites (All Complete)
- [x] Shared Kernel implemented (`src/shared_kernel/`) - 142 tests
- [x] Phase 7 Design Canon complete
- [x] ADR-013 Shared Kernel approved
- [x] All 16 IMPL tasks complete (975 tests)

#### Blocking Dependencies
None. ENFORCE-008d can proceed immediately.

### How (HOW will it be implemented?)

#### Approach: Incremental Refactoring with BDD

```
I-008d.1: Value Objects
├── 1.1 Refactor ProjectId to extend VertexId
├── 1.2 Preserve number/slug as convenience properties
└── 1.3 Update VO tests

I-008d.2: Entities (can parallel with I-008d.3)
├── 2.1 Refactor ProjectInfo to extend EntityBase
├── 2.2 Add IAuditable metadata
└── 2.3 Update entity tests

I-008d.3: New Domain Objects (can parallel with I-008d.2)
├── 3.1 Create SessionId extending VertexId
├── 3.2 Create Session aggregate
└── 3.3 Add session_id to ProjectInfo

I-008d.4: Infrastructure
├── 4.1 Update FilesystemProjectAdapter
├── 4.2 Handle migration of existing project data
└── 4.3 Update infrastructure tests
```

---

## Current vs Target Analysis

### ProjectId

| Aspect | Current | Target |
|--------|---------|--------|
| **Base Class** | None (standalone dataclass) | `VertexId` |
| **Format** | `PROJ-{nnn}-{slug}` | Same (preserve compatibility) |
| **Properties** | `value`, `number`, `slug` | `value` (inherit) + `number`, `slug` (extract) |
| **Validation** | In `__post_init__` + `parse()` | Via `_is_valid_format()` |
| **Generation** | `create(number, slug)` | `generate()` (for new format) + `create()` (legacy) |

**Key Decision**: Preserve existing format `PROJ-{nnn}-{slug}` for backwards compatibility. The `number` and `slug` can be extracted properties.

### ProjectInfo

| Aspect | Current | Target |
|--------|---------|--------|
| **Base Class** | None (standalone dataclass) | `EntityBase` |
| **Identity** | `id: ProjectId` | `_id: ProjectId` (via EntityBase) |
| **Audit** | None | `created_at`, `created_by`, `updated_at`, `updated_by` |
| **Version** | None | `version` (for optimistic concurrency) |
| **Properties** | `status`, `has_plan`, `has_tracker`, `path` | Same (preserve) |

---

## Breaking Change Assessment

### Breaking Changes

| Change | Impact | Mitigation |
|--------|--------|------------|
| ProjectId extends VertexId | Type hierarchy change | All checks using `isinstance(x, ProjectId)` still work |
| ProjectId.parse() → from_string() | API change | Add `from_string()` as alias, deprecate `parse()` |
| ProjectInfo.id → ProjectInfo._id | Property access change | Property accessor still works via EntityBase |
| New required fields on ProjectInfo | Constructor change | Default values for audit fields |

### Non-Breaking Changes

| Change | Reason |
|--------|--------|
| Format stays `PROJ-{nnn}-{slug}` | Existing project directories unaffected |
| `number` and `slug` properties | Available via extraction from `value` |
| Existing adapter contracts | IProjectRepository interface unchanged |

---

## Test Strategy

### Unit Tests Required

| Category | Count | Focus |
|----------|-------|-------|
| ProjectId VertexId compliance | 8 | `_is_valid_format()`, `from_string()`, inheritance |
| ProjectId backwards compat | 5 | `parse()` alias, `number`, `slug` extraction |
| ProjectInfo EntityBase compliance | 6 | Audit fields, version, id property |
| SessionId new VO | 8 | Standard VertexId tests |
| Session aggregate | 12 | Creation, state transitions, events |

### Test Locations

```
tests/session_management/unit/domain/
├── test_project_id.py          # Update existing (15 tests)
├── test_project_info.py        # Update existing (12 tests)
├── test_session_id.py          # NEW (8 tests)
└── test_session.py             # NEW (12 tests)
```

---

## Research Citations

### Industry Best Practices

1. **Value Object Migration** (Martin Fowler)
   - Source: martinfowler.com/bliki/ValueObject.html
   - Guidance: Preserve value equality semantics when changing hierarchy

2. **DDD Shared Kernel** (Eric Evans, Domain-Driven Design, 2003)
   - Chapter 14: Shared Kernel
   - Guidance: Shared kernel should be minimal, well-tested, and stable

3. **Entity Refactoring** (Vaughn Vernon, Implementing DDD, 2013)
   - Chapter 5: Entities
   - Guidance: Entity identity must remain stable during refactoring

### Context7 Research

1. **Python Dataclass Inheritance**
   - Frozen dataclasses can inherit from frozen dataclasses
   - Default values in parent require defaults in child (or field reordering)

2. **VertexId Pattern** (Canon PAT-001)
   - Abstract base with `_is_valid_format()` and `generate()`
   - Value equality via frozen dataclass

---

## File Change Inventory

### MODIFY

1. `src/session_management/domain/value_objects/project_id.py`
   - Lines affected: 32-157 (entire class)
   - Change: Extend VertexId, preserve compatibility

2. `src/session_management/domain/entities/project_info.py`
   - Lines affected: 16-110 (entire class)
   - Change: Extend EntityBase, add audit fields

3. `src/session_management/infrastructure/adapters/filesystem_project_adapter.py`
   - Lines affected: 189-195 (_read_project_info)
   - Change: Populate audit fields

4. `tests/session_management/unit/domain/test_project_id.py`
   - Add VertexId compliance tests

5. `tests/session_management/unit/domain/test_project_info.py`
   - Add EntityBase compliance tests

### CREATE

1. `src/session_management/domain/value_objects/session_id.py`
2. `src/session_management/domain/aggregates/__init__.py`
3. `src/session_management/domain/aggregates/session.py`
4. `tests/session_management/unit/domain/test_session_id.py`
5. `tests/session_management/unit/domain/test_session.py`

### DELETE

None - No files to delete.

---

## Implementation Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Test failures from format change | Low | Medium | Preserve PROJ-{nnn}-{slug} format |
| Circular imports with shared_kernel | Low | High | shared_kernel has no session_management imports |
| Adapter incompatibility | Medium | Medium | Update _read_project_info to handle new fields |
| Performance regression | Low | Low | No algorithmic changes |

---

## Success Criteria

- [ ] ProjectId extends VertexId
- [ ] ProjectId.number and .slug still work
- [ ] ProjectInfo extends EntityBase
- [ ] ProjectInfo has audit metadata
- [ ] SessionId and Session created
- [ ] All existing tests pass (zero regressions)
- [ ] 45+ new tests added
- [ ] Coverage ≥ 90%

---

## Next Steps

1. **I-008d.1.1**: Write failing tests for ProjectId VertexId compliance (RED)
2. **I-008d.1.1**: Implement ProjectId extending VertexId (GREEN)
3. **I-008d.1.1**: Verify backwards compatibility (REFACTOR)
4. Continue through I-008d.1.2, I-008d.1.3...

---

*Document generated as part of R-008d.0 Research Phase*
*Ready for I-008d.1 implementation*
