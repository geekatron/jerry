# ST-006: Automatic Session Rotation

> **Type:** story
> **Status:** completed
> **Priority:** critical
> **Impact:** critical
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

Multi-hook graduated escalation system for automatic session rotation. Hooks cannot directly invoke /compact — orchestration is distributed across the hook lifecycle per DEC-003.

**Escalation layers:**

| Tier | Hook | Action |
|------|------|--------|
| WARNING | prompt-submit | Adds escalation notice to additionalContext |
| CRITICAL | prompt-submit | Adds urgent checkpoint warning to additionalContext |
| EMERGENCY | stop gate | Blocks stop decision, prompts user to /compact |
| Compaction fired | pre-compact | Saves pre-compaction state checkpoint |
| Session restarts | session-start | Detects compaction vs /clear, injects resumption context |

**Aggressiveness levels (configurable):**
- `conservative` — warn at WARNING, block at EMERGENCY
- `moderate` — warn at WARNING, escalate at CRITICAL, block at EMERGENCY
- `aggressive` — escalate at WARNING, block at CRITICAL and EMERGENCY

The only manual step is the user running /compact or /clear when prompted. All other rotation steps are automatic.

---

## Acceptance Criteria

- [x] prompt-submit hook reads state file, adds WARNING escalation notice at WARNING tier
- [x] prompt-submit hook adds CRITICAL urgent warning at CRITICAL tier
- [x] Stop hook blocks at EMERGENCY with actionable message (run /compact)
- [x] Pre-compact hook saves fill + tier to state before compaction
- [x] Session-start detects compaction, injects `<compaction-notice>` XML
- [x] Session-start detects /clear, injects `<session-reset>` XML
- [x] Configurable aggressiveness via Jerry config key
- [x] Full rotation cycle testable end-to-end

---

## Dependencies

**Depends On:**
- EN-012 (context estimate for fill/tier data)
- EN-014 (stop hook gate — EMERGENCY blocking)
- EN-015 (pre-compact state persistence)
- EN-016 (session-start resumption context)
- DEC-003 (multi-hook rotation architecture decision)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-21 | Claude | completed | Multi-hook rotation operational. All 5 layers implemented and tested. Configurable aggressiveness in place. |
