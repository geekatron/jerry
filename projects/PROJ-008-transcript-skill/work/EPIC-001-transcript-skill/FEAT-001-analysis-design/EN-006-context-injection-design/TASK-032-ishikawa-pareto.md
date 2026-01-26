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
status: DONE
resolution: COMPLETED

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
remaining_work: 0
time_spent: 2

# === ORCHESTRATION ===
phase: 1
barrier: "BARRIER-1"
execution_mode: "SEQUENTIAL_FORWARD_FEEDING"  # DEC-001
ps_agent: "ps-analyst"
blocked_by: "TASK-031"  # Sequential dependency (DEC-001)
inputs_from: "TASK-031"  # 5W2H analysis feeds into this task
outputs_to: "TASK-033"  # Forward-feeding (DEC-001)
position_in_chain: 2  # Second in Phase 1 sequence
decision_ref: "EN-006:DEC-001"
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

### Dependencies

**DEC-001: Sequential Forward-Feeding Pattern**

This task is **Step 2** in the Phase 1 forward-feeding chain (TASK-031 → TASK-032 → TASK-033).

| Type | Item | Status |
|------|------|--------|
| Input ← | [TASK-031 (5W2H)](./TASK-031-5w2h-analysis.md) | **BLOCKING** this task |
| Input | [Research Synthesis](./docs/research/en006-research-synthesis.md) | Complete |
| Input | [Trade Space](./docs/research/en006-trade-space.md) | Complete |
| Output → | TASK-033 (Requirements) | Blocked by this task |
| Output | BARRIER-1 | Requires all Phase 1 tasks |

```
Sequential Forward-Feeding (DEC-001):
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  TASK-031    │────►│  TASK-032    │────►│  TASK-033    │────► BARRIER-1
│   (5W2H)     │     │(Ishikawa+P)  │     │   (Reqs)     │
└──────────────┘     └──────────────┘     └──────────────┘
                            ▲
                            │
                      [YOU ARE HERE]
```

**Required Input from TASK-031:**
- 5W2H "What" analysis → Defines mechanism for Ishikawa effect
- 5W2H "Who" analysis → Identifies people category causes
- 5W2H "How" analysis → Identifies method category causes
- 5W2H "Where" analysis → Identifies environment/technology causes

---

### Acceptance Criteria

**Ishikawa Criteria:**
- [x] **AC-001:** Fishbone diagram covers all 6 categories (People, Process, Technology, Materials, Methods, Environment - see Section 1.2)
- [x] **AC-002:** At least 3 root causes identified per category (18 total: P1-1 to P1-3, P2-1 to P2-3, T1-1 to T1-3, M1-1 to M1-3, D1-1 to D1-3, E1-1 to E1-3)
- [x] **AC-003:** Each root cause has mitigation strategy (see Section 1.3 tables with Mitigation column)
- [x] **AC-004:** Diagram rendered in ASCII or Mermaid (ASCII fishbone diagram in Section 1.2)

**Pareto Criteria:**
- [x] **AC-005:** At least 10 use cases analyzed (15 features F01-F15 analyzed in Section 2.1)
- [x] **AC-006:** Value/effort scores assigned to each (1-10 scale scoring in Section 2.2)
- [x] **AC-007:** Top 20% of use cases identified (F02, F11, F13 = top 20% delivering 27.2% value)
- [x] **AC-008:** Pareto chart visualized (ASCII chart in Section 2.3 with cumulative percentages)

**General Criteria:**
- [x] **AC-009:** Analysis incorporates BARRIER-0 research (cites en006-research-synthesis.md, en006-trade-space.md, EN-003 requirements)
- [x] **AC-010:** Documents follow L0/L1/L2 format (L0 Executive, L1 Technical, L2 Architect sections)

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
| Combined Ishikawa & Pareto Analysis | Analysis | [docs/analysis/en006-ishikawa-pareto-analysis.md](./docs/analysis/en006-ishikawa-pareto-analysis.md) | **COMPLETE** |

**Note:** Output will feed into TASK-033 (DEC-001 forward-feeding pattern). Single combined document per DEC-001 D-005.

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Task created for redesigned workflow |
| 2026-01-26 | **DONE**    | Ishikawa & Pareto analysis complete. All 10 AC met. Output: docs/analysis/en006-ishikawa-pareto-analysis.md. 18 root causes identified, 15 features prioritized. Forward-feeding to TASK-033. |

---

*Task ID: TASK-032*
*Workflow ID: en006-ctxinj-20260126-001*
*Phase: 1 (Requirements & Analysis)*
*Frameworks: Ishikawa, Pareto*
