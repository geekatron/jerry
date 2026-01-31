# TASK-422: Update agent definitions with model override

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-422"
work_type: TASK
title: "Update agent definitions with model override"
status: BACKLOG
priority: MEDIUM
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-031"
effort: 4
activity: DEVELOPMENT
```

---

## Description

Update all transcript agent definitions to support model override from CLI parameters. Currently models are hardcoded in agent .md files.

**Files to modify:**
- skills/transcript/agents/ts-parser.md
- skills/transcript/agents/ts-extractor.md
- skills/transcript/agents/ts-formatter.md
- skills/transcript/agents/ts-mindmap-mermaid.md
- skills/transcript/agents/ts-mindmap-ascii.md

---

## Acceptance Criteria

- [ ] Each agent has `model_override` context variable
- [ ] Default model preserved when no override provided
- [ ] Agent invocation passes model from CLI config
- [ ] Task tool `model` parameter used correctly

---

## Implementation Notes

### Agent Definition Update Pattern

**Current:**
```yaml
# ts-extractor.md
model: sonnet  # Hardcoded
```

**Target:**
```yaml
# ts-extractor.md
model: "{model_override | default('sonnet')}"  # Overridable with default

# Context variable
context:
  template_variables:
    model_override: null  # Set by orchestrator from CLI config
```

### Orchestrator Logic

```python
# In SKILL.md orchestration
# When invoking ts-extractor:
Task(
    description="ts-extractor: Extract entities",
    subagent_type="general-purpose",
    model=model_config.extractor,  # From CLI --model-extractor
    prompt=f"""
You are ts-extractor v1.3.0.
Model: {model_config.extractor}
...
"""
)
```

### Validation

The Task tool model parameter accepts: "sonnet", "opus", "haiku"

```yaml
"model": {
  "description": "Optional model to use for this agent...",
  "enum": ["sonnet", "opus", "haiku"],
  "type": "string"
}
```

### Agent Files to Update

| Agent | File | Default Model |
|-------|------|---------------|
| ts-parser | ts-parser.md | haiku |
| ts-extractor | ts-extractor.md | sonnet |
| ts-formatter | ts-formatter.md | sonnet |
| ts-mindmap-mermaid | ts-mindmap-mermaid.md | sonnet |
| ts-mindmap-ascii | ts-mindmap-ascii.md | sonnet |

---

## Related Items

- Parent: [EN-031: Model Selection Capability](./EN-031-model-selection-capability.md)
- Depends on: TASK-419 (Validate Task tool), TASK-420 (CLI params)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Agent definitions | Code | skills/transcript/agents/*.md |

### Verification

- [ ] All 5 agents updated
- [ ] Default behavior unchanged when no override
- [ ] Model parameter passed to Task tool
- [ ] Agent receives correct model

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-031 |
