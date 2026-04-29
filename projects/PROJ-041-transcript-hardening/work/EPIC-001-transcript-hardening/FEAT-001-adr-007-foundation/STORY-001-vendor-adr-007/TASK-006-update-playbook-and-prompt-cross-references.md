# TASK-006: Update PLAYBOOK.md and ts-formatter.prompt.md cross-references

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-001
> **Owner:** eng-lead

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Update every ADR-007 cross-reference in `skills/transcript/PLAYBOOK.md` and `skills/transcript/agents/ts-formatter.prompt.md` to use the new `docs/adrs/` path. Completes the SKILL.md+ts-formatter.md cross-reference cleanup begun in TASK-004 and TASK-005.

---

## Acceptance Criteria

- [ ] All ADR-007 references in PLAYBOOK.md and ts-formatter.prompt.md use the new `docs/adrs/` path
- [ ] `grep -r "transcript-skill/work/EPIC-001-transcript-skill" skills/transcript/` returns zero matches
- [ ] Updated references resolve to the actually existing file
