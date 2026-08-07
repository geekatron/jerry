TITLE: PROJ-032 Phase 2: engineering review of the nuclear-sop skill — methodology, prompts, security (internal tracking, no action needed)

**What this is:** an internal review-tracking issue for Phase 2 of the maintainer's independent review of PR #269 (the `/nuclear-sop` skill on the PR branch `proj-0039-nuclear-engineer`). No action is needed from the PR author; author-facing findings have their own issues (#350–#363).

**What the phase did and found:** a single engineering review, performed blind to the other review phases, examined the skill at PR head commit `bda64202` through three lenses — is the methodology actually executable, are the agent prompts sound, and what is the security posture (including a threat model of the skill's attacker-influenceable runtime inputs). Result: **30 findings — 4 critical, 16 major, 10 minor**; verdict: NO-GO for merge as shipped. The four criticals: the user-approval hold depends on a tool no agent is granted; the flagship worked example requires mid-procedure agent calls the executing agent structurally cannot make; the skill's self-check rule as written also applies to its own bookkeeping writes, so it never terminates; and the "independent verifier" takes its acceptance criteria from the very untrusted workflow file it is supposed to police, so a crafted workflow could certify itself. The review's own disposition line: the skill is "one focused revision cycle away from being a strong addition."

**Where the detail lives:** `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-001-independent-review/STORY-002-engineering-review/phase-2-eng-review.md` on branch `feat/proj-032-nuclear-sop-review` — executive summary up top, then full per-finding evidence and the threat table.

---
**Tracking:** internal review-tracking issue. Worktracker: `projects/PROJ-032-nuclear-sop-review` — **STORY-002**. Stays open until the review branch `feat/proj-032-nuclear-sop-review` merges.
