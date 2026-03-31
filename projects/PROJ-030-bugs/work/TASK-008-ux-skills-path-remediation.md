# TASK-008: UX skills path remediation — 11 sub-skills

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-03-31
> **Parent:** BUG-006

---

## Summary

Replace all `skills/ux-*/output/{engagement-id}/` and `skills/user-experience/output/{engagement-id}/` paths with `projects/${JERRY_PROJECT}/engagements/{engagement-id}/` across 60 config files in 11 sub-skills.

Full line-level audit: [`BUG-006-ux-audit-detail.md`](BUG-006-ux-audit-detail.md)

## Files Per Sub-Skill

| Sub-Skill | Files |
|-----------|-------|
| user-experience (parent) | 7 |
| ux-heuristic-eval | 5 |
| ux-jtbd | 5 |
| ux-lean-ux | 7 |
| ux-heart-metrics | 3 |
| ux-kano-model | 6 |
| ux-atomic-design | 6 |
| ux-inclusive-design | 7 |
| ux-behavior-design | 5 |
| ux-design-sprint | 4 |
| ux-ai-first-design | 5 |
| **Total** | **60** |

## Acceptance Criteria

- [ ] Zero `grep -rl 'skills/ux-.*output\|skills/user-experience.*output' skills/ux-*/ skills/user-experience/` matches
- [ ] All governance YAML files pass schema validation
- [ ] New paths use `projects/${JERRY_PROJECT}/engagements/` pattern
- [ ] UX wave signoff files use `projects/${JERRY_PROJECT}/engagements/{engagement-id}/wave-signoff-{wave-N}.md`
