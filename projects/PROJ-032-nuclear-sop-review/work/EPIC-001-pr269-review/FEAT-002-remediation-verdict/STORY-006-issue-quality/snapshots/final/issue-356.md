# GitHub issue #356: PROJ-032/BUG-007: nuclear-sop — replace the command block-list with a principled gating model (PR #269)

Assignees: victorlau1 malcolm-x-evo

**What this is about:** the execution agent's protection against dangerous shell commands is a substring block-list ("if the command contains one of these strings, pause"). Block-lists enumerate badness and always miss: `nc`, `python -m http.server`, base64-encoded exfiltration and similar all pass it today. The skill's prompt-injection screening likewise covers only one of the several attacker-influenceable inputs (workflow definitions, state files, lessons-learned entries, hold-point logs) that end up driving tool calls — and the screening step echoes suspect payloads verbatim into logs that later agents read. Meanwhile the repository already has a deterministic security enforcement engine this duplicates, weaker, at the prompt level.

**The design question to answer:** what principled command-gating model replaces the block-list — an allow-list, category-based pause points, or delegation to the existing deterministic enforcement engine — and what is the injection-screening scope across *all* definition-sourced fields that drive tool calls?

---
**Tracking:** severity major; not maintainer-fixable (the gating model must be redesigned, not extended). Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-007-executor-command-gating` (register section REM-07). Full analysis with candidate designs: `remediation-register.md` in `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`. Blocks merge of PR #269.
