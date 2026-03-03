# {{ENABLER_ID}}: {{ENABLER_TITLE}}

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-01-23 (ps-architect-002)
PURPOSE: Technical/infrastructure work that enables future value delivery

DESCRIPTION:
  Technical/infrastructure work that enables future value delivery.
  SAFe concept for architectural runway, tech debt, etc.

EXTENDS: DeliveryItem -> WorkItem

NOTE: Enabler is SAFe's formal construct for non-feature work.
      ADO approximates via ValueArea. JIRA uses labeling.
      Trace: CROSS-DOMAIN-SYNTHESIS.md Section 6.1 (Recommendation 3)
-->

> **Type:** enabler
> **Status:** {{STATUS}}
> **Priority:** {{PRIORITY}}
> **Impact:** {{IMPACT}}
> **Enabler Type:** {{ENABLER_TYPE}}
> **Created:** {{CREATED_AT}}
> **Due:** {{DUE_DATE}}
> **Completed:** {{COMPLETED_AT}}
> **Parent:** {{PARENT_ID}}
> **Owner:** {{ASSIGNEE}}
> **Effort:** {{EFFORT}}

<!--
STATUS VALUES: pending | in_progress | completed
PRIORITY VALUES: critical | high | medium | low
IMPACT VALUES: critical | high | medium | low
ENABLER_TYPE VALUES: infrastructure | exploration | architecture | compliance
TIMESTAMPS: Use ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
EFFORT: Story points (1-13 Fibonacci recommended)
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Template Structure](#template-structure) | Visual structure reference for enabler |
| [Frontmatter](#frontmatter) | YAML metadata schema for enablers |
| [Summary](#summary) | Brief description and technical scope |
| [Enabler Type Classification](#enabler-type-classification) | Infrastructure, exploration, architecture, compliance |
| [Problem Statement](#problem-statement) | Why this enabler is needed |
| [Business Value](#business-value) | How enabler supports feature delivery |
| [Technical Approach](#technical-approach) | High-level technical approach |
| [Non-Functional Requirements (NFRs) Addressed](#non-functional-requirements-nfrs-addressed) | NFRs this enabler addresses |
| [Technical Debt Category](#technical-debt-category) | Tech debt being addressed |
| [Children (Tasks)](#children-tasks) | Task inventory and tracking |
| [Progress Summary](#progress-summary) | Overall enabler progress |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Implementation Plan](#implementation-plan) | Phased implementation approach |
| [Risks and Mitigations](#risks-and-mitigations) | Known risks and mitigations |
| [Dependencies](#dependencies) | Dependencies and items enabled |
| [State Machine Reference](#state-machine-reference) | Enabler status transitions |
| [Containment Rules](#containment-rules) | Parent/child constraints |
| [Invariants](#invariants) | Business rules and constraints |
| [Related Items](#related-items) | Hierarchy and related work |
| [Architecture Runway Impact](#architecture-runway-impact) | For architecture enablers |
| [History](#history) | Status changes and key events |
| [System Mapping](#system-mapping) | ADO, SAFe, JIRA mappings |

---

## Template Structure

```
+---------------------------------------------------------------------+
|                        ENABLER TEMPLATE                              |
|                    Version 1.0.0 (ONTOLOGY-aligned)                  |
+---------------------------------------------------------------------+
| Header Block (blockquote)                                            |
|   |-- type: "enabler"                          [REQUIRED]            |
|   |-- status: pending|in_progress|completed    [REQUIRED]            |
|   |-- priority: critical|high|medium|low       [REQUIRED]            |
|   |-- impact: critical|high|medium|low         [REQUIRED]            |
|   |-- enabler_type: infra|explore|arch|comply  [REQUIRED]            |
|   |-- created: ISO-8601                        [REQUIRED]            |
|   |-- due: ISO-8601                            [OPTIONAL]            |
|   |-- completed: ISO-8601                      [OPTIONAL]            |
|   |-- parent: {ID}                             [REQUIRED]            |
|   |-- owner: {USER}                            [OPTIONAL]            |
|   +-- effort: points                           [OPTIONAL]            |
+---------------------------------------------------------------------+
| Summary Section                                 [REQUIRED]           |
| Problem Statement                               [REQUIRED]           |
| Business Value                                  [REQUIRED]           |
| Technical Approach                              [REQUIRED]           |
| NFRs Addressed                                  [RECOMMENDED]        |
| Children (Tasks)                                [OPTIONAL]           |
| Progress Summary                                [REQUIRED]           |
| Acceptance Criteria                             [REQUIRED]           |
| Risks and Mitigations                           [RECOMMENDED]        |
| History                                         [RECOMMENDED]        |
+---------------------------------------------------------------------+

CONTAINMENT:
  allowed_parents: [Feature, Epic]
  allowed_children: [Task]
  max_depth: 1
```

---

## Frontmatter

```yaml
# =============================================================================
# ENABLER WORK ITEM
# Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler Entity Schema)
# =============================================================================

# Identity (inherited from WorkItem - Section 2.1)
id: "{{ENABLER_ID}}"                       # Required, immutable - Format: EN-NNN
work_type: ENABLER                         # Required, immutable - Discriminator
title: "{{ENABLER_TITLE}}"                 # Required, 1-500 chars

# Classification
classification: ENABLER                    # INV-EN02: classification should be ENABLER

# State (see State Machine below)
status: pending                            # Required - pending | in_progress | completed
resolution: null                           # Optional - Set when status is completed

# Priority & Impact
priority: medium                           # Required - critical | high | medium | low
impact: medium                             # Required - critical | high | medium | low

# People
assignee: "{{ASSIGNEE}}"                   # Optional - Engineer responsible
created_by: "{{CREATED_BY}}"               # Required, auto-populated

# Timestamps (auto-managed)
created_at: "{{CREATED_AT}}"               # Required, auto, immutable (ISO 8601)
updated_at: "{{UPDATED_AT}}"               # Required, auto (ISO 8601)
completed_at: null                         # Optional - When enabler completed (ISO 8601)

# Hierarchy
parent_id: "{{PARENT_ID}}"                 # Required - Feature or Epic ID

# Tags
tags:
  - enabler
  - "{{TAG_1}}"
  - "{{TAG_2}}"

# =============================================================================
# DELIVERY ITEM PROPERTIES (Section 3.3.2)
# =============================================================================
effort: null                               # Optional - Story points (0-100)
acceptance_criteria: null                  # Required before in_progress (INV-D02)
due_date: null                             # Optional - ISO 8601 date

# =============================================================================
# ENABLER-SPECIFIC PROPERTIES (Section 3.4.9)
# =============================================================================
enabler_type: {{ENABLER_TYPE}}             # REQUIRED: infrastructure | exploration | architecture | compliance
nfrs: []                                   # Optional - Non-functional requirements addressed (max: 20 items)
technical_debt_category: null              # Optional - Category of tech debt being addressed (max: 100 chars)
```

---

## Summary

<!--
REQUIRED: Brief 1-3 sentence description of the Enabler.
Should communicate the technical value being delivered.
-->

{{ENABLER_SUMMARY}}

**Technical Scope:**
- {{SCOPE_1}}
- {{SCOPE_2}}

---

## Enabler Type Classification

<!--
Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.specific.enabler_type)
-->

| Type | Description | Examples |
|------|-------------|----------|
| **INFRASTRUCTURE** | Platform, tooling, DevOps enablers | CI/CD pipelines, monitoring setup |
| **EXPLORATION** | Research and proof-of-concept work | Technology spikes, prototypes |
| **ARCHITECTURE** | Architectural runway and design work | Service decomposition, API design |
| **COMPLIANCE** | Security, regulatory, and compliance requirements | GDPR implementation, SOC2 controls |

**This Enabler Type:** {{ENABLER_TYPE}}

---

## Problem Statement

<!--
REQUIRED: Why is this enabler needed?
-->

{{PROBLEM_STATEMENT}}

---

## Business Value

<!--
REQUIRED: How does this enabler support future feature delivery?
-->

{{BUSINESS_VALUE}}

### Features Unlocked

- {{FEATURE_UNLOCKED_1}}
- {{FEATURE_UNLOCKED_2}}

---

## Technical Approach

<!--
REQUIRED: High-level technical approach
-->

{{TECHNICAL_APPROACH}}

### Architecture Diagram

```
{{ASCII_ARCHITECTURE_DIAGRAM}}
```

---

## Non-Functional Requirements (NFRs) Addressed

<!--
RECOMMENDED: NFRs this enabler addresses
Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.specific.nfrs)
-->

| NFR Category | Requirement | Current State | Target State |
|--------------|-------------|---------------|--------------|
| {{NFR_CAT_1}} | {{NFR_REQUIREMENT_1}} | {{CURRENT_1}} | {{TARGET_1}} |
| {{NFR_CAT_2}} | {{NFR_REQUIREMENT_2}} | {{CURRENT_2}} | {{TARGET_2}} |

---

## Technical Debt Category

<!--
OPTIONAL: For enablers addressing technical debt
Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.specific.technical_debt_category)
-->

**Category:** {{TECH_DEBT_CATEGORY}}

**Description:** {{TECH_DEBT_DESCRIPTION}}

**Impact if not addressed:** {{TECH_DEBT_IMPACT}}

---

## Children (Tasks)

<!--
OPTIONAL: Track child tasks.
Source: ONTOLOGY-v1.md Section 3.4.9 - containment
allowed_children: [Task]
max_depth: 1
-->

### Task Inventory

| ID | Title | Status | Effort | Owner |
|----|-------|--------|--------|-------|
| {{TASK_ID_1}} | {{TASK_TITLE_1}} | {{TASK_STATUS_1}} | {{TASK_EFFORT_1}} | {{TASK_OWNER_1}} |
| {{TASK_ID_2}} | {{TASK_TITLE_2}} | {{TASK_STATUS_2}} | {{TASK_EFFORT_2}} | {{TASK_OWNER_2}} |

---

## Progress Summary

<!--
REQUIRED: Track overall enabler progress.
Update regularly as tasks progress.
-->

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [##########..........] 50% (3/6 completed)            |
| Effort:    [########............] 40% (8/20 points completed)    |
+------------------------------------------------------------------+
| Overall:   [#########...........] 45%                            |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | {{TOTAL_TASKS}} |
| **Completed Tasks** | {{COMPLETED_TASKS}} |
| **Total Effort (points)** | {{TOTAL_EFFORT}} |
| **Completed Effort** | {{COMPLETED_EFFORT}} |
| **Completion %** | {{COMPLETION_PCT}}% |

---

## Acceptance Criteria

<!--
REQUIRED: Conditions for enabler to be considered complete.
Should be defined before status is in_progress (INV-D02).
-->

### Definition of Done

- [ ] {{CRITERION_1}}
- [ ] {{CRITERION_2}}
- [ ] {{CRITERION_3}}
- [ ] Documentation updated
- [ ] Monitoring/alerting in place (if applicable)

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | {{TECHNICAL_CRITERION_1}} | [ ] |
| TC-2 | {{TECHNICAL_CRITERION_2}} | [ ] |

---

## Evidence

<!--
COMPLETION EVIDENCE: Verification that this enabler meets technical requirements.
Include NFR measurements, performance benchmarks, and technical proof points.
This is audit trail evidence (proving work was done), not knowledge evidence (research citations).
-->

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| {{DELIVERABLE_1}} | Infrastructure | {{DESC_1}} | [{{LINK_TEXT_1}}]({{URL_1}}) |
| {{DELIVERABLE_2}} | Configuration | {{DESC_2}} | [{{LINK_TEXT_2}}]({{URL_2}}) |
| {{DELIVERABLE_3}} | Documentation | {{DESC_3}} | [{{LINK_TEXT_3}}]({{URL_3}}) |

### NFR Verification

<!--
For enablers addressing non-functional requirements, document measurements.
-->

| NFR | Target | Measured | Method | Date |
|-----|--------|----------|--------|------|
| {{NFR_1}} | {{TARGET_1}} | {{MEASURED_1}} | {{METHOD_1}} | {{DATE_1}} |
| {{NFR_2}} | {{TARGET_2}} | {{MEASURED_2}} | {{METHOD_2}} | {{DATE_2}} |

### Technical Verification

| Criterion | Verification Method | Evidence | Verified By | Date |
|-----------|---------------------|----------|-------------|------|
| {{CRITERION_1}} | {{METHOD_1}} | [{{EVIDENCE_LINK_1}}]({{URL_1}}) | {{VERIFIER_1}} | {{DATE_1}} |
| {{CRITERION_2}} | {{METHOD_2}} | [{{EVIDENCE_LINK_2}}]({{URL_2}}) | {{VERIFIER_2}} | {{DATE_2}} |

### Verification Checklist

- [ ] All acceptance criteria verified
- [ ] All tasks completed
- [ ] NFR targets met (see measurements above)
- [ ] Technical review complete
- [ ] Documentation updated

---

## Implementation Plan

<!--
RECOMMENDED: Phased implementation approach
-->

### Phase 1: {{PHASE_1_NAME}}

{{PHASE_1_DESCRIPTION}}

### Phase 2: {{PHASE_2_NAME}}

{{PHASE_2_DESCRIPTION}}

---

## Risks and Mitigations

<!--
RECOMMENDED: Known risks and mitigation strategies
-->

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {{RISK_1}} | {{LIKELIHOOD_1}} | {{IMPACT_1}} | {{MITIGATION_1}} |
| {{RISK_2}} | {{LIKELIHOOD_2}} | {{IMPACT_2}} | {{MITIGATION_2}} |

---

## Dependencies

<!--
RECOMMENDED: Dependencies and items this enabler unlocks
-->

### Depends On

- [{{DEPENDENCY_1}}]({{DEPENDENCY_1_LINK}})
- [{{DEPENDENCY_2}}]({{DEPENDENCY_2_LINK}})

### Enables

- [{{ENABLES_1}}]({{ENABLES_1_LINK}})
- [{{ENABLES_2}}]({{ENABLES_2_LINK}})

---

## State Machine Reference

<!--
Source: ONTOLOGY-v1.md Section 3.4.9 - state_machine
Simplified to match worktracker conventions.
-->

```
+-------------------------------------------------------------------+
|                   ENABLER STATE MACHINE                            |
+-------------------------------------------------------------------+
|                                                                    |
|   +---------+     +-------------+     +-----------+               |
|   | PENDING |---->| IN_PROGRESS |---->| COMPLETED |               |
|   +---------+     +-------------+     +-----------+               |
|        |               |                   |                       |
|        v               v                   v                       |
|   (Planning)     (Implementing)      (Delivered)                  |
|                                                                    |
+-------------------------------------------------------------------+

Allowed Transitions:
- pending -> in_progress: Start implementation
- in_progress -> completed: All tasks done
- in_progress -> pending: Deprioritized
- completed -> in_progress: Reopened
```

---

## Containment Rules

<!--
Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.containment)
-->

| Rule | Value |
|------|-------|
| **Allowed Children** | Task |
| **Allowed Parents** | Feature, Epic |
| **Max Depth** | 1 |

### Hierarchy Diagram

```
FEAT-001: {{FEATURE_TITLE}}
|
+-- EN-001: {{ENABLER_TITLE}} (this enabler)
    |
    +-- TASK-001: Task
    +-- TASK-002: Task
```

---

## Invariants

<!--
Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.invariants)
-->

- **INV-D01:** effort must be non-negative (inherited from DeliveryItem)
- **INV-D02:** acceptance_criteria should be defined before in_progress (inherited)
- **INV-EN01:** enabler_type is REQUIRED
- **INV-EN02:** classification should be ENABLER
- **INV-EN03:** Enabler can have Feature or Epic as parent

---

## Related Items

<!--
RECOMMENDED: Link to related work items and artifacts.
-->

### Hierarchy

- **Parent:** [{{PARENT_TITLE}}]({{PARENT_LINK}})

### Related Items

- **Related Feature:** [{{RELATED_FEATURE}}]({{RELATED_FEATURE_LINK}})
- **Related Spike:** [{{RELATED_SPIKE}}]({{RELATED_SPIKE_LINK}})

---

## Architecture Runway Impact

<!--
OPTIONAL: For ARCHITECTURE type enablers
-->

**Current Runway:** {{CURRENT_RUNWAY}}

**Post-Enabler Runway:** {{POST_ENABLER_RUNWAY}}

---

## History

<!--
RECOMMENDED: Track status changes and key events.
Use ISO 8601 timestamps.
-->

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| {{CREATED_AT}} | {{CREATED_BY}} | pending | Enabler defined |
| {{DATE_2}} | {{AUTHOR_2}} | in_progress | Implementation started |
| {{DATE_3}} | {{AUTHOR_3}} | completed | Enabler complete |

---

## System Mapping

<!--
Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.system_mapping)
-->

| System | Mapping |
|--------|---------|
| **Azure DevOps** | PBI with ValueArea=Architectural |
| **SAFe** | Enabler (all types) |
| **JIRA** | Story with 'enabler' label |

---

## Compaction Resilience (T-004)

| Constraint | Failure Mode if Lost | Compensating Control | Detection |
|-----------|---------------------|---------------------|-----------|
| INV-EN01: enabler_type is REQUIRED | Enabler created without type classification | L3 AST validation (H-33) | `jerry ast validate` rejects missing enabler_type |
| INV-EN02: classification should be ENABLER | Classification set to BUSINESS instead | /worktracker skill enforcement | Worktracker audit detects classification mismatch |
| INV-EN03: Parent must be Feature or Epic | Enabler placed under wrong parent type | /worktracker skill enforcement (WTI rules) | Worktracker audit detects containment violation |
| INV-D02: acceptance_criteria before in_progress | Enabler started without defined AC | /worktracker skill enforcement | Manual review at status transition |

<!--
DESIGN RATIONALE:
Enabler is SAFe's formal construct for non-feature work.
ADO approximates via ValueArea. JIRA uses labeling.
Modeled as first-class for SAFe compatibility.
Trace: CROSS-DOMAIN-SYNTHESIS.md Section 6.1 (Recommendation 3)

PATTERN COMPLIANCE:
- P-001: Blockquote Header [COMPLIANT]
- P-002: Summary Section [COMPLIANT]
- P-005: History/Changelog [COMPLIANT]
- P-006: ISO 8601 Timestamps [COMPLIANT]
- P-007: Horizontal Rule Separators [COMPLIANT]
- P-019: Parent Reference [COMPLIANT]
- Children Tracking Section [COMPLIANT]
- Progress Summary Section [COMPLIANT]

WORKTRACKER ALIGNMENT:
- Status values: pending, in_progress, completed (per work-items.md)
- Priority/Impact: critical, high, medium, low (per work-items.md)
-->
