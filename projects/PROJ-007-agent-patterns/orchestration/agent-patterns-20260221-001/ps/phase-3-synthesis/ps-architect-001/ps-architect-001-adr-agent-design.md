# ADR-PROJ007-001: Agent Definition Format and Design Patterns

<!-- PS-ID: PROJ-007 | ENTRY: e-004 | AGENT: ps-architect-001 | DATE: 2026-02-21 -->
<!-- CRITICALITY: C4 (new ADR, AE-003 auto-C3+; will be baselined, AE-004 applies on modification) -->

> Architecture Decision Record codifying the canonical agent definition format, structural patterns, and behavioral constraints for Claude Code agents within the Jerry Framework.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language overview for stakeholders |
| [Status](#status) | ADR lifecycle state |
| [Context](#context) | Why this decision is needed |
| [Decision](#decision) | What we decided |
| [1. Canonical Agent Definition Template](#1-canonical-agent-definition-template) | Complete YAML+MD template with all fields |
| [2. JSON Schema for Agent Definition Validation](#2-json-schema-for-agent-definition-validation) | JSON Schema (Draft 2020-12) for YAML frontmatter |
| [3. Hexagonal Architecture Mapping](#3-hexagonal-architecture-mapping) | Agent definitions mapped to hexagonal layers |
| [4. Tool Security Tiers (T1-T5)](#4-tool-security-tiers-t1-t5) | Tiered tool access with selection guidelines |
| [5. Cognitive Mode Taxonomy](#5-cognitive-mode-taxonomy) | Five modes with selection criteria |
| [6. Progressive Disclosure Structure](#6-progressive-disclosure-structure) | Three-tier content organization |
| [7. Guardrails Template](#7-guardrails-template) | Required guardrail sections |
| [Consequences](#consequences) | Positive, negative, and risk outcomes |
| [Migration Path](#migration-path) | Transition plan for 37 existing agents |
| [Evidence Sources](#evidence-sources) | Traced citations with authority tiers |
| [Self-Review (S-010)](#self-review-s-010) | Pre-submission quality verification |

---

## L0: Executive Summary

This ADR establishes the canonical format for defining Claude Code agents within the Jerry Framework. It formalizes the implicit patterns already present in 37 production agents across 8 skills into an explicit, validatable, and enforceable standard.

The decision retains the proven YAML frontmatter + Markdown body format (used across all 37 agents) and adds JSON Schema validation for the YAML frontmatter -- the single highest-value enhancement identified across all Phase 1-2 research (+0.45 trade study delta in TS-2, +0.40 in TS-4, consensus #1 priority across all three NSE Phase 2 agents).

The ADR defines seven interconnected components: a canonical template (consolidating requirements AR-001 through AR-012 and PR-001 through PR-008), a JSON Schema (resolving open item OI-01), a hexagonal architecture mapping, five tool security tiers, a cognitive mode taxonomy, a progressive disclosure structure, and a guardrails template. Together, these components ensure that agent definitions are structurally consistent, machine-validatable, and aligned with the hexagonal dependency rule.

This is a C4-criticality decision because it establishes a baseline standard that will govern all future agent development. Modification after baselining triggers AE-004 (auto-C4).

---

## Status

**Proposed**

---

## Context

### Problem Statement

Jerry currently has 37 agents across 8 skills, all using the YAML frontmatter + Markdown body format. This format is proven at scale and industry-validated. However, agent definitions vary in structure, field coverage, and quality. There is no schema validation to catch structural errors before runtime. This leads to three concrete problems:

1. **Structural inconsistency.** Agent definitions vary in which fields they include, how they name fields, and whether they include guardrails, output specifications, or constitutional compliance. New agent authors have no authoritative template and must reverse-engineer the format from existing examples.

2. **No deterministic validation.** All quality assurance for agent definitions relies on LLM-based review (S-010 self-review, S-014 critic scoring). Structural defects -- missing required fields, invalid enum values, malformed name patterns -- cannot be caught deterministically. Schema validation would catch these at zero LLM cost (architecture Pattern 8, Quality Gate Layer 1).

3. **Implicit patterns are vulnerable to drift.** The patterns that make Jerry's agent architecture successful (specialist decomposition, cognitive mode assignment, progressive disclosure, tool restriction) are embodied in practice but not codified. As the framework grows beyond 37 agents, implicit patterns erode through entropy.

### Driving Evidence

| Finding | Source | Authority Tier |
|---------|--------|---------------|
| Schema validation is the highest-value single enhancement | Cross-agent consensus #1 (all 3 NSE Phase 2 agents) | Consensus (3 independent agents) |
| +0.45 delta for schema-validated YAML+MD (B5 vs B1) | Trade Study TS-2 (nse-explorer-001) | Industry Leader (Anthropic, Google, Microsoft inputs) |
| +0.40 delta for schema pre-check in QA architecture (D6 vs D2) | Trade Study TS-4 (nse-explorer-001) | Industry Leader |
| 52 formal requirements across 6 domains, 8/8 INCOSE quality pass | nse-requirements-001 | NASA SE process (NPR 7123.1D) |
| 10 design patterns validated against 37 production agents | nse-architecture-001 | Industry Leader + Jerry production data |
| 57 patterns cataloged, framework maturity 3.3/5 | ps-analyst-001 | Multi-source synthesis (Anthropic, Google, Microsoft, OpenAI) |
| 3 RED-zone risks: context rot (RPN 392), error amplification (RPN 336), rule proliferation | nse-risk-001, ps-investigator-001 | FMEA methodology |

### Constraints

| Constraint | Source | Impact on Decision |
|------------|--------|-------------------|
| P-003/H-01: Max one level of agent nesting | Constitution | Agent definitions must not enable recursive delegation |
| P-020/H-02: User authority cannot be overridden | Constitution | Agent definitions cannot override user decisions |
| P-022/H-03: No deception about capabilities | Constitution | Agent definitions must accurately represent capabilities |
| H-28: Description must include WHAT + WHEN + triggers | Skill standards | Description field validation requirements |
| H-25 through H-30: Skill and agent file standards | Skill standards | File naming, location, registration requirements |
| 31/35 HARD rule slots consumed (89%) | quality-enforcement.md | Cannot add many new HARD rules; consolidation preferred |
| Backward compatibility with 37 existing agents | Production reality | Schema must validate existing agents, not reject them |

### Open Items Resolved by This Decision

| OI-ID | Item | Resolution |
|-------|------|------------|
| OI-01 | JSON Schema format for agent definition validation | Resolved: JSON Schema Draft 2020-12. See [Section 2](#2-json-schema-for-agent-definition-validation). Rationale: widest tooling support (VS Code, ajv, Python jsonschema), industry-standard, interoperable with CI pipelines. |
| OI-03 | Open Agent Specification adoption | Resolved: Adopt compatible elements (version field, description semantics) but do not adopt the full specification. Jerry's YAML+MD format is richer than the Agent Spec's JSON-only format and includes behavioral sections the Agent Spec does not address. Compatible evolution is preferred over wholesale adoption. |
| OI-04 | Output schema variability across L0/L1/L2 levels | Resolved: Define a base output schema with required `levels` array. Agents producing stakeholder-facing deliverables MUST declare all three levels. The per-level content structure is agent-specific (documented in methodology section). See PR-008 in the template. |

---

## Decision

We adopt the Hybrid Schema-Validated Markdown approach (B5 from TS-2): retain the current YAML frontmatter + Markdown body format and add JSON Schema validation for YAML frontmatter. The decision comprises seven components detailed below.

### 1. Canonical Agent Definition Template

This template consolidates requirements AR-001 through AR-012 (agent structure) and PR-001 through PR-008 (prompt design) into a single authoritative reference. Fields marked REQUIRED correspond to MUST-priority requirements; fields marked RECOMMENDED correspond to SHOULD-priority requirements.

```yaml
---
# ============================================================
# CANONICAL AGENT DEFINITION TEMPLATE
# Version: 1.0.0
# Standard: ADR-PROJ007-001
# ============================================================

# --- IDENTIFICATION (AR-001, AR-007, AR-008, AR-009) ---
name: "{skill-prefix}-{function}"          # REQUIRED. Pattern: ^[a-z]+-[a-z]+(-[a-z]+)*$
                                           # Must match filename (without .md extension).
                                           # Skill prefix must match parent skill directory.
version: "1.0.0"                           # REQUIRED. Semantic versioning: MAJOR.MINOR.PATCH
                                           # Pattern: ^\d+\.\d+\.\d+$
description: >-                            # REQUIRED. WHAT the agent does + WHEN to invoke it
  {One-sentence role description}.         # + at least one trigger example.
  Invoke when {trigger condition}.         # Max 1024 chars. No XML tags. (H-28)
  Triggers: {keyword1}, {keyword2}.
model: opus                                # REQUIRED. Enum: opus | sonnet | haiku
                                           # Selection justification (PR-007):
                                           #   opus = complex reasoning, research, architecture
                                           #   sonnet = balanced analysis, standard production
                                           #   haiku = fast repetitive tasks, formatting, validation

# --- IDENTITY (PR-001, PR-002, PR-003) ---
identity:
  role: "{Singular Role Title}"            # REQUIRED. Clear, singular role. Unique within
                                           # parent skill (no two agents share a role).
  expertise:                               # REQUIRED. Minimum 2 entries.
    - "{Domain competency 1}"              # Specific, not generic. Shapes LLM reasoning
    - "{Domain competency 2}"              # and provides routing signals.
    - "{Domain competency 3}"
  cognitive_mode: "convergent"             # REQUIRED. Enum: divergent | convergent |
                                           # integrative | systematic | forensic
                                           # See Section 5 for selection criteria.

# --- PERSONA (PR-005) ---
persona:                                   # RECOMMENDED. Ensures consistent output voice.
  tone: "professional"                     # Enum: professional | technical | consultative
  communication_style: "consultative"      # Enum: consultative | directive | analytical
  audience_level: "adaptive"              # Enum: adaptive | expert | intermediate | beginner

# --- CAPABILITIES (AR-006, AR-012) ---
capabilities:
  allowed_tools:                           # REQUIRED. Principle of least privilege.
    - Read                                 # Select the lowest security tier that satisfies
    - Write                                # the agent's requirements.
    - Glob                                 # See Section 4 for T1-T5 tier definitions.
    - Grep
  output_formats:                          # RECOMMENDED. Declares supported output types.
    - markdown
  forbidden_actions:                       # REQUIRED. Minimum 3 entries. Must include
    - "Spawn recursive subagents (P-003)"  # constitutional constraints.
    - "Override user decisions (P-020)"
    - "Misrepresent capabilities or confidence (P-022)"

# --- GUARDRAILS (SR-002, SR-003, SR-009) ---
guardrails:
  input_validation:                        # REQUIRED. Format constraints for expected inputs.
    - "{field_name}_format: \"{regex}\""   # At least one validation rule.
  output_filtering:                        # REQUIRED. Minimum 3 entries.
    - no_secrets_in_output                 # Prevents sensitive information leakage.
    - no_executable_code_without_confirmation
    - all_claims_must_have_citations
  fallback_behavior: "warn_and_retry"      # REQUIRED. What happens on unresolvable error.
                                           # Enum: warn_and_retry | escalate_to_user |
                                           # persist_and_halt

# --- OUTPUT (PR-008) ---
output:
  required: true                           # REQUIRED. Whether agent must produce a file.
  location: "projects/${JERRY_PROJECT}/{artifact-type}/{naming-pattern}.md"
                                           # REQUIRED when output.required is true.
                                           # Uses ${JERRY_PROJECT} variable and kebab-case.
  levels:                                  # REQUIRED for stakeholder-facing agents.
    - L0                                   # Executive summary (ELI5)
    - L1                                   # Technical detail (engineer-level)
    - L2                                   # Strategic implications (architect-level)

# --- VALIDATION (post-completion checks) ---
validation:                                # RECOMMENDED. Declarative post-completion checks.
  post_completion_checks:
    - verify_file_created                  # Confirms output artifact exists.
    - verify_l0_l1_l2_present             # Confirms all output levels are present.
    - verify_citations_present             # Confirms factual claims cite sources.
    - verify_navigation_table              # Confirms H-23 compliance.

# --- CONSTITUTIONAL COMPLIANCE (SR-001) ---
constitution:
  reference: "docs/governance/JERRY_CONSTITUTION.md"
  principles_applied:                      # REQUIRED. Minimum: P-003, P-020, P-022.
    - "P-003: No Recursive Subagents (Hard)"
    - "P-020: User Authority (Hard)"
    - "P-022: No Deception (Hard)"

# --- SESSION CONTEXT (Handoff Schema) ---
session_context:                           # RECOMMENDED. Defines handoff data structure.
  schema: "docs/schemas/agent-handoff.json"
  on_receive:                              # Inbound processing steps.
    - "Validate handoff against schema"
    - "Read listed artifacts"
    - "Orient via key_findings"
  on_send:                                 # Outbound processing steps.
    - "Populate artifacts with file paths"
    - "Summarize completed work"
    - "Set confidence score"

# --- ENFORCEMENT (quality gate integration) ---
enforcement:                               # RECOMMENDED. Quality gate configuration.
  tier: "medium"                           # Enforcement tier: hard | medium | soft
  escalation_path: "{escalation description}"
---

# Agent Name: {Title}

<agent>

<identity>
## Identity

You are **{Role Title}**, a {cognitive_mode} specialist in the Jerry Framework.

**Expertise domains:**
- {expertise_1}: {brief elaboration}
- {expertise_2}: {brief elaboration}

**Key distinctions from similar agents:**
- Unlike {similar_agent}, you focus on {differentiation}.

**Cognitive mode: {mode}** -- You {mode_behavior_description}.
</identity>

<purpose>
## Purpose

{Two to three sentences describing what this agent does and why it exists.
Reference the specific problem this agent addresses.}
</purpose>

<input>
## Input

**Session Context Fields:**
| Field | Required | Description |
|-------|----------|-------------|
| `task_id` | Yes | Work item reference |
| `artifacts` | Yes | Prior output file paths |
| `key_findings` | No | Orientation bullets from upstream |

**Expected Input Format:**
{Description of what this agent expects to receive.}
</input>

<capabilities>
## Capabilities

**Tool Usage Patterns:**
| Tool | When to Use | Constraints |
|------|-------------|-------------|
| Read | {usage pattern} | {constraints} |
| Write | {usage pattern} | {constraints} |

**Tools NOT Available:** {List tools the agent cannot use and why.}
</capabilities>

<methodology>
## Methodology

**Process:**
1. {Step 1: description}
2. {Step 2: description}
3. {Step 3: description}
4. Apply self-review (S-010/H-15) before finalizing output.

**Decision Criteria:**
{Criteria the agent uses to make decisions during execution.}

**Quality Standards:**
- {quality_standard_1}
- {quality_standard_2}
</methodology>

<output>
## Output

**Artifact:** `{output.location}` (file path with variables)

**Structure:**
- L0: Executive Summary ({expected length})
- L1: Technical Detail ({expected length})
- L2: Strategic Implications ({expected length})

**Format Requirements:**
- Navigation table (H-23)
- Anchor links (H-24)
- Citations for all factual claims
</output>

<guardrails>
## Guardrails

**Constitutional Compliance:**
- P-003: NEVER spawn recursive subagents.
- P-020: NEVER override user intent. Ask before destructive operations.
- P-022: NEVER misrepresent actions, capabilities, or confidence.

**Input Validation:**
{Specific validation rules for this agent's inputs.}

**Output Filtering:**
- No secrets or credentials in output.
- No executable code without user confirmation.
- All claims must have citations.

**Failure Modes:**
| Failure | Response |
|---------|----------|
| {failure_1} | {response_1} |
| {failure_2} | {response_2} |
</guardrails>

</agent>
```

**Template Field Summary:**

| Category | Field | Requirement Level | Source Requirement |
|----------|-------|-------------------|-------------------|
| Identification | `name` | REQUIRED | AR-001, AR-007 |
| Identification | `version` | REQUIRED | AR-008 |
| Identification | `description` | REQUIRED | AR-009, H-28 |
| Identification | `model` | REQUIRED | PR-007 |
| Identity | `identity.role` | REQUIRED | PR-001 |
| Identity | `identity.expertise` | REQUIRED | PR-003 |
| Identity | `identity.cognitive_mode` | REQUIRED | PR-002 |
| Persona | `persona` | RECOMMENDED | PR-005 |
| Capabilities | `capabilities.allowed_tools` | REQUIRED | AR-006 |
| Capabilities | `capabilities.forbidden_actions` | REQUIRED | AR-012 |
| Guardrails | `guardrails.input_validation` | REQUIRED | SR-002 |
| Guardrails | `guardrails.output_filtering` | REQUIRED | SR-003 |
| Guardrails | `guardrails.fallback_behavior` | REQUIRED | SR-009 |
| Output | `output.required` | REQUIRED | PR-008 |
| Output | `output.location` | REQUIRED (when output.required=true) | AR-010 |
| Output | `output.levels` | REQUIRED (stakeholder-facing) | PR-008 |
| Validation | `validation` | RECOMMENDED | QR-003 |
| Constitution | `constitution.principles_applied` | REQUIRED | SR-001 |
| Session Context | `session_context` | RECOMMENDED | HR-001, HR-002 |
| Enforcement | `enforcement` | RECOMMENDED | QR-001 |
| Structure | Progressive disclosure (Tier 1/2/3 content organization) | REQUIRED | PR-004 [^1] |
| Structure | Instruction hierarchy (`constitution` section + `guardrails` ordering + `forbidden_actions`) | REQUIRED | PR-006 [^2] |

[^1]: PR-004 (Progressive Disclosure) is addressed by the three-tier content structure defined in [Section 6](#6-progressive-disclosure-structure), not by a single YAML field. The YAML frontmatter is Tier 2 content; the SKILL.md description is Tier 1; supplementary materials loaded via Read are Tier 3. The structural organization of the template itself implements PR-004.

[^2]: PR-006 (Instruction Hierarchy) is addressed by the combination of: (a) `constitution.principles_applied` declaring which constitutional principles apply, (b) `guardrails` sections establishing input/output/fallback constraints, and (c) `capabilities.forbidden_actions` specifying behavioral boundaries. Together these create the instruction hierarchy: constitutional principles > guardrails > methodology. No single YAML field captures this; the template's section ordering implements the hierarchy.

---

### 2. JSON Schema for Agent Definition Validation

This JSON Schema (Draft 2020-12) validates the YAML frontmatter of agent definition files. It resolves OI-01 and implements requirements AR-003, QR-003, and Pattern 8 Quality Gate Layer 1.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://jerry-framework.dev/schemas/agent-definition/v1.0.0",
  "title": "Jerry Agent Definition Schema",
  "description": "Validates YAML frontmatter of Jerry Framework agent definition files. ADR-PROJ007-001.",
  "type": "object",
  "required": [
    "name",
    "version",
    "description",
    "model",
    "identity",
    "capabilities",
    "guardrails",
    "output",
    "constitution"
  ],
  "properties": {
    "name": {
      "type": "string",
      "pattern": "^[a-z]+-[a-z]+(-[a-z]+)*$",
      "description": "Agent identifier. Must follow {skill-prefix}-{function} kebab-case pattern. (AR-007)"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Semantic version in MAJOR.MINOR.PATCH format. (AR-008)"
    },
    "description": {
      "type": "string",
      "maxLength": 1024,
      "not": {
        "pattern": "<[^>]+>"
      },
      "description": "WHAT + WHEN + triggers. Max 1024 chars, no XML tags. (AR-009, H-28)"
    },
    "model": {
      "type": "string",
      "enum": ["opus", "sonnet", "haiku"],
      "description": "Model tier selection. opus=complex, sonnet=balanced, haiku=fast. (PR-007)"
    },
    "identity": {
      "type": "object",
      "required": ["role", "expertise", "cognitive_mode"],
      "properties": {
        "role": {
          "type": "string",
          "minLength": 1,
          "description": "Clear, singular role title. Unique within parent skill. (PR-001)"
        },
        "expertise": {
          "type": "array",
          "items": { "type": "string", "minLength": 1 },
          "minItems": 2,
          "description": "Domain competencies. Minimum 2 entries, specific not generic. (PR-003)"
        },
        "cognitive_mode": {
          "type": "string",
          "enum": ["divergent", "convergent", "integrative", "systematic", "forensic"],
          "description": "Reasoning approach. See Section 5 for selection criteria. (PR-002)"
        }
      },
      "additionalProperties": false
    },
    "persona": {
      "type": "object",
      "properties": {
        "tone": {
          "type": "string",
          "enum": ["professional", "technical", "consultative"]
        },
        "communication_style": {
          "type": "string",
          "enum": ["consultative", "directive", "analytical"]
        },
        "audience_level": {
          "type": "string",
          "enum": ["adaptive", "expert", "intermediate", "beginner"]
        }
      },
      "additionalProperties": false,
      "description": "Output voice configuration. (PR-005)"
    },
    "capabilities": {
      "type": "object",
      "required": ["allowed_tools", "forbidden_actions"],
      "properties": {
        "allowed_tools": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": [
              "Read", "Write", "Edit", "Glob", "Grep", "Bash", "Task",
              "WebSearch", "WebFetch", "NotebookEdit",
              "mcp__context7__resolve-library-id",
              "mcp__context7__query-docs",
              "mcp__memory-keeper__context_save",
              "mcp__memory-keeper__context_get",
              "mcp__memory-keeper__context_search",
              "mcp__memory-keeper__context_checkpoint"
            ]
          },
          "description": "Authorized tool list. Principle of least privilege. (AR-006)"
        },
        "output_formats": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["markdown", "yaml", "json", "text"]
          },
          "description": "Supported output format types."
        },
        "forbidden_actions": {
          "type": "array",
          "items": { "type": "string" },
          "minItems": 3,
          "description": "Actions the agent must not perform. Must reference P-003, P-020, P-022. (AR-012)"
        }
      },
      "additionalProperties": false
    },
    "guardrails": {
      "type": "object",
      "required": ["input_validation", "output_filtering", "fallback_behavior"],
      "properties": {
        "input_validation": {
          "type": "array",
          "minItems": 1,
          "description": "Input format validation rules. At least one rule required. (SR-002)"
        },
        "output_filtering": {
          "type": "array",
          "minItems": 3,
          "items": { "type": "string" },
          "description": "Output safety filters. Minimum 3 entries. (SR-003)"
        },
        "fallback_behavior": {
          "type": "string",
          "enum": ["warn_and_retry", "escalate_to_user", "persist_and_halt"],
          "description": "Error recovery strategy. (SR-009)"
        }
      },
      "additionalProperties": false
    },
    "output": {
      "type": "object",
      "required": ["required"],
      "properties": {
        "required": {
          "type": "boolean",
          "description": "Whether the agent must produce an output artifact."
        },
        "location": {
          "type": "string",
          "description": "Artifact file path template with variables. (AR-010)"
        },
        "template": {
          "type": "string",
          "description": "Output template reference."
        },
        "levels": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["L0", "L1", "L2"]
          },
          "description": "Supported output disclosure levels. (PR-008)"
        }
      },
      "if": {
        "properties": { "required": { "const": true } }
      },
      "then": {
        "required": ["location"]
      },
      "additionalProperties": false
    },
    "validation": {
      "type": "object",
      "properties": {
        "file_must_exist": { "type": "boolean" },
        "link_artifact_required": { "type": "boolean" },
        "post_completion_checks": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "additionalProperties": false,
      "description": "Post-completion validation checks. (QR-003)"
    },
    "constitution": {
      "type": "object",
      "required": ["principles_applied"],
      "properties": {
        "reference": {
          "type": "string",
          "description": "Path to constitution document."
        },
        "principles_applied": {
          "type": "array",
          "items": { "type": "string" },
          "minItems": 3,
          "description": "Constitutional principles. Must include P-003, P-020, P-022. (SR-001)"
        }
      },
      "additionalProperties": false
    },
    "prior_art": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Referenced prior art citations."
    },
    "enforcement": {
      "type": "object",
      "properties": {
        "tier": {
          "type": "string",
          "enum": ["hard", "medium", "soft"]
        },
        "escalation_path": { "type": "string" }
      },
      "additionalProperties": false
    },
    "session_context": {
      "type": "object",
      "properties": {
        "schema": { "type": "string" },
        "on_receive": {
          "type": "array",
          "items": { "type": "string" }
        },
        "on_send": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "additionalProperties": false,
      "description": "Handoff protocol configuration. (HR-001, HR-002)"
    }
  },
  "additionalProperties": true
}
```

**Schema Design Decisions:**

| Decision | Rationale |
|----------|-----------|
| Draft 2020-12 selected | Widest tooling support: VS Code, Python `jsonschema`, JavaScript `ajv`, CI/CD pipelines. (OI-01 resolution) |
| `additionalProperties: true` at root | Allows backward-compatible field additions without schema revision. Fields within structured objects (identity, capabilities, guardrails) use `additionalProperties: false` for strictness where structure matters. |
| `enum` for `cognitive_mode` with 5 values | Consolidates PR-002's enumerated set. The nse-requirements-001 listed 8 modes; this schema adopts the 5 modes validated by nse-architecture-001's design patterns. The 3 modes removed (`strategic`, `critical`, `communicative`) are subsumed: `strategic` maps to `convergent` for decision-making, `critical` maps to `convergent` for review/evaluation, `communicative` maps to `divergent` for conversational agents. |
| `minItems: 3` for `forbidden_actions` | Ensures constitutional triplet (P-003, P-020, P-022) is always present. Additional forbidden actions are agent-specific. |
| `allowed_tools` enum includes MCP tools | Enables deterministic validation that agents only reference known tools. New tools require schema version update. See also the MCP infrastructure coupling row below for versioning guidance. |
| Conditional `location` requirement | `output.location` is required only when `output.required` is `true`, accommodating agents that operate as validators or conversational agents without file output. |
| MCP tool names in `allowed_tools` enum are infrastructure-coupled | The `mcp__memory-keeper__context_save` and `mcp__context7__*` names reflect the current MCP server configuration naming convention, which is an infrastructure detail. If MCP server names change (e.g., a rename from `context_save` to `store`), the schema enum becomes invalid. This coupling is an intentional trade-off: deterministic tool validation at CI time is worth the maintenance cost of tracking MCP configuration changes. **Schema versioning guidance:** MCP tool name changes MUST trigger a schema minor-version update. The schema CHANGELOG should track MCP tool name mappings per version. Schema consumers should pin to a specific schema version to avoid breakage during MCP transitions. |

**Schema Validation Against Existing Agents:**

To verify backward compatibility, the JSON Schema was validated against three existing agent frontmatter blocks representing different skill families, tool tiers, and cognitive modes. Results below.

**Agent 1: ps-researcher (problem-solving, T3/T5, divergent)**

| Field / Constraint | Result | Detail |
|--------------------|--------|--------|
| `name` pattern | PASS | "ps-researcher" matches `^[a-z]+-[a-z]+(-[a-z]+)*$` |
| `version` pattern | PASS | "2.3.0" matches `^\d+\.\d+\.\d+$` |
| `description` maxLength, no XML | PASS | 153 chars, no XML tags |
| `model` enum | PASS | "opus" is valid |
| `identity` required fields | PASS | role, expertise (4 items >= 2), cognitive_mode ("divergent") all present |
| `identity` additionalProperties | PASS | No extra fields in identity object |
| `persona` enums | PASS | tone="professional", communication_style="consultative", audience_level="adaptive" all valid |
| `capabilities.allowed_tools` enum | PASS | All 11 tools are valid enum values |
| `capabilities.forbidden_actions` minItems | PASS | 4 items >= 3 |
| `guardrails.input_validation` minItems | PASS | 2 items >= 1 |
| `guardrails.output_filtering` minItems, string type | PASS | 3 string items >= 3 |
| `guardrails.fallback_behavior` enum | PASS | "warn_and_retry" is valid |
| `output.required` + conditional `location` | PASS | required=true, location present |
| `output.levels` enum array | PASS | ["L0", "L1", "L2"] all valid |
| `constitution.principles_applied` minItems | PASS | 6 items >= 3 |
| `session_context` additionalProperties | **FAIL** | Frontmatter includes `schema_version`, `input_validation`, `output_validation` fields not declared in schema. Schema uses `additionalProperties: false` on `session_context`. |

**Verdict: 1 violation.** The `session_context` object includes extension fields (`schema_version`, `input_validation`, `output_validation`) beyond the three declared properties (`schema`, `on_receive`, `on_send`). Fix: Either add these fields to the schema's `session_context` definition, or change `session_context` to `additionalProperties: true`.

**Agent 2: adv-executor (adversary, T1, convergent)**

| Field / Constraint | Result | Detail |
|--------------------|--------|--------|
| `name` pattern | PASS | "adv-executor" matches |
| `version` pattern | PASS | "1.0.0" matches |
| `description` maxLength, no XML | PASS | ~170 chars, no XML tags |
| `model` enum | PASS | "sonnet" is valid |
| `identity` required fields | PASS | role, expertise (4 items), cognitive_mode ("convergent") present |
| `identity` additionalProperties | **FAIL** | Includes `belbin_role: "Monitor Evaluator"` not declared in schema |
| `persona.tone` enum | **FAIL** | "analytical" is not in enum ["professional", "technical", "consultative"] |
| `persona.communication_style` enum | **FAIL** | "evidence-based" is not in enum ["consultative", "directive", "analytical"] |
| `capabilities.allowed_tools` enum | PASS | ["Read", "Write", "Edit", "Glob", "Grep"] all valid |
| `capabilities.forbidden_actions` minItems | PASS | 6 items >= 3 |
| `guardrails.output_filtering` string type | **FAIL** | Items are key-value objects (e.g., `findings_must_have_severity: "Critical/Major/Minor"`), not plain strings |
| `guardrails.fallback_behavior` enum | **FAIL** | "warn_and_request_strategy_id" is not in enum ["warn_and_retry", "escalate_to_user", "persist_and_halt"] |
| `output` required at root | **FAIL** | No `output` section in frontmatter; `output` is a required top-level field |
| `constitution.principles_applied` minItems | PASS | 6 items >= 3 |

**Verdict: 6 violations.** The most significant are: missing required `output` section, `identity` extension field (`belbin_role`), `persona` enum values outside the declared set, `guardrails.output_filtering` items as objects instead of strings, and `fallback_behavior` custom value. These violations confirm the Migration Effort Estimate prediction that adversary agents would have "medium" violations.

**Agent 3: orch-planner (orchestration, T4, convergent)**

| Field / Constraint | Result | Detail |
|--------------------|--------|--------|
| `name` pattern | PASS | "orch-planner" matches |
| `version` pattern | PASS | "2.2.0" matches |
| `description` maxLength, no XML | PASS | ~103 chars, no XML tags |
| `model` enum | PASS | "sonnet" is valid |
| `identity` required fields | PASS | role, expertise (8 items), cognitive_mode ("convergent") present |
| `identity` additionalProperties | **FAIL** | Includes `orchestration_patterns` array not declared in schema |
| `persona` enums | PASS | tone, communication_style, audience_level all valid |
| `persona` additionalProperties | **FAIL** | Includes `character` field not declared in schema |
| `capabilities.allowed_tools` enum | **FAIL** | Uses `mcp__memory-keeper__store`, `mcp__memory-keeper__retrieve`, `mcp__memory-keeper__search` -- these names do not match schema enum values (`mcp__memory-keeper__context_save`, `mcp__memory-keeper__context_get`, `mcp__memory-keeper__context_search`, `mcp__memory-keeper__context_checkpoint`). Tool naming mismatch between production agents and schema. |
| `capabilities.forbidden_actions` minItems | PASS | 5 items >= 3 |
| `guardrails.input_validation` minItems | PASS | 2 items >= 1 |
| `guardrails.output_filtering` minItems, string type | PASS | 4 string items >= 3 |
| `guardrails.fallback_behavior` enum | PASS | "warn_and_retry" is valid |
| `output.required` + conditional `location` | PASS | required=true, location present |
| `output.levels` type | **FAIL** | `levels` is a nested object (`L0: {name, content}`) instead of an array of enum strings `["L0", "L1", "L2"]` |
| `output` additionalProperties | **FAIL** | Includes `secondary_artifacts` array not declared in schema |
| `validation` additionalProperties | **FAIL** | Includes `disclaimer_required` field not declared in schema |
| `constitution.principles_applied` minItems | PASS | 6 items >= 3 |
| `session_context` additionalProperties | **FAIL** | Same violation as ps-researcher: includes `schema_version`, `input_validation`, `output_validation` |

**Verdict: 7 violations.** The most architecturally significant is the MCP tool name mismatch: orch-planner uses `mcp__memory-keeper__store` while the schema enum specifies `mcp__memory-keeper__context_save`. This confirms the infrastructure coupling concern raised in Schema Design Decisions. Other violations involve `additionalProperties: false` rejecting extension fields that production agents legitimately use, and the `output.levels` structural mismatch (object vs. array).

**Validation Summary:**

| Agent | Violations | Critical Findings |
|-------|-----------|-------------------|
| ps-researcher | 1 | `session_context` extension fields |
| adv-executor | 6 | Missing `output`, `persona` enum gaps, `identity` extension, `guardrails` type mismatch |
| orch-planner | 7 | MCP tool name mismatch, `output.levels` structural mismatch, multiple `additionalProperties` violations |

**Schema Revision Recommendations (for schema v1.0.0 finalization):**

1. **Expand `persona` enums.** Add "analytical" to `tone` and "evidence-based" to `communication_style`. These are legitimate production values.
2. **Expand `fallback_behavior` enum** or change to open string. Agent-specific fallback behaviors (e.g., "warn_and_request_strategy_id") are valid specializations.
3. **Relax `additionalProperties` on `identity`, `persona`, `session_context`, `output`, and `validation`** to `true`, or add commonly-used extension fields (`belbin_role`, `orchestration_patterns`, `character`, `schema_version`, `secondary_artifacts`, `disclaimer_required`). The current `false` setting rejects legitimate production patterns.
4. **Reconcile MCP tool names.** The schema enum must match actual MCP tool names used in production. Either update the schema enum to match production usage (`mcp__memory-keeper__store`) or update production agents to match the schema (`mcp__memory-keeper__context_save`).
5. **Support both `output.levels` formats.** Either accept the array-of-enum format (schema current) and migrate production agents, or support both formats via `oneOf`.
6. **Make `output` RECOMMENDED rather than REQUIRED** for agents that do not produce file artifacts (e.g., adv-executor operates as a worker with output managed by the orchestrator).

These findings confirm that the schema is structurally sound but needs enum expansion and `additionalProperties` relaxation before production deployment. The Migration Path Phase 1 (validation-only) will surface these violations systematically across all 37 agents.

---

### 3. Hexagonal Architecture Mapping

Agent definitions map to hexagonal architecture (ports and adapters) layers by analogy. This mapping provides an architectural mental model ensuring that the domain layer (reasoning core) remains independent of runtime details, tool implementations, and output formats -- inspired by the same dependency direction principle as H-07 (which governs Python import dependencies), applied here to agent definition content organization. Note: this is an architectural analogy guiding content structure, not a direct implementation of H-07's code-level import constraints.

```
+------------------------------------------------------------------+
|                    INFRASTRUCTURE LAYER                           |
|  Claude Code Runtime | Context Window (200K) | Model Selection   |
|  MCP Servers | Filesystem | Session Manager                     |
|                                                                  |
|  MAPS TO: .claude/settings.local.json, model tier in YAML        |
+------------------------------------------------------------------+
|                                                                  |
|  +------------------------------------------------------------+ |
|  |                    ADAPTER LAYER                            | |
|  |                                                            | |
|  |  INBOUND ADAPTERS              OUTBOUND ADAPTERS           | |
|  |  - System prompt construction  - L0/L1/L2 output formatter | |
|  |  - Session context deserialize - Artifact writer            | |
|  |  - Guardrail input validator   - Handoff schema serializer  | |
|  |                                                            | |
|  |  MAPS TO: YAML frontmatter (persona, guardrails, output);  | |
|  |           XML-tagged behavioral sections in Markdown body   | |
|  +------------------------------------------------------------+ |
|                                                                  |
|  +------------------------------------------------------------+ |
|  |                      PORT LAYER                             | |
|  |                                                            | |
|  |  PRIMARY PORTS (Driving)    SECONDARY PORTS (Driven)       | |
|  |  - Task invocation          - File System I/O (Read/Write) | |
|  |  - Direct user invocation   - Search (Glob/Grep)           | |
|  |                             - Web Access (WebSearch/Fetch)  | |
|  |                             - MCP (Context7/MemoryKeeper)   | |
|  |                             - Execution (Bash/Task)         | |
|  |                                                            | |
|  |  MAPS TO: capabilities.allowed_tools in YAML frontmatter   | |
|  +------------------------------------------------------------+ |
|                                                                  |
|  +------------------------------------------------------------+ |
|  |                     DOMAIN LAYER (Core)                     | |
|  |                                                            | |
|  |  - Cognitive mode (divergent/convergent/integrative/etc.)   | |
|  |  - Expertise domain (research, architecture, review, etc.)  | |
|  |  - Decision logic (constitutional compliance, guardrails)   | |
|  |  - Quality standards (H-13 threshold, S-014 rubric)         | |
|  |  - Reasoning strategy (methodology, heuristics)             | |
|  |                                                            | |
|  |  MAPS TO: Markdown body (<identity>, <methodology>,         | |
|  |           <purpose>, <guardrails> sections)                 | |
|  +------------------------------------------------------------+ |
+------------------------------------------------------------------+
```

**Layer-to-Definition Mapping:**

| Hexagonal Layer | Agent Definition Location | Contents | Dependency Rule |
|----------------|--------------------------|----------|----------------|
| **Domain** | Markdown body: `<identity>`, `<purpose>`, `<methodology>`, `<guardrails>` sections | Cognitive mode, expertise, reasoning strategy, quality standards, decision logic | MUST NOT reference specific tools, output formats, or runtime details |
| **Port** | YAML: `capabilities.allowed_tools` | Abstract declarations of what tools the agent needs | Declares capabilities without implementing them |
| **Adapter** | YAML: `persona`, `guardrails`, `output`, `session_context`; Markdown: `<input>`, `<output>`, `<capabilities>` sections | System prompt construction, input validation, output formatting, handoff serialization | Implements port contracts; can change without modifying domain |
| **Infrastructure** | YAML: `model`; external: `.claude/settings.local.json`, MCP server configs | Runtime environment, model selection, MCP server connections | Outermost layer; changes here do not affect agent behavior logic |

**Hexagonal Invariant Verification:**

The domain layer (Markdown body reasoning sections) MUST NOT contain:
- Specific tool names (use capability descriptions instead: "search the codebase" not "use Grep")
- Output format details (these belong in the `<output>` adapter section)
- Model-specific instructions (model selection is infrastructure)
- MCP key patterns or file paths (these are adapter/infrastructure concerns)

This invariant is inspired by the same dependency direction principle as H-07 ("Domain layer MUST NOT import from application, infrastructure, or interface"), applied to agent definition content organization. H-07 governs Python import dependencies; this invariant extends the same directional discipline to markdown content structure, where "import" means "reference specific implementation details."

---

### 4. Tool Security Tiers (T1-T5)

Five security tiers control tool access, implementing the principle of least privilege (AR-006). The tier system was defined by nse-architecture-001 and validated against all 37 existing agents.

| Tier | Name | Tools Included | Use Case | Example Agents |
|------|------|---------------|----------|----------------|
| **T1** | Read-Only | Read, Glob, Grep | Evaluation, auditing, scoring, validation | adv-executor, adv-scorer, wt-auditor |
| **T2** | Read-Write | T1 + Write, Edit, Bash | Analysis, document production, code generation | ps-analyst, nse-architecture, ps-critic |
| **T3** | External | T2 + WebSearch, WebFetch, Context7 | Research, exploration, external documentation | ps-researcher, nse-explorer |
| **T4** | Persistent | T2 + Memory-Keeper | Cross-session state management, orchestration | orch-planner, orch-tracker, nse-requirements |
| **T5** | Full | T3 + T4 + Task | Orchestration with delegation, full capability | Lead agent, skill orchestrators |

**Selection Guidelines:**

1. **Default to T1.** Begin with the lowest tier and justify upward. If an agent only needs to read and evaluate, T1 is sufficient.

2. **T2 when the agent produces artifacts.** If the agent writes files (research reports, architecture docs, analysis outputs), T2 is the minimum. Bash is included for execution tasks (running tests, scripts).

3. **T3 when external information is needed.** Research and exploration agents that consult web sources, library documentation (Context7), or external APIs require T3. T3 agents MUST include citation guardrails (P-001, P-004) in `guardrails.output_filtering`.

4. **T4 when cross-session state is required.** Agents that store or retrieve context via Memory-Keeper (MCP-002 phase boundaries, multi-session research) require T4. T4 agents MUST follow the MCP key pattern: `jerry/{project}/{entity-type}/{entity-id}`.

5. **T5 requires explicit justification.** The Task tool enables agent delegation, which requires P-003 compliance verification. T5 is reserved for orchestrators and lead agents that coordinate other agents. Every T5 assignment must document why delegation is necessary.

**Constraints:**
- Worker agents (invoked via Task) MUST NOT include Task in their `allowed_tools` (enforces AR-004/P-003 single-level nesting).
- T3+ agents carrying external access MUST declare citation guardrails.
- T4+ agents using Memory-Keeper MUST follow the key namespace convention.

---

### 5. Cognitive Mode Taxonomy

Five cognitive modes classify how agents reason. The mode is declared in `identity.cognitive_mode` and shapes the agent's methodology, output structure, and iteration behavior. This taxonomy was validated by Pattern 9 (Cognitive Mode Pattern) from nse-architecture-001 and the taxonomy dimension analysis in ps-analyst-001.

| Mode | Description | Reasoning Pattern | Output Pattern | Iteration Behavior |
|------|-------------|-------------------|----------------|-------------------|
| **Divergent** | Explores broadly, generates options, discovers patterns | Wide search, multiple hypotheses, creative association | Multiple alternatives, options lists, broad coverage | Expands search space on each iteration |
| **Convergent** | Analyzes narrowly, selects options, produces conclusions | Focused evaluation, criteria-based selection, synthesis | Ranked recommendations, selected alternatives, focused analysis | Narrows from options to decision on each iteration |
| **Integrative** | Combines inputs from multiple sources into unified output | Cross-source correlation, pattern merging, gap filling | Unified narratives, cross-reference tables, gap analysis | Builds coherence across inputs on each iteration |
| **Systematic** | Applies step-by-step procedures, verifies compliance | Checklist execution, protocol adherence, completeness verification | Checklists, pass/fail tables, compliance matrices | Processes items sequentially without skipping |
| **Forensic** | Traces causes backward from symptoms to root causes | Causal chain analysis, evidence correlation, hypothesis testing | Root cause chains, evidence correlation, 5 Whys | Narrows hypothesis space on each iteration |

**Selection Criteria:**

| Agent Task Type | Recommended Mode | Rationale |
|----------------|-----------------|-----------|
| Research, exploration, brainstorming | Divergent | Needs breadth; premature convergence misses sources |
| Analysis, evaluation, scoring, review, architecture | Convergent | Needs focused conclusion from alternatives |
| Synthesis, cross-pipeline merging, taxonomy building | Integrative | Needs to unify multiple perspectives |
| Validation, auditing, compliance checking, formatting | Systematic | Needs procedural completeness |
| Root cause analysis, debugging, failure investigation | Forensic | Needs backward causal tracing |

**Design Implications by Mode:**

| Mode | Tool Profile | Model Recommendation | Context Budget Priority |
|------|-------------|---------------------|------------------------|
| Divergent | T3+ (needs external access) | Opus (complex reasoning) | Larger tool result allocation (~50%) |
| Convergent | T1 or T2 (focused input) | Sonnet or Opus | Balanced allocation |
| Integrative | T2 (multiple file reads) | Opus (complex synthesis) | Larger user message allocation for multi-source input |
| Systematic | T1 (read-only preferred) | Sonnet or Haiku (procedural) | Smaller allocation; systematic work is compact |
| Forensic | T2 or T3 (investigation needs) | Opus (complex reasoning) | Larger reasoning allocation (~35%) |

**Cognitive Mode Consolidation Note (PR-002):**

The nse-requirements-001 specification listed 8 cognitive modes: divergent, convergent, integrative, systematic, strategic, critical, forensic, communicative. This ADR consolidates to 5 modes based on the following analysis:

| Removed Mode | Subsumed By | Rationale |
|-------------|------------|-----------|
| `strategic` | `convergent` | Strategic planning is a form of convergent decision-making with longer time horizons. The methodology section in the agent body captures strategic framing. |
| `critical` | `convergent` | Critical evaluation is convergent reasoning applied to quality assessment. Critic agents (adv-scorer, ps-critic) use convergent mode with evaluation-specific methodology. |
| `communicative` | `divergent` | Conversational agents (sb-voice) explore user needs broadly, which is divergent reasoning in an interactive autonomy context. |

This consolidation reduces enum complexity without losing behavioral expressiveness. The agent body's `<methodology>` section captures mode-specific variations that the YAML enum cannot express.

---

### 6. Progressive Disclosure Structure

Agent definition content is organized into three tiers that load progressively, minimizing context window consumption and mitigating context rot (R-T01). This implements PR-004 and Pattern 4 (Progressive Disclosure).

```
Tier 1: METADATA              Tier 2: CORE                  Tier 3: SUPPLEMENTARY
(Always loaded, ~500 tok)      (On invocation, ~2K-8K tok)   (On demand, variable)
+------------------------+     +------------------------+     +------------------------+
| - Agent name           |     | - Full YAML frontmatter|     | - Output templates      |
| - Description (H-28)   |     | - Markdown body:       |     | - Prior work artifacts   |
| - Trigger keywords     |     |   <identity>           |     | - Strategy templates     |
| - Cognitive mode       |     |   <purpose>            |     | - Example outputs        |
|                        |     |   <input>              |     | - Reference documents    |
| Source: SKILL.md       |     |   <methodology>        |     | - Cross-pollination data |
| description field      |     |   <output>             |     |                          |
|                        |     |   <guardrails>         |     | Source: Read tool during |
| Purpose: Route to      |     |   <capabilities>       |     | execution                |
| correct agent          |     |                        |     |                          |
+------------------------+     | Source: Agent def file  |     | Purpose: Task-specific   |
                               | loaded by Task tool     |     | knowledge                |
                               +------------------------+     +------------------------+
```

**Tier Content Guidelines:**

| Tier | Maximum Size | Content Rules | Loading Mechanism |
|------|-------------|---------------|-------------------|
| Tier 1 | ~500 tokens per skill | Name + description + triggers only. No methodology, no examples, no templates. | SKILL.md `description` field, loaded at session start |
| Tier 2 | ~2,000-8,000 tokens per agent | Full YAML frontmatter + essential behavioral sections. No reference data, no prior work, no verbose examples. | Agent definition file, loaded when Task tool invokes the agent |
| Tier 3 | Variable (budget-aware) | Templates, prior artifacts, reference documents. Load only what is needed for the current task. Use Read with offset/limit for large files. | Read tool during agent execution; governed by CB-01 through CB-05 budget rules |

**Context Budget Rules (CB-01 through CB-05):**

> **Traceability note:** CB-01 through CB-05 are MEDIUM-tier recommendations introduced by this ADR to operationalize the progressive disclosure structure (PR-004) and context rot mitigation (R-T01, RPN 392). They are not traced to specific shall-statements in nse-requirements-001 because the requirements specify *what* progressive disclosure must achieve (PR-004: "The agent definition format SHALL support progressive disclosure of information based on need"), not *how* context budgets should be allocated. These rules bridge that gap as implementation-level guidance. They use SHOULD vocabulary (MEDIUM tier) and can be overridden with documented justification.

| Rule | Constraint | Tier | Rationale |
|------|-----------|------|-----------|
| CB-01 | Reserve >= 5% of context for output generation | MEDIUM | Prevents truncated output when context fills during reasoning. Operationalizes PR-004 Tier 3 loading discipline. |
| CB-02 | Tool results SHOULD NOT exceed 50% of total context | MEDIUM | Leaves room for reasoning; prefer targeted reads over bulk reads. Derived from R-T01 mitigation (context rot). |
| CB-03 | Prefer file-path references over inline content in handoffs | MEDIUM | Avoids duplicating large content across handoff + tool result reads. Operationalizes PR-004 Tier 1/Tier 2 boundary. |
| CB-04 | Use key_findings (3-5 bullets) for quick orientation; defer detail to file reads | MEDIUM | 500-token orientation prevents 5,000-token cold read. Operationalizes HR-002 handoff efficiency. |
| CB-05 | For files > 500 lines, use offset/limit parameters on Read | MEDIUM | Prevents single-file context exhaustion. Derived from R-T01 mitigation. |

---

### 7. Guardrails Template

Every agent definition must include guardrails addressing four areas: input validation, output filtering, forbidden actions, and fallback behavior. This section specifies the required structure and minimum content for each area, consolidating SR-002, SR-003, SR-009, and AR-012.

**Required Guardrail Sections:**

```yaml
guardrails:
  # --- INPUT VALIDATION (SR-002) ---
  # At least one validation rule. Format: field_name: "regex_pattern"
  # Purpose: First line of defense against malformed inputs.
  input_validation:
    - field_format: "^{pattern}$"

  # --- OUTPUT FILTERING (SR-003) ---
  # Minimum 3 entries. Prevents harmful/incorrect output.
  output_filtering:
    - no_secrets_in_output          # REQUIRED: Prevents API keys, credentials, tokens
    - no_executable_code_without_confirmation  # REQUIRED: Prevents unauthorized code execution
    - all_claims_must_have_citations # REQUIRED: Ensures factual claims are sourced

  # --- FALLBACK BEHAVIOR (SR-009) ---
  # What happens when the agent encounters an unresolvable error.
  fallback_behavior: "warn_and_retry"  # Options: warn_and_retry, escalate_to_user, persist_and_halt

# --- FORBIDDEN ACTIONS (AR-012, in capabilities section) ---
capabilities:
  forbidden_actions:
    - "Spawn recursive subagents (P-003)"   # REQUIRED: Constitutional constraint
    - "Override user decisions (P-020)"      # REQUIRED: Constitutional constraint
    - "Misrepresent capabilities (P-022)"    # REQUIRED: Constitutional constraint
    # Agent-specific forbidden actions below:
    - "{additional forbidden action}"
```

**Guardrail Selection Guide by Agent Type:**

| Agent Type | Additional Input Validation | Additional Output Filtering | Recommended Fallback |
|-----------|---------------------------|---------------------------|---------------------|
| Research (divergent, T3) | URL format validation, source tiering | Source authority tier required, stale data warnings | warn_and_retry |
| Analysis (convergent, T2) | Input schema validation, artifact path existence | Confidence bounds required, methodology citation | escalate_to_user |
| Validation (systematic, T1) | Criteria format validation | Binary pass/fail with evidence | persist_and_halt |
| Orchestration (T4-T5) | Phase state validation, predecessor completion | Progress percentage, blocker enumeration | escalate_to_user |
| Scoring (convergent, T1) | Rubric schema validation, score range validation | Anti-leniency statement, dimension-level breakdown | warn_and_retry |

**Constitutional Compliance Checklist (SR-001):**

Every agent MUST include in `constitution.principles_applied`:

| Principle | Constraint | Agent Behavior |
|-----------|-----------|----------------|
| P-003 | No recursive subagents | Worker agents MUST NOT include Task in allowed_tools |
| P-020 | User authority | NEVER override explicit user instructions |
| P-022 | No deception | Accurately report capabilities, confidence, and actions |

Additional principles are agent-specific and should trace to the governance document.

---

## Consequences

### Positive Consequences

| Consequence | Impact | Mechanism |
|-------------|--------|-----------|
| Deterministic structural validation | Catches missing fields, invalid enums, malformed names at CI time with zero LLM cost | JSON Schema validation (Section 2) as Quality Gate Layer 1 (Pattern 8) |
| Consistent agent definitions across the framework | New agents follow the same structure; reduced cognitive load for authors and consumers | Canonical template (Section 1) with field-level requirement traceability |
| Hexagonal dependency enforcement | Domain layer reasoning remains independent of tools and output formats; adaptable to runtime changes | Hexagonal mapping (Section 3) with invariant verification rules |
| Reduced critic workload | Schema validation catches structural defects before LLM-as-Judge evaluation, allowing critics to focus on content quality | Layered QA architecture (Pattern 8, ADR-003 from nse-architecture-001) |
| Tool access governance | Principle of least privilege enforced through tier system; security boundaries are explicit and auditable | T1-T5 tiers (Section 4) with selection guidelines |
| Context rot mitigation (R-T01) | Progressive disclosure loads only needed context; three-tier structure prevents upfront context exhaustion | Progressive disclosure structure (Section 6) with CB-01 through CB-05 budget rules |
| Error amplification mitigation (R-T02) | Structured handoff schema with required fields prevents free-text information loss at agent boundaries | Session context schema + handoff protocol (Sections 1, 2) |

### Negative Consequences

| Consequence | Impact | Mitigation |
|-------------|--------|------------|
| Schema maintenance overhead | JSON Schema must be updated when new fields or tools are added | Version the schema alongside framework releases; include schema update in tool addition checklist |
| Initial migration effort | 37 existing agents must be validated against the schema; some may need field additions | Phased migration (see [Migration Path](#migration-path)); schema is designed for backward compatibility |
| Cognitive mode consolidation friction | Reducing from 8 to 5 modes requires updating nse-requirements-001 rationale | Document the subsumption rationale (Section 5, consolidation note); existing agents already use the 5 validated modes |
| Template rigidity vs. authoring flexibility | Strict REQUIRED fields may feel constraining for rapid prototyping | Schema uses `additionalProperties: true` at root for extension; RECOMMENDED fields are not schema-enforced |
| Enum evolution requires schema updates | Adding new cognitive modes, tools, or fallback behaviors requires schema revision | Semantic versioning on schema; minor version for additions, major version for breaking changes |

### Risk Mitigation

**R-T01: Context Rot at Scale (RPN 392, RED zone)**

Mitigated through:
- Progressive disclosure (Section 6) -- loads context in three tiers, deferring detail until needed.
- Context budget rules CB-01 through CB-05 -- explicit allocation prevents exhaustion.
- Cognitive mode alignment (Section 5) -- each mode has design implications for context budget allocation.
- Limitation: Context rot during deep multi-agent orchestration (4+ handoffs, long sessions) is partially mitigated but not eliminated. Runtime context monitoring (GAP-06 from ps-analyst-001) is a complementary enhancement not addressed by this ADR.

**R-T02: Error Amplification (RPN 336, RED zone)**

Mitigated through:
- Structured handoff schema (Section 1, `session_context`) -- JSON Schema-validated data contracts prevent free-text information loss.
- Required handoff fields (`artifacts`, `summary`, `key_findings`, `blockers`, `confidence`, `criticality`) -- each serves a distinct purpose in context preservation.
- Quality gate at handoff boundaries (HR-006) -- sending agent's output must pass quality verification before handoff.
- Limitation: Handoff schema validation is defined in this ADR but runtime enforcement requires implementation (CI tooling or pre-invocation hook).

**R-P02: Rule Proliferation (31/35 HARD slots consumed, RED zone)**

Recommendation: Consolidate H-25 through H-30 (6 skill-standards rules) into 2 compound rules to reclaim 4 HARD rule slots:

| Current Rules | Proposed Compound Rule | Slots Reclaimed |
|--------------|----------------------|-----------------|
| H-25 (SKILL.md filename), H-26 (kebab-case folder), H-27 (no README.md in skill folder) | **H-25c: Skill Directory Standards.** Skill folder MUST use kebab-case matching name field. Skill file MUST be exactly SKILL.md. No README.md inside skill folder. | 2 |
| H-29 (full repo-relative paths), H-30 (register in CLAUDE.md + AGENTS.md) | **H-29c: Skill Registration and Paths.** SKILL.md MUST use full repo-relative paths. Every skill MUST be registered in CLAUDE.md and AGENTS.md. Every agent MUST be registered in AGENTS.md and parent SKILL.md. | 1 |
| H-28 (description quality) | Retain as-is (semantically distinct from structural rules) | 0 |

Net result: 6 rules consolidated to 3, reclaiming 3 HARD rule slots (from 31/35 to 28/35 = 80% utilization). This provides headroom for future governance needs without approaching the ceiling.

**Consolidation is a recommendation, not part of the decision.** Rule consolidation modifies `.context/rules/`, triggering AE-002 (auto-C3). It should be implemented as a separate change with its own ADR, not bundled with this agent definition standard.

### Trade-off: Schema Strictness vs. Authoring Flexibility

| Dimension | Strict Schema | Flexible Schema | This ADR's Position |
|-----------|--------------|----------------|---------------------|
| Required fields | Many required fields catch more errors | Fewer required fields allow faster authoring | **Moderate strictness**: 9 required top-level fields covering identification, identity, capabilities, guardrails, output, and constitution. Persona, validation, session_context, and enforcement are RECOMMENDED but not schema-enforced. |
| Enum values | Closed enums prevent invalid values | Open strings allow evolution | **Closed enums for stable sets** (model, cognitive_mode, fallback_behavior) and **open strings for evolving sets** (description, role, expertise). |
| Additional properties | `false` prevents unexpected fields | `true` allows extension | **Mixed**: `true` at root level for backward compatibility; `false` within structured objects (identity, capabilities, guardrails) for structural integrity. |

---

## Migration Path

### Phase 1: Validation-Only (Non-Breaking)

1. Deploy JSON Schema to `docs/schemas/agent-definition-v1.0.0.json`.
2. Run schema validation against all 37 existing agent definitions.
3. Catalog violations without requiring fixes. Expected violations: missing `forbidden_actions`, missing `input_validation`, missing `constitution` section, `cognitive_mode` values outside the 5-mode enum.
4. Duration: 1 sprint.

### Phase 2: Progressive Remediation

1. Fix violations in priority order:
   - P1: Add missing `capabilities.forbidden_actions` (constitutional compliance, AR-012).
   - P1: Add missing `guardrails.input_validation` (SR-002).
   - P2: Add missing `constitution.principles_applied` (SR-001).
   - P2: Align `cognitive_mode` to 5-mode enum (PR-002 consolidation).
   - P3: Add `session_context` for agents participating in orchestrated workflows.
2. Each skill team fixes their agents; no bulk automated rewrite.
3. Duration: 2-3 sprints.

### Phase 3: CI Enforcement

1. Add schema validation to CI pipeline (L5 enforcement layer).
2. New agent definitions MUST pass schema validation before merge.
3. Existing agents grandfathered until Phase 2 completion.
4. Duration: ongoing after Phase 2.

### Migration Effort Estimate

| Agent Group | Count | Expected Violations | Estimated Fix Effort |
|-------------|-------|--------------------|--------------------|
| Problem-solving agents | 10 | Low (ps-researcher is the reference example) | 2-4 hours |
| NASA SE agents | 6 | Medium (may lack forbidden_actions, constitution) | 4-6 hours |
| Adversary agents | 3 | Medium (read-only agents may lack output config) | 2-3 hours |
| Orchestration agents | 3 | Low (well-structured) | 1-2 hours |
| Worktracker agents | 5 | Medium (may lack session_context) | 3-5 hours |
| Transcript agents | 6 | High (newer skill, may have inconsistencies) | 4-8 hours |
| Saucer-boy agents | 4 | High (creative agents may deviate from structure) | 4-6 hours |
| **Total** | **37** | -- | **20-34 hours** |

---

## Evidence Sources

### Authority Tiers

| Tier | Definition | Sources in This ADR |
|------|-----------|---------------------|
| **Industry Leader** | Published guidance from Anthropic, Google, Microsoft, OpenAI | Anthropic Agent Skills architecture, Anthropic multi-agent guidance, Google ADK patterns, Google DeepMind contract-first delegation, Microsoft AI Agent Orchestration Patterns, OpenAI Agents SDK |
| **NASA SE Process** | NPR 7123.1D formal requirements engineering | nse-requirements-001 (52 shall-statements, INCOSE 8/8 PASS) |
| **Research Synthesis** | Multi-source analysis combining multiple Industry Leader sources | ps-analyst-001 (57 patterns, 8 families), ps-investigator-001 (28 FMEA modes) |
| **Trade Study** | Structured evaluation of alternatives with weighted scoring | TS-1 through TS-5 (nse-explorer-001) |
| **Jerry Production Data** | Operational evidence from 37 agents across 8 skills | AGENTS.md, existing agent definition files |
| **Community Expert** | Published analysis from recognized practitioners | LangChain State of Agent Engineering (2025), Chroma context rot research (2024) |

### Citation Index

| Claim | Evidence | Source | Authority Tier |
|-------|----------|--------|---------------|
| YAML+MD is the optimal agent definition format | B5 scored 4.45 vs B1 at 4.00 | TS-2 | Trade Study |
| Schema validation is highest-value enhancement | Consensus #1 across all 3 NSE Phase 2 agents | nse-to-ps handoff | Consensus (3 agents) |
| Single-level nesting prevents 17x error amplification | Uncoordinated topologies cause 17x amplification | ps-researcher-002, Google DeepMind (2026) | Industry Leader |
| Free-text handoffs are #1 failure source | Google multi-agent research (2026) | ps-researcher-002 | Industry Leader |
| Quality is #1 production blocker (32% of deployments) | LangChain State of Agent Engineering (2025) | ps-researcher-003 | Community Expert |
| Context rot degrades LLM performance as context fills | Chroma context rot research (2024) | ps-researcher-001 | Community Expert |
| Progressive disclosure three-tier model is validated | Anthropic Agent Skills architecture | ps-researcher-001 | Industry Leader |
| 5 cognitive modes cover the reasoning spectrum | Pattern 9 validated against 37 agents | nse-architecture-001 | Industry Leader + Production Data |
| Keyword routing handles ~80% of cases at ~1ms | Production routing analysis | ps-researcher-002 | Jerry Production Data |
| 31/35 HARD rule slots consumed (89%) | Rule inventory analysis | nse-risk-001 | Jerry Production Data |
| Layered QA (schema + self-review + critic) is optimal | D6 scored highest at 3.70 in TS-4 | TS-4 | Trade Study |
| Tool restriction by least privilege is industry consensus | Anthropic, Microsoft, NIST AC-6 | nse-architecture-001 | Industry Leader |
| 52 formal requirements pass 8/8 INCOSE quality criteria | Requirements quality verification | nse-requirements-001 | NASA SE Process |
| 28 failure modes identified, top RPN 392 (context rot) | FMEA analysis | ps-investigator-001 | Research Synthesis |

---

## Self-Review (S-010)

### Completeness Check

| Required Content (from task specification) | Status | Location |
|-------------------------------------------|--------|----------|
| Canonical Agent Definition Template | COMPLETE | [Section 1](#1-canonical-agent-definition-template) |
| JSON Schema (Draft 2020-12) for validation | COMPLETE | [Section 2](#2-json-schema-for-agent-definition-validation) |
| Hexagonal Architecture Mapping | COMPLETE | [Section 3](#3-hexagonal-architecture-mapping) |
| 5 Tool Security Tiers (T1-T5) | COMPLETE | [Section 4](#4-tool-security-tiers-t1-t5) |
| Cognitive Mode Taxonomy (5 modes) | COMPLETE | [Section 5](#5-cognitive-mode-taxonomy) |
| Progressive Disclosure Structure (3 tiers) | COMPLETE | [Section 6](#6-progressive-disclosure-structure) |
| Guardrails Template (4 sections) | COMPLETE | [Section 7](#7-guardrails-template) |
| R-T01 context rot mitigation | COMPLETE | [Consequences: Risk Mitigation](#risk-mitigation) |
| R-T02 error amplification mitigation | COMPLETE | [Consequences: Risk Mitigation](#risk-mitigation) |
| R-P02 rule proliferation recommendation | COMPLETE | [Consequences: Risk Mitigation](#risk-mitigation) |
| Schema strictness vs. flexibility trade-off | COMPLETE | [Consequences: Trade-off](#trade-off-schema-strictness-vs-authoring-flexibility) |
| Migration path for 37 agents | COMPLETE | [Migration Path](#migration-path) |
| Navigation table (H-23) | COMPLETE | [Document Sections](#document-sections) |
| L0 executive summary | COMPLETE | [L0: Executive Summary](#l0-executive-summary) |
| Evidence citations with authority tier | COMPLETE | [Evidence Sources](#evidence-sources) |
| Nygard ADR format (Title, Status, Context, Decision, Consequences) | COMPLETE | Full document structure |
| OI-01 resolution (JSON Schema format) | COMPLETE | [Context: Open Items](#open-items-resolved-by-this-decision) |
| OI-03 resolution (Open Agent Specification) | COMPLETE | [Context: Open Items](#open-items-resolved-by-this-decision) |
| Schema validation against existing agents | COMPLETE | [Section 2: Schema Validation Against Existing Agents](#2-json-schema-for-agent-definition-validation) |
| CB-01 through CB-05 traceability | COMPLETE | [Section 6: Context Budget Rules](#6-progressive-disclosure-structure) |
| PR-004 and PR-006 template field mapping | COMPLETE | [Template Field Summary footnotes](#1-canonical-agent-definition-template) |

### Internal Consistency Check

| Dimension | Check | Result |
|-----------|-------|--------|
| Schema fields match template | Every REQUIRED template field has a corresponding schema property with `required` constraint | CONSISTENT |
| Cognitive mode enum matches taxonomy | Schema enum (5 values) matches Section 5 taxonomy table | CONSISTENT |
| Tool tiers match schema enum | Schema `allowed_tools` enum covers all tools referenced in T1-T5 tiers | CONSISTENT |
| Template requirements trace to source | Field Summary table traces every field to its source requirement (AR-/PR-/SR-/HR-), including PR-004 and PR-006 via structural footnotes | CONSISTENT |
| Hexagonal mapping matches template structure | Domain = Markdown body sections; Port = allowed_tools; Adapter = persona/guardrails/output | CONSISTENT |
| Positive consequences trace to mechanisms | Each positive consequence cites the section that implements it | CONSISTENT |
| Risk mitigations trace to RED-zone risks | R-T01, R-T02, R-P02 all addressed with specific mechanisms and acknowledged limitations | CONSISTENT |

### Identified Limitations

1. **Runtime enforcement not addressed.** This ADR defines the schema and template for agent definitions but does not implement runtime validation tooling (CI hooks, pre-invocation validation). Implementation is a separate work item.

2. **Handoff schema validation is design-time only.** The session_context handoff schema is defined structurally but runtime enforcement (validating handoff data before delivery) requires implementation beyond this ADR.

3. **Cognitive mode consolidation is opinionated.** Reducing from 8 to 5 modes involves judgment calls about subsumption. The rationale is documented but an alternative decision to retain all 8 modes is defensible. The primary cost of 8 modes is enum complexity in the schema; the primary benefit of 5 modes is cleaner selection criteria.

4. **Migration effort estimates are approximate.** The 20-34 hour estimate is based on expected violation patterns; actual effort depends on agent-specific deviations not visible from the template alone.

5. **MCP tool list in schema will require maintenance.** The `allowed_tools` enum includes current MCP tools. New MCP tools (or removal of existing ones) require schema version updates. This is an intentional trade-off favoring validation strictness over evolution flexibility.

---

*ADR produced: 2026-02-21 | Agent: ps-architect-001 v1.0.0 | PS-ID: PROJ-007 | Entry: e-004*
*Criticality: C4 (new ADR, will be baselined)*
*Self-review (S-010): COMPLETE -- 20 completeness checks passed, 7 consistency checks passed, 5 limitations documented*
*Barrier 3 revision: 5 items addressed (P1: schema validation + CB traceability; P2: H-07 mapping + PR-004/PR-006 mapping; P3: MCP coupling acknowledgment)*
*Input artifacts: nse-to-ps handoff, nse-requirements-001, nse-architecture-001, ps-analyst-001, ps-to-nse handoff, ps-researcher.md*
