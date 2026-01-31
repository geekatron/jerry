# TASK-411: Restructure persona and add output sections in agents

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-411"
work_type: TASK
title: "Restructure persona and add output sections in agents"
status: BACKLOG
priority: HIGH
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-028"
effort: 2
activity: DEVELOPMENT
```

---

## Description

Move `persona` from nested `context.persona` to top-level and add `output` section to all agent definitions per PAT-AGENT-001. Addresses GAP-A-002 and GAP-A-005.

**Files to modify:**
- skills/transcript/agents/ts-parser.md
- skills/transcript/agents/ts-extractor.md
- skills/transcript/agents/ts-formatter.md
- skills/transcript/agents/ts-mindmap-mermaid.md
- skills/transcript/agents/ts-mindmap-ascii.md

---

## Acceptance Criteria

- [ ] All agents have top-level `persona` section (not nested under `context`)
- [ ] All agents have `output` section with required, location, levels
- [ ] Backward compatibility maintained (existing XML/Markdown sections unchanged)
- [ ] Pipeline test passes

---

## Implementation Notes

### Persona Restructure

**Current (WRONG):**
```yaml
context:
  persona:
    role: "..."
    expertise: [...]
```

**Target (CORRECT):**
```yaml
persona:
  tone: "professional"
  communication_style: "direct"
  audience_level: "adaptive"
```

### Output Section to Add

**ts-parser output:**
```yaml
output:
  required: true
  location: "{output_dir}/index.json, {output_dir}/chunks/"
  levels: [L0, L1, L2]
```

**ts-extractor output:**
```yaml
output:
  required: true
  location: "{output_dir}/extraction-report.json"
  levels: [L0, L1, L2]
```

**ts-formatter output:**
```yaml
output:
  required: true
  location: "{output_dir}/packet/"
  template: "ADR-002 packet structure"
  levels: [L0, L1, L2]
```

**ts-mindmap-mermaid output:**
```yaml
output:
  required: true
  location: "{output_dir}/08-mindmap/mindmap.mmd"
  levels: [L0, L1, L2]
```

**ts-mindmap-ascii output:**
```yaml
output:
  required: true
  location: "{output_dir}/08-mindmap/mindmap.ascii.txt"
  levels: [L0, L1, L2]
```

### Backward Compatibility

- Keep existing `context` section with `template_variables` if needed
- Only move persona to top-level
- Do not break existing XML tags or Markdown sections

---

## Related Items

- Parent: [EN-028: SKILL.md Compliance](./EN-028-skill-md-compliance.md)
- Gap: GAP-A-002 (persona nesting), GAP-A-005 (output missing)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| All 5 agent .md files | Agent Definitions | skills/transcript/agents/ |

### Verification

- [ ] Persona at top-level in all agents
- [ ] Output section in all agents
- [ ] Pipeline test passes
- [ ] Checklist items A-009-011, A-022-025 pass

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-028 |
