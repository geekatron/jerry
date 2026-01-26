# TASK-035: Specification Creation (Iterative)

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-035"
work_type: TASK

# === CORE METADATA ===
title: "Specification Creation (Iterative)"
description: |
  Phase 2: Create formal specification (SPEC) and JSON Schema for context
  injection mechanism. Uses same iterative loop as TDD with ps-architect,
  nse-architecture validation, and ps-critic quality scoring.

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: COMPLETE
resolution: DONE

# === PRIORITY ===
priority: CRITICAL

# === PEOPLE ===
assignee: "ps-architect + nse-architecture + ps-critic"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-26T16:00:00Z"
updated_at: "2026-01-26T23:30:00Z"
completed_at: "2026-01-26T23:30:00Z"

# === HIERARCHY ===
parent_id: "EN-006"

# === TAGS ===
tags:
  - "specification"
  - "json-schema"
  - "iterative"
  - "generator-critic"
  - "phase-2"

# === DELIVERY ITEM PROPERTIES ===
effort: 2
acceptance_criteria: |
  See Acceptance Criteria section below
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DESIGN
original_estimate: 3
remaining_work: 0
time_spent: 2
quality_score: 0.96
iterations_used: 1

# === ORCHESTRATION ===
phase: 2
barrier: "BARRIER-2"
execution_mode: "ITERATIVE"
ps_agent: "ps-architect"
nse_agent: "nse-architecture"
critic: "ps-critic"
blocked_by: null  # TASK-034 complete with 0.93
key_decision: "DEC-002"  # Claude Code Skills implementation approach
max_iterations: 3
quality_threshold: 0.90
```

---

## Content

### Description

Create the formal specification for the context injection mechanism, including:

1. **SPEC-context-injection.md** - Human-readable specification
2. **context-injection-schema.json** - Machine-readable JSON Schema

**CRITICAL DECISION (DEC-002):** This specification focuses on **Claude Code Skills** implementation approach, NOT Python CLI. The TDD's Python code (IContextProvider, ContextPayload, etc.) represents conceptual patterns that map to skill constructs:

| TDD Concept | Claude Code Skill Construct |
|-------------|----------------------------|
| `IContextProvider` interface | SKILL.md instructions |
| `load_static_context()` | `contexts/{domain}.yaml` |
| `resolve_template()` | Template variables `{{$variable}}` |
| `ContextPayload` | Skill invocation arguments |
| Agent integration | AGENT.md files |

This task uses the same iterative Generator-Critic loop as TASK-034:
- ps-architect generates specification
- nse-architecture validates against NASA SE standards
- ps-critic evaluates quality (must reach >= 0.90)

### Specification Structure

```markdown
# SPEC: Context Injection Mechanism

## Document Control
- Version: [X.Y]
- Status: [Draft/Review/Approved]
- Quality Score: [X.XX]

## 1. Introduction
### 1.1 Purpose
### 1.2 Scope
### 1.3 Definitions

## 2. Context Payload Specification
### 2.1 Payload Structure
### 2.2 Field Definitions
### 2.3 Validation Rules

## 3. Injection Points Specification
### 3.1 Orchestration Plan Injection
### 3.2 Agent Invocation Injection
### 3.3 Artifact Metadata Injection

## 4. Prompt Template Specification
### 4.1 Template Syntax
### 4.2 Variable Substitution
### 4.3 Conditional Logic

## 5. Security Specification
### 5.1 Input Validation
### 5.2 Sanitization Rules
### 5.3 Access Control

## 6. Error Handling Specification
### 6.1 Error Codes
### 6.2 Recovery Procedures

## 7. JSON Schema Reference
[Link to context-injection-schema.json]
```

### JSON Schema Template

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://jerry.dev/schemas/context-injection.json",
  "title": "Context Injection Payload",
  "description": "Schema for context injection mechanism payloads",
  "type": "object",
  "properties": {
    "domain": {
      "type": "string",
      "description": "Domain identifier for context specialization"
    },
    "context_files": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/ContextFile"
      }
    },
    "prompt_overrides": {
      "type": "object",
      "additionalProperties": {
        "$ref": "#/$defs/PromptOverride"
      }
    }
  },
  "required": ["domain"],
  "$defs": {
    "ContextFile": {
      "type": "object",
      "properties": {
        "path": { "type": "string" },
        "type": { "enum": ["entity_definitions", "extraction_rules", "prompt_template"] }
      },
      "required": ["path", "type"]
    },
    "PromptOverride": {
      "type": "object",
      "properties": {
        "template": { "type": "string" },
        "variables": { "type": "object" }
      }
    }
  }
}
```

### Acceptance Criteria

**Specification Content Criteria:**
- [x] **AC-001:** Spec follows established specification format
- [x] **AC-002:** All payload fields documented with types and constraints
- [x] **AC-003:** All injection points specified
- [x] **AC-004:** Prompt template syntax fully defined
- [x] **AC-005:** Security requirements documented
- [x] **AC-006:** Error handling specified

**JSON Schema Criteria:**
- [x] **AC-007:** Schema validates against JSON Schema Draft 2020-12
- [x] **AC-008:** All custom types defined in $defs
- [x] **AC-009:** Required fields marked
- [x] **AC-010:** Descriptions provided for all fields

**NASA SE Validation Criteria (nse-architecture):**
- [x] **AC-011:** Specification compliant with NASA SE Process 4
- [x] **AC-012:** Interface definitions complete
- [x] **AC-013:** Verification approach documented

**Quality Criteria (ps-critic):**
- [x] **AC-014:** Quality score >= 0.90 ✅ **ACHIEVED: 0.96**
- [x] **AC-015:** No ambiguous or incomplete definitions
- [x] **AC-016:** All TDD references resolved

### Deliverables

| Deliverable | Type | Link | Status |
|-------------|------|------|--------|
| Specification | Spec | docs/specs/SPEC-context-injection.md | COMPLETE |
| JSON Schema | Schema | docs/specs/schemas/context-injection-schema.json | COMPLETE |
| Iteration Feedback | Critique | docs/critiques/en006-spec-critique-v1.md | COMPLETE |

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Task created for redesigned workflow |
| 2026-01-26 | IN_PROGRESS | ps-architect created SPEC and JSON Schema |
| 2026-01-26 | COMPLETE    | ps-critic evaluation: 0.96 (ACCEPT). All 16/16 acceptance criteria met. |

---

*Task ID: TASK-035*
*Workflow ID: en006-ctxinj-20260126-001*
*Phase: 2 (Design & Architecture)*
*Pattern: Generator-Critic (Iterative)*
