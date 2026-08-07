# Issue #352: PROJ-032/BUG-003: nuclear-sop — verifier takes its criteria from the file it polices (trust anchor, PR #269)

**What this is about:** the skill's "independent verifier" agent (`sop-verifier`) takes its acceptance criteria, its expected file paths, and even the workflow's declared risk level from the workflow-definition file — the same untrusted input it exists to police. A crafted workflow definition can therefore declare itself low-risk and define passing criteria it trivially meets: the checker's authority comes from the thing being checked. Separately, the documentation claims the execution-state file carries SHA-256 tamper detection; no such mechanism is implemented anywhere, and a hand-edited state file resumes cleanly past every pause point.

**The design question to answer:** where do the verifier's criteria, expected paths, and the effective risk level come from, if not from the artifact they police — and is the tamper-evidence control going to be implemented for real, or withdrawn from every place the docs claim it?

---
**Tracking:** severity critical; not maintainer-fixable (design decision). Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-003-trust-boundary-state-tamper` (register section REM-03). Full analysis with candidate designs: `remediation-register.md` in `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`. Blocks merge of PR #269.
