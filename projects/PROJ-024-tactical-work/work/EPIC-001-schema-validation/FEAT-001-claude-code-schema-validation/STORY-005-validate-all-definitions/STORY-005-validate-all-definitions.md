# STORY-005: Validate All Agent and Skill Definitions Against Schemas

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-27T02:00:00Z
> **Due:**
> **Completed:** 2026-03-27T03:00:00Z
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What was done |
| [Evidence](#evidence) | Delivery artifacts |

---

## Summary

Ran the frontmatter schemas against all 89 agent definitions and 30 SKILL.md files. Found and fixed 4 defects:
- 3 skills using `tools:` instead of `allowed-tools:` (contract-design, test-spec, use-case)
- 4 skills using multiline YAML descriptions (contract-design, pm-pmm, test-spec, use-case)
- 1 skill with unquoted colon in description (pm-pmm)

Final result: 119/119 ALL PASSED.

---

## Evidence

| Deliverable | Path |
|-------------|------|
| Validation script | `scripts/validate_all_frontmatter.py` (migrated to CLI in STORY-008) |
| Validation report | `STORY-005-validate-all-definitions/validation-report.md` |
| Fixed skills | `skills/contract-design/SKILL.md`, `skills/pm-pmm/SKILL.md`, `skills/test-spec/SKILL.md`, `skills/use-case/SKILL.md` |
