# EN-018: Sub-Agent Transcript Parser (ISubAgentReader + TranscriptSubAgentReader)

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
> **Effort:** 2h

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

Port and adapter pair for reading per-agent context usage from JSONL transcripts:

- `ISubAgentReader` protocol — port in application layer; `read_agents() -> list[SubAgentInfo]`
- `TranscriptSubAgentReader` adapter — reads `.jerry/local/subagent-lifecycle.json`, then for each agent parses the last 8KB of its JSONL transcript to extract cumulative usage (three-field sum: `input_tokens + output_tokens + cache_read_input_tokens + cache_creation_input_tokens`)

JSONL usage path: `message.usage` nested field (corrected from SPIKE-003 OQ-9 finding — wrong field path was the original implementation error). Last entry in transcript = current cumulative usage state.

Fail-open per DEC-004 D-007: missing transcript, unreadable file, or parse error → agent skipped with `fill=0`.

---

## Acceptance Criteria

- [x] `ISubAgentReader` protocol in application ports layer
- [x] `TranscriptSubAgentReader` implements `ISubAgentReader`
- [x] Reads lifecycle JSON from `.jerry/local/subagent-lifecycle.json`
- [x] For each agent: reads last 8KB of JSONL transcript (file tail)
- [x] Extracts cumulative usage from `message.usage` path (four-field sum)
- [x] Returns `SubAgentInfo` list with agent_id and fill ratio per agent
- [x] Fail-open: missing/corrupt transcript → agent skipped (not error)
- [x] No domain imports from other bounded contexts (H-08)
- [x] One class per file (H-10), type hints (H-11), docstrings (H-12)
- [x] Unit tests with fixture JSONL transcripts

---

## Dependencies

**Depends On:**
- EN-009 (SubAgentInfo VO)
- EN-017 (lifecycle file populated by SubagentStop hook)
- SPIKE-003 OQ-9 finding (correct JSONL field path: `message.usage`, not top-level)

**Enables:**
- EN-013 (bootstrap wires TranscriptSubAgentReader into ContextEstimateService)
- ST-005 (jerry-statusline displays sub-agent fills from JSON response)

**Files:**
- `src/context_monitoring/application/ports/sub_agent_reader.py`
- `src/context_monitoring/infrastructure/adapters/transcript_sub_agent_reader.py`

---

## Technical Approach

ISubAgentReader port decouples the domain from transcript parsing. TranscriptSubAgentReader adapter reads .jerry/local/subagent-lifecycle.json to locate agent JSONL files, then for each agent reads the last 8KB of its JSONL transcript to extract the cumulative usage from the message.usage nested field (four-field sum: input_tokens + output_tokens + cache_read_input_tokens + cache_creation_input_tokens). Results are cached with configurable TTL for status line performance. Fail-open design skips agents with missing or unreadable transcripts rather than erroring.

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-21 | Claude | completed | ISubAgentReader port and TranscriptSubAgentReader adapter implemented. Corrected JSONL field path per SPIKE-003 OQ-9 finding. |
