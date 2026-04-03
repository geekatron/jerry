# Standards Enforcement Review: /use-case Skill

> **PS ID:** proj-021 | **Entry ID:** step-9-eng-lead-review | **Workflow ID:** use-case-skills-20260308-001
> **Date:** 2026-03-09 | **Agent:** eng-lead | **Step:** 9 (Phase 3 Implementation)
> **Input:** step-9-use-case-architecture.md (v1.2.0, PASSED 0.956)
> **Status:** PROPOSED
> **Version:** 1.0.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Compliance status and key findings at a glance |
| [L1: Standards Compliance Matrix](#l1-standards-compliance-matrix) | Evidence-based PASS/FAIL/N-A for every applicable standard |
| [Implementation Plan](#implementation-plan) | Ordered file creation plan for eng-backend with dependency graph |
| [Dependency Analysis](#dependency-analysis) | Internal prerequisites, external dependencies, blockers |
| [Findings](#findings) | Standards gaps, issues, recommendations, risk escalations |
| [L2: Strategic Implications](#l2-strategic-implications) | Maintainability, precedent-setting decisions, technical debt |
| [Self-Review Checklist (H-15 / S-010)](#self-review-checklist-h-15--s-010) | Pre-delivery quality verification |

---

## L0: Executive Summary

- The architecture design (step-9-use-case-architecture.md v1.2.0) is **implementation-ready**. All hard-rule compliance requirements (H-34, H-25, H-26, H-23, P-003, tool tiers) are satisfied by the specification. No blocking defects were identified during this review.
- **Two medium-priority findings** require action before eng-backend begins authoring agent definition files: (F-01) the `guardrails.output_filtering` array specified for both agents contains 5 entries but the schema minimum is 3 -- this is compliant, however one entry (`all_flow_steps_must_have_typed_classification`) is an agent behavioral rule rather than an output safety filter, and should be considered for relocation to `guardrails.input_validation`; (F-02) the SKILL.md frontmatter uses `allowed-tools` (hyphen) and `activation-keywords` (hyphen) per Jerry convention but these are Jerry-specific fields, not official Claude Code frontmatter fields -- this is intentional per existing skill patterns and compliant, but eng-backend must be briefed on which YAML fields are official vs. Jerry-convention.
- **One low-priority registration gap** exists: the architecture correctly designates eng-lead (sub-step 10a) as the author of SKILL.md (F-01) and UC_SKILL_CONTRACT.yaml (F-15), but the registration actions required by H-26 (CLAUDE.md, AGENTS.md, mandatory-skill-usage.md) are not yet tracked in any worktracker entity -- this review creates that tracking.
- All 17 files have a clear owner, criticality level, and dependency ordering that supports a low-risk parallel implementation.
- No external package dependencies. The production schema copy (F-17) is a filesystem copy from an existing design-phase artifact; no network or external toolchain access is required.

---

## L1: Standards Compliance Matrix

### H-34 Compliance -- Agent Definition Architecture

| Requirement | Evidence | Status |
|-------------|----------|--------|
| Dual-file architecture: `.md` + `.governance.yaml` per agent | Architecture specifies F-02/F-03 (uc-author) and F-04/F-05 (uc-slicer) as separate pairs. Directory tree explicit. | **PASS** |
| Official `.md` frontmatter fields only | Both agent frontmatter blocks use only recognized Claude Code fields: `name`, `description`, `model`, `tools`. No non-standard fields in frontmatter. | **PASS** |
| `.governance.yaml` required field: `version` (SemVer pattern) | Both specs declare `version: "1.0.0"`. Pattern `^\d+\.\d+\.\d+$` satisfied. | **PASS** |
| `.governance.yaml` required field: `tool_tier` (enum T1-T5) | Both declare `tool_tier: "T2"`. T2 is correct for Read-Write agents without external or delegation access. | **PASS** |
| `.governance.yaml` required field: `identity.role` | uc-author: "Use Case Author -- creates and elaborates...". uc-slicer: "Use Case Slicer -- decomposes...". Both non-empty, unique within the skill. | **PASS** |
| `.governance.yaml` required field: `identity.expertise` (min 2 entries) | uc-author: 3 entries. uc-slicer: 3 entries. Both exceed minimum. Entries are specific domain competencies (Cockburn, Jacobson), not generic labels. | **PASS** |
| `.governance.yaml` required field: `identity.cognitive_mode` (enum) | uc-author: `integrative`. uc-slicer: `systematic`. Both are valid enum values per the 5-mode taxonomy. Mode selections are appropriate: uc-author integrates stakeholder inputs into unified artifacts (integrative); uc-slicer applies step-by-step slicing procedures (systematic). | **PASS** |
| `capabilities.forbidden_actions` min 3 entries referencing P-003, P-020, P-022 | uc-author: 5 entries, first 3 explicitly reference P-003, P-020, P-022. uc-slicer: 6 entries, first 3 explicitly reference P-003, P-020, P-022. | **PASS** |
| `forbidden_action_format` declared | Both specify `"NPT-009-complete"`. All entries use `{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {impact}` format. | **PASS** |
| `constitution.principles_applied` min 3 entries including P-003, P-020, P-022 | Both declare P-003, P-020, P-022 plus P-001, P-002, P-004. All three required principles present. | **PASS** |
| Worker agents MUST NOT include `Task` in `tools` field (H-35 sub-item b) | Both agents list only: Read, Write, Edit, Glob, Grep, Bash. No `Task` tool present. | **PASS** |
| Markdown body XML-tagged sections required | Architecture specifies all 7 required sections (`<identity>`, `<purpose>`, `<input>`, `<capabilities>`, `<methodology>`, `<output>`, `<guardrails>`) for both agents with content summaries. | **PASS** |
| Schema validation target: `docs/schemas/agent-governance-v1.schema.json` | The governance YAML fields (`version`, `tool_tier`, `identity`, `persona`, `capabilities`, `guardrails`, `output`, `constitution`, `validation`, `session_context`, `enforcement`) align with the schema's required and recommended properties. `guardrails.fallback_behavior` is present (`escalate_to_user`) satisfying the schema's only `guardrails` required field. | **PASS** |

### H-25 Compliance -- Skill Naming and Structure

| Requirement | Evidence | Status |
|-------------|----------|--------|
| Skill file is exactly `SKILL.md` (case-sensitive) | F-01 specified as `skills/use-case/SKILL.md`. Exact case. | **PASS** |
| Skill folder uses kebab-case | `skills/use-case/` is kebab-case. | **PASS** |
| Skill folder name matches `name` field in frontmatter | Frontmatter declares `name: use-case`. Folder is `skills/use-case/`. Match confirmed. | **PASS** |
| No `README.md` inside skill folder | No README.md appears in the 16-file manifest. Not planned. | **PASS** |

### H-26 Compliance -- Skill Description, Paths, and Registration

| Requirement | Evidence | Status |
|-------------|----------|--------|
| `description` includes WHAT | "Guided use case authoring and slicing using Cockburn 12-step writing process and Jacobson UC 2.0 methodology" -- clear WHAT statement. | **PASS** |
| `description` includes WHEN | "Invoke when writing, creating, authoring, elaborating, slicing, or decomposing use cases" -- explicit WHEN clause. | **PASS** |
| `description` includes trigger phrases | 20 activation keywords listed. Multiple domain-specific triggers (cockburn, jacobson, basic flow, main success scenario, use case slice). | **PASS** |
| `description` under 1024 chars | The specified description text is approximately 370 characters. Well within limit. | **PASS** |
| No XML tags (`< >`) in frontmatter description | Description text inspected. No angle brackets present. | **PASS** |
| Full repo-relative paths in SKILL.md | Integration points table uses `docs/schemas/use-case-realization-v1.schema.json`, `skills/use-case/rules/use-case-writing-rules.md`, `skills/use-case/templates/`. All are full repo-relative paths. | **PASS** |
| Register in CLAUDE.md | **NOT YET DONE** -- Architecture assigns this to eng-lead (sub-step 10a, F-01). Action tracked as FIND-003 below. | **PENDING** |
| Register in AGENTS.md | **NOT YET DONE** -- Architecture assigns this to eng-lead (sub-step 10a, F-01). Action tracked as FIND-003 below. | **PENDING** |
| Register in mandatory-skill-usage.md | **NOT YET DONE** -- Architecture assigns this to eng-lead (sub-step 10a, F-01). Trigger map entry is designed (priority 13, keywords, negative keywords, compound triggers). Action tracked as FIND-003 below. | **PENDING** |

**Registration status note:** The PENDING entries above are not defects in the architecture document -- they are implementation tasks correctly assigned to eng-lead at sub-step 10a. This review confirms the assignment and flags it as a dependency for CLAUDE.md routing to work correctly. Registration must occur after F-01 (SKILL.md) is authored, but the trigger map entry design is complete and ready to apply.

### H-23 Compliance -- Markdown Navigation

| Requirement | Evidence | Status |
|-------------|----------|--------|
| Navigation table in architecture document (step-9-use-case-architecture.md, >30 lines) | Navigation table present at document top with 10 entries, all with anchor links. | **PASS** |
| All `##` headings covered in navigation | L0, L1, L2, 7 numbered sub-sections, GATE-2 Resolution, Self-Review, Iter-2 Log, Iter-3 Log all listed. | **PASS** |
| Navigation table uses anchor links (NAV-006) | All entries are in `[Section Name](#anchor)` format. Anchors verified against actual section names. | **PASS** |
| SKILL.md (F-01) design requires navigation | Architecture specifies a SKILL.md body following skill-standards.md structure. Navigation table is required per H-23/NAV-001. Architecture does not include the SKILL.md body content verbatim, but the SKILL.md design section establishes compliance with the standard. Nav requirement is eng-backend's responsibility during authoring. | **PASS (design) / PENDING (authoring)** |

### Tool Tier Verification

| Standard | Evidence | Status |
|----------|----------|--------|
| uc-author T2 (Read-Write) is appropriate | uc-author reads project context files and writes use case artifact files. No external network access, no cross-session state, no delegation. T2 (Read, Write, Edit, Glob, Grep, Bash) exactly matches the required capability set. | **PASS** |
| uc-slicer T2 (Read-Write) is appropriate | uc-slicer reads artifact files, writes updated frontmatter, and invokes Bash for worktracker CLI commands (`uv run jerry items create`). No external access or delegation. T2 is correct. | **PASS** |
| Neither agent includes Task tool (P-003) | Tools arrays: `[Read, Write, Edit, Glob, Grep, Bash]` for both. Task absent in both. | **PASS** |
| Tool count within 15-agent threshold (AP-07) | 6 tools per agent. Well below the 15-tool alert threshold. No selection accuracy risk. | **PASS** |

### Cognitive Mode Appropriateness (AD-M-001 through AD-M-009)

| Standard | Evidence | Status |
|----------|----------|--------|
| AD-M-001 -- Naming follows `{skill-prefix}-{function}` pattern | `uc-author` (prefix: uc, function: author). `uc-slicer` (prefix: uc, function: slicer). Pattern `^[a-z]+-[a-z]+(-[a-z]+)*$` satisfied. | **PASS** |
| AD-M-002 -- Version uses SemVer | `"1.0.0"` for both. | **PASS** |
| AD-M-003 -- Description max 1024 chars, no XML, WHAT+WHEN+trigger | uc-author: ~230 chars, includes WHAT/WHEN/triggers. uc-slicer: ~235 chars, includes WHAT/WHEN/triggers. | **PASS** |
| AD-M-004 -- L0 and L1 output levels declared | Both declare `levels: ["L0", "L1"]`. L2 not declared; not required for workflow agents that produce domain artifacts rather than stakeholder-facing analysis. Appropriate omission per AD-M-004 guidance for non-stakeholder-facing agents. | **PASS** |
| AD-M-005 -- `identity.expertise` min 2 specific entries | 3 specific entries each. All reference named methodologies (Cockburn, Jacobson, INVEST). | **PASS** |
| AD-M-006 -- `persona` declared | Both declare `tone: "methodical"`, `communication_style: "structured"`, `audience_level: "adaptive"`. | **PASS** |
| AD-M-007 -- `session_context` with `on_receive` / `on_send` | Both declare `session_context` with 3-item `on_receive` and 3-item `on_send`. Aligned with handoff protocol (HD-M-001). | **PASS** |
| AD-M-008 -- `validation.post_completion_checks` declared | uc-author: 6 checks. uc-slicer: 7 checks. Both include schema validation, artifact existence verification, and domain-specific semantic checks. | **PASS** |
| AD-M-009 -- Model selection justified per cognitive demands | Both use `sonnet`. Appropriate for `integrative` (synthesis of structured inputs, standard production task) and `systematic` (procedural checklist execution, compact work). Architecture explicitly documents sonnet as first choice with opus escalation path if quality scores fall below 0.92. | **PASS** |
| ET-M-001 -- `reasoning_effort` alignment | Not declared in governance YAML. Architecture does not specify reasoning_effort for either agent. Both are C3 files (per File Responsibility Matrix). C3 maps to `high` reasoning_effort per ET-M-001. This is a **medium-priority gap** (see FIND-001 below). | **GAP** |

### Dependency Governance

| Requirement | Evidence | Status |
|-------------|----------|--------|
| No external package dependencies required | All 16 skill files are markdown, YAML, or JSON. No Python packages, npm modules, or OS-level tooling beyond what Jerry Framework already provides (`uv run jerry items create` is an existing CLI command). | **PASS** |
| Production schema path correct | F-17: `docs/schemas/use-case-realization-v1.schema.json` is the designated production path. Copy source: `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/architecture/shared-schema.json`. Path follows existing schema directory conventions (verified: `docs/schemas/agent-governance-v1.schema.json` exists at that pattern). | **PASS** |
| Templates are self-contained | 4 template files contain only markdown and YAML placeholder syntax `{PLACEHOLDER}`. No external references, no imported libraries. | **PASS** |
| Composition file schema reference exists | Architecture cites `docs/schemas/agent-canonical-v1.schema.json` with verified `$id`. Reference pattern follows existing composition files (ps-researcher.agent.yaml). | **PASS** |
| Skill contract follows existing pattern | UC_SKILL_CONTRACT.yaml follows PS_SKILL_CONTRACT.yaml and NSE_SKILL_CONTRACT.yaml OpenAPI 3.0-inspired pattern. Both reference files verified in codebase. | **PASS** |

### P-003 Architecture Compliance

| Requirement | Evidence | Status |
|-------------|----------|--------|
| Single-level nesting diagram present | Section 6 includes explicit ASCII orchestration diagram: Main Context invokes uc-author, then uc-slicer. Workers do not invoke each other. | **PASS** |
| File-mediated handoff (no direct agent-to-agent) | "Agents communicate exclusively through the use case artifact file on disk." Handoff contract passes only artifact_path, detail_level, key_findings, success_criteria, schema_validation. No sub-agent spawning. | **PASS** |
| Worktracker integration via Bash (not via Task) | uc-slicer invokes worktracker via `uv run jerry items create` Bash command. Explicit "MUST NOT invoke /worktracker via Task -- P-003 violation" in system prompt outline. | **PASS** |

### H-22 Trigger Map Entry (Mandatory Skill Usage)

| Requirement | Evidence | Status |
|-------------|----------|--------|
| Trigger map entry designed with all 5 columns | Priority 13, detected keywords (21 terms), negative keywords (13 terms), compound triggers (8 phrase triggers), skill name. | **PASS** |
| Priority justified relative to adjacent skills | Priority 13 justification documented: gap analysis against /nasa-se (disjoint after negative filtering, 8-level numeric gap), against /user-experience (completely disjoint keyword sets, gap rule Step 3 not invocable). | **PASS** |
| Negative keywords prevent false positives | "requirements specification", "V&V", "technical review", "trade study", "compliance" suppress /nasa-se co-match. "test spec", "BDD", "Gherkin", "OpenAPI", "contract", "API design" suppress /test-spec and /contract-design co-matches. | **PASS** |

---

## Implementation Plan

### Dependency Graph

```
[F-17] docs/schemas/use-case-realization-v1.schema.json  (eng-infra, no deps)
   |
   +---> [F-02] uc-author.md                             (eng-backend, depends on F-17 for schema ref)
   |     [F-03] uc-author.governance.yaml                (eng-backend, parallel with F-02)
   |     [F-04] uc-slicer.md                             (eng-backend, parallel with F-02)
   |     [F-05] uc-slicer.governance.yaml                (eng-backend, parallel with F-02)
   |
   +---> [F-10] use-case-realization.template.md         (eng-backend, depends on F-17 schema fields)
   |     [F-11] use-case-brief.template.md               (eng-backend, parallel with F-10)
   |     [F-12] use-case-casual.template.md              (eng-backend, parallel with F-10)
   |     [F-13] use-case-slice.template.md               (eng-backend, parallel with F-10)
   |
   +---> [F-06] uc-author.agent.yaml                     (eng-backend, depends on F-02)
   |     [F-07] uc-author.prompt.md                      (eng-backend, depends on F-02, copy of body)
   |     [F-08] uc-slicer.agent.yaml                     (eng-backend, depends on F-04)
   |     [F-09] uc-slicer.prompt.md                      (eng-backend, depends on F-04, copy of body)
   |
   +---> [F-14] use-case-writing-rules.md                (eng-backend, no deps beyond methodology)
   |
   +---> [F-01] SKILL.md                                 (eng-lead, depends on F-02..F-05 for agent table)
   |     [F-15] UC_SKILL_CONTRACT.yaml                   (eng-lead, depends on F-02..F-05 for schema refs)
   |
   +---> [F-16] BEHAVIOR_TESTS.md                        (eng-qa, depends on F-01..F-14)

Registration actions (eng-lead, after F-01 complete):
   - CLAUDE.md skill table entry
   - AGENTS.md section (uc-author, uc-slicer entries)
   - mandatory-skill-usage.md trigger map row (priority 13)
```

### Ordered Creation Schedule

**Wave 1 -- Foundation (no internal dependencies, create in parallel):**

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-17 | `docs/schemas/use-case-realization-v1.schema.json` | eng-infra | C2 | File copy only. Source: `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/architecture/shared-schema.json`. Verify copy integrity with checksum. |
| F-14 | `skills/use-case/rules/use-case-writing-rules.md` | eng-backend | C2 | No external deps. Cockburn 12-step rules. Encode progressive loading (steps 1-4 / 1-10 / full per CB-05). |

**Wave 2 -- Agent Definitions (depend only on F-17 for schema ref):**

All 4 files can be created in parallel.

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-02 | `skills/use-case/agents/uc-author.md` | eng-backend | C3 | Official frontmatter + 7 XML-tagged body sections. Do NOT include `reasoning_effort` in .md; add to .governance.yaml (see FIND-001). |
| F-03 | `skills/use-case/agents/uc-author.governance.yaml` | eng-backend | C3 | Must validate against `docs/schemas/agent-governance-v1.schema.json`. Add `reasoning_effort: high` for C3 per ET-M-001 (FIND-001). |
| F-04 | `skills/use-case/agents/uc-slicer.md` | eng-backend | C3 | Same structural requirements as F-02. |
| F-05 | `skills/use-case/agents/uc-slicer.governance.yaml` | eng-backend | C3 | Same structural requirements as F-03. |

**Wave 3 -- Templates (depend only on F-17 for schema field alignment):**

All 4 files can be created in parallel.

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-10 | `skills/use-case/templates/use-case-realization.template.md` | eng-backend | C2 | Primary template; all schema fields present as placeholders. Validate that all required schema fields have corresponding `{PLACEHOLDER}` entries. |
| F-11 | `skills/use-case/templates/use-case-brief.template.md` | eng-backend | C2 | Minimal frontmatter template per architecture Section 4. |
| F-12 | `skills/use-case/templates/use-case-casual.template.md` | eng-backend | C2 | Bulleted outline template. |
| F-13 | `skills/use-case/templates/use-case-slice.template.md` | eng-backend | C2 | Slice document template; includes INVEST fields. |

**Wave 4 -- Composition Files (depend on Wave 2 agent definitions):**

All 4 files can be created in parallel once Wave 2 is complete.

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-06 | `skills/use-case/composition/uc-author.agent.yaml` | eng-backend | C2 | Follows `docs/schemas/agent-canonical-v1.schema.json`. Reference: `skills/problem-solving/composition/ps-researcher.agent.yaml`. Set `tools.forbidden: [agent_delegate]`. |
| F-07 | `skills/use-case/composition/uc-author.prompt.md` | eng-backend | C2 | Copy of F-02 markdown body. Must stay synchronized with F-02 on changes. |
| F-08 | `skills/use-case/composition/uc-slicer.agent.yaml` | eng-backend | C2 | Same as F-06 pattern for slicer. |
| F-09 | `skills/use-case/composition/uc-slicer.prompt.md` | eng-backend | C2 | Copy of F-04 markdown body. |

**Wave 5 -- Skill Entry Points (depend on Wave 2 agent definitions for agent table):**

Both can be created in parallel.

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-01 | `skills/use-case/SKILL.md` | eng-lead | C3 | Requires navigation table (H-23). Triple-lens audience structure per skill-standards.md. P-003 diagram required (multi-agent skill). All 14 SKILL.md body sections. After authoring, proceed to registration. |
| F-15 | `skills/use-case/contracts/UC_SKILL_CONTRACT.yaml` | eng-lead | C2 | Adapt PS_SKILL_CONTRACT.yaml pattern. Four agents (uc-author, uc-slicer). Schema `$ref` to `docs/schemas/use-case-realization-v1.schema.json`. |

**Wave 5b -- Registration (depends on F-01):**

| Action | File | Owner | Notes |
|--------|------|-------|-------|
| Register skill | CLAUDE.md -- Skills table | eng-lead | Add `/use-case` row to Quick Reference skills table. |
| Register agents | AGENTS.md | eng-lead | Add "/use-case Skill Agents" section: uc-author, uc-slicer entries with role and output location. Update Agent Summary table count. |
| Register trigger | mandatory-skill-usage.md | eng-lead | Insert priority-13 row in Trigger Map table using the designed entry from Section 2 of architecture document. |

**Wave 6 -- Tests (depends on all Wave 1-5 files):**

| File ID | File | Owner | Criticality | Notes |
|---------|------|-------|-------------|-------|
| F-16 | `skills/use-case/tests/BEHAVIOR_TESTS.md` | eng-qa | C3 | 7 minimum BDD scenarios specified in architecture Section 4 (F-16 subsection). All scenarios must map to acceptance criteria verifiable without running the full skill pipeline. Navigation table required (H-23). |

### Critical Path

```
F-17 (schema copy, Wave 1)
  --> F-02..F-05 (agent defs, Wave 2)
    --> F-01 (SKILL.md, Wave 5)
      --> Registration (Wave 5b)
        --> F-16 (tests, Wave 6)
```

The critical path length is 5 waves. Wave 3 (templates) and Wave 4 (composition) are off the critical path and can be developed concurrently with Waves 2 and 5 respectively. F-16 (BEHAVIOR_TESTS.md) is the terminal deliverable.

---

## Dependency Analysis

### Internal Dependencies (All Within Jerry Framework)

| Dependency | Consumer Files | Type | Status |
|------------|---------------|------|--------|
| `docs/schemas/agent-governance-v1.schema.json` | F-03, F-05 (.governance.yaml validation) | Schema validation | **EXISTS** -- confirmed at `/Users/adam.nowak/workspace/GitHub/geekatron/jerry-wt/feat/proj-021-use-case/docs/schemas/agent-governance-v1.schema.json` |
| `docs/schemas/agent-canonical-v1.schema.json` | F-06, F-08 (composition YAML) | Schema reference | **EXISTS** -- confirmed by architecture iter-3 verification note: `$id = https://jerry-framework.dev/schemas/agent-canonical/v1.0.0` |
| `skills/problem-solving/composition/ps-researcher.agent.yaml` | F-06, F-08 (reference implementation) | Pattern reference | **EXISTS** -- skill in production |
| `skills/problem-solving/contracts/PS_SKILL_CONTRACT.yaml` | F-15 (adaptation template) | Pattern reference | **EXISTS** -- confirmed in codebase |
| `docs/governance/JERRY_CONSTITUTION.md` | F-03, F-05 (`constitution.reference` field) | Reference | **EXISTS** -- standard path |
| `uv run jerry items create` (CLI command) | F-04 / F-09 (uc-slicer worktracker integration) | Runtime dependency | **EXISTS** -- Jerry v0.24.0, H-05 compliant |
| Source schema for F-17 | F-17 (file copy) | Source artifact | **EXISTS** -- `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/architecture/shared-schema.json` |

### Registration Prerequisites (Before Routing Works)

The three registration files must be updated before `/use-case` can be invoked via keyword routing. Until registration is complete, the skill can only be invoked via explicit `/use-case` slash command.

| File | Change Required | Priority |
|------|----------------|----------|
| `CLAUDE.md` | Add `/use-case` row to Quick Reference skills table | HIGH -- affects skill discoverability |
| `AGENTS.md` | Add `/use-case Skill Agents` section; update Agent Summary count | MEDIUM -- affects agent discovery |
| `.context/rules/mandatory-skill-usage.md` | Insert priority-13 trigger map row | HIGH -- affects H-22 proactive invocation |

### External Dependencies

None. The `/use-case` skill has no external package dependencies, no external API calls, no MCP server requirements. This is a T2 (Read-Write) skill that operates entirely on local filesystem artifacts.

### Blockers

None blocking implementation start. All Wave 1 prerequisites (schema files, CLI tooling, reference patterns) exist.

The only sequential constraint is F-17 must exist before eng-backend writes agent definitions that reference the production schema path. F-17 is a simple file copy requiring no design work, so it can be completed in under 5 minutes at the start of Wave 1.

---

## Findings

### FIND-001 -- Medium: ET-M-001 reasoning_effort Not Specified

**Standard:** ET-M-001 (agent-development-standards.md) -- Agent definitions SHOULD declare `reasoning_effort` aligned with criticality level. C3 deliverables map to `high`.

**Evidence:** The governance YAML specifications for both uc-author (F-03) and uc-slicer (F-05) do not include a `reasoning_effort` field. Both agents are classified as C3 (File Responsibility Matrix). Architecture document does not mention reasoning_effort.

**Impact:** Without explicit `reasoning_effort: high`, both agents default to the model baseline (no extended thinking allocation). For uc-author's integrative synthesis and uc-slicer's cross-field semantic validation, `high` reasoning effort reduces the risk of shallow integration or missed INVEST criteria. This is a SHOULD standard -- deviation is permissible with justification but the omission is unintentional.

**Recommendation:** Add `reasoning_effort: high` to both `.governance.yaml` specifications. The field is not part of the `agent-governance-v1.schema.json` required set and `additionalProperties: true` means it is schema-safe to add. Location: top-level field in governance YAML alongside `version` and `tool_tier`.

**Action:** eng-backend to add `reasoning_effort: high` to F-03 and F-05 during authoring.

---

### FIND-002 -- Medium: output_filtering Entry Categorization

**Standard:** AD-M-008 (agent-development-standards.md Guardrails Template) -- `output_filtering` entries should be output safety filters. `guardrails.input_validation` should contain prerequisite validation rules.

**Evidence:** uc-author's `output_filtering` array contains `all_flow_steps_must_have_typed_classification`. This is a check that every `flow_step` object has the `type` field populated. Structurally this is an output correctness rule (verifying the produced artifact). However, the JSON Schema already enforces `type` as required in `flow_step` via `required: [step, actor, action, type]`. The agent-level check is therefore a redundant semantic guard against the agent's own output -- appropriate as either an output filter or a post-completion check.

**Analysis:** The entry is not misplaced -- output_filtering is the correct location for "verify before finalizing" rules. The concern is that this is more precisely a structural completeness assertion than a "safety filter." The existing pattern in ps-analyst.governance.yaml (`conclusions_require_evidence`, `recommendations_require_rationale`) represents output quality enforcement, which is analogous. The architecture entry is consistent with precedent.

**Recommendation:** No change required. This is an advisory observation, not a blocking defect. The categorization is defensible per existing pattern. Document the intent as "output structural completeness" rather than "data safety" if clarity is desired.

---

### FIND-003 -- Low: H-26 Registration Actions Not in Worktracker

**Standard:** H-26(c) -- New skills MUST be registered in CLAUDE.md, AGENTS.md, and mandatory-skill-usage.md. H-32 -- GitHub Issue parity required for Jerry repo work items.

**Evidence:** The three registration actions (CLAUDE.md, AGENTS.md, mandatory-skill-usage.md) are correctly identified in the architecture's File Responsibility Matrix as eng-lead tasks at sub-step 10a. However, there is no worktracker entity tracking these registration actions. Until F-01 (SKILL.md) is complete and approved, the registration cannot be executed, but the tracking should exist.

**Impact:** Risk of registration being overlooked at handoff or session boundary. The registration gap would leave the skill inaccessible via keyword routing (H-22 violation) and undiscoverable in AGENTS.md.

**Recommendation:** Eng-lead to create a worktracker task tracking the three registration actions as acceptance criteria for the `/use-case` skill implementation story. Registration is the last eng-lead action before eng-reviewer closes out the implementation.

---

### FIND-004 -- Low: F-07 / F-09 Prompt Files Require Synchronization Protocol

**Standard:** P-001 (truth and accuracy) -- artifact content must be accurate and consistent.

**Evidence:** The composition files F-07 (`uc-author.prompt.md`) and F-09 (`uc-slicer.prompt.md`) are described as "a copy of the markdown body from the agent `.md` file." This means F-07 is a copy of the F-02 body and F-09 is a copy of the F-04 body. There is no mechanism specified to keep these synchronized when the agent definitions are updated.

**Impact:** If F-02 or F-04 are updated post-implementation, the composition prompt files could become stale, causing Task-invoked agents to use outdated methodology or guardrails.

**Recommendation:** Add a note to the composition files and BEHAVIOR_TESTS.md documenting the synchronization requirement: "This file is a manually-maintained copy of `skills/use-case/agents/uc-author.md` markdown body. When updating uc-author.md, this file MUST be updated in the same commit." A CI check (eng-devsecops scope) that validates content parity would eliminate the manual risk.

---

### FIND-005 -- Low: interactions Block Speculative Status in Production Schema

**Standard:** P-022 (no deception) -- limitations must be disclosed.

**Evidence:** The `shared-schema.json` (which becomes F-17, the production schema) includes the `interactions` block with `$comment` fields explicitly marking it "ARCHITECTURALLY SPECULATIVE: Phase 3 validation gate required before production adoption." This speculative marking will persist in the production schema at `docs/schemas/use-case-realization-v1.schema.json`.

**Assessment:** This is a known and accepted situation, carried forward from Phase 2 with full disclosure in the architecture document. The architecture's L2: Strategic Implications section and the `interactions` block schema description both disclose the speculative status. P-022 compliance is maintained. This finding is informational only -- the speculative status does not block F-17 creation or `/use-case` skill implementation.

**Recommendation:** The `$comment` markers in F-17 are correct disclosure. No action required for Phase 3 `/use-case` implementation. The validation gate (3 representative use cases in 2+ domains) is a Phase 4 concern tracked separately.

---

## L2: Strategic Implications

### Precedent-Setting Decisions

**1. File-Mediated Handoff as Architectural Default**

The `/use-case` skill establishes `file-mediated handoff via shared schema` as the canonical cross-agent communication pattern for the three-skill pipeline. This has positive maintainability implications: the shared artifact file is the sole trust boundary, and each consuming skill validates independently against the schema. The eng-lead recommendation is to document this pattern formally as `PAT-FILE-HANDOFF-001` in `.context/patterns/` once the three-skill pipeline is complete, so it can be referenced by future skill designs that need cross-skill data exchange.

**2. Two-Layer Validation as Standard Pattern**

The JSON Schema structural gate (Layer 1) + agent guardrail semantic gate (Layer 2) is a defensible pattern for all skills that produce structured artifacts. Layer 1 provides deterministic CI-level enforcement; Layer 2 handles semantic constraints that are impractical in JSON Schema (content-to-field consistency, cross-array references). When eng-backend is implementing this for `/use-case`, this pattern will become the de-facto standard that `/test-spec` and `/contract-design` will inherit. The test strategy for eng-qa (F-16, BDD scenarios 6 and 7) should explicitly verify both layers independently, not just the end-to-end result.

**3. Progressive Loading of Rules File (CB-05 Application)**

The architecture specifies that F-14 (use-case-writing-rules.md) should be loaded progressively using Read offset/limit aligned to the current detail level (steps 1-4 for BRIEFLY_DESCRIBED, steps 1-10 for ESSENTIAL_OUTLINE, full for FULLY_DESCRIBED). This is the first rules file in the framework to implement CB-05 progressive loading within a single invocation context. If this pattern proves effective at reducing context consumption without degrading agent quality, it should be documented as a rules-file design pattern and recommended for long rules files in other skills.

### Technical Debt Assessment

**Risk: Composition File Synchronization (FIND-004)**

The manual copy pattern for F-07/F-09 is the most significant technical debt introduced by this implementation. At low agent count (2 agents, 2 composition files) the cost is manageable. If `/test-spec` and `/contract-design` follow the same pattern, the framework will have 6+ agent-definition/composition pairs that must be manually kept in sync. The CI parity check recommended in FIND-004 is low cost and should be prioritized to prevent accumulation.

**Risk: Interactions Block Debt (FIND-005)**

The speculative interactions block (`ARCHITECTURALLY SPECULATIVE` markers in schema) represents acceptance of temporary technical debt in the production schema. The schema is designed for forward compatibility (`additionalProperties: true`), but the block's semantic validity is unverified until the Phase 3 validation gate runs. If the gate reveals the block is structurally insufficient for `/contract-design`'s OpenAPI generation, a schema minor version bump (1.0.0 to 1.1.0) will be required that cascades to all existing use case artifacts -- the number of affected artifacts will depend on how many are created before the gate executes.

**Long-Term Maintainability**

The 16-file skill structure is proportional to 2 agents and the Cockburn/Jacobson methodology depth. Future capability expansion (e.g., adding UC 3.0 support, adding a third agent for stakeholder-goal elicitation) will not require structural changes to the skill -- new files follow the established F-01 through F-17 pattern. The SKILL.md body uses the skill-standards.md 14-section structure which is stable. The schema versioning strategy (SemVer, `additionalProperties: true` for forward compatibility) provides a clear path for schema evolution without breaking existing consumers.

### SAMM Maturity Assessment (Relevant Practices)

| Practice | Current Maturity | Target (Post-Implementation) |
|----------|-----------------|------------------------------|
| Security Requirements (SSDF PO.1) | L1 -- requirements derived from threat model (STRIDE in architecture Section L2) | L1 maintained -- no new security capability required |
| Secure Design (SSDF PO.3) | L2 -- two-layer validation gate, T2 minimum privilege, JSON Schema contract | L2 maintained |
| Secure Build (SSDF PS.1) | L1 -- CI L5 schema validation gate for USE_CASE artifacts | L2 target -- add composition file parity check (FIND-004) |
| Code Integrity (SSDF PS.2) | L1 -- git tracks all artifact changes | L1 maintained |

---

## Self-Review Checklist (H-15 / S-010)

### Constitutional Compliance

- [x] **P-001 (Truth/Accuracy):** Every finding cites the specific standard ID and quotes the relevant specification evidence. Compliance determinations trace to documented fields and file locations.
- [x] **P-002 (File Persistence):** Review persisted to `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/implementation/step-9-eng-lead-review.md`.
- [x] **P-003 (No Recursive Subagents):** This is a read-and-write review document. No subagent delegation performed.
- [x] **P-022 (No Deception):** Limitations disclosed: the PENDING registration items are correctly labeled as future tasks, not defects. The ET-M-001 gap is a SHOULD standard deviation, not a HARD rule violation. Confidence levels appropriate.

### Structural Compliance

- [x] **H-23 (Navigation):** Navigation table present at document top. All `##` sections covered with anchor links.
- [x] **H-15 (Self-Review):** This section is the S-010 application.
- [x] **P-002 (Output levels):** L0 (executive summary), L1 (compliance matrix + implementation plan), L2 (strategic implications) all present.

### Standards Coverage Completeness

- [x] H-34 verified (14 sub-requirements checked)
- [x] H-25 verified (4 sub-requirements checked)
- [x] H-26 verified (8 sub-requirements checked, 3 PENDING implementation tasks identified)
- [x] H-23 verified (3 sub-requirements checked)
- [x] Tool tier verified (T2 appropriateness, Task exclusion, tool count)
- [x] AD-M-001 through AD-M-009 and ET-M-001 verified (10 standards checked)
- [x] Dependency governance verified (7 dependencies traced)
- [x] Implementation plan with dependency ordering, critical path, and wave structure produced
- [x] 5 findings produced with severity levels and actionable recommendations

### Adversarial Challenge (S-002: Devil's Advocate Applied)

**Challenge 1: "Is the PASS/FAIL analysis for H-34 valid, given that the governance YAML was not schema-validated against `agent-governance-v1.schema.json` at the code level?"**

The review verified the specified fields against the schema requirements by inspecting both the schema file (confirmed at `docs/schemas/agent-governance-v1.schema.json`) and the architecture's governance YAML specifications. The `required` array in the schema is `["version", "tool_tier", "identity"]` -- all three present in both specs. The `guardrails` sub-schema requires only `fallback_behavior` -- present in both. The `capabilities.forbidden_actions` minimum 3 entries are present with P-003/P-020/P-022 references. The PASS determinations are based on field-by-field comparison against the schema source, which is deterministic. Runtime schema validation (L3/L5) will be the authoritative check when the actual YAML files are authored.

**Challenge 2: "Should FIND-001 (ET-M-001) be elevated to a blocker given that C3 agents without reasoning_effort may produce lower-quality outputs that fail the quality gate?"**

ET-M-001 is a SHOULD standard (AD-M-009 complement), not a HARD rule. The quality gate consequence operates at the output level -- if uc-author produces use case artifacts that score below 0.92 (C2+ threshold), the revision cycle per H-14 catches it regardless of reasoning_effort setting. The `reasoning_effort` field influences how deeply the agent reasons internally, but it does not determine whether the output passes quality review. The recommended `high` setting reduces the risk of shallow synthesis but does not constitute a block. Medium priority is the correct severity.

**Challenge 3: "Is the critical path analysis correct, or does F-14 (use-case-writing-rules.md) belong on the critical path?"**

F-14 is referenced by both agent system prompts (F-02 and F-04) as a load-on-demand reference for the rules governing the methodology. Agent definitions that reference F-14 by path still function without F-14 present -- the agents would operate from their embedded methodology outlines in the `<methodology>` section and only load F-14 when needed. F-14 is therefore a dependency for correct full-detail operation, not a structural dependency for agent definition validity. Off-critical-path classification is correct.

---

*Standards Enforcement Review Version: 1.0.0*
*Input: step-9-use-case-architecture.md v1.2.0 (PASSED 0.956 / threshold 0.95)*
*Standards Verified: H-34, H-35 (sub-item), H-25, H-26, H-23, H-22, ET-M-001, AD-M-001..AD-M-009, tool tiers T1-T5, P-003 topology, dependency governance*
*Findings: 5 total (0 blocking, 2 medium, 3 low)*
*Implementation Plan: 17 files, 5+1 waves, critical path identified*
*Next Agent: eng-backend (Wave 1 can begin immediately)*
*Workflow ID: use-case-skills-20260308-001*
*Date: 2026-03-09*
