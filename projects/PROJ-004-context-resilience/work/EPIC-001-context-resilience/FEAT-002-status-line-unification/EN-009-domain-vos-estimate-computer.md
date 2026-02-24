# EN-009: Domain VOs + ContextEstimateComputer Service

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

5 frozen dataclass value objects and 1 pure domain service for the context estimate pipeline:

- `ContextUsageInput` — raw token counts from Claude Code stdin (input_tokens, output_tokens, cache_read_input_tokens, cache_creation_input_tokens, context_window)
- `ContextEstimate` — computed fill ratio, tier classification, thresholds
- `CompactionResult` — compaction detection state (detected flag, pre-compaction tier, session_id)
- `RotationAction` — enum (NONE, WARN, CHECKPOINT, BLOCK)
- `SubAgentInfo` — per-agent context fill data (agent_id, fill, transcript_path)
- `ContextEstimateComputer` — pure domain service: fill computation from exact current_usage, 5-tier classification, compaction detection, rotation action determination

No external dependencies. All pure domain logic.

---

## Acceptance Criteria

- [x] 5 frozen dataclasses with type hints and docstrings (H-11, H-12)
- [x] `ContextEstimateComputer.compute()` takes `ContextUsageInput`, returns `ContextEstimate`
- [x] Fill = (input_tokens + output_tokens + cache_read + cache_creation) / context_window
- [x] 5-tier classification: NOMINAL (<0.60), LOW (<0.70), WARNING (<0.80), CRITICAL (<0.88), EMERGENCY (>=0.88)
- [x] `RotationAction` determined from tier (WARN at WARNING, CHECKPOINT at CRITICAL, BLOCK at EMERGENCY)
- [x] No infrastructure imports in domain layer (H-07)
- [x] One class per file (H-10)
- [x] Unit tests for all compute paths

---

## Dependencies

**Depends On:**
- EN-003 (context_monitoring BC foundation — directory structure, `__init__.py` files)

**Enables:**
- EN-010 (application layer consumes these VOs)
- EN-012 (CLI handler uses ContextEstimate output)

**Files:**
- `src/context_monitoring/domain/value_objects/context_usage_input.py`
- `src/context_monitoring/domain/value_objects/context_estimate.py`
- `src/context_monitoring/domain/value_objects/compaction_result.py`
- `src/context_monitoring/domain/value_objects/rotation_action.py`
- `src/context_monitoring/domain/value_objects/sub_agent_info.py`
- `src/context_monitoring/domain/services/context_estimate_computer.py`

---

## Technical Approach

Five frozen dataclasses serve as value objects, encapsulating the domain model of context estimation. ContextEstimateComputer is a pure domain service with no I/O or external dependencies, computing fill ratio from exact token counts, classifying into 5-tier ThresholdTier, detecting compaction via token drop analysis, and determining rotation action from tier and aggressiveness configuration.

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-21 | Claude | completed | Domain VOs and ContextEstimateComputer implemented and tested. |
