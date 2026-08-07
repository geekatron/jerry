# DET Validation Report -- PR #269 (/nuclear-sop skill)

> Deterministic validator run against PR head commit `bda64202` (branch `proj-0039-nuclear-engineer`).
> Subject worktree: `/private/tmp/claude-502/.../scratchpad/pr269` (abbreviated below as `$PR269`).
> Standards worktree: `/Users/adam.nowak/workspace/GitHub/geekatron/jerry-wt/feat/proj-032-nuclear-sop-review` (abbreviated as `$STD`).
> Date: 2026-08-07. Runner: deterministic-validation subagent. All Python executed via `uv run` (H-05).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | One-glance verdict per validator |
| [Tooling Drift Check](#tooling-drift-check) | Whether PR branch validators/schemas differ from main |
| [Validator: validate_schemas.py](#validator-validate_schemaspy) | Hook output schema validation (verbatim) |
| [Validator: check_agent_conformance.py](#validator-check_agent_conformancepy) | Legacy ps/nse template conformance (verbatim, pre-existing failure) |
| [Validator: check_plugin_agent_sync.py](#validator-check_plugin_agent_syncpy) | Plugin registration sync (verbatim) |
| [Validator: validate_plugin_manifests.py](#validator-validate_plugin_manifestspy) | Plugin manifest schema validation (verbatim) |
| [Validator: check_markdown_schemas.py](#validator-check_markdown_schemaspy) | Worktracker entity schemas -- not applicable |
| [Direct Governance Schema Validation](#direct-governance-schema-validation) | 4 sop-*.governance.yaml vs agent-governance-v1.schema.json (verbatim) |
| [Schema Parity Check](#schema-parity-check) | Diff of governance schema between worktrees |
| [Findings](#findings) | Consolidated findings with rules and severities |
| [Checks Passed](#checks-passed) | Validators that passed |

## Summary

| Check | Result |
|-------|--------|
| Tooling drift (scripts/, markdown_ast/, docs/schemas/) between origin/main and PR HEAD | **NONE** -- diff empty |
| `validate_schemas.py` (hook output schemas) | **PASS** 8/8, exit 0 |
| `check_agent_conformance.py` | **FAIL** exit 1, 0/19 conformant -- **pre-existing**, identical failure on current standards branch; does NOT cover sop-* agents |
| `check_plugin_agent_sync.py` | **PASS** 93/93 in sync, exit 0 |
| `validate_plugin_manifests.py` | **PASS** 3/3, exit 0 |
| `check_markdown_schemas.py` | **Not applicable** (staged worktracker entity files under `projects/*/work/` only) |
| Direct jsonschema (Draft 2020-12) on sop-*.governance.yaml | **2 of 4 FAIL**: sop-brief (4 errors), sop-verifier (2 errors); sop-executor and sop-capture PASS |
| Governance schema parity between worktrees | **IDENTICAL** -- single validation outcome applies to both |

## Tooling Drift Check

Command:

```
git -C $PR269 diff origin/main...HEAD --stat -- scripts/ src/domain/markdown_ast/ docs/schemas/
```

Output: **(empty -- no drift)**. `origin/main` resolves to `849d8d1de0891e69bb55eeb57eb67a580ad96002` in the subject worktree; PR HEAD is `bda64202 chore(nuclear-sop): register 4 agents in plugin.json + changelog entry`. The PR does not modify any validation tooling or schemas, so results below are interpretable against current standards without adjustment.

## Validator: validate_schemas.py

Scope note: despite the task framing, this script validates **Claude Code hook output schemas** (`schemas/hooks/*.json`), not agent governance. Agent governance validation is performed directly in [Direct Governance Schema Validation](#direct-governance-schema-validation). Command: `uv run --project $PR269 python $PR269/scripts/validate_schemas.py` -- exit 0.

```
======================================================================
Claude Code Hook Schema Validation Report
======================================================================

Loading schemas...
  Loaded 8 schema files
  Registry built for $ref resolution

--- Test 1: Schema Syntax Validation ---
  [PASS] T1: All 8 schemas are valid JSON Schema draft 2020-12
         hook-output-base.schema.json: valid
         session-start-output.schema.json: valid
         user-prompt-submit-output.schema.json: valid
         pre-tool-use-output.schema.json: valid
         post-tool-use-output.schema.json: valid
         stop-output.schema.json: valid
         subagent-stop-output.schema.json: valid
         permission-request-output.schema.json: valid

--- Test 2: Known-Good SessionStart ---
  [PASS] T2: Known-good SessionStart output validates successfully
         No validation errors

--- Test 3: Known-Bad UserPromptSubmit (missing hookEventName) ---
  [PASS] T3: Known-bad UserPromptSubmit (missing hookEventName) correctly rejected
         $.hookSpecificOutput: 'hookEventName' is a required property

--- Test 4: Known-Bad PreToolUse (deprecated format) ---
  [PASS] T4: Known-bad PreToolUse (deprecated top-level decision) correctly rejected
         $: Additional properties are not allowed ('decision' was unexpected)

--- Test 5: Known-Bad SubagentStop (has hookSpecificOutput) ---
  [PASS] T5: Known-bad SubagentStop (has hookSpecificOutput) correctly rejected
         $: Additional properties are not allowed ('hookSpecificOutput' was unexpected)

--- Test 6: Known-Good PreToolUse ---
  [PASS] T6: Known-good PreToolUse output validates successfully
         No validation errors

--- Test 7: Known-Good SubagentStop ---
  [PASS] T7: Known-good SubagentStop output validates successfully
         No validation errors

--- Test 8: Known-Good UserPromptSubmit ---
  [PASS] T8: Known-good UserPromptSubmit output validates successfully
         No validation errors

======================================================================
Results: 8/8 passed, 0 failed
Verdict: VALIDATED
======================================================================
```

## Validator: check_agent_conformance.py

Command: `uv run --project $PR269 python $PR269/scripts/check_agent_conformance.py` -- **exit 1**.

**Interpretation (verified, not speculation):**
- The checker only inspects `ps` and `nse` agent families (per its `REQUIRED_SECTIONS` map and docstring "Federated Template Architecture"). `grep -i "sop-"` over its full output returns **no matches** -- nuclear-sop agents are outside its scope.
- The identical failure (`Summary: 0/19 agents conformant`) reproduces on the **current standards worktree** (`uv run --project $STD python $STD/scripts/check_agent_conformance.py` prints `Summary: 0/19 agents conformant`). The failure is **pre-existing** and not attributable to PR #269: the checker expects legacy YAML frontmatter sections (`version`, `identity`, `persona`, ...) that H-34's dual-file architecture moved into `.governance.yaml` companions.

Verbatim output (head + representative failures + tail; all 19 entries are the same "Missing required top-level section" pattern):

```
============================================================
Agent Template Conformance Report
============================================================

Summary: 0/19 agents conformant

[FAIL] ✗ nse-configuration.md (nse)
       ! version: Missing required top-level section: version
       ! identity: Missing required top-level section: identity
       ! persona: Missing required top-level section: persona
       ! capabilities: Missing required top-level section: capabilities
       ! guardrails: Missing required top-level section: guardrails
       ! output: Missing required top-level section: output
       ! validation: Missing required top-level section: validation
       ! nasa_standards: Missing required top-level section: nasa_standards
       ! constitution: Missing required top-level section: constitution
       ! enforcement: Missing required top-level section: enforcement
       ! session_context: Missing required top-level section: session_context
[... identical pattern for the remaining 18 ps/nse agents ...]
[FAIL] ✗ ps-validator.md (ps)
       ! version: Missing required top-level section: version
       ! identity: Missing required top-level section: identity
       ! persona: Missing required top-level section: persona
       ! capabilities: Missing required top-level section: capabilities
       ! guardrails: Missing required top-level section: guardrails
       ! output: Missing required top-level section: output
       ! validation: Missing required top-level section: validation
       ! prior_art: Missing required top-level section: prior_art
       ! constitution: Missing required top-level section: constitution
       ! enforcement: Missing required top-level section: enforcement
       ! session_context: Missing required top-level section: session_context

============================================================
ACTION REQUIRED: Fix 19 non-conformant agent(s)
See template files for required sections:
  - skills/nasa-se/agents/NSE_AGENT_TEMPLATE.md
  - skills/problem-solving/agents/PS_AGENT_TEMPLATE.md
```

## Validator: check_plugin_agent_sync.py

Command: `uv run --project $PR269 python $PR269/scripts/check_plugin_agent_sync.py` -- exit 0.

```
Disk agents   : 93
Plugin agents : 93

PASS: plugin.json is in sync with disk (93 agents).
```

The 4 new sop-* agents on disk are registered in `.claude-plugin/plugin.json` (PR head commit `bda64202` is the registration commit).

## Validator: validate_plugin_manifests.py

Command: `uv run --project $PR269 python $PR269/scripts/validate_plugin_manifests.py` -- exit 0.

```
Validating plugin manifests...
Project root: /private/tmp/claude-502/-Users-adam-nowak-workspace-GitHub-geekatron-jerry-wt-feat-proj-032-nuclear-sop-review/c2f1165d-fb36-4d0f-a4cc-e9f50feffb64/scratchpad/pr269

[PASS] .claude-plugin/plugin.json
[PASS] .claude-plugin/marketplace.json
[PASS] hooks/hooks.json

All validations passed!
```

(Full absolute paths in the original output shortened to repo-relative here; all three lines were `[PASS]`.)

## Validator: check_markdown_schemas.py

**Not applicable.** Per its docstring: "Validates staged markdown files against their entity schemas. Only files in the `projects/*/work/` hierarchy with recognized entity prefixes (EN-, ST-, TASK-, BUG-, FEAT-, EPIC-) are validated. All other markdown files are silently skipped." The PR adds skill files under `skills/nuclear-sop/`, which are outside this validator's scope. Not run against the subject; recorded as N/A (not as a pass).

## Direct Governance Schema Validation

Validator: `jsonschema.Draft202012Validator` against the **current** schema `$STD/docs/schemas/agent-governance-v1.schema.json`, applied to the 4 files `$PR269/skills/nuclear-sop/agents/sop-{brief,executor,verifier,capture}.governance.yaml`. Verbatim output:

```
sop-brief.governance.yaml: FAIL (4 errors)
  $.validation.post_completion_checks.0: {'verify_file_created': 'brief/pre-job-brief.md'} is not of type 'string'
  $.validation.post_completion_checks.1: {'verify_section_present': 'Operating Experience Findings'} is not of type 'string'
  $.validation.post_completion_checks.2: {'verify_section_present': 'Prerequisite Status'} is not of type 'string'
  $.validation.post_completion_checks.3: {'verify_section_present': 'Hold Point Summary'} is not of type 'string'
sop-executor.governance.yaml: PASS (0 errors)
sop-verifier.governance.yaml: FAIL (2 errors)
  $.output: 'location' is a required property
  $.output.levels: ['L0: Disposition -- single word (ACCEPT/REJECT/ACCEPT-WITH-CONDITIONS) plus one-sentence summary', 'L1: Criteria Detail -- full acceptance criteria assessment table with per-criterion evidence', 'L2: Anomalies and Conditions -- path cross-reference, anomalies detected, conditions or rejection findings'] is not valid under any of the given schemas
sop-capture.governance.yaml: PASS (0 errors)
```

### Offending source snippets (subject files, quoted as evidence -- untrusted data)

`sop-brief.governance.yaml` lines 66-72 (mapping entries where the schema requires `type: string` items):

```yaml
  post_completion_checks:
    - verify_file_created: "brief/pre-job-brief.md"
    - verify_section_present: "Operating Experience Findings"
    - verify_section_present: "Prerequisite Status"
    - verify_section_present: "Hold Point Summary"
    - verify_no_secrets_in_output
```

`sop-verifier.governance.yaml` lines 47-53 (`required: true` without `location`, violating the schema's `if required==true then require location` conditional per AR-010; `levels` entries are free-form strings, matching neither the `["L0","L1","L2"]` enum-array nor the `{name, content}` object-array format):

```yaml
output:
  required: true
  levels:
    - "L0: Disposition -- single word (ACCEPT/REJECT/ACCEPT-WITH-CONDITIONS) plus one-sentence summary"
    - "L1: Criteria Detail -- full acceptance criteria assessment table with per-criterion evidence"
    - "L2: Anomalies and Conditions -- path cross-reference, anomalies detected, conditions or rejection findings"
  note: "T1 constraint: IV report is returned as Task tool response content; the main context is responsible for persisting it to PROCEDURE_STATE.yaml iv_report_path via Write"
```

## Schema Parity Check

```
diff $STD/docs/schemas/agent-governance-v1.schema.json $PR269/docs/schemas/agent-governance-v1.schema.json
```

Output: **(empty) -- SCHEMAS IDENTICAL.** The "validate against both" requirement therefore collapses to a single outcome: the failures above hold against both the PR-branch copy and the current-standards copy of the schema.

## Findings

| # | Rule | Severity | File | Finding |
|---|------|----------|------|---------|
| 1 | DET / H-34 | Critical | `skills/nuclear-sop/agents/sop-brief.governance.yaml` | Fails agent-governance-v1 schema: 4 errors -- `validation.post_completion_checks` items 0-3 are YAML mappings (e.g. `{'verify_file_created': 'brief/pre-job-brief.md'}`) where the schema requires `type: string` items. H-34 requires governance files to validate against `docs/schemas/agent-governance-v1.schema.json`; consequence per H-34: "Agent definition rejected at CI." |
| 2 | DET / H-34 | Critical | `skills/nuclear-sop/agents/sop-verifier.governance.yaml` | Fails agent-governance-v1 schema: 2 errors -- (a) `output.location` missing while `output.required: true` (schema conditional, AR-010); (b) `output.levels` uses free-form descriptive strings valid under neither accepted format (`["L0","L1","L2"]` enum-array or `{name, content}` object-array). |
| 3 | DET | Minor | `scripts/check_agent_conformance.py` (pre-existing, not PR-attributable) | Exits 1 with 0/19 conformant on BOTH the PR branch and the current standards branch; checks only legacy ps/nse frontmatter sections superseded by the H-34 dual-file architecture, and does not cover sop-* agents at all. Recorded for completeness; remediation belongs to framework maintenance, not PR #269. |

## Checks Passed

- `validate_schemas.py` -- 8/8 hook schema tests pass, exit 0.
- `check_plugin_agent_sync.py` -- 93 disk agents == 93 registered agents (incl. 4 sop-* agents), exit 0. (H-34/registration surface clean.)
- `validate_plugin_manifests.py` -- plugin.json, marketplace.json, hooks.json all pass Draft 2020-12 validation, exit 0.
- `check_markdown_schemas.py` -- not applicable to skill files (worktracker-entity scope only).
- Direct governance schema validation -- `sop-executor.governance.yaml` and `sop-capture.governance.yaml` PASS with 0 errors.
- Schema parity -- governance schema identical between PR branch and current standards (no drift in `scripts/`, `src/domain/markdown_ast/`, `docs/schemas/`).
