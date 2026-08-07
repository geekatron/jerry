TITLE: PROJ-032 Phase 1: standards audit of the nuclear-sop skill — 32 findings, 6 critical (internal tracking, no action needed)

**What this is:** an internal review-tracking issue for Phase 1 of the maintainer's independent review of PR #269 (the `/nuclear-sop` skill on the PR branch `proj-0039-nuclear-engineer`). No action is needed from the PR author — findings that do need author attention have their own issues (#350–#356).

**What the phase did and found:** six independent auditors, each working blind of the others, checked every file of the skill (at PR head commit `bda64202`) against the repository's coding and documentation standards. Consolidated result: **32 findings — 6 critical, 15 major, 11 minor**, including five confirmed violations of the repo's non-negotiable "hard" rules: a worker agent instructed to invoke other agents (the framework allows delegation only one level deep, so a worker may never invoke another agent), a user-approval gate depending on a tool the agent is not granted, two agent metadata files failing their JSON schema, and long runtime-consumed files shipped without the required navigation tables. Phase verdict: not mergeable as shipped, but none of the defects looked beyond straightforward repair — the mechanical ones were later fixed by the maintainer on the PR branch (issues #357–#363), and the design-level ones were handed back to the author (#350–#356).

**Where the detail lives:** `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-001-independent-review/STORY-001-standards-compliance/phase-1-standards-report.md` on branch `feat/proj-032-nuclear-sop-review` — executive summary at the top, then the full findings register with per-file, per-line evidence.

---
**Tracking:** internal review-tracking issue. Worktracker: `projects/PROJ-032-nuclear-sop-review` — **STORY-001**. Stays open until the review branch `feat/proj-032-nuclear-sop-review` merges.
