# TASK-407: Add "Invoking an Agent" section to SKILL.md

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-407"
work_type: TASK
title: "Add Invoking an Agent section to SKILL.md"
status: BACKLOG
priority: HIGH
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-028"
effort: 1
activity: DOCUMENTATION
```

---

## Description

Add the "Invoking an Agent" section to transcript SKILL.md per PAT-SKILL-001. This section documents the three canonical methods for invoking individual agents.

**File to modify:**
- skills/transcript/SKILL.md

**Location:** After "Available Agents" section, before "Orchestration Flow"

---

## Acceptance Criteria

- [ ] "Invoking an Agent" section added to SKILL.md
- [ ] Method 1 (Task Tool) documented with example
- [ ] Method 2 (Natural Language) documented with example
- [ ] Method 3 (Direct Import) documented with warning

---

## Implementation Notes

**Content to add:**

```markdown
## Invoking an Agent

There are three ways to invoke individual agents from the transcript skill:

### Method 1: Task Tool (Recommended)

The orchestrator can use the Task tool to delegate work to a specific agent:

```
Claude: Use the Task tool to invoke ts-extractor with input from ts-parser output at output/index.json
```

**Example Task invocation:**
```python
Task(
    description="ts-extractor: Extract entities",
    subagent_type="general-purpose",
    model="sonnet",
    prompt="""
You are the ts-extractor agent (v1.4.0).

## INPUT
- index.json: output/index.json
- chunks: output/chunks/

## TASK
Extract all entities (speakers, actions, decisions, questions, topics) from the transcript chunks.

## OUTPUT
Create: output/extraction-report.json
"""
)
```

### Method 2: Natural Language

For interactive use, describe the agent invocation in natural language:

```
"Run ts-extractor on the parsed transcript at output/index.json to extract entities"
"Use ts-formatter to generate the Markdown packet from the extraction report"
```

### Method 3: Direct Import (Advanced)

For orchestration contexts, agents can be imported directly via the skill's agent registry.
This method is for advanced users building custom workflows.

**Warning:** Direct imports bypass skill-level validation and state management.
Use with caution and only when the Task tool is insufficient.
```

---

## Related Items

- Parent: [EN-028: SKILL.md Compliance](./EN-028-skill-md-compliance.md)
- Gap: GAP-S-001 from work-026-e-002

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| SKILL.md | Documentation | skills/transcript/SKILL.md |

### Verification

- [ ] Section present with 3 methods
- [ ] Checklist items S-015 through S-018 pass

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-028 |
