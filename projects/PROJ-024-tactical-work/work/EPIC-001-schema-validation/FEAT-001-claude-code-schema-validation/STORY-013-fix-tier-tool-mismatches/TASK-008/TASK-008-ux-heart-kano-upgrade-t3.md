# TASK-008: Fix M-008 -- ux-heart-analyst + ux-kano-analyst Upgrade to T3

> **Type:** task
> **Status:** completed
> **Priority:** medium
> **Created:** 2026-03-28T00:00:00Z
> **Parent:** STORY-013

---

## Summary

Upgrade ux-heart-analyst and ux-kano-analyst to T4 with WebSearch/WebFetch.

---

## Description

Both agents are T2 while 7 of 10 UX peer agents are T3. Analysis (ux-web-access-analysis.md) confirmed both need web access:
- ux-heart-analyst: Step 1 of Threshold Fallback Methodology requires industry benchmarks it can't access at T2 (P-022 concern)
- ux-kano-analyst: Can't observe competitive dynamics needed for feature lifecycle assessment

**User Feedback:** Upgrade both to T3 with WebSearch, WebFetch, and Context7.

## Acceptance Criteria

- [ ] `skills/ux-heart-metrics/agents/ux-heart-analyst.md` tools includes `WebSearch, WebFetch`
- [ ] `skills/ux-heart-metrics/agents/ux-heart-analyst.md` includes `mcpServers: context7: true`
- [ ] `skills/ux-heart-metrics/agents/ux-heart-analyst.governance.yaml` updated: `tool_tier: T3`
- [ ] `skills/ux-kano-model/agents/ux-kano-analyst.md` tools includes `WebSearch, WebFetch`
- [ ] `skills/ux-kano-model/agents/ux-kano-analyst.md` includes `mcpServers: context7: true`
- [ ] `skills/ux-kano-model/agents/ux-kano-analyst.governance.yaml` updated: `tool_tier: T3`
- [ ] T3 citation guardrails added to both governance files
- [ ] `jerry agents validate-frontmatter` passes for both

## Files to Change

- `skills/ux-heart-metrics/agents/ux-heart-analyst.md`
- `skills/ux-heart-metrics/agents/ux-heart-analyst.governance.yaml`
- `skills/ux-kano-model/agents/ux-kano-analyst.md`
- `skills/ux-kano-model/agents/ux-kano-analyst.governance.yaml`
