# TASK-006: eng-team path remediation

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-03-31
> **Parent:** BUG-006

---

## Summary

Replace all `skills/eng-team/output/{engagement-id}/` paths with `projects/${JERRY_PROJECT}/engagements/{engagement-id}/` across 22 config files.

## Files to Update

| Category | Count | Files |
|----------|-------|-------|
| SKILL.md | 1 | Lines 119-128, 261-273 |
| Agent governance | 10 | `skills/eng-team/agents/eng-*.governance.yaml` — `output.location` field |
| Agent composition | 10 | `skills/eng-team/composition/eng-*.agent.yaml` — `output.location` field |
| Templates | 1 | `skills/eng-team/templates/engagement-playbook.md` — Line 189 |

## Acceptance Criteria

- [ ] Zero `grep -r 'skills/eng-team/output' skills/eng-team/` matches in config files
- [ ] All governance YAML files pass schema validation
- [ ] New paths use `projects/${JERRY_PROJECT}/engagements/` pattern
