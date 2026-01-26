# TASK-010: Create EN-005 RUNBOOK

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-010"
work_type: TASK

# === CORE METADATA ===
title: "Create EN-005 RUNBOOK"
description: |
  Create troubleshooting runbook for the Transcript Skill following
  RUNBOOK.template.md structure with risk-based troubleshooting sections.

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: DONE
resolution: completed
relocation_note: |
  RELOCATED per DISC-004 and DEC-002 (2026-01-26):
  Implementation artifact moved to: skills/transcript/docs/RUNBOOK.md
  This task file documents design intent. Executable implementation now in skills/ folder.

# === PRIORITY ===
priority: MEDIUM

# === PEOPLE ===
assignee: "ps-architect"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"

# === HIERARCHY ===
parent_id: "EN-005"

# === TAGS ===
tags:
  - "runbook"
  - "operations"
  - "phase-3"

# === DELIVERY ITEM PROPERTIES ===
effort: 1
acceptance_criteria: |
  See Acceptance Criteria section below
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DOCUMENTATION
original_estimate: 2
remaining_work: 2
time_spent: 0
```

---

## State Machine

**Initial State:** `BACKLOG`

**Valid States:** `BACKLOG`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `REMOVED`

---

## Containment Rules

| Rule             | Value                           |
|------------------|---------------------------------|
| Allowed Children | Subtask                         |
| Allowed Parents  | Enabler                         |
| Max Depth        | 1                               |

---

## Content

### Description

Create the troubleshooting RUNBOOK for the Transcript Skill. Per DEC-001-008, the runbook covers all YELLOW risks from EN-003 FMEA:

```
RUNBOOK Troubleshooting Sections:
├── R-002: SRT Timestamp Issues (RPN: 8)
├── R-004: Missing Speaker Identification (RPN: 12)
├── R-006: Low Action Item Precision (RPN: 12)
├── R-007: Low Action Item Recall (RPN: 12)
├── R-008: Hallucination Detection (RPN: 12)
└── R-014: JSON Schema Compatibility (RPN: 9)
```

**Runbook Contents:**
- Symptom-Cause-Resolution mapping
- Decision trees for common issues
- Escalation matrix
- Recovery procedures
- L0/L1/L2 perspectives

### Acceptance Criteria

- [ ] **AC-001:** Follows `.context/templates/design/RUNBOOK.template.md` structure
- [ ] **AC-002:** All 5 YELLOW risks have troubleshooting sections
- [ ] **AC-003:** Symptom-Cause-Resolution tables for each issue
- [ ] **AC-004:** Decision trees in Mermaid for diagnosis
- [ ] **AC-005:** Escalation matrix defined
- [ ] **AC-006:** Recovery procedures documented
- [ ] **AC-007:** L0/L1/L2 perspectives included
- [ ] **AC-008:** Links to relevant TDD sections
- [ ] **AC-009:** File created at `docs/RUNBOOK-en005.md`
- [ ] **AC-010:** All decision trees validated

### Dependencies

| Type | Item | Status |
|------|------|--------|
| Blocked By | TASK-008 SKILL.md | PENDING |
| Parallel | TASK-009 PLAYBOOK | Can run parallel |
| Enables | TASK-011 TDD Review | Requires documentation complete |

### Implementation Notes

**Template Location:** `.context/templates/design/RUNBOOK.template.md`

**Risk-Based Structure (per DEC-001-008):**

```markdown
## R-002: SRT Timestamp Issues

### Symptoms
- Timestamps show negative values
- Time jumps between utterances
- Duration calculation errors

### Root Causes
| Cause | Likelihood | Impact |
|-------|------------|--------|
| Malformed SRT format | HIGH | MEDIUM |
| Encoding issues | MEDIUM | LOW |
| Missing start time | LOW | HIGH |

### Resolution Steps
1. Check SRT file encoding (UTF-8 expected)
2. Validate timestamp format (HH:MM:SS,mmm)
3. Run defensive parsing with fallback

### Decision Tree
graph TD
    A[Timestamp Error] --> B{Negative value?}
    B -->|Yes| C[Check start time]
    B -->|No| D{Time jump > 60s?}
    D -->|Yes| E[Check for missing segment]
    D -->|No| F[Format validation]

### Escalation
- L1: Check ts-parser logs
- L2: Review defensive parsing rules
- L3: Update timestamp normalization
```

### Related Items

- Parent: [EN-005 Design Documentation](./EN-005-design-documentation.md)
- Depends On: [TASK-008 SKILL.md](./TASK-008-skill-md.md)
- Reference: [DEC-001-008 RUNBOOK Risk Structure](./FEAT-001--DEC-001-design-approach.md)
- Reference: [EN-003 FMEA Analysis](../EN-003-requirements-synthesis/requirements/FMEA-ANALYSIS.md)

---

## Time Tracking

| Metric            | Value           |
|-------------------|-----------------|
| Original Estimate | 2 hours         |
| Remaining Work    | 2 hours         |
| Time Spent        | 0 hours         |

---

## Evidence

### Deliverables

| Deliverable | Type | Link | Status |
|-------------|------|------|--------|
| RUNBOOK-en005.md | Troubleshooting Runbook | ~~docs/RUNBOOK-en005.md~~ → **skills/transcript/docs/RUNBOOK.md** | RELOCATED |

### Verification

- [ ] Acceptance criteria verified
- [ ] All YELLOW risks covered
- [ ] Decision trees render correctly
- [ ] Reviewed by: TBD

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Initial task creation          |
| 2026-01-26 | DONE        | RUNBOOK created                 |
| 2026-01-26 | RELOCATED   | Moved to skills/transcript/docs/RUNBOOK.md per DISC-004, DEC-002 |

---

*Task ID: TASK-010*
*Workflow ID: en005-tdd-20260126-001*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance)*
