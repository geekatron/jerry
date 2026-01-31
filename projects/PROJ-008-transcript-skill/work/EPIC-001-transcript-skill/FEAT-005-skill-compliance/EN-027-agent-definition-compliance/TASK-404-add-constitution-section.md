# TASK-404: Add constitution section to all agents

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-404"
work_type: TASK
title: "Add constitution section to all agents"
status: BACKLOG
priority: CRITICAL
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-027"
effort: 1
activity: DEVELOPMENT
```

---

## Description

Add the `constitution` section to all 5 transcript skill agent YAML frontmatter per PAT-AGENT-001. This addresses GAP-A-007.

**Files to modify:**
- skills/transcript/agents/ts-parser.md
- skills/transcript/agents/ts-extractor.md
- skills/transcript/agents/ts-formatter.md
- skills/transcript/agents/ts-mindmap-mermaid.md
- skills/transcript/agents/ts-mindmap-ascii.md

**Section template (same for all agents):**

```yaml
constitution:
  reference: "docs/governance/JERRY_CONSTITUTION.md"
  principles_applied:
    - "P-001: Truth and Accuracy (Soft)"
    - "P-002: File Persistence (Medium)"
    - "P-003: No Recursive Subagents (Hard)"
    - "P-004: Provenance (Soft)"
    - "P-022: No Deception (Hard)"
```

---

## Acceptance Criteria

- [ ] All 5 agent files have `constitution` section
- [ ] All have `reference` pointing to Jerry Constitution
- [ ] All have `principles_applied` array with 5+ principles
- [ ] All include P-001, P-002, P-003, P-004, P-022

---

## Implementation Notes

**Standard constitution section (all agents):**

```yaml
constitution:
  reference: "docs/governance/JERRY_CONSTITUTION.md"
  principles_applied:
    - "P-001: Truth and Accuracy (Soft)"
    - "P-002: File Persistence (Medium)"
    - "P-003: No Recursive Subagents (Hard)"
    - "P-004: Provenance (Soft)"
    - "P-022: No Deception (Hard)"
```

**ts-extractor additional principle:**

```yaml
constitution:
  reference: "docs/governance/JERRY_CONSTITUTION.md"
  principles_applied:
    - "P-001: Truth and Accuracy (Soft)"
    - "P-002: File Persistence (Medium)"
    - "P-003: No Recursive Subagents (Hard)"
    - "P-004: Provenance (Soft)"
    - "P-011: Evidence-Based (Soft)"  # Extractions require citations
    - "P-022: No Deception (Hard)"
```

---

## Related Items

- Parent: [EN-027: Agent Definition Compliance](./EN-027-agent-definition-compliance.md)
- Gap: GAP-A-007 from work-026-e-002
- Reference: docs/governance/JERRY_CONSTITUTION.md

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| All 5 agent .md files | Agent Definitions | skills/transcript/agents/ |

### Verification

- [ ] All files have constitution section
- [ ] Checklist items A-029 through A-035 pass

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-027 |
