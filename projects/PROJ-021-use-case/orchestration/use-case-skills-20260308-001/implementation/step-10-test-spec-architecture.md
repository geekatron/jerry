# Skill Architecture Design: /test-spec

> **PS ID:** proj-021 | **Entry ID:** step-10-test-spec-architecture | **Workflow ID:** use-case-skills-20260308-001
> **Date:** 2026-03-09 | **Agent:** eng-architect | **Step:** 10 (Phase 3 Implementation)
> **Quality Threshold:** >= 0.95 (C4)
> **Status:** PROPOSED (P-020: user approval required before ACCEPTED)
> **Version:** 1.0.0
> **Lineage:** file-organization.md (v2.1.0, 0.951 PASS), agent-decomposition.md (v1.1.0, 0.963 PASS), frontmatter-schema.md (v1.0.0, 0.955 PASS), shared-schema.json (v1.0.0), step-9-use-case-architecture.md (v1.2.0, 0.956 PASS)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What to build, why, and key decisions in plain language |
| [L1: Technical Specification](#l1-technical-specification) | Implementation-ready specifications for every file |
| [1. File Manifest](#1-file-manifest) | Complete list of files to create with paths |
| [2. SKILL.md Design](#2-skillmd-design) | Routing, agent table, when-to-use, integration points |
| [3. Agent Definition Specifications](#3-agent-definition-specifications) | Per-agent .md frontmatter, .governance.yaml, system prompt outline |
| [4. Template Design](#4-template-design) | BDD scenario template and TDD test plan template |
| [5. Shared Schema Integration](#5-shared-schema-integration) | Input validation, Clark transformation mapping, error handling |
| [6. Cross-Skill Integration Model](#6-cross-skill-integration-model) | How /test-spec consumes /use-case output |
| [7. Quality Strategy](#7-quality-strategy) | Coverage mapping, 7 Cs quality framework, traceability |
| [8. Risk Register](#8-risk-register) | Implementation risks with mitigations |
| [L2: Strategic Implications](#l2-strategic-implications) | Long-term evolution, security posture, cross-skill pipeline |
| [ORCHESTRATION.yaml Reconciliation](#orchestrationyaml-reconciliation) | Mapping ORCH deliverables to architecture (SSOT) |
| [Self-Review Checklist](#self-review-checklist) | H-15 / S-010 verification |

---

## L0: Executive Summary

This document translates the Phase 2 architecture (3 documents, 1 JSON Schema, all scoring >= 0.95) into an implementation-ready specification for the `/test-spec` Jerry skill. The skill transforms structured use case artifacts produced by `/use-case` into BDD Gherkin test specifications using Clark's (2018) UC2.0-to-Gherkin mapping algorithm.

**What gets built.** 14 files organized under `skills/test-spec/`. Two agents: `tspec-generator` (transforms use case flows into Gherkin Feature files using Clark's deterministic mapping) and `tspec-analyst` (analyzes test coverage completeness against use case flow steps and extensions). Two templates provide the output formats. One rule file encodes Clark's transformation algorithm. One skill contract, one behavior test file, and the SKILL.md entry point complete the skill.

**Key architectural decisions.**

1. **2 agents, not 1.** The Phase 2 architecture (SSOT) defines 1 agent (`tspec-generator`) for `/test-spec` with a contingency: "If methodology section exceeds 1,500 tokens during Phase 3, split into `tspec-generator` (generation) and `tspec-validator` (7 Cs quality scoring)." This architecture introduces `tspec-analyst` (renamed from "tspec-validator" for clarity -- it performs coverage analysis, not pass/fail validation) because the two responsibilities require distinct cognitive modes: systematic for deterministic transformation, convergent for evaluative coverage analysis. The split is justified below in section 3.

2. **File-mediated integration.** Consistent with Step 9, `/test-spec` communicates with `/use-case` exclusively through the shared artifact file on disk, validated against `use-case-realization-v1.schema.json` at the input boundary. No direct agent-to-agent communication. P-003 compliant.

3. **Two-layer input validation.** Same pattern as Step 9: Layer 1 (JSON Schema structural validation of the use case artifact) plus Layer 2 (agent guardrail semantic validation of detail level, extension presence, and step type completeness). The input validation gate rejects insufficiently detailed use cases with actionable error messages directing users to `/use-case` for elaboration.

4. **ORCHESTRATION.yaml reconciliation.** The ORCHESTRATION.yaml lists `test-plan-generator` and `test-coverage-analyst` as agent names. The Phase 2 architecture (SSOT) defines `tspec-generator` with the `tspec-` prefix to avoid `ts-` collision with `/transcript`. This document uses the SSOT names (`tspec-generator`, `tspec-analyst`) and documents the mapping. See [ORCHESTRATION.yaml Reconciliation](#orchestrationyaml-reconciliation).

---

## L1: Technical Specification

### 1. File Manifest

14 files to create, organized by directory. All paths are relative to repository root.

#### Directory Tree

```
skills/test-spec/
+-- SKILL.md                                    # [F-01] Skill entry point (H-25)
+-- agents/
|   +-- tspec-generator.md                      # [F-02] Agent definition: UC-to-BDD generation
|   +-- tspec-generator.governance.yaml         # [F-03] Governance metadata (H-34)
|   +-- tspec-analyst.md                        # [F-04] Agent definition: test coverage analysis
|   +-- tspec-analyst.governance.yaml           # [F-05] Governance metadata (H-34)
+-- composition/
|   +-- tspec-generator.agent.yaml              # [F-06] Task tool invocation config
|   +-- tspec-generator.prompt.md               # [F-07] System prompt for Task invocation
|   +-- tspec-analyst.agent.yaml                # [F-08] Task tool invocation config
|   +-- tspec-analyst.prompt.md                 # [F-09] System prompt for Task invocation
+-- templates/
|   +-- bdd-scenario.template.md                # [F-10] Gherkin Feature output template
|   +-- test-plan.template.md                   # [F-11] TDD test plan output template
+-- rules/
|   +-- clark-transformation-rules.md           # [F-12] Clark (2018) mapping as agent rules
+-- contracts/
|   +-- TS_SKILL_CONTRACT.yaml                  # [F-13] Skill contract
+-- tests/
    +-- BEHAVIOR_TESTS.md                       # [F-14] BDD behavior tests for the skill
```

#### File Responsibility Matrix

| File ID | Primary Author (Sub-Step) | Reviewer | Criticality |
|---------|--------------------------|----------|-------------|
| F-01 | eng-lead (10a) | eng-reviewer | C3 |
| F-02, F-03 | eng-backend (10b) | eng-security, eng-reviewer | C3 |
| F-04, F-05 | eng-backend (10b) | eng-security, eng-reviewer | C3 |
| F-06, F-07 | eng-backend (10c) | eng-reviewer | C2 |
| F-08, F-09 | eng-backend (10c) | eng-reviewer | C2 |
| F-10, F-11 | eng-backend (10d) | eng-reviewer | C2 |
| F-12 | eng-backend (10e) | eng-reviewer | C3 |
| F-13 | eng-lead (10a) | eng-reviewer | C2 |
| F-14 | eng-qa (10f) | eng-reviewer | C3 |

**Composition file schema reference (F-06..F-09):** Composition files follow the canonical agent YAML schema (`docs/schemas/agent-canonical-v1.schema.json`). Reference implementation: `skills/use-case/composition/uc-author.agent.yaml` (Step 9). Required fields: `name`, `version`, `description`, `skill: test-spec`, `identity` (role, expertise, cognitive_mode), `model.tier`, `tools.native` (T1/T2 set), `tools.forbidden: [agent_delegate]`, `tool_tier`, `guardrails`, `output`, `constitution`. The `.prompt.md` files (F-07, F-09) contain the system prompt text used when the agent is invoked via Task tool -- a copy of the markdown body from the agent `.md` file.

**Skill contract specification (F-13):** TS_SKILL_CONTRACT.yaml follows the OpenAPI 3.0-inspired contract pattern established by Step 9 (`skills/use-case/contracts/UC_SKILL_CONTRACT.yaml`). Required top-level structure: `openapi: "3.0.3"`, `info` (title, version, description), `agents` (tspec-generator, tspec-analyst -- each with description, cognitive_mode, model, input/output schema), and `components.schemas`.

---

### 2. SKILL.md Design

#### Frontmatter (F-01)

```yaml
---
name: test-spec
description: >-
  BDD test specification generation from use case artifacts using Clark's (2018)
  UC2.0-to-Gherkin transformation algorithm. Transforms structured use case
  flows (basic flow, alternative flows, extensions) into Gherkin Feature files
  with Given-When-Then scenarios. Analyzes test coverage completeness against
  use case flow steps. Requires use case artifacts at detail_level >=
  ESSENTIAL_OUTLINE from /use-case skill. Invoke when generating test specs,
  BDD scenarios, Gherkin features, test plans, or analyzing test coverage
  from use cases.
version: "1.0.0"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
activation-keywords:
  - "test spec"
  - "test-spec"
  - "test specification"
  - "BDD"
  - "BDD scenario"
  - "Gherkin"
  - "feature file"
  - "Given When Then"
  - "generate tests from use case"
  - "Clark transformation"
  - "test coverage"
  - "test plan from use case"
  - "scenario mapping"
  - "happy path scenario"
  - "error scenario"
  - "test coverage analysis"
  - "use case to test"
---
```

#### Routing Keywords (Trigger Map Entry -- Priority 14)

Per agent-decomposition.md Trigger Map Extensions section:

| Column | Value |
|--------|-------|
| **Detected Keywords** | test spec, test-spec, test specification, BDD, BDD scenario, Gherkin, feature file, Given When Then, generate tests, Clark transformation, test coverage, test plan, scenario mapping, happy path scenario, error scenario, use case to test |
| **Negative Keywords** | requirements specification, V&V, technical review, use case authoring, write use case, create use case, OpenAPI, contract, API design, adversarial, tournament, transcript, penetration, exploit, code review, documentation, tutorial, unit test, pytest, integration test |
| **Priority** | 14 |
| **Compound Triggers** | "generate tests from use case" OR "BDD scenario" OR "feature file" OR "test specification" OR "test coverage analysis" OR "use case to test" (phrase match) |
| **Skill** | `/test-spec` |

**Priority 14 rationale:** Priority 14 places `/test-spec` one level below `/use-case` (priority 13). This ordering reflects the pipeline dependency: use case authoring must precede test generation. The keyword sets are disjoint from `/use-case` -- `/use-case` triggers on "write use case", "basic flow", "cockburn", "jacobson"; `/test-spec` triggers on "BDD", "Gherkin", "feature file", "test coverage". The negative keywords suppress false positives: "requirements specification" routes to `/nasa-se`; "unit test" and "pytest" are handled by Jerry's testing infrastructure directly, not by this skill; "write use case" routes to `/use-case`. Against `/adversary` (priority 7): "test" alone is suppressed by `/adversary`'s "quality scoring" and "adversarial" positive keywords; `/test-spec` requires compound triggers ("BDD scenario", "feature file") that do not overlap.

**Disambiguation: "test" keyword.** The word "test" alone is deliberately excluded from the positive keywords. In isolation, "test" is ambiguous: it could mean unit tests (no skill needed), adversarial quality testing (`/adversary`), or BDD test specification (`/test-spec`). The compound triggers require qualification ("BDD scenario", "test specification", "feature file") to route to `/test-spec`. This prevents AP-02 (Bag of Triggers) collisions with `/adversary` and direct pytest usage.

#### Agent Routing Table

| Agent | Role | Model | Cognitive Mode | Tool Tier | Decision Signal |
|-------|------|-------|---------------|-----------|-----------------|
| `tspec-generator` | Transforms use case flows into Gherkin BDD scenarios | sonnet | systematic | T2 | "generate", "transform", "create feature file", "map to Gherkin", "BDD from use case", "Clark" |
| `tspec-analyst` | Analyzes test coverage completeness against use case flows | sonnet | convergent | T1 | "coverage", "analyze coverage", "coverage gap", "missing scenarios", "completeness check", "7 Cs" |

**Default routing:** When intent is ambiguous between generation and analysis, route to `tspec-generator` first. Generation must precede coverage analysis. If the user says "generate and check coverage", invoke `tspec-generator` first, then `tspec-analyst` on the output.

#### When to Use

**Activate when:**

- Generating BDD Gherkin scenarios from a use case artifact
- Transforming use case flows (basic, alternative, extensions) into test specifications
- Creating a test plan document from use case structure
- Analyzing test coverage completeness against use case flow steps
- Verifying that all use case extensions have corresponding error scenarios
- Mapping use case preconditions/postconditions to Given/Then clauses

**NEVER invoke this skill when:**

- Task is writing or editing use case artifacts -- Consequence: `/test-spec` agents do not implement Cockburn's writing methodology; they consume use case output, not produce it; use `/use-case` instead.
- Task is generating API contracts from use case artifacts -- Consequence: `/test-spec` produces Gherkin BDD scenarios, not OpenAPI specifications; use `/contract-design` instead.
- Task is writing unit tests or pytest code -- Consequence: `/test-spec` produces human-readable BDD specifications, not executable test code; write tests directly or use `/eng-team` for test implementation guidance.
- Task is adversarial quality review of deliverables -- Consequence: use `/adversary` for quality scoring and adversarial critique.
- Use case artifact is at detail_level < ESSENTIAL_OUTLINE -- Consequence: Clark transformation requires typed flow steps and extensions; artifacts below ESSENTIAL_OUTLINE lack these; use `/use-case` to elaborate first.

#### Integration Points

| Integration | Direction | Mechanism | Pre-Condition |
|-------------|-----------|-----------|---------------|
| `/use-case` to `/test-spec` | tspec-generator reads UC artifact produced by uc-author/uc-slicer | Shared artifact file validated against `use-case-realization-v1.schema.json` | `$.detail_level` >= `ESSENTIAL_OUTLINE`, `$.extensions` non-empty, `$.basic_flow[*].type` present |
| `/test-spec` to `/worktracker` | tspec-analyst may update worktracker with coverage metrics | Bash + `uv run jerry items update` (H-05 compliant; MUST NOT invoke /worktracker via Task -- P-003) | Feature file exists with traceable scenario IDs |
| `/test-spec` output consumed by implementers | Feature files serve as acceptance criteria for implementation | Human-readable `.feature.md` files in project `test-specs/` directory | Scenarios verified by tspec-analyst coverage check |

---

### 3. Agent Definition Specifications

#### 3.1 Agent: tspec-generator

**Agent Split Justification**

The Phase 2 architecture defines a single `tspec-generator` agent with a contingency for splitting. This architecture introduces the split because:

1. **Distinct cognitive modes.** Clark transformation is a systematic, deterministic mapping (basic flow -> happy path scenario; extension -> error scenario). Coverage analysis is a convergent evaluation (assess completeness, identify gaps, rank coverage priorities). These are two different reasoning patterns per agent-development-standards.md Mode Selection Guide.

2. **Methodology section size.** The Clark transformation algorithm alone requires approximately 1,200 tokens (7 mapping steps + lookup table + slice-scoped generation logic). Adding the 7 Cs quality framework (~800 tokens) and coverage gap analysis (~600 tokens) exceeds the 1,500-token threshold from Pattern 1. The split keeps each agent's methodology under 1,500 tokens.

3. **Different input/output profiles.** `tspec-generator` reads a use case artifact and writes Feature files. `tspec-analyst` reads Feature files and the source use case artifact to produce a coverage report. They operate on different primary inputs.

4. **Invocation frequency difference.** Generation runs once per use case. Coverage analysis may run multiple times (after each generation iteration, after manual feature file edits, during quality gate reviews). Separating them allows independent invocation.

**Agent naming note:** "tspec-analyst" is chosen over "tspec-validator" because the agent performs evaluative coverage analysis (identifying gaps, computing coverage ratios, recommending priorities), not binary pass/fail validation. "Analyst" matches the convergent cognitive mode. "Validator" would imply a systematic pass/fail check which is a subset of what this agent does.

##### Official Frontmatter (F-02: `tspec-generator.md`)

```yaml
---
name: tspec-generator
description: >-
  BDD Test Specification Generator agent. Transforms use case artifacts into
  Gherkin BDD Feature files using Clark's (2018) UC2.0-to-Gherkin mapping
  algorithm. Maps basic flow to happy path scenario, alternative flows to
  additional scenarios, and extensions to error/negative scenarios. Requires
  input use case at detail_level >= ESSENTIAL_OUTLINE with typed flow steps.
  Invoke when generating, transforming, creating, or mapping use case flows
  to Gherkin BDD scenarios.
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

##### Governance YAML (F-03: `tspec-generator.governance.yaml`)

```yaml
version: "1.0.0"
tool_tier: "T2"
reasoning_effort: high

identity:
  role: "BDD Test Specification Generator -- transforms use case artifacts into Gherkin BDD Feature files using Clark's (2018) UC2.0-to-Gherkin mapping algorithm"
  expertise:
    - "Clark (2018) UC2.0-to-Gherkin transformation algorithm (basic flow to happy path, alternative flow to additional scenario, extension to error scenario)"
    - "BDD/Gherkin specification writing (Feature/Scenario/Given-When-Then structure, declarative style, Cucumber best practices)"
    - "Use case flow type interpretation (actor_action, system_response, validation) and mechanical mapping to Gherkin clause types (When, Then, And)"
  cognitive_mode: "systematic"

persona:
  tone: "methodical"
  communication_style: "structured"
  audience_level: "adaptive"

capabilities:
  forbidden_actions:
    - "P-003 VIOLATION: NEVER spawn recursive subagents or delegate to other agents via Task tool -- Consequence: agent hierarchy violation breaks orchestrator-worker topology and causes uncontrolled token consumption. tspec-generator is a T2 worker agent without Task tool access."
    - "P-020 VIOLATION: NEVER override user decisions about scenario scope, test priority, or feature file organization -- Consequence: unauthorized test scope changes erode trust and may invalidate test plans that depend on user-approved coverage boundaries."
    - "P-022 VIOLATION: NEVER misrepresent test coverage completeness -- Consequence: claiming full coverage when extensions are unmapped causes downstream implementers to believe all error paths are tested, leaving failure paths untested in production."
    - "SCHEMA VIOLATION: NEVER generate scenarios from use case artifacts that fail input validation (detail_level < ESSENTIAL_OUTLINE or missing extensions) -- Consequence: generating from incomplete input produces scenarios that omit error paths and lack Given clause grounding, creating a false sense of test completeness."
    - "METHODOLOGY VIOLATION: NEVER invent scenarios that do not trace to a specific use case flow step -- Consequence: untraceable scenarios cannot be verified against the use case source, breaking the Clark mapping contract and undermining the methodological guarantee that every scenario has a provenance chain."
  forbidden_action_format: "NPT-009-complete"
  output_formats:
    - "markdown"

guardrails:
  input_validation:
    - "Input artifact must exist and contain valid YAML frontmatter with $.work_type = USE_CASE"
    - "Input artifact $.detail_level must be >= ESSENTIAL_OUTLINE (reject BRIEFLY_DESCRIBED and BULLETED_OUTLINE with actionable error message)"
    - "Input artifact must have $.extensions array with at least 1 entry"
    - "Input artifact must have $.basic_flow with 3-9 steps, each with $.type field"
  output_filtering:
    - "no_secrets_in_output"
    - "every_scenario_must_trace_to_source_flow_step"
    - "all_given_clauses_must_derive_from_preconditions_or_flow_context"
    - "all_then_clauses_must_derive_from_postconditions_or_system_responses"
    - "scenario_names_must_include_source_step_reference"
  fallback_behavior: "escalate_to_user"

output:
  required: true
  location: "projects/${JERRY_PROJECT}/test-specs/UC-{DOMAIN}-{NNN}-{slug}.feature.md"
  template: "skills/test-spec/templates/bdd-scenario.template.md"
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
    - "verify_feature_file_created_at_output_location"
    - "verify_one_scenario_per_basic_flow"
    - "verify_one_scenario_per_alternative_flow"
    - "verify_one_scenario_per_extension"
    - "verify_all_scenarios_have_source_step_traceability"
    - "verify_given_clauses_present_in_happy_path"
    - "verify_then_clauses_present_in_happy_path"

session_context:
  on_receive:
    - "Load use case artifact and validate frontmatter against schema"
    - "Determine if generating for full use case or specific slice"
    - "Count expected scenario count: 1 (basic) + N (alternatives) + M (extensions)"
  on_send:
    - "Report feature file path and scenario count"
    - "List key findings: scenarios generated, coverage ratio (generated vs. expected), any unmapped flows"
    - "Flag if coverage is incomplete (some flows could not be mapped)"

enforcement:
  tier: "medium"
  escalation_path: "eng-reviewer"
```

##### System Prompt Outline (F-02 markdown body)

The markdown body of `tspec-generator.md` MUST include these XML-tagged sections per `agent-development-standards.md`:

| Section Tag | Content Summary |
|-------------|----------------|
| `<identity>` | BDD Test Specification Generator role. Systematic cognitive mode. Applies Clark's (2018) deterministic mapping algorithm. Distinction from tspec-analyst: generation (Clark transformation) vs. analysis (coverage evaluation). |
| `<purpose>` | Transforms structured use case artifacts into Gherkin BDD Feature files. Each use case flow element maps mechanically to a Gherkin scenario type. Enables testable acceptance criteria derivation from use case specifications. |
| `<input>` | Use case artifact at `$.detail_level` >= `ESSENTIAL_OUTLINE`. Must have: `$.basic_flow[*]` with `.type` field, `$.extensions[*]` with `.outcome` field, optionally `$.alternative_flows[*]`, `$.preconditions[*]`, `$.postconditions`. Optionally: specific slice ID for slice-scoped generation. |
| `<capabilities>` | Reads use case artifacts and shared schema. Writes Feature files (`.feature.md`) and optional test plan documents. Validates input against schema before transformation. No external research, no cross-session state, no delegation. |
| `<methodology>` | Clark (2018) UC2.0-to-Gherkin transformation algorithm (7-step process from agent-decomposition.md lines 236-246). Clark Mapping Table (deterministic lookup from agent-decomposition.md lines 248-259). Slice-scoped generation mode (from agent-decomposition.md lines 261-268). Reference: `skills/test-spec/rules/clark-transformation-rules.md` for operational rules. |
| `<output>` | Gherkin Feature file at `projects/${JERRY_PROJECT}/test-specs/UC-{DOMAIN}-{NNN}-{slug}.feature.md`. Template: `skills/test-spec/templates/bdd-scenario.template.md`. Optional: test plan at `projects/${JERRY_PROJECT}/test-specs/UC-{DOMAIN}-{NNN}-{slug}-test-plan.md`. |
| `<guardrails>` | Constitutional triplet (P-003, P-020, P-022). Domain guardrails: reject detail_level < ESSENTIAL_OUTLINE, reject missing extensions, every scenario must trace to source step, Given clauses from preconditions, Then clauses from postconditions/system_responses, step type determines Gherkin clause type (SD-07), extension outcome determines scenario type (SD-08). |

---

#### 3.2 Agent: tspec-analyst

##### Official Frontmatter (F-04: `tspec-analyst.md`)

```yaml
---
name: tspec-analyst
description: >-
  Test Coverage Analyst agent. Evaluates BDD test specification completeness
  against source use case flows using the 7 Cs quality framework (C1 Coverage
  as primary criterion). Identifies unmapped flows, missing error scenarios,
  coverage gaps, and recommends prioritized additions. Reads both the Feature
  file and the source use case artifact for cross-reference analysis. Invoke
  when analyzing coverage, checking completeness, identifying test gaps, or
  evaluating test specification quality against use case source.
model: sonnet
tools:
  - Read
  - Glob
  - Grep
  - Bash
---
```

**Tool tier: T1 (Read-Only).** The tspec-analyst agent reads Feature files and use case artifacts but does not modify them. Its output is a coverage report written to a new file, but it does not edit existing feature files or use case artifacts. T1 is selected per the principle of least privilege: the analysis function only needs read access to source artifacts; coverage reports are written as new files using Bash (echo/redirect via `uv run`). After review, T2 is warranted because the agent needs to write the coverage report file directly using the Write tool. T1 + Bash workaround for file writing would be an unnecessary complication when T2 provides clean Write access.

**Revised tool tier: T2 (Read-Write).** T2 is selected because the agent must write the coverage analysis report file. The Bash tool alone for file writes is fragile (quoting issues, large content) compared to the Write tool. This follows the same rationale as all other artifact-producing agents in the pipeline.

```yaml
---
name: tspec-analyst
description: >-
  Test Coverage Analyst agent. Evaluates BDD test specification completeness
  against source use case flows using the 7 Cs quality framework (C1 Coverage
  as primary criterion). Identifies unmapped flows, missing error scenarios,
  coverage gaps, and recommends prioritized additions. Reads both the Feature
  file and the source use case artifact for cross-reference analysis. Invoke
  when analyzing coverage, checking completeness, identifying test gaps, or
  evaluating test specification quality against use case source.
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

##### Governance YAML (F-05: `tspec-analyst.governance.yaml`)

```yaml
version: "1.0.0"
tool_tier: "T2"
reasoning_effort: high

identity:
  role: "Test Coverage Analyst -- evaluates BDD test specification completeness against source use case flows using the 7 Cs quality framework"
  expertise:
    - "7 Cs quality framework application to BDD test specifications (C1 Coverage as primary, C2-C7 as supporting quality indicators)"
    - "Use case flow-to-scenario traceability analysis (cross-referencing scenario Given/When/Then clauses against source basic_flow, alternative_flows, and extensions)"
    - "Test coverage gap identification and prioritized remediation recommendation"
  cognitive_mode: "convergent"

persona:
  tone: "analytical"
  communication_style: "evidence-based"
  audience_level: "adaptive"

capabilities:
  forbidden_actions:
    - "P-003 VIOLATION: NEVER spawn recursive subagents or delegate to other agents via Task tool -- Consequence: agent hierarchy violation breaks orchestrator-worker topology and causes uncontrolled token consumption. tspec-analyst is a T2 worker agent without Task tool access."
    - "P-020 VIOLATION: NEVER override user decisions about coverage priorities or acceptable coverage thresholds -- Consequence: unauthorized coverage threshold changes may cause the user to accept insufficient test coverage for high-risk flows."
    - "P-022 VIOLATION: NEVER misrepresent coverage metrics or gap severity -- Consequence: inflated coverage percentages or downgraded gap severity causes downstream teams to believe error paths are tested when they are not, leaving production failure paths unvalidated."
    - "ANALYSIS VIOLATION: NEVER modify Feature files or use case artifacts during analysis -- Consequence: tspec-analyst is a read-and-report agent; modifying source artifacts corrupts the provenance chain and may introduce untraceable scenarios that break Clark mapping guarantees."
    - "METHODOLOGY VIOLATION: NEVER report coverage without cross-referencing against the source use case artifact -- Consequence: coverage analysis based only on the Feature file cannot detect missing scenarios because there is no baseline to compare against; the use case artifact is the coverage baseline."
  forbidden_action_format: "NPT-009-complete"
  output_formats:
    - "markdown"

guardrails:
  input_validation:
    - "Feature file must exist at expected path and contain Gherkin Scenario blocks"
    - "Source use case artifact must exist and contain valid YAML frontmatter with $.work_type = USE_CASE"
    - "Source use case must have $.basic_flow, $.extensions (minimum for coverage baseline)"
  output_filtering:
    - "no_secrets_in_output"
    - "coverage_percentages_must_be_mathematically_verifiable"
    - "every_gap_must_cite_specific_unmapped_flow_element"
    - "recommendations_must_include_priority_and_effort_estimate"
  fallback_behavior: "escalate_to_user"

output:
  required: true
  location: "projects/${JERRY_PROJECT}/test-specs/UC-{DOMAIN}-{NNN}-{slug}-coverage.md"
  levels:
    - "L0"
    - "L1"
    - "L2"

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
    - "verify_coverage_report_created_at_output_location"
    - "verify_coverage_percentage_is_computed"
    - "verify_every_basic_flow_step_is_accounted_for"
    - "verify_every_extension_is_accounted_for"
    - "verify_gaps_cite_specific_flow_elements"

session_context:
  on_receive:
    - "Load Feature file and source use case artifact"
    - "Count total mappable flow elements: basic_flow steps + alternative_flows + extensions"
    - "Parse Feature file scenario list"
  on_send:
    - "Report coverage percentage and gap count"
    - "List key findings: mapped flows, unmapped flows, highest-priority gaps"
    - "Flag if coverage is below acceptable threshold for the goal level"

enforcement:
  tier: "medium"
  escalation_path: "eng-reviewer"
```

##### System Prompt Outline (F-04 markdown body)

| Section Tag | Content Summary |
|-------------|----------------|
| `<identity>` | Test Coverage Analyst role. Convergent cognitive mode. Evaluates completeness, identifies gaps, produces coverage reports. Distinction from tspec-generator: analysis (evaluative) vs. generation (transformative). |
| `<purpose>` | Verifies that generated BDD test specifications achieve adequate coverage of the source use case flows. Provides quantitative coverage metrics and prioritized gap remediation recommendations. |
| `<input>` | (1) Feature file produced by tspec-generator. (2) Source use case artifact with flow definitions. Both are required -- coverage analysis requires a baseline (use case) and a measured artifact (feature file). |
| `<capabilities>` | Reads Feature files and use case artifacts. Writes coverage analysis reports. Searches for related feature files across the project. Does not modify Feature files or use case artifacts. |
| `<methodology>` | 7 Cs quality framework (C1 Coverage primary, C2 Correctness, C3 Clarity, C4 Consistent Abstraction, C5 Consistent Structure, C6 Completeness of detail, C7 Conciseness). Coverage computation: mapped_scenarios / total_mappable_flows. Gap prioritization: extensions with outcome=failure > alternative flows > extensions with outcome=rejoin > extensions with outcome=success. |
| `<output>` | Coverage analysis report at `projects/${JERRY_PROJECT}/test-specs/UC-{DOMAIN}-{NNN}-{slug}-coverage.md`. Includes: L0 (coverage percentage, gap count, pass/fail assessment), L1 (per-flow mapping table, gap details, remediation recommendations), L2 (coverage trend analysis across related use cases, risk assessment for uncovered paths). |
| `<guardrails>` | Constitutional triplet (P-003, P-020, P-022). Domain guardrails: requires both Feature file and source UC artifact, coverage percentages must be mathematically verifiable, every gap must cite specific unmapped flow, does not modify source artifacts, does not generate scenarios (that is tspec-generator's domain). |

---

### 4. Template Design

#### F-10: bdd-scenario.template.md

**Purpose:** Primary output template for Gherkin Feature files. Implements the Clark transformation output format with YAML frontmatter for traceability back to the source use case.

**Used by:** `tspec-generator` (primary output)

**Format:** YAML frontmatter delimited by `---` followed by Gherkin Feature specification.

```markdown
---
source_use_case: UC-{DOMAIN}-{NNN}
source_title: "{USE_CASE_TITLE}"
source_detail_level: {DETAIL_LEVEL}
source_goal_level: {GOAL_LEVEL}
generated_by: tspec-generator
generated_at: "{ISO_8601_DATETIME}"
scenario_count: {TOTAL_SCENARIO_COUNT}
coverage:
  basic_flow_mapped: true
  alternative_flows_mapped: {ALT_FLOW_COUNT}
  extensions_mapped: {EXT_COUNT}
  total_flows: {TOTAL_FLOW_COUNT}
  mapped_flows: {MAPPED_FLOW_COUNT}
slice_id: null  # Populated when slice-scoped generation
version: "1.0.0"
---

# Feature: {USE_CASE_TITLE}

> As a {PRIMARY_ACTOR}, I want to {GOAL_DESCRIPTION} so that {STAKEHOLDER_INTEREST}.

## Happy Path

### Scenario: {USE_CASE_TITLE} - Main Success Scenario

**Source:** basic_flow (steps 1-{N})

Given {PRECONDITION_1}
  And {PRECONDITION_2}
When {PRIMARY_ACTOR} {ACTOR_ACTION_STEP_1}
  And System {SYSTEM_RESPONSE_STEP_2}
  And {ACTOR} {ACTOR_ACTION_STEP_3}
Then {POSTCONDITION_SUCCESS_1}
  And {POSTCONDITION_SUCCESS_2}

## Alternative Flows

### Scenario: {ALT_FLOW_NAME} - branches from step {N}

**Source:** AF-{NN} (branches_from_step: {N}, condition: "{CONDITION}")

Given {PRECONDITIONS}
  And {ALT_FLOW_CONDITION}
When {ALT_FLOW_STEPS}
Then {ALT_FLOW_OUTCOME}

## Error Scenarios

### Scenario: {EXTENSION_NAME} - error at step {N}

**Source:** EXT-{STEP}{LETTER} (anchor_step: {N}, outcome: failure)

Given {PRECONDITIONS}
  And {EXTENSION_CONDITION}
When {EXTENSION_TRIGGER_STEP}
Then {ERROR_HANDLING_STEPS}
  And {FAILURE_POSTCONDITION}

## Traceability Matrix

| Scenario | Source Flow | Source Step | Type |
|----------|-----------|------------|------|
| Main Success Scenario | basic_flow | 1-{N} | happy_path |
| {ALT_FLOW_NAME} | AF-{NN} | {BRANCH_STEP} | alternative |
| {EXT_NAME} | EXT-{STEP}{LETTER} | {ANCHOR_STEP} | error ({OUTCOME}) |
```

**Template design decisions:**

| Decision | Choice | Rationale |
|----------|--------|-----------|
| TD-01: YAML frontmatter in Feature files | Include frontmatter with source UC reference | Enables automated traceability verification. `tspec-analyst` can parse frontmatter to cross-reference source UC. Consistent with use case artifact format pattern. |
| TD-02: Scenario grouping by type | Happy Path, Alternative Flows, Error Scenarios sections | Reflects Clark's mapping categories. Readers can quickly locate error scenarios vs. happy path. Consistent with Cucumber documentation conventions. |
| TD-03: Source citation in every scenario | `**Source:** {flow_id} (step: {N})` annotation | Clark transformation guarantee: every scenario traces to a source flow. Without explicit citation, coverage analysis cannot verify completeness. |
| TD-04: Traceability matrix at end | Tabular summary of all scenario-to-flow mappings | Provides at-a-glance coverage view. Enables tspec-analyst to parse mappings programmatically. |
| TD-05: .feature.md extension | Markdown wrapper around Gherkin content | Standard `.feature` files cannot contain YAML frontmatter or Markdown sections. The `.feature.md` extension signals "Gherkin content in Markdown container." If Cucumber consumption is needed, the `scripts/extract-gherkin.sh` script (file-organization.md line 286) strips the Markdown wrapper. |

#### F-11: test-plan.template.md

**Purpose:** TDD test plan document template. Produced optionally by `tspec-generator` when a comprehensive test plan is requested (not just Feature file generation).

**Used by:** `tspec-generator` (optional output), `tspec-analyst` (reference for coverage analysis)

```markdown
---
source_use_case: UC-{DOMAIN}-{NNN}
source_title: "{USE_CASE_TITLE}"
plan_type: "BDD-TDD"
generated_by: tspec-generator
generated_at: "{ISO_8601_DATETIME}"
total_scenarios: {TOTAL}
priority_distribution:
  P0_critical: {COUNT}
  P1_high: {COUNT}
  P2_medium: {COUNT}
  P3_low: {COUNT}
version: "1.0.0"
---

# Test Plan: {USE_CASE_TITLE}

## Summary

| Metric | Value |
|--------|-------|
| Source Use Case | UC-{DOMAIN}-{NNN} |
| Goal Level | {GOAL_LEVEL} ({GOAL_SYMBOL}) |
| Total Scenarios | {TOTAL} |
| Happy Path | 1 |
| Alternative Flows | {ALT_COUNT} |
| Error Scenarios | {EXT_COUNT} |
| Coverage | {COVERAGE_PERCENT}% |

## Test Priority Matrix

| Priority | Scenarios | Rationale |
|----------|-----------|-----------|
| P0 (Critical) | {SCENARIO_NAMES} | Happy path + failure extensions for primary actor flows |
| P1 (High) | {SCENARIO_NAMES} | Alternative flows with business-critical conditions |
| P2 (Medium) | {SCENARIO_NAMES} | Extensions with rejoin outcomes |
| P3 (Low) | {SCENARIO_NAMES} | Extensions with alternate success outcomes |

## Scenario Inventory

### {SCENARIO_NAME}

| Field | Value |
|-------|-------|
| Source | {FLOW_ID}, step {STEP_N} |
| Type | {happy_path / alternative / error} |
| Priority | {P0-P3} |
| Given | {PRECONDITIONS} |
| When | {TRIGGER_ACTIONS} |
| Then | {EXPECTED_OUTCOMES} |
| Implementation Notes | {NOTES} |

## Coverage Gaps

{IDENTIFIED_GAPS_OR_NONE}

## Implementation Sequence

1. {FIRST_SCENARIO_TO_IMPLEMENT} (P0 -- establishes happy path)
2. {SECOND_SCENARIO} (P0 -- covers primary failure mode)
...
```

**Test plan template rationale:** The test plan template serves a different audience than the Feature file. Feature files are consumed by test implementers writing Cucumber/test code. Test plans are consumed by project managers and tech leads planning test implementation work. The priority matrix (TD-06) maps to Clark's output: basic flow = P0, extensions with outcome=failure = P0, alternative flows = P1/P2, extensions with outcome=success/rejoin = P2/P3.

---

### 5. Shared Schema Integration

#### Input Validation: Use Case Artifact

`tspec-generator` validates every input use case artifact before transformation. The validation follows the same two-layer pattern established by Step 9.

**Layer 1: JSON Schema Structural Validation (Deterministic)**

| What It Checks | Schema Mechanism | Token Cost |
|----------------|-----------------|-----------|
| Required fields present (11 fields including `$.basic_flow`) | `required` array | 0 |
| `$.basic_flow` has 3-9 items | `minItems: 3, maxItems: 9` | 0 |
| Each `$.basic_flow[*]` has `.step`, `.actor`, `.action`, `.type` | `$defs/flow_step` required fields | 0 |
| `$.basic_flow[*].type` is valid enum | `enum: [actor_action, system_response, validation]` | 0 |
| `$.extensions[*]` structure (id, name, anchor_step, condition, steps, outcome) | `$defs/extension` required fields | 0 |
| `$.extensions[*].outcome` matches pattern | `pattern: ^(success\|failure\|rejoin:\d+)$` | 0 |
| `$.alternative_flows[*]` structure (if present) | `$defs/alternative_flow` required fields | 0 |

**Layer 2: Agent Guardrail Semantic Validation (LLM-Evaluated)**

| What It Checks | Why Not in Schema | Agent Responsible |
|----------------|-------------------|-------------------|
| `$.detail_level` >= `ESSENTIAL_OUTLINE` | Agent-specific precondition | `tspec-generator` |
| `$.extensions` array is non-empty (at least 1 entry) | Structurally valid to have 0 extensions; agent decides completeness | `tspec-generator` |
| `$.basic_flow[*].type` values enable meaningful Clark transformation | Schema validates enum but not semantic usefulness | `tspec-generator` |
| `$.preconditions` present (for Given clause quality) | Optional field; absence is a quality warning, not a rejection | `tspec-generator` |
| `$.postconditions.success` present (for Then clause quality) | Optional field; absence is a quality warning, not a rejection | `tspec-generator` |

**Error Handling When Input Validation Fails:**

| Failure Type | Agent Response |
|-------------|----------------|
| `$.detail_level` < `ESSENTIAL_OUTLINE` | REJECT: "UC {id} is at {detail_level}. Clark transformation requires ESSENTIAL_OUTLINE or FULLY_DESCRIBED. Use /use-case to elaborate the use case first." |
| `$.extensions` absent or empty | REJECT: "UC {id} has no extensions. BDD test specifications require at least one extension to generate error scenarios. Use /use-case to add extension conditions." |
| `$.basic_flow` has < 3 steps | REJECT: "UC {id} basic_flow has {N} steps (minimum 3). The basic flow is insufficient for scenario generation. Use /use-case to elaborate the basic flow." |
| `$.basic_flow[*].type` missing on any step | REJECT: "UC {id} basic_flow step {N} is missing the type field. Clark transformation requires typed steps (actor_action, system_response, validation). Use /use-case to add step types." |
| `$.preconditions` absent | WARN: "UC {id} has no preconditions. Generated Given clauses will be limited. Consider adding preconditions via /use-case for richer test specifications." (Proceed with generation.) |
| `$.postconditions.success` absent | WARN: "UC {id} has no success postconditions. Generated Then clauses will be derived from system_response steps only. Consider adding postconditions via /use-case." (Proceed with generation.) |

#### Clark Transformation Mapping (Schema Field to Gherkin Element)

This is the deterministic mapping implemented by `tspec-generator`. Each use case schema field maps to a specific Gherkin element:

| Use Case Schema Field | JSON Path | Gherkin Element | Cardinality | Clark Rule |
|-----------------------|-----------|-----------------|-------------|------------|
| Title | `$.title` | Feature title | 1:1 | Step 2 |
| Goal level description | `$.goal_level` | Feature description | 1:1 | Step 2 |
| Primary actor | `$.primary_actor` | Scenario subject ("As a {actor}") | 1:1 | Step 2 |
| Preconditions | `$.preconditions[*]` | Given clauses | 1:N | Step 3 |
| Trigger | `$.trigger` | First When clause | 1:1 | Step 3 |
| Basic flow (actor_action steps) | `$.basic_flow[*]` where `.type = actor_action` | When clauses | 1:N | Step 3 (SD-07) |
| Basic flow (system_response steps) | `$.basic_flow[*]` where `.type = system_response` | Then clauses | 1:N | Step 3 (SD-07) |
| Basic flow (validation steps) | `$.basic_flow[*]` where `.type = validation` | Then assertion clauses | 1:N | Step 3 (SD-07) |
| Success postconditions | `$.postconditions.success[*]` | Final Then clauses | 1:N | Step 3 |
| Alternative flows | `$.alternative_flows[*]` | Additional Scenario (1 per flow) | 1:1 per alt flow | Step 4 |
| Alt flow condition | `$.alternative_flows[*].condition` | Given clause (additional condition) | 1:1 | Step 4 |
| Alt flow rejoin | `$.alternative_flows[*].rejoins_at_step` | Then clause (merge to step N) | 1:1 or null | Step 4 |
| Extensions | `$.extensions[*]` | Error/negative Scenario (1 per ext) | 1:1 per extension | Step 5 |
| Extension condition | `$.extensions[*].condition` | Given clause (error condition) | 1:1 | Step 5 |
| Extension outcome=failure | `$.extensions[*].outcome = "failure"` | Negative test scenario | 1:1 | Step 5 (SD-08) |
| Extension outcome=success | `$.extensions[*].outcome = "success"` | Alternate success scenario | 1:1 | Step 5 (SD-08) |
| Extension outcome=rejoin:{N} | `$.extensions[*].outcome = "rejoin:{N}"` | Additional scenario merging to step N | 1:1 | Step 5 (SD-08) |
| Slices (optional) | `$.slices[*].steps_included` | Scope filter for slice-scoped generation | Filter | Slice-scoped mode |

---

### 6. Cross-Skill Integration Model

#### Pipeline Position

```
/use-case                      /test-spec                     /contract-design
+---------------------------+  +---------------------------+  +-------------------+
| uc-author -> uc-slicer    |  | tspec-generator           |  | cd-generator      |
|                           |  |   |                       |  |                   |
| Produces:                 |  | Reads:                    |  | Reads:            |
|  $.basic_flow             |->|  $.basic_flow             |  |  $.interactions   |
|  $.alternative_flows      |  |  $.alternative_flows      |  |                   |
|  $.extensions             |  |  $.extensions             |  |                   |
|  $.preconditions          |  |  $.preconditions          |  |                   |
|  $.postconditions         |  |  $.postconditions         |  |                   |
|  $.trigger                |  |  $.trigger                |  |                   |
|  $.interactions           |  |  $.slices (optional)      |  |                   |
+---------------------------+  |                           |  +-------------------+
                               | Writes:                    |
                               |  .feature.md (external)    |
                               |  -test-plan.md (optional)  |
                               |                           |
                               | tspec-analyst              |
                               |   Reads:                   |
                               |    .feature.md + UC source |
                               |   Writes:                  |
                               |    -coverage.md (external) |
                               +---------------------------+
```

**Key integration properties:**

1. **tspec-generator does NOT modify the use case artifact.** It reads the artifact's YAML frontmatter, performs Clark transformation, and writes a separate Feature file. The source artifact remains unchanged.

2. **tspec-analyst reads both the Feature file and the source UC artifact.** Coverage analysis requires two inputs: the baseline (use case) and the measured artifact (feature file). Cross-referencing produces the coverage metric.

3. **No dependency on `/contract-design`.** `/test-spec` and `/contract-design` are independent consumers of `/use-case` output. They read different blocks of the same artifact (flows vs. interactions). Neither depends on the other.

4. **Slice-scoped generation.** When `$.slices[*]` are present in the use case artifact, `tspec-generator` can generate a Feature file scoped to a specific slice's `steps_included`, producing targeted test specifications for individual implementation increments.

#### Integration Pre-Conditions

| Pre-Condition | Validation Mechanism | Failure Action |
|---------------|---------------------|----------------|
| Use case artifact exists at expected path | File existence check (Read tool) | REJECT with path guidance |
| `$.work_type = USE_CASE` discriminator present | YAML frontmatter parse | REJECT: "Not a use case artifact" |
| `$.detail_level >= ESSENTIAL_OUTLINE` | Agent guardrail (Layer 2) | REJECT with elaboration guidance |
| `$.basic_flow` has 3-9 typed steps | Schema validation (Layer 1) | REJECT with step count/type guidance |
| `$.extensions` non-empty | Agent guardrail (Layer 2) | REJECT with extension authoring guidance |
| Schema validates overall | JSON Schema (Layer 1) | REJECT with validation error details |

---

### 7. Quality Strategy

#### Coverage Computation Model

The fundamental quality metric for `/test-spec` is **C1 Coverage**: the ratio of use case flow elements mapped to Gherkin scenarios.

**Coverage formula:**

```
coverage = mapped_scenarios / total_mappable_flows

where:
  total_mappable_flows = 1 (basic_flow)
                       + count($.alternative_flows)
                       + count($.extensions)

  mapped_scenarios = count(scenarios in Feature file
                          that trace to a source flow element)
```

**Coverage targets by goal level:**

| Goal Level | Target Coverage | Rationale |
|------------|----------------|-----------|
| USER_GOAL | 100% | Core use cases must have complete BDD coverage. All flows mapped. |
| SUMMARY | 80%+ | Summary-level UCs may have flows too abstract for direct BDD mapping. |
| SUBFUNCTION | 100% | Subfunctions are granular; complete coverage is achievable and expected. |

**Coverage gap priority ordering:**

| Priority | Gap Type | Rationale |
|----------|----------|-----------|
| P0 | Basic flow unmapped | Without a happy path scenario, no baseline test exists |
| P0 | Extension with outcome=failure unmapped | Failure paths are the highest-risk test gaps |
| P1 | Alternative flow unmapped | Alternative flows represent distinct business-critical paths |
| P2 | Extension with outcome=rejoin unmapped | Rejoin paths are error-recovery scenarios |
| P3 | Extension with outcome=success unmapped | Alternate success paths are lower-risk variations |

#### 7 Cs Quality Framework Application

The 7 Cs framework (from Clark research, DI-06, PAT-004) evaluates generated BDD specifications across seven quality dimensions:

| Criterion | Assessment Method | Pass Condition |
|-----------|-------------------|----------------|
| C1: Coverage | `mapped_scenarios / total_mappable_flows` | >= target for goal level |
| C2: Correctness | Each scenario's Given/When/Then traces to correct source elements | Zero incorrect mappings |
| C3: Clarity | Scenarios use declarative language ("what" not "how") | No implementation-specific language |
| C4: Consistent Abstraction | All scenarios at same abstraction level (no mixing UI detail with business logic) | Uniform abstraction across feature file |
| C5: Consistent Structure | All scenarios follow the same Given-When-Then pattern | No structural variation |
| C6: Completeness of Detail | Given clauses include all relevant preconditions; Then clauses include all postconditions | No missing precondition or postcondition |
| C7: Conciseness | No duplicate scenarios; no redundant steps within scenarios | Zero duplicates |

**Primary vs. supporting criteria:** C1 (Coverage) is the primary quality gate. C2-C7 are supporting quality indicators evaluated by `tspec-analyst` in the coverage report. A Feature file that achieves 100% C1 coverage but fails C2 (incorrect mappings) is flagged for revision.

---

### 8. Risk Register

| Risk ID | Category | Risk | Severity | Likelihood | Mitigation | Source |
|---------|----------|------|----------|------------|------------|--------|
| RISK-03 | Architecture | Clark transformation produces incorrect Gherkin mapping for complex extension chains | HIGH | LOW | Clark mapping is deterministic (lookup table, not generative). `tspec-analyst` cross-references output against source. rules/clark-transformation-rules.md provides explicit mapping reference. | DI-05, PAT-008 |
| RISK-07 | Quality | BDD scenario coverage gaps for use cases with many alternative flows | MEDIUM | MEDIUM | `tspec-analyst` computes coverage ratio and identifies gaps. Priority ordering ensures failure paths (P0) are generated first. Slice-scoped generation allows incremental coverage building. | DI-06, PAT-004 |
| RISK-15 | Implementation | 2-agent split creates unnecessary overhead if tspec-analyst invoked < 20% of time | LOW | MEDIUM | Monitor invocation frequency. Coverage analysis is lightweight (T2 read + write report). Merge to 1 agent if coverage analysis proves unnecessary after 20 feature file generations. | CF-04 |
| RISK-16 | Implementation | Clark transformation rules file (F-12) becomes too long for agent context budget | MEDIUM | LOW | Rules file targets < 500 lines. The Clark mapping is a 7-step algorithm with a deterministic lookup table; this is inherently compact. If rules exceed 500 lines, split into core mapping rules (Steps 1-5) and supplementary quality rules (Steps 6-7). | CB-05 |
| RISK-17 | Integration | Use case artifacts from `/use-case` arrive with inconsistent step types ($.basic_flow[*].type) | MEDIUM | LOW | Layer 2 input validation explicitly checks each step for type field. Rejection message directs user to `/use-case` for type annotation. Schema validation (Layer 1) catches missing type fields structurally. | SD-07 |
| RISK-18 | Quality | Extension outcome patterns (success/failure/rejoin) ambiguous in source UC | MEDIUM | LOW | Schema enforces `$.extensions[*].outcome` pattern `^(success\|failure\|rejoin:\d+)$`. Agent guardrail validates each extension has a classifiable outcome. If pattern does not match, agent escalates to user per H-31. | SD-08 |
| RISK-19 | Routing | "test" keyword collision with /adversary and direct pytest usage | MEDIUM | LOW | "test" alone excluded from positive keywords. Compound triggers require qualification ("BDD scenario", "feature file", "test specification"). Negative keywords suppress "unit test", "pytest". Priority 14 does not compete with /adversary at priority 7 on disjoint keyword sets. | AP-02, trigger map |
| RISK-20 | Integration | Feature file .feature.md extension not recognized by Cucumber tooling | LOW | MEDIUM | By design: `.feature.md` is a Markdown container for Gherkin content with YAML frontmatter (TD-05). `scripts/extract-gherkin.sh` (from file-organization.md) strips the Markdown wrapper for Cucumber consumption. Users who need pure `.feature` files can run the extraction script. | file-org line 286 |

---

## L2: Strategic Implications

### Long-Term Architectural Evolution

The `/test-spec` skill is the second skill in the three-skill pipeline. Its architecture establishes patterns specific to downstream consumer skills:

1. **Input validation gate as standard pattern.** The two-layer validation gate (JSON Schema structural + agent guardrail semantic) for consuming upstream artifacts is now established by both `/use-case` (output validation) and `/test-spec` (input validation). `/contract-design` should replicate this pattern for its input validation of the `$.interactions` block.

2. **Coverage analysis as a separate agent.** Separating generation from evaluation (tspec-generator vs. tspec-analyst) establishes a creator-evaluator pattern within a single skill. This is distinct from the cross-skill /adversary quality gate -- tspec-analyst evaluates domain-specific coverage, not general deliverable quality. `/contract-design` may benefit from a similar pattern (contract generation vs. contract validation).

3. **Feature file format as downstream contract.** The `.feature.md` format with YAML frontmatter becomes a de facto output contract for `/test-spec`. If other skills or tools consume Feature files, they should parse this format. The `source_use_case` frontmatter field enables automated traceability chains: UC artifact -> Feature file -> (future) test implementation.

### Security Posture Assessment

**Threat surface:** The `/test-spec` skill operates at T2 (Read-Write) tier for both agents. `tspec-generator` reads use case artifacts and writes Feature files. `tspec-analyst` reads Feature files and use case artifacts, writes coverage reports. No external network access (T3), no cross-session state (T4), no delegation (T5).

**STRIDE analysis (C1 -- routine, per skill scope):**

| Threat | Applicable? | Mitigation |
|--------|------------|------------|
| **S**poofing | LOW -- agents identified by name in composition files | Agent name validated by Task tool invocation |
| **T**ampering | LOW -- Feature files written to project workspace | tspec-analyst does not modify source artifacts; git tracks changes |
| **R**epudiation | LOW -- `generated_by` and `generated_at` fields in Feature file frontmatter | Metadata audit trail in Feature file YAML |
| **I**nformation Disclosure | LOW -- no secrets in use case artifacts or Feature files | `no_secrets_in_output` guardrail on both agents |
| **D**enial of Service | LOW -- context budget is the only resource consumed | CB-05 offset/limit on large file reads |
| **E**levation of Privilege | LOW -- T2 agents cannot access Task tool (H-35) | Tool tier enforcement in frontmatter `tools` field |

**NIST CSF 2.0 mapping:**

| Function | Control | Implementation |
|----------|---------|----------------|
| Identify | Asset inventory | Feature files and coverage reports cataloged via `source_use_case` frontmatter reference |
| Protect | Access control | T2 tier limits tool access; agents cannot escalate |
| Detect | Validation | Two-layer input validation detects invalid UC artifacts before transformation |
| Respond | Error handling | Fallback: `escalate_to_user` on both agents; tspec-analyst does not modify artifacts |
| Recover | Version control | Git tracks all Feature file changes; UC source artifacts provide regeneration baseline |

### Cross-Skill Pipeline Trust Boundary

The trust boundary established by Step 9 (shared artifact validated against `use-case-realization-v1.schema.json`) continues to operate at the `/test-spec` input boundary:

- A malformed artifact from `/use-case` cannot cause `tspec-generator` to produce incorrect output -- the input validation gate rejects it.
- The `$.work_type = USE_CASE` discriminator prevents non-use-case artifacts from being processed.
- The `$.detail_level >= ESSENTIAL_OUTLINE` gate enforces minimum quality before transformation.
- `tspec-generator` does not write back to the source artifact, maintaining the unidirectional data flow.

---

## ORCHESTRATION.yaml Reconciliation

The ORCHESTRATION.yaml (Step 10 deliverables) lists agent names and file paths that differ from the Phase 2 architecture (SSOT). This section documents the mapping.

### Agent Name Mapping

| ORCHESTRATION.yaml Name | Architecture (SSOT) Name | Rationale |
|------------------------|--------------------------|-----------|
| `test-plan-generator` | `tspec-generator` | Phase 2 architecture establishes `tspec-` prefix to avoid `ts-` collision with `/transcript`. "generator" function name is preserved. |
| `test-coverage-analyst` | `tspec-analyst` | Phase 2 architecture uses `tspec-` prefix. "analyst" replaces "coverage-analyst" for brevity per AD-M-001 kebab-case pattern. |

### File Path Mapping

| ORCHESTRATION.yaml Deliverable | Architecture File ID | Actual Path |
|-------------------------------|---------------------|-------------|
| `skills/test-spec/agents/test-plan-generator.md` | F-02 | `skills/test-spec/agents/tspec-generator.md` |
| `skills/test-spec/agents/test-plan-generator.governance.yaml` | F-03 | `skills/test-spec/agents/tspec-generator.governance.yaml` |
| `skills/test-spec/agents/test-coverage-analyst.md` | F-04 | `skills/test-spec/agents/tspec-analyst.md` |
| `skills/test-spec/agents/test-coverage-analyst.governance.yaml` | F-05 | `skills/test-spec/agents/tspec-analyst.governance.yaml` |
| `skills/test-spec/templates/bdd-scenario-template.md` | F-10 | `skills/test-spec/templates/bdd-scenario.template.md` |
| `skills/test-spec/templates/tdd-test-plan-template.md` | F-11 | `skills/test-spec/templates/test-plan.template.md` |
| `skills/test-spec/SKILL.md` | F-01 | `skills/test-spec/SKILL.md` (unchanged) |

**Naming convention applied:** File names follow the naming conventions established in file-organization.md (agent definition: `{prefix}-{function}.md`; template: `{descriptor}.template.{ext}`). The ORCHESTRATION.yaml names were preliminary; the architecture document names are authoritative.

### Additional Files Not in ORCHESTRATION.yaml

The following files are produced by this architecture but were not listed in the ORCHESTRATION.yaml deliverables:

| File ID | Path | Rationale for Addition |
|---------|------|----------------------|
| F-06 | `skills/test-spec/composition/tspec-generator.agent.yaml` | Required by dual-file + composition architecture (Step 9 pattern) |
| F-07 | `skills/test-spec/composition/tspec-generator.prompt.md` | Required by composition architecture |
| F-08 | `skills/test-spec/composition/tspec-analyst.agent.yaml` | Required by composition architecture |
| F-09 | `skills/test-spec/composition/tspec-analyst.prompt.md` | Required by composition architecture |
| F-12 | `skills/test-spec/rules/clark-transformation-rules.md` | Core transformation algorithm as agent rules (from file-org line 284) |
| F-13 | `skills/test-spec/contracts/TS_SKILL_CONTRACT.yaml` | Skill contract (from file-org line 288) |
| F-14 | `skills/test-spec/tests/BEHAVIOR_TESTS.md` | BDD behavior tests (from file-org line 290) |

---

## Self-Review Checklist (H-15, S-010)

- [x] **P-001 (Truth/Accuracy):** Every agent specification traces to agent-decomposition.md (tspec-generator: lines 212-294). Clark mapping rules cite S-03, DI-05, DI-06, PAT-008. Schema field references use JSON path notation matching shared-schema.json.
- [x] **P-002 (File Persistence):** Architecture document persisted at designated output path.
- [x] **P-004 (Provenance):** Phase 2 architecture documents cited throughout with version numbers and quality scores. Lineage block traces all dependencies.
- [x] **P-011 (Evidence-Based):** Agent split justification cites 4 independent criteria (cognitive modes, methodology size, I/O profiles, invocation frequency). Tool tier selection justified per principle of least privilege.
- [x] **P-020 (User Authority):** Status is PROPOSED, not ACCEPTED. ORCHESTRATION.yaml reconciliation documents naming divergences transparently.
- [x] **P-022 (No Deception):** tspec-analyst tool tier analysis initially considered T1 then explicitly revised to T2 with reasoning documented. Risk register includes RISK-15 (2-agent split overhead) as acknowledged concern.
- [x] **H-23 (Navigation):** Navigation table present with anchor links.
- [x] **H-34 (Dual-file architecture):** Both agents defined with .md frontmatter (Claude Code official fields only) and .governance.yaml (schema-validated). Constitutional triplet (P-003, P-020, P-022) present in both agents.
- [x] **H-35 (Constitutional compliance):** Both agents have >= 3 forbidden_actions. Neither worker agent has Task tool. Both declare P-003, P-020, P-022 in constitution.principles_applied.
- [x] **L0/L1/L2:** All three output levels present with appropriate audience depth.
- [x] **Consistency with Step 9:** File manifest format, governance YAML structure, composition file references, template design patterns, two-layer validation gate, risk register format, and STRIDE analysis all follow Step 9 architecture (v1.2.0) conventions.
- [x] **Schema integration:** Input validation references shared-schema.json fields by JSON path. Clark transformation mapping table links every UC schema field to its Gherkin output element.
- [x] **ORCHESTRATION.yaml reconciliation:** All 7 ORCH deliverables mapped to architecture file IDs with rationale for naming differences. 7 additional files documented.

### Adversarial Self-Check (S-002: Devil's Advocate)

**Challenge 1: "Is the 2-agent split premature? The Phase 2 architecture explicitly designed for 1 agent."**
The Phase 2 architecture includes the contingency: "If methodology section exceeds 1,500 tokens during Phase 3, split." The analysis in section 3 documents 4 independent criteria met for splitting. The split is reversible (RISK-15): if tspec-analyst invocation drops below 20% after 20 feature file generations, the agents can be merged. Starting with 2 agents is lower-risk than starting with 1 and splitting later (which would require updating composition files, SKILL.md routing, and behavior tests mid-implementation).

**Challenge 2: "Why is tspec-analyst T2 when it only reads and reports? Should it be T1?"**
This was explicitly analyzed in section 3.2. The agent must write the coverage report file. Using Bash for file writes (the T1 workaround) introduces quoting fragility and content size limitations. The Write tool (T2) provides clean file writing. The principle of least privilege is satisfied because T2 is the lowest tier that supports artifact writing.

**Challenge 3: "The .feature.md extension is nonstandard. Consumers expect .feature files."**
Correct. The `.feature.md` extension is a deliberate design choice (TD-05) to enable YAML frontmatter for traceability. The `scripts/extract-gherkin.sh` script (from file-organization.md) provides the extraction path for consumers that require standard `.feature` files. The trade-off is: traceability metadata (essential for tspec-analyst cross-referencing) vs. immediate Cucumber compatibility (achievable via extraction).

### Pre-Mortem (S-004): "It's 6 months later and /test-spec failed -- why?"

**Failure Mode 1: tspec-generator produces Gherkin that does not match Clark's published algorithm.**
Signal: Quality review finds scenarios that are invented rather than derived from source flows.
Mitigation: `clark-transformation-rules.md` (F-12) encodes the deterministic mapping. tspec-analyst cross-references every scenario against source flows. Post-completion checks verify 1:1 cardinality.

**Failure Mode 2: Use case artifacts from /use-case consistently fail /test-spec input validation.**
Signal: > 50% of UC artifacts are rejected by tspec-generator.
Mitigation: This indicates `/use-case` default output level is too low for `/test-spec` consumption. The fix is in `/use-case`: change the default detail_level from BULLETED_OUTLINE to ESSENTIAL_OUTLINE. The rejection messages guide users to `/use-case` for elaboration.

**Failure Mode 3: Coverage analysis by tspec-analyst adds no value -- users never invoke it.**
Signal: tspec-analyst invocation rate < 10% after 30 feature file generations.
Mitigation: Merge tspec-analyst back into tspec-generator as the post-generation quality check step. This reduces the agent count to 1 (matching the Phase 2 minimum design).

---

*Architecture Design Version: 1.0.0*
*Constitutional Compliance: P-001 (truth), P-002 (file persistence), P-003 (no recursive subagents), P-004 (provenance), P-011 (evidence-based alternatives), P-020 (user authority -- PROPOSED status), P-022 (no deception -- tool tier revision documented, split risk acknowledged)*
*Adversary Review Required: YES -- C4 all-10-strategy review at >= 0.95 threshold*
*Next Agent: adv-scorer (initial scoring)*
*Workflow ID: use-case-skills-20260308-001*
