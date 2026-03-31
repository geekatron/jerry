# TASK-010: Add output path MEDIUM standard to agent-development-standards.md

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-03-31
> **Parent:** BUG-006
> **Depends On:** TASK-006, TASK-007, TASK-008

---

## Summary

Add a new MEDIUM standard (AD-M-011) to `agent-development-standards.md` requiring all agent output paths to use `projects/${JERRY_PROJECT}/` prefix, never `skills/*/output/`.

## Acceptance Criteria

- [ ] New standard AD-M-011 added to the Agent Structure Standards table
- [ ] Standard references the `/problem-solving` pattern as the canonical reference
- [ ] Standard specifies the `projects/${JERRY_PROJECT}/engagements/` pattern for engagement-based skills
- [ ] AE-002 auto-escalation applies (touches `.context/rules/`)
