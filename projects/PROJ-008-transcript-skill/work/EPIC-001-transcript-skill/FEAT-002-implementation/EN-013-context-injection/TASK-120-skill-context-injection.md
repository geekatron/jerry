# TASK-120: Create SKILL.md context_injection Section

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-013 (Context Injection Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-120"
work_type: TASK
title: "Create SKILL.md context_injection Section"
description: |
  Add the context_injection section to skills/transcript/SKILL.md that
  enables domain-specific context loading per REQ-CI-F-002.

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
  - "skill-md"
  - "REQ-CI-F-002"

effort: 2
acceptance_criteria: |
  - context_injection section added to SKILL.md
  - default_domain set to "general"
  - domains array includes [general, transcript]
  - context_path points to ./contexts/
  - template_variables configured

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

Add the `context_injection` section to the transcript skill's SKILL.md file. This section configures how domain-specific context is loaded and injected into agent prompts at runtime.

### SKILL.md Section Structure

```yaml
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
```

### Template Variable Configuration

| Variable | Source | Format | Purpose |
|----------|--------|--------|---------|
| domain | invocation.domain | string | Current domain context |
| entity_definitions | context.entity_definitions | yaml | What entities to extract |
| extraction_rules | context.extraction_rules | list | How to extract entities |
| prompt_guidance | context.prompt_guidance | text | Expert guidance for agent |

### Acceptance Criteria

- [ ] `context_injection` section added to SKILL.md
- [ ] `default_domain` set to "general"
- [ ] `domains` array includes [general, transcript]
- [ ] `context_path` set to "./contexts/"
- [ ] At least 4 template variables configured
- [ ] YAML syntax validates
- [ ] Aligns with SPEC-context-injection.md Section 3.1

### Related Items

- Parent: [EN-013: Context Injection Implementation](./EN-013-context-injection.md)
- Blocked By: EN-006 (design complete)
- Blocks: TASK-121 (general.yaml), TASK-122 (transcript.yaml), TASK-124 (JSON Schema)
- References: [SPEC-context-injection.md Section 3.1](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md)
- References: REQ-CI-F-002 (Context Loading)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated SKILL.md | Implementation | skills/transcript/SKILL.md |
| YAML validation result | Evidence | (in this file) |

### Verification

- [ ] SKILL.md updated with context_injection section
- [ ] YAML syntax validates
- [ ] All template variables present
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-013 |
