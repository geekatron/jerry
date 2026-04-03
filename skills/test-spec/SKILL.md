---
name: test-spec
description: BDD test specification generation from use case artifacts using Clark's (2018) UC2.0-to-Gherkin transformation algorithm. Transforms structured use case flows (basic flow, alternative flows, extensions) into Gherkin Feature files with Given-When-Then scenarios. Analyzes test coverage completeness against use case flow steps. Requires use case artifacts at detail_level >= ESSENTIAL_OUTLINE from /use-case skill. Invoke when generating test specs, BDD scenarios, Gherkin features, test plans, or analyzing test coverage from use cases.
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

> **Version:** 1.0.0 | **Framework:** Jerry Framework | **Constitutional compliance:** P-003 (no recursive subagents), P-020 (user authority), P-022 (no deception)
> **Status:** PROPOSED | **Author:** eng-backend | **Date:** 2026-03-09

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Document Audience](#document-audience) | Who reads which sections |
| [Purpose](#purpose) | What this skill does and key capabilities |
| [When to Use](#when-to-use) | Activation conditions and anti-patterns |
| [Available Agents](#available-agents) | Agent routing table with decision signals |
| [P-003 Agent Topology](#p-003-agent-topology) | ASCII hierarchy diagram (multi-agent required) |
| [Invoking an Agent](#invoking-an-agent) | Three invocation modes |
| [Clark Transformation Reference](#clark-transformation-reference) | Domain methodology summary |
| [Input Requirements](#input-requirements) | Use case artifact prerequisites |
| [Output Artifacts](#output-artifacts) | Feature file and coverage report formats |
| [Integration Points](#integration-points) | Cross-skill connections |
| [Routing Entry (Priority 14)](#routing-entry-priority-14) | Trigger map entry for mandatory-skill-usage.md |
| [Constitutional Compliance](#constitutional-compliance) | Principle-to-agent mapping |
| [Quick Reference](#quick-reference) | Common workflows and agent selection |
| [References](#references) | File paths and external citations |

---

## Document Audience

| Level | Audience | Sections |
|-------|----------|---------|
| L0 | Stakeholders, project managers | [Purpose](#purpose), [When to Use](#when-to-use), [Quick Reference](#quick-reference) |
| L1 | Developers, QA engineers using the skill | [Available Agents](#available-agents), [Invoking an Agent](#invoking-an-agent), [Clark Transformation Reference](#clark-transformation-reference), [Input Requirements](#input-requirements), [Output Artifacts](#output-artifacts) |
| L2 | Framework maintainers, reviewers | [P-003 Agent Topology](#p-003-agent-topology), [Integration Points](#integration-points), [Constitutional Compliance](#constitutional-compliance), [References](#references) |

---

## Purpose

The `/test-spec` skill transforms structured use case artifacts produced by `/use-case` into BDD Gherkin test specifications using Clark's (2018) UC2.0-to-Gherkin deterministic mapping algorithm. It closes the gap between use case specifications and testable acceptance criteria.

**Key Capabilities:**

- Deterministic Clark transformation: every use case flow element maps to exactly one Gherkin scenario type (no invented scenarios)
- Happy path generation: basic flow -> 1 happy path Scenario with Given/When/Then clauses derived from preconditions, steps, and postconditions
- Error scenario generation: each extension -> 1 error/negative/rejoin Scenario determined by outcome type (failure, success, rejoin:{N})
- Alternative flow coverage: each alternative_flow -> 1 additional Scenario
- Full traceability: every Scenario carries a Source annotation and the Feature file includes a Traceability Matrix
- Coverage analysis: quantitative C1 Coverage metrics (mapped / total_mappable flows) with 7 Cs quality framework assessment and prioritized gap remediation
- Slice-scoped generation: when slices are defined via uc-slicer, generate Feature files scoped to specific implementation increments

---

## When to Use

**Activate this skill when:**

- Generating BDD Gherkin scenarios from a use case artifact
- Transforming use case flows (basic, alternative, extensions) into test specifications
- Creating a test plan document from use case structure for project planning
- Analyzing test coverage completeness against use case flow steps
- Verifying that all use case extensions have corresponding error scenarios
- Mapping use case preconditions/postconditions to Given/Then clauses

**NEVER invoke this skill when:**

- Task is writing or editing use case artifacts -- Consequence: `/test-spec` agents do not implement Cockburn's writing methodology; they consume use case output, not produce it; use `/use-case` instead.
- Task is generating API contracts from use case artifacts -- Consequence: `/test-spec` produces Gherkin BDD scenarios, not OpenAPI specifications; use `/contract-design` instead.
- Task is writing unit tests or pytest code -- Consequence: `/test-spec` produces human-readable BDD specifications, not executable test code; write tests directly or use `/eng-team` for test implementation guidance.
- Task is adversarial quality review of deliverables -- Consequence: use `/adversary` for quality scoring and adversarial critique.
- Use case artifact is at detail_level < ESSENTIAL_OUTLINE -- Consequence: Clark transformation requires typed flow steps and extensions; artifacts below ESSENTIAL_OUTLINE lack these; use `/use-case` to elaborate first.

---

## Available Agents

| Agent | Role | Model | Cognitive Mode | Tool Tier | Output Location | Decision Signal |
|-------|------|-------|----------------|-----------|-----------------|-----------------|
| `tspec-generator` | Transforms use case flows into Gherkin BDD scenarios using Clark algorithm | sonnet | systematic | T2 | `projects/${JERRY_PROJECT}/test-specs/UC-{DOMAIN}-{NNN}-{slug}.feature.md` | "generate", "transform", "create feature file", "map to Gherkin", "BDD from use case", "Clark" |
| `tspec-analyst` | Analyzes test coverage completeness against use case flows using 7 Cs framework | sonnet | convergent | T2 | `projects/${JERRY_PROJECT}/test-specs/UC-{DOMAIN}-{NNN}-{slug}-coverage.md` | "coverage", "analyze coverage", "coverage gap", "missing scenarios", "completeness check", "7 Cs" |

**Default routing:** When intent is ambiguous between generation and analysis, route to `tspec-generator` first. Generation must precede coverage analysis. When the user says "generate and check coverage," invoke `tspec-generator` first, then `tspec-analyst` on the output.

---

## P-003 Agent Topology

Both `tspec-generator` and `tspec-analyst` are T2 worker agents. They are invoked independently from MAIN CONTEXT. They do NOT invoke each other. The output of tspec-generator (Feature file on disk) is consumed by tspec-analyst via the filesystem -- not via direct agent-to-agent communication.

```
MAIN CONTEXT (orchestrator)
    |
    +-- tspec-generator (T2 worker) -- via Task tool
    |   Reads: UC artifact (.md with YAML frontmatter)
    |         docs/schemas/use-case-realization-v1.schema.json
    |         skills/test-spec/rules/clark-transformation-rules.md
    |   Writes: Feature file (.feature.md)
    |           Optional: test plan (-test-plan.md)
    |
    +-- tspec-analyst (T2 worker) -- via Task tool
        Reads: Feature file (.feature.md) -- produced by tspec-generator
               UC artifact (.md) -- same source artifact
        Writes: Coverage report (-coverage.md)

Workers do NOT invoke each other.
tspec-generator output (Feature file) is consumed by tspec-analyst via filesystem.
Cross-agent data flow is mediated by shared artifact files on disk (P-003 compliant).
```

---

## Invoking an Agent

### Natural Language Invocation

```
Generate BDD scenarios from use case UC-AUTH-001.
```

```
Analyze test coverage for the Feature file at
projects/PROJ-021/test-specs/UC-AUTH-001-validate-credentials.feature.md
against the source use case.
```

### Explicit Agent Invocation

```
Use tspec-generator to transform UC-AUTH-001 from
projects/PROJ-021/use-cases/UC-AUTH-001-validate-credentials.md
into a Gherkin Feature file.
```

```
Use tspec-analyst to produce a coverage report for
UC-AUTH-001-validate-credentials.feature.md.
```

### Task Tool Invocation (composition file)

```yaml
# Invoke tspec-generator via Task tool
task:
  agent: skills/test-spec/composition/tspec-generator.agent.yaml
  prompt: |
    Transform use case at projects/PROJ-021/use-cases/UC-AUTH-001-validate-credentials.md
    into a Gherkin Feature file. Output path:
    projects/PROJ-021/test-specs/UC-AUTH-001-validate-credentials.feature.md
```

```yaml
# Invoke tspec-analyst via Task tool
task:
  agent: skills/test-spec/composition/tspec-analyst.agent.yaml
  prompt: |
    Analyze coverage for:
    Feature file: projects/PROJ-021/test-specs/UC-AUTH-001-validate-credentials.feature.md
    Source UC: projects/PROJ-021/use-cases/UC-AUTH-001-validate-credentials.md
    Output coverage report to:
    projects/PROJ-021/test-specs/UC-AUTH-001-validate-credentials-coverage.md
```

---

## Clark Transformation Reference

Clark's (2018) UC2.0-to-Gherkin algorithm provides a deterministic mapping from use case structure to Gherkin Feature file structure. Full rules are in `skills/test-spec/rules/clark-transformation-rules.md`.

### Core Mapping Table

| Use Case Element | JSON Path | Gherkin Element | Cardinality | Rule |
|-----------------|-----------|-----------------|-------------|------|
| Title | `$.title` | Feature name | 1:1 | RULE-C2-01 |
| Primary actor | `$.primary_actor` | "As a" narrative | 1:1 | RULE-C2-01 |
| Preconditions | `$.preconditions[*]` | Given clauses | 1:N | RULE-C6-01 |
| Trigger | `$.trigger` | First When clause | 1:1 | RULE-C3-01 |
| Basic flow (actor_action steps) | `$.basic_flow[*]` type=actor_action | When clauses | 1:N | RULE-ST-01 |
| Basic flow (system_response steps) | `$.basic_flow[*]` type=system_response | Then clauses | 1:N | RULE-ST-02 |
| Basic flow (validation steps) | `$.basic_flow[*]` type=validation | Then assertion clauses | 1:N | RULE-ST-03 |
| Success postconditions | `$.postconditions.success[*]` | Final Then clauses | 1:N | RULE-C3-01 |
| Alternative flows | `$.alternative_flows[*]` | Additional Scenario (1 each) | 1:1 | RULE-C4-01 |
| Extensions (failure) | `$.extensions[*]` outcome=failure | Negative test Scenario | 1:1 | RULE-OT-01 |
| Extensions (success) | `$.extensions[*]` outcome=success | Alternate success Scenario | 1:1 | RULE-OT-02 |
| Extensions (rejoin) | `$.extensions[*]` outcome=rejoin:{N} | Rejoin Scenario to step N | 1:1 | RULE-OT-03 |

### 7 Cs Quality Framework (tspec-analyst)

| Criterion | Assessment |
|-----------|-----------|
| C1: Coverage | Primary -- mapped_scenarios / total_mappable_flows |
| C2: Correctness | Each scenario traces to correct source elements |
| C3: Clarity | Declarative language; no implementation specifics |
| C4: Consistent Abstraction | Uniform abstraction level across Feature file |
| C5: Consistent Structure | All scenarios follow Given-When-Then |
| C6: Completeness of Detail | All preconditions and postconditions included |
| C7: Conciseness | No duplicates; no redundant steps |

---

## Input Requirements

### Minimum Input (tspec-generator)

Use case artifact must satisfy ALL of the following (enforced by two-layer validation gate):

| Requirement | Field | Validation Layer |
|-------------|-------|-----------------|
| `$.work_type = USE_CASE` | Discriminator | Agent guardrail (Layer 2) |
| `$.detail_level >= ESSENTIAL_OUTLINE` | detail_level | Agent guardrail (Layer 2) |
| `$.basic_flow` has 3-9 steps | basic_flow | Schema (Layer 1) |
| Each `$.basic_flow[*]` has `.type` field | basic_flow[*].type | Schema (Layer 1) |
| `$.extensions` non-empty (1+ entries) | extensions | Agent guardrail (Layer 2) |

### Recommended Input (higher output quality)

- `$.preconditions[*]` -- enables Given clauses grounded in system state
- `$.postconditions.success[*]` -- enables Then clauses grounded in outcomes
- `$.trigger` -- enables first When clause grounded in initiating event
- `$.alternative_flows[*]` -- enables alternative scenario generation

### Input for tspec-analyst (both required)

1. Feature file at `projects/${JERRY_PROJECT}/test-specs/UC-{DOMAIN}-{NNN}-{slug}.feature.md`
2. Source UC artifact at `projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md`

---

## Output Artifacts

### tspec-generator: Feature File

**Path:** `projects/${JERRY_PROJECT}/test-specs/UC-{DOMAIN}-{NNN}-{slug}.feature.md`
**Format:** YAML frontmatter + Gherkin Feature content in Markdown sections
**Schema:** `docs/schemas/test-specification-v1.schema.json`
**Template:** `skills/test-spec/templates/bdd-scenario.template.md`

The `.feature.md` extension indicates "Gherkin content in a Markdown container with YAML frontmatter." This enables traceability metadata (source_use_case, generated_by, coverage snapshot) that standard `.feature` files cannot carry.

### tspec-analyst: Coverage Report

**Path:** `projects/${JERRY_PROJECT}/test-specs/UC-{DOMAIN}-{NNN}-{slug}-coverage.md`
**Format:** Markdown with L0/L1/L2 sections
**Template:** `skills/test-spec/templates/test-plan.template.md`

---

## Integration Points

| Integration | Direction | Mechanism | Pre-Condition |
|-------------|-----------|-----------|---------------|
| `/use-case` to `/test-spec` | tspec-generator reads UC artifact produced by uc-author or uc-slicer | Shared artifact file validated against `docs/schemas/use-case-realization-v1.schema.json` | `$.detail_level >= ESSENTIAL_OUTLINE`, `$.extensions` non-empty, `$.basic_flow[*].type` present |
| `/test-spec` to `/worktracker` | tspec-analyst may update worktracker with coverage metrics | Bash + `uv run jerry items update` (H-05 compliant; MUST NOT invoke /worktracker via Task -- P-003) | Feature file exists with traceable scenario IDs |
| `/test-spec` output consumed by implementers | Feature files serve as acceptance criteria for implementation | Human-readable `.feature.md` files in `projects/${JERRY_PROJECT}/test-specs/` | Scenarios verified by tspec-analyst coverage check |
| `/test-spec` parallel to `/contract-design` | Both are independent consumers of `/use-case` output | File-mediated -- both read the same UC artifact; neither depends on the other | UC artifact at ESSENTIAL_OUTLINE or FULLY_DESCRIBED |

---

## Routing Entry (Priority 14)

Per `agent-routing-standards.md` enhanced 5-column trigger map format. Registration in `mandatory-skill-usage.md` is complete.

| Detected Keywords | Negative Keywords | Priority | Compound Triggers | Skill |
|---|---|---|---|---|
| test spec, test-spec, test specification, BDD, BDD scenario, Gherkin, feature file, Given When Then, generate tests, Clark transformation, test coverage, test plan, scenario mapping, happy path scenario, error scenario, use case to test | requirements specification, V&V, technical review, use case authoring, write use case, create use case, OpenAPI, contract, API design, adversarial, tournament, transcript, penetration, exploit, code review, documentation, tutorial, unit test, pytest, integration test | 14 | "generate tests from use case" OR "BDD scenario" OR "feature file" OR "test specification" OR "test coverage analysis" OR "use case to test" (phrase match) | `/test-spec` |

**Disambiguation: "test" keyword.** "test" alone is excluded from positive keywords -- it is ambiguous between unit tests, adversarial testing, and BDD specification. Compound triggers require qualification ("BDD scenario", "feature file", "test specification") to route to `/test-spec`.

---

## Constitutional Compliance

| Principle | Application |
|-----------|-------------|
| P-001 (Truth/Accuracy) | Every generated scenario must trace to a source flow element. tspec-generator does not invent scenarios. |
| P-002 (File Persistence) | All outputs persisted to files: Feature files and coverage reports written to `projects/${JERRY_PROJECT}/test-specs/`. |
| P-003 (No Recursive Subagents) | tspec-generator and tspec-analyst are T2 worker agents. Neither has Task tool access. Neither invokes the other directly. |
| P-004 (Provenance) | Feature file YAML frontmatter carries source_use_case, generated_by, generated_at for full audit trail. |
| P-020 (User Authority) | tspec-generator does not override user decisions about scenario scope. tspec-analyst does not override user decisions about coverage thresholds. |
| P-022 (No Deception) | tspec-generator explicitly reports unmapped flows. tspec-analyst reports mathematically verifiable coverage percentages with numerator and denominator. |

---

## Quick Reference

### Common Workflows

| Workflow | Agent Sequence | Typical Duration |
|----------|---------------|-----------------|
| Generate BDD specs from UC | tspec-generator (single invocation) | 1-2 minutes |
| Generate + verify coverage | tspec-generator then tspec-analyst | 2-4 minutes |
| Coverage-only check (FF already exists) | tspec-analyst (single invocation) | 1-2 minutes |
| Slice-scoped generation | tspec-generator with slice_id parameter | 1-2 minutes |
| Full pipeline: UC to verified test specs | /use-case (uc-author) -> tspec-generator -> tspec-analyst | 5-10 minutes |

### Agent Selection Hints

| Signal | Route to |
|--------|----------|
| "Generate", "create", "transform", "make BDD scenarios" | tspec-generator |
| "Coverage", "analyze", "check completeness", "gaps", "missing" | tspec-analyst |
| Ambiguous intent | tspec-generator first (generation must precede analysis) |
| "Generate and check coverage" | tspec-generator, then tspec-analyst on output |

### Input Validation Quick Check

Before invoking tspec-generator, verify your use case artifact has:
- [ ] `detail_level: ESSENTIAL_OUTLINE` or `FULLY_DESCRIBED`
- [ ] `extensions:` array with at least 1 entry
- [ ] `basic_flow:` with 3-9 steps
- [ ] Each basic_flow step has a `type:` field (actor_action, system_response, or validation)

---

## References

| File | Purpose |
|------|---------|
| `skills/test-spec/agents/tspec-generator.md` | tspec-generator agent definition |
| `skills/test-spec/agents/tspec-generator.governance.yaml` | tspec-generator governance metadata |
| `skills/test-spec/agents/tspec-analyst.md` | tspec-analyst agent definition |
| `skills/test-spec/agents/tspec-analyst.governance.yaml` | tspec-analyst governance metadata |
| `skills/test-spec/composition/tspec-generator.agent.yaml` | tspec-generator canonical agent YAML (Task invocation) |
| `skills/test-spec/composition/tspec-generator.prompt.md` | tspec-generator system prompt copy |
| `skills/test-spec/composition/tspec-analyst.agent.yaml` | tspec-analyst canonical agent YAML (Task invocation) |
| `skills/test-spec/composition/tspec-analyst.prompt.md` | tspec-analyst system prompt copy |
| `skills/test-spec/rules/clark-transformation-rules.md` | Clark (2018) mapping algorithm as imperative rules |
| `skills/test-spec/templates/bdd-scenario.template.md` | Feature file output template |
| `skills/test-spec/templates/test-plan.template.md` | Test plan output template |
| `skills/test-spec/tests/BEHAVIOR_TESTS.md` | BDD behavior test scenarios for the skill |
| `skills/test-spec/samples/sample-test-specification.md` | Sample Feature file demonstrating the skill output |
| `docs/schemas/test-specification-v1.schema.json` | JSON Schema for Feature file YAML frontmatter |
| `docs/schemas/use-case-realization-v1.schema.json` | JSON Schema for input use case artifacts |
| Clark (2018) | Clark, T. D. (2018). Generating BDD Test Scenarios from Use Case Specifications. ICSTW 2018. |

---

> *Skill Version: 1.0.0 | Framework: Jerry Framework | Constitutional compliance: P-003, P-020, P-022*
> *Author: eng-backend | Date: 2026-03-09 | Status: ACTIVE*
> *SSOT: `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/implementation/step-10-test-spec-architecture.md`*
