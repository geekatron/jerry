# TASK-003: Fix M-003 -- ux-behavior-diagnostician Governance T2->T3

> **Type:** task
> **Status:** completed
> **Priority:** medium
> **Created:** 2026-03-28T00:00:00Z
> **Parent:** STORY-013

---

## Summary

Correct ux-behavior-diagnostician governance to T2 (frontmatter already T2).

---

## Description

`ux-behavior-diagnostician` declares `tool_tier: T2` in governance but frontmatter already has `WebSearch, WebFetch` (T3-level tools). Governance doesn't match reality.

**User Feedback:** Correct.

## Acceptance Criteria

- [ ] `skills/ux-behavior-design/agents/ux-behavior-diagnostician.governance.yaml` updated: `tool_tier: T3`
- [ ] `jerry agents validate-frontmatter --agent ux-behavior-diagnostician` passes

## Files to Change

- `skills/ux-behavior-design/agents/ux-behavior-diagnostician.governance.yaml`
