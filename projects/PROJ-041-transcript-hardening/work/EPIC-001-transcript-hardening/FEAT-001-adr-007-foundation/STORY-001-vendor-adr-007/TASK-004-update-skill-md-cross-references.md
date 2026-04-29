# TASK-004: Update skills/transcript/SKILL.md cross-references to docs/adrs/

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

Update every ADR-007 cross-reference in `skills/transcript/SKILL.md` to use the new `docs/adrs/ADR-007-output-template-specification.md` path. Replace any occurrence of the old jerry-core project path with the public path.

---

## Acceptance Criteria

- [ ] All ADR-007 references in `skills/transcript/SKILL.md` use the new `docs/adrs/` path
- [ ] `grep -r "transcript-skill/work/EPIC-001-transcript-skill" skills/transcript/SKILL.md` returns zero matches
- [ ] All updated cross-references resolve to the actually existing file in `docs/adrs/`
- [ ] No semantic content changed in SKILL.md (only path updates)
