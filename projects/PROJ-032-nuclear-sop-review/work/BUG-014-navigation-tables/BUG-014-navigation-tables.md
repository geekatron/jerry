# BUG-014: Navigation tables [REM-14]

> **Type:** bug
> **Status:** completed
> **Priority:** critical
> **Impact:** high
> **Severity:** critical
> **Created:** 2026-08-07T11:30:00Z
> **Completed:** 2026-08-07T13:30:00Z
> **Found In:** PR #269 head bda64202 (branch proj-0039-nuclear-engineer)
> **GitHub Issue:** [#363](https://github.com/geekatron/jerry/issues/363)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Defect, disposition, findings consumed, affected files |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect concretely |
| [Acceptance Criteria](#acceptance-criteria) | Observable outcomes of the fix |
| [Related Items](#related-items) | Register, parent story, GitHub issue |

## Summary

Three runtime-consumed long files ship with no navigation table — `templates/WORKFLOW_DEFINITION.template.md` (250 lines, consumed by sop-brief Step 0), `templates/HOLD_POINT_LOG.template.md` (76 lines), and `examples/c3-adr-workflow-definition.md` (559 lines, the QG-E4 fixture) — violating H-23/NAV-001, whose consequence is "document rejected".
NAV-004 coverage omissions also exist in files that do have nav tables: SKILL.md omits "## P-003 Compliance"; PLAYBOOK.md omits three top-level sections (PROCEDURE_STATE.yaml State Machine, Step Limits by Criticality, OE Accumulation Thresholds); docs/reference.md omits "## Related" (AGENTS.md's omission is fixed in REM-09/BUG-009).
Disposition: FIX-NOW — pure H-23/NAV-001/NAV-004/NAV-006 mechanical additions; the compliant corpus (23/25 canonical templates, 3 of the skill's own 5 templates) defines the format.
Source findings consumed: P1-006, S-003-04.
Affected files: `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md`, `skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md`, `skills/nuclear-sop/examples/c3-adr-workflow-definition.md`, `skills/nuclear-sop/SKILL.md`, `skills/nuclear-sop/PLAYBOOK.md`, `skills/nuclear-sop/docs/reference.md`.

## Steps to Reproduce

1. On PR #269 head `bda64202`, open the three G1 files (`templates/WORKFLOW_DEFINITION.template.md`, `templates/HOLD_POINT_LOG.template.md`, `examples/c3-adr-workflow-definition.md`): none contains a "Document Sections" table despite all exceeding the 30-line H-23 threshold.
2. Compare `##` headings against the existing nav tables in `SKILL.md`, `PLAYBOOK.md`, and `docs/reference.md`: "## P-003 Compliance", the three PLAYBOOK top-level sections, and "## Related" respectively have no rows.
3. Run the `/ast` nav validation (or a markdown-lint nav check) against the six files to confirm the H-23/NAV-004 violations.

## Acceptance Criteria

- [x] A "Document Sections" table (`| Section | Purpose |` with NAV-006 anchor links) added after the frontmatter/intro of each of the three G1 files, listing every `##` heading. (verified 2026-08-07)
- [x] The missing rows added to the existing nav tables of SKILL.md ("## P-003 Compliance"), PLAYBOOK.md (PROCEDURE_STATE.yaml State Machine, Step Limits by Criticality, OE Accumulation Thresholds), and docs/reference.md ("## Related"). (verified 2026-08-07)
- [x] Validation passes: for each of the six files, every `##` heading has a nav-table row and every anchor resolves (lowercase, hyphens, special chars stripped); `/ast` or markdown-lint nav check passes. (verified 2026-08-07)
- [x] Fix commit pushed to proj-0039-nuclear-engineer and referenced here. — commit c07033ce
- [x] PR #269 CI green at post-fix head. — 15/15, run 31174766440

## Related Items

- Remediation register (REM-14): [remediation-register.md](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md#rem-14-navigation-tables)
- Parent story: [STORY-004](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/STORY-004-remediation.md)
- GitHub Issue: [#363](https://github.com/geekatron/jerry/issues/363)
