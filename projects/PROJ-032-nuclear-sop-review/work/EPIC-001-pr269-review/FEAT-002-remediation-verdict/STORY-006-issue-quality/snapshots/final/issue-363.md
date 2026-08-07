# GitHub issue #363: PROJ-032/BUG-014: nuclear-sop — long markdown files missing required navigation tables (fixed on your branch)

Assignees:

**What this is:** one of seven mechanical fixes the maintainer applied directly to your PR #269 branch (`proj-0039-nuclear-engineer`) in commit `c07033ce`. Nothing for you to do unless you disagree with the fix.

**What was wrong:** this repo requires every long markdown file that agents consume at runtime to open with a navigation table — a `| Section | Purpose |` table with anchor links to each heading. On your branch, three long runtime-consumed files shipped without one: `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` (250 lines, read by the brief agent on every run), `skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md` (76 lines), and `skills/nuclear-sop/examples/c3-adr-workflow-definition.md` (559 lines, the skill's flagship worked example). Three more files had navigation tables missing rows for sections that exist: `skills/nuclear-sop/SKILL.md`, `skills/nuclear-sop/PLAYBOOK.md`, and `skills/nuclear-sop/docs/reference.md`.

**What the fix changed:** navigation tables were added to the three files that lacked them, matching the format used by 23 of the repo's 25 canonical templates (and by 3 of the skill's own 5 templates), and the missing rows were added to the other three files — with every anchor link checked to resolve to its heading.

**How to verify:** on `proj-0039-nuclear-engineer`, run `git diff c07033ce^ c07033ce -- skills/nuclear-sop/templates/ skills/nuclear-sop/examples/ skills/nuclear-sop/SKILL.md skills/nuclear-sop/PLAYBOOK.md skills/nuclear-sop/docs/reference.md`. CI at that commit: 15/15 green — https://github.com/geekatron/jerry/actions/runs/31174766440.

---
**Tracking:** worktracker `projects/PROJ-032-nuclear-sop-review/work/BUG-014-navigation-tables` (register section REM-14 in `remediation-register.md`, under `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`). Fix is already on your branch; this issue stays open only until PR #269's disposition is decided.
