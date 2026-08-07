# Issue #351: PROJ-032/BUG-002: nuclear-sop — how does the user-approval pause actually reach a human? (runtime model, PR #269)

**What this is about:** the skill's user-approval pause ("USER-HOLD" — the mechanism that stops work and asks a human before proceeding) calls a tool (`AskUserQuestion`) that none of the four agents is granted and that no agent in this repository has. Deeper problem: the docs never pin down *how the skill actually runs* — as a background worker agent (which has no way to stop and wait for a human at all) or as the main-session persona (which contradicts other documented guarantees). Every interactive gate in the skill inherits this ambiguity. Related: the rule "run a self-check before every file write" is non-terminating as written, because recording the self-check is itself a file write.

**The design question to answer:** what is the pinned runtime execution model, how do USER-HOLD and the briefing agent's six interactive gates actually reach a human under that model, and what is the terminating scope of the self-check rule?

---
**Tracking:** severity critical; not maintainer-fixable (design decision). Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-002-user-hold-runtime-model` (register section REM-02). Full analysis with candidate designs: `remediation-register.md` in `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`. Blocks merge of PR #269.
