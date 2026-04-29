# TASK-005: Update skills/transcript/agents/ts-formatter.md cross-references

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

Update every ADR-007 cross-reference in `skills/transcript/agents/ts-formatter.md` to use the new `docs/adrs/` path. The ts-formatter agent prompt cites ADR-007 as authoritative for output template rules; ensure the citation resolves in the public release.

---

## Acceptance Criteria

- [ ] All ADR-007 references in `skills/transcript/agents/ts-formatter.md` use the new `docs/adrs/` path
- [ ] `grep -r "transcript-skill/work/EPIC-001-transcript-skill" skills/transcript/agents/ts-formatter.md` returns zero matches
- [ ] Updated references resolve to the actually existing file
- [ ] No agent-prompt semantic changes (only path updates)
