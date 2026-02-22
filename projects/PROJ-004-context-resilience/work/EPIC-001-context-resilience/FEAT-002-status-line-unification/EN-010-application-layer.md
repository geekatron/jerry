# EN-010: Application Port (IContextStateStore) + ContextEstimateService

> **Type:** enabler
> **Status:** completed
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** architecture
> **Created:** 2026-02-21
> **Due:** --
> **Completed:** 2026-02-21
> **Parent:** FEAT-002
> **Owner:** --
> **Effort:** 2-3h

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Technical scope |
| [Acceptance Criteria](#acceptance-criteria) | Checklist |
| [Dependencies](#dependencies) | Relationships |
| [Technical Approach](#technical-approach) | Implementation strategy |
| [History](#history) | Status changes |

---

## Summary

Application layer for context estimation pipeline:

- `IContextStateStore` protocol — port for reading/writing cross-invocation context state (last_fill, last_tier, pre_compaction_fill, session_id)
- `ContextState` dataclass — state schema persisted between CLI invocations
- `ContextEstimateService` — orchestrates the estimation pipeline: parse stdin → compute estimate → detect compaction → determine rotation action → persist state to store
- `EstimateResult` — application-level result combining ContextEstimate + CompactionResult for CLI output

`IContextStateStore` allows test doubles and alternative backends (filesystem, memory) without changing service logic.

---

## Acceptance Criteria

- [x] `IContextStateStore` protocol with `load()` and `save(state: ContextState)` methods
- [x] `ContextState` dataclass: session_id, last_fill, last_tier, pre_compaction_fill, timestamp
- [x] `ContextEstimateService.estimate(raw_json: dict) -> EstimateResult`
- [x] Service orchestrates: parse → ContextEstimateComputer → compaction detection → RotationAction → store.save()
- [x] Compaction detection: pre_compaction_fill present in state AND current session_id differs from stored session_id
- [x] No infrastructure imports in application layer (H-08)
- [x] One class per file (H-10)
- [x] Type hints and docstrings (H-11, H-12)
- [x] Unit tests with InMemory store double

---

## Dependencies

**Depends On:**
- EN-009 (domain VOs and ContextEstimateComputer)

**Enables:**
- EN-011 (FilesystemContextStateStore implements IContextStateStore)
- EN-012 (CLI handler calls ContextEstimateService)
- EN-013 (bootstrap wires concrete store into service)

**Files:**
- `src/context_monitoring/application/ports/context_state_store.py`
- `src/context_monitoring/application/ports/context_state.py`
- `src/context_monitoring/application/services/context_estimate_service.py`
- `src/context_monitoring/application/services/estimate_result.py`

---

## Technical Approach

IContextStateStore protocol defines the port for load/save of cross-invocation state persistence, decoupling the application service from infrastructure. ContextEstimateService orchestrates the pipeline: parse stdin JSON, compute estimate via domain service, detect compaction by comparing current vs. stored fill state, determine rotation action, and persist state via the port. This single entry point serves both CLI and hook consumers.

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-21 | Claude | completed | IContextStateStore port, ContextState, ContextEstimateService, EstimateResult implemented and tested. |
