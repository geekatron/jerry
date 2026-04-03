# Skill Architecture Design: /contract-design

> **PS ID:** proj-021 | **Entry ID:** step-11-contract-design-architecture | **Workflow ID:** use-case-skills-20260308-001
> **Date:** 2026-03-09 | **Agent:** eng-architect | **Step:** 11 (Phase 3 Implementation)
> **Quality Threshold:** >= 0.95 (C4, user override C-008)
> **Status:** PROPOSED (P-020: user approval required before ACCEPTED)
> **Version:** 1.0.0
> **Lineage:** file-organization.md (v2.1.0, 0.951 PASS), agent-decomposition.md (v1.1.0, 0.963 PASS), frontmatter-schema.md (v1.0.0, 0.955 PASS), shared-schema.json (v1.0.0), step-9-use-case-architecture.md (v1.2.0, 0.956 PASS), step-10-test-spec-architecture.md (v1.1.0, 0.952 PASS)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What to build, why, and key decisions in plain language |
| [L1: Technical Specification](#l1-technical-specification) | Implementation-ready specifications for every file |
| [1. File Manifest](#1-file-manifest) | Complete list of files to create with paths |
| [2. SKILL.md Design](#2-skillmd-design) | Routing, agent table, when-to-use, integration points |
| [3. Agent Definition Specifications](#3-agent-definition-specifications) | Per-agent .md frontmatter, .governance.yaml, system prompt outline |
| [4. Template Design](#4-template-design) | OpenAPI, AsyncAPI, CloudEvents, JSON Schema template specifications |
| [5. Shared Schema Integration](#5-shared-schema-integration) | Input validation, UC-to-contract mapping, error handling |
| [6. Cross-Skill Integration Model](#6-cross-skill-integration-model) | How /contract-design consumes /use-case output |
| [7. Contract Type Mapping](#7-contract-type-mapping) | How each UC artifact field maps to each contract type |
| [8. Threat Model](#8-threat-model) | Trust boundaries, attack surfaces, STRIDE analysis |
| [9. Risk Register](#9-risk-register) | Implementation risks with mitigations |
| [L2: Strategic Implications](#l2-strategic-implications) | Long-term evolution, security posture, cross-skill pipeline |
| [ORCHESTRATION.yaml Reconciliation](#orchestrationyaml-reconciliation) | Mapping ORCH deliverables to architecture (SSOT) |
| [References](#references) | Full bibliographic citations for cited works |
| [Self-Review Checklist](#self-review-checklist) | H-15 / S-010 verification |

---

## L0: Executive Summary

This document translates the Phase 2 architecture (3 documents, 1 JSON Schema, all scoring >= 0.95) into an implementation-ready specification for the `/contract-design` Jerry skill. The skill transforms use case realization artifacts produced by `/use-case` (specifically the `interactions` block produced by `uc-slicer` during Activity 5) into API contract specifications.

**What gets built.** 14 files organized under `skills/contract-design/`. Two agents: `cd-generator` (transforms use case interaction sequences into OpenAPI 3.1 contract specifications using a novel UC-to-contract transformation algorithm) and `cd-validator` (validates generated contracts against OpenAPI/AsyncAPI/CloudEvents/JSON Schema standards and verifies traceability back to source interactions). Four template files provide output scaffolding for each supported contract type. One rule file, one skill contract, one behavior test file, and the SKILL.md entry point complete the skill.

**Key architectural decisions.**

1. **2 agents, not 1.** The Phase 2 architecture (SSOT) defines 1 agent (`cd-generator`) for `/contract-design` with guidance: "If methodology section exceeds 1,500 tokens during Phase 3, split." This architecture introduces `cd-validator` because: (a) the ORCHESTRATION.yaml explicitly lists `contract-validator` as a deliverable; (b) contract validation against OpenAPI 3.1 schema is a distinct systematic verification activity from the convergent contract generation; (c) the generator's methodology alone (~1,400 tokens for the 9-step algorithm plus extension-to-error-response mapping) leaves minimal headroom, and adding validation logic would exceed 1,500 tokens. The split follows the same pattern as Step 10's `tspec-generator`/`tspec-analyst` split.

2. **REST-first scope with template scaffolding.** The Phase 2 architecture defers AsyncAPI, CloudEvents, and event-driven contracts (DI-07, ASM-005, G-02). However, the ORCHESTRATION.yaml lists all four template files as deliverables. This architecture provides all four templates as structural scaffolding (header, metadata, placeholder sections) while marking AsyncAPI and CloudEvents content as `x-deferred: true` with implementation notes. The `cd-generator` agent generates OpenAPI content only in v1.0.0. The JSON Schema template is active because it provides the `components/schemas` definitions shared across all contract types.

3. **File-mediated integration.** Consistent with Steps 9 and 10, `/contract-design` communicates with `/use-case` exclusively through the shared artifact file on disk, validated against `use-case-realization-v1.schema.json` at the input boundary. No direct agent-to-agent communication. P-003 compliant.

4. **Two-layer input validation.** Same pattern as Steps 9 and 10: Layer 1 (JSON Schema structural validation of the use case artifact) plus Layer 2 (agent guardrail semantic validation of interaction completeness, source step cross-referencing, and actor role presence). The input validation gate rejects artifacts without the `interactions` block, with actionable error messages directing users to `/use-case` (`uc-slicer`) for realization.

5. **PROTOTYPE labeling.** Per G-01 (no prior art for UC-to-contract transformation) and LES-001, all generated contracts carry an `x-prototype: true` marker in the OpenAPI `info` section. The PROTOTYPE label persists until human review validates the generated contract's accuracy. This is the same approach documented in the Phase 2 architecture.

6. **ORCHESTRATION.yaml reconciliation.** The ORCHESTRATION.yaml lists `contract-generator` and `contract-validator` as agent names. The Phase 2 architecture (SSOT) defines `cd-generator` with the `cd-` prefix. This document uses the SSOT prefix convention: `cd-generator` and `cd-validator`. See [ORCHESTRATION.yaml Reconciliation](#orchestrationyaml-reconciliation).

---

## L1: Technical Specification

### 1. File Manifest

14 files to create, organized by directory. All paths are relative to repository root.

#### Directory Tree

```
skills/contract-design/
+-- SKILL.md                                    # [F-01] Skill entry point (H-25)
+-- agents/
|   +-- cd-generator.md                         # [F-02] Agent definition: UC-to-contract generation
|   +-- cd-generator.governance.yaml            # [F-03] Governance metadata (H-34)
|   +-- cd-validator.md                         # [F-04] Agent definition: contract validation
|   +-- cd-validator.governance.yaml            # [F-05] Governance metadata (H-34)
+-- composition/
|   +-- cd-generator.agent.yaml                 # [F-06] Task tool invocation config
|   +-- cd-generator.prompt.md                  # [F-07] System prompt for Task invocation
|   +-- cd-validator.agent.yaml                 # [F-08] Task tool invocation config
|   +-- cd-validator.prompt.md                  # [F-09] System prompt for Task invocation
+-- templates/
|   +-- openapi-template.yaml                   # [F-10] OpenAPI 3.1 output template
|   +-- asyncapi-template.yaml                  # [F-11] AsyncAPI 3.0 output template (scaffolding)
|   +-- cloudevents-template.yaml               # [F-12] CloudEvents 1.0 output template (scaffolding)
|   +-- json-schema-template.json               # [F-13] JSON Schema Draft 2020-12 output template
+-- rules/
|   +-- uc-to-contract-rules.md                 # [F-14] Novel transformation algorithm rules
+-- contracts/
|   +-- CD_SKILL_CONTRACT.yaml                  # [F-15] Skill contract
+-- tests/
|   +-- BEHAVIOR_TESTS.md                       # [F-16] BDD behavior tests for the skill
+-- samples/
    +-- sample-contract.openapi.yaml            # [F-17] Sample OpenAPI output demonstrating the skill
```

**Note on file count:** The ORCHESTRATION.yaml deliverable list specifies 10 files (F-01 through F-05, F-10 through F-13, plus SKILL.md). This architecture adds composition files (F-06 through F-09), rule file (F-14), skill contract (F-15), behavior tests (F-16), and sample (F-17) for parity with the established pattern from Steps 9 and 10. The 4 ORCHESTRATION.yaml-specified templates (F-10 through F-13) are included exactly as listed.

#### File Responsibility Matrix

| File ID | Primary Author (Sub-Step) | Reviewer | Criticality |
|---------|--------------------------|----------|-------------|
| F-01 | eng-lead (11a) | eng-reviewer | C3 |
| F-02, F-03 | eng-backend (11b) | eng-security, eng-reviewer | C3 |
| F-04, F-05 | eng-backend (11b) | eng-security, eng-reviewer | C3 |
| F-06, F-07 | eng-backend (11c) | eng-reviewer | C2 |
| F-08, F-09 | eng-backend (11c) | eng-reviewer | C2 |
| F-10 | eng-backend (11d) | eng-reviewer | C3 |
| F-11, F-12 | eng-backend (11d) | eng-reviewer | C2 |
| F-13 | eng-backend (11d) | eng-reviewer | C2 |
| F-14 | eng-backend (11e) | eng-reviewer | C3 |
| F-15 | eng-lead (11a) | eng-reviewer | C2 |
| F-16 | eng-qa (11f) | eng-reviewer | C3 |
| F-17 | eng-backend (11d) | eng-reviewer | C2 |

**Composition file schema reference (F-06..F-09):** Composition files follow the canonical agent YAML schema (`docs/schemas/agent-canonical-v1.schema.json`). Reference implementation: `skills/use-case/composition/uc-author.agent.yaml` (Step 9) and `skills/test-spec/composition/tspec-generator.agent.yaml` (Step 10). Required fields: `name`, `version`, `description`, `skill: contract-design`, `identity` (role, expertise, cognitive_mode), `model.tier`, `tools.native` (T1/T2 set), `tools.forbidden: [agent_delegate]`, `tool_tier`, `guardrails`, `output`, `constitution`. The `.prompt.md` files (F-07, F-09) contain the system prompt text used when the agent is invoked via Task tool -- a copy of the markdown body from the agent `.md` file.

**Skill contract specification (F-15):** CD_SKILL_CONTRACT.yaml follows the OpenAPI 3.0-inspired contract pattern established by Steps 9 and 10 (`skills/use-case/contracts/UC_SKILL_CONTRACT.yaml`, `skills/test-spec/contracts/TS_SKILL_CONTRACT.yaml`). Required top-level structure: `openapi: "3.0.3"`, `info` (title, version, description), `agents` (cd-generator, cd-validator -- each with description, cognitive_mode, model, input/output schema), and `components.schemas`.

---

### 2. SKILL.md Design

#### Frontmatter (F-01)

```yaml
---
name: contract-design
description: >-
  API contract generation from use case realization artifacts using a novel
  UC-to-contract transformation algorithm. Transforms use case interaction
  sequences (produced by /use-case uc-slicer Activity 5) into OpenAPI 3.1
  specifications with full traceability from API operations to source
  interaction steps. Validates generated contracts against OpenAPI schema
  standards. Requires use case artifacts at realization_level =
  INTERACTION_DEFINED with populated interactions block. Invoke when generating
  API contracts, OpenAPI specs, endpoint designs, request/response schemas,
  or operation mappings from use case artifacts.
version: "1.0.0"
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
activation-keywords:
  - "contract design"
  - "contract-design"
  - "API contract"
  - "OpenAPI"
  - "API spec"
  - "API specification"
  - "generate contract"
  - "contract from use case"
  - "API schema"
  - "endpoint design"
  - "operation mapping"
  - "request response schema"
  - "API generation"
  - "REST contract"
  - "swagger"
  - "use case to API"
  - "interaction to contract"
---
```

#### Routing Keywords (Trigger Map Entry -- Priority 15)

Per agent-decomposition.md Trigger Map Extensions section:

| Column | Value |
|--------|-------|
| **Detected Keywords** | contract design, contract-design, API contract, OpenAPI, API spec, API specification, generate contract, contract from use case, API schema, endpoint design, operation mapping, request response schema, API generation, REST contract, swagger, use case to API, interaction to contract |
| **Negative Keywords** | requirements specification, V&V, technical review, use case model, actor goal, write use case, BDD, Gherkin, scenario, test spec, feature file, adversarial, tournament, transcript, penetration, exploit, code review, pricing model, cloud pricing, documentation, tutorial |
| **Priority** | 15 |
| **Compound Triggers** | "API contract" OR "contract design" OR "OpenAPI" OR "generate contract" OR "contract from use case" OR "API specification" OR "use case to API" (phrase match) |
| **Skill** | `/contract-design` |

**Priority 15 rationale:** Priority 15 places `/contract-design` one level below `/test-spec` (priority 14) and two levels below `/use-case` (priority 13). This ordering reflects the pipeline dependency: use case authoring and test generation typically precede contract generation. The keyword sets are disjoint from both sibling skills -- `/use-case` triggers on "write use case", "basic flow", "cockburn"; `/test-spec` triggers on "BDD", "Gherkin", "feature file"; `/contract-design` triggers on "OpenAPI", "API contract", "endpoint design". The negative keywords suppress false positives: "BDD" and "Gherkin" route to `/test-spec`; "pricing model" prevents collision with `/pm-pmm`; "write use case" routes to `/use-case`.

**Disambiguation: "API" keyword.** The word "API" alone is excluded from positive keywords because it is ambiguous: it could mean API documentation (`/diataxis`), API security testing (`/red-team`), or API contract generation (`/contract-design`). The compound triggers require qualification ("API contract", "API specification", "generate contract") to route to `/contract-design`. This prevents AP-02 (Bag of Triggers) collisions.

**Disambiguation: "schema" keyword.** "schema" alone is excluded. In context with "JSON Schema" or "API schema", it routes here. In context with "database schema" or "validation schema", it routes elsewhere. Compound trigger "API schema" handles this.

#### Agent Routing Table

| Agent | Role | Model | Cognitive Mode | Tool Tier | Output Location | Decision Signal |
|-------|------|-------|----------------|-----------|-----------------|-----------------|
| `cd-generator` | Transforms UC interaction sequences into OpenAPI 3.1 contract specifications | opus | convergent | T2 | `projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}.openapi.yaml` | "generate", "create contract", "OpenAPI from use case", "map interactions to operations", "derive API" |
| `cd-validator` | Validates generated contracts against OpenAPI standards and verifies traceability | sonnet | systematic | T1 | `projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}-validation.md` | "validate contract", "check OpenAPI", "verify traceability", "contract compliance", "schema validation" |

**Default routing:** When intent is ambiguous between generation and validation, route to `cd-generator` first. Generation must precede validation. When the user says "generate and validate the contract," invoke `cd-generator` first, then `cd-validator` on the output.

#### When to Use

**Activate this skill when:**

- Generating OpenAPI 3.1 specifications from use case realization artifacts
- Transforming use case interaction sequences into API operations, paths, and schemas
- Creating request/response schemas from interaction preconditions and postconditions
- Mapping use case actors to API consumer/provider roles
- Deriving error responses from use case extension conditions
- Validating that a generated contract traces to all source interaction steps

**NEVER invoke this skill when:**

- Task is writing or editing use case artifacts -- Consequence: `/contract-design` agents do not implement Cockburn's writing methodology; they consume use case output, not produce it; use `/use-case` instead.
- Task is generating BDD test specifications from use case artifacts -- Consequence: `/contract-design` produces OpenAPI contracts, not Gherkin Feature files; use `/test-spec` instead.
- Task is writing OpenAPI specifications from scratch (not from use case artifacts) -- Consequence: `/contract-design` requires the structured `interactions` block as input; writing OpenAPI from free-form requirements is a manual authoring task, not a transformation.
- Task is adversarial quality review of deliverables -- Consequence: use `/adversary` for quality scoring and adversarial critique.
- Use case artifact does not have an `interactions` block -- Consequence: the UC-to-contract transformation requires `$.interactions[*]` produced by `uc-slicer` Activity 5; use `/use-case` to realize the use case first.
- Task is generating AsyncAPI or CloudEvents specifications -- Consequence: these contract types are deferred (DI-07, ASM-005, G-02); templates exist as scaffolding but agent generation logic is not implemented in v1.0.0.

#### Integration Points

| Integration | Direction | Mechanism | Pre-Condition |
|-------------|-----------|-----------|---------------|
| `/use-case` to `/contract-design` | cd-generator reads UC artifact produced by uc-slicer Activity 5 | Shared artifact file validated against `docs/schemas/use-case-realization-v1.schema.json` | `$.realization_level = INTERACTION_DEFINED`, `$.interactions` non-empty, each interaction has all required fields |
| `/contract-design` output consumed by implementers | OpenAPI specs serve as API implementation contracts | Human- and machine-readable `.openapi.yaml` files in `projects/${JERRY_PROJECT}/contracts/` | Contract validated by cd-validator |
| `/contract-design` parallel to `/test-spec` | Both are independent consumers of `/use-case` output | File-mediated -- both read the same UC artifact; neither depends on the other | UC artifact at INTERACTION_DEFINED (for /contract-design) or ESSENTIAL_OUTLINE+ (for /test-spec) |
| `/contract-design` to code generators | OpenAPI spec can feed OpenAPI Generator or similar tools | Standard OpenAPI 3.1 format | Contract passes cd-validator checks |

---

### 3. Agent Definition Specifications

#### 3.1 Agent: cd-generator

**Agent Split Justification**

The Phase 2 architecture defines a single `cd-generator` agent. This architecture introduces `cd-validator` as a second agent because:

1. **Distinct cognitive modes.** UC-to-contract transformation is a convergent evaluation activity (evaluate interaction steps, select optimal operation structure, resolve resource identification). Contract validation is a systematic verification activity (check schema compliance, verify traceability completeness, enumerate missing mappings). These are two different reasoning patterns per agent-development-standards.md Mode Selection Guide.

2. **ORCHESTRATION.yaml alignment.** The ORCHESTRATION.yaml explicitly lists `contract-validator` as a required deliverable alongside `contract-generator`. While the Phase 2 architecture defines 1 agent, the workflow deliverable list anticipates the split.

3. **Methodology section size.** The UC-to-contract transformation algorithm alone requires approximately 1,400 tokens (9 mapping steps + actor-role mapping table + extension-to-error mapping). Adding OpenAPI schema validation logic (~600 tokens), traceability verification (~400 tokens), and standards compliance checking (~300 tokens) would push the combined methodology to approximately 2,700 tokens, well exceeding the 1,500-token threshold from Pattern 1.

4. **Different input/output profiles.** `cd-generator` reads a UC artifact and writes OpenAPI YAML files. `cd-validator` reads generated OpenAPI files and the source UC artifact to produce a validation report. They operate on different primary inputs.

5. **Invocation frequency difference.** Generation runs once per use case realization. Validation may run multiple times (after each generation iteration, after manual contract edits, during quality gate reviews). Separating them allows independent invocation.

**Agent naming note:** "cd-validator" is chosen (rather than "cd-analyst" as with `tspec-analyst`) because this agent performs deterministic schema validation and binary pass/fail traceability checks, not evaluative analysis. "Validator" matches the systematic cognitive mode -- it checks compliance against defined standards. This is the opposite naming rationale from Step 10, where "analyst" was preferred because tspec-analyst performs evaluative coverage analysis.

##### Official Frontmatter (F-02: `cd-generator.md`)

```yaml
---
name: cd-generator
description: >-
  API Contract Generator agent. Transforms use case realization artifacts into
  OpenAPI 3.1 specifications using a novel UC-to-contract transformation
  algorithm. Maps interaction sequences to API paths and operations, derives
  HTTP methods from request semantics, extracts request/response schemas from
  interaction preconditions and postconditions, and maps extension conditions
  to error responses. Requires input use case at realization_level =
  INTERACTION_DEFINED with populated interactions block from uc-slicer
  Activity 5. Invoke when generating, creating, deriving, or mapping use case
  interactions to API contracts.
model: opus
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---
```

**Model Selection: Opus**

Justification (AD-M-009): This is the highest-risk agent in the three-skill pipeline (G-01 gap -- no prior art for the UC-to-contract transformation). The transformation algorithm is novel and requires complex reasoning to map use case interaction semantics to API contract structures. Unlike the Clark mapping in `/test-spec` (deterministic lookup), the UC-to-contract mapping requires judgment about: (a) resource identification from interaction receiver descriptions, (b) HTTP method inference from request semantics, (c) operation granularity decisions (one interaction = one operation vs. multiple interactions = one resource), and (d) schema structure derivation from natural language preconditions/postconditions. Opus is warranted for complex reasoning tasks with no established procedural template. If quality scores are consistently above 0.95 threshold after 10+ contract generations, Sonnet can be evaluated as a cost-reduction measure.

##### Governance YAML (F-03: `cd-generator.governance.yaml`)

```yaml
version: "1.0.0"
tool_tier: "T2"
# ET-M-001 compliance: reasoning_effort: max (C4 agent -- G-01 no prior art, novel algorithm)
# C4 classification: novel transformation algorithm with no prior art (G-01); governs API
# contract structure that feeds downstream code generation (irreversibility threshold met)
reasoning_effort: max

identity:
  role: "API Contract Generator -- transforms use case realization artifacts into OpenAPI 3.1 specifications using a novel UC-to-contract transformation algorithm"
  expertise:
    - "UC-to-contract transformation algorithm (interaction sequence to API operation mapping, resource identification, HTTP method inference from request semantics)"
    - "OpenAPI 3.1 specification authoring (paths, operations, request/response schemas, components, security schemes, error responses)"
    - "Actor-role-to-contract-role mapping (primary actor as API consumer, system as provider, supporting actors as external dependencies per IC-05)"
  cognitive_mode: "convergent"

persona:
  tone: "analytical"
  communication_style: "structured"
  audience_level: "adaptive"

capabilities:
  forbidden_actions:
    - "P-003 VIOLATION: NEVER spawn recursive subagents or delegate to other agents via Task tool -- Consequence: agent hierarchy violation breaks orchestrator-worker topology and causes uncontrolled token consumption. cd-generator is a T2 worker agent without Task tool access."
    - "P-020 VIOLATION: NEVER override user decisions about contract scope, operation granularity, resource naming, or which use case to transform -- Consequence: unauthorized contract structure changes erode trust and may invalidate integration agreements that depend on user-approved API design."
    - "P-022 VIOLATION: NEVER misrepresent contract completeness or traceability -- Consequence: claiming full coverage when interactions are unmapped causes downstream implementers to build against an incomplete API specification, leaving behavioral paths unimplemented."
    - "SCHEMA VIOLATION: NEVER generate contracts from use case artifacts that fail input validation (missing interactions block or detail_level below ESSENTIAL_OUTLINE) -- Consequence: generating from incomplete input produces contracts that omit API operations and lack request/response schema grounding, creating a false sense of API completeness."
    - "METHODOLOGY VIOLATION: NEVER invent API operations that do not trace to a specific use case interaction step -- Consequence: untraceable operations cannot be verified against the use case source, breaking the transformation contract and undermining the methodological guarantee that every API operation has a provenance chain."
    - "SCOPE VIOLATION: NEVER generate AsyncAPI or CloudEvents contracts in v1.0.0 -- Consequence: these contract types are deferred per DI-07 and ASM-005 until G-02 (multi-actor pub/sub mapping) is resolved. Premature generation produces untested output from unvalidated transformation logic."
  forbidden_action_format: "NPT-009-complete"
  output_formats:
    - "yaml"
    - "markdown"

guardrails:
  input_validation:
    - "Input artifact must exist and contain valid YAML frontmatter with $.work_type = USE_CASE"
    - "Input artifact must have $.interactions array with at least 1 entry (reject with actionable error directing to /use-case uc-slicer)"
    - "Input artifact $.detail_level must be >= ESSENTIAL_OUTLINE (reject BRIEFLY_DESCRIBED and BULLETED_OUTLINE)"
    - "Each $.interactions[*] must have all 7 required fields: id, source_step, source_flow, actor_role, system_role, request_description, response_description"
    - "Each $.interactions[*].source_step must reference an existing step in the flow identified by $.interactions[*].source_flow (cross-reference validation)"
    - "$.supporting_actors must be readable for IC-05 cross-referencing (warn if absent)"
  output_filtering:
    - "no_secrets_in_output"
    - "every_operation_must_trace_to_source_interaction"
    - "all_request_schemas_must_derive_from_interaction_preconditions"
    - "all_response_schemas_must_derive_from_interaction_postconditions"
    - "generated_contracts_must_carry_x_prototype_true"
    - "no_asyncapi_or_cloudevents_generation_in_v1"
  fallback_behavior: "escalate_to_user"

output:
  required: true
  location: "projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}.openapi.yaml"
  template: "skills/contract-design/templates/openapi-template.yaml"
  levels:
    - "L0"
    - "L1"

constitution:
  reference: "docs/governance/JERRY_CONSTITUTION.md"
  principles_applied:
    - "P-001"
    - "P-002"
    - "P-003"
    - "P-004"
    - "P-020"
    - "P-022"

validation:
  post_completion_checks:
    - "verify_openapi_file_created_at_output_location"
    - "verify_mapping_file_created_at_output_location"
    - "verify_one_operation_per_consumer_interaction"
    - "verify_x_prototype_true_in_info_section"
    - "verify_all_operations_have_source_interaction_traceability"
    - "verify_error_responses_trace_to_extension_conditions"
    - "verify_no_asyncapi_or_cloudevents_content_generated"

session_context:
  on_receive:
    - "Load use case artifact and validate frontmatter against schema"
    - "Count interactions and determine expected operation count"
    - "Identify consumer vs. provider interactions for operation classification"
    - "Cross-reference supporting_actors with interactions for IC-05 resolution"
  on_send:
    - "Report OpenAPI file path, mapping file path, and operation count"
    - "List key findings: operations generated, unmapped interactions (if any), error responses derived"
    - "Flag x-prototype status and recommend cd-validator for validation"

enforcement:
  tier: "medium"
  escalation_path: "eng-reviewer"
```

##### System Prompt Outline (F-02 markdown body)

The `cd-generator.md` markdown body will contain these XML-tagged sections:

**`<identity>`** -- API Contract Generator role, convergent cognitive mode, distinction from cd-validator (generator produces contracts; validator checks compliance).

**`<purpose>`** -- Transform structured use case realization artifacts into OpenAPI 3.1 specifications. Each interaction step maps to an API operation. Actor roles determine API directionality. Extension conditions map to error responses.

**`<input>`** -- Primary input: UC artifact at `$.realization_level = INTERACTION_DEFINED`. Required fields: `$.interactions[*]` with all 7 required sub-fields, `$.primary_actor`, `$.supporting_actors[*]`, `$.extensions[*]`. Session context fields: `artifact_path`, `output_path`, `success_criteria`.

**`<capabilities>`** -- T2 Read-Write capabilities. Load `skills/contract-design/rules/uc-to-contract-rules.md` for algorithm reference. No Task tool, no external research, no UC artifact modification. Capabilities NOT available: AsyncAPI/CloudEvents generation, cross-session state, delegation.

**`<methodology>`** -- The 9-step UC-to-contract transformation algorithm (detailed in [Section 7](#7-contract-type-mapping)):

| Step | Action | Schema Fields Read |
|------|--------|--------------------|
| 1 | Validate input | `$.realization_level`, `$.interactions`, `$.detail_level` |
| 2 | Identify resources | `$.interactions[*].system_role` (where = receiver), `$.interactions[*].request_description` |
| 3 | Map interactions to operations | `$.interactions[*].actor_role`, `$.interactions[*].system_role`, `$.interactions[*].source_step` |
| 4 | Derive HTTP methods | `$.interactions[*].request_description` semantic analysis |
| 5 | Extract request schemas | `$.interactions[*].preconditions[*]`, `$.interactions[*].request_description` |
| 6 | Extract response schemas | `$.interactions[*].postconditions[*]`, `$.interactions[*].response_description` |
| 7 | Map extensions to error responses | `$.extensions[*].anchor_step`, `$.extensions[*].condition`, `$.extensions[*].outcome` cross-referenced with `$.interactions[*].source_step` |
| 8 | Resolve supporting actor roles (IC-05) | `$.supporting_actors[*]`, `$.interactions[*].actor_role` |
| 9 | Compose and validate OpenAPI | All fields assembled; template applied; YAML output written |

**`<output>`** -- Two output files per generation: (1) OpenAPI 3.1 YAML at `projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}.openapi.yaml`; (2) Mapping document at `projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}-mapping.md`. L0 summary after creation. L1 is the files themselves.

**`<guardrails>`** -- Constitutional compliance (P-003, P-020, P-022). Two-layer input validation gate. Output constraints (traceability, no secrets, PROTOTYPE label). Forbidden actions per governance YAML.

#### 3.2 Agent: cd-validator

##### Official Frontmatter (F-04: `cd-validator.md`)

```yaml
---
name: cd-validator
description: >-
  API Contract Validator agent. Validates generated OpenAPI 3.1 specifications
  against the OpenAPI schema standard and verifies traceability from every API
  operation back to its source use case interaction step. Checks completeness
  (all interactions mapped), correctness (HTTP methods match request semantics),
  and standards compliance (valid OpenAPI structure). Requires both the
  generated contract file and the source use case artifact. Invoke when
  validating, checking, verifying, or auditing API contracts generated from
  use cases.
model: sonnet
tools:
  - Read
  - Glob
  - Grep
  - Bash
---
```

**Model Selection: Sonnet**

Justification (AD-M-009): Contract validation is a procedural, systematic activity. The agent follows a defined protocol (load contract, check schema compliance, verify traceability, count coverage). Sonnet handles structured verification tasks effectively. Haiku would be insufficient because the agent must interpret OpenAPI semantics and cross-reference against use case interaction structures.

**Tool Tier: T1 (Read-Only)**

Justification: Reads generated OpenAPI files and source UC artifacts; reads the OpenAPI 3.1 meta-schema for validation. Does not write output files in the primary validation path -- validation results are reported as structured output. When a validation report file is requested, the tool tier escalates to T2 for the report write. Given that cd-validator's primary deliverable is a validation report file (per output location pattern), T2 is the operational tier.

**Revised Tool Tier: T2 (Read-Write)**

The cd-validator produces a validation report file as its primary output. T2 is required.

```yaml
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
```

##### Governance YAML (F-05: `cd-validator.governance.yaml`)

```yaml
version: "1.0.0"
tool_tier: "T2"
# ET-M-001 compliance: reasoning_effort: high (C3 agent -- AE-002: touches skills/ governance)
reasoning_effort: high

identity:
  role: "API Contract Validator -- validates generated OpenAPI 3.1 specifications against schema standards and verifies traceability from every operation to source use case interaction"
  expertise:
    - "OpenAPI 3.1 schema validation (structural compliance, path/operation completeness, component reference integrity)"
    - "Contract-to-use-case traceability verification (operation-to-interaction mapping, coverage computation, gap identification)"
    - "API design standards compliance checking (RESTful conventions, HTTP method semantics, error response patterns)"
  cognitive_mode: "systematic"

persona:
  tone: "rigorous"
  communication_style: "structured"
  audience_level: "adaptive"

capabilities:
  forbidden_actions:
    - "P-003 VIOLATION: NEVER spawn recursive subagents or delegate to other agents via Task tool -- Consequence: agent hierarchy violation breaks orchestrator-worker topology and causes uncontrolled token consumption. cd-validator is a T2 worker agent without Task tool access."
    - "P-020 VIOLATION: NEVER override user decisions about validation scope, acceptance criteria, or which contracts to validate -- Consequence: unauthorized validation scope changes erode trust and may skip checks the user considers critical."
    - "P-022 VIOLATION: NEVER misrepresent validation results or traceability completeness -- Consequence: reporting a contract as valid when traceability gaps exist causes downstream implementers to build against an unverified specification."
    - "MODIFICATION VIOLATION: NEVER modify the generated contract file during validation -- Consequence: cd-validator is a read-only evaluator of contracts; modification is cd-generator's responsibility. Mixing evaluation with modification breaks the creator-critic separation."
  forbidden_action_format: "NPT-009-complete"
  output_formats:
    - "markdown"

guardrails:
  input_validation:
    - "Contract file must exist at specified path and contain valid YAML"
    - "Source use case artifact must exist and contain valid YAML frontmatter with $.interactions"
    - "Contract file must be an OpenAPI 3.1 specification (check openapi field)"
  output_filtering:
    - "no_secrets_in_output"
    - "validation_results_must_include_pass_fail_per_check"
    - "traceability_gaps_must_list_specific_interaction_ids"
    - "coverage_percentage_must_show_numerator_and_denominator"
  fallback_behavior: "escalate_to_user"

output:
  required: true
  location: "projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}-validation.md"
  levels:
    - "L0"
    - "L1"

constitution:
  reference: "docs/governance/JERRY_CONSTITUTION.md"
  principles_applied:
    - "P-001"
    - "P-002"
    - "P-003"
    - "P-020"
    - "P-022"

validation:
  post_completion_checks:
    - "verify_validation_report_created_at_output_location"
    - "verify_pass_fail_verdict_present"
    - "verify_traceability_matrix_present"
    - "verify_coverage_percentage_with_numerator_denominator"

session_context:
  on_receive:
    - "Load generated OpenAPI contract and source UC artifact"
    - "Verify both files exist before proceeding"
    - "Count interactions in UC artifact and operations in contract for coverage baseline"
  on_send:
    - "Report validation verdict (PASS/FAIL) with dimensional breakdown"
    - "Report traceability coverage percentage (mapped_operations / total_interactions)"
    - "List any unmapped interactions or invalid operations"

enforcement:
  tier: "medium"
  escalation_path: "eng-reviewer"
```

##### cd-validator Methodology Outline

| Step | Check Category | Verification |
|------|---------------|-------------|
| 1 | **Structural validity** | Contract YAML parses correctly; `openapi` field is "3.1.x"; `info`, `paths`, `components` sections present |
| 2 | **Path completeness** | Every `$.interactions[*]` where `actor_role = consumer` has a corresponding path+operation in the contract |
| 3 | **Operation correctness** | Each operation's HTTP method is semantically consistent with the source interaction's request_description |
| 4 | **Schema completeness** | Each operation has request body or parameters derived from interaction preconditions; each has response schemas derived from postconditions |
| 5 | **Error response mapping** | Extensions with `outcome = failure` that anchor to steps referenced by interactions produce corresponding 4xx/5xx responses |
| 6 | **Traceability** | Every operation carries `x-source-interaction` annotation; mapping document exists alongside contract |
| 7 | **PROTOTYPE label** | `x-prototype: true` present in `info` section |
| 8 | **Internal operations** | Interactions where `actor_role = provider` documented in `x-internal-operations`, not exposed as external paths |
| 9 | **IC-05 resolution** | Supporting actors referenced in interactions are documented in `components/schemas` descriptions |

---

### 4. Template Design

#### 4.1 F-10: openapi-template.yaml (Active)

The primary output template for `cd-generator`. Provides the structural scaffold for OpenAPI 3.1 output.

```yaml
# OpenAPI 3.1 Contract Template -- /contract-design skill
# Generated by cd-generator from use case realization artifacts
# Template version: 1.0.0

openapi: "3.1.0"
info:
  title: "{{UC_TITLE}} API Contract"
  version: "{{CONTRACT_VERSION}}"
  description: |
    API contract generated from use case {{UC_ID}} ({{UC_TITLE}}).
    Source artifact: {{UC_ARTIFACT_PATH}}
    Generated by: cd-generator ({{GENERATION_TIMESTAMP}})
    Transformation algorithm: UC-to-contract v1.0.0
  x-prototype: true
  x-source-use-case: "{{UC_ID}}"
  x-source-artifact: "{{UC_ARTIFACT_PATH}}"
  x-generated-by: "cd-generator"
  x-generated-at: "{{GENERATION_TIMESTAMP}}"
  x-scope: "{{UC_SCOPE}}"
  x-primary-actor: "{{PRIMARY_ACTOR}}"

paths:
  # One path group per identified resource
  # One operation per consumer interaction
  "{{RESOURCE_PATH}}":
    "{{HTTP_METHOD}}":
      operationId: "{{OPERATION_ID}}"
      summary: "{{INTERACTION_REQUEST_DESCRIPTION}}"
      description: |
        Source: Interaction {{INTERACTION_ID}} (step {{SOURCE_STEP}} in {{SOURCE_FLOW}})
        Actor role: {{ACTOR_ROLE}}
        System role: {{SYSTEM_ROLE}}
      x-source-interaction: "{{INTERACTION_ID}}"
      x-source-step: "{{SOURCE_STEP}}"
      x-source-flow: "{{SOURCE_FLOW}}"
      parameters: []
      # requestBody populated from interaction preconditions
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/{{REQUEST_SCHEMA_NAME}}"
      responses:
        "200":
          description: "{{INTERACTION_RESPONSE_DESCRIPTION}}"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/{{RESPONSE_SCHEMA_NAME}}"
        # Error responses derived from extensions anchored to this interaction's source step
        "{{ERROR_STATUS_CODE}}":
          description: "{{EXTENSION_CONDITION}}"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
          x-source-extension: "{{EXTENSION_ID}}"

components:
  schemas:
    # Request/response schemas derived from interaction pre/postconditions
    "{{REQUEST_SCHEMA_NAME}}":
      type: object
      description: "Request schema derived from {{INTERACTION_ID}} preconditions"
      properties: {}
    "{{RESPONSE_SCHEMA_NAME}}":
      type: object
      description: "Response schema derived from {{INTERACTION_ID}} postconditions"
      properties: {}
    ErrorResponse:
      type: object
      description: "Standard error response (derived from extension conditions)"
      properties:
        error:
          type: string
        code:
          type: string
        source_extension:
          type: string
          description: "Extension ID that generated this error response"

# Internal operations (interactions where actor_role = provider)
x-internal-operations:
  - interaction_id: "{{INTERNAL_INTERACTION_ID}}"
    source_step: "{{SOURCE_STEP}}"
    description: "{{INTERNAL_OPERATION_DESCRIPTION}}"
    supporting_actor: "{{SUPPORTING_ACTOR_NAME}}"
```

#### 4.2 F-11: asyncapi-template.yaml (Scaffolding -- Deferred)

```yaml
# AsyncAPI 3.0 Contract Template -- /contract-design skill
# Status: SCAFFOLDING (x-deferred: true)
# Deferred per DI-07, ASM-005, G-02 (multi-actor pub/sub mapping unresolved)
# Template version: 1.0.0

asyncapi: "3.0.0"
info:
  title: "{{UC_TITLE}} Async Contract"
  version: "{{CONTRACT_VERSION}}"
  description: |
    Async API contract template for use case {{UC_ID}}.
    DEFERRED: This template is structural scaffolding only.
    cd-generator v1.0.0 does not populate this template.
    Activation requires resolution of G-02 (multi-actor pub/sub mapping).
  x-deferred: true
  x-deferred-reason: "G-02: multi-actor pub/sub behavior mapping unresolved"
  x-activation-prerequisite: "Resolve G-02; extend cd-generator methodology steps 2-6 for event-driven patterns"
  x-source-use-case: "{{UC_ID}}"

channels:
  # Channels derived from interactions where actor_role = provider
  # and communication pattern is event-driven (publish/subscribe)
  "{{CHANNEL_NAME}}":
    description: "{{CHANNEL_DESCRIPTION}}"
    messages:
      "{{MESSAGE_NAME}}":
        $ref: "#/components/messages/{{MESSAGE_NAME}}"

components:
  messages:
    "{{MESSAGE_NAME}}":
      payload:
        $ref: "#/components/schemas/{{PAYLOAD_SCHEMA_NAME}}"
  schemas:
    "{{PAYLOAD_SCHEMA_NAME}}":
      type: object
      description: "Event payload derived from interaction postconditions"
      properties: {}
```

#### 4.3 F-12: cloudevents-template.yaml (Scaffolding -- Deferred)

```yaml
# CloudEvents 1.0 Contract Template -- /contract-design skill
# Status: SCAFFOLDING (x-deferred: true)
# Deferred per DI-07, ASM-005, G-02
# Template version: 1.0.0

# CloudEvents Specification: https://cloudevents.io/
# CloudEvents defines a standard envelope; this template defines the
# type registry and data schema mapping for use case-derived events.

x-deferred: true
x-deferred-reason: "G-02: multi-actor pub/sub behavior mapping unresolved"
x-activation-prerequisite: "Resolve G-02; define interaction-to-event-type mapping rules"
x-source-use-case: "{{UC_ID}}"

event_types:
  # Each event type derived from an interaction where the system publishes state changes
  - type: "{{DOMAIN}}.{{UC_SLUG}}.{{EVENT_NAME}}"
    source: "{{SYSTEM_SCOPE}}"
    specversion: "1.0"
    description: "{{EVENT_DESCRIPTION}}"
    datacontenttype: "application/json"
    dataschema: "#/schemas/{{EVENT_SCHEMA_NAME}}"
    x-source-interaction: "{{INTERACTION_ID}}"
    x-source-step: "{{SOURCE_STEP}}"

schemas:
  "{{EVENT_SCHEMA_NAME}}":
    type: object
    description: "Event data schema derived from interaction postconditions"
    properties: {}
```

#### 4.4 F-13: json-schema-template.json (Active)

The JSON Schema template provides the shared `components/schemas` definitions used by both the OpenAPI template and (when activated) the AsyncAPI and CloudEvents templates. This template is active in v1.0.0 because request/response schema generation is part of the core OpenAPI workflow.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "{{SCHEMA_ID}}",
  "title": "{{UC_TITLE}} Data Schemas",
  "description": "JSON Schema definitions generated from use case {{UC_ID}} interaction pre/postconditions. Source: {{UC_ARTIFACT_PATH}}. Generated by cd-generator.",
  "x-prototype": true,
  "x-source-use-case": "{{UC_ID}}",
  "x-generated-by": "cd-generator",
  "x-generated-at": "{{GENERATION_TIMESTAMP}}",
  "$defs": {
    "{{REQUEST_SCHEMA_NAME}}": {
      "type": "object",
      "description": "Request schema for {{INTERACTION_ID}} (derived from preconditions: {{PRECONDITIONS_SUMMARY}})",
      "x-source-interaction": "{{INTERACTION_ID}}",
      "properties": {},
      "required": []
    },
    "{{RESPONSE_SCHEMA_NAME}}": {
      "type": "object",
      "description": "Response schema for {{INTERACTION_ID}} (derived from postconditions: {{POSTCONDITIONS_SUMMARY}})",
      "x-source-interaction": "{{INTERACTION_ID}}",
      "properties": {},
      "required": []
    },
    "ErrorResponse": {
      "type": "object",
      "description": "Standard error response envelope (derived from extension conditions)",
      "properties": {
        "error": { "type": "string", "description": "Human-readable error message" },
        "code": { "type": "string", "description": "Machine-readable error code" },
        "source_extension": { "type": "string", "description": "Extension ID that generated this error" }
      },
      "required": ["error", "code"]
    }
  }
}
```

#### 4.5 F-14: uc-to-contract-rules.md Content Specification

The rule file encodes the novel UC-to-contract transformation algorithm as imperative rules, following the pattern of `skills/test-spec/rules/clark-transformation-rules.md`. Sections:

| Section | Content |
|---------|---------|
| Resource Identification Rules | RULE-RI-01 through RULE-RI-03: how to identify API resources from interaction receiver descriptions |
| Operation Mapping Rules | RULE-OM-01 through RULE-OM-04: how to map interaction steps to API operations |
| HTTP Method Inference Rules | RULE-HM-01 through RULE-HM-05: how to derive HTTP methods from request_description semantics |
| Schema Derivation Rules | RULE-SD-01 through RULE-SD-04: how to extract request/response schemas from pre/postconditions |
| Error Response Rules | RULE-ER-01 through RULE-ER-03: how to map extension conditions to HTTP error codes |
| Actor Role Rules | RULE-AR-01 through RULE-AR-03: how to classify interactions by actor role and IC-05 resolution |
| Traceability Rules | RULE-TR-01 through RULE-TR-02: how to annotate every operation with source interaction |

Each rule follows the format:
```
RULE-{CATEGORY}-{NN}: {imperative statement}
  Input: {schema fields read}
  Output: {OpenAPI element produced}
  Example: {concrete mapping example}
```

---

### 5. Shared Schema Integration

#### Input Validation Gate (Two-Layer)

**Layer 1 -- JSON Schema Structural Validation:**

The UC artifact is validated against `docs/schemas/use-case-realization-v1.schema.json`. This catches structural defects (missing required fields, type mismatches, pattern violations). Schema allOf constraint 1 enforces `$.interactions` presence when `$.realization_level = INTERACTION_DEFINED`.

**Layer 2 -- Agent Guardrail Semantic Validation (cd-generator):**

| Check | Action on Failure |
|-------|------------------|
| `$.interactions` absent or empty | REJECT: "UC {id} has no interactions block. Use /use-case (uc-slicer Activity 5) to identify system boundaries and interaction points first." |
| `$.detail_level < ESSENTIAL_OUTLINE` | REJECT: "UC {id} is at {detail_level}. Contract derivation requires ESSENTIAL_OUTLINE or FULLY_DESCRIBED." |
| Any `$.interactions[*]` missing `request_description` or `response_description` | REJECT: "UC {id} interaction {INT-nn} missing request/response description. Both are required for OpenAPI operation generation." |
| Any `$.interactions[*]` missing `source_step` or `source_flow` | REJECT: "UC {id} interaction {INT-nn} missing source_step or source_flow. Traceability from contract to use case step is required." |
| Any `$.interactions[*].source_step` not found in referenced flow | REJECT: "UC {id} interaction {INT-nn} references step {source_step} in {source_flow}, but that step does not exist. Verify the interactions block was derived from current flows." |
| Any `$.interactions[*]` missing `actor_role` or `system_role` | REJECT: "UC {id} interaction {INT-nn} missing actor_role or system_role. Both are required to determine OpenAPI operation directionality." |
| `$.supporting_actors` absent | WARN: "UC {id} has no supporting_actors. IC-05 cross-referencing will be limited. Consider adding supporting actors via /use-case." (Proceed.) |

---

### 6. Cross-Skill Integration Model

#### Pipeline Position

```
/use-case            /test-spec           /contract-design
    |                    |                     |
uc-author ---+      tspec-generator        cd-generator
             |           ^                     ^
uc-slicer ---+           |                     |
             |           |                     |
             v           |                     |
    [UC Artifact]--------+---------------------+
    (shared-schema.json validated)
         |
    Schema Gates:
    - /test-spec requires: $.detail_level >= ESSENTIAL_OUTLINE
    - /contract-design requires: $.realization_level = INTERACTION_DEFINED
                                 $.interactions non-empty
```

**Key property:** `/contract-design` is a read-only consumer of the UC artifact. It never modifies the source artifact. All output goes to separate files in `projects/${JERRY_PROJECT}/contracts/`.

#### P-003 Agent Topology

```
MAIN CONTEXT (orchestrator)
    |
    +-- cd-generator (T2 worker) -- via Task tool
    |   Reads: UC artifact (.md with YAML frontmatter)
    |          docs/schemas/use-case-realization-v1.schema.json
    |          skills/contract-design/rules/uc-to-contract-rules.md
    |          skills/contract-design/templates/openapi-template.yaml
    |          skills/contract-design/templates/json-schema-template.json
    |   Writes: OpenAPI contract (.openapi.yaml)
    |           Mapping document (-mapping.md)
    |
    +-- cd-validator (T2 worker) -- via Task tool
        Reads: OpenAPI contract (.openapi.yaml) -- produced by cd-generator
               UC artifact (.md) -- same source artifact
               Mapping document (-mapping.md)
        Writes: Validation report (-validation.md)

Workers do NOT invoke each other.
cd-generator output (OpenAPI + mapping) is consumed by cd-validator via filesystem.
Cross-agent data flow is mediated by shared artifact files on disk (P-003 compliant).
```

#### Handoff Data (orchestrator to cd-generator)

| Field | Value |
|-------|-------|
| `artifact_path` | `projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md` |
| `realization_level` | `INTERACTION_DEFINED` |
| `interaction_count` | Count of `$.interactions[*]` entries |
| `success_criteria` | At least 1 OpenAPI path+operation per consumer interaction; mapping document with traceability; x-prototype: true |

#### Handoff Data (orchestrator to cd-validator)

| Field | Value |
|-------|-------|
| `contract_path` | `projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}.openapi.yaml` |
| `artifact_path` | `projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md` |
| `mapping_path` | `projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}-mapping.md` |
| `success_criteria` | PASS verdict on all 9 validation checks; traceability coverage = 100% of consumer interactions |

---

### 7. Contract Type Mapping

This section defines how each UC artifact field maps to each contract type. This is the /contract-design equivalent of the Clark transformation table in /test-spec.

#### 7.1 UC Interaction-to-OpenAPI Mapping (Active)

| UC Schema Field | JSON Path | OpenAPI Element | Cardinality | Rule |
|----------------|-----------|-----------------|-------------|------|
| UC Title | `$.title` | `info.title` | 1:1 | RULE-RI-01 |
| UC Scope | `$.scope` | `info.x-scope` | 1:1 | RULE-RI-01 |
| Primary actor | `$.primary_actor` | `info.x-primary-actor` (API consumer role) | 1:1 | RULE-AR-01 |
| Interaction (consumer -> system) | `$.interactions[*]` where `.actor_role = consumer` | Path + Operation (external endpoint) | 1:1 per interaction | RULE-OM-01 |
| Interaction (system -> system) | `$.interactions[*]` where `.actor_role = provider` | `x-internal-operations` entry (not exposed as path) | 1:1 per interaction | RULE-OM-02 |
| Interaction request_description | `$.interactions[*].request_description` | Operation summary + HTTP method inference | 1:1 | RULE-HM-01 |
| Interaction response_description | `$.interactions[*].response_description` | 200 response description | 1:1 | RULE-SD-02 |
| Interaction preconditions | `$.interactions[*].preconditions[*]` | Request body schema properties / query parameters | 1:N | RULE-SD-01 |
| Interaction postconditions | `$.interactions[*].postconditions[*]` | Response schema properties | 1:N | RULE-SD-02 |
| Interaction source_step + source_flow | `$.interactions[*].source_step`, `.source_flow` | `x-source-interaction`, `x-source-step`, `x-source-flow` annotations | 1:1 | RULE-TR-01 |
| Extension (failure outcome) | `$.extensions[*]` where `.outcome = failure` | Error response (4xx/5xx) on operations whose source_step matches extension anchor_step | 1:N | RULE-ER-01 |
| Extension (success outcome) | `$.extensions[*]` where `.outcome = success` | Alternative success response (optional 2xx variant) | 1:1 | RULE-ER-02 |
| Supporting actor (external system) | `$.supporting_actors[*]` cross-referenced with interactions | `components/schemas` description documenting external dependency | 1:1 | RULE-AR-03 |

#### 7.2 HTTP Method Inference Rules

| Request Description Pattern | Inferred HTTP Method | Confidence | Rule |
|---------------------------|---------------------|------------|------|
| read, query, get, fetch, retrieve, look up, search, list, find | GET | High | RULE-HM-01 |
| create, add, submit, register, initiate, start, send, post | POST | High | RULE-HM-02 |
| update, modify, change, edit, set, replace | PUT or PATCH | Medium (PUT for full replace, PATCH for partial) | RULE-HM-03 |
| delete, remove, cancel, revoke, deactivate, terminate | DELETE | High | RULE-HM-04 |
| Ambiguous (does not match patterns above) | POST (default) + WARN | Low | RULE-HM-05 |

When confidence is "Medium" or "Low", `cd-generator` annotates the operation with `x-method-inference: {confidence}` and the matched pattern. `cd-validator` flags these for human review.

#### 7.3 Extension-to-Error-Response Mapping

| Extension Pattern | HTTP Status | Error Category | Rule |
|------------------|-------------|----------------|------|
| `outcome = failure` AND condition implies invalid input | 400 Bad Request | Client error -- malformed request | RULE-ER-01a |
| `outcome = failure` AND condition implies unauthorized | 401 Unauthorized or 403 Forbidden | Client error -- access control | RULE-ER-01b |
| `outcome = failure` AND condition implies not found | 404 Not Found | Client error -- resource absence | RULE-ER-01c |
| `outcome = failure` AND condition implies conflict/duplicate | 409 Conflict | Client error -- state conflict | RULE-ER-01d |
| `outcome = failure` AND condition implies system/internal error | 500 Internal Server Error | Server error | RULE-ER-01e |
| `outcome = failure` AND condition does not match patterns above | 422 Unprocessable Entity (default) + WARN | Unclassified error | RULE-ER-01f |

The extension condition text is analyzed for semantic patterns ("invalid", "unauthorized", "not found", "already exists", "timeout", "unavailable"). When pattern matching is inconclusive, the default 422 status is used with a `x-error-inference: low` annotation.

#### 7.4 UC Interaction-to-AsyncAPI Mapping (Deferred -- G-02)

| UC Schema Field | AsyncAPI Element | Status |
|----------------|-----------------|--------|
| Interactions where system publishes | Channels | DEFERRED |
| Event payload from postconditions | Message payload schema | DEFERRED |
| Actor role = provider | Publish operation | DEFERRED |

**Activation prerequisite:** Resolve G-02 (multi-actor pub/sub behavior mapping). Extend `cd-generator` methodology steps 2-6 with event-driven patterns. Estimate: schema v1.1.0 bump to add optional `async_interactions` block.

#### 7.5 UC Interaction-to-CloudEvents Mapping (Deferred -- G-02)

| UC Schema Field | CloudEvents Element | Status |
|----------------|-------------------|--------|
| Interaction where system changes state | Event type | DEFERRED |
| UC scope | Event source | DEFERRED |
| Postconditions | Event data | DEFERRED |

**Activation prerequisite:** Same as AsyncAPI. CloudEvents defines the envelope; AsyncAPI defines the channel. Both require G-02 resolution.

---

### 8. Threat Model

#### Trust Boundaries

```
+--------------------------------------------------+
|                   Jerry Framework                 |
|                                                   |
|  +-------------+    +---------------------------+ |
|  | /use-case   |    | /contract-design          | |
|  | (uc-slicer) |    |                           | |
|  |             |    |  TB-1: Input Boundary      | |
|  |  Produces   |--->|  UC artifact validation    | |
|  |  interactions|    |                           | |
|  +-------------+    |  cd-generator              | |
|                     |  (convergent, opus, T2)    | |
|                     |         |                  | |
|                     |         v                  | |
|                     |  TB-2: Output Boundary     | |
|                     |  Contract file generation  | |
|                     |         |                  | |
|                     |         v                  | |
|                     |  cd-validator              | |
|                     |  (systematic, sonnet, T2)  | |
|                     +---------------------------+ |
|                              |                    |
+------------------------------+--------------------+
                               |
                    TB-3: External Consumption
                    Implementers, code generators,
                    API gateways consume contracts
```

#### STRIDE Analysis per Trust Boundary

| TB | Threat | STRIDE Category | Risk | Mitigation |
|----|--------|----------------|------|------------|
| TB-1 | Malformed UC artifact with crafted interaction descriptions designed to inject OpenAPI directives | Tampering | Medium | Two-layer input validation gate. YAML frontmatter parsed separately from Markdown body. Schema validation rejects structural anomalies. |
| TB-1 | UC artifact at incorrect realization level passed to cd-generator | Elevation of Privilege | Low | Schema allOf constraint 1 enforces interactions presence. Agent guardrail rejects artifacts below ESSENTIAL_OUTLINE. |
| TB-1 | UC artifact with `source_step` references pointing to non-existent steps | Spoofing | Medium | Agent guardrail performs cross-reference validation (each source_step must resolve to an existing flow step). |
| TB-2 | Generated OpenAPI includes secrets from UC artifact | Information Disclosure | Low | Output filtering guardrail: `no_secrets_in_output`. cd-generator scans for patterns resembling API keys, tokens, passwords in generated content. |
| TB-2 | Generated OpenAPI carries `x-prototype: false` bypassing review | Repudiation | Low | Agent guardrail enforces `x-prototype: true`. cd-validator checks presence. |
| TB-2 | Generated contract omits error responses, creating false sense of completeness | Denial of Service (to downstream) | Medium | Extension-to-error-response mapping (RULE-ER-01). cd-validator checks that extensions anchored to interaction steps produce error responses. |
| TB-3 | External consumers treat PROTOTYPE contract as production-ready | Elevation of Privilege | High | `x-prototype: true` in info section. Mapping document explicitly states PROTOTYPE status. cd-validator flags absence as validation failure. |
| TB-3 | Code generators consume malformed OpenAPI producing insecure stubs | Tampering | Medium | cd-validator checks OpenAPI 3.1 structural compliance before contract is considered ready for consumption. |

#### DREAD Scoring (Top 3 Threats)

| Threat | Damage | Reproducibility | Exploitability | Affected Users | Discoverability | DREAD Score |
|--------|--------|-----------------|----------------|----------------|-----------------|-------------|
| External consumers treat PROTOTYPE as production-ready | 3 (incorrect API implementation) | 3 (every contract has this risk) | 2 (requires ignoring x-prototype) | 3 (all downstream implementers) | 3 (visible in contract header) | 14/25 |
| UC artifact with crafted interaction descriptions | 2 (incorrect contract structure) | 2 (requires specific crafting) | 1 (UC artifacts are internal) | 2 (contract consumers) | 2 (requires understanding the pipeline) | 9/25 |
| Generated contract omits error responses | 2 (missing error handling) | 2 (depends on extension coverage) | 1 (requires missing extensions) | 3 (all implementers of affected endpoints) | 2 (cd-validator catches this) | 10/25 |

#### NIST CSF 2.0 Mapping

| CSF Function | Application |
|-------------|-------------|
| **Identify** | Input validation gate identifies UC artifacts that are insufficiently realized. Trust boundary analysis identifies 3 boundary crossings. |
| **Protect** | Two-layer validation prevents malformed input. PROTOTYPE labeling prevents premature production use. T2 tool tier limits agent capabilities to read/write only. |
| **Detect** | cd-validator detects traceability gaps, structural defects, and missing PROTOTYPE labels. Post-completion checks provide deterministic detection. |
| **Respond** | Actionable rejection messages guide users to remediation (/use-case for elaboration). Escalate-to-user fallback for ambiguous failures. |
| **Recover** | Generated contracts are separate files (not modifications to source UC). Regeneration from corrected UC artifact restores correct state. |

---

### 9. Risk Register

| ID | Risk | Probability | Impact | Mitigation | Residual Risk |
|----|------|-------------|--------|------------|---------------|
| R-01 | UC-to-contract algorithm produces incorrect operation mapping (G-01 -- no prior art) | High | High | PROTOTYPE labeling (x-prototype: true). cd-validator traceability checks. Interactions block validation gate (3-UC criterion). Human review mandatory before PROTOTYPE removal. | Medium -- novel algorithm inherently produces uncertain output until validated against real use cases |
| R-02 | HTTP method inference from request_description text is unreliable for ambiguous descriptions | Medium | Medium | Confidence annotations (x-method-inference). cd-validator flags low-confidence inferences. Escalate to user for disambiguation. Default POST with WARN for unclassified. | Low -- human review catches misclassifications |
| R-03 | Schema derivation from natural language preconditions/postconditions produces incomplete schemas | High | Medium | cd-generator marks schemas with x-prototype: true. Property lists are derived from explicit condition text only (no invention). cd-validator checks schema presence but cannot verify semantic completeness. | Medium -- schema completeness depends on UC artifact quality |
| R-04 | AsyncAPI/CloudEvents templates remain unused (deferred scope never activated) | Medium | Low | Templates exist as documentation of intended architecture. No maintenance burden while deferred. Activation requires explicit ADR per G-02 resolution. | Low -- no operational impact |
| R-05 | cd-validator passes structurally valid but semantically incorrect contracts | Medium | Medium | cd-validator checks structural compliance and traceability. Semantic correctness (does this API operation actually represent the intended behavior?) requires human review. PROTOTYPE label prevents consumption without review. | Medium -- semantic review remains a human responsibility |
| R-06 | Opus model cost for cd-generator is disproportionate to value | Low | Low | Monitor quality scores. If consistently above 0.95 after 10+ runs, evaluate Sonnet as replacement. Model selection is justified by G-01 complexity. | Low -- model downgrade path exists |

---

## L2: Strategic Implications

### Long-Term Architecture Evolution

| Milestone | Change | Effort | Schema Impact |
|-----------|--------|--------|--------------|
| Phase 3 prototype validation | Run 3 UC -> OpenAPI transformations to validate interactions block | Medium | None (validation only) |
| AsyncAPI activation (G-02 resolved) | Extend cd-generator methodology for event-driven patterns; activate asyncapi-template.yaml | High | Schema v1.1.0 (add `async_interactions` block) |
| CloudEvents activation (G-02 resolved) | Extend cd-generator for event type registry; activate cloudevents-template.yaml | Medium | Shared with AsyncAPI schema change |
| GraphQL support | New template + methodology extension for query/mutation mapping | High | Schema v1.2.0 (add `query_interactions` block) |
| cd-generator model downgrade | Sonnet replaces Opus if quality scores consistent | Low | None |
| Automated contract testing | Integration with Pact or similar contract testing framework | Medium | None (consumes OpenAPI output) |

### Security Posture Trade-offs

| Decision | Security Benefit | Security Cost | Accepted? |
|----------|-----------------|---------------|-----------|
| PROTOTYPE labeling mandatory | Prevents premature production deployment | Requires explicit human action to remove label | Yes -- cost is minimal (one label removal), benefit is significant (prevents false confidence) |
| T2 (not T3) for both agents | No external data can contaminate contracts | Cannot validate against external OpenAPI registries | Yes -- contracts should be derived from UC artifacts only; external validation is a separate workflow |
| Agent guardrail (not schema) for semantic checks | More flexible than JSON Schema for cross-reference validation | Less deterministic than schema enforcement | Yes -- JSON Schema cannot express cross-array referential integrity |
| Two agents (not one) | Creator-critic separation for contract quality | Coordination overhead between generation and validation | Yes -- validation as a separate pass catches issues that self-review misses |

### Cross-Skill Pipeline Implications

The three-skill pipeline (`/use-case` -> `/test-spec` + `/contract-design`) establishes a pattern for Jerry's requirements-to-implementation workflow:

1. **Shared artifact as integration contract.** The `use-case-realization-v1.schema.json` serves as the single integration point. Adding new downstream skills (e.g., a future `/architecture-design` skill) requires only: (a) defining which schema fields the new skill reads, (b) adding agent guardrails for minimum input requirements, (c) producing separate output files. No changes to existing skills.

2. **Parallel consumer execution.** `/test-spec` and `/contract-design` can execute in parallel against the same UC artifact because both are read-only consumers. This parallelism scales to additional consumers without coordination overhead.

3. **Progressive realization as pipeline gate.** The realization level enum (`OUTLINED`, `STORY_DEFINED`, `INTERACTION_DEFINED`) serves as a pipeline readiness indicator. Each downstream skill declares its minimum realization level requirement. The orchestrator can check the current level before invoking downstream skills.

---

## ORCHESTRATION.yaml Reconciliation

The ORCHESTRATION.yaml (skills registry section) lists:

```yaml
- id: "contract-design"
  route: "/contract-design"
  agents: ["contract-generator", "contract-validator"]
  skill_dir: "skills/contract-design/"
  status: "pending"
```

The Phase 2 architecture (SSOT: agent-decomposition.md v1.1.0, 0.963 PASS) defines agent names with the `cd-` prefix convention to maintain consistency across all three skills.

| ORCHESTRATION.yaml Name | Architecture (SSOT) Name | Reconciliation |
|------------------------|-------------------------|----------------|
| `contract-generator` | `cd-generator` | Use SSOT name. `cd-` prefix follows the established naming convention (`uc-` for /use-case, `tspec-` for /test-spec, `cd-` for /contract-design). Agent file: `cd-generator.md`. |
| `contract-validator` | `cd-validator` (new -- split justified in Section 3) | Use SSOT prefix convention. Phase 2 defined 1 agent; this architecture introduces the split per the ORCHESTRATION.yaml's anticipated 2-agent structure. Agent file: `cd-validator.md`. |

The ORCHESTRATION.yaml deliverable list includes 4 template files. All 4 are delivered per the manifest:
- `openapi-template.yaml` -- Active (cd-generator populates in v1.0.0)
- `asyncapi-template.yaml` -- Scaffolding (deferred per DI-07, G-02)
- `cloudevents-template.yaml` -- Scaffolding (deferred per DI-07, G-02)
- `json-schema-template.json` -- Active (shared schema definitions)

---

## References

| File | Purpose |
|------|---------|
| `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/architecture/file-organization.md` | Phase 2: file organization, shared artifact format (R-01), directory structure |
| `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/architecture/agent-decomposition.md` | Phase 2: agent decomposition (SSOT), cd-generator specification, trigger map extensions |
| `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/architecture/frontmatter-schema.md` | Phase 2: JSON Schema specification, interactions block definition |
| `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/architecture/shared-schema.json` | JSON Schema Draft 2020-12 for UC realization documents |
| `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/implementation/step-9-use-case-architecture.md` | Step 9: /use-case architecture (pipeline origin skill) |
| `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/implementation/step-10-test-spec-architecture.md` | Step 10: /test-spec architecture (sibling pattern reference) |
| `skills/test-spec/SKILL.md` | Completed /test-spec skill (sibling reference) |
| `skills/test-spec/agents/tspec-generator.md` | tspec-generator agent (structural pattern reference) |
| `skills/test-spec/agents/tspec-generator.governance.yaml` | Governance YAML pattern reference |
| `.context/rules/agent-development-standards.md` | H-34 dual-file architecture, tool tiers, cognitive modes |
| `.context/rules/skill-standards.md` | H-25/H-26 skill naming and structure |
| `.context/rules/quality-enforcement.md` | Quality gate, criticality levels |
| `.context/rules/agent-routing-standards.md` | Trigger map format, circuit breaker, routing algorithm |
| `docs/schemas/use-case-realization-v1.schema.json` | Production JSON Schema location (Phase 3) |
| `docs/schemas/agent-governance-v1.schema.json` | Governance YAML schema (reference for H-34 compliance) |
| OpenAPI Specification 3.1.0 | https://spec.openapis.org/oas/v3.1.0 |
| AsyncAPI Specification 3.0.0 | https://www.asyncapi.com/docs/reference/specification/v3.0.0 |
| CloudEvents Specification 1.0.2 | https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md |
| Jacobson, I. et al. (2011) | Use-Case 2.0: The Guide to Succeeding with Use Cases |
| Larman, C. (2004) | Applying UML and Patterns, Ch. 18: System Sequence Diagrams to Operation Contracts |

---

## Self-Review Checklist (H-15, S-010)

- [x] **P-001 (Truth/Accuracy):** Every mapping rule traces to a specific schema field or Phase 2 architecture decision. HTTP method inference rules cite observable semantic patterns. No invented mappings.
- [x] **P-002 (File Persistence):** Output persisted to `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/implementation/step-11-contract-design-architecture.md`.
- [x] **P-003 (No Recursive Subagents):** Both cd-generator and cd-validator are T2 worker agents. Neither has Task tool in allowed tools. P-003 topology diagram included.
- [x] **P-004 (Provenance):** All Phase 2 documents cited with version numbers and quality scores. Cross-references to agent-decomposition.md, frontmatter-schema.md, file-organization.md, shared-schema.json.
- [x] **P-011 (Evidence-Based):** Agent split justified against Pattern 1 criteria with methodology token counts. ORCHESTRATION.yaml reconciliation documented with rationale. HTTP method inference backed by RESTful convention patterns.
- [x] **P-020 (User Authority):** Status is PROPOSED, not ACCEPTED. All deferred scope (AsyncAPI, CloudEvents) documented with activation prerequisites requiring user approval.
- [x] **P-022 (No Deception):** G-01 (no prior art) acknowledged explicitly. PROTOTYPE labeling mandated. Deferred scope clearly marked (x-deferred: true). HTTP method inference confidence levels disclosed (High/Medium/Low). R-01 risk rated High probability.
- [x] **H-23 (Navigation):** Navigation table present with anchor links to all major sections.
- [x] **H-25 (Skill Naming):** `contract-design` is kebab-case, matches SKILL.md `name` field. SKILL.md exact case. No README.md in skill folder.
- [x] **H-26 (Skill Registration):** Description includes WHAT (API contract generation from UC artifacts) + WHEN (realization_level = INTERACTION_DEFINED) + trigger phrases (OpenAPI, API contract, contract design). Under 1024 chars. No XML tags. Registration entries for CLAUDE.md and mandatory-skill-usage.md documented in routing section.
- [x] **H-34 (Agent Definition):** Dual-file architecture (cd-generator.md + cd-generator.governance.yaml, cd-validator.md + cd-validator.governance.yaml). Constitutional triplet (P-003, P-020, P-022) in principles_applied. 5+ forbidden_actions in NPT-009 format. Tool tier justified (T2 for both).
- [x] **L0/L1/L2:** All three output levels present with appropriate audience depth.
- [x] **Step 10 pattern consistency:** File manifest, agent definition format, governance YAML structure, template design, integration model, and threat model follow the established pattern from step-10-test-spec-architecture.md.
- [x] **ORCHESTRATION.yaml reconciliation:** Agent name mapping (contract-generator -> cd-generator, contract-validator -> cd-validator) documented with rationale. All 4 template deliverables accounted for.
- [x] **Phase 2 traceability:** cd-generator specification maps to agent-decomposition.md Skill 3 section. All schema fields, guardrails, and methodology steps trace to DI-07, DI-08, R-06, G-01, G-02, IC-05, ASM-005, LES-001.
- [x] **Threat model:** 3 trust boundaries, 8 STRIDE threats, DREAD scoring for top 3, NIST CSF 2.0 mapping to all 5 functions.
- [x] **Risk register:** 6 risks with probability/impact ratings, mitigations, and residual risk assessments.

### Adversarial Self-Check (S-002: Devil's Advocate)

**Challenge 1: "Is the 2-agent split justified when the Phase 2 architecture defines 1 agent?"**
The Phase 2 architecture explicitly anticipated this possibility ("If methodology section exceeds 1,500 tokens during Phase 3, split"). The ORCHESTRATION.yaml independently lists 2 agents. The methodology token analysis shows ~1,400 tokens for generation alone, ~1,300 tokens for validation, total ~2,700 tokens -- well above the 1,500-token threshold. The cognitive mode difference (convergent for generation vs. systematic for validation) provides additional justification per Pattern 1 split criteria.

**Challenge 2: "Should the deferred templates (AsyncAPI, CloudEvents) be omitted entirely rather than delivered as scaffolding?"**
The ORCHESTRATION.yaml lists all 4 templates as Step 11 deliverables. Omitting 2 would create a deliverable gap requiring ORCHESTRATION.yaml revision (an AE-003 auto-C3 change). Delivering scaffolding satisfies the deliverable requirement while being honest about scope (x-deferred: true). The scaffolding also documents the intended future architecture, serving as design documentation for when G-02 is resolved.

**Challenge 3: "Is Opus justified for cd-generator given the cost?"**
The Phase 2 architecture selected Opus with explicit justification (G-01 gap, complex reasoning, no procedural template). This architecture preserves that selection and adds a downgrade path (monitor quality scores; if consistently > 0.95 after 10+ runs, evaluate Sonnet). The novel algorithm's judgment requirements (resource identification, HTTP method inference, schema structure) exceed Sonnet's typical systematic-mode capabilities. The cost is bounded by the low invocation frequency (once per UC realization).

### Pre-Mortem (S-004): "It's 6 months later and this architecture failed -- why?"

**Failure Mode 1 (highest probability): The UC-to-contract transformation algorithm produces incorrect mappings.**
Signal: cd-validator consistently reports traceability gaps or semantically incorrect operations. Quality scores below 0.85.
Mitigation: PROTOTYPE labeling prevents production use. Algorithm rules are in a separate file (uc-to-contract-rules.md) that can be revised without restructuring the agent. Interactions block validation gate (3-UC criterion from Phase 2) catches fundamental design flaws before broad deployment.

**Failure Mode 2: HTTP method inference is too unreliable for natural language descriptions.**
Signal: > 30% of operations carry `x-method-inference: low` annotations. Users override method assignments manually more often than not.
Mitigation: Add a `http_method` field to the interaction schema definition (schema v1.1.0 minor bump). Let uc-slicer capture method intent during Activity 5 realization, removing the inference burden from cd-generator.

**Failure Mode 3: The 2-agent split was unnecessary -- cd-validator is invoked < 20% of the time.**
Signal: Users skip validation or rely solely on cd-generator's self-review.
Mitigation: Track invocation frequency. If cd-validator usage < 20% after 30 contract generations, merge validation logic back into cd-generator as a post-generation verification step. The merge is low-cost because both agents share the same T2 toolset and read the same input files.

---

*Architecture Version: 1.0.0*
*Constitutional Compliance: P-001 (truth), P-002 (file persistence), P-003 (no recursive subagents), P-004 (provenance), P-011 (evidence-based), P-020 (user authority -- PROPOSED status), P-022 (no deception -- G-01 acknowledged, PROTOTYPE labeling, deferred scope disclosed, confidence levels on inference)*
*Adversary Review Required: YES -- C4 all-10-strategy review at >= 0.95 threshold*
*Next Agent: adv-scorer (initial scoring)*
*Workflow ID: use-case-skills-20260308-001*
