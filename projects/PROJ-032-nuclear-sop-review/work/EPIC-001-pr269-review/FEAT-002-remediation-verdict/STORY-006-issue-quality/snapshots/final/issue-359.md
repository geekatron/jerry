# GitHub issue #359: PROJ-032/BUG-010: nuclear-sop — agent metadata files failed schema validation; one YAML unparseable (fixed on your branch)

Assignees:

**What this is:** one of seven mechanical fixes the maintainer applied directly to your PR #269 branch (`proj-0039-nuclear-engineer`) in commit `c07033ce`. Nothing for you to do unless you disagree with the fix.

**What was wrong:** deterministic validator failures plus standards drift under `skills/nuclear-sop/` on your branch. `composition/sop-verifier.agent.yaml` was not even parseable YAML (an unquoted `: ` inside the description scalar on line 9). `agents/sop-brief.governance.yaml` failed the repo's agent-governance JSON schema with 4 errors and `agents/sop-verifier.governance.yaml` with 2 — and the repo's rule for agent definitions makes any schema failure a CI-rejectable defect. Beyond the validators: the brief agent's section-number references contradicted the skill's own workflow template; none of the four agents declared where its output files go (the repo standard anchors agent output under the active project directory); agent identity prose named concrete tool calls where the standard requires capability language; and the executor agent omitted the reasoning-effort declaration its review tier calls for.

**What the fix changed:** quoting and format corrections make every YAML parseable and all four governance files pass the schema (independent re-check after the fix: 8 of 8 files valid); section numbering aligned to the template; project-anchored output locations declared for all four agents; tool names in identity prose replaced with capability wording; `reasoning_effort: high` added to the executor.

**How to verify:** on `proj-0039-nuclear-engineer`, run `git diff c07033ce^ c07033ce -- skills/nuclear-sop/agents/ skills/nuclear-sop/composition/`, or re-validate the governance files against `docs/schemas/agent-governance-v1.schema.json` (same branch) — zero errors. CI at that commit: 15/15 green — https://github.com/geekatron/jerry/actions/runs/31174766440.

---
**Tracking:** worktracker `projects/PROJ-032-nuclear-sop-review/work/BUG-010-agent-schema-conformance` (register section REM-10 in `remediation-register.md`, under `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`). Fix is already on your branch; this issue stays open only until PR #269's disposition is decided.
