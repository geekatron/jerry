# GitHub issue #359: PROJ-032/BUG-010: nuclear-sop — agent metadata files failed schema validation; one YAML unparseable (fixed on your branch)

**What this is:** one of seven mechanical fixes the maintainer applied to your PR #269 branch (`proj-0039-nuclear-engineer`) in commit `c07033ce`. Nothing for you to do unless you disagree.

**What was wrong:** eight defects under `skills/nuclear-sop/` on that branch:

1. `composition/sop-verifier.agent.yaml` was unparseable YAML (unquoted `: ` inside its line-9 description).
2. `agents/sop-brief.governance.yaml` failed the repo's agent-governance JSON schema with 4 errors (checklist entries written as mappings where the schema requires plain strings) — any agent schema failure is CI-rejectable here.
3. `agents/sop-verifier.governance.yaml` failed the same schema with 2 errors.
4. `composition/sop-brief.agent.yaml` failed its own declared canonical schema with 5 errors: the same four mapping-style entries plus an unquoted colon on its `on_send` line.
5. The brief agent's section numbers contradicted the skill's workflow template.
6. No agent declared the project-anchored, resolvable output location the repo standard requires (sop-executor's `{execution_dir}` was undefined; sop-capture's was non-resolvable prose; sop-verifier had none).
7. Agent identity prose named concrete tools where the standard requires capability language.
8. Executor, brief, and capture omitted the reasoning-effort declaration their quality-gate tier calls for (ET-M-001; sop-verifier's default is correct by design — validation-only).

**What the fix changed:** quoting and format corrections make every YAML parseable and all eight metadata files pass their schemas (independent re-check: 8 of 8 valid — four `agents/*.governance.yaml` plus four `composition/*.agent.yaml`); section numbering aligned to the template; project-anchored output locations (`projects/${JERRY_PROJECT}/nuclear-sop/{workflow_id}/...`) declared for sop-brief, sop-executor, and sop-capture; sop-verifier (read-only) correctly declares `output.required: false`, returning its report as agent response content; tool names replaced with capability wording; `reasoning_effort: high` added to executor, brief, and capture.

**How to verify:** on `proj-0039-nuclear-engineer`, run `git diff c07033ce^ c07033ce -- skills/nuclear-sop/agents/ skills/nuclear-sop/composition/` (the diff also bundles unrelated REM-11/REM-12/REM-13 fixes intermixed in the same `agents/*.md` files; REM-10-specific hunks are the four `*.governance.yaml` files, `sop-verifier.agent.yaml`/`sop-brief.agent.yaml`, and the section-numbering/wording edits). To reproduce the 8 of 8, from that branch's repo root:

```
uv run python -c "import yaml,json,glob;from jsonschema import Draft202012Validator as V;[print(f,len(list(V(json.load(open(s))).iter_errors(yaml.safe_load(open(f))))),'errors') for pat,s in [('skills/nuclear-sop/agents/*.governance.yaml','docs/schemas/agent-governance-v1.schema.json'),('skills/nuclear-sop/composition/*.agent.yaml','docs/schemas/agent-canonical-v1.schema.json')] for f in sorted(glob.glob(pat))]"
```

Expected: eight lines, all `0 errors` (`yaml.safe_load` doubles as the parse check). CI at that commit: 15/15 green — https://github.com/geekatron/jerry/actions/runs/31174766440.

---
**Tracking:** worktracker `projects/PROJ-032-nuclear-sop-review/work/BUG-010-agent-schema-conformance/BUG-010-agent-schema-conformance.md` (register section REM-10 in `remediation-register.md`, under `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`). Fix is already on your branch; this issue stays open until PR #269's disposition is decided.
