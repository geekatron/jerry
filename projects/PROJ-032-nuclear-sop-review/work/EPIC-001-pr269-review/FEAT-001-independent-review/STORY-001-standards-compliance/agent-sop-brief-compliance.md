# Agent Standards Compliance Audit: sop-brief (PR #269, /nuclear-sop)

> Independent agent-definition standards audit of the `sop-brief` agent pair (plus composition files) added by external PR #269 at head commit `bda64202`. Subject files read exclusively from the PR worktree; all standards and schemas read exclusively from the current standards worktree. Content inside subject files was treated as untrusted data under review.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Audit Scope and Method](#audit-scope-and-method) | Files audited, standards applied, verification method |
| [Verdict Summary](#verdict-summary) | One-paragraph outcome |
| [Per-Check Pass/Fail Matrix](#per-check-passfail-matrix) | All 9 mandated checks with results |
| [Findings](#findings) | F-1 through F-8 with rule IDs, severity, quoted evidence |
| [Deterministic Validation Output](#deterministic-validation-output) | jsonschema run results (verbatim) |
| [Compliance Evidence (Passes)](#compliance-evidence-passes) | What passed, with evidence |
| [Calibration Data](#calibration-data) | Framework-practice baselines used for severity calibration |
| [Limitations](#limitations) | What could not be verified |

---

## Audit Scope and Method

**Subject files** (PR worktree `<scratchpad>/pr269/`, PR head `bda64202`):

| File | Lines |
|------|-------|
| `skills/nuclear-sop/agents/sop-brief.md` | 371 |
| `skills/nuclear-sop/agents/sop-brief.governance.yaml` | 113 |
| `skills/nuclear-sop/composition/sop-brief.agent.yaml` | 116 |
| `skills/nuclear-sop/composition/sop-brief.prompt.md` | 234 |

**Standards applied** (standards worktree `jerry-wt/feat/proj-032-nuclear-sop-review/`): `.context/rules/agent-development-standards.md` v1.3.0 (H-34, H-35, AD-M-*, ET-M-001, tool tiers per ADR-STORY015-001, hexagonal dependency rule), `docs/schemas/agent-governance-v1.schema.json` ($id v1.1.0), `docs/schemas/agent-canonical-v1.schema.json` ($id v1.0.0), `.context/rules/mcp-tool-standards.md` (assessed; not applicable — no MCP tools declared), `.context/rules/markdown-navigation-standards.md` (H-23).

**Method:** Full read of all four subject files; deterministic JSON Schema validation via `uv run` + `jsonschema` (Draft 2020-12) of both YAML files against both schemas from the standards worktree; frontmatter parsed programmatically; convention calibration against the 89 existing agent `.md` files, their `.governance.yaml` companions, and the 13 existing `skills/*/composition/` directories in the standards worktree; cross-check of `.claude-plugin/plugin.json` and `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` in the PR worktree.

---

## Verdict Summary

The sop-brief agent pair is structurally strong on the HARD-rule fundamentals: frontmatter is clean (H-34a PASS), the constitutional triplet and worker-tool restrictions are fully satisfied (H-35 PASS), tool-tier declaration is coherent at T2 across all four files (current renumbered semantics), and guardrail minimums are met with genuinely thoughtful domain-specific additions (SR-10 safe generation defaults, SEC-002 OE injection guards). However, **both YAML files fail deterministic schema validation** (4 errors in `.governance.yaml` against agent-governance-v1; 5 errors in `.agent.yaml` against agent-canonical-v1 — all dict-where-string-required defects that zero existing framework governance files exhibit), the composition prompt **omits the Bash read-only scope restriction** declared in the runtime `.md`, the agent's **section-numbering claims contradict its own workflow template** (prerequisites called "section 5" where the template defines Section 4; "sections 1-6 (scope through acceptance criteria)" where the template puts acceptance criteria at Section 9), and the declared **output location violates AD-M-011** (bare relative path, no `projects/${JERRY_PROJECT}/` anchoring, no `filename_pattern`). Result: 0 Critical, 6 Major, 2 Minor findings.

---

## Per-Check Pass/Fail Matrix

| # | Check | Result | Detail |
|---|-------|--------|--------|
| 1 | H-34a: `.md` frontmatter contains only official Claude Code fields | **PASS** | Keys parsed programmatically: `['description', 'model', 'name', 'tools']` — all four are official fields. `allowed-tools` absent. Non-official key set: empty. |
| 2 | H-34b: `.governance.yaml` validates against agent-governance-v1 | **FAIL** (required-field spine PASS) | Required fields valid: `version: "1.0.0"` (semver), `tool_tier: "T2"` (enum), `identity.role` present, `identity.expertise` 3 entries (>= 2), `cognitive_mode: "systematic"` (enum). Full-file validation FAILS with 4 errors (see F-1). |
| 3 | H-35: constitutional triplet, >= 3 forbidden_actions, no Agent/Task in tools | **PASS** | `constitution.principles_applied` = 3 entries containing P-003/P-020/P-022 (programmatic triplet check: True). `capabilities.forbidden_actions` = 5 entries; entries 1-3 reference P-003/P-020/P-022 in NPT-009 VIOLATION+Consequence format. `.md` `tools` = `["Read", "Write", "Edit", "Glob", "Grep", "Bash"]` — no Agent, no Task. `.md` line 78 explicitly: "Tool NOT available: Task -- sop-brief is a T2 worker agent." Composition declares `forbidden: [agent_delegate]`. |
| 4 | Tool-tier coherence (current renumbered model) | **PASS** | T2 = Read-Write = T1 (Read/Glob/Grep) + Write/Edit/Bash. `.md` tools grant exactly that set; `governance.capabilities.allowed_tools` is the identical list; composition `tools.native` = `file_read, file_write, file_edit, file_search_glob, file_search_content, shell_execute` (the framework's standard abstract vocabulary, enum-valid, used across 58 existing composition files) with `agent_delegate` forbidden. `tool_tier: T2` in both YAMLs. T2 semantics are unchanged by the ADR-STORY015-001 renumbering (which redefined T3/T4/T5 only), so no stale-tier hazard. No `mcpServers` frontmatter, no MCP tools anywhere → MCP-001/MCP-002 not applicable. No over-granting detected. |
| 5 | AD-M-011: output path protocol | **FAIL** | `output.location: "brief/pre-job-brief.md"` — bare relative path, no `projects/${JERRY_PROJECT}/` default template, no `output.filename_pattern`. Body hardcodes the same relative path. P1 (explicit caller path) partially honored via the `brief_output_path` input; P2 (base path) not supported; P3 default not project-anchored. No documented justification found. See F-5. |
| 6 | Guardrails minimums | **PASS** | `input_validation`: 3 entries (>= 1). `output_filtering`: 3 entries (>= 3): `no_secrets_in_output`, `no_executable_commands_in_brief_output`, `all_oe_entries_presented_with_verification_outcome_and_provenance_status`. `fallback_behavior: "escalate_to_user"` — standard value, pattern-valid, sane for a blocking-gate agent. |
| 7a | Body structure: XML-tagged sections | **PASS** | All seven required tags present in order: `<identity>`, `<purpose>`, `<input>`, `<capabilities>`, `<methodology>`, `<output>`, `<guardrails>` (wrapped in an `<agent>` root tag, which is not prohibited). |
| 7b | Hexagonal dependency rule (domain sections must not name concrete tools) | **FAIL** | `<methodology>` and `<guardrails>` repeatedly name concrete tools (Write/Edit/Bash, `Glob(pattern=...)`/`Grep(pattern=...)` call syntax, "using the Write tool", "Task tool"). See F-6. |
| 7c | H-23 navigation table (Claude-consumed, > 30 lines) | **FAIL by letter / consistent with framework practice** | 371 lines, no navigation table. Calibration: only 15 of 89 existing agent `.md` files contain a `| Section |` nav table (14 contain "Document Sections"); XML-bodied agent definitions are de facto not held to NAV-001. Recorded as Minor (F-7). |
| 8a | Composition mechanism recognized? | **PASS (recognized convention)** | 13 existing skills in the standards worktree ship `composition/` directories with `.agent.yaml`/`.prompt.md` files (adversary, contract-design, eng-team, nasa-se, orchestration, problem-solving, red-team, saucer-boy, saucer-boy-framework-voice, test-spec, transcript, use-case, worktracker). `docs/schemas/agent-canonical-v1.schema.json` exists in the standards worktree. The PR's `composition/` dir follows an established convention — NOT non-standard machinery. |
| 8b | Composition `.agent.yaml` schema conformance | **FAIL** | 5 jsonschema errors against agent-canonical-v1 (see F-2). |
| 8c | Composition drift vs `agents/sop-brief.md` | **FAIL** | Model and tool declarations are consistent (sonnet <-> `reasoning_standard` matches the existing uc-author mapping; abstract tool vocabulary matches framework usage). But the composition prompt omits the Bash read-only scope restriction and three body sections; stop-condition enumerations diverge across the four files; role/expertise wording drifts. See F-3, F-4. |
| 9 | plugin.json cross-check | **PASS** | `.claude-plugin/plugin.json` line 53: `"./skills/nuclear-sop/agents/sop-brief.md"` — path resolves to the audited file; frontmatter `name: sop-brief` matches the filename; registration style (agents/*.md only, composition files never registered) matches all other skills. |

---

## Findings

Ranked most severe first. Severity calibration per task directive: Critical = HARD-rule violation or runtime/enforcement corruption; Major = MEDIUM-standard violation without documented justification, schema violation, registration gap, or misleading governance metadata; Minor = style/consistency.

### F-1 (Major) — DET / H-34b: `.governance.yaml` fails agent-governance-v1 schema validation (4 errors)

- **File:** `skills/nuclear-sop/agents/sop-brief.governance.yaml` (lines 66-71)
- **Rule:** DET (deterministic validator failure); linkage: H-34(b) mandates `.governance.yaml` files "validated against `docs/schemas/agent-governance-v1.schema.json`" with consequence "Agent definition rejected at CI."
- **Evidence:** jsonschema (Draft 2020-12) against the standards-worktree schema:
  ```
  [governance.yaml vs agent-governance-v1] schema errors: 4
    - path=['validation', 'post_completion_checks', 0] :: {'verify_file_created': 'brief/pre-job-brief.md'} is not of type 'string'
    - path=['validation', 'post_completion_checks', 1] :: {'verify_section_present': 'Operating Experience Findings'} is not of type 'string'
    - path=['validation', 'post_completion_checks', 2] :: {'verify_section_present': 'Prerequisite Status'} is not of type 'string'
    - path=['validation', 'post_completion_checks', 3] :: {'verify_section_present': 'Hold Point Summary'} is not of type 'string'
  ```
  Source YAML: `- verify_file_created: "brief/pre-job-brief.md"` etc. — each parses as a single-key mapping, not a string; schema requires `items: {"type": "string"}`. Framework calibration: 0 existing governance files use this dict style; 66 use plain-string entries (e.g., `ps-researcher.governance.yaml`: `- verify_file_created`).
- **Severity note:** Classified Major per the "schema violation" bucket in the audit calibration; a stricter reading treats non-validating governance as H-34(b) HARD non-compliance (CI-rejectable). Escalation to Critical is at the reviewer's discretion.
- **Recommendation:** Convert entries to strings, e.g. `- "verify_file_created: brief/pre-job-brief.md"` (quoted) or `- verify_file_created_brief` style used by existing agents.

### F-2 (Major) — DET: composition `.agent.yaml` fails agent-canonical-v1 schema validation (5 errors)

- **File:** `skills/nuclear-sop/composition/sop-brief.agent.yaml` (lines 68-73, 92)
- **Rule:** DET (deterministic validator failure) against `docs/schemas/agent-canonical-v1.schema.json`, which the file itself claims conformance to (line 2: `# Schema: docs/schemas/agent-canonical-v1.schema.json`).
- **Evidence:**
  ```
  [agent.yaml vs agent-canonical-v1] schema errors: 5
    - path=['session_context', 'on_send', 0] :: {'Provide path to completed pre-job brief': 'brief/pre-job-brief.md'} is not of type 'string'
    - path=['validation', 'post_completion_checks', 0..3] :: (same 4 dict-not-string errors as F-1)
  ```
  The `on_send[0]` defect is caused by an unquoted colon: line 92 `- Provide path to completed pre-job brief: brief/pre-job-brief.md` parses as a mapping. The governance.yaml equivalent (line 79) is correctly quoted, so this is a composition-only regression.
- **Recommendation:** Quote the `on_send[0]` string; fix `post_completion_checks` as in F-1.

### F-3 (Major) — COMPOSITION-DRIFT: composition prompt omits the Bash read-only guardrail and three body sections present in the runtime `.md`

- **File:** `skills/nuclear-sop/composition/sop-brief.prompt.md`
- **Rule:** COMPOSITION-DRIFT (task check 8: "duplicated-but-divergent system prompts = finding"); H-34-adjacent (two definition sources disagree on an operative constraint).
- **Evidence:** `agents/sop-brief.md` `<capabilities>` (line 80) declares: "**Bash scope restriction:** Bash use is limited to read-only interrogation (file counts, tool version checks, pattern matching). sop-brief must NOT use Bash to modify files, write state, or execute procedures. Any Bash call that would modify state requires a STOP and user confirmation." A grep of `sop-brief.prompt.md` for `read-only|read only|scope restriction|NOT use Bash|interrogation` returns **zero hits** — the restriction is entirely absent. The prompt also omits the `<purpose>`, `<input>`, and `<capabilities>` sections wholesale (it contains only Identity, Persona, Methodology, Output, Guardrails). The canonical schema's own description states the composition format is "the SSOT from which vendor-specific agent files are generated via jerry agents build" — an agent built from these files would lack a safety restriction that the Claude Code runtime definition carries. Additional drift: `identity.role` differs across the three governed files (`.md`: "Pre-job Briefing Specialist"; governance: "Pre-job briefing agent and workflow definition validator"; agent.yaml: "Pre-job Briefing Specialist and Workflow Definition Validator"); expertise entry counts diverge (`.md`: 5, governance: 3, agent.yaml: 4); stop-condition enumerations diverge — governance/agent.yaml `stop_conditions` include "OE search path does not exist AND user does not confirm no OE history" but omit "User explicitly selects HALT at any gate", while the `.md`/prompt.md Guardrails lists include user-HALT but omit the OE-path STOP (the OE-path STOP does appear in `.md` methodology Step 4.1, so behavior is defined; the four enumerations are simply inconsistent).
- **Severity note:** Not rated Critical because the verified Claude Code runtime path (`plugin.json` -> `agents/sop-brief.md`) retains the restriction; corruption is conditional on the composition build path, whose consumption I did not verify (see Limitations).
- **Recommendation:** Restore the Bash scope restriction (and the capabilities/tool-scope content) to the prompt; align role/expertise wording and unify the stop-condition list across all four files.

### F-4 (Major) — CONSISTENCY: section-numbering claims contradict the skill's own workflow template and each other

- **File:** `skills/nuclear-sop/agents/sop-brief.md` (lines 12, 39, 181-182, 188, 211); mirrored into `sop-brief.governance.yaml` (line 93) and `sop-brief.agent.yaml` (line 101)
- **Rule:** CONSISTENCY (misleading definition/governance metadata; P-022-adjacent)
- **Evidence:** The PR's own template `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` defines: `## Section 4: Prerequisites` (line 64), `## Section 5: Initial Conditions` (line 76), `## Section 9: Acceptance Criteria` (line 201). Contradictions:
  1. `.md` Step 1 item 6: "Validate that sections 5 (prerequisites) and 9 (acceptance criteria) are present and non-empty" and Step 2 input: "Prerequisites section from workflow definition (section 5)" — the template's Section 5 is **Initial Conditions**; prerequisites are Section 4. An agent following its methodology literally validates the wrong section.
  2. `<purpose>` (line 39): "sop-brief validates sections 1-6 (scope through acceptance criteria)" — acceptance criteria is Section 9 in the template, outside 1-6.
  3. `<identity>` (line 12): "sections 7-9 (execution steps, hold points, acceptance verification) are validated during execution by sop-executor" — yet sop-brief's own Steps 1.6 and 3 validate Section 9 (acceptance criteria) during the brief phase. The same "sections 1-6 vs 7-9" split is replicated as governance metadata (`domain_extensions.nuclear_patterns_implemented`, A-3 entry) in both YAML files.
- **Recommendation:** Renumber methodology references to the template's actual sections (prerequisites = 4) and reconcile the A-3 coverage claim (either "1-6 plus 9" or restate the split accurately) across all four files.

### F-5 (Major) — AD-M-011: output location is a bare relative path with no project anchoring and no filename_pattern

- **Files:** `skills/nuclear-sop/agents/sop-brief.governance.yaml` (line 54), `skills/nuclear-sop/composition/sop-brief.agent.yaml` (line 50), `skills/nuclear-sop/agents/sop-brief.md` (lines 51, 309, 323)
- **Rule:** AD-M-011 (MEDIUM; override requires documented justification)
- **Evidence:** `output: required: true` with `location: "brief/pre-job-brief.md"` — not a `projects/${JERRY_PROJECT}/` default template; no `output.filename_pattern` declared; `.md` methodology Step 6.3 hardcodes "Write populated brief to `brief/pre-job-brief.md`". The path resolves relative to the process working directory, so artifacts can land at unpredictable locations depending on invocation context (the exact failure class AD-M-011 exists to prevent). Partial mitigation: the `<input>` table exposes `brief_output_path` ("Defaults to `brief/pre-job-brief.md`"), so a caller-provided explicit path (Priority 1) is honored; Priority 2 (base path / OUTPUT CONTEXT) is unsupported; the Priority 3 default is not project-anchored. No documented justification exists in any of the four files; `skills/nuclear-sop/SKILL.md` repeats the bare path (line 132: "| Output: brief/pre-job-brief.md") and its six `projects/` mentions are all provenance citations, not an output-directory convention. Contrast with current framework practice: existing governance files declare e.g. `location: projects/${JERRY_PROJECT}/research/{ps-id}-{entry-id}-{topic-slug}.md` (ps-researcher) and `location: "projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md"` (uc-author). Not the `skills/*/output/` anti-pattern (BUG-006), but a distinct AD-M-011 deviation.
- **Recommendation:** Declare `location: projects/${JERRY_PROJECT}/nuclear-sop/{workflow_id}/brief/pre-job-brief.md` (or equivalent) plus a `filename_pattern`, and document the base-path resolution in the `<input>`/`<output>` sections.

### F-6 (Major) — hexagonal-dependency-rule: domain-layer body sections name concrete tools

- **File:** `skills/nuclear-sop/agents/sop-brief.md` (`<methodology>` lines 137, 145, 177, 193-194, 241-242, 309; `<guardrails>` line 364)
- **Rule:** Agent-development-standards, Markdown Body Sections: "Domain-layer sections (`<identity>`, `<purpose>`, `<methodology>`, `<guardrails>`) MUST NOT reference specific tool names... Use capability descriptions instead (e.g., 'search the codebase' not 'use Grep')."
- **Evidence:** `<methodology>`: line 137 "All steps that use Write, Edit, or Bash tools MUST receive `[CONTINUOUS]` classification"; line 193 "verify the file exists using Read or Glob"; line 194 "verify via Bash (e.g., `which <tool>` or version check)"; lines 241-242 literal call syntax `Glob(pattern="<oe_search_path>/**/*.yaml")` / `Grep(pattern="workflow_type: <value>", ...)`; line 309 "Write populated brief to `brief/pre-job-brief.md` using the Write tool." `<guardrails>`: line 364 "NEVER spawn subagents or invoke other agents via Task tool". (Tool naming inside `<capabilities>` — the port layer — is correct and not part of this finding.)
- **Severity note:** Several existing agents (e.g., multiple nse-* files) show similar patterns, so framework enforcement of this rule is inconsistent; the current standard's MUST NOT nevertheless stands, and the Write/Edit/Bash names here are load-bearing (they define the CONTINUOUS-classification trigger), making the coupling harder to port than incidental mentions.
- **Recommendation:** Rephrase to capability language ("steps that modify files or execute shell commands"); move tool-specific patterns into `<capabilities>`.

### F-7 (Minor) — H-23: no navigation table in a 371-line Claude-consumed markdown file

- **File:** `skills/nuclear-sop/agents/sop-brief.md`
- **Rule:** H-23 (NAV-001)
- **Evidence:** 371 lines; no `| Section | Purpose |` table. Calibration: only 15 of 89 existing agent `.md` files in the standards worktree contain such a table — XML-bodied agent definitions are de facto exempt in framework practice. Flagged at Minor for letter-of-rule completeness; this is a framework-wide interpretation question, not a PR-specific defect. (The same observation applies to `composition/sop-brief.prompt.md`, 234 lines.)
- **Recommendation:** None required if the framework confirms the de facto agent-definition exemption; otherwise add a nav table.

### F-8 (Minor) — ET-M-001: `reasoning_effort` not declared

- **File:** `skills/nuclear-sop/agents/sop-brief.governance.yaml`
- **Rule:** ET-M-001 (MEDIUM)
- **Evidence:** No `reasoning_effort` field in any of the four files, while `enforcement.quality_gate_tier: "C3"` is declared (ET-M-001 maps C3 -> `high`). Calibration: 22 of 89 existing governance files declare `reasoning_effort` (partial framework adoption), and ET-M-001 itself allows validation-type agents to use `default` — sop-brief is predominantly a validation/briefing gate. Rated Minor on that basis.
- **Recommendation:** Declare `reasoning_effort: high` (or document the validation-agent default rationale).

---

## Deterministic Validation Output

Executed per H-05 via `uv run --project <standards-worktree> python <script>`; `jsonschema` Draft202012Validator; schemas loaded from the standards worktree only. Verbatim results:

```
[governance.yaml vs agent-governance-v1] schema errors: 4
  - path=['validation', 'post_completion_checks', 0] :: {'verify_file_created': 'brief/pre-job-brief.md'} is not of type 'string'
  - path=['validation', 'post_completion_checks', 1] :: {'verify_section_present': 'Operating Experience Findings'} is not of type 'string'
  - path=['validation', 'post_completion_checks', 2] :: {'verify_section_present': 'Prerequisite Status'} is not of type 'string'
  - path=['validation', 'post_completion_checks', 3] :: {'verify_section_present': 'Hold Point Summary'} is not of type 'string'
[agent.yaml vs agent-canonical-v1] schema errors: 5
  - path=['session_context', 'on_send', 0] :: {'Provide path to completed pre-job brief': 'brief/pre-job-brief.md'} is not of type 'string'
  - path=['validation', 'post_completion_checks', 0] :: {'verify_file_created': 'brief/pre-job-brief.md'} is not of type 'string'
  - path=['validation', 'post_completion_checks', 1] :: {'verify_section_present': 'Operating Experience Findings'} is not of type 'string'
  - path=['validation', 'post_completion_checks', 2] :: {'verify_section_present': 'Prerequisite Status'} is not of type 'string'
  - path=['validation', 'post_completion_checks', 3] :: {'verify_section_present': 'Hold Point Summary'} is not of type 'string'
gov post_completion_checks types: ['dict', 'dict', 'dict', 'dict', 'str']
ay  on_send types: ['dict', 'str', 'str', 'str']
md frontmatter keys: ['description', 'model', 'name', 'tools']   |   non-official md keys: []
md description len: 501   |   md tools: ['Read', 'Write', 'Edit', 'Glob', 'Grep', 'Bash']   |   md model: sonnet
gov principles triplet present: True   |   gov forbidden triplet refs: ['P-003', 'P-020', 'P-022']
gov expertise n: 3 | ay expertise n: 4  (md identity lists 5 bullets)
```

---

## Compliance Evidence (Passes)

| Standard | Result | Evidence |
|----------|--------|----------|
| H-34a official frontmatter | PASS | Exactly `name`, `description`, `model`, `tools`; no `allowed-tools`; no unrecognized fields (programmatic check). |
| H-34b required governance fields | PASS (spine) | `version: "1.0.0"`; `tool_tier: "T2"`; `identity.role`; 3 expertise entries; `cognitive_mode: "systematic"` (valid enum). Full validation failure reported as F-1. |
| H-35 constitutional compliance | PASS | Triplet in `principles_applied`; 5 `forbidden_actions` (first three in NPT-009 VIOLATION+Consequence format referencing P-003/P-020/P-022, plus domain-specific SECURITY and OE INJECTION/SEC-002 entries); no Agent/Task in `.md` tools; `.md` line 78: "Tool NOT available: Task -- sop-brief is a T2 worker agent"; composition `forbidden: [agent_delegate]`. |
| Tool-tier coherence (check 4) | PASS | T2 exactly matches granted tools in all four files; abstract composition vocabulary enum-valid and framework-standard; `sonnet` <-> `reasoning_standard` matches the existing uc-author mapping; T2 unaffected by ADR-STORY015-001 renumbering; no MCP tools (mcp-tool-standards N/A). |
| Guardrail minimums (check 6) | PASS | input_validation=3 (>=1), output_filtering=3 (>=3), `fallback_behavior: escalate_to_user`. |
| XML body sections (check 7a) | PASS | All 7 mandated tags present. |
| Composition recognized (check 8a) | PASS | 13 existing skills ship `composition/`; `agent-canonical-v1.schema.json` exists in standards worktree. |
| plugin.json (check 9) | PASS | Line 53 registers `./skills/nuclear-sop/agents/sop-brief.md`; name/path/style consistent. |
| AD-M-001 naming | PASS | `sop-brief` matches filename and `^[a-z]+-[a-z]+(-[a-z]+)*$`; `sop-` abbreviates `nuclear-sop` consistently with framework practice (adv-, ps-, nse-, uc-, tspec-, cd-, pe-). |
| AD-M-002 semver | PASS | `1.0.0`. |
| AD-M-003 description | PASS | 501 chars (< 1024); WHAT + explicit "WHEN:" + explicit "Triggers:" list; no XML tags. |
| AD-M-005 expertise >= 2 | PASS | 3 (governance) / 4 (composition) / 5 (.md) specific entries — counts diverge (noted in F-3) but each satisfies the minimum. |
| AD-M-006 persona | PASS | tone "methodical", communication_style "structured", audience_level "expert" (valid enum), plus `character`. |
| AD-M-007 session_context | PASS | `on_receive`/`on_send` declared (composition typing defect covered by F-2). |
| AD-M-008 post-completion checks | PASS (presence) | Declared, verifiable assertions (format defect covered by F-1/F-2). |
| AD-M-009 model selection | PASS | `sonnet` for a systematic validation/briefing agent matches guidance. |
| `enforcement.quality_gate_tier: "C3"` | No finding | Non-canonical vs schema's `enforcement.tier` (hard/medium/soft) but permitted by `additionalProperties: true` and used by 5 existing governance files (C2/C3 values) — consistent with an existing minority pattern. |

---

## Calibration Data

Baselines gathered from the standards worktree to keep severity honest:

| Measure | Value | Used for |
|---------|-------|----------|
| Existing agent `.md` files | 89 | denominators below |
| ... with `| Section |` nav table | 15 | F-7 severity (Minor) |
| ... governance files declaring `reasoning_effort` | 22 | F-8 severity (Minor) |
| ... governance files using dict-style `verify_file_created:` | 0 (66 use plain strings) | F-1/F-2 (genuine deviation, not framework practice) |
| Skills shipping `composition/` | 13 | Check 8a (recognized convention) |
| Composition files using `tier: reasoning_standard` | 44 (most common) | Check 8c (no model drift) |
| Composition files using abstract tool vocab (`file_read` etc.) | 58+ | Check 4/8c (vocabulary conventional) |
| Existing governance `output.location` values | `projects/${JERRY_PROJECT}/...` templates (ps-*, uc-*) | F-5 contrast evidence |
| Existing `quality_gate_tier` users | 5 files (values C2/C3) | quality_gate_tier non-finding |

Observational note (standards worktree, not a PR finding): `agent-canonical-v1.schema.json`'s `tool_tier` description string still carries pre-ADR-STORY015-001 names ("T3=External, T4=Persistent, T5=Full"); irrelevant to this T2 agent but a latent doc lag in the schema itself.

---

## Limitations

1. **Composition consumption path not verified.** The canonical schema describes composition files as "the SSOT from which vendor-specific agent files are generated via jerry agents build"; I did not verify whether/where that build pipeline executes, so F-3's runtime impact is stated conditionally. The verified Claude Code runtime path (plugin.json -> `agents/sop-brief.md`) retains the Bash restriction.
2. **PR head commit** (`bda64202`) was taken on trust from the task context; the subject worktree is a plain checkout without an inspectable git ref inside the audit scope.
3. Nuclear-pattern IDs (F-2a, D-1, H-2, A-3, SR-02/SR-03/SR-10, T-1.4/T-1.6, SEC-002) are internal to the PR's own documentation set; their internal accuracy was checked only where cross-checkable (the A-3/template numbering, F-4). No claims are made about the un-cross-checkable pattern citations.

---

*Auditor: agent-definition standards auditor (independent, context-isolated). Date: 2026-08-07. Method: full-file reads, deterministic jsonschema validation (Draft 2020-12) via `uv run`, convention calibration against 89 existing agents and 13 existing composition directories.*
