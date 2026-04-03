# TASK-006: Fix M-006 -- pm-pmm SKILL.md Add allowed-tools

> **Type:** task
> **Status:** completed
> **Priority:** medium
> **Created:** 2026-03-28T00:00:00Z
> **Parent:** STORY-013

---

## Summary

Add allowed-tools field to pm-pmm SKILL.md.

---

## Description

`skills/pm-pmm/SKILL.md` has no `allowed-tools` field. All 5 pm agents have WebSearch/WebFetch in their frontmatter but the skill doesn't grant auto-approval.

**User Feedback:** Correct.

## Acceptance Criteria

- [ ] `skills/pm-pmm/SKILL.md` has `allowed-tools` field matching agent tool union
- [ ] `jerry agents validate-frontmatter --skill pm-pmm` passes

## Files to Change

- `skills/pm-pmm/SKILL.md`
