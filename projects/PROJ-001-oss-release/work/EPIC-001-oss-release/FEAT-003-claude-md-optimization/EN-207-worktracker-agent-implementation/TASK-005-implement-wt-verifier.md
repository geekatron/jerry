# TASK-005: Implement wt-verifier Agent

> **Type:** task
> **Status:** completed
> **Priority:** critical
> **Created:** 2026-02-02T12:00:00Z
> **Completed:** 2026-02-02T17:30:00Z
> **Parent:** EN-207
> **Owner:** Claude
> **Effort:** 3

---

## Summary

Implement the wt-verifier agent that validates work item acceptance criteria before closure. Enforces WTI-002 (No Closure Without Verification) and WTI-006 (Evidence-Based Closure).

## Acceptance Criteria

- [x] Agent file created at `skills/worktracker/agents/wt-verifier.md`
- [x] YAML frontmatter with identity, persona, capabilities sections
- [x] P-003 compliance (forbidden_actions includes subagent spawning)
- [x] P-002 compliance (mandatory file output)
- [x] WTI-002, WTI-003, WTI-006 enforcement documented
- [x] Invocation pattern with Task tool example
- [x] Output schema with verification_result structure
- [x] Usage examples covering pass, fail, and edge cases

## Evidence

- Agent file exists at `skills/worktracker/agents/wt-verifier.md`
- 726 lines of comprehensive documentation
- QG-1 review passed (0.95 P-003 compliance, 0.95 P-002 compliance)

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-02T12:00:00Z | pending | Task created |
| 2026-02-02T14:00:00Z | in_progress | Implementation started |
| 2026-02-02T17:30:00Z | completed | Agent implemented and reviewed |
