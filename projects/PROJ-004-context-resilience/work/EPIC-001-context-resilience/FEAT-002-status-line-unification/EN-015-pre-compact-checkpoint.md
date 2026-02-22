# EN-015: PreCompact Hook State Persistence

> **Type:** enabler
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-21
> **Due:** --
> **Completed:** 2026-02-21
> **Parent:** FEAT-002
> **Owner:** --
> **Effort:** 1h

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

Enhancement to the existing `HooksPreCompactHandler` (created in FEAT-001 EN-006) to save pre-compaction context state before compaction fires. This enables the session-start handler to detect compaction vs /clear on the next session.

State saved to `IContextStateStore`:
- `pre_compaction_fill` — context fill at time of compaction (from current state)
- `pre_compaction_tier` — tier classification at compaction time
- `session_id` — current session identifier

When the next session starts, if `pre_compaction_fill` is present in the state file and the session_id differs, compaction is detected (not /clear).

---

## Acceptance Criteria

- [x] `HooksPreCompactHandler` reads current state from `IContextStateStore`
- [x] Writes `pre_compaction_fill`, `pre_compaction_tier`, `session_id` before compaction fires
- [x] State persisted atomically (via FilesystemContextStateStore)
- [x] Existing checkpoint behavior (CheckpointService, session abandon) preserved
- [x] Fail-open: pre-compaction state save failure does not block compaction
- [x] One class per file (H-10), type hints (H-11), docstrings (H-12)

---

## Dependencies

**Depends On:**
- EN-011 (FilesystemContextStateStore — write destination)
- EN-010 (ContextState schema with pre_compaction_fill field)
- EN-003 (CheckpointService — existing pre-compact behavior preserved)

**Enables:**
- EN-016 (session-start detects compaction via pre_compaction_fill in state)
- ST-006 (compaction detection is one layer of automatic rotation)

**File:**
- `src/interface/cli/hooks/hooks_pre_compact_handler.py` (enhanced)

---

## Technical Approach

The PreCompact hook handler reads current context state from IContextStateStore and writes pre_compaction_fill, pre_compaction_tier, and session_id before compaction fires. This enables the session-start handler on the next session to detect compaction vs /clear by checking if pre_compaction_fill is present and the session_id differs. State persistence is fail-open: pre-compaction state save failure does not block compaction, and existing checkpoint behavior is preserved.

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-21 | Claude | completed | PreCompact handler enhanced to persist pre-compaction state. Compaction detection chain complete. |
