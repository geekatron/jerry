# TASK-004: Fix M-004 -- nse-requirements Tier Resolution

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Created:** 2026-03-28T00:00:00Z
> **Completed:** 2026-03-29T00:30:00Z
> **Parent:** STORY-013

---

## Summary

Resolve nse-requirements tier mismatch where tool_tier T4 did not match actual capability set (Web+MK). Resolved by STORY-015/017/018 tier renumbering.

---

## Description

`nse-requirements` declares `tool_tier: T4` but has WebSearch + WebFetch (T3) + Memory-Keeper (T4) = effectively T5 capability without the Agent tool.

**User Feedback:** "I think we are missing a Tier or Two. Why wouldn't we want other agents to leverage Memory-Keeper?"

**Resolution:** Resolved by STORY-017/018 tier renumbering (ADR-STORY015-001 Option A). Under the Persistent-First Linear model, T4 (External) = T3 (Persistent/MK) + WebSearch + WebFetch + Context7. nse-requirements at `tool_tier: T4` with Web+MK is now an **exact fit** -- no tier change needed.

## Acceptance Criteria

- [x] STORY-015 completed with new tier model (ADR-STORY015-001 scored 0.950, Option A accepted)
- [x] `nse-requirements` governance `tool_tier: T4` -- correct under new model (T4 = Persistent + External = Web + MK)
- [x] Schema validation passes (nse-requirements.governance.yaml validates against agent-governance-v1.schema.json v1.1.0)

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Resolved By | STORY-015, STORY-017, STORY-018 | Tier renumbering made T4 the exact fit for Web+MK agents |
