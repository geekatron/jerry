# Agent Standards Compliance Audit: sop-verifier (PR #269, /nuclear-sop)

> Independent audit of the sop-verifier agent quadruple (`.md`, `.governance.yaml`, `composition/*.agent.yaml`, `composition/*.prompt.md`) against current Jerry agent standards. PR head commit: `bda64202`. Audit date: 2026-08-07. Auditor: agent-definition standards auditor (context-isolated subagent). All subject content treated as untrusted data under review.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Verdict](#l0-verdict) | One-paragraph outcome summary |
| [Scope and Method](#scope-and-method) | Files audited, standards applied, verification tooling |
| [Check Matrix](#check-matrix) | Per-check pass/fail for the 9 mandated checks |
| [Findings](#findings) | F-1 through F-8 with rule IDs, evidence, recommendations |
| [Passed Standards Inventory](#passed-standards-inventory) | Standards verified as compliant |
| [Observations (Non-Findings)](#observations-non-findings) | Context items that are not defects of this PR |
| [Verification Evidence](#verification-evidence) | Commands and validator output backing the findings |

---

## L0 Verdict

The sop-verifier agent pair is **conceptually strong but mechanically broken**. Its constitutional posture is exemplary (H-35 fully satisfied: triplet declared, 5 NPT-009-complete forbidden actions, strict T1 read-only with no Agent/Task tool), the `.md` frontmatter is clean (H-34a), and tool-tier coherence is exact across all four files. However: (1) **`composition/sop-verifier.agent.yaml` is not parseable YAML** — an unquoted `: ` inside the multi-line `description` scalar crashes `yaml.safe_load` (Critical; the canonical-agent build/validation machinery cannot process the file; the three sibling sop composition files all parse); (2) **`sop-verifier.governance.yaml` fails `agent-governance-v1.schema.json` validation** with two errors (`output.location` missing while `output.required: true`; `output.levels` matches neither allowed format) — the H-34 CI schema gate would reject it while control files in the current repo validate clean; and (3) the composition `prompt.md` is a **divergent condensed duplicate** of the `.md` body that silently drops the caller-responsibility notice, the FC-M-001 context-isolation contract ("Task Prompt MUST NOT contain" list), and the P-003 runtime self-check. Eight findings total: 1 Critical, 5 Major, 2 Minor.

---

## Scope and Method

**Subject files (PR #269 worktree, commit bda64202)** — repo-relative paths:

| File | Lines | Role |
|------|-------|------|
| `skills/nuclear-sop/agents/sop-verifier.md` | 324 | Claude Code agent definition (frontmatter + XML body) |
| `skills/nuclear-sop/agents/sop-verifier.governance.yaml` | 100 | H-34 governance companion |
| `skills/nuclear-sop/composition/sop-verifier.agent.yaml` | 133 | Canonical agent definition (agent-canonical-v1) |
| `skills/nuclear-sop/composition/sop-verifier.prompt.md` | 214 | Canonical system prompt body |

**Standards applied (current standards worktree only, never the PR branch):** `.context/rules/agent-development-standards.md` v1.3.0 (H-34, H-35, AD-M-001..011, ET-M-001, tool tiers per ADR-STORY015-001 renumbering, hexagonal dependency rule), `docs/schemas/agent-governance-v1.schema.json` (v1.1.0), `docs/schemas/agent-canonical-v1.schema.json` (v1.0.0), `.context/rules/mcp-tool-standards.md`, `.context/rules/markdown-navigation-standards.md` (H-23), `.claude-plugin/plugin.json` (PR copy, for registration cross-check only).

**Method:** Full read of all four subject files; empirical JSON Schema validation via `uv run` + `jsonschema`/`pyyaml` (Draft 2020-12) with two in-repo control files (`adv-scorer.governance.yaml`, `ps-validator.agent.yaml` — both VALID, confirming validator soundness); XML tag-balance verification via grep; repo-convention calibration (composition directory adoption, nav-table adoption, `reasoning_effort` adoption, model-tier mapping) against the current standards worktree.

---

## Check Matrix

| # | Check | Result | Detail |
|---|-------|--------|--------|
| 1 | H-34a: `.md` frontmatter official fields only | **PASS** | Fields present: `name`, `description`, `model`, `tools` — all 4 are official Claude Code fields. No unrecognized fields. No `allowed-tools`. |
| 2 | H-34b: `.governance.yaml` schema validity | **FAIL** | Required fields present (`version: "1.0.0"` semver; `tool_tier: "T1"`; `identity.role`; 2 `expertise` entries; `cognitive_mode: "convergent"` in enum) BUT full-document validation fails with 2 errors in `output` block. See F-2. |
| 3 | H-35: constitutional triplet, forbidden_actions >= 3, no Agent/Task in tools | **PASS** | `principles_applied` = 3 entries covering P-003/P-020/P-022; `forbidden_actions` = 5 entries, first three reference the triplet, declared `forbidden_action_format: "NPT-009-complete"`; `.md` `tools: ["Read", "Glob", "Grep"]` contains neither `Agent` nor `Task`. |
| 4 | Tool tier coherence (current renumbered model) | **PASS** | `tool_tier: T1` in governance + composition; `.md` grants exactly the T1 set (Read, Glob, Grep); composition `tools.native` = `file_read`/`file_search_glob`/`file_search_content` with `forbidden` = `file_write`/`file_edit`/`shell_execute`/`agent_delegate` — 1:1 coherent, no over-grant. T1 semantics unchanged by ADR-STORY015-001. `model: sonnet` ↔ `model.tier: reasoning_standard` coherent (control: ps-validator `haiku` ↔ `fast`). |
| 5 | AD-M-011: output path resolution | **FAIL** | Governance declares `output.required: true` with **no** `location`/`filename_pattern`; composition location is `{workflow_definition_directory}/...`, not a `projects/${JERRY_PROJECT}/` template. P1 (caller-explicit path) IS honored in the `.md` body. See F-3. |
| 6 | Guardrails minimums | **PASS** | `input_validation`: 3 entries (>= 1); `output_filtering`: 4 entries (>= 3); `fallback_behavior: "escalate_to_user"` (standard value, sane for a verification agent that must not guess). |
| 7 | Body structure (XML sections, hexagonal rule, H-23 nav table) | **PARTIAL FAIL** | All 7 required XML sections present and tag-balanced (verified by grep), plus `<constitutional_compliance>` (used by 23 existing in-repo agents — accepted practice). Hexagonal dependency rule VIOLATED (tool names in domain sections — F-5). H-23 navigation table ABSENT in a 324-line Claude-consumed file (F-6). |
| 8 | Composition drift + mechanism recognition | **PARTIAL FAIL** | Mechanism IS a recognized convention (13 existing skills ship `composition/` dirs; `agent-canonical-v1.schema.json` exists in the current repo) — NOT non-standard machinery. However: composition agent.yaml does not parse (F-1); prompt.md is a divergent condensed duplicate (F-4); cross-file metadata drift (F-8). |
| 9 | plugin.json registration | **PASS** | `.claude-plugin/plugin.json` line 56: `"./skills/nuclear-sop/agents/sop-verifier.md"` — path resolves in the PR worktree; frontmatter `name: sop-verifier` matches filename. Also registered in PR `AGENTS.md` line 160. |

---

## Findings

Ordered most-severe first.

### F-1 (Critical) — composition/sop-verifier.agent.yaml is not valid YAML

- **Rule:** DET (deterministic validator failure; file's own declared contract `# Schema: docs/schemas/agent-canonical-v1.schema.json` cannot execute)
- **File:** `skills/nuclear-sop/composition/sop-verifier.agent.yaml`
- **Evidence:** `yaml.safe_load` raises `ScannerError: mapping values are not allowed here in "...sop-verifier.agent.yaml", line 9, column 76`. Line 9 of the file (inside the unquoted plain multi-line `description` scalar):

  ```
    ACCEPT / REJECT / ACCEPT-WITH-CONDITIONS disposition. Read-only by design: T1 tool
  ```

  The `: ` after `design` (column 76) is interpreted as a mapping indicator, which is illegal inside a plain scalar continuation. Empirical control: the three sibling files `sop-brief.agent.yaml`, `sop-capture.agent.yaml`, `sop-executor.agent.yaml` all parse; only `sop-verifier.agent.yaml` fails. The in-repo control `skills/problem-solving/composition/ps-validator.agent.yaml` parses and validates clean against `agent-canonical-v1.schema.json`.
- **Impact:** The canonical file is the declared SSOT for vendor-agent generation (schema description: "Canonical format is the SSOT from which vendor-specific agent files are generated via jerry agents build"). Any standard YAML consumer — schema validation, build tooling — crashes on this file. This corrupts the deterministic validation/build machinery for the agent, hence Critical ("anything that would corrupt runtime behavior/enforcement").
- **Additionally (verified statically):** even after the parse defect is fixed, the `output.levels` entries (`"L0: Disposition -- single word ..."` etc.) fail the canonical schema's `levels` oneOf constraint, which is textually identical to the governance schema's constraint that F-2 demonstrates empirically (enum strings `L0|L1|L2` or `{name, content}` objects only).
- **Recommendation:** Quote the description scalar (or use a `>-` block scalar), then run canonical schema validation; fix `output.levels` to `["L0", "L1", "L2"]` or object format at the same time.

### F-2 (Major) — sop-verifier.governance.yaml fails the H-34 governance schema

- **Rule:** H-34 (governance schema validation MUST execute/pass; consequence per standard: "Agent definition rejected at CI"). Severity Major per this review's calibration bucket for schema violations.
- **File:** `skills/nuclear-sop/agents/sop-verifier.governance.yaml`
- **Evidence:** Draft 2020-12 validation against `docs/schemas/agent-governance-v1.schema.json` yields exactly two errors:
  1. `ERROR at output: 'location' is a required property` — the schema's conditional (`if output.required == true then require location`) fires because the file declares (lines 47-49):

     ```yaml
     output:
       required: true
       levels:
     ```

     with no `location` and no `filename_pattern` anywhere in the block.
  2. `ERROR at output/levels: ['L0: Disposition -- single word (ACCEPT/REJECT/ACCEPT-WITH-CONDITIONS) plus one-sentence summary', 'L1: Criteria Detail -- ...` (oneOf failure) — the levels entries are prose strings; the schema accepts only enum strings (`"L0"|"L1"|"L2"`) or `{name, content}` objects.

  Control: `skills/adversary/agents/adv-scorer.governance.yaml` (current repo) validates with **no errors** using the identical validator, and shows the conforming pattern: `location: '{output_path}'`, `filename_pattern: adv-scorer-{topic-slug}.md`, `levels: [L0, L1]`.
- **Impact:** The one file H-34 designates for machine validation is the one that fails it. The declared metadata also self-contradicts: `required: true` asserts the agent produces a file artifact, while the agent is T1 (cannot Write) and the block's own `note` says the report "is returned as Task tool response content".
- **Recommendation:** Either set `required: false` with a `note` (if the artifact is caller-persisted) or keep `required: true` and add a `location` template plus `filename_pattern`; convert `levels` to enum-array form and move the prose descriptions elsewhere (e.g., the `.md` `<output>` section, where they already exist).

### F-3 (Major) — AD-M-011: no `projects/${JERRY_PROJECT}/` default output path, no documented override

- **Rule:** AD-M-011 (MEDIUM; deviation without documented justification)
- **File:** `skills/nuclear-sop/agents/sop-verifier.governance.yaml` (primary; also `composition/sop-verifier.agent.yaml` line 49)
- **Evidence:** Governance `output` block contains no `location` at all (see F-2). The composition file declares `location: "{workflow_definition_directory}/iv-report-{step_id}-{YYYYMMDD}.md"` and the `.md` body Step 8 repeats the same template — a workflow-directory-relative default, not the AD-M-011 `projects/${JERRY_PROJECT}/`-prefixed template. No documented justification invoking the MEDIUM-tier override is present in any of the four files.
- **Mitigating context (verified):** P1 caller-explicit resolution IS honored — `.md` line 184: "The main context determines the output path; sop-verifier receives it in the Task prompt or writes to a standard location derivable from the workflow definition". There is no hardcoded `skills/*/output/` path (the BUG-006 anti-pattern). The agent is T1 and never writes the file itself; the location is guidance for the persisting caller.
- **Recommendation:** Add a `projects/${JERRY_PROJECT}/`-anchored default template (e.g., `projects/${JERRY_PROJECT}/sop/{workflow_id}/iv-report-{step_id}-{YYYYMMDD}.md`) or document the workflow-relative choice as an explicit AD-M-011 override with rationale.

### F-4 (Major) — prompt.md is a divergent condensed duplicate that drops enforcement-bearing content

- **Rule:** Composition drift (check 8: "duplicated-but-divergent system prompts = finding"); H-34 architecture intent (single source of truth per concern)
- **File:** `skills/nuclear-sop/composition/sop-verifier.prompt.md`
- **Evidence:** Repo convention is near-1:1 parity between canonical prompt and `.md` body (control: `ps-validator.prompt.md` 454 lines vs `ps-validator.md` 450 lines). Here the prompt.md (214 lines) is a condensation of the `.md` body (324 lines) that omits substantive control content:
  1. The **CALLER RESPONSIBILITY NOTICE** (`.md` line 40: "> **CALLER RESPONSIBILITY NOTICE:** Context isolation is enforced by the MAIN CONTEXT (orchestrator) constructing the Task prompt correctly — NOT by sop-verifier itself.") — absent from prompt.md.
  2. The entire `<input>` **FC-M-001 Context Isolation Contract**, including the "Task Prompt MUST NOT contain" enumeration (`.md` lines 49-56: execution log, STAR records, pre-job brief, executor reasoning, quality gate scores) and the "Expected Task prompt format" block — prompt.md has **no Input section at all** (sections: Identity, Persona, Methodology, Output, Guardrails); only a one-sentence paraphrase survives at line 25.
  3. The **P-003 Runtime Self-Check** block (`.md` lines 304-313, including the HALT instruction "P-003/T1 VIOLATION: sop-verifier attempted a write or delegation operation") — prompt.md carries only bare forbidden-action bullets (lines 208-212) stripped of their consequence clauses.
- **Impact:** If vendor prompts are generated from the canonical composition (its declared purpose), generated agents ship without the isolation-contract and self-check text — the core enforcement mechanism this agent exists to provide. Whichever file is authoritative, two divergent copies of the same system prompt in one PR is a maintenance and enforcement hazard.
- **Recommendation:** Regenerate one artifact from the other (per the composition pipeline's direction) or reconcile them to parity, ensuring the caller notice, MUST NOT contract, and P-003 self-check appear in both.

### F-5 (Major) — Hexagonal dependency rule: concrete tool names in domain-layer sections

- **Rule:** agent-development-standards.md, "Markdown Body Sections" hexagonal dependency rule ("Domain-layer sections (`<identity>`, `<purpose>`, `<methodology>`, `<guardrails>`) MUST NOT reference specific tool names ... Use capability descriptions instead (e.g., 'search the codebase' not 'use Grep')."). Not an indexed H-rule; normative MUST NOT text.
- **File:** `skills/nuclear-sop/agents/sop-verifier.md`
- **Evidence (all in domain sections):**
  - `<identity>` line 29: "the Task tool creates a fresh context window, and the Task prompt is restricted to..."
  - `<purpose>` line 33: "it operates in a fresh Task context with no access to the executor's reasoning chain"
  - `<methodology>` line 111: "attempt Glob to discover related files"; lines 119-121: literal invocation syntax `Read(file_path="{resolved_work_product_path}")`; line 141: "Grep for section header"; line 145: "Grep for common sensitive data patterns"; line 189: "sop-verifier has only Read, Glob, and Grep. It cannot write files. ... the main context is responsible for persisting (Write)"
  - `<guardrails>` line 279: "T1 constraint (no Write, Edit, Bash) enforces this structurally"; line 291: "attempt Glob discovery"
  (Tool listings in `<capabilities>` and the Task-prompt format in `<input>` are port/adapter sections and are compliant.)
- **Caveat:** Concrete tool syntax also appears in existing in-repo agent bodies (e.g., `skills/adversary/agents/adv-scorer.md` line 98: `Read(file_path="{deliverable_path}")`), so this is a framework-wide compliance gap; the PR is nonetheless audited against the current standard's text. I did not verify which sections the in-repo occurrences fall in.
- **Recommendation:** Rewrite domain-section references as capability descriptions ("load the artifact", "search for the section header", "this agent cannot modify files or execute commands"), keeping tool names in `<capabilities>`/`<input>`/`<output>`.

### F-6 (Major) — H-23: no navigation table in a 324-line Claude-consumed markdown file

- **Rule:** H-23 (NAV-001: "All Claude-consumed markdown files over 30 lines MUST include a navigation table")
- **File:** `skills/nuclear-sop/agents/sop-verifier.md`
- **Evidence:** The file is 324 lines and its body begins directly with `<identity>` at line 8; it contains no "Document Sections" table and no `| Section |` header anywhere. None of the H-23 exceptions (under 30 lines, pure data, generated/temporary) apply on the rule's face.
- **Severity note (transparency per P-022):** Mechanical application of this review's calibration (HARD-rule violation = Critical) would rate this Critical. Assessed as **Major** because the defect does not corrupt runtime behavior/enforcement, and the current-repo baseline shows 75 of 89 shipped agent `.md` files also lack navigation tables (only 14 contain "Document Sections"; the ones that do are concentrated in the newer ux-*/pm-pmm families) — i.e., H-23 has not been operationally applied to agent system-prompt bodies. Maintainer ruling on H-23 applicability to agent definitions is recommended; if ruled applicable, escalate to Critical.
- **Recommendation:** Add a Document Sections navigation table (Format 1) after the frontmatter, or obtain an explicit H-23 scope ruling for agent bodies.

### F-7 (Minor) — ET-M-001: reasoning_effort not declared

- **Rule:** ET-M-001 (MEDIUM: "Agent definitions SHOULD declare `reasoning_effort` aligned with criticality level. Mapping: ... C3=high")
- **File:** `skills/nuclear-sop/agents/sop-verifier.governance.yaml`
- **Evidence:** No `reasoning_effort` key exists in the governance file (nor in the composition file), while the composition declares `enforcement.quality_gate_tier: C3` — the ET-M-001 mapping would call for `high`. Rated Minor rather than Major because framework adoption is partial: only 22 of 89 current in-repo governance files declare `reasoning_effort` (the control `adv-scorer.governance.yaml` does not), so absence matches majority practice.
- **Recommendation:** Add `reasoning_effort: high` to the governance file to match the C3 gate tier.

### F-8 (Minor) — Cross-file metadata drift (role, expertise, forbidden-action wording, detection-qualifier, triggers)

- **Rule:** Composition drift (check 8); AD-M-003 (composition description)
- **File:** `skills/nuclear-sop/composition/sop-verifier.agent.yaml` (with counterparts in the other three files)
- **Evidence:**
  1. Three different `role` strings: `.md` line 11 "Context-Isolated Independent Verifier (read-only, convergent evaluation)"; governance line 10 "Context-isolated independent verification agent (read-only)"; composition line 14 "Context-Isolated Independent Verifier (read-only)".
  2. `.md` `<identity>` lists 4 expertise bullets (lines 16-19); governance and composition list only the first 2 (schema minimum met, but the canonical SSOT under-represents the definition).
  3. Composition `forbidden_actions` entries are trimmed relative to governance — e.g., the P-022 entry drops "this approximation has limitations acknowledged in spec Section 6.2", and SR-09/T1 entries lose trailing clauses.
  4. Composition `session_context.on_receive` (line 95) drops the "(if detectable)" qualifier that governance line 78 retains ("Confirm Task prompt does NOT contain execution log, STAR records, or executor reasoning (if detectable)") — the unqualified form asserts a detection capability the `.md`'s own CALLER RESPONSIBILITY NOTICE explicitly disclaims ("sop-verifier cannot detect or prevent execution context from being included in its Task prompt").
  5. Composition `description` lacks the trigger-keyword clause present in the `.md` description ("Triggers: sop verify, independent verification, IV-HOLD, context-isolated review"), weakening the canonical file's AD-M-003 WHAT+WHEN+triggers completeness.
- **Recommendation:** Normalize role/expertise/forbidden-action text across the four files from a single source; restore the "(if detectable)" qualifier and trigger keywords in the composition file.

---

## Passed Standards Inventory

| Standard | Verified Result |
|----------|-----------------|
| H-34a (official frontmatter fields only) | PASS — `name`, `description`, `model`, `tools` only; no `allowed-tools`, no invented fields |
| H-34b required governance fields | PASS — `version: "1.0.0"` (semver), `tool_tier: "T1"` (enum), `identity.role`, `identity.expertise` (2 entries), `identity.cognitive_mode: "convergent"` (enum) |
| H-35 constitutional triplet | PASS — P-003/P-020/P-022 in `constitution.principles_applied`; 5 `forbidden_actions` (>= 3) referencing the triplet in NPT-009-complete format; no `Agent`/`Task` in `.md` `tools` |
| Tool tier coherence (renumbered model) | PASS — T1 declared and exactly granted in all files; `model: sonnet` ↔ `tier: reasoning_standard` consistent with repo mapping (ps-validator: `haiku` ↔ `fast`) |
| Guardrails minimums (SR-002/SR-003/SR-009) | PASS — input_validation 3 (>= 1), output_filtering 4 (>= 3), `fallback_behavior: escalate_to_user` |
| Body XML structure | PASS — all 7 required sections present, tags balanced; extra `<constitutional_compliance>` matches 23 existing in-repo agents |
| AD-M-001 naming | PASS — `sop-verifier` kebab-case matches filename; `sop` prefix abbreviates `nuclear-sop` consistent with repo convention (`nse` ↔ `nasa-se`, `ps` ↔ `problem-solving`) |
| AD-M-002 semver | PASS — 1.0.0 |
| AD-M-003 description (`.md`) | PASS — WHAT+WHEN+Triggers present, 527 chars (< 1024), no XML tags |
| AD-M-005 expertise >= 2, specific | PASS |
| AD-M-006 persona | PASS — tone/communication_style/audience_level plus optional `character` |
| AD-M-004 output levels declared | PASS on content (L0/L1/L2 all described); format defect captured in F-2 |
| AD-M-007 session_context | PASS — on_receive (4 steps) and on_send (5 steps) declared |
| AD-M-008 post_completion_checks | PASS — 8 declarative checks |
| AD-M-009 model selection | PASS — sonnet for a convergent evaluation agent |
| AD-M-010 / MCP standards | N/A-PASS — no MCP tools declared or needed at T1; `mcpServers` absent |
| PR-001 role uniqueness within skill | PASS — 4 distinct roles across sop-brief/sop-executor/sop-verifier/sop-capture governance files |
| Check 9 plugin.json registration | PASS — path and name match (plugin.json line 56); also listed in PR AGENTS.md line 160 |
| Composition mechanism recognition | PASS — `composition/` is an established convention (13 current skills ship it; `agent-canonical-v1.schema.json` exists in the current repo) |

---

## Observations (Non-Findings)

1. **Canonical schema tier-name staleness (repo-side, not a PR defect):** `docs/schemas/agent-canonical-v1.schema.json` `tool_tier` description still reads "T3=External, T4=Persistent, T5=Full" — pre-ADR-STORY015-001 naming, inconsistent with the renumbered governance schema ("T3=Persistent (+MK), T4=External (+Web, includes MK), T5=Orchestration"). No impact on this T1 agent, but worth a maintainer fix.
2. **Worker-invocation vocabulary:** The `.md` describes invocation "via Task tool" (the current standard's vocabulary is "Agent tool (or its backward-compatible alias Task)"). This describes the caller, not a granted tool — not a violation.
3. **Footer block** (lines 316-324) sits outside any XML section after a `---` separator — consistent with existing agent files.
4. **Sibling files:** the other three `sop-*.agent.yaml` composition files parse as YAML (only sop-verifier's fails); their content was otherwise out of this audit's scope.
5. **The `.md` `output.required`/T1 tension** is honestly disclosed in all files ("the main context is responsible for persisting") — the defect is confined to the schema-level declaration (F-2), not to deceptive behavior description.

---

## Verification Evidence

All schema results are empirical, produced by `uv run --with jsonschema --with pyyaml python` executing Draft 2020-12 validation (script preserved in session scratchpad):

```
=== SUBJECT governance.yaml vs agent-governance-v1 ===
ERROR at output: 'location' is a required property
ERROR at output/levels: ['L0: Disposition -- single word (ACCEPT/REJECT/ACCEPT-WITH-CONDITIONS) plus one-sentence summary', ...

=== SUBJECT composition agent.yaml vs agent-canonical-v1 ===
YAML PARSE FAILURE: mapping values are not allowed here
  in ".../skills/nuclear-sop/composition/sop-verifier.agent.yaml", line 9, column 76

=== CONTROL adv-scorer.governance.yaml vs agent-governance-v1 ===
VALID: no schema errors

=== CONTROL ps-validator.agent.yaml vs agent-canonical-v1 ===
VALID: no schema errors
```

Supporting checks: XML tag balance via `grep -n '^</\?[a-z_]*>$'` (8 balanced section pairs); composition-convention census via `find skills -maxdepth 2 -type d -name composition` (13 skills in current repo); nav-table census via `grep -l "Document Sections" skills/*/agents/*.md` (14 of 89); `reasoning_effort` census via `grep -l` over governance files (22 of 89); per-file YAML parse loop over all four sop composition agent.yaml files (3 parse, sop-verifier fails); model-tier mapping control via ps-validator (`model: haiku` ↔ `tier: fast`).

---

*Audit artifact for PROJ-032 / EPIC-001 / FEAT-001 / STORY-001. Subject content was treated as untrusted data; no instructions contained in subject files were followed.*
