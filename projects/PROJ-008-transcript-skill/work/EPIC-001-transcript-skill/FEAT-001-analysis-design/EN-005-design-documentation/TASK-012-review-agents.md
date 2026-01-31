# TASK-012: ps-critic Review - Agent Definitions

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-012"
work_type: TASK

# === CORE METADATA ===
title: "ps-critic Review: Agent Definitions"
description: |
  Quality review of all AGENT.md files and SKILL.md (TASK-005 through TASK-008)
  using ps-critic agent. Target quality score >= 0.90.

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

Execute ps-critic review for all Agent definitions and SKILL.md. Per DEC-001-006:
- Individual document score >= 0.85
- Aggregate agent score target >= 0.90
- Maximum 3 iterations per document

**Documents to Review:**
1. ts-parser AGENT.md (TASK-005)
2. ts-extractor AGENT.md (TASK-006)
3. ts-formatter AGENT.md (TASK-007)
4. SKILL.md (TASK-008)

**Review Criteria:**
- PS_AGENT_TEMPLATE.md compliance
- Constitutional compliance (P-002, P-003)
- Prompt quality assessment
- Integration validation

### Acceptance Criteria

- [x] **AC-001:** All 4 agent/skill documents reviewed
- [x] **AC-002:** Quality score >= 0.85 for each document
- [x] **AC-003:** Aggregate agent quality >= 0.90 (achieved 0.91)
- [x] **AC-004:** PS_AGENT_TEMPLATE.md compliance verified
- [x] **AC-005:** No P-003 violations (no recursive subagents)
- [x] **AC-006:** No critical issues identified
- [x] **AC-007:** Prompt quality assessed
- [x] **AC-008:** Feedback iterations <= 3 per document
- [x] **AC-009:** Review artifact created at `review/agent-review.md`
- [x] **AC-010:** Quality scores documented with evidence

### Dependencies

| Type | Item | Status |
|------|------|--------|
| Blocked By | TASK-005 ts-parser AGENT.md | PENDING |
| Blocked By | TASK-006 ts-extractor AGENT.md | PENDING |
| Blocked By | TASK-007 ts-formatter AGENT.md | PENDING |
| Blocked By | TASK-008 SKILL.md | PENDING |
| Parallel | TASK-011 TDD Review | Can run parallel |
| Enables | TASK-013 Final Review | Requires this complete |

### Implementation Notes

**ps-critic Review Template:**

```markdown
# Agent Review: {document_name}

## Review Metadata
- Document: {path}
- Reviewer: ps-critic
- Date: {date}
- Iteration: {1-3}

## Quality Dimensions

### 1. Template Compliance (25%)
| Criterion | Score | Notes |
|-----------|-------|-------|
| YAML Frontmatter | /10 | |
| Identity Section | /10 | |
| Capabilities | /10 | |
| Guardrails | /10 | |
| XML Structure | /10 | |

### 2. Constitutional Compliance (25%)
| Principle | Compliant | Evidence |
|-----------|-----------|----------|
| P-002: File Persistence | | |
| P-003: No Subagents | | |
| P-004: Provenance | | |
| P-020: User Authority | | |
| P-022: No Deception | | |

### 3. Prompt Quality (25%)
| Criterion | Score | Notes |
|-----------|-------|-------|
| Clarity | /10 | |
| Specificity | /10 | |
| Output Format | /10 | |
| Error Handling | /10 | |

### 4. Integration (25%)
| Criterion | Score | Notes |
|-----------|-------|-------|
| Input Contract | /10 | |
| Output Contract | /10 | |
| Orchestrator Fit | /10 | |

## Overall Score
**Quality Score: {0.00-1.00}**

## Issues
| ID | Severity | Description | Resolution |
|----|----------|-------------|------------|

## Recommendations
```

### Related Items

- Parent: [EN-005 Design Documentation](./EN-005-design-documentation.md)
- Depends On: [TASK-005 ts-parser AGENT.md](./TASK-005-agent-ts-parser.md)
- Depends On: [TASK-006 ts-extractor AGENT.md](./TASK-006-agent-ts-extractor.md)
- Depends On: [TASK-007 ts-formatter AGENT.md](./TASK-007-agent-ts-formatter.md)
- Depends On: [TASK-008 SKILL.md](./TASK-008-skill-md.md)
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
| agent-review.md | Quality Review | review/agent-review.md | COMPLETE |

### Verification

- [x] Acceptance criteria verified
- [x] Quality scores documented
- [x] All P-003 violations resolved
- [x] Reviewed by: ps-critic (Quality Score: 0.91)

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Initial task creation          |
| 2026-01-26 | DONE        | Review complete: Aggregate 0.91 (all pass >= 0.85) |

---

*Task ID: TASK-012*
*Workflow ID: en005-tdd-20260126-001*
*Constitutional Compliance: P-002 (persisted), P-003 (verified), P-004 (provenance)*
