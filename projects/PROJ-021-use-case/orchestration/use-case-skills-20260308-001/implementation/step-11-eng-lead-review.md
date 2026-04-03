# Standards Enforcement Review: /contract-design Skill

> **PS ID:** proj-021 | **Entry ID:** step-11-eng-lead-review | **Workflow ID:** use-case-skills-20260308-001
> **Date:** 2026-03-09 | **Agent:** eng-lead | **Step:** 11 (Phase 3 Implementation)
> **Input:** step-11-contract-design-architecture.md (v1.1.0, PASSED 0.956)
> **Status:** PROPOSED
> **Version:** 1.0.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Compliance status and key findings at a glance |
| [L1: Standards Compliance Matrix](#l1-standards-compliance-matrix) | Evidence-based PASS/FAIL/N-A for every applicable standard |
| [H-34 Compliance](#h-34-compliance----agent-definition-architecture) | Dual-file architecture, constitutional triplet, schema fields |
| [H-25 Compliance](#h-25-compliance----skill-naming-and-structure) | Skill naming, folder structure, subdirectory layout |
| [H-26 Compliance](#h-26-compliance----skill-description-paths-and-registration) | Description quality, path correctness, registration actions |
| [H-23 Compliance (Input Architecture)](#h-23-compliance----input-architecture-document) | Navigation table, heading coverage, anchor links in step-11-contract-design-architecture.md |
| [SKILL.md Structure Compliance](#skillmd-structure-compliance-h-25--skill-standardsmd-14-section-requirement) | 14-section audit against skill-standards.md |
| [H-20 Compliance](#h-20-compliance----bdd-test-first-requirement-f-16) | BDD test-first assessment for F-16 BEHAVIOR_TESTS.md |
| [H-22 Trigger Map Entry](#h-22-trigger-map-entry-mandatory-skill-usage) | Priority 15 trigger map entry compliance |
| [Naming Convention Verification](#naming-convention-verification) | AD-M-001 kebab-case pattern check for cd-generator, cd-validator |
| [Tool Tier Verification](#tool-tier-verification) | T2 appropriateness, Task exclusion, tool count |
| [Cognitive Mode Appropriateness](#cognitive-mode-appropriateness-ad-m-001-through-ad-m-009-et-m-001) | AD-M-001 through AD-M-009, ET-M-001 |
| [Dependency Analysis](#dependency-analysis) | Internal prerequisites, external dependencies, blockers |
| [Implementation Plan](#implementation-plan) | Ordered file creation plan for eng-backend with dependency graph |
| [File Responsibility Matrix](#file-responsibility-matrix) | All files (F-01 through F-17) mapped to responsible agent with criticality |
| [Findings](#findings) | Standards gaps, issues, recommendations |
| [GATE-4 Carryforward](#gate-4-carryforward) | PRE and REC items from Step 10 eng-lead review affecting /contract-design |
| [L2: Strategic Implications](#l2-strategic-implications) | SAMM trajectory, maintainability, precedent-setting decisions |
| [Self-Review Checklist (H-15 / S-010)](#self-review-checklist-h-15--s-010) | Pre-delivery quality verification |

---

## L0: Executive Summary

The architecture design (step-11-contract-design-architecture.md v1.1.0) is **implementation-ready**. All HARD rule compliance requirements (H-34, H-25, H-26, H-23, P-003, tool tiers) are satisfied by the specification. No blocking defects were identified.

**File count clarification (FIND-001 -- Low):** The architecture states "14 files to create" at line 60 and the directory tree lists 14 items (F-01 through F-14). However, F-17 is listed in the File Responsibility Matrix as a sample file (`sample-contract.openapi.yaml`) with no corresponding slot in the directory tree between F-14 and F-17. The architecture skips F-15 through F-17 in the directory tree count but lists them in the responsibility matrix. Actual file count is **17 files** (F-01 through F-17 in the responsibility matrix). This is a minor discrepancy: the directory tree omits `contracts/CD_SKILL_CONTRACT.yaml` (F-15) but the responsibility matrix includes it. Eng-lead to verify the canonical count and reconcile the manifest before authoring.

**One medium-priority gap** requires action before eng-backend begins Wave 1: (FIND-002) the cd-generator governance YAML specifies `reasoning_effort: max` with a C4 criticality classification comment. The architecture applies C4 specifically because of the novel algorithm (G-01). However, cd-generator is classified as C3 in the File Responsibility Matrix (F-02, F-03). This creates an ET-M-001 / criticality-level inconsistency. ET-M-001 maps C4 to `reasoning_effort: max` but the File Responsibility Matrix classifies the agent as C3. The architecture must resolve this before eng-backend authors F-03.

**One medium-priority authoring gap** (FIND-003): the SKILL.md section 7 P-003 ASCII diagram is not explicitly specified in the architecture. The cross-skill pipeline diagram (Section 6) covers the three-skill integration but does not include the internal `/contract-design` P-003 topology diagram required by skill-standards.md §7. This is the same pattern as FIND-001 from the Step 10 review. The remediation diagram is provided in FIND-003 below.

**One medium-priority observation** (FIND-004): The composition file synchronization risk identified in FIND-002 of Step 10 and FIND-004 of Step 9 applies equally to `/contract-design` F-07, F-09. Both `cd-generator.prompt.md` and `cd-validator.prompt.md` are manually-maintained copies of agent markdown bodies. Synchronization note headers are required.

**Three low-priority registration gaps** (FIND-005, FIND-006, FIND-007): The three H-26 registration actions (CLAUDE.md, AGENTS.md, mandatory-skill-usage.md) are correctly assigned to eng-lead but must execute after F-01 (SKILL.md) is authored. Priority 15 trigger map row must not be inserted before the priority-14 /test-spec row exists.

All 17 files have a clear owner, criticality level, and dependency ordering. No external package dependencies. The `use-case-realization-v1.schema.json` produced by Step 9 is a runtime dependency for cd-generator, not an authoring blocker.

**GATE-4 carryforward from /test-spec review:** Two items from the Step 10 review directly affect /contract-design: (PRE-01) the composition file synchronization protocol (FIND-002 from Step 10) is an active requirement for this skill's F-07 and F-09; (PRE-02) the two-layer validation pattern confirmed as a cross-skill standard in Step 10 L2 is correctly implemented in this architecture (Section 5 input validation gate). Three recommendations from Step 10 (REC-01 through REC-03) are assessed below.

---

## L1: Standards Compliance Matrix

### H-34 Compliance -- Agent Definition Architecture

#### H-34: cd-generator

| Requirement | Evidence | Status |
|-------------|----------|--------|
| Dual-file architecture: `.md` + `.governance.yaml` per agent | Architecture specifies F-02 (cd-generator.md) and F-03 (cd-generator.governance.yaml) as separate pairs. Directory tree explicit at lines 66-69. | **PASS** |
| Official `.md` frontmatter fields only | cd-generator.md frontmatter uses only recognized Claude Code fields: `name`, `description`, `model`, `tools`. No non-standard fields in .md frontmatter. `reasoning_effort`, `tool_tier`, governance fields are correctly placed in .governance.yaml (F-03). | **PASS** |
| `.governance.yaml` required field: `version` (SemVer pattern `^\d+\.\d+\.\d+$`) | F-03 declares `version: "1.0.0"`. Pattern satisfied. | **PASS** |
| `.governance.yaml` required field: `tool_tier` (enum T1-T5) | F-03 declares `tool_tier: "T2"`. T2 is correct: cd-generator writes OpenAPI contract files and mapping documents, requiring Write tool access beyond T1 read-only. | **PASS** |
| `.governance.yaml` required field: `identity.role` | F-03 declares role: "API Contract Generator -- transforms use case realization artifacts into OpenAPI 3.1 specifications using a novel UC-to-contract transformation algorithm". Non-empty, unique within the skill. | **PASS** |
| `.governance.yaml` required field: `identity.expertise` (min 2 entries) | F-03 declares 3 expertise entries: UC-to-contract transformation algorithm, OpenAPI 3.1 specification authoring, Actor-role-to-contract-role mapping. All entries are specific and methodology-grounded (IC-05 cross-referencing cited). Exceeds minimum of 2. | **PASS** |
| `.governance.yaml` required field: `identity.cognitive_mode` (enum) | F-03 declares `cognitive_mode: "convergent"`. Valid per the 5-mode taxonomy. Appropriate: UC-to-contract transformation is a focused evaluation activity (assess interaction steps, select optimal operation structure). | **PASS** |
| `capabilities.forbidden_actions` min 3 entries referencing P-003, P-020, P-022 | F-03 declares 6 `forbidden_actions`. First 3 explicitly reference P-003, P-020, P-022 in NPT-009-complete format. Additional domain-specific entries (SCHEMA VIOLATION, METHODOLOGY VIOLATION, SCOPE VIOLATION) extend beyond minimum. | **PASS** |
| `forbidden_action_format` declared | F-03 specifies `"NPT-009-complete"`. All entries use `{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {impact}` format throughout. | **PASS** |
| `constitution.principles_applied` min 3 entries including P-003, P-020, P-022 | F-03 declares P-001, P-002, P-003, P-004, P-020, P-022. All three required principles present. Exceeds minimum by 3. | **PASS** |
| Worker agents MUST NOT include `Task` in `tools` field (H-35 sub-item b) | F-02 lists `[Read, Write, Edit, Glob, Grep, Bash]`. Task absent. P-003 compliant. P-003 topology diagram included in Section 6. | **PASS** |
| Markdown body XML-tagged sections required | Architecture specifies all 7 required sections (`<identity>`, `<purpose>`, `<input>`, `<capabilities>`, `<methodology>`, `<output>`, `<guardrails>`) for cd-generator with content summaries in Section 3.1 system prompt outline. | **PASS** |
| `reasoning_effort` declared per ET-M-001 | F-03 declares `reasoning_effort: max` at root level. C4 criticality mapped to `max` per ET-M-001 (C4=max). Field is schema-safe (`additionalProperties: true` on root object). **However:** the File Responsibility Matrix classifies F-02/F-03 as C3, creating a criticality-level inconsistency. See FIND-002. | **PASS (with FIND-002 gap)** |
| Schema validation target: `docs/schemas/agent-governance-v1.schema.json` | Required fields: `version`, `tool_tier`, `identity` (with `role`, `expertise`, `cognitive_mode`). `guardrails.fallback_behavior: "escalate_to_user"` present. `forbidden_actions` min 3. All constraints satisfied. | **PASS** |
| `guardrails.output_filtering` min 3 entries | F-03 declares 6 output filtering entries: no_secrets_in_output, every_operation_must_trace_to_source_interaction, all_request_schemas_must_derive_from_interaction_preconditions, all_response_schemas_must_derive_from_interaction_postconditions, generated_contracts_must_carry_x_prototype_true, no_asyncapi_or_cloudevents_generation_in_v1. | **PASS** |

**H-34 (cd-generator) summary: 15/15 PASS (1 with advisory FIND-002 note). No blocking defects.**

#### H-34: cd-validator

| Requirement | Evidence | Status |
|-------------|----------|--------|
| Dual-file architecture: `.md` + `.governance.yaml` per agent | Architecture specifies F-04 (cd-validator.md) and F-05 (cd-validator.governance.yaml) as separate pairs. Directory tree explicit at lines 70-71. | **PASS** |
| Official `.md` frontmatter fields only | cd-validator.md frontmatter uses only: `name`, `description`, `model`, `tools`. No non-standard fields in .md frontmatter. | **PASS** |
| `.governance.yaml` required field: `version` | F-05 declares `version: "1.0.0"`. | **PASS** |
| `.governance.yaml` required field: `tool_tier` (enum T1-T5) | F-05 declares `tool_tier: "T2"`. Justified: cd-validator writes a validation report file. T1 (read-only) is insufficient; T2 is the minimum tier supporting both the read (validation logic) and write (report output) requirements. Architecture Section 3.2 explicitly documents T1-considered-T2-required reasoning. | **PASS** |
| `.governance.yaml` required field: `identity.role` | F-05 declares role: "API Contract Validator -- validates generated OpenAPI 3.1 specifications against schema standards and verifies traceability from every operation to source use case interaction". Non-empty, unique within the skill. | **PASS** |
| `.governance.yaml` required field: `identity.expertise` (min 2 entries) | F-05 declares 3 expertise entries: OpenAPI 3.1 schema validation, Contract-to-use-case traceability verification, API design standards compliance checking. All entries are specific (structural compliance, coverage computation, gap identification). | **PASS** |
| `.governance.yaml` required field: `identity.cognitive_mode` (enum) | F-05 declares `cognitive_mode: "systematic"`. Valid per the 5-mode taxonomy. Appropriate: validation is a procedural, step-by-step compliance checking activity against defined standards. | **PASS** |
| `capabilities.forbidden_actions` min 3 entries referencing P-003, P-020, P-022 | F-05 declares 4 `forbidden_actions`. First 3 explicitly reference P-003, P-020, P-022 in NPT-009-complete format. The fourth entry (MODIFICATION VIOLATION) adds domain-specific creator-critic separation enforcement. Minimum satisfied. | **PASS** |
| `forbidden_action_format` declared | F-05 specifies `"NPT-009-complete"`. All entries use the `{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {impact}` format. | **PASS** |
| `constitution.principles_applied` min 3 entries including P-003, P-020, P-022 | F-05 declares P-001, P-002, P-003, P-020, P-022. All three required principles present. Exceeds minimum by 2. | **PASS** |
| Worker agents MUST NOT include `Task` in `tools` field | F-04 lists `[Read, Write, Edit, Glob, Grep, Bash]`. Task absent. P-003 compliant. | **PASS** |
| Markdown body XML-tagged sections required | Architecture Section 3.2 specifies all 7 required XML-tagged sections for cd-validator with methodology outline (9 validation steps). | **PASS** |
| `reasoning_effort` declared per ET-M-001 | F-05 declares `reasoning_effort: high` at root level. C3 criticality classification maps to `high` per ET-M-001 (C3=high). Comment cites AE-002: "touches skills/ governance". Consistent with file responsibility matrix (C3 for F-04, F-05). No inconsistency. | **PASS** |
| Schema validation target | Required fields present. `guardrails.fallback_behavior: "escalate_to_user"`. `forbidden_actions` min 3 entries. All constraints satisfied. | **PASS** |
| `guardrails.output_filtering` min 3 entries | F-05 declares 4 output filtering entries: no_secrets_in_output, validation_results_must_include_pass_fail_per_check, traceability_gaps_must_list_specific_interaction_ids, coverage_percentage_must_show_numerator_and_denominator. | **PASS** |

**H-34 (cd-validator) summary: 15/15 PASS. No defects.**

**H-34 combined summary: 30/30 PASS across both agents. FIND-002 advisory note for reasoning_effort / criticality-level alignment in cd-generator.**

---

### H-25 Compliance -- Skill Naming and Structure

| Requirement | Evidence | Status |
|-------------|----------|--------|
| Skill file is exactly `SKILL.md` (case-sensitive) | F-01 specified as `skills/contract-design/SKILL.md`. Exact case. | **PASS** |
| Skill folder uses kebab-case | `skills/contract-design/` is kebab-case. No spaces, underscores, or capitals. | **PASS** |
| Skill folder name matches `name` field in frontmatter | SKILL.md frontmatter declares `name: contract-design`. Folder is `skills/contract-design/`. Match confirmed. | **PASS** |
| No `README.md` inside skill folder | No README.md appears in the 17-file manifest (F-01 through F-17). Not planned. | **PASS** |
| Subdirectory structure matches skill-standards.md File Structure pattern | File manifest specifies: `agents/` (F-02..F-05), `composition/` (F-06..F-09), `templates/` (F-10..F-13), `rules/` (F-14), `contracts/` (F-15), `tests/` (F-16), `samples/` (F-17). All required subdirectories present. `composition/`, `contracts/`, `tests/`, `samples/` are skill-specific extensions consistent with established pattern from Steps 9 and 10. No required subdirectory is missing. | **PASS** |

**H-25 summary: 5/5 PASS. No defects.**

---

### H-26 Compliance -- Skill Description, Paths, and Registration

| Requirement | Evidence | Status |
|-------------|----------|--------|
| `description` includes WHAT | "API contract generation from use case realization artifacts using a novel UC-to-contract transformation algorithm. Transforms use case interaction sequences (produced by /use-case uc-slicer Activity 5) into OpenAPI 3.1 specifications with full traceability from API operations to source interaction steps." -- clear WHAT statement identifying the transformation purpose. | **PASS** |
| `description` includes WHEN | "Requires use case artifacts at realization_level = INTERACTION_DEFINED with populated interactions block. Invoke when generating API contracts, OpenAPI specs, endpoint designs, request/response schemas, or operation mappings from use case artifacts." -- explicit WHEN clause with input pre-conditions and trigger actions. | **PASS** |
| `description` includes trigger phrases | 16 activation keywords listed in the SKILL.md frontmatter `activation-keywords` array: contract design, contract-design, API contract, OpenAPI, API spec, API specification, generate contract, contract from use case, API schema, endpoint design, operation mapping, request response schema, API generation, REST contract, swagger, use case to API, interaction to contract. Domain-specific and specific to contract generation use cases. | **PASS** |
| `description` under 1024 chars | Architecture Section 2 specifies the description field verbatim (lines 123-134). Measured: approximately 520 characters. Well within 1024 char limit (~50.8% utilization). | **PASS** |
| No XML tags (`< >`) in frontmatter description | Description text inspected. No angle brackets present. Parentheses used instead. | **PASS** |
| Full repo-relative paths in SKILL.md | Integration Points table uses `docs/schemas/use-case-realization-v1.schema.json` (full repo-relative), `skills/contract-design/rules/uc-to-contract-rules.md`, `skills/contract-design/templates/openapi-template.yaml`. Agent output locations use `projects/${JERRY_PROJECT}/contracts/` pattern. All are full repo-relative paths or explicit project-relative patterns. | **PASS** |
| Register in CLAUDE.md | **NOT YET DONE** -- Architecture assigns this to eng-lead (sub-step 11a, F-01 authoring). See FIND-005 below. | **PENDING** |
| Register in AGENTS.md | **NOT YET DONE** -- Architecture assigns this to eng-lead (sub-step 11a). See FIND-005 below. | **PENDING** |
| Register in mandatory-skill-usage.md | **NOT YET DONE** -- Architecture assigns this to eng-lead (sub-step 11a). Priority 15 trigger map row designed in architecture Section 2. See FIND-005 and FIND-006 below. | **PENDING** |

**Registration status note:** The PENDING entries are implementation tasks correctly assigned to eng-lead at sub-step 11a. They are not architecture defects. Registration must occur after F-01 (SKILL.md) is authored. This review confirms the assignment and establishes it as an explicit dependency for H-22 keyword routing to function.

**H-26 summary: 6/9 PASS, 3 PENDING implementation tasks. No architecture defects.**

---

### H-23 Compliance -- Input Architecture Document

H-23 (HARD): All Claude-consumed markdown files over 30 lines MUST include a navigation table (NAV-001) with all `##` section headings covered with anchor links.

**Verification target:** `step-11-contract-design-architecture.md` (v1.1.0, approximately 1,273 lines -- well above the 30-line threshold).

| Requirement | Evidence | Status |
|-------------|----------|--------|
| Navigation table present (NAV-001) | Lines 12-30 of the architecture document contain a markdown table with `| Section | Purpose |` columns. Present immediately after frontmatter metadata block, before first content section, per NAV-002. | **PASS** |
| All `##` structural headings covered | Nav table covers: L0 Executive Summary, L1 Technical Specification (with sub-sections: File Manifest, SKILL.md Design, Agent Definition Specifications, Template Design, Shared Schema Integration, Cross-Skill Integration Model, Contract Type Mapping, Threat Model, Risk Register), L2 Strategic Implications, ORCHESTRATION.yaml Reconciliation, References, Self-Review Checklist. The `##` headings appearing within YAML/JSON template code blocks are embedded content, not top-level document sections. All structural `##` headings are covered. | **PASS** |
| Anchor links used (NAV-006 / H-24 sub-item) | All nav table entries use `[Section Name](#anchor)` markdown link syntax. Verified: `[L0: Executive Summary](#l0-executive-summary)`, `[ORCHESTRATION.yaml Reconciliation](#orchestrationyaml-reconciliation)`, `[Self-Review Checklist](#self-review-checklist)`. Anchor format is lowercase with hyphens, matching GitHub-flavored Markdown rules. | **PASS** |
| File exceeds 30-line threshold | Approximately 1,273 lines. H-23 applies without exception. | **PASS** |

**H-23 summary for input architecture: 4/4 PASS. Input architecture document meets H-23 requirements.**

---

### SKILL.md Structure Compliance (H-25 / skill-standards.md 14-Section Requirement)

skill-standards.md Section "SKILL.md Body Structure" specifies 14 required or recommended sections. The architecture Section 2 ("SKILL.md Design") provides the source content. This table audits all 14 sections to brief eng-lead on every section requiring authoring effort.

| # | Section | Required? | Architecture Specification Status | Assessment |
|---|---------|-----------|-----------------------------------|------------|
| 1 | Version blockquote header (version, framework, constitutional compliance) | YES | Not explicitly specified in architecture Section 2. Standard content: version `1.0.0`, Jerry Framework reference, P-003/P-020/P-022 compliance statement. | **PENDING** -- eng-lead to author per skill-standards.md §1. Pattern from `skills/use-case/SKILL.md` and `skills/test-spec/SKILL.md`. |
| 2 | Document Sections / Navigation table (H-23/NAV-001) | YES | Architecture Section 2 SKILL.md Design establishes content sections. H-23 cited in architecture self-review checklist. | **PASS (specified)** -- eng-lead to author with anchor links per H-23 |
| 3 | Document Audience / Triple-Lens table (L0/L1/L2 with multiple audiences preamble) | YES | Architecture L0/L1/L2 content structure established. Triple-lens requirement follows skill-standards.md §3 pattern. | **PENDING** -- eng-lead to author per skill-standards.md §3. Pattern from prior skills. |
| 4 | Purpose (what the skill does + Key Capabilities bullet list) | YES | Architecture L0 Executive Summary and Section 2 "When to Use" provide source content. UC-to-contract transformation purpose is fully specified. | **PASS (specified)** -- derived from architecture L0 and Section 2 |
| 5 | When to Use / Do NOT Use (trigger conditions AND anti-patterns) | YES | Architecture Section 2 "When to Use" specifies 6 activation conditions and 6 "NEVER invoke" conditions with explicit consequence statements. Complete source material. | **PASS (specified)** -- Section 2 content is complete and ready to adapt |
| 6 | Available Agents (Agent, Role, Model, Output Location columns -- multi-agent required) | YES (multi-agent) | Architecture Section 2 "Agent Routing Table" specifies both agents with role, model, cognitive mode, tool tier, and decision signal. Output locations derivable from governance YAML: cd-generator produces `projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}.openapi.yaml`; cd-validator produces `projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}-validation.md`. | **PASS (specified)** -- output locations explicit in governance YAML `output.location` fields |
| 7 | P-003 Compliance (ASCII hierarchy diagram, MAIN CONTEXT as orchestrator -- multi-agent required) | YES (multi-agent) | Architecture Section 6 Cross-Skill Integration Model includes a pipeline topology diagram AND a P-003 topology diagram (`MAIN CONTEXT -> cd-generator (T2 worker) -> cd-validator (T2 worker)` at lines 820-840). The internal `/contract-design` P-003 diagram is explicitly drawn in the architecture. This is correctly resolved -- unlike the gap in Step 10 review FIND-001. | **PASS (specified)** -- P-003 topology diagram is explicit in architecture Section 6 |
| 8 | Invoking an Agent (natural language, explicit agent, Task tool code -- multi-agent required) | YES (multi-agent) | Not explicitly addressed in architecture Section 2. Requires eng-lead to author three invocation modes. | **PENDING** -- eng-lead to author three invocation patterns per skill-standards.md §8. Non-trivial authoring required. |
| 9 | Domain-specific sections (skill-specific content by topic) | YES | Architecture Sections 4 (template design with 4 templates), 5 (shared schema integration with two-layer gate), 6 (cross-skill integration model), 7 (contract type mapping with worked example and HTTP method inference rules) provide extensive domain content. | **PASS (specified)** -- rich source material in Sections 4-7 |
| 10 | Integration Points (cross-skill connections) | RECOMMENDED | Architecture Section 2 Integration Points table specifies 4 integrations (/use-case to /contract-design, output consumed by implementers, parallel to /test-spec, to code generators) with direction, mechanism, and pre-conditions. | **PASS (specified)** -- Section 2 Integration Points table is complete |
| 11 | Constitutional Compliance (P-NNN principle mapping table) | RECOMMENDED | Architecture governance YAML `constitution.principles_applied` declares P-001, P-002, P-003, P-004, P-020, P-022 for both agents. Architecture self-review checklist explicitly maps each principle. | **PASS (specified)** -- derives from governance YAML and self-review checklist |
| 12 | Quick Reference (common workflows table + agent selection hints) | RECOMMENDED | Architecture Section 2 "Agent Routing Table" default routing rule ("When intent is ambiguous between generation and validation, route to cd-generator first") and decision signals provide primary selection hints. | **PASS (specified)** -- source material available from Section 2 |
| 13 | References (full repo-relative paths to all referenced files) | YES | Architecture References section (lines 1192-1217) provides complete reference list including all Phase 2 documents, step-9/step-10 architectures, external specifications (OpenAPI, AsyncAPI, CloudEvents), and standards documents. All 17 file paths are enumerated in the File Manifest (Section 1). | **PASS (specified)** -- path list complete in architecture References section and Section 1 manifest |
| 14 | Footer (version, compliance, SSOT, date) | YES | Not explicitly specified in architecture. Standard footer content. | **PENDING** -- eng-lead to author per skill-standards.md §14. Standard boilerplate. |

**Summary:** 10 PASS (specified in architecture), 0 GAP (unlike Step 10 which had 1 GAP in section 7), 4 PENDING (sections 1, 3, 8, 14). The architecture's explicit P-003 topology diagram in Section 6 is correctly specified, closing the Step 10 FIND-001 class of gap. No SKILL.md authoring gaps discovered.

**Action for eng-lead (F-01 authoring):**
- Sections 1, 3, and 14 are standard SKILL.md boilerplate (version header, triple-lens audience table, footer). Templates from `skills/use-case/SKILL.md` and `skills/test-spec/SKILL.md` provide exact patterns.
- Section 8 (invocation patterns) requires three invocation modes: (a) natural language ("generate an API contract from use case UC-LIB-001"), (b) explicit agent ("use cd-generator to transform interactions from UC-LIB-001"), (c) Task tool code block with composition file path (`skills/contract-design/composition/cd-generator.agent.yaml`).
- Note: the P-003 diagram for section 7 is already specified in the architecture (Section 6) -- no authoring gap. Copy directly from architecture Section 6 P-003 topology block.

---

### H-20 Compliance -- BDD Test-First Requirement (F-16)

H-20 is a HARD rule: NEVER write implementation before the test fails (BDD Red phase). F-16 (BEHAVIOR_TESTS.md, eng-qa sub-step 11f) is the test deliverable for the `/contract-design` skill.

| Requirement | Evidence | Status |
|-------------|----------|--------|
| BDD scenarios use Given/When/Then Gherkin format (H-20) | The architecture does not enumerate specific BEHAVIOR_TESTS.md scenarios for /contract-design (consistent with Step 10 approach). The BDD behavior test pattern from Step 9 F-16 applies: Given [precondition], When [agent/action], Then [observable outcome]. Eng-qa must produce scenarios covering the skill's functional boundaries. Minimum scenario count derived independently below. | **PASS (design framework)** |
| Minimum scenario count covers main acceptance criteria | **Derivation from /contract-design acceptance criteria:** The minimum scenario count is derived from the skill's functional boundaries: (1) cd-generator UC-to-contract transformation has 4 mandatory coverage areas: valid INTERACTION_DEFINED input produces OpenAPI file (happy path), input rejection (missing interactions block), HTTP method inference (high-confidence and low-confidence cases), extension-to-error-response mapping -- requiring 4 scenarios minimum; (2) cd-generator PROTOTYPE labeling enforcement (x-prototype: true in generated contracts) is a critical safety mechanism requiring 1 scenario minimum; (3) cd-validator validation pipeline has 3 mandatory coverage areas: structural validity check (PASS and FAIL cases), traceability completeness check (100% and partial coverage), and PROTOTYPE label verification -- requiring 3 scenarios minimum; (4) cross-agent pipeline integration (cd-generator output consumed by cd-validator via filesystem) requires 1 integration scenario. Derived minimum: 4 + 1 + 3 + 1 = **9 scenarios**. This exceeds the Step 10 minimum of 7, reflecting the greater functional scope of two distinct transformation stages (generation and validation) plus the PROTOTYPE safety mechanism. | **PASS (design framework)** |
| BDD test-first ordering: F-16 is the terminal deliverable | Architecture File Responsibility Matrix places F-16 as eng-qa sub-step 11f, authored after all other files. All implementation files (F-02 through F-15, F-17) constitute the implementation. F-16 establishes the acceptance criteria before the skill is declared complete. | **PASS** |
| 90% line coverage (H-20 sub-item) | H-20 sub-item mandates >= 90% line coverage for Python test suites. F-16 is a Markdown BDD specification file, not a Python test suite. The /contract-design skill has no Python implementation files -- it is a pure Markdown/YAML skill. H-20 line coverage sub-item is not applicable to F-16. Consistent with the Step 10 N/A ruling for F-14. | **N/A (no Python)** |

**H-20 assessment summary:** The F-16 design framework satisfies H-20 BDD test-first requirements. Eng-qa must enumerate at least 9 concrete Given/When/Then scenarios before the skill is declared complete. The 9-scenario minimum is independently derived from /contract-design acceptance criteria (generation happy path, input rejection, HTTP method inference, extension mapping, PROTOTYPE labeling, validation structural check, traceability completeness, PROTOTYPE label verification, cross-agent pipeline). Architecture does not enumerate specific stubs for F-16 -- eng-qa must author all scenarios with concrete inputs and verifiable assertions.

**Note for eng-qa (F-16 authoring):** Scenarios must use specific concrete inputs: specific UC artifact path with realization_level = INTERACTION_DEFINED, specific interaction count, specific HTTP method inference verbs. The worked example in architecture Section 7.1.1 (UC-LIB-001 "Borrow a Book") provides ready-made scenario data (INT-01, POST /loans, CreateLoanRequest, 409 from EXT-2a). References: `skills/use-case/tests/BEHAVIOR_TESTS.md` (Step 9) and `skills/test-spec/tests/BEHAVIOR_TESTS.md` (Step 10) as pattern references for structure and format.

---

### H-22 Trigger Map Entry (Mandatory Skill Usage)

| Requirement | Evidence | Status |
|-------------|----------|--------|
| Trigger map entry designed with all 5 columns | Architecture Section 2 provides: Priority 15, 17 detected keywords, 21 negative keywords, compound triggers (phrase match), skill `/contract-design`. | **PASS** |
| Priority 15 justified relative to adjacent skills | Priority 15 justification documented in architecture: "places /contract-design one level below /test-spec (priority 14) and two levels below /use-case (priority 13). This ordering reflects the pipeline dependency." | **PASS** |
| Negative keywords prevent false positives | "requirements specification", "V&V" suppress /nasa-se co-match. "BDD", "Gherkin", "scenario", "test spec", "feature file" suppress /test-spec co-match. "write use case", "actor goal", "use case model" suppress /use-case co-match. "pricing model", "cloud pricing" suppress /pm-pmm co-match. "documentation", "tutorial" suppress /diataxis co-match. "adversarial", "tournament" suppress /adversary co-match. | **PASS** |
| "API" keyword disambiguation addressed | Architecture Section 2 explicitly explains: "API" alone is excluded from positive keywords because it is ambiguous. Compound triggers require qualification ("API contract", "API specification", "generate contract") to route to /contract-design. AP-02 (Bag of Triggers) collision prevention documented. | **PASS** |
| "schema" keyword disambiguation addressed | Architecture Section 2 explicitly explains: "schema" alone is excluded. "API schema" is the qualifying compound trigger. Prevents routing to /nasa-se (data schema) or other schema-adjacent skills. | **PASS** |
| Priority 15 does not conflict with existing trigger map | /test-spec is at priority 14. /use-case at priority 13. The gap between /contract-design (15) and the next-lower skills (/diataxis and /prompt-engineering at 11) is 4 levels, exceeding the 2-level gap requirement per agent-routing-standards.md Step 3. | **PASS** |

**H-22 summary: 6/6 PASS. Trigger map entry is well-designed with explicit disambiguation for "API" and "schema" keywords.**

---

### Naming Convention Verification

| Standard | Evidence | Status |
|----------|----------|--------|
| AD-M-001 -- `{skill-prefix}-{function}` kebab-case pattern | `cd-generator` (prefix: cd, function: generator). `cd-validator` (prefix: cd, function: validator). Pattern `^[a-z]+-[a-z]+(-[a-z]+)*$` satisfied for both. | **PASS** |
| Prefix consistency (`cd-`) | Both agents use `cd-` prefix, matching the parent skill folder `contract-design` with condensed prefix (consistent with `/use-case` -> `uc-` and `/test-spec` -> `tspec-` patterns established in Steps 9 and 10). | **PASS** |
| No collision with `/diataxis` or other skill prefixes | `cd-` prefix does not collide with any existing production skill prefix. The `/diataxis` skill uses `d-` or `diataxis-` not `cd-`. The engineering team's `eng-` prefix is fully distinct. | **PASS** |
| ORCHESTRATION.yaml name mapping | Architecture Section "ORCHESTRATION.yaml Reconciliation" explicitly maps ORCH names (`contract-generator`, `contract-validator`) to architecture SSOT names (`cd-generator`, `cd-validator`). Reconciliation table provides clear justification: "cd- prefix follows the established naming convention (uc- for /use-case, tspec- for /test-spec, cd- for /contract-design)". | **PASS** |
| "Validator" vs. "Analyst" naming rationale | Architecture Section 3 documents the distinct naming choice: "cd-validator" (not "cd-analyst") because the agent performs deterministic schema validation and binary pass/fail checks, not evaluative analysis. This is the opposite naming rationale from Step 10 where "analyst" was preferred for evaluative coverage analysis. Consistent with cognitive mode alignment: systematic mode suits "validator". | **PASS** |
| File naming follows established patterns | `.md` agent definitions: `{prefix}-{function}.md`. Governance YAML: `{prefix}-{function}.governance.yaml`. Composition files: `{prefix}-{function}.agent.yaml` and `{prefix}-{function}.prompt.md`. Templates: `{type}-template.{ext}`. Rules file: `uc-to-contract-rules.md`. Contract: `CD_SKILL_CONTRACT.yaml`. Tests: `BEHAVIOR_TESTS.md`. Samples: `sample-contract.openapi.yaml`. All follow Step 9 and Step 10 conventions. | **PASS** |

**Naming summary: 6/6 PASS. No naming defects. ORCHESTRATION.yaml name reconciliation fully documented.**

---

### Tool Tier Verification

| Standard | Evidence | Status |
|----------|----------|--------|
| cd-generator T2 (Read-Write) is appropriate | cd-generator reads UC artifacts, rules file, and templates; writes OpenAPI contract files and mapping documents. No external network access, no cross-session state, no delegation. T2 (Read, Write, Edit, Glob, Grep, Bash) exactly matches required capability set. | **PASS** |
| cd-validator T2 (Read-Write) is appropriate | cd-validator reads generated OpenAPI files, source UC artifacts, and mapping documents; writes the validation report file. T2 is the minimum tier supporting both read (validation logic) and write (report output) requirements. Architecture Section 3.2 explicitly documents T1-considered-T2-required reasoning. | **PASS** |
| Neither agent includes Task tool (P-003) | Tools arrays: `[Read, Write, Edit, Glob, Grep, Bash]` for both agents. Task absent in both. P-003 compliant. | **PASS** |
| Tool count within 15-agent threshold (AP-07) | 6 tools per agent. Well below the 15-tool alert threshold from AP-07. No tool selection accuracy risk. | **PASS** |
| Principle of least privilege satisfied | T2 is the lowest tier satisfying both agents' requirements. T3 (external access) not needed -- no external network calls; cd-generator must not consult external API registries (T2 restriction is a security benefit per Section L2 Security Posture Trade-offs). T4 (persistent state) not needed -- no cross-session Memory-Keeper usage. T5 (delegation) not needed -- no Task tool. | **PASS** |

**Tool tier summary: 5/5 PASS. T2 is correctly justified for both agents.**

---

### Cognitive Mode Appropriateness (AD-M-001 through AD-M-009, ET-M-001)

| Standard | Evidence | Status |
|----------|----------|--------|
| AD-M-001 -- Naming follows `{skill-prefix}-{function}` pattern | Verified in [Naming Convention Verification](#naming-convention-verification). | **PASS** |
| AD-M-002 -- Version uses SemVer | `"1.0.0"` for both agents. | **PASS** |
| AD-M-003 -- Description max 1024 chars, no XML, WHAT+WHEN+trigger | cd-generator: approximately 450 characters (architecture lines 246-255), includes WHAT (transforms use case realization artifacts into OpenAPI 3.1 specifications using novel UC-to-contract transformation algorithm), WHEN (generating, creating, deriving, mapping use case interactions to API contracts), triggers (contract generation, OpenAPI from use case, map interactions). cd-validator: approximately 420 characters (architecture lines 405-413), includes WHAT (validates generated OpenAPI 3.1 specifications), WHEN (validating, checking, verifying, auditing), triggers (contract validation, traceability check). Both well within 1024 char limit and contain no XML angle brackets. | **PASS** |
| AD-M-004 -- Output levels declared | cd-generator: `levels: ["L0", "L1"]` (contract file + summary). cd-validator: `levels: ["L0", "L1"]` (validation report + verdict). L0/L1 is appropriate for both: L0 is the generation/validation summary; L1 is the artifact files themselves. cd-validator does not need L2 because it produces operational validation results, not strategic trajectory assessments. | **PASS** |
| AD-M-005 -- `identity.expertise` min 2 specific entries | cd-generator: 3 entries, all specific (UC-to-contract algorithm with IC-05 citation, OpenAPI 3.1 authoring with structural elements enumerated, actor-role mapping with IC-05 and R-06 references). cd-validator: 3 entries, all specific (OpenAPI 3.1 schema validation with structural compliance details, contract-to-UC traceability verification with coverage computation, API design standards compliance). No generic entries. | **PASS** |
| AD-M-006 -- `persona` declared | cd-generator: `tone: "analytical"`, `communication_style: "structured"`, `audience_level: "adaptive"`. cd-validator: `tone: "rigorous"`, `communication_style: "structured"`, `audience_level: "adaptive"`. Both declare persona. cd-validator's "rigorous" tone is appropriate for a validation agent that must report pass/fail verdicts with specific evidence. | **PASS** |
| AD-M-007 -- `session_context` with `on_receive` / `on_send` | cd-generator: 4-item `on_receive` (load and validate UC artifact, count interactions, identify consumer vs. provider interactions, cross-reference supporting_actors), 3-item `on_send` (OpenAPI file path + operation count, key findings, x-prototype status). cd-validator: 3-item `on_receive` (load generated contract and UC artifact, verify both files exist, count interactions and operations), 3-item `on_send` (validation verdict with breakdown, traceability coverage percentage, unmapped interactions list). Both satisfy HR-002 handoff efficiency with 3-5 bullets each. | **PASS** |
| AD-M-008 -- `validation.post_completion_checks` declared | cd-generator: 7 checks (openapi file created, mapping file created, one operation per consumer interaction, x-prototype-true in info section, all operations have traceability, error responses trace to extension conditions, no asyncapi or cloudevents content). cd-validator: 4 checks (validation report created, pass-fail verdict present, traceability matrix present, coverage percentage with numerator/denominator). Both include artifact existence, domain semantic checks, and safety mechanism verification (x-prototype). | **PASS** |
| AD-M-009 -- Model selection justified per cognitive demands | cd-generator: `opus`. Justified (AD-M-009): novel transformation algorithm with no prior art (G-01 gap). Requires complex judgment for resource identification, HTTP method inference, schema structure derivation from natural language. Architecture Section 3.1 documents this explicitly with a downgrade path (evaluate Sonnet after 10+ runs if quality > 0.95). cd-validator: `sonnet`. Justified: procedural systematic activity. Agent follows a defined 9-step protocol. Architecture Section 3.2 documents the Haiku-considered-Sonnet-required reasoning. | **PASS** |
| ET-M-001 -- `reasoning_effort` alignment | cd-generator: `reasoning_effort: max` with C4 classification comment in governance YAML. cd-validator: `reasoning_effort: high` with C3 classification comment. ET-M-001 maps C4=max and C3=high. The cd-generator classification as C4 is justified by the G-01 novel algorithm with no prior art (irreversibility threshold met per architecture Section 3.1 comment). However, the File Responsibility Matrix at lines 98-99 classifies F-02 and F-03 as C3. **This inconsistency is FIND-002 (Medium)** -- ET-M-001 compliance depends on resolving whether cd-generator is C3 or C4. See FIND-002 for analysis and resolution path. | **PENDING (FIND-002)** |

**AD-M and ET-M summary: 9/10 PASS, 1 PENDING (ET-M-001 for cd-generator due to criticality inconsistency in FIND-002). cd-validator is 10/10 PASS.**

---

## Dependency Analysis

### Internal Dependencies (All Within Jerry Framework)

| Dependency | Consumer Files | Type | Status |
|------------|---------------|------|--------|
| `docs/schemas/agent-governance-v1.schema.json` | F-03, F-05 (.governance.yaml validation) | Schema validation | **EXISTS** -- confirmed at `docs/schemas/agent-governance-v1.schema.json` in repo root |
| `docs/schemas/agent-canonical-v1.schema.json` | F-06, F-08 (composition YAML) | Schema reference | **EXISTS** -- `$id: https://jerry-framework.dev/schemas/agent-canonical/v1.0.0`, confirmed as referenced in architecture Section 1 |
| `docs/schemas/use-case-realization-v1.schema.json` | F-02, F-04 (agent system prompt schema ref), F-03, F-05 (output validation ref) | Runtime input validation | **PRODUCED BY STEP 9** -- eng-infra Step 9 Wave 1 (Step 9 F-17). Must exist before /contract-design agents are invoked in production. Not an authoring dependency (agents reference it by path). Runtime dependency only. |
| `skills/use-case/composition/uc-author.agent.yaml` | F-06, F-08 (reference implementation pattern) | Pattern reference | **EXISTS** -- produced by Step 9 eng-backend |
| `skills/test-spec/composition/tspec-generator.agent.yaml` | F-06, F-08 (alternate reference pattern; closer structural analog to cd-generator) | Pattern reference | **EXISTS** -- produced by Step 10 eng-backend |
| `skills/test-spec/contracts/TS_SKILL_CONTRACT.yaml` | F-15 (adaptation template) | Pattern reference | **EXISTS** -- produced by Step 10 eng-lead |
| `docs/governance/JERRY_CONSTITUTION.md` | F-03, F-05 (`constitution.reference` field) | Reference | **EXISTS** -- standard path |
| `skills/contract-design/rules/uc-to-contract-rules.md` (F-14) | F-02 (cd-generator `<methodology>` section runtime load) | Runtime methodology reference | **PRODUCED BY THIS SKILL** -- created at Wave 2b (eng-backend). F-02 agent definition is syntactically valid without F-14, but cd-generator will fail at runtime if F-14 does not exist when it loads the rules file. Wave 2b (F-14) must complete before production invocations of cd-generator. |
| `skills/contract-design/templates/openapi-template.yaml` (F-10) | F-02 (cd-generator output template reference) | Runtime template reference | **PRODUCED BY THIS SKILL** -- created at Wave 3. Agent definition references template by path. |
| `skills/contract-design/templates/json-schema-template.json` (F-13) | F-02 (cd-generator secondary template reference for schema components) | Runtime template reference | **PRODUCED BY THIS SKILL** -- created at Wave 3. |

### Registration Prerequisites (Before Routing Works)

The three registration files must be updated by eng-lead before `/contract-design` can be invoked via keyword routing. Until registration is complete, the skill can only be invoked via explicit `/contract-design` slash command.

| File | Change Required | Priority |
|------|----------------|----------|
| `CLAUDE.md` | Add `/contract-design` row to Quick Reference Skills table | HIGH -- affects skill discoverability |
| `AGENTS.md` | Add `/contract-design Skill Agents` section; update Agent Summary count | MEDIUM -- affects agent discovery |
| `.context/rules/mandatory-skill-usage.md` | Insert priority-15 trigger map row after priority-14 `/test-spec` entry | HIGH -- affects H-22 proactive invocation |

**Exact trigger map row for mandatory-skill-usage.md (5-column enhanced format per agent-routing-standards.md):**

| Detected Keywords | Negative Keywords | Priority | Compound Triggers | Skill |
|---|---|---|---|---|
| contract design, contract-design, API contract, OpenAPI, API spec, API specification, generate contract, contract from use case, API schema, endpoint design, operation mapping, request response schema, API generation, REST contract, swagger, use case to API, interaction to contract | requirements specification, V&V, technical review, use case model, actor goal, write use case, BDD, Gherkin, scenario, test spec, feature file, adversarial, tournament, transcript, penetration, exploit, code review, pricing model, cloud pricing, documentation, tutorial | 15 | "API contract" OR "contract design" OR "OpenAPI" OR "generate contract" OR "contract from use case" OR "API specification" OR "use case to API" (phrase match) | `/contract-design` |

### External Dependencies

None. The `/contract-design` skill has no external package dependencies, no external API calls, no MCP server requirements. This is a T2 (Read-Write) skill operating entirely on local filesystem artifacts and the shared use case schema. The deferred AsyncAPI and CloudEvents templates reference external specifications as documentation citations only, not runtime dependencies.

### Blockers

None blocking implementation start. All Wave 1 prerequisites exist:
- `docs/schemas/agent-governance-v1.schema.json` -- exists
- `docs/schemas/agent-canonical-v1.schema.json` -- exists
- Reference composition file patterns (uc-author.agent.yaml, tspec-generator.agent.yaml) -- exist
- `skills/test-spec/contracts/TS_SKILL_CONTRACT.yaml` (F-15 pattern template) -- exists

**FIND-002 is advisory, not a blocker.** Eng-backend can begin Wave 1 while the C3/C4 criticality classification for cd-generator is resolved by eng-lead. The governance YAML content (including `reasoning_effort: max`) is correct regardless of which criticality label is applied to the file; only the file responsibility matrix row classification needs resolution.

---

## Implementation Plan

### Dependency Graph

```
[F-02] cd-generator.md                           (eng-backend, Wave 1, no internal deps)
[F-03] cd-generator.governance.yaml              (eng-backend, Wave 1, parallel with F-02)
[F-04] cd-validator.md                           (eng-backend, Wave 1, parallel with F-02)
[F-05] cd-validator.governance.yaml              (eng-backend, Wave 1, parallel with F-02)
   |
   +---> [F-06] cd-generator.agent.yaml          (eng-backend, Wave 2a, depends on F-02)
   |     [F-07] cd-generator.prompt.md           (eng-backend, Wave 2a, depends on F-02, copy of body + sync note)
   |     [F-08] cd-validator.agent.yaml          (eng-backend, Wave 2a, depends on F-04)
   |     [F-09] cd-validator.prompt.md           (eng-backend, Wave 2a, depends on F-04, copy of body + sync note)
   |
[F-14] uc-to-contract-rules.md                   (eng-backend, Wave 2b, no dep beyond methodology knowledge)
   |
[F-10] openapi-template.yaml                     (eng-backend, Wave 3a, parallel -- no internal deps)
[F-11] asyncapi-template.yaml                    (eng-backend, Wave 3a, parallel with F-10, scaffolding)
[F-12] cloudevents-template.yaml                 (eng-backend, Wave 3a, parallel with F-10, scaffolding)
[F-13] json-schema-template.json                 (eng-backend, Wave 3a, parallel with F-10)
[F-17] sample-contract.openapi.yaml              (eng-backend, Wave 3b, depends on F-10 template pattern)
   |
[F-01] SKILL.md                                  (eng-lead, Wave 4, depends on F-02..F-05 for agent table)
[F-15] CD_SKILL_CONTRACT.yaml                    (eng-lead, Wave 4, depends on F-02..F-05 for schema refs)
   |
Wave 4b -- Registration (eng-lead, depends on F-01):
   - CLAUDE.md skill table entry
   - AGENTS.md section (cd-generator, cd-validator entries)
   - mandatory-skill-usage.md trigger map row (priority 15)
   |
[F-16] BEHAVIOR_TESTS.md                         (eng-qa, Wave 5, depends on F-01..F-15, F-17)
```

### Ordered Creation Schedule

**Wave 1 -- Agent Definitions (no internal dependencies, create in parallel):**

All 4 files can be created in parallel. These are the critical-path foundation.

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-02 | `skills/contract-design/agents/cd-generator.md` | eng-backend | C3 (advisory: see FIND-002) | Official frontmatter + 7 XML-tagged body sections per system prompt outline in architecture Section 3.1. Do NOT include `reasoning_effort` in .md; it belongs in .governance.yaml (F-03). Description: verbatim from architecture Section 3.1 frontmatter block. Tools: `[Read, Write, Edit, Glob, Grep, Bash]`. Model: `opus`. |
| F-03 | `skills/contract-design/agents/cd-generator.governance.yaml` | eng-backend | C3 (advisory: see FIND-002) | Must validate against `docs/schemas/agent-governance-v1.schema.json`. `reasoning_effort: max` is specified in architecture (C4 justification for G-01 novel algorithm). Use verbatim governance YAML block from architecture Section 3.1 as source. Manual field-by-field inspection against required fields: `version`, `tool_tier`, `identity.role`, `identity.expertise` (min 2), `identity.cognitive_mode`. Root `additionalProperties: true` accepts `reasoning_effort` without schema error. |
| F-04 | `skills/contract-design/agents/cd-validator.md` | eng-backend | C3 | Same structural requirements as F-02. Source: architecture Section 3.2 frontmatter and system prompt outline. Cognitive mode: `systematic`. Model: `sonnet`. Tools: same T2 set. |
| F-05 | `skills/contract-design/agents/cd-validator.governance.yaml` | eng-backend | C3 | Same structural requirements as F-03. Source: architecture Section 3.2 governance YAML block. `reasoning_effort: high` (C3 mapping -- no inconsistency). Manual field-by-field inspection before Wave 2a begins. |

**Wave 2a -- Composition Files (depend on Wave 1):**

All 4 files can be created in parallel once Wave 1 is complete.

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-06 | `skills/contract-design/composition/cd-generator.agent.yaml` | eng-backend | C2 | Follows `docs/schemas/agent-canonical-v1.schema.json`. Primary reference: `skills/test-spec/composition/tspec-generator.agent.yaml` (closer structural analog). Set `skill: contract-design`, `tool_tier: T2`, `tools.forbidden: [agent_delegate]`. Identity fields from F-02 governance YAML. |
| F-07 | `skills/contract-design/composition/cd-generator.prompt.md` | eng-backend | C2 | Copy of F-02 markdown body. MUST add synchronization note header at top: "Synchronization note: This file is a manually-maintained copy of the markdown body from `skills/contract-design/agents/cd-generator.md`. When updating cd-generator.md, this file MUST be updated in the same commit." (See FIND-004.) |
| F-08 | `skills/contract-design/composition/cd-validator.agent.yaml` | eng-backend | C2 | Same pattern as F-06 for validator. Set `skill: contract-design`, `tool_tier: T2`, `tools.forbidden: [agent_delegate]`. |
| F-09 | `skills/contract-design/composition/cd-validator.prompt.md` | eng-backend | C2 | Copy of F-04 markdown body. Same synchronization note header as F-07, adapted for cd-validator.md. |

**Wave 2b -- Rules File (no internal dependencies, can parallel with Wave 2a):**

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-14 | `skills/contract-design/rules/uc-to-contract-rules.md` | eng-backend | C3 | Source: architecture Section 4.5 (complete specification with section outline and rule format). Must implement: RULE-RI-01 through RULE-RI-03 (resource identification), RULE-OM-01 through RULE-OM-04 (operation mapping), RULE-HM-01 through RULE-HM-05 (HTTP method inference), RULE-SD-01 through RULE-SD-04 (schema derivation), RULE-ER-01 through RULE-ER-03 (error response), RULE-AR-01 through RULE-AR-03 (actor role), RULE-TR-01 through RULE-TR-02 (traceability). Total minimum: 22 rules. HTTP method inference rules must cite RFC 9110 (Section 9) per architecture Section 7.2. Target size: < 500 lines per CB-05. Navigation table required (H-23 -- file will exceed 30 lines). Rule format: `RULE-{CATEGORY}-{NN}: {imperative statement}. Input: {schema fields read}. Output: {OpenAPI element produced}. Example: {concrete mapping example}`. The worked example in architecture Section 7.1.1 provides ready-made examples for RULE-RI-01, RULE-OM-01, RULE-HM-02, RULE-SD-01, RULE-SD-02, RULE-ER-01d, RULE-AR-03. |

**Wave 3a -- Templates (no internal dependencies, can parallel with Waves 1 and 2):**

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-10 | `skills/contract-design/templates/openapi-template.yaml` | eng-backend | C3 | Source: architecture Section 4.1 (verbatim template block). Active in v1.0.0. Must include all placeholder fields: `{{UC_TITLE}}`, `{{CONTRACT_VERSION}}`, `{{UC_ID}}`, `{{UC_ARTIFACT_PATH}}`, `{{GENERATION_TIMESTAMP}}`, `{{UC_SCOPE}}`, `{{PRIMARY_ACTOR}}`, and all path/operation placeholders. Template is fully specified -- copy verbatim. |
| F-11 | `skills/contract-design/templates/asyncapi-template.yaml` | eng-backend | C2 | Source: architecture Section 4.2 (verbatim template block). Scaffolding only -- `x-deferred: true`. Deferred per DI-07, ASM-005, G-02. Copy verbatim with deferred header. No generation logic in v1.0.0. |
| F-12 | `skills/contract-design/templates/cloudevents-template.yaml` | eng-backend | C2 | Source: architecture Section 4.3 (verbatim template block). Scaffolding only -- `x-deferred: true`. Same deferred status as F-11. Copy verbatim. |
| F-13 | `skills/contract-design/templates/json-schema-template.json` | eng-backend | C2 | Source: architecture Section 4.4 (verbatim template block). Active in v1.0.0 -- shared schema definitions. Must include `$schema`, `$id`, `x-prototype: true`, `$defs` with request/response schema placeholders. Copy verbatim. |

**Wave 3b -- Sample File (depends on F-10 template pattern):**

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-17 | `skills/contract-design/samples/sample-contract.openapi.yaml` | eng-backend | C2 | Demonstrative OpenAPI 3.1 output from the UC-LIB-001 "Borrow a Book" worked example in architecture Section 7.1.1. The worked example provides complete output (POST /loans, CreateLoanRequest, CreateLoanResponse, 409 Conflict from EXT-2a). Use verbatim output from the worked example section as the sample. Must carry `x-prototype: true` in info section. No placeholder fields -- this is a concrete, populated example. |

**Wave 4 -- Skill Entry Points (depend on Wave 1 agent definitions for agent table):**

Both can be created in parallel. Eng-lead authors both.

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-01 | `skills/contract-design/SKILL.md` | eng-lead | C3 | Requires all 14 skill-standards.md body sections. Key authoring notes: (1) Section 7 P-003 diagram: copy directly from architecture Section 6 P-003 topology block (this is already specified -- no gap). (2) Section 8 invocation patterns: three modes required (natural language, explicit agent, Task tool code block). (3) Sections 1, 3, 14 standard boilerplate. (4) Section 2 navigation table with anchor links required (H-23). References: `skills/use-case/SKILL.md` and `skills/test-spec/SKILL.md` as pattern references. After authoring, proceed to Wave 4b registration. |
| F-15 | `skills/contract-design/contracts/CD_SKILL_CONTRACT.yaml` | eng-lead | C2 | Adapt `skills/test-spec/contracts/TS_SKILL_CONTRACT.yaml` pattern. Two agents (cd-generator, cd-validator). Schema `$ref` to `docs/schemas/use-case-realization-v1.schema.json` for input type. Output schemas: OpenAPI contract YAML for cd-generator; validation report structure for cd-validator. OpenAPI 3.0-inspired format per architecture Section 1 skill contract specification. |

**Wave 4b -- Registration (depends on F-01, eng-lead):**

| Action | File | Owner | Notes |
|--------|------|-------|-------|
| Register skill | `CLAUDE.md` -- Skills table | eng-lead | Add `/contract-design` row to Quick Reference Skills table. |
| Register agents | `AGENTS.md` | eng-lead | Add "/contract-design Skill Agents" section with cd-generator and cd-validator entries. Update Agent Summary count. |
| Register trigger | `.context/rules/mandatory-skill-usage.md` | eng-lead | Insert the 5-column trigger map row at priority 15. Insert AFTER the priority-14 `/test-spec` row to preserve ordering. See FIND-006 ordering note. |

**Wave 5 -- Tests (depends on all Wave 1-4 files):**

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-16 | `skills/contract-design/tests/BEHAVIOR_TESTS.md` | eng-qa | C3 | Minimum 9 scenarios in proper Given/When/Then Gherkin syntax. Scenarios must cover: (1) cd-generator happy path (valid INTERACTION_DEFINED UC -> OpenAPI file created with x-prototype: true), (2) cd-generator input rejection (missing interactions block), (3) cd-generator HTTP method inference (high-confidence case: "requests" -> POST), (4) cd-generator HTTP method inference (low-confidence case -> default POST with x-method-inference annotation), (5) cd-generator PROTOTYPE labeling enforcement (x-prototype: true must be present in generated contract), (6) cd-validator structural validity check (valid OpenAPI passes), (7) cd-validator traceability completeness (100% consumer interactions mapped -> PASS), (8) cd-validator traceability gap detection (one consumer interaction unmapped -> FAIL with specific gap listed), (9) cross-agent pipeline integration (cd-generator output consumed by cd-validator). Navigation table required (H-23). Reference: `skills/test-spec/tests/BEHAVIOR_TESTS.md` for format. Use UC-LIB-001 worked example data from architecture Section 7.1.1 as concrete scenario input. |

### Critical Path

```
F-02..F-05 (agent defs, Wave 1)
  --> F-06..F-09 (composition, Wave 2a)
    --> F-01 (SKILL.md, Wave 4)
      --> Registration (Wave 4b)
        --> F-16 (tests, Wave 5)
```

The critical path is 5 waves, identical in structure to Step 10. F-10..F-14, F-17 are off the critical path and can be developed concurrently with Waves 1 and 2a.

**F-14 runtime dependency note:** F-14 (`uc-to-contract-rules.md`) is off the critical path for agent definition structural validity -- `cd-generator.md` references F-14 by path in its `<methodology>` section but remains syntactically valid without it. However, F-14 is on the critical path for correct runtime operation: cd-generator will produce low-quality or incorrect OpenAPI if it cannot load the transformation rules. Wave 2b should complete F-14 before production invocations occur. Treat F-14 as a Wave 1/2 parallel task.

**F-17 sample file note:** F-17 is off the critical path (it is a sample, not a dependency for any other file). However, it provides valuable demonstration material for the BEHAVIOR_TESTS.md worked examples in Wave 5. Completing F-17 before Wave 5 is recommended.

---

## File Responsibility Matrix

All 17 files to create, with responsible agent and criticality.

| File ID | Path | Author | Sub-Step | Reviewer | Criticality | Notes |
|---------|------|--------|----------|----------|-------------|-------|
| F-01 | `skills/contract-design/SKILL.md` | eng-lead | 11a | eng-reviewer | C3 | 14-section SKILL.md body. P-003 diagram specified in architecture Section 6. |
| F-02 | `skills/contract-design/agents/cd-generator.md` | eng-backend | 11b | eng-security, eng-reviewer | C3 | Official frontmatter + 7 XML-tagged sections. FIND-002 advisory. |
| F-03 | `skills/contract-design/agents/cd-generator.governance.yaml` | eng-backend | 11b | eng-security, eng-reviewer | C3 | Must pass `agent-governance-v1.schema.json`. `reasoning_effort: max`. FIND-002 advisory. |
| F-04 | `skills/contract-design/agents/cd-validator.md` | eng-backend | 11b | eng-security, eng-reviewer | C3 | Same structural requirements as F-02. Cognitive mode: systematic. |
| F-05 | `skills/contract-design/agents/cd-validator.governance.yaml` | eng-backend | 11b | eng-security, eng-reviewer | C3 | Same structural requirements as F-03. `reasoning_effort: high`. No inconsistency. |
| F-06 | `skills/contract-design/composition/cd-generator.agent.yaml` | eng-backend | 11c | eng-reviewer | C2 | Follows agent-canonical schema. Primary reference: tspec-generator.agent.yaml. |
| F-07 | `skills/contract-design/composition/cd-generator.prompt.md` | eng-backend | 11c | eng-reviewer | C2 | Copy of F-02 body. MUST add synchronization note header (FIND-004). |
| F-08 | `skills/contract-design/composition/cd-validator.agent.yaml` | eng-backend | 11c | eng-reviewer | C2 | Same as F-06 pattern for validator. |
| F-09 | `skills/contract-design/composition/cd-validator.prompt.md` | eng-backend | 11c | eng-reviewer | C2 | Copy of F-04 body. MUST add synchronization note header (FIND-004). |
| F-10 | `skills/contract-design/templates/openapi-template.yaml` | eng-backend | 11d | eng-reviewer | C3 | Verbatim from architecture Section 4.1. Active template. |
| F-11 | `skills/contract-design/templates/asyncapi-template.yaml` | eng-backend | 11d | eng-reviewer | C2 | Verbatim from architecture Section 4.2. Scaffolding (x-deferred: true). |
| F-12 | `skills/contract-design/templates/cloudevents-template.yaml` | eng-backend | 11d | eng-reviewer | C2 | Verbatim from architecture Section 4.3. Scaffolding (x-deferred: true). |
| F-13 | `skills/contract-design/templates/json-schema-template.json` | eng-backend | 11d | eng-reviewer | C2 | Verbatim from architecture Section 4.4. Active template. |
| F-14 | `skills/contract-design/rules/uc-to-contract-rules.md` | eng-backend | 11e | eng-reviewer | C3 | Min 22 rules covering 7 rule categories. < 500 lines. Navigation table required. |
| F-15 | `skills/contract-design/contracts/CD_SKILL_CONTRACT.yaml` | eng-lead | 11a | eng-reviewer | C2 | OpenAPI 3.0 inspired. Two agents. Schema $ref. |
| F-16 | `skills/contract-design/tests/BEHAVIOR_TESTS.md` | eng-qa | 11f | eng-reviewer | C3 | Min 9 BDD scenarios. Navigation table required. |
| F-17 | `skills/contract-design/samples/sample-contract.openapi.yaml` | eng-backend | 11d | eng-reviewer | C2 | UC-LIB-001 worked example output. Must carry x-prototype: true. |

**Eng-lead authors:** F-01, F-15, and the three registration actions (Wave 4b).
**Eng-backend authors:** F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-11, F-12, F-13, F-14, F-17 (14 files).
**Eng-qa authors:** F-16.

---

## Findings

### FIND-001 -- Low: File Count Discrepancy Between Directory Tree and File Manifest

**Standard:** P-001 (truth and accuracy) -- document must be internally consistent.

**Evidence:** Architecture line 60 states "14 files to create" and the directory tree (lines 64-90) enumerates 14 items (F-01 through F-14). However, the File Responsibility Matrix (lines 96-109) lists 17 entries: F-01 through F-09 (9 agent/composition files), F-10 through F-13 (4 templates), F-14 (rules), F-15 (skill contract), F-16 (behavior tests), and F-17 (sample). The directory tree omits F-15 (`contracts/CD_SKILL_CONTRACT.yaml`) from the tree listing even though it includes the `contracts/` directory. F-16 and F-17 appear in the tree as `tests/BEHAVIOR_TESTS.md` and `samples/sample-contract.openapi.yaml` respectively, confirming they are intended. The discrepancy is between the stated count ("14 files") and the actual manifest (17 files as evidenced by the responsibility matrix).

**Impact:** Engages all downstream agents with a potentially confusing count reference. If eng-backend interprets "14 files" as the canonical count, they may not author F-15, F-16, or F-17. The responsibility matrix is authoritative; the "14 files" statement and directory tree are inconsistent with it.

**Recommendation:** Eng-lead to establish canonical file count as **17 files** (F-01 through F-17 per the File Responsibility Matrix). No architecture revision needed for implementation to proceed. The responsibility matrix and directory tree together are sufficient for authoring.

**Action:** Treat this as a documentation note. The implementation plan above uses 17 files as the canonical count. Eng-lead to notify eng-backend that the correct file count is 17.

---

### FIND-002 -- Medium: cd-generator Criticality Classification Inconsistency (ET-M-001)

**Standard:** ET-M-001 -- Agent definitions SHOULD declare `reasoning_effort` aligned with criticality level. Mapping: C1=default, C2=medium, C3=high, C4=max.

**Evidence:** The cd-generator governance YAML (F-03) declares `reasoning_effort: max` with a comment: "ET-M-001 compliance: reasoning_effort: max (C4 agent -- G-01 no prior art, novel algorithm)" and "C4 classification: novel transformation algorithm with no prior art (G-01); governs API contract structure that feeds downstream code generation (irreversibility threshold met)". However, the File Responsibility Matrix (lines 98-99) classifies F-02 and F-03 as C3.

**Analysis:** Two independent criticality assessments are being applied:

1. The governance YAML applies **C4** because: (a) the UC-to-contract algorithm is novel with no prior art (G-01), (b) it governs API contract structure that feeds downstream code generation (irreversibility threshold), and (c) per quality-enforcement.md C4 definition: "Irreversible, architecture/governance/public."

2. The File Responsibility Matrix applies **C3** which is the standard AE-002 auto-escalation level for skill governance files: "Touches `skills/` [governance artifacts] -- Auto-C3 minimum."

Both classifications are defensible. C4 is justified by G-01 and the downstream code generation impact. C3 is the AE-002 minimum floor for governance artifacts in skills/. The confusion arises because the architecture applies both in different places.

**Resolution path:** Two options:
- Option A (Recommended): Adopt C4 for F-02 and F-03 in the File Responsibility Matrix. The `reasoning_effort: max` declaration is correct and reflects the actual risk profile. Update the File Responsibility Matrix notes to reference the C4 basis (G-01 novel algorithm, downstream code generation irreversibility).
- Option B: Adopt C3 for the responsibility matrix (AE-002 floor) and change `reasoning_effort: max` to `high` in F-03 to match C3. This reduces caution on the highest-risk agent in the three-skill pipeline.

Option A is recommended: the G-01 risk is genuine, the reasoning_effort: max declaration is already correct, and changing it would reduce quality assurance on a novel algorithm. The cost is one responsibility matrix field update.

**Impact:** Without resolution, eng-backend may author F-03 at the wrong criticality level, affecting how eng-security and eng-reviewer apply their review standards.

**Action:** Eng-lead to resolve criticality classification for F-02/F-03 before Wave 1 begins. Recommended resolution: update File Responsibility Matrix to C4 for F-02 and F-03. Add ORCHESTRATION.yaml update note if the criticality affects the review gate threshold.

---

### FIND-003 -- Medium: SKILL.md Section 8 Invocation Patterns Not Specified in Architecture

**Standard:** skill-standards.md §8 (required for multi-agent skills) -- SKILL.md MUST include three invocation options: (a) natural language, (b) explicit agent, (c) Task tool code block.

**Evidence:** Architecture Section 2 ("SKILL.md Design") specifies the SKILL.md content in detail (frontmatter, routing keywords, agent routing table, when-to-use, integration points). Section 8 "Invoking an Agent" content is not enumerated in the architecture. Unlike Section 7 (P-003 diagram -- which IS specified in architecture Section 6), Section 8 has no equivalent source specification in the architecture.

**Impact:** Without explicit specification, eng-lead must author Section 8 from scratch during F-01 authoring. This is non-trivial because Task tool code blocks reference composition file paths that must be exact. If eng-lead uses incorrect composition file paths, the Task invocation pattern will be non-functional.

**Recommendation:** Eng-lead to author Section 8 using this pattern:

```markdown
### Invoking an Agent

**Option A -- Natural Language:**
"Generate an API contract from use case UC-LIB-001 stored at projects/PROJ-021-use-case/use-cases/UC-LIB-001-borrow-a-book.md"

**Option B -- Explicit Agent:**
"Use cd-generator to transform the interactions from UC-LIB-001 into an OpenAPI 3.1 contract"

**Option C -- Task Tool (via composition file):**
Task({
  "agent": "skills/contract-design/composition/cd-generator.agent.yaml",
  "context": {
    "artifact_path": "projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md",
    "output_path": "projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}.openapi.yaml",
    "success_criteria": ["At least 1 OpenAPI path per consumer interaction", "x-prototype: true in info section", "Mapping document created"]
  }
})
```

Validate: follow cd-validator after cd-generator by invoking `skills/contract-design/composition/cd-validator.agent.yaml` with `contract_path` and `artifact_path` parameters.

**Action:** Eng-lead to author Section 8 during F-01 authoring using the pattern above. Reference: `skills/test-spec/SKILL.md` Section 8 (tspec-generator/tspec-analyst invocation patterns from Step 10) as structural model.

---

### FIND-004 -- Medium: Composition File Synchronization Protocol Required for F-07 and F-09

**Standard:** P-001 (truth and accuracy) -- artifact content must be accurate and consistent. Pattern from Step 10 FIND-002 (executed action) and Step 9 FIND-004 (executed action).

**Evidence:** F-07 (`cd-generator.prompt.md`) and F-09 (`cd-validator.prompt.md`) are described in the architecture as "copies of the markdown body from the agent `.md` file." The Step 9 implementation resolved this for `/use-case` by adding a synchronization note to `uc-author.prompt.md`. Step 10 replicated this for `/test-spec` (`tspec-generator.prompt.md`, `tspec-analyst.prompt.md`). The same protocol must be applied to F-07 and F-09.

**Impact:** If F-02 or F-04 are updated post-implementation, the composition prompt files could become stale, causing Task-invoked agents to use outdated methodology or guardrails. At this point the framework will have 6 manually-synchronized composition prompt file pairs (2 from /use-case, 2 from /test-spec, 2 from /contract-design). The synchronization note is the established mitigation. As noted in Step 10 L2, the authoritative fix is an automated CI parity check (eng-devsecops scope, referenced as eng-devsecops scope in Step 9 FIND-004).

**Recommendation:** Eng-backend to add the following note at the top of F-07 and F-09 (before the `<identity>` section):

> `Synchronization note: This file is a manually-maintained copy of the markdown body from skills/contract-design/agents/cd-generator.md (or cd-validator.md). When updating the corresponding agent .md file, this file MUST be updated in the same commit.`

**Action:** Eng-backend to add the synchronization note header during Wave 2a authoring of F-07 and F-09. This mirrors the established pattern from Steps 9 and 10.

---

### FIND-005 -- Low: H-26 Registration Actions Must Execute After F-01

**Standard:** H-26(c) -- New skills MUST be registered in CLAUDE.md, AGENTS.md, and mandatory-skill-usage.md. H-32 -- GitHub Issue parity for Jerry repo work items.

**Evidence:** The three registration actions are correctly assigned to eng-lead at sub-step 11a but depend on F-01 (SKILL.md) being authored first. Registration actions before F-01 is complete would cause stale registrations if SKILL.md content changes.

**Impact:** If registration occurs before F-01 is finalized, the CLAUDE.md and AGENTS.md entries may reference incorrect agent counts or routing information. The trigger map row is stable (designed in architecture) but the AGENTS.md entry requires accurate output location information from the finalized governance YAML.

**Action (tracked in this review):** Registration actions are tracked in Wave 4b above. The exact trigger map row is reproduced in the Dependency Analysis section. Eng-reviewer close-out checklist for the `/contract-design` skill MUST verify that all three registration files have been updated before marking implementation complete.

---

### FIND-006 -- Low: Trigger Map Row Must Be Inserted After Priority-14 /test-spec Entry

**Standard:** agent-routing-standards.md Priority Ordering -- trigger map rows must maintain ascending priority order for routing resolution algorithm clarity.

**Evidence:** The `/contract-design` trigger map row at priority 15 must be inserted immediately after the priority-14 `/test-spec` row in `mandatory-skill-usage.md`. The Step 10 review established the `/test-spec` priority-14 row as a prerequisite. Both priority-14 and priority-15 rows must be present and ordered correctly.

**Impact:** Incorrect ordering does not break routing functionality (the routing algorithm uses numeric comparison, not table order), but creates maintenance confusion. The trigger map table is an H-22 compliance artifact and should accurately represent the routing priority structure.

**Action:** Eng-lead to verify that the mandatory-skill-usage.md trigger map table is sorted by priority (ascending) after `/use-case` (13), `/test-spec` (14), and `/contract-design` (15) rows are all present. Insert /contract-design row after the /test-spec row.

---

### FIND-007 -- Low: F-14 uc-to-contract-rules.md Rule Count Minimum Requires Clarification

**Standard:** P-001 (truth and accuracy) -- implementation deliverables must be sufficiently specified for authoring.

**Evidence:** Architecture Section 4.5 enumerates rule categories for `uc-to-contract-rules.md` with counts: RULE-RI-01 through RULE-RI-03 (3), RULE-OM-01 through RULE-OM-04 (4), RULE-HM-01 through RULE-HM-05 (5), RULE-SD-01 through RULE-SD-04 (4), RULE-ER-01 through RULE-ER-03 (3), RULE-AR-01 through RULE-AR-03 (3), RULE-TR-01 through RULE-TR-02 (2). Total: 24 rules across 7 categories. However, the worked example in Section 7.1.1 references rule variants within the RULE-ER category (RULE-ER-01a through RULE-ER-01f -- 6 sub-variants of RULE-ER-01 alone). The architecture's Section 7.3 Extension-to-Error-Response Mapping table defines 6 error patterns (RULE-ER-01a through RULE-ER-01f) plus RULE-ER-02 and one unclassified fallback. This means RULE-ER-01 is actually 6 sub-rules, not 1.

**Impact:** Eng-backend may author only 3 ER rules (RULE-ER-01, RULE-ER-02, RULE-ER-03) instead of the full extension pattern library (RULE-ER-01a through RULE-ER-01f plus RULE-ER-02 and RULE-ER-03 = 8 effective rules). This would make the rules file incomplete relative to the architecture's transformation algorithm.

**Recommendation:** The implementation plan above specifies minimum 22 rules. For ER category: author RULE-ER-01 as a parent rule with 6 sub-variants (RULE-ER-01a through RULE-ER-01f) exactly as enumerated in architecture Section 7.3, plus RULE-ER-02 and RULE-ER-03. The parent-rule-with-sub-variant pattern is semantically rich and helps cd-generator apply the right sub-rule without over-complicating the primary rule count.

**Action:** Eng-backend to author RULE-ER sub-variants (RULE-ER-01a through RULE-ER-01f) following the architecture Section 7.3 table exactly. These sub-variants represent the complete extension condition pattern library.

---

## GATE-4 Carryforward

This section documents items from the `/test-spec` Step 10 implementation (FIND-001 through FIND-004, PRE-01, REC-01) that have direct relevance to `/contract-design` implementation.

| Step 10 Finding | Status | Impact on /contract-design |
|-----------------|--------|----------------------------|
| FIND-001 (SKILL.md Section 7 P-003 diagram not specified) | **RESOLVED in architecture** -- Architecture Section 6 explicitly includes the P-003 topology diagram for /contract-design. No gap exists. | No action required. |
| FIND-002 (Composition file synchronization protocol) | **Active requirement** -- Same technical debt applies to F-07 and F-09. | FIND-004 in this review mandates synchronization notes for F-07 and F-09. Action tracked. |
| FIND-003 (H-26 registration tracking) | **Replicated** -- Same tracking pattern applied in this review. | FIND-005 and FIND-006 establish registration tracking for /contract-design. |
| FIND-004 (Trigger map ordering) | **Replicated** -- Same ordering concern applies for priority 15. | FIND-006 mandates priority 15 insertion after priority 14. |

**PRE-01 (Pipeline input prerequisite):** The `/contract-design` input validation gate requires `$.realization_level = INTERACTION_DEFINED` and `$.interactions` non-empty. This is a stricter gate than `/test-spec` which requires only `$.detail_level >= ESSENTIAL_OUTLINE`. UC artifacts produced by `/use-case` default to BULLETED_OUTLINE, which does not satisfy `/test-spec`. UC artifacts at INTERACTION_DEFINED are explicitly a post-uc-slicer Activity 5 output -- requiring the `uc-slicer` agent specifically. This friction is documented in the architecture (Section 5 error messages guide users to uc-slicer). Eng-backend must include clear rejection messages with actionable guidance in cd-generator's `<guardrails>` section per architecture Section 5 input gate table. The WAIT behavior ("UC {id} has no interactions block. Use /use-case (uc-slicer Activity 5) to identify system boundaries and interaction points first.") is correct and should be copied verbatim into the agent definition.

**PRE-02 (Two-layer validation pattern as cross-skill standard):** Step 10 L2 recommended formally documenting the JSON Schema structural gate + agent guardrail semantic gate as `PAT-TWO-LAYER-VALIDATION-001`. This architecture correctly implements this pattern (Section 5). The documentation of this as a formal pattern in `.context/patterns/` remains a post-three-skill-pipeline action. Confirmed: all three skills now implement the two-layer validation pattern. Eng-lead recommends filing this as a worktracker Enabler item to document `PAT-TWO-LAYER-VALIDATION-001` after Step 11 implementation is complete.

**REC-01 (Cross-skill pipeline trust boundary via use-case-realization-v1.schema.json):** The trust boundary established in Step 9 (shared schema as the validation contract) is correctly inherited by /contract-design. cd-generator validates every input UC artifact against the shared schema (Layer 1) before applying the UC-to-contract algorithm. The `$.work_type = USE_CASE` discriminator guards against non-UC artifacts. The `$.realization_level` allOf constraint enforces interactions block presence. Confirmed correctly implemented in architecture Section 5.

**REC-02 (Methodology token count split criterion):** The Step 10 review confirmed the 1,500-token methodology section split criterion. The /contract-design architecture applies this correctly: the cd-generator methodology alone is ~1,400 tokens; adding validation logic would reach ~2,700 tokens, triggering the split. The cd-validator split is justified. No additional action.

**REC-03 (Output location explicitness in SKILL.md routing table):** Step 10 noted that the SKILL.md agent routing table must specify output locations for both agents. The /contract-design architecture Section 2 Agent Routing Table explicitly includes Output Location column for both agents. No gap.

---

## L2: Strategic Implications

### Precedent-Setting Decisions

**1. Three-Skill Pipeline Completion**

The `/contract-design` implementation completes the three-skill pipeline: `/use-case` (Phase 1: UC authoring) -> `/test-spec` + `/contract-design` (Phase 2: parallel consumers of UC output). This is the first complete downstream consumer ecosystem in the Jerry framework. The shared artifact schema (`use-case-realization-v1.schema.json`) has now been validated as a three-way integration contract. Future requirements-to-implementation skills (e.g., a `/architecture-design` or `/data-model` skill) can join the pipeline by declaring which schema fields they consume, without touching existing skills.

**2. PROTOTYPE Labeling as a First-Class Safety Mechanism**

The `x-prototype: true` enforcement in both cd-generator (output filtering rule) and cd-validator (post-completion check) establishes PROTOTYPE labeling as a formal safety pattern in Jerry. This is the first skill to implement a mandatory human-review gate through metadata annotation rather than process gate. The pattern is transferable: any skill producing speculative output (e.g., architecture diagrams, data models from requirements) should carry the same mechanism. Eng-lead recommends documenting `PAT-PROTOTYPE-LABEL-001` alongside `PAT-TWO-LAYER-VALIDATION-001`.

**3. Novel Algorithm Risk Management Pattern (G-01)**

The architecture's handling of G-01 (no prior art for UC-to-contract transformation) establishes a risk management pattern for novel algorithm implementation in Jerry skills:
- Use the highest-capability model (Opus) for generation
- Provide a formal rule file (uc-to-contract-rules.md) encoding the algorithm
- Mandate PROTOTYPE labeling on all outputs until validated against real use cases
- Define explicit downgrade criteria (quality scores consistently > 0.95 after 10+ runs -> evaluate Sonnet)
- Provide a worked example in the architecture (Section 7.1.1) that validates the algorithm's logic before a single line of implementation is written

This G-01 risk pattern should be referenced when any future skill proposes a novel transformation algorithm.

**4. Composition File Synchronization Accumulation**

At the completion of Step 11, the framework will have 6 manually-synchronized composition prompt file pairs. Step 9 and Step 10 identified this as growing technical debt. The eng-devsecops scope action (automated CI parity check between agent .md files and composition prompt.md files) should be treated as a P1 enabler for the next engineering sprint. The synchronization notes are the mitigation; they are not the solution.

### SAMM Maturity Assessment (Relevant Practices)

| Practice | Current Maturity (Post-Steps 9-10) | Target (Post-Step 11 Implementation) |
|----------|--------------------------------------|--------------------------------------|
| Security Requirements (SSDF PO.1) | L1 -- security requirements from STRIDE documented in architectures | L1 maintained -- /contract-design STRIDE analysis (8 threats across 3 trust boundaries) and DREAD scoring are the most comprehensive threat analysis of the three skills. PROTOTYPE labeling addresses TB-3 (external consumer treating PROTOTYPE as production-ready, DREAD 14/25 -- highest scored threat). |
| Secure Design (SSDF PO.3) | L2 -- two-layer validation gate, T2 minimum privilege, schema contract | L2 maintained -- /contract-design inherits the two-layer validation pattern. T2 tier for both agents. Schema contract at input boundary. The creator-critic agent separation (cd-generator writes; cd-validator checks) adds defense in depth beyond Steps 9 and 10. |
| Secure Build (SSDF PS.1) | L1 -- CI L5 schema validation gate | L1 maintained -- same CI gates apply. No new build tooling required. Composition file parity check (FIND-004) adds a low-cost L5 improvement when implemented. |
| Code Integrity (SSDF PS.2) | L1 -- git tracks all artifact changes | L1 maintained -- OpenAPI contracts and validation reports tracked via git. `x-generated-by`/`x-generated-at` metadata fields in contract info section add audit trail. PROTOTYPE label adds a human-review requirement embedded in the artifact itself. |
| Response (SSDF RV.3) | Not previously assessed | L1 emerging -- The first cross-skill trust boundary (TB-3: external consumers) has been formally modeled with DREAD scoring. The PROTOTYPE label is the first user-facing security control in the framework (vs. internal-only controls in Skills 9-10). |

### Technical Debt Assessment

**Risk: Composition File Synchronization (FIND-004)**

At 6 total composition prompt file pairs post-Step 11, the synchronization pattern has reached the threshold where automated enforcement is justified. The manual synchronization notes are sufficient for now but the accumulation rate (2 per skill) makes this a growing maintenance burden. If a fourth pipeline skill is added (e.g., /architecture-design), the framework would have 8 prompt file pairs. Eng-devsecops should implement the CI parity check before the fourth skill is initiated.

**Risk: G-01 Algorithm Quality (R-01 -- High probability, High impact)**

The UC-to-contract algorithm (uc-to-contract-rules.md + cd-generator methodology) is the highest-risk artifact in the three-skill pipeline. The risk is explicitly rated "High probability, High impact" in the architecture risk register. PROTOTYPE labeling prevents downstream damage, but the algorithm must be validated against at least 3 real use cases (the 3-UC criterion from Phase 2) before the PROTOTYPE label can be removed from any generated contract. Eng-lead recommends tracking this as an explicit quality gate: until 3 different use case types (functional, security, integration) have been successfully transformed and validated by cd-validator at >= 0.92, the skill should carry a warning in its SKILL.md that the transformation algorithm is in validation phase.

**Risk: AsyncAPI and CloudEvents Deferred Scope (R-04)**

The 2 deferred templates (F-11, F-12) create a future activation complexity. When G-02 (multi-actor pub/sub mapping) is resolved, the activation path requires: (a) extending cd-generator methodology with event-driven patterns, (b) updating uc-to-contract-rules.md with async rules, (c) activating the templates (remove x-deferred marker), (d) adding BDD scenarios for async contract generation to F-16. This is a medium-effort activation path. The templates as scaffolding correctly document the intended future architecture.

**Long-Term Maintainability**

The 17-file skill structure (vs. 14 files for /test-spec and 17+ for /use-case) is proportional to 2 agents, 4 templates, 1 algorithm rule file, plus samples and contracts. Future capability expansion would follow established patterns:
- AsyncAPI/CloudEvents activation: update F-11/F-12 from scaffolding to active, extend F-14 rule file, update F-16 tests
- GraphQL support: add F-10b graphql-template.json, extend F-14 with RULE-GQL-xx rules
- Schema evolution: handled by `use-case-realization-v1.schema.json` SemVer; agents reference the schema by path and automatically consume updated versions
- cd-generator model downgrade: single field change in F-03 governance YAML (model.tier: sonnet after quality validation)

---

## Self-Review Checklist (H-15 / S-010)

### Constitutional Compliance

- [x] **P-001 (Truth/Accuracy):** Every finding cites the specific standard ID and quotes the relevant specification evidence. Compliance determinations trace to documented fields and architecture sections with line number references where applicable.
- [x] **P-002 (File Persistence):** Review persisted to `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/implementation/step-11-eng-lead-review.md`.
- [x] **P-003 (No Recursive Subagents):** This is a read-and-write review document. No subagent delegation performed.
- [x] **P-022 (No Deception):** Limitations disclosed -- the PENDING registration items are correctly labeled as future tasks, not defects. FIND-002 criticality inconsistency is disclosed with analysis of both positions and a recommended resolution path. File count discrepancy (FIND-001) is disclosed with correct count established as 17 files. Confidence levels appropriate.

### Structural Compliance

- [x] **H-23 (Navigation):** Navigation table present at document top with anchor links to all major sections.
- [x] **H-15 (Self-Review):** This section is the S-010 application.
- [x] **P-002 (Output levels):** L0 (executive summary), L1 (compliance matrix + implementation plan), L2 (strategic implications) all present.

### Standards Coverage Completeness

- [x] H-34 verified -- cd-generator: 15/15 PASS (1 with FIND-002 advisory). cd-validator: 15/15 PASS. Combined 30/30.
- [x] H-25 verified -- 5/5 PASS. No skill naming or structure defects.
- [x] H-26 verified -- 6/9 PASS, 3 PENDING implementation tasks. No architecture defects; registration is correctly deferred to eng-lead Wave 4b.
- [x] H-23 verified -- navigation table in architecture: 4/4 PASS. H-23 requirement briefed for F-01, F-14, F-16 (all will exceed 30 lines).
- [x] H-20 verified -- BDD test-first assessment for F-16: design framework satisfies H-20; 9 scenarios derived from /contract-design acceptance criteria.
- [x] H-22 verified -- trigger map entry at priority 15: all 5 columns present; "API" and "schema" disambiguation explicitly documented in architecture.
- [x] Naming convention verified -- AD-M-001: cd-generator, cd-validator; 6/6 PASS including ORCHESTRATION.yaml reconciliation.
- [x] Tool tier verified -- T2 appropriateness for both agents; Task exclusion; tool count 6/15 threshold; 5/5 PASS.
- [x] AD-M-001 through AD-M-009 and ET-M-001 verified -- 9/10 PASS; 1 PENDING (ET-M-001 for cd-generator, FIND-002).
- [x] Dependency analysis -- 10 dependencies traced; 0 blockers; runtime vs. authoring dependencies distinguished.
- [x] Implementation plan -- 17 files, 5 waves (plus Wave 3b for sample), critical path identified with F-14 and F-17 runtime/demonstration dependency notes.
- [x] File responsibility matrix -- all 17 files mapped to owner, sub-step, reviewer, criticality.
- [x] GATE-4 carryforward -- 4 Step-10 findings assessed; 1 active requirement (FIND-004 synchronization notes), 1 resolved (Section 7 P-003 diagram gap pre-closed), 3 recommendations assessed (REC-01 trust boundary confirmed, REC-02 methodology token split confirmed, REC-03 output location confirmed).
- [x] 7 findings produced with severity levels and actionable recommendations.

### Adversarial Challenge (S-002: Devil's Advocate Applied)

**Challenge 1: "Is the PASS determination for H-34 valid given that governance YAML was not schema-validated at code level?"**

The review verified both governance YAML specifications against `docs/schemas/agent-governance-v1.schema.json` (read and confirmed in this review session). Schema `required` array: `["version", "tool_tier", "identity"]`. All three present in both specs. `guardrails` is not in the top-level required array but both specs declare `guardrails.fallback_behavior: "escalate_to_user"`. `capabilities.forbidden_actions` min 3 entries with P-003/P-020/P-022 references: cd-generator has 6 entries, cd-validator has 4 entries, both satisfying the min-3 constraint. The `additionalProperties: true` on the root governance schema object correctly accommodates the `reasoning_effort` field. The PASS determinations are based on field-by-field comparison against the schema source. Runtime schema validation (L3/L5) will be the authoritative check when actual YAML files are authored.

**Challenge 2: "Is the priority-15 /contract-design trigger map entry correctly analyzed for collisions with adjacent skills?"**

The keyword sets are verified as disjoint after negative filtering. /use-case triggers on "use case", "write use case", "cockburn", "basic flow" -- none of which appear in /contract-design positive keywords. /test-spec triggers on "BDD", "Gherkin", "feature file", "Clark transformation" -- all explicitly listed as negative keywords for /contract-design. The "API" disambiguation (excluding bare "API" as a positive keyword) is particularly important: it prevents /contract-design from over-triggering on any API-related request. The compound triggers ("API contract", "API specification") require domain-specific qualification that is absent from /use-case and /test-spec keywords. The priority-15 analysis is sound.

**Challenge 3: "Is the FIND-002 criticality inconsistency significant enough to be elevated to blocking?"**

FIND-002 is classified as Medium, not blocking. The reasoning: the governance YAML content (`reasoning_effort: max`) is correct and conservative regardless of the C3 vs. C4 label in the file responsibility matrix. The inconsistency affects the review gate applied by eng-security and eng-reviewer (C4 implies more rigorous adversarial review). However, the agent definitions are being reviewed by this review at the eng-lead level regardless. The recommendation to update the file responsibility matrix to C4 is the appropriate resolution -- it is a single-field change that aligns documentation without requiring architecture revision. Elevating to blocking would delay Wave 1 start without additional quality benefit, since the governance YAML content is already at the higher-caution level.

**Challenge 4: "Does the worked example in architecture Section 7.1.1 actually validate the UC-to-contract transformation algorithm?"**

The worked example demonstrates the algorithm on a single interaction (INT-01, POST /loans). It shows how resource identification (Step 2: "creates a loan record" -> `/loans`), HTTP method inference (Step 4: "requests for borrowing" -> POST), and schema derivation (Steps 5-6: preconditions -> CreateLoanRequest, postconditions -> CreateLoanResponse) function. However, it only tests RULE-OM-01 (consumer interaction -> external endpoint) -- it does not demonstrate RULE-OM-02 (provider interaction -> internal operation), which is essential for the system-to-system interaction cases. The worked example is necessary but not sufficient for algorithm validation. The 3-UC validation criterion (from Phase 2 architecture) addresses this gap by requiring multiple diverse use cases. PROTOTYPE labeling prevents premature production use. The assessment stands: the worked example is evidence-based (it traces through all 9 algorithm steps with specific field values) but the algorithm is not validated until the 3-UC criterion is satisfied in production.

---

*Standards Enforcement Review Version: 1.0.0*
*Input: step-11-contract-design-architecture.md v1.1.0 (PASSED 0.956 / threshold 0.95)*
*Standards Verified: H-34 (30/30 across both agents), H-35 (sub-item), H-25 (5/5), H-26 (6 PASS 3 PENDING), H-23 (4/4 PASS for input architecture), H-22 (trigger map 5-column; priority 15; API+schema disambiguation), H-20 (F-16 BDD framework; 9 scenarios derived), ET-M-001 (cd-generator PENDING FIND-002; cd-validator PASS), AD-M-001..AD-M-009, tool tiers T1-T5, P-003 topology, naming convention (cd-), dependency governance (10 traced), SKILL.md 14-section structure (10 PASS 0 GAP 4 PENDING)*
*Findings: 7 total (0 blocking, 3 medium, 4 low)*
*GATE-4 Carryforward: 4 Step-10 findings assessed; 1 active (FIND-004 synchronization notes); 3 recommendations confirmed no further action*
*Implementation Plan: 17 files, 5 waves (+Wave 3b), critical path identified with F-14 runtime dependency note*
*Next Agent: eng-backend (Wave 1 can begin immediately per FIND-002 advisory guidance)*
*Workflow ID: use-case-skills-20260308-001*
*Date: 2026-03-09*
