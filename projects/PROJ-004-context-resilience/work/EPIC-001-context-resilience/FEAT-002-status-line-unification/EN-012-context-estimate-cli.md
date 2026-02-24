# EN-012: `jerry context estimate` CLI Command

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
> **Effort:** 1-2h

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

CLI handler implementing `jerry context estimate`. Reads Claude Code JSON from stdin (UserPromptSubmit payload or direct invocation), runs domain estimation pipeline via `ContextEstimateService`, outputs structured JSON response.

Output schema:
```json
{
  "fill": 0.73,
  "tier": "WARNING",
  "rotation_action": "WARN",
  "compaction_detected": false,
  "session": { ...full Claude Code JSON passthrough... },
  "sub_agents": [ { "agent_id": "...", "fill": 0.45 } ],
  "thresholds": { "nominal": 0.60, "low": 0.70, "warning": 0.80, "critical": 0.88, "emergency": 0.88 }
}
```

Full passthrough of Claude Code JSON in `session` block enables consumers (jerry-statusline) to access raw data without re-parsing. Fail-open design: always exits 0; on error returns `{"fill": 0, "tier": "NOMINAL", "error": "..."}`.

---

## Acceptance Criteria

- [x] Reads JSON from stdin (Claude Code hook payload or direct pipe)
- [x] Calls `ContextEstimateService.estimate()` with parsed JSON
- [x] Returns structured JSON to stdout with fill, tier, rotation_action, compaction_detected, sub_agents, thresholds
- [x] Full Claude Code JSON passed through in `session` block (DEC-002 compliance)
- [x] Always exits 0 (fail-open)
- [x] On error: returns minimal valid JSON with error field
- [x] `--json` flag follows existing CLI pattern
- [x] One class per file (H-10), type hints (H-11), docstrings (H-12)

---

## Dependencies

**Depends On:**
- EN-010 (ContextEstimateService)
- EN-013 (bootstrap wires handler; parser registers `context estimate` subcommand)

**Enables:**
- ST-005 (jerry-statusline calls this command)
- ST-006 (prompt-submit reads output for escalation)

**Files:**
- `src/interface/cli/context/context_estimate_handler.py`
- `src/interface/cli/context/__init__.py`

---

## Technical Approach

The CLI handler reads Claude Code JSON from stdin, delegates to ContextEstimateService for domain computation, and outputs structured JSON to stdout. A complete session passthrough block includes all Claude Code fields alongside domain-computed context data, allowing consumers to access raw data without re-parsing. The fail-open design always exits 0, producing degraded JSON on error rather than failing the pipeline.

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-21 | Claude | completed | ContextEstimateHandler implemented. Fail-open, full session passthrough, structured JSON output. |
