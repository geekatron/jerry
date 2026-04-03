# TASK-007: Fix M-007 -- 6 UX Worker Agents Add disallowedTools: Agent

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Created:** 2026-03-28T00:00:00Z
> **Parent:** STORY-013

---

## Summary

Add disallowedTools: [Agent] to 6 UX worker agents (expanded to 10 + orchestrator in M-007).

---

## Description

H-35 says worker agents must not have the Agent tool. These 6 UX agents don't explicitly disallow it -- they inherit all tools from parent by not declaring `tools` or `disallowedTools`.

**User Feedback:** Add `disallowedTools`.

## Agents to Fix

1. `skills/ux-ai-first-design/agents/ux-ai-design-guide.md`
2. `skills/ux-atomic-design/agents/ux-atomic-architect.md`
3. `skills/ux-design-sprint/agents/ux-sprint-facilitator.md`
4. `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md`
5. `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md`
6. `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md`

## Acceptance Criteria

- [ ] All 6 agents have `disallowedTools: Agent` in frontmatter
- [ ] `jerry agents validate-frontmatter` passes for all 6
- [ ] Grep confirms no UX worker agent has Agent tool available

## Files to Change

- 6 agent `.md` files listed above
