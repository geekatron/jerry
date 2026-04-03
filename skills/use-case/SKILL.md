---
name: use-case
description: Guided use case authoring and decomposition using Cockburn's 12-step writing process and Jacobson UC 2.0 progressive narrative levels. Creates structured use case artifacts with YAML frontmatter validated against use-case-realization-v1.schema.json. Decomposes use cases into implementation-ready slices with INVEST criteria verification and produces realization interaction sequences for downstream /test-spec and /contract-design consumption. Invoke when writing, creating, authoring, elaborating, slicing, decomposing, or realizing use cases.
version: "1.0.0"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
activation-keywords:
  - "use case"
  - "use-case"
  - "write use case"
  - "create use case"
  - "author use case"
  - "elaborate use case"
  - "Cockburn"
  - "UC 2.0"
  - "Jacobson"
  - "actor goal"
  - "basic flow"
  - "main success scenario"
  - "extensions"
  - "alternative flow"
  - "use case slice"
  - "slice use case"
  - "INVEST criteria"
  - "use case realization"
  - "interaction sequence"
  - "goal level"
  - "primary actor"
  - "fully dressed"
  - "essential outline"
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
| [P-003 Agent Topology](#p-003-agent-topology) | ASCII hierarchy diagram -- multi-agent topology |
| [Invoking an Agent](#invoking-an-agent) | Three invocation modes |
| [Methodology Reference](#methodology-reference) | Cockburn 12-step and Jacobson UC 2.0 summary |
| [Input Requirements](#input-requirements) | Prerequisites per agent |
| [Output Artifacts](#output-artifacts) | Use case artifact and slice formats |
| [Integration Points](#integration-points) | Cross-skill connections |
| [Routing Entry (Priority 13)](#routing-entry-priority-13) | Trigger map entry for mandatory-skill-usage.md |
| [Constitutional Compliance](#constitutional-compliance) | Principle-to-agent mapping |
| [Quick Reference](#quick-reference) | Common workflows and agent selection |
| [Elaboration State Matrix](#elaboration-state-matrix-detail_level-x-realization_level) | 2D valid-state and readiness matrix |
| [References](#references) | File paths and external citations |

---

## Document Audience

| Level | Audience | Sections |
|-------|----------|---------|
| L0 | Stakeholders, project managers | [Purpose](#purpose), [When to Use](#when-to-use), [Quick Reference](#quick-reference) |
| L1 | Developers, analysts using the skill | [Available Agents](#available-agents), [Invoking an Agent](#invoking-an-agent), [Methodology Reference](#methodology-reference), [Input Requirements](#input-requirements), [Output Artifacts](#output-artifacts) |
| L2 | Framework maintainers, reviewers | [P-003 Agent Topology](#p-003-agent-topology), [Integration Points](#integration-points), [Constitutional Compliance](#constitutional-compliance), [References](#references) |

---

## Purpose

The `/use-case` skill provides guided use case authoring and decomposition through two complementary agents that implement industry-standard methodologies:

1. **uc-author** implements Cockburn's 12-step writing process and Jacobson UC 2.0 progressive narrative levels (Briefly Described through Fully Described) for creating structured use case artifacts.
2. **uc-slicer** implements Jacobson UC 2.0 Activities 2, 4, and 5 for decomposing use cases into implementation-ready slices with INVEST criteria verification, and producing the realization interaction sequences that enable downstream `/test-spec` and `/contract-design` consumption.

**Key Capabilities:**

- Progressive elaboration: artifacts evolve through four detail levels (BRIEFLY_DESCRIBED, BULLETED_OUTLINE, ESSENTIAL_OUTLINE, FULLY_DESCRIBED) with explicit prerequisites at each level transition
- Breadth-first authoring (PAT-001): Steps 1-4 for all use cases before depth elaboration of any single use case, preventing missed actors and incorrect goal levels
- Cockburn goal-level classification: SUMMARY (+), USER_GOAL (!), SUBFUNCTION (-) using the sea-metaphor (Cloud/Kite/Sea Level/Fish/Clam)
- Schema-validated output: all artifacts validate against `docs/schemas/use-case-realization-v1.schema.json`
- Five-state slice lifecycle: SCOPED > PREPARED > ANALYZED > IMPLEMENTED > VERIFIED with worktracker Story entity integration
- INVEST criteria verification on every slice before state advancement
- Realization interaction sequences (`$.interactions[]`) that feed directly into `/contract-design` cd-generator and `/test-spec` tspec-generator

---

## When to Use

**Activate this skill when:**

- Writing a new use case from a stakeholder description or actor goal
- Elaborating an existing use case artifact to a higher detail level (e.g., BULLETED_OUTLINE to ESSENTIAL_OUTLINE)
- Decomposing a use case into implementation-ready slices (Jacobson UC 2.0 Activity 2)
- Preparing slices with test cases and enhanced narrative (Activity 4)
- Analyzing slices to produce realization interaction sequences (Activity 5)
- Identifying actors, goals, and system scope for a new system or feature

**NEVER invoke this skill when:**

- Task is generating BDD test specifications from use case artifacts -- Consequence: `/use-case` creates use case artifacts; `/test-spec` consumes them to produce Gherkin Feature files. Using `/use-case` for test generation produces use case artifacts, not test specifications.
- Task is generating API contracts from use case artifacts -- Consequence: `/use-case` produces structured use case artifacts with interaction sequences; `/contract-design` transforms those interactions into OpenAPI specifications.
- Task is adversarial quality review of deliverables -- Consequence: use `/adversary` for quality scoring and adversarial critique.
- Task is requirements engineering with NASA NPR 7123.1D compliance -- Consequence: `/use-case` implements Cockburn/Jacobson methodology, not NPR requirements processes; use `/nasa-se` instead.
- Task is researching or analyzing a problem -- Consequence: `/use-case` is an authoring tool, not a research or analysis methodology; use `/problem-solving` instead.

---

## Available Agents

| Agent | Role | Model | Cognitive Mode | Tool Tier | Output Location | Decision Signal |
|-------|------|-------|----------------|-----------|-----------------|-----------------|
| `uc-author` | Creates and elaborates use case artifacts using Cockburn's 12-step writing process and Jacobson UC 2.0 progressive narrative levels | sonnet | integrative | T2 | `projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md` | "write", "create", "author", "elaborate", "expand", "describe", "draft", "refine", "use case" |
| `uc-slicer` | Decomposes use cases into implementation-ready slices following Jacobson UC 2.0 Activities 2, 4, and 5 | sonnet | systematic | T2 | Same artifact as input (in-place update adding `$.slices[]`, `$.interactions[]`) | "slice", "decompose", "break down", "prepare", "analyze", "realize", "INVEST", "interaction sequence" |

**Default routing:** When intent is ambiguous between authoring and slicing, route to `uc-author` first. Authoring must precede slicing -- `uc-slicer` requires `detail_level >= ESSENTIAL_OUTLINE` which is produced by `uc-author`. When the user says "create a use case and slice it," invoke `uc-author` first, then `uc-slicer` on the output.

---

## P-003 Agent Topology

Both `uc-author` and `uc-slicer` are T2 worker agents. They are invoked independently from MAIN CONTEXT. They do NOT invoke each other. The output of `uc-author` (use case artifact on disk) is consumed by `uc-slicer` via the filesystem -- not via direct agent-to-agent communication.

```
MAIN CONTEXT (orchestrator)
    |
    +-- uc-author (T2 worker) -- via Task tool
    |   Reads: Project context, existing UC artifacts
    |          docs/schemas/use-case-realization-v1.schema.json
    |          skills/use-case/rules/use-case-writing-rules.md
    |          skills/use-case/templates/*.template.md
    |   Writes: UC artifact (.md with YAML frontmatter)
    |
    +-- uc-slicer (T2 worker) -- via Task tool
        Reads: UC artifact (.md) -- produced by uc-author
               docs/schemas/use-case-realization-v1.schema.json
               skills/use-case/rules/use-case-writing-rules.md
        Writes: Updated UC artifact (adds $.slices[], $.interactions[])
                Optional: separate slice documents

Workers do NOT invoke each other.
uc-author output (UC artifact) is consumed by uc-slicer via filesystem.
Cross-agent data flow is mediated by shared artifact files on disk (P-003 compliant).
```

---

## Invoking an Agent

### Natural Language Invocation

```
Write a use case for user authentication in the AUTH domain.
```

```
Elaborate UC-AUTH-001 to Essential Outline level.
```

```
Slice UC-AUTH-001 into implementation-ready increments.
```

### Explicit Agent Invocation

```
Use uc-author to create a use case for user credential validation
at USER_GOAL level in the AUTH domain.
```

```
Use uc-slicer to decompose UC-AUTH-001 from
projects/PROJ-021/use-cases/UC-AUTH-001-validate-credentials.md
into slices with INVEST verification.
```

### Task Tool Invocation (composition file)

```yaml
# Invoke uc-author via Task tool
task:
  agent: skills/use-case/composition/uc-author.agent.yaml
  prompt: |
    Create a use case for user credential validation in the AUTH domain.
    Goal level: USER_GOAL. Target detail level: ESSENTIAL_OUTLINE.
    Output path: projects/PROJ-021/use-cases/UC-AUTH-001-validate-credentials.md
```

```yaml
# Invoke uc-slicer via Task tool
task:
  agent: skills/use-case/composition/uc-slicer.agent.yaml
  prompt: |
    Slice the use case at:
    projects/PROJ-021/use-cases/UC-AUTH-001-validate-credentials.md
    Perform Activities 2, 4, and 5. Create worktracker Story entities.
```

---

## Methodology Reference

### Cockburn 12-Step Writing Process (uc-author)

Full rules are in `skills/use-case/rules/use-case-writing-rules.md`. Steps are loaded progressively per target detail level.

| Step | Action | Output Added | Detail Level Gate |
|------|--------|-------------|-------------------|
| 1 | Identify goal level (SUMMARY/USER_GOAL/SUBFUNCTION) | `goal_level`, `goal_symbol` | BRIEFLY_DESCRIBED |
| 2 | Identify scope and domain | `scope`, `domain`, `id` | BRIEFLY_DESCRIBED |
| 3 | Identify primary actor and supporting actors | `primary_actor`, `supporting_actors[]`, `stakeholders[]` | BRIEFLY_DESCRIBED |
| 4 | Write the brief (title + 3-step basic_flow minimum) | `title`, `basic_flow` (3 steps) | BRIEFLY_DESCRIBED |
| 5 | Write the full basic flow (3-9 steps, typed) | `basic_flow` (3-9 steps, all with `type` field) | BULLETED_OUTLINE |
| 6 | Write preconditions, postconditions, trigger | `preconditions[]`, `postconditions`, `trigger` | BULLETED_OUTLINE |
| 7 | Write extensions (exception handling flows) | `extensions[]` | ESSENTIAL_OUTLINE |
| 8 | Write alternative flows | `alternative_flows[]` | ESSENTIAL_OUTLINE |
| 9 | Verify Cockburn's six quality indicators | Pass all 6 | ESSENTIAL_OUTLINE |
| 10 | Advance to ESSENTIAL_OUTLINE | `detail_level: ESSENTIAL_OUTLINE` | ESSENTIAL_OUTLINE |
| 11 | Extract sub-use cases | `related_use_cases[]` | FULLY_DESCRIBED |
| 12 | Advance to FULLY_DESCRIBED | `detail_level: FULLY_DESCRIBED` | FULLY_DESCRIBED |

### Jacobson UC 2.0 Slice Lifecycle (uc-slicer)

| Activity | Steps | Output |
|---------|-------|--------|
| Activity 2: Slice the Use Cases | Identify slice candidates, apply INVEST, create slice definitions | `$.slices[]` with `slice_state: SCOPED` |
| Activity 4: Prepare a Slice | Define test cases, enhance narrative, create worktracker Story | `slice_state: PREPARED` |
| Activity 5: Analyze a Slice | Identify system elements, allocate responsibilities, produce interactions | `$.interactions[]`, `realization_level: INTERACTION_DEFINED`, `slice_state: ANALYZED` |

### Goal Level Classification (Cockburn Sea Metaphor)

| Level | Symbol | Description | Example |
|-------|--------|-------------|---------|
| SUMMARY | (+) | Cloud/Kite -- high-level business goals | "Manage inventory" |
| USER_GOAL | (!) | Sea Level -- what an actor wants to achieve in one sitting | "Check out a book" |
| SUBFUNCTION | (-) | Fish/Clam -- substeps within a user goal | "Validate credentials" |

---

## Input Requirements

### uc-author Input

| Requirement | Constraint |
|-------------|-----------|
| User request describes a system capability or actor goal | Free text; agent applies H-31 if ambiguous |
| OR: existing use case artifact path for elaboration | File must exist, `$.work_type = USE_CASE` |

### uc-slicer Input

| Requirement | Constraint | Consequence of Violation |
|-------------|-----------|--------------------------|
| Artifact exists at specified path | File must be readable | REJECT with path error |
| `$.work_type = USE_CASE` | Discriminator field | REJECT |
| `$.detail_level >= ESSENTIAL_OUTLINE` | Must not be BRIEFLY_DESCRIBED or BULLETED_OUTLINE | REJECT with actionable message: "Use uc-author to elaborate first" |
| `$.basic_flow` has 3-9 steps | basic_flow array | REJECT |
| `$.extensions` non-empty | At least 1 extension | REJECT |

---

## Output Artifacts

### uc-author: Use Case Artifact

**Path:** `projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md`
**Format:** YAML frontmatter + Markdown narrative body
**Schema:** `docs/schemas/use-case-realization-v1.schema.json`
**Templates:** `skills/use-case/templates/use-case-{brief|casual|realization}.template.md`

### uc-slicer: Updated Use Case Artifact (in-place)

**Path:** Same as input artifact (in-place update)
**Added fields:** `$.slices[]`, `$.interactions[]`, `$.slice_ids[]`, `$.slice_state`, `$.realization_level`
**Optional:** Separate slice documents at `projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}/slices/`

### Downstream Consumption Readiness

| Consumer Skill | Minimum Input Level | Key Field Required |
|---------------|--------------------|--------------------|
| `/test-spec` (tspec-generator) | `detail_level >= ESSENTIAL_OUTLINE` | `$.basic_flow[*].type`, `$.extensions[]` |
| `/contract-design` (cd-generator) | `realization_level = INTERACTION_DEFINED` | `$.interactions[]` |

---

## Integration Points

| Integration | Direction | Mechanism | Pre-Condition |
|-------------|-----------|-----------|---------------|
| `/use-case` to `/test-spec` | tspec-generator reads UC artifact produced by uc-author | Shared artifact file validated against schema | `$.detail_level >= ESSENTIAL_OUTLINE`, `$.extensions` non-empty, `$.basic_flow[*].type` present |
| `/use-case` to `/contract-design` | cd-generator reads UC artifact after uc-slicer Activity 5 | Shared artifact file validated against schema | `$.realization_level = INTERACTION_DEFINED`, `$.interactions` non-empty |
| `/use-case` to `/worktracker` | uc-slicer creates Story entities for PREPARED slices | `uv run jerry items create` via Bash (H-05 compliant; P-003 no Task delegation) | Slices at `slice_state >= PREPARED` |
| All three skills share the same UC artifact | Shared schema: `docs/schemas/use-case-realization-v1.schema.json` | Schema validates input at every consumer boundary | Valid YAML frontmatter with `$.work_type = USE_CASE` |

---

## Routing Entry (Priority 13)

Per `agent-routing-standards.md` enhanced 5-column trigger map format. Priority 13 places `/use-case` above `/test-spec` (14) and `/contract-design` (15), reflecting that use case authoring precedes both test specification and contract generation in the pipeline.

| Detected Keywords | Negative Keywords | Priority | Compound Triggers | Skill |
|---|---|---|---|---|
| use case, use-case, write use case, create use case, author use case, elaborate use case, Cockburn, UC 2.0, Jacobson, actor goal, basic flow, main success scenario, extensions, alternative flow, use case slice, slice use case, INVEST criteria, use case realization, interaction sequence, goal level, primary actor, fully dressed, essential outline | BDD, Gherkin, feature file, test spec, test specification, OpenAPI, API contract, API spec, generate contract, adversarial, tournament, transcript, penetration, exploit, code review, documentation, tutorial, requirements specification, V&V, technical review | 13 | "write use case" OR "create use case" OR "use case" OR "author use case" OR "elaborate use case" OR "slice use case" OR "use case realization" (phrase match) | `/use-case` |

**Disambiguation notes:**
- "use case" routes here. "use case to test" routes to `/test-spec` via that skill's compound triggers.
- "use case to API" routes to `/contract-design` via that skill's compound triggers.
- "actor" alone is excluded (ambiguous with general discussion). "actor goal" or "primary actor" route here.
- "INVEST" alone is excluded (ambiguous with financial context in `/pm-pmm`). "INVEST criteria" routes here via compound trigger proximity.

---

## Constitutional Compliance

| Principle | Agent | Application |
|-----------|-------|-------------|
| P-001 (Truth/Accuracy) | uc-author | Every flow step is grounded in stakeholder input or domain knowledge. No invented actors or goals. |
| P-001 (Truth/Accuracy) | uc-slicer | INVEST assessments report actual criteria pass/fail. Coverage metrics are verifiable. |
| P-002 (File Persistence) | Both | All outputs persisted to files at `projects/${JERRY_PROJECT}/use-cases/`. |
| P-003 (No Recursive Subagents) | Both | Both are T2 worker agents. Neither has Task tool access. Neither invokes the other directly. |
| P-004 (Provenance) | Both | YAML frontmatter carries author, version, created_at, updated_at for full audit trail. |
| P-020 (User Authority) | uc-author | Does not override user decisions about scope, actor list, goal level, or target detail level. |
| P-020 (User Authority) | uc-slicer | Does not override user decisions about slice boundaries, priority ordering, or lifecycle state transitions. |
| P-022 (No Deception) | uc-author | Reports actual detail level achieved; does not claim ESSENTIAL_OUTLINE when extensions are missing. |
| P-022 (No Deception) | uc-slicer | Reports actual INVEST pass/fail per slice; does not advance state when prerequisites are not met. |

---

## Quick Reference

### Common Workflows

| Workflow | Agent Sequence | Typical Duration |
|----------|---------------|-----------------|
| Create brief use case | uc-author (BRIEFLY_DESCRIBED) | 1-2 minutes |
| Create working use case | uc-author (BULLETED_OUTLINE -- default) | 2-3 minutes |
| Create test-ready use case | uc-author (ESSENTIAL_OUTLINE) | 3-5 minutes |
| Elaborate existing UC to higher level | uc-author (reads existing, elaborates) | 2-4 minutes |
| Slice use case into increments | uc-slicer (Activities 2+4) | 2-4 minutes |
| Full realization pipeline | uc-author (ESSENTIAL_OUTLINE) -> uc-slicer (Activities 2+4+5) | 5-10 minutes |
| End-to-end: UC to test specs and contracts | uc-author -> uc-slicer -> tspec-generator + cd-generator | 10-20 minutes |

### Agent Selection Hints

| Signal | Route to |
|--------|----------|
| "Write", "create", "author", "draft", "elaborate", "expand" | uc-author |
| "Slice", "decompose", "break down", "INVEST", "realize" | uc-slicer |
| Ambiguous intent | uc-author first (authoring must precede slicing) |
| "Create and slice" | uc-author, then uc-slicer on output |
| "Generate tests from use case" | Not this skill -- route to `/test-spec` |
| "Generate API contract from use case" | Not this skill -- route to `/contract-design` |

### Detail Level Quick Check

| Level | Minimum Content | Ready For |
|-------|----------------|-----------|
| BRIEFLY_DESCRIBED | Title + 3-step basic flow + goal level | Human review only |
| BULLETED_OUTLINE | Steps 1-6 complete (actors, typed flow, pre/postconditions) | Internal discussion |
| ESSENTIAL_OUTLINE | Steps 1-10 complete (extensions, alternative flows, quality indicators) | `/test-spec`, `/use-case` uc-slicer, and `/contract-design` (after uc-slicer Activity 5 adds interactions) |
| FULLY_DESCRIBED | Steps 1-12 complete (sub-use cases extracted, all exceptions) | All consumers (maximum completeness) |

> **Note:** ESSENTIAL_OUTLINE + uc-slicer Activity 5 (`realization_level = INTERACTION_DEFINED`) is the minimum prerequisite for `/contract-design`. FULLY_DESCRIBED is not required. See Downstream Consumption Readiness table above.

---

### Elaboration State Matrix (detail_level x realization_level)

This 2D matrix shows which `(detail_level, realization_level)` combinations are valid and which transitions produce downstream-consumable artifacts.

| | `OUTLINED` | `STORY_DEFINED` | `INTERACTION_DEFINED` |
|---|---|---|---|
| **BRIEFLY_DESCRIBED** | Valid (initial state) | NOT PERMITTED (schema allOf block) | NOT PERMITTED (schema allOf block) |
| **BULLETED_OUTLINE** | Valid (working spec) | Valid (slices created, no interactions yet) | NOT PERMITTED (schema allOf block) |
| **ESSENTIAL_OUTLINE** | Valid (pre-slice) | Valid (Activities 2+4 complete) | **Ready for /contract-design and /test-spec** |
| **FULLY_DESCRIBED** | Valid (pre-slice) | Valid (Activities 2+4 complete) | **Ready for /contract-design and /test-spec (maximum completeness)** |

**Key rules:**
- `INTERACTION_DEFINED` requires `detail_level >= ESSENTIAL_OUTLINE` -- enforced by the schema's allOf conditional constraint
- `STORY_DEFINED` requires `detail_level >= BULLETED_OUTLINE` (slices need typed flow steps)
- `/contract-design` requires `realization_level = INTERACTION_DEFINED` (independent of detail_level)
- `/test-spec` requires `detail_level >= ESSENTIAL_OUTLINE` (independent of realization_level)
- The most common production target is `(ESSENTIAL_OUTLINE, INTERACTION_DEFINED)`

---

## References

| File | Purpose |
|------|---------|
| `skills/use-case/agents/uc-author.md` | uc-author agent definition |
| `skills/use-case/agents/uc-author.governance.yaml` | uc-author governance metadata |
| `skills/use-case/agents/uc-slicer.md` | uc-slicer agent definition |
| `skills/use-case/agents/uc-slicer.governance.yaml` | uc-slicer governance metadata |
| `skills/use-case/composition/uc-author.agent.yaml` | uc-author canonical agent YAML (Task invocation) |
| `skills/use-case/composition/uc-author.prompt.md` | uc-author system prompt copy |
| `skills/use-case/composition/uc-slicer.agent.yaml` | uc-slicer canonical agent YAML (Task invocation) |
| `skills/use-case/composition/uc-slicer.prompt.md` | uc-slicer system prompt copy |
| `skills/use-case/rules/use-case-writing-rules.md` | Cockburn 12-step + Jacobson UC 2.0 imperative rules |
| `skills/use-case/templates/use-case-brief.template.md` | BRIEFLY_DESCRIBED output template |
| `skills/use-case/templates/use-case-casual.template.md` | BULLETED_OUTLINE output template |
| `skills/use-case/templates/use-case-realization.template.md` | ESSENTIAL_OUTLINE / FULLY_DESCRIBED output template |
| `skills/use-case/templates/use-case-slice.template.md` | Separate slice document template (optional) |
| `skills/use-case/tests/BEHAVIOR_TESTS.md` | BDD behavior test scenarios for the skill |
| `skills/use-case/samples/sample-use-case.md` | Sample use case artifact demonstrating output format |
| `docs/schemas/use-case-realization-v1.schema.json` | JSON Schema for use case artifact YAML frontmatter |
| Cockburn, A. (2001) | *Writing Effective Use Cases*. Addison-Wesley. |
| Jacobson, I. et al. (2011) | *Use-Case 2.0: The Guide to Succeeding with Use Cases*. Ivar Jacobson International. |
| `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/implementation/step-9-use-case-architecture.md` | Architecture SSOT |

---

> *Skill Version: 1.0.0 | Framework: Jerry Framework | Constitutional compliance: P-003, P-020, P-022*
> *Author: eng-backend | Date: 2026-03-09 | Status: ACTIVE*
> *SSOT: `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/implementation/step-9-use-case-architecture.md`*
