# TASK-415: Add constraints and boundaries table

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-415"
work_type: TASK
title: "Add constraints and boundaries table"
status: BACKLOG
priority: MEDIUM
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-029"
effort: 1
activity: DOCUMENTATION
```

---

## Description

Add a constraints and boundaries table to PLAYBOOK.md that documents hard vs soft limits and their enforcement mechanisms. Addresses GAP-D-003: Constraints table missing.

**File to modify:**
- skills/transcript/docs/PLAYBOOK.md

**Location:** L2 section → "Constraints & Boundaries" subsection

---

## Acceptance Criteria

- [ ] Constraints table with Type, Limit, and Enforcement columns
- [ ] Clear distinction between Hard and Soft constraints
- [ ] All key transcript skill limits documented
- [ ] Enforcement mechanism for each constraint specified

---

## Implementation Notes

**Content to add:**

```markdown
### Constraints & Boundaries

| Constraint | Type | Limit | Enforcement |
|------------|------|-------|-------------|
| Chunk token limit | Hard | 18,000 tokens | Pipeline aborts |
| Packet file token limit | Soft | 31,500 tokens | Auto-split at heading |
| Packet file token limit | Hard | 35,000 tokens | Force split |
| Quality score threshold | Soft | 0.90 | Warning + continue |
| Subagent recursion | Hard | 0 levels | P-003 violation |
| Canonical file context | Hard | DO NOT READ | 99.8% data loss |
| Confidence threshold | Soft | 0.7 | Flagged as uncertain |
| Maximum topics in mindmap | Soft | 50 | Overflow handling |
| ASCII mindmap line width | Soft | 80 chars | Truncate with ... |

**Constraint Types:**
- **Hard:** Violation causes failure; pipeline aborts or operation rejected
- **Soft:** Violation triggers mitigation; operation continues with adjustment

**Reference:** ADR-004 (Token limits), DISC-009 (Canonical file constraint)
```

---

## Related Items

- Parent: [EN-029: Documentation Compliance](./EN-029-documentation-compliance.md)
- Gap: GAP-D-003 (Constraints table missing)
- Reference: ADR-004 (Token limits), DISC-009 (Large file analysis)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| PLAYBOOK.md | Documentation | skills/transcript/docs/PLAYBOOK.md |

### Verification

- [ ] Table with all required columns
- [ ] Hard vs Soft clearly distinguished
- [ ] All key constraints documented
- [ ] References included

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-029 |
