# GitHub issue #360: PROJ-032/BUG-011: nuclear-sop — lessons-learned files written as .yaml but documented as .md, silently breaking the feedback loop (fixed on your branch)

Assignees:

**What this is:** one of seven mechanical fixes the maintainer applied directly to your PR #269 branch (`proj-0039-nuclear-engineer`) in commit `c07033ce`. Nothing for you to do unless you disagree with the fix.

**What was wrong:** the skill's "operating experience" loop — capture lessons learned after each run, retrieve them before the next — was internally inconsistent about its own file format, on your branch. The rules file and the write path use `docs/experience/{entry_id}.yaml`, but the post-job template, one behavioral baseline, and the worked example all said `.md`. Entries written per those documents would be permanently invisible to retrieval, silently zeroing the feedback loop the skill names as its key capability — and one of the worked example's acceptance criteria was literally unsatisfiable. The retrieval protocol itself was specified three different ways across files, and the workflow definition's "Attachments" section was documented as runtime-written by the capture agent, whose procedure never actually writes it.

**What the fix changed:** `.yaml` and the workflow-ID-primary search protocol are now the single convention everywhere (template, baseline, example, both agents, and their mirror copies), and `skills/nuclear-sop/agents/sop-capture.md` gains an explicit step that appends the lessons-learned reference to the workflow definition's Attachments section — implementing what three documents already promised.

**How to verify:** on `proj-0039-nuclear-engineer`, run `git diff c07033ce^ c07033ce -- skills/nuclear-sop/`, and check that `grep -rn "experience/.*\.md" skills/nuclear-sop/` returns nothing. CI at that commit: 15/15 green — https://github.com/geekatron/jerry/actions/runs/31174766440.

---
**Tracking:** worktracker `projects/PROJ-032-nuclear-sop-review/work/BUG-011-oe-artifact-contract` (register section REM-11 in `remediation-register.md`, under `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`). Fix is already on your branch; this issue stays open only until PR #269's disposition is decided.
