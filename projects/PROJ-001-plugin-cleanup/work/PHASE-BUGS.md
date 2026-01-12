# Phase BUGS: Bug Tracking

> **Status**: ✅ RESOLVED (all bugs fixed)
> **Purpose**: Track bugs discovered during PROJ-001 development

---

## Navigation

| Link | Description |
|------|-------------|
| [← WORKTRACKER](../WORKTRACKER.md) | Back to index |
| [TECHDEBT](PHASE-TECHDEBT.md) | Technical debt |
| [DISCOVERY](PHASE-DISCOVERY.md) | Technical discoveries |
| [INITIATIVE-WT-SKILLS](INITIATIVE-WORKTRACKER-SKILLS.md) | Active initiative |

---

## Bug Summary

| ID | Title | Severity | Status | Phase Found |
|----|-------|----------|--------|-------------|
| BUG-001 | Phase 7 artifacts reference old `docs/` paths | MEDIUM | ✅ FIXED | Phase 7 |
| BUG-002 | Hook decision value needs verification | N/A | ✅ CLOSED | Phase 6 |
| BUG-003 | Pyright type errors in serializer.py | HIGH | ✅ FIXED | CI-002 |
| BUG-004 | Type variance warning in repository.py | LOW | ✅ FIXED | CI-002 |

---

## BUG-001: Phase 7 Artifacts Reference Old Paths ✅

> **Status**: FIXED
> **Resolution Date**: 2026-01-10
> **Severity**: MEDIUM

### Description

Multiple Phase 7 artifacts reference file paths using the old `docs/{category}/` convention instead of the correct `projects/PROJ-001-plugin-cleanup/{category}/` paths.

### Root Cause

The ps-* agents were updated (TD-001) to OUTPUT to project-centric paths, but the agents still used old `docs/` paths when REFERENCING other documents in their output content.

### Impact

Document lineage references were broken; traceability was compromised.

### Resolution

Fixed path references in 4 files (22 total references):

| File | References Fixed |
|------|------------------|
| `e-010-synthesis-status-report.md` | 8 |
| `e-007-implementation-gap-analysis.md` | 2 |
| `e-009-alignment-validation.md` | 2 |
| `e-006-unified-architecture-canon.md` | 10 |

### Validation

- `grep -r 'docs/(research|synthesis|analysis|decisions)/PROJ-001'` returns 0 matches
- Test suite: 98/98 tests passing (100%)

### Follow-up

Moved to TECHDEBT (TD-002): Update ps-* agents to use project-relative paths in REFERENCES.

---

## BUG-002: Hook Decision Value Verification ✅

> **Status**: CLOSED (Not a Bug)
> **Resolution Date**: 2026-01-10
> **Severity**: N/A

### Description

The `.claude/hooks/pre_tool_use.py` hook was modified to change the decision value from `"allow"` to `"approve"`.

### Research Findings

- Per Claude Code Hooks Mastery: Simple decision format uses `"approve"|"block"`
- Per Claude Code Official Docs: Prompt hooks return `"approve"` or `"deny"`
- The original `"allow"` value was **INCORRECT**
- The change to `"approve"` is **CORRECT**

### Resolution

No action needed - the change was correct.

### Follow-up

Moved to TECHDEBT (TD-003): Add unit tests for hook decision values.

---

## BUG-003: Pyright Type Errors in serializer.py ✅

> **Status**: FIXED (2026-01-11)
> **Severity**: HIGH
> **Phase Found**: CI-002 (GitHub Actions)

### Description

Pyright reports 2 type errors in `src/infrastructure/internal/serializer.py` at lines 137 and 176. The errors occur because `hasattr()` checks don't narrow the type for pyright, so it doesn't recognize the `to_dict` attribute.

### Evidence

GitHub Actions logs from run `20903651374`:
```
/home/runner/work/jerry/jerry/src/infrastructure/internal/serializer.py:137:28 - error: Cannot access attribute "to_dict" for class "type[DataclassInstance]"
  Attribute "to_dict" is unknown (reportAttributeAccessIssue)

/home/runner/work/jerry/jerry/src/infrastructure/internal/serializer.py:176:24 - error: Cannot access attribute "to_dict" for class "type[DataclassInstance]"
  Attribute "to_dict" is unknown (reportAttributeAccessIssue)
```

### Root Cause Analysis (5W1H)

| Question | Answer |
|----------|--------|
| What | Pyright cannot narrow type after `hasattr()` check |
| Why | `hasattr()` is runtime check, not understood by type checker |
| Who | Affects type checking CI job |
| Where | `src/infrastructure/internal/serializer.py:137,176` |
| When | During pyright static analysis in CI |
| How | Code uses `hasattr(obj, "to_dict")` but pyright doesn't narrow |

### Impact

- Type Check job fails
- CI pipeline blocked
- v0.0.1 release blocked

### Proposed Fix

**Option A: Use Protocol for type narrowing (Recommended)**

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class HasToDict(Protocol):
    def to_dict(self) -> dict: ...

# Then in serialize():
if isinstance(obj, HasToDict):
    data = obj.to_dict()  # Now pyright knows obj has to_dict
```

**Option B: Type ignore comments (Quick fix)**

```python
data = obj.to_dict()  # type: ignore[attr-defined]
```

### Files to Modify

| File | Action |
|------|--------|
| `src/infrastructure/internal/serializer.py` | Add Protocol or type: ignore |

### Resolution

Implemented **Option A: Use Protocol for type narrowing**.

1. Added `@runtime_checkable class HasToDict(Protocol)` to `src/infrastructure/internal/serializer.py`
2. Changed `hasattr(obj, "to_dict")` to `isinstance(obj, HasToDict)` at lines 150 and 189

This approach uses structural typing via Protocol, which pyright can use for type narrowing. The `@runtime_checkable` decorator allows `isinstance()` checks at runtime.

### Acceptance Criteria

- [x] Pyright reports 0 errors for serializer.py
- [ ] Type Check CI job passes - pending CI verification
- [x] No loss of functionality (isinstance is semantically equivalent to hasattr)
- [x] Existing tests still pass

---

## BUG-004: Type Variance Warning in repository.py ✅

> **Status**: FIXED (2026-01-11)
> **Severity**: LOW (Warning, not error)
> **Phase Found**: CI-002 (GitHub Actions)

### Description

Pyright warns that the type variable `TId` in the `IRepository` Protocol should be contravariant because it's used in input positions.

### Evidence

GitHub Actions logs from run `20903651374`:
```
/home/runner/work/jerry/jerry/src/work_tracking/domain/ports/repository.py:95:7 - warning: Type variable "TId" used in generic Protocol "IRepository" should be contravariant (reportInvalidTypeVarUse)
```

### Root Cause Analysis (5W1H)

| Question | Answer |
|----------|--------|
| What | Type variable variance mismatch in Protocol |
| Why | `TId` used in input positions (`get(id: TId)`) requires contravariance |
| Who | Affects type checking CI job |
| Where | `src/work_tracking/domain/ports/repository.py:95` |
| When | During pyright static analysis in CI |
| How | `TId = TypeVar("TId")` should be `TId = TypeVar("TId", contravariant=True)` |

### Impact

- Warning (not blocking, but indicates incorrect typing)
- CI treats warnings as acceptable but not ideal
- Could cause issues with type inference in callers

### Proposed Fix

```python
# Change from:
TId = TypeVar("TId")

# To:
TId = TypeVar("TId", contravariant=True)
```

However, this may have cascading effects. An alternative is to suppress the warning if contravariance causes other issues.

### Files to Modify

| File | Action |
|------|--------|
| `src/work_tracking/domain/ports/repository.py` | Add `contravariant=True` or suppress warning |

### Resolution

Changed `TId = TypeVar("TId")` to `TId = TypeVar("TId", contravariant=True)` in `src/work_tracking/domain/ports/repository.py` line 34.

Added a comment explaining the variance: `# Contravariant because TId appears only in input positions (get, delete, exists)`

This is the correct fix because `TId` is only used in input parameter positions (`get(id: TId)`, `delete(id: TId)`, `exists(id: TId)`), and type variables in input-only positions should be contravariant per the Liskov Substitution Principle.

### Acceptance Criteria

- [x] Pyright warning resolved (0 errors, 0 warnings)
- [x] No regression in existing type checking
- [x] Repository implementations still work correctly

---

## Bug Reporting Template

When reporting new bugs, use this template:

```markdown
## BUG-XXX: [Title]

> **Status**: 🐛 OPEN
> **Severity**: [CRITICAL|HIGH|MEDIUM|LOW]
> **Phase Found**: [Phase X]

### Description
[What is the bug?]

### Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Expected vs Actual]

### Root Cause Analysis (5W1H)
| Question | Answer |
|----------|--------|
| What | |
| Why | |
| Who | |
| Where | |
| When | |
| How | |

### Impact
[What does this break?]

### Proposed Fix
[How to fix it?]

### Acceptance Criteria
- [ ] Bug no longer reproducible
- [ ] Tests added to prevent regression
- [ ] Documentation updated if needed
```

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-09 | Claude | Initial creation |
| 2026-01-09 | Claude | Migrated to multi-file format |
| 2026-01-11 | Claude | Added BUG-003, BUG-004 (CI-002 failures) |
| 2026-01-11 | Claude | Fixed BUG-003, BUG-004 (CI-002 resolution) |
