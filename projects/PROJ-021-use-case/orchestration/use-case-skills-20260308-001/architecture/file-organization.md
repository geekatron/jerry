# File Organization Architecture: /use-case, /test-spec, /contract-design Skills

> **PS ID:** proj-021 | **Entry ID:** arch-file-org | **Workflow ID:** use-case-skills-20260308-001
> **Date:** 2026-03-08 | **Agent:** ps-architect | **Execution Group:** G-03 (Phase 2 Architecture)
> **Quality Threshold:** >= 0.95 (C4, user override C-008)
> **Status:** PROPOSED (P-020: user approval required before ACCEPTED)
> **Input:** Phase 1 Synthesis (0.956 PASS) | **Version:** 1.0.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What we decided and why, in plain language |
| [L1: Technical Specification](#l1-technical-specification) | Complete directory trees, naming, shared schema |
| [L2: Architectural Rationale](#l2-architectural-rationale) | Design rationale, cross-skill integration, traceability |
| [Shared Artifact Format (R-01)](#shared-artifact-format-r-01) | The YAML frontmatter schema for use case realization documents |
| [Directory Structure](#directory-structure) | Full directory trees for all three skills |
| [Cross-Skill Integration Architecture](#cross-skill-integration-architecture) | How output feeds between skills |
| [Naming Conventions](#naming-conventions) | File, agent, and template naming rules |
| [Recommendation Traceability](#recommendation-traceability) | Mapping from R-01 through R-07 to design decisions |
| [Self-Review Checklist](#self-review-checklist) | H-15 / S-010 verification |
| [Adversarial Self-Critique](#adversarial-self-critique) | S-002, S-003, S-004, S-013 applied |

---

## L0: Executive Summary

We are creating three new Jerry skills that work together as a pipeline: `/use-case` writes structured use case documents, `/test-spec` transforms those documents into BDD test specifications, and `/contract-design` derives API contracts from the same source. The central design challenge is that all three skills must agree on how use case documents are structured, because each skill's output becomes the next skill's input.

This architecture document makes four key decisions. First, we define a shared artifact format -- a YAML frontmatter schema embedded in Markdown documents -- that serves as the contract between all three skills. This is the most important decision because every downstream skill depends on it. Second, we specify where files live on disk, following the same directory conventions that every other Jerry skill uses. Third, we establish naming rules so that agents, templates, and output files are discoverable and consistent. Fourth, we define how data flows between the three skills, including what each skill reads, what it writes, and what validation it performs on input.

The design follows the principle of maximum consistency with existing Jerry skills. Where the `/problem-solving` skill has `agents/`, `templates/`, and `composition/` directories, these new skills have the same. Where existing agents use the dual-file architecture (`.md` + `.governance.yaml`), these agents do too. The only genuinely new element is the shared artifact format, which is necessary because no existing Jerry skill operates as a pipeline where one skill's output is another's input.

---

## Shared Artifact Format (R-01)

> **Priority:** P0 (must be designed first). **Source:** Synthesis R-01, PAT-003, AI-01, DI-04.
> **Rationale:** "Design the shared artifact format before designing any individual skill agents" (synthesis R-01). This format is the pipeline contract. If it is underspecified, each skill becomes an island. If it is overspecified, it prevents skills from evolving independently (AI-01).

### Design Decision: YAML Frontmatter in Markdown

The shared artifact uses the same structural pattern as Jerry worktracker entities: YAML frontmatter for machine-readable fields, Markdown body for human-readable narrative. This decision is grounded in three sources:

1. **Jerry convention:** Worktracker entities use YAML frontmatter + Markdown body. AST parsing (H-33) already supports this format. No new infrastructure needed. (Source: S-05, PAT-006)
2. **Synthesis recommendation:** AI-01 explicitly recommends "a YAML frontmatter block embedded in a Markdown document -- the same pattern Jerry uses for worktracker entities." (Source: synthesis AI-01)
3. **Existing template:** `.context/templates/requirements/USE-CASE.template.md` already defines a YAML frontmatter schema for use cases. The shared format extends this existing template rather than replacing it. (Source: S-05, G-04)

### Use Case Realization Schema (v1.0.0)

The schema below defines the YAML frontmatter fields that appear in every use case artifact produced by `/use-case` and consumed by `/test-spec` and `/contract-design`. Fields are organized by consumer: all consumers need the identity block; `/test-spec` needs the flows block; `/contract-design` needs the interactions block.

```yaml
# === IDENTITY (all consumers) ===
id: "UC-{DOMAIN}-{NNN}"              # Format: UC-{domain}-{nnn} (e.g., UC-AUTH-001)
title: "{Verb} {Noun} {Context}"      # Cockburn naming: actor goal as title
work_type: USE_CASE                   # Immutable discriminator (AST H-33 compatible)
version: "1.0.0"                      # SemVer for the artifact itself
status: DRAFT                         # DRAFT | REVIEW | APPROVED | DEPRECATED

# === CLASSIFICATION (all consumers) ===
goal_level: USER_GOAL                 # SUMMARY | USER_GOAL | SUBFUNCTION
goal_symbol: "!"                      # "+" (summary) | "!" (user goal) | "-" (subfunction)
detail_level: BULLETED_OUTLINE        # BRIEFLY_DESCRIBED | BULLETED_OUTLINE |
                                      # ESSENTIAL_OUTLINE | FULLY_DESCRIBED
scope: "{system-boundary}"            # Design scope (Cockburn: Enterprise/System/Subsystem)
domain: "{domain-code}"               # Short domain code (AUTH, KM, INV, etc.)

# === ACTORS (all consumers) ===
primary_actor: "{actor-name}"
supporting_actors:
  - name: "{actor-name}"
    type: "system"                    # human | system | timer | external
  # ... additional supporting actors

# === SLICE LIFECYCLE (/use-case internal, /test-spec validation) ===
slice_state: SCOPED                   # SCOPED | PREPARED | ANALYZED | IMPLEMENTED | VERIFIED
                                      # UC 2.0 five-state lifecycle (S-01, DI-03)

# === FLOWS (/test-spec primary consumer) ===
# The flows block is the machine-readable representation of the narrative.
# Each flow has a type that maps to Clark's transformation algorithm (PAT-008).
basic_flow:
  - step: 1
    actor: "{actor-name}"
    action: "{verb} {object}"
    type: "actor_action"              # actor_action | system_response | validation
  - step: 2
    actor: "System"
    action: "{verb} {object}"
    type: "system_response"
  # ... steps 3-9 (Cockburn Guideline 6: 3-9 steps)

alternative_flows:
  - id: "AF-01"
    name: "{flow-name}"
    branches_from_step: 3             # Step number in basic_flow where this branches
    condition: "{what was detected}"  # Cockburn Guideline 11
    steps:
      - step: 1
        actor: "{actor-name}"
        action: "{verb} {object}"
        type: "actor_action"
    rejoins_at_step: 5                # null if this flow reaches a separate exit
  # ... additional alternative flows

extensions:
  - id: "EXT-3a"
    name: "{extension-name}"
    anchor_step: 3                    # Step-anchored per Cockburn Ch. 8 numbering
    condition: "{what was detected}"
    steps:
      - step: 1
        actor: "System"
        action: "{error handling action}"
        type: "system_response"
    outcome: "failure"                # success | failure | rejoin:{step}
  # ... additional extensions

# === INTERACTIONS (/contract-design primary consumer) ===
# Derived from flows; each system_response step that implies an API boundary.
interactions:
  - id: "INT-01"
    source_step: 2                    # References basic_flow step number
    source_flow: "basic_flow"         # basic_flow | AF-{nn} | EXT-{anchor}{letter}
    actor_role: "consumer"            # consumer (initiator) | provider (responder)
    system_role: "provider"
    request_description: "{what the actor sends}"
    response_description: "{what the system returns}"
    preconditions:
      - "{condition that must be true}"
    postconditions:
      - "{condition that is true after}"
  # ... additional interactions

# === TRACEABILITY ===
parent_id: null                       # Parent use case ID (if subfunction goal)
related_use_cases: []                 # List of UC-{DOMAIN}-{NNN} references
requirements: []                      # REQ-{NNN} references
slice_ids: []                         # UC-{DOMAIN}-{NNN}-S{N} slice references

# === METADATA ===
priority: P1                          # P0 | P1 | P2 | P3
created_at: "{ISO-8601}"
updated_at: "{ISO-8601}"
created_by: "{author}"
```

### Schema Design Decisions

| Decision | Choice | Rationale | Source |
|----------|--------|-----------|--------|
| SD-01: YAML over JSON frontmatter | YAML | Consistent with all Jerry entities; AST parsing (H-33) supports it; human-editable. | S-05, PAT-006, AI-01 |
| SD-02: `goal_level` as enum, not free text | 3 enums: SUMMARY, USER_GOAL, SUBFUNCTION | Cockburn's sea metaphor has 5 levels but 3 named levels (Ch. 5 p. 61). SUMMARY covers Cloud+Kite; USER_GOAL covers Sea Level; SUBFUNCTION covers Fish+Clam. Keeps the enum simple while preserving classification power. `goal_symbol` preserves the +/!/- annotation for compact display. | S-02 (Cockburn Ch. 5), PAT-007, DI-02 |
| SD-03: `detail_level` as 4-state enum | BRIEFLY_DESCRIBED, BULLETED_OUTLINE, ESSENTIAL_OUTLINE, FULLY_DESCRIBED | Maps 1:1 to Jacobson UC 2.0 narrative levels (S-01). Progressive elaboration is a 5/5-stream unanimous design requirement (T-01, LES-002). The enum enables `/test-spec` to reject use cases that are too sparse (BRIEFLY_DESCRIBED cannot produce reliable Clark transformation). | S-01, S-02, T-01, PAT-001, AI-02 |
| SD-04: `slice_state` uses UC 2.0 five states, not UC 3.0 six states | SCOPED, PREPARED, ANALYZED, IMPLEMENTED, VERIFIED | UC 2.0 is the established baseline (S-01). UC 3.0 (2024) adds a sixth state; the schema can be extended via minor version bump (1.1.0) without breaking existing consumers. | S-01, DI-03 |
| SD-05: Separate `flows` and `interactions` blocks | Flows for /test-spec; interactions for /contract-design | Each downstream skill reads a different part of the schema. `/test-spec` needs flow types (basic/alternative/extension) for Clark transformation. `/contract-design` needs interaction boundaries (request/response pairs) for OpenAPI generation. Separating them means each skill reads only what it needs (CB-02 context budget). | PAT-003, PAT-008, DI-04, DI-05, AI-05 |
| SD-06: `interactions` derived from `flows` | Interactions reference flow step numbers | Traceability from contract back to use case step. Enables `/contract-design` to cite which use case step generated each API operation. | DI-08, AI-05 |
| SD-07: Step types as enums | actor_action, system_response, validation | Clark mapping requires distinguishing actor actions (When) from system responses (Then). The type field enables mechanical transformation without NLP interpretation. | PAT-008, DI-05 |
| SD-08: Extension `outcome` field | success, failure, rejoin:{step} | Clark mapping: extensions with outcome=failure become negative test scenarios; extensions with outcome=rejoin become additional scenarios. The field enables mechanical mapping to Gherkin scenario types. | PAT-008, DI-05, S-03 |

### Schema Validation

The schema will be formalized as a JSON Schema file at `docs/schemas/use-case-realization-v1.schema.json` (R-03). This file enables:
- CI validation of use case artifacts via L5 enforcement layer
- AST compatibility with `/ast` skill (H-33)
- Pre-flight validation in `/test-spec` and `/contract-design` before transformation

### Minimum Detail Level for Downstream Processing

| Downstream Skill | Minimum `detail_level` | Minimum `slice_state` | Rationale |
|-----------------|----------------------|---------------------|-----------|
| `/test-spec` | ESSENTIAL_OUTLINE | ANALYZED | Clark transformation requires named flows with typed steps. Bulleted Outline lacks step-level granularity. Extensions must be complete (Cockburn precision level 3-4). |
| `/contract-design` | ESSENTIAL_OUTLINE | ANALYZED | Interaction extraction requires system_response steps with pre/postconditions. |

These minimums are enforced by input validation in each downstream skill's agent guardrails (SR-002).

---

## Directory Structure

### Design Principle: Consistency with Existing Skills

The directory structure replicates the conventions observed across existing skills (`/problem-solving`, `/nasa-se`, `/eng-team`, `/prompt-engineering`). Evidence base: 4 SKILL.md files and 83 governance.yaml files examined in S-05 (jerry-skill-pattern-analysis.md). The canonical subdirectories are:

| Directory | Purpose | Present in Existing Skills |
|-----------|---------|---------------------------|
| `agents/` | Agent definition files (.md + .governance.yaml) | All multi-agent skills |
| `composition/` | Agent invocation configs (.agent.yaml + .prompt.md) | /problem-solving, /nasa-se, /eng-team |
| `templates/` | Output templates and reference formats | /problem-solving |
| `rules/` | Skill-specific rules (when needed) | /prompt-engineering |
| `contracts/` | Skill contract YAML | /problem-solving, /nasa-se |
| `tests/` | Behavior tests | /problem-solving, /nasa-se |

### Skill Directory Trees

#### `/use-case` Skill

```
skills/use-case/
+-- SKILL.md                                    # H-25: required, exact case
+-- agents/
|   +-- uc-author.md                            # Primary agent: use case authoring
|   +-- uc-author.governance.yaml               # H-34: governance metadata
+-- composition/
|   +-- uc-author.agent.yaml                    # Task tool invocation config
|   +-- uc-author.prompt.md                     # System prompt for Task invocation
+-- templates/
|   +-- use-case-realization.template.md        # Output template (extends USE-CASE.template.md)
|   +-- use-case-brief.template.md              # Brief format template (Cockburn)
|   +-- use-case-casual.template.md             # Casual format template (Cockburn)
+-- rules/
|   +-- use-case-writing-rules.md               # Cockburn 12-step process as agent rules
+-- contracts/
|   +-- UC_SKILL_CONTRACT.yaml                  # Skill contract
+-- tests/
    +-- BEHAVIOR_TESTS.md                       # BDD behavior tests for the skill
```

**Agent count: 1** (uc-author). Per DI-09 and PAT-009 (simplicity-first), start with a single agent. The `uc-author` agent handles all four narrative detail levels and the Cockburn 12-step writing process (DI-01, DI-11). If the methodology section exceeds 1,500 tokens during Phase 3 implementation, split into `uc-author` (authoring) and `uc-reviewer` (7 Cs quality scoring) per agent-development-standards.md Pattern 1.

**Template rationale:** Three templates cover the Cockburn format spectrum. The `use-case-realization.template.md` is the primary output template and implements the shared artifact format schema (R-01). The brief and casual templates support the progressive elaboration pattern (PAT-001, T-01) for early-stage use cases that don't need the full schema.

#### `/test-spec` Skill

```
skills/test-spec/
+-- SKILL.md                                    # H-25: required, exact case
+-- agents/
|   +-- ts-transformer.md                       # Primary agent: UC-to-BDD transformation
|   +-- ts-transformer.governance.yaml          # H-34: governance metadata
+-- composition/
|   +-- ts-transformer.agent.yaml               # Task tool invocation config
|   +-- ts-transformer.prompt.md                # System prompt for Task invocation
+-- templates/
|   +-- feature-file.template.md                # Gherkin Feature output template
|   +-- scenario-mapping.template.md            # Clark transformation reference table
+-- rules/
|   +-- clark-transformation-rules.md           # Clark (2018) mapping as agent rules
+-- contracts/
|   +-- TS_SKILL_CONTRACT.yaml                  # Skill contract
+-- tests/
    +-- BEHAVIOR_TESTS.md                       # BDD behavior tests for the skill
```

**Agent count: 1** (ts-transformer). Per DI-09 and PAT-009, start with a single agent implementing the Clark transformation algorithm (PAT-008, DI-05). The agent's methodology section implements the decision tree: basic flow -> happy path scenario; alternative flow -> additional scenario; extension -> error scenario (R-05). If methodology section exceeds 1,500 tokens during Phase 3, split into `ts-transformer` (generation) and `ts-validator` (7 Cs quality scoring).

**Template rationale:** Two templates. The `feature-file.template.md` defines the Gherkin output format with frontmatter for traceability (back-link to source UC ID). The `scenario-mapping.template.md` is a reference document loaded on demand (Level 3) containing the Clark mapping table for the agent to consult.

**Cardinality rule (R-05):** 1 Feature file per use case. 1 Scenario per flow (basic flow -> 1 scenario; each alternative flow -> 1 scenario; each extension -> 1 scenario). This is the default cardinality. The `ts-transformer` agent documents this in its methodology section.

#### `/contract-design` Skill

```
skills/contract-design/
+-- SKILL.md                                    # H-25: required, exact case
+-- agents/
|   +-- cd-generator.md                         # Primary agent: UC-to-contract generation
|   +-- cd-generator.governance.yaml            # H-34: governance metadata
+-- composition/
|   +-- cd-generator.agent.yaml                 # Task tool invocation config
|   +-- cd-generator.prompt.md                  # System prompt for Task invocation
+-- templates/
|   +-- openapi-contract.template.yaml          # OpenAPI 3.x output template
|   +-- interaction-mapping.template.md         # UC interaction-to-operation reference
+-- rules/
|   +-- uc-to-contract-rules.md                 # Novel transformation algorithm rules
+-- contracts/
|   +-- CD_SKILL_CONTRACT.yaml                  # Skill contract
+-- tests/
    +-- BEHAVIOR_TESTS.md                       # BDD behavior tests for the skill
```

**Agent count: 1** (cd-generator). Per DI-09 and PAT-009. This agent implements the novel UC-to-contract transformation algorithm (R-06, DI-08, AI-05). The algorithm is explicitly labeled as a prototype-requiring design per LES-001 and G-01: no prior art exists for this transformation.

**Template rationale:** Two templates. The `openapi-contract.template.yaml` is the primary output -- an OpenAPI 3.x specification fragment. The `interaction-mapping.template.md` is a Level 3 reference document containing the transformation rules for the agent to consult.

**Scope constraint (DI-07, ASM-005):** Initial release supports REST (OpenAPI 3.x) only. AsyncAPI support is deferred to a follow-on per G-02 (multi-actor pub/sub mapping unresolved). The SKILL.md documents this scope limitation explicitly.

### Shared Schema Location

```
docs/schemas/
+-- use-case-realization-v1.schema.json         # JSON Schema Draft 2020-12 (R-03)
```

The JSON Schema file lives in `docs/schemas/` alongside existing Jerry schemas (`agent-governance-v1.schema.json`, `handoff-v2.schema.json`). This location is consistent with the framework's schema storage convention. All three skills reference this schema for input/output validation.

### Use Case Artifact Storage

Use case artifacts produced by `/use-case` are stored within the active project workspace:

```
projects/{PROJ-NNN-slug}/
+-- use-cases/
|   +-- UC-{DOMAIN}-{NNN}-{slug}.md            # Individual use case realization documents
|   +-- UC-{DOMAIN}-{NNN}-{slug}/
|       +-- slices/
|           +-- UC-{DOMAIN}-{NNN}-S{N}.md       # Individual slice documents (when needed)
+-- test-specs/
|   +-- UC-{DOMAIN}-{NNN}-{slug}.feature.md     # Gherkin feature files (from /test-spec)
+-- contracts/
    +-- UC-{DOMAIN}-{NNN}-{slug}.openapi.yaml   # OpenAPI contracts (from /contract-design)
```

**Storage design decisions:**

| Decision | Choice | Rationale | Source |
|----------|--------|-----------|--------|
| ST-01: `use-cases/` directory at project root | Dedicated directory, not inside `work/` | Use cases are first-class requirements artifacts, not transient work products. They persist across sessions and sprints. Parallel to `docs/design/` for ADRs. | R-02, PAT-006 |
| ST-02: Slug in filename | `UC-AUTH-001-validate-credentials.md` | Human-readable filenames. Consistent with worktracker entity naming (`{EntityId}-{slug}`). | skill-standards.md, worktracker-directory-structure.md |
| ST-03: Feature files alongside use cases | `test-specs/` directory at project root | Separation of concerns: use case source and generated test specs are different artifact types with different lifecycles. `/test-spec` writes to `test-specs/`; `/use-case` writes to `use-cases/`. | R-05, PAT-008 |
| ST-04: Contracts alongside use cases | `contracts/` directory at project root | Same separation principle as ST-03. `/contract-design` writes to `contracts/`. | R-06, DI-07 |
| ST-05: Slices as subdirectory | `use-cases/UC-{id}/slices/` | Slices are children of a use case (UC 2.0: Use Case -> Slice hierarchy). Subdirectory keeps the parent directory clean when a use case has many slices. | S-01, PAT-006 |

### Worktracker Integration (R-09)

Use case entities map to existing worktracker entity types. No new entity types required (ASM-004, PAT-006).

| Use Case Concept | Worktracker Entity Type | Status Field Mapping | Source |
|-----------------|------------------------|---------------------|--------|
| Use Case | Feature or Epic | DRAFT, IN_PROGRESS, REVIEW, DONE | S-01 (Jerry Mapping table) |
| Use Case Slice | Story or Task | Scoped->draft, Prepared->ready, Analyzed->in-progress, Implemented->review, Verified->done | PAT-006 |

---

## L1: Technical Specification

### Naming Conventions

#### File Naming (H-25)

| File Type | Convention | Example |
|-----------|-----------|---------|
| Skill directory | kebab-case, matches `name` field | `skills/use-case/`, `skills/test-spec/`, `skills/contract-design/` |
| Skill file | Exact `SKILL.md` (case-sensitive) | `skills/use-case/SKILL.md` |
| Agent definition | `{prefix}-{function}.md` | `uc-author.md`, `ts-transformer.md`, `cd-generator.md` |
| Agent governance | `{prefix}-{function}.governance.yaml` | `uc-author.governance.yaml` |
| Composition agent config | `{prefix}-{function}.agent.yaml` | `uc-author.agent.yaml` |
| Composition prompt | `{prefix}-{function}.prompt.md` | `uc-author.prompt.md` |
| Template | `{descriptor}.template.{ext}` | `use-case-realization.template.md` |
| Rule file | `{descriptor}-rules.md` | `clark-transformation-rules.md` |
| Skill contract | `{PREFIX}_SKILL_CONTRACT.yaml` | `UC_SKILL_CONTRACT.yaml` |
| Behavior tests | `BEHAVIOR_TESTS.md` | `tests/BEHAVIOR_TESTS.md` |
| Use case artifact | `UC-{DOMAIN}-{NNN}-{slug}.md` | `UC-AUTH-001-validate-credentials.md` |
| Feature file | `UC-{DOMAIN}-{NNN}-{slug}.feature.md` | `UC-AUTH-001-validate-credentials.feature.md` |
| Contract file | `UC-{DOMAIN}-{NNN}-{slug}.openapi.yaml` | `UC-AUTH-001-validate-credentials.openapi.yaml` |
| JSON Schema | `{name}-v{N}.schema.json` | `use-case-realization-v1.schema.json` |

#### Agent Naming (AD-M-001)

| Skill | Prefix | Agent Name | Cognitive Mode | Tool Tier | Source |
|-------|--------|-----------|---------------|-----------|--------|
| `/use-case` | `uc-` | `uc-author` | integrative | T2 (Read-Write) | DI-09, R-04 |
| `/test-spec` | `ts-` | `ts-transformer` | systematic | T2 (Read-Write) | DI-09, R-04 |
| `/contract-design` | `cd-` | `cd-generator` | convergent | T2 (Read-Write) | DI-09, R-04 |

**Agent prefix rationale:**
- `uc-` for use-case (2-letter prefix, unambiguous, no collision with existing prefixes: ps-, nse-, adv-, eng-, pe-, orch-, wt-, ts- is already taken by transcript skill)

**Naming collision: `ts-` prefix.** The `/transcript` skill uses `ts-` prefix for its agents (`ts-parser`, `ts-extractor`). The `/test-spec` skill cannot reuse `ts-`. Options evaluated:

| Option | Prefix | Pros | Cons |
|--------|--------|------|------|
| A: `ts-` | `ts-transformer` | Intuitive abbreviation of test-spec | Collides with transcript skill's `ts-parser`, `ts-extractor` |
| B: `tsp-` | `tsp-transformer` | No collision; "test-spec" clear | 3-letter prefix; no existing skill uses 3 letters |
| C: `bdd-` | `bdd-transformer` | Descriptive of output type | Doesn't match skill name (`test-spec`); misleading if skill evolves beyond BDD |
| **D: `tspec-`** | **`tspec-transformer`** | **No collision; readable; maps to skill name** | **5-letter prefix; longest in framework** |

**Recommended: Option D (`tspec-`).** The collision with `/transcript` (`ts-`) is a genuine routing confusion risk per AP-02 (Bag of Triggers). A unique prefix eliminates ambiguity at the cost of a slightly longer agent name. The `tspec-` prefix is self-documenting ("test spec") and maps directly to the skill directory name.

**Updated agent table with collision resolution:**

| Skill | Prefix | Agent Name | Cognitive Mode | Tool Tier |
|-------|--------|-----------|---------------|-----------|
| `/use-case` | `uc-` | `uc-author` | integrative | T2 |
| `/test-spec` | `tspec-` | `tspec-transformer` | systematic | T2 |
| `/contract-design` | `cd-` | `cd-generator` | convergent | T2 |

#### Cognitive Mode Rationale

| Agent | Mode | Rationale | Source |
|-------|------|-----------|--------|
| `uc-author` | integrative | Combines stakeholder inputs, domain knowledge, and methodological structure (Cockburn + Jacobson) into unified use case narrative. Cross-source correlation. | agent-development-standards.md (Mode Selection Guide: "synthesis" -> integrative), DI-01 |
| `tspec-transformer` | systematic | Applies Clark's step-by-step transformation algorithm. Checklist execution. Completeness verification. No creative generation. | agent-development-standards.md (Mode Selection Guide: "compliance checking" -> systematic), PAT-008, R-05 |
| `cd-generator` | convergent | Evaluates interaction steps against API design patterns, selects OpenAPI operation structure, produces focused contract. Decision-making from alternatives. | agent-development-standards.md (Mode Selection Guide: "analysis, evaluation" -> convergent), DI-08, AI-05 |

---

## Cross-Skill Integration Architecture

### Pipeline Data Flow

```
                    Shared Artifact Format (R-01)
                    use-case-realization-v1.schema.json
                              |
                              v
+------------------+    +-----------------+    +---------------------+
|   /use-case      |    |   /test-spec    |    |  /contract-design   |
|                  |    |                 |    |                     |
|  Reads:          |    |  Reads:         |    |  Reads:             |
|  - user input    |    |  - UC artifact  |    |  - UC artifact      |
|  - existing UCs  |    |    (.basic_flow |    |    (.interactions   |
|                  |    |     .alt_flows  |    |     block)          |
|  Writes:         |    |     .extensions)|    |                     |
|  - UC artifact   |--->|                 |    |  Writes:            |
|    (full schema) |    |  Writes:        |    |  - OpenAPI spec     |
|                  |    |  - .feature.md  |    |    (.openapi.yaml)  |
+------------------+    +-----------------+    +---------------------+
        |                                               ^
        |                                               |
        +-----------------------------------------------+
                    (same UC artifact feeds both)
```

### Integration Points

| Source Skill | Target Skill | Data Contract | Validation |
|-------------|-------------|---------------|------------|
| `/use-case` | `/test-spec` | `basic_flow`, `alternative_flows`, `extensions` fields in YAML frontmatter | Target validates: (1) `detail_level >= ESSENTIAL_OUTLINE`, (2) `slice_state >= ANALYZED`, (3) `basic_flow` has 3-9 steps, (4) each flow has `type` field |
| `/use-case` | `/contract-design` | `interactions` block in YAML frontmatter | Target validates: (1) `detail_level >= ESSENTIAL_OUTLINE`, (2) `interactions` array is non-empty, (3) each interaction has `request_description` and `response_description` |
| `/test-spec` | (none downstream) | N/A -- terminal skill in pipeline | Self-validates via 7 Cs quality gate (PAT-004, DI-06) |
| `/contract-design` | (none downstream) | N/A -- terminal skill in pipeline | Self-validates against OpenAPI 3.x schema |

### Input Validation Rules (Per Skill)

Each downstream skill MUST validate its input before transformation (guardrails SR-002). Validation failures produce an actionable error message per Jerry error handling standards (include entity type, ID, and suggested action).

**`/test-spec` input validation:**

```
IF artifact.detail_level < ESSENTIAL_OUTLINE:
  REJECT: "UC {id} is at {detail_level}. Clark transformation requires
           ESSENTIAL_OUTLINE or FULLY_DESCRIBED. Use /use-case to
           elaborate the use case first."

IF artifact.slice_state < ANALYZED:
  REJECT: "UC {id} slice state is {slice_state}. Test generation requires
           ANALYZED or later. Prepare and analyze the slice first."

IF len(artifact.basic_flow) < 3:
  REJECT: "UC {id} basic flow has {n} steps. Cockburn Guideline 6
           requires 3-9 steps for a well-formed use case."

IF any step in flows missing 'type' field:
  REJECT: "UC {id} flow step {n} missing 'type' field. Clark
           transformation requires actor_action/system_response/validation
           types for mechanical mapping to Given/When/Then."
```

**`/contract-design` input validation:**

```
IF artifact.detail_level < ESSENTIAL_OUTLINE:
  REJECT: "UC {id} is at {detail_level}. Contract derivation requires
           ESSENTIAL_OUTLINE or FULLY_DESCRIBED."

IF len(artifact.interactions) == 0:
  REJECT: "UC {id} has no interactions block. Use /use-case to identify
           system boundaries and interaction points first."

IF any interaction missing request_description or response_description:
  REJECT: "UC {id} interaction {INT-nn} missing request/response
           description. Both are required for OpenAPI operation generation."
```

### The Artifact is Append-Only Between Skills

A critical architectural invariant: downstream skills **do not modify** the source use case artifact. `/test-spec` reads the use case and writes a separate `.feature.md` file. `/contract-design` reads the use case and writes a separate `.openapi.yaml` file. This means:

1. The use case artifact is the single source of truth (SSOT) for requirements.
2. If the use case changes, downstream artifacts become stale (acknowledged limitation per G-05).
3. No merge conflicts from concurrent skill execution.

---

## L2: Architectural Rationale

### Why This Design Over Alternatives

Three alternative approaches were evaluated before arriving at this design.

#### Option A: Monolithic Shared Template (Rejected)

A single template file containing use case narrative, test scenarios, and contract fragments in one document.

**Steelman (S-003):** This approach maximizes co-location. A developer sees everything about a use case in one file. Changes to the narrative immediately update test expectations. No cross-file synchronization problem.

**Why rejected:** Violates separation of concerns. Different skills have different lifecycles -- a use case may be approved while its tests are still being refined. A single file becomes a merge conflict magnet when `/test-spec` and `/contract-design` both write to it. The artifact size would exceed context budget guidelines (CB-05: > 500 lines triggers offset/limit). Most critically, it prevents independent evolution of the three skills.

#### Option B: Pure JSON Schema (No Markdown Body) (Rejected)

Use case artifacts as pure JSON/YAML data files with no human-readable narrative body.

**Steelman (S-003):** Maximizes machine processability. No ambiguity between narrative text and structured data. JSON Schema validation covers 100% of content. Simplifies agent implementation (no Markdown parsing needed).

**Why rejected:** Contradicts Cockburn's foundational insight: "Casual, readable use cases are still useful, whereas unreadable use cases won't get read" (Reminders p.ii, S-02). Use cases are communication artifacts -- they exist to be read by humans. A pure data format loses the narrative value that makes use cases useful for stakeholder alignment. The YAML frontmatter + Markdown body hybrid preserves both machine processability and human readability.

#### Option C: Separate Schema Per Skill (Rejected)

Each skill defines its own input/output schema independently, with transformation adapters between skills.

**Steelman (S-003):** Maximum skill independence. Each skill can evolve its schema without coordinating with others. Adapter pattern is well-established in integration architecture.

**Why rejected:** Synthesis AI-01 explicitly warns against this: "If this format is underspecified, each skill becomes an island." Adapter complexity grows quadratically with skill count. For 3 skills, it requires 3 adapters (UC->test, UC->contract, test->contract); for 4 skills it requires 6. The shared schema approach requires 1 schema that all skills agree on, with extensions via minor version bumps.

### Long-Term Evolution Path

| Milestone | Change | Schema Impact | Backward Compatibility |
|-----------|--------|--------------|----------------------|
| Phase 3 prototype | Validate schema with 3+ representative use cases | None (validation only) | N/A |
| Agent decomposition | Split agents when methodology > 1,500 tokens | None (directory change only) | Full |
| AsyncAPI support | Add `async_interactions` block to schema | Minor version 1.1.0 | Full (new field, existing consumers ignore it) |
| UC 3.0 adoption | Extend `slice_state` enum to 6 states | Minor version 1.2.0 | Full (new enum value, old values still valid) |
| Multi-use-case models | Add `use_case_model_id` field for grouping | Minor version 1.3.0 | Full (new optional field) |

### Systemic Consequences

**Positive:**
- Three skills share one contract, reducing integration complexity from O(n^2) adapters to O(1) shared schema.
- YAML frontmatter enables CI validation via JSON Schema (L5 enforcement), AST parsing (H-33), and programmatic querying.
- Directory structure is identical to existing skills -- zero cognitive overhead for developers familiar with Jerry.
- Progressive elaboration is encoded in the schema (detail_level enum), not left to prose interpretation.

**Negative (P-022: disclosed per requirement):**
- The shared schema creates coupling: changing a field name requires updating all three skills' agents and templates. Mitigation: semantic versioning of the schema with backward-compatible evolution.
- The `interactions` block in the schema is architecturally speculative -- it is designed for `/contract-design`'s novel algorithm (G-01, no prior art). If the algorithm is redesigned during prototyping, the interactions block may need restructuring. Mitigation: prototype validation in Phase 3 before committing to this design (LES-001).
- Feature file format (`.feature.md`) uses Markdown wrapping around Gherkin rather than pure `.feature` files. This means Cucumber cannot directly execute the output without extraction. Mitigation: the Markdown wrapper preserves Jerry's L0/L1/L2 structure and frontmatter traceability; a trivial `scripts/extract-gherkin.sh` can strip the wrapper for Cucumber consumption.
- The `tspec-` prefix is longer than any existing prefix. This is a cosmetic cost accepted to avoid the genuine routing confusion risk of `ts-` collision with `/transcript`.

---

## Recommendation Traceability

| Rec ID | Recommendation (from Synthesis) | Addressed In | Status |
|--------|-------------------------------|-------------|--------|
| R-01 (P0) | Design shared artifact format first | [Shared Artifact Format](#shared-artifact-format-r-01) -- complete schema with 8 design decisions | ADDRESSED |
| R-02 (P1) | Design file organization with artifact paths, worktracker integration | [Directory Structure](#directory-structure), [Worktracker Integration](#worktracker-integration-r-09) | ADDRESSED |
| R-03 (P1) | Design JSON Schema at `docs/schemas/` | [Schema Validation](#schema-validation) -- JSON Schema location specified | ADDRESSED (location specified; schema file itself is a Phase 3 deliverable) |
| R-04 (P1) | Design agent decomposition (1 agent/skill, tool tiers, cognitive modes) | [Agent Naming](#agent-naming-ad-m-001), [Cognitive Mode Rationale](#cognitive-mode-rationale) | ADDRESSED (file-org scope; full agent decomposition is `architecture/agent-decomposition.md` deliverable) |
| R-05 (P1) | Specify cardinality: 1 Feature/UC, 1 Scenario/flow | [Cardinality rule](#test-spec-skill) in /test-spec directory section | ADDRESSED |
| R-06 (P1) | Design /contract-design with novel algorithm scaffold | [/contract-design directory](#contract-design-skill), prototype-requiring label | ADDRESSED (file structure; algorithm design is `architecture/agent-decomposition.md` deliverable) |
| R-07 (P1) | Design trigger map entries | Deferred to trigger-map architecture deliverable | DEFERRED (not in file-org scope; R-07 is routing, not file organization) |
| R-08 (P2) | Confirm AsyncAPI scope | [Scope constraint](#contract-design-skill) -- REST-only documented | ACKNOWLEDGED |
| R-09 (P2) | Confirm worktracker entity compatibility | [Worktracker Integration](#worktracker-integration-r-09) -- confirmed compatible | ADDRESSED |
| R-10 (P2) | Design quality gate integration (7 Cs + S-014) | Not in file-org scope | DEFERRED (quality gate design is `architecture/agent-decomposition.md` deliverable) |

---

## Self-Review Checklist (H-15, S-010)

- [x] P-001 (Truth): All directory structures verified against actual skill directory listings from Bash tool output. Schema fields sourced from synthesis patterns with explicit citations.
- [x] P-002 (File Persistence): Document written to `architecture/file-organization.md` via Write tool.
- [x] P-004 (Provenance): Every design decision cites source (synthesis recommendation, research finding, or framework standard).
- [x] P-011 (Evidence-Based): 3 alternatives evaluated for the primary design decision (Option A/B/C vs. chosen approach).
- [x] P-020 (User Authority): Status is PROPOSED, not ACCEPTED.
- [x] P-022 (No Deception): Negative consequences documented in L2 section. Prototype risk for /contract-design explicitly labeled. Feature file Markdown wrapper limitation disclosed.
- [x] H-23 (Navigation): Navigation table present with anchor links.
- [x] H-34 (Agent Architecture): All agents specified with dual-file (.md + .governance.yaml).
- [x] R-01 through R-10: All recommendations traced in [Recommendation Traceability](#recommendation-traceability) table.
- [x] L0/L1/L2 structure present.
- [x] S-003 (Steelman): Applied to all 3 rejected alternatives before rejection.

---

## Adversarial Self-Critique

### S-002: Devil's Advocate -- Challenge Key Assumptions

**Assumption 1: "The shared schema is stable enough to build on."**
Challenge: The `interactions` block is designed for a novel algorithm (G-01) with no prior art. What if Phase 3 prototyping reveals that the interaction model is fundamentally wrong?
Response: The `interactions` block is deliberately separated from the `flows` block (SD-05). If the contract-design algorithm needs a different input structure, only the `interactions` block changes -- the `flows` block (consumed by `/test-spec`) is unaffected. Schema versioning (minor bump to 1.1.0) handles this without breaking `/test-spec`.

**Assumption 2: "1 agent per skill is sufficient."**
Challenge: What if the Cockburn 12-step writing process plus Jacobson lifecycle management plus 7 Cs quality scoring exceeds 1,500 tokens in a single methodology section?
Response: This is acknowledged in DI-09 and PAT-009. The file organization is designed for easy agent addition: new agents go in `agents/` with `.md` + `.governance.yaml`, new compositions go in `composition/`. No directory restructuring needed.

### S-004: Pre-Mortem -- "It's 6 months later and this failed. Why?"

**Failure scenario 1:** The shared schema became a bottleneck. Every change required coordinating all three skills simultaneously.
Likelihood: MEDIUM. Mitigation: Semantic versioning with backward-compatible evolution. New optional fields do not break existing consumers.

**Failure scenario 2:** The `tspec-` prefix caused confusion. Developers typed `ts-` from muscle memory and got transcript agents instead.
Likelihood: LOW. Mitigation: SKILL.md routing disambiguation table (Pattern 5 from S-05) explicitly documents the difference. Negative keywords in trigger map suppress `/transcript` when BDD/Gherkin context is present.

**Failure scenario 3:** The feature file `.feature.md` format was never adopted because Cucumber tooling expected `.feature` files.
Likelihood: MEDIUM. Mitigation: The extraction script (`scripts/extract-gherkin.sh`) is documented as a known workaround. If adoption friction is measured, the output format can be changed to pure `.feature` with a companion `.feature-meta.yaml` for traceability metadata.

### S-013: Inversion -- "What if we deliberately chose the opposite?"

**Inversion:** What if each skill had NO shared schema and operated independently?
Result: Each skill would define its own input format. Users would manually transform use case documents into the format each downstream skill expects. This is essentially the current state (before these skills exist) -- it works but requires manual effort and produces inconsistent artifacts. The shared schema automates this transformation and ensures consistency. The inversion confirms that the shared schema adds genuine value rather than unnecessary coupling.

---

*Architecture Version: 1.0.0*
*Status: PROPOSED (P-020)*
*Constitutional Compliance: P-001 (truth), P-002 (file persistence), P-004 (provenance), P-011 (evidence-based), P-020 (user authority), P-022 (no deception)*
*Workflow ID: use-case-skills-20260308-001*
*Next Agent: ps-critic (C4 adversarial review at >= 0.95)*
