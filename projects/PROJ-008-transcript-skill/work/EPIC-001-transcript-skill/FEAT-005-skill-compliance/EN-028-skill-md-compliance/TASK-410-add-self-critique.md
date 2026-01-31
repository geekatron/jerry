# TASK-410: Add self-critique checklist to Constitutional Compliance

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-410"
work_type: TASK
title: "Add self-critique checklist to Constitutional Compliance"
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

Add a self-critique checklist to the existing "Constitutional Compliance" section in SKILL.md per PAT-SKILL-001. Addresses GAP-S-005.

**File to modify:**
- skills/transcript/SKILL.md

**Location:** Add to existing "Constitutional Compliance" section

---

## Acceptance Criteria

- [ ] Self-critique checklist added with 5+ checkpoints
- [ ] References P-001, P-002, P-003, P-004, P-022
- [ ] Checklist is actionable (agents can self-verify)

---

## Implementation Notes

**Content to add to Constitutional Compliance section:**

```markdown
### Self-Critique Checklist

Before finalizing significant outputs, transcript skill agents should verify:

**Truth & Accuracy (P-001):**
- [ ] Are all extractions based on verifiable transcript content?
- [ ] Do confidence scores reflect actual certainty?
- [ ] Are entity counts accurate (not inflated)?

**File Persistence (P-002):**
- [ ] Are all outputs persisted to files (not just returned in context)?
- [ ] Is the output location documented in state handoff?

**No Recursion (P-003):**
- [ ] Am I operating as a worker agent (not spawning subagents)?
- [ ] Am I receiving input from orchestrator, not creating my own pipeline?

**Provenance (P-004):**
- [ ] Do all entities have citations to source segments?
- [ ] Are timestamp references included for verification?
- [ ] Can a human trace each extraction to its source?

**No Deception (P-022):**
- [ ] Am I being transparent about confidence scores and limitations?
- [ ] Are low-confidence extractions marked as uncertain?
- [ ] Are any gaps or failures honestly reported?

### Self-Critique Protocol

Agents SHOULD perform self-critique:
1. **Before completing:** Run through checklist items
2. **On error:** Document what went wrong and why
3. **On uncertainty:** Flag items for human review rather than guessing
```

---

## Related Items

- Parent: [EN-028: SKILL.md Compliance](./EN-028-skill-md-compliance.md)
- Gap: GAP-S-005 from work-026-e-002
- Reference: Jerry Constitution (P-001, P-002, P-003, P-004, P-022)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| SKILL.md | Documentation | skills/transcript/SKILL.md |

### Verification

- [ ] Self-critique checklist present
- [ ] 5+ checkpoints included
- [ ] Checklist item S-047 passes

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-028 |
