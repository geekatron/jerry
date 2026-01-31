# Domain Context Specifications

<!--
DOCUMENT: Domain Context Specifications Index
VERSION: 1.0.0
TASK: TASK-038 (Phase 3)
STATUS: COMPLETE
-->

---

> **DISCLAIMER:** This guidance is AI-generated based on NASA Systems Engineering
> standards. It is advisory only and does not constitute official NASA guidance.
> All SE decisions require human review and professional engineering judgment.

---

## Overview

This directory contains domain-specific context injection specifications for transcript analysis use cases. Each domain defines the entities, extraction rules, prompt templates, and validation criteria for analyzing meeting transcripts from that professional domain.

## Purpose

These specifications serve as **design artifacts** that define:

1. **WHAT** entities to extract from transcripts
2. **WHAT** patterns indicate those entities
3. **HOW** to instruct AI agents for extraction
4. **HOW** to validate extraction correctness

> **IMPORTANT:** These are design specifications only. The actual implementation
> (creating `contexts/{domain}.yaml` files, test transcripts, validation execution)
> is deferred to FEAT-002. See [DISC-001](../../EN-006--DISC-001-feat002-implementation-scope.md).

## Available Domains

| # | Domain | Target Users | Key Use Cases |
|---|--------|--------------|---------------|
| 1 | [Software Engineering](./01-software-engineering/) | Engineers, Tech Leads | Standups, sprint planning, code reviews |
| 2 | [Software Architecture](./02-software-architecture/) | Architects, Principal Engineers | Architecture reviews, ADR discussions |
| 3 | [Product Management](./03-product-management/) | PMs, Product Owners | Roadmap planning, feature prioritization |
| 4 | [User Experience](./04-user-experience/) | UX Researchers, Designers | Research interviews, usability testing |
| 5 | [Cloud Engineering](./05-cloud-engineering/) | SREs, DevOps Engineers | Incident post-mortems, capacity planning |
| 6 | [Security Engineering](./06-security-engineering/) | Security Engineers | Security audits, threat modeling |

## Domain Selection Guide

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DOMAIN SELECTION FLOWCHART                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  What type of meeting are you analyzing?                                     │
│                                                                              │
│  ┌─────────────────────────┐                                                │
│  │ Daily standup?          │─────────────────────► software-engineering     │
│  │ Sprint planning?        │                                                │
│  │ Code review?            │                                                │
│  └─────────────────────────┘                                                │
│                                                                              │
│  ┌─────────────────────────┐                                                │
│  │ Architecture review?    │─────────────────────► software-architecture    │
│  │ ADR discussion?         │                                                │
│  │ Design session?         │                                                │
│  └─────────────────────────┘                                                │
│                                                                              │
│  ┌─────────────────────────┐                                                │
│  │ Product strategy?       │─────────────────────► product-management       │
│  │ Roadmap planning?       │                                                │
│  │ Stakeholder meeting?    │                                                │
│  └─────────────────────────┘                                                │
│                                                                              │
│  ┌─────────────────────────┐                                                │
│  │ User interview?         │─────────────────────► user-experience          │
│  │ Usability testing?      │                                                │
│  │ Design critique?        │                                                │
│  └─────────────────────────┘                                                │
│                                                                              │
│  ┌─────────────────────────┐                                                │
│  │ Incident post-mortem?   │─────────────────────► cloud-engineering        │
│  │ Capacity planning?      │                                                │
│  │ Infrastructure review?  │                                                │
│  └─────────────────────────┘                                                │
│                                                                              │
│  ┌─────────────────────────┐                                                │
│  │ Security audit?         │─────────────────────► security-engineering     │
│  │ Threat modeling?        │                                                │
│  │ Compliance review?      │                                                │
│  └─────────────────────────┘                                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Directory Structure

Each domain follows a consistent structure:

```
{NN}-{domain-name}/
├── SPEC-{domain-name}.md       # Domain specification document
├── entities/
│   └── entity-definitions.yaml # Entity schema (design)
├── extraction/
│   └── extraction-rules.yaml   # Extraction patterns (design)
├── prompts/
│   └── prompt-templates.md     # Prompt designs
└── validation/
    └── acceptance-criteria.md  # Domain-specific validation
```

## Schema Reference

All domain specifications must conform to the [DOMAIN-SCHEMA.json](./DOMAIN-SCHEMA.json) JSON Schema.

### Entity Definition Schema

```yaml
domain: string              # Domain identifier (e.g., "software-engineering")
version: string             # Semantic version (e.g., "1.0.0")
entities:
  {entity_name}:
    description: string     # What this entity represents
    attributes:
      - {attr_name}: string # Attribute description
```

### Extraction Rules Schema

```yaml
extraction_rules:
  {entity_type}_patterns:
    - pattern: string       # Pattern with {variable} placeholders
    - pattern: string
```

### Prompt Template Schema

```markdown
## {Domain} Transcript Analysis

You are analyzing a {{$transcript_type}} transcript from a {context}.

### Context
- Variable: {{$variable}}

### Extraction Instructions
1. **Entity Type**: Description
   - Extract: attributes
   - Look for: patterns

### Output Format
{{$output_schema}}
```

## Cross-Domain Requirements

| Requirement | Description |
|-------------|-------------|
| **XD-001** | All domains use consistent entity schema structure |
| **XD-002** | All domains use consistent extraction rules structure |
| **XD-003** | All prompt templates use `{{$variable}}` syntax |
| **XD-004** | All domains validate against DOMAIN-SCHEMA.json |
| **XD-005** | VCRM links domains to SPEC-context-injection.md requirements |

## Traceability

### Requirements Coverage

These specifications implement the following requirements from [SPEC-context-injection.md](../../SPEC-context-injection.md):

| Requirement | Description | Coverage |
|-------------|-------------|----------|
| REQ-CI-F-001 | Domain-specific entity recognition | All 6 domains |
| REQ-CI-F-002 | Pattern-based extraction rules | All 6 domains |
| REQ-CI-F-003 | Configurable prompt templates | All 6 domains |
| REQ-CI-F-004 | Domain selection mechanism | README + flowchart |

### Verification

See [VCRM-domains.md](./VCRM-domains.md) for the complete Verification Cross Reference Matrix.

## Implementation (FEAT-002)

These specifications will be implemented in FEAT-002:

1. **Context Files**: `contexts/{domain}.yaml` for each domain
2. **Test Transcripts**: Real transcripts for validation
3. **Validation Tooling**: Schema validation + transcript testing

## References

| Document | Relationship |
|----------|--------------|
| [TDD-context-injection.md](../../design/TDD-context-injection.md) | Technical Design Document |
| [SPEC-context-injection.md](../../SPEC-context-injection.md) | Specification Document |
| [DISC-001](../../EN-006--DISC-001-feat002-implementation-scope.md) | FEAT-002 Implementation Scope |

---

*Document ID: TASK-038-README*
*Task: TASK-038*
*Phase: 3 (Integration, Risk & Examples)*
*Status: COMPLETE*
