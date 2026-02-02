# EN-202:BUG-004: TODO Section Not Migrated (EN-203 Pending)

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
CREATED: 2026-02-02 (Gap Analysis GAP-001)
PURPOSE: Document critical gap - TODO section behavioral content not preserved
-->

> **Type:** bug
> **Status:** closed
> **Resolution:** fixed
> **Priority:** critical
> **Impact:** critical
> **Severity:** critical
> **Created:** 2026-02-02T05:00:00Z
> **Due:** 2026-02-03T00:00:00Z
> **Completed:** 2026-02-02T06:00:00Z
> **Parent:** EN-202
> **Owner:** Claude
> **Found In:** CLAUDE.md (rewritten)
> **Fix Version:** EN-203

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Bug overview and key details |
| [Reproduction Steps](#reproduction-steps) | How to identify the gap |
| [Environment](#environment) | System configuration |
| [Evidence](#evidence) | Gap analysis documentation |
| [Root Cause Analysis](#root-cause-analysis) | Cause identification |
| [Fix Description](#fix-description) | Required remediation |
| [Acceptance Criteria](#acceptance-criteria) | Fix verification |
| [Related Items](#related-items) | Hierarchy and references |
| [History](#history) | Change log |
| [System Mapping](#system-mapping) | External system mappings |

---

## Summary

The `<todo>` section (lines 405-438, 34 lines) containing 19+ META TODO requirements was identified for migration to EN-203 but EN-203 has **NOT been executed**. This critical behavioral content is NOT preserved anywhere in the repository.

**Key Details:**
- **Symptom:** Claude will NOT maintain META TODO items as instructed
- **Frequency:** Every session - no META TODO behavioral guidance exists
- **Workaround:** None - content is completely missing

---

## Reproduction Steps

### Prerequisites

Access to gap analysis traceability matrix and new CLAUDE.md.

### Steps to Reproduce

1. Open new CLAUDE.md (80 lines)
2. Search for "META TODO" - no results
3. Search for "TODO list" - no results
4. Check `skills/worktracker/` for todo-integration rules - does not exist
5. Check EN-203 status - status: pending (NOT STARTED)

### Expected Result

META TODO behavioral requirements should be preserved either:
- In CLAUDE.md (condensed)
- In worktracker skill rules
- In a dedicated rules file

### Actual Result

Content is completely missing. EN-203 which was supposed to migrate this content has not been executed.

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | Any |
| **Browser/Runtime** | N/A (documentation file) |
| **Application Version** | CLAUDE.md (rewritten) |
| **Configuration** | Default |
| **Deployment** | Repository root |

---

## Evidence

### Bug Documentation

| Evidence | Type | Description | Date |
|----------|------|-------------|------|
| Gap Analysis traceability-matrix.md | Report | GAP-001 identified | 2026-02-02 |
| CLAUDE.md.backup lines 405-438 | Source | Original TODO section | 2026-02-02 |
| EN-203 status: pending | Verification | Migration not executed | 2026-02-02 |

### Lost Content (34 lines)

```markdown
<todo>
Use the task management tools (e.g. TaskCreate, TaskUpdate, TaskList, TaskGet) to manage your TODO list effectively.

REQUIRED BEHAVIOR:
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you are in project {JerryProjectId} | Workflow Id: {WorkflowId}
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to update the respective work tracker `*.md` files.
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to capture and update decisions...
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to update your respective `*.md` files...
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to document detailed bugs, discoveries...
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to Keep your TODO list up to date.
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to Keep your TODO list in sync...
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: Do NOT take shortcuts...
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: Ask questions...
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: Be truthful, accurate, evidence based...
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: You MUST ALWAYS document your work...
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: You MUST ALWAYS perform any kind of research...
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: You MUST perform research and analysis using Context7...
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: You MUST make data + evidence driven decisions...
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: You MUST persist your detailed analysis...
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: You MUST make all decisions in an evidence based process...
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: You MUST make ascii art and mermaid diagrams...

You MUST keep your TODO in sync with the work-tracker...
You MUST keep your TODO in sync with the orchestration plan...
You MUST reflect the actions you are taking in the TODO list...
</todo>
```

---

## Root Cause Analysis

### Root Cause

EN-203 (TODO Section Migration) was created as a planned enabler but was never executed. The CLAUDE.md rewrite (EN-202) proceeded to completion without ensuring EN-203 was also completed, leaving critical behavioral content orphaned.

### Contributing Factors

- EN-203 marked as "deferred" rather than "blocking"
- EN-202 completion criteria did not include EN-203 verification
- Gap analysis not performed until user challenged content preservation

---

## Fix Description

### Solution Approach

Execute EN-203 to migrate TODO section content to the worktracker skill.

### Required Changes

1. Create `skills/worktracker/rules/todo-integration-rules.md`
2. Preserve all 19+ META TODO requirements
3. Update CLAUDE.md Navigation table to reference the new rules file
4. Mark EN-203 as complete

### Target File

`skills/worktracker/rules/todo-integration-rules.md`

---

## Acceptance Criteria

### Fix Verification

- [ ] All 19+ META TODO requirements preserved in todo-integration-rules.md
- [ ] TODO sync requirements preserved
- [ ] Quality reminders (no shortcuts, be truthful) preserved
- [ ] Three-persona documentation requirement preserved
- [ ] Mermaid/ASCII diagram requirement preserved
- [ ] EN-203 marked as complete

### Quality Checklist

- [ ] Content matches original CLAUDE.md.backup lines 405-438
- [ ] Rules file follows skill rules template format
- [ ] CLAUDE.md Navigation table updated
- [ ] No behavioral requirements lost

---

## Related Items

### Hierarchy

- **Parent:** [EN-202: CLAUDE.md Rewrite](./EN-202-claude-md-rewrite.md)

### Related Items

- **Gap Analysis:** [traceability-matrix.md](./gap-analysis/traceability-matrix.md) (GAP-001)
- **Migration Target:** [EN-203: TODO Section Migration](../EN-203-todo-section-migration/EN-203-todo-section-migration.md)
- **Original Source:** CLAUDE.md.backup lines 405-438

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-02T05:00:00Z | Claude | pending | Initial report from gap analysis (GAP-001) |
| 2026-02-02T06:00:00Z | Claude | closed | FIXED: Created `skills/worktracker/rules/todo-integration-rules.md` with all 19+ META TODO requirements preserved. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Bug |
| **SAFe** | Defect |
| **JIRA** | Bug |
