# Agent Decomposition Architecture: /use-case, /test-spec, /contract-design

> **PS ID:** proj-021 | **Entry ID:** architecture-agent-decomposition | **Workflow ID:** use-case-skills-20260308-001
> **Date:** 2026-03-08 | **Agent:** ps-architect | **Execution Group:** Phase 2 Architecture (Step 8-draft)
> **Quality Threshold:** >= 0.95 (C4, user override C-008)
> **Status:** PROPOSED (per P-020 -- user authority required for acceptance)
> **Version:** 1.0.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Agent counts, rationale, and key design choices for all stakeholders |
| [L1: Technical Specifications](#l1-technical-specifications) | Per-agent specs, interaction model, trigger map extensions |
| [L2: Architectural Implications](#l2-architectural-implications) | Design rationale, cognitive mode analysis, risk assessment, evolution path |
| [Agent Inventory Summary](#agent-inventory-summary) | Quick-reference table of all agents across 3 skills |
| [Skill 1: /use-case](#skill-1-use-case) | 2 agents: uc-author, uc-slicer |
| [Skill 2: /test-spec](#skill-2-test-spec) | 1 agent: ts-generator |
| [Skill 3: /contract-design](#skill-3-contract-design) | 1 agent: cd-generator |
| [Agent Interaction Model](#agent-interaction-model) | Intra-skill and cross-skill interaction patterns |
| [Trigger Map Extensions](#trigger-map-extensions) | New keywords, negative keywords, compound triggers for all 3 skills |
| [Options Evaluated](#options-evaluated) | Alternatives considered per P-011 with trade-off analysis |
| [Risk Assessment](#risk-assessment) | Per-skill risk analysis with mitigations |
| [Traceability Matrix](#traceability-matrix) | Map to synthesis DI-01 through DI-12 and R-01 through R-10 |
| [Self-Review Checklist](#self-review-checklist) | H-15, S-010 pre-submission verification |

---

## L0: Executive Summary

We are designing the agent decomposition for three new Jerry skills that implement Ivar Jacobson's Use Case 2.0 methodology as a pipeline: `/use-case` creates use case artifacts, `/test-spec` derives BDD test specifications from those artifacts, and `/contract-design` generates API contracts from them.

**Agent count decision:** We propose a total of 4 agents across 3 skills:

| Skill | Agent Count | Agents | Rationale |
|-------|-------------|--------|-----------|
| `/use-case` | 2 | `uc-author`, `uc-slicer` | Two distinct cognitive modes required: authoring is integrative (exploring use case structure, combining stakeholder input); slicing is systematic (applying Jacobson's mechanical slicing patterns). This triggers the 2-cognitive-mode split criterion from `agent-development-standards.md` Pattern 1. |
| `/test-spec` | 1 | `ts-generator` | Single cognitive mode (systematic): Clark's UC2.0-to-Gherkin mapping is a deterministic lookup, not creative generation. One methodology, one mode, one agent. |
| `/contract-design` | 1 | `cd-generator` | Single cognitive mode (convergent): the novel UC-to-contract transformation evaluates interaction steps and converges on contract structures. Despite being the highest-risk skill, the transformation is a single-pass algorithm, not multi-step requiring separate agents. |

**Why this matters:** Starting with 4 agents (not 1 per skill, not the 8+ from the orchestration plan Phase 3 target) balances two competing forces. The synthesis unanimously recommends progressive complexity (PAT-001, PAT-009, ET-02) -- meaning we should not pre-build agents we might not need. But the synthesis also identifies that `/use-case` spans two genuinely different cognitive activities (authoring and slicing), which triggers the split criterion. The other two skills each have a single well-defined transformation algorithm, making a single agent sufficient.

**Pipeline architecture:** The three skills form a unidirectional pipeline driven by the shared artifact format (the use-case realization document). `/use-case` produces the artifact. `/test-spec` consumes it to generate BDD scenarios. `/contract-design` consumes it to generate OpenAPI schemas. The main context (orchestrator) coordinates the pipeline; agents never invoke each other (P-003 compliance).

---

## L1: Technical Specifications

### Agent Inventory Summary

| # | Agent Name | Skill | Role | Cognitive Mode | Model | Tool Tier | Traceability |
|---|-----------|-------|------|---------------|-------|-----------|--------------|
| 1 | `uc-author` | `/use-case` | Use Case Author | integrative | sonnet | T2 (Read-Write) | DI-01, DI-02, DI-11, R-04 |
| 2 | `uc-slicer` | `/use-case` | Use Case Slicer | systematic | sonnet | T2 (Read-Write) | DI-03, R-04, R-09 |
| 3 | `ts-generator` | `/test-spec` | BDD Test Spec Generator | systematic | sonnet | T2 (Read-Write) | DI-05, DI-06, R-05 |
| 4 | `cd-generator` | `/contract-design` | API Contract Generator | convergent | opus | T2 (Read-Write) | DI-07, DI-08, R-06 |

---

### Skill 1: /use-case

#### Agent 1.1: `uc-author`

**Identity**

| Field | Value | Source |
|-------|-------|--------|
| Role | Use Case Author -- creates and elaborates use case artifacts using Cockburn's 12-step writing process and Jacobson's UC 2.0 progressive narrative levels | DI-01, DI-11 |
| Expertise (1) | Cockburn use case writing methodology (12-step process, goal levels, precision levels, template formats Brief/Casual/Fully-Dressed) | S-02 (Cockburn research) |
| Expertise (2) | Jacobson UC 2.0 narrative levels (Briefly Described, Bulleted Outline, Essential Outline, Fully Described) and use-case modeling (actors, goals, use-case model) | S-01 (Jacobson research) |
| Expertise (3) | Stakeholder elicitation and goal decomposition using Cockburn's sea-metaphor classification (Cloud/Kite/Sea Level/Fish/Clam) | S-02, DI-02 |
| Cognitive Mode | **Integrative** -- combines inputs from multiple sources (stakeholder descriptions, existing system context, domain knowledge) into unified use case artifacts. Authoring requires cross-source correlation and gap filling (exploring what flows exist, what actors participate, what extensions handle failure). | AD-M-009 taxonomy, R-09 |

**Model Selection: Sonnet**

Justification (AD-M-009): The 12-step writing process is a structured procedure applied to ambiguous inputs (stakeholder descriptions). This falls into the "balanced analysis, standard production tasks" category. Opus would be justified if the authoring required complex multi-source reasoning beyond template application, but the Cockburn process provides sufficient procedural structure to constrain the integrative reasoning. Sonnet's structured-criteria strength (per `prompt-quality.md` agent selection guide) matches the named-framework methodology pattern.

**Tool Tier: T2 (Read-Write)**

Justification: The agent reads existing project context (use case templates, existing use cases, shared schema) and writes use case artifact files. No external research (T3) needed -- the methodology is embedded in the agent definition. No cross-session state (T4) needed -- artifacts persist as files per P-002. No delegation (T5) -- worker agent.

Tools: Read, Write, Edit, Glob, Grep, Bash

**Methodology Outline (Key Steps)**

The methodology implements Cockburn's 12-step writing process (S-02: Reminders pp. ii-iii, Ch. 22 Reminder 18 p. 223) with UC 2.0 progressive narrative levels:

| Step | Cockburn 12-Step | Agent Action |
|------|-----------------|--------------|
| 1 | Determine system scope and boundaries | Read project context; identify system boundary; set design scope (Enterprise/System/Subsystem) |
| 2 | Brainstorm and list primary actors | Enumerate human and non-human actors over system lifecycle |
| 3 | Brainstorm and exhaustively list user goals | Create actor-goal list; classify each goal by level (Cloud/Kite/Sea Level/Fish/Clam) |
| 4 | Write outer use case brief for each | Create use case artifacts at Briefly Described level (UC 2.0 narrative level 1) |
| 5 | Review and adjust scope | Validate actor-goal list against stakeholder input; merge or split as needed |
| 6 | Select a use case to expand | User selects or agent recommends based on value |
| 7 | Capture stakeholders, interests, preconditions, guarantees | Elaborate stakeholder contract per Cockburn Ch. 2 |
| 8 | Write Main Success Scenario (3-9 steps) | Apply Guideline 6 step-count rule; meet all interests and guarantees |
| 9 | Brainstorm extension conditions exhaustively | Anchor extensions to MSS step numbers (3a, 3b notation) |
| 10 | Write extension handling steps | Each extension terminates by rejoin, separate success, or failure |
| 11 | Extract sub-use-cases if needed | Refactor repeated sequences into subordinate use cases |
| 12 | Review for readability, completeness, stakeholder interests | Quality check against 7 Cs framework mapped to S-014 dimensions |

**Progressive Detail Levels:** The agent supports 4 output detail levels as discrete modes (DI-01, PAT-001):

| Level | UC 2.0 Name | Cockburn Mapping | Steps Active |
|-------|------------|-----------------|--------------|
| 1 | Briefly Described | Name + goal + brief | Steps 1-4 |
| 2 | Bulleted Outline | Brief + MSS bullets | Steps 1-8 |
| 3 | Essential Outline | + Extensions | Steps 1-10 |
| 4 | Fully Described | + Handling + Sub-UCs | Steps 1-12 |

Default: Level 2 (Bulleted Outline). Upgrade on demand per PAT-001 (progressive elaboration).

**Input/Output**

| Direction | Content | Format |
|-----------|---------|--------|
| Input | User request describing a system capability or existing use case to elaborate. Optionally: project context files, existing actor-goal list, system boundary description. | Natural language + optional file paths |
| Output | Use case artifact file with YAML frontmatter (goal_level, detail_level, primary_actor, supporting_actors, basic_flow, alternative_flows, extensions) and Markdown narrative body. | Shared artifact format (per R-01/R-03, schema defined separately in `shared-schema.json`) |

Output path: `projects/${JERRY_PROJECT}/use-cases/{UC-NNN}-{slug}.md` (per R-02)

**Guardrails (Beyond Constitutional Triplet)**

| Guardrail | Rationale | Source |
|-----------|-----------|--------|
| MUST classify every use case by goal level (Cloud/Kite/Sea Level/Fish/Clam) | Goal level determines downstream test scope and contract granularity | DI-02, PAT-007 |
| MUST enforce 3-9 steps in Main Success Scenario | Cockburn Guideline 6 (Ch. 7, p. 93); scenarios outside this range indicate wrong abstraction level | S-02 |
| MUST NOT advance to Fully Described without complete extension conditions | Extensions are the completeness criterion per PAT-002 (test-first verification framing) | S-02, DI-05 |
| MUST write breadth-first: scope actors and goals before elaborating individual use cases | Cockburn Reminders p. ii: "Work breadth-first, from lower precision to higher precision" | S-02, PAT-001 |
| MUST set `detail_level` in YAML frontmatter matching actual narrative completeness | Enables downstream `/test-spec` to check whether use case has sufficient detail for transformation | AI-02, DI-01 |
| MUST NOT bypass human review for generated use case content | CF-03 resolution: LLM generates, human validates | CF-03 |

---

#### Agent 1.2: `uc-slicer`

**Identity**

| Field | Value | Source |
|-------|-------|--------|
| Role | Use Case Slicer -- decomposes use cases into implementation-ready slices following Jacobson UC 2.0 Activity 2 (Slice the Use Cases) and Activity 4 (Prepare a Use-Case Slice) | DI-03, S-01 Activities 2+4 |
| Expertise (1) | Jacobson UC 2.0 slicing patterns (end-to-end slice selection, INVEST criteria application, slice state lifecycle management) | S-01 (Jacobson research, Activities 2+4) |
| Expertise (2) | Use case slice lifecycle management (Scoped > Prepared > Analyzed > Implemented > Verified) with worktracker integration | S-01 (slice lifecycle), PAT-006 |
| Cognitive Mode | **Systematic** -- applies step-by-step slicing procedures: identify basic flow as first slice, identify additional slices from alternatives and extensions, verify INVEST criteria, assign slice states. This is checklist execution and protocol adherence, not exploratory reasoning. | AD-M-009 taxonomy, R-09 |

**Model Selection: Sonnet**

Justification (AD-M-009): Slicing is a procedural, systematic activity. The agent follows a defined protocol (identify flows, create slices, verify INVEST). Sonnet's balanced capability handles the structured decision-making without requiring Opus-level reasoning. Haiku would be insufficient because slice identification requires understanding of use case flow dependencies.

**Tool Tier: T2 (Read-Write)**

Justification: Reads existing use case artifacts; writes slice definitions back into the artifact (slice sections in YAML frontmatter) and optionally creates worktracker Story entities for each slice.

Tools: Read, Write, Edit, Glob, Grep, Bash

**Methodology Outline (Key Steps)**

| Step | UC 2.0 Activity | Agent Action |
|------|-----------------|--------------|
| 1 | Activity 2: Identify first slice | Select the basic flow as the first slice (end-to-end through the concept) |
| 2 | Activity 2: Identify additional slices | Each alternative flow becomes a candidate slice; each significant extension becomes a candidate slice |
| 3 | Activity 2: Verify INVEST criteria | Each slice must be Independent, Negotiable, Valuable, Estimable, Small, Testable |
| 4 | Activity 2: Order slices | Rank by value; basic flow first; dependent slices after their dependencies |
| 5 | Activity 4: Prepare selected slice | Enhance narrative detail for the selected slice; define acceptance test cases |
| 6 | Activity 4: Define test cases | Each slice must have at least one test case before it is "Prepared" |
| 7 | State transition | Set slice_state in YAML frontmatter (Scoped -> Prepared) |

**Slice State Machine (UC 2.0 lifecycle mapped to worktracker):**

| UC 2.0 State | Worktracker Status | Entry Criteria | Exit Criteria |
|-------------|-------------------|----------------|---------------|
| Scoped | `draft` | Slice identified from use case flows | INVEST criteria verified |
| Prepared | `ready` | Test cases defined; narrative enhanced | Stakeholder approval for implementation |
| Analyzed | `in-progress` | System elements identified (Activity 5, realization) | Realization artifact produced |
| Implemented | `review` | Software built and unit tested | Integration test passed |
| Verified | `done` | Acceptance tests passed | Regression tests passed |

Source: S-01 (UC 2.0 slice lifecycle, pp. 15-16); PAT-006 (Jerry entity mapping).

**Input/Output**

| Direction | Content | Format |
|-----------|---------|--------|
| Input | Use case artifact at Essential Outline or Fully Described detail level (minimum: basic flow + extension conditions). Optionally: existing slice definitions for iterative refinement. | Shared artifact format (YAML frontmatter + Markdown) |
| Output | Updated use case artifact with `slices` section in YAML frontmatter: array of {slice_id, name, flows_included, slice_state, test_cases: []}. Optionally: worktracker Story entities per slice. | Shared artifact format + optional worktracker entities |

**Guardrails (Beyond Constitutional Triplet)**

| Guardrail | Rationale | Source |
|-----------|-----------|--------|
| MUST NOT slice a use case at detail_level < 3 (Essential Outline) | Extensions required for meaningful slicing; Briefly Described/Bulleted Outline lack flow information | DI-01 (detail level prerequisite) |
| MUST include basic flow as the first slice | UC 2.0 Principle 4: "choose the most central slice (end-to-end through the concept)" | S-01 p. 8 |
| MUST verify each slice has at least one test case before marking as "Prepared" | UC 2.0 Activity 4: "if no test cases, slice is NOT properly prepared" | S-01 Activity 4 |
| MUST map slice_state to worktracker entity status | Enables project tracking integration | PAT-006 |

---

### Skill 2: /test-spec

#### Agent 2.1: `ts-generator`

**Identity**

| Field | Value | Source |
|-------|-------|--------|
| Role | BDD Test Specification Generator -- transforms use case artifacts into Gherkin BDD scenarios using Clark's (2018) UC2.0-to-Gherkin mapping | DI-05, PAT-008 |
| Expertise (1) | Clark (2018) UC2.0-to-Gherkin transformation algorithm (basic flow to happy path, alternative flow to additional scenario, extension to error scenario) | S-03 (Clark mapping table) |
| Expertise (2) | BDD/Gherkin specification writing (Feature/Scenario/Given-When-Then structure, declarative style, Cucumber best practices) | S-03 (Adzic 2016 data, Cucumber principles) |
| Expertise (3) | 7 Cs quality framework application to generated test specifications (C1 Coverage as primary criterion) | S-03, DI-06, PAT-004 |
| Cognitive Mode | **Systematic** -- applies Clark's mapping algorithm as a deterministic lookup table. Each use case flow maps to a specific scenario type. The transformation is a step-by-step procedure, not creative generation. | AD-M-009 taxonomy, R-09 |

**Model Selection: Sonnet**

Justification (AD-M-009): The Clark transformation is a structured mapping with well-defined rules. Sonnet handles procedural, checklist-style work effectively. Opus is unnecessary because the mapping does not require complex reasoning -- it is a lookup table applied systematically. Haiku would be insufficient because the agent needs to correctly interpret use case flow semantics to map them to appropriate scenario types.

**Tool Tier: T2 (Read-Write)**

Justification: Reads use case artifacts (shared format); writes BDD feature files (.feature) and optional test plan documents (.md). No external research needed (the Clark mapping is embedded in the agent definition). No cross-session state. No delegation.

Tools: Read, Write, Edit, Glob, Grep, Bash

**Methodology Outline (Key Steps)**

The Clark (2018) UC2.0-to-Gherkin transformation algorithm:

| Step | Action | Clark Mapping Rule |
|------|--------|--------------------|
| 1 | **Validate input** | Check use case detail_level >= 3 (Essential Outline); reject if insufficient |
| 2 | **Extract Feature** | Use case title becomes Feature title; use case goal becomes Feature description; primary actor becomes the scenario subject |
| 3 | **Map basic flow to happy path** | Basic flow steps become a single Scenario with Given (preconditions), When (trigger + action steps), Then (postconditions/guarantees) |
| 4 | **Map each alternative flow to additional scenario** | Each alternative flow becomes its own Scenario: Given (preconditions + flow entry condition), When (alternative steps), Then (alternative outcome) |
| 5 | **Map each extension to error scenario** | Each extension condition becomes a negative test Scenario: Given (preconditions), When (trigger that causes extension condition), Then (extension outcome -- error handling) |
| 6 | **Apply Cockburn step-anchor naming** | Scenario names reference source step numbers (e.g., "Scenario: 3a - Credit check fails") for traceability |
| 7 | **Quality check against 7 Cs** | Verify C1 Coverage (all flows mapped), C4 Consistent Abstraction (scenarios at same detail level), C5/C6 Consistent Structure |

**Clark Mapping Table (Deterministic):**

| Use Case Element | Gherkin Element | Cardinality | Source |
|-----------------|----------------|-------------|--------|
| Use case title | Feature title | 1:1 | S-03 (Clark 2018) |
| Use case goal | Feature description | 1:1 | S-03 |
| Basic flow | Happy path Scenario | 1:1 | S-03 |
| Alternative flow | Additional Scenario | 1:1 per alternative | S-03 |
| Extension (step-anchored) | Error/negative Scenario | 1:1 per extension | S-03 |
| Preconditions | Given clauses | 1:N | S-03 |
| Postconditions/guarantees | Then clauses | 1:N | S-03 |
| Actor | Scenario subject ("As a {actor}") | 1:1 | S-03 |

**Output Cardinality Decision (resolves G-03):**

- 1 Feature file per use case
- 1 Scenario per flow (basic flow, each alternative, each extension)
- Feature file path: `projects/${JERRY_PROJECT}/test-specs/{UC-NNN}-{slug}.feature`
- Optional test plan document: `projects/${JERRY_PROJECT}/test-specs/{UC-NNN}-{slug}-test-plan.md`

Source: G-03 gap resolution. Rationale: 1 Feature per use case maintains traceability between use case and test specification. 1 Scenario per flow ensures C1 Coverage (every flow has a test).

**Input/Output**

| Direction | Content | Format |
|-----------|---------|--------|
| Input | Use case artifact at detail_level >= 3 (Essential Outline or Fully Described). Must have: basic_flow, extensions (at minimum). Optionally: alternative_flows, slices (for slice-scoped generation). | Shared artifact format (YAML frontmatter + Markdown) |
| Output | (1) Gherkin Feature file (.feature). (2) Optional: test plan document (.md) with coverage matrix showing which use case flows map to which scenarios. | .feature file + optional .md |

**Guardrails (Beyond Constitutional Triplet)**

| Guardrail | Rationale | Source |
|-----------|-----------|--------|
| MUST NOT generate scenarios from use cases at detail_level < 3 | Essential Outline is the minimum level with extension conditions; without extensions, test coverage is incomplete | PAT-008, DI-05 |
| MUST include traceability from each Scenario to source use case step number | Clark's step-anchor naming enables auditable traceability | S-03 (Clark step-anchor naming) |
| MUST verify C1 Coverage: every basic flow, alternative flow, and extension in the source use case produces at least one Scenario | Coverage is the primary quality criterion per 7 Cs | DI-06, PAT-004 |
| MUST use declarative Given-When-Then style (what, not how) | Cucumber best practice; imperative scenarios are brittle | S-03 (Cucumber declarative principle) |
| MUST reject use cases without at least one extension condition | A use case with only a basic flow and no extensions produces a trivially incomplete test specification | PAT-002 (test-first verification framing) |

---

### Skill 3: /contract-design

#### Agent 3.1: `cd-generator`

**Identity**

| Field | Value | Source |
|-------|-------|--------|
| Role | API Contract Generator -- transforms use case realization artifacts into OpenAPI 3.x contract specifications using a novel UC-to-contract transformation algorithm | DI-07, DI-08, R-06 |
| Expertise (1) | Use case realization interpretation (Activity 5 "Interaction Defined" level: system elements, responsibilities, interaction sequences) | S-01 (Activity 5 Expanded) |
| Expertise (2) | OpenAPI 3.x specification authoring (paths, operations, request/response schemas, component reuse) | DI-07 (REST-only initial scope) |
| Expertise (3) | Actor-role-to-contract-role mapping (primary actor as consumer, system as provider, interaction steps as operations) | R-06 (novel algorithm), G-01 |
| Cognitive Mode | **Convergent** -- evaluates interaction steps in the realization artifact and converges on the optimal contract structure. Each interaction step presents options (operation granularity, path structure, schema design) that must be resolved through focused evaluation and criteria-based selection. | AD-M-009 taxonomy |

**Model Selection: Opus**

Justification (AD-M-009): This is the highest-risk skill (G-01 gap -- no prior art). The transformation algorithm is novel and requires complex reasoning to map use case interaction semantics to API contract structures. Unlike the Clark mapping (deterministic lookup), the UC-to-contract mapping requires judgment about operation granularity, resource identification, and schema structure. Opus is warranted for complex reasoning tasks with no established procedural template to follow.

**Tool Tier: T2 (Read-Write)**

Justification: Reads use case realization artifacts (shared format); writes OpenAPI 3.x YAML files. No external research needed for the transformation itself (the algorithm is embedded in the agent definition). No cross-session state. No delegation. T3 (WebSearch) could be argued for looking up OpenAPI schema standards, but this is reference knowledge that should be embedded in the agent definition, not discovered at runtime.

Tools: Read, Write, Edit, Glob, Grep, Bash

**Methodology Outline (Key Steps)**

The novel UC-to-contract transformation algorithm (R-06, DI-08, G-01):

| Step | Action | Mapping Rule |
|------|--------|-------------|
| 1 | **Validate input** | Check use case has realization at "Interaction Defined" level (Level 3); check detail_level >= 3 |
| 2 | **Identify resources** | Each system element (service/component) that receives messages in the realization becomes a candidate API resource |
| 3 | **Map interaction steps to operations** | Each arrow in the realization interaction sequence maps to an HTTP operation. Actor-to-system arrows become request endpoints; system-to-system arrows become internal operations (documented but not externally exposed) |
| 4 | **Derive HTTP methods** | Operation semantics determine HTTP method: read/query -> GET; create -> POST; update -> PUT/PATCH; delete -> DELETE |
| 5 | **Extract request schemas** | Step preconditions + input parameters become request body/query parameter schemas |
| 6 | **Extract response schemas** | Step postconditions + return values become response schemas |
| 7 | **Map extensions to error responses** | Each extension condition becomes a 4xx/5xx response with appropriate error schema |
| 8 | **Compose OpenAPI document** | Assemble paths, operations, components/schemas, and info section |
| 9 | **Validate OpenAPI spec** | Check syntactic validity against OpenAPI 3.x specification |

**Actor-to-Contract-Role Mapping:**

| Use Case Element | Contract Element | Source |
|-----------------|-----------------|--------|
| Primary actor | API consumer (the caller) | R-06 |
| System (receiving messages) | API provider (the server) | R-06 |
| Supporting actor | External dependency (documented in components/schemas description) | R-06 |
| Interaction step (actor -> system) | Path + Operation (external endpoint) | R-06 |
| Interaction step (system -> system) | Internal operation (documented in x-internal-operations extension, not exposed as path) | R-06 |
| Step precondition | Request validation (required fields, format constraints) | R-06 |
| Step postcondition/guarantee | Response schema (success payload) | R-06 |
| Extension condition | Error response (4xx/5xx with error detail schema) | R-06 |

**Scope Constraint (DI-07, ASM-005):**

- **Initial release:** REST (OpenAPI 3.x) only
- **Deferred:** AsyncAPI, CloudEvents, event-driven contracts
- **Reason:** G-02 gap (multi-actor pub/sub behavior mapping) unresolved. AsyncAPI requires publisher/subscriber role mapping that does not cleanly derive from single-primary-actor use cases.

**Input/Output**

| Direction | Content | Format |
|-----------|---------|--------|
| Input | Use case artifact with realization at "Interaction Defined" level. Must have: interaction sequence with typed steps (actor, system element, operation, parameters, return values). | Shared artifact format (YAML frontmatter + Markdown) with realization section |
| Output | (1) OpenAPI 3.x YAML file. (2) Mapping document (.md) showing traceability from each interaction step to each API operation. | .yaml (OpenAPI) + .md (mapping) |

Output paths:
- Contract: `projects/${JERRY_PROJECT}/contracts/{UC-NNN}-{slug}-api.yaml`
- Mapping: `projects/${JERRY_PROJECT}/contracts/{UC-NNN}-{slug}-mapping.md`

**Guardrails (Beyond Constitutional Triplet)**

| Guardrail | Rationale | Source |
|-----------|-----------|--------|
| MUST NOT generate contracts from use cases without "Interaction Defined" level realization | The transformation requires typed interaction sequences; lower-level realizations lack the operation/parameter detail | S-01 Activity 5 (3 realization levels) |
| MUST label generated contracts as "PROTOTYPE" until validated by human review | Novel algorithm with no prior art; output requires validation | G-01 (no prior art), LES-001 |
| MUST include traceability from each API operation to source interaction step | Enables auditing of the transformation algorithm's correctness | R-06 |
| MUST NOT generate AsyncAPI or event-driven contracts in initial release | G-02 gap unresolved; multi-actor mapping not designed | DI-07, ASM-005 |
| MUST validate generated OpenAPI against the OpenAPI 3.x specification schema | Syntactic validity is a prerequisite for contract usefulness | DI-08 |
| MUST flag system-to-system interaction steps as internal (not exposed as external APIs) | Prevents leaking internal architecture through the public API contract | R-06 (actor-to-role mapping) |

---

### Agent Interaction Model

#### Intra-Skill Interaction: `/use-case` (2 agents)

```
Main Context (Orchestrator)
    |
    +-- uc-author (creates/elaborates use case artifact)
    |       |
    |       v  [artifact file on disk]
    |
    +-- uc-slicer (reads artifact, adds slice definitions)
            |
            v  [updated artifact file on disk]
```

**Interaction Pattern:** Sequential file-mediated handoff. The orchestrator invokes `uc-author` first to create the use case artifact. Once the artifact reaches detail_level >= 3 (Essential Outline), the orchestrator invokes `uc-slicer` to decompose it into slices. The two agents never communicate directly -- all coordination flows through the main context and the shared artifact file on disk. This is P-003 compliant (single-level nesting: main context -> worker).

**Handoff Data (uc-author -> uc-slicer, via orchestrator):**

| Field | Value |
|-------|-------|
| artifact_path | `projects/${JERRY_PROJECT}/use-cases/{UC-NNN}-{slug}.md` |
| detail_level | 3 or 4 (Essential Outline or Fully Described) |
| key_findings | Actor-goal list, basic flow summary, extension count |
| success_criteria | At least 1 slice identified; basic flow is first slice; each slice has INVEST assessment |

#### Cross-Skill Interaction: Pipeline

```
/use-case           /test-spec          /contract-design
    |                   |                    |
uc-author ---+     ts-generator         cd-generator
             |          ^                    ^
uc-slicer ---+          |                    |
             |          |                    |
             v          |                    |
    [UC Artifact]-------+--------------------+
    (shared artifact format on disk)
```

**Interaction Pattern:** Unidirectional pipeline mediated by the shared artifact format. The main context orchestrates the sequence:

1. Invoke `/use-case` agents to produce a use case artifact
2. Invoke `/test-spec` (`ts-generator`) passing the artifact path
3. Invoke `/contract-design` (`cd-generator`) passing the artifact path

Steps 2 and 3 can run in parallel (they both read the same artifact; neither modifies it). The orchestrator decides sequencing based on user request.

**P-003 Compliance:** All agents are workers invoked by the main context. No agent invokes another agent. The pipeline is coordinated externally, not internally.

**Cross-Skill Handoff Data:**

| From | To | Key Data | Pre-Condition |
|------|----|----------|---------------|
| `/use-case` | `/test-spec` | artifact_path, detail_level >= 3, extension count > 0 | Use case has basic flow + at least one extension condition |
| `/use-case` | `/contract-design` | artifact_path, realization_level = "interaction_defined" | Use case has Activity 5 realization with typed interaction steps |

---

### Trigger Map Extensions

New entries for `mandatory-skill-usage.md` trigger map. Priority >= 13 per synthesis recommendation R-07, DI-10 (above current maximum of 12 for `/user-experience`).

#### `/use-case` -- Priority 13

| Column | Value |
|--------|-------|
| **Detected Keywords** | use case, use-case, write use case, create use case, author use case, use case model, actor goal list, basic flow, main success scenario, alternative flow, extension, extension handling, fully dressed, casual use case, briefly described, sea level goal, goal level, use case slice, slice use case, UC 2.0, cockburn, jacobson |
| **Negative Keywords** | requirements specification, V&V, technical review, trade study, compliance, test spec, BDD, Gherkin, scenario, OpenAPI, contract, API design, schema, adversarial, tournament, transcript, penetration, exploit, code review, documentation, tutorial |
| **Priority** | 13 |
| **Compound Triggers** | "write use case" OR "create use case" OR "author use case" OR "use case model" OR "actor goal" OR "basic flow" OR "main success scenario" OR "use case slice" (phrase match) |
| **Skill** | `/use-case` |

**Collision Analysis:**

| Existing Skill | Shared Keywords | Resolution |
|---------------|----------------|------------|
| `/nasa-se` | "requirements", "design" | Negative keywords on `/use-case` suppress these; compound triggers on `/use-case` require "use case" co-occurrence |
| `/eng-team` | None directly | "requirements" suppressed by negative keyword |
| `/problem-solving` | "analyze" | Negative keywords on `/use-case` suppress standalone "analyze"; compound trigger requires "use case" context |

#### `/test-spec` -- Priority 14

| Column | Value |
|--------|-------|
| **Detected Keywords** | test spec, test specification, BDD, BDD scenario, Gherkin, feature file, Given When Then, happy path, error scenario, negative test, test case from use case, Clark mapping, scenario mapping, test coverage, acceptance test, specification by example |
| **Negative Keywords** | requirements, V&V, compliance, use case model, actor goal, write use case, create use case, OpenAPI, contract, API design, adversarial, tournament, transcript, penetration, exploit, code review, unit test, integration test, pytest, jest |
| **Priority** | 14 |
| **Compound Triggers** | "test specification" OR "BDD scenario" OR "Gherkin scenario" OR "Given When Then" OR "test case from use case" OR "specification by example" (phrase match) |
| **Skill** | `/test-spec` |

**Collision Analysis:**

| Existing Skill | Shared Keywords | Resolution |
|---------------|----------------|------------|
| `/eng-team` | "test" (broad) | Negative keywords suppress "unit test", "integration test", "pytest", "jest"; compound triggers require BDD-specific context |
| `/nasa-se` | "V&V", "compliance" | Negative keywords on `/test-spec` suppress these |
| `/problem-solving` | "evaluate" | Not in `/test-spec` keywords; no collision |

#### `/contract-design` -- Priority 15

| Column | Value |
|--------|-------|
| **Detected Keywords** | contract design, API contract, OpenAPI, API spec, API specification, generate contract, contract from use case, API schema, endpoint design, operation mapping, request response schema, API generation, REST contract, swagger |
| **Negative Keywords** | requirements, V&V, compliance, use case model, actor goal, write use case, BDD, Gherkin, scenario, test spec, adversarial, tournament, transcript, penetration, exploit, code review, pricing model, cloud pricing |
| **Priority** | 15 |
| **Compound Triggers** | "API contract" OR "contract design" OR "OpenAPI" OR "generate contract" OR "contract from use case" OR "API specification" (phrase match) |
| **Skill** | `/contract-design` |

**Collision Analysis:**

| Existing Skill | Shared Keywords | Resolution |
|---------------|----------------|------------|
| `/nasa-se` | "interface", "design" | "interface" not in `/contract-design` keywords; "design" only appears in compound "contract design" |
| `/eng-team` | "API" (broad) | `/contract-design` compound triggers require "API contract" or "API specification"; standalone "API" does not trigger |
| `/pm-pmm` | "pricing" | Negative keyword "pricing model" prevents collision |

---

## L2: Architectural Implications

### Design Rationale: Agent Count Decision

The agent count is the most consequential design decision in this document. Below is the analysis of why `/use-case` gets 2 agents while `/test-spec` and `/contract-design` get 1 each.

**Decision Framework (from `agent-development-standards.md` Pattern 1):**

Split an agent when EITHER of:
- (a) Methodology section exceeds 1,500 tokens
- (b) 2+ cognitive modes required within the same skill

**`/use-case` Analysis:**

| Criterion | Assessment | Triggers Split? |
|-----------|-----------|-----------------|
| Methodology size | Authoring alone (Cockburn 12-step + 4 narrative levels + goal classification) requires ~1,200 tokens. Slicing (INVEST criteria + slice lifecycle + worktracker mapping + slice state machine) requires ~800 tokens. Combined: ~2,000 tokens, exceeding the 1,500-token threshold. | **YES** (criterion a) |
| Cognitive modes | Authoring = integrative (exploring, combining, gap-filling). Slicing = systematic (checklist execution, INVEST verification, state transitions). Two distinct modes per the taxonomy. | **YES** (criterion b) |
| **Verdict** | Both criteria trigger the split. | **2 agents** |

**`/test-spec` Analysis:**

| Criterion | Assessment | Triggers Split? |
|-----------|-----------|-----------------|
| Methodology size | Clark mapping algorithm (7 steps + mapping table) requires ~800 tokens. Well within threshold. | No |
| Cognitive modes | Systematic only. The transformation is a deterministic lookup; no creative or evaluative reasoning required alongside the systematic procedure. | No |
| **Verdict** | Neither criterion triggers. | **1 agent** |

**`/contract-design` Analysis:**

| Criterion | Assessment | Triggers Split? |
|-----------|-----------|-----------------|
| Methodology size | UC-to-contract algorithm (9 steps + actor-role mapping + scope constraints) requires ~1,000 tokens. Within threshold. | No |
| Cognitive modes | Convergent only. The transformation evaluates options and converges on a contract structure. The evaluation and the generation happen in the same reasoning pass. | No |
| **Verdict** | Neither criterion triggers. | **1 agent** |

### Steelman Analysis: Arguments for Alternative Decompositions (S-003, H-16)

Before dismissing alternative agent counts, per H-16 (Steelman before critique), here are the strongest cases for the alternatives:

**Steelman: 1 agent for `/use-case` (reject the split)**

The strongest argument for a single `uc-author` agent that also slices: slicing is a natural continuation of authoring. Cockburn's 12-step process ends at step 12 (review), and the Jacobson slicing activities (2, 4) directly consume the authoring output. A single agent that does both avoids the handoff overhead between `uc-author` and `uc-slicer`, eliminates a file read/write round-trip, and reduces total tool invocations. The combined methodology at ~2,000 tokens is only 33% above the 1,500-token threshold -- not dramatically over.

**Why we still recommend the split:** The 33% overage is real and will grow as the methodology sections are refined during Phase 3 implementation. The cognitive mode difference is genuine and cannot be papered over: authoring requires exploring what flows exist (integrative/divergent), while slicing requires mechanically decomposing known flows (systematic). Mixing these modes in a single agent definition degrades prompt clarity. The handoff cost (one file read) is minimal compared to the quality improvement from mode-appropriate methodology sections.

**Steelman: 2 agents for `/test-spec` (add a ts-reviewer)**

The strongest argument: Clark's mapping produces raw Gherkin, but the 7 Cs quality gate (DI-06) is a separate concern from generation. A dedicated `ts-reviewer` agent applying S-014 with 7 Cs lens would implement proper creator-critic separation.

**Why we still recommend 1 agent:** The quality gate for generated test specifications should be handled by the existing `/adversary` skill (specifically `adv-scorer` with S-014 rubric adapted for 7 Cs). Creating a skill-specific reviewer would duplicate the quality framework that already exists. The `ts-generator` agent applies the 7 Cs as a self-review step (H-15) before output; the formal quality gate is the adversary skill's responsibility.

**Steelman: 2 agents for `/contract-design` (add a cd-validator)**

The strongest argument: this is the highest-risk skill (G-01). A separate validation agent could independently verify the generated OpenAPI against the specification schema, preventing the generator from self-validating.

**Why we still recommend 1 agent:** OpenAPI schema validation is a deterministic check (JSON Schema validation against the OpenAPI meta-schema), not a reasoning task requiring a separate agent. The `cd-generator` agent can execute this validation as a Bash command (`uv run python -c "import jsonschema; ..."` or equivalent) within its tool budget. Adding a separate agent for a deterministic validation check is AP-05 (Over-Routing/Premature Specialization).

### Cognitive Mode Analysis (R-09 Traceability)

Mapping of agent cognitive modes to UC 2.0 Activities:

| UC 2.0 Activity | Agent | Cognitive Mode | Rationale |
|-----------------|-------|---------------|-----------|
| Activity 1: Find Actors and Use Cases | uc-author | Integrative | Exploring scope, combining stakeholder input, discovering actors and goals |
| Activity 2: Slice the Use Cases | uc-slicer | Systematic | Mechanical decomposition following INVEST criteria |
| Activity 3: Inspect and Adapt | uc-author (re-invoked) | Integrative | Reviewing and adjusting scope based on feedback |
| Activity 4: Prepare a Use-Case Slice | uc-slicer | Systematic | Enhancing narrative detail, defining test cases per checklist |
| Activity 5: Analyze a Use-Case Slice | (realization -- future agent or main context) | Convergent | Identifying system elements and allocating responsibilities |
| Activity 7: Test the System | ts-generator | Systematic | Applying Clark's mapping algorithm deterministically |

**Note on Activity 5:** The realization activity (Activity 5) is currently the bridge between `/use-case` and `/contract-design`. It is not assigned to a dedicated agent because the realization is authored as part of the use case artifact (the `uc-author` generates the interaction sequence section when prompted for realization-level detail). If this proves insufficient during Phase 3 prototyping, a dedicated `uc-realizer` agent could be introduced.

**Note on Activity 6:** Activity 6 (Implement Software) is out of scope for these three skills. This is downstream implementation work handled by the existing `/eng-team` skill.

### Risk Assessment

| Risk ID | Skill | Risk | Severity | Likelihood | Mitigation | Source |
|---------|-------|------|----------|------------|------------|--------|
| RISK-01 | `/contract-design` | Novel algorithm produces incorrect or unusable OpenAPI contracts | HIGH | MEDIUM | (1) Opus model for complex reasoning. (2) "PROTOTYPE" label on output. (3) Human review mandatory per guardrail. (4) Prototyping at 0.85 quality floor before production. | G-01, LES-001, DI-08 |
| RISK-02 | `/use-case` | 2-agent split creates unnecessary handoff overhead | LOW | LOW | File-mediated handoff is a single Read operation. Revert to 1 agent if quality metrics show no benefit. | CF-04 |
| RISK-03 | `/test-spec` | Clark mapping produces trivially simple scenarios that miss edge cases | MEDIUM | LOW | 7 Cs quality gate (C1 Coverage) catches incomplete coverage. Extension exhaustiveness is enforced by `uc-author` guardrail. | DI-06, PAT-002 |
| RISK-04 | All 3 skills | Shared artifact format schema (not yet designed) proves insufficient for downstream transformations | HIGH | MEDIUM | R-01 (design shared format first) is P0 priority. Phase 3 prototype validates format before full implementation. | AI-01, ASM-001 |
| RISK-05 | All 3 skills | Routing collisions with existing skills (`/nasa-se`, `/eng-team`) despite compound triggers | MEDIUM | LOW | Negative keywords and compound triggers designed per PAT-005. Priority >= 13 avoids disrupting existing resolution. | T-07, DI-10 |
| RISK-06 | `/contract-design` | AsyncAPI requirement surfaces after initial release | LOW | MEDIUM | Scope explicitly deferred per DI-07, ASM-005. Architecture supports future extension without redesign. | G-02 |

### Pre-Mortem Analysis (S-004): "It's 6 Months Later and This Decision Failed -- Why?"

**Failure Mode 1: The 2-agent split in `/use-case` was premature.**
Signal: `uc-slicer` is invoked < 20% of the time; most users only author use cases without slicing. The split created maintenance overhead (two agent definitions, two governance files) for a rarely-used capability.
Mitigation: Track invocation frequency during Phase 3 prototype. If slicing invocations are < 20% after 30 use cases, merge back to 1 agent.

**Failure Mode 2: The 1-agent design for `/contract-design` was too simple.**
Signal: The novel algorithm requires multiple distinct reasoning passes (resource identification, operation mapping, schema extraction) that compete for context within a single agent invocation. Quality scores consistently below 0.85.
Mitigation: The convergent cognitive mode handles multi-step evaluation within a single pass. If quality scores drop, the first response is to increase the model from Opus to a more capable future model, not to split the agent. If the methodology section grows beyond 1,500 tokens during refinement, split at that point.

**Failure Mode 3: The trigger map compound triggers are too restrictive.**
Signal: Users describe use case work in vocabulary not covered by compound triggers (e.g., "create a user story" when they mean a use case; "write an API spec" without "OpenAPI" or "contract"). The skills are under-routed.
Mitigation: R-07 recommends reviewing the trigger map after Phase 3 prototype. Add synonyms discovered during real usage. Track routing misses per RT-M-008.

### Evolution Path

| Phase | Agent Count | Trigger |
|-------|-----------|---------|
| **Initial (Phase 3)** | 4 (2+1+1) | Current design |
| **Split trigger 1** | 5 | `/use-case` Activity 5 (realization) methodology exceeds 1,500 tokens -> add `uc-realizer` |
| **Split trigger 2** | 6 | `/contract-design` AsyncAPI support adds a second cognitive mode (systematic for spec generation alongside convergent for mapping) -> add `cd-async-generator` |
| **Split trigger 3** | 7 | `/test-spec` adds performance/load test generation (different methodology from BDD) -> add `ts-perf-generator` |
| **Ceiling** | 8-10 | Per ORCHESTRATION_PLAN.md Phase 3 target. Only if validated by usage data. |

### Design Implications Addressed

Every synthesis design implication is mapped to this architecture:

| DI ID | Requirement | How Addressed | Agent(s) |
|-------|-------------|---------------|----------|
| DI-01 | 4 narrative detail levels as discrete output modes | `uc-author` methodology: 4 levels mapped to Cockburn 12-step subsets; `detail_level` YAML field | uc-author |
| DI-02 | Goal level classification in every artifact | `uc-author` guardrail: MUST classify every use case by goal level; `goal_level` YAML field | uc-author |
| DI-03 | Slice lifecycle representation | `uc-slicer` methodology: 5-state lifecycle in YAML frontmatter; worktracker status mapping | uc-slicer |
| DI-04 | Shared artifact format | Used by all agents as input/output; defined separately in `shared-schema.json` (R-01/R-03) | All |
| DI-05 | Clark transformation as default algorithm | `ts-generator` methodology: Clark mapping table as deterministic lookup | ts-generator |
| DI-06 | 7 Cs quality framework for BDD specs | `ts-generator` guardrail: C1 Coverage check; quality gate via `/adversary` S-014 | ts-generator |
| DI-07 | REST-only initial scope | `cd-generator` scope constraint; AsyncAPI deferred; negative keyword prevents collision | cd-generator |
| DI-08 | Novel algorithm requires prototyping | `cd-generator` guardrail: PROTOTYPE label; Opus model; 0.85 quality floor | cd-generator |
| DI-09 | Start with 1 agent per skill, split at threshold | 4 agents total; `/use-case` split justified by both criteria; others single | All |
| DI-10 | Compound triggers and negative keywords | Trigger map extensions designed with compound triggers, negative keywords, priority >= 13 | All |
| DI-11 | Cockburn 12-step as methodology backbone | `uc-author` methodology section directly implements the 12-step process | uc-author |
| DI-12 | H-34 dual-file architecture | All agents require `.md` + `.governance.yaml`; constitutional triplet mandatory | All |

---

## Options Evaluated

### Option A: 1 Agent Per Skill (3 Total)

| Dimension | Assessment |
|-----------|-----------|
| **Pros** | Simplest architecture. Minimum maintenance overhead (3 agent definition files, 3 governance files). Follows synthesis recommendation R-04 literally. No handoff complexity within skills. |
| **Cons** | `/use-case` agent methodology exceeds 1,500-token threshold (~2,000 tokens combined). Mixes integrative and systematic cognitive modes in one agent, degrading prompt effectiveness. Does not satisfy the 2-cognitive-mode split criterion from Pattern 1. |
| **Score** | 6/10 -- follows simplicity principle (ET-02) but violates Pattern 1 split criteria |

### Option B: 2 Agents for /use-case, 1 Each for Others (4 Total) -- RECOMMENDED

| Dimension | Assessment |
|-----------|-----------|
| **Pros** | Respects both split criteria (methodology size and cognitive mode) for `/use-case`. Single agent for skills with single cognitive mode and methodology < 1,500 tokens. Balances simplicity with justified complexity. Clear evolution path if additional splits needed. |
| **Cons** | One additional agent and governance file vs. Option A. File-mediated handoff between `uc-author` and `uc-slicer` adds one Read operation per invocation. Slightly more complex routing within `/use-case` (orchestrator must decide which agent to invoke). |
| **Score** | 8/10 -- justified complexity matching framework standards |

### Option C: Full Decomposition per ORCHESTRATION_PLAN Phase 3 Target (8+ Total)

| Dimension | Assessment |
|-----------|-----------|
| **Pros** | Each UC 2.0 activity gets a dedicated agent with focused methodology. Maximum specialization. Matches the Phase 3 target list (`uc-author`, `uc-reviewer`, `uc-slicer`, `uc-analyst`; `ts-generator`, `ts-reviewer`; `cd-generator`, `cd-validator`). |
| **Cons** | Violates ET-02 (Anthropic simplicity principle): "start simple, add complexity only when measurably needed." Pre-decomposes before methodology sections are written and measured against the 1,500-token threshold. Creates 8+ governance files, 8+ agent definitions, and complex routing before validating the basic pipeline. Directly contradicts R-04 and CF-04 resolution. |
| **Score** | 4/10 -- premature complexity without validation |

### Option D: 3 Agents for /use-case (Author + Slicer + Reviewer) (5 Total)

| Dimension | Assessment |
|-----------|-----------|
| **Pros** | Adds a dedicated `uc-reviewer` that applies 7 Cs quality framework to use case artifacts. Implements creator-critic within the skill. Complete separation of concerns. |
| **Cons** | The review capability already exists in `/adversary` (adv-scorer with S-014). Creating `uc-reviewer` duplicates the quality framework. The quality gate should be skill-agnostic -- the 7 Cs map to S-014 dimensions per ET-03, so the adversary skill handles this without a dedicated agent. AP-05 (Over-Routing). |
| **Score** | 5/10 -- duplicates existing capability |

**Selected: Option B** (4 agents: uc-author, uc-slicer, ts-generator, cd-generator)

---

## Traceability Matrix

### Synthesis Recommendations (R-01 through R-10)

| R-ID | Priority | Recommendation | Addressed? | How |
|------|----------|---------------|------------|-----|
| R-01 | P0 | Design shared artifact format first | Not in scope (separate deliverable: `shared-schema.json`) | Deferred to file-organization and frontmatter-schema deliverables |
| R-02 | P1 | Design file organization | Not in scope (separate deliverable) | Deferred; this document specifies output paths per agent |
| R-03 | P1 | Design frontmatter schema + shared-schema.json | Not in scope (separate deliverable) | Deferred; all agents reference the shared format |
| R-04 | P1 | Start with 1 agent per skill; split at threshold | **YES** | `/use-case` split justified; `/test-spec` and `/contract-design` start with 1 |
| R-05 | P1 | Design Clark transformation as decision tree | **YES** | `ts-generator` methodology: Clark mapping table (7 steps) |
| R-06 | P1 | Design UC-to-contract transformation algorithm | **YES** | `cd-generator` methodology: 9-step algorithm with actor-role mapping |
| R-07 | P1 | Design trigger map entries with compound triggers | **YES** | Trigger map extensions section with collision analysis |
| R-08 | P2 | Confirm AsyncAPI scope | Documented as deferred | `cd-generator` scope constraint: REST-only initial release |
| R-09 | P2 | Confirm worktracker entity compatibility | **YES** | `uc-slicer` methodology: slice state to worktracker status mapping (PAT-006) |
| R-10 | P2 | Design quality gate integration (7 Cs + S-014) | **YES** | `ts-generator` guardrails: 7 Cs mapped to S-014 dimensions per ET-03. Quality gate handled by `/adversary`. |

### Synthesis Design Implications (DI-01 through DI-12)

See [Design Implications Addressed](#design-implications-addressed) table in L2 section. All 12 design implications addressed.

### Gap Closures

| Gap ID | Status | How Addressed |
|--------|--------|---------------|
| G-01 | **MITIGATED** | `cd-generator` methodology documents the novel algorithm. Opus model. PROTOTYPE label. 0.85 prototyping floor. |
| G-02 | **DEFERRED** | AsyncAPI scoped out of initial release per DI-07, ASM-005. Architecture supports future extension. |
| G-03 | **RESOLVED** | Cardinality decision documented: 1 Feature file per use case, 1 Scenario per flow. |
| G-04 | **RESOLVED** | `uc-slicer` uses existing worktracker entity types (Feature/Epic, Story/Task). No new entity types needed. |
| G-05 | **OUT OF SCOPE** | Stale downstream artifacts noted as known limitation. Not addressed in initial implementation. |

---

## Self-Review Checklist (H-15, S-010)

- [x] **P-001 (Truth/Accuracy):** Agent specifications match source methodology (Cockburn 12-step, Clark mapping, Jacobson Activities) with explicit page/section references
- [x] **P-002 (File Persistence):** Document persisted to `architecture/agent-decomposition-draft.md`
- [x] **P-004 (Provenance):** Every design decision cites synthesis findings (DI-xx, R-xx, PAT-xxx, S-xx) or framework standards (AD-M-xxx, Pattern 1)
- [x] **P-011 (Evidence-Based):** 4 alternatives evaluated (Options A-D) with scored trade-off analysis
- [x] **P-020 (User Authority):** Status PROPOSED; no decision finalized without user approval
- [x] **P-022 (No Deception):** Negative consequences documented for every option. Risk assessment includes 6 identified risks with mitigations. Pre-mortem identifies 3 failure modes.
- [x] **H-23:** Navigation table present with anchor links
- [x] **L0/L1/L2:** All three output levels present
- [x] **DI-01 through DI-12:** All 12 design implications addressed (traceability matrix)
- [x] **R-01 through R-10:** All 10 recommendations addressed or documented as out-of-scope (traceability matrix)
- [x] **S-003 (Steelman):** Steelman analysis applied to all rejected alternatives before dismissal (3 alternatives steelmanned)
- [x] **S-004 (Pre-Mortem):** 3 failure modes identified with signals and mitigations
- [x] **CF-04 resolved:** Agent count follows Pattern 1 criteria, not Phase 3 target list
- [x] **No H-34 governance files created** (those are Phase 3 deliverables; this document specifies what those files will contain)

### Adversarial Self-Check (S-002: Devil's Advocate)

**Challenge 1: "Is Sonnet really sufficient for `uc-author`?"**
The authoring process combines Cockburn's 12-step process with UC 2.0 narrative levels. The integrative cognitive mode suggests Opus per the Mode-to-Design Implications table in `agent-development-standards.md`. However, the Cockburn process provides enough procedural structure to constrain the reasoning. If quality scores fall below threshold during Phase 3, Opus is the first escalation path.

**Challenge 2: "Should `cd-generator` be T3 instead of T2?"**
The argument for T3: the agent might need to look up OpenAPI 3.x specification details. Counter: the OpenAPI specification is stable reference knowledge (not evolving rapidly) and should be embedded in the agent definition or a reference file loaded at Tier 2. Runtime web searches for specification details would introduce latency and non-determinism into what should be a deterministic transformation.

**Challenge 3: "Is the trigger map priority assignment arbitrary?"**
Priority 13/14/15 is assigned based on semantic specificity: `/use-case` (13) has the broadest keyword set and most collision potential; `/test-spec` (14) has BDD-specific keywords with less collision; `/contract-design` (15) has the narrowest, most specific keywords. Lower priority number = higher precedence, so `/use-case` wins ties over `/test-spec`, which wins over `/contract-design`. This matches the pipeline order (authoring before testing before contracts).

---

*Architecture Version: 1.0.0*
*Constitutional Compliance: P-001 (truth), P-002 (file persistence), P-003 (no recursive subagents), P-004 (provenance), P-011 (evidence-based alternatives), P-020 (user authority -- PROPOSED status), P-022 (no deception -- risks and negative consequences documented)*
*Adversary Review Required: YES -- C4 all-10-strategy review at >= 0.95 threshold*
*Next Agent: ps-critic (adversarial quality review)*
*Workflow ID: use-case-skills-20260308-001*
