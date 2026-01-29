# TASK-247: Update PLAYBOOK.md and RUNBOOK.md

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "EN-024:TASK-247"
work_type: TASK
title: "Update PLAYBOOK.md and RUNBOOK.md"
description: |
  Update the transcript skill PLAYBOOK.md and RUNBOOK.md documentation
  to include mindmap generation phase and troubleshooting guidance.
classification: ENABLER
status: BACKLOG
resolution: null
priority: MEDIUM
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-28T00:00:00Z"
updated_at: "2026-01-28T00:00:00Z"
parent_id: "EN-024"
tags:
  - documentation
  - playbook
  - runbook
effort: 2
acceptance_criteria: |
  - PLAYBOOK.md includes Phase 3.5: Mindmap Generation
  - RUNBOOK.md includes mindmap troubleshooting section
  - Time commitment table updated
  - Decision points updated for mindmap
  - Examples include --mindmap usage
activity: DOCUMENTATION
original_estimate: 2
remaining_work: 2
time_spent: 0
```

---

## Description

Update the transcript skill documentation (PLAYBOOK.md and RUNBOOK.md) to include mindmap generation as an optional pipeline phase.

### PLAYBOOK.md Changes

1. **Time Commitment Table**: Add mindmap phase duration
2. **Phase 3.5**: Add new section for mindmap generation
3. **Decision Point**: Add DP-2.5 for mindmap phase
4. **Quick Start**: Update with mindmap examples

### RUNBOOK.md Changes

1. **Troubleshooting Section**: Add mindmap-specific issues
2. **Recovery Procedures**: Add mindmap regeneration steps
3. **Common Issues**: Add Mermaid syntax errors

---

## Acceptance Criteria

- [ ] PLAYBOOK.md Phase 3.5 added for mindmap generation
- [ ] Time commitment table updated (~30-60 seconds for mindmaps)
- [ ] Decision point DP-2.5 added
- [ ] RUNBOOK.md troubleshooting section updated
- [ ] Mindmap regeneration procedure documented
- [ ] Examples show --mindmap flag usage

---

## Implementation Notes

### PLAYBOOK.md Updates

```markdown
## 5.5. Phase 3.5: Mindmap Generation (Optional)

### Entry Criteria
- [ ] --mindmap flag specified
- [ ] ts-formatter output available

### Procedure: Invoke ts-mindmap agents

**Invocation:**
```
IF --mindmap-format == "mermaid" OR "both":
  Invoke ts-mindmap-mermaid
IF --mindmap-format == "ascii" OR "both":
  Invoke ts-mindmap-ascii
```

**Verification:**
- [ ] 07-mindmap/mindmap.mmd created (if Mermaid enabled)
- [ ] 07-mindmap/mindmap.ascii.txt created (if ASCII enabled)
- [ ] Deep links valid

### Decision Point: DP-2.5

| Condition | Action |
|-----------|--------|
| Mindmap generation successful | PROCEED to Phase 4 |
| Mindmap generation failed | PROCEED with warning |
```

### RUNBOOK.md Updates

```markdown
## Mindmap Generation Issues

### Issue: Invalid Mermaid Syntax
**Symptom:** ps-critic reports MM-001 failure
**Cause:** Malformed mindmap output
**Resolution:**
1. Check extraction-report.json for valid data
2. Re-run mindmap generation only:
   `/transcript --regenerate-mindmap <packet-path>`

### Issue: ASCII Width Exceeded
**Symptom:** ps-critic reports AM-001 failure
**Cause:** Topic names too long
**Resolution:**
1. ASCII generator truncates at 80 chars
2. Check for exceptionally long topic names
```

---

## Related Items

- Parent: [EN-024: Mindmap Pipeline Integration](./EN-024-mindmap-pipeline-integration.md)
- Blocked By: [TASK-244: Pipeline Orchestration](./TASK-244-pipeline-orchestration-update.md)
- Target Files:
  - [skills/transcript/docs/PLAYBOOK.md](../../../../../skills/transcript/docs/PLAYBOOK.md)
  - [skills/transcript/docs/RUNBOOK.md](../../../../../skills/transcript/docs/RUNBOOK.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated PLAYBOOK.md | Documentation | skills/transcript/docs/PLAYBOOK.md |
| Updated RUNBOOK.md | Documentation | skills/transcript/docs/RUNBOOK.md |

### Verification

- [ ] Phase 3.5 documented
- [ ] Troubleshooting complete
- [ ] Examples accurate

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Initial task creation |
