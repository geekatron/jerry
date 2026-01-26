# TASK-032: Ishikawa & Pareto Analysis

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-032"
work_type: TASK

# === CORE METADATA ===
title: "Ishikawa & Pareto Analysis"
description: |
  Phase 1: Apply Ishikawa (fishbone) diagram for root cause analysis of
  potential failure modes, and Pareto (80/20) analysis to prioritize
  use cases and features.

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: BACKLOG
resolution: null

# === PRIORITY ===
priority: HIGH

# === PEOPLE ===
assignee: "ps-analyst"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-26T16:00:00Z"
updated_at: "2026-01-26T16:00:00Z"

# === HIERARCHY ===
parent_id: "EN-006"

# === TAGS ===
tags:
  - "analysis"
  - "ishikawa"
  - "pareto"
  - "root-cause"
  - "phase-1"

# === DELIVERY ITEM PROPERTIES ===
effort: 1
acceptance_criteria: |
  See Acceptance Criteria section below
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: ANALYSIS
original_estimate: 2
remaining_work: 2
time_spent: 0

# === ORCHESTRATION ===
phase: 1
barrier: "BARRIER-1"
execution_mode: "PARALLEL_WITH_TASK_031_033"
ps_agent: "ps-analyst"
blocked_by: "BARRIER-0"
```

---

## Content

### Description

Apply two complementary analysis frameworks:

**1. Ishikawa (Fishbone) Diagram:**
Root cause analysis for "Context Injection Failures" identifying causes across categories:
- People (user errors, training gaps)
- Process (workflow issues, missing steps)
- Technology (implementation bugs, integration issues)
- Environment (runtime conditions, dependencies)
- Materials (data quality, context sources)
- Methods (design patterns, approaches)

**2. Pareto (80/20) Analysis:**
Prioritize use cases to identify the 20% of features that deliver 80% of value:
- Use case frequency analysis
- Value/effort matrix
- Feature prioritization

### Acceptance Criteria

**Ishikawa Criteria:**
- [ ] **AC-001:** Fishbone diagram covers all 6 categories
- [ ] **AC-002:** At least 3 root causes identified per category
- [ ] **AC-003:** Each root cause has mitigation strategy
- [ ] **AC-004:** Diagram rendered in ASCII or Mermaid

**Pareto Criteria:**
- [ ] **AC-005:** At least 10 use cases analyzed
- [ ] **AC-006:** Value/effort scores assigned to each
- [ ] **AC-007:** Top 20% of use cases identified
- [ ] **AC-008:** Pareto chart visualized

**General Criteria:**
- [ ] **AC-009:** Analysis incorporates BARRIER-0 research
- [ ] **AC-010:** Documents follow L0/L1/L2 format

### Ishikawa Diagram Template

```
                                      CONTEXT INJECTION FAILURE
                                               │
              ┌────────────────────────────────┼────────────────────────────────┐
              │                                │                                │
         ┌────┴────┐                     ┌─────┴─────┐                    ┌─────┴─────┐
         │ PEOPLE  │                     │  PROCESS  │                    │TECHNOLOGY │
         └────┬────┘                     └─────┬─────┘                    └─────┬─────┘
              │                                │                                │
    ┌─────────┼─────────┐            ┌─────────┼─────────┐            ┌─────────┼─────────┐
    │         │         │            │         │         │            │         │         │
  Cause1   Cause2   Cause3        Cause1   Cause2   Cause3        Cause1   Cause2   Cause3
              │                                │                                │
              └────────────────────────────────┼────────────────────────────────┘
              │                                │                                │
         ┌────┴────┐                     ┌─────┴─────┐                    ┌─────┴─────┐
         │MATERIALS│                     │  METHODS  │                    │ENVIRONMENT│
         └────┬────┘                     └─────┬─────┘                    └─────┬─────┘
              │                                │                                │
    ┌─────────┼─────────┐            ┌─────────┼─────────┐            ┌─────────┼─────────┐
    │         │         │            │         │         │            │         │         │
  Cause1   Cause2   Cause3        Cause1   Cause2   Cause3        Cause1   Cause2   Cause3
```

### Pareto Analysis Template

```
| Use Case | Frequency | Value (1-10) | Effort (1-10) | Priority Score |
|----------|-----------|--------------|---------------|----------------|
| UC-001   | High      | 9            | 3             | 27             |
| UC-002   | Medium    | 7            | 2             | 24.5           |
| ...      | ...       | ...          | ...           | ...            |

Top 20% (delivering 80% value):
1. UC-001: [description]
2. UC-002: [description]
```

### Deliverables

| Deliverable | Type | Link | Status |
|-------------|------|------|--------|
| Ishikawa Analysis | Analysis | docs/analysis/en006-ishikawa-failure-modes.md | PENDING |
| Pareto Analysis | Analysis | docs/analysis/en006-pareto-use-cases.md | PENDING |

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Task created for redesigned workflow |

---

*Task ID: TASK-032*
*Workflow ID: en006-ctxinj-20260126-001*
*Phase: 1 (Requirements & Analysis)*
*Frameworks: Ishikawa, Pareto*
