# GitHub issue #358: PROJ-032/BUG-009: nuclear-sop — skill missing from enforcement lists, "nuclear workflow" misrouted, agent count wrong (fixed on your branch)

Assignees:

**What this is:** one of seven mechanical fixes the maintainer applied directly to your PR #269 branch (`proj-0039-nuclear-engineer`) in commit `c07033ce`. Nothing for you to do unless you disagree with the fix.

**What was wrong:** three registration-bookkeeping gaps on your branch. (1) In `.context/rules/mandatory-skill-usage.md`, `/nuclear-sop` was the only trigger-mapped skill missing from both the mandatory-invocation rule sentence and the comment that re-injects that rule into the model's context on every prompt — so the strongest, degradation-proof enforcement layer never covered it. (2) The skill's advertised activation phrase "nuclear workflow" actually routed to `/orchestration` ("workflow" matches that skill at higher priority, and no compound trigger existed to override it — despite the PR's collision analysis claiming one did). (3) `AGENTS.md` was never updated for the four new agents: no navigation-table entry, no summary row, and a total of 89 where the correct count is 93.

**What the fix changed:** `.context/rules/mandatory-skill-usage.md` now names `/nuclear-sop` in the rule sentence and in the per-prompt re-injection comment, and its trigger row gains the compound phrase `"nuclear workflow" OR "nuclear sop"` — phrase matches beat numeric priority in the routing algorithm, so the collision is resolved without touching `/orchestration`'s row. `AGENTS.md` gets the missing section link, a summary row, and the corrected total of 93.

**How to verify:** on `proj-0039-nuclear-engineer`, run `git diff c07033ce^ c07033ce -- .context/rules/mandatory-skill-usage.md AGENTS.md`. CI at that commit: 15/15 green — https://github.com/geekatron/jerry/actions/runs/31174766440.

---
**Tracking:** worktracker `projects/PROJ-032-nuclear-sop-review/work/BUG-009-registration-enforcement-surfaces` (register section REM-09 in `remediation-register.md`, under `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`). Fix is already on your branch; this issue stays open only until PR #269's disposition is decided.
