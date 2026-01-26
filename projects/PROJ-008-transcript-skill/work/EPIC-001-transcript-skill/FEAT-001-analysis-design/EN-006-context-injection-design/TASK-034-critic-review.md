# TASK-034: ps-critic Review & GATE-4 Preparation

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-034"
work_type: TASK

# === CORE METADATA ===
title: "ps-critic Review & GATE-4 Preparation"
description: |
  Conduct comprehensive ps-critic review of all EN-006 deliverables.
  Verify quality gates, traceability, and completeness before GATE-4
  human approval request.

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: BACKLOG
resolution: null

# === PRIORITY ===
priority: HIGH

# === PEOPLE ===
assignee: "ps-critic"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-26T15:00:00Z"
updated_at: "2026-01-26T15:00:00Z"

# === HIERARCHY ===
parent_id: "EN-006"

# === TAGS ===
tags:
  - "review"
  - "quality"
  - "gate-4"
  - "phase-5"

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

Conduct comprehensive ps-critic review of all EN-006 Context Injection Design deliverables. This is the quality gate before requesting human approval at GATE-4.

**Review Scope:**
```
PS-CRITIC REVIEW SCOPE
├── TASK-030: 5W2H Analysis Review
│   ├── Completeness: All 7 W's addressed?
│   ├── Evidence: Citations and references?
│   └── L0/L1/L2: All perspectives covered?
├── TASK-031: Specification Review
│   ├── Schema: Validates correctly?
│   ├── Security: Constraints documented?
│   └── Completeness: All aspects covered?
├── TASK-032: Integration Design Review
│   ├── P-003: Single nesting preserved?
│   ├── Alignment: Matches orchestration patterns?
│   └── Diagrams: Render correctly?
├── TASK-033: Examples Review
│   ├── Validation: Examples work against schema?
│   ├── Coverage: Distinct domains covered?
│   └── Usability: Clear and complete?
└── OVERALL EN-006 Review
    ├── Traceability: EN-003 requirements mapped?
    ├── ADR Compliance: ADR-001..005 followed?
    └── Quality Score: >= 0.90 required
```

**Quality Scoring Criteria:**
| Dimension | Weight | Criteria |
|-----------|--------|----------|
| Completeness | 25% | All deliverables present with all sections |
| Correctness | 25% | Technical accuracy, schema validation |
| Traceability | 20% | Requirements linked, ADRs referenced |
| Clarity | 15% | L0/L1/L2 documented, diagrams clear |
| Evidence | 15% | Citations, sources, prior art referenced |

### Acceptance Criteria

- [ ] **AC-001:** Quality score >= 0.90 achieved
- [ ] **AC-002:** All TASK-030..033 deliverables reviewed
- [ ] **AC-003:** Each deliverable rated with specific scores
- [ ] **AC-004:** EN-003 requirements traceability verified
- [ ] **AC-005:** ADR-001..005 compliance verified
- [ ] **AC-006:** P-003 (single nesting) compliance verified
- [ ] **AC-007:** All diagrams render correctly
- [ ] **AC-008:** All schemas validate correctly
- [ ] **AC-009:** Improvement recommendations documented (if any)
- [ ] **AC-010:** GATE-4 approval request prepared

### Dependencies

| Type | Item | Status |
|------|------|--------|
| Input | TASK-030 5W2H Analysis | Pending |
| Input | TASK-031 Context Injection Specification | Pending |
| Input | TASK-032 Orchestration Integration Design | Pending |
| Input | TASK-033 Example Orchestration Plans | Pending |
| Output | GATE-4 Human Approval | Requires this review pass |

### Implementation Notes

**Agent Assignment:** ps-critic

**Review Process:**
1. Read all deliverables from TASK-030..033
2. Apply quality scoring criteria
3. Check traceability to EN-003 requirements
4. Verify ADR compliance
5. Validate schemas and diagrams
6. Calculate overall quality score
7. Document findings in review artifact
8. Prepare GATE-4 approval request

**Quality Score Calculation:**
```
Score = (Completeness × 0.25) + (Correctness × 0.25) +
        (Traceability × 0.20) + (Clarity × 0.15) + (Evidence × 0.15)

Target: >= 0.90 (90%)
```

**Review Artifact Structure:**
```markdown
# ps-critic Review: EN-006 Context Injection Design

## Review Summary
- **Overall Score:** [X.XX / 1.00]
- **Verdict:** [PASS/FAIL]
- **Date:** YYYY-MM-DD

## Individual Deliverable Reviews
### TASK-030: 5W2H Analysis
[Detailed review]

### TASK-031: Context Injection Specification
[Detailed review]

### TASK-032: Orchestration Integration Design
[Detailed review]

### TASK-033: Example Orchestration Plans
[Detailed review]

## Quality Dimensions
| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | X.XX | ... |
| Correctness | X.XX | ... |
| Traceability | X.XX | ... |
| Clarity | X.XX | ... |
| Evidence | X.XX | ... |

## Recommendations
[Improvement suggestions if score < 0.90]

## GATE-4 Readiness
[Prepared approval request]
```

### Related Items

- Parent: [EN-006 Context Injection Design](./EN-006-context-injection-design.md)
- Input: [TASK-030 5W2H Analysis](./TASK-030-5w2h-analysis.md)
- Input: [TASK-031 Context Injection Specification](./TASK-031-context-injection-spec.md)
- Input: [TASK-032 Orchestration Integration](./TASK-032-orchestration-integration.md)
- Input: [TASK-033 Example Plans](./TASK-033-example-plans.md)
- Enables: GATE-4 Human Approval

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
| FEAT-001--CRIT-EN006-review.md | Review Document | ../FEAT-001--CRIT-EN006-review.md | PENDING |

### Verification

- [ ] Quality score >= 0.90
- [ ] All deliverables reviewed
- [ ] Traceability verified
- [ ] ADR compliance verified
- [ ] P-003 compliance verified
- [ ] GATE-4 request prepared
- [ ] Reviewed by: Human (GATE-4)

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Initial task creation          |

---

*Task ID: TASK-034*
*Workflow ID: en006-ctxinj-20260126-001*
*Constitutional Compliance: P-001 (truth), P-002 (persisted), P-004 (provenance), P-022 (no deception)*
