# WI-SAO-021: E2E Test Path Analysis

> **Document ID:** ANL-SAO-021-001
> **Work Item:** WI-SAO-021 (Orchestration Folder Refactoring)
> **Date:** 2026-01-10
> **Status:** COMPLETE

---

## Executive Summary

This analysis examines the existing E2E tests for hardcoded paths and determines their usefulness for validating the dynamic path scheme.

**Finding:** All 3 E2E tests have hardcoded paths but remain useful for validating orchestration patterns. They need to be UPDATED, not removed.

---

## 1. Test Inventory

| Test | File | Pattern Tested | Artifacts |
|------|------|----------------|-----------|
| TEST-001 | TEST-001-LINEAR-WORKFLOW.yaml | Sequential chain | 3 |
| TEST-002 | TEST-002-PARALLEL-WORKFLOW.yaml | Fan-out/Fan-in | 4 |
| TEST-003 | TEST-003-CROSSPOLL-WORKFLOW.yaml | Cross-pollination | 6 |

---

## 2. Hardcoded Path Analysis

### TEST-001: Linear Sequential Workflow

**Base Path:** `tests/e2e/artifacts/`

| Artifact | Current Path | Hardcoded? |
|----------|--------------|------------|
| Phase A output | `tests/e2e/artifacts/phase-a-output.md` | YES |
| Phase B output | `tests/e2e/artifacts/phase-b-output.md` | YES |
| Phase C output | `tests/e2e/artifacts/phase-c-output.md` | YES |

**Pipeline Key:** `linear` (dynamic)
**Workflow ID:** `TEST-001-LINEAR` (semantic, good)
**Issue:** No workflow_id in artifact path

### TEST-002: Parallel Fan-Out/Fan-In

**Base Path:** `tests/e2e/artifacts/`

| Artifact | Current Path | Hardcoded? |
|----------|--------------|------------|
| Parallel 1 output | `tests/e2e/artifacts/parallel-1-output.md` | YES |
| Parallel 2 output | `tests/e2e/artifacts/parallel-2-output.md` | YES |
| Parallel 3 output | `tests/e2e/artifacts/parallel-3-output.md` | YES |
| Synthesis output | `tests/e2e/artifacts/synthesis-output.md` | YES |

**Pipeline Key:** `fanout` (dynamic)
**Workflow ID:** `TEST-002-PARALLEL` (semantic, good)
**Issue:** No workflow_id in artifact path

### TEST-003: Cross-Pollinated Pipeline

**Base Path:** `tests/e2e/artifacts/`

| Artifact | Current Path | Hardcoded? |
|----------|--------------|------------|
| Alpha Phase 1 | `tests/e2e/artifacts/alpha-phase1-output.md` | YES |
| Alpha Phase 2 | `tests/e2e/artifacts/alpha-phase2-output.md` | YES |
| Beta Phase 1 | `tests/e2e/artifacts/beta-phase1-output.md` | YES |
| Beta Phase 2 | `tests/e2e/artifacts/beta-phase2-output.md` | YES |
| Alpha to Beta | `tests/e2e/artifacts/crosspoll/alpha-to-beta.md` | YES |
| Beta to Alpha | `tests/e2e/artifacts/crosspoll/beta-to-alpha.md` | YES |

**Pipeline Keys:** `alpha`, `beta` (dynamic, good)
**Workflow ID:** `TEST-003-CROSSPOLL` (semantic, good)
**Issue:** No workflow_id in artifact path, cross-pollination path not standard

---

## 3. Pattern Summary

### What's Good (Keep)

| Aspect | Status | Notes |
|--------|--------|-------|
| Workflow IDs | Good | Semantic, descriptive |
| Pipeline Keys | Good | Dynamic, not hardcoded |
| Orchestration Patterns | Good | Validates SEQUENTIAL, PARALLEL, BARRIER_SYNC |
| Checkpoint Structure | Good | Proper checkpointing |
| Metrics Tracking | Good | Comprehensive metrics |

### What Needs Updating

| Aspect | Current | Target | Impact |
|--------|---------|--------|--------|
| Base Path | `tests/e2e/artifacts/` | `orchestration/{workflow_id}/` | All 3 tests |
| Pipeline Path | `artifacts/{name}.md` | `{pipeline_id}/{phase}/{artifact}.md` | All 3 tests |
| Cross-Poll Path | `artifacts/crosspoll/` | `cross-pollination/barrier-{n}/` | TEST-003 |
| Schema Fields | Missing | Add `short_alias`, `paths` section | All 3 tests |

---

## 4. Recommended Updates

### 4.1 Path Structure Changes

**Current (TEST-001):**
```
tests/e2e/artifacts/
├── phase-a-output.md
├── phase-b-output.md
└── phase-c-output.md
```

**Target (TEST-001):**
```
orchestration/TEST-001-LINEAR/
└── linear/
    ├── phase-1/phase-a-output.md
    ├── phase-2/phase-b-output.md
    └── phase-3/phase-c-output.md
```

**Current (TEST-003):**
```
tests/e2e/artifacts/
├── alpha-phase1-output.md
├── alpha-phase2-output.md
├── beta-phase1-output.md
├── beta-phase2-output.md
└── crosspoll/
    ├── alpha-to-beta.md
    └── beta-to-alpha.md
```

**Target (TEST-003):**
```
orchestration/TEST-003-CROSSPOLL/
├── alpha/
│   ├── phase-1/phase1-output.md
│   └── phase-2/phase2-output.md
├── beta/
│   ├── phase-1/phase1-output.md
│   └── phase-2/phase2-output.md
└── cross-pollination/
    └── barrier-1/
        ├── alpha-to-beta/handoff.md
        └── beta-to-alpha/handoff.md
```

### 4.2 Schema Updates Required

Add to each test workflow:

```yaml
pipelines:
  {key}:
    id: "{pipeline-id}"
    short_alias: "{alias}"     # NEW: 2-4 char alias for paths
    skill_source: "{skill}"    # NEW: Originating skill

paths:                         # NEW: Path configuration
  base: "orchestration/{workflow.id}/"
  pipeline: "{base}/{short_alias}/{phase}/"
  barrier: "{base}/cross-pollination/barrier-{n}/"
```

---

## 5. Test Usefulness Assessment

| Test | Pattern Value | Keep? | Action |
|------|---------------|-------|--------|
| TEST-001 | SEQUENTIAL validation | YES | Update paths |
| TEST-002 | PARALLEL validation | YES | Update paths |
| TEST-003 | BARRIER_SYNC validation | YES | Update paths |

**Verdict:** All tests are useful and should be UPDATED, not removed.

---

## 6. Migration Plan

1. **Phase 1: Update Test Workflows**
   - Add `short_alias` and `paths` fields to all test workflows
   - Update artifact paths to new structure
   - Keep workflow IDs as-is (they're already good)

2. **Phase 2: Migrate Test Artifacts**
   - Create new directory structure under `orchestration/`
   - Move existing artifacts to new locations
   - Update all path references

3. **Phase 3: Validate**
   - Run orchestration skill against updated tests
   - Verify artifact creation at correct paths
   - Verify cross-pollination works

---

## 7. Files Requiring Changes

| File | Change Type | Priority |
|------|-------------|----------|
| `tests/e2e/TEST-001-LINEAR-WORKFLOW.yaml` | Update paths | HIGH |
| `tests/e2e/TEST-002-PARALLEL-WORKFLOW.yaml` | Update paths | HIGH |
| `tests/e2e/TEST-003-CROSSPOLL-WORKFLOW.yaml` | Update paths | HIGH |
| `tests/e2e/artifacts/*` | Migrate to new location | HIGH |
| `skills/orchestration/templates/*.yaml` | Add path schema | HIGH |

---

*Document ID: ANL-SAO-021-001*
*Classification: ANALYSIS*
*Generated: 2026-01-10*
