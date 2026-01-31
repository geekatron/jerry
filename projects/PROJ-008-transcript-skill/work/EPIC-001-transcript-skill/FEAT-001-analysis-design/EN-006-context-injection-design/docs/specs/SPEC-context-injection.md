# SPEC: Context Injection Mechanism

<!--
DOCUMENT: SPEC-context-injection.md
VERSION: 1.0.0
STATUS: DRAFT
TASK: TASK-035 (Phase 2)
AUTHOR: ps-architect
QUALITY TARGET: >= 0.90
NASA SE: Process 4 (Technical Solution Definition)
-->

---

## Document Control

| Attribute | Value |
|-----------|-------|
| **Document ID** | SPEC-CI-001 |
| **Version** | 1.0.0 |
| **Status** | DRAFT |
| **Quality Score** | Pending ps-critic review |
| **Created** | 2026-01-26 |
| **Author** | ps-architect |
| **NASA SE Process** | Process 4: Technical Solution Definition |

### Revision History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0.0 | 2026-01-26 | ps-architect | Initial specification for Claude Code Skills implementation |

### Document Relationships

| Relationship | Document | Purpose |
|--------------|----------|---------|
| **Complements** | TDD-context-injection.md | TDD provides conceptual design; this SPEC provides Claude Code Skills implementation details |
| **Implements** | en006-requirements-supplement.md | 20 formal requirements with "shall" statements |
| **Based On** | en006-5w2h-analysis.md | WHO/WHAT/WHEN/WHERE/WHY/HOW analysis |
| **Based On** | en006-ishikawa-pareto-analysis.md | 18 root causes, 15 features prioritized |

---

## 1. Introduction

### 1.1 Purpose

This specification defines how the Context Injection Mechanism is implemented within **Claude Code Skills** (SKILL.md, AGENT.md, contexts/*.yaml, hooks). It complements the Technical Design Document (TDD) by mapping conceptual design patterns to concrete Claude Code skill constructs.

> **Critical Decision (DEC-002):** The TDD's Python code is CONCEPTUAL - it represents design patterns that Claude Code Skills must implement through their native constructs.

### 1.2 Scope

**In Scope:**
- Context injection via SKILL.md context sections
- Agent persona context via AGENT.md files
- Domain schemas via `contexts/*.yaml` files
- Template variable syntax (`{{$variable}}`)
- Hook-based context loading (`context-loader` hook)
- Skill invocation context arguments

**Out of Scope:**
- Python CLI implementation (deferred to FEAT-002)
- Full MCP server implementation (future Phase 3)
- Cross-agent context sharing (future enhancement)

### 1.3 Definitions

| Term | Definition |
|------|------------|
| **Context Payload** | Structured data injected into agent prompts at invocation time |
| **Domain Schema** | YAML file defining entity types, extraction rules, and prompt guidance for a specific domain |
| **Static Context** | Pre-defined context loaded from files at skill activation |
| **Dynamic Context** | Runtime context provided via invocation arguments or tools |
| **Template Variable** | Placeholder using `{{$variable}}` syntax, resolved at prompt assembly time |
| **Injection Point** | Location in the skill/agent lifecycle where context is inserted |

### 1.4 Relationship to TDD

The TDD describes the Context Injection Mechanism using Python interfaces and patterns. This specification maps those concepts to Claude Code Skills constructs:

```
TDD-to-SKILL MAPPING
====================

TDD Concept                    │  Claude Code Skill Construct
───────────────────────────────┼──────────────────────────────────────
IContextProvider interface     │  SKILL.md context_injection section
load_static_context()          │  contexts/{domain}.yaml files
load_dynamic_context()         │  Invocation arguments + MCP tools
resolve_template()             │  {{$variable}} in prompt templates
ContextPayload dataclass       │  Skill invocation context object
ValidationResult               │  JSON Schema validation in hooks
CircuitBreaker                 │  Hook with timeout/retry logic
Agent integration              │  AGENT.md context sections
LoadContextCommand             │  Skill invocation with --domain flag
```

---

## 2. Context Payload Specification

### 2.1 Payload Structure

The context payload is the unified data structure passed to agents. It combines static and dynamic context into a single object.

```
CONTEXT PAYLOAD STRUCTURE (L0: ELI5)
====================================

Think of the context payload like a briefcase you give to a consultant:

┌─────────────────────────────────────────────────────────────────┐
│                        CONTEXT PAYLOAD                           │
│                     (The Consultant's Briefcase)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  📁 DOMAIN KNOWLEDGE (Which industry are we in?)                 │
│     domain: "legal"                                              │
│     display_name: "Legal Document Analysis"                      │
│                                                                  │
│  📋 ENTITY DEFINITIONS (What things to look for?)                │
│     party: { attributes: [name, role, jurisdiction] }            │
│     obligation: { attributes: [obligor, terms, deadline] }       │
│                                                                  │
│  📐 EXTRACTION RULES (How to find them?)                         │
│     rules: [ {id: "parties", confidence: 0.85}, ... ]            │
│                                                                  │
│  📝 PROMPT GUIDANCE (Expert advice for the AI)                   │
│     "When analyzing legal documents:                             │
│      1. Identify parties before obligations                      │
│      2. Cross-reference with party roles"                        │
│                                                                  │
│  🔧 RUNTIME DATA (What's specific to this job?)                  │
│     document_id: "contract-2026-001"                             │
│     user_preferences: { output_format: "json" }                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Field Definitions

#### 2.2.1 Required Fields

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `domain` | string | Domain identifier (e.g., "legal", "sales") | Pattern: `^[a-z][a-z0-9-]*$`, max 50 chars |
| `schema_version` | string | Semantic version of schema format | Pattern: `^\d+\.\d+\.\d+$` |
| `entity_definitions` | object | Map of entity type to definition | At least 1 entity required |
| `extraction_rules` | array | Ordered list of extraction rules | At least 1 rule required |

#### 2.2.2 Optional Fields

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `display_name` | string | Human-readable domain name | Titlecased `domain` |
| `prompt_guidance` | string | Expert guidance for agent prompts | Empty string |
| `metadata` | object | Additional context metadata | `{}` |
| `document_id` | string | ID of document being analyzed | `null` |
| `user_preferences` | object | User-specific preferences | `{}` |
| `previous_analysis` | object | Cached previous analysis results | `null` |

### 2.3 Validation Rules

All context payloads MUST be validated against the JSON Schema defined in `schemas/context-injection-schema.json`.

**Validation Timing:**
```
VALIDATION POINTS IN LIFECYCLE
==============================

     Load YAML        Merge Contexts       Resolve Templates
         │                  │                     │
         ▼                  ▼                     ▼
    ┌─────────┐        ┌─────────┐          ┌─────────┐
    │VALIDATE │        │VALIDATE │          │VALIDATE │
    │ Schema  │───────►│ Merged  │─────────►│ Output  │
    │ Format  │        │ Types   │          │ Format  │
    └─────────┘        └─────────┘          └─────────┘
         │                  │                     │
    Fail-Fast         Type Safety          Output Integrity
```

**Validation Rules Matrix:**

| Rule ID | Field | Constraint | Error Message |
|---------|-------|------------|---------------|
| V-001 | domain | Required, pattern match | "Domain identifier is required and must be lowercase alphanumeric" |
| V-002 | schema_version | Semantic version | "Schema version must be in X.Y.Z format" |
| V-003 | entity_definitions | Non-empty object | "At least one entity definition is required" |
| V-004 | extraction_rules | Non-empty array | "At least one extraction rule is required" |
| V-005 | extraction_rules[].id | Unique within array | "Extraction rule IDs must be unique" |
| V-006 | extraction_rules[].confidence_threshold | 0.0-1.0 range | "Confidence threshold must be between 0.0 and 1.0" |
| V-007 | entity_definitions[].attributes | Non-empty array | "Entity must have at least one attribute" |
| V-008 | payload size | <= 50MB | "Context payload exceeds maximum size of 50MB" |

---

## 3. Claude Code Skill Constructs

### 3.1 SKILL.md Context Section

The SKILL.md file is the primary entry point for context injection. It defines how context flows to agents.

#### 3.1.1 Structure

```yaml
---
name: transcript
description: Parse and extract from transcripts with domain-specific context
version: "1.0.0"
allowed-tools: Read, Write, Glob, Task

# CONTEXT INJECTION SECTION (REQ-CI-F-002)
context_injection:
  # Default domain when none specified
  default_domain: "general"

  # Available domain schemas
  domains:
    - legal
    - sales
    - engineering
    - general

  # Context files location
  context_path: "./contexts/"

  # Template variables available to agents
  template_variables:
    - name: domain
      source: invocation.domain
      default: "general"
    - name: extraction_rules
      source: context.extraction_rules
      format: yaml
    - name: entity_types
      source: context.entity_definitions
      format: list

activation-keywords:
  - "transcript"
  - "/transcript"
---
```

#### 3.1.2 Context Flow from SKILL.md

```
SKILL.md CONTEXT FLOW (L1: Engineer)
====================================

User Invocation                    SKILL.md Processing                Agent Execution
─────────────────                  ───────────────────                ───────────────

/transcript --domain legal         ┌─────────────────────┐
            │                      │ 1. Parse frontmatter │
            │                      │    context_injection │
            ▼                      └──────────┬──────────┘
    ┌───────────────┐                         │
    │ domain="legal"│                         ▼
    │ file="doc.vtt"│             ┌─────────────────────┐
    └───────┬───────┘             │ 2. Load domain YAML │
            │                      │    contexts/legal.  │
            │                      │    yaml              │
            │                      └──────────┬──────────┘
            │                                 │
            │                                 ▼
            │                      ┌─────────────────────┐
            │                      │ 3. Validate schema  │
            │                      │    against JSON     │
            │                      │    Schema           │
            │                      └──────────┬──────────┘
            │                                 │
            │                                 ▼
            │                      ┌─────────────────────┐
            │                      │ 4. Build context    │
            │                      │    payload object   │
            │                      └──────────┬──────────┘
            │                                 │
            └─────────────────────────────────┘
                                              │
                                              ▼
                                  ┌─────────────────────┐
                                  │ ts-parser AGENT     │
                                  │ ─────────────────── │
                                  │ Context available   │
                                  │ as {{$domain}},     │
                                  │ {{$extraction_rules}│
                                  └─────────────────────┘
```

### 3.2 AGENT.md Persona Context

Each agent can have persona-specific context in its AGENT.md file.

#### 3.2.1 Structure

```yaml
---
name: ts-extractor
version: "1.0.0"
description: "Extract semantic entities from transcripts"
model: "sonnet"

# AGENT-SPECIFIC CONTEXT (REQ-CI-F-003)
context:
  # Persona context merged with skill context
  persona:
    role: "Entity Extraction Specialist"
    expertise:
      - "Named Entity Recognition"
      - "Confidence scoring"
      - "Citation generation"

  # Domain overrides (merged with skill context)
  domain_extensions:
    legal:
      additional_entities:
        - "contract_clause"
        - "governing_law"
    sales:
      additional_entities:
        - "objection_type"
        - "buying_signal"

  # Template variables specific to this agent
  template_variables:
    - name: confidence_threshold
      default: 0.7
      type: float
    - name: max_extractions
      default: 100
      type: integer
---
```

#### 3.2.2 Context Merge Priority

```
CONTEXT MERGE ORDER (L2: Architect)
===================================

When multiple context sources provide the same field, later sources override earlier:

Priority (Low → High):
─────────────────────

1. SKILL.md default context
       │
       ▼
2. contexts/{domain}.yaml
       │
       ▼
3. AGENT.md persona context
       │
       ▼
4. AGENT.md domain_extensions
       │
       ▼
5. Invocation arguments (--domain, etc.)
       │
       ▼
┌─────────────────────────────┐
│     FINAL MERGED CONTEXT    │
│  (Highest priority wins)    │
└─────────────────────────────┘

Example:
─────────
SKILL.md:          confidence_threshold: 0.5
legal.yaml:        confidence_threshold: 0.7
ts-extractor.md:   confidence_threshold: 0.8
invocation:        --confidence 0.9

RESULT: confidence_threshold = 0.9 (invocation wins)
```

### 3.3 contexts/*.yaml Domain Files

Domain schema files define the domain-specific knowledge.

#### 3.3.1 File Location

```
skills/transcript/
├── SKILL.md
├── agents/
│   ├── ts-parser.md
│   ├── ts-extractor.md
│   └── ts-formatter.md
└── contexts/                    ← Domain schemas location
    ├── legal.yaml
    ├── sales.yaml
    ├── engineering.yaml
    └── general.yaml
```

#### 3.3.2 Schema Structure

```yaml
# contexts/legal.yaml
# Domain Schema for Legal Document Analysis
# Implements: REQ-CI-F-001, REQ-CI-F-007

schema_version: "1.0.0"
domain: "legal"
display_name: "Legal Document Analysis"

# Entity definitions (what to look for)
entity_definitions:
  party:
    description: "Legal entity in contract"
    attributes:
      - name: "name"
        type: "string"
        required: true
      - name: "role"
        type: "enum"
        values: ["buyer", "seller", "guarantor", "witness"]
      - name: "jurisdiction"
        type: "string"
    extraction_patterns:
      - '{{name}} (the "{{role}}")'
      - "{{role}}: {{name}}"

  obligation:
    description: "Contractual obligation"
    attributes:
      - name: "obligor"
        type: "string"
        required: true
      - name: "obligee"
        type: "string"
      - name: "terms"
        type: "string"
      - name: "deadline"
        type: "date"

  clause:
    description: "Contract clause"
    attributes:
      - name: "number"
        type: "string"
      - name: "title"
        type: "string"
      - name: "text"
        type: "string"
        required: true

# Extraction rules (how to find entities)
extraction_rules:
  - id: "parties"
    description: "Identify all parties mentioned by name and role"
    entity_type: "party"
    priority: 1
    confidence_threshold: 0.85
    patterns:
      - regex: '([A-Z][a-z]+ [A-Z][a-z]+)\s*\(the\s*"([^"]+)"\)'
        groups:
          name: 1
          role: 2

  - id: "dates"
    description: "Extract all dates in ISO 8601 format"
    entity_type: "date"
    priority: 2
    confidence_threshold: 0.90
    patterns:
      - regex: '\b(\d{4}-\d{2}-\d{2})\b'
      - regex: '\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'

  - id: "obligations"
    description: "Extract contractual obligations"
    entity_type: "obligation"
    priority: 3
    confidence_threshold: 0.80

# Prompt guidance (expert advice for AI)
prompt_guidance: |
  When analyzing legal documents:

  1. IDENTIFICATION PHASE
     - Identify all parties before analyzing obligations
     - Look for defined terms (capitalized with quotes)
     - Note the governing law and jurisdiction

  2. EXTRACTION PHASE
     - Cross-reference obligations with party roles
     - Link deadlines to specific obligations
     - Identify conditional clauses

  3. QUALITY CHECKS
     - Flag ambiguous terms for human review
     - Note missing standard clauses
     - Highlight unusual provisions

# Metadata
metadata:
  author: "Jerry Framework"
  created: "2026-01-26"
  compliance: ["GDPR", "CCPA"]
  industry_standards: ["IACCM", "WorldCC"]
```

### 3.4 Hook Scripts (context-loader)

For complex context loading scenarios, a hook script can handle validation and transformation.

#### 3.4.1 Hook Integration Points

```
HOOK INTEGRATION IN SKILL LIFECYCLE
===================================

     Skill Activation             Context Loading              Agent Dispatch
     ─────────────────            ───────────────              ──────────────

User: /transcript --domain legal
         │
         ▼
┌─────────────────────┐
│  SessionStart Hook  │ ◄─── (Optional) Pre-validation
│  (if configured)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  SKILL.md Parsed    │
│  context_injection  │
│  section loaded     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│                    CONTEXT-LOADER HOOK                       │
│                    ──────────────────                        │
│                                                              │
│  Inputs:                                                     │
│  • domain: "legal"                                           │
│  • skill_path: "./skills/transcript/"                        │
│  • invocation_args: {...}                                    │
│                                                              │
│  Processing:                                                 │
│  1. Load contexts/{domain}.yaml                              │
│  2. Validate against JSON Schema                             │
│  3. Apply circuit breaker for external calls (if any)        │
│  4. Merge with SKILL.md defaults                             │
│                                                              │
│  Outputs:                                                    │
│  • context_payload: {...validated context...}                │
│  • validation_errors: [] or [{field, message}]               │
│  • load_time_ms: 42                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
           │
           │  Context injected into agent prompts
           ▼
┌─────────────────────┐
│  Agent Execution    │
│  ts-parser →        │
│  ts-extractor →     │
│  ts-formatter       │
└─────────────────────┘
```

#### 3.4.2 Hook Output Schema

```yaml
# Hook output format for context-loader
hookSpecificOutput:
  hookEventName: "ContextLoad"
  additionalContext: |
    <context-payload>
    domain: legal
    schema_version: 1.0.0
    entity_definitions:
      party: {...}
      obligation: {...}
    extraction_rules:
      - {id: parties, confidence: 0.85}
    prompt_guidance: |
      When analyzing legal documents...
    </context-payload>

  validation:
    is_valid: true
    errors: []
    warnings:
      - "Optional field 'metadata.compliance' is missing"

  performance:
    load_time_ms: 42
    cache_hit: false
    fallback_used: false
```

---

## 4. Injection Points Specification

### 4.1 Skill Invocation Injection

Context is injected when a skill is invoked.

#### 4.1.1 Invocation Syntax

```bash
# Explicit domain selection
/transcript --domain legal meeting.vtt

# With additional context arguments
/transcript --domain sales \
  --confidence 0.8 \
  --output-format json \
  call-recording.vtt

# Using environment variable
export TRANSCRIPT_DOMAIN=legal
/transcript meeting.vtt
```

#### 4.1.2 Invocation Context Schema

| Argument | Type | Description | Default |
|----------|------|-------------|---------|
| `--domain` | string | Domain identifier | From SKILL.md `default_domain` |
| `--confidence` | float | Confidence threshold | 0.7 |
| `--output-format` | enum | Output format (json/markdown/yaml) | markdown |
| `--context-file` | path | Additional context YAML file | None |
| `--no-cache` | flag | Disable context caching | false |

### 4.2 Agent Invocation Injection

When agents are invoked by the skill orchestrator, context flows through state.

#### 4.2.1 State Passing Schema

```yaml
# State passed between agents
agent_state:
  # Immutable context (same for all agents)
  context:
    domain: "legal"
    entity_definitions: {...}
    extraction_rules: [...]
    prompt_guidance: "..."

  # Mutable state (evolves through pipeline)
  pipeline_state:
    current_agent: "ts-extractor"
    previous_outputs:
      ts-parser:
        canonical_json_path: "./output/canonical.json"
        segment_count: 142

    # Context enrichments from previous agents
    enrichments:
      detected_speakers: ["Alice", "Bob"]
      detected_language: "en"
```

#### 4.2.2 Agent Context Injection Template

```markdown
## {{$agent_name}} CONTEXT

**Domain:** {{$domain}}
**Display Name:** {{$display_name}}

### Entity Definitions
{{$entity_definitions}}

### Extraction Rules
{{$extraction_rules}}

### Prompt Guidance
{{$prompt_guidance}}

### Previous Agent Outputs
{{$previous_outputs}}
```

### 4.3 Artifact Metadata Injection

Generated artifacts include context provenance metadata.

#### 4.3.1 Artifact Header Schema

```yaml
# Artifact header format
artifact_header:
  version: "1.0"
  generated_at: "2026-01-26T14:30:00Z"

  # Context provenance
  context_provenance:
    domain: "legal"
    schema_version: "1.0.0"
    context_sources:
      - type: "skill"
        path: "skills/transcript/SKILL.md"
      - type: "domain"
        path: "skills/transcript/contexts/legal.yaml"
      - type: "agent"
        path: "skills/transcript/agents/ts-extractor.md"

    validation:
      validated: true
      schema_path: "schemas/context-injection-schema.json"
      validation_time_ms: 12

    invocation:
      arguments:
        domain: "legal"
        confidence: 0.85
      timestamp: "2026-01-26T14:30:00Z"
```

---

## 5. Prompt Template Specification

### 5.1 Template Syntax ({{$variable}})

Template variables use the Semantic Kernel-compatible syntax: `{{$variable_name}}`.

#### 5.1.1 Syntax Rules

| Syntax | Description | Example |
|--------|-------------|---------|
| `{{$variable}}` | Simple substitution | `{{$domain}}` → `"legal"` |
| `{{$nested.path}}` | Nested object access | `{{$context.entities}}` |
| `{{$array[0]}}` | Array indexing | `{{$rules[0].id}}` → `"parties"` |
| `{{$variable\|default:value}}` | Default value | `{{$format\|default:json}}` |
| `{{$variable\|upper}}` | Transform: uppercase | `{{$domain\|upper}}` → `"LEGAL"` |
| `{{$variable\|lower}}` | Transform: lowercase | `{{$NAME\|lower}}` → `"alice"` |
| `{{$variable\|json}}` | Format as JSON | `{{$entities\|json}}` |
| `{{$variable\|yaml}}` | Format as YAML | `{{$rules\|yaml}}` |
| `{{$variable\|list}}` | Format as bullet list | `{{$attributes\|list}}` |

#### 5.1.2 Reserved Variables

These variables are always available in templates:

| Variable | Type | Description |
|----------|------|-------------|
| `$domain` | string | Current domain identifier |
| `$schema_version` | string | Schema version |
| `$entity_definitions` | object | All entity definitions |
| `$extraction_rules` | array | All extraction rules |
| `$prompt_guidance` | string | Domain prompt guidance |
| `$agent_name` | string | Current agent name |
| `$skill_name` | string | Parent skill name |
| `$timestamp` | string | Current ISO timestamp |

### 5.2 Variable Substitution Rules

#### 5.2.1 Substitution Order

```
TEMPLATE RESOLUTION ORDER
=========================

Template: "Analyze this {{$domain}} transcript using {{$rules|json}}"

Step 1: Parse template for {{$...}} patterns
        Found: [$domain, $rules]

Step 2: Resolve each variable from context
        $domain → lookup in context.domain → "legal"
        $rules  → lookup in context.extraction_rules → [...]

Step 3: Apply transforms
        $rules|json → JSON.stringify([...]) → "[{...}]"

Step 4: Substitute into template
        "Analyze this legal transcript using [{...}]"

Step 5: Validate output length
        IF > token_limit THEN truncate/summarize
```

#### 5.2.2 Missing Variable Handling

| Scenario | Behavior | Example |
|----------|----------|---------|
| Variable missing, no default | Error | `{{$unknown}}` → ValidationError |
| Variable missing, has default | Use default | `{{$format\|default:json}}` → `"json"` |
| Variable null | Treat as empty string | `{{$optional}}` → `""` |
| Variable undefined in nested path | Error | `{{$a.b.c}}` where b missing → Error |

### 5.3 Conditional Logic

Template conditionals allow optional sections.

#### 5.3.1 Conditional Syntax

```
{{#if $variable}}
  Content when variable is truthy
{{/if}}

{{#if $variable}}
  Content when true
{{#else}}
  Content when false
{{/if}}

{{#unless $variable}}
  Content when variable is falsy
{{/unless}}

{{#each $array as $item}}
  Process {{$item}}
{{/each}}
```

#### 5.3.2 Conditional Example

```markdown
## Extraction Context

Domain: {{$domain}}

{{#if $prompt_guidance}}
### Expert Guidance
{{$prompt_guidance}}
{{/if}}

### Entity Types to Extract
{{#each $entity_definitions as $entity}}
- **{{$entity.name}}**: {{$entity.description}}
{{/each}}

{{#unless $extraction_rules}}
WARNING: No extraction rules defined for this domain.
{{/unless}}
```

---

## 6. Security Specification

### 6.1 Input Validation

All context inputs MUST be validated to prevent injection attacks.

#### 6.1.1 Validation Rules

| Input Type | Validation | Rationale |
|------------|------------|-----------|
| Domain identifier | Alphanumeric + hyphen only | Prevent path traversal |
| File paths | Canonicalize and check within allowed dirs | Prevent directory escape |
| YAML content | Parse with safe loader, no code execution | Prevent YAML bombs |
| Template variables | Whitelist allowed characters | Prevent template injection |
| JSON Schema | Validate against meta-schema | Prevent schema injection |

#### 6.1.2 Validation Diagram

```
INPUT VALIDATION CHAIN
======================

User Input                                Validated Input
──────────                                ───────────────

--domain "../../etc/passwd"
         │
         ▼
┌─────────────────────┐
│ STAGE 1: Sanitize   │
│ ─────────────────── │
│ Strip path chars    │
│ Lowercase           │
│ Max length check    │
└──────────┬──────────┘
         │
         ▼
┌─────────────────────┐
│ STAGE 2: Validate   │
│ ─────────────────── │
│ Pattern: ^[a-z-]+$  │
│ Length: <= 50       │
│ Whitelist: domains[]│
└──────────┬──────────┘
         │
         ▼ PASS or REJECT
┌─────────────────────┐
│ STAGE 3: Resolve    │
│ ─────────────────── │
│ Map to real path    │
│ Check file exists   │
│ Verify permissions  │
└──────────┬──────────┘
         │
         ▼
    "legal" (safe)
```

### 6.2 Sanitization Rules

| Data Type | Sanitization | Example |
|-----------|--------------|---------|
| String | HTML encode, strip control chars | `<script>` → `&lt;script&gt;` |
| Path | Resolve, check prefix | `../secret` → REJECT |
| Integer | Range check | `-1` → REJECT if min=0 |
| Float | Range check, precision limit | `0.99999999` → `1.0` |
| Array | Max length, element validation | `[1,2,...1000]` → REJECT if max=100 |

### 6.3 Access Control

#### 6.3.1 Context File Permissions

```
CONTEXT FILE ACCESS CONTROL
===========================

Allowed Paths:
├── skills/{skill_name}/contexts/*.yaml  ← Domain schemas
├── skills/{skill_name}/SKILL.md         ← Skill definition
├── skills/{skill_name}/agents/*.md      ← Agent definitions
└── ./.context/session/*.yaml            ← Session context

Denied Paths:
├── /etc/*                               ← System files
├── ~/.ssh/*                             ← SSH keys
├── ~/.aws/*                             ← Cloud credentials
├── ../*                                 ← Parent directory
└── ${HOME}/.env                         ← Environment secrets
```

#### 6.3.2 Access Control Matrix

| Actor | Read Context | Write Context | Modify Schema |
|-------|--------------|---------------|---------------|
| Skill | Yes | No | No |
| Agent | Yes | No | No |
| Hook | Yes | Yes (session only) | No |
| User | Yes | Yes | Yes (with approval) |

---

## 7. Error Handling Specification

### 7.1 Error Codes

| Code | Category | Description | Recovery |
|------|----------|-------------|----------|
| `CI-001` | Validation | Schema validation failed | Fix schema and retry |
| `CI-002` | Validation | Invalid domain identifier | Use valid domain |
| `CI-003` | Loading | Context file not found | Create file or use default |
| `CI-004` | Loading | YAML parse error | Fix YAML syntax |
| `CI-005` | Loading | File read permission denied | Check permissions |
| `CI-006` | Size | Context exceeds size limit | Reduce context size |
| `CI-007` | Template | Unknown template variable | Define variable or use default |
| `CI-008` | Template | Template syntax error | Fix template syntax |
| `CI-009` | External | MCP server unavailable | Use fallback context |
| `CI-010` | External | Circuit breaker open | Wait for reset |

### 7.2 Graceful Degradation

When errors occur, the system degrades gracefully rather than failing completely.

```
GRACEFUL DEGRADATION CHAIN
==========================

Primary Source Failed              Fallback Chain              Result
───────────────────────            ──────────────              ──────

MCP Server Down (CI-009)
         │
         ▼
┌─────────────────────┐
│ TRY: Cached context │───► HIT ───► Use cached
└──────────┬──────────┘
         │ MISS
         ▼
┌─────────────────────┐
│ TRY: Static context │───► OK ────► Use static
└──────────┬──────────┘
         │ FAIL
         ▼
┌─────────────────────┐
│ TRY: Default domain │───► OK ────► Use general.yaml
└──────────┬──────────┘
         │ FAIL
         ▼
┌─────────────────────┐
│ FINAL: Empty context│───► WARN ──► Proceed with warning
└─────────────────────┘

STATUS CODES:
• SUCCESS   = Primary source loaded
• PARTIAL   = Fallback used successfully
• FALLBACK  = Default context used
• DEGRADED  = Empty context, limited functionality
```

### 7.3 Recovery Procedures

#### 7.3.1 Automatic Recovery

| Error | Auto-Recovery | Max Retries | Backoff |
|-------|---------------|-------------|---------|
| CI-003 (File not found) | Create from template | 1 | N/A |
| CI-009 (MCP unavailable) | Retry with backoff | 3 | Exponential |
| CI-010 (Circuit open) | Wait for half-open | Auto | 30 seconds |

#### 7.3.2 Manual Recovery

| Error | Recovery Steps |
|-------|----------------|
| CI-001 (Schema invalid) | 1. Review validation errors 2. Fix schema 3. Re-validate 4. Retry |
| CI-004 (YAML parse error) | 1. Identify line number 2. Fix syntax 3. Validate YAML 4. Retry |
| CI-006 (Size exceeded) | 1. Identify large fields 2. Compress or split 3. Re-submit |

---

## 8. JSON Schema Reference

The formal JSON Schema for context payloads is defined in:

**Location:** `schemas/context-injection-schema.json`

### 8.1 Schema Overview

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://jerry.framework/schemas/context-injection/1.0.0",
  "title": "Context Injection Payload",
  "description": "Schema for validating context injection payloads in Claude Code Skills"
}
```

### 8.2 Type Definitions

The schema defines these custom types in `$defs`:

| Type | Description |
|------|-------------|
| `DomainIdentifier` | Validated domain string |
| `SemanticVersion` | X.Y.Z version format |
| `EntityDefinition` | Entity type definition |
| `EntityAttribute` | Single entity attribute |
| `ExtractionRule` | Rule for extracting entities |
| `PromptGuidance` | Expert guidance text |
| `ContextMetadata` | Additional context metadata |

### 8.3 Schema Validation

To validate a context payload:

```bash
# Using ajv-cli
ajv validate -s schemas/context-injection-schema.json -d context-payload.json

# Using Python jsonschema
python -c "
import json, jsonschema
schema = json.load(open('schemas/context-injection-schema.json'))
payload = json.load(open('context-payload.json'))
jsonschema.validate(payload, schema)
print('Valid!')
"
```

---

## Appendix A: Requirements Traceability

### A.1 Forward Traceability: Requirements → Specification

| Requirement | Spec Section | Implementation |
|-------------|--------------|----------------|
| REQ-CI-F-001 | 3.3 | contexts/*.yaml domain files |
| REQ-CI-F-002 | 3.1 | SKILL.md context_injection section |
| REQ-CI-F-003 | 3.2 | AGENT.md context sections |
| REQ-CI-F-004 | 4.1 | --domain CLI parameter |
| REQ-CI-F-005 | 3.4, 4 | Loading lifecycle, injection points |
| REQ-CI-F-006 | 2.3, 8 | JSON Schema validation |
| REQ-CI-F-007 | 3.3 | Pre-built domain templates |
| REQ-CI-F-008 | 5 | Template variable syntax |
| REQ-CI-F-009 | 3.2.2 | Context merge priority |
| REQ-CI-F-010 | 7 | Error handling specification |
| REQ-CI-F-011 | 7.2 | Graceful degradation chain |
| REQ-CI-P-001 | 3.4.2 | Hook performance tracking |
| REQ-CI-P-002 | 2.3 | 50MB size validation |
| REQ-CI-P-003 | 7.3 | Circuit breaker pattern |
| REQ-CI-I-001 | 3.1, 3.2, 3.3 | Skill construct integration |
| REQ-CI-I-002 | 2.2, 4 | Payload structure specification |
| REQ-CI-C-001 | 3.3 | Model-agnostic YAML format |
| REQ-CI-C-002 | 3, 4 | Jerry framework integration |

### A.2 Coverage Summary

```
REQUIREMENTS COVERAGE MATRIX
============================

Category        │ Total │ Covered │ Coverage
────────────────┼───────┼─────────┼──────────
Functional      │  11   │   11    │   100%
Performance     │   4   │    4    │   100%
Interface       │   3   │    3    │   100%
Constraint      │   2   │    2    │   100%
────────────────┼───────┼─────────┼──────────
TOTAL           │  20   │   20    │   100%
```

---

## Appendix B: TDD Pattern Mapping

### B.1 Complete Mapping Table

| TDD Concept | Python Pattern | Claude Code Skill Construct | Section |
|-------------|----------------|----------------------------|---------|
| `IContextProvider` | Protocol class | SKILL.md `context_injection` section | 3.1 |
| `load_static_context()` | Method | `contexts/{domain}.yaml` file loading | 3.3 |
| `load_dynamic_context()` | Method | Invocation arguments + MCP tool calls | 4.1 |
| `resolve_template()` | Method | `{{$variable}}` substitution engine | 5 |
| `validate_context()` | Method | JSON Schema validation in hook | 2.3, 8 |
| `merge_contexts()` | Method | Context merge priority rules | 3.2.2 |
| `ContextPayload` | Dataclass | Skill invocation context object | 2 |
| `Context` | Dataclass | Domain schema YAML structure | 3.3.2 |
| `ContextResult` | Dataclass | Hook output schema | 3.4.2 |
| `ValidationResult` | Dataclass | Validation errors array | 2.3, 7.1 |
| `ValidationError` | Dataclass | Individual error object | 7.1 |
| `ContextLoadStatus` | Enum | Status codes in error handling | 7.1 |
| `CircuitBreaker` | Class | Hook timeout/retry logic | 7.3 |
| `LoadContextCommand` | Command | Skill invocation with arguments | 4.1 |
| `LoadContextCommandHandler` | Handler | SKILL.md orchestration | 3.1.2 |

### B.2 Why This Mapping Works

```
PATTERN-TO-CONSTRUCT RATIONALE (L2: Architect)
==============================================

The TDD uses Python patterns because they:
1. Define clear contracts (Protocol classes)
2. Are widely understood by engineers
3. Enable automated testing

Claude Code Skills implement these patterns through:
1. SKILL.md - Defines the "interface" contract
2. AGENT.md - Implements "persona context"
3. contexts/*.yaml - Provides "static data"
4. Hooks - Handles "runtime behavior"

This mapping preserves:
✓ Single Responsibility (each construct has one purpose)
✓ Dependency Inversion (skill depends on abstractions)
✓ Open/Closed (extend via new domains, not code changes)
✓ Interface Segregation (minimal coupling between constructs)
```

---

## Appendix C: Verification Approach

### C.1 Verification Methods

| Requirement | Method | Approach |
|-------------|--------|----------|
| REQ-CI-F-001 | Test | Load sample YAML, verify context object fields |
| REQ-CI-F-002 | Test | Parse SKILL.md, extract context_injection section |
| REQ-CI-F-003 | Test | Load AGENT.md, verify persona context merged |
| REQ-CI-F-004 | Test | CLI `--domain legal` loads legal.yaml |
| REQ-CI-F-005 | Test | State machine transitions in correct order |
| REQ-CI-F-006 | Test | Valid/invalid payloads against JSON Schema |
| REQ-CI-F-007 | Inspection | Verify 3 domain templates exist |
| REQ-CI-F-008 | Test | `{{$domain}}` resolves to "legal" |
| REQ-CI-F-009 | Test | Merge 3 contexts, verify priority |
| REQ-CI-F-010 | Test | Adapter error propagates, no silent fail |
| REQ-CI-F-011 | Test | MCP unavailable triggers fallback |
| REQ-CI-P-001 | Test | Measure static context load time |
| REQ-CI-P-002 | Test | 51MB context rejected |
| REQ-CI-P-003 | Test | 5 failures opens circuit |
| REQ-CI-I-001 | Analysis | Architecture review of constructs |
| REQ-CI-I-002 | Analysis | Interface review of payload structure |
| REQ-CI-C-001 | Analysis | No provider-specific features in schemas |
| REQ-CI-C-002 | Demo | End-to-end skill invocation with context |

### C.2 Test Scenarios

```
TEST SCENARIO MATRIX
====================

Scenario Category │ Count │ Examples
──────────────────┼───────┼──────────────────────────────────────
Happy Path        │   8   │ Load legal.yaml successfully
                  │       │ Template resolves all variables
                  │       │ Context merges correctly
──────────────────┼───────┼──────────────────────────────────────
Negative          │   6   │ Invalid domain identifier rejected
                  │       │ Schema validation fails for invalid
                  │       │ Size limit exceeded
──────────────────┼───────┼──────────────────────────────────────
Edge Case         │   4   │ Empty context gracefully handled
                  │       │ Maximum nesting depth
                  │       │ Unicode in domain names
──────────────────┼───────┼──────────────────────────────────────
Integration       │   4   │ SKILL.md + AGENT.md + domain.yaml
                  │       │ Full pipeline context flow
──────────────────┼───────┼──────────────────────────────────────
TOTAL             │  22   │
```

---

## History

| Date | Version | Author | Notes |
|------|---------|--------|-------|
| 2026-01-26 | 1.0.0 | ps-architect | Initial specification for Claude Code Skills implementation |

---

*Document ID: SPEC-CI-001*
*Task: TASK-035*
*Phase: 2 (Design Phase)*
*NASA SE Process: 4 (Technical Solution Definition)*
*Quality Target: >= 0.90*
