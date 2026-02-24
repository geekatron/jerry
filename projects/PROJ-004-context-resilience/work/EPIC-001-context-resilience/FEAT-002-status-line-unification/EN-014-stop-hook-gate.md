# EN-014: Stop Hook Gate (`context-stop-gate.py`)

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

Stop hook that gates Claude from stopping when context is at EMERGENCY tier. Reads `.jerry/local/context-state.json` directly (fast path — no subprocess), inspects current tier, returns Claude Code stop decision.

Response schema:
- `{"decision": "block", "reason": "Context at EMERGENCY tier (0.91 fill). Please run /compact before stopping."}` — at EMERGENCY
- `{"decision": "approve"}` — all other tiers or file missing (fail-open)

Fail-open: on any error (file missing, JSON corrupt, tier unknown), returns `approve` and logs to stderr.

---

## Acceptance Criteria

- [x] `hooks/context-stop-gate.py` thin wrapper calling `jerry hooks stop-gate`
- [x] `HooksStopGateHandler` reads state file, returns `decision: block` at EMERGENCY
- [x] Returns `decision: approve` when tier < EMERGENCY or state file missing
- [x] Reason message includes fill percentage and action guidance
- [x] Fail-open: always exits 0
- [x] Registered in `hooks/hooks.json` for Stop event
- [x] One class per file (H-10), type hints (H-11), docstrings (H-12)

---

## Dependencies

**Depends On:**
- EN-011 (FilesystemContextStateStore — state file location)
- EN-013 (bootstrap wires handler; parser registers `hooks stop-gate`)
- EN-012 (ContextEstimateService — state schema)

**Enables:**
- ST-006 (automatic session rotation — stop gate is one layer of the multi-hook orchestration)

**Files:**
- `src/interface/cli/hooks/hooks_stop_gate_handler.py`
- `hooks/context-stop-gate.py`

---

## Technical Approach

A thin wrapper hook in hooks/context-stop-gate.py calls jerry hooks stop-gate. The handler reads fill state from IContextStateStore via direct file access (fast path without subprocess overhead), returns decision: block at EMERGENCY tier with reason message including fill percentage and action guidance, and approves all other tiers or missing state file. The fail-open design ensures errors log to stderr but always exit 0.

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-21 | Claude | completed | Stop hook gate implemented. Blocks at EMERGENCY, approves otherwise, fail-open. |
