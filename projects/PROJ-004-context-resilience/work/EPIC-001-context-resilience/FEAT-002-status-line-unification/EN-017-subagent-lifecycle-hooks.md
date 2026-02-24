# EN-017: Sub-Agent Lifecycle Hooks (SubagentStop)

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

`HooksSubagentStopHandler` records agent completion events to `.jerry/local/subagent-lifecycle.json`. Claude Code only provides `SubagentStop` (not `SubagentStart`) — agent start time is not available from the API.

Lifecycle record schema per agent:
```json
{
  "agent_id": "abc123",
  "transcript_path": "/path/to/agent.jsonl",
  "stopped_at": "2026-02-21T10:30:00Z"
}
```

The lifecycle file enables `TranscriptSubAgentReader` (EN-018) to locate agent transcripts for per-agent context fill computation. Always returns `{"decision": "approve"}` (stop hooks cannot block agent completion).

---

## Acceptance Criteria

- [x] `hooks/subagent-stop.py` thin wrapper calling `jerry hooks subagent-stop`
- [x] `HooksSubagentStopHandler` appends agent record to `.jerry/local/subagent-lifecycle.json`
- [x] Record includes: agent_id, transcript_path (from stdin payload), stopped_at (ISO 8601)
- [x] Atomic append (read → append → write) or JSONL append
- [x] Always returns `{"decision": "approve"}` (fail-open, cannot block)
- [x] Registered in `hooks/hooks.json` for SubagentStop event
- [x] One class per file (H-10), type hints (H-11), docstrings (H-12)

---

## Dependencies

**Depends On:**
- EN-013 (bootstrap registers `hooks subagent-stop` in parser and adapter)

**Enables:**
- EN-018 (TranscriptSubAgentReader reads lifecycle JSON to find agent transcripts)

**Files:**
- `src/interface/cli/hooks/hooks_subagent_stop_handler.py`
- `hooks/subagent-stop.py`

---

## Technical Approach

The SubagentStop hook handler parses agent_id and transcript_path from the Claude Code hook payload and appends agent lifecycle records to .jerry/local/subagent-lifecycle.json. Each record captures agent_id, transcript_path, and stopped_at timestamp (ISO 8601). The lifecycle file enables TranscriptSubAgentReader to locate agent transcripts for per-agent context fill computation. Always returns decision: approve (fail-open), as stop hooks cannot block agent completion.

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-21 | Claude | completed | SubagentStop lifecycle hook implemented. Records agent_id + transcript_path to lifecycle file. |
