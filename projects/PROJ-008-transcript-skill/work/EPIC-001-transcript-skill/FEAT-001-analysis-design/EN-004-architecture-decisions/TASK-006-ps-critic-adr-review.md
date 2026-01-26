# TASK-006: ps-critic ADR Review

<!--
TEMPLATE: Task (DRAFT)
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 0.1.0
STATUS: DRAFT - Pending review

DESCRIPTION:
  Specific work unit typically completed in hours to a day.
  Universal concept with identical semantics across ADO, SAFe, and JIRA.

EXTENDS: DeliveryItem -> WorkItem
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-006"                           # Enabler-scoped ID
work_type: TASK                          # Immutable discriminator

# === CORE METADATA ===
title: "ps-critic ADR Review"
description: |
  Conduct formal review of all 5 ADRs (ADR-001 through ADR-005) using the
  ps-critic agent. Verify consistency, completeness, and adherence to
  template and quality standards.

# === CLASSIFICATION ===
classification: ENABLER                  # Architecture enabler work

# === LIFECYCLE STATE ===
status: BACKLOG                          # See State Machine below
resolution: null                         # Set when status is DONE or REMOVED

# === PRIORITY ===
priority: HIGH                           # Quality gate before GATE-3

# === PEOPLE ===
assignee: "ps-critic"                    # Primary agent
created_by: "Claude"                     # Auto-set on creation

# === TIMESTAMPS (Auto-managed) ===
created_at: "2026-01-26T00:00:00Z"       # ISO 8601 datetime
updated_at: "2026-01-26T00:00:00Z"       # ISO 8601 datetime

# === HIERARCHY ===
parent_id: "EN-004"                      # Parent Enabler

# === TAGS ===
tags:
  - "review"
  - "quality"
  - "ps-critic"
  - "adr"
  - "transcript-skill"

# === DELIVERY ITEM PROPERTIES ===
effort: 1                                # Story points
acceptance_criteria: |
  - All 5 ADRs reviewed for template compliance
  - All 5 ADRs reviewed for content quality
  - Inconsistencies identified and documented
  - Recommendations provided for improvements
  - Final quality score assigned
  - Review report generated
due_date: null                           # ISO 8601 date

# === TASK-SPECIFIC PROPERTIES ===
activity: TESTING                        # Review/validation work
original_estimate: 2                     # Initial time estimate in hours
remaining_work: 2                        # Remaining effort in hours
time_spent: 0                            # Actual time logged in hours
```

---

## State Machine

**Initial State:** `BACKLOG`

**Valid States:** `BACKLOG`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `REMOVED`

| From State    | Allowed Transitions                    |
|---------------|----------------------------------------|
| BACKLOG       | IN_PROGRESS, REMOVED                   |
| IN_PROGRESS   | BLOCKED, DONE, REMOVED                 |
| BLOCKED       | IN_PROGRESS, REMOVED                   |
| DONE          | IN_PROGRESS (Reopen)                   |
| REMOVED       | (Terminal - no transitions)            |

---

## Containment Rules

| Rule             | Value                           |
|------------------|---------------------------------|
| Allowed Children | Subtask                         |
| Allowed Parents  | Story, Bug, Enabler             |
| Max Depth        | 1                               |

---

## Invariants

- **INV-D01:** effort must be non-negative (inherited from DeliveryItem)
- **INV-D02:** acceptance_criteria should be defined before IN_PROGRESS (inherited)
- **INV-T01:** Task can have Story, Bug, or Enabler as parent
- **INV-T02:** remaining_work <= original_estimate when both set
- **INV-T03:** time_spent should be updated when DONE

---

## System Mapping

| System | Mapping                          |
|--------|----------------------------------|
| ADO    | Task                             |
| SAFe   | Task                             |
| JIRA   | Task, Sub-task                   |

---

## Content

### Description

Conduct formal ps-critic review of all 5 Architecture Decision Records created in EN-004. This task is blocked until TASK-001 through TASK-005 are complete.

**Review Scope:**
- ADR-001: Agent Architecture
- ADR-002: Artifact Structure & Token Management
- ADR-003: Bidirectional Deep Linking
- ADR-004: File Splitting Strategy
- ADR-005: Agent Implementation Approach

**Review Criteria:**
1. **Template Compliance**: Does each ADR follow the template?
2. **Content Quality**: Are options well-reasoned? Is rationale clear?
3. **Consistency**: Are ADRs consistent with each other?
4. **Completeness**: Are all required sections present and complete?
5. **References**: Are citations and references properly documented?

### Acceptance Criteria

- [ ] ADR-001 reviewed and feedback provided
- [ ] ADR-002 reviewed and feedback provided
- [ ] ADR-003 reviewed and feedback provided
- [ ] ADR-004 reviewed and feedback provided
- [ ] ADR-005 reviewed and feedback provided
- [ ] Cross-ADR consistency verified
- [ ] Review report generated with quality scores
- [ ] Recommendations documented
- [ ] All critical issues resolved before GATE-3

### Implementation Notes

**Process:**
1. Use @problem-solving skill with ps-critic agent
2. Review each ADR against template structure
3. Assess content quality and reasoning
4. Check for inter-ADR consistency
5. Generate review report with scores and recommendations
6. Iterate with ps-architect if revisions needed

**Review Checklist per ADR:**
- [ ] Context section complete with problem statement
- [ ] At least 3 options considered
- [ ] Pros/cons documented for each option
- [ ] Decision rationale is clear
- [ ] Consequences (positive, negative, neutral) documented
- [ ] Risks identified with mitigations
- [ ] References provided
- [ ] Template format followed

**Quality Scoring Criteria:**
| Score | Meaning |
|-------|---------|
| 0.90+ | Excellent - Ready for GATE-3 |
| 0.80-0.89 | Good - Minor revisions needed |
| 0.70-0.79 | Acceptable - Some revisions needed |
| <0.70 | Needs Work - Significant revisions required |

### Blocked By

| Task | Title | Status |
|------|-------|--------|
| TASK-001 | Create ADR-001: Agent Architecture | pending |
| TASK-002 | Create ADR-002: Artifact Structure | pending |
| TASK-003 | Create ADR-003: Bidirectional Linking | pending |
| TASK-004 | Create ADR-004: File Splitting Strategy | pending |
| TASK-005 | Create ADR-005: Agent Implementation | pending |

### Related Items

- Parent: [EN-004: Architecture Decision Records](./EN-004-architecture-decisions.md)
- Blocked By: TASK-001, TASK-002, TASK-003, TASK-004, TASK-005
- Output: ADR Review Report

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

| Deliverable | Type | Link |
|-------------|------|------|
| ADR Review Report | Review Document | TBD |
| Quality Score Matrix | Assessment | TBD |

### Verification

- [ ] All 5 ADRs reviewed
- [ ] Quality score >= 0.90
- [ ] No critical issues remaining
- [ ] Review report complete
- [ ] Ready for GATE-3 human approval

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Initial creation from template |

---

<!--
JERRY ALIGNMENT:
  existing_type: "WorkType.TASK"
  changes_needed: "None - already exists"
-->
