# Skill Architecture Design: /use-case

> **PS ID:** proj-021 | **Entry ID:** step-9-use-case-architecture | **Workflow ID:** use-case-skills-20260308-001
> **Date:** 2026-03-08 | **Agent:** eng-architect | **Step:** 9 (Phase 3 Implementation)
> **Quality Threshold:** >= 0.95 (C4)
> **Status:** PROPOSED (P-020: user approval required before ACCEPTED)
> **Version:** 1.0.0
> **Lineage:** file-organization.md (v2.1.0, 0.951 PASS), agent-decomposition.md (v1.1.0, 0.963 PASS), frontmatter-schema.md (v1.0.0, 0.955 PASS), shared-schema.json (v1.0.0), phase-1-synthesis.md (v1.0.0, 0.956 PASS)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What to build, why, and key decisions in plain language |
| [L1: Technical Specification](#l1-technical-specification) | Implementation-ready specifications for every file |
| [1. File Manifest](#1-file-manifest) | Complete list of files to create with absolute paths |
| [2. SKILL.md Design](#2-skillmd-design) | Routing, agent table, when-to-use, integration points |
| [3. Agent Definition Specifications](#3-agent-definition-specifications) | Per-agent .md frontmatter, .governance.yaml, system prompt outline |
| [4. Template Design](#4-template-design) | Template purpose, format, placeholders, skeletons |
| [5. Shared Schema Integration](#5-shared-schema-integration) | Runtime validation, two-layer gate, error handling |
| [6. Intra-Skill Interaction Model](#6-intra-skill-interaction-model) | uc-author to uc-slicer handoff, orchestration, progressive realization |
| [7. Risk Register](#7-risk-register) | Implementation risks carried forward and new |
| [L2: Strategic Implications](#l2-strategic-implications) | Long-term evolution, cross-skill integration, security posture |
| [GATE-2 Issue Resolution](#gate-2-issue-resolution) | Disposition of Phase 2 quality gate flagged items |
| [Self-Review Checklist](#self-review-checklist) | H-15 / S-010 verification |

---

## L0: Executive Summary

This document translates the Phase 2 architecture (3 documents, 1 JSON Schema, all scoring >= 0.95) into an implementation-ready specification for the `/use-case` Jerry skill. The skill provides guided use case authoring following Cockburn's 12-step writing process and Jacobson's UC 2.0 methodology.

**What gets built.** 16 files organized under `skills/use-case/`. Two agents: `uc-author` (creates and elaborates use case artifacts through progressive detail levels) and `uc-slicer` (decomposes use cases into implementation-ready slices and produces the realization interaction sequence). Four templates provide the output formats. One rule file encodes Cockburn's 12-step process. One skill contract, one behavior test file, and the SKILL.md entry point complete the skill.

**Key architectural decisions.**

1. **2 agents, not 4.** The ORCHESTRATION.yaml lists 4 agents (uc-author, uc-slicer, tspec-generator, cd-generator). The architecture (SSOT) defines 2 agents for `/use-case`. The other 2 belong to `/test-spec` and `/contract-design` respectively. This document covers only the 2 `/use-case` agents.

2. **File-mediated handoff.** Agents communicate exclusively through the use case artifact file on disk, validated against `shared-schema.json` at every boundary. No direct agent-to-agent communication. P-003 compliant (main context orchestrates both workers).

3. **Two-layer validation.** Layer 1: JSON Schema structural validation (field presence, types, enums, patterns). Layer 2: Agent guardrail semantic validation (detail level prerequisites, cross-field referential integrity, procedural constraints). Neither layer alone is sufficient; both are required.

**GATE-2 issue dispositions.** Three items flagged during Phase 2 quality review are addressed: (a) tspec-generator `$.slice_state >= ANALYZED` guardrail -- noted as `/test-spec` scope, not implemented here; (b) DI-05 cross-citation at uc-author guardrail -- confirmed incorrect, corrected to DI-01; (c) uc-slicer explicit `$.realization_level` setting -- incorporated as a mandatory guardrail.

---

## L1: Technical Specification

### 1. File Manifest

16 files to create, organized by directory. All paths are relative to repository root.

#### Directory Tree

```
skills/use-case/
+-- SKILL.md                                    # [F-01] Skill entry point (H-25)
+-- agents/
|   +-- uc-author.md                            # [F-02] Agent definition: use case authoring
|   +-- uc-author.governance.yaml               # [F-03] Governance metadata (H-34)
|   +-- uc-slicer.md                            # [F-04] Agent definition: use case slicing
|   +-- uc-slicer.governance.yaml               # [F-05] Governance metadata (H-34)
+-- composition/
|   +-- uc-author.agent.yaml                    # [F-06] Task tool invocation config
|   +-- uc-author.prompt.md                     # [F-07] System prompt for Task invocation
|   +-- uc-slicer.agent.yaml                    # [F-08] Task tool invocation config
|   +-- uc-slicer.prompt.md                     # [F-09] System prompt for Task invocation
+-- templates/
|   +-- use-case-realization.template.md        # [F-10] Full realization template (R-01)
|   +-- use-case-brief.template.md              # [F-11] Brief format (Cockburn)
|   +-- use-case-casual.template.md             # [F-12] Casual format (Cockburn)
|   +-- use-case-slice.template.md              # [F-13] Slice document template (UC 2.0)
+-- rules/
|   +-- use-case-writing-rules.md               # [F-14] Cockburn 12-step as agent rules
+-- contracts/
|   +-- UC_SKILL_CONTRACT.yaml                  # [F-15] Skill contract
+-- tests/
    +-- BEHAVIOR_TESTS.md                       # [F-16] BDD behavior tests
```

Additionally, one file is copied from design-phase artifact to production location:

```
docs/schemas/use-case-realization-v1.schema.json  # [F-17] Production schema (from shared-schema.json)
```

#### ORCHESTRATION.yaml Reconciliation

The ORCHESTRATION.yaml deliverable list references 4 agents across 3 skills. The Phase 2 architecture (SSOT) defines:

| Agent | Skill | In This Document? | Rationale |
|-------|-------|--------------------|-----------|
| `uc-author` | `/use-case` | **YES** | Activities 1-3 (authoring) |
| `uc-slicer` | `/use-case` | **YES** | Activities 2+4+5 (slicing, realization) |
| `tspec-generator` | `/test-spec` | No -- separate skill implementation | Clark transformation |
| `cd-generator` | `/contract-design` | No -- separate skill implementation | UC-to-contract transformation |

This document covers the 2 `/use-case` agents only. The `/test-spec` and `/contract-design` skills require their own architecture documents per their respective implementation steps.

#### File Responsibility Matrix

| File ID | Primary Author (Sub-Step) | Reviewer | Criticality |
|---------|--------------------------|----------|-------------|
| F-01 | eng-lead (10a) | eng-reviewer | C3 |
| F-02, F-03 | eng-backend (10b) | eng-security, eng-reviewer | C3 |
| F-04, F-05 | eng-backend (10b) | eng-security, eng-reviewer | C3 |
| F-06, F-07 | eng-backend (10c) | eng-reviewer | C2 |
| F-08, F-09 | eng-backend (10c) | eng-reviewer | C2 |
| F-10..F-13 | eng-backend (10d) | eng-reviewer | C2 |
| F-14 | eng-backend (10e) | eng-reviewer | C2 |
| F-15 | eng-lead (10a) | eng-reviewer | C2 |
| F-16 | eng-qa (10f) | eng-reviewer | C3 |
| F-17 | eng-infra (10g) | eng-reviewer | C2 |

---

### 2. SKILL.md Design

#### Frontmatter (F-01)

```yaml
---
name: use-case
description: >-
  Guided use case authoring and slicing using Cockburn 12-step writing process
  and Jacobson UC 2.0 methodology. Creates structured use case artifacts with
  progressive detail levels (Briefly Described through Fully Described),
  decomposes into implementation-ready slices with INVEST criteria, and produces
  realization interaction sequences for downstream /test-spec and
  /contract-design consumption. Invoke when writing, creating, authoring,
  elaborating, slicing, or decomposing use cases.
version: "1.0.0"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
activation-keywords:
  - "use case"
  - "use-case"
  - "write use case"
  - "create use case"
  - "author use case"
  - "use case model"
  - "actor goal list"
  - "basic flow"
  - "main success scenario"
  - "alternative flow"
  - "extension handling"
  - "fully dressed"
  - "casual use case"
  - "briefly described"
  - "sea level goal"
  - "goal level"
  - "use case slice"
  - "slice use case"
  - "UC 2.0"
  - "cockburn"
  - "jacobson"
---
```

#### Routing Keywords (Trigger Map Entry -- Priority 13)

Per agent-decomposition.md Trigger Map Extensions section:

| Column | Value |
|--------|-------|
| **Detected Keywords** | use case, use-case, write use case, create use case, author use case, use case model, actor goal list, basic flow, main success scenario, alternative flow, extension, extension handling, fully dressed, casual use case, briefly described, sea level goal, goal level, use case slice, slice use case, UC 2.0, cockburn, jacobson |
| **Negative Keywords** | requirements specification, V&V, technical review, trade study, compliance, test spec, BDD, Gherkin, scenario, OpenAPI, contract, API design, schema, adversarial, tournament, transcript, penetration, exploit, code review, documentation, tutorial |
| **Priority** | 13 |
| **Compound Triggers** | "write use case" OR "create use case" OR "author use case" OR "use case model" OR "actor goal" OR "basic flow" OR "main success scenario" OR "use case slice" (phrase match) |
| **Skill** | `/use-case` |

#### Agent Routing Table

| Agent | Role | Model | Cognitive Mode | Tool Tier | Decision Signal |
|-------|------|-------|---------------|-----------|-----------------|
| `uc-author` | Creates and elaborates use case artifacts (Activities 1-3) | sonnet | integrative | T2 | "write", "create", "author", "elaborate", "expand", "describe", "draft", "refine" |
| `uc-slicer` | Decomposes use cases into slices and produces realization (Activities 2+4+5) | sonnet | systematic | T2 | "slice", "decompose", "break down", "split into stories", "prepare slice", "analyze slice", "realize" |

**Default routing:** When intent is ambiguous or combines authoring + slicing, route to `uc-author` first, then `uc-slicer`. Authoring precedes slicing in the pipeline.

**"Refine" disambiguation:** "refine" defaults to `uc-author`. Switch to `uc-slicer` only if user clarifies decomposition intent (e.g., "refine the slicing" vs. "refine the use case").

#### When to Use

**Activate when:**

- Writing a new use case from stakeholder descriptions or system capabilities
- Elaborating an existing use case to a deeper detail level (Briefly Described to Fully Described)
- Building an actor-goal list for a system scope
- Decomposing a use case into implementation-ready slices
- Advancing slices through the UC 2.0 lifecycle (Scoped, Prepared, Analyzed)
- Producing the realization interaction sequence for downstream `/test-spec` or `/contract-design`

**NEVER invoke this skill when:**

- Task is writing requirements specifications or V&V documents -- Consequence: Use case methodology applied to requirements produces artifacts that do not satisfy requirements traceability standards; use `/nasa-se` instead.
- Task is generating BDD test scenarios from existing use cases -- Consequence: `/use-case` agents do not implement Clark's transformation algorithm; generated test specs will lack proper Gherkin structure; use `/test-spec` instead.
- Task is generating API contracts from use case artifacts -- Consequence: `/use-case` agents do not implement the UC-to-contract transformation; use `/contract-design` instead.
- Task is routine code review or security analysis -- Consequence: Use case methodology is inapplicable to code artifacts; use `/eng-team` or `/problem-solving` instead.
- User explicitly asks for a quick user story without methodology rigor -- Consequence: Full 12-step Cockburn process applied to a simple user story wastes context budget; create the story directly without skill invocation.

#### Integration Points

| Integration | Direction | Mechanism | Pre-Condition |
|-------------|-----------|-----------|---------------|
| `/use-case` to `/test-spec` | Output of uc-author/uc-slicer consumed by tspec-generator | Shared artifact file validated against `use-case-realization-v1.schema.json` | `$.detail_level` >= `ESSENTIAL_OUTLINE`, `$.extensions` non-empty |
| `/use-case` to `/contract-design` | Output of uc-slicer consumed by cd-generator | Shared artifact file with `$.interactions[*]` populated | `$.realization_level` = `INTERACTION_DEFINED`, `$.interactions` minItems: 1 |
| `/use-case` to `/worktracker` | uc-slicer creates Story entities for each slice | Worktracker entity creation via `/worktracker` skill invocation | `$.slices[*]` with `$.slice_state` >= `SCOPED` |
| `/use-case` to `/ast` | Frontmatter extraction and validation via AST (H-33) | `jerry ast frontmatter` and `jerry ast validate` CLI commands | `$.work_type` = `USE_CASE` discriminator |

---

### 3. Agent Definition Specifications

#### 3.1 Agent: uc-author

##### Official Frontmatter (F-02: `uc-author.md`)

```yaml
---
name: uc-author
description: >-
  Use Case Author agent. Creates and elaborates use case artifacts using
  Cockburn's 12-step writing process and Jacobson UC 2.0 progressive narrative
  levels. Produces structured YAML frontmatter validated against
  use-case-realization-v1.schema.json. Invoke when writing, creating, authoring,
  elaborating, expanding, describing, drafting, or refining use cases.
model: sonnet
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---
```

##### Governance YAML (F-03: `uc-author.governance.yaml`)

```yaml
version: "1.0.0"
tool_tier: "T2"

identity:
  role: "Use Case Author -- creates and elaborates use case artifacts using Cockburn's 12-step writing process and Jacobson's UC 2.0 progressive narrative levels"
  expertise:
    - "Cockburn use case writing methodology (12-step process, goal levels, precision levels, template formats Brief/Casual/Fully-Dressed)"
    - "Jacobson UC 2.0 narrative levels (Briefly Described, Bulleted Outline, Essential Outline, Fully Described) and use-case modeling (actors, goals, use-case model)"
    - "Stakeholder elicitation and goal decomposition using Cockburn's sea-metaphor classification (Cloud/Kite/Sea Level/Fish/Clam)"
  cognitive_mode: "integrative"

persona:
  tone: "methodical"
  communication_style: "structured"
  audience_level: "adaptive"

capabilities:
  forbidden_actions:
    - "P-003 VIOLATION: NEVER spawn recursive subagents or delegate to other agents via Task tool -- Consequence: agent hierarchy violation breaks orchestrator-worker topology and causes uncontrolled token consumption. uc-author is a T2 worker agent without Task tool access."
    - "P-020 VIOLATION: NEVER override user decisions about use case scope, detail level, or actor classification -- Consequence: unauthorized scope changes erode trust and may invalidate downstream artifacts that depend on user-approved use case boundaries."
    - "P-022 VIOLATION: NEVER misrepresent the completeness or detail level of a use case artifact -- Consequence: setting $.detail_level to FULLY_DESCRIBED when extensions are incomplete causes downstream /test-spec and /contract-design to process insufficient input, producing invalid outputs."
    - "SCHEMA VIOLATION: NEVER produce use case artifacts that fail validation against use-case-realization-v1.schema.json -- Consequence: invalid artifacts break the CI validation pipeline (L5) and cause downstream agent rejection."
    - "METHODOLOGY VIOLATION: NEVER skip Cockburn steps 1-4 (scope, actors, goals, brief) and jump directly to Main Success Scenario writing -- Consequence: depth-first authoring without breadth-first foundation produces use cases with missed actors, incorrect goal levels, and incomplete stakeholder coverage."
  forbidden_action_format: "NPT-009-complete"
  output_formats:
    - "markdown"
    - "yaml"

guardrails:
  input_validation:
    - "User request must describe a system capability, actor goal, or reference an existing use case to elaborate"
    - "If elaborating existing artifact: file must exist and contain valid YAML frontmatter with $.work_type = USE_CASE"
  output_filtering:
    - "no_secrets_in_output"
    - "all_flow_steps_must_have_typed_classification"
    - "detail_level_must_match_actual_content_depth"
    - "goal_symbol_must_be_consistent_with_goal_level"
    - "status_must_remain_DRAFT_until_human_review"
  fallback_behavior: "escalate_to_user"

output:
  required: true
  location: "projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md"
  template: "skills/use-case/templates/use-case-realization.template.md"
  levels:
    - "L0"
    - "L1"

constitution:
  reference: "docs/governance/JERRY_CONSTITUTION.md"
  principles_applied:
    - "P-003"
    - "P-020"
    - "P-022"
    - "P-001"
    - "P-002"
    - "P-004"

validation:
  post_completion_checks:
    - "verify_file_created_at_output_location"
    - "verify_yaml_frontmatter_validates_against_schema"
    - "verify_basic_flow_has_3_to_9_steps"
    - "verify_goal_level_is_set"
    - "verify_detail_level_matches_content"
    - "verify_all_flow_steps_have_type_field"

session_context:
  on_receive:
    - "Load project context and existing use case artifacts"
    - "Determine if creating new or elaborating existing"
    - "Identify target detail level from user request"
  on_send:
    - "Report artifact path and detail level achieved"
    - "List key findings: actor count, goal level, basic flow step count, extension count"
    - "Flag if detail level is insufficient for downstream /test-spec consumption"

enforcement:
  tier: "medium"
  escalation_path: "eng-reviewer"
```

##### System Prompt Outline (F-02 markdown body)

The markdown body of `uc-author.md` MUST include these XML-tagged sections per `agent-development-standards.md`:

| Section Tag | Content Summary |
|-------------|----------------|
| `<identity>` | Use Case Author role. Integrative cognitive mode. Combines stakeholder inputs, domain knowledge, and Cockburn structure into unified use case artifacts. Distinction from uc-slicer: authoring (Activities 1-3) vs. slicing (Activities 2+4+5). |
| `<purpose>` | Produces structured use case artifacts following Cockburn's 12-step writing process at Jacobson UC 2.0 progressive detail levels. Enables downstream `/test-spec` and `/contract-design` consumption via validated shared artifact format. |
| `<input>` | User request describing a system capability or actor goal. Optionally: existing use case artifact path for elaboration, project context files, actor-goal list, system boundary description. |
| `<capabilities>` | Reads project context and existing artifacts. Writes use case artifact files with YAML frontmatter and Markdown narrative body. Validates output against shared schema. No external research, no cross-session state, no delegation. |
| `<methodology>` | Cockburn 12-step writing process (full table from agent-decomposition.md lines 95-108). Progressive detail levels (4 modes from agent-decomposition.md lines 112-117). Default: Level 2 (Bulleted Outline). Reference: `skills/use-case/rules/use-case-writing-rules.md` for operational rules. |
| `<output>` | Use case artifact file at `projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md`. YAML frontmatter validates against `docs/schemas/use-case-realization-v1.schema.json`. Template: `skills/use-case/templates/use-case-realization.template.md` (primary) or brief/casual templates for early-stage artifacts. |
| `<guardrails>` | Constitutional triplet (P-003, P-020, P-022). Domain guardrails: goal level classification mandatory (DI-02), 3-9 MSS steps (Cockburn Guideline 6), breadth-first authoring (PAT-001), detail_level must match content (DI-01), status remains DRAFT until human review (CF-03), extensions required before FULLY_DESCRIBED (S-02, DI-01 -- corrected from DI-05 per GATE-2 note 2). Schema validation on all output. |

##### GATE-2 Note 2 Resolution: DI-05 Cross-Citation

The uc-author guardrail "MUST NOT advance to Fully Described without complete extension conditions" was cited as "S-02, DI-05" in agent-decomposition.md line 136. DI-05 is defined as "Clark transformation" (tspec-generator's domain). The correct citation is **DI-01** ("4 narrative detail levels as discrete output modes") and **S-02** (Cockburn writing process). The corrected guardrail source in this architecture document is: `S-02, DI-01`.

---

#### 3.2 Agent: uc-slicer

##### Official Frontmatter (F-04: `uc-slicer.md`)

```yaml
---
name: uc-slicer
description: >-
  Use Case Slicer agent. Decomposes use cases into implementation-ready slices
  following Jacobson UC 2.0 Activity 2 (Slice the Use Cases), Activity 4
  (Prepare a Use-Case Slice), and Activity 5 (Analyze a Use-Case Slice). Manages
  the five-state slice lifecycle (Scoped through Verified) and produces the
  realization interaction sequence consumed by /contract-design. Invoke when
  slicing, decomposing, breaking down, preparing, analyzing, or realizing use
  case slices.
model: sonnet
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---
```

##### Governance YAML (F-05: `uc-slicer.governance.yaml`)

```yaml
version: "1.0.0"
tool_tier: "T2"

identity:
  role: "Use Case Slicer -- decomposes use cases into implementation-ready slices following Jacobson UC 2.0 Activities 2, 4, and 5"
  expertise:
    - "Jacobson UC 2.0 slicing patterns (end-to-end slice selection, INVEST criteria application, slice state lifecycle management)"
    - "Use case slice lifecycle management (Scoped > Prepared > Analyzed > Implemented > Verified) with worktracker integration"
    - "Use case realization: Activity 5 system element identification, responsibility allocation, and interaction sequence production"
  cognitive_mode: "systematic"

persona:
  tone: "methodical"
  communication_style: "structured"
  audience_level: "adaptive"

capabilities:
  forbidden_actions:
    - "P-003 VIOLATION: NEVER spawn recursive subagents or delegate to other agents via Task tool -- Consequence: agent hierarchy violation breaks orchestrator-worker topology and causes uncontrolled token consumption. uc-slicer is a T2 worker agent without Task tool access."
    - "P-020 VIOLATION: NEVER override user decisions about slice boundaries, priority ordering, or lifecycle state transitions -- Consequence: unauthorized slice modifications invalidate implementation planning that depends on user-approved decomposition."
    - "P-022 VIOLATION: NEVER misrepresent slice lifecycle state or INVEST assessment results -- Consequence: setting $.slice_state to PREPARED when test cases are absent causes downstream implementers to begin work on slices that lack acceptance criteria, producing untestable software."
    - "SCHEMA VIOLATION: NEVER produce artifacts that fail validation against use-case-realization-v1.schema.json allOf constraints -- Consequence: setting $.realization_level to INTERACTION_DEFINED without populating $.interactions[*] violates allOf constraint 1 and breaks /contract-design input validation."
    - "LIFECYCLE VIOLATION: NEVER skip the SCOPED state and create slices directly at PREPARED or ANALYZED -- Consequence: skipping INVEST criteria verification produces slices that are not independent, not valuable, or not testable, degrading implementation quality."
    - "REALIZATION VIOLATION: NEVER set $.realization_level without verifying that the corresponding blocks are populated -- Consequence: realization_level is a derived summary field; setting it without populating the actual blocks produces an internally inconsistent artifact that passes schema structural validation but fails semantic checks."
  forbidden_action_format: "NPT-009-complete"
  output_formats:
    - "markdown"
    - "yaml"

guardrails:
  input_validation:
    - "Input artifact must exist and contain valid YAML frontmatter with $.work_type = USE_CASE"
    - "Input artifact $.detail_level must be >= ESSENTIAL_OUTLINE (reject BRIEFLY_DESCRIBED and BULLETED_OUTLINE)"
    - "Input artifact must have $.basic_flow with 3-9 steps"
  output_filtering:
    - "no_secrets_in_output"
    - "all_slices_must_have_steps_included"
    - "basic_flow_must_be_first_slice"
    - "realization_level_must_match_populated_blocks"
    - "slice_state_must_be_explicitly_set_on_every_transition"
  fallback_behavior: "escalate_to_user"

output:
  required: true
  location: "projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md"
  template: "skills/use-case/templates/use-case-slice.template.md"
  levels:
    - "L0"
    - "L1"

constitution:
  reference: "docs/governance/JERRY_CONSTITUTION.md"
  principles_applied:
    - "P-003"
    - "P-020"
    - "P-022"
    - "P-001"
    - "P-002"
    - "P-004"

validation:
  post_completion_checks:
    - "verify_artifact_validates_against_schema_including_allOf"
    - "verify_basic_flow_is_first_slice"
    - "verify_each_slice_has_invest_assessment"
    - "verify_test_cases_present_when_slice_state_gte_PREPARED"
    - "verify_interactions_present_when_realization_level_INTERACTION_DEFINED"
    - "verify_realization_level_is_explicitly_set"
    - "verify_slice_state_is_explicitly_set"

session_context:
  on_receive:
    - "Load target use case artifact and validate frontmatter"
    - "Determine current detail level and realization level"
    - "Identify which Activity (2, 4, or 5) to perform based on current state"
  on_send:
    - "Report artifact path, slice count, and realization level achieved"
    - "List key findings: slice IDs, INVEST pass/fail summary, interaction count"
    - "Flag if realization level is sufficient for downstream /contract-design consumption"

enforcement:
  tier: "medium"
  escalation_path: "eng-reviewer"
```

##### System Prompt Outline (F-04 markdown body)

| Section Tag | Content Summary |
|-------------|----------------|
| `<identity>` | Use Case Slicer role. Systematic cognitive mode. Applies step-by-step slicing procedures following Jacobson UC 2.0. Distinction from uc-author: slicing/realization (Activities 2+4+5) vs. authoring (Activities 1-3). |
| `<purpose>` | Decomposes use case artifacts into implementation-ready slices. Manages the five-state lifecycle. Produces the realization interaction sequence that enables `/contract-design` consumption. |
| `<input>` | Use case artifact at `$.detail_level` >= `ESSENTIAL_OUTLINE`. Must have `$.basic_flow[*]` and `$.extensions[*]` at minimum. Optionally: existing `$.slices[*]` for iterative refinement. |
| `<capabilities>` | Reads use case artifacts. Writes slice definitions and interactions back into the artifact YAML frontmatter. Creates worktracker Story entities for each slice. Validates output against shared schema including allOf constraints. |
| `<methodology>` | 8-step methodology (full table from agent-decomposition.md lines 167-176). Slice state machine (5 states from agent-decomposition.md lines 180-186). INVEST criteria verification. Activity 5 realization producing `$.interactions[*]`. Reference: `skills/use-case/rules/use-case-writing-rules.md` for lifecycle rules. |
| `<output>` | Updated use case artifact at same path with `$.slices[*]`, `$.interactions[*]`, `$.slice_state`, `$.realization_level`, `$.slice_ids[*]` added. Optionally: separate slice documents under `use-cases/UC-{id}/slices/`. |
| `<guardrails>` | Constitutional triplet (P-003, P-020, P-022). Domain guardrails: reject detail_level < ESSENTIAL_OUTLINE (DI-01), basic flow as first slice (S-01), test cases before PREPARED state (S-01 Activity 4), interactions required at ANALYZED/INTERACTION_DEFINED (S-01 Activity 5, allOf constraint 1), MUST explicitly set `$.realization_level` on every state transition (GATE-2 note 3), MUST explicitly set `$.slice_state` on every lifecycle transition. |

##### GATE-2 Note 3 Resolution: Explicit $.realization_level Setting

The uc-slicer MUST explicitly set `$.realization_level` on every state transition. This is now encoded as:
- A forbidden action: "REALIZATION VIOLATION: NEVER set $.realization_level without verifying that the corresponding blocks are populated"
- An output filtering guardrail: "realization_level_must_match_populated_blocks"
- A post-completion check: "verify_realization_level_is_explicitly_set"

---

### 4. Template Design

#### F-10: use-case-realization.template.md

**Purpose:** Primary output template for fully structured use case artifacts. Implements the shared artifact format (R-01) with all schema blocks.

**Used by:** `uc-author` (primary output at all detail levels), `uc-slicer` (updates YAML frontmatter sections)

**Format:** YAML frontmatter delimited by `---` followed by Markdown narrative body.

**Placeholder structure:** Placeholders use `{PLACEHOLDER}` syntax for agent substitution.

```markdown
---
# === IDENTITY ===
id: UC-{DOMAIN}-{NNN}
title: "{TITLE}"
work_type: USE_CASE
version: "1.0.0"
status: DRAFT

# === CLASSIFICATION ===
goal_level: {GOAL_LEVEL}
goal_symbol: "{GOAL_SYMBOL}"
detail_level: {DETAIL_LEVEL}
scope: "{SCOPE}"
domain: {DOMAIN}

# === ACTORS ===
primary_actor: "{PRIMARY_ACTOR}"
supporting_actors:
  - name: "{SUPPORTING_ACTOR_NAME}"
    type: {SUPPORTING_ACTOR_TYPE}
stakeholders:
  - name: "{STAKEHOLDER_NAME}"
    interest: "{STAKEHOLDER_INTEREST}"

# === CONDITIONS ===
preconditions:
  - "{PRECONDITION}"
postconditions:
  success:
    - "{SUCCESS_GUARANTEE}"
  failure:
    - "{MINIMUM_GUARANTEE}"
trigger: "{TRIGGER_EVENT}"

# === FLOWS ===
basic_flow:
  - step: 1
    actor: "{ACTOR}"
    action: "{ACTION_VERB_OBJECT}"
    type: {STEP_TYPE}

# === EXTENSIONS ===
extensions:
  - id: EXT-{STEP}{LETTER}
    name: "{EXTENSION_NAME}"
    anchor_step: {ANCHOR_STEP}
    condition: "{CONDITION}"
    steps:
      - step: 1
        actor: "{ACTOR}"
        action: "{ACTION}"
        type: {STEP_TYPE}
    outcome: "{OUTCOME}"

# === ALTERNATIVE FLOWS ===
alternative_flows:
  - id: AF-{NN}
    name: "{ALT_FLOW_NAME}"
    branches_from_step: {BRANCH_STEP}
    condition: "{CONDITION}"
    steps:
      - step: 1
        actor: "{ACTOR}"
        action: "{ACTION}"
        type: {STEP_TYPE}
    rejoins_at_step: {REJOIN_STEP}

# === TRACEABILITY ===
parent_id: null
related_use_cases: []
requirements: []
slice_ids: []

# === METADATA ===
priority: {PRIORITY}
created_at: "{ISO_8601_DATETIME}"
created_by: "{AUTHOR}"
realization_level: {REALIZATION_LEVEL}
---

# {TITLE}

## Goal

{ONE_SENTENCE_GOAL_DESCRIPTION}

## Context

{SYSTEM_SCOPE_AND_CONTEXT}

## Main Success Scenario

1. {ACTOR} {ACTION}.
2. System {RESPONSE}.
...

## Extensions

{STEP}a. {CONDITION}:
  1. {HANDLING_STEP}.

## Alternative Flows

### AF-{NN}: {ALT_FLOW_NAME}

At step {N}, when {CONDITION}:
1. {ALT_STEP}.
...

## Notes

{ADDITIONAL_CONTEXT_OR_OPEN_QUESTIONS}
```

#### F-11: use-case-brief.template.md

**Purpose:** Lightweight template for Cockburn Brief format. Used for early-stage use cases at BRIEFLY_DESCRIBED level.

**Used by:** `uc-author` (when producing Level 1 detail)

**Format:** Minimal YAML frontmatter + single-paragraph narrative.

```markdown
---
id: UC-{DOMAIN}-{NNN}
title: "{TITLE}"
work_type: USE_CASE
version: "1.0.0"
status: DRAFT
goal_level: {GOAL_LEVEL}
scope: "{SCOPE}"
primary_actor: "{PRIMARY_ACTOR}"
detail_level: BRIEFLY_DESCRIBED
basic_flow:
  - step: 1
    actor: "{ACTOR}"
    action: "{HIGH_LEVEL_ACTION}"
    type: actor_action
  - step: 2
    actor: "System"
    action: "{HIGH_LEVEL_RESPONSE}"
    type: system_response
  - step: 3
    actor: "{ACTOR}"
    action: "{COMPLETION_ACTION}"
    type: actor_action
created_at: "{ISO_8601_DATETIME}"
created_by: "{AUTHOR}"
---

# {TITLE}

**Primary Actor:** {PRIMARY_ACTOR}
**Goal:** {ONE_SENTENCE_GOAL}
**Brief:** {TWO_TO_THREE_SENTENCE_DESCRIPTION}
```

#### F-12: use-case-casual.template.md

**Purpose:** Cockburn Casual format. Middle ground between Brief and Fully Dressed. Used at BULLETED_OUTLINE level.

**Used by:** `uc-author` (when producing Level 2 detail -- the default)

**Format:** YAML frontmatter with basic_flow + Markdown narrative with bulleted scenario.

```markdown
---
id: UC-{DOMAIN}-{NNN}
title: "{TITLE}"
work_type: USE_CASE
version: "1.0.0"
status: DRAFT
goal_level: {GOAL_LEVEL}
goal_symbol: "{GOAL_SYMBOL}"
detail_level: BULLETED_OUTLINE
scope: "{SCOPE}"
domain: {DOMAIN}
primary_actor: "{PRIMARY_ACTOR}"
basic_flow:
  - step: 1
    actor: "{ACTOR}"
    action: "{ACTION}"
    type: {STEP_TYPE}
  # ... 3-9 steps
created_at: "{ISO_8601_DATETIME}"
created_by: "{AUTHOR}"
---

# {TITLE}

**Primary Actor:** {PRIMARY_ACTOR}
**Goal Level:** {GOAL_LEVEL} ({GOAL_SYMBOL})
**Trigger:** {TRIGGER_EVENT}

## Main Success Scenario

1. {ACTOR} {ACTION}.
2. System {RESPONSE}.
...

## Possible Extensions

- At step {N}: {CONDITION} (not yet elaborated)
- At step {M}: {CONDITION} (not yet elaborated)
```

#### F-13: use-case-slice.template.md

**Purpose:** Template for individual slice documents when uc-slicer produces separate files per slice.

**Used by:** `uc-slicer` (optional output alongside in-artifact slicing)

**Format:** YAML frontmatter referencing parent use case + slice-specific fields.

```markdown
---
slice_id: UC-{DOMAIN}-{NNN}-S{N}
parent_use_case: UC-{DOMAIN}-{NNN}
title: "{SLICE_TITLE}"
slice_state: {SLICE_STATE}
realization_level: {REALIZATION_LEVEL}
steps_included:
  - flow: basic_flow
    steps: [{STEP_NUMBERS}]
  - flow: "{ALT_OR_EXT_ID}"
    steps: [{STEP_NUMBERS}]
invest_assessment:
  independent: {BOOL}
  negotiable: {BOOL}
  valuable: {BOOL}
  estimable: {BOOL}
  small: {BOOL}
  testable: {BOOL}
test_cases:
  - "{TEST_CASE_DESCRIPTION}"
---

# Slice: {SLICE_TITLE}

**Parent Use Case:** [{PARENT_TITLE}](../UC-{DOMAIN}-{NNN}-{slug}.md)
**State:** {SLICE_STATE}
**INVEST:** {PASS_FAIL_SUMMARY}

## Included Steps

{FLOW_STEP_LISTING}

## Test Cases

1. {TEST_CASE_1}
2. {TEST_CASE_2}

## Realization (Activity 5)

{INTERACTION_SEQUENCE_NARRATIVE -- only present at ANALYZED state}
```

---

### 5. Shared Schema Integration

#### Schema File Location

| Context | Path |
|---------|------|
| Design-phase artifact (current) | `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/architecture/shared-schema.json` |
| Production schema (Phase 3 deliverable) | `docs/schemas/use-case-realization-v1.schema.json` |

The production copy is created by copying the design-phase artifact. The production path is the CI validation target and the path referenced by agent guardrails.

#### Runtime Schema Usage

| Consumer | When | How | Action on Failure |
|----------|------|-----|-------------------|
| `uc-author` | After writing artifact | Read schema, parse artifact frontmatter, validate required fields and basic_flow constraints | If validation fails: fix the artifact before presenting to user. Do not write invalid artifacts. |
| `uc-slicer` | Before reading artifact (input validation) | Validate input artifact against schema | If validation fails: reject with actionable error message specifying which required fields are missing. |
| `uc-slicer` | After updating artifact | Validate updated artifact including allOf constraints | If validation fails: fix the artifact. Specifically verify constraints 1 (interactions at INTERACTION_DEFINED) and 2 (slices at STORY_DEFINED+). |
| CI pipeline (L5) | On commit | JSON Schema validation of all `*.md` files under `use-cases/` with `work_type: USE_CASE` | Fail the CI check. Block merge. |

#### Two-Layer Validation Gate Design

**Layer 1: JSON Schema Structural Validation (Deterministic)**

| What It Checks | How | Token Cost |
|----------------|-----|-----------|
| Required fields present (11 fields) | `required` array in schema | 0 (deterministic) |
| Field types correct (string, integer, array, object) | `type` constraints | 0 |
| Enum values valid (goal_level, status, detail_level, etc.) | `enum` arrays | 0 |
| Pattern constraints (id format, extension id format, etc.) | `pattern` regex | 0 |
| Array bounds (basic_flow 3-9 items, minItems on various arrays) | `minItems`, `maxItems` | 0 |
| Conditional requirements (allOf constraints 1-5) | `allOf` with `if/then` | 0 |
| Sub-object structure ($defs: flow_step, alternative_flow, extension, interaction, slice) | `$ref` resolution | 0 |

**Layer 2: Agent Guardrail Semantic Validation (LLM-Evaluated)**

| What It Checks | Why Not in Schema | Agent Responsible |
|----------------|-------------------|-------------------|
| `$.detail_level` matches actual content depth | Requires content analysis (is the narrative actually at Essential Outline level?) | `uc-author` |
| `$.basic_flow[*].actor` matches `$.primary_actor` or `$.supporting_actors[*].name` | Cross-field referential integrity beyond JSON Schema practical capability | `uc-author` |
| Extensions are non-empty before FULLY_DESCRIBED | Having 0 extensions is structurally valid; completeness is semantic | `uc-author` |
| `$.detail_level` >= ESSENTIAL_OUTLINE for slicing input | Agent-specific precondition, not global schema rule | `uc-slicer` |
| `$.interactions[*].source_step` references existing step in `$.interactions[*].source_flow` | Cross-array referential integrity beyond JSON Schema capability | `uc-slicer` |
| `$.realization_level` is consistent with actual block population | `realization_level` is a convenience summary; semantic consistency requires inspection | `uc-slicer` |

**Error Handling When Validation Fails:**

| Failure Type | Agent Response | User Visibility |
|-------------|----------------|-----------------|
| Layer 1: Missing required field | Agent fixes the artifact (adds default or prompts user for value). Does NOT write the invalid artifact. | Transparent: agent reports which field was missing and what action was taken. |
| Layer 1: Invalid enum value | Agent corrects to nearest valid enum. If ambiguous, escalates to user per H-31. | Transparent: agent reports the correction. |
| Layer 1: allOf constraint violation | Agent ensures the conditional block is populated before setting the triggering field. Example: populate `$.interactions[*]` before setting `$.realization_level` to `INTERACTION_DEFINED`. | Transparent. |
| Layer 2: Content/detail mismatch | Agent downgrades `$.detail_level` to match actual content, or elaborates content to match declared level. Reports the adjustment. | Transparent. |
| Layer 2: Cross-field reference violation | Agent fixes the reference (e.g., corrects actor name in flow step) or escalates to user if the correct value is ambiguous. | Transparent. |

---

### 6. Intra-Skill Interaction Model

#### Orchestration Pattern

```
Main Context (Orchestrator)
    |
    +-- [1] uc-author (creates/elaborates use case artifact)
    |       |
    |       v  [artifact file on disk, Layer 1 + Layer 2 validated]
    |
    +-- [2] uc-slicer (reads artifact, adds slices + interactions)
            |
            v  [updated artifact file, re-validated]
```

**P-003 compliance:** Single-level nesting. Main context invokes workers. Workers never invoke each other or spawn sub-workers. All coordination flows through the main context and the shared artifact file on disk.

**Sequential, not parallel:** uc-author must complete before uc-slicer can begin. The ordering is enforced by the detail_level prerequisite: uc-slicer rejects input at detail_level < ESSENTIAL_OUTLINE, which uc-author must produce first.

#### Handoff Contract: uc-author to uc-slicer (via orchestrator)

The orchestrator passes the following data to uc-slicer after uc-author completes:

| Field | Type | Value | Source |
|-------|------|-------|--------|
| `artifact_path` | string | `projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md` | uc-author output location |
| `detail_level` | enum | `>= ESSENTIAL_OUTLINE` | uc-author output `$.detail_level` |
| `key_findings` | array (3-5 items) | Actor-goal list summary, basic flow step count, extension count, recommended first slice | uc-author session_context.on_send |
| `success_criteria` | array | "At least 1 slice identified", "Basic flow is first slice", "Each slice has INVEST assessment" | Architecture specification |
| `schema_validation` | boolean | `true` (artifact passes shared-schema.json) | uc-author post-completion check |

**Handoff validation (SV-01..SV-07 per agent-development-standards.md):**

- SV-04: artifact_path resolves to existing file (uc-author wrote it)
- SV-06: detail_level >= ESSENTIAL_OUTLINE (prerequisite for slicing)

#### Progressive Realization Flow

```
[New Request]
    |
    v
uc-author (Steps 1-4)  -->  OUTLINED / BRIEFLY_DESCRIBED
    |                        ($.basic_flow exists, 3+ steps)
    |
uc-author (Steps 5-10) -->  OUTLINED / ESSENTIAL_OUTLINE
    |                        ($.extensions, $.alternative_flows added)
    |
uc-author (Steps 11-12) --> OUTLINED / FULLY_DESCRIBED
    |                        ($.stakeholders, sub-UCs extracted)
    |
    v
[Handoff to uc-slicer when $.detail_level >= ESSENTIAL_OUTLINE]
    |
    v
uc-slicer (Steps 1-4)  -->  STORY_DEFINED
    |                        ($.slices[*], $.slice_state = SCOPED)
    |
uc-slicer (Steps 5-6)  -->  STORY_DEFINED
    |                        ($.slices[*].test_cases, $.slice_state = PREPARED)
    |
uc-slicer (Steps 7-8)  -->  INTERACTION_DEFINED
    |                        ($.interactions[*], $.slice_state = ANALYZED)
    |
    v
[Available for /test-spec at STORY_DEFINED+]
[Available for /contract-design at INTERACTION_DEFINED]
```

#### Within-Skill Agent Selection

The main context (orchestrator) selects the agent based on:

| User Intent Pattern | Agent | Rationale |
|--------------------|-------|-----------|
| "Write a use case for..." | uc-author | Creating new artifact |
| "Elaborate UC-AUTH-001 to Essential Outline" | uc-author | Deepening existing artifact |
| "Add extensions to UC-AUTH-001" | uc-author | Adding flows (Step 9-10) |
| "Slice UC-AUTH-001 into stories" | uc-slicer | Decomposition |
| "Prepare slice UC-AUTH-001-S1" | uc-slicer | Lifecycle advancement |
| "Analyze slice UC-AUTH-001-S1 (Activity 5)" | uc-slicer | Realization production |
| "Create and slice UC-AUTH-001" | uc-author first, then uc-slicer | Combined request, sequential |
| "Refine UC-AUTH-001" | uc-author (default) | Ambiguous; default to authoring |

---

### 7. Risk Register

Risks carried forward from agent-decomposition.md Risk Assessment (RISK-01 through RISK-09) plus implementation-specific risks (RISK-10 through RISK-14).

| Risk ID | Category | Risk | Severity | Likelihood | Mitigation | Source |
|---------|----------|------|----------|------------|------------|--------|
| RISK-02 | Architecture | 2-agent split creates unnecessary handoff overhead for uc-slicer invoked < 20% of time | LOW | LOW | File-mediated handoff is a single Read. Track invocation frequency; merge to 1 agent if < 20% after 30 use cases. | CF-04, agent-decomp |
| RISK-04 | Schema | Shared schema proves insufficient for downstream transformations | HIGH | LOW | `additionalProperties: true` enables forward-compatible extension. Validation gate catches structural inadequacy early. Version evolution path documented. | AI-01, ASM-001 |
| RISK-05 | Routing | Routing collisions with existing skills (/nasa-se, /eng-team keywords overlap) | MEDIUM | LOW | Negative keywords suppress cross-matches. Compound triggers require phrase match. Priority 13 with 2-level gap analysis documented. | T-07, DI-10 |
| RISK-09 | Schema | Schema validation fails on artifacts missing optional-but-expected fields | LOW | MEDIUM | `$.detail_level` has `default: "BULLETED_OUTLINE"` in schema. Agent guardrails validate semantic prerequisites independently. Two-layer validation designed for this case. | agent-decomp |
| RISK-10 | Implementation | Template placeholders conflict with YAML special characters (colons, brackets) | LOW | MEDIUM | Placeholders use `{PLACEHOLDER}` syntax which is YAML-safe in quoted strings. Templates use double-quoted YAML strings for all placeholder values. Agent must ensure correct quoting. | New |
| RISK-11 | Implementation | Cockburn 12-step rules file (F-14) becomes too long for agent context budget | MEDIUM | LOW | Rules file targets < 500 lines. Use progressive disclosure: load steps 1-4 for BRIEFLY_DESCRIBED, steps 1-10 for ESSENTIAL_OUTLINE, full 12 steps for FULLY_DESCRIBED. Offset/limit on Read per CB-05. | CB-05 |
| RISK-12 | Implementation | Agent composition files (F-06..F-09) incorrectly configure Task tool invocation | MEDIUM | LOW | Follow existing composition patterns from `/problem-solving` and `/eng-team`. Test with actual Task tool invocation during Phase 3 prototyping. | New |
| RISK-13 | Quality | Sonnet model insufficient for uc-author integrative reasoning, quality scores < 0.92 | MEDIUM | LOW | Model override to Opus documented as first escalation path (agent-decomposition.md). Monitor quality scores during Phase 3. | agent-decomp model selection |
| RISK-14 | Integration | Registration in CLAUDE.md, AGENTS.md, mandatory-skill-usage.md incomplete | LOW | LOW | File responsibility matrix assigns eng-lead for registration (F-01). H-26 compliance verified by eng-reviewer. Checklist item in BEHAVIOR_TESTS.md. | H-26 |

---

## L2: Strategic Implications

### Long-Term Architectural Evolution

The `/use-case` skill is the first skill in a three-skill pipeline. Its architecture establishes patterns that `/test-spec` and `/contract-design` must follow:

1. **Shared schema as integration contract.** The `use-case-realization-v1.schema.json` is the machine-readable contract between all three skills. Changes to this schema affect all downstream consumers. Schema version evolution (1.0.0 to 1.1.0 to 2.0.0) is the primary compatibility concern.

2. **Two-layer validation as standard pattern.** The JSON Schema structural + agent guardrail semantic validation pattern established here should be replicated by `/test-spec` (input validation of use case artifacts) and `/contract-design` (input validation of interaction blocks). This pattern is generalizable to any Jerry skill that consumes structured artifacts.

3. **File-mediated handoff as default.** The artifact-on-disk handoff pattern (no direct agent-to-agent communication) is the simplest P-003-compliant coordination mechanism. It works because the shared schema provides the contract that would otherwise require a handoff protocol. This pattern is recommended for all skills in the pipeline.

### Security Posture Assessment

**Threat surface:** The `/use-case` skill operates at T2 (Read-Write) tier. Both agents read project files and write use case artifacts. No external network access (T3), no cross-session state (T4), no delegation (T5).

**STRIDE analysis (C1 -- routine, per skill scope):**

| Threat | Applicable? | Mitigation |
|--------|------------|------------|
| **S**poofing | LOW -- agents identified by name in composition files | Agent name validated by Task tool invocation |
| **T**ampering | LOW -- artifacts written to project workspace | Schema validation on write; git tracks changes |
| **R**epudiation | LOW -- `$.created_by` and `$.last_modified_by` fields track authorship | Metadata audit trail in frontmatter |
| **I**nformation Disclosure | LOW -- no secrets in use case artifacts | `no_secrets_in_output` guardrail on both agents |
| **D**enial of Service | LOW -- context budget is the only resource consumed | CB-05 offset/limit on large file reads |
| **E**levation of Privilege | LOW -- T2 agents cannot access Task tool (H-35) | Tool tier enforcement in frontmatter `tools` field |

**NIST CSF 2.0 mapping:**

| Function | Control | Implementation |
|----------|---------|----------------|
| Identify | Asset inventory | Use case artifacts cataloged via `$.id` pattern and worktracker |
| Protect | Access control | T2 tier limits tool access; agents cannot escalate |
| Detect | Validation | Two-layer validation detects malformed artifacts at write time |
| Respond | Error handling | Fallback: `escalate_to_user` on both agents |
| Recover | Version control | Git tracks all artifact changes; schema versioning enables rollback |

### Cross-Skill Pipeline Security Boundary

The cross-skill pipeline (`/use-case` to `/test-spec` to `/contract-design`) operates on a trust model where the shared artifact is the trust boundary. Each skill validates the artifact against the shared schema before consuming it. This means:

- A malformed artifact from `/use-case` cannot cause `/test-spec` to produce incorrect output -- the input validation gate rejects it.
- The `$.work_type = USE_CASE` discriminator prevents non-use-case artifacts from being processed by these skills.
- The `realization_level` and `detail_level` gates enforce minimum quality before downstream transformation.

---

## GATE-2 Issue Resolution

| # | Issue | Disposition | Where Addressed |
|---|-------|-------------|-----------------|
| 1 | tspec-generator guardrails should require `$.slice_state >= ANALYZED` per frontmatter-schema.md | **Noted, not implemented.** This is a `/test-spec` concern. tspec-generator input validation should check `$.slice_state >= ANALYZED` in addition to `$.detail_level >= ESSENTIAL_OUTLINE`. Flagged for the `/test-spec` architecture document. | This section (documentation only) |
| 2 | DI-05 cross-citation at uc-author guardrail line 136 may be wrong (should be DI-01) | **Confirmed incorrect; corrected.** DI-05 = "Clark transformation" (tspec-generator domain). The correct citation for "MUST NOT advance to Fully Described without complete extensions" is DI-01 ("4 narrative detail levels") + S-02 (Cockburn process). | Section 3.1, system prompt outline `<guardrails>` |
| 3 | uc-slicer guardrails should mandate setting `$.realization_level` explicitly | **Incorporated.** Added as: (a) forbidden action "REALIZATION VIOLATION", (b) output filtering guardrail "realization_level_must_match_populated_blocks", (c) post-completion check "verify_realization_level_is_explicitly_set", (d) additional forbidden action covering `$.slice_state` explicit setting. | Section 3.2, governance YAML and system prompt outline |

---

## Self-Review Checklist (H-15, S-010)

### Constitutional Compliance

- [x] **P-001 (Truth/Accuracy):** Every specification traces to Phase 2 architecture documents (file-organization.md, agent-decomposition.md, frontmatter-schema.md, shared-schema.json) with specific line references where applicable.
- [x] **P-002 (File Persistence):** Document persisted to `implementation/step-9-use-case-architecture.md`.
- [x] **P-003 (No Recursive Subagents):** Both agents are T2 workers without Task tool. P-003 compliance diagram included in Section 6.
- [x] **P-004 (Provenance):** Source documents cited throughout. Lineage header traces to all 5 Phase 2 inputs.
- [x] **P-020 (User Authority):** Status is PROPOSED. No design decision finalized without user approval.
- [x] **P-022 (No Deception):** Limitations disclosed: interactions block is architecturally speculative (carried forward from Phase 2). GATE-2 issues addressed transparently with disposition rationale.

### Structural Compliance

- [x] **H-23 (Navigation):** Navigation table present with anchor links to all sections.
- [x] **H-25 (Skill naming):** Skill directory is `skills/use-case/` (kebab-case). Skill file is `SKILL.md` (exact case).
- [x] **H-26 (Skill description):** Description includes WHAT + WHEN + trigger phrases, under 1024 chars, no XML tags.
- [x] **H-34 (Agent definitions):** Dual-file architecture (.md + .governance.yaml) specified for both agents. All required governance fields (version, tool_tier, identity with role/expertise/cognitive_mode) specified. Constitutional triplet (P-003, P-020, P-022) in principles_applied. Minimum 3 forbidden_actions with NPT-009 format. Worker agents (T2) do not include Task tool.
- [x] **L0/L1/L2:** All three output levels present with appropriate audience depth.

### Completeness Verification

- [x] **File Manifest:** 16 files + 1 schema copy = 17 total. Every file has a path, purpose, responsible agent, and criticality level.
- [x] **SKILL.md Design:** Frontmatter, routing keywords, agent table, when-to-use (with consequences per NPT-013), integration points all specified.
- [x] **Agent Definitions:** Both agents have: official frontmatter, governance YAML (all required + recommended fields), system prompt outline (7 XML sections), forbidden actions (5+ per agent, NPT-009 format).
- [x] **Template Design:** 4 templates with purpose, format, placeholder structure, consuming agent, and example skeleton.
- [x] **Shared Schema Integration:** Runtime usage table, two-layer validation gate design, error handling for all failure types.
- [x] **Intra-Skill Interaction:** Orchestration pattern (P-003), handoff contract, progressive realization flow, agent selection criteria.
- [x] **Risk Register:** 9 carried forward + 5 new = 14 risks. Each has severity, likelihood, mitigation, source.

### GATE-2 Issue Resolution

- [x] **Issue 1 (tspec-generator slice_state):** Noted as out-of-scope for this skill; flagged for /test-spec architecture.
- [x] **Issue 2 (DI-05 cross-citation):** Confirmed incorrect; corrected to DI-01 + S-02 in Section 3.1.
- [x] **Issue 3 (explicit realization_level):** Incorporated in uc-slicer governance YAML (forbidden actions, output filtering, post-completion checks).

### Adversarial Self-Check (S-002: Devil's Advocate)

**Challenge 1: "Are 16 files too many for a 2-agent skill?"**
The file count is driven by the dual-file architecture (H-34: .md + .governance.yaml per agent = 4 files), composition files (2 per agent = 4 files), templates (4 for the format spectrum), and standard skill infrastructure (SKILL.md, rules, contract, tests = 4 files). Total: 4+4+4+4 = 16. Each file has a distinct purpose; no file duplicates another's responsibility. Existing multi-agent skills (/adversary with 3 agents, /problem-solving with 10 agents) follow the same pattern at larger scale. 16 files is proportional to 2 agents.

**Challenge 2: "Is the two-layer validation gate over-engineered for a single skill?"**
The two-layer pattern is required because JSON Schema cannot express all necessary constraints (cross-field references, semantic content matching). Without Layer 2, artifacts that pass structural validation but fail semantic checks would propagate to downstream skills. The pattern is established in Phase 2 architecture (frontmatter-schema.md "Constraints not encoded in schema" table) and is not a design choice of this architecture document. This document operationalizes an already-decided pattern.

**Challenge 3: "Should the composition files (F-06..F-09) be deferred to Phase 3 prototyping?"**
Composition files define how the main context invokes agents via Task tool. They are required for any invocation beyond direct agent selection. Deferring them would leave the skill unable to be invoked programmatically by orchestration workflows. The file manifest includes them because they are part of the minimum viable skill structure per existing patterns (/problem-solving, /nasa-se, /eng-team all have composition directories).

---

*Architecture Design Version: 1.0.0*
*Constitutional Compliance: P-001 (truth), P-002 (file persistence), P-003 (no recursive subagents), P-004 (provenance), P-020 (user authority -- PROPOSED status), P-022 (no deception -- speculative block warnings carried forward, GATE-2 issues disclosed)*
*Quality Review Required: YES -- C4 all-10-strategy review at >= 0.95 threshold*
*Next Agent: eng-lead (Step 10: implementation plan and task decomposition)*
*Workflow ID: use-case-skills-20260308-001*
