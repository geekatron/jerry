TITLE: PROJ-032/BUG-008: nuclear-sop — docs claimed "not registered" and "approved for all risk levels"; both corrected (fixed on your branch)

**What this is:** one of seven mechanical fixes the maintainer applied directly to your PR #269 branch (`proj-0039-nuclear-engineer`) in commit `c07033ce`. Nothing for you to do unless you disagree with the fix.

**What was wrong:** the skill's two entry-point documents, on your branch, made false or contradictory claims about the skill's own state. `skills/nuclear-sop/SKILL.md` said the skill was "NOT registered and NOT live-routable" — while the very same PR registered it in five files (`CLAUDE.md`, `AGENTS.md`, the skill trigger map, `plugin.json`, `CHANGELOG.md`). SKILL.md also carried a stale "copy-ready" trigger-table row that diverged from the applied one and would have corrupted routing if pasted. And SKILL.md claimed the skill was "approved for all criticality levels" (the framework's risk tiers) while `PLAYBOOK.md` said the opposite — and the validation evidence behind the higher-risk approval had been invalidated (see #353).

**What the fix changed:** SKILL.md now states the true registration status (registered, with pointers to the live files); the stale trigger-row copy is deleted in favor of a pointer to the single live source; and — the conservative call — approval for higher-risk work is withdrawn pending real re-validation: the skill is approved for low-risk (C1–C2) use only, stated identically in SKILL.md, PLAYBOOK.md, the rules file, and the reference docs.

**How to verify:** on `proj-0039-nuclear-engineer`, run `git diff c07033ce^ c07033ce -- skills/nuclear-sop/SKILL.md skills/nuclear-sop/PLAYBOOK.md`. CI at that commit: 15/15 green — https://github.com/geekatron/jerry/actions/runs/31174766440.

---
**Tracking:** worktracker `projects/PROJ-032-nuclear-sop-review/work/BUG-008-registration-status-truth` (register section REM-08 in `remediation-register.md`, under `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`). Fix is already on your branch; this issue stays open only until PR #269's disposition is decided.
