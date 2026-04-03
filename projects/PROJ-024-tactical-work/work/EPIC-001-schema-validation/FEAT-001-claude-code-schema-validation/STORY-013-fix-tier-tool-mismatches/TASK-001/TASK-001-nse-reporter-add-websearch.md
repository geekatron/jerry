# TASK-001: Fix M-001 -- nse-reporter Add WebSearch

> **Type:** task
> **Status:** completed
> **Priority:** medium
> **Created:** 2026-03-28T00:00:00Z
> **Parent:** STORY-013

---

## Summary

Add WebSearch to nse-reporter frontmatter tools for T4 compliance.

---

## Description

`nse-reporter` governance declares `tool_tier: T3` but frontmatter has `WebFetch` without `WebSearch`. Incomplete T3 implementation.

**User Feedback:** Correct.

## Acceptance Criteria

- [ ] `skills/nasa-se/agents/nse-reporter.md` frontmatter `tools` includes `WebSearch`
- [ ] `jerry agents validate-frontmatter --agent nse-reporter` passes

## Files to Change

- `skills/nasa-se/agents/nse-reporter.md` -- add `WebSearch` to tools
