# {{TITLE}}

<!--
TEMPLATE: Enabler (DRAFT)
SOURCE: ONTOLOGY-v1.md Section 3.4.9
VERSION: 0.1.0
STATUS: DRAFT - Pending review

DESCRIPTION:
  Technical/infrastructure work that enables future value delivery.
  SAFe concept for architectural runway, tech debt, etc.

EXTENDS: DeliveryItem -> WorkItem

NOTE: Enabler is SAFe's formal construct for non-feature work.
      ADO approximates via ValueArea. JIRA uses labeling.
      Trace: CROSS-DOMAIN-SYNTHESIS.md Section 6.1 (Recommendation 3)
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
id: "{{ID}}"                           # Format: PREFIX-NNN (e.g., EN-001)
work_type: ENABLER                     # Immutable discriminator

# === CORE METADATA ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
title: "{{TITLE}}"                     # Required, 1-500 chars
description: |
  {{DESCRIPTION}}

# === CLASSIFICATION ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
classification: ENABLER                # INV-EN02: classification should be ENABLER

# === LIFECYCLE STATE ===
# Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.state_machine)
status: BACKLOG                        # See State Machine below
resolution: null                       # Set when status is DONE or REMOVED

# === PRIORITY ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
priority: MEDIUM                       # CRITICAL | HIGH | MEDIUM | LOW

# === PEOPLE ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
assignee: "{{ASSIGNEE}}"               # Engineer responsible
created_by: "{{CREATED_BY}}"           # Auto-set on creation

# === TIMESTAMPS (Auto-managed) ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
created_at: "{{CREATED_AT}}"           # ISO 8601 datetime
updated_at: "{{UPDATED_AT}}"           # ISO 8601 datetime

# === HIERARCHY ===
# Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.containment)
parent_id: "{{PARENT_ID}}"             # Feature or Epic ID

# === TAGS ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
tags:
  - enabler
  - "{{TAG_1}}"
  - "{{TAG_2}}"

# === DELIVERY ITEM PROPERTIES ===
# Source: ONTOLOGY-v1.md Section 3.3.2 (DeliveryItem)
effort: null                           # Story points or effort estimate (0-100)
acceptance_criteria: |
  {{ACCEPTANCE_CRITERIA}}
due_date: null                         # ISO 8601 date

# === ENABLER-SPECIFIC PROPERTIES ===
# Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.specific)
enabler_type: {{ENABLER_TYPE}}         # REQUIRED: INFRASTRUCTURE | EXPLORATION | ARCHITECTURE | COMPLIANCE
nfrs:                                  # Non-functional requirements addressed (max: 20 items)
  - "{{NFR_1}}"
  - "{{NFR_2}}"
technical_debt_category: "{{TECH_DEBT_CATEGORY}}"  # Category of tech debt being addressed (max: 100 chars)
```

---

## State Machine

<!-- Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.state_machine) -->

**Initial State:** `BACKLOG`

**Valid States:** `BACKLOG`, `READY`, `IN_PROGRESS`, `BLOCKED`, `IN_REVIEW`, `DONE`, `REMOVED`

```
              +-----------+
              |  BACKLOG  |
              +-----+-----+
                    |
          +---------+---------+
          |                   |
          v                   v
      +-------+          +---------+
      | READY |          | REMOVED |
      +---+---+          +---------+
          |
    +-----+-----+
    |           |
    v           v
+------------+ +---------+
| IN_PROGRESS| | BACKLOG |
+-----+------+ +---------+
      |
  +---+---+---+
  |   |   |   |
  v   v   v   v
+---+ +---+ +---+ +---+
|BLK| |REV| |DON| |REM|
+---+ +---+ +---+ +---+
  |     |     |
  v     v     v
+------------+
| IN_PROGRESS| (Reopen/Continue)
+------------+

Legend: BLK=BLOCKED, REV=IN_REVIEW, DON=DONE, REM=REMOVED
```

| From State    | Allowed Transitions                              |
|---------------|--------------------------------------------------|
| BACKLOG       | READY, REMOVED                                   |
| READY         | IN_PROGRESS, BACKLOG, REMOVED                    |
| IN_PROGRESS   | BLOCKED, IN_REVIEW, DONE, REMOVED                |
| BLOCKED       | IN_PROGRESS, REMOVED                             |
| IN_REVIEW     | DONE, IN_PROGRESS                                |
| DONE          | IN_PROGRESS (Reopen)                             |
| REMOVED       | (Terminal - no transitions)                      |

---

## Containment Rules

<!-- Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.containment) -->

| Rule             | Value                           |
|------------------|---------------------------------|
| Allowed Children | Task                            |
| Allowed Parents  | Feature, Epic                   |
| Max Depth        | 1                               |

---

## Invariants

<!-- Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.invariants) -->

- **INV-D01:** effort must be non-negative (inherited from DeliveryItem)
- **INV-D02:** acceptance_criteria should be defined before IN_PROGRESS (inherited)
- **INV-EN01:** enabler_type is REQUIRED
- **INV-EN02:** classification should be ENABLER
- **INV-EN03:** Enabler can have Feature or Epic as parent

---

## System Mapping

<!-- Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.system_mapping) -->

| System | Mapping                                |
|--------|----------------------------------------|
| ADO    | PBI with ValueArea=Architectural       |
| SAFe   | Enabler (all types)                    |
| JIRA   | Story with 'enabler' label             |

---

## Enabler Types

<!-- Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.specific.enabler_type) -->

| Type           | Description                                              | Examples                          |
|----------------|----------------------------------------------------------|-----------------------------------|
| INFRASTRUCTURE | Platform, tooling, DevOps enablers                       | CI/CD pipelines, monitoring setup |
| EXPLORATION    | Research and proof-of-concept work                       | Technology spikes, prototypes     |
| ARCHITECTURE   | Architectural runway and design work                     | Service decomposition, API design |
| COMPLIANCE     | Security, regulatory, and compliance requirements        | GDPR implementation, SOC2 controls|

---

## Content

### Problem Statement

<!-- Why is this enabler needed? -->

{{PROBLEM_STATEMENT}}

### Business Value

<!-- How does this enabler support future feature delivery? -->

{{BUSINESS_VALUE}}

### Technical Approach

<!-- High-level technical approach -->

{{TECHNICAL_APPROACH}}

### Non-Functional Requirements (NFRs) Addressed

<!-- Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.specific.nfrs) -->

| NFR Category    | Requirement                          | Current State | Target State |
|-----------------|--------------------------------------|---------------|--------------|
| {{NFR_CAT_1}}   | {{NFR_REQUIREMENT_1}}                | {{CURRENT_1}} | {{TARGET_1}} |
| {{NFR_CAT_2}}   | {{NFR_REQUIREMENT_2}}                | {{CURRENT_2}} | {{TARGET_2}} |

### Technical Debt Category

<!-- Source: ONTOLOGY-v1.md Section 3.4.9 (Enabler.specific.technical_debt_category) -->

**Category:** {{TECH_DEBT_CATEGORY}}

**Description:** {{TECH_DEBT_DESCRIPTION}}

**Impact if not addressed:** {{TECH_DEBT_IMPACT}}

---

## Acceptance Criteria

- [ ] {{CRITERION_1}}
- [ ] {{CRITERION_2}}
- [ ] {{CRITERION_3}}
- [ ] Documentation updated
- [ ] Monitoring/alerting in place (if applicable)

---

## Implementation Plan

### Phase 1: {{PHASE_1_NAME}}

{{PHASE_1_DESCRIPTION}}

### Phase 2: {{PHASE_2_NAME}}

{{PHASE_2_DESCRIPTION}}

### Tasks

<!-- Child tasks to be created -->

| Task ID | Title                        | Estimate |
|---------|------------------------------|----------|
| {{ID}}  | {{TASK_TITLE}}               | {{EST}}  |

---

## Risks and Mitigations

| Risk                    | Likelihood | Impact | Mitigation                       |
|-------------------------|------------|--------|----------------------------------|
| {{RISK_1}}              | {{LIKE_1}} | {{IMP_1}} | {{MIT_1}}                     |
| {{RISK_2}}              | {{LIKE_2}} | {{IMP_2}} | {{MIT_2}}                     |

---

## Dependencies

### Depends On

- [{{DEPENDENCY_1}}]({{DEPENDENCY_1_LINK}})
- [{{DEPENDENCY_2}}]({{DEPENDENCY_2_LINK}})

### Enables

<!-- What features/capabilities does this enabler unlock? -->

- [{{ENABLES_1}}]({{ENABLES_1_LINK}})
- [{{ENABLES_2}}]({{ENABLES_2_LINK}})

---

## Related Items

- Parent: [{{PARENT_TITLE}}]({{PARENT_LINK}})
- Related Feature: [{{RELATED_FEATURE}}]({{RELATED_FEATURE_LINK}})
- Related Spike: [{{RELATED_SPIKE}}]({{RELATED_SPIKE_LINK}})

---

## Architecture Runway Impact

<!-- For ARCHITECTURE type enablers -->

**Current Runway:** {{CURRENT_RUNWAY}}

**Post-Enabler Runway:** {{POST_ENABLER_RUNWAY}}

**Features Unlocked:**
- {{FEATURE_UNLOCKED_1}}
- {{FEATURE_UNLOCKED_2}}

---

## History

| Date       | Status       | Notes                          |
|------------|--------------|--------------------------------|
| {{DATE}}   | Created      | Enabler defined                |
| {{DATE}}   | READY        | Ready for sprint               |
| {{DATE}}   | IN_PROGRESS  | Implementation started         |
| {{DATE}}   | IN_REVIEW    | Ready for technical review     |
| {{DATE}}   | DONE         | Enabler complete               |

---

<!--
JERRY ALIGNMENT:
  existing_type: "None"
  changes_needed: "Add ENABLER to WorkType enum"

DESIGN RATIONALE:
  Enabler is SAFe's formal construct for non-feature work.
  ADO approximates via ValueArea. JIRA uses labeling.
  Modeled as first-class for SAFe compatibility.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 6.1 (Recommendation 3)
-->
