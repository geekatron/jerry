# GitHub issue #355: PROJ-032/BUG-006: nuclear-sop — lessons-learned loop can't work as specified (lifecycle redesign, PR #269)

Assignees: victorlau1 malcolm-x-evo

**What this is about:** the skill keeps a shared "operating experience" store — lessons-learned files each run writes and later runs read back. As specified, the loop cannot actually work: the "synthesis" entry type the rules demand is missing from the entry schema, and the write-validation rules reject it — so compliant synthesis entries cannot exist, and the accumulation threshold ratchets monotonically toward a repo-wide stop condition that blocks unrelated work. The store is also a prompt-injection channel (low-risk runs write files that high-risk runs read), mitigated only by a text label, and the provenance flags false-fire after routine cleanup of the work directory.

**The design question to answer:** what lifecycle makes the loop real — a writable schema with a single owner for synthesis entries, thresholds that cannot deadlock unrelated executions, and a provenance/trust model for a corpus shared across risk levels?

---
**Tracking:** severity major; not maintainer-fixable (design decision). Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-006-oe-feedback-loop-design` (register section REM-06). Full analysis with candidate designs: `remediation-register.md` in `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`. Blocks merge of PR #269.
