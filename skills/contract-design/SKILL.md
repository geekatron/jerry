---
name: contract-design
description: API contract generation from use case realization artifacts using a novel UC-to-contract transformation algorithm. Transforms use case interaction sequences (produced by /use-case uc-slicer Activity 5) into OpenAPI 3.1 specifications with full traceability from API operations to source interaction steps. Validates generated contracts against OpenAPI schema standards. Requires use case artifacts at realization_level = INTERACTION_DEFINED with populated interactions block. Invoke when generating API contracts, OpenAPI specs, endpoint designs, request/response schemas, or operation mappings from use case artifacts.
version: "1.0.0"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
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

> **Version:** 1.0.0 | **Framework:** Jerry Framework | **Constitutional compliance:** P-003 (no recursive subagents), P-020 (user authority), P-022 (no deception)
> **Status:** ACTIVE | **Author:** eng-backend | **Date:** 2026-03-09

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
| [UC-to-Contract Algorithm Reference](#uc-to-contract-algorithm-reference) | Domain methodology summary |
| [Input Requirements](#input-requirements) | Use case artifact prerequisites |
| [Output Artifacts](#output-artifacts) | OpenAPI contract, mapping document, validation report, PROTOTYPE review checklist |
| [Integration Points](#integration-points) | Cross-skill connections |
| [Routing Entry (Priority 15)](#routing-entry-priority-15) | Trigger map entry for mandatory-skill-usage.md |
| [Constitutional Compliance](#constitutional-compliance) | Principle-to-agent mapping |
| [Quick Reference](#quick-reference) | Common workflows and agent selection |
| [References](#references) | File paths and external citations |

---

## Document Audience

| Level | Audience | Sections |
|-------|----------|---------|
| L0 | Stakeholders, product managers | [Purpose](#purpose), [When to Use](#when-to-use), [Quick Reference](#quick-reference) |
| L1 | Developers, API designers using the skill | [Available Agents](#available-agents), [Invoking an Agent](#invoking-an-agent), [UC-to-Contract Algorithm Reference](#uc-to-contract-algorithm-reference), [Input Requirements](#input-requirements), [Output Artifacts](#output-artifacts) |
| L2 | Framework maintainers, reviewers | [P-003 Agent Topology](#p-003-agent-topology), [Integration Points](#integration-points), [Constitutional Compliance](#constitutional-compliance), [References](#references) |

---

## Purpose

The `/contract-design` skill transforms structured use case realization artifacts produced by `/use-case` into OpenAPI 3.1 API contract specifications using a novel UC-to-contract transformation algorithm. It closes the gap between behavioral use case specifications and machine-readable API contracts that downstream code generators and implementers can consume.

**Key Capabilities:**

- Novel UC-to-contract transformation: every interaction step in the `$.interactions` block maps to exactly one API operation or internal operation documentation entry (no invented operations)
- HTTP method inference: derives GET/POST/PUT/PATCH/DELETE from the semantic content of `request_description` fields, grounded in RFC 9110 (HTTP Semantics, Section 9), with High/Medium/Low confidence annotations
- Request/response schema derivation: extracts schema properties directly from `preconditions` (request body) and `postconditions` (response body) of each interaction
- Error response mapping: maps use case extension conditions with `outcome = failure` to 4xx/5xx HTTP status codes using semantic pattern analysis
- Actor role mapping: maps primary actor to API consumer role, provider interactions to internal operations documentation, and supporting actors to `components/schemas` descriptions per IC-05
- Full traceability: every operation carries `x-source-interaction`, `x-source-step`, `x-source-flow` annotations; the separate mapping document provides the complete traceability chain from OpenAPI operation back to use case step
- PROTOTYPE labeling: all generated contracts carry `x-prototype: true` in the `info` section until human review validates semantic correctness (non-negotiable safety gate per RULE-TR-02)
- Contract validation: 9-step protocol verifying structural compliance, traceability completeness (100% of consumer interactions mapped), and PROTOTYPE label presence

---

## When to Use

**Activate this skill when:**

- Generating OpenAPI 3.1 specifications from use case realization artifacts at `realization_level = INTERACTION_DEFINED`
- Transforming use case interaction sequences into API operations, paths, and schemas
- Creating request/response schemas from interaction preconditions and postconditions
- Mapping use case actors to API consumer/provider roles
- Deriving error responses from use case extension conditions
- Validating that a generated contract traces to all source interaction steps
- Checking whether a generated OpenAPI contract meets structural compliance and traceability standards

**NEVER invoke this skill when:**

- Task is writing or editing use case artifacts -- Consequence: `/contract-design` agents do not implement Cockburn's writing methodology; they consume use case output, not produce it; use `/use-case` instead.
- Task is generating BDD test specifications from use case artifacts -- Consequence: `/contract-design` produces OpenAPI contracts, not Gherkin Feature files; use `/test-spec` instead.
- Task is writing OpenAPI specifications from scratch (not from use case artifacts) -- Consequence: `/contract-design` requires the structured `interactions` block as input; writing OpenAPI from free-form requirements is a manual authoring task, not a transformation.
- Task is adversarial quality review of deliverables -- Consequence: use `/adversary` for quality scoring and adversarial critique.
- Use case artifact does not have an `interactions` block -- Consequence: the UC-to-contract transformation requires `$.interactions[*]` produced by `uc-slicer` Activity 5; use `/use-case` to realize the use case first.
- Task is generating AsyncAPI or CloudEvents specifications -- Consequence: these contract types are deferred (DI-07, ASM-005, G-02); templates exist as scaffolding but agent generation logic is not implemented in v1.0.0.

---

## Available Agents

| Agent | Role | Model | Cognitive Mode | Tool Tier | Output Location | Decision Signal |
|-------|------|-------|----------------|-----------|-----------------|-----------------|
| `cd-generator` | Transforms UC interaction sequences into OpenAPI 3.1 contract specifications using the UC-to-contract transformation algorithm | opus | convergent | T2 | `projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}.openapi.yaml` | "generate", "create contract", "OpenAPI from use case", "map interactions to operations", "derive API" |
| `cd-validator` | Validates generated contracts against OpenAPI 3.1 structural standards and verifies traceability from every operation to source interaction | sonnet | systematic | T2 | `projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}-validation.md` | "validate contract", "check OpenAPI", "verify traceability", "contract compliance", "schema validation" |

**Default routing:** When intent is ambiguous between generation and validation, route to `cd-generator` first. Generation must precede validation. When the user says "generate and validate the contract," invoke `cd-generator` first, then `cd-validator` on the output.

---

## P-003 Agent Topology

Both `cd-generator` and `cd-validator` are T2 worker agents. They are invoked independently from MAIN CONTEXT. They do NOT invoke each other. The output of `cd-generator` (OpenAPI YAML and mapping document on disk) is consumed by `cd-validator` via the filesystem -- not via direct agent-to-agent communication.

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

---

## Invoking an Agent

### Natural Language Invocation

```
Generate an OpenAPI contract from the use case at
projects/PROJ-021/use-cases/UC-AUTH-001-validate-credentials.md
```

```
Validate the OpenAPI contract at
projects/PROJ-021/contracts/UC-AUTH-001-validate-credentials.openapi.yaml
against the source use case.
```

### Explicit Agent Invocation

```
Use cd-generator to transform UC-AUTH-001 from
projects/PROJ-021/use-cases/UC-AUTH-001-validate-credentials.md
into an OpenAPI 3.1 contract at
projects/PROJ-021/contracts/UC-AUTH-001-validate-credentials.openapi.yaml
```

```
Use cd-validator to validate
projects/PROJ-021/contracts/UC-AUTH-001-validate-credentials.openapi.yaml
against projects/PROJ-021/use-cases/UC-AUTH-001-validate-credentials.md
```

### Task Tool Invocation (composition file)

```yaml
# cd-generator invocation via composition file
from: skills/contract-design/composition/cd-generator.agent.yaml
session_context:
  artifact_path: "projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md"
  output_path: "projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}.openapi.yaml"
  success_criteria:
    - "At least 1 operation per consumer interaction"
    - "x-prototype: true in info section"
    - "Mapping document with full traceability annotations"
```

---

## UC-to-Contract Algorithm Reference

The UC-to-contract transformation algorithm encodes a novel 9-step mapping procedure. The full algorithm is defined in `skills/contract-design/rules/uc-to-contract-rules.md`. Key mappings summarized here for reference:

### Interaction-to-Operation Mapping

| UC Artifact Field | OpenAPI Element | Rule |
|------------------|-----------------|------|
| `$.title` | `info.title` | RULE-RI-01 |
| `$.primary_actor` | `info.x-primary-actor` (API consumer role) | RULE-AR-01 |
| Interaction where `actor_role = consumer` | External path + operation | RULE-OM-01 |
| Interaction where `actor_role = provider` | `x-internal-operations` entry | RULE-OM-02 |
| `request_description` | Operation `summary` + HTTP method inference | RULE-HM-01 through RULE-HM-05 |
| `preconditions` | Request body schema properties | RULE-SD-01 |
| `postconditions` | Response body schema properties | RULE-SD-02 |
| Extension with `outcome = failure` | 4xx/5xx error response | RULE-ER-01 |
| `supporting_actors` | `components/schemas` descriptions (IC-05) | RULE-AR-03 |
| `source_step` + `source_flow` | `x-source-interaction`, `x-source-step`, `x-source-flow` | RULE-TR-01 |
| (always) | `info.x-prototype: true` | RULE-TR-02 |

### HTTP Method Inference (RULE-HM series)

| Request Description Pattern | Inferred Method | Confidence |
|---------------------------|-----------------|------------|
| read, query, get, fetch, retrieve, look up, search, list, find | GET | High |
| create, add, submit, register, initiate, start, send, post | POST | High |
| update, modify, change, edit, set, replace | PUT or PATCH | Medium |
| delete, remove, cancel, revoke, deactivate, terminate | DELETE | High |
| Ambiguous (no pattern match) | POST (default) + WARN | Low |

Low and Medium confidence operations carry `x-method-inference: {confidence}` annotation and are flagged by `cd-validator` for human review.

### PROTOTYPE Labeling (Non-Negotiable)

All generated contracts carry `x-prototype: true` in the `info` section. This label is mandatory because the UC-to-contract transformation algorithm is novel (no prior art -- G-01) and all generated contracts require human review before production use. `cd-validator` Step 7 treats absence of this label as a mandatory FAIL with no override permitted.

---

## Input Requirements

### cd-generator Input

| Requirement | Constraint | Consequence of Violation |
|------------|-----------|--------------------------|
| Artifact exists at specified path | File must be readable | REJECT with path error |
| `$.work_type = USE_CASE` | Discriminator field must match | REJECT |
| `$.realization_level = INTERACTION_DEFINED` | Must not be OUTLINED or STORY_DEFINED | REJECT with actionable message directing to `/use-case` |
| `$.interactions` non-empty array | At least 1 entry required | REJECT with message: "Use /use-case (uc-slicer Activity 5) to identify system boundaries first" |
| Each interaction has all 7 required fields | `id`, `source_step`, `source_flow`, `actor_role`, `system_role`, `request_description`, `response_description` | REJECT for missing field |
| `source_step` resolves to a flow step | Cross-reference validation | REJECT for broken reference |
| `$.supporting_actors` readable | Needed for IC-05 | WARN (proceed without IC-05 cross-referencing) |

### cd-validator Input

| Requirement | Constraint | Consequence of Violation |
|------------|-----------|--------------------------|
| Contract file exists at specified path | File must be readable | REJECT |
| Contract is valid YAML | Must parse without errors | REJECT |
| `openapi` field is "3.1.x" | Must be OpenAPI 3.1 | Step 1 FAIL |
| Source UC artifact exists | Required for traceability | REJECT |
| `$.interactions` in UC artifact | Required for traceability check | REJECT |

---

## Output Artifacts

### cd-generator Outputs

**Primary output -- OpenAPI contract (`.openapi.yaml`):**

```
Location: projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}.openapi.yaml
Contents: OpenAPI 3.1 YAML with paths, operations, schemas, error responses,
          traceability annotations, x-internal-operations, and x-prototype: true
```

**Secondary output -- Mapping document (`-mapping.md`):**

```
Location: projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}-mapping.md
Contents: Traceability table mapping each OpenAPI operation to its source
          interaction ID, step number, flow name, and HTTP method confidence.
          Includes PROTOTYPE status notice.
```

### cd-validator Output

**Validation report (`-validation.md`):**

```
Location: projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}-validation.md
Contents: 9-step per-check PASS/FAIL verdicts, traceability coverage as N/M = P%,
          traceability matrix, and list of gaps with recommended remediation.
```

### Output Quality Gate

The PROTOTYPE label (`x-prototype: true`) remains on all contracts until:
1. `cd-validator` produces a PASS verdict on all 9 checks
2. A human reviewer confirms semantic correctness of the contract
3. The reviewer explicitly removes the `x-prototype: true` label

Neither cd-generator nor cd-validator removes the PROTOTYPE label. That action is a human decision (P-020 user authority).

### PROTOTYPE Review Checklist

When `cd-validator` produces a PASS verdict, a human reviewer MUST complete this checklist before removing the `x-prototype: true` label. This checklist constitutes the formal sign-off ceremony. Record completion in the validation report alongside the cd-validator PASS verdict.

**Reviewer checklist (all items required for label removal):**

| # | Check | Reviewer Action |
|---|-------|----------------|
| 1 | cd-validator PASS confirmed | Verify `-validation.md` shows overall PASS with all 9 steps individually PASS |
| 2 | HTTP method semantics correct | For every operation: manually verify the inferred HTTP method matches the use case intent -- especially any operations with `x-method-inference: medium` or `x-method-inference: low` |
| 3 | Resource naming is correct | Path names (`/resources/{id}`) match the domain entities and naming conventions of the target system |
| 4 | Request/response schemas are complete | Required fields are present; field names match the implementation's data model; no spurious required fields |
| 5 | Error responses are correct | Each 4xx/5xx response maps to an actual failure condition; status codes follow RFC 9110 semantics for the operation |
| 6 | No invented operations | Every operation traces to a specific `$.interactions` entry in the source UC artifact via `x-source-interaction` annotation |
| 7 | Supporting actors are correctly referenced | `components/schemas` descriptions and `x-internal-operations` entries accurately represent external system dependencies |
| 8 | Contract is suitable for downstream consumption | The contract can serve as a binding specification for implementation; no ambiguous operations remain |

**Sign-off format (append to `-validation.md`):**

```markdown
## PROTOTYPE Review Sign-Off

**Reviewer:** {name}
**Date:** {YYYY-MM-DD}
**Checklist:** All 8 items verified
**Decision:** APPROVED for label removal
**Action taken:** x-prototype: true removed from info section
**Notes:** {any caveats or conditional approvals}
```

**Audit trail:** The sign-off record in `-validation.md` is the audit trail. Do not remove the PROTOTYPE label without appending this section. The sign-off is permanent -- do not delete it after label removal.

---

## Integration Points

| Integration | Direction | Mechanism | Pre-Condition |
|-------------|-----------|-----------|---------------|
| `/use-case` to `/contract-design` | cd-generator reads UC artifact produced by uc-slicer Activity 5 | Shared artifact file validated against `docs/schemas/use-case-realization-v1.schema.json` | `$.realization_level = INTERACTION_DEFINED`, `$.interactions` non-empty |
| `/contract-design` output to implementers | OpenAPI specs serve as API implementation contracts | Human- and machine-readable `.openapi.yaml` files | Contract validated by cd-validator |
| `/contract-design` parallel to `/test-spec` | Both are independent consumers of `/use-case` output | File-mediated -- both read the same UC artifact; neither depends on the other | UC artifact at INTERACTION_DEFINED (for this skill) or ESSENTIAL_OUTLINE+ (for /test-spec) |
| `/contract-design` to code generators | OpenAPI spec feeds OpenAPI Generator or similar tools | Standard OpenAPI 3.1 format | Contract passes cd-validator checks; PROTOTYPE label removed by human reviewer |

---

## Routing Entry (Priority 15)

> For insertion into `mandatory-skill-usage.md` Trigger Map (per agent-routing-standards.md Phase 1 5-column format). Priority 15 places `/contract-design` below `/test-spec` (14) and `/use-case` (13), reflecting the pipeline dependency order.

| Column | Value |
|--------|-------|
| **Detected Keywords** | contract design, contract-design, API contract, OpenAPI, API spec, API specification, generate contract, contract from use case, API schema, endpoint design, operation mapping, request response schema, API generation, REST contract, swagger, use case to API, interaction to contract |
| **Negative Keywords** | requirements specification, V&V, technical review, use case model, actor goal, write use case, BDD, Gherkin, scenario, test spec, feature file, adversarial, tournament, transcript, penetration, exploit, code review, pricing model, cloud pricing, documentation, tutorial |
| **Priority** | 15 |
| **Compound Triggers** | "API contract" OR "contract design" OR "OpenAPI" OR "generate contract" OR "contract from use case" OR "API specification" OR "use case to API" (phrase match) |
| **Skill** | `/contract-design` |

**Disambiguation notes:**
- "API" alone is excluded (ambiguous with `/diataxis` for API docs, `/red-team` for API security testing). Compound triggers require qualification.
- "schema" alone is excluded. "API schema" routes here; "database schema" does not.
- "BDD" and "Gherkin" route to `/test-spec` via negative keyword suppression.

---

## Constitutional Compliance

| Principle | Agent | Application |
|-----------|-------|-------------|
| P-003 (No recursive subagents) | Both agents | Neither cd-generator nor cd-validator has the Task tool. No agent-to-agent invocation. Cross-agent communication via filesystem only. |
| P-020 (User authority) | Both agents | User decides contract scope, operation granularity, resource naming. PROTOTYPE label removal is a user/reviewer decision. Neither agent removes or overrides x-prototype. |
| P-022 (No deception) | cd-generator | G-01 (no prior art) acknowledged. PROTOTYPE label mandatory. Confidence annotations (high/medium/low) on HTTP method inference. REJECT messages are specific and actionable. |
| P-022 (No deception) | cd-validator | FAIL verdicts cite specific evidence. Traceability gaps list specific interaction IDs (not generic descriptions). Coverage expressed as N/M = P%, not just percentage. |
| P-001 (Truth/Accuracy) | Both agents | Every mapping traces to a specific UC schema field or RFC 9110 clause. No invented API operations. |
| P-002 (File Persistence) | Both agents | All outputs persisted to files; no inline-only responses. |

---

## Quick Reference

### Common Workflows

**Generate OpenAPI from use case (single step):**
```
Use cd-generator on the UC artifact at INTERACTION_DEFINED level.
Output: .openapi.yaml + -mapping.md
```

**Generate and validate:**
```
1. Use cd-generator to produce .openapi.yaml and -mapping.md
2. Use cd-validator to produce -validation.md
3. Review validation report; remediate any FAIL verdicts
4. Human review validates semantic correctness; remove x-prototype: true
```

**Check if UC is ready for contract generation:**
```
Verify: $.realization_level = INTERACTION_DEFINED
Verify: $.interactions is non-empty
Verify: Each interaction has id, source_step, source_flow, actor_role,
        system_role, request_description, response_description
If missing interactions: run /use-case uc-slicer Activity 5 first
```

### Agent Selection Guide

| User Intent | Agent | Rationale |
|-------------|-------|-----------|
| "Generate an API contract from my use case" | cd-generator | Transformation from UC to OpenAPI |
| "Create OpenAPI spec from interactions block" | cd-generator | Same transformation task |
| "Validate the contract I generated" | cd-validator | 9-step validation protocol |
| "Check traceability coverage of the contract" | cd-validator | Step 2 path completeness check |
| "Generate and validate in one workflow" | cd-generator then cd-validator | Generation must precede validation |

---

## References

| File | Purpose |
|------|---------|
| `skills/contract-design/agents/cd-generator.md` | cd-generator agent definition (F-02) |
| `skills/contract-design/agents/cd-generator.governance.yaml` | cd-generator governance metadata (F-03) |
| `skills/contract-design/agents/cd-validator.md` | cd-validator agent definition (F-04) |
| `skills/contract-design/agents/cd-validator.governance.yaml` | cd-validator governance metadata (F-05) |
| `skills/contract-design/composition/cd-generator.agent.yaml` | Task tool invocation config for cd-generator (F-06) |
| `skills/contract-design/composition/cd-generator.prompt.md` | System prompt for Task tool invocation (F-07) |
| `skills/contract-design/composition/cd-validator.agent.yaml` | Task tool invocation config for cd-validator (F-08) |
| `skills/contract-design/composition/cd-validator.prompt.md` | System prompt for Task tool invocation (F-09) |
| `skills/contract-design/templates/openapi-template.yaml` | OpenAPI 3.1 output template (F-10) |
| `skills/contract-design/templates/asyncapi-template.yaml` | AsyncAPI 3.0 scaffolding -- deferred (F-11) |
| `skills/contract-design/templates/cloudevents-template.yaml` | CloudEvents 1.0 scaffolding -- deferred (F-12) |
| `skills/contract-design/templates/json-schema-template.json` | JSON Schema Draft 2020-12 template (F-13) |
| `skills/contract-design/rules/uc-to-contract-rules.md` | Novel UC-to-contract transformation algorithm (F-14, 24 rules) |
| `skills/contract-design/contracts/CD_SKILL_CONTRACT.yaml` | Skill interface contract (F-15) |
| `skills/contract-design/tests/BEHAVIOR_TESTS.md` | BDD behavior tests, 10 scenarios (F-16) |
| `skills/contract-design/samples/sample-contract.openapi.yaml` | UC-LIB-001 "Borrow a Book" sample output (F-17) |
| `docs/schemas/use-case-realization-v1.schema.json` | Input validation schema |
| `docs/schemas/agent-governance-v1.schema.json` | H-34 governance YAML validation schema |
| `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/implementation/step-11-contract-design-architecture.md` | Architecture SSOT (v1.1.0, 0.956 PASS) |
| OpenAPI Specification 3.1.0 | https://spec.openapis.org/oas/v3.1.0 |
| RFC 9110 (2022) HTTP Semantics | https://www.rfc-editor.org/rfc/rfc9110#section-9 -- Basis for HTTP method inference |
| Jacobson, I. et al. (2011) | Use-Case 2.0: The Guide to Succeeding with Use Cases |
