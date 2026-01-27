# TASK-123: Add AGENT.md Context Sections to ts-* Agents

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-013 (Context Injection Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-123"
work_type: TASK
title: "Add AGENT.md Context Sections to ts-* Agents"
description: |
  Add context sections to ts-parser, ts-extractor, and ts-formatter agent
  definitions to enable persona context merge per REQ-CI-F-003.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T19:00:00Z"
updated_at: "2026-01-26T19:00:00Z"

parent_id: "EN-013"

tags:
  - "implementation"
  - "context-injection"
  - "agent-md"
  - "REQ-CI-F-003"

effort: 2
acceptance_criteria: |
  - ts-parser.md has context.persona section
  - ts-extractor.md has context.persona section
  - ts-formatter.md has context.persona section
  - Each persona defines role, expertise, behavior
  - Template variables for agent-specific config

due_date: null

activity: DEVELOPMENT
original_estimate: 4
remaining_work: 4
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Content

### Description

Add `context` sections to each of the three transcript skill agents (ts-parser, ts-extractor, ts-formatter). These sections define agent-specific persona context that merges with skill and domain context at invocation time.

### Agent Context Section Structure

```yaml
# AGENT-SPECIFIC CONTEXT (implements REQ-CI-F-003)
context:
  # Persona context merged with skill context
  persona:
    role: "{Agent Role}"
    expertise:
      - "{Expertise Area 1}"
      - "{Expertise Area 2}"
    behavior:
      - "{Behavioral Guideline 1}"
      - "{Behavioral Guideline 2}"

  # Template variables specific to this agent
  template_variables:
    - name: {variable_name}
      default: {default_value}
      type: {type}
```

### ts-parser Context Section

```yaml
context:
  persona:
    role: "Transcript Parsing Specialist"
    expertise:
      - "VTT/SRT format parsing"
      - "Timestamp extraction and normalization"
      - "Speaker identification from format cues"
    behavior:
      - "Preserve original speaker names exactly as written"
      - "Normalize timestamps to milliseconds"
      - "Handle multi-format input gracefully"

  template_variables:
    - name: timestamp_format
      default: "ms"
      type: string
    - name: speaker_detection
      default: true
      type: boolean
```

### ts-extractor Context Section

```yaml
context:
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
```

### ts-formatter Context Section

```yaml
context:
  persona:
    role: "Document Formatting Specialist"
    expertise:
      - "Claude-friendly Markdown generation"
      - "Token budget management"
      - "Bidirectional deep linking"
    behavior:
      - "Never exceed 35K tokens per file (ADR-002)"
      - "Split at semantic boundaries, not arbitrary points"
      - "Generate backlinks for all forward references"

  template_variables:
    - name: token_limit
      default: 35000
      type: integer
    - name: soft_limit_percent
      default: 90
      type: integer
    - name: generate_anchors
      default: true
      type: boolean
```

### Context Merge Order

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CONTEXT MERGE PRIORITY                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. SKILL.md context_injection (lowest priority)                             │
│            │                                                                 │
│            ▼                                                                 │
│  2. contexts/{domain}.yaml (domain context)                                  │
│            │                                                                 │
│            ▼                                                                 │
│  3. AGENT.md context.persona (agent-specific)                                │
│            │                                                                 │
│            ▼                                                                 │
│  4. Invocation arguments (highest priority)                                  │
│                                                                              │
│  Later sources OVERRIDE earlier sources for same keys                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] ts-parser.md has `context.persona` section
- [ ] ts-extractor.md has `context.persona` section
- [ ] ts-formatter.md has `context.persona` section
- [ ] Each persona has role (string)
- [ ] Each persona has expertise (array)
- [ ] Each persona has behavior (array)
- [ ] Each agent has relevant template_variables
- [ ] YAML syntax validates for all agents
- [ ] Aligns with SPEC-context-injection.md Section 3.2

### Related Items

- Parent: [EN-013: Context Injection Implementation](./EN-013-context-injection.md)
- Blocked By: [TASK-121: general.yaml](./TASK-121-general-domain-schema.md)
- Blocks: [TASK-125: Validation and test scenarios](./TASK-125-context-validation.md)
- References: [SPEC-context-injection.md Section 3.2](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md)
- References: REQ-CI-F-003 (Agent Context Merge)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated ts-parser.md | Implementation | skills/transcript/agents/ts-parser.md |
| Updated ts-extractor.md | Implementation | skills/transcript/agents/ts-extractor.md |
| Updated ts-formatter.md | Implementation | skills/transcript/agents/ts-formatter.md |

### Verification

- [ ] ts-parser.md context section added
- [ ] ts-extractor.md context section added
- [ ] ts-formatter.md context section added
- [ ] All YAML syntax validates
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-013 |
