# FEAT-002:DEC-004: Sub-Agent Tracking via Transcript Parsing + Lifecycle Hooks

> **Type:** decision
> **Status:** accepted
> **Priority:** high
> **Created:** 2026-02-21
> **Completed:** 2026-02-21
> **Parent:** FEAT-002
> **Owner:** --
> **Related:** DEC-002, DEC-003

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Decision overview |
| [Decision Context](#decision-context) | Background and constraints |
| [Decision](#decision) | Choice made and rationale |
| [Sub-decisions](#sub-decisions) | Detailed sub-decisions D-007 through D-015 |
| [Decision Summary](#decision-summary) | Quick reference |
| [Related Artifacts](#related-artifacts) | Traceability |
| [Document History](#document-history) | Change log |

---

## Summary

Sub-agents are session-scoped with accessible JSONL transcripts. Jerry computes per-agent context fill from cumulative usage data (last entry = current state). Two-layer approach: lifecycle hooks (SubagentStop) for fast agent counts and transcript locations, transcript parsing for detailed per-agent fill computation.

---

## Decision Context

### Background

FEAT-002 requires sub-agent context fill to be visible in jerry-statusline. Three options were considered: (A) state file written by sub-agent hooks, (B) transcript parsing from JSONL files, (C) Claude Code API for agent usage (not available).

### Constraints

- Claude Code provides SubagentStop but not SubagentStart
- Sub-agent transcripts are JSONL files accessible on the filesystem
- Cumulative usage in transcript: last entry's `message.usage` field = current cumulative state
- Context windows vary by model/subscription — NEVER hardcode window sizes (D-015)

---

## Decision

**We decided:** Two-layer tracking:
1. `SubagentStop` lifecycle hook records agent_id + transcript_path to `.jerry/local/subagent-lifecycle.json`
2. `TranscriptSubAgentReader` parses last 8KB of each agent's JSONL for cumulative usage

**Rationale:** Lifecycle hooks are lightweight (fast path for counts). Transcript parsing provides accurate fill data without requiring Claude Code API changes. JSONL transcripts are always accessible and contain cumulative usage.

---

## Sub-decisions

| ID | Decision |
|----|----------|
| D-007 | Fail-open design: missing/corrupt agent transcript → agent skipped, not error |
| D-010 | Stop gate triggers at EMERGENCY only (not CRITICAL) — avoid blocking at non-critical levels |
| D-013 | Full Claude Code JSON passthrough in `session` block of estimate response |
| D-014 | Sub-agent tracking via two-layer approach (lifecycle hooks + transcript parsing) |
| D-015 | NEVER hardcode context window sizes — always read from Claude Code stdin `context_window` field |

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-004 | Sub-agent tracking via SubagentStop lifecycle hooks + JSONL transcript parsing | 2026-02-21 | Accepted |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-002](./FEAT-002-status-line-unification.md) | Parent feature |
| Related | [EN-017](./EN-017-subagent-lifecycle-hooks.md) | SubagentStop lifecycle hook |
| Related | [EN-018](./EN-018-sub-agent-transcript-parser.md) | Transcript parser adapter |
| Research | SPIKE-003 OQ-9 | Correct JSONL field path (`message.usage`) found during validation |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-21 | Claude | Created. Sub-agent tracking approach accepted. D-007 through D-015 sub-decisions captured. |

---

## Metadata

```yaml
id: "FEAT-002:DEC-004"
parent_id: "FEAT-002"
work_type: DECISION
title: "Sub-Agent Tracking via Transcript Parsing + Lifecycle Hooks"
status: ACCEPTED
priority: HIGH
created_by: "Claude"
created_at: "2026-02-21"
decided_at: "2026-02-21"
```
