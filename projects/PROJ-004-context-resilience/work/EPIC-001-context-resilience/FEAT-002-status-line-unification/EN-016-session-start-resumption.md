# EN-016: SessionStart compact|clear Resumption Context

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

Enhancement to the existing `HooksSessionStartHandler` (FEAT-001 EN-006) to detect compaction vs /clear from the context state file and inject appropriate resumption context.

Detection logic:
- If `pre_compaction_fill` present in state file AND session_id differs from stored → **compaction detected**
- If state file missing or no `pre_compaction_fill` → **session reset (/clear or new session)**

Injected XML (appended to `additionalContext`):
- Compaction: `<compaction-notice tier="CRITICAL" fill="0.89">Context was compacted at CRITICAL tier (89% fill). Review checkpoint at .jerry/checkpoints/. Resume from last orchestration state.</compaction-notice>`
- Reset: `<session-reset>New session started. No prior compaction state detected.</session-reset>`

---

## Acceptance Criteria

- [x] Reads `IContextStateStore` at session start
- [x] Detects compaction: `pre_compaction_fill` present + session_id mismatch
- [x] Injects `<compaction-notice>` XML with pre-compaction tier and fill
- [x] Injects `<session-reset>` XML when no compaction detected
- [x] Appended to `additionalContext` alongside existing project + quality context
- [x] Clears `pre_compaction_fill` from state after injection (one-time notification)
- [x] Fail-open: state read failure does not block session start
- [x] One class per file (H-10), type hints (H-11), docstrings (H-12)

---

## Dependencies

**Depends On:**
- EN-015 (pre-compact handler writes pre_compaction_fill to state)
- EN-011 (FilesystemContextStateStore — read source)
- EN-010 (ContextState schema)

**Enables:**
- ST-006 (session-start resumption context is the final layer of automatic rotation)

**File:**
- `src/interface/cli/hooks/hooks_session_start_handler.py` (enhanced)

---

## Technical Approach

The enhanced session-start hook detects compaction vs /clear by checking for pre_compaction_fill in the state file and comparing session IDs. On compaction, a compaction-notice XML element is injected with pre-compaction tier and fill, resumption guidance, and checkpoint location. On /clear or new session, a session-reset XML element is injected. The pre_compaction_fill is cleared after injection to ensure one-time notification, and fail-open error handling prevents state read failure from blocking session start.

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-21 | Claude | completed | Session-start handler enhanced with compaction/clear detection. Injects appropriate resumption XML. |
