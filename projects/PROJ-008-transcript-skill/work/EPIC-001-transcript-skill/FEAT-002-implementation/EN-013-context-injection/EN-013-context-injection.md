# EN-013: Context Injection Implementation

<!--
TEMPLATE: Enabler
VERSION: 2.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
REVISED: 2026-01-26 per DISC-001 alignment analysis
NOTE: Implements YAML-only approach per SPEC-context-injection.md Section 3
-->

> **Type:** enabler
> **Status:** gate-ready
> **Priority:** medium
> **Impact:** high
> **Created:** 2026-01-26T00:00:00Z
> **Revised:** 2026-01-26T17:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** FEAT-002
> **Owner:** Claude
> **Target Sprint:** Sprint 4
> **Effort Points:** 5
> **Gate:** GATE-5 (Core Implementation Review)

---

## Summary

Implement the **context injection mechanism** designed in EN-006 using **Claude Code Skills constructs only** (SKILL.md, AGENT.md, contexts/*.yaml). No Python code is generated - context injection is achieved through YAML configuration and template variable resolution.

**Implements:** [SPEC-context-injection.md Section 3](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md#3-claude-code-skill-constructs)

**Technical Justification:**
- DEC-002: TDD Python is conceptual - Claude Code Skills implement via YAML
- SPEC Section 3 maps Python patterns to SKILL.md, AGENT.md, contexts/*.yaml
- Enables domain-specific agent specialization without code duplication
- Template variables (`{{$variable}}`) provide runtime customization

---

## Design Reference (L0/L1/L2)

### L0: The Briefcase Analogy

Context injection is like giving a consultant a **specialized briefcase** before a job:

```
THE CONSULTANT'S BRIEFCASE (Context Injection)
==============================================

        CONSULTANT                           SPECIALIZED BRIEFCASE
        (ts-extractor)                       (Injected Context)
            │                                     │
            │                                     │
            ▼                                     ▼
    ┌───────────────┐                  ┌────────────────────────────┐
    │               │                  │    DOMAIN: "legal"          │
    │   "I extract  │                  │    ────────────────         │
    │   entities    │ ◄──── receives ──│    What to look for:        │
    │   from text"  │                  │    - Contract clauses       │
    │               │                  │    - Legal parties          │
    │               │                  │    - Obligations            │
    │               │                  │                             │
    │   (Same       │                  │    How to find them:        │
    │    skill)     │                  │    - Pattern: "hereby..."   │
    │               │                  │    - Confidence: 0.85       │
    └───────────────┘                  └────────────────────────────┘

    "I'm the same consultant, but my briefcase tells me this is a
     LEGAL document, so I look for legal entities, not sales leads."
```

### L1: Component Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Context Injection Implementation                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  IMPLEMENTATION: YAML configuration files (NO Python code)                   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    SKILL.md Context Section                          │   │
│  │ ────────────────────────────────────────────────────────────────────│   │
│  │ context_injection:                                                   │   │
│  │   default_domain: "general"                                          │   │
│  │   domains: [legal, sales, engineering, general]                      │   │
│  │   context_path: "./contexts/"                                        │   │
│  │   template_variables:                                                │   │
│  │     - { name: domain, source: invocation.domain }                    │   │
│  │     - { name: extraction_rules, source: context.extraction_rules }   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│                                      ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    contexts/{domain}.yaml                            │   │
│  │ ────────────────────────────────────────────────────────────────────│   │
│  │ schema_version: "1.0.0"                                              │   │
│  │ domain: "legal"                                                      │   │
│  │ entity_definitions: { party: {...}, obligation: {...} }              │   │
│  │ extraction_rules: [ { id: "parties", confidence: 0.85 } ]            │   │
│  │ prompt_guidance: "When analyzing legal documents..."                  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│                                      ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    AGENT.md Context Section                          │   │
│  │ ────────────────────────────────────────────────────────────────────│   │
│  │ context:                                                             │   │
│  │   persona:                                                           │   │
│  │     role: "Entity Extraction Specialist"                             │   │
│  │     expertise: ["NER", "Confidence scoring"]                         │   │
│  │   domain_extensions:                                                 │   │
│  │     legal: { additional_entities: ["contract_clause"] }              │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│                                      ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Template Variable Resolution                      │   │
│  │ ────────────────────────────────────────────────────────────────────│   │
│  │ "Extract {{$entity_types}} from text using {{$extraction_rules}}"    │   │
│  │                          │                         │                 │   │
│  │                          ▼                         ▼                 │   │
│  │               ["party", "obligation"]     [{id: "parties"...}]       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  OUTPUT: Context-enriched prompts at agent invocation time                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### L2: Strategic Considerations

- **DEC-002 Compliance:** No Python code - YAML configuration implements conceptual TDD patterns
- **SPEC Section 3 Mapping:**
  - `IContextProvider` → SKILL.md `context_injection` section
  - `load_static_context()` → contexts/{domain}.yaml files
  - `load_dynamic_context()` → Invocation arguments + MCP tools
  - `resolve_template()` → `{{$variable}}` syntax in prompts
- **Context Merge Priority:** SKILL.md → domain.yaml → AGENT.md → invocation args
- **Validation:** JSON Schema validation at load time (REQ-CI-F-009)

---

## Benefit Hypothesis

**We believe that** implementing context injection via Claude Code Skills constructs per SPEC Section 3

**Will result in** domain-specific agent specialization without code duplication

**We will know we have succeeded when:**
- SKILL.md `context_injection` section configured correctly
- contexts/*.yaml files validate against JSON Schema
- AGENT.md persona context merges with domain context
- Template variables (`{{$variable}}`) resolve correctly
- Context payload < 50MB (REQ-CI-P-002)
- Loading time < 500ms (REQ-CI-P-001)
- Human approval received at GATE-5

---

## Acceptance Criteria

### Definition of Done

- [ ] SKILL.md `context_injection` section implemented (REQ-CI-F-002)
- [ ] contexts/*.yaml domain schema files created (REQ-CI-F-001)
- [ ] AGENT.md persona context sections added (REQ-CI-F-003)
- [ ] Template variable resolution working (REQ-CI-F-004)
- [ ] Context merge order verified (SKILL → domain → AGENT → args)
- [ ] JSON Schema validation functional (REQ-CI-F-009)
- [ ] ps-critic review passed
- [ ] Human approval at GATE-5

### Technical Criteria (from SPEC-context-injection.md)

| # | Criterion | SPEC Section | Verified |
|---|-----------|--------------|----------|
| AC-1 | SKILL.md context_injection section present | 3.1 | [ ] |
| AC-2 | At least one domain.yaml file created | 3.3 | [ ] |
| AC-3 | AGENT.md has context.persona section | 3.2 | [ ] |
| AC-4 | Template variables resolve to values | 3.4 | [ ] |
| AC-5 | Context merge order correct | 3.2.2 | [ ] |
| AC-6 | Validation errors are descriptive | 2.3 | [ ] |
| AC-7 | Works with ts-extractor agent | 3.2 | [ ] |
| AC-8 | Performance < 500ms load time | REQ-CI-P-001 | [ ] |

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner | Effort | Blocked By |
|----|-------|--------|-------|--------|------------|
| [TASK-120](./TASK-120-skill-context-injection.md) | Create SKILL.md context_injection section | **DONE** | Claude | 2 | EN-006 |
| [TASK-121](./TASK-121-general-domain-schema.md) | Create general.yaml domain schema | **DONE** | Claude | 1 | TASK-120 |
| [TASK-122](./TASK-122-transcript-domain-schema.md) | Create transcript.yaml domain schema | **DONE** | Claude | 1 | TASK-120 |
| [TASK-123](./TASK-123-agent-context-sections.md) | Add AGENT.md context sections to ts-* agents | **DONE** | Claude | 2 | TASK-121 |
| [TASK-124](./TASK-124-json-schema-validation.md) | Create JSON Schema for context validation | **DONE** | Claude | 1 | TASK-120 |
| [TASK-125](./TASK-125-context-validation.md) | Create validation and test scenarios | **DONE** | Claude | 1 | TASK-123, TASK-124 |

**NOTE:** Task IDs start at TASK-120 to avoid conflicts with EN-007 (TASK-101-105), EN-008 (TASK-106-112), and EN-009 (TASK-113-119).
**Task files created:** 2026-01-26 with detailed acceptance criteria and evidence requirements.

---

## Implementation Artifacts

### Artifact 1: SKILL.md Context Section

**File:** `skills/transcript/SKILL.md`

```yaml
---
name: transcript
description: Parse and extract from transcripts with domain-specific context
version: "1.0.0"
allowed-tools: Read, Write, Glob, Task

# CONTEXT INJECTION (implements REQ-CI-F-002)
context_injection:
  # Default domain when none specified
  default_domain: "general"

  # Available domain schemas
  domains:
    - general      # Default: no domain-specific entities
    - transcript   # Transcript-specific: speakers, topics, action items

  # Context files location
  context_path: "./contexts/"

  # Template variables available to agents
  template_variables:
    - name: domain
      source: invocation.domain
      default: "general"
    - name: entity_definitions
      source: context.entity_definitions
      format: yaml
    - name: extraction_rules
      source: context.extraction_rules
      format: list
    - name: prompt_guidance
      source: context.prompt_guidance
      format: text

activation-keywords:
  - "transcript"
  - "/transcript"
---
```

### Artifact 2: Domain Schema (contexts/transcript.yaml)

**File:** `skills/transcript/contexts/transcript.yaml`

```yaml
# Domain Schema for Transcript Analysis
# Implements: REQ-CI-F-001, REQ-CI-F-007
schema_version: "1.0.0"
domain: "transcript"
display_name: "Transcript Analysis"

# Entity definitions (what to extract)
entity_definitions:
  action_item:
    description: "Task or commitment made during conversation"
    attributes:
      - name: "text"
        type: "string"
        required: true
      - name: "assignee"
        type: "string"
      - name: "due_date"
        type: "date"
      - name: "confidence"
        type: "float"
    extraction_patterns:
      - "{{assignee}} will {{text}}"
      - "{{assignee}}, can you {{text}}"
      - "action item: {{text}}"

  decision:
    description: "Decision made during conversation"
    attributes:
      - name: "text"
        type: "string"
        required: true
      - name: "decided_by"
        type: "string"
      - name: "rationale"
        type: "string"
    extraction_patterns:
      - "we've decided to {{text}}"
      - "the decision is {{text}}"
      - "let's go with {{text}}"

  question:
    description: "Question raised during conversation"
    attributes:
      - name: "text"
        type: "string"
        required: true
      - name: "asked_by"
        type: "string"
      - name: "answered"
        type: "boolean"

  speaker:
    description: "Person speaking in the transcript"
    attributes:
      - name: "name"
        type: "string"
        required: true
      - name: "role"
        type: "string"
      - name: "segment_count"
        type: "integer"

# Extraction rules (how to find entities)
extraction_rules:
  - id: "action_items"
    entity_type: "action_item"
    confidence_threshold: 0.7
    priority: 1
  - id: "decisions"
    entity_type: "decision"
    confidence_threshold: 0.8
    priority: 2
  - id: "questions"
    entity_type: "question"
    confidence_threshold: 0.75
    priority: 3

# Expert guidance for agent prompts
prompt_guidance: |
  When analyzing transcripts for entity extraction:

  1. **Action Items**: Look for commitments with specific owners and deadlines.
     Phrases like "will do", "by Friday", "I'll handle" indicate action items.

  2. **Decisions**: Identify explicit decisions with consensus language.
     Phrases like "we've decided", "let's go with", "agreed" indicate decisions.

  3. **Questions**: Track open questions and whether they were answered.
     Mark as answered if a response follows within the transcript.

  4. **Confidence Scoring**:
     - 0.9+ : Explicit indicator present ("action item:", "decision:")
     - 0.7-0.9: Strong implicit signal with context
     - 0.5-0.7: Ambiguous, flag for human review
     - <0.5: Do not extract
```

### Artifact 3: AGENT.md Context Section

**File:** `skills/transcript/agents/ts-extractor.md` (partial)

```yaml
---
name: ts-extractor
version: "1.0.0"
description: "Extract semantic entities from transcripts"
model: "sonnet"

# AGENT-SPECIFIC CONTEXT (implements REQ-CI-F-003)
context:
  # Persona context merged with skill context
  persona:
    role: "Entity Extraction Specialist"
    expertise:
      - "Named Entity Recognition"
      - "Confidence scoring with tiered extraction"
      - "Citation generation for anti-hallucination"
    behavior:
      - "Always cite source segment for each extraction"
      - "Use tiered extraction: Rule → ML patterns → LLM inference"
      - "Apply PAT-004: Citation-Required for all entities"

  # Template variables specific to this agent
  template_variables:
    - name: confidence_threshold
      default: 0.7
      type: float
    - name: max_extractions
      default: 100
      type: integer
    - name: citation_required
      default: true
      type: boolean
---
```

---

## Context Merge Flow

```
CONTEXT MERGE ORDER (per SPEC Section 3.2.2)
============================================

                SKILL.md                 domain.yaml              AGENT.md
               context_injection          (loaded)                 context
                     │                       │                        │
                     │                       │                        │
      ┌──────────────▼──────────────────────▼────────────────────────▼──────────────┐
      │                                                                              │
      │  1. SKILL.md default_domain: "general"                                       │
      │                    │                                                         │
      │                    ▼                                                         │
      │  2. contexts/transcript.yaml loaded → entity_definitions, extraction_rules   │
      │                    │                                                         │
      │                    ▼                                                         │
      │  3. ts-extractor.md context.persona → role, expertise                        │
      │                    │                                                         │
      │                    ▼                                                         │
      │  4. Invocation args: --domain transcript, --confidence 0.8                   │
      │                    │                                                         │
      │                    ▼                                                         │
      │  ┌────────────────────────────────────────────────┐                         │
      │  │              MERGED CONTEXT                     │                         │
      │  │  domain: "transcript"                           │                         │
      │  │  entity_definitions: { action_item:..., ... }   │                         │
      │  │  extraction_rules: [ {id: "action_items"...} ]  │                         │
      │  │  persona.role: "Entity Extraction Specialist"   │                         │
      │  │  confidence_threshold: 0.8 (from invocation)    │                         │
      │  └────────────────────────────────────────────────┘                         │
      │                                                                              │
      └──────────────────────────────────────────────────────────────────────────────┘
```

---

## Template Variable Resolution

```
TEMPLATE VARIABLE SYNTAX: {{$variable}}
=======================================

BEFORE RESOLUTION (in agent prompt):
────────────────────────────────────
"You are an {{$persona.role}}.

Extract the following entity types from the transcript:
{{$entity_definitions}}

Apply these extraction rules:
{{$extraction_rules}}

{{$prompt_guidance}}"


AFTER RESOLUTION (at invocation):
─────────────────────────────────
"You are an Entity Extraction Specialist.

Extract the following entity types from the transcript:
- action_item: Task or commitment made during conversation
- decision: Decision made during conversation
- question: Question raised during conversation
- speaker: Person speaking in the transcript

Apply these extraction rules:
- action_items (confidence >= 0.7, priority 1)
- decisions (confidence >= 0.8, priority 2)
- questions (confidence >= 0.75, priority 3)

When analyzing transcripts for entity extraction:
1. Action Items: Look for commitments with specific owners...
2. Decisions: Identify explicit decisions with consensus language...
..."
```

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002: Implementation](../FEAT-002-implementation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Implements | [SPEC-context-injection.md Section 3](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md) | Claude Code Skills implementation |
| Implements | [TDD-context-injection.md](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/design/TDD-context-injection.md) | Conceptual design (Python → YAML mapping) |
| Depends On | EN-006 | Design specification (FEAT-001) |
| Depends On | EN-009 | ts-formatter needs context for output |
| References | DEC-002 | Implementation Approach Decision |
| Blocks | EN-014 | Domain Context Files depend on injection mechanism |

### Discovery Reference

- [DISC-001](../FEAT-002--DISC-001-enabler-alignment-analysis.md) - Alignment analysis (YAML-only correction)

---

## YAML-Only Implementation Note

**CRITICAL (DEC-002):** This enabler produces **YAML configuration files only**:
- `SKILL.md` context_injection section
- `contexts/*.yaml` domain schema files
- `AGENT.md` context sections
- `schemas/context-injection-schema.json` (validation)

**NO Python or executable code is created.** The TDD-context-injection.md Python code is conceptual - it describes patterns that Claude Code Skills implement through native YAML constructs.

See [SPEC-context-injection.md Section 3](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md#3-claude-code-skill-constructs) for the complete TDD-to-SKILL mapping.

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | pending | Enabler created (with Python pseudocode) |
| 2026-01-26 | Claude | revised | MAJOR rewrite per DISC-001: YAML-only implementation per SPEC Section 3; tasks renumbered to TASK-120+ |
| 2026-01-28 | Claude | gate-ready | All 6 tasks DONE. Created: SKILL.md context_injection, contexts/general.yaml, contexts/transcript.yaml, schemas/context-domain-schema.json, agent context sections (ts-parser, ts-extractor, ts-formatter), context-injection-tests.yaml (18 test cases). Ready for ps-critic/nse-qa reviews. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (tagged Technical) |
| **SAFe** | Enabler Story |
| **JIRA** | Task |
