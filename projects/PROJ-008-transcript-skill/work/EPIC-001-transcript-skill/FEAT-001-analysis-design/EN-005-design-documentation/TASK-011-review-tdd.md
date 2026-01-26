# TASK-011: ps-critic Review - TDD Documents

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-011"
work_type: TASK

# === CORE METADATA ===
title: "ps-critic Review: TDD Documents"
description: |
  Quality review of all TDD documents (TASK-001 through TASK-004) using
  ps-critic agent. Target quality score >= 0.90.

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: DONE
resolution: completed

# === PRIORITY ===
priority: HIGH

# === PEOPLE ===
assignee: "ps-critic"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"

# === HIERARCHY ===
parent_id: "EN-005"

# === TAGS ===
tags:
  - "review"
  - "quality"
  - "phase-4"

# === DELIVERY ITEM PROPERTIES ===
effort: 1
acceptance_criteria: |
  See Acceptance Criteria section below
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: TESTING
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

Execute ps-critic review for all Technical Design Documents. Per DEC-001-006:
- Individual document score >= 0.85
- Aggregate TDD score target >= 0.90
- Maximum 3 iterations per document

**Documents to Review:**
1. TDD-transcript-skill.md (TASK-001)
2. TDD-ts-parser.md (TASK-002)
3. TDD-ts-extractor.md (TASK-003)
4. TDD-ts-formatter.md (TASK-004)

**Review Criteria:**
- Template compliance
- ADR alignment
- Completeness check
- Technical accuracy
- L0/L1/L2 balance

### Acceptance Criteria

- [ ] **AC-001:** All 4 TDD documents reviewed
- [ ] **AC-002:** Quality score >= 0.85 for each document
- [ ] **AC-003:** Aggregate TDD quality >= 0.90
- [ ] **AC-004:** ADR traceability verified for each TDD
- [ ] **AC-005:** No critical issues identified
- [ ] **AC-006:** Template compliance verified
- [ ] **AC-007:** Requirements coverage confirmed
- [ ] **AC-008:** Feedback iterations <= 3 per document
- [ ] **AC-009:** Review artifact created at `review/tdd-review.md`
- [ ] **AC-010:** Quality scores documented with evidence

### Dependencies

| Type | Item | Status |
|------|------|--------|
| Blocked By | TASK-001 TDD Overview | PENDING |
| Blocked By | TASK-002 TDD ts-parser | PENDING |
| Blocked By | TASK-003 TDD ts-extractor | PENDING |
| Blocked By | TASK-004 TDD ts-formatter | PENDING |
| Parallel | TASK-012 Agent Review | Can run parallel |
| Enables | TASK-013 Final Review | Requires this complete |

### Implementation Notes

**ps-critic Review Template:**

```markdown
# TDD Review: {document_name}

## Review Metadata
- Document: {path}
- Reviewer: ps-critic
- Date: {date}
- Iteration: {1-3}

## Quality Dimensions

### 1. Template Compliance (20%)
| Criterion | Score | Notes |
|-----------|-------|-------|
| L0 Section | /10 | |
| L1 Section | /10 | |
| L2 Section | /10 | |
| ADR Checklist | /10 | |
| RTM Present | /10 | |

### 2. Technical Accuracy (30%)
| Criterion | Score | Notes |
|-----------|-------|-------|
| Architecture | /10 | |
| Data Contracts | /10 | |
| Algorithms | /10 | |

### 3. ADR Alignment (25%)
| ADR | Compliance | Evidence |
|-----|------------|----------|
| ADR-001 | | |
| ADR-002 | | |
| ADR-003 | | |
| ADR-004 | | |
| ADR-005 | | |

### 4. Completeness (25%)
| Criterion | Score | Notes |
|-----------|-------|-------|
| All sections | /10 | |
| Diagrams | /10 | |
| Examples | /10 | |

## Overall Score
**Quality Score: {0.00-1.00}**

## Issues
| ID | Severity | Description | Resolution |
|----|----------|-------------|------------|

## Recommendations
```

### Related Items

- Parent: [EN-005 Design Documentation](./EN-005-design-documentation.md)
- Depends On: [TASK-001 TDD Overview](./TASK-001-tdd-overview.md)
- Depends On: [TASK-002 TDD ts-parser](./TASK-002-tdd-ts-parser.md)
- Depends On: [TASK-003 TDD ts-extractor](./TASK-003-tdd-ts-extractor.md)
- Depends On: [TASK-004 TDD ts-formatter](./TASK-004-tdd-ts-formatter.md)
- Reference: [DEC-001-006 ps-critic Review Strategy](./FEAT-001--DEC-001-design-approach.md)

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
| tdd-review.md | Quality Review | review/tdd-review.md | PENDING |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality scores documented
- [ ] All issues resolved or deferred
- [ ] Reviewed by: TBD

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Initial task creation          |

---

*Task ID: TASK-011*
*Workflow ID: en005-tdd-20260126-001*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance), P-011 (evidence-based)*
