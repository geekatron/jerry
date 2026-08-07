# GitHub issue #355: nuclear-sop — lessons-learned loop can't work as specified (lifecycle redesign, PR #269)

Assignees: victorlau1 malcolm-x-evo

**What this is about:** the skill keeps a shared "operating experience" store — lessons-learned files each run writes and later runs read back. As specified, the loop cannot actually work: the "synthesis" entry type the rules demand is missing from the entry schema, and the write-validation rules reject it — so compliant synthesis entries cannot exist, and the accumulation threshold ratchets monotonically toward a stop condition that blocks every future execution of the same workflow type, repo-wide. The store is also a prompt-injection channel (low-risk runs write files that high-risk runs read), mitigated only by guard labels on 2 of the interpolated fields, plus a separate forgeable provenance cross-reference, and the provenance flags false-fire after routine cleanup of the work directory.

Affected files: skills/nuclear-sop/agents/sop-brief.md, skills/nuclear-sop/agents/sop-capture.md, skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md, skills/nuclear-sop/PLAYBOOK.md, skills/nuclear-sop/behavioral-baselines/bb-003-oe-feedback-loop-integrity.md.

**The design question to answer:** what lifecycle makes the loop real — a writable schema with a single owner for synthesis entries, thresholds that cannot deadlock unrelated executions, a retention/archival rule so provenance survives routine work/ cleanup, and an injection-trust model for a corpus shared across risk levels? Reply on this issue with your proposed design before implementing it.

---
**Tracking:** severity major; not maintainer-fixable (design decision). Internal tracking file: [BUG-006-oe-feedback-loop-design.md](https://github.com/geekatron/jerry/blob/feat/proj-032-nuclear-sop-review/projects/PROJ-032-nuclear-sop-review/work/BUG-006-oe-feedback-loop-design/BUG-006-oe-feedback-loop-design.md) (see the linked analysis for the full design write-up).

Full analysis and redesign question: [remediation-register.md, section REM-06](https://github.com/geekatron/jerry/blob/feat/proj-032-nuclear-sop-review/projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md#rem-06-oe-feedback-loop-design). Propose the redesign on your own PR branch — the branch cited above is reference material only.

This is 1 of 7 coordinated PR #269 design blockers (issues #350-#354, #356); all seven must close before merge.
