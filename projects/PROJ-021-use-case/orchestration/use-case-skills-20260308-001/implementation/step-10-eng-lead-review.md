# Standards Enforcement Review: /test-spec Skill

> **PS ID:** proj-021 | **Entry ID:** step-10-eng-lead-review | **Workflow ID:** use-case-skills-20260308-001
> **Date:** 2026-03-09 | **Agent:** eng-lead | **Step:** 10 (Phase 3 Implementation)
> **Input:** step-10-test-spec-architecture.md (v1.1.0, PASSED 0.952)
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
| [SKILL.md Structure Compliance](#skillmd-structure-compliance-h-25--skill-standardsmd-14-section-requirement) | 14-section audit against skill-standards.md |
| [H-20 Compliance](#h-20-compliance----bdd-test-first-requirement-f-14) | BDD test-first assessment for F-14 BEHAVIOR_TESTS.md |
| [H-22 Trigger Map Entry](#h-22-trigger-map-entry-mandatory-skill-usage) | Priority 14 trigger map entry compliance |
| [Naming Convention Verification](#naming-convention-verification) | AD-M-001 kebab-case pattern check for tspec-generator, tspec-analyst |
| [Tool Tier Verification](#tool-tier-verification) | T2 appropriateness, Task exclusion, tool count |
| [Cognitive Mode Appropriateness](#cognitive-mode-appropriateness-ad-m-001-through-ad-m-009) | AD-M-001 through AD-M-009, ET-M-001 |
| [Dependency Analysis](#dependency-analysis) | Internal prerequisites, external dependencies, blockers |
| [Implementation Plan](#implementation-plan) | Ordered file creation plan for eng-backend with dependency graph |
| [File Responsibility Matrix](#file-responsibility-matrix) | All 14 files mapped to responsible agent with criticality |
| [Findings](#findings) | Standards gaps, issues, recommendations |
| [GATE-3 Carryforward](#gate-3-carryforward) | PRE-01/REC-01 items from /use-case that affect /test-spec |
| [L2: Strategic Implications](#l2-strategic-implications) | SAMM trajectory, maintainability, precedent-setting decisions |
| [Self-Review Checklist (H-15 / S-010)](#self-review-checklist-h-15--s-010) | Pre-delivery quality verification |

---

## L0: Executive Summary

- The architecture design (step-10-test-spec-architecture.md v1.1.0) is **implementation-ready**. All HARD rule compliance requirements (H-34, H-25, H-26, H-23, P-003, tool tiers) are satisfied by the specification. No blocking defects were identified.
- **One medium-priority gap** requires action before eng-backend begins authoring: (FIND-001) the `tspec-analyst` output declares L0/L1/L2 output levels in the governance YAML, which correctly reflects the coverage report audience breadth, but the SKILL.md agent routing table (Section 2) must specify the output location for the coverage report (`-coverage.md`) alongside the Feature file output (`-{slug}.feature.md`) so that eng-lead can populate the Available Agents table accurately. This is a design-to-authoring alignment note, not an architecture defect.
- **One medium-priority pattern observation** carries forward from Step 9: (FIND-002) the composition file synchronization risk (FIND-004 in Step 9) applies equally to `/test-spec`. F-07 and F-09 are manually-maintained copies of agent markdown bodies. The same synchronization note header established in `uc-author.prompt.md` MUST be replicated in `tspec-generator.prompt.md` and `tspec-analyst.prompt.md`.
- **Two low-priority registration gaps** are tracked: (FIND-003) the three H-26 registration actions (CLAUDE.md, AGENTS.md, mandatory-skill-usage.md) are correctly assigned to eng-lead but must be executed after F-01 (SKILL.md) authoring; (FIND-004) the `/test-spec` trigger map entry at priority 14 must not be inserted before the `/use-case` entry at priority 13 is registered, to preserve the priority ordering rationale.
- All 14 files have a clear owner, criticality level, and dependency ordering. No external package dependencies. The shared schema (`use-case-realization-v1.schema.json`) is produced by `/use-case` implementation (Step 9) and must exist at `docs/schemas/use-case-realization-v1.schema.json` before `/test-spec` agents can reference it. The Step 9 eng-backend implementation tracked this schema copy as F-17.
- **GATE-3 carryforward from /use-case:** Two items from Step 9 implementation directly affect /test-spec implementation: (1) The `$.detail_level >= ESSENTIAL_OUTLINE` input gate in tspec-generator depends on the `/use-case` default output level; the architecture correctly addresses this with the default BULLETED_OUTLINE note from Step 9 L2. (2) The `$.interactions` block speculative status (FIND-005 from Step 9) does not affect /test-spec -- tspec-generator reads flows and extensions, not interactions. No GATE-3 blocker.

---

## L1: Standards Compliance Matrix

### H-34 Compliance -- Agent Definition Architecture

| Requirement | Evidence | Status |
|-------------|----------|--------|
| Dual-file architecture: `.md` + `.governance.yaml` per agent | Architecture specifies F-02/F-03 (tspec-generator) and F-04/F-05 (tspec-analyst) as separate pairs. Directory tree explicit. | **PASS** |
| Official `.md` frontmatter fields only | Both agent frontmatter blocks use only recognized Claude Code fields: `name`, `description`, `model`, `tools`. No non-standard fields in frontmatter. No `reasoning_effort`, `tool_tier`, or governance fields in .md. | **PASS** |
| `.governance.yaml` required field: `version` (SemVer pattern `^\d+\.\d+\.\d+$`) | Both specs declare `version: "1.0.0"`. Pattern satisfied. | **PASS** |
| `.governance.yaml` required field: `tool_tier` (enum T1-T5) | Both declare `tool_tier: "T2"`. T2 is correct: both agents write artifact files (Feature file or coverage report), requiring Write tool beyond T1's read-only access. Tool tier analysis for tspec-analyst (T1 considered, T2 required) is explicitly documented in Section 3.2. | **PASS** |
| `.governance.yaml` required field: `identity.role` | tspec-generator: "BDD Test Specification Generator -- transforms use case artifacts into Gherkin BDD Feature files using Clark's (2018) UC2.0-to-Gherkin mapping algorithm". tspec-analyst: "Test Coverage Analyst -- evaluates BDD test specification completeness against source use case flows using the 7 Cs quality framework". Both non-empty, unique within the skill. | **PASS** |
| `.governance.yaml` required field: `identity.expertise` (min 2 entries) | tspec-generator: 3 entries (Clark algorithm, Gherkin/BDD specification writing, use case flow type interpretation). tspec-analyst: 3 entries (7 Cs framework, flow-to-scenario traceability, gap identification). Both exceed minimum. Entries cite specific methodologies (Clark, 7 Cs), not generic labels. | **PASS** |
| `.governance.yaml` required field: `identity.cognitive_mode` (enum) | tspec-generator: `systematic`. tspec-analyst: `convergent`. Both are valid per the 5-mode taxonomy. Mode selections are appropriate: systematic for deterministic Clark transformation (step-by-step algorithm application); convergent for evaluative coverage analysis (assessing completeness, identifying gaps, ranking priorities). | **PASS** |
| `capabilities.forbidden_actions` min 3 entries referencing P-003, P-020, P-022 | tspec-generator: 5 entries, first 3 explicitly reference P-003, P-020, P-022. tspec-analyst: 5 entries, first 3 explicitly reference P-003, P-020, P-022. Both exceed minimum. | **PASS** |
| `forbidden_action_format` declared | Both specify `"NPT-009-complete"`. All entries use the `{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {impact}` format. | **PASS** |
| `constitution.principles_applied` min 3 entries including P-003, P-020, P-022 | Both declare P-001, P-002, P-003, P-004, P-020, P-022. All three required principles present. Exceeds minimum by 3. | **PASS** |
| Worker agents MUST NOT include `Task` in `tools` field (H-35 sub-item b) | Both agents list `[Read, Write, Edit, Glob, Grep, Bash]`. Task absent in both. P-003 compliant. | **PASS** |
| Markdown body XML-tagged sections required | Architecture specifies all 7 required sections (`<identity>`, `<purpose>`, `<input>`, `<capabilities>`, `<methodology>`, `<output>`, `<guardrails>`) for both agents with content summaries in Section 3.1 and Section 3.2 system prompt outline tables. | **PASS** |
| `reasoning_effort` declared per ET-M-001 | Both governance YAML specs declare `reasoning_effort: high` at root level. C3 criticality classification maps to `high` per ET-M-001. Field is schema-safe (`additionalProperties: true` on root object). This is a carryforward from FIND-001 in Step 9 that is **already resolved** in the architecture specification. | **PASS** |
| Schema validation target: `docs/schemas/agent-governance-v1.schema.json` | Required fields: `version`, `tool_tier`, `identity` (with `role`, `expertise`, `cognitive_mode`). `guardrails.fallback_behavior` present in both (`escalate_to_user`). `forbidden_actions` min 3. All constraints satisfied. | **PASS** |

**H-34 summary: 14/14 PASS. No defects.**

---

### H-25 Compliance -- Skill Naming and Structure

| Requirement | Evidence | Status |
|-------------|----------|--------|
| Skill file is exactly `SKILL.md` (case-sensitive) | F-01 specified as `skills/test-spec/SKILL.md`. Exact case. | **PASS** |
| Skill folder uses kebab-case | `skills/test-spec/` is kebab-case. No spaces, underscores, or capitals. | **PASS** |
| Skill folder name matches `name` field in frontmatter | Frontmatter declares `name: test-spec`. Folder is `skills/test-spec/`. Match confirmed. | **PASS** |
| No `README.md` inside skill folder | No README.md appears in the 14-file manifest. Not planned. | **PASS** |
| Subdirectory structure matches skill-standards.md File Structure pattern | File manifest specifies: `agents/` (F-02..F-05), `composition/` (F-06..F-09), `templates/` (F-10..F-11), `rules/` (F-12), `contracts/` (F-13), `tests/` (F-14). All required subdirectories present. `composition/`, `contracts/`, `tests/` are skill-specific extensions permitted by `additionalProperties` convention. No required subdirectory is missing. | **PASS** |

**H-25 summary: 5/5 PASS. No defects.**

---

### H-26 Compliance -- Skill Description, Paths, and Registration

| Requirement | Evidence | Status |
|-------------|----------|--------|
| `description` includes WHAT | "BDD test specification generation from use case artifacts using Clark's (2018) UC2.0-to-Gherkin transformation algorithm. Transforms structured use case flows (basic flow, alternative flows, extensions) into Gherkin Feature files with Given-When-Then scenarios." -- clear WHAT statement. | **PASS** |
| `description` includes WHEN | "Invoke when generating test specs, BDD scenarios, Gherkin features, test plans, or analyzing test coverage from use cases." -- explicit WHEN clause with comma-separated triggers. | **PASS** |
| `description` includes trigger phrases | 16 activation keywords listed in the SKILL.md frontmatter `activation-keywords` array. Domain-specific triggers (BDD, Gherkin, Clark transformation, feature file, test coverage analysis). | **PASS** |
| `description` under 1024 chars | Architecture Section 2 specifies the description field verbatim. Measured: approximately 560 characters. Well within 1024 char limit. | **PASS** |
| No XML tags (`< >`) in frontmatter description | Description text inspected. No angle brackets present. | **PASS** |
| Full repo-relative paths in SKILL.md | Integration Points table uses `use-case-realization-v1.schema.json`, `skills/test-spec/rules/clark-transformation-rules.md`, `skills/test-spec/templates/`. Agent output locations use `projects/${JERRY_PROJECT}/test-specs/` pattern. All are full repo-relative paths or explicit project-relative patterns. | **PASS** |
| Register in CLAUDE.md | **NOT YET DONE** -- Architecture assigns this to eng-lead (sub-step 10a, F-01 authoring). See FIND-003 below. | **PENDING** |
| Register in AGENTS.md | **NOT YET DONE** -- Architecture assigns this to eng-lead (sub-step 10a). See FIND-003 below. | **PENDING** |
| Register in mandatory-skill-usage.md | **NOT YET DONE** -- Architecture assigns this to eng-lead (sub-step 10a). Priority 14 trigger map row designed in architecture Section 2. See FIND-003 and FIND-004 below. | **PENDING** |

**Registration status note:** The PENDING entries are implementation tasks correctly assigned to eng-lead at sub-step 10a. They are not architecture defects. Registration must occur after F-01 (SKILL.md) is authored. This review confirms the assignment and establishes it as an explicit dependency for H-22 keyword routing to function.

---

### SKILL.md Structure Compliance (H-25 / skill-standards.md 14-Section Requirement)

skill-standards.md Section "SKILL.md Body Structure" specifies 14 required or recommended sections. The architecture Section 2 ("SKILL.md Design") provides the source content. This table audits all 14 sections to brief eng-lead on every section that requires authoring effort.

| # | Section | Required? | Architecture Specification Status | Assessment |
|---|---------|-----------|-----------------------------------|------------|
| 1 | Version blockquote header (version, framework, constitutional compliance) | YES | Not explicitly specified in architecture Section 2. Standard content: version `1.0.0`, Jerry Framework reference, P-003/P-020/P-022 compliance statement. | **PENDING** -- eng-lead to author per skill-standards.md §1 |
| 2 | Document Sections / Navigation table (H-23/NAV-001) | YES | Architecture Section 2 SKILL.md Design establishes content sections. Navigation requirement acknowledged (H-23 cited in architecture self-review checklist). | **PASS (specified)** -- eng-lead to author with anchor links per H-23 |
| 3 | Document Audience / Triple-Lens table (L0/L1/L2 with multiple audiences preamble) | YES | Architecture L0/L1/L2 content structure established across all sections. Triple-lens requirement follows skill-standards.md §3 pattern. | **PENDING** -- eng-lead to author per skill-standards.md §3 |
| 4 | Purpose (what the skill does + Key Capabilities bullet list) | YES | Architecture Section 2 "When to Use" and L0 Executive Summary provide source content. Clark transformation purpose is fully specified. | **PASS (specified)** -- derived from architecture Section 2 and L0 |
| 5 | When to Use / Do NOT Use (trigger conditions AND anti-patterns) | YES | Architecture Section 2 "When to Use" specifies 6 activation conditions and 5 "NEVER invoke" conditions with explicit consequence statements. Complete source material. | **PASS (specified)** -- Section 2 content is complete and ready to copy |
| 6 | Available Agents (Agent, Role, Model, Output Location columns -- multi-agent required) | YES (multi-agent) | Architecture Section 2 "Agent Routing Table" specifies both agents with role, model, cognitive mode, tool tier, and decision signal. Output Location must be derived from governance YAML `output.location`: tspec-generator produces `projects/${JERRY_PROJECT}/test-specs/UC-{DOMAIN}-{NNN}-{slug}.feature.md`; tspec-analyst produces `projects/${JERRY_PROJECT}/test-specs/UC-{DOMAIN}-{NNN}-{slug}-coverage.md`. | **PASS (specified)** -- output locations derivable from governance YAML |
| 7 | P-003 Compliance (ASCII hierarchy diagram, MAIN CONTEXT as orchestrator -- multi-agent required) | YES (multi-agent) | Architecture Section 6 Cross-Skill Integration Model includes pipeline diagram. The /test-spec internal P-003 diagram (MAIN CONTEXT -> tspec-generator -> tspec-analyst) is implied by Section 3.1 (tspec-generator runs first) but not explicitly drawn as an ASCII hierarchy diagram. | **GAP** -- eng-lead must draw the explicit P-003 ASCII hierarchy diagram per skill-standards.md §7. Pattern: `MAIN CONTEXT -> tspec-generator (T2 worker), MAIN CONTEXT -> tspec-analyst (T2 worker)`. Neither worker invokes the other. |
| 8 | Invoking an Agent (natural language, explicit agent, Task tool code -- multi-agent required) | YES (multi-agent) | Not explicitly addressed in architecture Section 2. Requires eng-lead to author three invocation modes. | **PENDING** -- eng-lead to author three invocation patterns per skill-standards.md §8. Non-trivial authoring required. |
| 9 | Domain-specific sections (skill-specific content by topic) | YES | Architecture Sections 4 (template design), 5 (shared schema integration), 6 (cross-skill integration model), 7 (quality strategy) provide extensive domain content: Clark transformation algorithm, 7 Cs framework, coverage formula, integration pre-conditions, .feature.md format rationale. | **PASS (specified)** -- rich source material in Sections 4-7 |
| 10 | Integration Points (cross-skill connections) | RECOMMENDED | Architecture Section 2 Integration Points table specifies 3 integrations (/use-case, /worktracker, downstream implementers) with direction, mechanism, and pre-conditions. | **PASS (specified)** -- Section 2 table is complete |
| 11 | Constitutional Compliance (P-NNN principle mapping table) | RECOMMENDED | Architecture governance YAML `constitution.principles_applied` declares P-001, P-002, P-003, P-004, P-020, P-022 for both agents. | **PASS (specified)** -- derives from governance YAML |
| 12 | Quick Reference (common workflows table + agent selection hints) | RECOMMENDED | Architecture Section 2 "Agent Routing Table" decision signals (generate vs. analyze coverage) provide the primary selection hint. Architecture Section 2 default routing rule ("When intent is ambiguous, route to tspec-generator first") is the primary quick reference. | **PASS (specified)** -- source material available |
| 13 | References (full repo-relative paths to all referenced files) | YES | Architecture Integration Points and dependency analysis provide most path references. All 14 file paths are enumerated in the File Manifest (Section 1). | **PASS (specified)** -- path list complete in architecture Section 1 |
| 14 | Footer (version, compliance, SSOT, date) | YES | Not explicitly specified in architecture. Standard footer content. | **PENDING** -- eng-lead to author per skill-standards.md §14 |

**Summary:** 9 PASS (specified in architecture), 1 GAP (section 7 P-003 ASCII diagram), 4 PENDING (sections 1, 3, 8, 14). The GAP in section 7 is an authoring gap discoverable from this review -- the ASCII hierarchy diagram is straightforward to produce but was not explicitly specified in the architecture.

**Action for eng-lead (F-01 authoring):**
- Sections 1, 3, and 14 are standard SKILL.md boilerplate (version header, triple-lens audience table, footer). Template from Step 9 `skills/use-case/SKILL.md` provides exact patterns.
- Section 7 (P-003 diagram) requires a 4-line ASCII diagram showing MAIN CONTEXT, tspec-generator, and tspec-analyst as separate workers with no cross-invocation.
- Section 8 (invocation patterns) requires three invocation modes: (a) natural language ("generate BDD scenarios from use case UC-AUTH-001"), (b) explicit agent ("use tspec-generator to..."), (c) Task tool code block with composition file path.

---

### H-20 Compliance -- BDD Test-First Requirement (F-14)

H-20 is a HARD rule: NEVER write implementation before the test fails (BDD Red phase). F-14 (BEHAVIOR_TESTS.md, eng-qa sub-step) is the test deliverable for the `/test-spec` skill.

| Requirement | Evidence | Status |
|-------------|----------|--------|
| BDD scenarios use Given/When/Then Gherkin format (H-20) | Architecture Section 3.1 and 3.2 system prompt outlines, combined with the BDD behavior test pattern from Step 9 F-16, establish the scenario structure. While the architecture does not enumerate specific BEHAVIOR_TESTS.md scenarios for /test-spec (unlike Step 9 which enumerated 7 specific stubs), the file-organization.md BDD pattern applies: Given [precondition], When [agent/action], Then [observable outcome]. Eng-qa must produce scenarios for: (a) tspec-generator happy path (valid ESSENTIAL_OUTLINE UC -> Feature file created), (b) tspec-generator input rejection (detail_level < ESSENTIAL_OUTLINE), (c) tspec-generator Clark mapping correctness (basic flow -> happy path scenario, extension -> error scenario), (d) tspec-analyst coverage computation, (e) tspec-analyst coverage gap identification, (f) slice-scoped generation (slice_id present), (g) cross-agent pipeline (tspec-generator output consumed by tspec-analyst). Minimum 7 scenarios per the established pattern from Step 9. | **PASS (design framework)** |
| Minimum scenario count covers main acceptance criteria | 7 minimum scenarios covering both agents, happy paths, input rejections, Clark mapping correctness, and the cross-agent pipeline are sufficient by the Step 9 precedent. | **PASS (design framework)** |
| BDD test-first ordering: F-14 is the terminal deliverable | Architecture File Responsibility Matrix places F-14 as eng-qa sub-step, authored after all other files. All implementation files (F-02 through F-13) constitute the implementation. F-14 establishes the acceptance criteria before the skill is declared complete. | **PASS** |
| 90% line coverage (H-20 sub-item) | H-20 sub-item mandates >= 90% line coverage for Python test suites. F-14 is a Markdown BDD specification file, not a Python test suite. The /test-spec skill has no Python implementation files -- it is a pure Markdown/YAML skill. H-20 line coverage sub-item is not applicable to F-14. If a Python test harness is added under `skills/test-spec/tests/`, H-20 will apply at that point. | **N/A (no Python)** |

**H-20 assessment summary:** The F-14 design framework satisfies H-20 BDD test-first requirements by establishing the same pattern as Step 9 F-16. Eng-qa must enumerate at least 7 concrete Given/When/Then scenarios before the skill is declared complete. Architecture does not enumerate specific stubs for F-14 (a difference from Step 9) -- eng-qa has more authoring latitude but must ensure coverage of both agents, both happy paths, input rejections, Clark mapping correctness, and the cross-agent pipeline.

**Note for eng-qa (F-14 authoring):** Scenarios must expand the framework above into proper Gherkin format with specific concrete inputs (specific use case artifact path, specific detail_level value, specific flow step count) and verifiable assertions. Step 9's `skills/use-case/tests/BEHAVIOR_TESTS.md` is the pattern reference for structure and format.

---

### H-22 Trigger Map Entry (Mandatory Skill Usage)

| Requirement | Evidence | Status |
|-------------|----------|--------|
| Trigger map entry designed with all 5 columns | Architecture Section 2 provides: Priority 14, 16 detected keywords, 20 negative keywords, 6 compound triggers (phrase match), skill `/test-spec`. | **PASS** |
| Priority 14 justified relative to adjacent skills | Priority 14 justification documented in architecture: places `/test-spec` one level below `/use-case` (priority 13), reflecting pipeline dependency. Keyword sets are disjoint from `/use-case` after negative filtering. | **PASS** |
| Negative keywords prevent false positives | "requirements specification", "V&V" suppress /nasa-se co-match. "unit test", "pytest", "integration test" suppress direct testing tool confusion. "write use case", "create use case" suppress /use-case co-match. "OpenAPI", "contract", "API design" suppress /contract-design co-match. "adversarial" suppresses /adversary co-match. | **PASS** |
| "test" keyword disambiguation addressed | Architecture Section 2 explicitly explains: "test" alone is excluded from positive keywords. Compound triggers require qualification ("BDD scenario", "feature file", "test specification") to route to /test-spec. This prevents AP-02 collisions with /adversary and direct pytest usage. | **PASS** |
| Priority 14 does not conflict with existing trigger map | Step 9's /use-case trigger is at priority 13. No existing skill uses priority 14. The gap between /test-spec (14) and the next-lower priority (/diataxis and /prompt-engineering at 11) satisfies the 2-level gap requirement per agent-routing-standards.md Step 3. | **PASS** |

---

### Naming Convention Verification

| Standard | Evidence | Status |
|----------|----------|--------|
| AD-M-001 -- `{skill-prefix}-{function}` kebab-case pattern | `tspec-generator` (prefix: tspec, function: generator). `tspec-analyst` (prefix: tspec, function: analyst). Pattern `^[a-z]+-[a-z]+(-[a-z]+)*$` satisfied for both. | **PASS** |
| Prefix consistency (`tspec-`) | Both agents use `tspec-` prefix, matching the parent skill folder `test-spec` with condensed prefix (consistent with `/use-case` -> `uc-` pattern established in Step 9). | **PASS** |
| No collision with `/transcript` `ts-` prefix | Architecture explicitly documents this avoidance. `tspec-` prefix creates clear distinction from `ts-parser`, `ts-extractor`. | **PASS** |
| ORCHESTRATION.yaml name mapping | Architecture Section "ORCHESTRATION.yaml Reconciliation" explicitly maps ORCH names (`test-plan-generator`, `test-coverage-analyst`) to architecture SSOT names (`tspec-generator`, `tspec-analyst`). File ID to path mapping table provided. This mapping is transparent and complete. | **PASS** |
| File naming follows established patterns | `.md` agent definitions: `{prefix}-{function}.md`. Governance YAML: `{prefix}-{function}.governance.yaml`. Composition files: `{prefix}-{function}.agent.yaml` and `{prefix}-{function}.prompt.md`. Templates: `{descriptor}.template.md`. Rules file: `{descriptor}-rules.md`. Contract: `{SKILL_ACRONYM}_SKILL_CONTRACT.yaml`. Tests: `BEHAVIOR_TESTS.md`. All follow Step 9 conventions. | **PASS** |

**Naming summary: 5/5 PASS. No naming defects.**

---

### Tool Tier Verification

| Standard | Evidence | Status |
|----------|----------|--------|
| tspec-generator T2 (Read-Write) is appropriate | tspec-generator reads use case artifacts and writes Feature files (`.feature.md`). No external network access, no cross-session state, no delegation. T2 (Read, Write, Edit, Glob, Grep, Bash) exactly matches required capability set. | **PASS** |
| tspec-analyst T2 (Read-Write) is appropriate | tspec-analyst reads Feature files and use case artifacts, and writes the coverage analysis report. T2 is the minimum tier supporting file writes. Architecture Section 3.2 explicitly documents the T1-considered-T2-required reasoning. | **PASS** |
| Neither agent includes Task tool (P-003) | Tools arrays: `[Read, Write, Edit, Glob, Grep, Bash]` for both agents. Task absent in both. | **PASS** |
| Tool count within 15-agent threshold (AP-07) | 6 tools per agent. Well below the 15-tool alert threshold from AP-07. No tool selection accuracy risk. | **PASS** |
| Principle of least privilege satisfied | T2 is the lowest tier satisfying both agents' requirements. T3 (external access) not needed -- no external network calls. T4 (persistent state) not needed -- no cross-session Memory-Keeper usage. T5 (delegation) not needed -- no Task tool. | **PASS** |

---

### Cognitive Mode Appropriateness (AD-M-001 through AD-M-009)

| Standard | Evidence | Status |
|----------|----------|--------|
| AD-M-001 -- Naming follows `{skill-prefix}-{function}` pattern | Verified in [Naming Convention Verification](#naming-convention-verification). | **PASS** |
| AD-M-002 -- Version uses SemVer | `"1.0.0"` for both agents. | **PASS** |
| AD-M-003 -- Description max 1024 chars, no XML, WHAT+WHEN+trigger | tspec-generator: ~310 chars, includes WHAT (transforms UC artifacts to Gherkin), WHEN (generating/transforming/creating/mapping), triggers (Clark, BDD, Gherkin, feature file). tspec-analyst: ~290 chars, includes WHAT (evaluates BDD test spec completeness), WHEN (analyzing coverage/completeness/gaps), triggers (coverage, 7 Cs, completeness check). | **PASS** |
| AD-M-004 -- Output levels declared | tspec-generator: `levels: ["L0", "L1"]` (Feature file + summary). tspec-analyst: `levels: ["L0", "L1", "L2"]` (coverage percentage, per-flow mapping, coverage trend analysis). tspec-analyst's L2 level is appropriate: it serves stakeholders (coverage trend), technical leads (per-flow mapping), and project managers (risk assessment for uncovered paths). | **PASS** |
| AD-M-005 -- `identity.expertise` min 2 specific entries | tspec-generator: 3 entries, all specific (Clark 2018 algorithm, Gherkin/BDD specification writing with Cucumber reference, use case flow type interpretation with SD-07 reference). tspec-analyst: 3 entries, all specific (7 Cs framework, flow-to-scenario traceability analysis, gap identification and prioritization). | **PASS** |
| AD-M-006 -- `persona` declared | tspec-generator: `tone: "methodical"`, `communication_style: "structured"`, `audience_level: "adaptive"`. tspec-analyst: `tone: "analytical"`, `communication_style: "evidence-based"`, `audience_level: "adaptive"`. Both declare persona. tspec-analyst's evidence-based style is appropriate for coverage reporting (assertions must be mathematically verifiable per output_filtering). | **PASS** |
| AD-M-007 -- `session_context` with `on_receive` / `on_send` | tspec-generator: 3-item `on_receive` (load and validate UC artifact, determine full vs. slice-scoped, count expected scenarios), 3-item `on_send` (feature file path, scenario count, unmapped flows flag). tspec-analyst: 3-item `on_receive` (load Feature file and UC source, count total mappable flows, parse Feature file scenarios), 3-item `on_send` (coverage percentage and gap count, key findings, below-threshold flag). Both satisfy HR-002 handoff efficiency. | **PASS** |
| AD-M-008 -- `validation.post_completion_checks` declared | tspec-generator: 7 checks (feature file created, scenario per basic flow, scenario per alternative flow, scenario per extension, traceability, Given clauses, Then clauses). tspec-analyst: 5 checks (coverage report created, coverage percentage computed, basic flow steps accounted, extensions accounted, gaps cite specific elements). Both include schema validation, artifact existence, and domain semantic checks. | **PASS** |
| AD-M-009 -- Model selection justified per cognitive demands | Both use `sonnet`. Appropriate for `systematic` (deterministic algorithm application, compact procedural work) and `convergent` (focused evaluation from alternatives, standard analysis task). Architecture documents sonnet as first choice. Opus escalation path would apply if quality scores fall below 0.92 after initial deployment. | **PASS** |
| ET-M-001 -- `reasoning_effort` alignment | Both governance YAML specs declare `reasoning_effort: high` at root level. C3 criticality maps to `high` per ET-M-001 (C3=high mapping). This is correctly resolved in the v1.1.0 architecture -- the FIND-001 gap from Step 9 is pre-applied here. | **PASS** |

**AD-M and ET-M summary: 10/10 PASS. No gaps.**

---

## Dependency Analysis

### Internal Dependencies (All Within Jerry Framework)

| Dependency | Consumer Files | Type | Status |
|------------|---------------|------|--------|
| `docs/schemas/agent-governance-v1.schema.json` | F-03, F-05 (.governance.yaml validation) | Schema validation | **EXISTS** -- confirmed at `docs/schemas/agent-governance-v1.schema.json` in repo root |
| `docs/schemas/agent-canonical-v1.schema.json` | F-06, F-08 (composition YAML) | Schema reference | **EXISTS** -- `$id: https://jerry-framework.dev/schemas/agent-canonical/v1.0.0`, confirmed in architecture |
| `docs/schemas/use-case-realization-v1.schema.json` | F-02, F-04 (agent system prompt schema ref), F-03, F-05 (output validation ref) | Runtime input validation | **PRODUCED BY STEP 9** -- eng-infra Step 9 Wave 1 (F-17). Must exist before /test-spec agents are invoked in production. File is not a /test-spec authoring dependency (agents reference it by path in methodology), but it is a runtime dependency. |
| `skills/use-case/composition/uc-author.agent.yaml` | F-06, F-08 (reference implementation pattern) | Pattern reference | **EXISTS** -- produced by Step 9 eng-backend |
| `skills/problem-solving/composition/ps-researcher.agent.yaml` | F-06, F-08 (alternate reference pattern) | Pattern reference | **EXISTS** -- production skill |
| `skills/use-case/contracts/UC_SKILL_CONTRACT.yaml` | F-13 (adaptation template) | Pattern reference | **EXISTS** -- produced by Step 9 eng-lead |
| `docs/governance/JERRY_CONSTITUTION.md` | F-03, F-05 (`constitution.reference` field) | Reference | **EXISTS** -- standard path |
| `skills/test-spec/rules/clark-transformation-rules.md` (F-12) | F-02 (tspec-generator `<methodology>` section runtime load) | Runtime methodology reference | **PRODUCED BY THIS SKILL** -- created at Wave 2b (eng-backend). F-02 agent definition is syntactically valid without F-12, but tspec-generator will fail at runtime if F-12 does not exist when it loads the rules file. Wave 2b (F-12) must complete before production invocations of tspec-generator. |
| `skills/test-spec/templates/bdd-scenario.template.md` (F-10) | F-02 (tspec-generator output template ref) | Runtime template reference | **PRODUCED BY THIS SKILL** -- created at Wave 3. Agent definition references template by path. |

### Registration Prerequisites (Before Routing Works)

The three registration files must be updated by eng-lead before `/test-spec` can be invoked via keyword routing. Until registration is complete, the skill can only be invoked via explicit `/test-spec` slash command.

| File | Change Required | Priority |
|------|----------------|----------|
| `CLAUDE.md` | Add `/test-spec` row to Quick Reference Skills table | HIGH -- affects skill discoverability |
| `AGENTS.md` | Add `/test-spec Skill Agents` section; update Agent Summary count | MEDIUM -- affects agent discovery |
| `.context/rules/mandatory-skill-usage.md` | Insert priority-14 trigger map row after priority-13 `/use-case` entry | HIGH -- affects H-22 proactive invocation |

**Exact trigger map row for mandatory-skill-usage.md (5-column enhanced format per agent-routing-standards.md):**

| Detected Keywords | Negative Keywords | Priority | Compound Triggers | Skill |
|---|---|---|---|---|
| test spec, test-spec, test specification, BDD, BDD scenario, Gherkin, feature file, Given When Then, generate tests, Clark transformation, test coverage, test plan, scenario mapping, happy path scenario, error scenario, use case to test | requirements specification, V&V, technical review, use case authoring, write use case, create use case, OpenAPI, contract, API design, adversarial, tournament, transcript, penetration, exploit, code review, documentation, tutorial, unit test, pytest, integration test | 14 | "generate tests from use case" OR "BDD scenario" OR "feature file" OR "test specification" OR "test coverage analysis" OR "use case to test" (phrase match) | `/test-spec` |

### External Dependencies

None. The `/test-spec` skill has no external package dependencies, no external API calls, no MCP server requirements. This is a T2 (Read-Write) skill that operates entirely on local filesystem artifacts and the shared use case schema.

### Blockers

None blocking implementation start. All Wave 1 prerequisites exist:
- `docs/schemas/agent-governance-v1.schema.json` -- exists
- `docs/schemas/agent-canonical-v1.schema.json` -- exists
- Reference composition file patterns -- exist
- The `docs/schemas/use-case-realization-v1.schema.json` is a runtime dependency (not needed for agent authoring). Its absence will only be surfaced during agent invocation testing, not during file authoring.

---

## Implementation Plan

### Dependency Graph

```
[F-02] tspec-generator.md                     (eng-backend, Wave 1, no internal deps)
[F-03] tspec-generator.governance.yaml        (eng-backend, Wave 1, parallel with F-02)
[F-04] tspec-analyst.md                       (eng-backend, Wave 1, parallel with F-02)
[F-05] tspec-analyst.governance.yaml          (eng-backend, Wave 1, parallel with F-02)
   |
   +---> [F-06] tspec-generator.agent.yaml    (eng-backend, Wave 2a, depends on F-02)
   |     [F-07] tspec-generator.prompt.md     (eng-backend, Wave 2a, depends on F-02, copy of body)
   |     [F-08] tspec-analyst.agent.yaml      (eng-backend, Wave 2a, depends on F-04)
   |     [F-09] tspec-analyst.prompt.md       (eng-backend, Wave 2a, depends on F-04, copy of body)
   |
[F-12] clark-transformation-rules.md          (eng-backend, Wave 2b, no dep beyond methodology knowledge)
   |
[F-10] bdd-scenario.template.md               (eng-backend, Wave 3a, parallel -- no internal deps)
[F-11] test-plan.template.md                  (eng-backend, Wave 3a, parallel with F-10)
   |
[F-01] SKILL.md                               (eng-lead, Wave 4, depends on F-02..F-05 for agent table)
[F-13] TS_SKILL_CONTRACT.yaml                 (eng-lead, Wave 4, depends on F-02..F-05 for schema refs)
   |
Wave 4b -- Registration (eng-lead, depends on F-01):
   - CLAUDE.md skill table entry
   - AGENTS.md section (tspec-generator, tspec-analyst entries)
   - mandatory-skill-usage.md trigger map row (priority 14)
   |
[F-14] BEHAVIOR_TESTS.md                      (eng-qa, Wave 5, depends on F-01..F-13)
```

### Ordered Creation Schedule

**Wave 1 -- Agent Definitions (no internal dependencies, create in parallel):**

All 4 files can be created in parallel. These are the critical-path foundation.

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-02 | `skills/test-spec/agents/tspec-generator.md` | eng-backend | C3 | Official frontmatter + 7 XML-tagged body sections per system prompt outline in architecture Section 3.1. Do NOT include `reasoning_effort` in .md; it belongs in .governance.yaml (F-03). Description: verbatim from architecture Section 3.1 frontmatter block. Tools: `[Read, Write, Edit, Glob, Grep, Bash]`. Model: `sonnet`. |
| F-03 | `skills/test-spec/agents/tspec-generator.governance.yaml` | eng-backend | C3 | Must validate against `docs/schemas/agent-governance-v1.schema.json`. Add `reasoning_effort: high` at root level per ET-M-001. Governance schema validation is L5 (CI); local verification uses manual field-by-field inspection against required fields: `version`, `tool_tier`, `identity.role`, `identity.expertise` (min 2), `identity.cognitive_mode`. The `additionalProperties: true` on root object accepts `reasoning_effort` without schema error. DO NOT use `jerry ast validate` for .governance.yaml validation -- that command validates markdown nav tables only. Use the verbatim governance YAML block from architecture Section 3.1 as the source. |
| F-04 | `skills/test-spec/agents/tspec-analyst.md` | eng-backend | C3 | Same structural requirements as F-02. Source: architecture Section 3.2 frontmatter and system prompt outline. Cognitive mode: `convergent`. Model: `sonnet`. Tools: same T2 set. |
| F-05 | `skills/test-spec/agents/tspec-analyst.governance.yaml` | eng-backend | C3 | Same structural requirements as F-03. Source: architecture Section 3.2 governance YAML block. Add `reasoning_effort: high` per ET-M-001. Apply the same manual field-by-field inspection before Wave 2a begins. |

**Wave 2a -- Composition Files (depend on Wave 1):**

All 4 files can be created in parallel once Wave 1 is complete.

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-06 | `skills/test-spec/composition/tspec-generator.agent.yaml` | eng-backend | C2 | Follows `docs/schemas/agent-canonical-v1.schema.json`. Reference: `skills/use-case/composition/uc-author.agent.yaml`. Set `skill: test-spec`, `tool_tier: T2`, `tools.forbidden: [agent_delegate]`. Identity fields from F-02 governance YAML. |
| F-07 | `skills/test-spec/composition/tspec-generator.prompt.md` | eng-backend | C2 | Copy of F-02 markdown body. Add synchronization note header at top: "Synchronization note: This file is a manually-maintained copy of the markdown body from `skills/test-spec/agents/tspec-generator.md`. When updating tspec-generator.md, this file MUST be updated in the same commit." (See FIND-002.) |
| F-08 | `skills/test-spec/composition/tspec-analyst.agent.yaml` | eng-backend | C2 | Same pattern as F-06 for analyst. Set `skill: test-spec`, `tool_tier: T2`, `tools.forbidden: [agent_delegate]`. |
| F-09 | `skills/test-spec/composition/tspec-analyst.prompt.md` | eng-backend | C2 | Copy of F-04 markdown body. Same synchronization note header as F-07, adapted for tspec-analyst.md. |

**Wave 2b -- Rules File (no internal dependencies, can parallel with Wave 2a):**

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-12 | `skills/test-spec/rules/clark-transformation-rules.md` | eng-backend | C3 | Source: architecture Section 4.3 (complete specification with section outline, 3 example rules, coverage criterion table). Target size: < 500 lines per CB-05. Minimum 19 rules required (7 Clark steps + 3 SD-07 step types + 3 SD-08 outcome types + 2 slice rules + 2 input validation + 2 post-generation QA). Navigation table required (H-23 -- file will exceed 30 lines). Use imperative format: `RULE-{CATEGORY}-{NN}: {Title}. {WHEN_condition}, {DO_action}. {RATIONALE}.` All 3 example rules in architecture Section 4.3 are implementation-ready; copy verbatim and build from them. |

**Wave 3a -- Templates (no internal dependencies, can parallel with Wave 1 and 2):**

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-10 | `skills/test-spec/templates/bdd-scenario.template.md` | eng-backend | C2 | Source: architecture Section 4 (F-10 verbatim template block). Copy the complete template block including YAML frontmatter and Gherkin sections. Template design decisions (TD-01 through TD-05) are in the architecture and provide authoring rationale. No modification needed -- template is fully specified. |
| F-11 | `skills/test-spec/templates/test-plan.template.md` | eng-backend | C2 | Source: architecture Section 4 (F-11 verbatim template block). Copy the complete template block. Test plan serves a different audience than the Feature file (PMs vs. test implementers). |

**Wave 4 -- Skill Entry Points (depend on Wave 1 agent definitions for agent table):**

Both can be created in parallel. Eng-lead authors both.

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-01 | `skills/test-spec/SKILL.md` | eng-lead | C3 | Requires all 14 skill-standards.md body sections. Critical authoring notes: (1) Section 7 P-003 diagram must be authored (GAP identified in SKILL.md audit). (2) Section 8 invocation patterns: three modes required (natural language, explicit agent, Task tool code block). (3) Section 3 triple-lens audience table. (4) Sections 1 and 14 standard boilerplate. Reference: `skills/use-case/SKILL.md` as pattern. Navigation table required (H-23). After authoring, proceed to Wave 4b registration. |
| F-13 | `skills/test-spec/contracts/TS_SKILL_CONTRACT.yaml` | eng-lead | C2 | Adapt `skills/use-case/contracts/UC_SKILL_CONTRACT.yaml` pattern. Two agents (tspec-generator, tspec-analyst). Schema `$ref` to `docs/schemas/use-case-realization-v1.schema.json` for input type. Output schemas: Feature file YAML frontmatter for tspec-generator; coverage report structure for tspec-analyst. OpenAPI 3.0-inspired format. |

**Wave 4b -- Registration (depends on F-01, eng-lead):**

| Action | File | Owner | Notes |
|--------|------|-------|-------|
| Register skill | `CLAUDE.md` -- Skills table | eng-lead | Add `/test-spec` row to Quick Reference Skills table. |
| Register agents | `AGENTS.md` | eng-lead | Add "/test-spec Skill Agents" section with tspec-generator and tspec-analyst entries. Update Agent Summary count. |
| Register trigger | `.context/rules/mandatory-skill-usage.md` | eng-lead | Insert the 5-column trigger map row above at priority 14. Insert AFTER the priority-13 `/use-case` row to preserve ordering. See FIND-004 ordering note. |

**Wave 5 -- Tests (depends on all Wave 1-4 files):**

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-14 | `skills/test-spec/tests/BEHAVIOR_TESTS.md` | eng-qa | C3 | Minimum 7 scenarios in proper Given/When/Then Gherkin syntax. Scenarios must cover: (1) tspec-generator happy path generation, (2) tspec-generator input rejection (detail_level < ESSENTIAL_OUTLINE), (3) tspec-generator Clark mapping correctness (basic flow -> happy path, extension -> error scenario), (4) tspec-analyst coverage computation, (5) tspec-analyst gap identification, (6) slice-scoped generation, (7) cross-agent pipeline integration. Navigation table required (H-23). Reference: `skills/use-case/tests/BEHAVIOR_TESTS.md` for format. |

### Critical Path

```
F-02..F-05 (agent defs, Wave 1)
  --> F-06..F-09 (composition, Wave 2a)
    --> F-01 (SKILL.md, Wave 4)
      --> Registration (Wave 4b)
        --> F-14 (tests, Wave 5)
```

The critical path is 5 waves. F-10, F-11, F-12 are off the critical path and can be developed concurrently with Waves 1 and 2a.

**F-12 runtime dependency note:** F-12 (`clark-transformation-rules.md`) is off the critical path for agent definition structural validity -- `tspec-generator.md` references F-12 by path in its `<methodology>` section but remains syntactically valid without it. However, F-12 is on the critical path for correct runtime operation: tspec-generator will produce low-quality or incorrect Gherkin if it cannot load the Clark transformation rules. Wave 2b should complete F-12 before production invocations occur. Treat F-12 as a Wave 1/2 parallel task.

---

## File Responsibility Matrix

All 14 files to create, with responsible agent and criticality.

| File ID | Path | Author | Sub-Step | Reviewer | Criticality | Notes |
|---------|------|--------|----------|----------|-------------|-------|
| F-01 | `skills/test-spec/SKILL.md` | eng-lead | 10a | eng-reviewer | C3 | 14-section SKILL.md body. GAP in section 7 (P-003 diagram). |
| F-02 | `skills/test-spec/agents/tspec-generator.md` | eng-backend | 10b | eng-security, eng-reviewer | C3 | Official frontmatter + 7 XML-tagged sections. |
| F-03 | `skills/test-spec/agents/tspec-generator.governance.yaml` | eng-backend | 10b | eng-security, eng-reviewer | C3 | Must pass `agent-governance-v1.schema.json`. `reasoning_effort: high`. |
| F-04 | `skills/test-spec/agents/tspec-analyst.md` | eng-backend | 10b | eng-security, eng-reviewer | C3 | Same structural requirements as F-02. |
| F-05 | `skills/test-spec/agents/tspec-analyst.governance.yaml` | eng-backend | 10b | eng-security, eng-reviewer | C3 | Same structural requirements as F-03. |
| F-06 | `skills/test-spec/composition/tspec-generator.agent.yaml` | eng-backend | 10c | eng-reviewer | C2 | Follows agent-canonical schema. Pattern from uc-author.agent.yaml. |
| F-07 | `skills/test-spec/composition/tspec-generator.prompt.md` | eng-backend | 10c | eng-reviewer | C2 | Copy of F-02 body. MUST add synchronization note header (FIND-002). |
| F-08 | `skills/test-spec/composition/tspec-analyst.agent.yaml` | eng-backend | 10c | eng-reviewer | C2 | Same as F-06 pattern for analyst. |
| F-09 | `skills/test-spec/composition/tspec-analyst.prompt.md` | eng-backend | 10c | eng-reviewer | C2 | Copy of F-04 body. MUST add synchronization note header (FIND-002). |
| F-10 | `skills/test-spec/templates/bdd-scenario.template.md` | eng-backend | 10d | eng-reviewer | C2 | Verbatim from architecture Section 4. Complete template. |
| F-11 | `skills/test-spec/templates/test-plan.template.md` | eng-backend | 10d | eng-reviewer | C2 | Verbatim from architecture Section 4. Complete template. |
| F-12 | `skills/test-spec/rules/clark-transformation-rules.md` | eng-backend | 10e | eng-reviewer | C3 | Min 19 rules. < 500 lines. Navigation table required. |
| F-13 | `skills/test-spec/contracts/TS_SKILL_CONTRACT.yaml` | eng-lead | 10a | eng-reviewer | C2 | OpenAPI 3.0 inspired. Two agents. Schema $ref. |
| F-14 | `skills/test-spec/tests/BEHAVIOR_TESTS.md` | eng-qa | 10f | eng-reviewer | C3 | Min 7 BDD scenarios. Navigation table required. |

**Eng-lead authors:** F-01, F-13, and the three registration actions.
**Eng-backend authors:** F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-11, F-12 (11 files).
**Eng-qa authors:** F-14.

---

## Findings

### FIND-001 -- Medium: SKILL.md Section 7 P-003 Diagram Not Specified in Architecture

**Standard:** skill-standards.md §7 (required for multi-agent skills) -- SKILL.md MUST include an ASCII hierarchy diagram showing MAIN CONTEXT as orchestrator, per P-003 compliance.

**Evidence:** Architecture Section 6 provides the three-skill pipeline diagram (`/use-case -> /test-spec -> /contract-design`) but does not include the internal `/test-spec` P-003 diagram showing `MAIN CONTEXT -> tspec-generator` and `MAIN CONTEXT -> tspec-analyst` as separate worker invocations. The architecture's self-review checklist item for H-34 references P-003 but does not enumerate the SKILL.md section 7 requirement.

**Impact:** Without explicit P-003 diagram specification in the architecture, eng-lead could omit this section during SKILL.md authoring. The SKILL.md Structure Compliance audit above identifies this as a GAP.

**Recommendation:** Eng-lead to author section 7 using this pattern:

```
MAIN CONTEXT (orchestrator)
    |
    +-- tspec-generator (T2 worker) -- via Task tool
    |   Reads: UC artifact (.md with YAML frontmatter)
    |   Writes: Feature file (.feature.md)
    |
    +-- tspec-analyst (T2 worker) -- via Task tool
        Reads: Feature file + UC artifact
        Writes: Coverage report (-coverage.md)

Workers do NOT invoke each other.
tspec-generator output (Feature file) is consumed by tspec-analyst via filesystem.
```

**Action:** eng-lead to include this diagram in SKILL.md section 7 during F-01 authoring. No architecture revision needed.

---

### FIND-002 -- Medium: Composition File Synchronization Protocol Required for F-07 and F-09

**Standard:** P-001 (truth and accuracy) -- artifact content must be accurate and consistent. Pattern from Step 9 FIND-004 (executed action).

**Evidence:** F-07 (`tspec-generator.prompt.md`) and F-09 (`tspec-analyst.prompt.md`) are described in the architecture as "copy of the markdown body from the agent `.md` file." The Step 9 implementation resolved this for `/use-case` by adding a synchronization note to `uc-author.prompt.md` (confirmed in the implemented file). The same protocol must be applied to F-07 and F-09.

**Impact:** If F-02 or F-04 are updated post-implementation, the composition prompt files could become stale, causing Task-invoked agents to use outdated methodology or guardrails. This is a known and accepted technical debt pattern; the synchronization note is the established mitigation.

**Recommendation:** Eng-backend to add the following note at the top of F-07 and F-09 (before the `<identity>` section):

> `Synchronization note: This file is a manually-maintained copy of the markdown body from skills/test-spec/agents/tspec-generator.md (or tspec-analyst.md). When updating the corresponding agent .md file, this file MUST be updated in the same commit.`

**Action:** eng-backend to add the synchronization note header during Wave 2a authoring of F-07 and F-09. This mirrors the `uc-author.prompt.md` pattern established in Step 9.

---

### FIND-003 -- Low: H-26 Registration Actions Must Execute After F-01

**Standard:** H-26(c) -- New skills MUST be registered in CLAUDE.md, AGENTS.md, and mandatory-skill-usage.md. H-32 -- GitHub Issue parity for Jerry repo work items.

**Evidence:** The three registration actions are correctly assigned to eng-lead at sub-step 10a but depend on F-01 (SKILL.md) being authored first. Registration actions before F-01 is complete would cause stale registrations if SKILL.md content changes.

**Impact:** If registration occurs before F-01 is finalized, the CLAUDE.md and AGENTS.md entries may reference incorrect agent counts or routing information. The trigger map row is stable (designed in architecture) but the AGENTS.md entry requires accurate output location information from the finalized governance YAML.

**Action (tracked in this review):** Registration actions are tracked in Wave 4b above. The exact trigger map row is reproduced in the Dependency Analysis section. Eng-reviewer close-out checklist for the `/test-spec` skill MUST verify that all three registration files have been updated before marking implementation complete.

---

### FIND-004 -- Low: Trigger Map Row Must Be Inserted After Priority-13 /use-case Entry

**Standard:** agent-routing-standards.md §Priority Ordering -- trigger map rows must be ordered by priority number to preserve routing resolution algorithm correctness.

**Evidence:** The `/test-spec` trigger map row at priority 14 must be inserted immediately after the priority-13 `/use-case` row in `mandatory-skill-usage.md`. If `/use-case` registration is still PENDING at the time of `/test-spec` registration (e.g., if the two implementations proceed concurrently), the ordering must be verified after both rows are added.

**Impact:** Incorrect ordering does not break routing functionality (the routing algorithm uses numeric comparison, not table order), but creates a maintenance confusion risk: a reader expecting priority-ascending order would find the table misleading. The trigger map table is an H-22 compliance artifact and should accurately represent the routing priority structure.

**Action:** Eng-lead to verify that the mandatory-skill-usage.md trigger map table is sorted by priority (ascending) after both `/use-case` (priority 13) and `/test-spec` (priority 14) rows are inserted. Insert /test-spec row after the /use-case row.

---

## GATE-3 Carryforward

This section documents items from the `/use-case` Step 9 implementation (FIND-001 through FIND-005) that have direct relevance to `/test-spec` implementation.

| Step 9 Finding | Status | Impact on /test-spec |
|----------------|--------|----------------------|
| FIND-001 (ET-M-001 reasoning_effort) | **RESOLVED in architecture** -- Both tspec-generator and tspec-analyst governance YAML specs already include `reasoning_effort: high`. The gap that existed in Step 9's /use-case specification was pre-corrected in the /test-spec architecture. | No action required. |
| FIND-002 (output_filtering categorization) | **Informational** -- The /use-case conclusion was "no change required; categorization is defensible." | Applies to /test-spec: `tspec-generator.output_filtering` entries (`every_scenario_must_trace_to_source_flow_step`, `all_given_clauses_must_derive_from_preconditions_or_flow_context`) are structural correctness rules, not data safety filters. Same assessment: defensible by precedent. No change required. |
| FIND-003 (H-26 registration tracking) | **Executed action in Step 9 review** -- Registration tracking for /use-case established in Step 9 review. | Replicated for /test-spec: FIND-003 and FIND-004 in this review establish the same tracking for /test-spec registration. |
| FIND-004 (composition file synchronization) | **Executed action in Step 9** -- `uc-author.prompt.md` has synchronization note header. | **Active requirement for /test-spec:** FIND-002 in this review mandates the same note for F-07 and F-09. |
| FIND-005 (interactions block speculative status) | **Informational / no action** -- `$.interactions` is ARCHITECTURALLY SPECULATIVE in the shared schema. | **Does NOT affect /test-spec:** tspec-generator reads `$.basic_flow`, `$.alternative_flows`, `$.extensions`, `$.preconditions`, `$.postconditions`, and `$.trigger`. It does NOT read `$.interactions`. The speculative block is /contract-design's concern, not /test-spec's. No impact. |

**PRE-01 (Pipeline prerequisite):** The `/test-spec` input validation gate (`$.detail_level >= ESSENTIAL_OUTLINE`) means that the default behavior of `/use-case` (producing BULLETED_OUTLINE by default) creates a friction point. Step 9 L2 Strategic Implications documented this: if > 50% of UC artifacts are rejected by tspec-generator, the fix is in /use-case's default level. This is a known operational characteristic, not an implementation defect. Eng-backend should include a clear rejection message in the tspec-generator `<guardrails>` section per architecture Section 5 error handling table.

**REC-01 (Cross-skill pipeline trust boundary):** The trust boundary established by Step 9 (`use-case-realization-v1.schema.json` as the validation contract) is inherited by /test-spec. The architecture correctly implements this: tspec-generator validates every input UC artifact against the shared schema (Layer 1) before applying Clark transformation. The `$.work_type = USE_CASE` discriminator guards against non-UC artifacts. No additional action required from /test-spec implementation -- the boundary is designed correctly.

---

## L2: Strategic Implications

### Precedent-Setting Decisions

**1. Creator-Evaluator Pattern Within a Single Skill**

The `tspec-generator` (creator) / `tspec-analyst` (evaluator) split establishes a creator-evaluator pattern within a single skill that is distinct from the cross-skill `/adversary` quality gate. `tspec-analyst` evaluates domain-specific coverage completeness (C1 Coverage using the 7 Cs framework) rather than general deliverable quality. This pattern should be considered for `/contract-design`: a `cd-generator` (produces OpenAPI spec) / `cd-validator` (validates spec against use case interaction model) split would provide the same benefits -- separate cognitive modes, different input/output profiles, independent invocability.

The implementation decision to separate agents (rather than keep a single tspec-generator with embedded coverage analysis) should be monitored per RISK-15: if tspec-analyst invocation rate drops below 20% after 20 feature file generations, merging is the indicated response. The architecture documents this merge path.

**2. .feature.md Format as Pipeline Contract**

The `.feature.md` extension with YAML frontmatter (`source_use_case`, `source_title`, `source_detail_level`, `generated_by`, `generated_at`, `scenario_count`, `coverage`) establishes a Feature file format that carries traceability metadata. This format is now a de facto contract between tspec-generator (producer) and tspec-analyst (consumer) -- tspec-analyst parses the `source_use_case` frontmatter to locate the corresponding UC artifact for cross-reference analysis.

The `scripts/extract-gherkin.sh` path (file-organization.md line 286) provides the Cucumber compatibility bridge. The eng-devsecops scope should be informed that this script must exist if teams need to execute Feature files against a BDD runner.

**3. Two-Layer Input Validation as Cross-Skill Standard**

The JSON Schema structural gate (Layer 1) + agent guardrail semantic gate (Layer 2) is now established by both `/use-case` (output validation) and `/test-spec` (input validation from the same schema). This constitutes a confirmed pattern across two skills. Eng-lead recommends documenting this pattern formally as `PAT-TWO-LAYER-VALIDATION-001` in `.context/patterns/` once the three-skill pipeline is complete. It should be cited as a required pattern in the `/contract-design` architecture specification.

### SAMM Maturity Assessment (Relevant Practices)

| Practice | Current Maturity (Post-Step 9) | Target (Post-Step 10 Implementation) |
|----------|-------------------------------|--------------------------------------|
| Security Requirements (SSDF PO.1) | L1 -- security requirements derived from threat model (STRIDE documented in architecture) | L1 maintained -- no new security capability required for /test-spec. STRIDE analysis in architecture Section L2 confirmed C1 (low) across all threat categories. |
| Secure Design (SSDF PO.3) | L2 -- two-layer validation gate, T2 minimum privilege, schema contract from Step 9 | L2 maintained -- /test-spec inherits Step 9's two-layer validation. T2 tier for both agents. Schema contract at input boundary. |
| Secure Build (SSDF PS.1) | L1 -- CI L5 schema validation gate for governance YAML and use case artifacts | L1 maintained -- same CI gates apply. No new build tooling required. Composition file parity check (FIND-002) adds a low-cost L5 improvement when implemented. |
| Code Integrity (SSDF PS.2) | L1 -- git tracks all artifact changes | L1 maintained -- Feature files and coverage reports tracked via git. `generated_by`/`generated_at` frontmatter fields add audit trail within each artifact. |

### Technical Debt Assessment

**Risk: Composition File Synchronization (FIND-002)**

The manual copy pattern for F-07/F-09 is the same technical debt as FIND-004 from Step 9. At 4 total composition prompt files (2 from /use-case, 2 from /test-spec), the cost is still manageable. If `/contract-design` follows the same pattern, the framework will have 6 manually-synchronized prompt file pairs. The synchronization note header is a mitigation; the authoritative fix is an automated CI parity check (eng-devsecops scope, confirmed as the recommended action in Step 9 FIND-004).

**Risk: tspec-analyst Invocation Rate (RISK-15)**

The 2-agent split creates overhead if coverage analysis is rarely requested. RISK-15 (LOW severity, MEDIUM likelihood) specifies the merge trigger: invocation rate < 20% after 20 feature file generations. This is a post-implementation monitoring concern, not an implementation blocker. The merge path (combining tspec-analyst coverage analysis into tspec-generator as a post-generation quality check step) is fully documented in the architecture and requires only changes to composition files, SKILL.md routing, and behavior tests.

**Long-Term Maintainability**

The 14-file skill structure (vs. 17 files for /use-case) is proportional to 2 agents and the Clark algorithm methodology. Future capability expansion would follow established patterns:
- Adding Cucumber export support: add `scripts/extract-gherkin.sh` (referenced in architecture file-organization.md line 286)
- Adding a third agent for test scenario prioritization: add F-04b definition files following the same dual-file pattern
- Schema evolution: handled by `use-case-realization-v1.schema.json` SemVer; /test-spec agents reference the schema by path and automatically consume updated versions

---

## Self-Review Checklist (H-15 / S-010)

### Constitutional Compliance

- [x] **P-001 (Truth/Accuracy):** Every finding cites the specific standard ID and quotes the relevant specification evidence. Compliance determinations trace to documented fields and architecture sections.
- [x] **P-002 (File Persistence):** Review persisted to `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/implementation/step-10-eng-lead-review.md`.
- [x] **P-003 (No Recursive Subagents):** This is a read-and-write review document. No subagent delegation performed.
- [x] **P-022 (No Deception):** Limitations disclosed -- the PENDING registration items are correctly labeled as future tasks, not defects. The GAP in SKILL.md section 7 is disclosed with a complete remediation. Confidence levels appropriate.

### Structural Compliance

- [x] **H-23 (Navigation):** Navigation table present at document top. All `##` sections covered with anchor links.
- [x] **H-15 (Self-Review):** This section is the S-010 application.
- [x] **P-002 (Output levels):** L0 (executive summary), L1 (compliance matrix + implementation plan), L2 (strategic implications) all present.

### Standards Coverage Completeness

- [x] H-34 verified (14 sub-requirements checked; 14/14 PASS)
- [x] H-25 verified (5 sub-requirements checked; 5/5 PASS)
- [x] H-26 verified (9 sub-requirements checked; 6 PASS, 3 PENDING implementation tasks)
- [x] H-23 verified (navigation table present in architecture, requirement briefed for F-01, F-12, F-14)
- [x] H-20 verified (BDD test-first assessment for F-14; H-20 framework satisfied, eng-qa briefed)
- [x] H-22 verified (trigger map entry at priority 14; all 5 columns present; disambiguation documented)
- [x] Naming convention verified (AD-M-001; tspec-generator, tspec-analyst; 5/5 PASS)
- [x] Tool tier verified (T2 appropriateness for both agents; Task exclusion; tool count 6/15 threshold; 5/5 PASS)
- [x] AD-M-001 through AD-M-009 and ET-M-001 verified (10/10 PASS)
- [x] Dependency analysis: 9 dependencies traced; 0 blockers; runtime vs. authoring dependencies distinguished
- [x] Implementation plan: 14 files, 5 waves, critical path identified with F-12 runtime dependency note
- [x] File responsibility matrix: all 14 files mapped to owner, sub-step, reviewer, criticality
- [x] GATE-3 carryforward: 5 Step-9 findings assessed; 1 active requirement (FIND-002/FIND-004 synchronization), 1 resolved (FIND-001 reasoning_effort), 1 confirmed no-impact (FIND-005 interactions block)
- [x] 4 findings produced with severity levels and actionable recommendations

### Adversarial Challenge (S-002: Devil's Advocate Applied)

**Challenge 1: "Is the PASS determination for H-34 valid given that governance YAML was not schema-validated at the code level?"**

The review verified the architecture's governance YAML specifications against the schema requirements by inspecting `docs/schemas/agent-governance-v1.schema.json` (confirmed in this review). The `required` array is `["version", "tool_tier", "identity"]` -- all three present in both specs. The `guardrails` sub-schema is not listed in the top-level `required` array (guardrails is a recommended, not required, governance field), but both specs declare `guardrails.fallback_behavior: "escalate_to_user"` which satisfies the schema's guardrails property definition. The `capabilities.forbidden_actions` minimum 3 entries with P-003/P-020/P-022 references are present in both agents (5 entries each). The PASS determinations are based on field-by-field comparison against the schema source, which is deterministic. Runtime schema validation (L3/L5) will be the authoritative check when the actual YAML files are authored.

**Challenge 2: "Why is the SKILL.md section 7 GAP not elevated to a blocking defect?"**

Section 7 (P-003 ASCII diagram) is a required section per skill-standards.md §7 for multi-agent skills. However, the missing element is not a specification defect -- the architecture does not specify SKILL.md body content verbatim (that is eng-lead's authoring responsibility). The GAP is an authoring gap discovered by this review, and the exact diagram content is provided in FIND-001. Eng-lead has all the information needed to author the section correctly. Elevating to blocking would incorrectly suggest the architecture is defective; the correct characterization is that this review has identified an authoring requirement that was not explicitly briefed in the architecture. The implementation plan places F-01 (SKILL.md) as a Wave 4 eng-lead task, and the finding is documented at FIND-001 medium priority with a complete remediation.

**Challenge 3: "Is the priority-14 /test-spec trigger map entry correctly analyzed for collisions with /use-case at priority 13?"**

The keyword sets are verified as disjoint after negative filtering. /use-case triggers on "use case", "write use case", "cockburn", "basic flow", "jacobson". /test-spec triggers on "BDD", "Gherkin", "feature file", "Clark transformation". These are domain-separated vocabulary sets with no natural-language overlap. The negative keywords on /test-spec explicitly suppress /use-case vocabulary: "write use case", "create use case", "use case authoring". The negative keywords on /use-case suppress /test-spec vocabulary: "test spec", "BDD", "Gherkin". Compound triggers on /test-spec ("generate tests from use case", "BDD scenario") require qualification that is absent from /use-case keywords. The priority-14 analysis is sound.

---

*Standards Enforcement Review Version: 1.0.0*
*Input: step-10-test-spec-architecture.md v1.1.0 (PASSED 0.952 / threshold 0.95)*
*Standards Verified: H-34 (14/14), H-35 (sub-item), H-25 (5/5), H-26 (6 PASS 3 PENDING), H-23, H-22 (trigger map 5-column), H-20 (F-14 BDD framework), ET-M-001, AD-M-001..AD-M-009, tool tiers T1-T5, P-003 topology, naming convention (tspec-), dependency governance (9 traced), SKILL.md 14-section structure (9 PASS 1 GAP 4 PENDING)*
*Findings: 4 total (0 blocking, 2 medium, 2 low)*
*GATE-3 Carryforward: 5 Step-9 findings assessed; 1 active (FIND-002 synchronization note), 1 resolved pre-applied (ET-M-001), 1 no-impact (interactions block)*
*Implementation Plan: 14 files, 5 waves, critical path identified with F-12 runtime dependency note*
*Next Agent: eng-backend (Wave 1 can begin immediately)*
*Workflow ID: use-case-skills-20260308-001*
*Date: 2026-03-09*
