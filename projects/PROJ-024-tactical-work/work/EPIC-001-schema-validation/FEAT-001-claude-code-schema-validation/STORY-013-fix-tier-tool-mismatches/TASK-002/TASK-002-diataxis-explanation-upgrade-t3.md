# TASK-002: Fix M-002 -- diataxis-explanation Upgrade to T3

> **Type:** task
> **Status:** completed
> **Priority:** medium
> **Created:** 2026-03-28T00:00:00Z
> **Parent:** STORY-013

---

## Summary

Upgrade diataxis-explanation to T4 with WebSearch/WebFetch.

---

## Description

`diataxis-explanation` has `cognitive_mode: divergent` but `tool_tier: T2`. agent-development-standards.md maps divergent mode to T3+ ("Needs breadth; premature convergence misses sources").

**User Feedback:** Upgrade to T3.

## Acceptance Criteria

- [ ] `skills/diataxis/agents/diataxis-explanation.md` frontmatter `tools` includes `WebSearch, WebFetch`
- [ ] `skills/diataxis/agents/diataxis-explanation.md` frontmatter includes `mcpServers: context7: true`
- [ ] `skills/diataxis/agents/diataxis-explanation.governance.yaml` updated: `tool_tier: T3`
- [ ] T3 citation guardrails added to governance `guardrails.output_filtering`
- [ ] `jerry agents validate-frontmatter --agent diataxis-explanation` passes

## Files to Change

- `skills/diataxis/agents/diataxis-explanation.md`
- `skills/diataxis/agents/diataxis-explanation.governance.yaml`
