# ST-005: jerry-statusline Phase 1 Integration

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-21
> **Due:** --
> **Completed:** 2026-02-21
> **Parent:** FEAT-002
> **Owner:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | User story and scope |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Dependencies](#dependencies) | Relationships |
| [History](#history) | Status changes |

---

## Summary

jerry-statusline v3.0 calls `jerry context estimate` to get context fill data, compaction status, and sub-agent information. Uses the response to render context, compaction, and sub-agent segments. Falls back to standalone mode (direct transcript parsing) if `jerry context estimate` is unavailable or times out.

Key additions to `statusline.py` (external repo at `github.com/geekatron/jerry-statusline (external repo),`):

- `try_jerry_estimate()` — subprocess call to `jerry context estimate`, parses JSON response, returns None on failure (triggers fallback)
- `build_sub_agents_segment()` — renders per-agent context fill pills from `sub_agents` list
- `_jerry_tier_to_color()` — maps Jerry tier strings to statusline color codes using `thresholds` block

---

## Acceptance Criteria

- [x] `try_jerry_estimate()` calls `jerry context estimate` with 2s timeout
- [x] Returns parsed JSON response on success, None on timeout/error (fail-open)
- [x] Context segment uses Jerry's `fill` and `tier` when available
- [x] Compaction segment shown when `compaction_detected: true`
- [x] Sub-agents segment shown when `sub_agents` list non-empty
- [x] `_jerry_tier_to_color()` maps NOMINAL/LOW→green, WARNING→yellow, CRITICAL/EMERGENCY→red
- [x] Falls back to standalone mode when Jerry unavailable (no Jerry install, wrong directory, etc.)
- [x] Statusline refresh < 200ms additional latency from Jerry call (p50=96ms confirmed by SPIKE-004)

---

## Dependencies

**Depends On:**
- EN-012 (`jerry context estimate` CLI command)
- ST-004 (thresholds block in JSON response)
- SPIKE-004 (latency confirmed within budget)

**File:**
- `github.com/geekatron/jerry-statusline (external repo),statusline.py` (external repo)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-21 | Claude | completed | jerry-statusline v3.0 complete. try_jerry_estimate(), build_sub_agents_segment(), _jerry_tier_to_color() implemented. Fallback mode verified. |
