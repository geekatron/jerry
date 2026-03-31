# TASK-007: red-team path remediation

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-03-31
> **Parent:** BUG-006

---

## Summary

Replace all `skills/red-team/output/{engagement-id}/` paths with `projects/${JERRY_PROJECT}/engagements/{engagement-id}/` across 25 config files.

## Files to Update

| Category | Count | Files |
|----------|-------|-------|
| SKILL.md | 1 | Lines 106-116, 188, 274, 521-528, 535 |
| Agent governance | 11 | `skills/red-team/agents/red-*.governance.yaml` — `output.location` field |
| Agent composition | 11 | `skills/red-team/composition/red-*.agent.yaml` — `output.location` field |
| Templates | 2 | `pentest-engagement.md` (Lines 151, 189-192), `engagement-playbook.md` (Line 81) |

## Acceptance Criteria

- [ ] Zero `grep -r 'skills/red-team/output' skills/red-team/` matches in config files
- [ ] All governance YAML files pass schema validation
- [ ] New paths use `projects/${JERRY_PROJECT}/engagements/` pattern
