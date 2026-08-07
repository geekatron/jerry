# GitHub issue #363: nuclear-sop: 6 files with missing or incomplete navigation tables — fix applied on your branch, open pending PR #269 disposition (PROJ-032/BUG-014)

Assignees:

**What this is:** one of seven mechanical fixes the maintainer applied to your PR #269 branch (`proj-0039-nuclear-engineer`) in commit `c07033ce`. Nothing for you to do unless you disagree — if so, comment here or reply on PR #269.

**What was wrong:** this repo requires every Claude-consumed markdown file over 30 lines to open with a navigation table — a `| Section | Purpose |` table with anchor links to each heading. Six files on your branch fell short:

- `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` — no navigation table (250 lines; loaded only by the brief agent's optional Step 0)
- `skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md` — no navigation table (76 lines)
- `skills/nuclear-sop/examples/c3-adr-workflow-definition.md` — no navigation table (559 lines; the skill's flagship example)
- `skills/nuclear-sop/SKILL.md` — table present but missing rows
- `skills/nuclear-sop/PLAYBOOK.md` — table present but missing rows
- `skills/nuclear-sop/docs/reference.md` — table present but missing rows

**What the fix changed:** navigation tables were added to the three files lacking them, matching 23 of the repo's 25 canonical templates (the `.context/templates/` corpus) and 3 of the skill's own 5 templates; the missing rows were added to the other three — every anchor checked to resolve to its heading.

**How to verify:** run `git fetch origin proj-0039-nuclear-engineer`, then: `git diff c07033ce^ c07033ce -- skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md skills/nuclear-sop/examples/c3-adr-workflow-definition.md skills/nuclear-sop/SKILL.md skills/nuclear-sop/PLAYBOOK.md skills/nuclear-sop/docs/reference.md`. If the commit is no longer on the branch, use the PR Files tab filtered to these six paths. Note: this commit also carries unrelated fixes in these same files (tracked in sibling issues #357, #359, #360, #361, #362 — #358 does not touch these six files) — only the added "Document Sections" tables and navigation-table rows belong to this issue. CI at that commit: 15/15 green — https://github.com/geekatron/jerry/actions/runs/31174766440; commit: https://github.com/geekatron/jerry/commit/c07033ce.

---
**Tracking:** worktracker (this repo's internal work-item record) `projects/PROJ-032-nuclear-sop-review/work/BUG-014-navigation-tables` (register section REM-14 in `remediation-register.md`, under `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`; internal maintainer tracking, no action needed). The fix is on your branch; this issue stays open until PR #269's disposition is decided. PR #269's merge remains blocked by seven other unresolved review clusters (issues #350–#356; REM-01..07 in the same register, including core safety-architecture items) unrelated to this fix.
