# GitHub issue #350: PROJ-032/BUG-001: nuclear-sop — who may invoke agents mid-procedure? (delegation redesign, PR #269)

Assignees: victorlau1 malcolm-x-evo

**What this is about:** the nuclear-sop skill's execution agent (`sop-executor`) is instructed, at certain built-in pause points, to invoke *other* agents — e.g. calling a quality reviewer when a quality-gate pause fires. But in this framework a worker agent may not invoke further agents (delegation is one level deep: main session → worker, never worker → worker). The same file that gives this instruction also states the agent "cannot invoke any other agent." The flagship example workflow additionally requires outside agents mid-procedure with no way to suspend and resume the executor's step-tracking around them, and the composed sequence exceeds the framework's three-handoff routing ceiling.

**The design question to answer:** who invokes quality gates and external agents mid-procedure, and how does `sop-executor` suspend and resume its place-keeping around them?

**Acceptable descope:** drop mid-procedure agent composition entirely and rewrite the example workflow to match — the review found that a legitimate answer, provided the shipped text matches the reduced scope.

---
**Tracking:** severity critical; not maintainer-fixable (design decision). Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-001-qg-hold-delegation-topology` (register section REM-01). Full analysis with candidate designs: `remediation-register.md` in `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`. Blocks merge of PR #269.
