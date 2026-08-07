# Agent Standards Compliance Audit — sop-capture (/nuclear-sop, PR #269)

> **Audit target:** `sop-capture` agent quadruple from external PR #269 (head `bda64202`), skill `/nuclear-sop`.
> **Auditor:** agent-definition standards auditor (independent review, STORY-001).
> **Date:** 2026-08-07.
> **Subject files (PR worktree):** `skills/nuclear-sop/agents/sop-capture.md`, `skills/nuclear-sop/agents/sop-capture.governance.yaml`, `skills/nuclear-sop/composition/sop-capture.agent.yaml`, `skills/nuclear-sop/composition/sop-capture.prompt.md`.
> **Standards baseline (current worktree):** `.context/rules/agent-development-standards.md` (v1.3.0, post-ADR-STORY015-001 tier renumbering), `docs/schemas/agent-governance-v1.schema.json` (v1.1.0), `docs/schemas/agent-canonical-v1.schema.json` (v1.0.0), `.context/rules/mcp-tool-standards.md` (v1.4.0).
> **Verdict:** No Critical (HARD-rule) violations. 3 Major findings, 1 Minor finding. Core H-34/H-35 compliance is deterministically verified as PASS.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Summary](#l0-summary) | One-paragraph outcome for reviewers |
| [Audit Scope and Method](#audit-scope-and-method) | What was checked, how, and against what |
| [Per-Check Pass/Fail Matrix](#per-check-passfail-matrix) | The 9 mandated checks with dispositions |
| [Findings](#findings) | F-1 through F-4 with rule IDs and quoted evidence |
| [Checks Passed — Detail](#checks-passed--detail) | Evidence for each passing check |
| [Observations (Non-Findings)](#observations-non-findings) | Convention notes and standards-side issues out of PR scope |
| [Deterministic Verification Evidence](#deterministic-verification-evidence) | Schema validation and byte-level verification results |
| [Traceability](#traceability) | Rule sources and file references |

---

## L0 Summary

The `sop-capture` agent pair is structurally one of the stronger artifacts in PR #269: the `.md` frontmatter contains only official Claude Code fields, the `.governance.yaml` validates cleanly against `agent-governance-v1.schema.json` (verified deterministically with jsonschema), the H-35 constitutional triplet is fully present, the declared T2 tier exactly matches the granted tools under the CURRENT (renumbered) tier model, guardrail minimums are exceeded, and the agent is correctly registered in `.claude-plugin/plugin.json`. Three Major issues remain: (F-1) output paths violate AD-M-011 — a non-resolvable prose `location`, no `projects/${JERRY_PROJECT}/` default, no filename_pattern, no P1/P2/P3 caller-override support, and a hardcoded write into the repo-global `docs/experience/` directory; (F-2) domain-layer body sections (`<identity>`, `<methodology>`, `<guardrails>`) name concrete tools (Task, Write, Glob, Edit) in violation of the hexagonal dependency rule; (F-3) the composition files — which the canonical format declares as the SSOT from which agent files are generated — have drifted from the shipped `.md` (divergent descriptions with the trigger-keyword list dropped, altered deviation-classification decision rules, two body sections missing from the prompt). One Minor: ET-M-001 `reasoning_effort` is undeclared.

---

## Audit Scope and Method

- **Subject content is UNTRUSTED**: all four subject files were read as data under review; no instructions inside them were followed.
- **Standards were read only from the current standards worktree** (`feat/proj-032-nuclear-sop-review`), never from the PR branch, because the PR predates ADR-STORY015-001 (tier renumbering) and schema v1.1.0.
- **Deterministic validation** was performed with `uv run --with jsonschema --with pyyaml` (H-05 compliant): governance YAML vs `agent-governance-v1.schema.json`, canonical YAML vs `agent-canonical-v1.schema.json`, frontmatter field-set vs the 12 official Claude Code fields.
- **Convention benchmarking**: where a check depends on repo convention (composition mechanism, nav tables in agent files, prompt-mirroring fidelity, canonical description parity), the reference implementation cited by AD-M-011 (`skills/problem-solving/` — ps-critic pair) and `skills/adversary/agents/adv-scorer.md` in the current worktree were used as the norm.
- **Severity calibration** (per task charter): Critical = HARD-rule (H-xx) violation or runtime/enforcement corruption; Major = MEDIUM-standard violation without documented justification, schema violation, registration gap, or misleading governance metadata; Minor = style/consistency.

---

## Per-Check Pass/Fail Matrix

| # | Check | Disposition | Notes |
|---|-------|-------------|-------|
| 1 | H-34a — `.md` frontmatter official fields only | **PASS** | Fields: `name`, `description`, `model`, `tools` — all official. No `allowed-tools`, no unrecognized fields (deterministically verified). |
| 2 | H-34b — governance schema validity | **PASS** | `VALID` against `agent-governance-v1.schema.json`. `version: "1.0.0"` (semver), `tool_tier: "T2"`, `identity.role` present, 4 expertise entries (>=2), `cognitive_mode: "systematic"` (in enum). |
| 3 | H-35 — constitutional triplet, forbidden_actions >=3, no Agent/Task | **PASS** | P-003/P-020/P-022 all present in `principles_applied`; 5 `forbidden_actions` referencing the triplet (NPT-009-complete format); `tools` contains neither `Agent` nor `Task`. |
| 4 | Tool tier coherence (current renumbered model) | **PASS** | T2 = Read-Write = T1 + Write/Edit/Bash. Granted: `Read, Write, Edit, Glob, Grep, Bash` — exact T2 set, no over-grant. Composition `tools.native` maps 1:1; `forbidden: [agent_delegate]`. No MCP servers (correct for T2). T1/T2 semantics unchanged by ADR-STORY015-001, so no renumbering hazard applies. |
| 5 | AD-M-011 — output path protocol | **FAIL** | Finding F-1. Prose non-template `location`, no `projects/${JERRY_PROJECT}/` default, no `filename_pattern`, no P1/P2/P3 acceptance in body, hardcoded repo-global `docs/experience/` write. |
| 6 | Guardrails minimums | **PASS** | `input_validation`: 4 (>=1). `output_filtering`: 5 (>=3). `fallback_behavior: escalate_to_user` (standard value, sane for a completion-gating agent). |
| 7 | Body structure (XML sections, hexagonal rule, H-23) | **PARTIAL** | All 7 required sections present and byte-verified balanced (identity 8–27, purpose 29–33, input 35–55, capabilities 57–73, methodology 75–235, output 237–261, guardrails 263–293; file is 293 lines). Hexagonal rule **FAIL** — Finding F-2. H-23 nav table absent — PASS by repo convention (see Observations O-1). |
| 8 | Composition drift + mechanism legitimacy | **PARTIAL** | `composition/` **is** a recognized Jerry convention (13 existing skills ship it: adversary, contract-design, eng-team, nasa-se, orchestration, problem-solving, red-team, saucer-boy, saucer-boy-framework-voice, test-spec, transcript, use-case, worktracker) — NOT non-standard machinery. Canonical YAML is `VALID` against `agent-canonical-v1.schema.json`. However content drift vs the shipped `.md` **FAIL** — Finding F-3. |
| 9 | plugin.json registration | **PASS** | `.claude-plugin/plugin.json` line 54: `"./skills/nuclear-sop/agents/sop-capture.md"` — path resolves to an existing file; frontmatter `name: "sop-capture"` matches the filename stem (plugin.json entries are path-only; no name field to mismatch). |

---

## Findings

### F-1 — AD-M-011 violation: output location is not a resolvable project-scoped template and body offers no caller override (Major)

- **Rule:** AD-M-011 (`.context/rules/agent-development-standards.md`, MEDIUM Standards) — "Agent output paths SHOULD follow the Unified Output Path Resolution Protocol... Agents SHOULD declare `output.location` as a project-relative default template using `projects/${JERRY_PROJECT}/` prefix, and SHOULD declare `output.filename_pattern`... Agents SHOULD accept caller-provided explicit paths (Priority 1) or base paths (Priority 2)... Reference architecture: `/problem-solving` agents."
- **Files:** `skills/nuclear-sop/agents/sop-capture.governance.yaml` (lines 53–63), `skills/nuclear-sop/composition/sop-capture.agent.yaml` (lines 52–62), `skills/nuclear-sop/agents/sop-capture.md` (`<output>` table lines 240–245).
- **Evidence:**
  - governance.yaml lines 54–55: `required: true` / `location: "capture/oe-entry-{entry_id}.yaml and docs/experience/{entry_id}.yaml"` — a prose "X and Y" string, not a path template; a path resolver cannot consume it.
  - No `filename_pattern` key anywhere in governance or canonical output blocks.
  - Neither path carries the `projects/${JERRY_PROJECT}/` prefix. Contrast reference: `skills/problem-solving/composition/ps-critic.agent.yaml` line 49: `location: projects/${JERRY_PROJECT}/critiques/{ps-id}-{entry-id}-{iteration}-critique.md`.
  - `capture/` is a bare relative path whose anchor ("Root of workflow working directory", `.md` line 40) is defined only implicitly; from the agent definition alone the write destination is ambiguous.
  - `docs/experience/{entry_id}.yaml` is a hardcoded repo-root-global directory: OE entries from every project accumulate in one shared corpus with no project scoping.
  - The `.md` body contains no P1 (explicit path) / P2 (base path) / P3 (default) resolution language; the output table (lines 240–245) presents all four artifact paths as fixed.
- **Documented justification check:** partial. The `.md` (line 200) justifies the `docs/experience/` half ("matches behavior-rules.md OE Search Mechanism Glob pattern" — the sop-brief retrieval loop depends on this location). No justification exists for the non-template prose form, the missing `filename_pattern`, the missing `${JERRY_PROJECT}` scoping of the local artifact, or the absent P1/P2 override support. This is not the `skills/*/output/` anti-pattern (BUG-006/GH #230), but it is a MEDIUM violation without complete documented justification.
- **Severity:** Major.
- **Recommendation:** Split `output.location` into a machine-resolvable primary template (e.g., `location: "projects/${JERRY_PROJECT}/nuclear-sop/{workflow_id}/capture/oe-entry-{entry_id}.yaml"`), keep the dual-write declaration in `dual_write_paths` (already structured), add `filename_pattern`, and add explicit P1/P2/P3 resolution language to the `<output>` section. If the repo-global `docs/experience/` corpus is intentional, record the AD-M-011 override justification in the governance file itself and address project-scoping/collision behavior (entry_id contains no project discriminator).

### F-2 — Hexagonal dependency rule violation: domain-layer body sections name concrete tools (Major)

- **Rule:** `agent-development-standards.md` §Agent Definition Schema › Markdown Body Sections (hexagonal dependency rule; MUST NOT tier language; adjacent to H-34 but not one of its two registered sub-items): "Domain-layer sections (`<identity>`, `<purpose>`, `<methodology>`, `<guardrails>`) MUST NOT reference specific tool names... Use capability descriptions instead (e.g., 'search the codebase' not 'use Grep')."
- **File:** `skills/nuclear-sop/agents/sop-capture.md`.
- **Evidence (file line numbers):**
  - `<identity>` line 24: "Perform fresh-context independent verification for C3+ workflows (that is sop-verifier via **Task tool**)"
  - `<identity>` line 26: "Spawn subagents or delegate via **Task tool** (T2 worker; Task tool is absent)"
  - `<methodology>` line 143: "Before **calling Write**, validate that every required field... DO NOT **call Write**."
  - `<methodology>` line 161: "**Use Glob** to count existing OE entry files"
  - `<methodology>` line 222: "**Mark procedure complete:** **Edit** PROCEDURE_STATE.yaml:"
  - `<guardrails>` line 284: "Required OE field missing | **Block Write**; report specific missing field"
  - `<guardrails>` line 290: "P-003: T2 worker. **Task tool** is absent from tools list."
- **Norm check:** the AD-M-011-cited reference architecture agent `skills/problem-solving/agents/ps-critic.md` contains zero concrete tool names in its domain sections (grep for "Use Glob|Use Grep|call Write|Task tool" returns nothing). `skills/adversary/agents/adv-scorer.md` has exactly one "Task tool" mention inside a P-003 prohibition — so a P-003-context Task mention in guardrails has limited precedent, but methodology-level "Use Glob"/"call Write"/"Edit ..." tool choreography does not.
- **Severity:** Major (unregistered MUST within agent-development-standards; does not corrupt runtime enforcement — Claude Code tool gating comes from frontmatter, which is correct — so not Critical).
- **Recommendation:** Rewrite domain-section references as capability descriptions ("count existing OE entries by filename pattern", "block the artifact write", "update the procedure state record", "delegation capability is absent"). Tool-specific choreography belongs in `<capabilities>` (lines 57–73), which already covers it correctly.

### F-3 — Composition drift: canonical SSOT and prompt diverge from the shipped runtime agent (Major)

- **Rule:** check-8 drift criterion ("duplicated-but-divergent system prompts / inconsistent metadata = finding"); AD-M-003 (description WHAT+WHEN+triggers) regression risk; `agent-canonical-v1.schema.json` header: "Canonical format is the SSOT from which vendor-specific agent files are generated via jerry agents build."
- **Files:** `skills/nuclear-sop/composition/sop-capture.agent.yaml`, `skills/nuclear-sop/composition/sop-capture.prompt.md` vs `skills/nuclear-sop/agents/sop-capture.md`.
- **Evidence:**
  1. **Description divergence (routing-relevant).** `.md` line 3 ends: "...WHEN: invoked as Step 4 (mandatory final step) of every nuclear-sop execution. Triggers: sop capture, post-job brief, OE capture, operating experience, lessons learned." The canonical description (agent.yaml lines 6–12) is differently worded ("classifies deviations" vs "documents deviations"), drops the "WHEN:" label and the entire "Triggers:" keyword list, and appends "Implements nuclear patterns F-2b..., H-1..., H-2...". Reference convention keeps the two identical (ps-critic.agent.yaml line 6 ff. is verbatim the ps-critic.md description). If `jerry agents build` regenerates the `.md` from the declared SSOT, the routing description loses its trigger keywords — an AD-M-003 regression introduced silently.
  2. **Decision-rule divergence.** `.md` line 132 (`NONE` classification): "all STAR Review outcomes show \"outcome matched expectation\"" vs agent.yaml line 135 and prompt.md line 87: "all STAR Review outcomes PASS" — different outcome vocabulary for the same classification gate. `.md` line 134 (`MAJOR`) includes "some acceptance criteria may not be met" — dropped in agent.yaml line 137 and prompt.md line 89. `.md` line 135 (`STOP-WORK`) includes "not all steps completed" — dropped in agent.yaml line 138.
  3. **Missing sections in prompt.** The `.md` body has 7 sections including `<input>` (lines 35–55) and `<capabilities>` (lines 57–73); `sop-capture.prompt.md` carries only Identity/Persona/Methodology/Output/Guardrails — Input and Capabilities are absent. Reference convention (`ps-critic.prompt.md`) mirrors the `.md` body verbatim, heading-for-tag.
  4. **Persona divergence.** governance.yaml line 21 declares `character: "Nuclear plant procedures analyst applying post-job review discipline..."`; the canonical persona block (agent.yaml lines 22–25) omits `character` even though `agent-canonical-v1.schema.json` (lines 68–71) defines the field.
- **Severity:** Major (misleading governance metadata: the file that self-declares as generation SSOT would not reproduce the shipped runtime agent; the runtime/composition pair cannot round-trip).
- **Recommendation:** Regenerate the composition pair from the shipped `.md` (or vice versa, then rebuild): make descriptions identical including the Triggers list, align the deviation-classification wording (pick one STAR-outcome vocabulary — whichever matches sop-executor's actual log vocabulary), mirror all 7 body sections into the prompt, and carry `persona.character` into the canonical file.

### F-4 — ET-M-001: `reasoning_effort` undeclared (Minor)

- **Rule:** ET-M-001 (`agent-development-standards.md`, MEDIUM Standards) — "Agent definitions SHOULD declare `reasoning_effort` aligned with criticality level... Validation-only agents (e.g., ps-validator, wt-auditor) MAY use `default`."
- **File:** `skills/nuclear-sop/agents/sop-capture.governance.yaml` (absent; grep for `reasoning_effort` returns nothing in any of the four subject files).
- **Evidence:** No `reasoning_effort` key in governance, canonical, or `.md`. The agent serves workflows up to C4 (input `criticality: C1 | C2 | C3 | C4`, `.md` line 52), where the ET-M-001 mapping suggests `high`/`max`.
- **Severity:** Minor, not Major, for two reasons: (a) sop-capture is a systematic, checklist-driven capture/validation agent, plausibly within ET-M-001's "validation-only agents MAY use default" allowance; (b) current-repo practice is mixed — only ~5 existing agents declare the field (e.g., `ux-lean-ux-facilitator`, `pm-*` governance files), so absence matches the dominant repo pattern.
- **Recommendation:** Declare `reasoning_effort` explicitly (e.g., `medium`, with a note that C3+/C4 procedure closure warrants it), or document the default-tier justification.

---

## Checks Passed — Detail

| Rule / Check | Evidence |
|--------------|----------|
| **H-34a** frontmatter fields | Deterministic parse: fields = `['description', 'model', 'name', 'tools']`; unofficial fields = NONE. `allowed-tools` (a SKILL.md-only field) is not present. |
| **H-34b** governance schema | jsonschema Draft 2020-12: **VALID**. `version: "1.0.0"` matches `^\d+\.\d+\.\d+$`; `tool_tier: "T2"` in enum; `identity.role` = "Post-job operating experience capture and mandatory OE schema enforcer"; `identity.expertise` = 4 entries; `identity.cognitive_mode: "systematic"` in the 5-mode enum. |
| **H-35** constitutional triplet | governance lines 67–70: P-003/P-020/P-022 all present in `principles_applied` (3 entries, minItems 3 satisfied). `capabilities.forbidden_actions` = 5 entries (>=3), first three reference P-003/P-020/P-022 in NPT-009-complete format with consequences. Frontmatter `tools` excludes `Agent` and `Task` (deterministically verified). |
| **Tool tier coherence** | Declared T2 in governance (line 6) and canonical (line 38). Granted tools `Read, Write, Edit, Glob, Grep, Bash` = exactly the T2 (Read-Write) set per current standards ("T2: T1 + Write, Edit, Bash"). No `mcpServers` field — no Memory-Keeper/Context7 (correct: MCP would require T3+). Canonical `tools.native` (`file_read, file_write, file_edit, file_search_glob, file_search_content, shell_execute`) maps 1:1 to the frontmatter grant; `forbidden: [agent_delegate]` mirrors the Task exclusion. `model.tier: reasoning_standard` ↔ `model: "sonnet"` matches the reference mapping (ps-critic: reasoning_standard/sonnet). |
| **Guardrails (SR-002/SR-003/SR-009)** | `input_validation`: 4 rules (execution_log_final_check, criticality_enum `^(C1\|C2\|C3\|C4)$`, workflow_id_format, iv_report_required_for_c3plus). `output_filtering`: 5 entries. `fallback_behavior: escalate_to_user` (standard value, pattern-valid). |
| **Body XML sections** | All 7 required sections present as balanced siblings; byte-verified: file is 293 lines, ends `...verification.\n</guardrails>\n`; tag-only lines at 8/27, 29/33, 35/55, 57/73, 75/235, 237/261, 263/293. (An apparent stray trailing `</output>` in an earlier read was the tool-result wrapper, not file content — disproven by `wc -l` + `od -c`.) |
| **AD-M-001** naming | `sop-capture` matches `^[a-z]+-[a-z]+(-[a-z]+)*$` and the filename stem. Prefix `sop-` abbreviates `nuclear-sop` consistently with repo convention (problem-solving→ps-, nasa-se→nse-, saucer-boy→sb-). |
| **AD-M-002** semver | `1.0.0` in governance and canonical. |
| **AD-M-003** description | WHAT (OE capture agent, dual-write, comparison) + WHEN ("WHEN: invoked as Step 4 (mandatory final step)") + Triggers (5 keywords). 573 chars < 1024. No XML tags. |
| **AD-M-004** output levels | `levels: [L0, L1, L2]` declared; body specifies all three (lines 249–253). |
| **AD-M-005** expertise | 4 specific entries (schema minimum 2), all domain-specific, none generic. |
| **AD-M-006** persona | tone `methodical`, communication_style `structured`, audience_level `expert` (enum-valid), plus `character`. |
| **AD-M-007** session_context | `on_receive` (5 steps) and `on_send` (5 steps) declared in governance lines 94–106. |
| **AD-M-008** post_completion_checks | 6 verifiable assertions (governance lines 74–80). |
| **AD-M-009** model selection | `sonnet` for a systematic-mode agent — matches the Mode-to-Design table ("systematic → sonnet or haiku"). |
| **MCP standards** | No MCP tools declared anywhere in the quadruple; MCP-001/MCP-002/AD-M-010 not applicable (agent performs no external library research and no cross-session persistence beyond file writes). |
| **plugin.json (check 9)** | Entry `"./skills/nuclear-sop/agents/sop-capture.md"` present (line 54 of `.claude-plugin/plugin.json`); target file exists at that path in the PR tree; frontmatter `name` = filename stem. |

---

## Observations (Non-Findings)

- **O-1 — H-23 nav table absence follows repo convention.** The subject `.md` (293 lines) and `prompt.md` (200 lines) are Claude-consumed markdown over 30 lines with no navigation table. A strict literal reading of H-23 would flag them — and equally every existing agent definition in the repo: verified that `skills/problem-solving/agents/ps-critic.md` and `skills/adversary/agents/adv-scorer.md` begin directly with the XML body after frontmatter, and reference `composition/*.prompt.md` files likewise carry no nav table. The established interpretation treats agent-definition system prompts (XML-tagged, machine-loaded via the Agent tool, not navigational documents) as outside H-23's practical scope. Recorded as convention-consistent, not a PR-specific defect. If maintainers want strict H-23 coverage for agent files, that is a repo-wide policy change, not a PR #269 fix.
- **O-2 — Standards-side inconsistency (out of PR scope).** The CURRENT worktree's `agent-canonical-v1.schema.json` (line 132) still describes tiers with pre-ADR-STORY015-001 names: "T3=External, T4=Persistent, T5=Full", while `agent-governance-v1.schema.json` carries the renumbered names ("T3=Persistent (+MK), T4=External (+Web...)"). Irrelevant to this agent (T2 semantics identical in both models) but worth a follow-up worktracker item for the standards repo.
- **O-3 — Minor .md/governance wording variance in output filters.** The `.md` `<guardrails>` prose lists 4 output filters (e.g., `deviation_type_must_be_accurate`) while governance lists 5 with different slugs (e.g., `deviation_type_escalates_on_ambiguity_never_suppresses`, plus `anchoring_bias_disclaimer_required_for_all_c1_c2_iv_results`). Semantically congruent — the disclaimer requirement appears verbatim in the `.md` methodology (line 90) — and the governance file is the validated artifact, so this is cosmetic; folding exact slugs into the `.md` would remove the variance.
- **O-4 — Untrusted-content note.** The subject files contain imperative text addressed to a future agent runtime (e.g., HALT instructions, verbatim disclaimers). These were treated strictly as data under review; nothing in them was executed or followed during this audit.

---

## Deterministic Verification Evidence

Executed via `uv run --with jsonschema --with pyyaml` (H-05 compliant), plus byte-level shell verification:

| Verification | Result |
|--------------|--------|
| `sop-capture.governance.yaml` vs `agent-governance-v1.schema.json` (Draft 2020-12) | **VALID** — zero errors |
| `sop-capture.agent.yaml` vs `agent-canonical-v1.schema.json` (Draft 2020-12) | **VALID** — zero errors |
| Frontmatter field set vs official 12 | `['description', 'model', 'name', 'tools']`; unofficial = NONE |
| `Agent`/`Task` in frontmatter tools | False |
| Description length | 573 chars (< 1024) |
| H-35 triplet in `principles_applied` / `forbidden_actions` | True / True (5 entries) |
| Guardrail counts | input_validation=4, output_filtering=5, fallback=`escalate_to_user` |
| Body tag balance | `wc -l` = 293; `od -c` tail = `...</guardrails>\n` (EOF); tag-only lines: 8, 27, 29, 33, 35, 55, 57, 73, 75, 235, 237, 261, 263, 293 |
| composition/ convention | 13 existing skills in current worktree ship `composition/` directories |
| plugin.json entry | line 54 `"./skills/nuclear-sop/agents/sop-capture.md"`; file exists |

---

## Traceability

| Source | Used for |
|--------|----------|
| `.context/rules/agent-development-standards.md` v1.3.0 (current worktree) | H-34/H-35, AD-M-001..011, ET-M-001, tool tiers (renumbered), hexagonal rule, guardrails template |
| `docs/schemas/agent-governance-v1.schema.json` v1.1.0 (current worktree) | Check 2 deterministic validation |
| `docs/schemas/agent-canonical-v1.schema.json` v1.0.0 (current worktree) | Check 8 composition validation |
| `.context/rules/mcp-tool-standards.md` v1.4.0 (current worktree) | MCP applicability (none declared) |
| `.context/rules/markdown-navigation-standards.md` (current worktree) | H-23 assessment (O-1) |
| `skills/problem-solving/` (ps-critic pair), `skills/adversary/agents/adv-scorer.md` (current worktree) | Reference-architecture norms for AD-M-011, description parity, prompt mirroring, hexagonal rule, nav-table convention |
| PR #269 head `bda64202` worktree | All four subject files, `.claude-plugin/plugin.json` |

*End of audit. Findings ranked: F-1 (Major, AD-M-011), F-2 (Major, hexagonal rule), F-3 (Major, composition drift), F-4 (Minor, ET-M-001).*
