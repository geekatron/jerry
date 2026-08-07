# Issue #353: PROJ-032/BUG-004: nuclear-sop — validation test contained its own answer key; redo it blind (PR #269)

**What this is about:** the skill's approval for higher-risk work rested on a claim that its self-check protocol caught 3 out of 3 planted errors, "empirically validated." The test fixture ships in this PR — and it contains the trap annotations and the expected correct answers inline, in the same file the tested agent reads before answering. A test whose subject can read the answer key validates nothing. The maintainer remediation (commit `c07033ce`) has already withdrawn the higher-risk approval; the skill is currently restricted to low-risk use.

**The design question to answer:** what blind, independently executed, statistically meaningful validation — answer keys stripped, live transcripts, independent authorship and scoring, more than three trials — replaces the invalidated walkthrough before any higher-risk approval claim returns?

---
**Tracking:** severity critical; not maintainer-fixable (evidence cannot be manufactured by a maintainer). Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-004-qg-e4-validation-evidence` (register section REM-04). Full analysis with candidate designs: `remediation-register.md` in `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`. Blocks any restoration of higher-risk approval; the low-risk-only restriction otherwise stands.
