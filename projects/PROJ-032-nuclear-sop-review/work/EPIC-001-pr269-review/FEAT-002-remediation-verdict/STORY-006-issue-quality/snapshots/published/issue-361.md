# GitHub issue #361: nuclear-sop: state machine specified three different ways; completion handoff type-broken (fixed on your branch) [PROJ-032/BUG-012]

**What this is:** one of seven mechanical fixes the maintainer applied directly to your PR #269 branch (`proj-0039-nuclear-engineer`) in commit `c07033ce`. Nothing for you to do unless you disagree; if so, comment on this issue before PR #269's disposition is decided.

**What was wrong:** three contract breaks in the skill's execution-state tracking.

1. The state machine differed across the rules file, the state-file template, and a behavioral baseline: divergent transitions after verifier rejection, and a "WAIVED" outcome the baseline requires but the template's allowed values omit.
2. The completion handoff was self-contradictory and type-broken. The executor agent set status COMPLETED before the capture agent ran, a transition the skill's own rules forbid. It also recorded `execution_log_final` as a file path, while the capture agent's first step halts unless it is the literal boolean `true`, halting the mandatory capture phase of every run.
3. The verifier's hold-point check read the state file only "if accessible," silently skipping when missing: the fail-open gap the PR's own QG-E6 quality-gate report had flagged OPEN, RPN-144, REMEDIATION REQUIRED (tracked internally as finding SEC-008), shipped unfixed.

**What the fix changed:**

1. Transitions aligned to the rules file as the single source of truth; template and baseline now match.
2. The executor leaves status IN-PROGRESS and sets `execution_log_final` to a path; the capture agent checks the path resolves to a real file and remains the sole writer of COMPLETED.
3. The verifier now fails closed: a missing or unreadable state file is recorded as an anomaly and blocks unconditional ACCEPT.

**Files:** `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml`, `skills/nuclear-sop/agents/sop-executor.md`, `skills/nuclear-sop/agents/sop-capture.md`, `skills/nuclear-sop/agents/sop-verifier.md` (+ composition twins `skills/nuclear-sop/composition/sop-executor.prompt.md`, `skills/nuclear-sop/composition/sop-capture.prompt.md`, `skills/nuclear-sop/composition/sop-verifier.prompt.md`).

**How to verify:** on `proj-0039-nuclear-engineer`, run `git diff c07033ce^ c07033ce -- skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml skills/nuclear-sop/agents/sop-executor.md skills/nuclear-sop/agents/sop-capture.md skills/nuclear-sop/agents/sop-verifier.md skills/nuclear-sop/composition/sop-executor.prompt.md skills/nuclear-sop/composition/sop-capture.prompt.md skills/nuclear-sop/composition/sop-verifier.prompt.md` (or view https://github.com/geekatron/jerry/commit/c07033ce filtered to those paths). CI at that commit: 15/15 green (https://github.com/geekatron/jerry/actions/runs/31174766440).

---
**Tracking (both on branch `feat/proj-032-nuclear-sop-review`, or the same paths under `main` once this review branch merges):** internal tracking record `projects/PROJ-032-nuclear-sop-review/work/BUG-012-state-machine-contract/BUG-012-state-machine-contract.md`; register section REM-12 in `remediation-register.md` under `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/`. This issue stays open only until PR #269's disposition is decided. Seven unrelated design-defect clusters (issues #350-#356) remain open and block PR #269 from merging.
