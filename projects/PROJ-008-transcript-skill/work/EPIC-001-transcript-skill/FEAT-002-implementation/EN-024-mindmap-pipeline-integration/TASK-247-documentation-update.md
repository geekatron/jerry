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
status: DONE
resolution: COMPLETED
priority: MEDIUM
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-28T00:00:00Z"
updated_at: "2026-01-30T00:00:00Z"
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
remaining_work: 0
time_spent: 2
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

- [x] PLAYBOOK.md Phase 3.5 added for mindmap generation
- [x] Time commitment table updated (~30-60 seconds for mindmaps)
- [x] Decision point DP-2.5 added (plus renumbered DP-3 and DP-4)
- [x] RUNBOOK.md troubleshooting section updated (R-015, R-016, R-017)
- [x] Mindmap regeneration procedure documented
- [x] Examples show --mindmap flag usage (--no-mindmap, --mindmap-format)

---

## Implementation Notes

### PLAYBOOK.md Updates (Per ADR-006)

```markdown
## 5.5. Phase 3.5: Mindmap Generation (Default)

### Entry Criteria
- [ ] --no-mindmap flag NOT specified (mindmaps ON by default)
- [ ] ts-formatter output available (ts_formatter_output)

### Procedure: Invoke ts-mindmap agents

**Invocation (Default - mindmaps enabled):**
```
IF --no-mindmap flag is NOT set:  # Default behavior
  IF --mindmap-format == "mermaid" OR "both" (default):
    Invoke ts-mindmap-mermaid
    Output: 08-mindmap/mindmap.mmd
  IF --mindmap-format == "ascii" OR "both" (default):
    Invoke ts-mindmap-ascii
    Output: 08-mindmap/mindmap.ascii.txt
ELSE:
  Skip mindmap generation (user opted out)
```

**Verification:**
- [ ] 08-mindmap/mindmap.mmd created (if Mermaid enabled)
- [ ] 08-mindmap/mindmap.ascii.txt created (if ASCII enabled)
- [ ] Deep links valid (anchor format: #xxx-NNN)
- [ ] ts_mindmap_output state key populated

### Decision Point: DP-2.5

| Condition | Action |
|-----------|--------|
| Mindmap generation successful | PROCEED to Phase 4 |
| Mindmap generation failed | PROCEED with warning (graceful degradation) |
| --no-mindmap specified | SKIP Phase 3.5, PROCEED to Phase 4 |

Reference: ADR-006 Section 5.3, 5.4
```

### RUNBOOK.md Updates (Per ADR-006 Section 5.4)

```markdown
## Mindmap Generation Issues

### Issue: Invalid Mermaid Syntax
**Symptom:** ps-critic reports MM-001 failure
**Cause:** Malformed mindmap output
**Resolution:**
1. Check extraction-report.json for valid data
2. Re-run mindmap generation only:
   `jerry transcript mindmap <packet-path> --format mermaid`
3. Verify Mermaid syntax at mermaid.live

Reference: ADR-006 Section 5.5 (MM-001 criterion)

### Issue: ASCII Width Exceeded
**Symptom:** ps-critic reports AM-001 failure
**Cause:** Topic names too long
**Resolution:**
1. ASCII generator truncates at 80 chars
2. Check for exceptionally long topic names in extraction report
3. Re-run with: `jerry transcript mindmap <packet-path> --format ascii`

Reference: ADR-006 Section 5.5 (AM-001 criterion)

### Issue: Mindmap Generation Failed (Graceful Degradation)
**Symptom:** ts_mindmap_output.overall_status == "failed"
**Cause:** Agent execution error
**Resolution:**
1. Review warning message in output
2. Core packet files (00-07) should still be present
3. Follow regeneration instructions provided in output
4. Manual regeneration: `jerry transcript mindmap <packet-path>`

Reference: ADR-006 Section 5.4 (Graceful Degradation)
```

---

## Related Items

- Parent: [EN-024: Mindmap Pipeline Integration](./EN-024-mindmap-pipeline-integration.md)
- Blocked By: [TASK-244: Pipeline Orchestration](./TASK-244-pipeline-orchestration-update.md)
- **ADR Reference:** [ADR-006: Mindmap Pipeline Integration](../../../../../docs/adrs/ADR-006-mindmap-pipeline-integration.md) - Sections 5.3, 5.4, 5.5
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

- [x] Phase 3.5 documented (PLAYBOOK.md Section 7)
- [x] Troubleshooting complete (RUNBOOK.md Sections 4.7-4.9)
- [x] Examples accurate (--no-mindmap, --mindmap-format mermaid|ascii|both)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Initial task creation |
| 2026-01-30 | Updated | **ADR-006 ALIGNMENT**: Updated PLAYBOOK and RUNBOOK examples to reflect opt-out behavior (--no-mindmap). Changed paths from 07-mindmap/ to 08-mindmap/ per DISC-001. Added ADR-006 section references. Updated decision points and troubleshooting guidance. |
| 2026-01-30 | **DONE** | **TASK COMPLETE**: Updated both PLAYBOOK.md (v1.0.0→v1.1.0) and RUNBOOK.md (v1.0.0→v1.1.0). **PLAYBOOK changes:** Added Phase 3.5 Mindmap Generation section, updated Time Commitment table (+30-60s for mindmaps), added DP-2.5 and DP-3 decision points, renumbered Phase 4 to Section 8, added 4 mindmap-related documents to Related Documents. **RUNBOOK changes:** Added 3 new diagnostic procedures (R-015 Mermaid Syntax, R-016 ASCII Width, R-017 Graceful Degradation), updated decision tree with Phase 3.5 branch, added ts-mindmap agents to systems list. All changes reference ADR-006 sections. |
